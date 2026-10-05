# Three proven styles

Both styles share the rules, the music-first structure and the gates. They
differ in how a feature is introduced. Pick one per film; mixing them reads as
two films stitched together.

## A. Crisp real-app (the "product is the hero" cut)

The product window fills most of the frame and the camera moves inside it.
It suits an audience that wants proof the product exists and works.

- **Capture at device pixel ratio 2 and never upscale a raster.** "The
  screenshots are blurred" came from scaling 1x captures up for punch-ins. Every
  still is captured at DPR 2 and the camera's zoom is capped so no raster is
  drawn above 1.0x its natural size (gate: zero tolerance, see `qa-gates.md`).
- **Animate state sequences, not video.** Capture one still per UI state (one
  per typed character for a caption being typed, one per hover for a switcher)
  and swap them on the timeline. Stills stay sharp under any camera move; a
  screen recording does not.
- **The cursor lives inside the camera layer.** Drawn outside it, the cursor
  drifts off its target as the camera zooms. Test: at every click the cursor tip
  sits within a few pixels of the target in the delivered frame.
- **Do the real action.** Show the real Approve click and the real Approved tab
  that follows, not a badge pasted on top.
- **Reframe instead of retouching.** When a capture shows something the owner
  does not want (a beta badge, a disclosure they waived), move the camera so it
  is out of frame; never paint over product UI.

## B. Chapter style (the "intro video" cut)

Built from the company's earlier intro video at the owner's request: bright
gradient background, a persistent brand pill, full-screen chapter cards and
playful stickers. It suits a first-touch audience.

- **Brand pill, top left, for the whole film.** The logo mark plus the current
  feature name ("Approvals", "Client workspaces"), updating per section. It
  replaces an eyebrow line: having both says the same thing twice.
- **Chapter cards: one bar, standard reading rule.** A full-screen brand-colour
  card with an icon and a 1 to 2 word title wipes in on the section's first
  downbeat. Title lands within 0.25 s, holds, and wipes away in the last 0.2 s of
  the bar. A first version gave cards 2 beats and a looser reading rule; the
  titles were readable for only 0.2 to 0.5 s. Cards obey the same rule R as
  every other node.
- **Not every section gets a card.** A section that already opens with its own
  colour takeover (here, white label on brand orange) puts its title inside the
  takeover instead; a card in front of it is two lifts in a row.
- **Typed headlines: type the lead phrase only.** Typing a whole headline at a
  readable speed eats the reading time; type the first phrase (about 36
  characters per second) and pop the accent phrase in. Headlines that must be
  read during a busy scene use the mask reveal instead.
- **Stickers follow the action.** Emoji or clay stickers pop in as the thing
  they stand for appears (a tooth when the dental client is hovered), in the
  same order. Stickers in a different order from the hovers read as random.
- **Chips are crops of the real UI**, never redrawn: a strip cut from the real
  capture (an "Approved" row) floats out as a chip.
- **One sound per card edge.** A swoosh in, a softer one out. A section start
  that already has a big hit does not also get a swoosh.

## Rendering facts both styles depend on

- **Hide with opacity, never `visibility`.** A child with `visibility: visible`
  is still painted when its scene's clip is hidden with `visibility: hidden`.
  Typed characters set visible one by one leaked into every later scene.
- **`immediateRender: false` on any GSAP `fromTo` that is not the first tween
  on its element.** Otherwise its start state is applied at time 0: a window
  was drawn at 0.94 scale for the first 15 s.
- **Emoji are PNGs, not an emoji font.** The colour emoji system font fails the
  renderer's font lint and renders differently per machine.
- **Use the logo file you mean.** A brand folder can hold several variants (a
  blue one sat next to the orange one); crop the mark from the canonical
  wordmark if no mark file exists.

## C. Problem-led story (the "aha" cut)

Built on style A's crisp captures, structured as buyer problems (see `story.md`):
a short pain line over a graphic "before", the real UI solving it with a camera push
on the action, a recap of every solved state, proof, and the ask. One signature moment
sits on the biggest music lift; in the case study it was the real app re-skinning to
an agency's brand (see `rebrand-capture.md`). It suits a landing-page hero whose job
is recognition ("that is my week") before features.
