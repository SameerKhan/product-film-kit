#!/usr/bin/env python3
"""Mix a rendered (silent) film: one continuous music excerpt, peak-aligned SFX, ducking,
button ending, two-pass loudnorm + limiter, then measure the audio gates.

Usage: mix.py cue-sheet.json   (see examples/cue-sheet.example.json)

Gates printed at the end (exit 1 on any failure):
  M1  music-only RMS lift >= 1.15 at each bar listed in "lift_bars"
  M2  final-mix onset >= 6 dB (peak in 150 ms after vs RMS of 300 ms before) at each slide start
  loudness  -14 LUFS +-1 integrated, true peak <= -1 dBTP
  ledger    every audio file's sha256 matches "ledger" (when given)
"""
import array, hashlib, json, math, os, re, subprocess, sys

cfg = json.load(open(sys.argv[1])); base = os.path.dirname(os.path.abspath(sys.argv[1]))
P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
BPM = cfg['bpm']; BEAT = 60 / BPM; BAR = 4 * BEAT
IN, DUR, FIN = cfg['music']['in_point'], cfg['duration'], cfg['final_hit']
t = lambda bar, beat=0: (bar - 1) * BAR + beat * BEAT  # film bar 1 starts at 0 s
LEDGER = cfg.get('ledger', {})


def src(path):
    p = P(path)
    if LEDGER:
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        assert LEDGER.get(os.path.basename(p)) == h, f'LEDGER FAIL {p}'
    return p


def pcm(path, a=None, b=None, sr=8000):
    rng = (['-ss', f'{a}'] if a is not None else []) + (['-to', f'{b}'] if b is not None else [])
    raw = subprocess.run(['ffmpeg', '-v', 'error', *rng, '-i', path, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    x = array.array('h'); x.frombytes(raw); return x


def peak_at(path):
    """Seconds from file start to the loudest sample. SFX files start with silence; shift cues by this."""
    a = [abs(v) for v in pcm(path)]; return a.index(max(a)) / 8000


def dur(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                                capture_output=True, text=True, check=True).stdout)


def rms(x): return math.sqrt(sum(v * v for v in x) / max(1, len(x))) + 1e-9


def when(c):  # a cue time is either seconds ("t") or a bar position ("bar", optional "beat", optional "offset")
    return c['t'] if 't' in c else t(c['bar'], c.get('beat', 0)) + c.get('offset', 0)


cues = []
for c in cfg['cues']:
    path = src(os.path.join(cfg.get('sfx_dir', ''), c['file']))
    al = c.get('align', 'peak')  # peak: loudest sample on the cue; end: file ends on the cue (risers); start: no shift
    x = when(c) - {'peak': peak_at, 'end': dur, 'start': lambda _: 0}[al](path)
    if 0 <= x < DUR: cues.append((max(0.0, x), path, c.get('gain', 0.5)))
cues.sort()

SLIDES = [when(s) for s in cfg['slides']]
duck = [(when(d) - d.get('lead_beats', 0) * BEAT, when(d) + d.get('hold', 0), d['gain']) for d in cfg.get('ducks', [])]
duck += [(s, s + cfg.get('slide_duck_s', 0.3), cfg.get('slide_duck_gain', 0.7)) for s in SLIDES]
vexpr = '*'.join(f'if(between(t,{a:.3f},{b:.3f}),{v},1)' for a, b, v in duck) or '1'
music = src(cfg['music']['file'])
inputs = ['-i', P(cfg['video']), '-i', music]
f = [f"[1:a]atrim={IN}:{IN + FIN},asetpts=PTS-STARTPTS,afade=t=in:d=0.25,afade=t=out:st={FIN - 0.025:.3f}:d=0.025,"
     f"volume='{vexpr}':eval=frame,apad=whole_dur={DUR}[m]"]
for i, (x, p, g) in enumerate(cues):
    inputs += ['-i', p]; f.append(f'[{i + 2}:a]volume={g},adelay={int(x * 1000)}:all=1[s{i}]')
f.append('[m]' + ''.join(f'[s{i}]' for i in range(len(cues))) + f'amix=inputs={len(cues) + 1}:normalize=0:duration=first,atrim=0:{DUR}[mx]')
fc = ';'.join(f); out = P(cfg['out'])

r = subprocess.run(['ffmpeg', '-hide_banner', *inputs, '-filter_complex', fc + ';[mx]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[o]',
                    '-map', '[o]', '-f', 'null', '-'], capture_output=True, text=True)
m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', fc + f';[mx]{ln},alimiter=limit=0.75:attack=2:release=60:level=false[o]',
                '-map', '0:v', '-map', '[o]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', out], check=True)

r = subprocess.run(['ffmpeg', '-hide_banner', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r.stderr)[-1]); TP = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r.stderr)[-1])
M1 = {b: round(rms(pcm(music, IN + t(b), IN + t(b + 1))) / rms(pcm(music, IN + t(b - 1), IN + t(b))), 2) for b in cfg.get('lift_bars', [])}
M2 = {}
for s in SLIDES + [FIN]:
    pre = rms(pcm(out, max(0, s - 0.3), s)); post = max(abs(v) for v in pcm(out, s, s + 0.15)) / math.sqrt(2)
    M2[round(s, 2)] = round(20 * math.log10(post / pre), 1)
print(json.dumps({'out': out, 'LUFS': I, 'TP': TP, 'cues': len(cues), 'M1_music_lift': M1, 'M2_onset_dB': M2}, indent=1))
fail = []
if not (abs(I + 14) <= 1 and TP <= -1.0): fail.append('loudness')
if any(v < 1.15 for v in M1.values()): fail.append('M1')
if any(v < 6 for v in M2.values()): fail.append('M2')
print('GATES', 'PASS' if not fail else 'FAIL ' + ','.join(fail))
sys.exit(1 if fail else 0)
