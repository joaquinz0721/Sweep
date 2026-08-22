#!/usr/bin/env python3
"""Flag the constructions that make a draft read as machine-written.

Usage:  python3 voice_check.py draft.txt
        python3 voice_check.py -            (reads stdin)

A clean run is not proof the writing is good. It only means these
specific moves are absent. Read the draft out loud afterwards.
"""
import re
import sys

CHECKS = [
    # (label, regex, what to do about it)
    ("em dash", r"[—–]",
     "Hard rule 4. Use a comma, a semicolon, or two sentences."),

    ("summarizing tag", r",\s*which (?:is|was|are|were)\b",
     "Move 3. The clause restates the sentence it hangs off. Cut it."),

    ("summarizing tag", r"(?:^|(?<=[.!?]\s))That is\b",
     "Move 3. A sentence whose subject is the previous sentence. Cut it."),

    ("antithesis", r"\bwould not be\b|\bdoes not\b.{0,30}\bit does\b|"
                   r"\bis not\b.{0,40}\bit is\b|\bnot because\b.{0,40}\bbut\b|"
                   r"\bnot just\b|\bnot only\b.{0,40}\bbut also\b",
     "Move 2. Say the honest half once, plainly, and stop."),

    ("self-aphorism", r"\bis where I\b|\bwhere I am most\b|\bmy best work\b|"
                      r"\bwhere the\b.{0,40}\bmeet\b|\bthe kind of (?:work|engineer)\b|"
                      r"\bI am the kind of\b",
     "Move 1. Report what he did instead of characterizing him."),

    ("hedge", r"\beager to\b|\bconfident that\b|\bI hope to\b|\bI believe I would\b|"
              r"\bexcited (?:to|about)\b|\bpassionate about\b|\bI am writing to express\b",
     "Rule 4. Cut it."),

    ("consultant vocabulary", r"\bleverage\b|\butilize\b|\bspearhead|\bsynerg|\brobust\b|"
                              r"\bseamless\b|\bcutting.edge\b|\bskill ?set\b|\bdeep dive\b|"
                              r"\bdelve\b|\blandscape\b|\bin today's\b",
     "He would not say it out loud."),

    ("misattribution", r"50\+?\s*(?:precision\s*)?measurements[^.]{0,80}(?:Kelvin|internship)",
     "The 50 plus measurements belong to the ratcheting screwdriver project."),
]

BANNED_CLAIMS = ["FEA", "CFD", " NX", "Teamcenter", "ANSYS", "AutoCAD", "Revit", "BIM", "Creo"]


def main() -> int:
    src = sys.stdin.read() if sys.argv[1:2] == ["-"] else open(sys.argv[1], encoding="utf8").read()
    lines = src.splitlines()
    hits = []

    for n, line in enumerate(lines, 1):
        for label, pattern, advice in CHECKS:
            for m in re.finditer(pattern, line, re.I):
                hits.append((n, label, m.group(0).strip(), advice))
        for claim in BANNED_CLAIMS:
            if claim.lower() in line.lower():
                hits.append((n, "do not claim", claim.strip(),
                             "Not on his resume. SolidWorks is his CAD."))

    body = [ln for ln in lines if ln.strip()]
    if body:
        last = body[-1]
        if not re.search(r"thank|\?|appreciate|glad to|happy to|Sincerely", last, re.I):
            hits.append((len(lines), "closing flourish", last[:60],
                         "Move 4. End with the ask or with thanks, nothing after."))

    if not hits:
        print("clean: none of the four moves, no hedges, no banned claims.")
        print("now read it out loud and cut anything he would not say to a person.")
        return 0

    print(f"{len(hits)} to look at:\n")
    for n, label, text, advice in hits:
        print(f"  line {n:>3}  [{label}]  {text!r}")
        print(f"           {advice}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
