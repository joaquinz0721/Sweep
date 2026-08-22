# Post-application followup: is it feasible?

Study of 2026-08-22. **Nothing was built, nothing was sent, no contact was researched for a real company beyond the three probes recorded below.** This answers one question: if the dashboard grew a Send email button that fires after an application goes in, how much of that can actually be automated, and where does it break?

The asked-for behavior, restated so it can be measured:

> On button press, find a recruiter or a person at that company, get their email, or failing that their Handshake or LinkedIn profile, and produce a short enthusiastic followup message that is ready to send. One click from the dashboard.

Four capabilities are hiding inside that sentence. They do not have the same answer.

| Capability | Verdict |
|---|---|
| Find a named recruiter at the company | Partly. Roughly one company in three, from web search, never from LinkedIn or Handshake directly |
| Get that person's real email address | **No.** Not reliably, not for anyone. This is the blocker |
| Produce a ready-to-send Gmail draft | **Yes.** Fully supported today, and it stays inside hard rule 1 |
| Message them on Handshake or LinkedIn | **No.** Not from any surface available here, ever |

So the feature is feasible, but not in the shape it was asked for. What is feasible is a two-stage version where the contact is found once and stored on the row, and the button drafts from what is already known. The rest of this file is the evidence and the shape.

---

## 1. Recruiter discovery: partly, and not through the two named sites

### LinkedIn and Handshake are both closed, and for two independent reasons each

Tested live this session from a cloud session in the `Sweep` environment:

```
WebFetch https://www.linkedin.com/search/results/people/?keywords=Kairos%20Power%20recruiter
  -> EGRESS_BLOCKED: Access to www.linkedin.com is blocked by the network egress proxy.

WebFetch https://app.joinhandshake.com/job-search/11252619
  -> EGRESS_BLOCKED: Access to app.joinhandshake.com is blocked by the network egress proxy.
```

The proxy is the first wall and it is the removable one, since an environment's allowed-domains list could name either host. The second wall is not removable:

- **LinkedIn people search requires an authenticated session.** Even allowlisted, an unauthenticated fetch lands on a login wall, and LinkedIn's terms forbid automated collection of profile data. Adding it to the allowlist buys a login page, not a recruiter.
- **Handshake requires CU Boulder SSO.** There is no public API, no connector in the installed set (Gmail, Drive, Indeed, ZipRecruiter, Autosheet, Google Calendar), and the SSO handshake cannot be completed by an unattended session.
- **Hard rule 3 blocks the browser workaround anyway,** and the 2026-08-21 finding stands: browser tools cannot reach into a cross-origin frame, and driving a logged-in Handshake session is precisely the kind of per-cell browser work the cost discipline section exists to prevent.

The Handshake wall has a particular sting: 3 of the top rows on the board are Handshake-sourced, and the recruiter contact on a Handshake posting is often visible **to Joaquin, logged in, in the posting itself.** An agent cannot see it. He can, in about eight seconds.

### What does work: the search index sees the profiles even though we cannot

Search engines index public LinkedIn profiles, so a name arrives through search even when the site itself is shut. Three probes, deliberately spanning company sizes:

| Company | Query | Result |
|---|---|---|
| Kairos Power | recruiter, university recruiting | **Named a talent acquisition person** with a profile URL, plus the generic `careers@kairospower.com` |
| H3X Technologies | recruiter, talent acquisition, people ops | No recruiter. Company page, careers page, one employee profile. A startup with no dedicated recruiter |
| Medtronic | campus recruiter, university relations, Boulder | Nothing usable. Job listings, a competitor's recruiter, a CU job posting |

One hit in three, and the pattern behind it is worth more than the ratio: **mid-size companies have a findable named recruiter; startups have no recruiter to find; giants have a recruiting queue rather than a person.** Medtronic is the nearest MUST APPLY row on the board and it is the case this fails hardest on.

### What never works: the actual email address

The address is never in the search results. What is in the search results is an entire industry of pattern aggregators, RocketReach, LeadIQ, Tomba, ContactOut, NeverBounce, AeroLeads, each publishing a guessed format. For one company the returned snippets disagreed with themselves inside a single answer: `lastname@` at 97.3 percent in one line, `firstinitial.lastname@` and `firstname@` a few lines later. The verified addresses are behind the paywall, which is the whole business model.

**Do not build guessing.** A guessed address does one of three things: bounces, sits in a stranger's inbox, or reaches the right person from a candidate who could not be bothered to get their name right. The third is worse than sending nothing, and it is aimed at exactly the companies he most wants.

Reliable address sources, in descending order of value:

1. **The Handshake posting itself**, which frequently names the recruiter and sometimes their email. Joaquin sees this, an agent does not.
2. **A generic inbox** published by the company, `careers@`, `internships@`, `university@`. Real and verifiable, low reply rate, but honest and never wrong.
3. **A person named in a press release, paper, or conference listing** with a university or company address on it. Occasional, worth catching when it appears.
4. **His own CU network**, alumni at the company. Out of scope for an agent, high value in reality.

---

## 2. The Gmail half: fully feasible, today, no new plumbing

The Gmail connector is connected and enabled. `create_draft` takes `to`, `subject`, `body`, optional `htmlBody`, `cc`, `bcc`, attachments, and returns a draft id and thread id. A draft lands in his Gmail, formatted, addressed, and unsent.

This is the shape hard rule 1 already asks for: **assemble and hand over, he sends.** Drafting is not transmitting. The rule survives untouched, and it should be restated inside whatever gets built, because `send_message` sits one tool away from `create_draft` in the same connector and no future session should ever reach for it.

