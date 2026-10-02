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

## Producing
Any image model works. With the Codex CLI on a ChatGPT plan, `image_generation` is
built in: `codex exec -s workspace-write -C <dir> "Use your image generation tool to
create <file>.png ..."`. Run several in parallel; review all side by side for style
drift and stray text; downscale to about 800 px; hash them; use
`mix-blend-mode: multiply` on matching backgrounds.
