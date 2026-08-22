# Desk sitting checklist, 2026-08-21

> **STATUS: MOSTLY SPENT.** Steps 1, 2 and 5 ran and their results are recorded inline below and folded into `docs/MEMORY.md`. Step 3 is superseded by the move to cloud routines. Step 4, ZipRecruiter, was later completed and its observed schema is in `MEMORY.md` section 8. Kept for the reasoning, the LinkedIn alert table, and the observe-then-write discipline, which still applies to any new source.

Written by the cloud session that read `MEMORY.md` and `source-expansion-scoping.md`. Nothing has been changed yet, because all four items are gated on Joaquin being at the machine. This doc is what to do at the desk, in the order that actually works.

---

## What this session verified from here

Three things, all checked live, none guessed.

1. **The network allowlist is still not set.** `WebFetch` on the tracker URL returned the block on `da80ff29-...frame.claudeusercontent.com`. So a session still cannot read the page or `data/applied.json`. Everything in `MEMORY.md` section 1 is still current.
2. **ZipRecruiter is not installed.** Registry says `installState: not_installed`, `isAuthless: true`, exactly one tool, `search_jobs`. Matches the scoping doc. It cannot be installed from a cloud session; Joaquin has to connect it.
3. **There are zero LinkedIn emails in the Gmail account.** A search for anything from `linkedin.com` in the last 90 days returns nothing at all, not just no job alerts. Gmail itself is connected and answering. See step 5, this raises a question worth settling first.

Also confirmed: `list_triggers` returns empty, so both sweep tasks really are desktop-local and their prompts have to be edited in the desktop app by hand.

---

## One change to the order

The prompt asked for allowlist second. Do it **first**, for two reasons.

- The tick test in step 2 is more useful after the allowlist is on. Once it is on, a fresh session can read `data/applied.json` directly and confirm the save server side, instead of relying on eyeballing two screens.
- The repointed sweeps in step 3 will publish to the hosted artifact. Publishing hits the stale-read guard, which wants a `WebFetch` that currently cannot succeed. If the sweeps are repointed while the block is still up, the first run of each one walks straight into that guard and either fails or needs `force: true`, which is exactly the thing `MEMORY.md` says not to reach for casually.

Working order: allowlist, tick test, repoint sweeps, ZipRecruiter, LinkedIn.

---

## Step 1. Allowlist `*.frame.claudeusercontent.com`

**Corrected 2026-08-21 after reading the actual docs.** The earlier version of this section was vague about where the setting lives and overcautious about what it costs. Both are fixed below.

**It is not in claude.ai account settings.** Personal cloud environments have no settings page and no direct URL. The only way in is the environment selector:

1. In the desktop app, or at claude.ai/code, find the **cloud icon** in the row directly above the message box. Click it.
2. A menu opens with a Local section and a Cloud section. **2026-08-21: there is no existing cloud environment listed, only "Create environment".** So click **Create environment** rather than looking for a gear. The gear only appears on an environment that already exists.
3. The dialog has four fields: Name, **Network access**, Environment variables, Setup script.
4. Set **Network access** to **Custom**. Four levels exist: None, Trusted, Full, Custom.
5. In **Allowed domains**, one domain per line, add:

```
*.frame.claudeusercontent.com
```

6. **Tick the checkbox "Also include default list of common package managers."** This keeps the entire Trusted default list, so nothing that works today stops working.
7. Save.

**This is a strict improvement, not a tradeoff.** The docs have a paragraph on exactly this: "If sessions in the environment work with artifacts, include `*.frame.claudeusercontent.com` in your list. Claude Code fetches artifact content from that host." The level cannot currently be Full, because Full reaches any domain and the read would not be blocked. So it is on Trusted or on a Custom list missing this host, and either way Custom plus the defaults checkbox plus this one host loses nothing. Ignore the long domain list this doc carried before; it was unnecessary.

Two things worth knowing:

- **MCP connector traffic does not go through this allowlist at all.** Indeed, Gmail and Drive travel through Anthropic's servers, not the session network, so the sweeps' connector calls were never affected by this setting either way.
- **The change applies to new sessions, not running ones.** After saving, the chat you are in keeps its old network config. Start a fresh chat to test.

**How to confirm it worked.** New chat in the empluzz environment: "WebFetch the tracker artifact URL from MEMORY.md and tell me whether you got page content or the allowlist block." Content means it is on.

---

## Step 2. Confirm the applied state actually saves

> **RESULT 2026-08-21: FAILED, then later RESOLVED by a different route.** The chip read "read only here, ticks stay on this device". The files form of `publish` is not available in his view, so applied state was not saving into the artifact. The fix that shipped was the page rebuilding its own source and republishing with `publish(html)`, described in `MEMORY.md` section 3. **14 ticks now save into the artifact and travel laptop to phone.** Phone to laptop is still open, bug 14.

Do this on the laptop, in a normal browser tab, at the tracker URL in `MEMORY.md` section 1.

1. Open it. Before touching anything, read the chip in the header and note what it says.
2. Tick **Marotta Controls**. It is one of only two unapplied internship rows, so it is easy to find and easy to undo.
3. Wait three full seconds. The write is debounced, so a faster read tells you nothing.
4. Read the chip again.
5. Open the same URL on the phone. Fresh load, not a cached tab. Confirm the Marotta row is ticked.
6. Untick Marotta on whichever device, wait three seconds, and confirm on the other. The untick is a second test of the same path, and it puts the board back where it was.

