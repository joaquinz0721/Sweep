---
name: application-packet-builder
description: "Write a ready-to-send, correctly formatted cover letter as a Google Doc for an internship or scholarship application, and save it to the Packets folder in Drive. Use when the user says \"write a cover letter for X\", \"go ahead on 1 and 3\" in reply to a sweep report, or names a role to write for."
---

# Cover Letter Builder

Writes one formatted cover letter per application and saves it to Drive. **Never submits anything. Never writes to the spreadsheet.**

**Do not use the word "packet."** The deliverable is a cover letter. Joaquin does not want a tailored resume per application; his master resume goes out unmodified. Do not edit it, do not produce field sheets, apply notes, or watch lists as separate documents. Anything the user needs to know that is not in the letter goes in the chat reply.

**Trigger:** the user asks in chat. Either "write a cover letter for [company]" or "go ahead on 1 and 3" in reply to a sweep report, where the numbers map to that report's numbered items.

**Data source (read only):** the Cowork artifact `application-command-center`. Read it with `list_artifacts`, stage it with `device_stage_files` using `artifact_ids`, then read the staged file. Row data lives in the `INT`, `SCH`, `CAL`, `OUT`, and `PROF` arrays inside the script block.

**The Google Sheet `138-KAgu9j9qCFeAn_pTTRWVmhEhXOwIpCTb2K8eraRk` is a FROZEN ARCHIVE.** Never read it and never write to it.

**Packets folder:** Drive folder ID `1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP` (named `Packets`, inside `Internship and Scholarship Tracker Project`). If a Drive write fails with "Requested entity was not found", search Drive for a folder named `Packets` inside the tracker project rather than creating a new one.

---

## HARD CONSTRAINTS

**1. Never transmit anything.** No email, no form submission, no clicking apply, no messaging a recruiter. Assemble and hand over. The user sends.

**2. Never write to the spreadsheet.** The sheet is frozen and out of scope.

**3. Every letter is delivered as a formatted native Google Doc, never as a `.docx` and never as chat text.** He opens these in Google Docs and cannot open Word files. A letter pasted into chat, saved as plain text, or uploaded as a .docx is a failed deliverable.

**4. Every letter goes in the Packets folder.** Even when the posting says a cover letter is optional. Even when the user asked only for a draft. Write it, save it, verify the write returned a real file ID, and give the link.

**5. Do not use the Chrome extension for tracker data.** Use it only for a job posting that will not render any other way, and say why.

---

## FORMATTING, non-negotiable

**The deliverable is a native Google Doc.** Do not upload a `.docx`. Do not create the doc from plain text, which strips all formatting. The working method is to generate styled HTML and let Drive convert it, which preserves the house format exactly.

Build the HTML with the bundled generator:

```
python3 scripts/build_letter_html.py spec.json
```

`spec.json`:

```json
{
  "out": "/tmp/Cover Letter - Company.html",
  "date": "August 18, 2026",
  "hiring_team": "Acme Summer 2027 Internship Hiring Team",
  "paragraphs": ["body 1", "body 2", "body 3", "body 4", "thank-you closing"]
}
```

Exactly 5 paragraphs: four body paragraphs plus the closing that begins `Thank you for considering my application.` The generator emits the house format:

- Name centered and bold, Times New Roman 11pt
- `Centennial, CO  |  720-435-0880  |  joaquinz0721@gmail.com  |  linkedin.com/in/joaquinzarazua` centered, LinkedIn as a live hyperlink
- Date, hiring team line, and `Dear Hiring Manager,` left aligned
- 11pt throughout, 10pt space after each paragraph, one blank line after the salutation and before `Sincerely,`
- `Sincerely,` and `Joaquin Zarazua` at the foot

**Upload it like this**, passing the HTML as `textContent`:

```
create_file(
  title = "Cover Letter - Joaquin Zarazua - [Company] - [Role] [Year]",   # no file extension
  parentId = "1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP",
  contentMimeType = "text/html",
  textContent = <the generated HTML>
)
```

**Do NOT set `disableConversionToGoogleType`.** Leaving it off is what makes Drive convert the upload into a real Google Doc. Setting it true leaves a Word file he cannot open. Confirm the response shows `mimeType: application/vnd.google-apps.document`; if it shows anything else, the upload was wrong.

**Do not put a file extension in the title.** Google Docs have no extension.

**Verify before reporting.** Open the returned `viewUrl` in the browser and screenshot it. Check the name is centered and bold, the LinkedIn link is live, the body is left aligned, and the whole letter fits on one page. This is the one sanctioned browser use in this skill besides an unrenderable job posting.

**Report the link** to the Google Doc. Do not send a file to chat; he works from Drive.

## WRITING RULES

### Rule 1: Never use em dashes

Not in letters, notes, summaries, or chat replies about this work. Use a comma, a semicolon, a colon, parentheses, or two sentences. This is absolute. His own writing contains none, and a stray em dash is the clearest tell that text was not written by him.

### Rule 2: Public versus private material

