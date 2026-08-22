"""Shared marker logic for the command center harness.

Mirrors buildDoc() in the dashboard exactly. If buildDoc changes, change this
and re-run, never the other way round.
"""
import json, re

H_A = "<!--" + "ACC-HEAD" + "-->"
H_B = "<!--" + "/ACC-HEAD" + "-->"
B_A = "<!--" + "ACC-BODY" + "-->"
B_B = "<!--" + "/ACC-BODY" + "-->"
S_A = "/*" + "ACC-STATE" + "*/"
S_B = "/*/" + "ACC-STATE" + "*/"

PREFIX = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
SEAM   = '\n</head>\n<body>\n'
SUFFIX = '\n</body>\n</html>'


def cut(src):
    """Return (head, body) slices inclusive of their markers, as buildDoc does."""
    h0, h1 = src.find(H_A), src.find(H_B)
    b0, b1 = src.find(B_A), src.find(B_B)
    if h0 < 0 or h1 <= h0 or b0 < 0 or b1 <= b0:
        raise ValueError("document markers missing")
    return src[h0:h1 + len(H_B)], src[b0:b1 + len(B_B)]


def swap_state(body, payload):
    a0, a1 = body.find(S_A), body.find(S_B)
    if a0 < 0 or a1 <= a0:
        raise ValueError("state markers missing")
    blob = S_A + "const PUB=" + json.dumps(payload, separators=(",", ":")) + ";" + S_B
    return body[:a0] + blob + body[a1 + len(S_B):]


def rebuild(src, payload=None):
    """The canonical reconstruction. This is the fixed point, not the file on disk."""
    head, body = cut(src)
    if payload is not None:
        body = swap_state(body, payload)
    return PREFIX + head + SEAM + body + SUFFIX


def read_state(src):
    a0, a1 = src.find(S_A), src.find(S_B)
    if a0 < 0 or a1 <= a0:
        raise ValueError("state markers missing")
    raw = src[a0 + len(S_A):a1]
    m = re.match(r"\s*const PUB=(.*);\s*$", raw, re.S)
    if not m:
        raise ValueError("state block not parseable: " + raw[:80])
    return json.loads(m.group(1))


def slugs(src, kind="int"):
    return re.findall(r'"(' + kind + r'-[a-z0-9-]+)"', src)
