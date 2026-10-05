---
name: product-film
description: Make a fast, music-driven product launch film for a SaaS landing page (hero cut plus 1:1 and ad cut-downs) from real product footage, with every claim traceable to the page and every gate measured. Use when someone asks for a launch video, teaser, hero video, product film, or a video for a landing page, or says "make it hooking", "cut it to the music", or "use real app footage".
---

# Product film

A workflow for building a 30 to 60 second product launch film that people watch
to the end. It was distilled from a real production (see
`references/case-study.md`): several cuts were rejected by the owner as
"monotonous", "too slow" or "empty", and each rule below exists because a cut
failed without it.

The film is built as code (HTML + GSAP rendered to MP4 with HyperFrames, or any
deterministic HTML-to-video renderer), so every rule is checkable by a script,
not just by taste.

## The non-negotiables (read `references/rules.md` for the full list)

1. **Never AI-generate product UI.** Product screens come from the real app or
   from design-file exports. AI is fine for illustrations and icons (see
   `references/illustrations.md`).
2. **Brand and product on screen from frame 0.** The payoff lands by about 2 s.
3. **The music decides the structure.** Measure the track (bars, energy, lifts,
   breakdowns) before writing the storyboard. Big story turns sit on measured
   lifts. The ending must not sit in a breakdown.
4. **Every slide start gets an audible accent, on the beat.** Sound effects are
   peak-aligned: most SFX files start with silence, so an unaligned "hit" lands
   after the beat.
5. **Every on-screen string traces to the landing page or to a line the owner
   approved**, and every condition ("on plans that include it", "beta") stays
   attached and visible.
6. **Every product frame carries a visible "Sample data" label**, checked on
   every frame by OCR, unless the owner waives it (record the decision).
7. **Text breaks by phrase, never mid-phrase**, and every text node passes the
   reading rule: `0.3 s x words + 0.9 s` on screen (0.4 s entrance + 0.5 s floor).
8. **Real-app capture never touches production**: no test signups (they pollute
   the funnel metrics), a deny-by-default offline browser, and the app's own
   demo data with fictional names that you have web-checked.

## Workflow

Each phase ends at a gate. Owner decisions are asked, recorded and never
re-decided silently.

1. **Brief and source of truth.** Extract the landing page's visible copy into
   `copy.txt`. This file is the only claim source. List the owner's rules
   (brand colours, fonts, disclosures, things never to show).
2. **Music first.** Pick 2 or 3 licensed tracks. Run
   `scripts/music_map.py <track>` for each: BPM, beat phase, per-bar energy,
   lifts and breakdowns. Choose the in-point so the first lift lands at the end
   of the hook (about 2 bars in). Reject tracks whose breakdown would cover the
   last 8 bars. Let the owner hear auditions cut from the real in-point.
   Licences that forbid remixing: one continuous excerpt, no splicing or
   looping; volume ducking is mixing, not remixing. See `references/music.md`.
3. **Storyboard on the bar grid.** Sections of 2 or 4 bars; story turns on
   measured lifts; a one-bar breath before the biggest reveal; one hero move in
   the whole film. Tell one continuous journey with match cuts (the object
   carries across), not a slide list. Count words: budget about 90 for 50 s.
   Run `scripts/reading_rule.py` on the node schedule. Pick one style from
   `references/styles.md`: crisp real-app (the product window is the hero),
   chapter style (brand pill, one-bar chapter cards, stickers) or problem-led story
   (buyer problems, graphic "before" mock-ups, one signature moment; see
   `references/story.md`). For a re-skin or white-label moment, read
   `references/rebrand-capture.md` before planning the capture.
4. **Critique the plan before building** (if `/tri-plan` or a second model is
   available): one lens for "is it right" (claims, timings, music, gates) and
   a separate lens for "is it safe to run" (privileges, network, disk, licences).
5. **Capture real footage** (optional but strongest): see `references/capture.md`.
   Short 0.5 to 2 s micro-interactions aligned to beats (a caption typing with a
   live preview, a reply being typed, a workspace switcher opening) plus 2x
   stills for punch-ins. Never long walkthroughs. For motion that must stay
   sharp under a camera move, capture one 2x still per UI state and swap them.
6. **Illustrations** for any scene that is only text: one consistent clay or
   flat style, no text, no logos, no UI. See `references/illustrations.md`.
7. **Build and render.** Generate the composition from a bar-indexed timeline
   (never hand-placed seconds). Render 16:9 and 1:1 (9:16 for ads) with
   `HYPERFRAMES_VERSION=<pinned> scripts/render.sh <dir> <name> [timeout]`
   (staging dir, timeout, process-tree cleanup, disk floor; exit 124 = timed out).
8. **Mix.** `scripts/mix.py cue-sheet.json`: one continuous music excerpt,
   peak-aligned SFX, ducking under big hits, two-pass loudnorm to -14 LUFS, a
   limiter so the true peak stays at or below -1 dBTP after AAC encoding.
9. **Gates** (all must pass; see `references/qa-gates.md`): claims registry
   (`scripts/claims_gate.py`),
   every-frame OCR for disclosures and status truth, rule R per node, music lift
   at the chosen bars (M1), SFX onset at every slide start (M2), loudness,
   forbidden-name OCR on real footage, an owner listening pass (M3), and for
   real footage: zero raster upscale, capture fidelity, cursor on target and no
   leaked layers. Run them as one command that stops at the first failure.
10. **Owner review**, then cut-downs (15 s, 6 s), a text transcript for
    accessibility, and web encodes. Publishing is a separate approval.

## Files

- `references/rules.md`: every rule, with the failure that produced it
- `references/music.md`: choosing, measuring and cutting to a track
- `references/copy-and-claims.md`: claims, conditions, line breaks, reading rule
- `references/capture.md`: safe real-app capture (offline, mocked, renamed)
- `references/illustrations.md`: AI illustration brief and style prompt
- `references/qa-gates.md`: every gate and how to measure it, and lessons from the gates
- `references/styles.md`: the crisp real-app and chapter styles, and the rendering facts both need
- `references/story.md`: the problem-led structure, and why a crisp catalogue got no "aha"
- `references/rebrand-capture.md`: capturing a real white-label or theme re-skin honestly
- `references/pipeline-ops.md`: the one-command pipeline, owner gates, sandbox facts and tooling traps
- `references/case-study.md`: the production this was distilled from
- `scripts/`: `claims_gate.py`, `music_map.py`, `mix.py`, `reading_rule.py`, `ocr.swift`,
  `ocr_gate.py`, `rename.py`, `fetch.sh`, `render.sh`, `capture/harness.mjs`
  (each has usage in its header)
- `examples/`: a cue sheet, a reading-rule node list, OCR checks and a rename
  map, all taken from the case study
