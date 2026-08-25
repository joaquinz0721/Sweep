# dashboard/

## The current source

`application-command-center-1787637025-41row.html`, 110333 bytes, md5 `414cb2ab7b2529c02a641628ae8dfb08`.

Taken from the live artifact on 2026-08-22, reconstructed with `verify/mkbase2.py --null-state`,
then patched with `patches/apply-delegation.py` to give the Build letter button its
Opus-to-Sonnet delegation prompt. 41 internship rows, 12 scholarship rows, `applied:null`
because the ticks are Joaquin's and travel with the live page, never with a file here.
All 48 assertions in `verify/` pass against it, and it is its own canonical reconstruction,
so it is a fixed point and safe as an edit base.

**It has not been published.** The live artifact still runs the old Build letter code
until someone republishes, and a republish has to carry the 14 live ticks, so it must be
built from a fresh read of the artifact rather than from this null-state file.

## Also here, historical

`application-command-center-1787336084-pre16row.html`, 78,656 bytes, md5 `9aac4a4f8233f1d15ec13549dc3706ec`.

**This is NOT the current dashboard and it is now two builds behind.** It is the authored build as it stood immediately before the sixteen-row verification change of 2026-08-21, and it is roughly three publishes behind the live artifact. Verified by inspection on 2026-08-21:

- All four marker pairs present, `ACC-STATE` present, no injected frame runtime.
- State block holds `applied:null`, so it is an authored build and not a served copy.
- **`int-h3x-electromagnetics-intern` is absent**, which is the tell: that slug was added in version `1787353283-20cc`. So none of the sixteen-row edits are in this file.

Three files in `Downloads` on device `jz` are byte-identical to it: `dashboardapplication-command-center.html`, `target2.html`, `target2_1.html`. The file `MEMORY.md` calls `application-command-center-2026-08-21-v3.html` **does not exist on the device.** The nearest older build, `application-command-center-2026-08-21-v2.html` (67,770 bytes), is also on the device and is further behind. `application-command-center-2026-08-21.html` (64,484 bytes) is a raw shell copy: no markers, frame runtime present. Do not use it as an edit base.

## What this file is good for

A diff base and a reference for structure, the harness, and the `buildDoc()` marker logic. It is a legitimate historical build.

## What it is NOT good for

**Never publish from it.** It would silently revert the sixteen-row change and every fact verified on 2026-08-21. Per `docs/MEMORY.md` section 3, the canonical edit base is always the reconstruction taken from the live artifact, never the last file on disk. That rule is exactly why this file is labeled rather than named `application-command-center.html`.

## Getting the current source, and shipping a change

Proven from a cloud Claude Code session on 2026-08-22, no local machine involved:

1. Read the artifact with the **Artifact tool's `read` action**. It returns the whole document and sets the tracked base version. `WebFetch` still cannot reach the frame host from a cloud session and is not needed.
2. Reconstruct with `verify/mkbase2.py`. Plain for a publish payload, so the live ticks survive; `--null-state` for the copy that gets committed here.
3. Make the change as an anchored find/replace, never byte offsets. `patches/` holds the scripts.
4. Verify: `verify/run.sh path/to/build.html`, all 48 assertions, plus the tick count before and after.
5. Publish passing the artifact URL and the favicon `🎯`. Never `force`, never a `capabilities` object, since omitting it carries the stored declaration forward.
6. Read it back and confirm row counts, slugs and ticks before reporting it done. Record the new slug in `docs/MEMORY.md` section 1 and commit the null-state build here.
