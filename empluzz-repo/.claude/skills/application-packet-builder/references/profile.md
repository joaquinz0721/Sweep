# Joaquin's layer

**This file is his. Nothing auto-updates it, and it outranks every generic rule
in the skill.** Where this file and `references/voice-dna.md` disagree, this file
wins. Where this file and something Joaquin says in the conversation disagree, he
wins and this file gets updated afterward.

Facts a script needs live in `config/profile.json`. Judgment lives here.

---

## Who is writing

CU Boulder, Mechanical Engineering, graduating May 2028. Targeting Summer 2027
internships. A college senior writing to engineers, not an executive writing to a
board. Every register decision follows from that.

## Target roles

| Archetype | What the posting is buying | What he leads with |
|---|---|---|
| **Manufacturing / process engineering** | Someone who can move a real number on a real line | Yield 20% to 85% over 6 build iterations, the 2 SOPs, the fixturing |
| **Mechanical design / prototyping** | Someone who models a part that can actually be made | SolidWorks depth plus the fact that he machines what he draws |
| **Thermal** | Someone who has been near thermal hardware | Kelvin vapor chamber work, plus or minus 0.1 mm across builds |
| **Test / metrology / quality** | Someone who measures carefully and writes it down | 50+ precision measurements on the screwdriver teardown, modeled under 0.5 mm |
| **MEP / building systems** | Usually AutoCAD and Revit, which he does not have | SolidWorks depth, the additive and thermal work, and the process discipline. See the gap play below. |

## Adaptive framing

Same three experiences, different order depending on what the posting buys
first. Never a different set of facts.

- **Kelvin Thermal Technologies**, summer 2026, past tense always. The yield
  number, the fixturing time saved, the tolerance, the SOPs.
- **Ratcheting screwdriver teardown**, his own time. The measurement discipline
  and the modeling. **The 50+ measurements belong to this project, never to
  Kelvin.** Misattributing it is the single most common error in our letters and
  the checker blocks on it.
- **Compressed-air wobbler engine**, 6 parts, mill and lathe. Proof he can make
  a thing, not only draw one.
- **Peer Leader**, 20+ first-year students. Explaining a decision to somebody who
  has not seen the constraint yet, which is most of engineering communication.

## The narrative underneath every letter

He spent a summer closing the gap between a drawing and a part that goes
together, and he wants another one. That is the through line. The independent
projects are evidence he does this when nobody is paying him, which is the
argument a student can make that a professional cannot.

## The gap play

Postings ask constantly for tools he does not have. The full list is
`do_not_claim` in `config/profile.json` and the checker blocks on every one of
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

## Awards

Name one only when it maps to the role. Listing awards that do not connect reads
as padding.

- **Clinton J. Helton Manufacturing Scholarship**, SME Education Foundation.
  Belongs in any manufacturing, production or process engineering letter; it is a
  manufacturing-specific award from the manufacturing engineering society, which
  is exactly the point.
- **CU Esteemed Scholars Hale award.** Academic merit, use sparingly.
- **Opportunity Next Colorado** and **Hispanic National Merit recognition.** Only
  on a direct match.

## Location and housing

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

## Learned voice rules

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

## Voice calibration

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
`references/voice-dna.md`.

## Scholarships

Swap the letter for essay drafts. Pull from the essay bank named in the
dashboard's `PROF` array (`Scholarship Q's`, `Scholarship Responses`) and
**adapt, do not regenerate.** Flag any prompt with no match in the bank rather
than writing cold. Essays follow the same delivery rule: a formatted Google Doc
in the Packets folder, never chat text only.
