#!/bin/bash
# render.sh <composition_dir> <name> [timeout_s]: render a HyperFrames composition into a staging dir,
# promote it atomically to <composition_dir>/renders/, and kill the renderer's whole process tree on
# failure, timeout or signal. Exit 0 = rendered, 1 = render failed, 124 = timed out, 130 = interrupted.
# Env: HYPERFRAMES_VERSION (required: pin it), MIN_FREE_GB (default 5), FPS (default 30).
set -uo pipefail
DIR="$1"; NAME="$2"; LIMIT="${3:-600}"
VER="${HYPERFRAMES_VERSION:-}"
[[ "$VER" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "set HYPERFRAMES_VERSION to an exact version (e.g. 0.8.106), not a tag or range"; exit 1; }
[[ "$NAME" =~ ^[A-Za-z0-9._-]+$ ]] || { echo "name must be letters, digits, dot, dash or underscore"; exit 1; }
cd "$DIR" || exit 1
export HYPERFRAMES_TELEMETRY_DISABLED=1 DO_NOT_TRACK=1
# a dedicated npm cache and an empty user config: no shared ~/.npm, no registry tokens from ~/.npmrc
export npm_config_cache="${NPM_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/product-film/npm}" npm_config_userconfig=/dev/null
[ -L renders ] && { echo "renders/ is a symlink; refusing"; exit 1; }
FREE=$(df -k . | awk 'NR==2{print int($4/1048576)}')
[ "$FREE" -gt "${MIN_FREE_GB:-5}" ] || { echo "STOP: ${FREE} GB free; free space first"; exit 1; }
STAGE=$(mktemp -d "$PWD/.staging.XXXX") || exit 1
mkdir -p renders; DEST="renders/$(date +%Y%m%d-%H%M%S)-$NAME.mp4"; PID=""

tree() { local p; for p in $(pgrep -P "$1" 2>/dev/null); do tree "$p"; done; echo "$1"; }  # children first
killtree() {
  [ -n "$PID" ] || return 0
  local pids; pids=$(tree "$PID")
  kill -TERM $pids 2>/dev/null; sleep 1; kill -KILL $pids 2>/dev/null
  wait "$PID" 2>/dev/null
  for p in $pids; do kill -0 "$p" 2>/dev/null && { echo "WARNING: process $p survived cleanup"; return 1; }; done
  return 0
}
cleanup() { killtree; rm -rf "$STAGE"; }
trap 'cleanup; exit 130' INT TERM
trap 'rm -rf "$STAGE"' EXIT

npx -y "hyperframes@$VER" render -f "${FPS:-30}" -o "$STAGE/out.mp4" > "$STAGE/log.txt" 2>&1 &
PID=$!
start=$SECONDS
while kill -0 "$PID" 2>/dev/null; do
  if [ $((SECONDS - start)) -ge "$LIMIT" ]; then
    echo "render timed out after ${LIMIT}s"; tail -3 "$STAGE/log.txt"; killtree; exit 124
  fi
  sleep 1
done
rc=0; wait "$PID" || rc=$?; PID=""
if [ "$rc" -eq 0 ] && [ -s "$STAGE/out.mp4" ]; then
  [ -e "$DEST" ] && { echo "$DEST exists; refusing to overwrite"; exit 1; }
  mv "$STAGE/out.mp4" "$DEST" || { echo "could not move the render into renders/"; exit 1; }; echo "$DEST"; exit 0
fi
echo "render failed (exit $rc)"; tail -3 "$STAGE/log.txt"; exit 1
