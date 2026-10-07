#!/usr/bin/env python3
"""Tests for dashboard/ingest.py. Run: python3 dashboard/verify/test_ingest.py

Fixture: the committed null-state build with a real looking applied block put
back in, because ingest refuses a null-state build on purpose. Every refusal
case must leave the build untouched and exit 2."""
import glob, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DASH = os.path.dirname(HERE)
INGEST = os.path.join(DASH, "ingest.py")
BUILD = sorted(glob.glob(os.path.join(DASH, "application-command-center-*.html")),
               key=os.path.getmtime)[-1]
TICKS = {"int-medtronic-engineering-intern": "2026-08-17", "int-spacex-eng-intern": "2026-08-17"}

passed = failed = 0


def check(name, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print("  PASS  " + name)
    else:
        failed += 1
        print("  FAIL  " + name + ("  " + detail if detail else ""))


def fixture(tmp):
    src = open(BUILD, encoding="utf-8").read()
    assert '"applied":null' in src, "expected the committed build to be null-state"
    src = src.replace('"applied":null', '"applied":' + json.dumps(TICKS, separators=(",", ":")), 1)
    p = os.path.join(tmp, "build.html")
    open(p, "w", encoding="utf-8").write(src)
    return p


def run(tmp, payload, build, *extra):
    pp = os.path.join(tmp, "payload.json")
    open(pp, "w", encoding="utf-8").write(payload if isinstance(payload, str) else json.dumps(payload))
    r = subprocess.run([sys.executable, INGEST, pp, "--build", build] + list(extra),
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def js_arrays(path):
    """Evaluate INT, SCH, CAL and OUT the way the browser will."""
    js = r"""
const fs=require("fs");const s=fs.readFileSync(process.argv[1],"utf8");
const g=n=>{const h="const "+n+"=[";const a=s.indexOf(h);const b=s.indexOf("\n];",a);
  return eval(s.slice(a+h.length-1,b+2))};
console.log(JSON.stringify({INT:g("INT"),SCH:g("SCH"),CAL:g("CAL"),OUT:g("OUT")}));"""
    r = subprocess.run(["node", "-e", js, path], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else None


def new_row(slug="int-test-co-me-intern", **kw):
    r = {"conviction": "STRONG", "company": "Test Co", "role": "Mechanical Engineering Intern",
         "location": "Denver, CO", "term": "Summer 2027", "deadline": "", "source": "Indeed",
         "url": "https://example.com/job/1", "packet": "Not started",
         "notes": "LOCAL. Posting read 2026-10-07. Housing SILENT and irrelevant locally.",
         "status": "OPEN", "hint": "", "wage": "$27-30/hr", "slug": slug}
    r.update(kw)
    return r


def base(**kw):
    p = {"kind": "int", "swept": "2026-10-07", "label": "test, Oct 7",
         "summary": "Test sweep.", "new": [new_row()], "update": [], "screen_out": []}
    p.update(kw)
    return p


def main():
    tmp = tempfile.mkdtemp(prefix="ingest-test-")
    b = fixture(tmp)
    orig = open(b, encoding="utf-8").read()
    before = js_arrays(b)
    check("fixture evaluates in node", before is not None)
    first = before["INT"][0][13]

    code, out = run(tmp, base(), b)
    check("preview of a clean payload exits 0", code == 0, out)
    check("preview writes nothing", open(b, encoding="utf-8").read() == orig)
    check("preview names the new slug", "int-test-co-me-intern" in out)

    upd = {"slug": first, "set": {"hint": "checked Oct 7"}, "append_note": "RECHECKED 2026-10-07."}
    p = base(update=[upd], screen_out=[{"name": "Nope Inc", "role": "Intern", "reason": "Wrong term."}])
    outp = os.path.join(tmp, "merged.html")
    code, out = run(tmp, p, b, "--apply", "--out", outp)
    check("apply exits 0", code == 0, out)
    after = js_arrays(outp)
    check("merged build still evaluates in node", after is not None)
    if after:
        check("one INT row added", len(after["INT"]) == len(before["INT"]) + 1)
        check("SCH untouched", after["SCH"] == before["SCH"])
        check("new row lands with all 14 fields", after["INT"][-1][13] == "int-test-co-me-intern" and len(after["INT"][-1]) == 14)
        r0 = [r for r in after["INT"] if r[13] == first][0]
        check("update set the hint", r0[11] == "checked Oct 7")
        check("update appended the note", r0[9].endswith("RECHECKED 2026-10-07."))
        check("other existing rows byte identical", after["INT"][1:-1] == before["INT"][1:])
        check("Calendar row stamped with the swept date", after["CAL"][-1][6] == "2026-10-07" and len(after["CAL"]) == len(before["CAL"]) + 1)
        check("Screened Out row added", after["OUT"][-1][1] == "Nope Inc" and after["OUT"][-1][3] == "2026-10-07")
    m = open(outp, encoding="utf-8").read()
    st = lambda s: s[s.find("/*ACC-STATE*/"):s.find("/*/ACC-STATE*/")]
    check("state block byte identical", st(m) == st(orig))
    check("--out left the input build alone", open(b, encoding="utf-8").read() == orig)

    refusals = [
        ("existing slug as new", base(new=[new_row(slug=first)])),
        ("duplicate slug in payload", base(new=[new_row(), new_row()])),
        ("bad slug shape", base(new=[new_row(slug="Int_Bad")])),
        ("sch slug on int tab", base(new=[new_row(slug="sch-wrong-tab")])),
        ("em dash in notes", base(new=[new_row(notes="LOCAL " + chr(0x2014) + " fine")])),
        ("unknown status", base(new=[new_row(status="MAYBE")])),
        ("unknown conviction", base(new=[new_row(conviction="GREAT")])),
        ("bad deadline", base(new=[new_row(deadline="Oct 1")])),
        ("non hourly wage", base(new=[new_row(wage="$50,000/yr")])),
        ("missing field", base(new=[{k: v for k, v in new_row().items() if k != "url"}])),
        ("empty required field", base(new=[new_row(company=" ")])),
        ("unknown key", base(new=[new_row(extra="x")])),
        ("update to a slug that does not exist", base(new=[], update=[{"slug": "int-nope", "append_note": "x"}])),
        ("update that changes a slug", base(new=[], update=[{"slug": first, "set": {"slug": "int-new"}}])),
        ("update that changes nothing", base(new=[], update=[{"slug": first}])),
        ("bad kind", base(kind="both")),
        ("impossible date", base(swept="2026-02-30")),
        ("malformed JSON", "{not json"),
    ]
    for name, p in refusals:
        code, out = run(tmp, p, b, "--apply")
        check("refuses: " + name, code == 2 and "REFUSED" in out, out.strip()[:120])
    check("no refusal touched the build", open(b, encoding="utf-8").read() == orig)

    nb = os.path.join(tmp, "null.html")
    open(nb, "w", encoding="utf-8").write(open(BUILD, encoding="utf-8").read())
    code, out = run(tmp, base(), nb, "--apply")
    check("refuses a null-state build", code == 2 and "applied:null" in out, out)

    code, out = run(tmp, base(new=[new_row(slug="int-test-oos", location="Austin, TX", notes="Good work.")]), b)
    check("warns, exit 1, on an out of state row with no housing line", code == 1 and "WARN" in out, out)
    dup = before["INT"][0]
    code, out = run(tmp, base(new=[new_row(slug="int-test-dupe", company=dup[1], role=dup[2])]), b)
    check("warns on a likely duplicate requisition", code == 1 and "looks like existing row" in out, out)

    print("\ntest_ingest.py: %d passed, %d failed, %d assertions" % (passed, failed, passed + failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
