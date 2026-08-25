# dashboard/verify

Rebuilt 2026-08-22. The original six files lived in a cloud session workspace and that
container is gone; `docs/MEMORY.md` section 7 always said to rebuild from its description
if that happened, and it carried enough detail to do it. This is that rebuild.

**56 assertions, all passing** against `../application-command-center-1787637025-41row.html`
on Node 22, Python 3.11, Chromium via Playwright.

## Run it

```bash
./run.sh                       # uses the committed build
./run.sh path/to/other.html    # or any authored build
```

`run.sh` builds the fixtures, runs the three suites, writes screenshots to `/tmp/acc-shots`,
and tells you to go and look at them. Do look at them.

### Setup, in a fresh container

`node_modules` is not committed. Install Playwright first, from this directory:

```bash
npm i playwright --no-audit --no-fund
```

`package.json` pins the version that was last known to work here. `node_modules`,
`__pycache__` and `.pyc` files are ignored and never belong in a commit.

**On a Claude Code cloud session, do NOT run `npx playwright install`.** Chromium is already
at `/opt/pw-browsers` and the environment points Playwright at it. The catch, hit on
2026-08-22: the preinstalled build can be older than the one the freshly installed
Playwright expects, and the launch fails with `Executable doesn't exist at
.../chromium_headless_shell-<newer>/chrome-headless-shell-linux64/chrome-headless-shell`.
The cheap fix is a shim directory that maps the expected name onto the build that is
actually present, then point `PLAYWRIGHT_BROWSERS_PATH` at it:

```bash
PW=/tmp/pwb                      # anywhere writable
HS=/opt/pw-browsers/chromium_headless_shell-<present>/chrome-linux
mkdir -p $PW/chromium_headless_shell-<expected>/chrome-headless-shell-linux64
ln -sf $HS/* $PW/chromium_headless_shell-<expected>/chrome-headless-shell-linux64/
ln -sf $PW/chromium_headless_shell-<expected>/chrome-headless-shell-linux64/headless_shell \
       $PW/chromium_headless_shell-<expected>/chrome-headless-shell-linux64/chrome-headless-shell
cp /opt/pw-browsers/chromium_headless_shell-<present>/INSTALLATION_COMPLETE \
   $PW/chromium_headless_shell-<expected>/
NODE_PATH=$PWD/node_modules PLAYWRIGHT_BROWSERS_PATH=$PW ./run.sh
```

Both revision numbers are in the error message: the one it wants, and the one in
`/opt/pw-browsers`. Installing a Playwright version matching the present build works too
and is tidier if you know which version that is.

## Files

| File | What it is |
|---|---|
| `accdoc.py` / `accdoc.js` | The marker cut, the state swap, and the canonical rebuild. A line-for-line mirror of `buildDoc()` in the dashboard, in both languages, so fixtures and assertions cannot drift apart. |
| `shell.py` | Simulates the artifact shell's transform: injects a frame runtime and a `<base href>`, drops the `cowork-artifact-meta` block, dissolves the `</head><body>` seam, drifts the whitespace. Deliberately more hostile than the real shell. |
| `mkbase2.py` | Derives the canonical reconstruction from a served copy. This is the edit base, not the file on disk. |
| `mklive3.py` | Builds a served copy carrying a **realistic** state block, the 14 ticks from `MEMORY.md` section 2. It refuses to tick a slug that is not in `INT`. |
| `harness.js` | Local server pinned under the injected base href, the five `window.claude.use` stubs, the report printer. |
| `verify.js` | Core suite, 56 assertions. The last fifteen, I1 to I15, hold the shape of the Build letter prompt: that it still tells Opus to delegate to a Sonnet subagent, that the row facts a cold subagent cannot look up are inside the brief, that no em dash ever reaches the clipboard, that Opus asks the four questions before it spawns anything, that the brief makes the subagent run `check_letter.py` and refuse to build on a block, that it bans negative parallelism and dead AI vocabulary, that it no longer demands a number in every paragraph, that no pay figure reaches the clipboard on either kind, that the gate command is an absolute path a cold session actually has, and that scrubbing the pay sentence leaves the rest of the tracker note intact, and that a scholarship award figure still survives because it is public information about the award and not his pay. |
| `verify-upgrade.js` | Round trip and fixed point, 8 assertions. |
| `verify-upgrade2.js` | Layout and reading position, 7 assertions. |
| `shots.js` | Screenshots at 390, 760, 1440. |

