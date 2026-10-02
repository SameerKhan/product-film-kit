#!/usr/bin/env python3
"""Mix a rendered (silent) film: one continuous music excerpt, peak-aligned SFX, ducking,
button ending, two-pass loudnorm + limiter, then measure the audio gates.

Usage: mix.py cue-sheet.json   (see examples/cue-sheet.example.json)

Gates printed at the end (exit 1 on any failure):
  ledger    every audio file's sha256 matches the ledger (a fetch.sh fetch-ledger.tsv, or a
            {"file.mp3": "<sha256>"} map). Refused without one unless "allow_unhashed": true.
  M1        music-only RMS lift >= 1.15 at each bar listed in "lift_bars"
  M2        final-mix onset >= 6 dB (peak in the 150 ms after vs RMS of the 300 ms before) at each slide start
  M2-cue    every slide start has an SFX cue on it, so M2 cannot pass on a music transient alone
  loudness  -14 LUFS +-1 integrated, true peak <= -1 dBTP
"""
import array, hashlib, json, math, os, re, subprocess, sys

cfg = json.load(open(sys.argv[1])); base = os.path.dirname(os.path.abspath(sys.argv[1]))
num = float   # every number from the cue sheet goes through float(): nothing reaches the filtergraph as raw text


def P(p):
    q = p if os.path.isabs(p) else os.path.join(base, p)
    return os.path.abspath(q)


BPM = num(cfg['bpm']); BEAT = 60 / BPM; BAR = 4 * BEAT
IN, DUR, FIN = num(cfg['music']['in_point']), num(cfg['duration']), num(cfg['final_hit'])
t = lambda bar, beat=0: (num(bar) - 1) * BAR + num(beat) * BEAT  # film bar 1 starts at 0 s
FF = ['ffmpeg', '-v', 'error', '-protocol_whitelist', 'file,pipe']   # local files only: no URLs, no playlists fetching remote segments


def load_ledger(v):
    if isinstance(v, dict): return v
    if isinstance(v, str):
        return {l.split('\t')[0]: l.split('\t')[1] for l in open(P(v)) if '\t' in l}
    return {}


LEDGER = load_ledger(cfg.get('ledger'))
if not LEDGER and not cfg.get('allow_unhashed'):
    sys.exit('no ledger: point "ledger" at fetch.sh\'s fetch-ledger.tsv (or set "allow_unhashed": true for a draft)')


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()


def src(path):
    p = P(path)
    if not os.path.isfile(p): sys.exit(f'not a local file: {p}')
    if LEDGER and LEDGER.get(os.path.basename(p)) != sha256(p): sys.exit(f'LEDGER FAIL {p}')
    return p


def pcm(path, a=None, b=None, sr=8000):
    rng = (['-ss', f'{num(a):.4f}'] if a is not None else []) + (['-to', f'{num(b):.4f}'] if b is not None else [])
    raw = subprocess.run([*FF, *rng, '-i', path, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                         capture_output=True, check=True, timeout=600).stdout
    x = array.array('h'); x.frombytes(raw); return x


def peak_at(path):
    """Seconds from file start to the loudest sample. SFX files start with silence; shift cues by this."""
    a = [abs(v) for v in pcm(path)]; return a.index(max(a)) / 8000 if a else 0.0


def dur(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-protocol_whitelist', 'file', '-show_entries', 'format=duration',
                                 '-of', 'csv=p=0', path], capture_output=True, text=True, check=True, timeout=60).stdout)


def rms(x): return math.sqrt(sum(v * v for v in x) / max(1, len(x))) + 1e-9


def when(c):  # a cue time is either seconds ("t") or a bar position ("bar", optional "beat", optional "offset")
    return num(c['t']) if 't' in c else t(c['bar'], c.get('beat', 0)) + num(c.get('offset', 0))


cues, cue_at = [], []
for c in cfg['cues']:
    path = src(os.path.join(cfg.get('sfx_dir', ''), c['file']))
    al = c.get('align', 'peak')  # peak: loudest sample on the cue; end: file ends on the cue (risers); start: no shift
    at = when(c); x = at - {'peak': peak_at, 'end': dur, 'start': lambda _: 0}[al](path)
    if 0 <= at < DUR:   # filter on the cue time; a peak shift before 0 s is clamped, not dropped
        cues.append((max(0.0, x), path, num(c.get('gain', 0.5))))
        if al != 'end': cue_at.append(at)