What the chip means:

| Chip text | Meaning | Action |
|---|---|---|
| ticks saved to this artifact | Working as designed. | Nothing |
| ticks not yet saved | Write in flight, or still debouncing | Wait, then reread |
| read only here, ticks stay on this device | The files form of `publish` is not available in his view. | Stop and report the exact wording; the route has to change |
| save failed, ticks kept on this device | The write was attempted and rejected | Open the browser console, copy the error code, report it |

---

## Step 3. Repoint both sweep tasks

> **SUPERSEDED.** The block was never the sweep prompt, it was the surface the sweeps run on. A Cowork scheduled task cannot publish the artifact no matter what its prompt says. The replacement plan is cloud routines pinned to `empluzz`, in `docs/artifact-write-routes.md` door 4b. The block below is kept only because a routine's prompt will need most of the same wording.

```
Write results to the hosted tracker artifact at <TRACKER URL>.
Update it by calling the Artifact tool with `url` set to that exact URL.
Never publish without `url`; publishing without it creates a duplicate tracker
and splits the board in two.
Do not read or write the Google Sheet.
Assign a stable slug to every new row: `int-` or `sch-` prefix, then lowercase
letters, digits and hyphens only. Never change the slug on an existing row;
all applied state is keyed on it.
Write today's date into the Last Checked field of every row you check. The
header's swept stamp is derived from the newest date in CAL, so this is what
keeps it honest.
```

**Note the capabilities wording in the original version of this block was wrong.** It told the sweep to pass `capabilities: {artifact:{}, downloads:true}` on every publish. The correct rule, confirmed twice since, is to **omit `capabilities` entirely**, which carries the stored declaration forward. Do not restate it.

---

## Step 4. ZipRecruiter

> **DONE.** Installed and probed 2026-08-21. Real argument names and result fields are in `MEMORY.md` section 8. The discipline below is why that section exists and should be repeated for any new source.

Connect it from the connector directory in settings. It is authless, so there is no ZipRecruiter account and no login step. After connecting, make sure it is toggled on for the chat you are working in, since a connector can be authenticated at the org level and still switched off in a given chat.

Then say so in chat, and this is the single call that gets made, one call only:

> `search_jobs` for a mechanical engineering internship near Boulder, Colorado.

The point is to read the real request and response, not to get results. What gets recorded into `MEMORY.md` afterward:

- the exact argument names the tool accepts, and which are required
- whether location is a string, a pair of fields, or a structured object
- how salary comes back, and whether it is hourly or annualized, since the Do next score compares against the $26.00/hr Kelvin floor
- whether posting date is present and in what format, since that is what makes an incremental sweep cheap
- the exact field holding the apply URL

No sweep code gets written before that. The filter list in the scoping doc is marketing copy and is not a schema.

After the first two real sweeps, compare unique rows against what Indeed already produced. Under roughly 15 percent unique, ZipRecruiter drops to monthly instead of per sweep.

---

## Step 5. LinkedIn as an email alert source

> **DONE 2026-08-21.** All four alerts created, all four confirmation mails read, and the confirmations carried a first batch of matches that became fifteen deduped postings. Sender and subject formats are in `MEMORY.md` section 9. The recurring digest format is still unknown.

**Settle this.** There is not a single email from LinkedIn in this Gmail account in 90 days. That means one of three things: the LinkedIn account uses a different address, LinkedIn email notifications are switched off entirely, or there is a filter routing them somewhere the search did not reach. Check which, because the whole design depends on the mail landing in `joaquinz0721@gmail.com`.

### The alerts to create

Create each one by running the search in LinkedIn Jobs, setting the filters, then toggling **Set alert** on the results page.

| # | Search terms | Location | Filters | Frequency |
|---|---|---|---|---|
| 1 | mechanical engineering intern | Boulder, Colorado, 50 mile radius | Job type: Internship. Experience level: Internship | Daily |
| 2 | manufacturing engineering intern | Boulder, Colorado, 50 mile radius | Job type: Internship. Experience level: Internship | Daily |
| 3 | mechanical engineering intern summer 2027 | United States | Job type: Internship. Experience level: Internship | Weekly |
| 4 | design engineer intern | United States | Job type: Internship. Experience level: Internship | Weekly |

The split is deliberate. Colorado is daily because volume is low and every hit clears the relocation rule automatically. National is weekly because volume is high.

Four is the right number. More alerts do not widen coverage much and they do make the Gmail read more expensive.

### Make the sweep read cheap

In Gmail, create a filter: from contains `linkedin.com`, subject contains `job`, apply label `job-alerts`, and skip the inbox if the noise is unwelcome. Then the sweep query is one exact label read rather than a fuzzy search.

### The Gmail read, and an honest correction

The scoping doc estimated 1 to 2 tool calls per sweep for this. That is optimistic. `search_threads` returns previews only, roughly the five oldest messages per thread and no message bodies, so the actual postings need a `get_thread` per alert email. Realistic cost is one `search_threads` plus three to six `get_thread` calls per sweep. Still trivially cheap next to 25 to 40 browser round trips, so the recommendation does not change, but the number in the doc should.

First sweep query:

```
from:jobalerts-noreply@linkedin.com newer_than:8d
```

`newer_than:8d` rather than 7 gives an overlap day so a weekly alert never falls between two sweeps.
