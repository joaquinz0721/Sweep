# Voice DNA

The anti-slop rulebook. Ported from `santifer/career-ops` (`voice-dna.template.md`,
MIT), with Tier 2 rewritten for Joaquin's register.

**The enforceable lists live in `config/banned.json`, not here.** This file is
why. `scripts/check_letter.py` reads the JSON; edit that file when a rule
changes, and this one only when the reasoning does.

---

## Two tiers

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
2. `references/profile.md`, his own layer
3. Tier 1 here
4. Tier 2 here, then everything else

His layer wins over this file. If he adopts a habit that contradicts a rule
below, the rule is what changes.

---

## Tier 1: what marks text as machine-written

### Dead vocabulary

Roughly 90 words in `config/banned.json` under `dead_vocabulary`. These are
statistically overrepresented in LLM output; they are the fingerprint. One is
enough to fail a draft. The worst offenders for an engineering letter:
*leverage, robust, seamless, innovative, spearheaded, facilitated, meticulous,
passionate, cutting-edge, showcase, foster, testament, best practices, proven
track record.*

Also banned: **"serves as", "stands as", "marks a", "represents a"** when used
to dodge "is". Just say *is*.

### Dead phrases and mechanical transitions

*"It's important to note", "in order to" (say "to"), "at the end of the day",
"moving forward", "in other words".* And the openers we already banned: *"I am
writing to express", "I am pleased to", "I am excited to".*

Transitions: *furthermore, additionally, moreover, that said, with that in
mind.* Let the sentences sit next to each other. If two sentences need a
connector to relate, the second sentence is in the wrong place.

### Negative parallelism, the big one

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

### Puffery and significance inflation

*"A pivotal moment", "marking a significant shift", "setting the stage for".*
State the fact. The reader decides whether it is significant. In a cover letter
this shows up as inflating a summer internship into a transformation; the yield
number is impressive on its own and gets less so the moment it is described as
impressive.

### The rule of three

*"speed, efficiency, and innovation."* Three adjectives, three short phrases,
three items, every time. It makes thin analysis look complete.

**Use two. Or four. Or the one that matters.** One three-item list in a letter
is fine and often natural. Two is a pattern. The checker warns at two.

### False ranges

*"From prototyping to production."* If there is no meaningful middle ground
between the two ends, the range is decoration. Name one thing instead.

### Elegant variation

The repetition penalty pushes a model to swap terms: a company becomes "the
firm", then "the organization", then "the employer". **Use the name again.**
Forced synonyms read worse than repetition. This applies hard to company names
in a letter, where the swap reads as though the writer forgot who they were
writing to.

### Participle padding

*"...highlighting my commitment to quality", "...underscoring the importance
of", "...reflecting broader trends in".* An "-ing" clause bolted to a sentence
to manufacture depth. Delete it. If the analysis matters it deserves a sentence
with a claim in it.

### Metronome rhythm

Every sentence the same length, every paragraph the same number of sentences,
even pacing throughout. Machine text has no texture.

This is the rule our old five-paragraph spec broke by design, and it is a large
part of why the IMEG letter read as AI. Real writing breathes unevenly. Short.
Then longer. Then one that earns its length because the thought needed the room.

`check_letter.py` measures the spread of paragraph and sentence lengths and
warns when it goes flat.

### Collaborative leakage

*"I hope this helps", "Certainly", "Great question", "Would you like me to".*
These belong in chat. They must never reach a document.

---

## Tier 2: Joaquin's register

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

## Frequency labels

Every rule carries a weight. Applying all of them as absolutes is what produced
the stiff, formulaic output in the first place.

- **HARD RULE.** Never violate. Everything in `config/banned.json`, the em dash
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

## The litmus test

Before the doc gets built, read the draft once and ask:

> **Does this sound like something Joaquin would actually write, or does it
> sound like an AI trying very hard to imitate him?**

If it feels forced, pull back. The checker catches patterns. This catches the
thing the checker cannot.
