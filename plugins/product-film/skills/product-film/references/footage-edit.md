# Editing real footage: talking-head reels and recuts of an editor's video

The rest of this kit builds a film from screens, music and copy. This page covers
the other common job: a person on camera. A founder explains a launch, two
colleagues introduce a feature, or an editor has already cut a long video and you
need short vertical cuts from it. It was distilled from two such productions: a
two-person feature reel shot raw, and a founder's two-minute launch video that an
editor had already finished (b-roll, music, burned captions), recut into a
49-second reel in 9:16, 4:5 and 16:9. Most rules name the failure behind them; the
rest are techniques that worked.

**The checks on this page are not shipped as scripts** (the productions' scripts
were tied to their footage). Build each one in your own pipeline and show it
failing on its planted defect (see `qa-gates.md`) before the first cut is planned;
until then, nothing here is enforced. Controls that need a real frame (for example
a third-party inbox frame) run only after consent is recorded.

## 0. People first

- **Consent comes before any processing**, including transcription and the review
  of an editor's cut. Record, per person: the date, how it was asked, what they
  were told the footage is for, each channel (processing, organic posts, the
  website, paid ads), and how to withdraw. Colleagues must be free to refuse with
  no consequence; ask in a way that makes that true.
- **Bind consent to the exact recordings.** Store the sha256 of each source file in
  the consent record and refuse to process any other file. A consent record that
  names no recording let any video run under it.
- **Footage of faces and voices is sensitive working data.** Private workspace
  (mode 700, umask 077), outside any git repository and outside cloud-synced
  folders. Derived audio and stills are purged at every exit; the original
  recordings stay where the owner keeps them and are never pruned by the pipeline.

## 1. Review the editor's cut before touching it

If an editor already delivered a cut, the first deliverable (after consent) is a
short, measured review they can act on, in their own timecode. What it found on a
real cut:

- **Loudness.** The body measured about -19 LUFS with peaks at -0.1 dBFS, against
  a common delivery target of about -14 LUFS integrated and -1 dBTP: it plays quiet
  and the near-0 dB peaks can clip after a platform re-encode. Measure the body
  (trim the outro first): `ffmpeg -i cut.mp4 -t <body seconds> -af ebur128=peak=true -f null -`.
- **Captions.** One small white word at a time disappeared on white product
  screens. Phrase captions (2 to 4 words) on a solid box survive any background.
- **The brand name.** Run speech-to-text on the cut and read it: the transcript
  heard the brand name as a different word early in the video. Ask the speaker to
  listen; either re-take or trim.
- **Outro length.** A 10-second outro on a short reel; 2.5 to 3 s with the URL is
  enough.
- **Claims.** Check every spoken product claim against the product's capability
  list. The owner may keep a claim as their own statement, but record it as a
  decision, never as a silent pass.

## 2. Raw versus the editor's cut: measure the offset

- **Measure, do not assume.** On the real job the editor's cut was the raw footage
  shifted by a constant 120 ms. An editor may also retime, slip or stretch, so
  cross-correlate the audio envelopes (10 ms RMS) in a window around every range
  you reuse, not just one; disagreeing windows mean the offset is not constant.
  Record the measured offset in setup, so later runs compare against it rather than
  re-learning it.
- **External mic audio versus camera audio**: the raw mic file and the audio
  embedded in the raw video correlated at 0.999 at a 35 ms offset (encoder
  padding). Use the embedded track; it is already in sync with the picture.
- **Lip sync by machine is weak.** Automatic mouth-opening versus audio correlation
  was inconclusive; filmstrips of plosives ("b", "p") were the useful evidence. The
  owner listens and decides.
- **A frame diff between the two files does not isolate the editor's overlays** when
  the editor colour-graded or reframed: every pixel differs. Find overlay bounds by
  looking at stills.

## 3. Cut points: the waveform decides, not the transcript

- **Transcript word times are approximate.** Whisper's were often 40 ms off and once
  240 ms early. Use the transcript for which words are said and in what order; take
  every boundary from the waveform. Cut points placed at transcript word ends clipped the last word of
  two lines on the first plan.
- **Every in and out sits in a measured quiet window**: 10 ms RMS on the 48 kHz
  source, room tone about -56 dB, quiet meaning at or below -50 dB. Choose the in
  at least 60 ms before the first word (the handle), and the out after the last
  word and before the next. The gate then checks the 40 ms just outside each cut
  (before the in, after the out): that is where a clipped or leaking word shows up.
- **Some joins have no silence.** Between two phrases, a breath and the first
  word's tail ran continuously at -40 to -46 dB. Cut at the local minimum with a
  30 ms fade, give that one join a written exception (its own limit and the
  reason), and never loosen the rule for the others.
- **Know how your renderer rounds lengths.** This pipeline floored each segment to
  whole frames (30 fps), which moved an out point up to 33 ms earlier, back into a
  breath. Choose the in point so the rounded out lands where you measured.
- **Caption only what is heard.** The transcript put one word inside a cut that the
  waveform showed was silent; captioning by transcript alone would have shown a
  word nobody hears. A word whose transcript end runs past the out point is not
  captioned, and the audio check after every out catches a word that really is cut.
