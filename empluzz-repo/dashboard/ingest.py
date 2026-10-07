#!/usr/bin/env python3
"""Merge a sweep payload into a tracker build. Preview by default, write on --apply.

    python3 dashboard/ingest.py <payload.json> --build <build.html>
    python3 dashboard/ingest.py <payload.json> --build <build.html> --apply [--out <file>]

The build is the reconstruction of a FRESH read of the live artifact
(dashboard/verify/mkbase2.py), never the null-state file committed in dashboard/,
or the applied ticks go to null on publish. Without --out, --apply rewrites the
build in place.

Payload, written by the internship-sweep or scholarship-sweep agent:

    {
      "kind": "int",                       # or "sch"
      "swept": "2026-10-07",               # the day the sweep ran
      "label": "web and Indeed, Oct 7",    # short, goes in the CAL row name
      "summary": "what was searched, what answered, what did not",
      "new":    [ {<named fields>}, ... ],
      "update": [ {"slug": "...", "set": {<named fields>}, "append_note": "..."}, ... ],
      "screen_out": [ {"name": "...", "role": "...", "reason": "..."}, ... ]
    }

Named fields for an internship row (INT):
    conviction company role location term deadline source url packet notes status hint wage slug
and for a scholarship row (SCH):
    conviction name sponsor award opens deadline gate url packet notes status hint slug

Rules it enforces, and refuses the whole payload on any one of them:
  * a known kind, a real swept date, no unknown keys anywhere
  * every new row carries every field (empty string is allowed where noted),
    a conviction and status the board knows, and a new slug that matches
    ^int-[a-z0-9-]+$ or ^sch-[a-z0-9-]+$, unique across both tabs
  * an update names a slug that exists on that tab and never changes a slug
  * deadlines are YYYY-MM-DD or empty, urls are http(s)
  * no em dash or en dash in any string (CLAUDE.md hard rule 4)
  * the ACC-STATE block, which holds his applied ticks, is byte identical
    before and after, and every document marker still appears exactly once

Warnings, which print but do not refuse: a new row whose company and role look
like an existing row or a Screened Out row, and an out of state new internship
whose notes never say SILENT, EXPLICITLY, CONFIRMED or a housing word, because
CLAUDE.md rule 6 wants that stated on every such row.

Exit codes: 0 clean, 1 clean with warnings, 2 refused. Nothing is written
unless --apply is given and the exit would be 0 or 1.
"""
import argparse, datetime, json, re, sys

INT_FIELDS = ["conviction", "company", "role", "location", "term", "deadline", "source",
              "url", "packet", "notes", "status", "hint", "wage", "slug"]
SCH_FIELDS = ["conviction", "name", "sponsor", "award", "opens", "deadline", "gate",
              "url", "packet", "notes", "status", "hint", "slug"]
FIELDS = {"int": INT_FIELDS, "sch": SCH_FIELDS}
ARRAY = {"int": "INT", "sch": "SCH"}
# Fields a new row may leave as an empty string. Everything else must say something.
MAY_BE_EMPTY = {"deadline", "hint", "wage", "opens"}
CONVICTIONS = {"MUST APPLY", "STRONG", "STRETCH", "WATCH", "CLOSED"}
STATUSES = {"OPEN", "NOTYET", "UNCONFIRMED", "BLOCKED", "CLOSED"}
PACKETS = {"Not started", "Ready", "Done", "Blocked", "Deadline passed"}
SLUG_RE = {"int": re.compile(r"^int-[a-z0-9]+(-[a-z0-9]+)*$"),
           "sch": re.compile(r"^sch-[a-z0-9]+(-[a-z0-9]+)*$")}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Built from codepoints so this file carries none of the characters it bans.
DASHES = (chr(0x2014), chr(0x2013))
MARKERS = ["<!--ACC-HEAD-->", "<!--/ACC-HEAD-->", "<!--ACC-BODY-->", "<!--/ACC-BODY-->",
           "/*ACC-STATE*/", "/*/ACC-STATE*/"]
TOP_KEYS = {"kind", "swept", "label", "summary", "new", "update", "screen_out"}
HOUSING_WORDS = re.compile(r"SILENT|EXPLICITLY|CONFIRMED|housing|relocation|LOCAL", re.I)


class Refuse(Exception):
    pass


def real_date(s):
    if not isinstance(s, str) or not DATE_RE.match(s):
        return False
    try:
        datetime.date.fromisoformat(s)
        return True
    except ValueError:
        return False


# ---- reading the build ---------------------------------------------------

