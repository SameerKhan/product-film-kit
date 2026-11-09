# Reworking an approved film after the team watches it

The owner approved a 91 s feature launch film in four formats. Then the team watched it and
sent three notes:

- A decorative motif (the product photo inside circles, in every scene) meant nothing to
  them.
- The design the film ends on was not something they would post: its text was too small at
  phone size.
- Nobody knew one word in the copy.

This page covers the round that fixed those notes without losing the music, the formats or
the gates. It sits on top of `change-an-approved-film.md` (adding a beat, narrow crops, the
colour waiver, chunk reuse) and `polish-review.md` (full-size frame review). Read those
first. Every rule here names the failure behind it.

At the end, each format still had 1 to 3 raw gate failures. Every one of them had also
failed in the previous round (whose narrow formats had 8 to 10), and the owner was shown
each one before approving. That is not a pass: in this kit each such failure must become an
exact, recorded waiver that the gate reports as WAIVED (section 6). Reviewers found 11 problems in the build
tools: 9 were real and fixed, and the other 2 were refuted with evidence and the reviewer
agreed.

**Nothing on this page ships as a script.** Build each check in your own pipeline and show
it failing on a planted defect (`qa-gates.md`) before trusting it.

## 1. Turn each note into a viewer problem, then search every take for it

- **Name what the viewer loses, not what the reviewer disliked.** "The circles are
  irrelevant" became "the eye goes to a shape that is not the product". "Not postable"
  became "the end design fails the reading test at the smallest width it appears on screen"
  (here about 360 px wide in a 1080 px narrow format; ask the owner for the display sizes
  that matter on each platform). Each problem gets a fix and a check that
  would have caught it.
- **Search every take for an old word, not just the scenes the note names.** The unknown
  word was taken out of the main design, but it was still on screen in a different scene,
  inside a template the analytics view showed. That take had to be re-shot. OCR the
  candidate for every retired word before review.
- **Read the full plan back to the owner before re-shooting.** The plan said one scene would
  not be re-filmed. After seeing stills, the owner asked for it to be re-filmed after all,
  because it still showed the old word. Show stills of every scene that carries text you
  are changing, and let the owner rule on each one.

## 2. When the product's AI feature makes the design

- **Find out exactly what the AI does before you script it.** The feature looked like
  "AI designs the post". In fact the AI writes only the words (headline, kicker, body, a
  photo search term); the product's templates make the layout. A weak layout was not the
  AI's fault, and the film must not claim the AI did more than it does.
- **Finish the design in the real editor, with real UI steps.** The first end
  design was unreadable at posting size. The new one was made by 14 scripted steps in the
  product editor (set the photo as the background, delete a shape, retype the headline,
  change two colours and two sizes, add the logo from the saved brand kit). The same script
  then ran as one filmed take, cut into short beats and time-ramped where needed
  (`change-an-approved-film.md`), so the film shows a design a customer could really make
  without becoming a long walkthrough. Never paint the final design outside the product.
- **The film ends on a design someone would post.** The last design on screen is the one
  marketing will be judged by. Check it at the smallest width it appears in each format.
- **Record the AI call once, then replay it.** The filming sandbox replays a recorded AI
  response and refuses a different input, so retakes stay identical. A new caption needs
  one real call, made in its own sandboxed step outside the offline capture: a cleared
  environment, read access only to the approved input, network only to the approved
  provider, and the owner's approval of the provider and of exactly what is sent. It is
  recorded, then replayed. Keep the recording and its input next to each
  other, and treat a replay that accepts a different input as a fault.
- **Put a hard spend limit on every paid AI request.** Every request goes through one
  wrapper that holds a lock on its counter file, reserves the request's maximum possible
  charge (fixed output caps and a recorded price) before sending, refuses past the owner's
  approved counts or dollar limit, and settles the real charge after. A crash leaves the
  reservation counted, never refunded silently. The round stayed well inside its limit.
- **AI photos are allowed, AI product screens are not.** The product photo in the post was
  AI-generated, with a provenance file (prompt, model, date, cost, which one was chosen).
  Say so when you hand the film over (section 8).

## 3. Sources that cannot go stale

- **Stage assets by content hash, never by filename.** The composition copied assets into
  the previous round's frozen folder by name and never refreshed them. A changed image with
  the same name would have kept the old pixels. Stage into a folder owned by this round,
  keyed by each file's hash, and never write into a frozen folder.
- **Keep three baselines, each a list of files with hashes.** (1) Earlier rounds' files and
  shared inputs this round must not change, frozen at the start. (2) Files the owner approves
  during the round, added when approved. (3) Every capture and composition source, frozen
  when composition ends. Re-check (3) before each format renders, so all formats come from
  identical sources. Fixes during gate rounds change (3); record each change. After the
  owner approves, write (3) again from the sources the approved candidates were built from,
  keep the old list, and log both hashes. If any source differs from what built a
  candidate, that candidate is stale and becomes a new one.
