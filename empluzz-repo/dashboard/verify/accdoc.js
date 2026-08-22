/* JS mirror of accdoc.py. Marker literals are assembled at runtime here for the
 * same reason the dashboard does it: a whole literal in this file would be found
 * by indexOf instead of the real marker if this file were ever concatenated in. */
const H_A = "<!--" + "ACC-HEAD" + "-->";
const H_B = "<!--" + "/ACC-HEAD" + "-->";
const B_A = "<!--" + "ACC-BODY" + "-->";
const B_B = "<!--" + "/ACC-BODY" + "-->";
const S_A = "/*" + "ACC-STATE" + "*/";
const S_B = "/*/" + "ACC-STATE" + "*/";

const PREFIX = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n';
const SEAM = '\n</head>\n<body>\n';
const SUFFIX = '\n</body>\n</html>';

function countOf(s, needle) {
  let n = 0, i = 0;
  for (;;) { const j = s.indexOf(needle, i); if (j < 0) break; n++; i = j + needle.length; }
  return n;
}

/* A real marker is the comment form. The script also mentions the bare names
 * when it assembles them, so count the comment form only. */
function markerCounts(s) {
  return { H_A: countOf(s, H_A), H_B: countOf(s, H_B), B_A: countOf(s, B_A), B_B: countOf(s, B_B),
           S_A: countOf(s, S_A), S_B: countOf(s, S_B) };
}

function rebuild(src, payload) {
  const h0 = src.indexOf(H_A), h1 = src.indexOf(H_B);
  const b0 = src.indexOf(B_A), b1 = src.indexOf(B_B);
  if (h0 < 0 || h1 <= h0 || b0 < 0 || b1 <= b0) throw new Error("document markers missing");
  const head = src.slice(h0, h1 + H_B.length);
  let body = src.slice(b0, b1 + B_B.length);
  if (payload) {
    const a0 = body.indexOf(S_A), a1 = body.indexOf(S_B);
    if (a0 < 0 || a1 <= a0) throw new Error("state markers missing");
    body = body.slice(0, a0) + S_A + "const PUB=" + JSON.stringify(payload) + ";" + S_B + body.slice(a1 + S_B.length);
  }
  return PREFIX + head + SEAM + body + SUFFIX;
}

function readState(src) {
  const a0 = src.indexOf(S_A), a1 = src.indexOf(S_B);
  if (a0 < 0 || a1 <= a0) throw new Error("state markers missing");
  const raw = src.slice(a0 + S_A.length, a1);
  const m = raw.match(/^\s*const PUB=([\s\S]*);\s*$/);
  if (!m) throw new Error("state block not parseable");
  return JSON.parse(m[1]);
}

function slugs(src, kind) {
  const re = new RegExp('"(' + (kind || "int") + '-[a-z0-9-]+)"', "g");
  const out = []; let m;
  while ((m = re.exec(src))) out.push(m[1]);
  return out;
}


/* Count a tag as MARKUP only. The dashboard's own buildDoc() carries the string
 * '<!DOCTYPE html>\n<html lang="en">...' as a literal inside its script, so a raw
 * substring count reports two <html> on a perfectly healthy single-wrapper
 * document. That false alarm is exactly what a nesting check must not raise.
 * Strip script bodies first, then count. */
function stripScripts(s) {
  return s.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "<script></script>");
}
function markupCounts(s) {
  const t = stripScripts(s);
  return { html: countOf(t, "<html"), htmlClose: countOf(t, "</html>"),
           body: countOf(t, "<body"), bodyClose: countOf(t, "</body>") };
}

module.exports = { H_A, H_B, B_A, B_B, S_A, S_B, PREFIX, SEAM, SUFFIX, countOf, markerCounts, stripScripts, markupCounts, rebuild, readState, slugs };