def array_span(src, name):
    """Return (start, end) of the text between 'const NAME=[' and its closing '];'."""
    head = "const %s=[" % name
    a = src.find(head)
    if a < 0 or src.find(head, a + 1) >= 0:
        raise Refuse("expected exactly one '%s' in the build" % head)
    a += len(head)
    b = src.find("\n];", a)
    if b < 0:
        raise Refuse("could not find the end of %s" % name)
    return a, b


def parse_array(src, name):
    """One row per line is the board's format. Refuse anything else rather than guess."""
    a, b = array_span(src, name)
    rows = []
    for ln in src[a:b].split("\n"):
        t = ln.strip()
        if not t:
            continue
        if t.endswith(","):
            t = t[:-1]
        try:
            r = json.loads(t)
        except ValueError:
            raise Refuse("%s holds a line that is not one JSON row: %s" % (name, t[:80]))
        if not isinstance(r, list):
            raise Refuse("%s holds a non-array line" % name)
        rows.append(r)
    return rows


def render_array(rows):
    return "\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n"


def replace_array(src, name, rows):
    a, b = array_span(src, name)
    return src[:a] + render_array(rows) + src[b:]


def state_block(src):
    a, b = src.find("/*ACC-STATE*/"), src.find("/*/ACC-STATE*/")
    if a < 0 or b <= a:
        raise Refuse("ACC-STATE block not found, refusing to touch a build without his ticks")
    return src[a:b]


def tick_count(src):
    m = re.search(r'"applied":(\{.*?\}|null)', state_block(src))
    if not m or m.group(1) == "null":
        return None
    return len(json.loads(m.group(1)))


# ---- validation ------------------------------------------------------------

def no_dashes(where, value):
    if isinstance(value, str) and any(d in value for d in DASHES):
        raise Refuse("%s contains an em or en dash; use a comma, semicolon or two sentences" % where)


def check_keys(where, obj, allowed):
    extra = set(obj) - set(allowed)
    if extra:
        raise Refuse("%s has unknown keys: %s" % (where, ", ".join(sorted(extra))))


