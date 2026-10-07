# dashboard/

Every file here is a null-state build: `applied:null`, because the applied ticks
are Joaquin's and live with the artifact, never with a file in this repo. Each is
named for the live version it corresponds to, and the name is a claim about its
bytes. Do not patch a build in place unless you are about to rename it.

## The current source

`application-command-center-1791367605-intsweep.html`, 172,102 bytes, md5
`1a5690ae7bdbb90722898e629b0bdf96`.

The null-state copy of live version `1791367605-4df8`, published 2026-10-07 by the
first sweep through the built pipeline. 69 internship rows, 12 scholarship rows. On top of
the `1791366720` build it carries four new UNCONFIRMED rows (CesiumAstro, USA Rare Earth,
Salas O'Brien, Sierra Space), a recheck note on the Xcel Power Generation Analytics row,
two Screened Out rows and a Calendar row stamped 2026-10-07. All written by `ingest.py`.

Verified before the publish: all 56 assertions pass (41 + 8 + 7), 41 ticks in and out with
the state block byte identical, and the published version reconstructs byte-identical to
the payload.

## Previous source

`application-command-center-1791366720-sweeppipeline.html`, 165,289 bytes, md5
`b14b29804b9492c7b725f82679d57ff5`.

The null-state copy of live version `1791366720-cf74`, which shipped the wage-floor split
and the Run Sweep buttons pointing at the built pipeline. Superseded 2026-10-07 by the
sweep above. Kept as history; do not edit from it.

## Older source

`application-command-center-1787637025-41row.html`, 110,115 bytes, md5
`7ea70b3fbe0d763231731c181ca863a3`.

The build that shipped the writing-system button as live version
`1787637025-0b51`. Superseded 2026-08-25.

It briefly carried the coursework and assertion-count edits, applied here while
the publish route was blocked. Those bytes were the right change in the wrong
file: patching a build named for an older live version makes its name a lie.
Restored to its published bytes on merge. The change itself shipped in the
current source above, and the two builds were diffed to prove it: identical
except for the `updated` date in the state block.

## Also here, historical

`application-command-center-1787336084-pre16row.html`, 78,656 bytes, md5
`9aac4a4f8233f1d15ec13549dc3706ec`.

**This is NOT the current dashboard and it is several builds behind.** It is the
authored build as it stood immediately before the sixteen-row verification change
of 2026-08-21. Verified by inspection that day:

- All four marker pairs present, `ACC-STATE` present, no injected frame runtime.
- State block holds `applied:null`, so it is an authored build, not a served copy.
- **`int-h3x-electromagnetics-intern` is absent**, which is the tell: that slug
  arrived in version `1787353283-20cc`. So none of the sixteen-row edits are here.

Commit `75e0827` used this file as a scratch base for the delegation prompt and
left 73 changed lines in it, which broke the one thing it is for. Restored to its
labeled bytes on merge; the delegation prompt lives in the current source and in
`patches/`.

Three files in `Downloads` on device `jz` are byte-identical to the restored
file: `dashboardapplication-command-center.html`, `target2.html`, `target2_1.html`.
The file `MEMORY.md` calls `application-command-center-2026-08-21-v3.html` **does
not exist on the device.** `application-command-center-2026-08-21-v2.html`
(67,770 bytes) is also there and is further behind.
`application-command-center-2026-08-21.html` (64,484 bytes) is a raw shell copy:
no markers, frame runtime present. Do not use it as an edit base.

### What it is good for

A diff base for that moment, and a reference for structure, the harness, and the
`buildDoc()` marker logic.

### What it is NOT good for

**Never publish from it.** It would silently revert the sixteen-row change and
every fact verified on 2026-08-21.

## Shipping a change

The full procedure, the publish gate's two refusals, and what to do when it
refuses twice are in **`docs/artifact-publish-runbook.md`**. Read that first; it
exists so a session spends one full read instead of five. The short form:

1. `Artifact action:"read"` on the URL. This sets the tracked base version.
2. **`Read` every line of the file that fetch names.** The `Read` tool, in this
   session, before the publish. Bash `cat`, `sed` and `grep` do not satisfy the
   gate, and neither does a file an earlier fetch left behind.
3. Reconstruct with `verify/mkbase2.py`. Plain for the publish payload so the
   live ticks survive; `--null-state` for the copy committed here.
4. Change it with an anchored find and replace, never byte offsets. `patches/`
   holds the scripts.
5. Verify: `npm install` in `verify/`, then
   `ACC_CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome bash verify/run.sh <build>`.
   All 56 assertions, plus the tick count before and after.
6. Publish with the artifact `url` and favicon `🎯`. Never `force`, never a
   `capabilities` object.
7. Read it back, confirm row counts, slugs and ticks, record the new version in
   `docs/MEMORY.md` section 1, and commit the null-state build here.
