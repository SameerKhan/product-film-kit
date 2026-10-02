# Illustrations and icons

AI-generated illustrations are fine for page components (hero art, icons, scene
dressing). They are never used for product UI.

## Brief (reuse verbatim for a consistent set)
> Soft 3D clay-style object(s), matte clay material, smooth soft studio lighting,
> premium SaaS marketing look, palette: <primary>, <soft tint>, cream, one deep
> accent. Centered with generous margins, soft contact shadow. Background plain
> flat <page colour> (or pure white for icons on white cards). Absolutely NO text,
> NO letters, NO numbers, NO logos, NO brand marks, NO user-interface screens.
> Square 1:1.

## Which scenes
- Hook: the pain as an object (a knot of envelopes and chat bubbles).
- Each feature card: one small icon (domain, palette, login, email, roles, stages, 2FA).
- Long-tail or trust scenes: one hero object group (padlock + shield + key).
- Never on a status moment where the art could imply something untrue (no
  "approved" stamp on a pending approval).

## Placement grammar
A three-model design review of the case-study film turned these into rules:
- **Supporting object (300 to 360 px)** in a split scene: directly under the
  headline block, its visible left edge on the text's left edge. Generated art has
  10 to 18% built-in padding, so offset the box by that padding, not the image.
  Never a free corner: a corner object reads as decoration added afterwards.
- **Focal object (300 to 340 px)** inside a diagram (a ring of icons): centred on the
  diagram's optical centre, which is not the box centre when the art is lopsided.
- **Feature hero (about 600 px)** next to a stack of cards: its visual centre on the
  stack's centre line.
- **Small accent (about 200 px)** in a centred-headline scene: beside the headline.
- **The wordmark lane is reserved.** Nothing sits under or touching the logo.
- **Every placement value must be generated, never a literal**: in the case study a
  missing `f` prefix sent `{L(120, 340)}` to the browser as CSS, and the scene only
  looked roughly right by accident. Grep the built HTML for `{` inside `style=`.

## Producing
Any image model works. With the Codex CLI on a ChatGPT plan, `image_generation` is
built in: `codex exec --ephemeral -s workspace-write -C <empty-dir> "Use your image
generation tool to create <file>.png ..." < /dev/null`. Write access is needed to save the
image, so point `-C` at an empty folder made for the art, never a repo or your home folder. Run several in parallel; review all side by side for style
drift and stray text; downscale to about 800 px; hash them; use
`mix-blend-mode: multiply` on matching backgrounds.
