# Session opener

Paste this into a fresh session that has this repo checked out. Ported from the Cowork version on 2026-08-21; the only change is that the docs are files now, not claude.ai project knowledge.

---

Read `docs/MEMORY.md` before doing anything else.

Then do exactly one thing: **read section 10, the to-do inventory, out to me.**

Read it out grouped the way it is written, under its four headings: Applications, Scholarships, Dashboard, and Plumbing. Keep each item to one line. Do not summarise it into a paragraph, do not merge the groups, and do not drop the items you think are small. I want to see the whole board at once, which is the point.

For each group, say how many items it holds.

Two things to flag as you go, in one line each, because they are time-bound and everything else is not:

- The nearest deadline on the board and how many days out it is from today. As of 2026-08-21 that is IMEG, 2026-09-19.
- Whether SHPE membership has been recorded as done anywhere, since it blocks ScholarSHPE and has to happen before February 2027.

Then stop and ask me what to work on. Do not start work, do not open postings, do not build anything, and do not update the dashboard until I pick something.

## Context you need so you do not go the wrong way

- **Dashboard writes for interactive work have two proven routes as of 2026-08-22.** A cloud Claude Code session can do it: the Artifact tool's own `read` action returns the document and sets the base version, then a normal publish carrying the URL and the favicon `🎯` goes through. `WebFetch` still cannot reach the frame host from a cloud session and is not needed. A local Code-tab session in the Desktop app also works and is the older route. Procedures in `docs/MEMORY.md` sections 1 and 3. A Cowork session cannot publish at all, and `docs/artifact-write-routes.md` explains why so nobody re-litigates it.
- **The sweeps still cannot write the dashboard.** That is the only part of bug 12 still open and it needs GitHub connected to Claude plus routines pinned to `empluzz`.
- **The repo has the dashboard source and the harness**, since 2026-08-22. `dashboard/application-command-center-1787428545-41row.html` and `dashboard/verify/`. Run `dashboard/verify/run.sh` before any dashboard change ships; 48 assertions.
- **Never read or write the frozen Google Sheet.** Never submit or transmit anything on my behalf. Never use em dashes.
- **Do not write a cover letter for any row carrying a VERIFY chip** until the actual posting has been read. Eight rows are in that state.

If I pick application verification, the six that still need one fact each are Oxy wage, Zipline wage, Skydio term, MatX whether it is live at all, Kairos housing, and Elliott relocation.
