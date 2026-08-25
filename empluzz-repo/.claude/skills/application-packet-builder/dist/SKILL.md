---
name: application-packet-builder
description: "Write a ready-to-send, correctly formatted cover letter as a Google Doc for an internship or scholarship application, and save it to the Packets folder in Drive. Use when the user says \"write a cover letter for X\", \"go ahead on 1 and 3\" in reply to a sweep report, or names a role to write for."
---

<!-- GENERATED FILE. Do not edit.
     Source: .claude/skills/application-packet-builder/ in the empluzz repo.
     Rebuild: python3 scripts/build_account_skill.py
     Edit the source files and regenerate; edits here are lost. -->

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
| the **profile** section | **Joaquin's layer.** Who he is, his framing, his learned voice rules, housing policy. Outranks everything below it. |
| the **voice-dna** section | Anti-slop rulebook and register. Why the banned lists exist. |
| the **writing** section | The reader on the other end. Risk map, six-second gate, keyword mirroring, ATS. |
| the **followup** section | The post-application follow-up, a different and much shorter artifact. |
| the embedded `profile.json` | Machine-readable facts: contact details, resume numbers, do-not-claim list. |
| the embedded `banned.json` | The enforceable word and pattern lists. |
| the gate | The gate. Blocks the build on a real defect. |
| the builder | Renders the house format. Runs the gate first and refuses on a block. |

**Precedence**, highest first:

1. What Joaquin says in this conversation
2. the **profile** section
3. the **voice-dna** section Tier 1
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
signals. Show him the list. Rules for using them are in the **writing** section,
including which paragraphs never get mirrored vocabulary.

### 4. Name the gaps, and ask

Check the posting against the embedded `profile.json` for tools on the do-not-claim
list, for a term or location conflict, and for anything the posting requires that
he does not have. For each one, ask how he wants it handled. Offer: address it
directly, say nothing, or his own angle. **Auto-insert nothing.** If there are no
gaps, say so and move on.

Housing is its own question. See the rule in the **profile** section.

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
  metronome rule in the **voice-dna** section.
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

A different artifact. Full spec in the **followup** section. Delivered as plain
chat text plus an optional Gmail draft, never sent, never filed in Packets, and
never carrying a number.

## Rules

- One letter per application. Never batch several applications into one document.
- Never read or write the frozen tracker spreadsheet.
- Never edit the master resume.
- **Never submit anything.**

---

# profile

> Joaquin's layer. Outranks every generic rule in this document.

**This file is his. Nothing auto-updates it, and it outranks every generic rule
in the skill.** Where this file and the **voice-dna** section disagree, this file
wins. Where this file and something Joaquin says in the conversation disagree, he
wins and this file gets updated afterward.

Facts a script needs live in the embedded `profile.json`. Judgment lives here.

---

### Who is writing

CU Boulder, Mechanical Engineering, graduating May 2028. Targeting Summer 2027
internships. A college senior writing to engineers, not an executive writing to a
board. Every register decision follows from that.

### Target roles

| Archetype | What the posting is buying | What he leads with |
|---|---|---|
| **Manufacturing / process engineering** | Someone who can move a real number on a real line | Yield 20% to 85% over 6 build iterations, the 2 SOPs, the fixturing |
| **Mechanical design / prototyping** | Someone who models a part that can actually be made | SolidWorks depth plus the fact that he machines what he draws |
| **Thermal** | Someone who has been near thermal hardware | Kelvin vapor chamber work, plus or minus 0.1 mm across builds |
| **Test / metrology / quality** | Someone who measures carefully and writes it down | 50+ precision measurements on the screwdriver teardown, modeled under 0.5 mm |
| **MEP / building systems** | Usually AutoCAD and Revit, which he does not have | SolidWorks depth, the additive and thermal work, and the process discipline. See the gap play below. |

### Adaptive framing

Same three experiences, different order depending on what the posting buys
first. Never a different set of facts.

- **Kelvin Thermal Technologies**, summer 2026, past tense always. The yield
  number, the fixturing time saved, the tolerance, the SOPs.
- **Ratcheting screwdriver reverse-engineering project**, **school coursework,
  not his own time.** He calls it "my reverse-engineering project". The
  measurement discipline and the modeling. **The 50+ measurements belong to this
  project, never to Kelvin.** Misattributing it is the single most common error
  in our letters and the checker blocks on it.
- **Compressed-air wobbler engine**, 6 parts, mill and lathe. **Also school
  coursework.** Proof he can make a thing, not only draw one.
- **Never call either project personal, independent, self-directed, done on his
  own time, or done with no deadline or grade attached.** Corrected 2026-08-25
  after he struck those words out of the Freeform packet himself. They were
  assigned work and he does not want them sold as hobby projects.
- **Peer Leader**, 20+ first-year students. Explaining a decision to somebody who
  has not seen the constraint yet, which is most of engineering communication.

### The narrative underneath every letter

He spent a summer closing the gap between a drawing and a part that goes
together, and he wants another one. That is the through line. The coursework
projects are evidence that the loop is a habit rather than one lucky summer: he
measured, modeled and machined before the internship and kept doing it after.

### The gap play

Postings ask constantly for tools he does not have. The full list is
`do_not_claim` in the embedded `profile.json` and the checker blocks on every one of
them: **FEA, CFD, NX, Teamcenter, ANSYS, AutoCAD, Revit, BIM, Creo, welding.**

SolidWorks is his CAD. He machines, does sheet metal, laser cutting and 3D
printing.

When a posting asks for a tool he lacks:

- **Never claim it, never imply it, never hedge toward it.** No "familiar with",
  no "exposure to", no listing it beside tools he does have.
- **Say nothing, or say it plainly.** Silence on a tool is normal in a letter and
  costs nothing. If the tool is central enough that silence looks evasive, one
  clean sentence naming what he has instead is stronger than a dodge.
- **Lead around it.** MEP and building-services postings (IMEG among them) want
  AutoCAD or Revit. Open on SolidWorks depth and the additive and thermal work,
  and let the process discipline carry the rest.
- Ask Joaquin before writing any sentence that acknowledges a gap. It is his call
  whether to raise it at all.

### Certifications

**CSWA, Certified SolidWorks Associate.** In the embedded `profile.json` under
`credentials.verified`, so the checker treats it as a real claim. Anything else
asserted as a certification draws a warning, because a certification is easy to
write and hard to walk back. Add it to that list before a letter claims it.

### Awards

Name one only when it maps to the role. Listing awards that do not connect reads
as padding.

- **Clinton J. Helton Manufacturing Scholarship**, SME Education Foundation.
  Belongs in any manufacturing, production or process engineering letter; it is a
  manufacturing-specific award from the manufacturing engineering society, which
  is exactly the point.
- **CU Esteemed Scholars Hale award.** Academic merit, use sparingly.
- **Opportunity Next Colorado** and **Hispanic National Merit recognition.** Only
  on a direct match.

### Location and housing

Standing policy as of 2026-08-21. He applies to out-of-state roles even when
housing and relocation are not supported, and out-of-state is no longer capped
at STRETCH.

**In the letter:** keep the availability line neutral unless the posting states
housing or relocation support. Never write a sentence committing him to relocate
on terms the posting has not offered.

**In the chat reply:** say plainly which of the two is true, because they are
different and the tracker treats them differently. Either the listing is
**SILENT** on housing and relocation, or it **EXPLICITLY refuses** relocation
help. **Silence is not refusal and must never be written as if it were.**

### Learned voice rules

Each of these came from a specific output that was wrong.

- **No em dashes, anywhere.** His own writing contains none, so a stray one is
  the clearest single tell that text was not written by him. Letters, notes,
  chat, commits, code comments.
- **Never "y'all", "yall", or "ya'll".** Removed permanently. It read as a mail
  merge tic when it turned up in the same slot in every follow-up.
- **Keep "I believe this role is an incredible fit."** It looks like a hedge and
  it is not. It is his line and it stays, in follow-ups.
