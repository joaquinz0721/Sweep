# The followup plan

**How to start this work:** open a fresh session in this repo and say *"go on the followup plan."* Read this file top to bottom before touching anything. It is written for Opus holding the thread, with Sonnet subagents doing the legwork.

| | |
|---|---|
| **Goal** | After Joaquin applies to a role, one button on the dashboard produces a ready-to-send Gmail draft to a real person at that company. |
| **Status** | Planned, not started. Feasibility settled 2026-08-22 in `docs/post-application-followup-feasibility.md`. |
| **Shape** | Two stages. Capture the contact once per company, then draft from what is known. |
| **Hard limit** | Drafts only. He presses send. Hard rule 1 is not bent for this feature. |
| **Est. size** | Four phases, one dashboard publish each. Phase 5 is optional. |

---

## 0. Before you touch anything

Read in this order. All three are in this repo.

1. `docs/MEMORY.md`, the whole file. It overrides this plan wherever they conflict.
2. `CLAUDE.md`, the hard rules. Rules 1, 4, 7 and 8 all bite on this feature.
3. `docs/post-application-followup-feasibility.md`, the study this plan comes from. It contains the evidence for every decision in section 2, so you do not need to re-derive any of it.

Then confirm three things before writing a line of code:

- [ ] The live tracker reads back through the Artifact tool's `read` action. If it does not, stop and report; do not attempt any workaround.
- [ ] The tick count on the live page matches what `MEMORY.md` records. If it does not, say so and stop.
- [ ] `dashboard/verify/run.sh` passes all 48 assertions against the committed build.

---

## 1. What is being built

```
  he applies to a role
          |
          v
  [ row on the dashboard ]
          |
          +--> "Find contact"  ...... copies a research prompt, he pastes it into a chat,
          |                            a Sonnet subagent researches, and it ends by emitting
          |                            a JSON block he pastes back into the page
          |
          +--> "Paste contact"  ..... he types or pastes a recruiter straight in, which is
          |                            the highest quality path, since Handshake postings
          |                            often name the recruiter and only he can see them
          |
          v
  [ contact stored on the page, keyed by company ]
          |
          +--> "Draft email"  ....... verified address or generic inbox: a Gmail draft
          |                            appears, addressed, written, unsent
          |
          +--> "Copy message"  ...... profile only: the message text goes to his clipboard
                                       and the profile opens in a new tab
```

Everything the page stores saves the same way his applied ticks save, through the page's own self-publish. No session is needed for a paste to persist.

---

## 2. Decisions already made

Do not re-litigate these. Each one has evidence behind it in the study.

| Decision | Why |
|---|---|
| Contacts are stored per **company**, not per row | H3X holds five rows. Five rows must never become five emails to one person. Hard rule 8 keeps the rows separate; outreach is deduped above them. |
| **Never guess an email address** | Pattern aggregators contradict themselves. A guess that reaches the right person with the wrong name costs more than silence. |
| Manual capture is **first class**, not a fallback | Handshake postings name recruiters. Joaquin can read them, an agent cannot. He has said he will do the manual step. |
| Gmail `create_draft` only, never `send_message` | Hard rule 1. The send tool sits one call away in the same connector, so say so in every prompt this feature generates. |
| Buttons **copy prompts**, they do not run agents | `runScheduledTask` does not exist in the artifact frame, established 2026-08-21. Every button on this page works this way. |
| The page's `mcp` capability is **out of scope for phases 1 to 4** | Reaching it means rewriting the tracker's capability declaration and probably moving its runtime contract, on the page holding his ticks. Phase 5 only, on a clone first. |
| Figures **are** allowed in a personal message | Settled by Joaquin 2026-08-22. See hard rule 7 as amended. One figure per message, not three. |

---

## 3. Phase 1: the data model and the paste control

**Goal:** the page can hold a contact and he can put one in by hand.

**Deliverable:** one dashboard publish through route 0a.

### The state

`PUB` currently holds `{v:4, updated, applied}`. Take it to `v:5` and add two maps. Both must default to `{}` when absent, so an older build never crashes on a newer page or the reverse.

