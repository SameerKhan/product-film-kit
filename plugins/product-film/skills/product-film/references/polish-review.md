# Polish review: getting a real-app film past "these screens look cut"

Scripted gates prove only the properties they measure. They do not prove a film looks finished. This page is
what closed that gap on one production: a 79 s launch film for a feature inside a SaaS
product, built from real app captures, with AI images only for non-product scenes.

The owner watched round 7 and said many UI screens looked cut and unpolished. Round 8 then
passed its gates and its builder's own inventory ("none found"), and frame reviewers still
listed 25 must-fix faults. Round 9 fixed 18 of them and added 9 new ones. Round 10 had no new
must-fix fault in review, and the owner approved it. Rules name the failure behind them.

"Candidate" below means the encode under review. Every re-render is a new candidate, and the
final is still the exact candidate the owner watched and approved (`rules.md`).

**Nothing on this page ships as a script.** The production's gates were tied to its build.
Build each check in your own pipeline and show it failing on a planted defect (see
`qa-gates.md`) before trusting it.

## 1. Who looks at what

- **Only stills of the current candidate count.** An inventory filled while building
  described earlier candidates. Fill it after the last encode, from frames extracted from
  that file, and record the file's hash. Say which frames were viewed, and that viewing stills is not
  watching the film.
- **Do the polish pass on full-size frames, not contact sheets.** Three earlier reviews used
  reduced sheets and missed faults that were obvious at 1920. This is about polish only:
  the every-distinct-frame privacy sheet in `footage-edit.md` still applies.
- **Split the film across reviewers, one per segment.** Each extracts 4 frames per second
  for their segment, opens at least one frame per 0.5 s, and steps through every transition
  frame by frame, because a cut object can flash for only a few frames. Sampling elsewhere
  can still miss a short fault: report what was sampled, not "clean". Use only reviewers the
  owner has allowed to see unreleased product frames.
- **Give them a list of what is already known, and require a frame path per finding.** The
  list stops repeats. The path stops invented findings. Tell them the segment may be clean,
  so they do not pad.
- **Grade every finding MUST, SHOULD or NIT, and verify each MUST on your own frame** before
  sending it back to the builder.
- **Re-check the last round's list against the new encode, row by row.** Use four verdicts:
  FIXED, GONE-WITH-THE-BEAT (the whole beat was cut, on a recorded decision),
  CHANGED-BUT-WRONG and STILL-THERE. In round 10, 28 rows came
  back 15, 4, 5 and 4. "Fixed" alone would have hidden the 5 that only moved the fault.
- **Re-review every rebuild.** Round 9's fixes created new faults, and only a fresh review
  on the new encode showed them.

## 2. Gates can hide what they should catch

- **Audit the gate changes as hard as the film.** Round 9 widened containers and declared
  two planes full bleed. The gates then went quiet on three real faults: a cropped grid, a
  pale line on the payoff and a sliced dialog. Restoring the containers brought the faults
  back into view so they could be fixed. A move to a container, threshold or exemption is a
  declared, measured exception the owner decides (`rules.md`), and a PASS after one stays
  unproven until someone has looked at those frames.
- **Sort every FAIL into REAL or FALSE ALARM, with a measurement.** In one audit a margin
  failure was a locator snapping to tile edges and a cursor (true margin about 10 css px),
  while a 6 px margin elsewhere was real. Fix the locator; never loosen the limit.
- **An exemption without proof is an open item.** Report it as unproven, not as passing.
- **NOT-RUN is never a pass.** A plane that was never found settled, or a headline that was
  never read, reports NOT-RUN.
- **Check what escapes a gate.** Images that no plane list named escaped both UI gates in
  this film. List the objects no gate covers, so a person knows to look at them.
- **Long sample windows can mask a dead stretch.** A check that passed over a 6 s window
  hid a screen that stayed rigid for most of it. The gate was then reporting less than the
  owner would see.

## 3. Two gates worth building

Each runs on delivered pixels, and each needs its planted defects. The numbers are what this
production used on a 1920 master: a starting point to calibrate on your own planted defects,
not a standard. Per-plane radius and css scale come from your build manifest, which only says
where to look; convert css px to film px with that scale, and scale the film-px limits to your
output width.

| Gate | Measures | Planted defect it must catch |
|---|---|---|
| Polish: corners | at settled frames of a rounded plane, the sliver of each corner outside the declared radius shows only the film behind, the plane surface or a blend of the two (colour distance within 24 of those, to allow for antialiasing and compression) | a dialog with capture background in its corners |
| Polish: padding | no content ink within 8 css px of a plane edge, unless the plane is a declared full bleed | a label touching the plane edge |
| Polish: headline clearance | at least 24 px at 1920 between the lowest headline ink and the plane below | a headline touching a plane |
| Polish: frame margin | a whole plane stays at least 32 px at 1920 from every frame edge, unless declared full bleed | a plane near the frame edge |
| Lifeless | register each sample pair (0.3 s apart) with one global zoom and pan, remove global brightness shifts, then classify: static, flat (camera only), cursor only, or alive. Thresholds used at 960x540: static means under 0.025 % of pixels change by more than 10 luma; flat means the residue after the rigid move is under 0.006 % of pixels at 16 luma; cursor means what remains fits about 72x80 px (a small real UI change can land here too, which errs toward failing, so a person looks at each failure). Fail on a run over the limit (used on a 100 BPM grid: static over 1 beat, camera only over 2 beats, cursor only over 1 bar). Mask only your declared caption overlays, so a caption cannot reset a dead run while a real UI text change still counts | a flat screenshot under a slow push; plus, on every run, synthetic frame pairs built from the film's richest frame (a still pair, a camera-only pair, a cursor-only pair and a pair whose panels move against each other), reporting DETECTOR_BROKEN if any is misclassified |

