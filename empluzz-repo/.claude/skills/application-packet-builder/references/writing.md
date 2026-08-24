# Writing for the reader on the other end

Recruiter-side heuristics, keyword mirroring, and ATS rules. Adapted from
`santifer/career-ops` (`modes/_writing.md`, `modes/heuristics/recruiter-side.md`,
MIT).

Applies to cover letters, essays, form answers and follow-ups. It does not apply
to sweep reports or anything internal.

---

## The risk map

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

## The six-second gate

A first reader gives the top third of the page about six seconds. In that space
it must be impossible to miss:

- the role he is applying for,
- the strongest matching thing he has done, with its number,
- and that it was real work with a real outcome.

If a reader has to assemble his fit from scattered sentences, the opening
paragraph is wrong. Rewrite it before touching anything else.

## Sentence shape for evidence

The pattern that works: **action, then the thing acted on, then the method, then
the outcome.**

- "Raised assembly yield from 20% to 85% across 6 build iterations by reworking
  the fixturing."
- "Cut 45 minutes from a 280 minute build, about 16%, with custom assembly
  fixturing."

Weak starts to avoid when a stronger truth is available: *helped, assisted,
supported, was responsible for, worked on, participated in, had the opportunity
to.* He did the thing. Say he did the thing.

## Keyword mirroring

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

## ATS reality

Optimize for parsing and for a human, not for tricks.

- Exact posting keywords only where they are true.
- No hidden text, no white font, no keyword stuffing, no decorative layout.
- No skill or number that is not in `config/profile.json`.
- The Google Doc house format parses cleanly already. Do not add tables, columns,
  text boxes or images to a letter.

## What never goes in a letter

- A wage or salary figure, ever.
- A tool from the `do_not_claim` list.
- A number that is not on his resume, unless it was verified from the posting and
  passed to the checker with `--allow`.
- A sentence that would be equally true in a letter to a different employer.
