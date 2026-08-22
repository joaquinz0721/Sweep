#!/usr/bin/env python3
"""Build a served copy carrying a REALISTIC state block.

This exists because of a real failure on 2026-08-21. A gate was calibrated
against a build whose state block held `applied:null`; the moment a tick saved,
the live page grew 586 characters and every baked-in length number went stale.

Rehearsing against applied:null is rehearsing against a document that does not
exist in production. Always rehearse against this.

    python3 mklive3.py AUTHORED.html LIVE.html [--ticks N]
"""
import argparse
import accdoc, shell

# The 14 ticks recorded in docs/MEMORY.md section 2, in order.
TICKS = [
    ("int-medtronic-engineering-intern", "2026-08-17"),
    ("int-wdc-hardware-intern", "2026-08-17"),
    ("int-anduril-mech-intern", "2026-08-17"),
    ("int-spacex-eng-intern", "2026-08-17"),
    ("int-kairos-mech-mfg-intern", "2026-08-18"),
    ("int-ge-mfg-intern", "2026-08-18"),
    ("int-ge-systems-intern", "2026-08-18"),
    ("int-greatplains-design-intern", "2026-08-18"),
    ("int-boeing-facilities-intern", "2026-08-18"),
    ("int-anduril-mfg-intern", "2026-08-18"),
    ("int-vertiv-liquid-cooling-intern", "2026-08-18"),
    ("int-bae-operations-coop", "2026-08-18"),
    ("int-elliott-design-intern", "2026-08-18"),
    ("int-marotta-space-systems-intern", "2026-08-21"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--ticks", type=int, default=len(TICKS))
    ap.add_argument("--base", default="/")
    a = ap.parse_args()
    src = open(a.src, encoding="utf-8").read()

    applied = dict(TICKS[:a.ticks])
    present = set(accdoc.slugs(src, "int"))
    missing = [k for k in applied if k not in present]
    if missing:
        raise SystemExit("mklive3.py: refusing to tick slugs that are not in INT: " + ", ".join(missing))

    payload = {"v": 4, "updated": "2026-08-21", "count": len(applied), "applied": applied}
    authored = accdoc.rebuild(src, payload)
    served = shell.transform(authored, base=a.base)
    open(a.dst, "w", encoding="utf-8").write(served)
    print("mklive3.py: {} ticks, authored {} chars, served {} chars, delta {:+d}".format(
        len(applied), len(authored), len(served), len(authored) - len(src)))


if __name__ == "__main__":
    main()
