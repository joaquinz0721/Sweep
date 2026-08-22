# dashboard/

## What is here

`application-command-center-1787336084-pre16row.html`, 78,656 bytes, md5 `9aac4a4f8233f1d15ec13549dc3706ec`.

**This is NOT the current dashboard.** It is the authored build as it stood immediately before the sixteen-row verification change of 2026-08-21, and it is roughly three publishes behind the live artifact. Verified by inspection on 2026-08-21:

- All four marker pairs present, `ACC-STATE` present, no injected frame runtime.
- State block holds `applied:null`, so it is an authored build and not a served copy.
- **`int-h3x-electromagnetics-intern` is absent**, which is the tell: that slug was added in version `1787353283-20cc`. So none of the sixteen-row edits are in this file.

Three files in `Downloads` on device `jz` are byte-identical to it: `dashboardapplication-command-center.html`, `target2.html`, `target2_1.html`. The file `MEMORY.md` calls `application-command-center-2026-08-21-v3.html` **does not exist on the device.** The nearest older build, `application-command-center-2026-08-21-v2.html` (67,770 bytes), is also on the device and is further behind. `application-command-center-2026-08-21.html` (64,484 bytes) is a raw shell copy: no markers, frame runtime present. Do not use it as an edit base.

## What this file is good for

A diff base and a reference for structure, the harness, and the `buildDoc()` marker logic. It is a legitimate historical build.

## What it is NOT good for

**Never publish from it.** It would silently revert the sixteen-row change and every fact verified on 2026-08-21. Per `docs/MEMORY.md` section 3, the canonical edit base is always the reconstruction taken from the live artifact, never the last file on disk. That rule is exactly why this file is labeled rather than named `application-command-center.html`.

## Getting the current source

Run a local Code-tab session, `WebFetch` the artifact, reconstruct on the marker pairs as `buildDoc()` does, and commit the result here as `application-command-center.html` with its version slug recorded in `docs/MEMORY.md` section 1.
