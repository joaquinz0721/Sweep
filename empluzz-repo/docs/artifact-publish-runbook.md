# Publishing to the tracker artifact, and how to tell fast when you cannot

Written 2026-08-25, after the coursework-rule change failed to ship from a cloud
Claude Code session. It covers the workflow that DID ship version
`1787637025-0b51`, the exact failure seen this time, and the cheap probe that
tells you within a minute which situation you are in.

The artifact is `https://claude.ai/code/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594`.

---

## 1. The workflow that works (route 0a)

```
fetch  ->  full read  ->  rebuild from that file  ->  verify  ->  publish  ->  read back
```

1. **Fetch.** `Artifact action:"read"` on the URL. The result names a saved file
   under `tool-results/artifact-da80ff29-<version>.html` and states the version.
   This fetch is what sets the tracked base version. Never publish from a file an
   earlier fetch handed you.
2. **Full read.** `Read` every line of that saved file. It is about 1100 lines and
   roughly 56K tokens, so it takes five or six calls; the per-read cap is 25K
   tokens. Budget for it.
3. **Rebuild from that exact file.** `python3 dashboard/verify/mkbase2.py <saved
   file> <out>` strips the injected frame runtime and reconstructs the authored
   document, keeping the live applied ticks. Apply your change to the
   reconstruction with anchored find/replace, never by hand and never by offset.
4. **Verify.** `ACC_CHROMIUM=/opt/pw-browsers/chromium bash dashboard/verify/run.sh <out>`.
   All 56 assertions must pass. Also confirm the tick count mkbase2 reports going
   in matches what you expect, and diff the data arrays against the source so the
   only change is yours.
5. **Publish.** `Artifact` with `file_path`, the artifact `url`, favicon `🎯`, and
   nothing else. **No `force`. No `capabilities` object**, so the stored
   declaration carries forward.
6. **Read back.** Fetch again, confirm the new version id, and grep the served
   copy for the string you added.

## 2. What went wrong on 2026-08-25

The workflow above was run faithfully, twice, and the publish never landed. The
gate returns two errors and alternates between them:

- **"You hadn't viewed the live version of this artifact, so the publish was
  refused ... that version counts as viewed once you have Read every line of that
  file."** Returned even immediately after reading all 1107 lines of the file the
  current fetch had just handed over.
- **"this is the identical content already refused against the newer version
  1787690446-c1a6, resent unchanged."**

**The diagnosis that took the longest to see:** the rebuild is deterministic.
`mkbase2` plus the same anchored edits produces the same bytes every time, so a
payload rebuilt from a later fetch is byte-identical to the one already refused
(verified with md5). That is why the gate calls it a resend. Change the payload
and the gate stops saying "identical" and goes back to "hadn't viewed", which is
the check that never clears. **The read is what is failing to register, and no
amount of re-reading fixes it.**

`force:true` is not the way out. With the user's explicit confirmation it was
tried once and the server, not the tool, rejected it:

```
deploy 400: this artifact self-publishes - provide the baseVersion you edited from
```

The Artifact tool exposes no `baseVersion` parameter. This artifact writes its own
versions when a tick is saved, and the live version `1787690446-c1a6` was written
that way, from inside the page, earlier the same day.

## 3. The probe, before spending anything

Full reads of this file cost roughly 50K tokens each. Three failed cycles cost
about 250K. Do this first, every time:

1. Fetch, read the file in full, and publish a **one-line throwaway change**
   (a comment, a label). Total cost is one cycle.
2. If it lands, discard the throwaway with your real change on the next cycle and
   carry on with section 1.
3. If it returns either error above, **stop**. You are in the 2026-08-25 state and
   more reads will not clear it.

## 4. When the probe fails

- **Do not retry the loop.** Both errors are deterministic and neither is a
  transient.
- **Do not force.** The server refuses force on this artifact by design.
- **Hand the merged build to Joaquin** so he can publish it from the Code tab
  (route 0), which does not go through this gate. The container is disposable, so
  send the file rather than leaving it in `/tmp`.
- **Never commit a state-carrying build.** The repo copy is `applied:null` by
  convention; a build carrying live ticks is a transfer artifact, not a source
  file.
- Write down the version id you read, the errors verbatim, and what you tried.

## 5. Rules that do not change

- A republish is always built from a fresh read. Publishing the committed
  null-state file sets every applied tick to null.
- Pass the URL, or you create a second artifact and split the tracker in two.
- Pass the favicon `🎯` so the tab icon stays stable.
- Never pass a `capabilities` object. A non-empty one revokes anything not
  restated, which silently breaks tick saving.
- The verification harness is 56 assertions: 41 plus 8 plus 7.
