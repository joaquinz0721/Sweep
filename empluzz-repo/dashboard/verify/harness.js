/* Shared plumbing for the command center verification suites.
 *
 * Two rules encoded here, both learned the hard way:
 *
 *  1. Serve over http://localhost at a path matching the <base href> the shell
 *     injects. Over file://, or at the wrong path, the page's fetch of its own
 *     source 404s and buildDoc throws transform_error, which looks like a code
 *     failure and is not one.
 *  2. Stub window.claude BEFORE any page script runs. initRemote() reads it on
 *     load, so a stub installed after navigation is a stub that never existed.
 */
const http = require("http");
const fs = require("fs");
const path = require("path");

const UUID = "da80ff29-3a14-48a4-9d69-762e79ff2594";
const BASE = `/artifact/${UUID}/`;

function serve(dir) {
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split("?")[0]);
    if (!p.startsWith(BASE)) { res.writeHead(404); return res.end("not under base href"); }
    let rel = p.slice(BASE.length) || "index.html";
    const file = path.join(dir, rel);
    if (!file.startsWith(dir) || !fs.existsSync(file)) { res.writeHead(404); return res.end("404"); }
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" });
    res.end(fs.readFileSync(file));
  });
  return new Promise(r => server.listen(0, "127.0.0.1", () => r({
    server, url: `http://127.0.0.1:${server.address().port}${BASE}`
  })));
}

/* The five stub shapes. `absent` is not an error case: it is what a plain
 * browser tab sees, and the page must still work there. */
function stubScript(mode) {
  return `(() => {
    window.__pub = [];
    window.__pubCount = 0;
    if (${JSON.stringify(mode)} === "absent") { try { delete window.claude; } catch(e){} return; }
    const fail = (code, message) => { const e = new Error(message||code); e.code = code; return e; };
    window.claude = {
      use: async (ns) => {
        if (ns !== "artifact") return null;
        return {
          publish: async (html) => {
            window.__pubCount++;
            window.__pub.push(typeof html === "string" ? html : JSON.stringify(html));
            switch (${JSON.stringify(mode)}) {
              case "resolve": return { ok: true, version: "test-0001" };
              case "not_writer": throw fail("not_writer", "not a writer");
              case "capability_disabled": throw fail("capability_disabled", "publishing files is not available in this view");
              case "conflict": throw fail("conflict", "newer version exists");
              case "rate_limited": throw fail("rate_limited", "slow down");
              default: return { ok: true };
            }
          }
        };
      }
    };
  })();`;
}

async function openPage(browser, url, mode, opts = {}) {
  const ctx = await browser.newContext({
    viewport: opts.viewport || { width: 1440, height: 900 },
    deviceScaleFactor: 1
  });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", e => errors.push(String(e)));
  page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
  /* The injected frame runtime points at frame.claudeusercontent.com, which this
   * sandbox cannot reach. Fulfil those requests locally so a network refusal does
   * not masquerade as a page error. The runtime only needs to be PRESENT in the
   * served copy; it never needs to execute for these assertions. */
  await ctx.route("**://*.frame.claudeusercontent.com/**", r =>
    r.fulfill({ status: 200, contentType: "application/javascript", body: "/* stub */" }));
  await page.addInitScript(stubScript(mode));
  if (opts.initScript) await page.addInitScript(opts.initScript);
  await page.goto(url, { waitUntil: "networkidle" });
  page.__errors = errors;
  return { ctx, page, errors };
}

/* The debounce is 3500ms. Anything shorter than this and the test is measuring
 * the timer, not the code. */
const DEBOUNCE_WAIT = 5200;

class Report {
  constructor(name) { this.name = name; this.rows = []; }
  ok(label, cond, detail) {
    this.rows.push({ label, pass: !!cond, detail: detail === undefined ? "" : String(detail) });
    const mark = cond ? "  PASS" : "  FAIL";
    console.log(`${mark}  ${label}${cond ? "" : "   <- " + (detail === undefined ? "" : detail)}`);
    return !!cond;
  }
  eq(label, actual, expected) {
    return this.ok(label, Object.is(actual, expected), `got ${JSON.stringify(actual)} want ${JSON.stringify(expected)}`);
  }
  get passed() { return this.rows.filter(r => r.pass).length; }
  get failed() { return this.rows.filter(r => !r.pass).length; }
  summary() {
    console.log(`\n${this.name}: ${this.passed} passed, ${this.failed} failed, ${this.rows.length} assertions`);
    return this.failed === 0;
  }
}

module.exports = { serve, stubScript, openPage, Report, DEBOUNCE_WAIT, UUID, BASE };
