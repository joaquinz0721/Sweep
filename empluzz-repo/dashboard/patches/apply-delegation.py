#!/usr/bin/env python3
"""Apply the Build letter delegation change to any application-command-center build.

Anchored find/replace, never offsets, per docs/MEMORY.md section 3. Every anchor
must appear exactly once or the script refuses to write anything.

    python3 apply-delegation.py IN.html OUT.html
"""
import io, sys, re

SRC, DST = sys.argv[1], sys.argv[2]
s = io.open(SRC, encoding="utf-8").read()

# the new cvPrompt / cvBtn pair, lifted verbatim from the committed repo build
NEW = io.open(sys.argv[3], encoding="utf-8").read()

def sub(a, b):
    global s
    n = s.count(a)
    if n != 1:
        sys.exit("REFUSED: anchor appears %d times, expected 1: %r" % (n, a[:70]))
    s = s.replace(a, b)

old_block_start = "function cvPrompt(kind,i){"
old_block_end = "    flash(btn,\"Copied\",'Packet prompt for '+r[1]+' copied. Paste it into a new chat and the letter gets written and filed in Packets.'));\n}"
i0 = s.index(old_block_start)
i1 = s.index(old_block_end) + len(old_block_end)
old_block = s[i0:i1]
if old_block.count("function cvPrompt") != 1 or old_block.count("function cvBtn") != 1:
    sys.exit("REFUSED: the cvPrompt/cvBtn span is not the shape this patch expects")
sub(old_block, NEW.rstrip("\n"))

sub("""   This page cannot reach Drive or start a chat on its own, so every action
   button hands you a ready prompt instead. Paste it into a new chat and the
   packet builder does the writing and the filing. Nothing is ever submitted. */""",
"""   This page cannot reach Drive or start a chat on its own, so every action
   button hands you a ready prompt instead. Paste it into a new chat and the
   chat does the writing and the filing. Nothing is ever submitted. */""")

sub("""    ' title="'+(done?'Rewrite the cover letter for this role':'Build the cover letter for this role and file it in Packets')+'">'+""",
"""    ' title="'+(done?'Copy the Opus prompt to rewrite this letter through a Sonnet subagent':'Copy the Opus prompt that hands this letter to a Sonnet subagent and files it in Packets')+'">'+""")

sub("""     +'<p class="hint"><b>Build letter</b> copies a ready packet prompt for that row. Paste it into a fresh chat '
     +'and the cover letter gets written and filed in Packets. Nothing is ever submitted for you. '""",
"""     +'<p class="hint"><b>Build letter</b> copies an orchestration prompt for that row. Paste it into a fresh '
     +'<b>Opus</b> chat: Opus hands the drafting to a Sonnet subagent, which runs the packet skill and files the '
     +'Google Doc in Packets, then Opus reads it back and fixes the voice before you get the link. '
     +'Nothing is ever submitted for you. '""")

if "—" in s:
    sys.exit("REFUSED: an em dash is present in the output")
io.open(DST, "w", encoding="utf-8").write(s)
print("apply-delegation.py: %s chars -> %s chars" % (len(io.open(SRC,encoding='utf-8').read()), len(s)))