```js
PUB.contacts = {
  "kairospower": {
    kind:   "verified" | "generic" | "profile" | "none",
    name:   "",              // person, empty for a generic inbox
    email:  "",              // only if seen published somewhere citable
    url:    "",              // LinkedIn or Handshake profile
    source: "",              // where it came from, required, free text
    found:  "2026-08-22"
  }
}

PUB.outreach = {
  "kairospower": [ { date:"2026-08-22", slug:"int-kairos-mech-mfg-intern", channel:"email" } ]
}
```

**The company key** is the company string lowercased with every non-alphanumeric character stripped. Write it once as `coKey(name)` and use it from every reader and writer. Show the resolved key in the paste preview, so a company renamed in a row cannot silently orphan its contact.

### The control

A `Paste contact` panel, opened from the row, with four fields: name, email, profile URL, source. Rules for it:

- Requires **either** an email **or** a profile URL. Neither means nothing to store.
- Requires `source` to be non-empty. A contact with no provenance is a guess.
- Sets `kind` automatically: an address at the company domain is `verified`, an address like `careers@` or `university@` is `generic`, a URL with no address is `profile`.
- Previews what it will write, including the company key and any contact it would overwrite, before it commits.
- Never touches `applied`. Ever.

### The row

A contact chip next to the existing Build letter button, four states, colored through the existing style vocabulary rather than new colors: `verified`, `generic`, `profile`, `none`.

### Acceptance

- [ ] Paste a contact, reload the page, it is still there.
- [ ] Tick count unchanged before and after the publish.
- [ ] `run.sh` extended with assertions for `v:5`, both maps present, `coKey` stability, and the chip rendering for all four states.

---

## 4. Phase 2: Find contact

**Goal:** a button that hands over a research prompt good enough that the answer comes back paste-ready.

**Deliverable:** one publish, plus a new patch script under `dashboard/patches/`.

Model this on `dashboard/patches/build-letter-delegation.js`, which is the worked example of a delegating button in this codebase. Copy its shape: the button builds a self-contained brief from the row and copies it, the prompt tells Opus to spawn a Sonnet subagent, and the subagent starts cold.

The research brief must say, in its own words:

1. **Do not fetch LinkedIn or Handshake.** Both are blocked at the egress proxy and behind auth walls. Tested 2026-08-22. Use web search only.
2. Look for, in this order: a named recruiter or university relations person at the company; the company's published careers or internships inbox; a named engineer or manager on the team, if the company is small enough that no recruiter exists.
3. **Never guess or construct an address.** If an address was not seen published somewhere citable, it does not exist.
4. Return exactly one JSON block, in the shape phase 1 accepts, plus the source URL for every field.
5. Report `kind: "none"` honestly when nothing was found. That is a good answer, and roughly two companies in three will get it.

The prompt ends by telling him to paste the block into the Paste contact panel.

### Acceptance

- [ ] Run it once against Kairos Power, which is known to return a named person plus a generic inbox.
- [ ] Run it once against Medtronic, which is known to return nothing usable, and confirm the subagent says `none` rather than inventing something.

---

## 5. Phase 3: Draft email

**Goal:** the button that finishes the job.

**Deliverable:** one publish.

Behavior depends on the stored `kind`:

| Stored | Button says | What it does |
|---|---|---|
| `verified` or `generic` | Draft email | Copies a prompt that writes the message in his voice and creates the Gmail draft |
| `profile` | Copy message | Copies the message text, opens the profile in a new tab, he pastes and sends |
| `none` | Find contact | Falls back to phase 2 rather than pretending |

The generated prompt must carry his voice rules, the row's facts, and this line verbatim: **create a draft, never send. Do not call `send_message`.**

If `outreach` already holds an entry for this company inside 21 days, the button says so first and asks him to confirm, naming the date and the role it was sent for.

### Acceptance

- [ ] One real draft lands in Gmail, addressed correctly, unsent.
- [ ] A second press for a different H3X row warns about the first.

---

## 6. Phase 4: the log

**Goal:** the board remembers who was written to.

**Deliverable:** one publish, and it can ship with phase 3 if the change stays small.

