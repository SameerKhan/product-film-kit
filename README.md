# product-film-kit

**Make a 30 to 60 second product launch video with Claude Code**: the kind of
short, music-driven film that sits at the top of a SaaS landing page, built
from your real product and cut to the beat.

You describe the product and point Claude at your landing page. The `/product-film`
skill walks Claude through the whole job (music, storyboard, screens, render,
sound mix) and checks the result with scripts before you see it.

It came out of a real production: a hero film for
[Social Champ](https://www.socialchamp.com)'s agency page that went through nine
versions. Cuts were rejected as "too slow", "monotonous", "empty" and "blurry",
and every rule in this kit exists because a cut failed without it.
[Read the case study](plugins/product-film/skills/product-film/references/case-study.md).

## Who it is for

- Founders and marketers who want a launch or landing-page video without hiring
  a studio.
- Developers who want the video built as code, so it can be re-rendered when
  the product changes.

You need Claude Code. You do not need video-editing software.

## Quick start

1. Install the plugin inside Claude Code:

   ```bash
   /plugin marketplace add SameerKhan/product-film-kit
   /plugin install product-film@product-film-kit
   ```

2. Ask for a video, for example:

   > Make a 45 second launch video for our landing page at https://example.com.
   > Use real screens from the app and cut it to an upbeat track.

   Or type `/product-film` to start the guided workflow.

3. Claude will ask you a few decisions along the way (which track, which
   style, what may or may not appear on screen) and show you the cut before
   anything is published.

## What you get

- A landscape (16:9) and a square (1:1) MP4, plus smaller web versions.
- Short cut-downs for ads (15 s and 6 s) once you approve the main film.
- The result of every check, so you can see what was measured.

## How it works

| Step | What happens | Why it matters |
|---|---|---|
| 1. Copy | Claude saves your landing page's text. Every word on screen must come from it or be approved by you. | The video never promises something the page does not. |
| 2. Music | The track is measured: tempo, and where the music gets bigger or quieter. | Scene changes land on the beat; the ending never lands on a quiet patch. |
| 3. Storyboard | Scenes are planned on the music's bars, with a word budget (about 90 words for 50 s). | Fast enough to keep people watching, slow enough to read. |
| 4. Screens | Real product screens, captured from a local copy of your app with all network access blocked, using demo data. | No fake UI, no real customer data, no test accounts on your live site. |
| 5. Build | The video is written as an HTML page with animations, then rendered to MP4. | Change a line, re-render; no manual editing. |
| 6. Sound | One continuous music excerpt, sound effects timed exactly to the beat, levels set for the web. | It sounds polished on laptop, phone and headphones. |
| 7. Checks | Scripts measure the sound and read every frame, and stop the build if anything is wrong (see below). | You review a film that already passed the checks, not a draft. |

## Two styles to choose from

| Style | Looks like | Good for |
|---|---|---|
| **Crisp real-app** | Your product window fills the screen and the camera moves around it: real clicks, real typing, pin-sharp. | Showing that the product exists and works. |
| **Chapter** | Bright background, a small brand label that names each feature, full-screen title cards between sections, playful stickers. | A first introduction to the brand. |

Details and the pitfalls of each:
[styles](plugins/product-film/skills/product-film/references/styles.md).

## The checks

Every one of these must pass before the film is shown to you. Most are scripts
in this kit; the screen checks are recipes in the
[checks guide](plugins/product-film/skills/product-film/references/qa-gates.md)
that Claude builds for your film.

- **Words**: every on-screen sentence comes from your page or your approval, and
  stays on screen long enough to read (0.3 s per word plus 0.9 s).
- **Sharpness**: no screenshot is ever enlarged beyond the size it was captured.
- **Accuracy**: what the film shows matches the real app (for example, a post
  marked Pending is never shown as Approved).
- **Names**: no real business or customer name appears in any frame (checked by
  reading every frame with OCR).
- **Sound**: the music builds where the story turns, every scene change has an
  audible accent, and loudness meets web standards (-14 LUFS).
- **You**: a final listen and watch by a person. No script replaces this.

## What you need

**Required**

| Tool | Used for |
|---|---|
| Claude Code | running the skill |
| `ffmpeg` | measuring music, mixing sound, checking frames |
| Python 3.9 or newer | the helper scripts (no extra packages) |
| Node 22 and [HyperFrames](https://github.com/heygen-com/hyperframes) | turning the HTML page into an MP4 (any deterministic HTML-to-video renderer works) |

**Optional**

| Tool | Used for |
|---|---|
| Playwright | capturing real screens from your app |
| A Mac with `swiftc` | the every-frame text checks (uses Apple's on-device text recognition) |
| An image model | illustrations for scenes with no product screen (never for product UI) |
| A licensed music track | Claude can help you choose, but you supply the licence |

## Ground rules the kit enforces

- **No AI-generated product screens.** Real app or design-file exports only.
  AI is fine for illustrations.
- **No test signups on your live site.** They pollute your analytics and CRM.
- **Licences respected.** Music that may not be remixed is used as one unbroken
  excerpt; every asset is logged with its licence.
- **Your decisions are recorded**, such as dropping a "beta" tag, and then
  checked so they cannot slip back in.

## Helper scripts

Claude runs these for you; you only need them if you want to work by hand. They
live in `plugins/product-film/skills/product-film/scripts/`, and each prints its
usage at the top of the file.

| Script | Does |
|---|---|
| `music_map.py` | measures a track: tempo, beats, where it builds and drops |
| `mix.py` | mixes music and sound effects and checks the result |
| `reading_rule.py` | checks every line is on screen long enough to read |
| `claims_gate.py` | checks every on-screen string against the approved copy |
| `ocr_gate.py` + `ocr.swift` | reads every frame to find required and forbidden text |
| `rename.py` | swaps demo names in a copy of your app's source |
| `fetch.sh` | downloads assets safely (https only, allowed hosts, hashed) |
| `render.sh` | renders the video with a timeout and clean shutdown |
| `capture/harness.mjs` | captures real app screens with all network access blocked |

## Learn more

- [All rules, and the failure behind each](plugins/product-film/skills/product-film/references/rules.md)
- [Music](plugins/product-film/skills/product-film/references/music.md),
  [copy and claims](plugins/product-film/skills/product-film/references/copy-and-claims.md),
  [capturing your app](plugins/product-film/skills/product-film/references/capture.md),
  [illustrations](plugins/product-film/skills/product-film/references/illustrations.md),
  [checks](plugins/product-film/skills/product-film/references/qa-gates.md)
- [Changelog](CHANGELOG.md)

## Contributing

Issues and pull requests are welcome. Run `bash scripts/check.sh` before
pushing (CI runs it too). A new rule should say which failure it prevents.

## Licence

MIT for this kit. Music, sound effects and logos you use have their own
licences: keep a record of each, and read the licence itself, not a summary.
