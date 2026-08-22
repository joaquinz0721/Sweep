# Code-tab session prompt, dashboard update 2026-08-21 (rev 2)

> **STATUS: SHIPPED AND SPENT.** This change set was published on 2026-08-21 as version `1787353283-20cc`. Do not send it again; it would re-apply edits that are already live. It is kept in the repo for one reason: **it is the canonical worked example of a route-0 local Code-tab prompt.** Copy its shape, its gate list, and its procedure section when writing the next one. Replace the Edits section entirely.

Rev 2 folds in the IMEG, AMD, and Oxy postings Joaquin read manually. **Rev 1 is superseded, do not send it.**

Paste everything below the line into a **Local** session in the **Code** tab of the desktop app. Not a cloud session unless that session is pinned to the `empluzz` environment; a plain cloud session sits behind the egress proxy and the WebFetch in step 1 will fail.

---

You are running as a local Code-tab session on my machine. Read `docs/MEMORY.md`, section 3 especially, then do the work below.

**Artifact:** https://claude.ai/code/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594

**Hard rules for this session.** No em dashes anywhere, in code, notes, or chat. Never read or write the Google Sheet. Never submit or transmit anything. Do not touch the applied ticks; I manage those myself. One publish for the whole change set, never per row.

**Standing rule, apply it and do not undo it later.** Every eligible requisition gets its own row with its own slug, forever, even when several are at the same company. Do not consolidate H3X into one row. Do not consolidate anything.

## Procedure, follow it exactly

1. `WebFetch` the artifact URL. This is what sets the tracked baseVersion and unlocks the Artifact tool. Do not skip it even if you think you have the source.
2. **Reconstruct the authored document from the marker pairs.** What the fetch returns is the shell's transformed copy, not the authored source. Cut on `<!--ACC-HEAD-->` / `<!--/ACC-HEAD-->` and `<!--ACC-BODY-->` / `<!--/ACC-BODY-->` and re-wrap, the same way `buildDoc()` does. Do not edit the served document in place. This step is also what stops the wrapper nesting from compounding.
3. Make the edits below against that reconstruction.
4. Publish passing the artifact **url**. No `force`. Do not pass a `capabilities` object at all, so the stored declaration carries forward. Pass the favicon `🎯`.
5. Read back and verify.

## Gates, all of them, before you publish

- Parse the `ACC-STATE` block before and after. **Refuse to publish if the applied-tick count changed.** It should be 14 unless I have ticked something today.
- **Gate on the delta your edits produce, never on absolute document length.** A baked-in length number goes stale the moment a tick saves. Check state and structure independently.
- Assert every marker appears exactly once.
- Assert all row slugs are unique, `[a-z0-9-]` only, and that no existing slug changed.
- Assert no injected frame runtime leaked into the payload.
- Log the reconstructed length and the applied-tick count on one line so a failure is diagnosable.

**Find rows by company plus role text, not by a slug I have given you.** Assign a new slug only to the one new row.

## Edits

Row shape is `INT`: `[conviction, company, role, location, term, deadline, source, url, packetStatus, notes, status, hint, wage, SLUG]`. Slug is index 13. A note containing `[UNVERIFIED]` or `STILL CONFIRM` is what fires the VERIFY chip, so clearing a chip means removing those tokens from that note.

Every field below came from the employer's own posting. Details and quotes are in `docs/verification-2026-08-21.md`.

### IMEG, this one has moved to the front of the queue

**Deadline 2026-09-19, twenty-nine days out.** That is now the nearest deadline anywhere on the board, ahead of the ACEC scholarship on October 1. Set it and make sure the Days Left column picks it up.

- Conviction **STRONG**, status **OPEN**, clear VERIFY
- Role: `Mechanical Engineering Intern | Greenwood Village, CO`, req `R-16570`
- Location: `Greenwood Village, CO` (Workday files it under Denver Metro, CO)
- Term: `Summer 2027 confirmed, 10-12 weeks, full time in office`
- Deadline: `2026-09-19`. The posting says it may be extended if unfilled, so record the date as firm and the extension as a note, not the other way round.
- Wage: `22-24`, under my preference, render red
- Major: `Completed at least 2 years toward a BS in Mechanical Engineering`
- Housing: `SILENT`. Local, so it does not matter.
- Note must also carry: `Sponsorship not available. Requires AutoCAD and/or BIM. Work is HVAC and building mechanical systems, geothermal, chilled beams, central plants, energy recovery.`

### AMD, downgrade

The posting lists `Computer Science, Computer Engineering, Electrical Engineering or a related field`. **Mechanical Engineering is not named**, and every technical skill listed is software, digital logic, or circuit theory. This is the same situation as the H3X Power Electronics req.

- Conviction to **STRETCH**, status OPEN, clear VERIFY
- Req `90790`, locations include `Longmont, CO` and `Fort Collins, CO`
- Term: `Summer 2027, May 24 to Aug 13 2027 for semester students. Spring/Summer and Summer/Fall co-op options also listed.`
- Deadline: none stated
- Wage: posted annually as `$59,072 to $88,608`. Convert and mark it estimated the same way the Indeed rows are: `28-43 est.` at 40 hours a week. Do not store the annual figure in the wage field.
- Housing: `SILENT`
- Note: `ME not a listed major, skills list is CS and EE. Applying registers general interest across all AMD intern reqs, not this one alone. No visa sponsorship.`

