# Task prompt: add the per-row Follow-up button to the dashboard

> **STATUS: NOT SHIPPED.** The button does not exist on the live board. This file is the prompt that builds it. Written 2026-08-24, in the same session that filed the follow-up format spec into the skill and `docs/followup.md`. Nothing here has been run.

Paste everything below the line into a fresh session that has this repo checked out and can reach the tracker artifact. A **cloud Claude Code session** works, through route 0a, and is the cheapest option. A **local Code-tab session** in the desktop app also works. A Cowork session cannot publish and must not be used.

---

You are shipping one change to the tracker dashboard: a per-row **Follow-up** button. Read `docs/MEMORY.md` sections 1 and 3, `dashboard/README.md`, and `.claude/skills/application-packet-builder/references/followup.md` before you touch anything.

**Artifact:** https://claude.ai/code/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594

**Hard rules for this session.** No em dashes anywhere, in code, in docs, in commit messages, or in chat. Never read or write the Google Sheet `138-KAgu9j9qCFeAn_pTTRWVmhEhXOwIpCTb2K8eraRk`. Never submit or transmit anything. Do not touch the applied ticks; Joaquin manages those himself. One publish for the whole change set.

## The goal

Every internship row and every scholarship row gets a second action button, **Follow-up**, sitting beside the existing **Build letter** button. Clicking it copies a ready-to-use prompt for drafting the post-application follow-up message for that row, the same way Build letter copies the packet orchestration prompt today.

The button is for rows he has **already applied to**, which is what a follow-up is. Put it on every row anyway rather than hiding it behind the applied tick: a hidden control is a control nobody finds, and reading tick state at render time couples the button to the state block for no benefit. The copied prompt opens by saying it is for a role already applied to, which is enough.

## The pattern to copy, exactly

The existing **Build letter** button is `cvPrompt()` and `cvBtn()` in the dashboard script block, installed into a build by `dashboard/patches/apply-delegation.py` from the replacement block in `dashboard/patches/build-letter-delegation.js`. Read all three before writing a line.

Build the same shape:

- A new `fuPrompt(kind,i)` and `fuBtn(kind,i,btn)` pair, and a `fuBrief(kind,r)` split mirroring `cvBrief(kind,r)`.
- A new replacement block file `dashboard/patches/followup-button.js`, next to `build-letter-delegation.js`.
- A new anchored patch script `dashboard/patches/apply-followup.py`, next to `apply-delegation.py`, with the same contract: **anchors, never byte offsets**, and it **refuses to write anything** if an anchor is missing or appears more than once. Copy the `sub()` helper and its refusal message verbatim.
- The same em dash guard at the foot of the script, copied verbatim from `apply-delegation.py`: if the em dash character U+2014 is present in the output, exit without writing. Copy that line out of the existing script rather than retyping it, so this file stays free of the character it is banning.
- Update `dashboard/patches/README.md` with a section for the new script, in the style of the existing one.

The patch has four edits, matching the delegation patch's shape:

1. Insert the `fuBrief` / `fuPrompt` / `fuBtn` block. Anchor it on the end of the `cvBtn` function so the two live together.
2. Add the button to the row action cell, beside the Build letter button, on both tables.
3. Give it a `title` tooltip in the same voice as the Build letter one.
4. Add a line to the board hint explaining what Follow-up copies, in the same voice as the Build letter hint.

## The rule that makes the button work

**The copied prompt must be self-contained.** This is the single most important thing in this task, and it is the same reason the Build letter brief is self-contained: the session receiving the paste starts cold. It cannot see the chat, it cannot see the dashboard, and it may not have the skill loaded at all.

So the follow-up rules travel **inside the copied text**. At minimum, the clipboard payload carries:

- The four sentence template, with its slots.
- The slot rules: FIELD is one noun phrase of six words or fewer with no internal "and" and no internal comma; the optional DETAIL attaches with one comma and the word "particularly" and is a single phrase; **two or three experience items, preferring two**, same grammatical shape, none containing the word "and", serial comma before the final "and" when there are three. The old spec mandated exactly three, which made every message carry an identical list in an identical slot. That is the same mail-merge tic that got "y'all" removed, and it is a documented AI tell. See `references/voice-dna.md`.
- The ban on `y'all`, `yall`, and `ya'll`. Permanent, not an option.
- **No numbers of any kind.** No yield figures, no cycle times, no tolerances, no dates, no wage.
- **No em dashes.**
- **Name the company**, twice, spelled the way the employer spells it.
- **Sentences 2 and 3 are never joined by "and".** This is the rule the old template broke on and it has to be stated, not implied.
- The do-not-claim list: FEA, CFD, NX, Teamcenter, ANSYS, AutoCAD, Revit, BIM, Creo, welding. SolidWorks is his CAD.
- Kelvin Thermal Technologies is past tense.
- Keep the line "I believe this role is an incredible fit." It looks like a hedge; it is his line and it stays.

**Point at the canonical source as well.** The prompt names `.claude/skills/application-packet-builder/references/followup.md` and says that where the button text and the skill disagree, **the skill wins** and the button text gets regenerated from it. The inlined copy is for a cold session that cannot read the repo, not a second source of truth.

## Row facts to inline, per row

Follow the `cvBrief()` split: internship rows read from `INT`, scholarship rows from `SCH`.

`INT` row shape is `[conviction, company, role, location, term, deadline, source, url, packetStatus, notes, status, hint, wage, SLUG]`. Inline:

- company, `r[1]`
- **exact role title as posted**, `r[2]`, and say in the prompt that this is the title to use verbatim in sentence 1
- location, `r[3]`
- the apply URL, `r[7]`
- the tracker notes, `r[9]`, which is where the FIELD and the optional DETAIL come from

