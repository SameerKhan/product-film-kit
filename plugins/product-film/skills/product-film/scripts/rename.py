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

root, mp = os.path.realpath(sys.argv[1]), json.load(open(sys.argv[2])); apply = '--apply' in sys.argv
# "scratch only" is enforced, not hoped for: refuse a git checkout (or anything inside one) and your home folder itself
d = root
while True:
    if os.path.exists(os.path.join(d, '.git')): sys.exit(f'refusing: {d} is a git checkout; run on a scratch copy (git archive | tar -x)')
    if os.path.dirname(d) == d: break
    d = os.path.dirname(d)
if root in (os.path.expanduser('~'), '/'): sys.exit('refusing: point at a scratch folder, not your home folder')
skipped = []
OLD = re.compile(mp['residual_regex'], re.I); counts = {a: 0 for a, _ in mp['map']}; files = residual = 0
for d, dirs, fs in os.walk(root):  # does not follow directory symlinks
    dirs[:] = [x for x in dirs if x not in ('node_modules', '.git')]
    for f in fs:
        p = os.path.join(d, f)
        st = os.lstat(p)
        if os.path.islink(p) or st.st_nlink > 1: skipped.append(os.path.relpath(p, root)); continue   # never write through links
        try: s = open(p, encoding='utf-8').read()
        except UnicodeDecodeError: continue   # binary files
        except OSError: skipped.append(os.path.relpath(p, root)); continue
        if not OLD.search(s): continue
        files += 1; n = s
        for a, b in mp['map']: counts[a] += n.count(a); n = n.replace(a, b)
        if apply and n != s:
            tmp = p + '.rename-tmp'
            with open(tmp, 'w', encoding='utf-8') as fh: fh.write(n)
            os.chmod(tmp, st.st_mode & 0o7777); os.replace(tmp, p)   # atomic: an interrupted run never leaves half a file
        left = OLD.findall(n)
        if left: residual += len(left); print('RESIDUAL', os.path.relpath(p, root), len(left))
print(json.dumps({'files': files, 'replacements': sum(counts.values()), 'residual': residual,
                  'skipped_links_or_unreadable': skipped[:20], 'by_pattern': {k: v for k, v in counts.items() if v}}, indent=1))
sys.exit(1 if residual or skipped else 0)   # a skipped file was not scanned, so "zero residual" would be unproven
