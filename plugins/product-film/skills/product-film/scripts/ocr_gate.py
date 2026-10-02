#!/usr/bin/env python3
"""Every-frame OCR gates on a rendered film.

Usage: ocr_gate.py film.mp4 checks.json [--ocr build/ocr]
checks.json:
{
  "must_show": [   # text that must be readable in EVERY frame of the window, inside the crop box
    {"name": "sample-chip", "want": "Sample data", "box": [1590, 132, 210, 66], "from": 0.6, "to": 13.2},
    {"name": "pending",     "want": "Pending",     "box": [1520, 590, 200, 110], "from": 4.4, "to": 11.3}
  ],
  "forbid": {      # no frame in the window may contain a match (full frame, sampled at fps)
    "regex": "old[\\W_]{0,7}brand", "from": 11.7, "to": 21.5, "fps": 10
  },
  "negative_control": {"want": "Sample data", "at": 49.0, "box": [1590, 132, 210, 66]}
}
The negative control is a frame where the text must NOT be found, proving the gate can fail.
Requires macOS (Vision) via scripts/ocr.swift compiled to a binary.
"""
import argparse, json, os, re, subprocess, sys, tempfile

ap = argparse.ArgumentParser(); ap.add_argument('film'); ap.add_argument('checks'); ap.add_argument('--ocr', default='build/ocr')
a = ap.parse_args(); C = json.load(open(a.checks)); res = {}; fail = False


def frames(td, start, end, vf):
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{start:.3f}', '-to', f'{end:.3f}', '-i', a.film, '-vf', vf,
                    os.path.join(td, '%05d.png')], check=True)
    fs = sorted(os.path.join(td, f) for f in os.listdir(td))
    return subprocess.run([a.ocr, *fs], capture_output=True, text=True, check=True).stdout.splitlines() if fs else []


crop = lambda b: f'crop={b[2]}:{b[3]}:{b[0]}:{b[1]},scale={b[2] * 3}:{b[3] * 3}'
for c in C.get('must_show', []):
    with tempfile.TemporaryDirectory() as td:
        lines = frames(td, c['from'], c['to'], crop(c['box']))
        miss = [l.split('\t')[0][-9:] for l in lines if c['want'].lower() not in l.lower()]
        res[c['name']] = {'frames': len(lines), 'fails': len(miss), 'first_fails': miss[:5]}
        fail |= bool(miss) or not lines
if 'forbid' in C:
    fb = C['forbid']; rx = re.compile(fb['regex'], re.I)
    with tempfile.TemporaryDirectory() as td:
        lines = frames(td, fb['from'], fb['to'], f"fps={fb.get('fps', 10)}")
        hits = [l.split('\t')[0][-9:] for l in lines if rx.search(l)]
        res['forbid'] = {'frames': len(lines), 'hits': hits[:5]}; fail |= bool(hits) or not lines
if 'negative_control' in C:
    n = C['negative_control']
    with tempfile.TemporaryDirectory() as td:
        lines = frames(td, n['at'], n['at'] + 0.04, crop(n['box']))
        found = any(n['want'].lower() in l.lower() for l in lines)
        res['negative_control'] = {'found': found, 'ok': not found}; fail |= found
print(json.dumps(res, indent=1)); print('OCR GATES', 'FAIL' if fail else 'PASS'); sys.exit(1 if fail else 0)
