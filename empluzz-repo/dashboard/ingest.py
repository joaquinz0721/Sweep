#!/usr/bin/env python3
"""
Merge a sweep payload into application-command-center.html.

    python3 ingest.py payload.json                 # preview, writes nothing
    python3 ingest.py payload.json --apply         # actually edit the file
    python3 ingest.py payload.json --apply -o X    # write somewhere else

This is the ONLY sanctioned way for a sweep to reach the dashboard. A sweep
agent produces the payload and never touches the HTML, never publishes, and
never sees the artifact. Everything a sweep could get wrong is a hard error
here rather than a silent corruption of the board.

What it refuses to do, and why:

  * It never removes a row and never merges two rows into one. Standing
    instruction from Joaquin, 2026-08-21: every requisition keeps its own row
    and its own slug forever, even when several sit at the same company.
  * It never changes an existing slug. All applied state is keyed on the slug,
    so rewording a role title used to orphan a tick and the row came back
    unapplied. New rows get a slug, existing rows keep theirs.
  * It never touches the ACC-STATE block, and it verifies byte-for-byte that
    it did not. That block holds his applied ticks. Rule 10 says never touch
    them and refuse to publish if the count changed, so the count is asserted.
  * It rejects em dashes anywhere in any field. Hard rule 4.
  * A new row whose slug already exists is an error, not an update. Updating
    an existing row goes through "patch", which sets named fields only, so a
    sweep that has learned one fact cannot blank the other thirteen.

Untouched rows keep their exact original line text, so the diff of a sweep
shows only what the sweep actually changed.
"""

import argparse
import json
import re
import sys

# Field order is mandatory and is the contract the sweep agents emit against.
INT_FIELDS = ["conviction", "company", "role", "location", "term", "deadline",
              "source", "url", "packet", "notes", "status", "hint", "wage", "slug"]
SCH_FIELDS = ["conviction", "name", "sponsor", "award", "opens", "deadline",
              "gate", "url", "packet", "notes", "status", "hint", "slug"]
OUT_FIELDS = ["kind", "company", "role", "date", "reason"]
CAL_FIELDS = ["kind", "name", "tier", "window", "date", "status", "lastChecked", "note"]

SPEC = {
    "int": {"array": "INT", "fields": INT_FIELDS, "slug_at": 13, "prefix": "int-"},
    "sch": {"array": "SCH", "fields": SCH_FIELDS, "slug_at": 12, "prefix": "sch-"},
    "out": {"array": "OUT", "fields": OUT_FIELDS, "slug_at": None, "prefix": None},
}

CONVICTION = {"MUST APPLY", "STRONG", "STRETCH", "WATCH"}
STATUS = {"OPEN", "NOTYET", "CLOSED", "UNCONFIRMED", "BLOCKED"}
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# U+2014 em dash and U+2013 en dash. Rule 4 names the em dash; the en dash is
# caught too because it is the same mistake wearing a different hat.
DASHES = {"—": "em dash", "–": "en dash"}


class Refused(Exception):
    """A payload that must not reach the board."""


def find_array(src, name):
    """Return (start, end, body) for `const NAME=[ ... ];` at top level."""
    open_pat = "const %s=[\n" % name
    i = src.find(open_pat)
    if i < 0:
        raise Refused("could not find `const %s=[` in the source" % name)
    body_start = i + len(open_pat)
    end = src.find("\n];", body_start)
    if end < 0:
        raise Refused("`const %s=[` is never closed with `];`" % name)
    return body_start, end, src[body_start:end]