One caveat for anything that runs unattended: **a routine's fired sessions carry no connectors** unless they are attached at creation, and the trigger tool refused to attach any from this session (`the connectors parameter is not available for this organization`). A routine that drafts email would have to be created from the claude.ai routines UI, where connectors are picked per routine. An interactive session, which is where this feature actually belongs, has Gmail already.

---

## 3. The button: what "one click" can honestly mean

Three architectures, and the differences are real.

### A. Copy a prompt, the Build letter pattern

The proven mechanism already shipping on this dashboard. The button builds a self-contained prompt from the row and copies it; he pastes it into a session; the agent researches, drafts, files. Cost: one paste. Buys: everything, including judgment about whether this company is even worth a cold email.

Note that `window.cowork.runScheduledTask` does not exist in the artifact frame, established 2026-08-21. **Every button on this page is a copy-a-prompt button.** There is no third option where the page silently runs an agent.

### B. The page calls Gmail itself, through the `mcp` capability

A published artifact can declare `capabilities: {mcp: {servers: [{server: "Gmail", tools: [...]}]}}` and call the viewer's connectors with the viewer's credentials. That makes a genuine one-click draft possible with no paste at all. Three things to weigh before anyone reaches for it:

1. **The page has no agent inside it.** It can only send what is already on the row. It cannot research, cannot judge, cannot write a message tailored to a person it has never heard of. Option B is a delivery mechanism, not a solution to section 1.
2. **It requires rewriting the tracker's capability declaration.** Stored today: `{artifact, downloads}`, contract 0.2.11. A non-empty `capabilities` object is a full-set declaration, so anything not restated is revoked, and revoking `artifact` silently breaks tick saving. `CLAUDE.md` currently says never pass the object at all, and that rule exists for good reason.
3. **`mcp` may not exist on contract 0.2.11.** The current runtime contract is 0.2.15. Moving the tracker's contract to reach the capability is a deliberate change to how the live page behaves, on the page that holds his 14 ticks.

If option B is ever attempted, it goes on a **clone page first**, the way the routine-publish probe was done this session. Never first on the tracker.

### C. Two stages, which is what this study recommends

Split discovery from drafting, because they have different success rates and different costs.

**Stage 1, Find contact.** Runs per company, not per row, and only when he asks. A subagent searches, and records one of exactly four outcomes on the row:

- `verified email` plus the source it came from
- `generic inbox` plus the address
- `profile only` plus a LinkedIn or Handshake URL and a name
- `nothing found`

It never guesses an address, and it never writes an address it did not see published somewhere it can cite.

**Stage 2, the button.** Behavior depends on what stage 1 stored:

- verified email or generic inbox: build the message and create the Gmail draft, ready for him to read and send
- profile only: copy the message text to the clipboard and open the profile, since he can paste into LinkedIn or Handshake in ten seconds and no automation can
- nothing found: say so plainly, and offer the generic inbox path

That is one click in the case that matters and one paste in the case that cannot be helped, which is the honest ceiling.

---

## 4. Data model, if it gets built

**Do not add a field to the `INT` and `SCH` row arrays.** They are positional, 14 slots with the slug at index 13, and 48 harness assertions read them. Store contacts the way `applied` is already stored, as a map keyed on slug in the state block:

```js
CONTACTS = { "int-kairos-mech-mfg-intern": {
  kind: "verified" | "generic" | "profile" | "none",
  name: "", email: "", url: "", source: "", found: "2026-08-22"
}}
```

Keying on slug inherits the property the slug was introduced for: a sweep rewording a role title does not orphan the contact.

**Dedupe outreach by company, not by row.** Hard rule 8 says every requisition keeps its own row forever, and H3X holds five. Five rows must never become five emails to the same person in one week. The contact record is per company; the followup log is per company; the button on the second H3X row should say when the first one was already written to.

**Log what was sent.** A `followed: {company: date}` map, so a second application to the same company three weeks later produces a different message rather than a duplicate.

---

## 5. The message itself

The template in the request is right in shape and thin in substance. It says nothing a hundred other applicants could not send, and his voice rules already solve that: lead with evidence, not intent; carry one real number; cut any sentence that would be equally true about another company. Length 90 to 130 words for an email, shorter for a LinkedIn note, which caps around 300 characters unless connected.

One policy question that needs his answer, since the rules do not settle it: **hard rule 7 keeps numbers off LinkedIn.** A LinkedIn direct message is not an indexed public page, but it is on LinkedIn. Either the rule extends to DMs, in which case the LinkedIn variant runs without figures and leans on the project names, or it does not, in which case say so once and the variant can carry one number. Until he answers, the safe reading is the strict one: **no figures in a LinkedIn message.**

Timing: send within 24 to 48 hours of the application while the requisition is still being screened, one contact per company, and never a second message to someone who did not reply.

---

## 6. Verdict

**Feasible, in the two-stage form, and worth building after the plumbing question settles.** The email half is solid. The button half is proven mechanism. The research half returns a usable contact for maybe a third of companies and a generic inbox for many of the rest, which is worth having as long as the failure modes are visible on the row rather than hidden behind a guessed address.

**Not feasible as literally asked.** LinkedIn and Handshake cannot be searched, read, or messaged from here, and no verified email address can be found for a named person without a paid data provider. Anything that appears to do those things is guessing, and guessing wrong is worse for him than staying quiet.

Not started, per instruction. This file is the study.
