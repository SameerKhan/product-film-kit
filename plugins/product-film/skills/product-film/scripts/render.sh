#!/bin/bash
# render.sh <composition_dir> <name> [timeout_s]: render a HyperFrames composition into a staging dir,
# promote it atomically to <composition_dir>/renders/, and kill the whole process group on failure or timeout.
# Env: HYPERFRAMES_VERSION (pin it), MIN_FREE_GB (default 5), FPS (default 30).
set -euo pipefail
DIR="$1"; NAME="$2"; LIMIT="${3:-600}"; VER="${HYPERFRAMES_VERSION:?pin a version, e.g. HYPERFRAMES_VERSION=0.8.106}"
cd "$DIR"
export npm_config_offline="${npm_config_offline:-false}" HYPERFRAMES_TELEMETRY_DISABLED=1 DO_NOT_TRACK=1
FREE=$(df -k . | awk 'NR==2{print int($4/1048576)}'); [ "$FREE" -gt "${MIN_FREE_GB:-5}" ] || { echo "STOP: ${FREE} GB free; free space first"; exit 1; }
STAGE=$(mktemp -d "$PWD/.staging.XXXX"); DEST="renders/$(date +%Y%m%d-%H%M%S)-$NAME.mp4"; mkdir -p renders
set -m
npx -y "hyperframes@$VER" render -f "${FPS:-30}" -o "$STAGE/out.mp4" > "$STAGE/log.txt" 2>&1 &
PID=$!; PGID=$(ps -o pgid= -p $PID | tr -d ' ')
cleanup() { kill -TERM -- -"$PGID" 2>/dev/null || true; sleep 1; kill -KILL -- -"$PGID" 2>/dev/null || true; rm -rf "$STAGE"; }
trap 'cleanup; exit 130' INT TERM
( sleep "$LIMIT"; kill -TERM -- -"$PGID" 2>/dev/null ) & WD=$!
if wait $PID; then kill $WD 2>/dev/null || true; mv "$STAGE/out.mp4" "$DEST"; rm -rf "$STAGE"; echo "$DEST"
else kill $WD 2>/dev/null || true; echo "render failed or timed out (limit ${LIMIT}s)"; tail -3 "$STAGE/log.txt"; cleanup; exit 1; fi
