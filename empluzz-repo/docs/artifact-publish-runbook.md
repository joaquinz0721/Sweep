# Updating the tracker artifact without burning a session on it

One file, one procedure. Read this before touching the artifact and you spend
roughly 60K tokens shipping a change. Skip it and you spend 250K discovering the
same three facts again, which is exactly what happened on 2026-08-25.

The artifact is `https://claude.ai/code/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594`.
Live version at last write: `1787695423-9d50`, published 2026-08-25 from a cloud
Claude Code session, 17 applied ticks, 41 internship rows, 12 scholarship rows.

---

## 0. The one thing that decides whether this works

The publish gate wants proof you have seen the version you are overwriting. That
proof is **the `Read` tool, over every line of the file the current fetch just
handed you, in this session, with the publish following right after.**

Things that look like reading and do not count:

- `cat`, `sed -n`, `head`, `grep` through Bash. The bytes reach you; the gate
  does not see it. In auto mode the standing instruction is to prefer Bash for
  file reads. **This file is the exception. Use `Read`.**
- A file an earlier fetch left on disk, even at the same version id and the same
  path. Fetch again and read what the new fetch names.
- Reads that happened before a context compaction. Treat a compaction between
  the read and the publish as if the read never happened.

Do the fetch and the full read as the **first** thing in the session, then
publish. Everything else, the rebuild, the harness, the docs, can happen after
the bytes are in hand, and none of it should sit between the read and the
publish if you can help it.

## 1. The procedure

```
fetch -> full Read -> rebuild -> verify -> publish -> read back -> commit
```

**1. Fetch.** `Artifact` with `action:"read"` and the URL. The result names a
saved file, `tool-results/artifact-da80ff29-<version>.html`, and states the
version. This call is what sets the tracked base version.

**2. Full Read.** `Read` the saved file end to end. About 1107 lines, roughly
56K tokens, five or six calls at the 25K per-read cap. Sequential offsets, no
gaps. This is the expensive step and it is not optional.

**3. Rebuild from that exact file.**

```bash
cd /home/user/Sweep/empluzz-repo
python3 dashboard/verify/mkbase2.py <saved-file> /tmp/apb/work/live-base.html
```

`mkbase2` strips the injected frame runtime and reconstructs the authored
document while keeping the live applied ticks. Apply the change to the
reconstruction with anchored find and replace. Never by byte offset, never by
hand. Reusable edits live in `dashboard/patches/`.

**4. Verify.**

```bash
cd dashboard/verify && npm install          # node_modules does not survive a fresh container
ACC_CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome bash run.sh /tmp/apb/work/live-base.html
```

All 56 assertions, 41 plus 8 plus 7. The pinned Playwright does not match the
image's default Chromium, hence the explicit binary; `harness.js` documents the
hatch. Also confirm the tick count in equals the tick count out and that the
INT and SCH row arrays are byte-identical to the source.

**5. Publish.** `Artifact` with `file_path`, the artifact `url`, `favicon:"🎯"`,
and nothing else. No `force`. No `capabilities` object, so the stored
declaration carries forward untouched.

**6. Read back.** Fetch again, confirm the new version id, and grep the served
copy for the string you added. `mkbase2` on the served copy should collapse
cleanly and be stable on a second generation.

**7. Commit.** Rebuild with `--null-state` and commit that, named
`application-command-center-<version>-<tag>.html`. The ticks are Joaquin's and
stay with the live page. Then update `dashboard/README.md` (name, byte count,
md5), `docs/MEMORY.md` section 1 (new version id) and `docs/sweep-pipeline.md`
if the assertion count or the button text moved.

## 2. When it refuses

Two errors, and they mean different things:

| Error | Meaning | Move |
|---|---|---|
| "You hadn't viewed the live version of this artifact" | The view check did not register. Section 0. | Fetch again, `Read` every line, publish immediately. **Once.** |
| "identical content already refused against the newer version X, resent unchanged" | Your payload is byte for byte what was already refused. | Not a new failure. See below. |

**The rebuild is deterministic.** `mkbase2` plus the same anchored edits produces
identical bytes every time; this was proven with md5 across two fetches. So a
payload rebuilt from a fresher fetch is the same payload, and the gate is telling
the truth when it calls it a resend. Changing the fetch does not change the
bytes, which is why the two errors alternate and why the loop feels unbreakable.

**`force:true` is not an escape.** Tried once with Joaquin's explicit
confirmation and rejected by the server, not the tool:

```
deploy 400: this artifact self-publishes - provide the baseVersion you edited from
```

The Artifact tool exposes no `baseVersion` parameter. The page writes its own
versions whenever a tick is saved, so a version written from inside the page can
sit under you at any time.

**Hard stop: two refusals and you are done in this session.** Reading again costs
50K tokens and has never once cleared it. Take an exit:

- **Preferred: a fresh session.** Both successful publishes, `1787637025-0b51`
  and `1787695423-9d50`, came from sessions whose first artifact fetch was in
  that session. The session that failed five cycles had fetched the same version
  earlier and crossed a compaction. Hand the next session the merged build file
  and this doc, and it lands on the first try.
- **Or hand the build to Joaquin** for the Code tab, which does not go through
  this gate. Containers are disposable, so send the file, do not leave it in
  `/tmp`.

Either way, write down the version id you read, both error strings verbatim, and
what you tried.

## 3. The cheap probe, if you are unsure

Full reads cost about 50K tokens each, so find out early which state you are in.
Fetch, `Read` in full, and publish a **one-line throwaway change**, a comment or
a label. One cycle total. If it lands, spend the next cycle on the real change.
If it returns either error, stop, per section 2. Do not probe if your real change
is already built and verified; just publish that and let it be the probe.

## 4. Invariants

- **Always build from a fresh read.** Publishing the committed null-state file
  sets every applied tick to null and erases Joaquin's work.
- **Always pass the URL.** Without it you create a second artifact and split the
  tracker in two.
- **Always pass favicon 🎯.** A changed favicon reads to him as a different page.
- **Never pass a `capabilities` object.** A non-empty one revokes anything not
  restated, which silently kills tick saving. Omitting it carries
  `{artifact, downloads}`, contract `0.2.11`, forward intact.
- **Never commit a build carrying live ticks.** `--null-state` or it does not go
  in the repo.
- **56 assertions.** If a suite reports 48 or 41, the count in a doc or in the
  page's own `sweepPrompt()` is stale; fix it in the same commit.
- **Wrapper nesting of 2/2 on a served copy is cosmetic.** It collapses to 1/1
  on reconstruction and is stable at a third generation. Check it, do not panic
  at it.

## 5. Token budget

| Step | Cost |
|---|---|
| Fetch | ~1K |
| Full read, 1107 lines | ~50 to 56K |
| Rebuild, patch, harness | ~5K |
| Publish and read back | ~10K |
| **One clean cycle** | **~70K** |
| Each failed cycle | ~55K, and it buys nothing |

The whole point of this file is that the second row is paid once.
