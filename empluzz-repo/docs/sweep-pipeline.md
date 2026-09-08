# Sweep pipeline

## Status: BUILT and RUN, 2026-09-08.

`dashboard/ingest.py` exists, the internship sweep has been run through it end to
end, and the result was published to the live tracker as version
`1788869745-d88d`. The six steps below are a procedure now, not a design.

What changed on 2026-09-08:

- **`dashboard/ingest.py` was written.** Preview by default, `--apply` to write,
  merges `INT_new` and `SCH_new` by slug, stamps a CAL row so `SWEPT` moves.
  It refuses malformed JSON, a row without a slug, a wrong field count, a
  duplicate slug, an em dash, and any change that would move the state block.
  It never publishes and it never touches the applied ticks.
- **The sweep agent still does not exist.** `internship-sweep` is not an agent in
  a cloud Claude Code session; the two sweep prompts are still stored only in the
  desktop app and are still missing from `prompts/`. The 2026-09-08 sweep was run
  by hand by the orchestrating session. Step 1 below is still aspirational.
- **Step 5 named a file that has never existed.** `sweepPrompt()` said to publish
  `dashboard/application-command-center.html`. It was corrected in the same
  publish to say the merged build, and to say the payload must come from a fresh
  read or the ticks go to null.

### The one thing that is easy to get wrong

`INT` rows carry 14 fields with the slug at index 13. `SCH` rows carry 13 fields
with the slug at index 12. The dashboard source says so directly above `const
SCH` and the first draft of `ingest.py` ignored it and used a literal 13 for
both, which crashed on the SCH array. `SLUG_AT[kind]`, never a literal.

## The six steps

1. **Spawn the sweep agent on Sonnet.** `internship-sweep` or `scholarship-sweep`. It searches, scores, and writes a JSON payload of new and changed rows. It never publishes and it never edits the dashboard. That refusal is correct behavior and it is load bearing, per `docs/MEMORY.md` section 1.
2. **Preview:** `python3 dashboard/ingest.py <payload>`. Prints what it would do, N new and M updated, and changes nothing.
3. **Apply:** `python3 dashboard/ingest.py <payload> --apply`. Merges into the `INT` and `SCH` arrays and stamps the CAL Last Checked row so the header `SWEPT` date moves.
4. **Verify:** `dashboard/verify/run.sh`. All 56 assertions must pass. See the note on the count below.
5. **Publish** to the tracker artifact, passing its URL and the favicon `🎯`. Never `force`, never a `capabilities` object. The payload must be built from a **fresh read of the live artifact**, never from the null-state file committed here, or the applied ticks go to null. Proven working from a cloud session on 2026-09-08, first try, 28 ticks in and 28 out.
6. **Commit** the null-state build so the repo and the live page do not drift.

Standing guard rails, agreed 2026-08-21 and unchanged: never touch the applied ticks, refuse to publish if the tick count moved, refuse rows without a slug, refuse malformed JSON, and always preview before committing.

## Open questions the builder has to settle first

- **Which surface runs the sweep.** A Cowork session cannot publish the artifact at all. A cloud Claude Code session can, through route 0a. A scheduled routine is a third surface and has never been tested. `docs/MEMORY.md` section 1 has the whole matrix.
- **Whether ingest merges in the repo or in the page.** The alternative design, the **Paste sweep results** control, has the sweep emit JSON and the live page merge and republish itself. That needs no publish rights in the sweep at all. It is described in `docs/MEMORY.md` section 1 and it is a genuinely different architecture from `ingest.py`.
- **What the sweep agents actually are.** `internship-sweep---summer-27` and `scholarship-sweeper---26-27` are stored locally by the Cowork desktop app. Their prompts have never been recovered into `prompts/`.

## The assertion count, resolved 2026-08-25

**Resolved.** The harness has **56** assertions, measured by running `dashboard/verify/run.sh`
on 2026-08-25: 41 in `verify.js`, 8 in `verify-upgrade.js`, 7 in `verify-upgrade2.js`. The
earlier note here recorded 48 (33 + 8 + 7), measured on 2026-08-24 before I8 to I15 were
added to `verify.js`.

The button text was the other half of the drift: `sweepPrompt()` on the live board said
"all 41 assertions must pass", not the 56 this document previously claimed it said. Both
halves are now correct and agree at 56, shipped in live version `1787695423-9d50`.

Note for a future session: the harness needs `npm install` in `dashboard/verify/`, and in a
container whose Chromium build does not match the pinned Playwright, point `ACC_CHROMIUM` at
the preinstalled binary (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`). `harness.js`
documents that escape hatch.
