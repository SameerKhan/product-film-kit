# Capturing a real re-skin (white label, themes, tenant branding)

Use this when the signature moment is "your product, in someone else's brand":
white-label, custom themes, per-tenant branding. The rule that never bends: both
states are **real renders of the shipped app**. The film may transition between
them; it may not paint one of them.

## How a white-label app usually decides its brand

Read the source before planning; do not assume. In the case-study app:

- **Mode by hostname.** Any host that is not one of the vendor's own domains (or
  localhost) puts the app in tenant mode.
- **The page itself changes for a tenant host.** The `index.html` boot script
  rewrote `<base href>` to a different asset path, so every bundle and stylesheet
  was requested from a path the capture's static server did not serve.
- **The branding arrives from a cache before any network call.** At boot the app
  applied a tenant config it had cached in browser storage (keyed by hostname, and
  accepted only when the cached domain matched the host). In the demo workspace the
  live branding fetch was skipped entirely, so the cache path was the one that
  branded the screen.
- **The brand is a palette, a logo, a name.** A full colour palette generated from
  one primary colour, a logo swapped into a few known surfaces, and a text rewriter
  that renamed the vendor's display name (case-sensitive, so URLs were left alone).

Your app will differ. The capture recipe below is the shape; the details come from
reading your own code.

## The capture recipe

1. **Serve the built app on a fake tenant host.** Use a reserved name
   (`app.<agency>.example`, RFC 2606, cannot resolve on the internet) and map it to
   127.0.0.1 in the browser only: Chrome's `--host-resolver-rules="MAP <host>
   127.0.0.1"`. Nothing on the machine's DNS changes.
2. **Use one fixed port**, so the sandbox can allow exactly it (see
   `pipeline-ops.md`).
3. **Treat both origins as first-party** in the request router (the vendor origin on
   127.0.0.1 and the tenant origin), keep everything else deny-by-default.
4. **Mount what the tenant page asks for**: the rewritten asset path mapped to the
   build root, and the agency logo on its own path, both with realpath containment.
5. **Seed the branding where the product reads it**, on the tenant origin only, and
   wait until the product has applied it (for example, the primary colour CSS
   variable equals the agency colour). Do not pre-compute what the product would
   compute (in the case study the palette function was not exported from the
   bundle); let the app do it.
6. **Capture the same screen twice**, vendor brand and tenant brand, same viewport,
   same clip, DPR 2.

## Gates that make it honest (all fail the capture, none just report)

- **No vendor asset in the tenant state.** Every visible `<img>` and CSS background
  inside the clip is checked against a pinned list of the vendor's brand files
  (derived from the build by filename pattern, not hand-listed), plus the vendor
  state's own logo URL.
- **No vendor display name in visible text.**
- **The agency logo and colour are applied** (computed style), even where the logo
  itself is off screen.
- **Negative control:** inject the real vendor logo into the tenant page; the check
  must catch it, or the run fails.
- **Big enough to be the moment:** the share of changed pixels between the two
  states (per pixel delta over 12) must clear a floor (4 % in the case study; the
  chosen screen changed 10.6 %).
- **Verified targets:** at least three surfaces that are clearly vendor-coloured
  before (30 % or more of the colour) and agency-coloured after (30 % or more, under
  5 % vendor colour, half the surface changed). These are the camera's slam targets.
- **Attestation:** source SHA, build-tree hash, the full source-tree hash before and
  after, hashes of every capture input and output, browser version. A failed
  capture writes its own dated record and never overwrites the last good one.

## What the case study learned

- **The logo was not on screen.** The app's demo banner covered the corner where the
  sidebar logo sits, and every capture clips below the banner. The owner was told
  before approving the pair, and the moment became the colour change. Do not remove
  a demo banner to get the shot: that is changing the product UI.
- **The re-skin found product bugs.** A chart line, metric icons and the assistant's
  branding stayed in the vendor's colour on a tenant domain. Report these to the
  product team as bugs; never crop them out silently or recolour product pixels.
- **Owner gates around it:** the owner chose the agency name and colour, checked (or
  waived) a name-collision search themselves, and approved the captured pair before
  any film work. The film then refuses to build if those files change.
