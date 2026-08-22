#!/usr/bin/env python3
"""Simulate the artifact shell's transform of a published document.

The shell does not serve back what you published. Observed behaviour, recorded
in docs/MEMORY.md section 1:

  - it injects a frame runtime into the head
  - it drops the `cowork-artifact-meta` block
  - it dissolves the `</head><body>` seam
  - relative URLs resolve against an injected <base href>, so `fetch("index.html")`
    only works when the page is served at that path

Authored content survives contiguously and HTML comments survive, which is the
whole reason the marker cut works at all.

This script applies a deliberately hostile version of that transform: it also
drifts whitespace at the seam. If buildDoc survives this, it survives the real
shell. Usage:

    python3 shell.py IN.html OUT.html [--uuid UUID]
"""
import argparse, re, sys

RUNTIME = (
    '<script type="module" crossorigin '
    'src="https://{uuid}.frame.claudeusercontent.com/assets/frame-runtime.js"></script>\n'
    '<script type="module" crossorigin '
    'src="https://{uuid}.frame.claudeusercontent.com/assets/artifact.CRhVHzSt.js"></script>\n'
    '<link rel="modulepreload" crossorigin '
    'href="https://{uuid}.frame.claudeusercontent.com/assets/db.CRhVHzSt.js">\n'
)

DEFAULT_UUID = "da80ff29-3a14-48a4-9d69-762e79ff2594"


def transform(src, uuid=DEFAULT_UUID, base="/"):
    out = src

    # 1. drop the cowork-artifact-meta block if present
    out = re.sub(
        r'<script[^>]*id="cowork-artifact-meta"[^>]*>.*?</script>\s*',
        "", out, flags=re.S)

    # 2. inject base href plus the frame runtime immediately after <head>
    inject = '<base href="{}">\n'.format(base) + RUNTIME.format(uuid=uuid)
    if "<head>" in out:
        out = out.replace("<head>", "<head>\n" + inject, 1)
    else:
        out = inject + out

    # 3. dissolve the </head><body> seam, and drift the whitespace while we are
    #    at it, because whitespace is exactly what drifts across a real round trip
    out = re.sub(r'\s*</head>\s*<body[^>]*>\s*', "</head><body>", out, count=1)

    # 4. and drift the tail the same way
    out = re.sub(r'\s*</body>\s*</html>\s*$', "</body></html>", out, count=1)

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--uuid", default=DEFAULT_UUID)
    ap.add_argument("--base", default="/")
    a = ap.parse_args()
    src = open(a.src, encoding="utf-8").read()
    out = transform(src, a.uuid, a.base)
    open(a.dst, "w", encoding="utf-8").write(out)
    print("shell.py: {} -> {}  {} chars -> {} chars".format(a.src, a.dst, len(src), len(out)))


if __name__ == "__main__":
    main()
