# Case study: a 50 s agency hero film for Social Champ

Social Champ is a social media management platform. The film was made for its
agency and enterprise landing page: 50.4 s, 16:9 and 1:1, music only, no voiceover.

## What the owner rejected, and the rule that came out of it

| Cut | Owner feedback | Measured cause | Rule now |
|---|---|---|---|
| v3 (62 s) | "too slow" | average shot 6.3 s; long page sentences | shots 2 to 4 s; about 90 words; sections of 2 or 4 bars |
| v4 | "monotonous, no upbeat on new slides" | 7 of 9 cuts on flat or falling music; SFX landed 50 to 900 ms late because of lead silence | measure the track first; turns on lifts; peak-aligned hits; M1/M2 gates |
| v4 | "it's a promotional video" | a caveat line about the assistant making mistakes | promotional copy may drop a caveat when the owner decides |
| v4 | (review) | a messaging app shown in the publish grid; the page says it is inbox-only | exact lists; claims registry checks the grid |
| v6 | "screens look pretty empty" | text-only scenes | clay-style illustrations, no text or UI |
| v6 | "the logo gets mixed in the orange" | dark wordmark on brand orange | white wordmark on coloured scenes |
| v6 | "client is on the next line" | width-based wrapping ("Still chasing client / approvals?") | phrase spans, nowrap |
| v7 | "we don't need to say BETA", remove "Sample data" | owner waived both disclosures | waivers recorded, then enforced as forbidden strings |
| v7 | "Inbox supports more platforms" | inbox scene showed two channels | show the breadth the page claims |
| v7 | a white-label line "is too much text" | a full page sentence | a narrower shortened line |
| v8 | "screenshots are blurred, not crisp" | 1x captures scaled up for punch-ins | 2x state-sequence capture, zero-upscale and fidelity gates (style A) |
| v9 | owner asked for a version in the style of the company's earlier intro video | | chapter style (style B), cards on the standard reading rule |

## Choices that worked
- Track: 123 BPM, measured section lift used as the downbeat anchor; in-point
  chosen so the first lift lands on film bar 3. A different track was dropped
  because a 15-bar breakdown would have covered the call to action.
- Structure (bars): hook 2, approvals 4, composer 2, publish ring 2, inbox 2,
  workspace switcher 1, white label 4, report 2, assistant 2, governance 2,
  logos 2, end card with a button ending on the final hit.
- Real footage from a local build of the app at a pinned commit, with the app's
  own demo workspace, served offline with every API call mocked. The demo brand
  name collided with real businesses, so it was renamed in the source before
  building; client workspace names were invented and web-checked.
- Every gate passed on the final cut: -14.0 LUFS, -2.2 dBTP, music lifts 2.01,
  1.16, 1.24 at the three turns, slide onsets 6.5 to 12.2 dB, "Sample data"
  readable on every product frame, 0 old-name OCR hits.

## v8 and v9
- v8 (54.3 s) went back to the app: every still recaptured at 2x as state
  sequences, a cursor inside the camera layer, the real Approve click, a
  Listening scene, a named agency testimonial from the page, and governance
  dropped for time. It added the crisp, fidelity, cursor and hold gates.
- v9 reused v8's captures and timeline in the chapter style. Its review found
  chapter titles readable for under half a second, sound cues left on old
  timings after a retime, stickers out of hover order, a disabled gate check and
  a leak check that could not tell the probe page from the renderer. All are
  rules or gate lessons now.

## What it cost
Four model-critic rounds on the plan, one bake-off of two renderers, three
disk-space stops, and roughly a day of wall time. Most of the time went to the
music map and the capture harness, both now scripts in this kit.
