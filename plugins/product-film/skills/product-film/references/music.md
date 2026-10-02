# Music: choose, measure, cut

## Choosing
1. Shortlist 5 to 10 licensed tracks (check the licence page itself: ads and web
   use allowed? remixing allowed? Content ID registration banned?). Save a dated
   copy of the licence page and the item URL; hash every file.
2. Run `scripts/music_map.py track.mp3`. Reject tracks with no lifts (a flat
   energy line). Prefer a clear early lift followed by sustained energy.
3. For each finalist, pick the in-point so the first lift lands on bar 3 of the
   film (after a 2-bar hook). Check the map: the last 8 bars of the film must not
   fall into a breakdown.
4. Give the owner full-length auditions cut from the real in-point.

## Measuring (what `music_map.py` prints)
- BPM from the onset autocorrelation (80 to 180 BPM search).
- Beat phase from the onset grid, cross-checked on a 120 Hz low-passed kick band.
  If the two disagree by about half a beat, anchor the downbeat to the measured
  section lift (section changes land on downbeats) and confirm by ear.
- Per-bar energy (0 to 9) for the whole track, and the music-only lift ratio at
  every candidate section boundary.

## Cutting
- Build the timeline in integer bars; derive seconds from BPM and phase.
- Section starts snap to downbeats; inside a section, motion lands on beats.
- If the reading rule leaves no slack before a lift, snap to half-beats rather
  than lengthening the film.
- Button ending: cut the music on the final hit (25 ms fade) and let the hit ring.