- **Cover letters and essays keep the hard numbers.** They go to a named reader in a hiring context.
- **Anything public facing, such as LinkedIn, keeps no numbers and no process specifics.** Yield figures, cycle times, tolerances, and named test methods from a private employer's R&D do not belong on an indexed page.
- **Never put a wage figure in a letter.** The dashboard tracks pay; the letter does not mention it.

### Rule 3: Keep his structure

Four body paragraphs: opening, core experience, a distinguishing project or independent interest, then a short paragraph where leadership and logistics round out the picture. Then the closing. Roughly 350 to 450 words of body text. Register: earnest, plain, professional. He is a college senior, not an executive. No swagger, no consultant vocabulary, no words he would not say out loud.

Past letters live in the Drive folder `Cover Letters` (folder ID `1pPulXeoTIXN6sJXuAByc2sW37dThROoB`). Read one before drafting if the voice needs refreshing.

**If the application asks for a "message to the hiring team" rather than a cover letter**, write 250 to 320 words, warmer and more personal, and allow one piece of light wit that is factually true rather than a joke. Still deliver it as a formatted document.

### Rule 4: Make every sentence carry weight

**Lead with evidence, not intent.** Never open with `I am writing to express my interest in...`. Open with one concrete sentence of his best relevant work, then name the role.

**Every body paragraph carries at least one number** from the resume. Pick the ones the posting cares about:

- yield raised from 20% to 85% across 6 build iterations (Kelvin)
- 45 minutes cut from a 280 minute build, about 16% (Kelvin, custom assembly fixturing)
- ±0.1 mm tolerances held across builds (Kelvin)
- 2 SOPs authored (Kelvin)
- 50+ precision measurements, modeled to under 0.5 mm (**ratcheting screwdriver project, NOT Kelvin**, do not misattribute this)
- 6-part compressed-air wobbler engine, mill and lathe
- 20+ first-year students mentored (Peer Leader)

**Use past tense for Kelvin Thermal Technologies.** That internship ended August 2026.

**Cut every hedge:** `I am eager to`, `I am confident that`, `I hope to`, `I believe I would`.

**Cut filler.** If a sentence would be equally true in a letter to any other company, cut it or make it specific.

**Be specific about the employer.** Name a real product, program, site, or technical problem. Tell the user which company-specific claims to verify if the posting was not read in full.

**Surface the relevant award.** He holds the Clinton J. Helton Manufacturing Scholarship from the SME Education Foundation, a CU Esteemed Scholars Hale award, Opportunity Next Colorado, and Hispanic National Merit recognition. Name one only when it maps to the role: the SME award belongs in any manufacturing, production, or process-engineering letter, because it is a manufacturing-specific award from the manufacturing engineering society. Do not list awards that do not connect.

**Never inflate.** Do not claim a skill, tool, or outcome not already on the resume, and never claim anything under `Known gaps, DO NOT CLAIM` (FEA, CFD, NX, Teamcenter, ANSYS). He has SolidWorks, not Creo and not AutoCAD. He does machining, sheet metal, laser cutting, and 3D printing, not welding. Strength comes from specificity, not bigger adjectives.

---

## Flow

1. Read the row and the `PROF` array from the dashboard artifact. Fetch the posting from the row's apply URL if it can be read cheaply.
2. Draft the five paragraphs. Check the word count and scan for em dashes and for anything in the do-not-claim list.
3. Run `scripts/build_letter_html.py` to produce the HTML.
4. Upload it to the Packets folder as `text/html` with conversion left ON, so Drive makes a Google Doc.
5. Open the resulting doc in the browser and screenshot it to confirm the format held.
6. Report: the direct link, which company-specific claims to verify, and anything still unconfirmed, especially housing.

**Housing and relocation are a hard rule:** outside Colorado requires housing or relocation stated on the posting. Never write a line committing him to relocate further than that rule allows. If housing is unstated, keep the availability line neutral and flag it in chat.

If a posting cannot be verified, write the letter anyway and say exactly what is unconfirmed. Do not stall.

## Scholarships

Swap the letter for **essay drafts**. Pull from the essay bank named in `PROF` (`Scholarship Q's`, `Scholarship Responses`) rather than writing cold. Adapt, do not regenerate. Flag any prompt with no match in the bank. Essays follow the same delivery rule: saved to the Packets folder as formatted Google Docs, never left in chat only.

## Rules

- One letter per application. Never batch several applications into one document.
- Never read or write the frozen tracker spreadsheet.
- Never edit the master resume.
- **Never submit anything.**

---

## POST-APPLICATION FOLLOW-UP

A short message to a recruiter or an engineer at a company Joaquin has **already applied to**. Roughly 80 words. Sent by email, LinkedIn, or Handshake.

**This is not the "message to the hiring team" variant in Rule 3.** That one is 250 to 320 words and replaces a cover letter. This one is a four sentence note sent after the application is in. Do not conflate them.

### Absolutes