- Writing a draft appends to `PUB.outreach` under the company key.
- The row shows a quiet `written 3d ago` marker.
- A company written to twice in one week is visibly flagged.

---

## 7. Phase 5, optional: take the paste out

Two ways to remove the last manual step, both explicitly out of scope until phases 1 to 4 are shipped and used for real.

**5a. Contact refresh as a routine.** Proven possible on 2026-08-22: a scheduled routine reads the tracker and publishes to an artifact declaring the `artifact` capability. Evidence in `docs/artifact-write-routes.md`. Such a routine could fill in contacts for rows that have none and publish the result. Note that a routine created from inside a session gets **no connectors**, so it must be created from the routines page on claude.ai if it needs Gmail or Drive.

**5b. The page calls Gmail itself.** The `mcp` capability lets a published page call his connectors directly, which would make the draft appear with no paste at all. Three cautions, all in the study: the page has no agent inside it and can only send what the row already holds; declaring capabilities is a full-set declaration and failing to restate `artifact` silently breaks tick saving; and `mcp` may not exist on the contract the tracker is pinned to. **If this is attempted, it happens on a clone page first**, the way the routine probe was done.

---

## 8. The message

Two variants, both in his voice, both built from the row plus his resume facts.

**Email**, 90 to 130 words. No letterhead, no `Dear Hiring Manager`. Subject names the role and the requisition if there is one.

> Open with the application and the role, one sentence. Then one paragraph that earns the reader's time: the single most relevant thing he has done, carrying one real figure. Then one sentence on why this company specifically, which must not be true of any other company. Close with thanks and his name.

**LinkedIn or Handshake message**, under 300 characters if they are not connected. Same structure, compressed, and **one figure is allowed** per hard rule 7 as amended 2026-08-22.

Non-negotiables, all from `CLAUDE.md`:

- No em dashes anywhere.
- Kelvin Thermal Technologies is past tense.
- Never claim FEA, CFD, NX, Teamcenter, ANSYS, AutoCAD, or Revit and BIM. SolidWorks is his CAD.
- Cut every hedge. No "eager to", no "confident that", no "I am writing to express my interest".

---

## 9. Publishing, every phase, no exceptions

Route 0a, an interactive cloud session, which is proven twice. The full procedure is in `MEMORY.md` section 3. In short:

1. Read the live page with the Artifact tool's `read` action. The read is what sets the tracked base version.
2. Reconstruct on the ACC marker pairs with `dashboard/verify/mkbase2.py`. The read returns the shell's transformed copy, never the authored source, so editing what comes back directly produces garbage.
3. Apply the change as an anchored patch script in `dashboard/patches/`, one change per script.
4. Run `dashboard/verify/run.sh`, all assertions green, **against the payload before it is sent.**
5. Count the applied ticks in the payload. If the count differs from the live page, **refuse to publish** and say so loudly.
6. Publish with the artifact URL and favicon `🎯`. No `force`. No `capabilities` object at all.
7. Read it back. Check the ticks again, and check `markupCounts` from `dashboard/verify/accdoc.js`.
8. Commit the reconstructed build with `mkbase2.py --null-state` and update `MEMORY.md` with the new version slug.

One publish per phase, never one per change.

---

## 10. What not to do

- Do not add a field to the `INT` or `SCH` row arrays. They are positional, 14 slots, slug at index 13, and 48 assertions read them.
- Do not consolidate the five H3X rows. Hard rule 8. Dedupe the outreach, never the rows.
- Do not fetch LinkedIn or Handshake, and do not ask for them to be allowlisted. The proxy is not the only wall.
- Do not build an email-pattern guesser, even as a "suggestion" the user confirms.
- Do not call `send_message`, and do not build anything that could.
- Do not touch the applied ticks, the frozen Google Sheet, or the tracker's capability declaration.

---

## 11. Ask him if you need to

- Which contact he wants preferred when a company has both a named recruiter and a generic inbox. Assume the named person until he says otherwise.
- Whether the 21 day duplicate window is right.
- Whether he wants the followup offered automatically when he ticks a row applied, or only on demand. Assume on demand.

---

*Written 2026-08-22 from the feasibility study of the same date. Nothing in this plan has been built.*
