# Build letter delegation, and the cloud publish route

2026-08-22. What this session did, in the order it mattered, so a fresh session can pick up without reading a transcript.

## What was asked

Rework the per-row **Build letter** button so that clicking it yields a prompt addressed to Opus that redirects the drafting to a Sonnet subagent, rather than a prompt whichever chat receives it runs itself.

## What the button does now

It copies an orchestration prompt in three parts:

1. An instruction to Opus: do not write this one yourself, spawn one subagent with the model set to Sonnet, and pass the brief through verbatim.
2. The brief itself, fenced with `---8<---`. Self-contained, because a subagent starts cold and can see neither the chat nor the dashboard. It carries the row facts, the skill name, the Packets and past-letters folder ids, and the hard rules: never submit, never touch the frozen sheet, no em dash, no pay figure, and the do-not-claim list including AutoCAD and Revit.
3. A voice pass for Opus on the way back: read the doc, cut anything equally true of another employer, check the numbers are attributed right, scan for em dashes and hedges, rewrite in place if it reads generic.

Internship and scholarship rows diverge only in the last thing the subagent is asked to report. A role asks whether the posting states housing or relocation, with the reminder that silence is not refusal. A scholarship asks for essay-bank coverage and the eligibility gate instead. The old prompt asked scholarships about housing, which was never right.

This splits `CLAUDE.md`'s cost rule rather than contradicting it: Sonnet carries the long skill run and the Drive write, Opus keeps the voice, and the tool transcript never lands in the expensive thread.

## The thing that was actually broken

The first report back was "looks unchanged", with a pasted prompt in the old format. It was not a bug. The change existed only in the repo, and the board being clicked is the live artifact, which nothing had republished.

Checking that turned up a worse problem. The pasted prompt carried facts the repo copy did not have: Centennial rather than Englewood, the ITAR requirement, the $2,000 housing allowance, $35/hr. The repo was two builds behind the live board.

| | repo copy | live board |
|---|---|---|
| Internship rows | 29 | 41 |
| Applied ticks | null | 14 |
| Boom Supersonic | Englewood, `[UNVERIFIED]` | Centennial, verified |

Publishing the committed file would have deleted twelve rows and all fourteen ticks. **This is the general hazard: the repo is a build, the live page is the truth, and a republish is always built from a fresh read.**

## How it shipped

Read the live artifact, reconstructed it with `mkbase2.py`, applied the button change as an anchored find/replace, verified, published, read it back. Version `1787428545-d4e8` to `1787430085-95fa`. Fourteen ticks in, fourteen out, same slugs. Capability declaration carried forward as `{artifact, downloads}` on contract 0.2.11 by omitting the parameter.

## The finding worth more than the change

**A cloud Claude Code session can read and publish the tracker.** Not through `WebFetch`, which still cannot reach the frame host from behind the egress proxy, but through the **Artifact tool's own `read` action**, which returns the whole document and sets the tracked baseVersion. The publish after it is ordinary. No laptop, no console script, no allowlist.

That closes section 6 item 0 and narrows the open question to routines, which are a different surface and are what the sweeps actually need. Testing that is cheap: one routine that reads the artifact and reports the byte count. Nothing about the sweeps should be built until that call has been made.

The wrapper-nesting caveat from 2026-08-21 fired on this publish and was chased down rather than assumed: two html and body wrappers came back where one went in, reconstruction collapses it to one, and a third generation does not drift. Cosmetic, self-healing on the next tick, still worth checking every time.

## What is in the repo now

- `dashboard/application-command-center-1787428545-41row.html`, the current source, `applied:null`, never publishable as-is.
- `dashboard/patches/`, anchored one-change edit scripts, with `apply-delegation.py` and the replacement block it installs.
- `dashboard/verify/`, 48 assertions, `run.sh` defaulting to the current build. Seven of those (I1 to I7) hold the shape of the Build letter prompt, including that no em dash ever reaches the clipboard.

## Left open

- Whether a scheduled routine can publish. The one thing blocking the sweeps.
- `prompts/sweep-prompt-internship.txt` and `sweep-prompt-scholarship.txt` still exist only inside the two desktop scheduled tasks.
- Bug 17, Oxy's location field, and bug 6, the note-toggle scroll jump. Both still open, both cheap, neither touched here.
- The sweep buttons still call `window.cowork.runScheduledTask` and will need replacing when the sweeps move.
