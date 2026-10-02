# Real-app footage, safely

## Never
- A test signup on production: it creates CRM/billing/analytics records and
  trial emails, polluting the very funnel metrics the team watches. The account is
  also empty.
- Capturing any screen that can show real customer data.

## The safe path (proven)
1. **Source**: `mkdir -p scratch/src && git -C <repo> archive <pinned-sha> <app> <demo-data dirs> | tar -x -C scratch/src`.
   No worktree (it mutates shared git metadata), never the working tree of
   someone's checkout. `scripts/rename.py` refuses to run inside a git checkout.
2. **Dependencies**: install with caches inside scratch, empty npm/yarn config (no
   registry credentials readable), `--ignore-scripts`, then run only the named
   steps the build needs (for example `patch-package`). If there is no lockfile,
   save the resolved lockfile as the record.
3. **Demo data**: use the app's own demo template, generated offline (stub the
   database model before requiring the template service). Rename any demo brand
   that collides with a real business **in the source before building**, then
   scan source, built bundle, generated data, live DOM text and OCR of frames.
   Web-check every invented name.
4. **Browser**: fresh non-persistent context, service workers blocked, WebSockets
   closed, a context-level deny-by-default router installed before any page:
   the local build origin is the only real transport; API calls are fulfilled from
   fixtures by endpoint and method; the app's own static icons are served from a
   hashed local mirror; everything else is aborted and logged. Any unmatched API
   or localhost request fails the run. This is a request-level boundary inside the
   browser, not an operating-system firewall: for an app you do not trust, also run
   the capture with the network off. If the pinned Playwright wants a browser
   revision you do not have, use the installed Chrome (`channel: "chrome"`), which
   runs on a fresh temporary profile.
5. **Shots**: dismiss onboarding modals; keep the app's own "sample data" banner;
   draw a visible eased cursor; record 1080p video plus 2x stills in separate
   contexts; close the context before reading the video file.
6. **Edit**: cards tagged "Real app" and "Sample data"; 0.5 to 2 s windows chosen
   from 2 fps contact sheets of each clip.

`scripts/capture/harness.mjs` is a template of this harness. Put your app's live-mode
variables in `REFUSE_IF_SET` so the harness refuses to start when any is set.