- **Numbers stay off public surfaces.** Letters and essays keep the hard figures,
  because they go to a named reader in a hiring context. LinkedIn, Handshake and
  anything indexed get none: no yield figures, no cycle times, no tolerances, no
  named test methods. Those come out of a private employer's R&D.
- **Never a wage figure in a letter.** The dashboard tracks pay. The letter does
  not mention it.
- **Kelvin is past tense.** That internship ended August 2026. A present-tense
  Kelvin sentence is a factual error, not a style slip, and the checker blocks it.

### Voice calibration

His past letters live in Drive folder `1pPulXeoTIXN6sJXuAByc2sW37dThROoB`
(`Cover Letters`).

**Read one before drafting.** Not optional, and not "if the voice needs
refreshing" the way the old skill put it, which meant it never happened. Read the
most recent one and note how he actually opens, how long his sentences run, and
where he puts the award.

Store what you learn as description, never as sentences. Do not lift a phrase
from a past letter into a new one; the reader may have seen it, and reused
sentences across employers are their own tell.

His observed pattern, from the letters already in that folder:

- Header block, date, `[Company] Hiring Team`, `Dear Hiring Manager,`
- Four body paragraphs, then `Thank you for considering my application.`
- `Sincerely,` and his name
- Roughly 350 to 450 words of body
- Earnest and plain throughout

Treat the four-paragraph shape as **his default, not a requirement.** Four is
what he has written; the checker permits 4 to 6 so that a letter can breathe when
the material calls for it. What is required is that the shape is chosen for this
posting rather than poured into a mold. See the metronome rule in
the **voice-dna** section.

### Scholarships

