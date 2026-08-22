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


### Rule 5: The four moves that make it read as machine-written

Joaquin flagged this on 2026-08-22 after reading a draft: the letters were factually right and still sounded generated. The cause was not word choice, it was four rhetorical moves. **They are banned outright.** Each one below is quoted from real drafts, including a letter already sitting in his Drive folder, so treat this as a list of things that have already gone out, not a hypothetical.

**Move 1. The self-aphorism.** A sentence that characterizes him instead of reporting what he did, usually shaped as `where X and Y meet` or `X is where I am most useful`.

> I do my best work where the drawing and the shop floor meet.
> Hands-on fabrication is where I am most useful. *(shipped in the Anduril letter)*

Fix: delete it. The sentence after it was already doing the work. `At Kelvin I modeled the fixturing in SolidWorks, then machined it myself.`

**Move 2. The antithesis.** Two clauses set against each other for rhythm: `X would be new to me. Y would not be.`, `it is not X, it is Y`, `not because X, but because Y`.

> Composite layup would be new to me. Process variability and proving out a change with data would not be.

Fix: say the honest half once, plainly, and stop. `I have not done carbon fiber layup.` Admitting a gap is good. Building a couplet out of it is not.

**Move 3. The summarizing tag.** A clause or sentence whose subject is the previous sentence. It restates what was just said, labels it, and usually echoes the posting's own vocabulary back at the reader.

> That is shop floor process work with data behind it, which is what the manufacturing posting describes.
> ...which is the procurement piece the posting lists under executing your own solutions. *(Anduril letter)*
> ...which is the daily contact this internship describes. *(Anduril letter)*
> ...which is most of what a good work instruction has to do. *(Anduril letter)*

Three in one letter is a fingerprint. Fix: cut the tag and keep the fact. The reader wrote the posting and does not need it read back to them.

**Move 4. The closing flourish.** A last line that reaches for meaning instead of ending.

> ...and to leave behind documentation that outlasts the internship.

Fix: end with the ask, or with thanks. Nothing after that.

### The test to run on every draft

Read each sentence alone and ask: **does it state a fact, ask a question, or make a request?** If it does none of those, or if its subject is another sentence, cut it. Facts do not need a bow on them.

Two supporting habits:

- **Vary the rhythm.** Three item lists in every paragraph, and paired short sentences for emphasis, are both tells. Let some sentences run long and some stop early.
- **Never explain their own job or posting to them.** State what he did and let the match be obvious.

Then run the checker before the doc is built:

```
python3 scripts/voice_check.py /tmp/draft.txt
```

It greps for the banned constructions plus em dashes and the standing hedge list. **A clean run is not proof the writing is good, only that these four moves are absent.** Read it out loud after, and cut anything he would not say to a person.

---

## Flow

1. Read the row and the `PROF` array from the dashboard artifact. Fetch the posting from the row's apply URL if it can be read cheaply.
2. Draft the five paragraphs. Then run the Rule 5 pass: `python3 scripts/voice_check.py` on the draft, read every sentence against the one-sentence test, and rewrite anything that fails. Check the word count, the do-not-claim list, and that the 50 plus measurements stayed on the screwdriver project. **Do not build the doc until this pass is done**, since reformatting a bad draft only makes it a well formatted bad draft.
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
