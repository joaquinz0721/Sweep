# Migration status, 2026-08-21

What this drop contains, what it changed, and what is still missing.

## What is here

| Path | Status |
|---|---|
| `CLAUDE.md` | **Regenerated.** Replaces whatever is in the repo now. |
| `docs/MEMORY.md` | **Regenerated, canonical.** Overwrite the copy already in the repo. |
| `docs/artifact-write-routes.md` | New to the repo |
| `docs/verification-2026-08-21.md` | New to the repo. Cited by `MEMORY.md` section 2. |
| `docs/source-expansion-scoping.md` | New to the repo |
| `docs/support-request.md` | New to the repo. Unsent. |
| `docs/history/code-tab-prompt-2026-08-21.md` | New. Shipped and spent; kept as the worked route-0 example. |
| `docs/history/desk-checklist-2026-08-21.md` | New. Mostly spent; kept for the reasoning and the LinkedIn alert table. |
| `prompts/session-opener.md` | New. The Cowork "next session" prompt, ported to repo paths. |
| `.claude/skills/application-packet-builder/` | **This row was false until 2026-08-24.** It said the skill was copied from the account-synced skill, belt and braces, and the directory existed in no commit in this repo's history. It was actually copied in on 2026-08-24, from `~/.claude/skills/synced/application-packet-builder/`, byte for byte, with the POST-APPLICATION FOLLOW-UP section appended to `SKILL.md`. The account copy still loads too, and **committing here does not update it.** |

## What changed in the regenerated files

**Every `claude/<name>.md` citation is now `docs/<name>.md`.** The one remaining mention of a `claude/` path in `MEMORY.md` is a direct quote of what a session reported in the past and is correct as history.

**`CLAUDE.md` gained four things the claude.ai project instructions never had:**

1. Hard rule 8, never consolidate rows. Standing instruction from 2026-08-21, previously only in `MEMORY.md`.
2. Hard rule 9, the wage floor is a preference and not a filter, with the `est.` convention.
3. Hard rule 10, never touch the applied ticks.
4. The AutoCAD and BIM exclusion folded into hard rule 5, and a surface matrix saying which session types can write the tracker.

Hard rule 6 already carried the corrected relocation policy and still does. Rule 3 is reworded from "never use the Chrome extension" to "never drive a browser", since the reason is now structural rather than economic.

**`MEMORY.md` gained a section 0** with the repo layout, and its plumbing to-do list now names the three files that still need to be committed. Two to-do items are closed by this drop: the copy-paste fidelity check, and the rule 6 correction.

## What is still missing, and only Joaquin can supply it

These are on device `jz`, in `Downloads`, and no cloud session can reach them.

1. ~~**`dashboard/application-command-center.html`**~~ **CLOSED 2026-08-22, and not from the device.** The current source was pulled straight from the live artifact by a cloud session and committed as `application-command-center-1787428545-41row.html`. The device build was three publishes behind and would have cost 12 rows. Nothing on `jz` is needed for this any more.
2. ~~**`dashboard/verify/`**~~ **CLOSED 2026-08-22, rebuilt rather than recovered.** The originals were never on the device. 48 assertions now, and bug 15 is fixed in the rebuild.
3. **`prompts/sweep-prompt-internship.txt` and `prompts/sweep-prompt-scholarship.txt`**. These are the source for the routine prompts when the sweeps move.

## Do not delete yet

That condition is met: a cloud session read and published the artifact on 2026-08-22, version `1787430085-95fa`. The claude.ai `empluzz` project can be retired whenever Joaquin wants, though there is no cost to leaving it as an archive. The two sweep prompts in item 3 below are the only thing still worth extracting from the old surfaces.

Never touch the frozen Google Sheet at any point.

## One caveat on the committed skill

`application-packet-builder` reads its row data the Cowork way: `list_artifacts`, then `device_stage_files` with `artifact_ids`, then read the staged file. **None of those tools exist in a Claude Code session.** The skill will still load, and everything about voice, format, Drive output and the hard constraints is surface-independent and correct, but the data-source step needs rewriting before it runs outside Cowork.

The Claude Code equivalent is `WebFetch` on the tracker URL from a local session or a cloud session pinned to `empluzz`, then parse the `INT`, `SCH`, `CAL`, `OUT` and `PROF` arrays out of the script block. Do not rewrite it until section 6 item 0 has confirmed which of those reads works, or you will write against a route that is still closed.

Until then, keep building letters in Cowork where the skill works as written, and use the repo for dashboard and plumbing work.

---

# Update 2026-08-22: the device sweep

