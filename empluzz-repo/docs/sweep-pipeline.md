# Sweep pipeline

**Built 2026-10-07.** This is the procedure the dashboard's **Run Internship Sweep** and
**Run Scholarship Sweep** buttons point at. It runs in a cloud Claude Code session on the
`Sweep` repo (route 0a), because that is the surface that can read and publish the tracker.
A Cowork session cannot publish it, ever; see `CLAUDE.md`.

The pieces:

| Piece | Where | What it does |
|---|---|---|
| Sweep agents | `.claude/agents/internship-sweep.md`, `.claude/agents/scholarship-sweep.md` at the **repo root** | Sonnet. Search, score, write one JSON payload. Never publish, never edit HTML, never `--apply`. |
| Ingest | `empluzz-repo/dashboard/ingest.py` | Validates the payload, previews the merge, and on `--apply` writes it into a build. Refuses the whole payload on any defect. |
| Ingest tests | `empluzz-repo/dashboard/verify/test_ingest.py` | 38 assertions. Run after any change to `ingest.py`. |
| Board harness | `empluzz-repo/dashboard/verify/run.sh` | The 56 assertions every publish already needs. |

Paths below are relative to `empluzz-repo/` unless they start with `.claude/`.

## The procedure

```
fetch -> sweep agent -> preview -> HIS GO -> fresh fetch + full Read -> apply -> verify -> publish -> read back -> commit
```

**1. Fetch for context.** `Artifact` `action:"read"` on the tracker URL, then rebuild:

    python3 dashboard/verify/mkbase2.py <saved file> /tmp/apb/work/sweep-base.html

This copy is only for the agent to read. It is not the publish base.

**2. Spawn the agent on Sonnet.** `internship-sweep` or `scholarship-sweep`, with two
paths in the prompt: `BUILD=/tmp/apb/work/sweep-base.html` and
`PAYLOAD=/tmp/apb/work/sweep-int.json` (or `sweep-sch.json`). If the agent type is not
listed in the session, spawn a general-purpose agent with the model set to Sonnet and
give it the whole of the matching `.claude/agents/*.md` file as its instructions. The agent
runs the preview itself and fixes its own payload until ingest stops refusing.

**3. Preview, and show him.**

    python3 dashboard/ingest.py /tmp/apb/work/sweep-int.json --build /tmp/apb/work/sweep-base.html

Paste the whole preview into the chat, every `+`, `~` and `WARN` line, plus the agent's
best finds. **Wait for his go.** He can drop rows; edit the payload and preview again.

**4. Fresh fetch and full Read, immediately before the publish.** This is the step the
publish gate checks, so it comes after his go and not before. `Artifact` `action:"read"`
again, then `Read` every line of the file it names, as `docs/artifact-publish-runbook.md`
section 0 describes. Then:

    python3 dashboard/verify/mkbase2.py <new saved file> /tmp/apb/work/live-base.html

Ingest is repeatable on purpose: the same payload applies to this fresh base, so any tick
he made while the sweep ran is carried, not lost.

**5. Apply.**

    python3 dashboard/ingest.py /tmp/apb/work/sweep-int.json --build /tmp/apb/work/live-base.html --apply

If it refuses here but passed in step 3, the board changed underneath (usually a slug that
now exists). Tell him; do not hand edit around it.

**6. Verify.**

    cd dashboard/verify && npm install
    ACC_CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome bash run.sh /tmp/apb/work/live-base.html

All 56 must pass. Ingest already refuses to change the `ACC-STATE` block; check the tick
count in the preview line matches the live read anyway.

**7. Publish.** `Artifact` with `file_path` set to the merged build, the tracker `url`, and
the favicon. No `force`, no `capabilities`. If the gate refuses as not viewed, go back to
step 4, not to step 1.

**8. Read back.** Fetch again, rebuild with `mkbase2.py`, and `cmp` against the payload:
it should be byte identical.

**9. Commit.** `mkbase2.py <payload> dashboard/application-command-center-<version>-<tag>.html --null-state`,
point `CLAUDE.md` and `dashboard/README.md` at it, add a line to `docs/MEMORY.md`, push.

## The payload

Named fields, so an agent cannot put a wage in the notes column by miscounting.

    {
      "kind": "int" | "sch",
      "swept": "YYYY-MM-DD",
      "label": "short, goes in the Calendar row name",
      "summary": "what was searched, what answered, what did not",
      "new":    [ { every field for the tab } ],
      "update": [ { "slug": "...", "set": { some fields }, "append_note": "..." } ],
      "screen_out": [ { "name": "...", "role": "...", "reason": "..." } ]
    }

Internship fields: `conviction company role location term deadline source url packet notes status hint wage slug`.
Scholarship fields: `conviction name sponsor award opens deadline gate url packet notes status hint slug`.

Ingest also appends a Calendar row stamped with `swept`, which moves the header's
"last swept" date, and adds Screened Out rows dated `swept`.

**Refused outright:** unknown keys, a missing or empty required field, a conviction or
status the board does not know, a slug that already exists or is malformed or on the wrong
tab, an update to a slug that does not exist or that tries to change a slug, a deadline
that is not `YYYY-MM-DD`, a wage that is not hourly, a non-http url, any em or en dash, a
null-state build, and any merge that would change the `ACC-STATE` block, the tick count,
or the count of any document marker.

**Warned, not refused:** a new row that looks like an existing requisition or a Screened
Out row (never consolidate, but confirm), and an out of state internship whose notes never
state the housing position.

## Guard rails, unchanged since 2026-08-21

Never touch the applied ticks. Refuse to publish if the tick count moved. Refuse rows
without a slug. Refuse malformed JSON. Always preview before committing.

## Still open

- **Routines.** A scheduled routine is a different surface from an interactive cloud
  session and has never been tested against the artifact. Until it is, a sweep is
  something he starts, not something that runs while the laptop is closed.
- **The old Cowork scheduled tasks** `internship-sweep---summer-27` and
  `scholarship-sweeper---26-27` still exist on his desktop and still cannot publish.
  They are superseded by this; he can delete them.
