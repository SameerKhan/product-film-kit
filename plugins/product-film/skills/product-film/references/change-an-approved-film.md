# Changing an approved film: a new beat, four formats, the music still on time

What one production learned when the owner asked for a new 9.6 s beat in the middle of
an approved 79.2 s launch film, plus one colour rule across every scene, in 16:9, 1:1, 4:5
and 9:16. With 2.4 s more on one hold, the film grew to 91.2 s on the same track. The builder's gates passed. The
review found the final hit no longer sat on the music, and the new beat's payoff was
invisible in the three narrow formats. Rules name the failure behind them.

**Nothing on this page ships as a script.** Build each check in your own pipeline and show
it failing on a planted defect (`qa-gates.md`) before trusting it.

## 1. Inserting a beat moves the music under everything after it

- **Every later hit moves against the track.** The track keeps playing from the same
  in-point, so a scene that used to sit on a lift now sits wherever the track is 9.6 s
  later. List every hit, scene start and press after the insert and re-measure each one.
  Do not shift them all by the insert length and assume they still land.
- **Choose the insert length in bars, not from the content.** A five-bar insert put four
  approved scenes on weak bars. A four-bar insert plus one more bar on one settled hold
  kept six scenes on measured lifts. Report the hold you added as a change to an approved
  scene, because it is one. (This production counted a bar as 2.4 s, which is the error the
  next points warn about.)
- **Measure onsets on the track, not only bar energy.** The final hit moved onto a bar
  whose energy looked right, but its own onset was weak (0.32), with stronger onsets
  0.3 s and 0.6 s later. The strong onset the approved cut had used, a jump of about
  13 dB, now fell inside another scene with nothing happening on screen. Every gate
  passed it, because they checked the film's bar grid. Gate each hit on the music alone,
  never the final mix (its own sound effects would count as onsets). The kit's scripts do
  not measure this yet, so build it, for example:
  - decode the track excerpt to mono at 22,050 Hz;
  - frames of 2,048 samples with a Hann window, hop 220 samples (about 100 frames a
    second); take the magnitude spectrum and compress it as log(1 + magnitude);
  - onset strength per frame = the sum over all bins of the positive increase from the
    previous frame, divided by the excerpt's 99th percentile of that value;
  - the hit's strength is the peak within 50 ms either side of the hit;
  - FAIL if that is under 0.5, or if any onset within half a bar either side of the hit is
    more than 1.5 times stronger.
  These are starting numbers, not a standard, and a different onset measure gives
  different values. This production's own measure read the moved hit at 0.32 with a
  neighbour at 0.73, and the approved hit at 0.73, the strongest near it. Calibrate on your
  approved hit, prove the gate on a planted defect (that hit moved 0.3 s off its onset),
  and say where the track's biggest onsets now fall.
- **Never round the bar.** The track's bar was 2.412 s; the film's grid was 2.4 s. The
  error is 12 ms a bar and about 0.45 s by bar 38, enough to put a hit beside the music.
  Derive seconds from the measured BPM and phase (`music.md`), and re-check after any
  change in length.
- **Check the sound effects inside the new beat too.** Taps placed on the capture's own
  clicks landed 100 to 230 ms off the nearest strong onset. Either nudge the press to the
  onset or keep that tap quiet; report which.

## 2. A long real take inside a short beat: ramp time, do not cut

- This is a declared exception to the "short micro-interactions, never long walkthroughs"
  rule (`SKILL.md`): one continuous action whose point is that it is continuous. Record
  the exception, and after retiming re-run the fidelity and cursor checks on the result.
