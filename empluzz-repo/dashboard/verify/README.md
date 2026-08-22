# dashboard/verify

Rebuilt 2026-08-22. The original six files lived in a cloud session workspace and that
container is gone; `docs/MEMORY.md` section 7 always said to rebuild from its description
if that happened, and it carried enough detail to do it. This is that rebuild.

**41 assertions, all passing** against `../application-command-center-1787336084-pre16row.html`
on Node 22, Python 3.11, Chromium via Playwright.

## Run it

```bash
./run.sh                       # uses the committed build
./run.sh path/to/other.html    # or any authored build
```

`run.sh` builds the fixtures, runs the three suites, writes screenshots to `/tmp/acc-shots`,
and tells you to go and look at them. Do look at them.

## Files

| File | What it is |
|---|---|
| `accdoc.py` / `accdoc.js` | The marker cut, the state swap, and the canonical rebuild. A line-for-line mirror of `buildDoc()` in the dashboard, in both languages, so fixtures and assertions cannot drift apart. |
| `shell.py` | Simulates the artifact shell's transform: injects a frame runtime and a `<base href>`, drops the `cowork-artifact-meta` block, dissolves the `</head><body>` seam, drifts the whitespace. Deliberately more hostile than the real shell. |
| `mkbase2.py` | Derives the canonical reconstruction from a served copy. This is the edit base, not the file on disk. |
| `mklive3.py` | Builds a served copy carrying a **realistic** state block, the 14 ticks from `MEMORY.md` section 2. It refuses to tick a slug that is not in `INT`. |
| `harness.js` | Local server pinned under the injected base href, the five `window.claude.use` stubs, the report printer. |
| `verify.js` | Core suite, 26 assertions. |
| `verify-upgrade.js` | Round trip and fixed point, 8 assertions. |
| `verify-upgrade2.js` | Layout and reading position, 7 assertions. |
| `shots.js` | Screenshots at 390, 760, 1440. |

## Assertion inventory

**verify.js, 26.** Served fixture is a faithful hostile shell copy (A1-A5). A plain browser
tab with no capability still renders, errors nothing, publishes nothing, and keeps the
localStorage backstop (B1-B4). An idle load publishes nothing (C1). The slug under test
really exists in `INT` and the bug-15 phantom does not (D1-D2). The published payload is a
complete document, carries every marker exactly once, leaks no frame runtime and no meta
block, carries the new tick, grows the count by exactly one, changes no existing slug, keeps
every slug unique and `[a-z0-9-]`, and has exactly one html and one body wrapper as markup
(E1-E10). The four rejection branches behave: `capability_disabled` and `not_writer` drop to
read-only and never retry, `conflict` reads as synced, `rate_limited` backs off (F1-F4).

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
