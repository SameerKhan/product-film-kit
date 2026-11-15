# Rebuilding a film on a teammate's cut, with real product output

A designer on the team made their own 60 s version of a launch film in a motion tool. The
owner liked its structure more than the approved 91 s film and said: take the good parts
of their video and build our version on the real product. This page covers the 13 versions
that followed over two days, in four formats, reviewed by the owner and the designer in
turns.

It sits on top of `rework-after-feedback.md` (notes into viewer problems, real exports,
gate conflicts) and `polish-review.md` (full-size frame review). Read those first. Every
rule here names the failure behind it.

**Nothing on this page ships as a script.** Build each check in your own pipeline and show
it failing on a planted defect (`qa-gates.md`) before trusting it.

## 1. What to take from the teammate's cut, and what to rebuild

- **Take the structure, the timings, the copy framing and the visual rules.** Their hook,
  the order of features, the scene start times, one short headline per feature, the place
  the music drops out and the look of the background all carried over. Write their scene
  start times down as a list and build to it.
- **Their headlines are new copy until the owner approves them.** Every line goes through
  the claims check like any other: it is on the landing page, or it gets a dated,
  owner-approved entry in the copy list (`copy-and-claims.md`). Two of their lines were
  in neither and were still open questions for the owner when the files were handed
  over. That is a third disclosed gap: a line with no approval fails the claims gate, so
  the owner approves it in writing or it comes out before the film is published.
- **Rebuild every product picture.** Their product screens were redrawn in the motion tool
  ("UI rebuilt at 1.6 to 2x"). Redrawn screens showed a control the product does not have
  (a spelling check). Every picture in the new film is a recording or an export from the
  real product.
- **Check their music edit twice: the licence, then the source.** First, the licence must
  allow cutting and rejoining the track (`music.md`); a no-remix licence rules their edit
  out whatever it sounds like. Second, the edit must come from your licensed file. That
  is shown by records, not by ear: their project holds the same source file as yours
  (identical hash) and an edit list naming the stretches used. Here it did. Comparing two
  renders can only show that they sound alike, never where a file came from. Without the
  source file and the edit list, cut your own edit from the licensed file to their
  timings.
- **Do not reuse sound effects that came bundled with their tool** unless you can show the
  licence. Section 7 builds replacements.
- **Never run a teammate's project scripts, and read only what the owner cleared.** You
  cannot tell from a file listing what is private, and opening a file to find out is
  already too late. Ask the owner (or the teammate) for a clean copy that holds only the
  spec, the timings and the assets the film needs, or for a written list of the files you
  may open. Do not follow links that point outside it, and keep private paths and
  people's names out of your notes. The archive here had paths from another operating
  system and scripts nobody had reviewed.
- **Ask for the project folder, not the rendered page.** The shared preview page did not
  allow downloads, and timings read off a video are guesses.

## 2. Design-led, not screen-led

The first rebuild put the real screens where the redrawn ones had been. The designer
rejected it in one line: it looked machine-made. Their reasons, and the fixes:

- **The same sample business in every scene.** One bakery appeared in templates, sizes,
  background removal and the report. The story still follows one post from the first
  line to "scheduled" (`story.md`); that post keeps its business. Scenes that show the
  product's range (the template wall, brand kit, background removal, retouch) use other
  kinds of business and other photos, so range looks like range.
- **Panels cut off at the card edge, and dense screens nobody could read.** Not every
  scene needs product chrome. Show the *result* large (a real export) on a simple card,
  and show a control only when the press is the point. The owner's wording became the
  rule: simple illustrated cards and icons, real exports as the pictures.
- **Show each export at its real shape.** Square and 2:3 exports had been squeezed into
  4:5 cards. Read each export's pixel size and lay the card out from it.
- **Use the product's own icon for the feature.** A generic pencil was swapped for the
  icon the product ships for that feature.
- **An empty-looking result is a failure even when it is real.** A report scene showed
  one slide with little on it. It now shows three slides with their numbers.

## 3. Real output means every asset the product would load

