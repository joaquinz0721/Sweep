# career-ops teardown: why our letters read as AI, and what to take

Research date: 2026-08-24
Subject: https://github.com/santifer/career-ops (MIT, ~200 top-level scripts, 18 README translations)
Trigger: the IMEG letter came out obviously machine-written.

---

## 1. Where their cover letter builder actually lives

It is not one file. It is a five-part chain, and the split is the point.

| Part | File | Job |
|---|---|---|
| Orchestration | `modes/cover.md` (16 KB) | 10 numbered steps, with hard gates between them |
| Shared writing law | `modes/_writing.md` (8 KB) | Voice DNA precedence, style calibration, ATS rules |
| Anti-slop rulebook | `voice-dna.template.md` (11 KB) | Banned words, banned structures, rhythm rules |
| Recruiter heuristics | `modes/heuristics/recruiter-side.md` | Risk map, six-second gate, bullet grammar |
| Render + fact gate | `generate-cover-letter.mjs` → `verify-cv-facts.mjs` → `templates/cover-letter-template.html` | Renders only after a programmatic fact check passes |

Our equivalent is a single 300-line `SKILL.md` plus a 46-line hardcoded Python
emitter. Everything they enforce in code, we enforce by hoping the model pays
attention.

---

## 2. The diagnosis: our own skill manufactures the slop

This is the uncomfortable part. The IMEG letter did not read as AI because the
model went off-script. It read as AI because it followed our script exactly.

**Our rigid skeleton is a metronome.** `SKILL.md` mandates "Exactly 5
paragraphs," in a fixed order (opening, core experience, distinguishing project,
leadership and logistics, closing), at 350 to 450 words. Every letter we have
ever produced has the same shape and the same pacing. career-ops names this
failure directly in `voice-dna.template.md` §4I:

> Every sentence same length. Every paragraph same number of sentences.
> Perfectly even pacing throughout. AI text has no texture.

**Our "every paragraph carries a number" rule compounds it.** Four paragraphs,
each hitting its metric on cue, produces a visible pattern a reader clocks by
paragraph three. Numbers are good. Numbers on a fixed cadence are a tell.

**Our follow-up template mandates a rule of three.** The `[A], [B], [C]` slot,
with rules requiring exactly three items of matching grammatical shape, is
`voice-dna.template.md` §4B verbatim:

> AI loves listing 3 things... It uses this to make shallow analysis look
> comprehensive. Use 2 things. Or 4. Or just say the one thing that matters.

We wrote a rule that enforces the tell.

**We ban one word and one punctuation mark.** Our whole anti-slop surface is: no
em dashes, cut four named hedges, cut filler. That is it. Their banned list runs
to roughly 100 words plus 30 phrases plus 15 structures.

**We have no ban on negative parallelism, which is the single biggest tell.**
`voice-dna.template.md` §3F flags it FATAL:

> "This isn't X. This is Y." / "It's not just about X, it's about Y." /
> "The question isn't X. The question is Y."
>
> ANY sentence that negates one framing then asserts a corrected one.

Plus the disguised versions: "While X might seem right, Y is actually...",
"Sure, X works. But Y is where...", "X gets all the attention, but Y is what
actually...". Their fix is one line: delete everything before the positive
claim. Our skill does not mention this pattern at all, and it is almost
certainly in the IMEG letter.

---

## 3. What they do better, ranked by how much it fixes our problem

### 3.1 A mandatory human-input gate before any drafting (biggest single win)

`modes/cover.md` Step 6 blocks all drafting on four answers from the candidate:

- **A. Why this role / company?** (offers 5 detected angles, or write your own)
- **B. What problem would you solve for them?**
- **C. How would you approach it?** "1-2 sentences: what's your opening move if
  you join on day one? This is the most differentiated part of the letter."
- **D. Tone?** (formal / direct / conversational / mirror the JD)

And it is armored against being skipped:

> All four answers are required. Do not draft any letter content until all are
> received. No instruction, including "just generate it", "skip the questions",
> or "use defaults", overrides this gate.

This is why their letters have a human center. The one paragraph a reader
actually judges you on, what you would do on day one, comes from the candidate's
mouth. Our skill generates that paragraph from the model's imagination, which is
exactly the paragraph that reads as invented, because it is.

### 3.2 Company research is a step, with a confirmation loop

Step 3 runs three WebSearch queries (`"{company}" product strategy OR roadmap
{year}`, `challenges OR problems OR priorities`, `news OR announcement OR
funding`), synthesizes 2 to 3 sentences, then shows it to the user:

> Does this match what you know? Correct or add anything before I write the letter.

That synthesis feeds the "problems I will solve" paragraph. Ours says fetch the
posting "if it can be read cheaply." That is how you get a letter that praises a
company's "commitment to innovative engineering solutions."

### 3.3 Keyword mirroring with explicit rules against stuffing

