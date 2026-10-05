# Story: from a feature catalogue to a film people feel

The case-study film went through three story structures. The gates passed on all of
them; only the story changed what the owner said about it. This file is the
structure that finally worked, and the measured reasons the earlier ones did not.

## 1. A catalogue is not a story

v10 was crisp and correct: nine features, about 5 s each, each with a headline and
a real screen. The owner's question was whether it gave a buyer an "aha". It did
not: the film opened on one real pain (chasing approvals), solved it, and then
became a list. Nothing carried from one scene to the next and nothing was at stake.

**Rule:** pick three or four problems your buyer already has, in their words, and
build the film as problem, then the real product solving it, then the next problem.
Drop features that do not solve one of those problems, however good they are.
(v11 dropped publishing, inbox, listening and the brand character this way.)

## 2. The shape that works

| Beat | What the viewer sees | What makes it work |
|---|---|---|
| Hook | the first pain line, product already on screen | product on screen from frame 0 |
| Problem N, before | a short pain line ("Clients mixed in one calendar?") over the problem itself | the problem is shown, not just named |
| Problem N, after | the real UI solving it, with the feature named once | real clicks, real states |
| Recap | every solved state side by side, one outcome line | the viewer sees the sum, not a fifth feature |
| Proof | logos or a quote the owner cleared | earned after the payoff, not before |
| Ask | one primary call to action, pressed on the final hit | the film ends on an action |

- **Pain lines are short questions in the buyer's words** (4 or 5 words), approved by
  the owner, because they are not page copy. Each must pass the reading rule in its
  slot; two 5-word lines in v11 failed it until a boundary moved by half a beat.
- **Carry one client through.** A small chip ("Client: Quillhaven Coffee") on the
  approval and the report scenes makes four features read as one agency's week.
- **Name the feature once.** A feature pill appears only in "after" scenes; the
  "before" lines carry no product name on purpose.

## 3. Show the pain, do not tell it

v11 put each pain line next to the product window, blurred. The owner: "looks nice,
but it doesn't have a wow effect". The diagnosis, in order of weight:

1. **A blurred screenshot is not painful.** The viewer must recognise their own bad
   day: a pile of unread email threads, a calendar where every client looks the
   same, a spreadsheet and a clock at 11:48 PM.
2. **The payoffs were small UI changes in a window a third of the frame wide.**
3. **Every beat had the same shape and energy**, so the film listed instead of built.
4. **There was no signature moment.**

v12 fixed all four:

- **Graphic "before" mock-ups, no text at all.** At these cut speeds a word cannot
  meet the reading rule (one word needs 1.2 s; a half-bar cut is under 1 s), and the
  pain line already carries the meaning. Shapes only: avatar circles, grey text
  bars, red unread badges, same-grey calendar chips with red clash rings, error-
  hatched cells, a clock face. They are generic (no real product's chrome, never
  your own UI faked) and the owner approves stills of each before the film is built.
  A gate proves they hold no text (see `qa-gates.md`, G-notext).
- **One signature moment, on the biggest music lift.** For an agency product the
  strongest one was white label: the real app re-skinning from the vendor's brand to
  the agency's, in place, with a sweep. See `rebrand-capture.md` for how to capture
  it honestly. The sweep is a film transition between two real renders; nothing on
  screen claims the product animates.
- **Push the camera in on every payoff.** At the Approve click, the hover on the
  third client and the Export click the camera goes to about 0.97 of its maximum
  sharp zoom, holds through the state change and pulls back within one beat (gate:
  G-push).
- **Escalate, and say what you measure.** "It builds" is not checkable. v12 states
  it as events per beat: hook 1, calendar chips 2 (on 8th notes), the slams trade
  rate for size (three camera slams onto the vendor branding), report cuts 1 then 2.
  Exact event times live in the generator and in the geometry, and a gate checks
  that every event visibly happens (G-render-events).

## 4. Frame the signature moment tight

The first v12 wipe swept the whole screen at a wide framing. In stills the colour
change covered so little of the frame that it read as a flicker while the
background change dominated. Frame the moment on the largest surfaces that change
(here: the active tab, the workspace toggle, the sort control), make the visible
part of the sweep span the whole transition (0.45 s), and pull back over a bar
afterwards to show the whole re-skinned product.

## 5. Things that look like story problems but are layout bugs

- A decorative pile that is behind the product window in one format (DOM order),
  and in front in the other. Give overlays their own layer above the window.
- A mock wrapper with zero size (its children are absolutely positioned): content
  gates cannot see it. Give wrappers an explicit size.
- The first frames of a "before": the window steps aside, the mock is still empty
  and the line has not risen yet, so the frame is background only (G-empty fails).
  Start the line's reveal a tenth of a second before the window leaves.

## 6. Questions to ask the owner, in this order

1. Which three or four buyer problems? In their words, not the page's.
2. The pain lines (offer two or three per problem; they need approval).
3. What is the signature moment, and is it real in the product today?
4. One client name carried through, or none?
5. What to drop: say it out loud, because every dropped feature is a feature
   someone on the team built.
