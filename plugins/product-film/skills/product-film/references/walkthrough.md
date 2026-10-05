# Step-by-step walkthrough, and worked examples

This is what making a film with `/product-film` looks like from your side: what you
say, what Claude asks, what it runs, what you get, and what to check at each stop.
The timings are from the case study (a 54 s agency hero film).

## Before you start (10 minutes)

- Your landing page URL (the film may only say what the page says).
- Access to a local build of your web app, or design-file exports if you cannot run it.
- A licensed music track, or a licence you can buy from (Claude helps choose).
- Decide who signs off. That person answers the questions marked **You decide**.
- On a Mac, install `ffmpeg`, Node 22, Python 3 and Google Chrome; Playwright comes
  from your app's own dev dependencies or `npm i -D playwright`.

## Step 1. Brief (5 minutes)

**You say:**

> Make a 50 second hero film for our agency page at https://example.com/agencies.
> Our buyers are agencies running 10 to 50 client accounts. Use real screens from the
> app, and cut it to an upbeat track. Square version too.

**Claude does:** saves the page's visible text as `copy.txt`, the only claim source,
and lists your rules: brand colours, fonts, disclosures, things never to show.

**You decide:** anything that must never appear (a beta tag, a customer name, a
competitor), and whether the demo-data label stays on screen.

## Step 2. Story (20 minutes, the most important step)

**Claude asks:**
1. Which three or four problems do your buyers have, in their words?
2. Two or three pain lines per problem (4 or 5 words each), for you to pick from.
3. The signature moment: one thing the product does that a buyer would remember.
   It must be real in the product today.
4. One client name to carry through the film, or none.
5. Which features to drop. Every feature that does not solve one of the problems goes.

**Example answers from the case study:** problems: chasing approvals over email,
clients mixed in one calendar, the vendor's branding showing to clients, report day.
Pain lines: "Still chasing client approvals?", "Clients mixed in one calendar?",
"Still showing vendor branding?", "Another client report due?". Signature moment: the
real app re-skinning to an agency's brand. Client: Quillhaven Coffee (a fictional
demo brand). Dropped: publishing, inbox, listening, the assistant character.

See `story.md` for why this structure works.

## Step 3. Music (15 minutes)

**Claude runs** for each candidate track:

```bash
python3 scripts/music_map.py track.mp3
python3 scripts/music_map.py track.mp3 --in 8.048 --bars 28   # the film's bars for a chosen in-point
```

It prints tempo, beat phase and one line per bar with an energy bar chart and the
lifts and drops. Claude proposes an in-point so the first lift lands at the end of
the hook, and rejects tracks whose breakdown would cover the call to action.

**You decide:** the track, after hearing auditions cut from the real in-point.

## Step 4. Plan, critiqued (30 to 90 minutes)

Claude writes the plan: the storyboard on the bar grid, every line with its reading
time, the captures needed, the gates, and what the scripts may and may not touch.
With `/tri-plan` (or another model available) the plan is critiqued twice: once for
"is it right" and once for "is it safe to run".

**You decide:** the open decisions the critics leave for you. Typical ones: the pain
lines, the client name, who approves the scripts, any exception to a check.

**Check:** the reading-time table passes for every line (`scripts/reading_rule.py`).

## Step 5. Capture the real screens (30 to 60 minutes)

Claude adapts `scripts/capture/harness.mjs` to your local build: every API call is
answered by fixtures, everything else is blocked, demo data only, renamed to
fictional names you have web-checked (`scripts/rename.py` on a scratch copy).

```bash
node scripts/capture/harness.mjs survey     # one still per route + a network report
```

Then it captures each scene as a sequence of 2x stills, one per UI state (a hover, a
click, each typed character). For a re-skin moment it captures the same screen in
both brands (`rebrand-capture.md`).

**You check:** the survey stills. For a re-skin, Claude shows you the two states side
by side and how much of the screen changes. **You decide:** which screen.

## Step 6. Mock-ups and illustrations (20 minutes)

For each "before" scene Claude draws graphic mock-ups (shapes only, no text, never
your UI): an unread-email pile, a jammed calendar, a report scramble. Illustrations
(clay or flat style, from an image model) fill any scene that is only text.

**You check:** a still of every mock-up. Ask for a second round if they are not
dramatic enough: "push them further" worked in the case study.

## Step 7. Build and rehearse (1 to 2 hours, mostly unattended)

Claude generates the film from the bar-indexed timeline, renders both formats and
runs every check (`qa-gates.md`) in a **rehearsal** that can never publish. Failures
are fixed in the film or, often, in the checker itself; a threshold is never lowered
without your yes.

```bash
HYPERFRAMES_VERSION=0.8.106 bash scripts/render.sh compositions/land film 1500
python3 scripts/mix.py cue-sheet.json          # music + SFX + loudness gates
python3 scripts/ocr_gate.py film.mp4 checks.json --ocr build/ocr
```

**You check:** a contact sheet of stills at every beat, before the final run.