cues.sort()

SLIDES = [when(s) for s in cfg['slides']]
duck = [(when(d) - num(d.get('lead_beats', 0)) * BEAT, when(d) + num(d.get('hold', 0)), num(d['gain'])) for d in cfg.get('ducks', [])]
duck += [(s, s + num(cfg.get('slide_duck_s', 0.3)), num(cfg.get('slide_duck_gain', 0.7))) for s in SLIDES]
vexpr = '*'.join(f'if(between(t,{a:.3f},{b:.3f}),{v:.4f},1)' for a, b, v in duck) or '1'
music = src(cfg['music']['file']); video = P(cfg['video'])
if not os.path.isfile(video): sys.exit(f'not a local file: {video}')
inputs = ['-protocol_whitelist', 'file', '-i', video, '-protocol_whitelist', 'file', '-i', music]
f = [f"[1:a]atrim={IN:.4f}:{IN + FIN:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.25,afade=t=out:st={FIN - 0.025:.3f}:d=0.025,"
     f"volume='{vexpr}':eval=frame,apad=whole_dur={DUR:.4f}[m]"]
for i, (x, p, g) in enumerate(cues):
    inputs += ['-protocol_whitelist', 'file', '-i', p]; f.append(f'[{i + 2}:a]volume={g:.4f},adelay={int(x * 1000)}:all=1[s{i}]')
f.append('[m]' + ''.join(f'[s{i}]' for i in range(len(cues))) + f'amix=inputs={len(cues) + 1}:normalize=0:duration=first,atrim=0:{DUR:.4f}[mx]')
fc = ';'.join(f); out = P(cfg['out']); os.makedirs(os.path.dirname(out), exist_ok=True)
tmp = out + '.partial.mp4'   # written beside the target, promoted only when complete

r = subprocess.run(['ffmpeg', '-hide_banner', *inputs, '-filter_complex', fc + ';[mx]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[o]',
                    '-map', '[o]', '-f', 'null', '-'], capture_output=True, text=True, timeout=1800)
if r.returncode != 0 or '{' not in r.stderr: sys.exit('loudness pass failed:\n' + r.stderr[-800:])
m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={num(m['input_i'])}:measured_TP={num(m['input_tp'])}:measured_LRA={num(m['input_lra'])}"
      f":measured_thresh={num(m['input_thresh'])}:offset={num(m['target_offset'])}:linear=true")
try:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', fc + f';[mx]{ln},alimiter=limit=0.75:attack=2:release=60:level=false[o]',
                    '-map', '0:v', '-map', '[o]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', tmp], check=True, timeout=1800)
    os.replace(tmp, out)
finally:
    if os.path.exists(tmp): os.remove(tmp)

r = subprocess.run(['ffmpeg', '-hide_banner', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True, timeout=600)
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r.stderr)[-1]); TP = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r.stderr)[-1])
M1 = {b: round(rms(pcm(music, IN + t(b), IN + t(num(b) + 1))) / rms(pcm(music, IN + t(num(b) - 1), IN + t(b))), 2) for b in cfg.get('lift_bars', [])}
M2 = {}
for s in SLIDES + [FIN]:
    pre = rms(pcm(out, max(0, s - 0.3), s)); post = max([abs(v) for v in pcm(out, s, s + 0.15)] or [0]) / math.sqrt(2) + 1e-9
    M2[round(s, 2)] = round(20 * math.log10(post / pre), 1)
uncued = [round(s, 2) for s in SLIDES + [FIN] if not any(abs(s - c) <= 0.05 for c in cue_at)]
print(json.dumps({'out': out, 'LUFS': I, 'TP': TP, 'cues': len(cues), 'M1_music_lift': M1, 'M2_onset_dB': M2,
                  'slides_without_cue': uncued, 'ledger_checked': bool(LEDGER)}, indent=1))
fail = []
if not (abs(I + 14) <= 1 and TP <= -1.0): fail.append('loudness')
if any(v < 1.15 for v in M1.values()): fail.append('M1')
if any(v < 6 for v in M2.values()): fail.append('M2')
if uncued: fail.append('M2-cue')
print('GATES', 'PASS' if not fail else 'FAIL ' + ','.join(fail))
sys.exit(1 if fail else 0)
