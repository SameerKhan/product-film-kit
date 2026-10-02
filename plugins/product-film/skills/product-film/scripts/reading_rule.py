#!/usr/bin/env python3
"""Reading rule R: every text node is on screen for at least 0.3 s x words + 0.5 s + 0.4 s entrance.

Usage: reading_rule.py nodes.json
nodes.json: [{"id": "hook", "text": "Still chasing client approvals?", "enter": 0.2, "exit": 3.6}, ...]
"enter" is when the LAST element of a block has started entering (a block that staggers in
within 0.4 s counts as one node). Exit code 1 if any node is short.
"""
import json, sys

WPS, FLOOR, ENTRANCE = 0.3, 0.5, 0.4
nodes = json.load(open(sys.argv[1])); bad = 0
for n in nodes:
    words = len(n['text'].split()); need = WPS * words + FLOOR + ENTRANCE; have = n['exit'] - n['enter']
    ok = have + 1e-6 >= need; bad += not ok
    print(f"{'OK ' if ok else 'SHORT'} {n['id']:<14} {words:>2} words  on {have:5.2f}s  need {need:5.2f}s")
print(f'{len(nodes) - bad}/{len(nodes)} nodes pass')
sys.exit(1 if bad else 0)