## Step 8. Sign off and deliver (1 hour, unattended)

**You decide:** approve the scripts (Claude prints one command for you to run, or you
delegate it, and the delegation is recorded). Then the real run delivers:

- `film-land.mp4`, `film-sq.mp4`, `film-land-web1080.mp4`, `film-land-web720.mp4`,
  `film-sq-web.mp4`, `film-poster.png`, and a manifest of every input and script hash.
- It lands in a candidate folder until you give the embed size.

**You check (no script replaces this):**
1. Watch with sound on headphones and on a laptop.
2. Watch muted, at the size it will sit on the page.
3. Watch the square version.
Then say where it goes. Publishing is always a separate approval.

## Step 9. Cut-downs (30 minutes)

> Make a 15 s and a 6 s cut for ads, and a 9:16 version for stories.

The 15 s keeps the hook, one problem with its fix, the signature moment and the ask;
the 6 s keeps the signature moment and the ask. Same checks, same sign-off.

## Feedback that works

| Instead of | Say |
|---|---|
| "make it better" | "it looks nice but has no wow: what would make an agency owner stop scrolling?" |
| "it's slow" | "cut every shot to 2 to 4 s and move the turns onto the music's lifts" |
| "it's boring" | "show the pain instead of naming it" or "push the camera in on every click" |
| "the screens look bad" | "the screenshots look soft: are any of them enlarged?" |
| "too much text" | "shorten this line, keep it narrower than the page line" |
| "the music feels off" | "which cuts sit on flat or falling music?" |

## Worked examples

**1. Problem-led landing-page hero (the case study).**

> Make a 50 s hero for our agency page. Build it as four problems our buyers have, each
> shown before and solved in the real app after. One signature moment on the biggest
> lift. Real screens only, square version too.

**2. A single feature launch, 30 s, crisp real-app style.**

> We just shipped bulk scheduling. Make a 30 s launch film: the problem in one line, the
> real flow (pick 20 posts, set the slots, approve), the result, the call to action.
> Crisp style, pin-sharp screens, cut to a 120 BPM track.

**3. A brand introduction in chapter style.**

> Make a 45 s intro film for new visitors in the chapter style: a title card per
> feature, the brand pill top-left, playful stickers, our three core features only.

**4. A white-label or theme re-skin moment.**

> Our app supports custom branding per workspace. Capture the same screen in our brand
> and in a fictional agency's brand on a fake tenant host, and use the switch as the
> signature moment on the bar-12 lift. Show me the pair before you build anything.

**5. Re-render after a product change.**

> The approvals screen changed in this week's release. Recapture only that scene from
> the new build, re-render, and re-run every check. Keep everything else identical.

**6. Pre-launch, no app to run yet.**

> The feature is not built yet. Use our design-file exports for the screens (never
> AI-generated UI), label them "Preview", and keep every claim on the page's roadmap
> wording.

**7. Ads from an approved film.**

> From the approved hero, make a 15 s and a 6 s cut and a 9:16 version. Keep the hook
> and the signature moment, end on the call to action, same loudness target.

## Doing it by hand

Every script prints its usage at the top of the file. A minimal run with the files in
`examples/`:

```bash
cd plugins/product-film/skills/product-film
python3 scripts/reading_rule.py examples/nodes.example.json      # every line long enough to read?
python3 scripts/music_map.py your-track.mp3                      # tempo, bars, lifts, drops
python3 scripts/claims_gate.py film.html copy.txt examples/claims.example.json
python3 scripts/mix.py examples/cue-sheet.example.json           # after editing the paths
mkdir -p build && swiftc -O scripts/ocr.swift -o build/ocr      # macOS: the OCR helper
python3 scripts/ocr_gate.py film.mp4 examples/ocr-checks.example.json --ocr build/ocr
```

## When something goes wrong

| Symptom | Usual cause | Fix |
|---|---|---|
| "The screenshots look blurred" | a 1x capture scaled up for a punch-in | capture at 2x, cap the camera zoom, run the zero-upscale check |
| Cuts feel off the music | turns placed on flat or falling bars; SFX with lead silence | re-map the track; peak-align every SFX |
| A frame flagged empty | a scene change where the window leaves before the next element arrives | start the next element a tenth of a second earlier |
| A layer shows in the wrong scene | a child set `visibility: visible` outlives its hidden parent | hide with opacity; hide a shot's layers at its end |
| OCR finds nothing in the sandbox | Apple Vision needs warming outside the sandbox first | warm up outside, then probe a known frame inside |
| A text check misses a word that is clearly there | OCR returned a Cyrillic or Greek lookalike letter | fold lookalikes to Latin before matching |
| Several holds score the same | ffmpeg kept an existing temp file (no `-y`) | one file per extraction, pass `-y` |
| A brand change "passes" with the wrong brand | SSIM cannot tell brands apart at wide framing | check colour on the surfaces that change, with an inverse control |
| The toolchain check fails after an update | a package manager upgraded a pinned binary | confirm the source, get sign-off, write a new baseline |
