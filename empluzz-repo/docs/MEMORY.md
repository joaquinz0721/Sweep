# empluzz running memory

**This is the running memory file. Read it at the start of every session, before doing anything else. Update it at the end of any session that changes state.** Section 10 is the standing to-do inventory of everything never touched; section 6 is the priority ordering. `CLAUDE.md` at the repo root is loaded automatically; this file is not, so a session has to open it deliberately.

Last updated: 2026-08-25 (twelfth session: **the coursework rule and the assertion count SHIPPED to the live board**, version `1787695423-9d50`, through the cloud route 0a. Three changes, no row edits: the coursework rule added to the Sonnet subagent brief ("the ratcheting screwdriver reverse-engineering project and the compressed-air wobbler engine were school coursework, never call either one personal, independent, self-directed, done on my own time, or ungraded"), the same rule appended to the Opus voice-pass checklist, and `sweepPrompt()` step 4 corrected from "all 41 assertions must pass" to 56. Gates on the publish: **17 applied ticks in and 17 out with the state block byte identical**, 41 INT and 12 SCH rows unchanged, every marker exactly once on the reconstruction, and **all 56 assertions green** against the payload before it was sent. Wrapper nesting came back 2/2 again and self healed on reconstruction, byte identical to a reconstruction of the payload, stable on a third generation. **The publish gate needs the live version Read line by line, and grepping the saved file does not count** — the whole file has to go through Read. **The harness needs `npm install` in `dashboard/verify/` and `ACC_CHROMIUM` pointed at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`** in a container whose Chromium build does not match the pinned Playwright; `harness.js` documents that hatch. The assertion count is settled at 56 and `docs/sweep-pipeline.md` no longer carries the stale 48. Committed build: `dashboard/application-command-center-1787695423-56assert.html`. Eleventh session before that: **the writing system button SHIPPED to the live board**, version `1787637025-0b51`, through the cloud route 0a. **Route 0a is now proven twice**, and a Claude Code cloud session that can read the artifact is the cheapest route; the local Code-tab route is no longer the only one. Gates on the publish: 16 applied ticks in and 16 out with the state block byte identical, 41 INT and 12 SCH rows unchanged, all five data arrays identical, every marker exactly once, no injected runtime, and **56 assertions** green. The wrapper nesting came back 2/2 again and self healed on reconstruction, byte identical to a reconstruction of the payload, no drift on a third generation. **The publish refuses until the live version has been Read line by line**; a re-Read of a file an earlier refusal handed you does not count, you have to fetch the artifact again. Two defects were found by generating the clipboard text and reading it rather than trusting it: the gate command was a relative path that resolves to nothing in a cold subagent, and the brief leaked the posted wage and his Kelvin rate through the tracker note. Both fixed, `noPay()` scrubs pay from the note while keeping the award figure on scholarship rows. The account copy of the skill is now generated as a single file at `.claude/skills/application-packet-builder/dist/SKILL.md`, because the uploader takes one markdown file; **it is GENERATED, rebuild it with `scripts/build_account_skill.py` and never edit it by hand**, and **he still has to re-upload it himself**. Tenth session before that: **the writing system, ported from `santifer/career-ops`.** The IMEG letter came back obviously machine written, so the cover letter builder was torn down against career-ops and rebuilt. The finding: **our own skill was manufacturing the tells.** The fixed five-paragraph shape with a number in every paragraph is a metronome, the follow-up's mandatory three-item list is a rule of three, and we had no ban at all on negative parallelism, which is the biggest tell there is. The skill is now four reference files plus two JSON data files, with `references/profile.md` as **his layer** outranking everything. Two scripts: `check_letter.py` is a real gate with no bypass (banned vocabulary, negative parallelism, do-not-claim tools, numbers not on his resume, misattribution, present-tense Kelvin) and `build_letter_html.py` runs it and refuses to write a file on a block. **Google Doc delivery is unchanged.** The Build letter button now asks him four questions before it spawns the subagent; that block is in the repo and **not yet on the live board**, ships with `dashboard/patches/apply-writing-system.py`. Harness is **52 assertions**, I8 to I11 added, all green. **The account copy of the skill is NOT updated by this commit and he has to sync it himself.** Teardown evidence in `docs/research/career-ops-teardown.md`. Ninth session before that: **the post-application follow-up spec, and a repo drift clearance.** The follow-up format is now written down for the first time, canonical in the skill under POST-APPLICATION FOLLOW-UP, background in `docs/followup.md`. **The skill itself is now actually committed to `.claude/skills/`**, which `CLAUDE.md` had claimed since the migration and which was false until today. `docs/sweep-pipeline.md` exists as an honest stub, `prompts/followup-button.md` is written and unshipped, and the harness assertion count was re-measured at **48**. **All of it is on `main`**, fast-forwarded on 2026-08-24; `main` is the branch to read from. Eighth session before that: the Build letter delegation change and the cloud publish route, version `1787430085-95fa`. Seventh session: **repo migration.** All project docs rewritten for the repository, `claude/` paths rewritten to `docs/`, `CLAUDE.md` regenerated with the never-consolidate rule, the wage-preference rule, the AutoCAD and BIM exclusion, and the surface matrix folded in. Sixth session before that: route 0 carried its first real change, sixteen rows edited in one publish, version `1787353283-20cc`, 14 ticks intact, every gate green. Eleven postings verified against employer sources; VERIFY chips 18 to 8. **IMEG is now the nearest deadline on the whole board, 2026-09-19.**)

---

## 0. Repo layout, since this file now lives in one

```
CLAUDE.md                                   loaded automatically, hard rules
docs/MEMORY.md                              this file
docs/artifact-write-routes.md               which surfaces can write the tracker
docs/verification-2026-08-21.md             posting evidence, direct quotes
docs/source-expansion-scoping.md            LinkedIn and ZipRecruiter reasoning
docs/support-request.md                     the gateway support request, unsent
docs/followup.md                            post-application follow-up background, the two broken outputs
docs/sweep-pipeline.md                      STUB. The pipeline is not built and ingest.py does not exist
docs/history/code-tab-prompt-2026-08-21.md  shipped; the worked route-0 example
docs/history/desk-checklist-2026-08-21.md   mostly spent; kept for reasoning
docs/history/build-letter-delegation-2026-08-22.md
                                            the delegation change and the cloud publish route
dashboard/application-command-center-1787428545-41row.html
                                            CURRENT source, from the live artifact 2026-08-22, applied:null
dashboard/application-command-center-1787336084-pre16row.html
                                            historical build, do NOT publish from it
dashboard/patches/                          anchored one-change edit scripts, README explains each
dashboard/verify/                           rebuilt harness, 56 assertions, run.sh
prompts/session-opener.md                   paste into a fresh session on this repo
prompts/followup-button.md                  the prompt that ships the Follow-up button; NOT shipped
prompts/                                    the two sweep prompts are still missing
.claude/skills/application-packet-builder/  packet spec AND the follow-up spec. Committed 2026-08-24, real at last
```

Everything that used to be cited as `claude/<name>.md` is now `docs/<name>.md`.

---

## 1. Where the tracker lives

**Source of truth: the hosted artifact.**
https://claude.ai/code/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594

- Live version: **`1787430085-95fa`, published 2026-08-22 from a cloud Claude Code session.** Verified by reading it back: 41 internship rows, 12 scholarship rows, 41 unique slugs, 14 applied ticks unchanged, all four marker pairs once each. The capability declaration survived as `{artifact, downloads}`, contract 0.2.11, carried forward by omitting the parameter. Still read the live page before anything version-dependent, but this slug is trustworthy as written. Historical note, and the reason that warning existed: **UNKNOWN, do not trust a recorded slug.** The last slug this file recorded is `1787353283-20cc` (after `1787339155-f74b`, after `1787336084-e040`), but **Joaquin ran a further manual Code-tab edit after that on 2026-08-21 and the resulting version was never reported here.** Read the live page and take the slug from it before doing anything that depends on the version. Two things that edit could have changed without anyone noticing: the capability declaration (if it passed a non-empty `capabilities` object it would have revoked what was not restated, which silently breaks tick saving) and the favicon.
- **Favicon is `🎯`, set 2026-08-21.** The Artifact tool requires the parameter on every publish and no prior value had ever been recorded, so one was chosen. Keep it stable; a changed favicon reads as a different page. If the original was something else, restore it once and record it here.
- Private to Joaquin, confirmed "only me" 2026-08-21. Opens on any browser including his phone.
- Capabilities declared and granted: `{artifact:{}, downloads:true}`, contract 0.2.11, carried forward untouched through the 2026-08-21 publish.
- Authored source of record: **`dashboard/application-command-center-1787428545-41row.html` in this repo**, since 2026-08-22. `applied:null` in its state block while the LIVE page holds his real ticks, so it is a build and never a publish payload on its own. See section 3. The device-`Downloads` era is over; nothing on `jz` is current.

### THE CENTRAL CONSTRAINT: only the page itself can publish

A **Cowork** session cannot publish to this artifact with the Artifact tool. Two guards, in order:

1. `This session hasn't viewed the latest version of the artifact. Read it first (WebFetch the URL)` is the stale-read guard, unsatisfiable while the allowlist blocks the frame host.
2. With `force: true`, a harder one: `deploy 400: this artifact self-publishes, provide the baseVersion you edited from`. Because the page declares the `artifact` capability, the server demands a base version and **the Artifact tool exposes no parameter for it.** Force does not help.

A successful `WebFetch` is what sets the tracked baseVersion, so **the read unlocks the tool.** The read needs `*.frame.claudeusercontent.com` on the session's network allowlist.

### ROUTES OUT: settled 2026-08-21, do not re-litigate

Full evidence in `docs/artifact-write-routes.md`. Summary:

0a. **A CLOUD CLAUDE CODE SESSION CAN BOTH READ AND PUBLISH, proven 2026-08-22.** Not through `WebFetch` and not through the allowlist: through the **Artifact tool's own `read` action**, which returned the full 117.5KB document and set the tracked baseVersion, after which a normal publish carrying the URL and the favicon went through and produced `1787430085-95fa`. No force, no `capabilities` object, no console script, no local machine. This is a second interactive route and it is cheaper than route 0 because it needs nothing on his desk. **It says nothing yet about routines**, which run on a different surface; the sweeps are still blocked until that is tested the same way.
0. **ALSO WORKS, proven twice: a LOCAL Code-tab session in the Desktop app.** No GitHub, no cloud environment, no console. Cloud sessions sit behind the egress proxy, which is the entire reason the allowlist matters; a local session runs on his machine, on his own network, with no proxy, so `WebFetch` reaches the frame host and the tracked baseVersion gets set. The Artifact tool then publishes normally. Procedure in section 3. **This does not fix the sweeps**, which need the laptop closed.
1. **Session-gateway artifact reads: CLOSED.** The phrase appears in zero Anthropic documentation across docs.claude.com, code.claude.com, and support.claude.com. Not a setting, plan feature, admin toggle, or documented rollout. A support request is drafted in `docs/support-request.md` and is a background long shot, not a plan.
2. **Cowork bound to a cloud environment: IMPOSSIBLE, confirmed three ways.** (a) The cloud-environments doc enumerates the surfaces that use environments and Cowork is not among them. (b) "The Desktop app" in that list means the **Code** tab; the desktop doc says the app has three tabs, Chat, Cowork, Code, and documents the environment selector as a Code-tab control. (c) The Cowork architecture overview says a cloud session uses the same network-access setting that governs local Cowork and chat, and that setting's domain-allowlist option is documented as Team and Enterprise only. Also: the Cowork scheduled-task tool accepts an `environment_id` argument but swallowed a deliberately invalid value without error and echoed no environment back, so it is not a binding. **Stop tuning `empluzz` for Cowork's sake.**
3. **Driving Chrome: CLOSED, tested live 2026-08-21 with Joaquin's approval, then reverted.** His Chrome is authenticated and the artifact renders fully. But `javascript_tool` executes only in a tab's top document and has no frame-targeting parameter. From the top `claude.ai` frame, every access into the artifact frame throws `SecurityError` (`contentWindow.document`, `.claude`, `.eval`, any query through it); the iframe's `allow-same-origin` refers to its own origin, not claude.ai's. Navigating straight at the frame URL lands on `claude.ai/code/frame/<uuid>`, which is another claude.ai shell that nests `<uuid>.frame.claudeusercontent.com` inside it, and `window.claude` is undefined at every level a tool can reach. The runtime is always one cross-origin hop past the tools. **Hard rule 3 stands as written.**
4. **THE ROUTE THAT WORKS FOR UNATTENDED WORK: a cloud routine** at `claude.ai/code/routines`, which has an environment picker in its creation form. **This is what fixes the sweeps.** Minimum interval one hour, daily run cap, connectors selected per routine. Prerequisite: cloud sessions require a GitHub repository, which now exists. See section 10.

Interactive changes go through route 0. The console script (section 3) is the fallback and must not be broken. **The sweeps still cannot write the dashboard at all**, because a local session needs the laptop open and awake. **This is unrelated to the dashboard's HTML.** Editing the page, however extensively, does not give a scheduled task the ability to publish it; the block is the surface the task runs on, not the document. Asked and answered 2026-08-21. Their refusal-to-publish guard is correct and load-bearing and must stay until they move to routines.

### READING the artifact: allowlist blocked in Cowork, console route works

`WebFetch` fails in a Cowork session and in any cloud session outside `empluzz`. The error names two routes and both are off. Re-confirmed live 2026-08-21. The permission check itself always passes, so this is never an access problem. **`WebFetch` SUCCEEDS in a local Code-tab session**, which is route 0 above.

**The Artifact tool's own `action: "read"` is ALSO blocked from Cowork, tested 2026-08-21.** It fails with the same allowlist error naming `*.frame.claudeusercontent.com`, plus "artifact reads through the session gateway are not enabled for this session". So both read routes are closed from Cowork, not just `WebFetch`. Do not spend another session rediscovering this.

**RETESTED FROM COWORK 2026-08-24, AND THE PROVISIONING EXCUSE IS SPENT.** A **fresh** Cowork session called `Artifact action:"read"` on the tracker URL and got the identical allowlist error naming `*.frame.claudeusercontent.com`, plus "artifact reads through the session gateway are not enabled for this session". The allowlist entry had already been saved on `empluzz` and this was a brand new container, so the old "the container predated the change" explanation no longer covers it. **Cowork is not bound to the `empluzz` environment**, which is what route 2 in the section above says on documentary grounds and what this now confirms empirically. **Route 0, route 0a, and the paste design remain the routes. Stop retesting this from Cowork.**

Historical, kept so nobody re-runs the reasoning: the allowlist entry is saved on the `empluzz` environment, and a mid-session retest on 2026-08-21 failed for what was then thought to be provisioning reasons only, the sandbox's egress rules being fixed when the container is provisioned. That hypothesis is now dead for Cowork. It was never tested for a cloud session pinned to `empluzz`, and it does not need to be: route 0a does not use the allowlist at all.

**Console route, the fallback.** Relative URLs inside the artifact serve the version the view loaded:

```js
window.__src = await (await fetch('index.html')).text(); window.__src.length
```

then, as a SEPARATE console entry (a top-level `await` makes DevTools wrap the snippet and the Command Line API is unavailable inside that wrapper, which is why a combined paste fails with `copy is not defined`):

```js
copy(window.__src)
```

What comes back is the SHELL'S copy: it injects a frame runtime, drops the `cowork-artifact-meta` block, and dissolves the `</head><body>` seam, while preserving authored content contiguously and keeping HTML comments.

**Getting into the artifact frame's console.** The artifact runs in an iframe on `<uuid>.frame.claudeusercontent.com`. Chrome's console defaults to the top frame, where `window.claude` is undefined on a perfectly healthy artifact. Right-click inside the dashboard table, then Inspect. **A console result from the top frame means nothing.** This produced one false negative already. Note there are now known to be two nested claude.ai shells above the real frame, so pick the innermost.

**Google Sheet `138-KAgu9j9qCFeAn_pTTRWVmhEhXOwIpCTb2K8eraRk`:** frozen archive through 2026-08-17. Never read, never write.

**Packets folder:** Drive ID `1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP`
**Past cover letters (voice reference):** Drive ID `1pPulXeoTIXN6sJXuAByc2sW37dThROoB`
**Downloads on device `jz`** holds the authored builds and the console scripts. A cloud session has no access to it; that is what the repo is for, and moving those files in is an open item.

### THE ACTUAL GOAL FOR THE SWEEPS, restated by Joaquin 2026-08-21

**Read this before proposing anything about sweeps.** Earlier sessions drifted into solving unattended operation. That is not what he wants for now. What he wants is:

> He logs on, opens the dashboard, presses "Run internship sweep" or "Run scholarship sweep", the task runs on Sonnet, and the website ends up updated.

He is present. Unattended is not the requirement.

**Why the one-press version still does not work:** the sweep runs as a Cowork session, and a Cowork session cannot publish the artifact regardless of what triggered it. Manual versus scheduled was never the blocker. See the central constraint above.

**THE DESIGN THAT DOES WORK, agreed 2026-08-21, not yet built.** The page can already publish itself; that is how ticks save. So the sweep never needs publish rights. Flip the contract:

1. He presses the run button. The task runs on Sonnet, finds and scores, and **ends by emitting a JSON block of new and changed rows instead of attempting to publish.**
2. He copies it, clicks a new **Paste sweep results** control on the dashboard, pastes.
3. The page validates, shows a preview of what it will do (N new, M updated), he confirms, and it merges into `INT`/`SCH` and republishes itself through the same path the ticks use. It also stamps the CAL Last Checked row so `SWEPT` updates.

Press, wait, copy, paste. Two deliverables when it is built: a route-0 Code-tab prompt adding the ingest control, and a full rewrite of both sweep prompts to emit the payload. Guard rails for the ingest control: never touch `applied` state, refuse rows without a slug, refuse malformed JSON, always preview before committing.

**BUTTON TEST RESULT, 2026-08-21: `window.cowork.runScheduledTask` DOES NOT EXIST in the artifact frame.** Pressing "Run internship sweep" fires the fallback, which copies this to the clipboard: `Fire the scheduled task internship-sweep---summer-27 now, then update the command center with the results.` So the button is a copy-a-prompt button, and that is the mechanism, not a bug. Consistent with the frame runtime's module list, which has no scheduled-task surface. **Note the copied text is now actively wrong**: it instructs a Cowork session to update the command center, which a Cowork session cannot do, so every run ends in a failed publish and a chat report. Fix that wording as part of whatever gets built.

**BUT DO NOT BUILD THE PASTE DESIGN YET.** It is a workaround for the allowlist being closed to Cowork. Now that the repo exists, a cloud session or routine pinned to `empluzz` may make it unnecessary. Test that first, section 6 item 0.

### Sweep tasks

`internship-sweep---summer-27` and `scholarship-sweeper---26-27` are stored locally by the Cowork desktop app; `list_triggers` returns empty from a cloud session, so they cannot be seen or edited from there. Master prompts were delivered as `sweep-prompt-internship.txt` and `sweep-prompt-scholarship.txt`; rewrite in full rather than patching. **Neither prompt file is in the repo yet.** They refuse to publish when the artifact `WebFetch` is blocked and report in chat instead, which is currently every run. **Planned replacement: cloud routines pinned to `empluzz`.**

---

## 2. Application state

**14 ticks are saved IN THE ARTIFACT as of 2026-08-21** and confirmed to travel laptop to phone. The artifact is now the authoritative record; this table is the backup.

| Applied | Company | Role | Slug |
|---|---|---|---|
| 2026-08-17 | Medtronic | Engineering Intern, Summer 2027 | `int-medtronic-engineering-intern` |
| 2026-08-17 | Western Digital | Summer 2027 Intern, Hardware Engineering | `int-wdc-hardware-intern` |
| 2026-08-17 | Anduril Industries | 2027 Mechanical Engineer Intern | `int-anduril-mech-intern` |
| 2026-08-17 | SpaceX | Summer 2027 Engineering Internship/Co-op | `int-spacex-eng-intern` |
| 2026-08-18* | Kairos Power | Mechanical and Manufacturing Engineering Intern | `int-kairos-mech-mfg-intern` |
| 2026-08-18* | GE Aerospace | Manufacturing Engineering Intern, Summer 2027 | `int-ge-mfg-intern` |
| 2026-08-18* | GE Aerospace | Systems Engineering Intern, Electric Power | `int-ge-systems-intern` |
| 2026-08-18* | Great Plains Manufacturing | Summer 2027 Design Engineer track | `int-greatplains-design-intern` |
| 2026-08-18* | Boeing | Summer 2027 Facilities Engineering | `int-boeing-facilities-intern` |
| 2026-08-18* | Anduril Industries | 2027 Manufacturing Engineer Intern | `int-anduril-mfg-intern` |
| 2026-08-18* | Vertiv | ME Intern, Liquid Cooling | `int-vertiv-liquid-cooling-intern` |
| 2026-08-18* | BAE Systems USA | Operations Engineering Co-op | `int-bae-operations-coop` |
| 2026-08-18* | Elliott Machine Works | Design Engineering Intern | `int-elliott-design-intern` |
| 2026-08-21 | Marotta Controls | ME Intern, Space Systems (test tick) | `int-marotta-space-systems-intern` |

\* Dates reconstructed 2026-08-21, approximate.

### VERIFICATION PASS, 2026-08-21. The alert rows are no longer guesses.

The four LinkedIn alerts, deduped by job id, yielded **15 unique postings**, one of which (National Laboratory of the Rockies, graduate only) was already screened out. Eleven were read from the employer's own posting or ATS. Field-by-field evidence with direct quotes is in **`docs/verification-2026-08-21.md`**. LinkedIn itself blocks automated reads via robots.txt, so nothing came from a LinkedIn job page.

**Deadlines, the whole picture.** Only two active rows carry dates at all:

| Deadline | Row | Note |
|---|---|---|
| **2026-09-19** | **IMEG** | Nearest deadline on the entire board, ahead of the ACEC scholarship. Posting says it may extend if unfilled; do not plan around that. |
| 2027-01-01 | Kiewit | Posting active 08/18/2026 to 01/01/2027. |

Everything else is silent on deadline.

**Verified and ready for a letter:**

- **IMEG**, Mechanical Engineering Intern, Greenwood Village. Req R-16570. Summer 2027 confirmed, 10-12 weeks in office. **Deadline 2026-09-19.** $22-24/hr, under the preference so it renders red. Needs 2 years completed toward a BS in ME. **Requires AutoCAD and/or BIM. He has NEITHER, confirmed 2026-08-21; SolidWorks only.** The letter leads with SolidWorks depth and the additive work and never claims AutoCAD or Revit. See section 5. Sponsorship not available. Work is HVAC, geothermal, chilled beams, central plants, energy recovery, which is the closest thing on the board to Kelvin. STRONG.
- **Kiewit**, Equipment Engineer Intern, Equipment Services. Start May/June 2027. $18-25/hr, red. ME, MET, Diesel Tech or Automotive Tech. Citizenship SILENT, housing SILENT. Lone Tree and Denver both on the req. STRONG.
- **Boom Supersonic**, Summer 2027 Engineering and Tech Internship. **Centennial, CO, not Englewood.** 12 weeks. $35/hr hardware. **US person required under ITAR and EAR**, quoted in the verification doc. **Housing allowance $2,000 stated.** STRONG.
- **Freeform**, Mechanical Engineering Intern, Los Angeles. Summer 2027, on site. $30/hr undergrad. ME or aerospace, ABET. **ITAR US person required. Relocation assistance provided.** STRONG.
- **H3X Technologies**, Louisville, **five separate reqs, four of them eligible.** All pay $23-37/hr and all state a relocation package. **The Spring objection is dead:** every posting says "full time Spring Intern, but also have availability for Summer 2027 and extended Co-Op positions." Mechanical Design, Advanced Manufacturing, Test and Electromagnetics all accept Mechanical Engineering and are STRONG. **Power Electronics is CLOSED, EE and Computer Engineering only, confirmed.** Fifteen minutes from him and the best technical fit on the board.
- **Oxy**, Engineering Intern, Oil and Gas. Req JR110204. Summer 2027, May to August, 12 weeks. **Relocation assistance and/or fully furnished corporate housing provided.** Any engineering degree, GPA 2.85. **Graduation window December 2027 to May 2029, and he graduates May 2028, so he qualifies.** Upgraded to STRONG. Two catches: **must apply at oxy.com/students to be considered**, and Platteville is not among the six Workday locations even though the prose mentions Colorado.
- **AMD**, 2027 Undergrad Product Development Engineering Intern/Co-op. Req 90790, Longmont and Fort Collins among the sites. Summer 2027, May 24 to Aug 13. **Downgraded to STRETCH: the posting asks for CS, Computer Engineering or EE and does not name Mechanical Engineering**, and every listed skill is software or circuit theory. Applying registers general interest across all AMD intern reqs, which is the only reason to keep it. Posted annually at $59,072 to $88,608, stored as `$28-43/hr est.`
- **Explico**, Denver. $18-25/hr, red. **Accident reconstruction, biomechanics, human factors, visualization and marketing.** No mechanical design track. Wrong field. Kept as WATCH and a last resort only.
- **Zipline**, South San Francisco. Summer 2027, May/June to Aug/Sept. Second year of undergrad must be completed. Housing SILENT. **Wage was not readable, chip stays.**
- **Skydio**, San Mateo. $41/hr undergrad, the highest wage found. E-Verify only, no ITAR clause. Housing SILENT. **Term never stated, chip stays.**
- **MatX**, Mountain View. **Not listed on MatX's own job board as of 2026-08-21**, which shows eight full time engineering roles and no interns. Absence is strong evidence but not proof, so it stays unverifiable rather than closed. Weakest fit anyway.

**Eight VERIFY chips remain**, down from 18: Oxy (wage), Zipline (wage), Skydio (term), MatX (term and whether it is live), Kairos (housing), Elliott (relocation), and **HSF and GMiS on the scholarship tab**.

**HSF and GMiS were a surprise.** This file previously said "nothing open except AIAA" on the scholarship side. Two scholarship rows carrying VERIFY chips contradicts that. Nobody has looked at them. Do that before trusting any scholarship claim in this file.

### RELOCATION RULE CHANGED BY JOAQUIN, 2026-08-21

He will apply to out-of-state roles **even when housing or relocation is not supported.** Out-of-state is no longer capped at STRETCH. Instead every such row must state plainly which of these is true:

- the listing is **SILENT** on housing and relocation, or
- the listing **EXPLICITLY refuses** relocation help.

Silence is not refusal and must not be written as if it were.

**`CLAUDE.md` in this repo carries the corrected wording**, so a session reading the repo gets the right rule. Hard rule 6 in the claude.ai project settings still states the OLD policy and a session cannot edit it from inside; that only matters for Cowork and chat sessions on that project. Elliott and Anduril still carry stale reasoning under the new policy and have not been re-scored.

### WAGE FLOOR IS A PREFERENCE, NOT A FILTER, decided 2026-08-21

`BASE_WAGE=26` is the Kelvin floor. Joaquin will still apply to roles under it as a last resort. Under-floor rows render red through the existing `.wg.down` style and are **never filtered and never downranked**. Five rows are currently red: IMEG $22-24, Kiewit $18-25, Explico $18-25, Marotta $18-24, Jacobs $19.20.

### ITAR, since it comes up constantly

International Traffic in Arms Regulations. US law covering aerospace and defense technology; a covered employer may only let a "US person" see the technical detail, so they screen at application. A US person is a US citizen, a lawful permanent resident, or someone with asylum or refugee status. It is about immigration status, not origin, and it is **not** a security clearance. Currently binding on Boom and Freeform. **Joaquin has not confirmed his status either way; do not assume it.**

---

## 3. Dashboard architecture

Five arrays in the script block: `INT`, `SCH`, `CAL`, `OUT`, `PROF`. Days Left and the Do next score compute on every load and are never stored.

`INT` row: `[conviction, company, role, location, term, deadline, source, url, packetStatus, notes, status, hint, wage, SLUG]`
`SCH` row: `[conviction, name, sponsor, award, opensRaw, deadline, gate, url, packetStatus, notes, status, hint, SLUG]`

Slug is the last field: **index 13 on `INT`, index 12 on `SCH`**, read through `SLUG_AT[kind]`. **Assign a slug to every new row, never change an existing one.** **30 INT slugs as of 2026-08-21**, all unique, the newest being `int-h3x-electromagnetics-intern`. Slugs are `[a-z0-9-]` only.

Conviction weights: `MUST APPLY 100, STRONG 70, STRETCH 40, WATCH 15`. `BASE_WAGE=26`, the Kelvin floor. Statuses: `OPEN`, `NOTYET`, `UNCONFIRMED` (-40), `BLOCKED` (-400), `CLOSED` (-800). A note containing `[UNVERIFIED]` or `STILL CONFIRM` fires the VERIFY chip.

**Wage display.** `.wg.down` sets `color:var(--must);background:var(--blbg)` when a wage range tops out below `BASE_WAGE`. It already existed; reuse it rather than adding a second colour. The chip is an inline-block span inside the cell, so the stacked-card layout under 700px is unaffected. **Wages derived from an annual figure carry an `est.` marker** and the annual number lives in the note, not the wage field. AMD was the first of these: `$28-43/hr est.` from $59,072 to $88,608.

### Applied state: publish(html), shipped and WORKING

**The files form of publish is dead for this artifact.** `claude.use("artifact")` returns a real namespace, so the capability is granted, but `publish({path:...})` rejects `capability_disabled`, "publishing files is not available in this view". Private artifact, Chrome, owner: none of the documented causes except the artifact itself. **Permanent for the view, never retry it.**

**Current route: the page rebuilds its own source and republishes with `publish(html)`.**

- Shared state lives inline between `/*ACC-STATE*/` and `/*/ACC-STATE*/` as `const PUB={...}`. It travels with the document, so any browser opening the artifact sees it. No data file, no fetch, no 404.
- `buildDoc()` fetches `index.html`, cuts authored content out on `<!--ACC-HEAD-->` / `<!--/ACC-HEAD-->` and `<!--ACC-BODY-->` / `<!--/ACC-BODY-->`, swaps the state block, re-wraps into a complete document.
- **Marker strings are assembled at runtime** (`MK=x=>"<!--"+x+"-->"`, `S_A="/*"+"ACC-STATE"+"*/"`). If the literals appeared whole in the script, `indexOf` would find those instead of the real markers.
- Never serialize the live DOM; it carries the injected runtime and viewer session state.
- On success **this view reloads**. Tab, filter, sort, expanded notes and scroll are parked in `sessionStorage` (`acc_ui_v1`) before the call and restored by `restoreUI()`. Chip says "saving ticks, the page will refresh".
- Debounced 3500ms. A tick during an in-flight publish is safe: `flushSave` compares what it sent against the state now and reschedules if they differ.
- An idle load does not publish.
- Load priority: unpublished local ticks, then published state, then device memory, then `SEED`. Compared canonically so key order cannot fake a dirty flag.
- `localStorage` (`acc_applied_v3`) is the backstop on every path.
- `conflict` treated as synced. `rate_limited` backs off 15s. `not_writer` / `not_granted` / `not_declared` / `consent_required` / `capability_disabled` / `capability_removed` / `read_only_path` are permanent, drop to read-only. `too_large` / `invalid_content` / `transform_error` stop and log.

**Live doc is still rejected:** it is a property an artifact is CREATED with and a republish cannot convert one, and every table is built from JS arrays at render time, explicitly not part of a live doc.

**`db` would suit this far better than self-publishing.** The frame runtime ships a module (`db.CRhVHzSt.js`; full set: artifact, assets, comments, db, downloads, embed, mcp, permissions, room, sample, self, user) but `db` is not on the list this account may declare. Revisit if that changes.

### THE WORKING PROCEDURE, CHEAPEST FIRST: ship a change from a CLOUD Claude Code session

Proven 2026-08-22 on the Build letter delegation change. No laptop, no console, nothing on his desk. Same shape as the local procedure below, with step 1 replaced:

1. **Read the artifact with the Artifact tool's `read` action**, not `WebFetch`. It returns the whole document and sets the tracked baseVersion. `WebFetch` still cannot reach the frame host from behind the egress proxy and is not needed.
2. Reconstruct with `dashboard/verify/mkbase2.py`. Plain for the publish payload so the live ticks survive; `--null-state` for the copy committed to `dashboard/`.
3. Edit the reconstruction as an **anchored find/replace**. `dashboard/patches/` holds the scripts and each refuses to write if an anchor is missing or doubled.
4. Verify before sending: `dashboard/verify/run.sh <build>` for all 56 assertions, plus the tick count and the marker counts on the payload itself. The full publish procedure is `docs/artifact-publish-runbook.md`.
5. Publish passing the **url** and the favicon `🎯`. No `force`, no `capabilities` object.
6. Read back and check row counts, unique slugs, tick count, markers, **and the html/body wrapper count**. See the nesting note below.

**The wrapper nesting is real and self-healing.** A publish through this route came back with two html and body wrappers as markup where one went in. Reconstructing that published version collapses it to one, that reconstruction is byte-identical to a reconstruction of the payload, and a third generation does not drift. So the page normalises it on the next tick and nothing ratchets. Check it every time anyway with `markupCounts` from `dashboard/verify/accdoc.js`; one clean case is not a proof.

### THE OLDER PROCEDURE: ship a change from a LOCAL Code-tab session

Proven twice, most recently on a sixteen-row change 2026-08-21. Desktop app, Code tab, **Local** session. Then:

1. `WebFetch` the artifact URL. This sets the tracked baseVersion and is what unlocks the tool.
2. **Reconstruct the authored document from the marker pairs.** The read returns the SHELL'S transformed copy, not the authored source. Cut on `<!--ACC-HEAD-->` / `<!--/ACC-HEAD-->` and `<!--ACC-BODY-->` / `<!--/ACC-BODY-->` and re-wrap, exactly as `buildDoc()` does. **The pasting is gone; the reconstruction dance is not.** A prompt that omits this will try to edit the served document in place and produce garbage.
3. Edit the reconstruction.
4. Publish passing the artifact **url**. No `force`. No `capabilities` object at all. **Pass the favicon `🎯`** so the tab icon stays stable.
5. Read back and re-verify.

### THE HAZARD THAT COST ONE SESSION A MEMORY UPDATE

**A local Code-tab session did not see claude.ai project docs.** On 2026-08-21 the session reported that `claude/verification-2026-08-21.md` "does not exist anywhere I can see", and its edit to `MEMORY.md` landed on a local file, not on the project doc, which was still showing the old version slug afterwards. It works on the filesystem, not on the project.

**The repo migration is the fix for this.** A session with the repo checked out reads `docs/MEMORY.md` off the filesystem and can commit the update back. Until the repo is the working copy everywhere, two rules still apply:

- **Put every fact a local session needs directly in the prompt** if it is not working in the repo. Never point it at a claude.ai project doc path.
- **Verify a memory update landed** with `project_read`, or with `git diff`, rather than trusting the report.

**Known wrapper behavior, benign but understand it.** The Artifact tool wraps published content in its own body skeleton, so a publish through this route leaves the authored document nested one level deeper. Two markup instances of `<html` and `<body` on the live page is the expected result, not an error. It self-repairs on the next tick. Confirmed again 2026-08-21 on `1787353283-20cc`. **Nesting cannot compound so long as step 2 is always performed**, because reconstructing from the markers discards any wrapper. That is the real reason step 2 is mandatory.

**Gates that must be in the prompt every time:**

- Parse the `ACC-STATE` block before and after, and refuse to publish if the tick count changed. Best practice, proven on the sixteen-row change: keep the block **byte-identical** between edit base and payload and never rewrite it at all.
- **NEVER gate on absolute document length.** This cost a failed attempt on 2026-08-21: the gate was set from a build whose state block held `applied:null`, and the moment a tick saved, the live page grew 586 characters and every baked-in number went stale. **Gate on the DELTA the edits produce.** State and structure must be checked independently.
- Assert every marker appears exactly once, row slugs are unique, and no injected runtime leaked in.
- Log the reconstructed length and the applied-tick count so a failure is diagnosable from one line.
- **Expect your own assertions to be wrong before the edit is.** Two gates failed on the 2026-08-21 run and both were bad assertions, not bad edits.

**Reference numbers from the sixteen-row change:** reconstructed 79,242 chars, published 80,838, delta +1,596, 14 ticks before and after, capability declaration `{artifact, downloads}` contract 0.2.11 carried forward.

### How to ship a dashboard change by console script, the current fallback

1. Get the live source through the console route and reconstruct the authored document.
2. Derive the **canonical reconstruction** as your edit base, not the file you last published. `buildDoc`'s wrapper normalises the head/body seam and drops the trailing newline, so the reconstruction is one character shorter than the published file. That reconstruction is the fixed point.
3. Build the new version locally and verify with the harness in section 7.
4. Compute **anchored find/replace edits**, never byte offsets. Whitespace drifts across a shell round trip.
5. Apply the same gates listed above.
6. Rehearse in Playwright against a simulated shell copy **that carries a realistic state block**, and assert byte-identical output.

### Other current behavior

- **`SWEPT` is derived** from the newest `Last Checked` in `CAL` (index 6). A CAL row for the LinkedIn alerts was added 2026-08-21, so the header now reads that date.
- **Mobile.** Viewport meta plus a JS guard. Tables in `.tw` (`overflow-x:auto`); under 700px rows become stacked cards. 0px horizontal overflow at 390, 760, 1440.
- **Term strings are compacted to fit the column.** AMD reads `Summer 2027 (May 24-Aug 13)` and Oxy reads `Summer 2027 (May-Aug, 12 wks)`; the full wording including co-op options is verbatim in the notes.
- **Repo versus live, checked and reconciled 2026-08-22.** A cloud session read `1787428545-d4e8` and found the repo two builds behind: the live board carried **41 internship rows and 14 ticks**, the file committed as `pre16row` carried 29 and a null state, and Boom Supersonic was still unverified there as Englewood. Fixed both ways. The refreshed authored build is `dashboard/application-command-center-1787428545-41row.html`, null state, 48 assertions passing, and the live page was republished as `1787430085-95fa` carrying the same change with all 14 ticks intact. **Any future republish still has to be built from a fresh read**, never from the null-state file in the repo, or the ticks go to null.
- Stat pills tab scoped. Notes collapse to one line. **Build letter** per row copies an **orchestration prompt** as of 2026-08-22: it is addressed to Opus and tells Opus to hand the drafting to a Sonnet subagent, then read the result back and fix the voice before the link reaches Joaquin. The brief inside it is self-contained, because a subagent starts cold and can see neither the chat nor the dashboard. Internship and scholarship rows differ only in the last line each asks for, housing status versus essay-bank coverage. Assertions I1 to I7 in `dashboard/verify/verify.js` hold that shape. **Export Applied** uses `downloads` with a blob fallback. **Sweep buttons** call `window.cowork.runScheduledTask` where it exists, else copy the run command. Note these buttons will not work from a routine-driven world; revisit once the sweeps move.

---

## 4. Known bugs and weaknesses

1. **Applied state.** Laptop to phone **CONFIRMED WORKING 2026-08-21**. **Phone to laptop is still OPEN, see bug 14.**
2. ~~Row keys fragile.~~ FIXED.
3. ~~Sideways scroll on phone.~~ FIXED.
4. ~~`SWEPT` hardcoded.~~ FIXED.
5. **Capability declarations.** **Omitting** `capabilities` on a redeploy carries the stored declaration forward and preserves the contract pin. `{}` is an explicit clear-all. A **non-empty object** is a full-set declaration and revokes anything not restated. Re-confirmed on the 2026-08-21 sixteen-row publish.
6. Toggling a note calls a full `render()`, which can jump scroll on long tables. Low harm, and more visible now the board is 30 rows.
7. ~~404 for `data/applied.json`.~~ FIXED, the file is gone.
8. ~~State fix unverified against the real runtime.~~ Superseded.
9. ~~Read-only chip cause unknown.~~ **CLOSED.**
10. ~~Host versus artifact for the disabled files form.~~ **CLOSED.** It is the artifact.
11. ~~Whether `fetch('index.html')` returns a complete document.~~ **CLOSED.**
12. **HALF CLOSED.** Interactive dashboard writes are SOLVED via a local Code-tab session, route 0 in section 1, procedure in section 3, now proven on a real multi-row change. **Still open for the sweeps only**, which need to run with the laptop closed and therefore need a cloud routine pinned to `empluzz`. That needs GitHub connected to Claude; as of 2026-08-21 his account showed three authorized OAuth apps (Git Credential Manager, GitHub CLI, Visual Studio Code) and one GitHub App (Copilot Chat), none of them Claude. Repo `joaquinz0721/The-Sweeper` exists. Note before connecting: the docs state a cloud session can reach any repository the connected account can see, not only the ones ticked at install.
13. **OPEN, low.** ZipRecruiter returns annual salary only, no hourly and no deadline. Any ZipRecruiter row needs a conversion and an `est.` marker. The convention now exists and is applied to AMD, so this is a matter of using it, not inventing it.
14. **OPEN. Phone-to-laptop ticks do not travel.** He unticked Marotta on his phone and it never reached the laptop. Leading theory: the 3500ms debounce never fired because backgrounding or locking a phone suspends timers, so no publish was attempted. Planned fix: flush on `visibilitychange` when hidden and dirty, plus a manual save control so a tick never depends on a timer surviving. Not yet built.
15. ~~Harness ticks a phantom slug.~~ **FIXED 2026-08-22 in the rebuilt harness.** It asserts the slug exists in `INT` before toggling, asserts `int-marotta-controls-me-intern` is absent, and `mklive3.py` refuses to build a fixture that ticks an unknown slug.
16. **NARROWED, process.** A local Code-tab session cannot see claude.ai project docs. In the repo this stops mattering, since the docs are files. Any prompt sent to a session that is NOT working in the repo must still carry its facts inline.
17. **OPEN, cosmetic but wrong.** Oxy's location field still reads `Platteville, CO`. The Workday req lists six sites, none of them Platteville, though the posting prose mentions Colorado. The note carries the doubt; the field does not. Fix it on the next write, or confirm the Colorado placement first.

---

## 5. Working rules

The hard rules live in `CLAUDE.md` at the repo root and are loaded automatically. Summary of the ones that bite most often:

**NEVER CONSOLIDATE ROWS, standing instruction from Joaquin 2026-08-21.** Every eligible requisition gets its own row and its own slug, forever, even when several sit at the same company. He intends to apply to each one separately. H3X currently holds five rows. Do not tidy them into one, ever, and do not let a future session decide it would be neater.

**The wage floor is a preference, not a filter.** See section 2. Under-floor rows stay on the board, render red, and keep their scoring.

**Tools he has, and tools he does not.** Never claim FEA, CFD, NX, Teamcenter or ANSYS. Add to that list, confirmed by Joaquin 2026-08-21: **he does not have AutoCAD and does not have any BIM or Revit experience. SolidWorks is his CAD.** MEP and building-services postings ask for AutoCAD or BIM constantly, IMEG among them. Write around it by leading with SolidWorks depth and the additive and thermal work; never imply the others.

Rule 3, no browser for tracker data, was deliberately lifted for one test on 2026-08-21 and the test came back negative on structural grounds, so the rule now has a technical reason as well as an economic one. See section 1 route 3.

Cost discipline: one publish per change, never per-cell editing. Start a fresh session for packet work. Sonnet is fine for assembly; use Opus when a cover letter or essay is the deliverable.

---

## 6. Next up, in order

0. ~~**RETEST THE ARTIFACT READ FROM A CLOUD SESSION.**~~ **DONE 2026-08-22, and it does more than read.** The Artifact tool's `read` action returned the whole document from a cloud session, and the publish that followed succeeded. Route 0a in section 1. `WebFetch` was never tried, so nothing here says the allowlist works; the tool route simply does not need it. **The open question is now narrower: can a scheduled routine do the same?** That is a different surface and it is what the sweeps actually need. Test it the same way, with the Artifact tool rather than `WebFetch`, before building anything on it. **The Cowork half of this question is also answered, 2026-08-24:** a brand new Cowork session still cannot read the artifact, same allowlist error, so the provisioning excuse is spent and Cowork is confirmed not bound to `empluzz`. See section 1. Stop retesting that.
1. **IMEG, deadline 2026-09-19.** Nearest date on the board and the next thing to do. **Unblocked:** the AutoCAD question is settled, he has SolidWorks only, so the letter works around it per section 5. Write it in a fresh chat on Opus with the packet builder skill.
2. **Confirm his ITAR status.** Citizen, green card, asylum or refugee status all qualify. It gates Boom and Freeform and takes him ten seconds to answer.
3. **Join SHPE.** Real-world action only he can take, hard cliff February 2027, unblocks ScholarSHPE.
4. **ACEC Colorado scholarship, Oct 1.** Second nearest date on the board. No packet started.
5. **Look at HSF and GMiS.** Two scholarship rows carry VERIFY chips and nobody knows what they are. This file's claim that only AIAA is open is not trustworthy until that is checked.
6. **Finish the six rows that still need a fact:** Oxy wage, Zipline wage, Skydio term, MatX whether it is live at all, Kairos housing, Elliott relocation.
7. **Re-score Elliott and Anduril** under the new relocation policy.
8. **Fix Oxy's location field** (bug 17) on the next dashboard write.
9. ~~**Commit the dashboard build and the verification harness.**~~ **DONE 2026-08-22.** The harness was rebuilt from its description; the build came from the live artifact through route 0a, not from the device. The repo can verify a change.
10. **Connect GitHub to Claude, then recreate the sweeps as cloud routines** pinned to `empluzz`. All that remains of bug 12.
11. **Fix the phone-to-laptop save gap** (bug 14).
12. **Fold ZipRecruiter into the internship sweep** (section 8). Needs a term filter; the salary conversion convention now exists.
13. **Watch for the first recurring LinkedIn digest** and record its subject format (section 9).
14. Tailored-resume button. Back burner.
15. Send the support request in `docs/support-request.md`. Background long shot, do not block on it.

---

## 6b. Route 0a FAILED on 2026-08-25, and what it cost

**Resolved the same day, from a different session.** A fresh cloud session
fetched the artifact, read all 1107 lines, and published on the first attempt:
live version `1787695423-9d50`, 17 ticks, 41 INT and 12 SCH rows unchanged, all
56 assertions green. The difference was the session, not the procedure. The full
method, the gate's two errors and the exits are now in
`docs/artifact-publish-runbook.md`, which is the file to read before any future
republish. What follows is the failure itself, kept because the diagnosis is what
makes the runbook's rules make sense.

The coursework rule for the Build letter button could not be published from a
cloud Claude Code session. Route 0a worked twice before; it did not work this
time and the reason is worth writing down.

**The loop.** The Artifact tool's publish gate alternates between two refusals
and there is no state in which both are satisfied:

- Straight after `action:"read"`: *"You hadn't viewed the live version of this
  artifact, so the publish was refused ... that version counts as viewed once you
  have Read every line of that file."*
- After Reading all 1107 lines of the saved file: *"this is the identical content
  already refused against the newer version 1787690446-c1a6, resent unchanged."*

Changing the content between attempts does not break the loop. Two genuine edits
were added mid-cycle (the stale 41-assertion string, then the coursework rule in
the voice-pass checklist) and the next attempt went back to "hadn't viewed". Five
full reads of the 124.9KB file were performed across the attempts, all after a
fresh fetch, and none of them registered.

**Force is not the escape hatch here.** `force:true`, with Joaquin's explicit
confirmation, returns a server error rather than a tool refusal:

    deploy 400: this artifact self-publishes - provide the baseVersion you edited from

The Artifact tool exposes no `baseVersion` parameter, so a forced publish cannot
satisfy that check. This is specific to a self-publishing artifact: the page
writes its own new versions when a tick is saved, and the last version, c1a6, was
saved from inside the page on 2026-08-25.

**What this costs.** Roughly 250K tokens of reads for nothing. Do not retry the
cycle from a cloud session on the strength of "route 0a is proven": it is proven
for a version the page did not write. **Before spending anything, publish a
one-line probe change and see whether it lands.**

**What still works.** The merged build itself was fine: fresh read, 17 ticks
intact, 41 INT and 12 SCH rows byte-identical, markers once each, 56 assertions
green. The blocker is the publish gate, not the payload. Route 0, the local
Code-tab route, was not tried this session and remains the fallback; the merged
file has to be carried there by hand because a state-carrying build is never
committed.

---

## 7. How to verify a dashboard change

**REBUILT AND COMMITTED 2026-08-22, `dashboard/verify/`.** The original six files were never on device `jz` and died with their container. They were rebuilt from this section's description, which turned out to carry enough detail to do it. **56 assertions, all passing**, re-measured 2026-08-25 on Node 22, Python 3.11 and Chromium: 41 in `verify.js`, 8 in `verify-upgrade.js`, 7 in `verify-upgrade2.js`. It read 48 (33 + 8 + 7) until I8 to I15 were added to `verify.js`. This paragraph said **41** until 2026-08-24; that was the count of the ORIGINAL harness described in prose here, carried over into the rebuild's write-up by mistake. The rebuild landed at 48 and `dashboard/verify/README.md` said so from the start. **56 is the number.** Both places that used to say 41, `sweepPrompt()` in the dashboard HTML and the header comment in `dashboard/verify/run.sh`, were corrected on 2026-08-25 and the button text shipped in live version `1787695423-9d50`. Run `dashboard/verify/run.sh`. The file set is `accdoc.py`, `accdoc.js`, `shell.py`, `mkbase2.py`, `mklive3.py`, `harness.js`, `verify.js`, `verify-upgrade.js`, `verify-upgrade2.js`, `shots.js`, `run.sh`; the per-file breakdown and the full assertion inventory are in `dashboard/verify/README.md`.

Three things the rebuild confirmed independently, worth recording because each was previously only an assertion in prose:

- **The committed build is already its own canonical reconstruction.** `rebuild(src) == src`, byte for byte. The fixed point is real and measurable, not a figure of speech.
- **The applied:null trap reproduces exactly.** Baking the 14 ticks into that build grows it by **+586 characters**, the same number this file recorded from the failed gate on 2026-08-21. The harness now rehearses against a realistic state block by default, which is what `mklive3.py` is for.
- **Wrapper nesting cannot compound.** Three generations of publish-then-shell-transform converge byte-identically, provided the marker reconstruction is always performed. That was the theory in section 3; it is now tested.

- Serve over `http://localhost` (not `file://`), **at a path matching the `<base href>` the shell injects**, or the page's fetch of its own source 404s.
- Simulate the shell transform: inject a frame-runtime head, drop the `cowork-artifact-meta` block, dissolve the `</head><body>` seam.
- Stub `window.claude.use` five ways: absent, `publish` resolving, and `publish` rejecting `not_writer`, `capability_disabled`, `conflict`. **The `capability_disabled` case is the real production condition and no earlier stub covered it.**
- Assert the payload is a full document, carries no injected runtime, contains the new tick and the seed rows.
- **Assert the round trip is a fixed point:** transform the published document again, confirm every marker appears exactly once, then load that second generation in a clean browser with no `localStorage` and confirm the tick is present and it does not immediately republish.
- Assert `sessionStorage` UI restore, and that an idle load publishes nothing.
- Assert `scrollWidth === clientWidth` at 390, 760, 1440.
- Serve a copy with the shell's viewport meta removed to prove the JS guard carries mobile alone.
- **Use real slugs** (bug 15) and assert the slug exists in `INT` before toggling it.
- Take the screenshots and actually look at them.

**Two traps the 2026-08-22 rebuild fell into, both bad assertions rather than bad code.** Counting `<html>` as a raw substring reports two wrappers on a healthy document, because `buildDoc()` carries that literal inside its own script; strip script bodies before counting. And a ticked row leaves the Internships tab for the Applied archive, so an assertion that looks for its checkbox on the default tab reads a survived tick as a lost one. Both are the rule in section 3 playing out: expect your own assertions to be wrong before the edit is.

**Caveat that cost two sessions: a green local run is evidence the code is right, never that the feature works.** The first build passed four stubs and failed in production because the runtime does not serve the form it was built on. The console probe is the better instrument: `await claude.use("artifact")` then a real call, in his browser, in the artifact frame. Thirty seconds, no network needed.

---

## 8. ZipRecruiter connector, observed 2026-08-21

Installed and working, no auth prompt. One tool, `mcp__ZipRecruiter__search_jobs`, deferred so load it with ToolSearch. US and Canada only.

**Arguments:** `job_role`, `location` (concrete city/state/zip, not "near me"), `radius_miles`, `employment_types` (use `INTERNSHIP`), `location_types` (`PHYSICAL`/`REMOTE`/`HYBRID`), `seniority_classes` (`NO_EXPERIENCE`/`JUNIOR`/`MID`/`SENIOR`), `salary_min`/`salary_max` (annual, max 300000), `max_posted_minutes_ago` (min 1440), `offset`, `skills`, `country_admin_code`, `unsupported_filters`.

**Result fields:** `title`, `company`, `location`, `is_remote`, `salary:{min_annual,max_annual}` (either may be null), `company_logo`, `job_redirect_url`, `job_type`, `benefits`, `days_ago`. Envelope: `request`, `results`, `status`, `meta:{count,limit,total}`, `search_url`, `warnings`.

**What matters:** page size is **5** (probe returned count 5, limit 5, total 16), so paginate with `offset` or most rows are never seen. Salary is **annual only**. **No deadline field**; `days_ago` is the only time signal. `job_redirect_url` is a tokenised redirect, not a clean posting URL. **No term scoping**: a probe for "mechanical engineering intern" near Boulder returned mostly Summer 2026 and adjacent disciplines, so filter on term and mark anything unstated UNCONFIRMED. No housing or relocation data, so state SILENT per the new rule.

---

## 9. Job sources, observed 2026-08-21

### LinkedIn alerts

Four alerts created 2026-08-21, all four confirmation mails read the same day.

- **Sender: `jobalerts-noreply@linkedin.com`.** Narrow the sweep query to `from:jobalerts-noreply@linkedin.com newer_than:8d`.
- **Subject format (creation): `Joaquin: your job alert for {NAME} in {LOCATION} has been created`.**
- **The confirmation mails carry a first batch of matches**, which is where the new rows came from. They are not just receipts.
- **The recurring digest has NOT arrived yet**, so its subject format is unknown. Keep the query broad enough to catch both, and record the digest format here when it lands.
- `search_threads` returns previews without bodies. Use `get_thread` with `messageFormat: PLAIN_TEXT` per thread.
- The alerts overlap heavily; dedupe by LinkedIn job id from the `jobs/view/{id}` URL. Four alerts deduped to 15 unique postings.
- The four alerts: Mechanical Engineering Intern Summer 2027 (Denver), Manufacturing Engineering Intern (Denver), mechanical Engineering Intern (Denver), design Engineer Intern (**United States**).
- **Two cosmetic issues on his end:** two alert names carry a stray leading tab from pasting, and the design alert is scoped nationwide, which is why the California roles appeared. Rescope it to Denver if that becomes noise.

### Reading a posting, what actually works

Learned the hard way on 2026-08-21 while verifying eleven rows.

- **LinkedIn job pages are unreadable.** `WebFetch` returns `ROBOTS_DISALLOWED`. Do not try. The alert mail gives you the job id; go find the employer's own posting with it.
- **Workday and Phenom portals do not render.** IMEG (`imeg.wd1.myworkdayjobs.com`), Oxy (`oxy.wd5.myworkdayjobs.com`) and AMD (`careers.amd.com`) all returned navigation chrome and no job body. These need Joaquin to open them and paste, which is exactly what he did.
- **Greenhouse, Ashby and Rippling read cleanly.** Freeform (`job-boards.greenhouse.io/freeformfuturecorp`), Skydio and MatX (`jobs.ashbyhq.com/<slug>`, and the JSON at `api.ashbyhq.com/posting-api/job-board/<slug>` when the page will not load), Boom (`ats.rippling.com/boom-supersonic`).
- **Built In Colorado is the best source for small Colorado companies.** All five H3X reqs came from `builtincolorado.com/company/h3x-technologies`, including one that was not in any alert.
- **Aggregator mirrors work when the original will not.** Zipline came from the Techstars job board. Treat anything missing there as unread rather than absent; Zipline's wage is missing for exactly this reason.
- **The Indeed connector found none of these.** Fresh postings are not syndicated to it. Do not spend calls on it for new reqs.

---

## 10. TO DO: never touched

Items never started, or planned and not built. Section 6 is the priority ordering; this section is the inventory. Move an item out only when it is genuinely done, and say where the work landed.

### Applications

- [x] ~~Read the postings carrying VERIFY chips.~~ **DONE 2026-08-21.** Eleven read from employer sources, three of those (IMEG, AMD, Oxy) pasted in by Joaquin because their portals will not render. Evidence in `docs/verification-2026-08-21.md`, shipped to the board in version `1787353283-20cc`.
- [ ] **IMEG letter, deadline 2026-09-19.** No longer blocked. He has SolidWorks only, no AutoCAD and no BIM, so the letter is written around that per section 5. Fresh chat, Opus.
- [ ] **Confirm his ITAR status.** Gates Boom and Freeform.
- [ ] **Six rows still need one fact each:** Oxy wage, Zipline wage, Skydio term, MatX whether it is live, Kairos housing, Elliott relocation.
- [ ] **Re-score Elliott Machine Works and Anduril** under the relocation policy Joaquin changed on 2026-08-21. Elliott still says "capped at STRETCH per the relocation rule". Anduril still notes housing is not stated.
- [ ] Decide whether Explico and MatX stay on the board at all. Both were kept for now, Explico as a deliberate last resort.
- [x] ~~**Write down the post-application follow-up format.**~~ **DONE 2026-08-24.** Canonical in `.claude/skills/application-packet-builder/SKILL.md` under POST-APPLICATION FOLLOW-UP; background, the five defects, and both before-and-after pairs in `docs/followup.md`. Before that day the only spec anywhere was a single inline example sentence in a Google Doc, which is why the two generated follow-ups came out broken. `y'all` is banned permanently.
- [ ] **There are zero Gmail drafts in the account**, checked 2026-08-24. The two broken follow-ups were generated in chat and never saved anywhere, which is why `docs/followup.md` quotes them rather than linking them. Nothing has ever been sent.
- [ ] **No follow-up has been sent or drafted since the spec landed.** Kairos Power and Western Digital are the two that were attempted and both outputs were broken; they were never sent. Redraft them against the spec when he asks.

### Scholarships, all untouched

- [ ] **Join SHPE.** Must happen before February 2027 or ScholarSHPE stays blocked. Real-world action only Joaquin can take.
- [ ] **HSF and GMiS.** Two rows on the scholarship tab carry VERIFY chips and nobody has looked at either. Their existence contradicts the old claim that only AIAA is open, so do this before trusting anything else on that tab.
- [ ] ACEC Colorado, deadline Oct 1. No packet started.
- [ ] SME, the Helton renewal, deadline Nov 1. **Highest stakes on the board.** No packet started.
- [ ] CU Boulder General and BOLD, deadline Dec 1. No packets started.
- [ ] AIAA. Weak fit, WATCH. Decide whether to bother.

### Dashboard, planned and not built

- [ ] **Bug 14, phone-to-laptop ticks do not travel.** Planned fix: flush on `visibilitychange` when hidden and dirty, plus a manual save control so a tick never depends on a timer surviving a phone lock. Not written.
- [x] ~~Bug 15, harness flaw.~~ **FIXED 2026-08-22** in the rebuilt harness.
- [x] ~~**Build letter delegates to a Sonnet subagent.**~~ **SHIPPED 2026-08-22**, live in `1787430085-95fa`. The button copies a prompt addressed to Opus that hands the drafting to a Sonnet subagent and keeps the voice pass with Opus. `docs/history/build-letter-delegation-2026-08-22.md`.
- [ ] **Bug 17, Oxy's location field** still reads Platteville when the req does not list it.
- [ ] **Bug 6**, toggling a note calls a full `render()` and can jump scroll on long tables. More visible now the board is 41 internship rows.
- [ ] **Sweep buttons will break when the sweeps move to routines.** They call `window.cowork.runScheduledTask`. Nothing has been designed to replace that.
- [ ] **The Follow-up button is NOT built.** The prompt that ships it is written and unshipped at `prompts/followup-button.md`, dated 2026-08-24. It adds a per-row **Follow-up** button beside **Build letter** on both tables, copying a self-contained prompt for the post-application follow-up. It needs a route 0 or route 0a publish and it is its own job. The format spec it depends on is now at `.claude/skills/application-packet-builder/references/followup.md`, and the three-item experience list it inlines became two or three on 2026-08-24. Regenerate the clipboard text from that file.
- [x] ~~**Stale string: `sweepPrompt()` said "all 41 assertions must pass".**~~ **DONE 2026-08-25**, shipped in live version `1787695423-9d50`. The harness has 56 (41 + 8 + 7) and the button now says 56. `dashboard/verify/run.sh` and `docs/sweep-pipeline.md` agree.
- [ ] **The sweep buttons point at two things that do not exist.** `sweepPrompt()` tells the receiving session to run `python3 dashboard/ingest.py` and to publish `dashboard/application-command-center.html`. **Neither file exists**, in the working tree or in any commit. `docs/sweep-pipeline.md`, which the same prompt names, was created 2026-08-24 as an honest stub saying exactly that. Anyone pressing a sweep button today is sent to nothing. Building the pipeline is a separate job; see the Plumbing group.
- [ ] Tailored-resume button. Back burner, never started.

### Plumbing

- [x] ~~**Get the CURRENT dashboard source into `dashboard/`.**~~ **DONE 2026-08-22**, and not from the device, which never had it. Read the live artifact from a cloud session with the Artifact tool, reconstructed it with `mkbase2.py --null-state`, committed it as `application-command-center-1787428545-41row.html`. 41 internship rows against the 29 in the old committed build.
- [x] ~~**Commit the verification harness into `dashboard/verify/`.**~~ **DONE 2026-08-22**, rebuilt rather than recovered. 48 assertions then, 56 now.
- [x] ~~**Get the work onto `main`, again.**~~ **DONE 2026-08-25.** `main` in `joaquinz0721/Sweep` was three sessions behind at `3b2ea9c`, with the writing system on it but not the tone rules, the coursework fix, the runbook, the doc reconciliation or the current build. Fast-forwarded to `9a853de` on Joaquin's say-so, no merge commit. **`main` is the branch to read from again.** `claude/publish-app-command-center-merged-m3z4ik` is merged in and safe to delete, as are `claude/blissful-mendel-cpxh8b`, `claude/build-letter-sonnet-subagent-tb2j0a`, `claude/career-ops-research-unsklz` and `claude/freeform-cover-letter-ftpu5i`. **A cloud session cannot delete a remote branch**: the git relay returns HTTP 403 on a delete refspec while ordinary pushes work, and the GitHub tools expose no branch-delete call. Joaquin deletes them, or nobody does. Still unmerged and left alone: `claude/empluzz-repo-access-jw3npv` (5 commits) and `claude/zen-ramanujan-vopvob` (7). If a future session lands on a `claude/...` branch, ask before fast-forwarding `main`, then do it rather than leaving the work stranded.
- [x] ~~**Actually commit the skill to `.claude/skills/`.**~~ **DONE 2026-08-24.** `CLAUDE.md` and `MIGRATION.md` had both claimed since the migration that `application-packet-builder` was committed here belt and braces. **It was not.** The directory existed in no commit in this repo's history. The account-synced copy was found at `~/.claude/skills/synced/application-packet-builder/` and copied in byte for byte, then the POST-APPLICATION FOLLOW-UP section was appended to `SKILL.md`. The claim is true now. **Committing it here does NOT update the copy on his claude.ai account, and the account copy is what Cowork loads.** He has to save the updated `SKILL.md` to his account himself.
- [ ] **Recover `sweep-prompt-internship.txt` and `sweep-prompt-scholarship.txt`.** Not on device `jz` either. The only surviving copies are inside the two desktop scheduled tasks; open each in the desktop app and copy the prompt out into `prompts/`.
- [x] ~~**RETEST the artifact read from a cloud session.**~~ **DONE 2026-08-22, and the publish works too.** Route 0a in section 1. The open version of this question is now about routines, which are a different surface.
- [x] ~~Confirm `window.cowork.runScheduledTask` exists in the artifact frame.~~ **ANSWERED 2026-08-21: it does not exist.** The run buttons are copy-a-prompt buttons. See section 1.
- [ ] **Build the sweep-ingest path** if the retest fails: the Paste sweep results control on the dashboard, and both sweep prompts rewritten to emit a JSON payload rather than attempting to publish. Design is in section 1.
- [ ] **Write `dashboard/ingest.py` and turn `docs/sweep-pipeline.md` from a stub into a procedure.** Confirmed 2026-08-24: `ingest.py` exists nowhere, not in the working tree, not in any blob in any commit, not on any reachable disk. `docs/sweep-pipeline.md` did not exist either and is now a stub that says so and records the six intended steps. **Nobody should follow the sweep button prompt until this is real.** Deliberately not written in that session; inventing an ingest pipeline to satisfy a dangling reference is worse than the dangling reference.
- [ ] **Connect GitHub to Claude**, then rebuild `internship-sweep---summer-27` and `scholarship-sweeper---26-27` as cloud routines pinned to `empluzz`. All that remains of bug 12.
- [x] ~~Check the repo files survived the copy-paste round trip.~~ **RESOLVED 2026-08-21 by regenerating every doc from the claude.ai project source rather than trusting the pasted copies.** `CLAUDE.md` and every file under `docs/` in this repo are the canonical versions.
- [x] ~~Update hard rule 6 in the claude.ai project settings.~~ **RESOLVED for the repo.** `CLAUDE.md` here carries the corrected relocation rule plus the never-consolidate rule, the wage-preference rule, and the AutoCAD and BIM exclusion. The claude.ai project settings are still stale and only matter for Cowork and chat sessions on that project; fix them there when convenient or retire the project once the repo is the working copy.
- [ ] **Fold ZipRecruiter into the internship sweep** (section 8). Needs a term filter; the `est.` conversion convention now exists.
- [ ] **Record the recurring LinkedIn digest subject format** (section 9) once the first one lands. Only the creation-confirmation format is known.
- [ ] Rescope the nationwide `design Engineer Intern` LinkedIn alert to Denver if the California rows become noise, and strip the stray leading tab from two alert names.
- [ ] **Confirm the favicon.** `🎯` was set 2026-08-21 because the publish requires the parameter and no prior value was on record. If the tab icon used to be something else, restore it and write it down in section 1.
- [ ] Send the support request in `docs/support-request.md`. Background long shot, do not block on it.