A slow push on a flat screenshot still reads as a dead screen. Do not pass the lifeless gate
with a faster moving backdrop: a backdrop circle was the only thing moving during one
data beat. The fix is a real state change in the product. The reading rule still applies: never cut a
hold short to pass this gate. Keep text readable and let something real change or move
during the hold, or declare a measured exception with its reason.

## 4. What the reviewers kept finding

**Cut UI**
- A panel cropped through a neighbouring row, or a thin sliver of the next row along its
  bottom edge.
- Capture background or a second frame showing around a dialog.
- A dialog sliced into two cards to save space. Restoring it exposed a truncated field that
  the slice had been hiding, so a crop can hide a fault as well as cause one.

**Motion and transitions**
- Dissolves between different scales read as double exposure. Prefer a clean cut. An iris
  that showed a wrongly scaled second copy of the photo was replaced by a hard cut.
- A zoom through a mask can show a hard-edged disc of the wrong scale for a few frames.
- An object that changes size and position across a cut reads as a jump.
- Flying objects cover the words being read. Clear them first: on a collage, the other cards
  left before the main card rose.
- Slow drift pulls planes out of line with the headline. Drift a group by one value, or
  start the plane offset so it rests on the margin.
- A background made of overlapping rays formed a ragged disc at frame centre. Look at it
  when nothing covers it.

**Cursor**
- It must travel. A cursor that appears already parked looks like a compositing slip.
- Click on the label or its centre, not the corner of the button, and not in the gap between
  two rows.
- Keep the click ring off the letters, or shorten it, so the label does not look damaged.
- Keep the whole arrow inside the frame.
- A click needs a visible result on the next frames.

**Consistency**
- The same object should keep one corner radius and one shadow across beats.
- A plate with square corners beside rounded cards reads as raw capture.
- A state the film shows being changed must not silently change back in the next beat.

**Non-product plates**
- A slowly drifting photo plate can bring a fragment of another object into a thin strip
  beside a panel. Check the last frames of each drift.

## 5. Product faults: report, decide, do not repaint

Filming exposes real product bugs: a truncated field, a low-resolution attachment
thumbnail, an overlay that stays on during a before-and-after comparison.

- Never repaint product pixels, and never crop in a way that misrepresents what the product
  does. A plain framing choice is fine.
- Trace each one to its cause in the code, so "small change" is a measurement.
- Put each to the owner as a decision: keep the shot, or fix the product and re-take. Give a
  recommendation. Draft one ticket for the product team, and file it when the owner agrees.
- If a beat exists only to show something broken, cutting it is a legitimate option. Record
  who made that call. When the owner has not ruled, the ledger says the agent's ruling, not
  "owner ruling". One builder wrote the wrong one, and it took a read of the ledger to catch.

## 6. Working with the owner's notes

- **Never burn a review mark into a frame.** A "Proposed line, not approved" tag on the
  film forced a re-render as soon as the line was approved, and the owner ruled that such a
  mark must never appear, even if it means asking first. Ask in chat and list the open items
  beside the cut.
  This does not cover a real disclosure such as a "Sample data" label, which stays until the
  owner waives it.
- **Use the track the owner named.** Remixed options built on the agent's own pick were
  thrown away when the owner asked why their track was not used. Audition alternatives only
  if asked.
- **Measure a track's tone, not only its lifts.** A track with a dark opening was rejected
  for a bright launch, though its lifts were in the right places.
- **"I didn't see it" means it isn't in the film yet.** The owner missed a beat that turned
  analytics into a chart, though the beat was there. Show the input becoming the result,
  large, with time to read it, and check that frame at each target embed width, including the
  narrowest phone width you expect (this film used 390 px).
- **"Too fast" gets a measurement.** Slowing down means settled time on each screen, one
  idea at a time. Report settled time per beat against an agreed rule, such as one bar, on top of the
  per-node reading rule and never in place of it. Holding longer does not help when the screen is unreadable, so fix the framing first.
- **Record an approval verbatim, next to how you read it.** A general "looks good" approves
  the cut. It does not by itself answer a specific open question you put to the owner. Ask
  about any you cannot settle from it, and keep each listed as open until they answer.
  Publishing stays a separate approval.
- **A re-render after approval is a new candidate.** Compare it with the approved file frame
  by frame, report any difference outside the intended boxes, and have the owner watch and
  approve it. That comparison is evidence for their decision, not a substitute for it.
- **Measure the renderer's own noise first.** Rendering one unchanged scene twice here gave a
  maximum difference of 43 of 255, so a diff means little without that control. A borderline
  gate also flipped from FAIL to PASS on a re-render with no timing change. That is not a fix.

## 7. Before release

Keep these on the list after the cut is approved. None of them is proved by a good-looking
film:

- the safe-area gate for each format, and the other formats and cut-downs;
- every feature flag the film depends on is really open, and the release that ships it merged;
- a music licence held by the company that publishes, not by a personal account;
- a test upload, unlisted and approved, to see whether the track triggers a content claim;
- legal review of AI-generated faces in a demo, and of any stock licence, and of invented
  numbers shown without a label;
- no frame of a real person goes to an outside reviewer.