def split_rows(body, array_name):
    """Split an array body into one (text, parsed) pair per row line.

    Each row sits on its own line. Keeping the original text lets untouched
    rows survive a sweep byte-for-byte, so the diff shows only real changes.
    """
    rows = []
    for lineno, line in enumerate(body.split("\n"), 1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("/*") or stripped.startswith("//"):
            raise Refused("%s line %d is a comment inside the array; "
                          "this script cannot safely rewrite that" % (array_name, lineno))
        text = stripped[:-1] if stripped.endswith(",") else stripped
        try:
            parsed = json.loads(text)
        except ValueError as exc:
            raise Refused("%s line %d is not valid JSON: %s" % (array_name, lineno, exc))
        if not isinstance(parsed, list):
            raise Refused("%s line %d is not an array" % (array_name, lineno))
        rows.append({"text": text, "row": parsed})
    return rows


def check_no_dashes(where, value):
    if not isinstance(value, str):
        return
    for ch, label in DASHES.items():
        if ch in value:
            raise Refused("%s contains an %s, which hard rule 4 forbids. "
                          "Use a comma, a semicolon, or two sentences." % (where, label))


def validate_row(kind, row, index):
    spec = SPEC[kind]
    fields = spec["fields"]
    where = "new %s row %d" % (kind, index + 1)

    if not isinstance(row, list):
        raise Refused("%s is not an array" % where)
    if len(row) != len(fields):
        raise Refused("%s has %d fields, expected exactly %d (%s)"
                      % (where, len(row), len(fields), ", ".join(fields)))
    for pos, value in enumerate(row):
        if not isinstance(value, str):
            raise Refused("%s field `%s` is %s, every field must be a string"
                          % (where, fields[pos], type(value).__name__))
        check_no_dashes("%s field `%s`" % (where, fields[pos]), value)

    get = lambda name: row[fields.index(name)]

    if kind in ("int", "sch"):
        if get("conviction") not in CONVICTION:
            raise Refused("%s conviction is %r, must be one of %s"
                          % (where, get("conviction"), sorted(CONVICTION)))
        if get("status") not in STATUS:
            raise Refused("%s status is %r, must be one of %s"
                          % (where, get("status"), sorted(STATUS)))
        deadline = get("deadline")
        if deadline and not DATE_RE.match(deadline):
            raise Refused("%s deadline is %r, must be YYYY-MM-DD or empty" % (where, deadline))

        slug = row[spec["slug_at"]]
        if not slug:
            raise Refused("%s has no slug. Every row needs a stable slug; "
                          "applied state is keyed on it." % where)
        if not SLUG_RE.match(slug):
            raise Refused("%s slug %r must be lowercase [a-z0-9-] only" % (where, slug))
        if not slug.startswith(spec["prefix"]):
            raise Refused("%s slug %r must start with %r" % (where, slug, spec["prefix"]))
        if not get("url"):
            raise Refused("%s has no url" % where)


def serialize(row):
    return json.dumps(row, ensure_ascii=False)


def apply_payload(src, payload):
    """Return (new_src, report). Pure; does no IO."""
    report = {"new": [], "patched": [], "cal": []}

    # Read every array up front so a failure anywhere leaves the file untouched.
    arrays = {}
    for kind, spec in SPEC.items():
        start, end, body = find_array(src, spec["array"])
        arrays[kind] = {"start": start, "end": end,
                        "rows": split_rows(body, spec["array"]), "dirty": False}

    # Existing slugs, so a new row cannot collide and a patch cannot miss.
    existing = {}
    for kind in ("int", "sch"):
        at = SPEC[kind]["slug_at"]
        for entry in arrays[kind]["rows"]:
            slug = entry["row"][at] if len(entry["row"]) > at else ""
            if slug:
                existing.setdefault(kind, {})[slug] = entry

    # ---- new rows -------------------------------------------------------
    seen_in_payload = set()
    for kind in ("int", "sch", "out"):
        for i, row in enumerate(payload.get("new", {}).get(kind, [])):
            validate_row(kind, row, i)
            if kind in ("int", "sch"):
                slug = row[SPEC[kind]["slug_at"]]
                if slug in seen_in_payload:
                    raise Refused("slug %r appears twice in this payload" % slug)
                seen_in_payload.add(slug)
                if slug in existing.get(kind, {}):
                    raise Refused(
                        "slug %r already exists on the board. A new row cannot "
                        "reuse it. To change an existing row use `patch`, which "
                        "sets named fields and leaves the rest alone." % slug)
                report["new"].append((kind, slug, row[1], row[2] if kind == "int" else row[3]))
            else:
                report["new"].append((kind, "", row[1], row[2]))
            arrays[kind]["rows"].append({"text": serialize(row), "row": row})
            arrays[kind]["dirty"] = True

    # ---- patches to existing rows ---------------------------------------
    for i, patch in enumerate(payload.get("patch", [])):
        if not isinstance(patch, dict):
            raise Refused("patch %d is not an object" % (i + 1))
        kind = patch.get("kind", "int")
        if kind not in ("int", "sch"):
            raise Refused("patch %d has kind %r, expected int or sch" % (i + 1, kind))
        slug = patch.get("slug", "")
        entry = existing.get(kind, {}).get(slug)
        if entry is None:
            raise Refused("patch %d targets slug %r, which is not on the board. "
                          "A patch never creates a row." % (i + 1, slug))
        sets = patch.get("set", {})
        if not isinstance(sets, dict) or not sets:
            raise Refused("patch %d for %r sets nothing" % (i + 1, slug))

        fields = SPEC[kind]["fields"]
        row = list(entry["row"])
        changed = []
        for name, value in sets.items():
            if name == "slug":
                raise Refused("patch %d tries to change the slug of %r. Slugs are "
                              "permanent; applied state is keyed on them." % (i + 1, slug))
            if name not in fields:
                raise Refused("patch %d for %r sets unknown field %r. Known fields: %s"
                              % (i + 1, slug, name, ", ".join(fields)))
            if not isinstance(value, str):
                raise Refused("patch %d for %r sets %s to a %s, must be a string"
                              % (i + 1, slug, name, type(value).__name__))
            check_no_dashes("patch %d field `%s`" % (i + 1, name), value)
            if name == "conviction" and value not in CONVICTION:
                raise Refused("patch %d sets conviction to %r" % (i + 1, value))
            if name == "status" and value not in STATUS:
                raise Refused("patch %d sets status to %r" % (i + 1, value))
            if name == "deadline" and value and not DATE_RE.match(value):
                raise Refused("patch %d sets deadline to %r, must be YYYY-MM-DD" % (i + 1, value))
            pos = fields.index(name)
            if row[pos] != value:
                changed.append((name, row[pos], value))
                row[pos] = value
        if changed:
            entry["text"] = serialize(row)
            entry["row"] = row
            arrays[kind]["dirty"] = True
            report["patched"].append((slug, changed))

    # ---- CAL freshness stamps -------------------------------------------
    cal_updates = payload.get("cal", [])
    if cal_updates:
        start, end, body = find_array(src, "CAL")
        cal_rows = split_rows(body, "CAL")
        by_name = {}
        for entry in cal_rows:
            if len(entry["row"]) > 1:
                by_name[entry["row"][1]] = entry
        dirty = False
        for i, upd in enumerate(cal_updates):
            if not isinstance(upd, dict):
                raise Refused("cal update %d is not an object" % (i + 1))
            name = upd.get("name", "")
            entry = by_name.get(name)
            if entry is None:
                raise Refused("cal update %d names %r, which is not in CAL. "
                              "A sweep stamps existing calendar rows, it does not add them."
                              % (i + 1, name))
            row = list(entry["row"])
            changed = []
            for field, value in upd.items():
                if field == "name":
                    continue
                if field not in CAL_FIELDS:
                    raise Refused("cal update %d sets unknown field %r" % (i + 1, field))
                if not isinstance(value, str):
                    raise Refused("cal update %d sets %s to a non-string" % (i + 1, field))
                check_no_dashes("cal update %d field `%s`" % (i + 1, field), value)
                if field in ("date", "lastChecked") and value and not DATE_RE.match(value):
                    raise Refused("cal update %d sets %s to %r, must be YYYY-MM-DD"
                                  % (i + 1, field, value))
                pos = CAL_FIELDS.index(field)
                if row[pos] != value:
                    changed.append((field, row[pos], value))
                    row[pos] = value
            if changed:
                entry["text"] = serialize(row)
                entry["row"] = row
                dirty = True
                report["cal"].append((name, changed))
        if dirty:
            arrays["cal"] = {"start": start, "end": end, "rows": cal_rows, "dirty": True}

    # ---- splice back, last array first so offsets stay valid -------------
    out = src
    for kind in sorted(arrays, key=lambda k: arrays[k]["start"], reverse=True):
        block = arrays[kind]
        if not block["dirty"]:
            continue
        body = ",\n".join(entry["text"] for entry in block["rows"])
        out = out[:block["start"]] + body + out[block["end"]:]

    return out, report


def assert_state_untouched(before, after):
    """The applied ticks must come through a sweep completely unchanged."""
    pat = re.compile(re.escape("/*ACC-STATE*/") + r"(.*?)" + re.escape("/*/ACC-STATE*/"), re.S)
    a, b = pat.search(before), pat.search(after)
    if not a or not b:
        raise Refused("the ACC-STATE markers are missing after the merge")
    if a.group(1) != b.group(1):
        raise Refused("the merge changed the applied-state block. Rule 10: never "
                      "touch his ticks.")
    counts = [re.search(r'"count":(\d+)', g.group(1)) for g in (a, b)]
    if counts[0] and counts[1] and counts[0].group(1) != counts[1].group(1):
        raise Refused("the applied tick count changed from %s to %s"
                      % (counts[0].group(1), counts[1].group(1)))
    for marker in ("<!--ACC-HEAD-->", "<!--/ACC-HEAD-->", "<!--ACC-BODY-->", "<!--/ACC-BODY-->"):
        if after.count(marker) != 1:
            raise Refused("marker %s appears %d times after the merge, expected exactly 1"
                          % (marker, after.count(marker)))


def main():
    ap = argparse.ArgumentParser(description="Merge a sweep payload into the dashboard.")
    ap.add_argument("payload", help="JSON file emitted by a sweep agent")
    ap.add_argument("-d", "--dashboard", default="application-command-center.html")
    ap.add_argument("-o", "--out", default=None, help="defaults to editing in place")
    ap.add_argument("--apply", action="store_true", help="write the change; otherwise preview only")
    args = ap.parse_args()

    with open(args.payload, encoding="utf-8") as fh:
        try:
            payload = json.load(fh)
        except ValueError as exc:
            print("REFUSED: the payload is not valid JSON: %s" % exc, file=sys.stderr)
            return 2
    with open(args.dashboard, encoding="utf-8") as fh:
        src = fh.read()

    try:
        out, report = apply_payload(src, payload)
        assert_state_untouched(src, out)
    except Refused as exc:
        print("REFUSED: %s" % exc, file=sys.stderr)
        return 2

    n_new, n_patch, n_cal = len(report["new"]), len(report["patched"]), len(report["cal"])
    print("%d new, %d updated, %d calendar stamps" % (n_new, n_patch, n_cal))
    for kind, slug, a, b in report["new"]:
        print("  + [%s] %s | %s" % (kind, a, b))
        if slug:
            print("      slug %s" % slug)
    for slug, changed in report["patched"]:
        print("  ~ %s" % slug)
        for name, old, new in changed:
            trim = lambda s: (s[:60] + "...") if len(s) > 60 else s
            print("      %s: %r -> %r" % (name, trim(old), trim(new)))
    for name, changed in report["cal"]:
        print("  @ %s" % name)
        for field, old, new in changed:
            print("      %s: %r -> %r" % (field, old, new))

    if not (n_new or n_patch or n_cal):
        print("\nNothing to do.")
        return 0

    if not args.apply:
        print("\nPreview only. Nothing written. Re-run with --apply to commit,")
        print("then run dashboard/verify/run.sh before publishing.")
        return 0

    target = args.out or args.dashboard
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(out)
    print("\nWrote %s (%d bytes). Now run dashboard/verify/run.sh on it." % (target, len(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
