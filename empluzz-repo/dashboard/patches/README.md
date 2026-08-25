# dashboard/patches

Anchored find/replace scripts for shipping one change into a build. Anchors, never
byte offsets, because whitespace drifts across a shell round trip. Every script
refuses to write anything if an anchor is missing or appears more than once.

## apply-delegation.py

Turns the per-row **Build letter** button from a prompt the pasted-into chat runs
itself into an orchestration prompt addressed to Opus, which hands the drafting to
a Sonnet subagent and keeps the voice pass. Four edits: the `cvPrompt` and `cvBtn`
pair, the clipboard comment, the button tooltip, and the board hint.

```bash
python3 apply-delegation.py IN.html OUT.html new-block.js
```

`new-block.js` is the replacement `cvPrompt`/`cvBtn` pair, which lives in
`build-letter-delegation.js` next to this file. Already applied to
`application-command-center-1787428545-41row.html`; keep the script for the next
build that comes back from the live artifact still carrying the old shape.


## apply-writing-system.py

Installs the career-ops writing system into the **Build letter** button. Four
edits: the `cvBrief` / `cvRules` / `cvPrompt` / `cvBtn` block, the button
tooltip, and the board hint.

```bash
python3 apply-writing-system.py IN.html OUT.html build-letter-delegation.js
```

What changes in the copied prompt:

- **Opus asks the four questions before it spawns anything.** Why this company,
  what he would be good at, what he would want to be doing in his first week, and
  tone. A subagent cannot ask him anything, and the first-week answer is the only
  paragraph of a letter that is genuinely his. This is the change that most
  affects whether a letter reads as written or generated.
- The brief carries the anti-slop rules: no negative parallelism, no dead AI
  vocabulary, and no number in every paragraph on a cadence.
- The brief makes the subagent lay the gate down from the skill and run
  `/tmp/apb/scripts/check_letter.py`, and **refuse to build the doc on exit code
  2**, with the no-shell checklist named as the fallback. An earlier draft wrote
  the command as a relative `scripts/` path, which resolves to nothing in the
  cold session the brief is written for.
- **Pay never reaches the clipboard.** `noPay()` drops any sentence in the
  tracker note carrying a currency figure, because the note routinely carries
  the posted wage and sometimes his Kelvin rate. A scholarship award figure is
  kept: that is public information about the award, not his compensation.

`build-letter-delegation.js` next to this file is the replacement block, and it
is the same file `apply-delegation.py` reads. Run this against a build that
already carries the 2026-08-22 delegation block; for anything older run
`apply-delegation.py` first.

**NOT SHIPPED.** The live board still carries the 2026-08-22 button. This needs a
route 0 publish built from a fresh read of the live artifact, never from the file
committed in `dashboard/`. Assertions I8 to I11 in `dashboard/verify/verify.js`
hold the new shape and pass against a patched build.
