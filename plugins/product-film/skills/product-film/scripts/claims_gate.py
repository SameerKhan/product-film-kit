#!/usr/bin/env python3
"""Claims gate: every visible string in the composition is sourced, every required item is present,
exact lists match the page, and forbidden strings never appear.

Usage: claims_gate.py composition.html copy.txt claims.json   (see examples/claims.example.json)

copy.txt     the landing page's visible copy (the only claim source)
claims.json  {"approved": {"<exact text>": "<who approved, when>"},   # owner-approved short lines + system strings
              "required": ["<exact text>", ...],                      # claims, caveats, CTAs that must appear
              "forbidden": ["<text>", ...],                           # never on screen (case-insensitive)
              "exact_lists": [{"name": "publish grid", "regex": "plat-([a-z-]+)\\\\.", "within": "<regex for the block>",
                               "expected": ["facebook", ...]}]}
A text node passes if it is approved, or (minus a trailing full stop) appears verbatim in copy.txt.
Exit 1 on any failure.
"""
import html, json, re, sys

doc, copy_txt, cfg = open(sys.argv[1]).read(), open(sys.argv[2]).read(), json.load(open(sys.argv[3]))
body = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>|<!--[\s\S]*?-->', '', doc)
texts = [re.sub(r'\s+', ' ', html.unescape(x)).strip() for x in re.findall(r'>([^<>]+)<', body)]
texts = [x for x in texts if x]
page = re.sub(r'\s+', ' ', copy_txt).lower()
approved = cfg.get('approved', {})
res = {
    'unsourced': sorted({x for x in texts if x not in approved and x.rstrip('.').lower() not in page}),
    # phrase spans split one line into several text nodes, so required items are matched on the joined text
    'missing_required': [r for r in cfg.get('required', []) if r not in texts and r not in ' '.join(texts)],
    'forbidden_found': [f for f in cfg.get('forbidden', []) if f.lower() in ' '.join(texts).lower()],
    'lists': {},
}
for L in cfg.get('exact_lists', []):
    scope = re.search(L['within'], body, re.S) if L.get('within') else None
    hay = scope.group(0) if scope else ('' if L.get('within') else body)
    got = re.findall(L['regex'], hay)
    res['lists'][L['name']] = {'ok': sorted(got) == sorted(L['expected']), 'got': got,
                               'extra': sorted(set(got) - set(L['expected'])), 'missing': sorted(set(L['expected']) - set(got))}
fail = res['unsourced'] or res['missing_required'] or res['forbidden_found'] or any(not v['ok'] for v in res['lists'].values())
print(json.dumps(res, indent=1)); print('CLAIMS GATE', 'FAIL' if fail else 'PASS')
sys.exit(1 if fail else 0)
