#!/usr/bin/env python3
"""Flatten the skill into one SKILL.md for the claude.ai account uploader.

The account skill uploader takes a single markdown file. The repo copy is a
directory, because four short reference files are easier to maintain than one
long one. This script generates the flat build so the two can never drift: the
flat file is derived, never hand edited.

    python3 scripts/build_account_skill.py
    -> dist/SKILL.md

The support files (both scripts and both JSON configs) are embedded verbatim in
fenced blocks, plus one bash block that writes them back to disk in the layout
the scripts expect. The scripts resolve config as dirname(dirname(__file__)) +
/config, so writing to /tmp/apb/scripts and /tmp/apb/config runs them unmodified.
Nothing is rewritten, so the code path in the flat build is the tested one.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIST = os.path.join(ROOT, "dist")

def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()

def strip_frontmatter(text):
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    return (m.group(0), text[m.end():]) if m else ("", text)

def demote(text, levels=1):
    """Push every heading down so the merged file has one h1."""
    return re.sub(r"^(#{1,5}) ", lambda m: "#" * (len(m.group(1)) + levels) + " ",
                  text, flags=re.M)

def repoint(text):
    """Turn file-path cross references into references to sections of the flat
    build. Applied to the prose only. The install block must stay byte identical
    to the repo files, so it never goes through here."""
    text = re.sub(r"`references/([a-z-]+)\.md`", r"the **\1** section", text)
    text = text.replace("`config/profile.json`", "the embedded `profile.json`")
    text = text.replace("`config/banned.json`", "the embedded `banned.json`")
    text = text.replace("`scripts/check_letter.py`", "the gate")
    text = text.replace("`scripts/build_letter_html.py`", "the builder")
    return text

def body(rel, levels=1):
    _, text = strip_frontmatter(read(rel))
    # Drop the first heading; the section header we emit replaces it.
    text = re.sub(r"^#\s+.*?\n+", "", text, count=1)
    return repoint(demote(text.strip(), levels))

SUPPORT = ["config/profile.json", "config/banned.json",
           "scripts/check_letter.py", "scripts/build_letter_html.py"]

def install_block():
    """One bash block that recreates the support files under /tmp/apb."""
    lines = ["set -e", "mkdir -p /tmp/apb/config /tmp/apb/scripts", ""]
    for rel in SUPPORT:
        lines.append(f"cat > /tmp/apb/{rel} <<'APB_EOF'")
        lines.append(read(rel).rstrip("\n"))
        lines.append("APB_EOF")
        lines.append("")
    lines.append("python3 -c \"import json;[json.load(open(f)) for f in "
                 "['/tmp/apb/config/profile.json','/tmp/apb/config/banned.json']]\"")
    lines.append('echo "letter tool ready at /tmp/apb/scripts/"')
    return "\n".join(lines)

def manual_checklist():
    """Derived from banned.json so it cannot drift from what the gate enforces."""
    b = json.loads(read("config/banned.json"))
    p = json.loads(read("config/profile.json"))
    nums = sorted({t for e in p["resume_numbers"] for t in e["tokens"]},
                  key=lambda s: (len(s), s))
    out = []
    out.append("Run this by eye, in this order. It is the same set the script "
               "enforces, minus the arithmetic.\n")
    out.append("1. **Negative parallelism.** Any sentence that negates one framing "
               "and then asserts a corrected one. This is the biggest tell and the "
               "one to hunt first:\n")
    for e in b["negative_parallelism"][:8]:
        out.append(f"   - {e['label']}")
    out.append("\n   Plus the disguised forms: \"While X might seem right, Y is "
               "actually\", \"Sure, X works. But Y is where\", \"X gets all the "
               "attention, but Y\". Fix: delete everything before the positive claim.\n")
    out.append("2. **Dead vocabulary.** Any one of these fails the draft. The full "
               "list is in the embedded `banned.json`; these are the ones that "
               "actually turn up in his letters:\n")
    common = ["leverage", "robust", "seamless", "innovative", "spearheaded",
              "facilitated", "meticulous", "passionate", "showcase", "foster",
              "testament", "crucial", "pivotal", "streamline", "cutting-edge",
              "best practices", "proven track record", "demonstrated ability"]
    out.append("   " + ", ".join(f"`{w}`" for w in common) + "\n")
    out.append("3. **Dead openers.** " + ", ".join(
        f'"{p_}"' for p_ in b["dead_phrases"] if p_.startswith("i ")) + "\n")
    out.append("4. **Mechanical transitions.** " + ", ".join(
        f"`{w}`" for w in b["dead_transitions"]) + "\n")
    out.append("5. **Em dashes.** None, anywhere. Also no en dash used as one.\n")
    out.append("6. **Tools he does not have.** " + ", ".join(
        f"`{t}`" for t in p["do_not_claim"]) +
        ". Naming one to deny it is allowed and often better than silence. "
        "Claiming one, or hedging toward it, is not.\n")
    out.append("7. **Numbers.** Every figure in the letter must be one of these, "
               "or verified from the posting and called out in the reply:\n")
    out.append("   " + ", ".join(f"`{n}`" for n in nums) + "\n")
    out.append("8. **Attribution.** The 50+ precision measurements and the 0.5 mm "
               "model belong to the ratcheting screwdriver project. Never to Kelvin.\n")
    out.append("9. **Tense.** No present-tense sentence about Kelvin Thermal "
               "Technologies. That internship ended August 2026.\n")
    out.append("10. **Certifications.** CSWA is the only one on file. Anything else "
               "asserted as a certification needs checking before it ships.\n")
    out.append("11. **Rule of three.** At most one three-item list in the letter. "
               "Two is a pattern.\n")
    out.append("12. **Rhythm.** Read the paragraph word counts. If they are all "
               "within about 15% of each other, or every paragraph lands a number, "
               "the letter has a metronome and needs a short paragraph.\n")
    return "\n".join(out)

def main():
    fm, skill = strip_frontmatter(read("SKILL.md"))
    if not fm:
        sys.exit("SKILL.md has no frontmatter")

    # Point the reference-file mentions at the sections of this same document.
    skill = repoint(skill)

    parts = [
        fm.rstrip("\n"),
        "",
        "<!-- GENERATED FILE. Do not edit.",
        "     Source: .claude/skills/application-packet-builder/ in the empluzz repo.",
        "     Rebuild: python3 scripts/build_account_skill.py",
        "     Edit the source files and regenerate; edits here are lost. -->",
        "",
        skill.strip(),
        "",
        "---",
        "",
        "# profile",
        "",
        "> Joaquin's layer. Outranks every generic rule in this document.",
        "",
        body("references/profile.md"),
        "",
        "---",
        "",
        "# voice-dna",
        "",
        body("references/voice-dna.md"),
        "",
        "---",
        "",
        "# writing",
        "",
        body("references/writing.md"),
        "",
        "---",
        "",
        "# followup",
        "",
        body("references/followup.md"),
        "",
        "---",
        "",
        "# The gate",
        "",
        "Two paths. Take the first one whenever a shell is available, because it "
        "checks things a person reading cannot: every number against the resume, "
        "the misattribution, the tense, and roughly 160 banned strings.",
        "",
        "## Path 1, with a shell",
        "",
        "Run this once per session to lay the tool down:",
        "",
        "```bash",
        install_block(),
        "```",
        "",
        "Then gate every draft before it becomes a document:",
        "",
        "```bash",
        "python3 /tmp/apb/scripts/check_letter.py draft.txt",
        "python3 /tmp/apb/scripts/check_letter.py draft.txt --kind followup",
        "python3 /tmp/apb/scripts/check_letter.py /tmp/spec.json --allow 1965",
        "```",
        "",
        "Exit 0 is clean, 1 is advisory and worth reading, **2 means fix it and "
        "re-run.** To build the upload HTML, which runs the gate again and writes "
        "nothing on a block:",
        "",
        "```bash",
        "python3 /tmp/apb/scripts/build_letter_html.py /tmp/spec.json",
        "```",
        "",
        "## Path 2, no shell",
        "",
        manual_checklist(),
    ]

    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, "SKILL.md")
    text = "\n".join(parts).rstrip() + "\n"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)

    for ch, name in ((chr(0x2014), "em dash"), (chr(0x2013), "en dash")):
        if ch in text:
            sys.exit(f"REFUSED: {name} in the generated build")
    print(f"{out}  {len(text)} bytes, {len(text.splitlines())} lines")

if __name__ == "__main__":
    main()