`Downloads` on device `jz` was connected and searched. Six of the eight requested files do not exist there.

## Found, and committed

| Requested | Reality |
|---|---|
| `application-command-center-2026-08-21-v3.html` | **Does not exist.** The newest authored build on the device is 78,656 bytes, present three times under different names, all byte-identical (md5 `9aac4a4f8233f1d15ec13549dc3706ec`): `dashboardapplication-command-center.html`, `target2.html`, `target2_1.html`. Committed as `dashboard/application-command-center-1787336084-pre16row.html`. See `dashboard/README.md`. |

**It is three publishes behind the live artifact.** `int-h3x-electromagnetics-intern` is absent from it, and that slug was added in `1787353283-20cc`, so none of the sixteen-row verification change is in this file. It is a valid historical build and a valid diff base. It must never be used as a publish base.

## Not found at all

| Requested | Reality |
|---|---|
| `verify.js` | Not on the device |
| `shell.py` | Not on the device |
| `verify-upgrade.js` | Not on the device |
| `verify-upgrade2.js` | Not on the device |
| `mkbase2.py` | Not on the device |
| `mklive3.py` | Not on the device |
| `sweep-prompt-internship.txt` | Not on the device |
| `sweep-prompt-scholarship.txt` | Not on the device |

Searched the whole of `Downloads` at every depth, plus `Sweep`, `empluzz-repo-files` and `ClaudeProj`. The only loose scripts present are `upgrade-console.js` and `upgrade-rows.js`, which are the console-route helpers, not the harness. The only `.txt` is `Memory.txt`.

This matches what `MEMORY.md` section 7 always said: the harness lived in a cloud session workspace, and **that container is gone.** The line "rebuild from this description if the container is gone" was not a hedge, it was a prediction. Section 7 carries all 41 assertions of the ORIGINAL harness in prose, so a rebuild is a real option rather than a guess. The rebuild came out at 48.

The two sweep prompt files were delivered into a Cowork chat and were never saved to disk. The live copies are inside the two desktop scheduled tasks, which is the only place they still exist. Recovering them means opening each task in the desktop app and copying the prompt out.

## Correction: the environment checkbox is still an open question

The Node 22, Python 3.11, Chromium, npm and PyPI reported as present are this **Cowork cloud container's** toolchain. That is a different thing from the `empluzz` Claude Code cloud environment, and it does not settle the package-manager checkbox.

The checkbox concern is specific: setting an environment's Network access to **Custom** replaces the Trusted default domain list unless **Also include default list of common package managers** is ticked. It is a property of that environment's egress rules. Nothing observable from this container tests it, because this container is not in that environment. Confirming it takes one look at the environment dialog, or one `npm ping` from a session actually pinned to `empluzz`.

The docs have not been changed to say otherwise, and should not be until that check happens.

## Harness: rebuilt, not recovered

The six files were rebuilt from `docs/MEMORY.md` section 7 and committed to `dashboard/verify/`. **48 assertions, all passing** on Node 22, Python 3.11 and Chromium in this container. Run `dashboard/verify/run.sh`. (This line read **41** until 2026-08-24, which was the original harness's count carried over by mistake; the rebuild has 48 and the run was re-measured to confirm it.)

Three findings fell out of the rebuild that were previously only claims in prose:

1. **The committed build is already its own canonical reconstruction**, byte for byte. The fixed point is measurable.
2. **The applied:null trap reproduces exactly.** Baking the 14 ticks into that build grows it by **+586 characters**, the same number `MEMORY.md` recorded from the gate that failed on 2026-08-21. The harness now rehearses against a realistic state block by default.
3. **Wrapper nesting cannot compound.** Three generations of publish-then-shell-transform converge byte-identically, as long as the marker reconstruction is always performed.

Bug 15 is closed. The rebuilt suite asserts the slug exists in `INT` before toggling, asserts the phantom `int-marotta-controls-me-intern` is absent, and `mklive3.py` refuses to build a fixture that ticks an unknown slug.

Two of my own assertions were wrong before any code was, both now recorded in `dashboard/verify/README.md`: counting `<html>` as a raw substring double-counts because `buildDoc()` carries that literal inside its own script, and a ticked row leaves the Internships tab for the Applied archive.

Screenshots at 390, 760 and 1440 were rendered and inspected. The board renders correctly at all three, stacked cards under 700px, no sideways scroll. They also confirm the staleness diagnosis visually: Boom still reads Englewood, H3X still sits at WATCH with "Spring term, collides with class", IMEG is still UNCONFIRMED, and the wages are still "not listed". Every one of those is something the sixteen-row change fixed.