def check_field(kind, where, key, val):
    if not isinstance(val, str):
        raise Refuse("%s.%s must be a string" % (where, key))
    no_dashes("%s.%s" % (where, key), val)
    if key == "conviction" and val not in CONVICTIONS:
        raise Refuse("%s.conviction '%s' is not one of %s" % (where, val, sorted(CONVICTIONS)))
    if key == "status" and val not in STATUSES:
        raise Refuse("%s.status '%s' is not one of %s" % (where, val, sorted(STATUSES)))
    if key == "packet" and val not in PACKETS:
        raise Refuse("%s.packet '%s' is not one of %s" % (where, val, sorted(PACKETS)))
    if key == "deadline" and val and not real_date(val):
        raise Refuse("%s.deadline '%s' must be YYYY-MM-DD or empty" % (where, val))
    if key == "url" and not re.match(r"^https?://", val):
        raise Refuse("%s.url must start with http:// or https://" % where)
    if key == "wage" and val and "/hr" not in val:
        raise Refuse("%s.wage '%s' must be an hourly figure like $24-30/hr, or empty" % (where, val))


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def validate(payload, src):
    if not isinstance(payload, dict):
        raise Refuse("payload must be a JSON object")
    check_keys("payload", payload, TOP_KEYS)
    kind = payload.get("kind")
    if kind not in FIELDS:
        raise Refuse("kind must be 'int' or 'sch'")
    if not real_date(payload.get("swept")):
        raise Refuse("swept must be a real YYYY-MM-DD date")
    for k in ("label", "summary"):
        if not isinstance(payload.get(k), str) or not payload[k].strip():
            raise Refuse("%s must be a non-empty string" % k)
        no_dashes(k, payload[k])
    new = payload.get("new", [])
    upd = payload.get("update", [])
    out = payload.get("screen_out", [])
    for k, v in (("new", new), ("update", upd), ("screen_out", out)):
        if not isinstance(v, list):
            raise Refuse("%s must be a list" % k)

    fields = FIELDS[kind]
    rows = {"int": parse_array(src, "INT"), "sch": parse_array(src, "SCH")}
    for k, n in (("int", 14), ("sch", 13)):
        bad = [r for r in rows[k] if len(r) != n]
        if bad:
            raise Refuse("existing %s rows are not all %d fields; the build is not one this script knows" % (ARRAY[k], n))
    existing = {r[-1] for r in rows["int"]} | {r[-1] for r in rows["sch"]}
    out_rows = parse_array(src, "OUT")
    warns = []

    seen = set()
    for i, r in enumerate(new):
        where = "new[%d]" % i
        if not isinstance(r, dict):
            raise Refuse("%s must be an object of named fields" % where)
        check_keys(where, r, fields)
        missing = [f for f in fields if f not in r]
        if missing:
            raise Refuse("%s is missing %s" % (where, ", ".join(missing)))
        for f in fields:
            check_field(kind, where, f, r[f])
            if f not in MAY_BE_EMPTY and not r[f].strip():
                raise Refuse("%s.%s may not be empty" % (where, f))
        sl = r["slug"]
        if not SLUG_RE[kind].match(sl):
            raise Refuse("%s.slug '%s' must match %s" % (where, sl, SLUG_RE[kind].pattern))
        if sl in existing:
            raise Refuse("%s.slug '%s' already exists; send it as an update instead" % (where, sl))
        if sl in seen:
            raise Refuse("%s.slug '%s' appears twice in the payload" % (where, sl))
        seen.add(sl)
        who = r.get("company", r.get("name"))
        key = (norm(who), norm(r.get("role", r.get("sponsor", ""))))
        for er in rows[kind]:
            if (norm(er[1]), norm(er[2])) == key:
                warns.append("%s looks like existing row %s (%s, %s). Never consolidate, but confirm it is a different requisition." % (where, er[-1], er[1], er[2]))
        for o in out_rows:
            if len(o) >= 3 and norm(o[1]) == norm(who) and norm(o[2]) == key[1]:
                warns.append("%s matches a Screened Out row for %s. Only resurface it if the screen out reason is spent, and say so in the notes." % (where, o[1]))
        if kind == "int" and "LOCAL" not in r["notes"] and ", CO" not in r["location"] and not HOUSING_WORDS.search(r["notes"]):
            warns.append("%s (%s) looks out of state and its notes never state the housing position. CLAUDE.md rule 6 wants SILENT or EXPLICITLY refuses said plainly." % (where, who))

    by_slug = {r[-1]: r for r in rows[kind]}
    useen = set()
    for i, u in enumerate(upd):
        where = "update[%d]" % i
        if not isinstance(u, dict):
            raise Refuse("%s must be an object" % where)
        check_keys(where, u, {"slug", "set", "append_note"})
        sl = u.get("slug")
        if sl not in by_slug:
            raise Refuse("%s.slug '%s' is not a row on the %s tab" % (where, sl, ARRAY[kind]))
        if sl in useen:
            raise Refuse("%s.slug '%s' is updated twice; fold them into one update" % (where, sl))
        useen.add(sl)
        st = u.get("set", {})
        if not isinstance(st, dict):
            raise Refuse("%s.set must be an object" % where)
        check_keys(where + ".set", st, [f for f in fields if f != "slug"])
        if "slug" in u.get("set", {}):
            raise Refuse("%s tries to change a slug; slugs never change" % where)
        for f, v in st.items():
            check_field(kind, where + ".set", f, v)
            if f not in MAY_BE_EMPTY and not v.strip():
                raise Refuse("%s.set.%s may not be empty" % (where, f))
        an = u.get("append_note", "")
        if not isinstance(an, str):
            raise Refuse("%s.append_note must be a string" % where)
        no_dashes(where + ".append_note", an)
        if not st and not an.strip():
            raise Refuse("%s changes nothing" % where)

    for i, o in enumerate(out):
        where = "screen_out[%d]" % i
        if not isinstance(o, dict):
            raise Refuse("%s must be an object" % where)
        check_keys(where, o, {"name", "role", "reason"})
        for f in ("name", "role", "reason"):
            if not isinstance(o.get(f), str) or not o[f].strip():
                raise Refuse("%s.%s must be a non-empty string" % (where, f))
            no_dashes("%s.%s" % (where, f), o[f])

    return kind, rows, out_rows, warns


# ---- merge -----------------------------------------------------------------

