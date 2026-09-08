#!/usr/bin/env python3
"""Merge a sweep payload into a command-center build.

    python3 dashboard/ingest.py PAYLOAD.json [--target BUILD.html] [--apply] [--out FILE]

Without --apply it prints what it would do and writes nothing. That is the
preview the sweep pipeline calls for and it is the default on purpose.

What it does
------------
Merges the payload's INT_new and SCH_new rows into the INT and SCH arrays of a
build, keyed on the slug (index 13 on INT, index 12 on SCH, never a literal),
and stamps a Calendar row's Last Checked
date so the header SWEPT stamp moves. A slug already present is an update and
its row is replaced in place; a slug not present is an append.

What it refuses to do
---------------------
The guard rails are Joaquin's, agreed 2026-08-21, and none of them has a flag:

- It never reads, writes, or reasons about the applied ticks. The state block is
  copied byte for byte from input to output and compared afterwards. If it moved,
  ingest fails and writes nothing.
- A row without a slug, with the wrong field count, or with a malformed slug is
  a hard failure for the whole run, not a skipped row.
- Two payload rows carrying the same slug is a hard failure.
- Malformed JSON is a hard failure, which is what json.load already does; this
  file just declines to catch it into a warning.
- It never consolidates. Rows are matched only on an exact slug, so two
  requisitions at one company stay two rows forever (hard rule 8).
- It never publishes. Publishing is the runbook's job, from a fresh read.

Exit codes: 0 clean, 1 refused.
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "verify"))
import accdoc  # noqa: E402

# INT and SCH are NOT the same shape. The source comment above const SCH says it
# outright: the slug is index 12 there and index 13 on INT. Never use a literal.
FIELDS = {"INT": 14, "SCH": 13}
SLUG_AT = {"INT": 13, "SCH": 12}
KIND = {"INT": "int", "SCH": "sch"}
CONVICTIONS = {"MUST APPLY", "STRONG", "STRETCH", "WATCH"}
STATUSES = {"OPEN", "NOTYET", "CLOSED", "UNCONFIRMED", "BLOCKED"}
CAL_NAME_AT, CAL_TYPE_AT, CAL_CHECKED_AT = 1, 0, 6
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def newest_build():
    """The newest authored build in dashboard/, by the version in its name.

    Never hardcode one. A build is named for the live version it came from, so
    naming it here means this default becomes a lie the next time one ships,
    which is exactly what happened to run.sh and to the sweep button.
    """
    found = glob.glob(os.path.join(HERE, "application-command-center-*.html"))
    if not found:
        return os.path.join(HERE, "application-command-center-MISSING.html")
    def ver(path):
        m = re.search(r"application-command-center-(\d+)", os.path.basename(path))
        return int(m.group(1)) if m else -1
    return max(found, key=ver)


class Refused(Exception):
    """Anything that should stop the run and write nothing."""


def die(msg):
    raise Refused(msg)


# ---------------------------------------------------------------- array slicing

def array_span(src, name):
    """Byte span of the rows inside `const NAME=[` ... `\\n];`, exclusive of both."""
    head = "const " + name + "=["
    a = src.find(head)
    if a < 0:
        die("array %s not found in the target" % name)
    if src.find(head, a + 1) >= 0:
        die("array %s appears more than once; refusing to guess" % name)
    start = a + len(head)
    end = src.find("\n];", start)
    if end < 0:
        die("array %s is not terminated by a line starting with ];" % name)
    return start, end


def parse_rows(src, name):
    """Return [(row, raw_text)] for one array. Order preserved."""
    start, end = array_span(src, name)
    body = src[start:end]
    rows = []
    for raw in re.findall(r"^\[.*\],?$", body, re.M):
        text = raw[:-1] if raw.endswith(",") else raw
        try:
            rows.append((json.loads(text), text))
        except ValueError as e:
            die("a %s row in the target is not valid JSON: %s" % (name, e))
    return rows


def render(row):
    return json.dumps(row, ensure_ascii=False, separators=(",", ":"))


# ------------------------------------------------------------------ validation

def check_payload_rows(rows, name, label):
    kind, want, slug_at = KIND[name], FIELDS[name], SLUG_AT[name]
    seen = {}
    for i, row in enumerate(rows):
        where = "%s[%d]" % (label, i)
        if not isinstance(row, list):
            die("%s is not a list" % where)
        if len(row) != want:
            die("%s has %d fields, expected %d for %s" % (where, len(row), want, name))
        if not all(isinstance(f, str) for f in row):
            die("%s has a non-string field; every field is a string" % where)
        slug = row[slug_at]
        if not slug.strip():
            die("%s has no slug. A row without a slug is refused, always." % where)
        if not re.match(r"^" + kind + r"-[a-z0-9-]+$", slug):
            die("%s has a malformed slug %r; expected %s-[a-z0-9-]+" % (where, slug, kind))
        if row[0] not in CONVICTIONS:
            die("%s has conviction %r, not one of %s" % (where, row[0], sorted(CONVICTIONS)))
        if row[10] not in STATUSES:
            die("%s has status %r, not one of %s" % (where, row[10], sorted(STATUSES)))
        if row[5].strip() and not DATE.match(row[5].strip()):
            die("%s has deadline %r, which is neither empty nor YYYY-MM-DD" % (where, row[5]))
        flat = json.dumps(row, ensure_ascii=False)
        if "—" in flat or "–" in flat:
            die("%s contains an em dash or en dash, which is banned everywhere" % where)
        if slug in seen:
            die("%s and %s carry the same slug %r" % (seen[slug], where, slug))
        seen[slug] = where


# ----------------------------------------------------------------------- merge

def plan(src, name, new_rows):
    slug_at = SLUG_AT[name]
    existing = parse_rows(src, name)
    for r, _ in existing:
        if len(r) != FIELDS[name]:
            die("a %s row in the target has %d fields, expected %d"
                % (name, len(r), FIELDS[name]))
    index = {r[slug_at]: i for i, (r, _) in enumerate(existing)}
    adds, updates = [], []
    for row in new_rows:
        slug = row[slug_at]
        if slug in index:
            old = existing[index[slug]][0]
            if old != row:
                updates.append((slug, old, row))
        else:
            adds.append(row)
    return existing, index, adds, updates


def splice(src, name, existing, index, adds, updates):
    rows = [list(r) for r, _ in existing]
    for slug, _old, new in updates:
        rows[index[slug]] = new
    rows.extend(adds)
    start, end = array_span(src, name)
    body = "\n" + ",\n".join(render(r) for r in rows) + "\n"
    return src[:start] + body + src[end:]


def stamp_cal(src, stamp):
    """Upsert one CAL row by (type, name) and set its Last Checked date."""
    date = stamp.get("last_checked", "")
    if not DATE.match(date):
        die("cal_stamp.last_checked %r is not YYYY-MM-DD" % date)
    rows = [list(r) for r, _ in parse_rows(src, "CAL")]
    want = (stamp.get("type", "Internship"), stamp["name"])
    hit = None
    for i, r in enumerate(rows):
        if (r[CAL_TYPE_AT], r[CAL_NAME_AT]) == want:
            if hit is not None:
                die("two CAL rows already match %r; refusing to guess" % (want,))
            hit = i
    if hit is None:
        row = [want[0], want[1], stamp.get("tier", "A"),
               stamp.get("window", "Continuous"), stamp.get("check_starting", ""),
               stamp.get("status", "PENDING"), date, stamp.get("notes", "")]
        if len(row) != len(rows[0]):
            die("built a CAL row of %d fields against existing %d" % (len(row), len(rows[0])))
        rows.append(row)
        action = "added"
    else:
        was = rows[hit][CAL_CHECKED_AT]
        rows[hit][CAL_CHECKED_AT] = date
        if stamp.get("notes"):
            rows[hit][-1] = stamp["notes"]
        action = "bumped from %s" % (was or "empty")
    start, end = array_span(src, "CAL")
    body = "\n" + ",\n".join(render(r) for r in rows) + "\n"
    return src[:start] + body + src[end:], action


def swept(src):
    best = ""
    for r, _ in parse_rows(src, "CAL"):
        d = r[CAL_CHECKED_AT] or ""
        if DATE.match(d) and d > best:
            best = d
    return best or "never"


# ------------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(description="Merge a sweep payload into a build.")
    ap.add_argument("payload")
    ap.add_argument("--target", default=newest_build(),
                    help="build to merge into; default is the newest committed build")
    ap.add_argument("--apply", action="store_true",
                    help="write the merge. Without this nothing is written.")
    ap.add_argument("--out", help="where to write; default is in place over --target")
    a = ap.parse_args()

    with open(a.payload, encoding="utf-8") as fh:
        pay = json.load(fh)          # malformed JSON dies here, uncaught, by design
    src = open(a.target, encoding="utf-8").read()

    int_new = pay.get("INT_new") or []
    sch_new = pay.get("SCH_new") or []
    check_payload_rows(int_new, "INT", "INT_new")
    check_payload_rows(sch_new, "SCH", "SCH_new")

    state_before = accdoc.read_state(src)
    ticks_before = len(state_before.get("applied") or {})

    out = src
    totals = []
    for name, new_rows in (("INT", int_new), ("SCH", sch_new)):
        existing, index, adds, updates = plan(out, name, new_rows)
        totals.append((name, len(existing), adds, updates))
        if a.apply and (adds or updates):
            out = splice(out, name, existing, index, adds, updates)

    stamp = pay.get("cal_stamp")
    if stamp is None and pay.get("cal_last_checked"):
        stamp = {"name": "Internship sweep (aggregators)", "type": "Internship",
                 "last_checked": pay["cal_last_checked"]}
    cal_action = None
    if stamp:
        if a.apply:
            out, cal_action = stamp_cal(out, stamp)
        else:
            _, cal_action = stamp_cal(out, stamp)

    # ---- report
    print("ingest.py")
    print("  payload : %s" % a.payload)
    print("  target  : %s" % a.target)
    print("  mode    : %s" % ("APPLY" if a.apply else "PREVIEW, nothing is written"))
    print("  ticks   : %d applied, untouched" % ticks_before)
    print()
    n_new = n_upd = 0
    for name, had, adds, updates in totals:
        n_new += len(adds); n_upd += len(updates)
        print("  %s: %d rows in target, %d new, %d updated" % (name, had, len(adds), len(updates)))
        for row in adds:
            print("      + %-46s %-10s %s" % (row[SLUG_AT[name]], row[0], row[1]))
        for slug, old, new in updates:
            print("      ~ %s" % slug)
            for i, (o, n) in enumerate(zip(old, new)):
                if o != n:
                    print("          [%d] %r" % (i, o))
                    print("           -> %r" % (n,))
    if stamp:
        print()
        print("  CAL: %r Last Checked %s (%s)" % (stamp["name"], stamp["last_checked"], cal_action))
        print("  SWEPT: %s -> %s" % (swept(src), stamp["last_checked"]))
    print()
    print("  TOTAL: %d new, %d updated" % (n_new, n_upd))

    if not a.apply:
        print()
        print("Preview only. Re-run with --apply to write it.")
        return 0

    # ---- invariants, checked on the bytes we are about to write
    if accdoc.read_state(out) != state_before:
        die("the state block changed. Applied ticks are never touched. Nothing written.")
    a0, a1 = src.find(accdoc.S_A), src.find(accdoc.S_B)
    b0, b1 = out.find(accdoc.S_A), out.find(accdoc.S_B)
    if src[a0:a1] != out[b0:b1]:
        die("the state block is not byte identical. Nothing written.")
    for name in ("INT", "SCH"):
        merged = parse_rows(out, name)
        if len({r[SLUG_AT[name]] for r, _ in merged}) != len(merged):
            die("the merged %s array has duplicate slugs. Nothing written." % name)
    for marker in (accdoc.H_A, accdoc.H_B, accdoc.B_A, accdoc.B_B, accdoc.S_A, accdoc.S_B):
        if out.count(marker) != 1:
            die("marker %r appears %d times, expected once" % (marker, out.count(marker)))

    dst = a.out or a.target
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    print()
    print("WROTE %s" % dst)
    print("  %d applied ticks, unchanged. Verify next: dashboard/verify/run.sh" % ticks_before)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refused as e:
        print("REFUSED: %s" % e, file=sys.stderr)
        sys.exit(1)
