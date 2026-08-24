#!/usr/bin/env python3
"""Gate a drafted letter before it becomes a Google Doc.

Everything the skill used to enforce by asking the model to pay attention is
enforced here instead: banned vocabulary, negative parallelism, tools Joaquin
does not have, and numbers that are not on his resume.

    python3 scripts/check_letter.py spec.json
    python3 scripts/check_letter.py draft.txt --kind followup
    python3 scripts/check_letter.py spec.json --allow 1965 --allow 400

Exit codes:
    0   pass, nothing found
    1   warn, advisory findings only, drafting may continue
    2   BLOCK, do not build the doc until these are fixed

--allow takes a number verified from the posting or from company research, and
is the deliberate escape hatch for a real figure that is not on the resume. It
has to be typed out, which is the point: an unexplained number in a letter to an
employer is the failure this script exists to catch.
"""
import sys, os, json, re, argparse, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def load(name):
    with open(os.path.join(ROOT, "config", name), encoding="utf-8") as fh:
        return json.load(fh)

# ── findings ────────────────────────────────────────────────────────────

BLOCK, WARN = "BLOCK", "warn"

class Report:
    def __init__(self):
        self.items = []

    def add(self, level, rule, detail, fix=""):
        self.items.append((level, rule, detail, fix))

    @property
    def blocks(self):
        return [i for i in self.items if i[0] == BLOCK]

    @property
    def warns(self):
        return [i for i in self.items if i[0] == WARN]

    def render(self):
        if not self.items:
            return "PASS. Nothing found.\n"
        out = []
        for level, rule, detail, fix in self.blocks + self.warns:
            tag = "BLOCK" if level == BLOCK else "warn "
            out.append(f"[{tag}] {rule}: {detail}")
            if fix:
                out.append(f"         fix: {fix}")
        out.append("")
        out.append(f"{len(self.blocks)} blocking, {len(self.warns)} advisory.")
        if self.blocks:
            out.append("Do not build the doc. Fix the blocking findings and re-run.")
        return "\n".join(out) + "\n"

# ── text helpers ────────────────────────────────────────────────────────

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

def sentences(text):
    return [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]

def find_phrase(text, phrase):
    """Whole-phrase, case-insensitive, word-bounded where the edges are word chars."""
    lead = r"\b" if phrase[0].isalnum() else ""
    tail = r"\b" if phrase[-1].isalnum() else ""
    return re.search(lead + re.escape(phrase) + tail, text, re.I)

