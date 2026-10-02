#!/usr/bin/env python3
"""Deterministic rename of demo names inside a SCRATCH source copy (never a real checkout).

Usage: rename.py <src_dir> <rename-map.json> [--apply]
rename-map.json: {"residual_regex": "old[\\W_]{0,7}(and|n)?[\\W_]{0,7}brand",
                  "map": [["Old & Brand", "New Name"], ["oldbrand", "newname"], ...]}
List the longest / most specific variants first. Prints per-pattern counts; with --apply writes
files, then reports any residual match. Exit 1 on residuals. Re-scan the built bundle and the
generated demo data too; then OCR the footage (scripts/ocr_gate.py "forbid").
"""
import json, os, re, sys

root, mp = sys.argv[1], json.load(open(sys.argv[2])); apply = '--apply' in sys.argv
OLD = re.compile(mp['residual_regex'], re.I); counts = {a: 0 for a, _ in mp['map']}; files = residual = 0
for d, dirs, fs in os.walk(root):
    dirs[:] = [x for x in dirs if x not in ('node_modules', '.git')]
    for f in fs:
        p = os.path.join(d, f)
        try: s = open(p, encoding='utf-8').read()
        except (UnicodeDecodeError, OSError): continue
        if not OLD.search(s): continue
        files += 1; n = s
        for a, b in mp['map']: counts[a] += n.count(a); n = n.replace(a, b)
        if apply and n != s: open(p, 'w', encoding='utf-8').write(n)
        left = OLD.findall(n)
        if left: residual += len(left); print('RESIDUAL', os.path.relpath(p, root), len(left))
print(json.dumps({'files': files, 'replacements': sum(counts.values()), 'residual': residual,
                  'by_pattern': {k: v for k, v in counts.items() if v}}, indent=1))
sys.exit(1 if residual else 0)
