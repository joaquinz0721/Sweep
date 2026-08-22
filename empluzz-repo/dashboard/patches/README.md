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