`SCH` row shape is `[conviction, name, sponsor, award, opensRaw, deadline, gate, url, packetStatus, notes, status, hint, SLUG]`. Inline the scholarship name `r[1]`, the sponsor `r[2]`, the link `r[7]`, and the notes `r[9]`. A scholarship follow-up names the sponsor where a role follow-up names the company, and it refers to the application rather than to a role, so the template's role clause changes and nothing else does. Keep the divergence between the two kinds as small as `cvBrief()` keeps it.

Do not inline the wage, ever. Rule 4 of the follow-up absolutes bans numbers, and the wage is the easiest one to leak.

## Delivery, state it inside the copied prompt

- **Plain text in the chat reply**, so he can paste it straight into LinkedIn or Handshake.
- **A Gmail draft as well**, only if a real email address is known and he asks for one. Draft only. **Never send.**
- **Never filed in the Packets folder.** That folder is for cover letters and essays.

## The ship procedure, follow it exactly

From `dashboard/README.md` and `docs/MEMORY.md` section 3:

1. **Read the live artifact with the Artifact tool's `read` action.** Not `WebFetch`, which cannot reach the frame host from behind the egress proxy. The read is also what sets the tracked baseVersion and unlocks the publish.
2. **Reconstruct** with `dashboard/verify/mkbase2.py`. **Plain** for the publish payload, so the live ticks survive. **`--null-state`** for the copy that gets committed to `dashboard/`. These are two different files and mixing them up is how the ticks get deleted.
3. **Apply the anchored patch** to the reconstruction: `python3 dashboard/patches/apply-followup.py IN.html OUT.html dashboard/patches/followup-button.js`.
4. **Verify:** `dashboard/verify/run.sh <build>`. Every assertion passes or you stop.
5. **Publish** passing the artifact **url** and the favicon `🎯`. **No `force`. No `capabilities` object at all**, so the stored declaration carries forward; a non-empty object revokes anything not restated and that silently breaks tick saving.
6. **Read it back** and confirm row counts, unique slugs, tick count, the four marker pairs, and the html and body wrapper counts with `markupCounts` from `dashboard/verify/accdoc.js`.
7. **Commit the null-state build** from step 2 to `dashboard/`, along with the two new patch files and the new assertions. Record the new version slug in `docs/MEMORY.md` section 1.

## Gates, all of them, before you publish

- **Applied tick count identical before and after. Refuse to publish if it moved.** Best practice, proven on the sixteen-row change: keep the `ACC-STATE` block byte-identical between the edit base and the payload and never rewrite it at all.
- **Gate on the delta your edits produce, never on absolute document length.** A baked-in length number goes stale the moment a tick saves. That cost a failed attempt on 2026-08-21. Check state and structure independently.
- **Every marker appears exactly once.** All four document markers and both state markers.
- **All row slugs unique, `[a-z0-9-]` only, and no existing slug changed or disappeared.**
- **No injected frame runtime and no `cowork-artifact-meta` block in the payload.**
- **No em dash anywhere in the clipboard text**, on either kind. Assert it against the generated string, not by eye.
- **New assertions in `dashboard/verify/`** holding the shape of the follow-up prompt, the same way I1 to I7 hold the Build letter one. At minimum: the prompt carries the row facts a cold session cannot look up, it names the canonical skill section, it bans `y'all` and contains none, it states that sentences 2 and 3 are separate, it carries the do-not-claim list and the never-send rule, it contains no digits drawn from the row, and no em dash reaches the clipboard on either kind. Add them to the inventory in `dashboard/verify/README.md` and update the assertion total there and in `run.sh`.
- Log the reconstructed length and the applied-tick count on one line so a failure is diagnosable from the log alone.
- **Expect your own assertions to be wrong before the edit is.** Two gates failed on the 2026-08-21 run and both were bad assertions. Counting `<html>` as a raw substring double counts, because `buildDoc()` carries that literal inside its own script; strip script bodies first. A ticked row leaves the Internships tab for the Applied archive, so walk every tab.

## The two warnings that cost the last session time

1. **The repo copy is a build. The live page is the truth.** A republish is always built from a fresh read of the artifact, never from the null-state file committed in `dashboard/`. Publishing the committed file on 2026-08-22 would have deleted twelve rows and all fourteen ticks. The full account is in `docs/history/build-letter-delegation-2026-08-22.md`.
2. **A change that exists only in the repo looks like nothing happened.** The last session's first report back was "looks unchanged", because the board being clicked is the live artifact and nothing had republished it. If Joaquin says the button is not there, check whether you actually published before you go looking for a bug.

## Sweep this up while you are in there

`sweepPrompt()` in the dashboard says **"all 41 assertions must pass"**. The harness has **48**, confirmed by running `dashboard/verify/run.sh` on 2026-08-24: 33 in `verify.js`, 8 in `verify-upgrade.js`, 7 in `verify-upgrade2.js`. Fix the string to whatever the harness reports at the time you publish, since your own new assertions will move the number again. The header comment in `dashboard/verify/run.sh` says 41 as well and is stale for the same reason.

While you are in `sweepPrompt()`, note that it also points at `docs/sweep-pipeline.md`, at `dashboard/ingest.py`, and at `dashboard/application-command-center.html`. The first is now an honest stub saying the pipeline is not built; the other two do not exist. **Do not build them here.** That is a separate job.

## What this task does not do

- It does not build the recruiter or contact lookup. There is no route that finds a named contact for a row, so `[First name]` is filled in by hand or the greeting line is dropped.
- It does not change the Build letter button, the applied ticks, or any row data.
- It does not touch the sweep pipeline.

## Report back

The new version slug, the tick count in and out, the assertion count after your additions, the exact clipboard text the button produces for one internship row and one scholarship row, and the commit SHA.
