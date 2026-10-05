# Running the pipeline safely (and the traps that cost hours)

The case-study pipeline grew from "render and look" to one command with four
stages. Every item here is something that broke, leaked or lied at least once.

## The one-command shape

| Stage | Where it runs | What it does |
|---|---|---|
| S0 | outside the sandbox, project code only | lock, owner decisions, stale-state recovery, hash checks, input manifest, toolchain check |
| S1 | generation sandbox | generate both formats (rule R and event checks fail the build) |
| S2 | run sandbox, cleared environment, every step bounded and watched | profile controls, planted gate controls, crisp gates, render, every post-render gate, encodes, final text check, smoke checks of earlier versions |
| S3 | outside | re-hash inputs and scripts, promote staging atomically, assert file modes, write and verify a manifest |

Modes worth having: a dry run (stops before render), a **rehearsal** that renders and
runs every gate but deletes its staging and can never promote (so post-render bugs
surface before anyone signs off), and a post-render re-run that refuses unless the
recorded renders are unchanged.

## Owner gates that the scripts enforce

- **Decisions live in a folder the sandboxes cannot read or write**, owned by the
  person who signs off. The pipeline reads it from outside the sandbox and stops on
  any missing field, naming it. Never a default.
- **Approval of the scripts is a record of hashes** that the owner writes (the
  pipeline only prints the command). Any changed script after approval stops the run.
  If the owner delegates this, record the delegation and what was unreviewed.
- **A baseline of protected trees**, hashed by the owner before any code is written,
  so a run proves earlier deliveries and shared checkouts were not touched. This is
  detection, not prevention: say so.
- **Pinned approvals of captured footage and mock-ups**: the run refuses if a file
  the owner approved has changed.
- **Final versus candidate.** Until the owner has given the embed size and watched
  the film muted at that size, a run ends in a candidate folder, not the final one.
- **Waivers are named, per item and per format**, with the measured value and the
  reason, and do not carry over to the next version without the owner saying so.

## macOS sandbox-exec (Seatbelt) facts, measured

- A default-deny file-read profile breaks every process (exit 134) until it allows
  reading the root directory entry itself: `(allow file-read-data (literal "/"))`.
  It reveals no file contents.
- Deny file **contents and listings** (`file-read-data`), not all reads: path
  resolution needs `stat` on every parent directory, so `(deny file-read* ...)` on a
  parent of the project made the project unreadable too.
- Seatbelt cannot restrict a bind to loopback: `localhost:PORT` rules also allowed a
  bind on `0.0.0.0:PORT`. Enforce it with a watcher that kills the run if any process
  in the tree listens on a non-loopback address, and test the watcher with a planted
  listener every run.
- Use one fixed port for the capture server and allow exactly that port for bind,
  inbound and outbound; allow Unix sockets only inside the run directory and the
  browser's own singleton directory.
- Paths in profiles must be realpaths (`/private/var/...`, `/private/tmp/...`), and
  Unix socket paths must stay under 104 characters (use a short run directory).
- **Every profile rule gets a control that must fail**: a TCP connect to another
  loopback port, a connect to a local database port, a bind to another port, a Unix
  socket outside the run dir, a read of a planted `.env` file inside the project, a
  read of a planted file outside it, reads of the user's temp and cache folders, a
  write outside the allowed paths, a remote request. Plus two that must succeed.

## Process and cleanup

- Run every step under a supervisor that owns a process group, escalates TERM to
  KILL and fails if anything survives.
- The wrapper's own cleanup must stop and reap its background jobs (capture, watcher,
  controls) before it deletes the lock and the run directory. Track the job PIDs
  explicitly; counting "descendants of $$" also counts the counting pipeline.
- Take the lock first, set the trap immediately after, then write anything.
- Chrome leaves singleton folders in the user temp directory. Remove only the ones
  created during this run that no live process holds; a failed removal fails the run.
- On failure, remove staging; never leave a half-written deliverable behind.
- Failed and superseded captures are kept for inspection and deleted only by a
  purge tool that removes exact listed regular files, refuses symlinks, and logs
  every hash.

## Traps that looked like film failures

- **Apple Vision OCR returns blank text inside the sandbox** until it has run once
  outside it (its model cache cannot be populated from inside). Warm it up outside on
  a known frame, then prove it reads that frame inside, or stop as a tool error. A QA
  window where every OCR line is blank is a tool error, not a film failure.
- **ffmpeg without `-y` silently keeps an existing file** in a non-interactive run.
  Two holds extracted to the same temp name were both scored against the first frame.
  Use one file per extraction and pass `-y`.
- **OCR returns lookalike letters.** At 2x Vision read "App" with a Cyrillic capital A,
  and the gate's normaliser dropped it. Fold common Cyrillic and Greek lookalikes to
  Latin before matching.
- **A Homebrew upgrade changed the Python binary** between two runs, failing the
  pinned toolchain check. Confirm the source (an official bottle), get the owner's
  yes, write a new baseline for this version, and keep the old one unchanged.
- **An inline comment pasted before a statement silently disabled a negative control**
  (the control caught it by failing for the wrong reason). Check that controls fail
  for the reason they plant, not just that they fail.
- **A stale reference to the previous version's probe script** made QA measure the
  old page. Grep every new script for the old version number before the first run.