- **Merge ranges that are contiguous in the source.** Two lines planned as separate
  cuts were one continuous take; splitting them added a jump cut for nothing.

## 4. Reusing the editor's b-roll

- **Measure where the editor burned captions before you crop.** The plan guessed
  y 740 to 800; the measured band was y 858 to 924 of 1080. Every crop must avoid
  that band, checked by geometry on every run. The check caught a crop that started
  7 px inside the band.
- **Crops come from a crop table** (id, rectangle in source pixels, the time window
  where the shot really shows that UI), reviewed as stills before the first build.
  A vertical crop can be tighter than the 16:9 one so small UI text grows.
- **Hold, do not stretch.** When the editor's shot is shorter than the line it
  illustrates, hold its first or last frame, for example
  `tpad=start_mode=clone:start_duration=0.6:stop_mode=clone:stop_duration=0.8`.
  Slowing or looping a UI recording changes its motion speed visibly.
- **Snap layout changes to caption boundaries.** A caption that straddles a layout
  change jumps position mid-phrase. Move each planned shot change to the nearest
  caption-card start.
- **Drop b-roll that cannot be read.** Floating cards in perspective with tiny text
  added nothing at any size; the speaker shot was better.
- **A shallow UI strip in an empty panel reads as a rendering mistake** (all three
  reviewers said so). The same strip floating over the speaker shot as a lower
  third reads as "typing a prompt".

## 5. Privacy in reused product footage

- **Editors record real accounts.** The inbox b-roll showed real people's handles
  and a stranger's message naming her role and organisation. Crop to first-party
  UI only (here: the composer line with the speaker's own prompt), and never show
  the list.
- **OCR alone fails open.** A word that is on screen for two frames, a short
  handle, an OCR variant, and a held frame (one image, many frames on screen) all
  slip through a text allowlist.
- **Review every distinct frame, then bind the cut to exactly those frames.** In
  setup, extract every source crop frame the plan puts on screen (decoded, before
  any scaling), group identical frames by hash, and have a person look at every
  distinct frame (contact sheets), not a sample: hashing records what was looked
  at, it does not look. Store the hash of each reviewed frame. The gate extracts the
  same frames on every run and fails on any frame whose pixels differ from the
  reviewed set: a changed crop, time window or source fails.
- **Prove the gate with the production code path.** The planted control must run a
  real third-party frame through the same function the gate uses (an earlier
  control tested a different predicate and could pass while the gate failed open).

## 6. Sound and layout

- **Raw mic recordings can arrive very quiet.** One measured -43.5 LUFS, and the
  cleanup chain (gate, compressor), tuned for a louder input, left the dialogue
  only 0.5 dB above the music. Measure the dialogue's integrated loudness first and
  apply a pre-gain to the level your chain expects (about -24 LUFS for this one).
- **No upscaling, in any format.** Speaker crops are taken at 1.0x (one source
  pixel per output pixel); UI crops are scaled at most 1.0x; the renderer refuses
  more.
- **The raw full frame shows the studio.** In 16:9 the editor's zoom had hidden a
  shelf and a light at the frame edges; an inner crop at 1.0x on a plain border
  removes them without upscaling.
- **Captions on an opaque box**, checked on the rendered frame. An earlier renderer
  drew the box at 92% opacity, so the background showed through.
- **Prompt cards for spoken examples.** When the speaker lists things they would ask
  the product, show each one as a card on its first spoken word, worded as spoken,
  and check each by OCR on the rendered frame.

## 7. Delivery, approval and retention

- **The owner approves a candidate; the final is that candidate.** Promote the
  exact files the owner watched (bound by the candidate manifest's hash) rather
  than re-rendering, and verify the copy, not just the source, before the move.
- **One manifest covers every other file in a final**, including the approval
  record (the manifest does not list itself), and export verifies it exactly: no
  missing files, no extra files, no symlinks.
- **Export finals only.** The first export accepted candidates, which would have
  copied unreviewed face and voice footage to a shared folder before the owner's
  review. A candidate is viewed in place.
- **Compare like with like.** The first final step compared a sources-only tool
  hash list with one that also held compiled binaries and refused every final.
  Check that today's tool sources and the candidate's own recorded tool sources
  both match the approved list.
- **Retention in code, with a truth table.** Candidates built before an accepted
  final go 7 days after it; abandoned candidates go after 14 days; derived scratch
  and logs go with them; build inputs and original recordings are never pruned;
  the candidate named for promotion is never pruned. The first version of the
  pruner keyed every candidate on the final's age and would have deleted the one
  waiting for approval, plus a build input; a confirmation review caught it.

## 8. Review lessons from these jobs

- **Each confirmation pass found a bug in the fix**: the pruner above, then a race
  where the named candidate could be pruned in the same run. Review the fix, not
  just the original.
- **Run state machines, do not read them.** Promotion, export and pruning were
  each proven with a truth table in a sandboxed home folder (missing approval,
  wrong candidate, planted extra file, world-writable approvals, tampered final,
  overwrite).
- **Plan rounds can contradict each other.** One round asked for a lead-in line to
  be restored; a later one called it awkward. Keep a ledger and answer with the
  earlier finding.
