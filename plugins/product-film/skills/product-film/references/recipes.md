# Recipes: the exact messages to type, step by step

Each recipe is the sequence of messages you type into Claude Code, in order. After
each message, the line below it says what Claude does and what it will ask you. Edit
the parts in angle brackets. You can stop after any step and pick up later: Claude
keeps the plan, the decisions and the files on disk.

`/tri-plan` and `/tri-review` (plan critique and code review by two other models) come
from [model-crosscheck](https://github.com/SameerKhan/model-crosscheck). Without them,
type "Critique this plan once for correctness and once for safety" and "Review the
film code for bugs before I sign off" instead.

## 0. One-time setup (terminal)

```bash
brew install ffmpeg node@22 python        # macOS; any package manager works elsewhere
cd <your project folder>
claude                                     # start Claude Code
```

Inside Claude Code:

```text
/plugin marketplace add SameerKhan/product-film-kit
/plugin install product-film@product-film-kit
```

Check it is there:

```text
/product-film
```

Claude replies with the workflow and asks what film you want. You can then follow
any recipe below.

---

## Recipe A. Problem-led landing-page hero (about 50 s)

The case-study film. Allow a day, most of it unattended.

1. **Brief**

   ```text
   /product-film Make a 50 second hero film for <https://yoursite.com/page>. Our buyers are <who, e.g. agencies running 10 to 50 client accounts>. Build it as the problems they have, each shown before and solved in the real app after. Landscape and square.
   ```

   Claude saves the page copy as the claim source and asks for your rules.

2. **Rules**

   ```text
   Never show: <a beta tag, real customer names, competitor names>. Brand colour <#hex>, fonts <names>. The demo data label <stays / may be dropped>.
   ```

3. **Problems and pain lines**

   ```text
   The problems are: <1>, <2>, <3>, <4>. Suggest two or three short pain lines for each, in the buyer's words.
   ```

   Claude proposes lines that fit the reading rule. Pick one per problem:

   ```text
   Use: "<line 1>", "<line 2>", "<line 3>", "<line 4>". Drop every feature that does not solve one of these.
   ```

4. **Signature moment**

   ```text
   What should the signature moment be? It must be real in the product today.
   ```

   Claude proposes options (for an agency product: a white-label re-skin). Answer:

   ```text
   Go with <option>. Carry one client through the film: <fictional client name>.
   ```

5. **Music**

   ```text
   Find two or three upbeat tracks with a licence that allows web and ads use, measure them, and play me auditions from the real in-point.
   ```

   Claude maps each track and explains where the lifts fall. Pick one:

   ```text
   Use track <n>.
   ```

6. **Plan, with a critique**

   ```text
   /tri-plan the film
   ```

   (Or, without that skill: "Write the full plan, then critique it once for correctness and once for safety before showing me.") Claude returns the plan and the decisions the critics left open. Answer each, or:

   ```text
   Approve with your recommended defaults.
   ```

7. **Capture**

   ```text
   Capture the screens from a local build of the app, offline, with demo data. Show me the survey stills first.
   ```

   Look at the stills, then:

   ```text
   Looks right. Capture the state sequences.
   ```

8. **Before scenes**

   ```text
   Show me stills of every "before" mock-up.
   ```

   If they feel flat:

   ```text
   Push them further: more chaotic and dramatic, still no text.
   ```

   When they work:

   ```text
   Approve the mock-ups.
   ```

9. **Build and rehearse**

   ```text
   Build the film and run a rehearsal: render both formats and every check, but publish nothing. Show me a contact sheet of every beat.
   ```

   Claude fixes anything the checks find. If a check needs an exception, Claude asks you; answer per item (for example "extend the waiver for that one tile").

10. **Review before sign-off**

    ```text
    /tri-review the film code
    ```

11. **Sign off and deliver**

    ```text
    Print the approval command.
    ```

    Paste it into your terminal yourself, or delegate:

    ```text
    You do all.
    ```

    Then:

    ```text
    Run the delivery and open the folder when it is done.
    ```

12. **Your review**

    Watch it with sound, muted at the size it will sit on the page, and the square version. Then:

    ```text
    The embed size is <width x height>. I watched it muted at that size: approved. Promote it to final.
    ```

    Publishing stays separate:

    ```text
    Prepare it for <the landing page / ads>, but do not publish until I say so.
    ```

---

## Recipe B. Single feature launch (about 30 s, crisp real-app)

1. ```text
   /product-film Make a 30 second launch film for <feature> on <https://yoursite.com/feature>. Crisp real-app style: one problem line, the real flow, the result, the call to action. Landscape and square.
   ```
2. ```text
   The flow to show is: <step 1>, <step 2>, <step 3>. The result is <what the user sees at the end>.
   ```
3. ```text
   Never show: <anything>. The call to action is "<button text>".
   ```
4. ```text
   Pick an upbeat track around <120> BPM, measure it, and put the reveal of the result on the biggest lift.
   ```
5. ```text
   Capture each step as 2x stills from a local build, offline, demo data. Show me the stills.
   ```
6. ```text
   Build it, push the camera in on every click, and run the rehearsal. Show me a contact sheet.
   ```
7. ```text
   Run /tri-review, then print the approval command.
   ```
8. ```text
   Run the delivery and open the folder.
   ```
9. ```text
   Approved at <embed size>. Promote to final.
   ```

---

## Recipe C. Brand introduction (about 45 s, chapter style)

1. ```text
   /product-film Make a 45 second introduction film for first-time visitors to <https://yoursite.com>. Chapter style: a title card per feature, a brand label naming each one, playful stickers. Our three core features are <1>, <2>, <3>.
   ```
2. ```text
   Brand colour <#hex>, wordmark <file or URL>. Stickers must match these actions: <list>.
   ```
3. ```text
   Measure two tracks and give each chapter card exactly one bar on a lift.
   ```
4. ```text
   Capture the three features from a local build; illustrations are fine for any scene with no product screen, but never AI-generated product UI.
   ```
5. ```text
   Show me a still of every chapter card and every sticker before you render.
   ```
6. ```text
   Build, rehearse, /tri-review, then deliver to the candidate folder.
   ```
7. ```text
   Approved. Promote to final.
   ```

---

## Recipe D. A white-label or theme re-skin moment

Use inside Recipe A or B when the product supports custom branding or themes.

1. ```text
   Read the app's source and tell me exactly how it decides a tenant's branding: the hostname rule, the asset paths, where the branding is cached and applied.
   ```
2. ```text
   Pick a fictional agency name and a colour far from ours. Show me a code-drawn logo for it. I will check the name is not a real agency.
   ```
3. ```text
   Capture the same screen in our brand and in the agency's brand on a fake tenant host, offline and sandboxed. Fail the capture if any of our logos or names leak into the tenant state.
   ```
4. ```text
   Show me the pair side by side, how much of the screen changes, and any surface that kept our colour.
   ```
5. ```text
   Use <screen> for the signature moment on the <bar n> lift. Report any surface that kept our colour to the product team as a bug; do not crop it out.
   ```

---

## Recipe E. Re-render after a product release

1. ```text
   The <screen> changed in this week's release. List every scene in the film that shows it.
   ```
2. ```text
   Recapture only those scenes from the new build, same states, same camera. Show me the new stills next to the old ones.
   ```
3. ```text
   Re-render and run every check. Keep everything else identical.
   ```
4. ```text
   Run /tri-review on what changed, then deliver as a new candidate.
   ```

---

## Recipe F. Pre-launch, nothing to run yet

1. ```text
   /product-film Make a 30 second teaser for <feature>, which is not built yet. Use our design-file exports for every screen (never AI-generated UI) and label them "Preview".
   ```
2. ```text
   Here are the exports: <folder or Figma link>. Use only claims from <the roadmap page or the approved announcement text>.
   ```
3. ```text
   Measure a track, build it, run the rehearsal and show me a contact sheet.
   ```
4. ```text
   Approved. Deliver to the candidate folder.
   ```

---

## Recipe G. Ad cut-downs from an approved film

1. ```text
   From the approved film, make a 15 second cut and a 6 second cut, plus 9:16 versions of both.
   ```
2. ```text
   The 15 s keeps the hook, <one problem> with its fix, the signature moment and the call to action. The 6 s keeps the signature moment and the call to action.
   ```
3. ```text
   Same checks, same loudness target, captions burned in for sound-off viewing.
   ```
4. ```text
   Show me all four, then deliver to a separate ads folder. Do not upload anywhere.
   ```

---

## Short replies that move things along

| When Claude asks | You can answer |
|---|---|
| a decision with a recommended option | "Recommended." or "Approve with defaults." |
| to see stills before building | "Show me." |
| a style call (looks flat) | "Push it further." |
| a check exception | "Extend it for that one item only." or "No exception; fix it." |
| to sign the scripts | "Print the command." (you run it) or "You do all." (recorded delegation) |
| to publish | "Not yet." (nothing leaves the machine until you say so) |