- **Serve every asset the product needs from approved local files.** Template photos
  drew as orange placeholder boxes in every take. The harness had never answered the
  editor's request for library photos. The harness stays deny-by-default (`capture.md`):
  add each needed kind of request to the allowlist with a local fixture taken from the
  product's own files, keep everything else blocked, log the kind and id of every request
  (never headers or tokens), and fail the take if an allowlisted kind goes unanswered or
  a placeholder is drawn.
- **A saved brand kit recolours everything.** With the kit on, every template took the
  kit's teal and the variety vanished. Record varied templates in a session without the
  kit, and the brand scene in a session with it.
- **Features have limits; find them before you storyboard.** The editor offered
  background removal and retouch only on a standalone photo, not on a photo inside a
  template frame. The plan had assumed both.
- **A forbidden word can sit inside a real screen.** One real list in the product named a
  competitor. Use a different real screen; do not paint the word out.
- **When the product and the page disagree on a number, the owner rules, in writing.**
  The build had eight sizes and the landing page said seven. Neither number went in the
  film: the line became "Every size", as a dated owner-approved entry in the copy list.
  A font count was true only after a pending change shipped, so its entry carried a
  condition, and the release checklist said: check it shipped, else use the old number.
  It shipped, and that was checked, before the final files were handed over.

## 4. Never put hand-made designs under an AI-feature headline

One scene's headline says the product turns your caption into a design. The designs the
feature really made from the film's photos were not good enough to post.

- **Do not design better ones by hand and show them under that headline.** That is a
  claim the product cannot keep. Tell the owner, with the real outputs side by side.
- **Give the owner the real choices:** cut the scene, change the headline to something
  the product does do, or hold the film for a product fix. The owner chose to hold.
- **Write up the product fault with the evidence:** the input caption and photos, the
  three exports, the build they came from, and what a postable result would need. Draft
  the ticket and file it only when the owner agrees (`polish-review.md`).
- **When the fix ships, prove which build you recorded.** Record the commit you built
  from, and tie it to what is deployed with the release record or deploy manifest. Where
  the site serves the built asset under a content-hashed name, fetching it and matching
  the hash is a good second check; it is not possible on every site.
- **The owner decides which outputs are good enough, from stills.** Show every output at
  the size it appears in the film and record the ruling for each. The fixed feature
  offered three new layouts. Two were good and one was weak. The scene shows three posts
  made from three photos, using only the two good layouts (one of them twice); the owner
  and the team were told the weak one was left out.
- **The words must be the feature's real words too.** In this production the layouts were
  the product's real output, but the words on them came from a fixed test reply, because
  the AI text step was not run live. The review page said so in plain words and the owner
  was told when the files were handed over. That is a disclosed gap, not a pass: before
  such a film is published, record one real response for the exact approved input inside
  the spend limit (`rework-after-feedback.md`, section 2), rebuild the scene from it, and
  gate it again.

## 5. The post a scene ends on must be one a brand would share

Background removal and retouch each end on a finished post. It took three rounds:

1. Real output of the caption feature from the cut-out photo: real, plain, rejected
   ("people won't share these").
2. Library templates with the photo swapped in the editor: rejected. The frame clipped
   the person's head, and the second post was flat.
3. Two new designs after looking at how current speaker posts and beauty posts are laid
   out: approved.

What made round 3 work:

- **Look at current posts of that kind first, and write down what they share.** The owner
  names the platform and the kind of business to look at; a dozen recent posts is
  enough. Speaker posts: the cut-out person anchored at the bottom with headroom, one
  bold shape behind, a large display headline. Beauty posts: warm neutrals, a large light
  serif, the portrait in a soft frame. Take the layout ideas, never the posts.
- **Make the design with real steps in the real editor** (`rework-after-feedback.md`,
  section 2), so the film never shows a result the product cannot produce. This
  production cut a corner here: the two layouts were written as files in the product's
  own design format, opened in the product, given their photo with the product's own
  Replace control and exported by the product. The owner was told exactly that. Opening a
  file proves the product can render the design, not that a customer can build it. Treat
  that as a disclosed gap, not a pass: before the film is published, rebuild each such
  post with real steps in the editor, export it, and gate the scene again.
