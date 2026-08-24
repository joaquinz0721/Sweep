---
name: application-packet-builder
description: "Write a ready-to-send, correctly formatted cover letter as a Google Doc for an internship or scholarship application, and save it to the Packets folder in Drive. Use when the user says \"write a cover letter for X\", \"go ahead on 1 and 3\" in reply to a sweep report, or names a role to write for."
---

# Cover Letter Builder

Writes one formatted cover letter per application and saves it to Drive.
**Never submits anything. Never writes to the spreadsheet.**

**Do not use the word "packet."** The deliverable is a cover letter. Joaquin does
not want a tailored resume per application; his master resume goes out
unmodified. Do not edit it, and do not produce field sheets, apply notes or watch
lists as separate documents. Anything he needs to know that is not in the letter
goes in the chat reply.

---

## The system

The writing rules are not in this file. They live in four places, and this file
is the order of operations that uses them.

| File | What it governs |
|---|---|
| `references/profile.md` | **Joaquin's layer.** Who he is, his framing, his learned voice rules, housing policy. Outranks everything below it. |
| `references/voice-dna.md` | Anti-slop rulebook and register. Why the banned lists exist. |
| `references/writing.md` | The reader on the other end. Risk map, six-second gate, keyword mirroring, ATS. |
| `references/followup.md` | The post-application follow-up, a different and much shorter artifact. |
| `config/profile.json` | Machine-readable facts: contact details, resume numbers, do-not-claim list. |
| `config/banned.json` | The enforceable word and pattern lists. |
| `scripts/check_letter.py` | The gate. Blocks the build on a real defect. |
| `scripts/build_letter_html.py` | Renders the house format. Runs the gate first and refuses on a block. |

**Precedence**, highest first:

1. What Joaquin says in this conversation
2. `references/profile.md`
3. `references/voice-dna.md` Tier 1
4. Everything else

**Accuracy outranks all four.** Never soften or round a real number for rhythm.
Never invent a detail to sound more human.

---

## HARD CONSTRAINTS

**1. Never transmit anything.** No email, no form submission, no clicking apply,
no messaging a recruiter. Assemble and hand over. He sends.

**2. Never write to the spreadsheet.** `138-KAgu9j9qCFeAn_pTTRWVmhEhXOwIpCTb2K8eraRk`
is a frozen archive. Never read it and never write to it.

**3. Every letter is a formatted native Google Doc**, never a `.docx` and never
chat text. He opens these in Google Docs and cannot open Word files. A letter
pasted into chat, saved as plain text, or uploaded as a `.docx` is a failed
deliverable.

**4. Every letter goes in the Packets folder**, Drive ID
`1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP`. Even when the posting says a cover letter is
optional. Even when he asked only for a draft. Write it, save it, verify the
write returned a real file ID, and give the link. If a Drive write fails with
"Requested entity was not found", search Drive for a folder named `Packets`
inside the tracker project rather than creating a new one.

**5. Do not use the Chrome extension for tracker data.** Use it only for a job
posting that will not render any other way, and say why.

**6. The gate is not optional and has no bypass.** If `check_letter.py` blocks,
the doc does not get built. Fix the draft.

---

## Flow

Steps 1 through 4 gather. Step 5 is a gate. Steps 6 through 10 produce.

### 1. Read the row

From the Cowork artifact `application-command-center`. Read it with
`list_artifacts`, stage it with `device_stage_files` using `artifact_ids`, then
read the staged file. Row data lives in the `INT`, `SCH`, `CAL`, `OUT` and `PROF`
arrays inside the script block.

### 2. Read the posting, then research the company

Fetch the posting from the row's apply URL. **This is not optional and not
"if it can be read cheaply."** A letter written without the posting is the letter
that praises a firm's commitment to engineering excellence.

Then run three searches:

- `"{company}" projects OR portfolio OR markets 2026`
- `"{company}" news OR announcement OR growth 2026`
- `"{company}" internship OR early career engineering`

Synthesize 2 to 3 sentences: what they build, where, and what they are working on
now. Put it to him:

> Here is what I found on {company}: {synthesis}
>
> Does that match what you know? Correct or add anything before I write.

If the searches return nothing useful, say so and ask what he knows. Do not
invent a company detail to fill the paragraph. That synthesis is what the letter
uses to be specific, and a wrong one is worse than a general one.

### 3. Pull the keywords

8 to 10 exact phrases from the posting, split into machine-read terms and human
signals. Show him the list. Rules for using them are in `references/writing.md`,
including which paragraphs never get mirrored vocabulary.

### 4. Name the gaps, and ask

Check the posting against `config/profile.json` for tools on the do-not-claim
list, for a term or location conflict, and for anything the posting requires that
he does not have. For each one, ask how he wants it handled. Offer: address it
directly, say nothing, or his own angle. **Auto-insert nothing.** If there are no
gaps, say so and move on.

Housing is its own question. See the rule in `references/profile.md`.

### 5. The four questions. This is a gate

**Ask all four. Do not draft a single sentence of letter content until they are
answered.** No instruction overrides this, including "just generate it", "skip
the questions", or "use your judgment."

