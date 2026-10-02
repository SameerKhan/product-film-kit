# Changelog

Plugin versions live in `plugins/product-film/.claude-plugin/plugin.json`.

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