def context(text, match, width=48):
    a = max(0, match.start() - width // 2)
    b = min(len(text), match.end() + width // 2)
    return "..." + text[a:b].replace("\n", " ").strip() + "..."

# ── checks ──────────────────────────────────────────────────────────────

# Built from codepoints so this file stays free of the characters it bans, the
# same convention dashboard/patches/apply-delegation.py follows. U+2014 em dash,
# U+2013 en dash.
DASHES = ((chr(0x2014), "em dash"), (chr(0x2013), "en dash"))

def check_dashes(text, rep):
    for ch, name in DASHES:
        if ch in text:
            m = re.search(re.escape(ch), text)
            rep.add(BLOCK, name, context(text, m),
                    "comma, semicolon, colon, parentheses, or two sentences")

def check_lists(text, rep, banned):
    for word in banned["dead_vocabulary"]:
        m = find_phrase(text, word)
        if m:
            rep.add(BLOCK, "dead AI vocabulary", f'"{word}" -> {context(text, m)}',
                    "say the plain thing instead")
    for phrase in banned["dead_phrases"]:
        m = find_phrase(text, phrase)
        if m:
            rep.add(BLOCK, "dead phrase", f'"{phrase}"', "delete it or rewrite the sentence")
    for word in banned["dead_transitions"]:
        if re.search(r"(?i)(^|[.;]\s+)" + re.escape(word) + r"\b", text):
            rep.add(WARN, "mechanical transition", f'"{word}"',
                    "let the sentences sit next to each other")
    for phrase in banned["copulative_avoidance"]:
        m = find_phrase(text, phrase)
        if m:
            rep.add(WARN, "copulative avoidance", f'"{phrase}"', 'just say "is" or "has"')
    for word in banned["participle_padding"]:
        m = find_phrase(text, word)
        if m:
            rep.add(WARN, "participle padding", f'"{word}"',
                    "delete the phrase, or give the claim its own sentence")
    for phrase in banned["hedges"]:
        m = find_phrase(text, phrase)
        if m:
            rep.add(WARN, "hedge", f'"{phrase}"', "lead with the evidence instead")
    for phrase in banned["engagement_bait"] + banned["never_write"]:
        m = find_phrase(text, phrase)
        if m:
            rep.add(BLOCK, "never write this", f'"{phrase}"', "remove it")

def check_negative_parallelism(text, rep, banned):
    for entry in banned["negative_parallelism"]:
        m = re.search(entry["pattern"], text)
        if m:
            rep.add(BLOCK, "negative parallelism (the single biggest tell)",
                    f'{entry["label"]} -> {context(text, m, 80)}',
                    "delete everything before the positive claim and keep only what it IS")

# A letter is allowed to NAME a tool he does not have, in order to say plainly
# that he does not have it. references/profile.md calls that the gap play and
# prefers it to a dodge when the posting makes the tool central. Blocking the
# disclaimer along with the claim would have forced the letter to be evasive,
# which is the opposite of the rule. A negated mention drops to a warning so a
# human still reads the sentence; an unqualified one still blocks.
NEGATORS = re.compile(
    r"\b(neither|nor|not|never|no|none|without|lack(?:s|ing|ed)?|"
    r"haven'?t|hasn'?t|don'?t|doesn'?t|didn'?t|instead of|rather than|"
    r"unfamiliar|yet to)\b", re.I)

def check_do_not_claim(text, rep, profile):
    for term in profile["do_not_claim"]:
        for sent in sentences(text):
            m = find_phrase(sent, term)
            if not m:
                continue
            if NEGATORS.search(sent):
                rep.add(WARN, "names a tool he does not have, and reads as a disclaimer",
                        f'"{term}" -> "{sent[:100]}..."',
                        "fine if the sentence really does deny it; block it yourself if it hedges toward having it")
            else:
                rep.add(BLOCK, "claims a tool or skill he does not have",
                        f'"{term}" -> {context(text, m)}',
                        profile["do_not_claim_note"])

NUM = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*(%?)")

def check_numbers(text, rep, profile, extra_allowed):
    allowed = set(extra_allowed)
    for entry in profile["resume_numbers"]:
        for tok in entry["tokens"]:
            allowed.add(tok.rstrip("+").rstrip("%"))
    for m in NUM.finditer(text):
        raw = m.group(1).replace(",", "")
        if raw in allowed:
            continue
        rep.add(BLOCK, "number is not on his resume", f'"{m.group(0).strip()}" -> {context(text, m)}',
                "use a resume figure, or pass --allow "
                f"{raw} if you verified it from the posting")

def check_attribution(text, rep, profile):
    for entry in profile["resume_numbers"]:
        forbidden = entry.get("never_attribute_to")
        if not forbidden:
            continue
        for sent in sentences(text):
            hit = any(re.search(r"(?<![\w.])" + re.escape(t.rstrip("+")) + r"\b", sent)
                      for t in entry["tokens"])
            if not hit:
                continue
            for bad in forbidden:
                if re.search(r"\b" + re.escape(bad), sent, re.I):
                    rep.add(BLOCK, "number attributed to the wrong project",
                            f'{entry["claim"]} belongs to {entry["owner"]}, not {bad} -> "{sent[:90]}..."',
                            f'move the figure onto {entry["owner"]} or drop it')

def check_tense(text, rep, profile):
    for job in profile["employment"]:
        if job["tense"] != "past":
            continue
        for sent in sentences(text):
            if job["employer"].split()[0].lower() not in sent.lower():
                continue
            if re.search(r"\b(i am|i'm|currently|presently)\b", sent, re.I):
                rep.add(BLOCK, "present tense on a finished job",
                        f'{job["employer"]} ended {job["ended"]} -> "{sent[:90]}..."',
                        job["note"])

RULE_OF_THREE = re.compile(r"\b[\w][\w'-]*(?:\s+[\w'-]+){0,3},\s+[\w'-]+(?:\s+[\w'-]+){0,3},\s+and\s+[\w'-]+")

def check_rule_of_three(text, rep):
    hits = RULE_OF_THREE.findall(text)
    if len(hits) >= 2:
        rep.add(WARN, "rule of three, more than once",
                f"{len(hits)} three-item lists: " + "; ".join(f'"{h[:40]}"' for h in hits[:3]),
                "use two items, or four, or just the one that matters")

def check_rhythm(paragraphs, rep):
    lengths = [len(p.split()) for p in paragraphs]
    if len(lengths) >= 3:
        spread = statistics.pstdev(lengths) / (sum(lengths) / len(lengths))
        if spread < 0.14:
            rep.add(WARN, "metronome paragraphs",
                    f"word counts {lengths}, spread {spread:.0%}",
                    "let one paragraph run long and one land short")
    for i, para in enumerate(paragraphs, 1):
        sent_lens = [len(s.split()) for s in sentences(para)]
        if len(sent_lens) >= 3:
            spread = statistics.pstdev(sent_lens) / (sum(sent_lens) / len(sent_lens))
            if spread < 0.18:
                rep.add(WARN, "metronome sentences",
                        f"paragraph {i} sentence lengths {sent_lens}",
                        "break one sentence in half, or let one earn its length")

def check_generic(paragraphs, rep):
    """Sentences with no proper noun and no number are the ones that could go to anyone."""
    for i, para in enumerate(paragraphs, 1):
        for sent in sentences(para):
            words = sent.split()
            if len(words) < 8:
                continue
            has_proper = any(w[0].isupper() for w in words[1:] if w[0].isalpha())
            has_number = bool(NUM.search(sent))
            if not has_proper and not has_number:
                rep.add(WARN, "could appear in any letter to any company",
                        f'paragraph {i}: "{sent[:80]}..."',
                        "name the employer, the product, or the figure, or cut it")

def followup_body(paragraphs, profile):
    """Drop the greeting and the signature. Neither is body, and counting them
    made a correct four-sentence message report as five."""
    name = profile["identity"]["name"].lower()
    keep = []
    for para in paragraphs:
        flat = para.strip().lower().rstrip(".,")
        if re.match(r"^(hi|hello|hey|dear)\b[^.!?]{0,40}$", flat):
            continue
        if flat == name:
            continue
        keep.append(para)
    return keep

def check_length(paragraphs, rep, profile, kind):
    hf = profile["house_format"]
    if kind == "followup":
        paragraphs = followup_body(paragraphs, profile)
        words = sum(len(p.split()) for p in paragraphs)
        lo, hi, cap = 60, 90, 110
        if words > cap:
            rep.add(BLOCK, "follow-up over the hard cap", f"{words} words, cap {cap}", "cut a clause")
        elif not lo <= words <= hi:
            rep.add(WARN, "follow-up length", f"{words} words, target {lo} to {hi}", "")
        body = " ".join(paragraphs)
        if len(sentences(body)) != 4:
            rep.add(WARN, "follow-up sentence count",
                    f"{len(sentences(body))} sentences, the template is 4", "")
        if re.search(r"(?i)\bin\b[^.;]{2,40}\band\b[^.;]{2,40}\bi believe this role\b", body):
            rep.add(BLOCK, "sentences 2 and 3 joined",
                    "the field clause and the fit clause are one sentence",
                    "split them, this is the failure the template was rewritten to prevent")
        return
    words = sum(len(p.split()) for p in paragraphs)
    if not hf["body_words_min"] <= words <= hf["body_words_max"]:
        rep.add(WARN, "body length",
                f'{words} words, target {hf["body_words_min"]} to {hf["body_words_max"]}', "")
    if not hf["paragraphs_min"] <= len(paragraphs) <= hf["paragraphs_max"]:
        rep.add(WARN, "paragraph count",
                f'{len(paragraphs)}, expected {hf["paragraphs_min"]} to {hf["paragraphs_max"]}', "")

# ── entry ───────────────────────────────────────────────────────────────

def read_paragraphs(path):
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            spec = json.load(fh)
        return spec["paragraphs"]
    with open(path, encoding="utf-8") as fh:
        return [p.strip() for p in re.split(r"\n\s*\n", fh.read()) if p.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="spec.json, or a plain-text draft with blank-line paragraphs")
    ap.add_argument("--kind", default="letter", choices=["letter", "essay", "followup"])
    ap.add_argument("--allow", action="append", default=[],
                    help="a number verified from the posting; repeatable")
    args = ap.parse_args()

    profile, banned = load("profile.json"), load("banned.json")
    paragraphs = read_paragraphs(args.path)
    text = "\n\n".join(paragraphs)
    rep = Report()

    check_dashes(text, rep)
    check_lists(text, rep, banned)
    check_negative_parallelism(text, rep, banned)
    check_do_not_claim(text, rep, profile)
    check_attribution(text, rep, profile)
    check_tense(text, rep, profile)
    check_rule_of_three(text, rep)
    check_length(paragraphs, rep, profile, args.kind)

    if args.kind == "followup":
        check_numbers(text, rep, profile, [])          # a follow-up carries no numbers at all
        for m in NUM.finditer(text):
            rep.add(BLOCK, "follow-up contains a number",
                    f'"{m.group(0).strip()}"',
                    "follow-ups may land on LinkedIn or Handshake; no figures, ever")
    else:
        check_numbers(text, rep, profile, [a.strip() for a in args.allow])
        check_rhythm(paragraphs, rep)
        check_generic(paragraphs, rep)

    sys.stdout.write(rep.render())
    sys.exit(2 if rep.blocks else (1 if rep.warns else 0))

if __name__ == "__main__":
    main()