- **Retire the previous round's launchers loudly.** This round's working copies of the old
  launch scripts print "retired" and exit non-zero, so nobody rebuilds the old round by
  habit. The frozen copy of the earlier round stays byte for byte as it was.

## 4. Narrow formats: more traps

`change-an-approved-film.md` covers payoffs inside the crop. This round added four more.

- **A plane disappears when its clip ends.** A chart that slid in vanished one frame after
  its source clip ran out. Every plane needs a hold segment to the end of its time on
  screen, and a check that each plane's clips cover its visible window.
- **Real takes can go blank under you.** In one take the side panel emptied once the result
  landed, so a narrow crop showed a white panel. The build held an earlier frame that still
  showed the controls. That puts the controls next to a result they never sit beside in the
  product, so treat it as a product fault (`polish-review.md`, `rules.md`): report it, and
  offer a retake, a product fix, keeping the truthful shot, or cutting the beat. Never crop
  around it. Hold the earlier frame only if the owner rules so, with the reason recorded.
- **A slide-in can hide the number the film is about.** A gate required a value ("1,186")
  to be readable throughout its window. A card that slid in hid it for 2 frames. A bigger
  card and a delayed slide only moved the gap. Popping the card in place fixed it. Test the
  exact frames the qualifier must cover after every change to that scene.
- **Small opposite drifts of real planes read as alive, and big ones break padding.** The
  lifeless gate counts only planes moving against each other; a whole-frame zoom is "camera
  only". Two product planes drifting apart by about 1 to 1.5 % of the 1080 px frame width
  passed it. Bigger drifts pushed content into the padding gate's edge margin. Calibrate the
  numbers for your own output size. A real state change in the product is still the better
  fix (`polish-review.md`); drifts only help a hold that must stay still to be read.

## 5. OCR false alarms: fix the frame, not the rule

- The forbidden-names OCR check had a handle rule (an @ or a copyright mark followed by a
  word). It fired twice in the tall format:
  - The orange press ring of a click, drawn over the word "at", read as "@at".
  - A tilted card showing a network name, a dot and the business name was read as a
    handle.
- The fixes were to the frames: a smaller close-up so the ring no longer sat on the word,
  and the card's rotation set to 0. The regex stayed strict. Loosening a privacy check to
  pass one frame lets a real handle through later.
- Add each false alarm to the planted-defect set as a frame that must pass, next to a real
  handle that must fail.

## 6. When gates disagree with each other, or with the music

- **Some gate pairs cannot both pass.** The UI-match gate needed a toolbar visible to match
  the product; the padding gate forbade content that close to the plane edge. That is an
  owner decision, not a tuning job. Show both readings and recommend one.
- **A payoff press and the beat can disagree.** The push gate measures the camera at each
  payoff action through the state change it causes. The owner kept one press on the musical
  hit, where the push could not hold through that change. The build took that target off
  the payoff list with the ruling recorded. Better: keep the target in the gate's list and
  have the gate report WAIVED for exactly that target, with its measurement and the
  decision reference. A target removed from the list is never measured, and looks like a
  pass. Do not move the click silently.
- **Label every exemption with who ruled.** Use "owner-accepted, decision N, date" or
  "OPEN, no owner ruling (carried from round N)". An agent first marked seven exemptions as
  covered by one new owner ruling. Four of them were older open items the owner had never
  ruled on, and were put back to OPEN.
- **Compare every remaining failure with the previous round.** Report each one as "carried"
  or "new", so the owner sees what this round made worse. Either way, before the final
  files are named, each failure is fixed or turned into a recorded waiver for that format
  and film version (`change-an-approved-film.md`, section 4). A general "approved" does not
  answer a specific open question.

## 7. Build tools: what review caught

- **A comment inserted in the middle of a line swallowed the code after it, twice.**
  - The first time, it caused a syntax error and the render failed loudly.
  - The second time, it silently disabled one animation, so a card stopped moving out of
    the way. Two reviewers caught it.
  - A parser check passes in the silent case. Never put code after a comment marker on the
    same line, and diff the generated timeline (or the tween list) before and after an edit
    that only adds comments.
- **The gate runner must check it is gating the right file.** The build asserts that the
  candidate's filename names the format being gated. A name proves little on its own: also
  check the decoded width, height, frame count and duration against the format, and bind
  the run to the candidate's hash.
- **Clean up only your own scratch.** The runner's clean-up removed more than its own
  outputs. Delete only the exact disposable scratch files the run wrote, in a folder the run
  owns, refusing links (`pipeline-ops.md`). Never delete raw reports, manifests, waiver
  reports or kept captures.