- **Size the frame to the cut-out's own shape.** A frame with a different aspect cropped
  the head.
- **Before and after share one framing.** The product re-fits a cut-out, so the raw photo
  had to be positioned to match or the head jumped.
- **The photo leaves as the post arrives.** A post laid over the photo read as clutter.
- **No made-up web addresses that look like test data** on a post the viewer is meant to
  admire.

## 6. Pacing: a result needs time to be seen

The owner watched the cut and said two scenes were too fast. Every automated check had
passed.

- **A before, an action and a result need about 3 s.** Both scenes were 1.8 s. They are
  now 3.0 s and 3.4 s.
- **Do not play a recording much faster than 1.6 times real speed** when the viewer must
  follow it. One ran at 2.4 times.
- **Hold the finished result for most of a second** before the cut; here 0.8 s or more.
- **These three numbers are one owner's rulings on one film, not constants.** Use them as
  starting floors (3.0 s, 1.6 times, 0.8 s), have the owner confirm or change them after
  watching, and record the confirmed values as the gate's thresholds. The reading rule
  (`qa-gates.md`) still applies on top.
- **Pay for the time from the longest earlier scenes, a little from each.** Every scene
  after the lengthened ones, the ending and the music's later hits stay where they were.
  The shortened scenes and the ones between them do move: re-measure each of their new
  starts against the track's onsets (`change-an-approved-film.md`). Five scenes gave 0.4
  to 1.2 s each; the scene that gave most is the one to re-watch.
- **If earlier scenes cannot give enough time, stop and ask.** The choices are to cut a
  scene, shorten another, or move later scenes and re-measure every hit against the
  track (`change-an-approved-film.md`). The owner picks.
- **Add the check you were missing.** For every scene with a result: scene length, the
  recording's speed factor, and how long the result is fully on screen, each against the
  recorded threshold. Plant a 1.8 s scene and a 2.4 times clip and show the check failing.
- **A re-timed film is a new candidate.** Render every format, run every gate, review the
  frames, and get the owner's approval again before any file is called final.
- **Say what you did not watch.** Frame strips prove order and holds. They do not prove
  the motion feels right; only a person watching does.

## 7. Sound made in-house

- **Generate the effects** (ticks, clicks, pops, whooshes, a low hit, a two-note chime)
  from noise and sine recipes, so no effect needs a licence. Keep each recipe in the
  build, and name the cached file by the recipe's hash.
- **Effects carry any stretch where the music is silent,** so they play louder there and
  quieter under the track.
- **Reset timestamps before you trim the mix.** A trim placed straight after the mix cut
  the sound short, because the mixed stream's timestamps did not start at zero. Pad every
  input that is shorter than the film to the full length, mix, reset the timestamps, and
  only then trim to the film's length so a long track cannot overrun the picture.
- **Leave headroom before the lossy encode, and gate the encoded file, not the mix.** A
  mix limited close to full scale and encoded to AAC at 192k came out 2 to 5 dB over its
  limit, and adding a second limiter made it worse. Lossy encoding adds overshoot at any
  bitrate; a higher bitrate only made it smaller here. Keep the kit's order (`qa-gates.md`,
  the loudness row): normalise loudness to the target first, keep a true-peak margin of a
  few dB before the encode, then measure integrated loudness and true peak on the encoded
  file and fail the build if either is off target. The masters measured -14.0 LUFS and a
  true peak of -2.9 dBTP after encoding at 256k.
- **Every other encode needs the same check.** A small web copy of the same film, with
  its sound re-encoded at about 160k, measured +0.8 dBTP. Copy the master's sound stream
  into web copies instead of encoding it again, or gate each copy.

## 8. Narrow formats