## Assertion inventory

**verify.js, 33.** Served fixture is a faithful hostile shell copy (A1-A5). A plain browser
tab with no capability still renders, errors nothing, publishes nothing, and keeps the
localStorage backstop (B1-B4). An idle load publishes nothing (C1). The slug under test
really exists in `INT` and the bug-15 phantom does not (D1-D2). The published payload is a
complete document, carries every marker exactly once, leaks no frame runtime and no meta
block, carries the new tick, grows the count by exactly one, changes no existing slug, keeps
every slug unique and `[a-z0-9-]`, and has exactly one html and one body wrapper as markup
(E1-E10). The four rejection branches behave: `capability_disabled` and `not_writer` drop to
read-only and never retry, `conflict` reads as synced, `rate_limited` backs off (F1-F4).
The Build letter prompt tells Opus to delegate to a Sonnet subagent, carries the row facts,
the skill name and the Packets folder id, keeps the never-submit and never-claim rules inside
the brief, keeps the voice pass with Opus, reaches the clipboard with no em dash on either
kind, and asks a scholarship about the essay bank rather than about housing (I1-I7).

**verify-upgrade.js, 8.** After a shell round trip every marker still appears once; the
reconstruction of the served copy is byte-identical to what was published; a third generation
does not drift, which is the proof that wrapper nesting cannot compound; the reconstruction
carries one html and one body wrapper; a state swap changes nothing outside the state block;
the tick survives a clean load with no `localStorage`; the second generation does not
immediately republish; a mutilated document refuses to publish and says so (G1-G8).

**verify-upgrade2.js, 7.** Zero horizontal overflow at 390, 760, 1440; stacked cards and a
hidden header row under 700px; a real table above it with the wide table scrolling inside
`.tw`; the reading position parked in `sessionStorage` before the publish; and with no
viewport meta served, the JS guard adds one and 390px still does not scroll sideways (H1-H7).

## Two traps this rebuild walked into, recorded so nobody re-walks them

**Counting `<html>` as a substring is wrong.** `buildDoc()` carries the literal
`'<!DOCTYPE html>\n<html lang="en">...'` inside its own script, so a raw substring count
reports two `<html>` on a perfectly healthy single-wrapper document. `markupCounts()` strips
script bodies first. A naive nesting check raises a false alarm every single time.

**A ticked row leaves the Internships tab.** The first version of G6 looked for the checkbox
on the default tab and got `null`, which read as "the tick did not survive" when the tick had
survived and simply moved to the Applied archive. The assertion now walks every tab.

Both are instances of the rule in `MEMORY.md` section 3: **expect your own assertions to be
wrong before the code is.**

## The caveat that must stay attached

A green run here is evidence the code is right. It is **never** evidence the feature works.
The first build of this dashboard passed four stubs and still failed in production, because
the runtime does not serve the form it was built on. The better instrument is thirty seconds
in the real artifact frame: `await claude.use("artifact")`, then a real call.

## Bug 15 is fixed

The old `verify.js` ticked `int-marotta-controls-me-intern`, which has never existed.
`toggle()` creates a key for any string, so the assertion passed on a phantom row. This
rebuild asserts the slug exists in `INT` before toggling (D1), asserts the phantom is absent
(D2), and `mklive3.py` refuses to build a fixture that ticks an unknown slug.
