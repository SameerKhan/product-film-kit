# Rules, and the failure each one prevents

## Story and pacing
- **Hook = pain + product + brand, from frame 0.** A slogan over a mascot did not
  stop anyone; a blurred product frame behind the pain line did. Payoff by about 2 s.
- **One continuous journey, not a feature list.** "Frame flies in, headline, next"
  repeated for 30 s read as a catalogue. Match cuts that carry an object across
  (the approved card becomes the post that publishes) read as a story.
- **Shots average 2 to 4 s; sections are 2 or 4 bars.** A measured 6.3 s average
  shot was the main reason a 62 s cut felt slow.
- **Word budget.** About 90 words for 50 s. Long page sentences forced 4 to 10 s
  static holds.
- **One hero move per film** (for example a spotlight lift of one card). Reusing it
  cheapens it.
- **Promotional copy may drop negative caveats only when the owner decides**, and
  only if what remains is still true.
- **Cover feature categories, not every detail.** "Everything on the page in 50 s"
  is mathematically unreadable; group the long tail into one card or a 90 s explainer.

## Music and sound
- **Measure the track before the storyboard.** Per-bar energy shows lifts and
  breakdowns. A track that looked right by ear had a 15-bar breakdown that would
  have put the call to action on quiet music.
- **Big turns on measured lifts; the ending not in a breakdown.**
- **Every slide start gets an audible accent of at least 6 dB above the 300 ms
  before it.** A cut where 7 of 9 transitions sat on flat or falling music was
  called "monotonous".
- **Peak-align every SFX.** Library SFX start with 50 to 900 ms of silence, so hits
  placed at the cue time land after the beat. Shift each cue by its own time-to-peak.
- **At most 3 big impacts.** Everything else is ticks, pops, sweeps.
- **Duck the music about 3 dB for 300 ms under big hits**, and 6 dB for 2 beats
  before the biggest reveal (a breath). Ducking is mixing, not remixing.
- **Respect "no remix" licences**: one continuous excerpt from one in-point.
- **A gate that combines music and SFX can be gamed**: measure the music alone for
  lifts (M1) and the SFX onset separately (M2), then a human listens (M3).

## Copy and claims
- **The landing page is the claim source.** Every on-screen string is page copy, a
  shortened page phrase the owner approved, or a closed list of system strings.
- **Conditions stay attached and visible** for the whole time the claim is visible.
- **Lists must be exact.** If the page says "publish to 12 platforms" and two
  messaging apps are inbox-only, they cannot appear in the publish grid.
- **Status truth.** A frame showing a Pending approval is never animated to Approved.
- **Integrations get a "Works with" label**, or they read as customers.
- **Third-party logos need owner clearance**, and customer-logo claims must be current.

## Typography
- **Break by phrase**: each phrase is its own `display:block; white-space:nowrap`
  span ("Still chasing / client approvals?"), never wherever the width runs out.
- **Reading rule R per text node**: on screen at least `0.3 s x words + 0.9 s`,
  measured from the entrance of the last element of a block.
- **Logo contrast**: switch the wordmark to solid white on coloured backgrounds.

## Visuals
- **Never AI-generate product UI.** Real app or design-file exports only.
- **Empty scenes get illustrations**: one consistent style, no text, no logos, no UI.
- **Real footage**: short micro-interactions on beats; keep the app's honest demo
  banner; tag cards "Real app" and "Sample data".
- **Before calling a product feature broken, check which component the route
  renders.** A commented-out handler in a legacy component was wrongly reported as
  a broken drag-and-drop that worked fine in the live component.

## Operations
- **Disk gates before every heavy step**; a full disk breaks other people's work.
- **Clean up on SIGTERM, not just Ctrl-C**: killed runs leave browser temp profiles.
- **Package caches inside the scratch folder**, empty registry config, install
  scripts off except the named steps; record the resolved versions.
- **Pin every external tool and asset**, hash it, and keep a licence ledger.
- **Owner decisions are explicit and recorded**; never fake reviewer consensus.
