#!/usr/bin/env bash
# Repository invariants. Run locally before a release; CI runs it on every push.
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0
err() { echo "FAIL: $*"; fail=1; }

PLUGIN=plugins/product-film/.claude-plugin/plugin.json
SKILLS=plugins/product-film/skills

# 0. No symlinks: every later check reads files, and a link could point outside the checkout.
links=$(find . -type l -not -path './.git/*')
[ -z "$links" ] || { echo "$links"; err "symlink in repo"; }

# 1. Every JSON file is valid.
while IFS= read -r f; do python3 -m json.tool "$f" >/dev/null 2>&1 || err "invalid JSON: $f"; done \
  < <(find . -name '*.json' -not -path './.git/*')

# 2. Skill frontmatter names match their directories and appear in README + manifests.
for dir in "$SKILLS"/*/; do
  skill=$(basename "$dir")
  name=$(sed -n 's/^name: *//p' "$dir/SKILL.md" | head -1)
  [ "$name" = "$skill" ] || err "$skill/SKILL.md frontmatter name is '$name'"
  grep -q "/$skill" README.md || err "README does not mention /$skill"
  grep -q "/$skill" "$PLUGIN" || err "plugin.json description omits /$skill"
  grep -q "/$skill" .claude-plugin/marketplace.json || err "marketplace.json description omits /$skill"
  # every file the SKILL.md index names exists
  for ref in $(grep -oE '`(references|scripts|examples)/[A-Za-z0-9_./-]+`' "$dir/SKILL.md" | tr -d '`' | sort -u); do
    [ -e "$dir/$ref" ] || err "$skill/SKILL.md names missing file $ref"
  done
done

# 3. The plugin version is the newest CHANGELOG entry.
version=$(python3 -c "import json;print(json.load(open('$PLUGIN'))['version'])")
top=$(sed -n 's/^## \([0-9][0-9.]*\) .*/\1/p' CHANGELOG.md | head -1)
[ "$version" = "$top" ] || err "plugin.json is $version but the newest CHANGELOG entry is $top"

# 4. Scripts parse.
for f in "$SKILLS"/*/scripts/*.py; do   # parse only: py_compile would leave __pycache__ behind
  python3 -c 'import ast,sys; ast.parse(open(sys.argv[1]).read(), sys.argv[1])' "$f" || err "python: $f"; done
for f in "$SKILLS"/*/scripts/*.sh scripts/*.sh; do bash -n "$f" || err "bash: $f"; done
if command -v node >/dev/null; then
  for f in "$SKILLS"/*/scripts/capture/*.mjs; do node --check "$f" || err "node: $f"; done
fi

# 5. The reading-rule example passes (the script and the docs agree).
python3 "$SKILLS"/product-film/scripts/reading_rule.py "$SKILLS"/product-film/examples/nodes.example.json >/dev/null || err "reading rule example fails"

# 6. No em-dashes in published text (house style).
python3 - <<'PY' || err "em-dash found"
import pathlib, sys
files = [f for f in sorted(pathlib.Path(".").rglob("*")) if f.is_file() and ".git" not in f.parts
         and f.suffix in {".md", ".sh", ".json", ".yml", ".yaml", ".py", ".mjs", ".swift"}]
hits = [f"{f}:{n}" for f in files for n, l in enumerate(f.read_text(encoding="utf-8").splitlines(), 1) if chr(0x2014) in l]
if hits: print("\n".join(hits[:5]))
sys.exit(1 if hits else 0)
PY

# 7. No private paths or secrets leak into a public repo.
#    Prints file:line only, never the matching text, so a real secret does not land in CI logs.
bad=$(grep -rlInE '/Users/|/home/[a-z]|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[abpr]-[A-Za-z0-9-]{10,}|npm_[A-Za-z0-9]{30,}|[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.com' \
  --exclude-dir=.git --exclude=check.sh . || true)
[ -z "$bad" ] || { echo "$bad"; err "private path, personal email or secret-looking string in the files above"; }

if [ "$fail" -ne 0 ]; then exit 1; fi
echo "all checks passed"
