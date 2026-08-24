# Sweep pipeline

## THE PIPELINE IS NOT BUILT. DO NOT FOLLOW THE BUTTON PROMPT.

The **Run Internship Sweep** and **Run Scholarship Sweep** buttons on the dashboard copy a prompt that tells the receiving session to "Follow docs/sweep-pipeline.md" and then to run `python3 dashboard/ingest.py`. As of 2026-08-24:

- **`dashboard/ingest.py` does not exist.** Not in the working tree, not in any commit in this repo's history, not anywhere on any machine that has been searched.
- **This file did not exist either** until it was created as this stub, so the button pointed at nothing at all.
- **`dashboard/application-command-center.html`**, which step 5 of the button prompt names as the publish payload, does not exist under that name. The committed build is `dashboard/application-command-center-1787428545-41row.html`, and it carries `applied:null`, so it is never a publish payload on its own. See `dashboard/README.md`.

Anyone who presses one of those buttons today gets a prompt that sends them to three things that are not there. Nobody should follow it until the pipeline is real.

Building the pipeline is its own job. It was deliberately not done in the session that wrote this file, because writing an ingest path is a real piece of engineering and inventing one to satisfy a dangling reference would have been worse than the dangling reference.

## The intended design, for whoever builds it

These are the six steps the dashboard button already describes, recorded here as the design rather than as a procedure. They have never been run.

1. **Spawn the sweep agent on Sonnet.** `internship-sweep` or `scholarship-sweep`. It searches, scores, and writes a JSON payload of new and changed rows. It never publishes and it never edits the dashboard. That refusal is correct behavior and it is load bearing, per `docs/MEMORY.md` section 1.
2. **Preview:** `python3 dashboard/ingest.py <payload>`. Prints what it would do, N new and M updated, and changes nothing.
3. **Apply:** `python3 dashboard/ingest.py <payload> --apply`. Merges into the `INT` and `SCH` arrays and stamps the CAL Last Checked row so the header `SWEPT` date moves.
4. **Verify:** `dashboard/verify/run.sh`. All 48 assertions must pass. See the note on the count below.
5. **Publish** to the tracker artifact, passing its URL and the favicon `🎯`. Never `force`, never a `capabilities` object. The payload must be built from a **fresh read of the live artifact**, never from the null-state file committed here, or the applied ticks go to null.
6. **Commit** the null-state build so the repo and the live page do not drift.

Standing guard rails, agreed 2026-08-21 and unchanged: never touch the applied ticks, refuse to publish if the tick count moved, refuse rows without a slug, refuse malformed JSON, and always preview before committing.

## Open questions the builder has to settle first

- **Which surface runs the sweep.** A Cowork session cannot publish the artifact at all. A cloud Claude Code session can, through route 0a. A scheduled routine is a third surface and has never been tested. `docs/MEMORY.md` section 1 has the whole matrix.
- **Whether ingest merges in the repo or in the page.** The alternative design, the **Paste sweep results** control, has the sweep emit JSON and the live page merge and republish itself. That needs no publish rights in the sweep at all. It is described in `docs/MEMORY.md` section 1 and it is a genuinely different architecture from `ingest.py`.
- **What the sweep agents actually are.** `internship-sweep---summer-27` and `scholarship-sweeper---26-27` are stored locally by the Cowork desktop app. Their prompts have never been recovered into `prompts/`.

## The stale assertion count in the button text

The button prompt's step 4 says "all 41 assertions must pass". The harness has **48**, verified by running `dashboard/verify/run.sh` on 2026-08-24: 33 in `verify.js`, 8 in `verify-upgrade.js`, 7 in `verify-upgrade2.js`. The string lives inside `sweepPrompt()` in the dashboard HTML and only matters once someone republishes, so it was left alone rather than edited into a build nobody is publishing. Sweep it up on the next dashboard change.
