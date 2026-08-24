#!/usr/bin/env python3
"""Render a letter as HTML that Google Drive converts into a native Google Doc
carrying Joaquin's house format.

    python3 scripts/build_letter_html.py spec.json
    python3 scripts/build_letter_html.py spec.json --allow 1965

Upload the result with create_file(contentMimeType='text/html',
textContent=<this output>) and DO NOT set disableConversionToGoogleType.
Leaving conversion on is what makes Drive produce a real Google Doc.

spec.json:
    {
      "out": "/tmp/Cover Letter - Company.html",
      "date": "August 24, 2026",
      "hiring_team": "Acme Summer 2027 Internship Hiring Team",
      "paragraphs": ["body 1", "body 2", "body 3", "body 4", "closing"],
      "kind": "letter"          # or "essay"; optional, defaults to letter
    }

Identity, house format and the letter gate all come from config/, so nothing
about Joaquin is hardcoded here. The gate runs before anything is written: a
blocking finding means no file, by design. There is no bypass flag.
"""
import sys, os, json, html, argparse, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def load_profile():
    with open(os.path.join(ROOT, "config", "profile.json"), encoding="utf-8") as fh:
        return json.load(fh)

def styles(hf):
    font = f"font-family:{hf['font']};font-size:{hf['size']};"
    return {
        "p":     font + f"margin:0 0 {hf['space_after']} 0;text-align:left;",
        "ctr":   font + "margin:0;text-align:center;",
        "ctr2":  font + f"margin:0 0 {hf['contact_space_after']} 0;text-align:center;",
    }

def build(profile, date_line, hiring_team, paragraphs):
    hf, ident = profile["house_format"], profile["identity"]
    lo, hi = hf["paragraphs_min"], hf["paragraphs_max"]
    if not lo <= len(paragraphs) <= hi:
        raise ValueError(
            f"expected {lo} to {hi} paragraphs (body plus closing), got {len(paragraphs)}")

    s, e = styles(hf), html.escape
    out = ['<html><head><meta charset="utf-8"></head><body>']
    out.append(f'<p style="{s["ctr"]}"><b>{e(ident["name"])}</b></p>')
    out.append(
        f'<p style="{s["ctr2"]}">{e(ident["city"])}&nbsp; |&nbsp; {e(ident["phone"])}'
        f'&nbsp; | {e(ident["email"])}&nbsp; |&nbsp; '
        f'<a href="{e(ident["linkedin_url"])}">{e(ident["linkedin_text"])}</a></p>')
    out.append(f'<p style="{s["p"]}">{e(date_line)}</p>')
    out.append(f'<p style="{s["p"]}">{e(hiring_team)}</p>')
    out.append(f'<p style="{s["p"]}">{e(hf["salutation"])}</p>')
    out.append(f'<p style="{s["p"]}">&nbsp;</p>')
    for para in paragraphs:
        out.append(f'<p style="{s["p"]}">{e(para)}</p>')
    out.append(f'<p style="{s["p"]}">&nbsp;</p>')
    out.append(f'<p style="{s["p"]}">{e(hf["signoff"])}</p>')
    out.append(f'<p style="{s["p"]}">{e(ident["name"])}</p>')
    out.append("</body></html>")
    return "\n".join(out)

def gate(spec_path, kind, allow):
    """Run the letter gate. A blocking finding stops the build."""
    cmd = [sys.executable, os.path.join(HERE, "check_letter.py"), spec_path, "--kind", kind]
    for a in allow:
        cmd += ["--allow", a]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stderr.write(proc.stdout)
    if proc.returncode == 2:
        sys.stderr.write(
            "\nRefusing to build the doc. Fix the blocking findings above and re-run.\n")
        sys.exit(2)
    return proc.returncode

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--allow", action="append", default=[],
                    help="a number verified from the posting; passed through to the gate")
    args = ap.parse_args()

    with open(args.spec, encoding="utf-8") as fh:
        spec = json.load(fh)

    gate(args.spec, spec.get("kind", "letter"), args.allow)

    profile = load_profile()
    doc = build(profile, spec["date"], spec["hiring_team"], spec["paragraphs"])
    dest = spec.get("html_out") or spec["out"].rsplit(".", 1)[0] + ".html"
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(dest)

if __name__ == "__main__":
    main()