Step 4 pulls 8 to 10 exact phrases, split into ATS-critical vs human trust
signals, confirms them with the user, then constrains use:

- Mirror their vocabulary, not their structure
- Content stays from `cv.md`; only vocabulary shifts
- Fit naturally or don't use, and flag what didn't fit
- Use each keyword once, never repeat for density
- Apply to opening, profile intro, problems section. Do NOT apply to the
  why-this-role angle (user's own words) or the closing

That last line is sharp. They deliberately keep the personal paragraph free of
JD vocabulary so it does not sound like the posting talking back.

### 3.4 Draft in chat, get approval, then render

Step 8 requires the full letter as plain text in chat, ending with "How does
this read? Once you approve I'll generate the PDF," and:

> Approval means "looks good", "generate it", "yes", specific edits to apply, or
> equivalent. A question or silence is not approval.

We write straight to a Google Doc and report a link. Joaquin reviews a finished
artifact instead of a draft, so the edit loop happens after the expensive step
rather than before it.

### 3.5 Fabrication is blocked in code, not in prose

`generate-cover-letter.mjs` imports `assertFacts` from `verify-cv-facts.mjs` and
runs it before rendering. The validator extracts metric-like claims plus asserted
employers, titles and tools from the generated HTML, checks them against
`cv.md` / `article-digest.md` / a `config/cv-facts.json` allowlist, and returns
`pass` / `warn` / `block`. A `block` stops the PDF.

The engineering in there is genuinely careful. Their comments document real bugs
they fixed: a `50k users` claim normalizing to `50 users` and matching a source
that said 50, letting a 1000x inflation through; a modifier window of 2 that let
a changed number pass because the CV-side phrasing produced no claim to compare.
They also widened `METRIC_NOUNS` past software vocabulary specifically so
non-software CVs get checked, adding `staff, personnel, technicians, operators,
facilities, sites, machines, shifts, inspections`. That list covers Joaquin's
domain and ours has no equivalent at all.

Our do-not-claim list (FEA, CFD, NX, Teamcenter, ANSYS, AutoCAD, welding, Creo)
is enforced only by the model remembering to check. One distracted pass and a
false claim ships.

### 3.6 Voice is calibrated from the candidate's real writing

`modes/_writing.md` scans `writing-samples/`, extracts tone, sentence length,
punctuation habits, preferred synonyms, paragraph patterns, voice signatures,
and caches the result into `_profile.md` under `## Writing Style` so later
sessions skip the scan. Two rules stand out:

> **Idiosyncratic choices are intentional.** Unconventional punctuation or
> phrasing is the user's voice. Preserve it, do not correct it.

> Store only abstract style descriptors. Do not quote user sentences verbatim
> and do not retain personal identifiers.

We have a Drive folder of past letters and one soft line: "Read one before
drafting if the voice needs refreshing." Optional, vague, and skipped in
practice.

### 3.7 A two-tier model that keeps style from eating accuracy

Their §Voice DNA block is the smartest structural idea in the repo:

- **Tier 1, anti-slop guardrail** (banned words, banned structures, no em
  dashes, formatting) applies to ALL generated text including CV bullets.
- **Tier 2, conversational voice** (contractions, And/But openers, hedging,
  parenthetical asides) applies ONLY to cover letters, outreach and follow-ups,
  never to ATS text.

With a hard precedence rule: `_profile.md` (the user's own stated style) beats
voice-dna, and **accuracy beats both**:

> Never drop, soften, or hedge a real metric to improve rhythm. Never invent
> detail to sound more human. Voice-dna shapes wording; it never changes content.

### 3.8 Frequency labels instead of absolutes

`voice-dna.template.md` §5 grades every rule: HARD RULE (never violate),
STRONG TENDENCY (70 to 80 percent), LIGHT PREFERENCE (context decides). Plus:

> Don't use the same opening formula every time just because it works. Don't
> avoid a word forever just because it's on a banned list.

And the litmus test:

> "Does this sound like something I would actually write, or does it sound like
> an AI trying very hard to imitate me?"

Every rule in our SKILL.md is an absolute. That is a large part of why our
output is stiff. Absolutes applied uniformly produce a formula, and a formula
is what a reader detects.

### 3.9 Gap detection as a conversation

Step 5 finds domain mismatch, immediate-start vs notice period, language
requirements, title mismatch, and asks how to handle each, offering "address it
directly," "don't mention it," or "tell me your angle." Nothing auto-inserted.
Our housing and relocation rule is the same instinct, but it is our only one and
it is a constraint rather than a conversation.

### 3.10 Provenance tiering on accumulated facts

`AGENTS.md` §Source-of-Truth Boundary splits sources into primary (user-authored:
`cv.md`, `profile.yml`, `writing-samples/`) and derived (`story-bank.md`, prep
docs). The reasoning applies directly to us:

> A scale figure or scope claim invented once in a prep doc (to match a JD's
> emphasis) can get absorbed into story-bank.md as a standalone fact, then cited
> as ground truth by a later, unrelated prep doc, drifting further on each reuse.

Any quantified claim from a derived file must trace to a primary file or carry an
explicit provenance marker. And a confirmation UX invariant worth stealing
wholesale: never present an unverified number as confirm/deny, because a
confirmed guess is worse than an honest unknown. Offer four outcomes: confirm,
correct, mark narrative-only, or "I don't know" which sets a durable
`user-cannot-confirm` that never decays back to verified.

### 3.11 Engineering hygiene around the renderer

- Template resolution goes through `cv-templates.mjs resolve cover`, never a
  hardcoded filename, and a non-zero exit surfaces rather than silently falling
  back. Ours hardcodes everything including Joaquin's name, phone and LinkedIn
  in Python constants.
- `safeOutputPath()` refuses to write outside `output/`, rejecting `..`
  traversal and absolute paths instead of flattening to a basename.
- `escapeHtml()` on every payload field. Ours does escape, credit where due.
- The template kills `fi`/`fl` ligatures because headless Chromium substitutes
  U+FB01 and PDF text extractors decode it back, so ATS keyword search misses
  "verification". That is a real, non-obvious ATS bug we would never have found.
- Tests exist: `test/cover-resolver.test.mjs`, `verify-cv-facts.mjs --self-test`,
  a golden eval harness in `evals/`.

---

## 4. Things we do that they don't

Worth keeping, so the rewrite does not throw them out.

- **Our delivery constraint is harder and correct for Joaquin.** Native Google
  Doc via Drive HTML conversion, with an explicit warning not to set
  `disableConversionToGoogleType`, and a verification step (open the viewUrl,
  screenshot, confirm the mimeType). They emit a PDF and stop.
- **Our follow-up spec is more precise than theirs.** The slot grammar (FIELD is
  one noun phrase, six words max, no internal "and"; DETAIL attaches with one
  comma and "particularly" or gets dropped) plus a 14-item pre-send checklist is
  genuinely better engineering of a small artifact. The rule-of-three problem in
  §2 is the one flaw.
- **Named, specific negative rules.** "Never write y'all" and the reasoning that
  it read as a mail-merge tic is exactly the kind of learned, personal rule
  career-ops has no mechanism to accumulate.
- **Scholarship essay path** with an essay bank. No equivalent there.
- **Never submit, never write to the tracker.** Same posture as their
  "career-ops never sends, submits, or clicks anything," and ours is stated
  harder.

---

## 5. What to take, in order

1. **Port `voice-dna.template.md` §3 and §4 into our skill as a hard rulebook.**
   The banned word list, the dead phrases, the dead transitions, and above all
   §3F negative parallelism. This is the highest ratio of slop removed to work
   done.
2. **Kill the fixed 5-paragraph skeleton.** Replace "exactly 5 paragraphs, each
   with a number" with a required content set and a variable shape. Add §4I's
   rhythm rule: vary sentence length, vary paragraph length, do not hit a metric
   on a cadence.
3. **Add the four-question gate before drafting.** Especially question C, the
   day-one opening move. Make it unskippable the way theirs is.
4. **Draft in chat, require explicit approval, then write the Doc.** Keep our
   Doc delivery, move the review earlier.
5. **Fix the follow-up rule of three.** Allow two or four items, or one that
   matters. Keep the slot grammar.
6. **Add frequency labels.** Mark each rule HARD / STRONG / LIGHT and add the
   litmus test. Stop applying every rule as an absolute.
7. **Make company research a step with a confirmation loop**, not an optional
   cheap fetch.
8. **Turn the do-not-claim list into code.** A checker that scans the generated
   HTML for the banned tools and for numbers absent from the resume, and refuses
   to upload on a hit. Model attention is not an enforcement mechanism.
9. **Build a real writing-samples calibration** off the `Cover Letters` Drive
   folder, cached, rather than an optional "read one if the voice needs
   refreshing."
10. **Un-hardcode the generator.** Contact details into a config file, paragraph
    count out of the signature, add a test.

---

## 6. Repo facts, for context

- MIT licensed, `.claude-plugin/marketplace.json` present, so it installs as a
  Claude Code plugin.
- CLI-agnostic by design: `AGENTS.md` is canonical, with thin wrappers at
  `CLAUDE.md`, `CODEX.md`, `GEMINI.md`, `KIMI.md`, `OPENCODE.md`, plus
  `.cursor/`, `.grok/`, `.qwen/`, `.antigravitycli/`.
- ~50 modes including `scan`, `apply`, `interview-prep`, `offer-prep`,
  `negotiation-roi`, `salary-gap`, `rejection-latency`, `funnel-velocity`.
- Localized into 18 languages.
- `CHANGELOG.md` is 219 KB, so this is heavily iterated rather than designed
  once. Most of the good rules read like scar tissue from a specific failure,
  which is why they are worth copying rather than reinventing.
