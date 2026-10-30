# UI in the room: compositing product UI behind a speaker, and making it move

`footage-edit.md` covers cutting real footage of people. This page covers the next step
those reels usually get asked for: "the animation in a coloured box looks dated, put the
product in the room". Instead of a panel beside the speaker, product UI sits on the wall
BEHIND the person (a person matte keeps them in front), giant words pass behind the head,
and the UI moves the way modern explainers do: cards assemble from their parts, a cursor
presses a real control and the next screen springs out of it, nothing sits frozen.

It was distilled from one production: a founder's 49-second reel (9:16, 4:5, 16:9) remade
in-scene, then remade again after the owner said the first in-scene version still felt
static next to the reference ("it's not exactly the same screenshots, they're more
interactive, they move around"). Rules name the failure behind them where there was one.
At the time of writing the owner had not yet signed off the final cut, so treat the
design choices as tested by gates, not by an audience.

**Nothing on this page ships as a script.** The production's renderer, builder and gates
were tied to its footage. Build each check in your own pipeline and show it failing on its
planted defect (see `qa-gates.md`) before trusting it.

## 1. Study the reference's motion, not its stills

- **Six stills of a reference miss everything that matters.** The first analysis looked
  at frames at 6, 10, 27, 39, 46 and 55 s and concluded "cards on the wall". The second,
  at 4 frames per second, found that the cards are built from parts, that a screen
  recording plays inside one card, that a cursor clicks a dialog and its state changes,
  that UI rises out of a laptop the presenter holds, and that nothing is ever still.
- **Sample the reference at 0.25 s or finer, through the whole film.** If the video sits
  on a site you can watch but should not download, capture it while it plays: in the
  browser, `video.requestVideoFrameCallback` hands you every presented frame; draw every
  0.25 s into in-memory canvases (4 x 4 grids per sheet) and read the sheets. Seeking does
  not work on streaming players: they only buffer what they are playing and evict the rest.
- **Write the result as a beat table and a technique catalogue**, with times. The
  catalogue that came out of this one:
  - staggered builds from real parts (0.1 to 0.25 s apart, spring overshoot);
  - live content inside cards (playing UI, playing clips);
  - simulated cursor micro-interactions with a visible state change;
  - UI anchored to props and gestures (out of a held laptop, where the hand points);
  - never static: slow drift on every hold;
  - staggered exits in reverse order;
  - depth both ways: some graphics behind the person, some in front;
  - kinetic type, one word at a time in sync with speech;
  - process diagrams: a source, a line drawn behind the person, outputs spawning;
  - clean talking stretches between graphic beats;
  - an end card with a pressed CTA over live footage.
- **Then check which techniques your footage can support.** A hand-pose pass (Apple
  Vision `VNDetectHumanHandPoseRequest`, 2 fps) showed the founder's hands mostly low,
  and the one raised two-hand gesture fell inside a cut, so gesture anchoring was
  dropped. Check the probe against the edit, not the raw.

## 2. The in-scene composite

- **Person matte per frame, on the exact plate frames.** Pipe the plate (after crop,
  scale and any extension) as raw frames into the segmenter (Apple Vision
  `VNGeneratePersonSegmentationRequest`, `.accurate`) and write one matte per output
  frame, plus face and upper-body boxes. Computing the matte once at source geometry and
  transforming it later lets plate and matte drift apart by a frame or a pixel.
- **Composite order:** plate, then the BEHIND layer, then the person (plate through the
  matte, lightly blurred edge), then the FRONT layer. Two renderer processes, one per
  layer, streamed through FIFOs.
- **A matte defect only matters where a graphic shows through it.** Over plain footage a
  hole in the matte shows the same plate pixels and is invisible. Count defects only where
  the RENDERED behind layer has alpha (not where you think a card is: moving, revealed and
  fading graphics make static rectangles wrong). Prove the rule with a synthetic control: a
  moving element over a planted matte hole must be flagged on exactly the one frame where
  it covers the hole.
- **Giant words behind the head** must cross the person (some glyph pixels behind them) and
  still read (OCR edit distance at most 1 on the hero frame). Tune the height per word and
  per format; a floor of 1 % hidden glyph pixels proves the word passes behind someone.
- **Keep the frozen end card off the person checks** (or check the head only): it is a
  blurred frame under a veil.

## 3. Motion built from real screenshots

The owner chose real product pixels over new screen recordings. That sets a ceiling
(see section 6), but a lot of the reference's feel is reachable:

- **Cut each card into its real parts** (tiles, rows, swatches, chips, chart bars, a
  button), declared as rectangles in the source with the source's sha256. Verify the
  rectangles with OCR line boxes: no text line may cross a part edge (a time stamp clipped
  by a row's edge was caught this way), and every line in the format's crop is inside a
  part or on a declared static list (axis labels).
- **A flat screenshot has no "before" state.** A chart image already contains its bars; a
  button can be burned into a photo. Build a CLEAN BASE: the source with every part
  rectangle filled row by row from a part-free column of the same image (a white card gets
  a uniform fill; a chart keeps each gridline row's colour). Parts arrive over the base. A
  gate proves the base equals the source outside the parts, that every fill equals its row
  sample, and that once every part has arrived the card equals the source. The fills are
  then the only non-source product pixels ever on screen, and only under parts that have
  not arrived yet. Say so in the deviations file.
- **Nested parts are holes.** An unread dot inside a message row is its own part; the row's
  image has the dot's rectangle filled, so the dot cannot show before it pops.
- **Grow chart bars with a clip reveal, never a spring.** An underdamped spring overshoots,
  so the bar would shrink back. Reveal bottom-up with a monotone ease and gate on monotonic
  visible height.
- **One click, with a true result.** The cursor glides to a real control, the control dips
  (about 3 %), a ring expands, and the next real screen springs out of the pressed control's
  centre. Only click where the result shown is what that control really does: an "Open
  approval workflows" button does not approve anything, so it got no click.
- **Redact personal data at ingest, not on screen.** One public product card showed an email
  address in a sample row. Cut the band out of the input itself, delete the full file once
  the redacted one is pinned, and gate that no email-shaped string appears in any OCR output
  or gate report (approved handles such as "@brand" stay allowed).
- **Spring numbers must satisfy their own caps.** A plan said "damping 0.55, overshoot at
  most +4 %". From 0.6x, damping 0.55 overshoots about 5 %, and from 0.35x about 8 %.
  Pick the damping from the cap (0.62 and 0.68 here) and measure the peak and settle time
  in a unit test.
- **Rest scale = fitted scale / peak multiplier.** With overshoot and hold drift, a card
  drawn at its fitted size spends frames larger than its zone and larger than its source
  pixels. Divide by the measured peak and both hold on every frame.
- **Compute all easing in one place.** The builder writes dense per-frame keyframes (centre,
  scale, opacity; clip rects for reveals); the renderer only interpolates. Gates read the
  same keyframes, so the builder, renderer and gates cannot disagree about the maths.
- **Add new features behind their own fields.** Without them the renderer must produce
  byte-identical frames and geometry: test that on real timelines before anything else
  (120 frames and three geometry dumps, all identical, here).

## 4. Timing against a fixed cut

- **Anchor beats to spoken words**, then snap the card's entry to the music's beat (at most
  half a beat), and compute every downstream promise from the SNAPPED time.
- **A reading rule can be infeasible against the owner's cut.** The four-word key line of a
  card that must leave when the next card springs out needed 2.1 s; the cut allowed about
  1 s. Do not weaken the rule silently: declare a measured exception for that card, let the
  gate enforce the measured floor, and list it in the deviations file.
- **Choose each card's key line deliberately.** Usually it is the line the voice is about.
  Make the rest texture, as the reference does with its dense cards. Order the parts so the
  key arrives first and leaves last.
- **A legibility floor can come from what the owner already approved.** The smallest key line
  in the approved previous cut (18 px OCR line height in 9:16) became the floor; a later
  layout change that dropped below it (17.5 px) was caught and fixed.
- **A card may run past its range end** into the next clip when its parts need the time to
  leave in order, as long as nothing else is on that part of the wall.

## 5. Gates for this kind of motion

Each must fail on its planted defect before it is trusted (see `qa-gates.md`):
- **Clean base:** equality outside the parts, fills equal row samples, built card equals
  source. Compare premultiplied colour: straight-alpha values of semi-transparent corner
  pixels are rounding noise after a premultiplied round trip.
- **Slices:** inside the source; no OCR line crosses a part edge; full coverage of the
  format's crop minus a declared static list; no "@" in the redacted source.
- **Motion:** each card builds in at least two steps; during the hold the float scale
  rises on every frame at the authored drift (within 10 %) and the base grows at least
  1 px per second. Read the float keyframes; integer boxes repeat across frames.
- **Cursor:** each press lands inside its target's drawn box; the arrow never enters the
  person zone.
- **Choreography:** spawn origin within 6 px of the pressed control's centre, at the
  declared start scale; declared entry times; reverse exit order; dots after their rows;
  swatches and chips in order; dimmed siblings at their target opacity; ring growing;
  pressed part drawn above its siblings; cursor top-most; bar reveals monotonic.
- **Collision and wall, every frame, from the renderer's own drawn boxes.** Use group
  unions: parts of one card may overlap each other, different groups may not. The only
  exemption is a declared parent to child handoff, for at most 0.35 s from the child's
  first frame. Controls cover an unrelated pair, the wrong format and outside the window.
- **Reading time and legibility of each key line; one whoosh per card group** (reaching the
  mixer's actual input file); **no email-shaped strings.**

## 6. Lessons from building it

- **The gates found six real defects in the first five full runs, each in a few minutes:**
  - a one-piece card's peak scale was computed from a guess, and the renderer refused to
    draw it 1.8 % above source;
  - the spawned card started at the cursor's press point and poked out of its zone;
  - the fix (clamping the path to the card's own box) moved the spawn origin 53 px in one
    format, caught by the choreography gate;
  - the clamp skipped the one frame where the card was exactly box-sized (float equality);
  - straight-alpha comparisons failed on rounded corners;
  - a padded label box sat off-frame by design for a giant word.
  Run the full pipeline early and often; review the output, not the plan.
- **Critics converge on rules and diverge on taste.** Two model reviewers agreed on
  every engineering blocker. They disagreed on whether real-pixel motion can match a
  reference built from live screen recordings. That is an owner decision: build the
  reversible version, watch it, then decide whether recordings are worth their cost
  (demo data, a privacy pass over every on-screen handle, new claims approvals).
- **Never keep a production's workspace in a temporary directory.** A reboot wiped
  `/tmp` and with it the tools, assets and candidates. The workspace was rebuilt by
  replaying every file-writing step from the session transcript (about 1,100 steps, path
  substituted) and proven by the approval hashes: the tool trees matched their old
  fingerprints, a re-run of the speech model reproduced the pinned transcript byte for
  byte, re-downloads matched their pinned hashes, and two identical renders showed the
  remaining difference was run-to-run matte noise (about 1 KB per file). Work in a durable
  folder, and keep the hashes that make such a recovery provable.
- **Snapshot before you edit a working pipeline:** the whole tree with a per-file
  inventory, restored into a fresh folder and checked for no extra and no missing files.
  Extracting an archive over the old tree is not a rollback: it leaves new files behind.
  Delete the snapshot (it holds approval records) once the final is exported, with a date.
