# Sweep source expansion: LinkedIn and ZipRecruiter

Scoped 2026-08-21. Scoping only, nothing built. This answers next-up item 3 in `MEMORY.md`.

Context for why this matters now: only 2 internships remain active on the board (Marotta Controls and Jacobs, both LATER, both capped by the relocation rule). The internship pipeline is worked out until new postings land, so source coverage is the binding constraint, not packet throughput.

---

## Short version

| Source | Verdict | Cost per sweep | Why |
|---|---|---|---|
| ZipRecruiter | **Turn it on** | About 1 tool call per query, same shape as Indeed | First-party Claude connector, no account needed |
| LinkedIn, via connector | Not possible | n/a | No connector exists, no public jobs API |
| LinkedIn, via Chrome extension | **Do not build** | 25 to 40 round trips | The exact cost pattern the project already banned, plus account risk |
| LinkedIn, via email alerts to Gmail | **Build this instead** | 1 to 2 tool calls | Free, no ToS exposure, Gmail is already connected |

---

## ZipRecruiter

**It is already a first-party connector in the Claude registry.** Made by ZipRecruiter Inc., category Productivity, shipped June 2026. The registry reports `isAuthless: true` and exactly one tool, `search_jobs`. Authless is the important word: no ZipRecruiter account, no OAuth dance, no credential to keep alive. It is currently `not_installed` for this org.

This is the same architectural shape as the Indeed connector already in the sweep, so the marginal cost is understood rather than guessed: one tool call per query, results inline in the response, no browser anywhere.

**Advertised filters:** job title, company, location, salary range, distance, remote or hybrid, employment type, and posting date. Result cards carry salary, location, benefits, and role detail. Posting date and salary matter here specifically: posting date is what makes an incremental sweep cheap, and salary feeds the wage term in the Do next score against the $26.00/hr Kelvin floor.

**What I could not determine, and will not guess.** I have not observed a real `search_jobs` request and response pair, because the connector is not installed in this session. The published docs page at `api.ziprecruiter.com/mcp/docs` is a JavaScript shell with no readable content. So the exact argument names and result encoding are unknown. **The first run must be an observation run:** install the connector, make one call, read the actual shape, then write the sweep against what came back. Do not write sweep code against the filter list above; it is marketing copy, not a schema.

> **Superseded 2026-08-21.** The observation run happened. The real argument names and result fields are recorded in `MEMORY.md` section 8. Use that, not the paragraph above.

**Realistic sweep cost.** Figure 3 to 6 calls to cover the query space he needs: mechanical engineering intern Summer 2027, manufacturing engineering intern, design engineering intern, once for Colorado and once national. Call it 4 calls of a few thousand tokens each. Against a browser sweep that is a rounding error.

**The real risk is not cost, it is overlap.** ZipRecruiter and Indeed both aggregate heavily from the same ATS feeds (Workday, Greenhouse, iCIMS). A large fraction of what comes back will already be on the board from Indeed. Budget for dedupe on company plus normalized role plus location before anything is written to the dashboard, and expect the unique yield to be meaningfully smaller than the raw result count. If the first observation run shows unique yield under roughly 15 percent, the connector is not earning its call and should be dropped back to a monthly rather than per-sweep source.

**One more free option found while looking.** Dice is also in the registry, also authless, also a single `search_jobs` tool. Dice is tech and IT focused, so for a mechanical engineering sophomore the expected yield is close to zero. Skip it.

---

## LinkedIn

### There is no legitimate API route

LinkedIn's official job-related APIs are Talent Solutions, and they are for **posting** jobs, not searching them. Access is partner-gated, granted to ATS vendors and enterprise recruiting platforms under contract. A student cannot obtain it, and there is no public jobs search endpoint at any tier.

The "LinkedIn Jobs API" products that show up in search results are third-party scrapers reselling LinkedIn data. They cost money, their legality is contested, and they violate LinkedIn's terms to varying degrees. Not appropriate here.

Crustdata is in the Claude registry and does expose `crustdata_job_search` and `crustdata_job_search_live` over LinkedIn-derived data, but it is an authenticated, paid B2B sales-intelligence product aimed at go-to-market teams. Wrong tool at the wrong price for one undergraduate's internship search.

### The Chrome extension route is the trap this project already escaped

That leaves driving his logged-in LinkedIn session with the Chrome extension. Two independent reasons not to.

**Cost.** LinkedIn job search is an infinite-scroll single-page app where the result list gives you a title and company, and the actual description lives in a right-hand pane that only populates when you click the card. So a sweep is: navigate, then repeated scroll plus read cycles to materialize a page of about 25 results, then one to two round trips per job that looks worth reading. Realistically **25 to 40 tool round trips for one useful sweep**. `MEMORY.md` records that browser-driven dashboard editing cost roughly thirty round trips per sweep and that the fix was to stop doing it. Rebuilding that cost on the intake side rather than the write side is the same mistake wearing a different hat.

**Account risk.** Automating LinkedIn while signed in as him is against their user agreement and their anti-automation systems are aggressive. The downside is a restriction on the account he actually needs for recruiting, right as he is trying to be visible to engineering employers. That is a bad trade for marginal coverage.

**And the coverage gain is small anyway.** Intern postings from the large engineering employers he is targeting (Medtronic, GE Aerospace, Boeing, BAE, Vertiv, Anduril) are ATS-mirrored and already reachable through Indeed and Handshake. The genuinely unique-to-LinkedIn slice for a Summer 2027 mechanical engineering internship is thin, and it skews toward small firms posting directly, which is exactly the segment least likely to state housing or relocation and therefore capped at STRETCH by the relocation rule regardless.

### The cheap LinkedIn route that does work

**Let LinkedIn push to him instead of pulling from LinkedIn.**

He creates job alerts in LinkedIn's own UI, once, by hand: the searches he cares about, set to daily or weekly email. LinkedIn then emails him new matching postings. The Gmail MCP is already connected to this project. A sweep does one `search_threads` for recent LinkedIn job alert mail, reads the postings out, and scores them like any other row.

- Cost: 1 to 2 tool calls per sweep, plus reading a few emails.
- ToS exposure: zero. This is LinkedIn's own product working as designed.
- Account risk: zero.
- Setup: about ten minutes of his time, none of mine, and it never needs maintaining.

The tradeoff is honest: alerts only surface what LinkedIn's own matching decides to send, so coverage is narrower than a real search, and there is a lag of up to a day. For a search where the constraint is that almost nothing new is posting anyway, that is an acceptable trade at roughly one fortieth the cost.

> **Built 2026-08-21.** Four alerts exist and the sender and subject formats are recorded in `MEMORY.md` section 9. The realistic cost is one `search_threads` plus three to six `get_thread` calls, not the 1 to 2 estimated above.

---

## Recommendation, in order

1. **Install the ZipRecruiter connector and do an observation run.** One `search_jobs` call, inspect the real response shape, record the argument names and result fields in `MEMORY.md`. Then wire it into `internship-sweep---summer-27` behind a dedupe against existing Indeed rows.
2. **Measure unique yield on the first two real sweeps.** Under about 15 percent unique, demote ZipRecruiter to monthly.
3. **Set up LinkedIn email alerts and read them from Gmail.** This is the LinkedIn answer. It is not a compromise version of scraping, it is the correct design.
4. **Do not build LinkedIn browser automation.** Cost and account risk both point the same way.
5. Skip Dice.

Both sweep tasks are stored locally by the Cowork desktop app, so items 1 and 3 require Joaquin at the desktop to edit the task prompts. That is the same blocker as next-up item 2, and the two should be done in one sitting.