Swap the letter for essay drafts. Pull from the essay bank named in the
dashboard's `PROF` array (`Scholarship Q's`, `Scholarship Responses`) and
**adapt, do not regenerate.** Flag any prompt with no match in the bank rather
than writing cold. Essays follow the same delivery rule: a formatted Google Doc
in the Packets folder, never chat text only.

### Tone calibration from his own rewrites

Added 2026-08-25 after he rewrote the Freeform cover letter and the Freeform
application questions by hand. Both versions are in the Packets folder. Where a
rule below and an older rule in this file disagree, this section is newer and it
is drawn from his own typing, so it wins.

**What he kept untouched.** Every evidence sentence. The Kelvin paragraph, the
yield figures, the fixturing time, the tolerance, the SOP count, the screwdriver
measurements, the CSWA line, all of it survived word for word. He does not
rewrite facts. He rewrites the sentences between them. That is where the drafting
effort belongs.

**Contractions.** He writes I've, I'm, it's, can't. Drafts with zero contractions
read stiff next to his own text. Use them.

**Stated enthusiasm is his register, not a hedge.** He wrote "more than excited
to apply at Freeform", "I can't express how excited I am", "truly excites me",
and "I can't think of a more intriguing thing". Do not strip these as filler.
They are the warmth he adds when he goes over a draft. The banned hedges are
still banned: he never writes "eager to", "confident that", or "hope to".

**Candid self-disclosure, then the pivot.** His opener for why engineering was
"To be completely honest, I originally picked engineering because I was good at
math and science and it offered a stable career ahead of me." He will admit an
unflattering starting motive and then say what changed. Keep that move when the
question invites it.

**His sentences run long.** He expanded several short declaratives into clauses
joined by and, while, and which. A three word sentence like "The reason changed."
is my rhythm and not his. Let his sentences breathe.

**He supplies the lived detail.** He added the metal grade laser cutter, the
design freedom problem at Kelvin, the intern cohort, and the country club line.
None of it was available to me. When a paragraph needs connective tissue, ask him
for the anecdote instead of writing a claim that spans the gap.

**What he cut, and why it matters.**

- The Hispanic Scholarship Fund sentence. He asked for it, then struck it. Do not
  volunteer background or identity items in application text.
- "I have not printed metal." He struck the gap acknowledgment. The standing
  ask-first rule holds and the default answer is no.
- "Neither one had a deadline or a grade attached to it." Struck, because the
  projects were coursework. See the correction above.
- The Peer Leader item, in the teamwork answer. He replaced it with the Kelvin
  intern cohort and years working the line at Columbine Country Club. For team
  and pressure questions he prefers real work environments over the mentoring
  role.

**Banned vocabulary governs my drafting, not his.** He wrote "cutting edge
technology" himself. Never edit his own sentence to satisfy the list.

**Spelling.** He types "Solidworks". Finished documents use "SolidWorks".

**Closings.** He ends warm and forward looking. "I am ready to start in May 2027,
and I can't express how excited I am to get the opportunity to apply my
experience and skills to the work at Freeform." A flat closing is one of the
first things he rewrites.

### Facts that came out of those rewrites

- **Columbine Country Club**, back of house, several years on the line. High
  pressure teamwork under a ticket clock. His preferred teamwork evidence.
- **Kelvin intern cohort**, small, mixed expertise, and he moved between multiple
  projects rather than owning one. His preferred adaptability evidence.
- **The Freeform hook in his words**: at Kelvin, fabrication limited design
  freedom. Sometimes they needed the strength of metal in a printed part, other
  times the geometry a printer gives that the metal grade laser cutter cannot.
  That is why AI controlled metal printing reads as the step up from his last
  internship.

---

# voice-dna

The anti-slop rulebook. Ported from `santifer/career-ops` (`voice-dna.template.md`,
MIT), with Tier 2 rewritten for Joaquin's register.

**The enforceable lists live in the embedded `banned.json`, not here.** This file is
why. the gate reads the JSON; edit that file when a rule
changes, and this one only when the reasoning does.

---

### Two tiers

**Tier 1, the anti-slop guardrail.** Banned vocabulary, banned structures, no em
dashes, no negative parallelism, rhythm. Applies to **everything generated**:
cover letters, essays, follow-ups, chat replies about this work, commit
messages, docs in this repo.

**Tier 2, register.** How a sentence should sound once Tier 1 has cleared. This
applies to letters, essays and follow-ups only.

**Accuracy outranks both.** Never drop, soften or round a real number to improve
rhythm. Never invent a detail to sound more human. Voice DNA shapes wording; it
never changes content. A letter that reads a little stiff and is true beats a
letter that flows and is not.

**Precedence**, highest first:

1. What Joaquin says in the conversation
2. the **profile** section, his own layer
3. Tier 1 here
4. Tier 2 here, then everything else

His layer wins over this file. If he adopts a habit that contradicts a rule
below, the rule is what changes.

---

### Tier 1: what marks text as machine-written

#### Dead vocabulary

Roughly 90 words in the embedded `banned.json` under `dead_vocabulary`. These are
statistically overrepresented in LLM output; they are the fingerprint. One is
enough to fail a draft. The worst offenders for an engineering letter:
*leverage, robust, seamless, innovative, spearheaded, facilitated, meticulous,
passionate, cutting-edge, showcase, foster, testament, best practices, proven
track record.*

Also banned: **"serves as", "stands as", "marks a", "represents a"** when used
to dodge "is". Just say *is*.

#### Dead phrases and mechanical transitions

*"It's important to note", "in order to" (say "to"), "at the end of the day",
"moving forward", "in other words".* And the openers we already banned: *"I am
writing to express", "I am pleased to", "I am excited to".*

Transitions: *furthermore, additionally, moreover, that said, with that in
mind.* Let the sentences sit next to each other. If two sentences need a
connector to relate, the second sentence is in the wrong place.

#### Negative parallelism, the big one

This is the single most reliable tell, and the one our skill said nothing about
until now. Every model does it, several times per output, because it makes a
shallow idea sound considered.

> "This isn't X. This is Y." · "It's not just about X, it's about Y." ·
> "Not only X, but also Y." · "Less X, more Y." · "The question isn't X."
> "You don't need X. You need Y."

And the disguised versions, which are the same skeleton in a coat:

> "While X might seem right, Y is actually..." · "Sure, X works. But Y is where
> the real..." · "X gets all the attention, but Y is what actually..."

**Any sentence that negates one framing and then asserts a corrected one.**

The fix is one move: delete everything before the positive claim. "It's not
about the tooling, it's about the process" becomes "It's about the process."
The negated half carried no information. A reader does not need to be told what
something is not before learning what it is.

#### Puffery and significance inflation

*"A pivotal moment", "marking a significant shift", "setting the stage for".*
State the fact. The reader decides whether it is significant. In a cover letter
this shows up as inflating a summer internship into a transformation; the yield
number is impressive on its own and gets less so the moment it is described as
impressive.

#### The rule of three

*"speed, efficiency, and innovation."* Three adjectives, three short phrases,
three items, every time. It makes thin analysis look complete.

**Use two. Or four. Or the one that matters.** One three-item list in a letter
is fine and often natural. Two is a pattern. The checker warns at two.

#### False ranges

*"From prototyping to production."* If there is no meaningful middle ground
between the two ends, the range is decoration. Name one thing instead.

#### Elegant variation

The repetition penalty pushes a model to swap terms: a company becomes "the
firm", then "the organization", then "the employer". **Use the name again.**
Forced synonyms read worse than repetition. This applies hard to company names
in a letter, where the swap reads as though the writer forgot who they were
writing to.

#### Participle padding

*"...highlighting my commitment to quality", "...underscoring the importance
of", "...reflecting broader trends in".* An "-ing" clause bolted to a sentence
to manufacture depth. Delete it. If the analysis matters it deserves a sentence
with a claim in it.

#### Metronome rhythm

Every sentence the same length, every paragraph the same number of sentences,
even pacing throughout. Machine text has no texture.

This is the rule our old five-paragraph spec broke by design, and it is a large
part of why the IMEG letter read as AI. Real writing breathes unevenly. Short.
Then longer. Then one that earns its length because the thought needed the room.

`check_letter.py` measures the spread of paragraph and sentence lengths and
warns when it goes flat.

#### Collaborative leakage

*"I hope this helps", "Certainly", "Great question", "Would you like me to".*
These belong in chat. They must never reach a document.

---

### Tier 2: Joaquin's register

career-ops writes Tier 2 for a technical blogger: contractions, sentences opening
with "And", hedges like "kinda", parenthetical asides. **That voice is wrong
here** and importing it raw would make the letters worse. He is a college senior
writing to an engineering hiring team. The register below is his, taken from his
own letters.

- **Earnest and plain.** No swagger, no consultant vocabulary, no word he would
  not say out loud in a shop.
- **Evidence first, intent second.** Open on the strongest concrete thing he has
  done, then name the role. Never open on wanting the job.
- **Active voice, first person.** "I raised yield", not "yield was raised".
- **Concrete nouns, physical verbs.** He machines, models, measures, fixtures,
  scraps parts, holds a tolerance. Physical verbs are available to him that are
  not available to most applicants; use them.
- **Contractions: sparing.** Natural in a follow-up message. Rare in a letter.
  Not banned, not a default.
- **Sentences may open with And or But** when the rhythm calls for it, which is
  perhaps once in a letter. Not a tic to reach for.
- **Specific beats large.** "6 build iterations" beats "extensive iteration".
  Strength comes from precision, never from a bigger adjective.
- **Say the uncertain thing plainly** when it is real: what he has not done, what
  a posting asks for that he lacks. He is a student and a letter that admits a
  boundary is more credible than one that does not.
- **If the point is made, stop.** No paragraph that restates the letter.

---

### Frequency labels

Every rule carries a weight. Applying all of them as absolutes is what produced
the stiff, formulaic output in the first place.

- **HARD RULE.** Never violate. Everything in the embedded `banned.json`, the em dash
  ban, the do-not-claim list, the number rules. `check_letter.py` blocks on
  these.
- **STRONG TENDENCY, 70 to 80%.** Evidence-first openings, active voice, varied
  rhythm, a number in most paragraphs, naming the employer specifically.
- **LIGHT PREFERENCE, context decides.** Word choice, paragraph order, where the
  award goes, whether a contraction fits. Unlabelled guidance is light.

**Do not overfit.** Do not use the same opening formula every time because it
worked once. Do not avoid a word forever because it sits near a banned one. Let
the posting and the material decide the shape.

---

### The litmus test

Before the doc gets built, read the draft once and ask:

> **Does this sound like something Joaquin would actually write, or does it
> sound like an AI trying very hard to imitate him?**

If it feels forced, pull back. The checker catches patterns. This catches the
thing the checker cannot.

---

# writing

Recruiter-side heuristics, keyword mirroring, and ATS rules. Adapted from
`santifer/career-ops` (`modes/_writing.md`, `modes/heuristics/recruiter-side.md`,
MIT).

Applies to cover letters, essays, form answers and follow-ups. It does not apply
to sweep reports or anything internal.

---

### The risk map

Before drafting, build this internally. **Do not print it.** It decides emphasis,
nothing else.

| The doubt in the reader's head | What answers it | How the letter uses that |
|---|---|---|
| Can a sophomore do this work? | Kelvin was production, not a shadowing program | Lead with the yield number, which is an outcome and not a duty |
| Does he actually know the tools? | SolidWorks plus the machining | Put the exact tool in a sentence where it did something |
| Is the experience relevant here? | Adjacent process, different domain | Translate the proof into the posting's language, never restate the posting |
| Is there a logistics blocker? | Term dates, location, housing | Answer only if the posting raised it. See the housing rule in `profile.md` |
| Is this a form letter? | Weak or broad sentences | Rewrite any sentence that would survive a find-and-replace of the company name |

**Never invent evidence to close a doubt.** A doubt left open is survivable. A
fabricated claim found later is not.

### The six-second gate

A first reader gives the top third of the page about six seconds. In that space
it must be impossible to miss:

- the role he is applying for,
- the strongest matching thing he has done, with its number,
- and that it was real work with a real outcome.

If a reader has to assemble his fit from scattered sentences, the opening
paragraph is wrong. Rewrite it before touching anything else.

### Sentence shape for evidence

The pattern that works: **action, then the thing acted on, then the method, then
the outcome.**

- "Raised assembly yield from 20% to 85% across 6 build iterations by reworking
  the fixturing."
- "Cut 45 minutes from a 280 minute build, about 16%, with custom assembly
  fixturing."

Weak starts to avoid when a stronger truth is available: *helped, assisted,
supported, was responsible for, worked on, participated in, had the opportunity
to.* He did the thing. Say he did the thing.

### Keyword mirroring

Pull 8 to 10 exact phrases from the posting before drafting, split into two
groups:

- **Machine-read terms.** Tool names, methodology names, the exact role title.
- **Human signals.** The verbs the company uses (own, drive, define, build), the
  nouns for their own products and programs, their outcome language.

Then, when drafting:

- **Mirror their vocabulary, never their structure.** A letter shaped like the
  posting reads as a mail merge.
- **Content stays from his resume.** Only word choice shifts. A keyword never
  introduces a claim.
- **Fit naturally or drop it.** If a term will not go in without bending a
  sentence, leave it out and flag it in the chat reply as unused.
- **Use each term once.** Repeating for density is keyword stuffing and a human
  reader sees it immediately.
- **Apply to the opening, the experience paragraphs, and the problems
  paragraph.** Do **not** apply to the paragraph carrying his own reason for
  applying, or to the closing. Those are in his words. Mirroring there is what
  makes a letter sound like the posting talking back at the reader.

### ATS reality

Optimize for parsing and for a human, not for tricks.

- Exact posting keywords only where they are true.
- No hidden text, no white font, no keyword stuffing, no decorative layout.
- No skill or number that is not in the embedded `profile.json`.
- The Google Doc house format parses cleanly already. Do not add tables, columns,
  text boxes or images to a letter.

### What never goes in a letter

- A wage or salary figure, ever.
- A tool from the `do_not_claim` list.
- A number that is not on his resume, unless it was verified from the posting and
  passed to the checker with `--allow`.
- A sentence that would be equally true in a letter to a different employer.

---

# followup

A short message to a recruiter or an engineer at a company Joaquin has **already
applied to**. Roughly 80 words, sent by email, LinkedIn or Handshake.

**This is not the "message to the hiring team" variant**, which is 250 to 320
words and replaces a cover letter. This is a four sentence note sent after the
application is in. Do not conflate them.

Background, including the two broken outputs this spec was written to prevent, is
in `docs/followup.md`.

---

### Absolutes

1. **Never send it.** Draft only. Joaquin sends.
2. **Never "y'all", "yall", or "ya'll".** Removed permanently.
3. **No em dashes.** Tier 1 of the **voice-dna** section applies in full here,
   banned vocabulary included.
4. **No numbers of any kind.** No yield figures, no cycle times, no tolerances,
   no dates, no wage. A follow-up may land on LinkedIn or Handshake, and resume
   numbers stay off public surfaces. The experience items carry the weight
   instead. `check_letter.py --kind followup` blocks on any digit.
5. **Never claim** anything on the `do_not_claim` list in
   the embedded `profile.json`. SolidWorks is his CAD.
6. **Kelvin Thermal Technologies is past tense.**
7. **Name the company.** A follow-up that never names the employer is a form
   letter.

### The template

```
Hi [First name],

