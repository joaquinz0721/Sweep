#!/usr/bin/env python3
"""Derive the canonical reconstruction from a shell-served copy.

This is the edit base. Not the file you last published, and not the served copy.
buildDoc's re-wrap normalises the seam and drops the trailing newline, so the
reconstruction can be shorter than the file that produced it. That reconstruction
is the fixed point and every gate is measured against it.

    python3 mkbase2.py SERVED.html BASE.html [--null-state]
"""
import argparse
import accdoc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--null-state", action="store_true",
                    help="write applied:null, producing a shippable authored build")
    a = ap.parse_args()
    src = open(a.src, encoding="utf-8").read()
    payload = None
    if a.null_state:
        st = accdoc.read_state(src)
        payload = {"v": 4, "updated": st.get("updated", "2026-08-21"), "applied": None}
    out = accdoc.rebuild(src, payload)
    open(a.dst, "w", encoding="utf-8").write(out)
    st = accdoc.read_state(out)
    n = len(st.get("applied") or {})
    print("mkbase2.py: {} chars -> {} chars, {} applied ticks".format(len(src), len(out), n))


if __name__ == "__main__":
    main()
