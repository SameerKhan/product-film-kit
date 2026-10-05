# Changelog

Plugin versions live in `plugins/product-film/.claude-plugin/plugin.json`.

## 1.2.1 (2026-10-05)

- New `references/walkthrough.md`: the whole job from the owner's side in nine steps
  (what you say, what Claude asks, what it runs, what you check), feedback phrasings
  that work, seven worked example prompts, doing it by hand with the example files,
  and a troubleshooting table from the case study's failures.
- README: a step-by-step section and a table of example prompts to start from.

## 1.2.0 (2026-10-05)

From three more cuts of the case-study film (v10 correct, v11 problem-led, v12 "wow"),
and the pipeline that delivered them.

- New `references/story.md`: why a crisp feature catalogue got no "aha", the
  problem-led structure (pain line, graphic "before", real "after", recap, proof,
  ask), showing pain instead of naming it, one signature moment on the biggest lift,
  payoff push-ins, escalation measured in events per beat, layout bugs that look like
  story problems.
- New `references/rebrand-capture.md`: capturing a real white-label or theme re-skin
  (fake tenant host mapped in the browser only, rewritten asset paths, seeding the
  branding the app hydrates from, fail-closed brand gates with a negative control,
  changed-pixel exit, verified colour targets, attestation).
- New `references/pipeline-ops.md`: the S0 to S3 one-command pipeline, owner gates kept
  outside the sandbox (decisions, footage and mock-up approvals, script approval
  record, protected-tree baseline, candidate versus final), measured macOS Seatbelt
  facts, process and cleanup rules, and tooling traps (Vision OCR blank inside the
  sandbox until warmed, ffmpeg without `-y` keeping an old file, Cyrillic lookalikes
  from OCR, a Homebrew upgrade changing a pinned binary).
- Gates: empty, push, no-text mock-ups, rendered events, event-cue sync, re-skin brand
  colour and re-skin text, final text on every encode; lessons (SSIM cannot tell two
  brands apart, OCR gates must fail closed, sample the whole moment, overlaps change
  what OCR sees); every gate planted with a defect on every run.
- Styles: a third style, problem-led story. Rules: a story section and operations rules.
- Case study: v10 to v12. README: rewritten with the why, the example film, the
  structure, the checks, safety and sign-off.
- `media/`: the v12 example film (720p), its poster and a storyboard.

## 1.1.0 (2026-10-03)

From two more cuts of the case-study film (v8 crisp real-app, v9 chapter style).

- New `references/styles.md`: the crisp real-app style (2x state-sequence
  capture, zero upscale, cursor inside the camera layer, reframe instead of
  retouch) and the chapter style (brand pill, one-bar chapter cards on the
  standard reading rule, typed lead phrase, stickers in action order, chips cut
  from real UI), plus rendering facts: hide with opacity not visibility,
  `immediateRender: false` on later `fromTo` tweens, emoji as PNGs.
- Gates: crisp, fidelity, cursor, hold and leak gates documented, with lessons
  (a probe page is not the renderer, cap masks, re-read OCR misses at a second
  scale, exclude designed moments explicitly, gates exit nonzero).
- Capture: state sequences with pin checks and atomic promotion.
- Case study: v7 to v9 rows and what their reviews found.

## 1.0.1 (2026-10-02)

- Illustrations: use real transparency, not `mix-blend-mode: multiply` (animated
  layers are isolated and the blend stops applying); Codex image runs need
  `--skip-git-repo-check` outside a repo.
- Rules: disclosures (sample-data chips, beta tags) may be waived by the owner,
  recorded and then enforced as forbidden strings; shortened lines must stay
  narrower than the page line.

## 1.0.0 (2026-10-02)

Hardened after a /tri-review (Claude + Codex + Gemini, walkthrough and operations passes) before
the first public push; see the commit log for each fix.

- First release: the `/product-film` skill, distilled from a 50 s agency hero
  film (see `references/case-study.md`).
- Rules with the failure behind each one, a 10-phase workflow, and references
  for music, claims, safe real-app capture, illustrations and QA gates.
- Scripts: `music_map.py` (BPM, phase, per-bar energy, lifts), `mix.py`
  (one-excerpt music, peak-aligned SFX, ducking, loudness, M1/M2 gates),
  `reading_rule.py`, `ocr_gate.py` + `ocr.swift` (every-frame OCR on macOS),
  `rename.py`, `fetch.sh` (quarantined, hashed asset fetch), `render.sh`
  (HyperFrames render with staging, timeout, process-group cleanup, disk floor)
  and an offline deny-by-default Playwright capture harness template.