- **Keep platform overlays off anything the viewer must read.** The designer asked for
  the bottom 11% of the tall formats and a margin on each side to stay clear. Treat that
  as one team's ruling: use the per-format safe areas in `qa-gates.md`, ask the owner
  which platforms matter, and record the bounds as numbers the gate can test.
- **An old narrow-only variant silently overrides a new clip.** A scene kept showing last
  round's clip in the tall formats. List every per-format override and delete the stale
  ones at the start of a round.
- **An entrance that starts after the scene's exit stays on screen** into the next scene.
  Check each entrance time against the scene's end in every format.
- **Text presets land on top of the subject.** Check where the product puts new text
  before you record the step.

## 9. One review page for everyone

- **One page, one link, for the whole production.** The owner and the designer both keep
  that link. Each version replaces the videos at the top and adds a dated note that says
  what changed and what is still open.
- **Give every version's web copies a new file name.** Reused names showed cached old
  video.
- **When you message a reviewer, name the version to skip.** They may still be on the one
  before last.
- **Know who can open the page.** A page of an unreleased film should be limited to named
  reviewers. Test it: open the link in a private browser window with no sign-in; it
  must refuse. If the owner chooses to share it by link, record that choice, keep anything
  private off the page, and remember it updates for everyone the moment you publish:
  decide whether a reviewer should see a version before you publish it, not after.
- **State honest limits on the page:** what is stubbed, which output was left out and why,
  what is not for posting yet.
- **When a version is chosen, trim the page to it** and keep a copy of the full page with
  the production.

## 10. Final files for upload

- **Check the colour range of the masters.** Frames rendered as JPEG and encoded directly
  made full-range video. A player that ignores the full-range flag shows it with the
  wrong contrast: crushed blacks and clipped whites. Convert the pixels from full to
  limited range in the encode (8-bit 4:2:0, fast start, sound copied untouched). Then verify
  the pixels and all four tags, because both can be wrong on their own: the luma of a
  pure white frame reads 235 in 8-bit video, not 255; range reads limited; and matrix, primaries and
  transfer all read BT.709. In one encoder version the primaries and transfer options
  were silently not written when they followed a scale filter; setting them in the
  filter chain or with a bitstream filter worked. Compare frames from a dark, a bright
  and a saturated scene against the master, decoding both to RGB, within a similarity
  threshold you record. Better still, fix the range in the render so no second encode is
  needed.
- **Converted delivery files are new bytes.** Run the gates on them and have the owner
  watch and approve them, not just the candidate they came from.
- **Name delivery files for the person uploading,** not for the build, and say which
  format goes to which platform.
- **Restate every open release gate when you hand the files over,** even if the owner has
  heard them: music licence, a private test upload to see whether the platform flags the
  track, the legal check, any claim that depends on a change still shipping.
- **Final files come only from an approved candidate.** If anything changed after the
  last approval, it goes back through gates, review and approval first.
- **Keep the last approved version as a fallback,** and move old drafts to the trash
  rather than deleting them.

## 11. Tooling traps from this production

- **A watcher's test must first prove the planted process exists.** A cleanup test
  "passed" while a local web server it had started stayed up for over an hour; the search
  by name had not matched the renamed process. Record the process id and process group
  when you start something, check the id still belongs to what you started (start time,
  command), and stop only that. Never match by name or folder alone; that can hit another
  session's work.
- **A wait loop that searches for a script's name matches itself.** Poll the recorded
  process id instead (a shell's `wait` only works on its own children), and check each
  time that the id still belongs to the process you started.
- **Scratch folders are wiped between sessions.** Keep the production and the review page
  source in the production folder, not in scratch. Approvals and an independent backup
  still live outside the build sandbox (`pipeline-ops.md`).
- **Shells differ.** In one common shell `$name:flags` applies a modifier to the variable,
  and an unquoted variable holding several words is not split into words. Write `${name}`
  and do list handling in a script language.
- **Bind the checks to the files they checked.** The render writes a manifest of each
  candidate's hash and its inputs' hashes; the checks refuse a candidate that does not
  match it, and exit non-zero on any failure.