I just applied to the [exact role title as posted] role at [Company] and wanted to reach
out to express my sincerest enthusiasm. I'm very interested in the work [Company] is doing
in [FIELD][, particularly DETAIL]. I believe this role is an incredible fit for my
experience in [EXPERIENCE ITEMS]. Thank you in advance for your consideration.

Joaquin Zarazua
```

Email subject line, when the channel is email:
`Application for [exact role title as posted]`

### Slot rules

**[FIELD]**

- One noun phrase, six words maximum.
- No internal "and". No internal comma.
- It names what the company builds; it is not a sentence about it.
  `advanced nuclear` is right. `getting a new reactor design built as real
  hardware` is wrong, that is a gerund clause and it does not fit this slot.

**[, particularly DETAIL]**, optional, at most one

- For a site, program, product or technical problem worth naming.
- Attaches with one comma and the word "particularly". Nothing else.
- A single phrase. No internal "and", no second comma, no clause.
- **If it will not fit that shape, drop it.** A shorter message that says less
  beats a run-on.

**[EXPERIENCE ITEMS]**

- **Two or three items. Vary it between messages, and prefer two.** This is the
  one rule that changed when the writing system came over from career-ops. The
  old spec mandated exactly three, which made every follow-up he sent carry an
  identical three-item list in an identical slot: the same mail-merge tic that
  got "y'all" removed, and a documented AI tell (see the rule of three in
  the **voice-dna** section). Two items, chosen because they are the two the
  posting actually asked for, reads sharper and cannot form a pattern across
  messages.
- Serial comma before the final "and" when there are three.
- All items the same grammatical shape: noun phrases, two to five words each.
- **No item may contain the word "and".** "SolidWorks and GD&T" is two items
  disguised as one; pick one.
- Prefer noun forms over gerunds: `process yield improvement`, not `raising
  process yield`.
- Drawn from the resume, ordered to match what the posting asks for first.

**[Company]**

- Spelled the way the employer spells it. `Kairos Power`, not `Kairos`.
- Appears twice, once in sentence 1 and once in sentence 2. If the name runs
  longer than three words, the second mention may read `the work the team is
  doing in ...`.
- Do not swap in a synonym on the second mention. See elegant variation in
  the **voice-dna** section.

**[First name]**

- If no contact name is known, drop the greeting line entirely and open on
  sentence 1.
- Never "Dear Hiring Manager" here. This is a message, not a letter.

### Sentence rules

- **Sentences 2 and 3 are separate sentences.** Never joined by "and". This is
  what fixes the old template, which collapsed the moment the field slot grew.
  The checker blocks on the joined form.
- No sentence carries more than one "and", except the sentence with the
  experience list, where the only "and" is the serial one.
- Body is 60 to 90 words. Hard cap 110.
- **Keep "I believe this role is an incredible fit."** It looks like a hedge and
  it is not. It is his line and it stays.
- Cut every other hedge: "eager to", "confident that", "hope to", "I would love
  to", "I feel that".

### Before handing it over

Run the checker. It covers most of this list mechanically:

```bash
python3 scripts/check_letter.py draft.txt --kind followup
```

Then read for the things it cannot see:

- [ ] Exactly four sentences in the body
- [ ] Company named twice, spelled the way the employer spells it
- [ ] Exact role title as posted
- [ ] FIELD is one noun phrase, six words or fewer, no "and", no comma
- [ ] DETAIL is absent, or is one phrase attached with ", particularly"
- [ ] Two or three experience items, same shape, none containing "and"
- [ ] Not the same item count as the last follow-up he sent
- [ ] Name on its own line, no trailing period
- [ ] Nothing sent

### Delivery

- **Plain text in the chat reply**, so he can paste it straight into LinkedIn or
  Handshake. This is the one deliverable in this skill allowed to be chat text;
  the Google Doc rule applies to letters and essays, not to follow-ups.
- **A Gmail draft as well**, only when a real email address is known and he has
  asked for one. Draft only. Never send.
- **Never filed in the Packets folder.** That folder is for cover letters and
  essays.

### Worked example

Kairos Power, Mechanical and Manufacturing Engineering Intern, two items:

```
Hi [First name],

I just applied to the Mechanical and Manufacturing Engineering Intern role at Kairos Power
and wanted to reach out to express my sincerest enthusiasm. I'm very interested in the work
Kairos Power is doing in advanced nuclear, particularly turning a new reactor design into
real hardware. I believe this role is an incredible fit for my experience in prototype build
iteration and process yield improvement. Thank you in advance for your consideration.

Joaquin Zarazua
```

The before-and-after pair for this and for Western Digital, with the reasoning,
is in `docs/followup.md`.

---

# The gate

Two paths. Take the first one whenever a shell is available, because it checks things a person reading cannot: every number against the resume, the misattribution, the tense, and roughly 160 banned strings.

## Path 1, with a shell

Run this once per session to lay the tool down:

```bash
set -e
mkdir -p /tmp/apb/config /tmp/apb/scripts