1. **Never send it.** Draft only. Joaquin sends.
2. **Never write "y'all", "yall", or "ya'll".** Removed from the template permanently. It is not professional and it read as a mail merge tic when it appeared in the same slot in every message.
3. **No em dashes.**
4. **No numbers of any kind.** No yield figures, no cycle times, no tolerances, no dates, no wage. A follow-up may land on LinkedIn or Handshake, and hard rule 7 keeps resume numbers off public surfaces. The three experience items carry the weight instead.
5. **Never claim** FEA, CFD, NX, Teamcenter, ANSYS, AutoCAD, Revit, BIM, Creo, or welding. SolidWorks is his CAD.
6. **Kelvin Thermal Technologies is past tense.** That internship ended August 2026.
7. **Name the company.** A follow-up that never names the employer is a form letter.

### The template

```
Hi [First name],

I just applied to the [exact role title as posted] role at [Company] and wanted to reach
out to express my sincerest enthusiasm. I'm very interested in the work [Company] is doing
in [FIELD][, particularly DETAIL]. I believe this role is an incredible fit for my
experience in [A], [B], and [C]. Thank you in advance for your consideration.

Joaquin Zarazua
```

Email subject line, when the channel is email: `Application for [exact role title as posted]`

### Slot rules, this is where the old version broke

**[FIELD]**

- One noun phrase, six words maximum.
- No internal "and". No internal comma.
- It names what the company builds, it is not a sentence about it. `advanced nuclear` is right. `getting a new reactor design built as real hardware` is wrong; that is a gerund clause and it does not fit this slot.

**[, particularly DETAIL]**, optional, at most one

- For a site, program, product, or technical problem worth naming.
- Attaches with one comma and the word "particularly". Nothing else.
- A single phrase. No internal "and", no second comma, no clause.
- **If it will not fit that shape, drop it.** A shorter message that says less beats a run-on.

**[A], [B], [C]**

- Exactly three. Serial comma before the final "and".
- All three the same grammatical shape: noun phrases, two to five words each.
- **No item may contain the word "and".** "SolidWorks and GD&T" is two items disguised as one; pick one.
- Prefer noun forms over gerunds: `process yield improvement`, not `raising process yield`.
- Drawn from the resume, ordered to match what the posting asks for first.

**[Company]**

- Spelled the way the employer spells it. `Kairos Power`, not `Kairos`.
- Appears twice, once in sentence 1 and once in sentence 2. If the name runs longer than three words, the second mention may read `the work the team is doing in ...`.

**[First name]**

- If no contact name is known, drop the greeting line entirely and open on sentence 1.
- Never write "Dear Hiring Manager" here. This is a message, not a letter.

### Sentence rules

- **Sentences 2 and 3 are separate sentences.** They are never joined by "and". This single change is what fixes the old template, which collapsed the moment the field slot grew.
- No sentence carries more than one "and", except sentence 3, where the only "and" is the serial one closing the three item list.
- Body is 60 to 90 words. Hard cap 110.
- **Keep "I believe this role is an incredible fit."** It looks like a hedge and it is not. It is Joaquin's line and it stays.
- Cut every other hedge: "eager to", "confident that", "hope to", "I would love to", "I feel that".

### Checklist, run it before handing anything over

- [ ] No "y'all", "yall", or "ya'll" anywhere
- [ ] No em dash
- [ ] Exactly four sentences in the body
- [ ] Sentences 2 and 3 are separate, not joined by "and"
- [ ] Company named twice, spelled the way the employer spells it
- [ ] Exact role title as posted
- [ ] FIELD is one noun phrase, six words or fewer, no "and", no comma
- [ ] DETAIL is absent, or is one phrase attached with ", particularly"
- [ ] Three experience items, same grammatical shape, none containing "and"
- [ ] No numbers, no wage
- [ ] Nothing from the do-not-claim list
- [ ] Kelvin in past tense if mentioned
- [ ] Body is 60 to 90 words, hard cap 110
- [ ] Name on its own line, no trailing period
- [ ] Nothing sent

### Delivery

- **Plain text in the chat reply**, so Joaquin can paste it straight into LinkedIn or Handshake. This is the one deliverable in this skill that is allowed to be chat text; the Google Doc rule in HARD CONSTRAINTS 3 applies to letters and essays, not to follow-ups.
- **A Gmail draft as well**, only when a real email address is known and he has asked for one. Draft only. Never send.
- **Follow-ups are not filed in the Packets folder.** That folder is for cover letters and essays.

### Worked example

Kairos Power, Mechanical and Manufacturing Engineering Intern:

```
Hi [First name],

I just applied to the Mechanical and Manufacturing Engineering Intern role at Kairos Power
and wanted to reach out to express my sincerest enthusiasm. I'm very interested in the work
Kairos Power is doing in advanced nuclear, particularly turning a new reactor design into
real hardware. I believe this role is an incredible fit for my experience in prototype build
iteration, SolidWorks modeling, and process yield improvement. Thank you in advance for your
consideration.

Joaquin Zarazua
```

The before-and-after pair for this and for Western Digital, with the reasoning, is in `docs/followup.md`.
