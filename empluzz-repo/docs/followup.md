# Post-application follow-up, the background

**The canonical rules live in `.claude/skills/application-packet-builder/references/followup.md`.** If this file and the skill ever disagree, **the skill wins.** Anyone changing the format changes the skill first, then updates this file to match. This file is the record of why the format is what it is; it is deliberately not a second copy of the rules, because two copies drift.

A follow-up is a short message to a recruiter or an engineer at a company Joaquin has already applied to. Roughly 80 words, four sentences, sent by email, LinkedIn, or Handshake. It is not the "message to the hiring team" variant, which is 250 to 320 words and replaces a cover letter.

---

## Where the format came from, and why it had to be written down

Until 2026-08-24 the only place this format had ever been written down was one inline `Ie:"..."` example inside a nested bullet in a Google Doc called SWEEPER TODO LIST. It was not in the skill, not in `CLAUDE.md`, not anywhere in this repo, and not in any blob in any commit in this repo's history. All of those were checked.

One example sentence with no rules attached is not a spec. A generator handed one example copies its surface and has nothing to fall back on when the content does not fit, which is exactly what happened.

---

## The two broken outputs. BEFORE, do not reproduce these

These are the actual generated messages, quoted verbatim. They are here as evidence of the five defects below, and as the thing the current spec exists to prevent. **Neither of these is a model to copy.**

**BEFORE, Kairos Power:**

> I just applied to the Mechanical and Manufacturing Engineering Intern role and wanted to reach out to express my sincerest enthusiasm. I'm very interested in the work y'all are doing in advanced nuclear, and getting a new reactor design built as real hardware and I believe this role is an incredible fit for my experience in prototype build iteration, SolidWorks and GD&T, and raising process yield. Thank you in advance for your consideration.  Joaquin Zarazua

**BEFORE, Western Digital:**

> I just applied to the Summer 2027 Hardware Engineering Intern role and wanted to reach out to express my sincerest enthusiasm. I'm very interested in the work y'all are doing in data storage hardware, and at the Longmont site in particular and I believe this role is an incredible fit for my experience in thermal management for electronics, precision prototype builds, and LabVIEW test setups. Thank you in advance for your consideration.

---

## Why the old template broke, five defects

**1. The clause junction is invisible.** The template joined two independent clauses with a bare "and" and no comma. That survives only while the field slot stays two or three words long. Both outputs overfilled it, so the reader hits "as real hardware and I believe" with no boundary to land on. Four instances of "and" inside one 45 word sentence.

**2. Coordinated items of different grammatical types.** "in advanced nuclear" is a prepositional phrase built on a noun. "getting a new reactor design built as real hardware" is a gerund clause. The template coordinated them as though they were parallel. Western Digital has the same fault: "in data storage hardware" set against "at the Longmont site in particular".

**3. The three item experience list is not parallel, and it hides a nested "and".** "prototype build iteration" is a noun phrase, "SolidWorks and GD&T" is two items pretending to be one, and "raising process yield" is a gerund. Three items, three different shapes, and a fourth item smuggled in on a conjunction.

**4. Neither message names the company.** The word Kairos never appears in the Kairos message. The words Western Digital never appear in the Western Digital message. A follow-up that never names the employer is a form letter, and it reads as one.

**5. `y'all` is a frozen literal, and the sign-off is unpinned.** The same word sat in the same slot in every message, which is the tell of a mail merge rather than a person. The closing was inconsistent too: one message ends with a double space and his name run on after the closing sentence, the other ends with nothing at all.

**`y'all` is out permanently.** Not a variable, not an option, not a channel-dependent choice. Removed from the template.

---

## Before and after

### Kairos Power, Mechanical and Manufacturing Engineering Intern

**BEFORE, broken:**

> I just applied to the Mechanical and Manufacturing Engineering Intern role and wanted to reach out to express my sincerest enthusiasm. I'm very interested in the work y'all are doing in advanced nuclear, and getting a new reactor design built as real hardware and I believe this role is an incredible fit for my experience in prototype build iteration, SolidWorks and GD&T, and raising process yield. Thank you in advance for your consideration.  Joaquin Zarazua

**AFTER:**

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

### Western Digital, Summer 2027 Hardware Engineering Intern

**BEFORE, broken:**

> I just applied to the Summer 2027 Hardware Engineering Intern role and wanted to reach out to express my sincerest enthusiasm. I'm very interested in the work y'all are doing in data storage hardware, and at the Longmont site in particular and I believe this role is an incredible fit for my experience in thermal management for electronics, precision prototype builds, and LabVIEW test setups. Thank you in advance for your consideration.

**AFTER:**

```
Hi [First name],

I just applied to the Summer 2027 Hardware Engineering Intern role at Western Digital and
wanted to reach out to express my sincerest enthusiasm. I'm very interested in the work
Western Digital is doing in data storage hardware, particularly at the Longmont site. I
believe this role is an incredible fit for my experience in thermal management for
electronics, precision prototype builds, and LabVIEW test setups. Thank you in advance for
your consideration.

Joaquin Zarazua
```

---

## What changed and why

| Old | New | Why |
|---|---|---|
| Sentence 2 carried the field, the site detail, and the fit claim | Field and optional detail in sentence 2, fit claim alone in sentence 3 | The junction was a bare "and" with no comma. It disappeared the moment the field slot grew past three words. |
| `in advanced nuclear, and getting a new reactor design built as real hardware` | `in advanced nuclear, particularly turning a new reactor design into real hardware` | A prepositional phrase and a gerund clause were coordinated as though parallel |
| `prototype build iteration, SolidWorks and GD&T, and raising process yield` | `prototype build iteration, SolidWorks modeling, and process yield improvement` | Three different grammatical shapes, plus a nested "and" hiding a fourth item |
| `the work y'all are doing` | `the work Kairos Power is doing` | y'all is out permanently, and the employer was never named in either message |
| Name missing, or run on after the closing with a double space | Name on its own line, no trailing period | It was inconsistent between messages and unpinned in the template |

---

## Not built yet

Nobody should assume any of this exists.

- **Recruiter and contact lookup on LinkedIn and Handshake. Not built.** There is no route that finds a named contact for a row. `[First name]` is filled in by hand, or the greeting line is dropped entirely.
- **A per-row Follow-up button on the dashboard. Not built.** It needs a route 0 publish and it is its own job. The prompt that ships it is `prompts/followup-button.md`; the button itself does not exist on the live board.
- **Channel choice. No primary channel has been picked.** Email, LinkedIn and Handshake are all in play and none has been chosen as the default. Write to the normal length; Joaquin trims for LinkedIn himself if he has to.

## Drafts on record

There are **zero Gmail drafts** in the account. The two broken messages above were generated in chat on the day and were never saved anywhere, which is why they are quoted here rather than linked.
