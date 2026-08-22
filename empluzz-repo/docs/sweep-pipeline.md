# The sweep pipeline

Designed and tested 2026-08-22. This replaces the Cowork scheduled tasks, which could
never publish, and it retires the paste-ingest design in `MEMORY.md` section 1.

## The shape of it

```
  Opus orchestrator (this session)
        |
        |  Agent tool, model: sonnet
        v
  internship-sweep  /  scholarship-sweep          .claude/agents/*.md
        |            Sonnet 5, no Artifact tool, no Write tool
        |            searches, scores, writes ONLY a payload
        v
  payload.json
        |
        |  python3 dashboard/ingest.py payload.json          <- preview, writes nothing
        |  python3 dashboard/ingest.py payload.json --apply  <- edits the HTML
        v
  dashboard/application-command-center.html
        |
        |  dashboard/verify/run.sh                           <- 41 assertions
        v
  Artifact publish, by the ORCHESTRATOR only
        |
        v
  git commit, same file, so repo and live page never drift
```

The point of the split: **the sweep never publishes and never edits the dashboard.** It
emits data. Everything that can corrupt the board is a hard error in `ingest.py` rather
than a silent mistake in a 900-line HTML file. The orchestrator is the only thing holding
the artifact's baseVersion, which is what the self-publishing page demands.

This is why the old architecture failed and this one does not. Cowork could not publish,
so the sweeps were built to attempt a publish and then report failure. Here nothing needs
Cowork to publish, because the surface that publishes is the one that already can.

## Running it

```
Run an internship sweep. Write the payload to /tmp/sweep-int.json.
```

The orchestrator spawns the agent, gets the payload back, then:

```bash
cd dashboard
python3 ingest.py /tmp/sweep-int.json                 # read the preview, check the counts
python3 ingest.py /tmp/sweep-int.json --apply
ACC_CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome ./verify/run.sh
```

Then publish, passing the artifact URL and the favicon, never `force`, never a
`capabilities` object. Then commit the same file.

Both sweeps can run at once. They touch different arrays and `ingest.py` takes one payload
at a time, so merge them in two calls rather than one.

## What `ingest.py` refuses

Each of these is a real failure mode that has cost a session before, or that the
standing rules forbid outright. All are tested.

| Refusal | Why |
|---|---|
| A new row whose slug already exists | Rows are never consolidated. Changing an existing row goes through `patch`. |
| A row with no slug, or a slug that is not `[a-z0-9-]` | Applied ticks are keyed on the slug. No slug means the tick orphans. |
| A patch that changes a slug | Same reason. Slugs are permanent. |
| A patch targeting a slug not on the board | A patch never creates a row. |
| A row with the wrong field count | The 14-field and 13-field shapes are positional. |
| An invalid conviction or status | They drive the sort and the chips. |
| A deadline that is not `YYYY-MM-DD` | Prose dates broke the days-left maths. |
| An em dash or en dash anywhere | Hard rule 4. |
| Anything that changes the ACC-STATE block or the tick count | Hard rule 10. Asserted byte-for-byte after the merge. |
| Malformed JSON | Obvious, but it is the most common agent failure. |

Untouched rows keep their original line text, so a sweep's diff shows only what the sweep
actually changed. A three-change payload produced a seven-line diff in testing.

## Environment findings, tested 2026-08-22

These decide what a sweep agent can actually do. Verified from both the orchestrator and a
Sonnet subagent.

- **`WebFetch` is EGRESS BLOCKED for every job domain.** Greenhouse, Ashby, Built In,
  LinkedIn and Workday all return `EGRESS_BLOCKED` from the network proxy, before the
  request reaches the site. This is not the old `ROBOTS_DISALLOWED` behaviour and it is
  not selective. The sweep agents are therefore defined without `WebFetch` at all.
- **`WebSearch` WORKS**, and is the replacement. It returns a synthesized summary that in
  practice carries the pay range, GPA floor and requirements. A probe on H3X returned
  `$23-37/hr` and the 3.0 GPA floor, both matching what the board already had. It is
  weaker evidence than reading the posting, so rows sourced this way should lean
  `UNCONFIRMED`.
- **Gmail works, but every LinkedIn alert is in TRASH.** A default query returns zero and
  looks exactly like an empty mailbox. The sweep must pass `in:anywhere` or
  `includeTrash: true`. One probe concluded there was no LinkedIn mail at all because of
  this; the mail was there the whole time.
- **There are FIVE alert-creation mails, not four** as `MEMORY.md` section 9 records. The
  fifth is `Mechanical Engineering Intern Summer 2027 in United States`, nationwide scope,
  sent 2026-08-21 03:56 UTC. Two subjects do carry the stray leading tab that section 9
  predicted.
- **Still no recurring digest.** All five are `has been created` confirmations, so the
  digest subject format remains unobserved. Keep the query broad.
- **ZipRecruiter works** and behaves exactly as section 8 describes: page size 5, annual
  salary only, no deadline field, no term scoping.
- **A Sonnet subagent inherits the full MCP tool surface**, including Gmail, ZipRecruiter,
  Indeed, and, importantly, the **Artifact tool**. That is why the agent definitions pin
  an explicit `tools:` list. Do not spawn a sweep as a bare `general-purpose` agent, which
  gets everything including the ability to publish.

## What is still untested

**Whether a scheduled routine inherits this same access.** Everything above was proven in
an interactive cloud session. If a routine-fired session has the same tool surface and the
same artifact access, the sweeps can run unattended on a schedule. If it does not, this
pipeline still works, it just needs Joaquin to start it. That is the next test, and it is
the only thing standing between this design and the one-press version he asked for.
