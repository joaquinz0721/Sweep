# Post-application follow-up

A short message to a recruiter or an engineer at a company Joaquin has **already
applied to**. Roughly 80 words, sent by email, LinkedIn or Handshake.

**This is not the "message to the hiring team" variant**, which is 250 to 320
words and replaces a cover letter. This is a four sentence note sent after the
application is in. Do not conflate them.

Background, including the two broken outputs this spec was written to prevent, is
in `docs/followup.md`.

---

## Absolutes

1. **Never send it.** Draft only. Joaquin sends.
2. **Never "y'all", "yall", or "ya'll".** Removed permanently.
3. **No em dashes.** Tier 1 of `references/voice-dna.md` applies in full here,
   banned vocabulary included.
4. **No numbers of any kind.** No yield figures, no cycle times, no tolerances,
   no dates, no wage. A follow-up may land on LinkedIn or Handshake, and resume
   numbers stay off public surfaces. The experience items carry the weight
   instead. `check_letter.py --kind followup` blocks on any digit.
5. **Never claim** anything on the `do_not_claim` list in
   `config/profile.json`. SolidWorks is his CAD.
6. **Kelvin Thermal Technologies is past tense.**
7. **Name the company.** A follow-up that never names the employer is a form
   letter.

## The template

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

## Slot rules

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
  `references/voice-dna.md`). Two items, chosen because they are the two the
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
  `references/voice-dna.md`.

**[First name]**

- If no contact name is known, drop the greeting line entirely and open on
  sentence 1.
- Never "Dear Hiring Manager" here. This is a message, not a letter.

## Sentence rules

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

## Before handing it over

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

## Delivery

- **Plain text in the chat reply**, so he can paste it straight into LinkedIn or
  Handshake. This is the one deliverable in this skill allowed to be chat text;
  the Google Doc rule applies to letters and essays, not to follow-ups.
- **A Gmail draft as well**, only when a real email address is known and he has
  asked for one. Draft only. Never send.
- **Never filed in the Packets folder.** That folder is for cover letters and
  essays.

## Worked example

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
