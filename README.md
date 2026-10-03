# product-film-kit

A Claude Code skill, `/product-film`, for making a 30 to 60 second product launch
film for a SaaS landing page that people actually watch to the end: fast, cut to
the music, built from real product footage, and with every claim traceable to
the page.

It came out of a real production (a hero film for
[Social Champ](https://www.socialchamp.com)'s agency page). The owner rejected
cuts as "too slow", "monotonous", "empty" and "hard to read", and each rule here
exists because a cut failed without it. See
[the case study](plugins/product-film/skills/product-film/references/case-study.md).

## What it enforces

- **Music first.** Measure the track (BPM, beat phase, per-bar energy, lifts,
  breakdowns) before writing the storyboard. Story turns land on measured lifts;
  the call to action never lands in a breakdown.
- **An accent on every slide**, with sound effects peak-aligned (most SFX files
  start with silence, so a naive cue lands late).
- **Claims traced to the page**, with conditions kept attached, exact lists, and
  no status shown that the app would not show.
- **Never AI-generate product UI.** Use the real app (captured safely offline) or
  design-file exports. AI illustrations are fine for empty scenes.
- **"Sample data" readable on every product frame**, checked by OCR.
- **Phrase-based line breaks** and a per-node reading-time rule.
- **Two proven styles**: crisp real-app (2x state-sequence capture, no raster
  ever upscaled) and chapter style (brand pill, one-bar chapter cards, stickers
  that follow the action). See
  [styles](plugins/product-film/skills/product-film/references/styles.md).
- **No production side effects**: no test signups, deny-by-default network,
  scratch-only installs, pinned tools, a hashed licence ledger.

## Install

```bash
/plugin marketplace add SameerKhan/product-film-kit
/plugin install product-film@product-film-kit
```

Then ask Claude for a launch video, a hero film or a teaser, or run `/product-film`.

## Requirements

| Need | For |
|---|---|
| `ffmpeg` / `ffprobe` | music map, mix, gates |
| Python 3.9+ (stdlib only) | all `.py` scripts |
| Node 22 + [HyperFrames](https://github.com/heygen-com/hyperframes) (pinned) | rendering HTML + GSAP to MP4 (any deterministic HTML-to-video renderer works) |
| Playwright | optional real-app capture |
| macOS + `swiftc` | every-frame OCR gates (Apple Vision, on-device) |
| An image model (optional) | illustrations, never product UI |

## Scripts

All live in `plugins/product-film/skills/product-film/scripts/`, and each one
prints its usage in its header.

| Script | Does |
|---|---|
| `music_map.py` | BPM, beat phase (cross-checked on the kick band), per-bar energy and lift ratios; film bars for a chosen in-point; breakdown warning |
| `mix.py` | one continuous music excerpt (licence-safe), peak-aligned SFX cue sheet, ducking, button ending, two-pass loudnorm + limiter; gates M1 (music lift), M2 (slide onset), loudness |
| `reading_rule.py` | checks every text node is on screen for `0.3 s x words + 0.9 s` |
| `ocr_gate.py` + `ocr.swift` | every-frame OCR: required text present, forbidden names absent, negative control |
| `rename.py` | renames demo names in a scratch source copy and proves zero residuals |
| `fetch.sh` | https-only, host-allowlisted, hashed asset fetch |
| `render.sh` | pinned HyperFrames render with staging, timeout, process-group cleanup and a disk floor |
| `capture/harness.mjs` | offline Playwright harness: local build only, API from fixtures, everything else aborted |

## Contributing

Issues and pull requests are welcome. Run `bash scripts/check.sh` before
pushing (CI runs it too). New rules should say which failure they prevent.

## Licence

MIT. Music, SFX and logos you use carry their own licences: record them in a
ledger and read the licence page itself, not a summary.