def merge(payload, src):
    kind, rows, out_rows, warns = validate(payload, src)
    fields = FIELDS[kind]
    before_state = state_block(src)
    before_ticks = tick_count(src)
    target = [list(r) for r in rows[kind]]
    idx = {r[-1]: i for i, r in enumerate(target)}
    changes = []

    for u in payload.get("update", []):
        r = target[idx[u["slug"]]]
        for f, v in u.get("set", {}).items():
            j = fields.index(f)
            if r[j] != v:
                changes.append("  ~ %s  %s: %r -> %r" % (u["slug"], f, r[j][:60], v[:60]))
                r[j] = v
        an = u.get("append_note", "").strip()
        if an:
            j = fields.index("notes")
            r[j] = (r[j].rstrip() + "  " + an).strip()
            changes.append("  ~ %s  notes: + %r" % (u["slug"], an[:90]))

    for r in payload.get("new", []):
        target.append([r[f] for f in fields])
        changes.append("  + %s  %s, %s  [%s, %s]" % (r["slug"], r[fields[1]], r[fields[2]], r["conviction"], r["status"]))

    out_new = list(out_rows)
    typ = "Internship" if kind == "int" else "Scholarship"
    for o in payload.get("screen_out", []):
        out_new.append([typ, o["name"], o["role"], payload["swept"], o["reason"]])
        changes.append("  - screened out  %s, %s" % (o["name"], o["role"]))

    cal = parse_array(src, "CAL")
    next_check = (datetime.date.fromisoformat(payload["swept"]) + datetime.timedelta(days=14)).isoformat()
    n_new, n_upd, n_out = len(payload.get("new", [])), len(payload.get("update", [])), len(payload.get("screen_out", []))
    cal_note = "%s Ingested by dashboard/ingest.py: %d new, %d updated, %d screened out." % (
        payload["summary"].strip(), n_new, n_upd, n_out)
    cal.append([typ, "%s sweep (%s)" % (typ, payload["label"].strip()), "A", "Continuous",
                next_check, "PENDING", payload["swept"], cal_note])
    changes.append("  * Calendar row stamped %s, so the header SWEPT date moves" % payload["swept"])

    out_src = replace_array(src, ARRAY[kind], target)
    out_src = replace_array(out_src, "OUT", out_new)
    out_src = replace_array(out_src, "CAL", cal)

    # Gates on the result, independent of the logic above.
    if state_block(out_src) != before_state:
        raise Refuse("the ACC-STATE block changed; his applied ticks must never move")
    if tick_count(out_src) != before_ticks:
        raise Refuse("the applied tick count changed")
    for m in MARKERS:
        if out_src.count(m) != 1:
            raise Refuse("marker %s appears %d times after the merge" % (m, out_src.count(m)))
    check = parse_array(out_src, ARRAY[kind])
    if len(check) != len(rows[kind]) + n_new:
        raise Refuse("row count after the merge is not the row count before plus the new rows")
    slugs = [r[-1] for r in parse_array(out_src, "INT")] + [r[-1] for r in parse_array(out_src, "SCH")]
    if len(slugs) != len(set(slugs)):
        raise Refuse("the merge produced a duplicate slug")

    summary = {"kind": kind, "new": n_new, "updated": n_upd, "screened_out": n_out,
               "rows_before": len(rows[kind]), "rows_after": len(check), "ticks": before_ticks}
    return out_src, changes, warns, summary


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("payload")
    ap.add_argument("--build", required=True,
                    help="reconstruction of a fresh live read, from dashboard/verify/mkbase2.py")
    ap.add_argument("--apply", action="store_true", help="write the merged build")
    ap.add_argument("--out", help="write here instead of rewriting --build in place")
    a = ap.parse_args()
    try:
        with open(a.payload, encoding="utf-8") as fh:
            try:
                payload = json.load(fh)
            except ValueError as e:
                raise Refuse("payload is not valid JSON: %s" % e)
        with open(a.build, encoding="utf-8") as fh:
            src = fh.read()
        if tick_count(src) is None:
            raise Refuse("this build carries applied:null. Ingest into a reconstruction of a fresh live read, never the committed null-state file")
        merged, changes, warns, s = merge(payload, src)
    except Refuse as e:
        print("REFUSED: %s" % e)
        print("Nothing was written.")
        sys.exit(2)

    print("%s sweep payload: %d new, %d updated, %d screened out. %s rows %d -> %d. Applied ticks %d, untouched." % (
        "Internship" if s["kind"] == "int" else "Scholarship", s["new"], s["updated"], s["screened_out"],
        ARRAY[s["kind"]], s["rows_before"], s["rows_after"], s["ticks"]))
    print("\n".join(changes))
    for w in warns:
        print("WARN: " + w)
    if a.apply:
        dest = a.out or a.build
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(merged)
        print("Applied. Wrote %s (%d chars)." % (dest, len(merged)))
    else:
        print("Preview only. Re-run with --apply to write it.")
    sys.exit(1 if warns else 0)


if __name__ == "__main__":
    main()