cat > /tmp/apb/config/profile.json <<'APB_EOF'
{
  "_comment": "Machine-readable facts for scripts/build_letter_html.py and scripts/check_letter.py. The prose layer that governs voice lives in references/profile.md. Keep the two in sync: a number added here must be real, and a number removed here will start failing the letter gate.",
  "identity": {
    "name": "Joaquin Zarazua",
    "city": "Centennial, CO",
    "phone": "720-435-0880",
    "email": "joaquinz0721@gmail.com",
    "linkedin_text": "linkedin.com/in/joaquinzarazua",
    "linkedin_url": "http://linkedin.com/in/joaquinzarazua"
  },
  "house_format": {
    "font": "'Times New Roman',serif",
    "size": "11pt",
    "space_after": "10pt",
    "contact_space_after": "15pt",
    "salutation": "Dear Hiring Manager,",
    "signoff": "Sincerely,",
    "body_words_min": 350,
    "body_words_max": 450,
    "paragraphs_min": 4,
    "paragraphs_max": 6
  },
  "education": {
    "school": "University of Colorado Boulder",
    "degree": "Mechanical Engineering",
    "graduation": "May 2028",
    "targeting": "Summer 2027"
  },
  "credentials": {
    "_comment": "Certifications he actually holds. check_letter.py warns on any 'certified' claim naming something absent from this list, because a certification is exactly the kind of claim that is easy to assert and hard to walk back.",
    "verified": [
      {
        "name": "CSWA",
        "full": "Certified SolidWorks Associate",
        "aliases": [
          "CSWA",
          "Certified SolidWorks Associate",
          "SolidWorks Associate"
        ]
      }
    ]
  },
  "employment": [
    {
      "employer": "Kelvin Thermal Technologies",
      "tense": "past",
      "ended": "August 2026",
      "note": "Every mention must be past tense. A present-tense Kelvin sentence is a factual error, not a style slip."
    }
  ],
  "resume_numbers": [
    {
      "tokens": [
        "20%",
        "85%"
      ],
      "claim": "yield raised from 20% to 85%",
      "owner": "Kelvin Thermal Technologies"
    },
    {
      "tokens": [
        "6"
      ],
      "claim": "across 6 build iterations",
      "owner": "Kelvin Thermal Technologies"
    },
    {
      "tokens": [
        "45",
        "280",
        "16%"
      ],
      "claim": "45 minutes cut from a 280 minute build, about 16%, via custom assembly fixturing",
      "owner": "Kelvin Thermal Technologies"
    },
    {
      "tokens": [
        "0.1"
      ],
      "claim": "plus or minus 0.1 mm tolerances held across builds",
      "owner": "Kelvin Thermal Technologies"
    },
    {
      "tokens": [
        "2"
      ],
      "claim": "2 SOPs authored",
      "owner": "Kelvin Thermal Technologies"
    },
    {
      "tokens": [
        "50",
        "50+",
        "0.5"
      ],
      "claim": "50+ precision measurements, modeled to under 0.5 mm",
      "owner": "ratcheting screwdriver reverse-engineering project (school coursework, never call it personal or own-time work)",
      "never_attribute_to": [
        "Kelvin"
      ]
    },
    {
      "tokens": [
        "6"
      ],
      "claim": "6-part compressed-air wobbler engine, mill and lathe",
      "owner": "wobbler engine project (school coursework, never call it personal or own-time work)"
    },
    {
      "tokens": [
        "20",
        "20+"
      ],
      "claim": "20+ first-year students mentored",
      "owner": "Peer Leader"
    },
    {
      "tokens": [
        "2027"
      ],
      "claim": "Summer 2027 target term",
      "owner": "availability"
    },
    {
      "tokens": [
        "2028"
      ],
      "claim": "May 2028 graduation",
      "owner": "education"
    },
    {
      "tokens": [
        "2026"
      ],
      "claim": "August 2026, when the Kelvin internship ended",
      "owner": "employment"
    }
  ],
  "do_not_claim": [
    "FEA",
    "finite element",
    "CFD",
    "computational fluid",
    "NX",
    "Teamcenter",
    "ANSYS",
    "AutoCAD",
    "Revit",
    "BIM",
    "Creo",
    "welding",
    "welded",
    "weld"
  ],
  "do_not_claim_note": "SolidWorks is his CAD. He does machining, sheet metal, laser cutting, and 3D printing. MEP and building-services postings ask for AutoCAD or BIM constantly; write around it by leading with SolidWorks depth and the additive and thermal work.",
  "awards": [
    {
      "name": "Clinton J. Helton Manufacturing Scholarship",
      "body": "SME Education Foundation",
      "use_when": "manufacturing, production, or process engineering"
    },
    {
      "name": "CU Esteemed Scholars Hale award",
      "body": "University of Colorado Boulder",
      "use_when": "academic merit is relevant"
    },
    {
      "name": "Opportunity Next Colorado",
      "body": "Opportunity Next",
      "use_when": "rarely, only on a direct match"
    },
    {
      "name": "Hispanic National Merit recognition",
      "body": "College Board",
      "use_when": "rarely, only on a direct match"
    }
  ],
  "drive": {
    "packets_folder": "1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP",
    "letters_folder": "1pPulXeoTIXN6sJXuAByc2sW37dThROoB"
  }
}
APB_EOF

cat > /tmp/apb/config/banned.json <<'APB_EOF'
{
  "_comment": "Single source of truth for the banned lists. references/voice-dna.md is the prose explanation of WHY these are banned; this file is what scripts/check_letter.py enforces. Ported from santifer/career-ops voice-dna.template.md sections 3 and 4, MIT licensed. Edit here, not in the prose.",

  "dead_vocabulary": [
    "delve", "realm", "harness", "unlock", "tapestry", "paradigm", "cutting-edge",
    "revolutionize", "intricate", "intricacies", "showcasing", "showcase", "crucial",
    "pivotal", "surpass", "meticulously", "meticulous", "vibrant", "unparalleled",
    "leverage", "leveraged", "leveraging", "synergy", "synergies", "innovative",
    "game-changer", "testament", "commendable", "groundbreaking", "foster", "fostering",
    "holistic", "garner", "accentuate", "pioneering", "trailblazing", "unleash",
    "versatile", "transformative", "redefine", "seamless", "seamlessly", "robust",
    "breakthrough", "empower", "streamline", "frictionless", "elevate", "effortless",
    "data-driven", "insightful", "proactive", "mission-critical", "visionary",
    "disruptive", "reimagine", "unprecedented", "leading-edge", "synergize",
    "democratize", "state-of-the-art", "immersive", "supercharge", "interplay",
    "captivate", "spearheaded", "spearhead", "facilitated", "orchestrated",
    "championed", "passionate", "results-oriented", "best-in-class",
    "stakeholder alignment", "actionable insights", "move the needle", "north star",
    "unique opportunity", "perfect fit", "strong track record", "proven track record",
    "demonstrated ability", "best practices", "in today's"
  ],

  "dead_phrases": [
    "it's important to note", "it is important to note", "it's worth noting",
    "it is worth noting", "in order to", "at the end of the day", "moving forward",
    "to put this in perspective", "what makes this particularly",
    "the implications here", "in other words", "it goes without saying",
    "let's dive in", "let's explore", "let's unpack", "dive into",
    "i am pleased to", "i am writing to express", "i am excited to",
    "i am writing to apply", "i would like to express", "i am reaching out to express my interest"
  ],

  "dead_transitions": [
    "furthermore", "additionally", "moreover", "that said", "that being said",
    "with that in mind", "it is also worth mentioning", "on top of that"
  ],

  "negative_parallelism": [
    {"pattern": "(?i)\\bit'?s not (just )?(about )?[^.;]{2,60}?[,.] it'?s\\b", "label": "It's not X, it's Y"},
    {"pattern": "(?i)\\bis not (just )?[^.;]{2,60}?[,.] (it|this|that) is\\b", "label": "is not X, it is Y"},
    {"pattern": "(?i)\\b(this|that|it) isn'?t [^.;]{2,60}?[.;] (this|that|it) is\\b", "label": "This isn't X. This is Y"},
    {"pattern": "(?i)\\bnot only [^.;]{2,60}? but also\\b", "label": "Not only X, but also Y"},
    {"pattern": "(?i)\\bless [a-z]+, more [a-z]+\\b", "label": "Less X, more Y"},
    {"pattern": "(?i)\\bthe question isn'?t\\b", "label": "The question isn't X"},
    {"pattern": "(?i)\\byou don'?t need [^.;]{2,60}?[.;] you need\\b", "label": "You don't need X. You need Y"},
    {"pattern": "(?i)\\bforget [^.;]{2,40}?[.;] (this|that|it|here)\\b", "label": "Forget X. This is Y"},
    {"pattern": "(?i)\\bstop [a-z]+ing [^.;]{2,60}?[.;] start\\b", "label": "Stop X. Start Y"},
    {"pattern": "(?i)\\bwhile [^.;]{2,60}? might seem [^.;]{0,40}?, [^.;]{2,40}? is actually\\b", "label": "While X might seem, Y is actually (disguised)"},
    {"pattern": "(?i)\\bsure, [^.;]{2,60}?[.;] but [^.;]{2,40}? is where\\b", "label": "Sure X. But Y is where (disguised)"},
    {"pattern": "(?i)\\bgets all the attention, but\\b", "label": "X gets the attention, but Y (disguised)"},
    {"pattern": "(?i)\\brather than (just )?[^.;]{2,50}?, i (built|led|ran|cut|held|raised)\\b", "label": "Rather than X, I Y (reframe)"}
  ],

  "copulative_avoidance": [
    "serves as", "stands as", "marks a", "represents a", "boasts a",
    "holds the distinction of"
  ],

  "participle_padding": [
    "highlighting", "underscoring", "emphasizing", "reflecting broader",
    "contributing to the", "showcasing the", "demonstrating the importance"
  ],

  "hedges": [
    "i am eager to", "i'm eager to", "eager to", "i am confident that",
    "i am confident", "i hope to", "i believe i would", "i would love to",
    "i feel that", "i think i could", "i am passionate about"
  ],

  "engagement_bait": [
    "let that sink in", "read that again", "this changes everything",
    "full stop", "here's the part nobody"
  ],

  "never_write": ["y'all", "yall", "ya'll"]
}
APB_EOF

