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

## Gates for edits of real footage (see `footage-edit.md`)

None of these ships as a script; build each and prove it with its planted defect
before the first cut is planned. Controls that need a real frame (such as a
third-party inbox frame) run only after consent is recorded.

| Gate | Measures | Planted defect it must catch |
|---|---|---|
| Words | every captioned word (identity and order from the transcript) ends inside its cut; the 40 ms just before every in and just after every out is room tone (at or below -50 dB 10 ms RMS, or a written per-join exception) | an out point moved 60 ms into a word |
| Cut (rendered) | at every join of the rendered dialogue: no click (largest sample-to-sample step within 2 ms of the join above -30 dBFS) and no dropout (more than 60 ms below -60 dB) | a join rendered without its fades |
| Offset | the editor's cut minus the raw footage, envelope cross-correlation, in a window around every reused range; each within 20 ms of the offset recorded in setup | one reused range shifted by 100 ms |
| UI frames | the hash of every source UI frame the cut shows (decoded, before scaling) is in the set a person reviewed | a frame of the real inbox list |
| UI words | OCR of the same frames against an allowlist, held frames weighted by their on-screen frames | the same inbox frame, through the same function |
| Burned captions | every crop rectangle avoids the measured caption band of the source | a crop over the band |
| Captions | the caption tokens equal the transcript tokens of the cuts, in order (a sequence check, not a timing check); every caption read by OCR at its midpoint (re-read once at 2x if blank) | a dropped word; the wrong words |
| Caption box | on every caption's midpoint frame, a pixel 12 px inside the box's left edge at its vertical centre (padding, never text) matches the box colour | a box rendered at 92% opacity over a light frame |
| Prompt cards | each card reads by OCR on the rendered frame 0.6 s after it arrives | a card removed from the timeline |
| Safe area | captions, labels, end-card images and logos inside the text-safe area (used here: 9:16 x 60 to 940, y 220 to 1500; 4:5 x 60 to 1020, y 70 to 1190; 16:9 x 96 to 1824, y 60 to 1020) | a caption at the bottom edge |

- **Weight held frames.** A frame held for 25 frames is one image but 25 frames on
  screen; counting images let a word on a held frame pass as one-frame OCR noise.
- **Keep gate scratch out of each other's way.** Per-segment frame folders inside the
  gate's temp folder were picked up as sampled frames; filter by exact file name.
- **Hash what you OCR.** A frame-hash pass run with `framemd5` over the whole file
  (no `-an` or `-map 0:v`) also hashed the audio packets, giving 2.5 times more
  hashes than frames. Hash the extracted image files, which are the same files the
  OCR reads.

## Gates for in-scene UI and motion

For product UI composited behind a speaker and built from real screenshots
(`in-scene-motion.md`). None ships as a script; each must fail on its planted defect.

| Gate | Measures | Planted defect it must catch |
|---|---|---|
| Matte (visible) | face and torso coverage, and stray matte on the wall, counted only where the RENDERED behind layer has alpha | a moving graphic over a matte hole: flagged on exactly the frame it covers the hole |
| Behind | each giant word: 1 to 35 % of its glyph pixels behind a person at entry, hero and exit; OCR edit distance at most 1 on the hero frame | a word fully behind the person; a word that misses everyone |
| Clean base | base equals source outside the parts; every fill equals its row sample; the built card equals the source (premultiplied colour, 2 levels, 99.9 % of pixels) | a fill outside the part rects; a missing part |
| Slices | parts inside the source; no OCR line crosses a part edge; every line in the format's crop is in a part or a declared static list | a part rect shifted through a title |
| Motion | each card builds in at least 2 steps; the float scale rises on every hold frame at the authored drift (within 10 %) and the base grows at least 1 px/s | a frozen card; a single-step card; a 0.01 %/s drift |
| Cursor | each press inside its target's drawn box; the arrow never in the person zone | a press 2000 px off; a path through the face |
| Choreography | spawn origin within 6 px at the declared start scale; entry times; reverse exits; ordered builds; dim level; ring grows; pressed part on top; cursor top-most; bar reveals monotonic | a card spawned 40 px off |
| Collision and wall | every frame, from the renderer's drawn boxes, group unions, 20 px padding; one declared handoff may overlap for at most 0.35 s | an unrelated pair overlapping 0.2 s; the declared pair outside its window |
| Read and legible | each card's key line on screen for 0.3 s per word + 0.9 s (or a declared, measured exception) and at least the approved line height | a key line held 0.5 s; a key line at 0.2x |
| Upscale | the drawn size (rest x peak keyframe scale) never above the source pixels; the renderer refuses too | a spring overshoot taking a card to 1.035x |
| Cues and email | one whoosh per on-beat card group, in the mixer's input; no email-shaped string in any OCR output or report | a card's whoosh removed; a planted address |

- **Compare premultiplied colour on cut-outs.** Rounded corners and transparent margins
  fail a straight-alpha comparison after a premultiplied round trip.
- **Read geometry from the renderer, not the plan.** Per-frame drawn boxes found a spawned
  card leaving its zone for 3 frames, then (after a fix) its origin moved 53 px; a static
  check of rest positions saw neither.
