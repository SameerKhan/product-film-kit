# Gates

| Gate | Measures | Tool |
|---|---|---|
| Lint | composition contract, contrast | the renderer's own check (HyperFrames `check`) |
| Claims | every visible string sourced; required items present; exact lists | `scripts/claims_gate.py` over the generated HTML |
| R | reading time per text node | `scripts/reading_rule.py` |
| Disclosure | "Sample data" readable in every product frame | `scripts/ocr_gate.py` (macOS Vision via `ocr.swift`) |
| Status truth | a Pending badge reads "Pending" in every frame of its scene | `scripts/ocr_gate.py` |
| Forbidden names | no old or real-business name in any real-footage frame | `scripts/ocr_gate.py` (`forbid` in checks.json) |
| Network | zero requests reached the network outside the local build | capture harness log |
| M1 | music-only energy lift at the chosen section bars | `scripts/mix.py` |
| M2 | onset at least 6 dB in the final mix at every slide start, and an SFX cue on each one | `scripts/mix.py` |
| Loudness | -14 LUFS integrated (plus or minus 1), true peak at or below -1 dBTP | `scripts/mix.py` |
| M3 | a human listens on headphones, laptop and phone | owner |
| Crisp | no raster image drawn above 1.0x its natural size in any frame; no visible image failed to load | per-frame probe of the composition (seek, read each image's scale chain) |
| Fidelity | each held UI state in the delivered video matches its source capture: luma SSIM at least 0.97 with a 1 px registration search | ffmpeg `ssim` on the mapped region |
| Cursor | at every click the cursor tip is within 6 px of its target | per-frame probe |
| Holds | in typing sequences every state is held 1 to 45 frames, in order | the composition's state timeline |
| Leak | nothing inside an inactive scene is painted | per-frame probe (see below) |

Always run a negative control for OCR gates (a frame where the text must NOT be
found), so you know the gate can fail.

## Lessons from the gates themselves

- **A probe page is not the renderer.** Probing the composition in a plain
  browser (seek the timeline, read the DOM) skips the renderer's runtime, which is
  what hides inactive scenes. A leak check written naively flagged every element.
  Do what the runtime does first (hide each inactive clip), then look for children
  that are still visible. Prove it by planting a leak in a throwaway copy and
  watching the gate fail.
- **A disabled check looks like a passing one.** A hold-length check sat behind
  `&& false` through several runs. Review gates for checks that cannot fail.
- **Mask, but cap the mask.** Decorative overlays (cursor, stickers, chips) are
  masked out of fidelity comparisons; cap the masked area (15% of the region) or
  the gate ends up scoring the masks.
- **OCR engines miss sharp frames.** Apple Vision returned nothing for a crisp
  frame at 3x that it read at 4x. Re-read a miss once at a second scale; count it
  only when both fail, and print the missed frame times so a failure is
  debuggable.
- **Exclude designed moments explicitly.** White flashes and full-screen chapter
  cards cover the product by design; list them in the gate rather than loosening
  the thresholds.
- **Gates exit nonzero.** A gate that prints FAIL and exits 0 is skipped by the
  pipeline. Build one command that runs every gate in order and stops at the
  first failure.