cat > /tmp/apb/scripts/check_letter.py <<'APB_EOF'
#!/usr/bin/env python3
"""Gate a drafted letter before it becomes a Google Doc.

Everything the skill used to enforce by asking the model to pay attention is
enforced here instead: banned vocabulary, negative parallelism, tools Joaquin
does not have, and numbers that are not on his resume.

    python3 scripts/check_letter.py spec.json
    python3 scripts/check_letter.py draft.txt --kind followup
    python3 scripts/check_letter.py spec.json --allow 1965 --allow 400

Exit codes:
    0   pass, nothing found
    1   warn, advisory findings only, drafting may continue
    2   BLOCK, do not build the doc until these are fixed

--allow takes a number verified from the posting or from company research, and
is the deliberate escape hatch for a real figure that is not on the resume. It
has to be typed out, which is the point: an unexplained number in a letter to an
employer is the failure this script exists to catch.
"""
import sys, os, json, re, argparse, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def load(name):
    with open(os.path.join(ROOT, "config", name), encoding="utf-8") as fh:
        return json.load(fh)

# ── findings ────────────────────────────────────────────────────────────

BLOCK, WARN = "BLOCK", "warn"

class Report:
    def __init__(self):
        self.items = []

    def add(self, level, rule, detail, fix=""):
        self.items.append((level, rule, detail, fix))

    @property
    def blocks(self):
        return [i for i in self.items if i[0] == BLOCK]

    @property
    def warns(self):
        return [i for i in self.items if i[0] == WARN]

    def render(self):
        if not self.items:
            return "PASS. Nothing found.\n"
        out = []
        for level, rule, detail, fix in self.blocks + self.warns:
            tag = "BLOCK" if level == BLOCK else "warn "
            out.append(f"[{tag}] {rule}: {detail}")
            if fix:
                out.append(f"         fix: {fix}")
        out.append("")
        out.append(f"{len(self.blocks)} blocking, {len(self.warns)} advisory.")
        if self.blocks:
            out.append("Do not build the doc. Fix the blocking findings and re-run.")
        return "\n".join(out) + "\n"

# ── text helpers ────────────────────────────────────────────────────────

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

def sentences(text):
    return [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]

def find_phrase(text, phrase):
    """Whole-phrase, case-insensitive, word-bounded where the edges are word chars."""
    lead = r"\b" if phrase[0].isalnum() else ""
    tail = r"\b" if phrase[-1].isalnum() else ""
    return re.search(lead + re.escape(phrase) + tail, text, re.I)