### Oxy, upgrade

- Conviction **STRETCH to STRONG**, status OPEN, clear VERIFY
- Req `JR110204`
- **Housing is stated and positive:** `Relocation Assistance and/or fully-furnished Corporate Housing provided, if applicable`
- Term: `Summer 2027, May to August, 12 weeks`
- Major: `Pursuing a degree in Engineering`, GPA 2.85 minimum
- **Graduation window December 2027 to May 2029. I graduate May 2028, so I qualify.** Put that in the note; it is the kind of thing that is easy to lose.
- Deadline: none stated
- Wage: not stated on the posting, so `STILL CONFIRM wage` stays in the note and **the chip stays up** for that reason alone
- Location note: `Workday lists 6 locations, Midland TX, Carlsbad NM, Denver City TX, Houston TX, The Woodlands TX and one more. Platteville CO is not among them, though the posting prose mentions Colorado. Confirm the Colorado placement before writing anything.`
- Note must also carry: `Must apply at oxy.com/students to be considered. A LinkedIn apply alone may not count.`

### H3X Technologies, five separate rows, keep them separate

Shared across all five: wage `23-37`, `Relocation package stated`, citizenship SILENT, no deadline, Louisville CO, in office.

The reason these sat at WATCH was Spring colliding with coursework. The postings say "full time Spring Intern, but also have availability for Summer 2027 and extended Co-Op positions", so that objection is dead. Term note for all: `Spring req, Summer 2027 availability stated on posting`.

| Row | Change |
|---|---|
| Mechanical Design Engineer Intern (Spring) | WATCH to **STRONG**, status OPEN, clear VERIFY. Major: BS or grad ME or similar, GPA 3.0+. |
| Advanced Manufacturing Engineering Intern (Spring) | WATCH to **STRONG**, status OPEN, clear VERIFY. Major: BS or grad ME or similar, GPA 3.0+. |
| Test Engineering Intern (Spring) | WATCH to **STRONG**, status OPEN, clear VERIFY. Major: ME or similar, GPA 3.0+. |
| Power Electronics Engineering Intern (Spring) | status **CLOSED**. Note: `EE and Computer Engineering only, ME not listed, confirmed on posting 2026-08-21`. |

**Add one new row**, slug `int-h3x-electromagnetics-intern`:
Conviction STRONG, company `H3X Technologies`, role `Electromagnetics Engineering Intern (Spring)`, location `Louisville, CO`, term `Spring req, Summer 2027 availability stated on posting`, no deadline, source `Built In Colorado`, url `https://www.builtincolorado.com/job/electromagnetics-engineering-intern-spring/10750089`, wage `23-37`, status OPEN, note: `Posting names Mechanical Engineering explicitly. Relocation package stated. Citizenship SILENT.` No VERIFY token; this one was read.

### The rest

| Row | Change |
|---|---|
| **Kiewit**, Equipment Engineer Intern | Deadline **2027-01-01**, wage `18-25` (red), term `start May/June 2027`, housing `SILENT`, clear VERIFY, conviction stays STRONG. Note: wage under my preference, and both Lone Tree and Denver are on the req. |
| **Boom Supersonic** | Location Englewood to **Centennial, CO**, wage `35`, housing `Housing allowance $2,000 stated`, clear VERIFY. Note must record: **US person required under ITAR and EAR.** |
| **Freeform** | Wage `30`, term `Summer 2027 confirmed`, housing `Relocation assistance provided`, clear VERIFY, STRONG stands. Note must record: **ITAR US person required.** Major ME or aerospace, ABET. |
| **Zipline** | Term `Summer 2027, May/June to Aug/Sept`, requirement `second year of undergrad completed`, housing `SILENT`. Wage was not readable, so **keep the chip** with `STILL CONFIRM wage`. |
| **Skydio** | Wage `41`, citizenship `E-Verify only, no ITAR clause`, housing `SILENT`. Term was not stated, so **keep the chip** with `STILL CONFIRM term`. |
| **Explico** | Keep on the board as a last resort. Note: `Accident reconstruction and biomechanics consultancy, no mechanical design track, $18-25/hr under preference`. Wage `18-25` (red), conviction WATCH, clear VERIFY since the program page was read. |
| **MatX** | Note: `Not listed on MatX own job board as of 2026-08-21, only 8 full-time engineering roles there`. Keep the chip. |

### Two behavior changes

1. **Wages below `BASE_WAGE` (26) render red** in the wage cell so I can see at a glance which roles are under my preference. Do not filter them and do not downrank them; the scoring stays exactly as it is. I still intend to apply to these as a last resort. If a red or warning style already exists in the stylesheet, reuse it rather than adding a new colour. Keep it working in the stacked-card mobile layout under 700px.
2. Any wage stored as an estimate from an annual figure carries the `est.` marker, matching the existing Indeed rows. AMD is the first of these.

## After publishing

- Read the artifact back and confirm the applied-tick count is unchanged.
- Count `<html` and `<body` as markup and confirm there is exactly one of each. If the wrapper left the document nested one level deeper, say so; it self-repairs on my next tick and is not an error.
- Report the before and after VERIFY chip count, and confirm IMEG now shows as the nearest deadline on the board.
- Tell me the new version slug.