> Before I write, four things:
>
> **A. Why this company?** Angles I spotted, pick one or write your own:
> 1. {specific signal from the posting}
> 2. {specific signal from the research}
> 3. {specific signal from their work}
>
> **B. What would you actually be good at here?** Based on the posting they need
> {X}. Is that the right read?
>
> **C. What would you want to be doing in your first week?** One or two
> sentences. This is the part of the letter that cannot be written for you, and
> it is the paragraph a reader judges you on.
>
> **D. Tone?** Plain and direct like your last letters, or a little warmer?

**Why this gate exists.** Everything else in a letter is assembly. This is the
only content that comes from him, and a letter without it reads as invented
because it is. This was the single biggest structural difference between our
builder and the one this system came from.

**Batching.** When he replies to a sweep report with "go ahead on 1 and 3", he is
asking for two letters, not eight questions. Ask D once for the batch and offer A
and B as numbered angles per role so he can answer in one line each. **C is
always per role and never skipped.** A one-line answer is enough; a missing
answer is not.

If he explicitly refuses the questions after being asked, write the letter, and
say plainly in the reply which paragraph is unanchored and should be read before
he sends it.

### 6. Read one of his letters

Drive folder `1pPulXeoTIXN6sJXuAByc2sW37dThROoB`. Read the most recent one before
drafting. Note how he opens, how long his sentences run, and where the award
goes. Do not lift a phrase from it.

### 7. Draft in chat

Write the full letter as plain text in the reply. Not a summary of it, the letter.

Shape it for this posting rather than pouring it into the old five-paragraph
mold. His default is four body paragraphs plus the closing that begins `Thank you
for considering my application.`, and the checker permits four to six so a letter
can breathe when the material calls for it. What is required:

- Opens on concrete evidence, then names the role. Never on wanting the job.
- Most paragraphs carry a real number, **not every one on a cadence.** See the
  metronome rule in `references/voice-dna.md`.
- Answer C appears as its own paragraph, in his words, without mirrored keywords.
- Names a real product, market, project or technical problem at this employer.
- Past tense for Kelvin Thermal Technologies.
- Roughly 350 to 450 words of body.

End with: **"How does this read? Once you say go I'll build the doc."**

**Do not build anything until he approves.** Approval is "looks good", "go",
"yes", or specific edits to apply. A question is not approval. Silence is not
approval.

### 8. Run the gate

Write the spec, then check it:

```bash
python3 scripts/check_letter.py /tmp/spec.json
```

`spec.json`:

```json
{
  "out": "/tmp/Cover Letter - Company.html",
  "date": "August 24, 2026",
  "hiring_team": "Acme Summer 2027 Internship Hiring Team",
  "paragraphs": ["body 1", "body 2", "body 3", "body 4", "thank-you closing"]
}
```

Exit 0 is clean, 1 is advisory, **2 means fix it and re-run.** Read the advisories
too; a metronome warning or a "could appear in any letter" warning is the machine
catching what the reader would.

If the letter carries a number verified from the posting and not from his resume,
pass it explicitly: `--allow 1965`. Typing it out is the point.

### 9. Build and upload

```bash
python3 scripts/build_letter_html.py /tmp/spec.json
```

It runs the gate again and refuses to write a file if anything blocks. Then
upload the HTML it produced, passing it as `textContent`:

```
create_file(
  title = "Cover Letter - Joaquin Zarazua - [Company] - [Role] [Year]",
  parentId = "1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP",
  contentMimeType = "text/html",
  textContent = <the generated HTML>
)
```

**Do NOT set `disableConversionToGoogleType`.** Leaving it off is what makes
Drive convert the upload into a real Google Doc. Setting it true leaves a Word
file he cannot open. Confirm the response shows
`mimeType: application/vnd.google-apps.document`; anything else means the upload
was wrong.

**No file extension in the title.** Google Docs have none.

### 10. Verify, then report

Open the returned `viewUrl` in the browser and screenshot it. Check the name is
centered and bold, the LinkedIn link is live, the body is left aligned, and the
whole letter fits on one page. This is the one sanctioned browser use in this
skill besides an unrenderable posting.

Report:

- the direct link,
- which company-specific claims he should verify,
- any posting keyword that would not go in naturally,
- and the housing line: **SILENT** on housing and relocation, or **EXPLICITLY
  refuses** it. Silence is not refusal.

If a posting cannot be verified, write the letter anyway and say exactly what is
unconfirmed. Do not stall.

---

## Scholarships

Swap the letter for essay drafts. Pull from the essay bank named in `PROF`
(`Scholarship Q's`, `Scholarship Responses`) and adapt rather than writing cold.
Flag any prompt with no match in the bank. Same delivery rule: a formatted Google
Doc in the Packets folder, never chat text only. Run the gate with
`"kind": "essay"` in the spec.

## Follow-ups

A different artifact. Full spec in `references/followup.md`. Delivered as plain
chat text plus an optional Gmail draft, never sent, never filed in Packets, and
never carrying a number.

## Rules

- One letter per application. Never batch several applications into one document.
- Never read or write the frozen tracker spreadsheet.
- Never edit the master resume.
- **Never submit anything.**