def context(text, match, width=48):
    a = max(0, match.start() - width // 2)
    b = min(len(text), match.end() + width // 2)
    return "..." + text[a:b].replace("\n", " ").strip() + "..."

# ── checks ──────────────────────────────────────────────────────────────

# Built from codepoints so this file stays free of the characters it bans, the
# same convention dashboard/patches/apply-delegation.py follows. U+2014 em dash,
# U+2013 en dash.
DASHES = ((chr(0x2014), "em dash"), (chr(0x2013), "en dash"))

def check_dashes(text, rep):
    for ch, name in DASHES:
        if ch in text:
            m = re.search(re.escape(ch), text)
            rep.add(BLOCK, name, context(text, m),
                    "comma, semicolon, colon, parentheses, or two sentences")

def check_lists(text, rep, banned):
    for word in banned["dead_vocabulary"]:
        m = find_phrase(text, word)
        if m:
            rep.add(BLOCK, "dead AI vocabulary", f'"{word}" -> {context(text, m)}',
                    "say the plain thing instead")
    for phrase in banned["dead_phrases"]:
        m = find_phrase(text, phrase)
        if m:
            rep.add(BLOCK, "dead phrase", f'"{phrase}"', "delete it or rewrite the sentence")
    for word in banned["dead_transitions"]:
        if re.search(r"(?i)(^|[.;]\s+)" + re.escape(word) + r"\b", text):
            rep.add(WARN, "mechanical transition", f'"{word}"',
                    "let the sentences sit next to each other")
    for phrase in banned["copulative_avoidance"]:
        m = find_phrase(text, phrase)
        if m:
            rep.add(WARN, "copulative avoidance", f'"{phrase}"', 'just say "is" or "has"')
    for word in banned["participle_padding"]:
        m = find_phrase(text, word)
        if m:
            rep.add(WARN, "participle padding", f'"{word}"',
                    "delete the phrase, or give the claim its own sentence")
    for phrase in banned["hedges"]:
        m = find_phrase(text, phrase)
        if m:
            rep.add(WARN, "hedge", f'"{phrase}"', "lead with the evidence instead")
    for phrase in banned["engagement_bait"] + banned["never_write"]:
        m = find_phrase(text, phrase)
        if m:
            rep.add(BLOCK, "never write this", f'"{phrase}"', "remove it")

def check_negative_parallelism(text, rep, banned):
    for entry in banned["negative_parallelism"]:
        m = re.search(entry["pattern"], text)
        if m:
            rep.add(BLOCK, "negative parallelism (the single biggest tell)",
                    f'{entry["label"]} -> {context(text, m, 80)}',
                    "delete everything before the positive claim and keep only what it IS")

# A letter is allowed to NAME a tool he does not have, in order to say plainly
# that he does not have it. references/profile.md calls that the gap play and
# prefers it to a dodge when the posting makes the tool central. Blocking the
# disclaimer along with the claim would have forced the letter to be evasive,
# which is the opposite of the rule. A negated mention drops to a warning so a
# human still reads the sentence; an unqualified one still blocks.
NEGATORS = re.compile(
    r"\b(neither|nor|not|never|no|none|without|lack(?:s|ing|ed)?|"
    r"haven'?t|hasn'?t|don'?t|doesn'?t|didn'?t|instead of|rather than|"
    r"unfamiliar|yet to)\b", re.I)

def check_do_not_claim(text, rep, profile):
    for term in profile["do_not_claim"]:
        for sent in sentences(text):
            m = find_phrase(sent, term)
            if not m:
                continue
            if NEGATORS.search(sent):
                rep.add(WARN, "names a tool he does not have, and reads as a disclaimer",
                        f'"{term}" -> "{sent[:100]}..."',
                        "fine if the sentence really does deny it; block it yourself if it hedges toward having it")
            else:
                rep.add(BLOCK, "claims a tool or skill he does not have",
                        f'"{term}" -> {context(text, m)}',
                        profile["do_not_claim_note"])

NUM = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*(%?)")

def check_numbers(text, rep, profile, extra_allowed):
    allowed = set(extra_allowed)
    for entry in profile["resume_numbers"]:
        for tok in entry["tokens"]:
            allowed.add(tok.rstrip("+").rstrip("%"))
    for m in NUM.finditer(text):
        raw = m.group(1).replace(",", "")
        if raw in allowed:
            continue
        rep.add(BLOCK, "number is not on his resume", f'"{m.group(0).strip()}" -> {context(text, m)}',
                "use a resume figure, or pass --allow "
                f"{raw} if you verified it from the posting")

def check_attribution(text, rep, profile):
    for entry in profile["resume_numbers"]:
        forbidden = entry.get("never_attribute_to")
        if not forbidden:
            continue
        for sent in sentences(text):
            hit = any(re.search(r"(?<![\w.])" + re.escape(t.rstrip("+")) + r"\b", sent)
                      for t in entry["tokens"])
            if not hit:
                continue
            for bad in forbidden:
                if re.search(r"\b" + re.escape(bad), sent, re.I):
                    rep.add(BLOCK, "number attributed to the wrong project",
                            f'{entry["claim"]} belongs to {entry["owner"]}, not {bad} -> "{sent[:90]}..."',
                            f'move the figure onto {entry["owner"]} or drop it')

CERT_CLAIM = re.compile(
    r"\b(?:i am|i'?m|holds?|hold|earned|received)\s+(?:a\s+|an\s+|the\s+)?"
    r"([A-Za-z][\w .+/-]{1,60}?)\s*(?:certified|certification|certificate)\b", re.I)

def check_credentials(text, rep, profile):
    """A certification is easy to assert and hard to walk back. Warn on any
    'certified' claim that does not name something in the verified list."""
    verified = profile.get("credentials", {}).get("verified", [])
    aliases = {a.lower() for c in verified for a in c.get("aliases", [c["name"]])}
    for sent in sentences(text):
        for m in CERT_CLAIM.finditer(sent):
            named = m.group(1).strip().lower()
            if any(a in named or named in a for a in aliases):
                continue
            rep.add(WARN, "certification claim not in the verified list",
                    f'"{m.group(0).strip()}" -> "{sent[:90]}..."',
                    "add it to credentials.verified in config/profile.json if he really holds it, "
                    "otherwise cut the sentence")

def check_tense(text, rep, profile):
    for job in profile["employment"]:
        if job["tense"] != "past":
            continue
        for sent in sentences(text):
            if job["employer"].split()[0].lower() not in sent.lower():
                continue
            if re.search(r"\b(i am|i'm|currently|presently)\b", sent, re.I):
                rep.add(BLOCK, "present tense on a finished job",
                        f'{job["employer"]} ended {job["ended"]} -> "{sent[:90]}..."',
                        job["note"])

RULE_OF_THREE = re.compile(r"\b[\w][\w'-]*(?:\s+[\w'-]+){0,3},\s+[\w'-]+(?:\s+[\w'-]+){0,3},\s+and\s+[\w'-]+")

def check_rule_of_three(text, rep):
    hits = RULE_OF_THREE.findall(text)
    if len(hits) >= 2:
        rep.add(WARN, "rule of three, more than once",
                f"{len(hits)} three-item lists: " + "; ".join(f'"{h[:40]}"' for h in hits[:3]),
                "use two items, or four, or just the one that matters")

def check_rhythm(paragraphs, rep):
    lengths = [len(p.split()) for p in paragraphs]
    if len(lengths) >= 3:
        spread = statistics.pstdev(lengths) / (sum(lengths) / len(lengths))
        if spread < 0.14:
            rep.add(WARN, "metronome paragraphs",
                    f"word counts {lengths}, spread {spread:.0%}",
                    "let one paragraph run long and one land short")
    for i, para in enumerate(paragraphs, 1):
        sent_lens = [len(s.split()) for s in sentences(para)]
        if len(sent_lens) >= 3:
            spread = statistics.pstdev(sent_lens) / (sum(sent_lens) / len(sent_lens))
            if spread < 0.18:
                rep.add(WARN, "metronome sentences",
                        f"paragraph {i} sentence lengths {sent_lens}",
                        "break one sentence in half, or let one earn its length")

def check_generic(paragraphs, rep):
    """Sentences with no proper noun and no number are the ones that could go to anyone."""
    for i, para in enumerate(paragraphs, 1):
        for sent in sentences(para):
            words = sent.split()
            if len(words) < 8:
                continue
            has_proper = any(w[0].isupper() for w in words[1:] if w[0].isalpha())
            has_number = bool(NUM.search(sent))
            if not has_proper and not has_number:
                rep.add(WARN, "could appear in any letter to any company",
                        f'paragraph {i}: "{sent[:80]}..."',
                        "name the employer, the product, or the figure, or cut it")

def followup_body(paragraphs, profile):
    """Drop the greeting and the signature. Neither is body, and counting them
    made a correct four-sentence message report as five."""
    name = profile["identity"]["name"].lower()
    keep = []
    for para in paragraphs:
        flat = para.strip().lower().rstrip(".,")
        if re.match(r"^(hi|hello|hey|dear)\b[^.!?]{0,40}$", flat):
            continue
        if flat == name:
            continue
        keep.append(para)
    return keep

def check_length(paragraphs, rep, profile, kind):
    hf = profile["house_format"]
    if kind == "followup":
        paragraphs = followup_body(paragraphs, profile)
        words = sum(len(p.split()) for p in paragraphs)
        lo, hi, cap = 60, 90, 110
        if words > cap:
            rep.add(BLOCK, "follow-up over the hard cap", f"{words} words, cap {cap}", "cut a clause")
        elif not lo <= words <= hi:
            rep.add(WARN, "follow-up length", f"{words} words, target {lo} to {hi}", "")
        body = " ".join(paragraphs)
        if len(sentences(body)) != 4:
            rep.add(WARN, "follow-up sentence count",
                    f"{len(sentences(body))} sentences, the template is 4", "")
        if re.search(r"(?i)\bin\b[^.;]{2,40}\band\b[^.;]{2,40}\bi believe this role\b", body):
            rep.add(BLOCK, "sentences 2 and 3 joined",
                    "the field clause and the fit clause are one sentence",
                    "split them, this is the failure the template was rewritten to prevent")
        return
    words = sum(len(p.split()) for p in paragraphs)
    if not hf["body_words_min"] <= words <= hf["body_words_max"]:
        rep.add(WARN, "body length",
                f'{words} words, target {hf["body_words_min"]} to {hf["body_words_max"]}', "")
    if not hf["paragraphs_min"] <= len(paragraphs) <= hf["paragraphs_max"]:
        rep.add(WARN, "paragraph count",
                f'{len(paragraphs)}, expected {hf["paragraphs_min"]} to {hf["paragraphs_max"]}', "")

# ── entry ───────────────────────────────────────────────────────────────

def read_paragraphs(path):
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            spec = json.load(fh)
        return spec["paragraphs"]
    with open(path, encoding="utf-8") as fh:
        return [p.strip() for p in re.split(r"\n\s*\n", fh.read()) if p.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="spec.json, or a plain-text draft with blank-line paragraphs")
    ap.add_argument("--kind", default="letter", choices=["letter", "essay", "followup"])
    ap.add_argument("--allow", action="append", default=[],
                    help="a number verified from the posting; repeatable")
    args = ap.parse_args()

    profile, banned = load("profile.json"), load("banned.json")
    paragraphs = read_paragraphs(args.path)
    text = "\n\n".join(paragraphs)
    rep = Report()

    check_dashes(text, rep)
    check_lists(text, rep, banned)
    check_negative_parallelism(text, rep, banned)
    check_do_not_claim(text, rep, profile)
    check_attribution(text, rep, profile)
    check_credentials(text, rep, profile)
    check_tense(text, rep, profile)
    check_rule_of_three(text, rep)
    check_length(paragraphs, rep, profile, args.kind)

    if args.kind == "followup":
        check_numbers(text, rep, profile, [])          # a follow-up carries no numbers at all
        for m in NUM.finditer(text):
            rep.add(BLOCK, "follow-up contains a number",
                    f'"{m.group(0).strip()}"',
                    "follow-ups may land on LinkedIn or Handshake; no figures, ever")
    else:
        check_numbers(text, rep, profile, [a.strip() for a in args.allow])
        check_rhythm(paragraphs, rep)
        check_generic(paragraphs, rep)

    sys.stdout.write(rep.render())
    sys.exit(2 if rep.blocks else (1 if rep.warns else 0))

if __name__ == "__main__":
    main()
APB_EOF

cat > /tmp/apb/scripts/build_letter_html.py <<'APB_EOF'
#!/usr/bin/env python3
"""Render a letter as HTML that Google Drive converts into a native Google Doc
carrying Joaquin's house format.

    python3 scripts/build_letter_html.py spec.json
    python3 scripts/build_letter_html.py spec.json --allow 1965

Upload the result with create_file(contentMimeType='text/html',
textContent=<this output>) and DO NOT set disableConversionToGoogleType.
Leaving conversion on is what makes Drive produce a real Google Doc.

spec.json:
    {
      "out": "/tmp/Cover Letter - Company.html",
      "date": "August 24, 2026",
      "hiring_team": "Acme Summer 2027 Internship Hiring Team",
      "paragraphs": ["body 1", "body 2", "body 3", "body 4", "closing"],
      "kind": "letter"          # or "essay"; optional, defaults to letter
    }

Identity, house format and the letter gate all come from config/, so nothing
about Joaquin is hardcoded here. The gate runs before anything is written: a
blocking finding means no file, by design. There is no bypass flag.
"""
import sys, os, json, html, argparse, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def load_profile():
    with open(os.path.join(ROOT, "config", "profile.json"), encoding="utf-8") as fh:
        return json.load(fh)

def styles(hf):
    font = f"font-family:{hf['font']};font-size:{hf['size']};"
    return {
        "p":     font + f"margin:0 0 {hf['space_after']} 0;text-align:left;",
        "ctr":   font + "margin:0;text-align:center;",
        "ctr2":  font + f"margin:0 0 {hf['contact_space_after']} 0;text-align:center;",
    }

def build(profile, date_line, hiring_team, paragraphs):
    hf, ident = profile["house_format"], profile["identity"]
    lo, hi = hf["paragraphs_min"], hf["paragraphs_max"]
    if not lo <= len(paragraphs) <= hi:
        raise ValueError(
            f"expected {lo} to {hi} paragraphs (body plus closing), got {len(paragraphs)}")

    s, e = styles(hf), html.escape
    out = ['<html><head><meta charset="utf-8"></head><body>']
    out.append(f'<p style="{s["ctr"]}"><b>{e(ident["name"])}</b></p>')
    out.append(
        f'<p style="{s["ctr2"]}">{e(ident["city"])}&nbsp; |&nbsp; {e(ident["phone"])}'
        f'&nbsp; | {e(ident["email"])}&nbsp; |&nbsp; '
        f'<a href="{e(ident["linkedin_url"])}">{e(ident["linkedin_text"])}</a></p>')
    out.append(f'<p style="{s["p"]}">{e(date_line)}</p>')
    out.append(f'<p style="{s["p"]}">{e(hiring_team)}</p>')
    out.append(f'<p style="{s["p"]}">{e(hf["salutation"])}</p>')
    out.append(f'<p style="{s["p"]}">&nbsp;</p>')
    for para in paragraphs:
        out.append(f'<p style="{s["p"]}">{e(para)}</p>')
    out.append(f'<p style="{s["p"]}">&nbsp;</p>')
    out.append(f'<p style="{s["p"]}">{e(hf["signoff"])}</p>')
    out.append(f'<p style="{s["p"]}">{e(ident["name"])}</p>')
    out.append("</body></html>")
    return "\n".join(out)

def gate(spec_path, kind, allow):
    """Run the letter gate. A blocking finding stops the build."""
    cmd = [sys.executable, os.path.join(HERE, "check_letter.py"), spec_path, "--kind", kind]
    for a in allow:
        cmd += ["--allow", a]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stderr.write(proc.stdout)
    if proc.returncode == 2:
        sys.stderr.write(
            "\nRefusing to build the doc. Fix the blocking findings above and re-run.\n")
        sys.exit(2)
    return proc.returncode

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--allow", action="append", default=[],
                    help="a number verified from the posting; passed through to the gate")
    args = ap.parse_args()

    with open(args.spec, encoding="utf-8") as fh:
        spec = json.load(fh)

    gate(args.spec, spec.get("kind", "letter"), args.allow)

    profile = load_profile()
    doc = build(profile, spec["date"], spec["hiring_team"], spec["paragraphs"])
    dest = spec.get("html_out") or spec["out"].rsplit(".", 1)[0] + ".html"
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(dest)

if __name__ == "__main__":
    main()
APB_EOF

python3 -c "import json;[json.load(open(f)) for f in ['/tmp/apb/config/profile.json','/tmp/apb/config/banned.json']]"
echo "letter tool ready at /tmp/apb/scripts/"
```

Then gate every draft before it becomes a document:

```bash
python3 /tmp/apb/scripts/check_letter.py draft.txt
python3 /tmp/apb/scripts/check_letter.py draft.txt --kind followup
python3 /tmp/apb/scripts/check_letter.py /tmp/spec.json --allow 1965
```

Exit 0 is clean, 1 is advisory and worth reading, **2 means fix it and re-run.** To build the upload HTML, which runs the gate again and writes nothing on a block:

```bash
python3 /tmp/apb/scripts/build_letter_html.py /tmp/spec.json
```

## Path 2, no shell

Run this by eye, in this order. It is the same set the script enforces, minus the arithmetic.

1. **Negative parallelism.** Any sentence that negates one framing and then asserts a corrected one. This is the biggest tell and the one to hunt first:

   - It's not X, it's Y
   - is not X, it is Y
   - This isn't X. This is Y
   - Not only X, but also Y
   - Less X, more Y
   - The question isn't X
   - You don't need X. You need Y
   - Forget X. This is Y

   Plus the disguised forms: "While X might seem right, Y is actually", "Sure, X works. But Y is where", "X gets all the attention, but Y". Fix: delete everything before the positive claim.

2. **Dead vocabulary.** Any one of these fails the draft. The full list is in the embedded `banned.json`; these are the ones that actually turn up in his letters:

   `leverage`, `robust`, `seamless`, `innovative`, `spearheaded`, `facilitated`, `meticulous`, `passionate`, `showcase`, `foster`, `testament`, `crucial`, `pivotal`, `streamline`, `cutting-edge`, `best practices`, `proven track record`, `demonstrated ability`

3. **Dead openers.** "i am pleased to", "i am writing to express", "i am excited to", "i am writing to apply", "i would like to express", "i am reaching out to express my interest"

4. **Mechanical transitions.** `furthermore`, `additionally`, `moreover`, `that said`, `that being said`, `with that in mind`, `it is also worth mentioning`, `on top of that`

5. **Em dashes.** None, anywhere. Also no en dash used as one.

6. **Tools he does not have.** `FEA`, `finite element`, `CFD`, `computational fluid`, `NX`, `Teamcenter`, `ANSYS`, `AutoCAD`, `Revit`, `BIM`, `Creo`, `welding`, `welded`, `weld`. Naming one to deny it is allowed and often better than silence. Claiming one, or hedging toward it, is not.

7. **Numbers.** Every figure in the letter must be one of these, or verified from the posting and called out in the reply:

   `2`, `6`, `20`, `45`, `50`, `0.1`, `0.5`, `16%`, `20%`, `20+`, `280`, `50+`, `85%`, `2026`, `2027`, `2028`

8. **Attribution.** The 50+ precision measurements and the 0.5 mm model belong to the ratcheting screwdriver project. Never to Kelvin.

9. **Tense.** No present-tense sentence about Kelvin Thermal Technologies. That internship ended August 2026.

10. **Certifications.** CSWA is the only one on file. Anything else asserted as a certification needs checking before it ships.

11. **Rule of three.** At most one three-item list in the letter. Two is a pattern.

12. **Rhythm.** Read the paragraph word counts. If they are all within about 15% of each other, or every paragraph lands a number, the letter has a metronome and needs a short paragraph.