- The real editor take was about 13 s of source for a four-bar beat. Cuts would make the
  cursor jump. A time ramp kept one continuous take: action at about 1.25x (the
  speed the product's own popups run at), idle stretches at 1.5x to 4x, measured from
  frames before baking.
- **The end must be the polished result, held long enough to read.** The ramp left about
  1 s on the finished design; the pacing gate wanted 2.3 s. Budget the settled end first,
  then fit the ramp into what is left. Never shorten the payoff hold to pass a lifeless
  gate: propose a measured exception, and apply it only when the owner approves it.

## 3. Narrow formats: the payoff must happen inside the crop

- A wide editor does not fit in 1080 px. The narrow versions hard-cut between a crop of
  the side panel and a crop of the page. The beat's whole point was a layer moving back so
  the words came out on top, and both presses that did it fell on the panel crop. The
  viewer saw the dark photo, then a cut to the finished design. The change itself was
  never shown.
- **For each format, write down the frame where cause and effect are both visible.** If no
  single crop holds both, cut to the page crop before the press lands, not after.
- **Keep the planes on one left edge.** One square version had the page crop 67 px further
  right than the headline and panel, so the frame jumped sideways on every hard cut.
- **Check the end frame at the narrowest phone width** you expect (`polish-review.md`).

## 4. When an owner's colour rule fails a contrast gate

- The owner ruled that text on orange is always white. White on that orange measures
  about 2.9:1, under the 3.0 the contrast gate asks for large text. First offer a design
  that meets 3.0 (a darker orange or a dark band behind the words; type size and weight do
  not change the ratio). If the owner keeps the rule, **do not lower the threshold.** The
  gate still measures and prints each line's ratio. Record a waiver naming the owner, the
  reason, the lines, the formats, the measured ratio, the date and the film version it
  covers (it does not carry over to the next version unless renewed, `pipeline-ops.md`),
  and have the gate report WAIVED for exactly those lines. Any other line under 3.0
  still FAILs, and a waived line whose ratio gets worse FAILs too.
- Implement it as one rule on the class, not per line, and check every such line on stills
  of the final encode for what is really behind it. A line that lands on a light card
  moves; it is not recoloured back.
- If a gate only knew the old colour (a headline-clearance gate that read only dark ink),
  add the new reading, prove it on a planted defect, and report it as a gate change.

## 5. Rebuild safety: reused chunks, gate drivers, disk

- **A reused render must prove its inputs did not change.** The build reused a scene's
  rendered chunk when the scene's page hashed the same. The hash ignored the images and
  video the page loads, so a changed asset with the same filename would have kept the old
  pixels. Hash every input file's contents, and use a fresh run id each run so a stale
  chunk cannot pass as new.
- **The gate driver must fail when a gate fails.** One driver printed DONE and exited 0
  with FAILs in its reports. Exit non-zero on any FAIL or ERROR, and print the counts.
- **DETECTOR_BROKEN is not a pass.** The lifeless gate failed its own self-test on the
  wide version. A plain still-frame scan then found a 1.5 s near-static stretch in a
  data hold. When a detector is broken, run an independent check and look at the frames.
- **A gate that reads the source captures, not the encoded film, proves nothing about
  the film.** One continuity gate passed on some runs and read empty on others; it was
  reading capture images. Gate the delivered pixels.
- **A guard that skips cases must log what it skipped.** A new line that skipped boxes
  outside the frame stopped a crash, but nothing said which states went unchecked.
- **Check free disk before every render and stop under a floor.** Four formats needed
  about 10 GB. Measure your peak temporary use and set the floor above it plus a reserve
  (`render.sh` reads `MIN_FREE_GB`, default 5, which was too low here). Files moved to the Trash still take space until the owner empties it, and
  the agent does not empty it. Clean up the gates' own scratch when done and say how big
  it was.
- **Prove the four candidate files agree.** Same frame count, same duration, and one audio PCM
  hash in all formats, recorded next to each file's hash.

## 6. Review, then wait for the owner's ears

- Review the candidate encodes of every format, not just the wide one: the narrow payoff fault
  was only visible there.
- Ask reviewers different questions (walk the build as written, operations, audit the
  gates), not one prompt three times. If a reviewer is out of quota, say so and name who
  did review; never present two reviewers as three.
- **Do not rebuild before the owner has listened.** Each rebuild of four formats takes
  hours, and the owner's ear may change the same fixes (which onset to hit, how long to
  hold). Report the findings, recommend an order, and batch them.
- The rebuild is a new candidate: gates, review and the owner's approval again
  (`polish-review.md`). Publishing is a separate approval after that.
