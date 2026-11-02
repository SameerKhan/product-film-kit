# Make your first launch film, explained very simply

This page explains the whole job in small words and short steps, as if to a small child.
You do not need to know video editing. You talk to Claude, and Claude does the work.

The example all the way through is a real film: the launch film for the Design editor in
[Social Champ](https://www.socialchamp.com), a social media tool. It is about 90 seconds
long, it shows the real editor, and it is cut to one song. You can make the same kind of
film for your own product by following the same steps.

## The big idea, in one picture

A launch film is like a picture book with music.

- Each **page** of the book is a **scene**. One scene shows one thing your product does.
- The **music** is the clock. Pages turn when the music goes **boom**.
- The **pictures** are your **real app**. Never pretend pictures of your app.
- The **words** on each page are short, and they stay long enough to read.

That is all a launch film is. Everything below is how to do it carefully.

## What you need before you start

1. **Claude Code**, with this kit installed (step 0 in `recipes.md` shows how).
2. **Your product**, running on your computer, with pretend data in it (pretend names, not
   real customers).
3. **Your landing page**. Every word in the film must come from it, or be a word you say yes to.
4. **A song you are allowed to use.** Read its licence yourself.
5. **Space on your computer.** Four sizes of a 90 second film needed about 10 GB. Ask
   Claude to measure how much one render uses and to stop when free space is below that
   plus a few GB (it sets `MIN_FREE_GB` for the render script, which on its own only stops
   under 5 GB).

## Step 1. Tell Claude what the film is about

Say it like you would to a friend. Claude asks about anything you leave out.

> Make a launch film for our new Design editor. People can make a social post picture
> right inside our app. Show the real editor. About 80 seconds, bright and happy. Use the
> words on https://example.com/features/design. Never show a competitor's name.

**What Claude does:** reads your page, saves its words, and asks you a few questions.

**What you do:** answer the questions. If you are not sure, say "Recommended."

## Step 2. Pick the song first

The song comes before the pictures, because the song decides when the pages turn.

> Here is the song I want: [file]. Measure it. Tell me where it gets loud, where it gets
> quiet, and where the big booms are.

**What Claude does:** measures the song. It finds the beat, the bars (groups of 4 beats;
pick a song that counts in fours, the kind most pop songs are), the loud parts and the
quiet parts.

**What you do:** listen to the start Claude picks. It should be **bright from the very
first second**. A dark, slow start makes a happy film feel sad.

**Remember:** the biggest page turns go on the biggest booms. The last page goes on the
last big boom.

## Step 3. Plan the pages (the storyboard)

> Plan the scenes. One idea per scene. Put the big moments on the big booms. Show me the
> list with times before you build anything.

For the Design editor film, the pages went like this (no secrets here, only what the
editor does):

| Page | What you see |
|---|---|
| Hello | the brand and the editor, right away (in your film, put the buyer's problem here too) |
| Open | someone opens the editor from a post |
| Edit anything | someone changes the words, adds a photo, moves a layer, and the picture gets better |
| Post | the design goes into a real post |
| Brand | the company's own colours and logo |
| Clean-up tools | taking out a background, fixing a photo, picking fonts |
| Data | a chart that turns into a nice picture |
| Sizes | one design, many sizes |
| Save | saving it to post later |
| Ask | "try it", on the last big boom |

**Not a list of slides.** A film that is just "feature, feature, feature" gets boring. Make
the pages one trip: your first page shows the problem (for example, a plain post that
needs a picture), and the same design travels from page to page, getting better, until it is posted. Each
page hands its picture to the next one.

**What you do:** read the list. Cross out anything that is not true in your product today.

## Step 4. Take real pictures of your app

> Capture each scene from our real app on my computer, offline, with pretend data. Short
> clips, 1 or 2 seconds each. Show me the stills first.

**What Claude does:** opens your app in a locked browser that cannot reach the internet,
clicks through each scene and records it. It never signs up on your real website.

Three safety rules here, every time:
- **Pretend names are checked.** Claude searches each made-up name on the web, so it is not
  a real business by accident.
- **A small "Sample data" label** sits on every product picture, unless you say it may go
  (Claude writes your decision down).
- **A reader checks every frame** for real names and for that label.

**What you do:** look at every still. Is any real customer name showing? Is anything
broken? Say so. **A bug in your app is told to you, never painted over.**

## Step 5. Build the film

> Build the film from the plan. Render it in 16:9, square, 4:5 and tall 9:16.

The kit makes 16:9 and square by default. We asked for 4:5 (feeds) and 9:16 (stories and
reels) too, so ask for them if you want them.

**What Claude does:** writes the film as a web page with moving parts, then turns it into
video files, one for each size. A phone-tall video is not a wide video squeezed. Claude
picks what part of the screen to show in each size.

**What you check:** in the tall and square ones, can you **see the thing change**? In the
Design film, the moment the words popped back on top happened off-screen in the tall
version. The fix is to show the page, not the side panel, at that moment.

## Step 6. Add the sound

**What Claude does:** puts in the song as one long piece (no chopping), adds little tap
and whoosh sounds right on the beat, and makes it as loud as videos on the web should be.

**What you check:** do the clicks and booms happen **at the same time as** what you see?

## Step 7. Let the checkers look first

Before you watch, scripts check the film for you. Some come with the kit (words, reading
time, sound, every-frame text). Claude builds the others for your film (sharpness, cut-off
edges, frozen screens), and first proves each one catches a mistake planted on purpose.
Together they check that:

- every word comes from your page or your yes;
- every word stays long enough to read;
- no picture of your app is blurry or stretched;
- big moments sit on the music's booms;
- nothing looks cut off at the edges;
- nothing sits frozen for too long.

**Important:** a checker that says PASS can still be wrong. In the Design film, every
checker passed, and a person still found that the last boom had slid off the music.
So a person always looks too.

## Step 8. You watch and listen

This is the most important step, and only you can do it.

- Watch with sound, on a laptop.
- Watch it small and muted, the way it sits on your page.
- Watch the tall one on your phone.
- Watch **every** size you will use, 4:5 too. A size you did not watch is not approved.

Then tell Claude in plain words:

| If you feel | Say |
|---|---|
| it is too fast | "Too fast. Hold each screen one bar longer." |
| a screen looks chopped | "This screen at 0:42 looks cut. Fix the framing." |
| the ending feels weak | "Put the last click on the strongest boom near the end." |
| you love it | "Approved." |

Claude **waits for you before building again**. Making all four sizes takes hours, so
it is better to fix everything in one go.

## Step 9. Changing a film you already liked

You can add a page later. In the Design film, the owner added the "edit anything" page in
the middle, after the film was approved.

> Add a 4 bar scene (about 10 seconds) after "Open" that shows someone editing a design:
> change the text, add a photo, move a layer. Keep the same song. Keep everything else the
> same.

Ask for scenes in **bars**, not seconds, so the pages still turn on the music.

**What changes:** every page after the new one moves later, so every boom has to be
checked again. Read `change-an-approved-film.md` for why.

## Step 10. Sharing it

Nothing is posted anywhere until you say so. When you love the film:

> Approved. Make the web versions and a 15 second cut.

Those are **new files**, so you watch them too before saying yes to them. Saying yes to
the film is not saying yes to posting it. Posting is its own yes, at the end:

> Approved for publishing: [the exact files].

Before you say that, check: the song licence is in your company's name, every feature in
the film is really switched on for customers, and a test upload does not get flagged for
the music.

## The ten rules, very short

1. Real app pictures only. Never AI pictures of your app.
2. Pick the song first.
3. Big moments on big booms.
4. One idea per page.
5. Short words that stay long enough to read.
6. Pretend data, never real customers.
7. Pick one text colour for each background colour and keep it everywhere (ours: white on orange).
8. End on something beautiful your customer would post.
9. No "not approved" stickers burned into the video. Ask in chat instead.
10. You watch and listen before anything is shared.
