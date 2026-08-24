#!/usr/bin/env python3
"""Install the career-ops writing system into the Build letter button.

Replaces the current delegation block with the one in
build-letter-delegation.js, which adds the four questions Opus asks before it
spawns anything, the gate the subagent must run, and the anti-slop rules that
travel inside the clipboard text.

Anchored find/replace, never offsets, per docs/MEMORY.md section 3. Every anchor
must appear exactly once or the script refuses to write anything.

    python3 apply-writing-system.py IN.html OUT.html build-letter-delegation.js

Run this against a build that already carries the 2026-08-22 delegation block.
For a build that predates it, run apply-delegation.py first.
"""
import io, sys

SRC, DST = sys.argv[1], sys.argv[2]
s = io.open(SRC, encoding="utf-8").read()

NEW = io.open(sys.argv[3], encoding="utf-8").read()

def sub(a, b):
    global s
    n = s.count(a)
    if n != 1:
        sys.exit("REFUSED: anchor appears %d times, expected 1: %r" % (n, a[:70]))
    s = s.replace(a, b)

# The block runs from the delegation comment through the end of cvBtn. Both ends
# are unique in a delegated build; the guard below proves the span is the shape
# this patch expects before anything is written.
block_start = "/* The button hands over an orchestration prompt"
block_end = ("    flash(btn,\"Copied\",'Opus prompt for '+r[1]+' copied. Paste it into a fresh "
             "Opus chat. It hands the draft to a Sonnet subagent, then checks the voice before "
             "the link comes back to you.'));\n}")

if s.count(block_start) != 1:
    sys.exit("REFUSED: the delegation comment appears %d times, expected 1. "
             "Run apply-delegation.py first if this build predates 2026-08-22."
             % s.count(block_start))
if s.count(block_end) != 1:
    sys.exit("REFUSED: the cvBtn tail this patch expects is not present exactly once. "
             "The button may already carry the writing system.")

i0 = s.index(block_start)
i1 = s.index(block_end) + len(block_end)
old_block = s[i0:i1]
for name in ("function cvBrief", "function cvPrompt", "function cvBtn"):
    if old_block.count(name) != 1:
        sys.exit("REFUSED: the button span is not the shape this patch expects, %r" % name)
sub(old_block, NEW.rstrip("\n"))

sub("""    ' title="'+(done?'Copy the Opus prompt to rewrite this letter through a Sonnet subagent':'Copy the Opus prompt that hands this letter to a Sonnet subagent and files it in Packets')+'">'+""",
"""    ' title="'+(done?'Copy the Opus prompt to rewrite this letter, four questions first, then a Sonnet subagent':'Copy the Opus prompt that asks you four questions, then hands this letter to a Sonnet subagent and files it in Packets')+'">'+""")

sub("""     +'<p class="hint"><b>Build letter</b> copies an orchestration prompt for that row. Paste it into a fresh '
     +'<b>Opus</b> chat: Opus hands the drafting to a Sonnet subagent, which runs the packet skill and files the '
     +'Google Doc in Packets, then Opus reads it back and fixes the voice before you get the link. '
     +'Nothing is ever submitted for you. '""",
"""     +'<p class="hint"><b>Build letter</b> copies an orchestration prompt for that row. Paste it into a fresh '
     +'<b>Opus</b> chat: Opus asks you four short questions first, then hands the drafting to a Sonnet subagent, '
     +'which runs the packet skill, passes the letter gate and files the Google Doc in Packets. Opus reads it back '
     +'and fixes the voice before you get the link. Nothing is ever submitted for you. '""")

if chr(0x2014) in s:  # em dash, by codepoint so this file stays free of it
    sys.exit("REFUSED: an em dash is present in the output")
io.open(DST, "w", encoding="utf-8").write(s)
print("apply-writing-system.py: %s chars -> %s chars"
      % (len(io.open(SRC, encoding="utf-8").read()), len(s)))
