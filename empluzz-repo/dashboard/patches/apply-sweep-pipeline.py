#!/usr/bin/env python3
"""Point the Run Internship Sweep and Run Scholarship Sweep buttons at the real
pipeline in docs/sweep-pipeline.md, built 2026-10-07.

    python3 apply-sweep-pipeline.py IN.html OUT.html

One edit: the comment above sweepPrompt() and the sweepPrompt() function itself,
from the comment's first line to the end of the function. Refuses to write if
either anchor is missing or appears more than once.
"""
import sys

START = "/* This is a copy-a-prompt button and always was. The old code first tried\n"
END = '    "Show me the ingest preview before you apply it."\n  ].join("\\n");\n}\n'

NEW = r'''/* This is a copy-a-prompt button and always was; window.cowork.runScheduledTask
   does not exist in this frame (tested 2026-08-21) and a Cowork session cannot
   publish this page anyway. The pipeline it points at was BUILT on 2026-10-07:
   a Sonnet sweep agent writes a JSON payload, dashboard/ingest.py validates and
   previews it, he says go, and the session merges it into a FRESH read of this
   page, runs the harness and publishes. Keep this text in step with
   docs/sweep-pipeline.md, which is the full procedure. */
function sweepPrompt(kind){
  const what=kind==="int"
    ? "Summer 2027 internship sweep"
    : "2026-27 scholarship sweep";
  const agent=kind==="int" ? "internship-sweep" : "scholarship-sweep";
  const pay="/tmp/apb/work/sweep-"+kind+".json";
  return [
    "Run the "+what+" for the empluzz project, in the Sweep repo.",
    "",
    "Read empluzz-repo/CLAUDE.md, then follow empluzz-repo/docs/sweep-pipeline.md",
    "step by step. Commands run from empluzz-repo/. The short version:",
    "1. Read the tracker with the Artifact tool, then rebuild it for the agent:",
    "   python3 dashboard/verify/mkbase2.py <saved file> /tmp/apb/work/sweep-base.html",
    "2. Spawn the "+agent+" agent on Sonnet with BUILD=/tmp/apb/work/sweep-base.html",
    "   and PAYLOAD="+pay+". It searches, scores and writes the payload. It never",
    "   publishes. If that agent type is not listed, spawn a general-purpose agent",
    "   on Sonnet and give it .claude/agents/"+agent+".md as its instructions.",
    "3. Preview:  python3 dashboard/ingest.py "+pay+" --build /tmp/apb/work/sweep-base.html",
    "   Show me the whole preview and the best finds. Wait for my go.",
    "4. After my go, read the tracker AGAIN and Read every line of the new file,",
    "   then rebuild it: mkbase2.py <new saved file> /tmp/apb/work/live-base.html",
    "5. Apply:    python3 dashboard/ingest.py "+pay+" --build /tmp/apb/work/live-base.html --apply",
    "6. Verify:   dashboard/verify/run.sh /tmp/apb/work/live-base.html   (all 56 must pass)",
    "7. Publish live-base.html to the tracker with its URL and the favicon. Never",
    "   force, never a capabilities object. Read it back and confirm it matches.",
    "8. Commit the null-state copy to main so the repo and the page do not drift.",
    "",
    "Never touch my applied ticks, and refuse to publish if the tick count moved.",
    "Never apply before I have seen the preview."
  ].join("\n");
}
'''


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: apply-sweep-pipeline.py IN.html OUT.html")
    src = open(sys.argv[1], encoding="utf-8").read()
    for name, anchor in (("start", START), ("end", END)):
        n = src.count(anchor)
        if n != 1:
            sys.exit("REFUSED: %s anchor appears %d times, expected 1. Nothing written." % (name, n))
    a = src.index(START)
    b = src.index(END) + len(END)
    if b <= a:
        sys.exit("REFUSED: anchors out of order. Nothing written.")
    out = src[:a] + NEW + src[b:]
    open(sys.argv[2], "w", encoding="utf-8").write(out)
    print("apply-sweep-pipeline: replaced %d chars with %d" % (b - a, len(NEW)))


if __name__ == "__main__":
    main()
