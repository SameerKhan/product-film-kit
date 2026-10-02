#!/bin/bash
# fetch.sh <sources.json> <out_dir>: quarantined asset fetch (music, SFX, logos).
# https only, host allowlist, no cross-host redirects, content-type + size checks, sha256 ledger.
# sources.json: {"hosts": ["assets.example.com"], "sources": [{"id": "music-x", "url": "https://...", "kind": "audio/mpeg", "max": 20000000}]}
set -euo pipefail
SRC="$1"; Q="$2"; mkdir -p "$Q"; LEDGER="$Q/fetch-ledger.tsv"; : > "$LEDGER"
host_of() { python3 -c "import sys,urllib.parse;print(urllib.parse.urlparse(sys.argv[1]).hostname)" "$1"; }
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));[print(s["id"],s["url"],s["kind"],s["max"]) for s in d["sources"]]' "$SRC" |
while read -r id url kind max; do
  case "$url" in https://*) ;; *) echo "REJECT non-https $id"; exit 1;; esac
  host=$(host_of "$url")
  python3 -c 'import json,sys;sys.exit(0 if sys.argv[2] in json.load(open(sys.argv[1]))["hosts"] else 1)' "$SRC" "$host" || { echo "REJECT host $host"; exit 1; }
  ext="${url##*.}"; case "$kind" in text/html) ext=html;; esac; out="$Q/$id.$ext"
  final=$(curl -sS -A 'Mozilla/5.0' --proto =https -L --max-redirs 3 --max-filesize "$max" -o "$out" -w '%{url_effective} %{content_type}' "$url")
  [ "$(host_of "${final%% *}")" = "$host" ] || { echo "REJECT cross-host redirect $id"; rm -f "$out"; exit 1; }
  ctype="${final#* }"
  echo "$ctype" | grep -qi "${kind%%;*}" || { echo "REJECT type $id: $ctype"; rm -f "$out"; exit 1; }
  printf '%s\t%s\t%s\t%s\t%s\n' "$(basename "$out")" "$(shasum -a 256 "$out" | cut -d' ' -f1)" "$(wc -c < "$out" | tr -d ' ')" "$ctype" "$url" >> "$LEDGER"
done
echo "fetched $(wc -l < "$LEDGER" | tr -d ' ') files into $Q (recorded $(date -u +%FT%TZ)); save the licence page next to them"
