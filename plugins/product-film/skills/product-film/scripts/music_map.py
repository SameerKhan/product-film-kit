#!/usr/bin/env python3
"""Map a music track before you storyboard: BPM, beat phase, per-bar energy, lifts, breakdowns.

Python stdlib + ffmpeg only (no numpy / librosa).

Usage:
  music_map.py track.mp3                         # estimate BPM + phase, print the bar map
  music_map.py track.mp3 --bpm 123 --downbeat 11.95   # override after checking by ear
  music_map.py track.mp3 --in 8.048 --bars 26    # show the film's bars for a chosen in-point

Output: one line per bar: track time, film bar (when --in is given), energy 0-9 as a bar
chart, and the music-only lift ratio vs the previous bar (LIFT >= 1.15, DROP <= 0.80).
"""
import argparse, array, math, subprocess, sys

SR, HOP = 11025, 256  # ~23 ms analysis frames


def decode(path, sr=SR, lowpass=None):
    af = ['-af', f'lowpass=f={lowpass}'] if lowpass else []
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, *af, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    a = array.array('h'); a.frombytes(raw); return a


def frame_rms(a):
    out = []
    for i in range(len(a) // HOP):
        s = 0
        for v in a[i * HOP:(i + 1) * HOP]: s += v * v
        out.append(math.sqrt(s / HOP))
    return out


def onset(e):
    lg = [math.log(1 + x) for x in e]
    return [max(0.0, lg[i] - lg[i - 1]) if i else 0.0 for i in range(len(lg))]


def estimate_bpm(o, lo=80, hi=180):
    fps = SR / HOP; best = (0, 0)
    for b in [x / 2 for x in range(lo * 2, hi * 2 + 1)]:
        lag = fps * 60 / b; L = int(lag); fr = lag - L; s = 0
        for i in range(L + 1, len(o)): s += o[i] * ((1 - fr) * o[i - L] + fr * o[i - L - 1])
        if s > best[0]: best = (s, b)
    return best[1]


def estimate_phase(o, bpm, seconds=60):
    fps = SR / HOP; period = fps * 60 / bpm; best = (0, 0)
    for k in range(200):
        ph = k / 200 * period; s = 0; x = ph
        while x < min(len(o) - 1, fps * seconds): s += o[int(x)]; x += period
        if s > best[0]: best = (s, ph / fps)
    return best[1]


def seg_rms(a, t0, t1, sr=SR):
    x = a[max(0, int(t0 * sr)):max(0, int(t1 * sr))]
    return math.sqrt(sum(v * v for v in x) / max(1, len(x))) + 1e-9


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('track'); ap.add_argument('--bpm', type=float); ap.add_argument('--downbeat', type=float,
                    help='a known downbeat in track seconds (e.g. a measured section lift)')
    ap.add_argument('--in', dest='inpt', type=float, help='film in-point in track seconds')
    ap.add_argument('--bars', type=int, default=0, help='film length in bars (with --in)')
    a = ap.parse_args()

    pcm = decode(a.track); dur = len(pcm) / SR
    o = onset(frame_rms(pcm[:SR * 90]))
    bpm = a.bpm or estimate_bpm(o)
    beat = 60 / bpm; bar = 4 * beat
    phase = estimate_phase(o, bpm)
    kick = onset(frame_rms(decode(a.track, lowpass=120)[:SR * 90]))
    kphase = estimate_phase(kick, bpm)
    d = abs(phase - kphase) % beat
    print(f'track {dur:.2f}s  BPM {bpm}  beat {beat:.3f}s  bar {bar:.3f}s')
    print(f'beat phase: onsets {phase:.3f}s, kick band {kphase:.3f}s' +
          ('  (DISAGREE by ~half a beat: anchor --downbeat to a measured lift, confirm by ear)' if min(d, beat - d) > beat / 4 else ''))
    db = a.downbeat if a.downbeat is not None else phase
    first = db - math.floor(db / bar) * bar
    energies = []; t = first
    while t + bar <= dur: energies.append((t, seg_rms(pcm, t, t + bar))); t += bar
    mx = max(e for _, e in energies)
    print(f'downbeat anchor {db:.3f}s; first full bar at {first:.3f}s\n')
    print('  track_s  film  energy      lift')
    for i, (t0, e) in enumerate(energies):
        r = e / energies[i - 1][1] if i else 1.0
        tag = 'LIFT' if r >= 1.15 else ('DROP' if r <= 0.80 else '')
        fb = ''
        if a.inpt is not None:
            n = round((t0 - a.inpt) / bar) + 1
            fb = f'{n:>4}' if 1 <= n <= (a.bars or 10 ** 6) else '    '
        lvl = min(9, int(9 * e / mx))
        print(f'{t0:9.3f} {fb:>5}  {"#" * lvl:<9} {r:5.2f} {tag}')
    if a.inpt is not None and a.bars:
        tail = [e for t0, e in energies if a.inpt + (a.bars - 8) * bar <= t0 < a.inpt + a.bars * bar]
        if tail and min(tail) < 0.5 * mx: print('\nWARNING: the last 8 film bars include a breakdown (energy < 50% of peak)')


if __name__ == '__main__':
    sys.exit(main())
