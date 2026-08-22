# empluzz

Internship and scholarship search for Joaquin Zarazua. CU Boulder Mechanical Engineering, May 2028 graduation, targeting Summer 2027.

## Read this first

Read `docs/MEMORY.md` before doing anything else. It is the running memory file: live tracker URL, current application state, dashboard architecture, and the known bug list. It overrides anything below that conflicts with it. Update it at the end of any session that changes state.

## Where everything lives

- **Tracker, source of truth:** the hosted artifact at `https://claude.ai/code/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594`. Update rules are in `docs/MEMORY.md`. **Never publish to it without passing its URL**, or you create a duplicate and split the tracker in two. Never pass `force`. Never pass a `capabilities` object, since omitting it carries the stored declaration forward and a non-empty object revokes anything not restated. Pass the favicon `🎯` so the tab icon stays stable.
- **Dashboard source:** `dashboard/application-command-center.html`. The verification harness is in `dashboard/verify/`.
- **Google Sheet `138-KAgu9j9qCFeAn_pTTRWVmhEhXOwIpCTb2K8eraRk`:** FROZEN ARCHIVE. Never read it, never write to it. History through 2026-08-17 only.
- **Packets folder:** Drive ID `1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP`
- **His past cover letters, voice reference:** Drive ID `1pPulXeoTIXN6sJXuAByc2sW37dThROoB`
- **Skill:** `application-packet-builder`. It is enabled on his claude.ai account and also committed to `.claude/skills/` here, belt and braces. It carries the full packet spec.

## Which surface can write the tracker

Settled 2026-08-21, full evidence in `docs/artifact-write-routes.md`. Do not re-litigate any of it.

- **Local Code-tab session in the Desktop app: WORKS.** This is route 0 and the only proven interactive route. A local session has no egress proxy in front of it, so `WebFetch` reaches the frame host, the tracked baseVersion gets set, and the Artifact tool publishes normally. Procedure in `docs/MEMORY.md` section 3.
- **Cloud session pinned to the `empluzz` environment: should work, untested.** Needs `*.frame.claudeusercontent.com` on that environment's allowed-domains list, plus the **Also include default list of common package managers** checkbox or the verification harness loses npm and PyPI. A cloud session in `Default` cannot read the artifact. If a session finds it cannot read it, that is the environment, not a permissions problem. Report it and stop. Do not attempt a forced publish.
- **Cowork session: CANNOT, ever.** Cowork is not bound to cloud environments. Confirmed three ways.
- **Driving a browser: CANNOT.** The artifact runtime sits one cross-origin hop past where browser tools execute.

## Hard rules, no exceptions

1. **Never submit or transmit anything.** No applications, no emails, no forms. Assemble and hand over. He sends.
2. **Never write to the Google Sheet.** Dashboard only.
3. **Never drive a browser for tracker data.** Established 2026-08-21 that browser tools cannot reach the artifact runtime anyway. Use the browser only for a job posting that will not render any other way.
4. **Never use em dashes.** Anywhere. Not in letters, notes, commits, or chat replies. Use commas, semicolons, or two sentences.
5. **Never claim FEA, CFD, NX, Teamcenter, or ANSYS.** He does not have them and postings ask for them constantly. **Add to that list: he has no AutoCAD and no BIM or Revit experience. SolidWorks is his CAD.** MEP and building-services postings ask for AutoCAD or BIM constantly, IMEG among them. Write around it by leading with SolidWorks depth and the additive and thermal work.
6. **Relocation, current policy as of 2026-08-21.** He will apply to out-of-state roles even when housing or relocation is not supported. Out-of-state is no longer capped at STRETCH. Every such row must state plainly which is true: the listing is **SILENT** on housing and relocation, or the listing **EXPLICITLY refuses** relocation help. Silence is not refusal and must never be written as if it were.
7. **Numbers belong in resumes and cover letters, never on LinkedIn** or anything public. Yield figures and cycle times from a private employer's R&D do not go on an indexed page.
8. **Never consolidate rows.** Standing instruction from Joaquin, 2026-08-21. Every eligible requisition gets its own row and its own slug, forever, even when several sit at the same company. He intends to apply to each one separately. H3X currently holds five rows. Do not tidy them into one, ever, and do not let a future session decide it would be neater.
9. **The wage floor is a preference, not a filter.** `BASE_WAGE=26` is the Kelvin floor. He will still apply to roles under it as a last resort. Under-floor rows render red through the existing `.wg.down` style and are **never filtered and never downranked**. A wage derived from an annual figure carries an `est.` marker and the annual number lives in the note, not the wage field.
10. **He tracks applied status himself** by ticking boxes on the dashboard. Never touch the applied ticks, and refuse to publish if the tick count changed.

## Writing in his voice

Read one of his letters before drafting. His pattern: header block with name and contact, date, `[Company] Hiring Team`, `Dear Hiring Manager`, four paragraphs, `Thank you for considering my application`, `Sincerely`. Roughly 350 to 450 words. Earnest and plain, no swagger.

Then make it strong:

- **Lead with evidence, not intent.** Never open with "I am writing to express my interest."
- **Every body paragraph carries a number** from the resume: yield 20% to 85%, 45 minutes off a 280 minute build, plus or minus 0.1 mm, 6 build iterations, 2 SOPs, 20+ students mentored, 6-part wobbler engine.
- **Past tense for Kelvin Thermal Technologies.** That internship ended August 2026.
- **Cut hedges** ("eager to", "confident that") and any sentence that would be equally true of another company.
- If the application asks for a **message to the hiring team** rather than a cover letter, drop the letterhead, write 250 to 320 words, warmer, and allow one piece of light wit that is factually true.

## How work happens

- **Sweeps** find and score opportunities. Under the current arrangement they cannot publish the tracker and their refusal to publish is correct behavior that must stay. They never build packets.
- **Packets** are built on request: "build a packet for Kairos Power." The skill handles the rest and saves to the Packets folder. No spreadsheet writes, no status columns.
- **The dashboard Build letter button delegates.** It copies a prompt addressed to Opus that tells Opus to spawn a Sonnet subagent, pass it a self-contained brief, and then do the voice pass on what comes back. Drafting and filing run on Sonnet; the voice pass stays on Opus. Do not paste that prompt into a Sonnet chat, since there is nothing above the subagent to check the voice.
- **Dashboard changes** ship as one publish for the whole change set, never per row, through route 0. `docs/history/code-tab-prompt-2026-08-21.md` is the worked example of a route-0 prompt; copy its shape and its gate list.

## Cost discipline, learned the hard way

Driving a browser to edit data cost roughly thirty round trips per sweep. Writing the dashboard costs one publish. Never go back to per-cell editing.

Start a fresh session for packet work rather than continuing a long thread, since every message re-reads the whole history. Sonnet is fine for assembly work. Use Opus when a cover letter or essay is the deliverable, because voice is where it earns its cost.

As of 2026-08-22 those two split inside one session rather than across two: Opus holds the thread and the voice pass, a Sonnet subagent does the skill run, the Drive write, and the screenshot check. The long tool transcript stays in the subagent context, so the Opus thread only ever sees the brief and the finished letter.
