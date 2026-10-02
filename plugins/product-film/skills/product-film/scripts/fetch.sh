#!/bin/bash
# fetch.sh <sources.json> <out_dir>: quarantined asset fetch (music, SFX, logos).
# https only, host allowlist, no cross-host redirects, content-type + size checks, sha256 ledger.
# sources.json: {"hosts": ["assets.example.com"], "sources": [{"id": "music-x", "url": "https://...", "kind": "audio/mpeg", "max": 20000000}]}
set -euo pipefail
SRC="$1"; Q="$2"; mkdir -p "$Q"; LEDGER="$Q/fetch-ledger.tsv"; NEW=$(mktemp "$Q/.ledger.XXXXXX"); trap 'rm -f "$NEW"' EXIT
host_of() { python3 -c "import sys,urllib.parse;print(urllib.parse.urlparse(sys.argv[1]).hostname)" "$1"; }
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));[print("\t".join([s["id"],s["url"],s["kind"],str(int(s["max"]))])) for s in d["sources"]]' "$SRC" |
while IFS=$'\t' read -r id url kind max; do
  # ids become file names: letters, digits, dot, dash, underscore only (no ../, no slashes)
  [[ "$id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { echo "REJECT unsafe id: $id"; exit 1; }
  case "$url" in https://*) ;; *) echo "REJECT non-https $id"; exit 1;; esac
  host=$(host_of "$url")
  python3 -c 'import json,sys;sys.exit(0 if sys.argv[2] in json.load(open(sys.argv[1]))["hosts"] else 1)' "$SRC" "$host" || { echo "REJECT host $host"; exit 1; }
  ext="${url##*.}"; ext="${ext%%[?#]*}"; case "$kind" in text/html) ext=html;; esac
  [[ "$ext" =~ ^[A-Za-z0-9]{1,8}$ ]] || ext=bin
  out="$Q/$id.$ext"; part="$out.part"
  # redirects are NOT followed: a followed redirect fetches from the new host before any check can run
  # -q first: ignore ~/.curlrc (proxies, headers, netrc); downloads land in .part and replace the old file only on success
  res=$(curl -q -sS -A 'Mozilla/5.0' --proto =https --connect-timeout 15 --max-time 300 --max-filesize "$max" \
        -o "$part" -w '%{http_code} %{content_type}' "$url") || { echo "REJECT $id: curl failed"; rm -f "$part"; exit 1; }
  code="${res%% *}"; ctype="${res#* }"
  [ "$code" = 200 ] || { echo "REJECT $id: HTTP $code (redirects are not followed; use the final URL)"; rm -f "$part"; exit 1; }
  echo "$ctype" | grep -qi "${kind%%;*}" || { echo "REJECT type $id: $ctype"; rm -f "$part"; exit 1; }
  mv -f "$part" "$out"
  printf '%s\t%s\t%s\t%s\t%s\n' "$(basename "$out")" "$(shasum -a 256 "$out" | cut -d' ' -f1)" "$(wc -c < "$out" | tr -d ' ')" "$ctype" "$url" >> "$NEW"
done
mv -f "$NEW" "$LEDGER"   # the old ledger is replaced only when every source passed
echo "fetched $(wc -l < "$LEDGER" | tr -d ' ') files into $Q (recorded $(date -u +%FT%TZ)); save the licence page next to them"