- **Keep the raw gate report.** Write the waiver-applied report as a separate file that
  names the raw report's hash and each waiver, so the printed counts and the files agree
  and the original failures stay on record.
- **Assert hold lengths.** A time ramp now asserts that its final hold is at least the
  settled-hold minimum the owner agreed (2.3 s here), so a later edit cannot shave it.
- Reviewers also claimed things that were not true. Check each claim against the code that
  was reviewed, and send a refuted one back once with the evidence.

## 8. Approval, final files and hand-off

- **Ask each open question with a recommendation.** The owner answered "do what you
  recommend". Record that as numbered decisions, one per question, with the date, so a
  later round can see exactly what was ruled. A question that was not asked is not
  answered by that reply.
- **Rename to the final name only after the owner has watched all formats** and every
  remaining failure has a recorded ruling. Check each file's hash before and after the move
  against the hash the gates ran on, log it, then write baseline (3) again (section 3). Leave other sessions' work folders alone.
- **Hand it to the team that will post it, and ask for approval to post.** The hand-off
  ticket held:
  - a table of each size and the platforms it is for;
  - the story in five steps;
  - what is real (every screen recorded from the product) and what is not (a made-up
    business, an AI-generated photo);
  - direct questions: approval to post, size per platform, whether to make a 15 to 30 s cut
    and what it keeps, captions and first lines, and one known issue for their opinion.
- **Notify people through a mechanism the tool really notifies through**, and read the task
  back to confirm it worked. In this production's tracker, assignees were notified and a
  name typed into the description was not; check how yours behaves.
- Publishing waits for the posting team's approval and the owner's separate yes.

## 9. The second round of notes

The posting team watched the reworked film and sent a second, shorter set of notes. The
fixes were small, but a three-model review of that round still found real faults. Most
are new here; the items that name an earlier rule (section 7, the claim registry, the
exit-status rule) add only the new evidence.

- **Show the product's real output for every size, never crops of one screenshot.** A scene
  promising "every post size" was built by cropping one screenshot into eight shapes. That
  shows a picture being cut, not the product resizing a design. Export each size from the
  real editor and write a manifest: the hash of the approved design the exports were made
  from, then one row per size with its id and file hash. Freeze the list of size ids the
  scene promises. The build refuses to run if the manifest's ids differ from that frozen
  list, if any export's recomputed hash differs from its row, or if the design hash
  differs from the approved final's entry in baseline (2), the owner-approved files
  (section 3).
- **Measure a lockup in the rendered frame, not in the code.** A feature name set next to
  the brand wordmark sat 13 px above the wordmark's baseline, its letters were visibly
  smaller, and the pair was off centre by 22 px. The CSS numbers all looked right. Measure
  the ink of the wordmark image (where its baseline and x-height fall), size and place the
  text from those measurements, then check a rendered still: baseline within 1 px, centre
  within 2 px.
- **A layout branch for one format can lose the animation.** A new narrow layout for one
  card was added as a separate branch of the build, and that branch never got the card's
  entrance step, so the card stayed invisible in the narrow formats only. In every format,
  not just the one you changed, check that each element scheduled for that format becomes
  visible inside its scheduled window (the rendered-events check in `qa-gates.md`, run per
  format).
- **Expected hashes carried from the previous round go stale quietly.** A capture checked
  the design it started from against the previous round's final hash, a constant left in
  the script, and failed for a reason that had nothing to do with the design. Read the
  expected hash from baseline (2) (section 3), never from a constant in
  the script and never from the live file being checked, which would bless any change.
- **Section 7's line-insertion trap came back a third time** (text inserted into the
  middle of a line swallowed the assignment after it). New evidence: after fixing it,
  rebuild the timeline and compare it byte for byte with the one that was rendered; that
  proved the fix changed nothing else.
- **Copy the owner asks for still needs its registry entry, at once.** The owner asked
  for a shorter end line. Both outside reviewers flagged it, because the claim registry
  (`copy-and-claims.md`) had no entry for it. Add the entry when the line goes in:
  `owner-approved` with the date, and the page sentence it rests on, so a reviewer can check the
  shorter line does not widen the claim.
- **When review calls a text card or a run of screens lifeless.** Here a card holding a
  line of text for nearly 2 s read as a frozen frame; a slow drift of about 1.5 % of the
  frame height over its time on screen was enough. Three product screens in a row read as
  a slideshow; merging two related beats into one shot fixed the rhythm without cutting
  content. These are remedies for what review flagged, not rules for every card.
- **A review leg that falls back must say so.** One reviewer ran on a backup model because
  its main model was out of quota. Name the model that actually ran in the report, so a
  reader does not over-trust the coverage.
- **The exit-status rule (`change-an-approved-film.md`) was broken again.** The runner
  printed every failure and exited 0. New evidence: plant a missing candidate and check
  the exit status itself, since reading the printed report hid the fault.
