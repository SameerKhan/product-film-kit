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
| Empty | no delivered frame is background only (luma std-dev under 6 at 96x54), plus a DOM list of elements required on screen per interval | ffmpeg grey frames + per-frame probe |
| Push | at each payoff action the camera is at least 0.95 of its maximum sharp zoom, holds through the state change, and is under 0.8 of it one beat later | per-frame probe of the camera transform |
| No-text mock-ups | "before" mock-ups hold no text node, no CSS `content`, no icon font, no image, canvas or SVG; OCR of their areas finds no word | DOM probe + OCR of the rendered areas |
| Rendered events | every event in the geometry manifest visibly happens at its time: the element goes from hidden to shown, at least half inside the frame; camera slams move the camera; the wipe progresses | per-frame probe |
| Event-cue sync | every visual event has exactly one sound cue and every event cue has an event | the mixer reads the same manifest |
| Re-skin brand | before the wipe the verified brand surfaces are vendor-coloured, after it agency-coloured (and under 5 % vendor colour), measured on the delivered frames | pixel sampling of mapped target rects |
| Re-skin text | after the wipe the window never shows the vendor's display name, in any case; every frame must actually be read | OCR, fail-closed (see below) |
| Final | every on-screen string is readable in every delivered file, at the time it should be | OCR spot checks on each encode |

Always run a negative control for every gate (a planted defect the gate must
catch), and check it fails for the reason it plants. The case-study pipeline plants
eight on every run: a pill leak, a blur in an "after" scene, a removed camera push, a
word, CSS-generated text and an image inside a mock-up, a suppressed event, and a
removed story string; plus a v8 film with known empty frames, and a string that is
not in the film for the final text check.

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

- **SSIM cannot tell two brands apart at a wide framing.** The vendor-brand frame
  scored 0.988 against the tenant-brand source: the colour change covered too little
  of the frame, and orange and blue differ little in luma. SSIM proves sharpness.
  Prove the re-skin with colour on the verified surfaces, and keep an inverse control
  (a vendor frame tested as the tenant brand must fail).
- **OCR gates must fail closed.** A check that passes when it finds nothing passes
  when OCR returns nothing. Require the gate to read something it knows is there (the
  screen's own tab text on 90 % of frames), match the forbidden text in any case, and
  plant the forbidden text onto real frames as a control.
- **Sample the whole moment, not one frame.** A re-skin checked at one frame before
  and one after missed bugs that a hold at each camera slam and at three points of
  the after scene found (including a gate bug: every hold reusing the first frame).
- **Overlaps change what OCR sees.** In the square format the "before" pile sits over
  the live window, so the app's own text shows through its gaps. Run the rendered
  no-text check where the mock sits on plain background, and rely on the DOM check
  elsewhere.
