/* verify.js -- core suite for the application command center.
 *
 * 33 assertions. Run with:  node verify.js
 * Fixtures are built by shell.py / mkbase2.py / mklive3.py; run.sh does both.
 *
 * The one caveat that must stay attached to every green run: this is evidence
 * the code is right, never that the feature works. The first build passed four
 * stubs and still failed in production, because the runtime does not serve the
 * form it was built on. The console probe in the real artifact frame is the
 * better instrument. See docs/MEMORY.md section 7.
 */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const A = require("./accdoc.js");
const H = require("./harness.js");

const FIX = process.env.ACC_FIX || "/tmp/acc-fixtures";
const REAL_SLUG = "int-kiewit-equipment-eng-intern";     // exists in INT, unticked in the live fixture
const PHANTOM = "int-marotta-controls-me-intern";        // bug 15: never existed

(async () => {
  const R = new H.Report("verify.js");
  const served = fs.readFileSync(path.join(FIX, "index.html"), "utf8");

  /* ---- A. the served fixture is a faithful hostile shell copy ---- */
  const mc = A.markerCounts(served);
  R.ok("A1 served copy keeps all four document markers, exactly once each",
    mc.H_A === 1 && mc.H_B === 1 && mc.B_A === 1 && mc.B_B === 1, JSON.stringify(mc));
  R.ok("A2 served copy keeps the state markers, exactly once each",
    mc.S_A === 1 && mc.S_B === 1, JSON.stringify(mc));
  R.ok("A3 served copy has no cowork-artifact-meta block",
    !served.includes("cowork-artifact-meta"));
  R.ok("A4 served copy has the head/body seam dissolved",
    served.includes("</head><body>") && !/\n<\/head>\n<body>/.test(served));
  R.ok("A5 served copy carries an injected base href and frame runtime",
    /<base href="[^"]+">/.test(served) && served.includes("frame.claudeusercontent.com"));

  const { server, url } = await H.serve(FIX);
  const browser = await H.launchChromium(chromium);

  try {
    /* ---- B. a plain browser tab, no capability at all ---- */
    {
      const { ctx, page, errors } = await H.openPage(browser, url, "absent");
      const rows = await page.locator("table tbody tr").count();
      R.ok("B1 page renders rows with no artifact capability present", rows > 0, `rows=${rows}`);
      R.ok("B2 no page errors on a capability-free load", errors.length === 0, errors.join(" | "));
      await page.evaluate(s => window.toggle(s), REAL_SLUG);
      await page.waitForTimeout(H.DEBOUNCE_WAIT);
      const pubs = await page.evaluate(() => window.__pubCount);
      R.eq("B3 nothing is published when there is no capability", pubs, 0);
      const ls = await page.evaluate(() => localStorage.getItem("acc_applied_v3"));
      R.ok("B4 localStorage backstop still records the tick", !!ls && ls.includes(REAL_SLUG), String(ls).slice(0, 120));
      await ctx.close();
    }

    /* ---- C. idle load must not publish ---- */
    {
      const { ctx, page } = await H.openPage(browser, url, "resolve");
      await page.waitForTimeout(H.DEBOUNCE_WAIT);
      const pubs = await page.evaluate(() => window.__pubCount);
      R.eq("C1 an idle load publishes nothing", pubs, 0);
      await ctx.close();
    }

    /* ---- D. slug guards. Bug 15 was an assertion passing on a phantom row ---- */
    {
      R.ok("D1 the slug under test really exists in INT",
        A.slugs(served, "int").includes(REAL_SLUG), REAL_SLUG);
      R.ok("D2 the bug-15 phantom slug is absent from INT",
        !A.slugs(served, "int").includes(PHANTOM), PHANTOM);
    }

    /* ---- E. the published payload ---- */
    {
      const { ctx, page } = await H.openPage(browser, url, "resolve");
      const before = A.readState(served);
      const beforeCount = Object.keys(before.applied || {}).length;
      await page.evaluate(s => window.toggle(s), REAL_SLUG);
      await page.waitForTimeout(H.DEBOUNCE_WAIT);
      const pubs = await page.evaluate(() => window.__pub);
      R.eq("E1 exactly one publish for one tick", pubs.length, 1);
      const doc = pubs[0] || "";
      R.ok("E2 payload is a complete document",
        doc.startsWith("<!DOCTYPE html>") && doc.trimEnd().endsWith("</html>"), doc.slice(0, 40));
      const pm = A.markerCounts(doc);
      R.ok("E3 payload carries every marker exactly once",
        Object.values(pm).every(v => v === 1), JSON.stringify(pm));
      R.ok("E4 no injected frame runtime leaked into the payload",
        !doc.includes("claudeusercontent.com") && !doc.includes("<base href="));
      R.ok("E5 no cowork-artifact-meta in the payload", !doc.includes("cowork-artifact-meta"));
      const after = A.readState(doc);
      R.ok("E6 payload state carries the new tick", !!(after.applied || {})[REAL_SLUG],
        JSON.stringify(Object.keys(after.applied || {}).length));
      R.eq("E7 tick count grew by exactly one", Object.keys(after.applied || {}).length, beforeCount + 1);
      const sBefore = new Set(A.slugs(served, "int").concat(A.slugs(served, "sch")));
      const sAfter = new Set(A.slugs(doc, "int").concat(A.slugs(doc, "sch")));
      const lost = [...sBefore].filter(x => !sAfter.has(x));
      R.ok("E8 no existing slug changed or disappeared", lost.length === 0, lost.join(","));
      const all = A.slugs(doc, "int").concat(A.slugs(doc, "sch"));
      const uniq = new Set(all);
      R.ok("E9 every row slug is unique and [a-z0-9-] only",
        [...uniq].every(s => /^[a-z0-9-]+$/.test(s)), `${uniq.size} unique of ${all.length} refs`);
      const kc = A.markupCounts(doc);
      R.ok("E10 exactly one html and one body wrapper as MARKUP, no nesting",
        kc.html === 1 && kc.htmlClose === 1 && kc.body === 1 && kc.bodyClose === 1,
        JSON.stringify(kc));
      await ctx.close();
    }

    /* ---- F. the rejection branches. capability_disabled is the real one ---- */
    async function branch(mode) {
      const { ctx, page } = await H.openPage(browser, url, mode);
      await page.evaluate(s => window.toggle(s), REAL_SLUG);
      await page.waitForTimeout(H.DEBOUNCE_WAIT);
      const chip = (await page.locator("#sync").textContent()) || "";
      const pubs = await page.evaluate(() => window.__pubCount);
      await page.evaluate(s => window.toggle(s), "int-zipline-me-intern");
      await page.waitForTimeout(H.DEBOUNCE_WAIT);
      const pubs2 = await page.evaluate(() => window.__pubCount);
      await ctx.close();
      return { chip: chip.trim(), pubs, pubs2 };
    }
    {
      const r = await branch("capability_disabled");
      R.ok("F1 capability_disabled drops to read-only and never retries",
        /read only here/.test(r.chip) && r.pubs2 === r.pubs, `${r.chip} pubs ${r.pubs}->${r.pubs2}`);
    }
    {
      const r = await branch("not_writer");
      R.ok("F2 not_writer drops to read-only and never retries",
        /read only here/.test(r.chip) && r.pubs2 === r.pubs, `${r.chip} pubs ${r.pubs}->${r.pubs2}`);
    }
    {
      const r = await branch("conflict");
      R.ok("F3 conflict is treated as synced, not as a failure",
        /saved to this artifact/.test(r.chip), r.chip);
    }
    {
      const r = await branch("rate_limited");
      R.ok("F4 rate_limited keeps the tick local and backs off rather than hammering",
        /not yet saved|saving ticks/.test(r.chip) && r.pubs2 <= r.pubs + 2, `${r.chip} pubs ${r.pubs}->${r.pubs2}`);
    }

    /* ---- I. the Build letter prompt. It is an orchestration prompt now, so the
       thing worth asserting is that it still tells Opus to delegate and still
       carries everything a cold subagent needs. ---- */
    {
      const { ctx, page } = await H.openPage(browser, url, "absent");
      const pInt = await page.evaluate(() => window.cvPrompt("int", 0));
      const pSch = await page.evaluate(() => window.cvPrompt("sch", 0));
      const row = await page.evaluate(() => [INT[0][1], INT[0][2], INT[0][7]]);
      R.ok("I1 the internship prompt tells Opus to delegate to a Sonnet subagent",
        /Do not write this one yourself/.test(pInt) && /model set to Sonnet/.test(pInt), pInt.slice(0, 80));
      R.ok("I2 it carries the row facts a cold subagent cannot look up",
        row.every(v => pInt.includes(v)), row.join(" | "));
      R.ok("I3 it names the skill and the Packets folder id",
        pInt.includes("application-packet-builder") && pInt.includes("1m0ruwyAbO6SLFFQ7-ebVKhiCQTvQFtTP"));
      R.ok("I4 it keeps the never-submit and never-claim rules inside the brief",
        /never submit or transmit anything/.test(pInt) && /FEA, CFD, NX, Teamcenter, ANSYS, AutoCAD/.test(pInt));
      R.ok("I5 it keeps the voice pass with Opus rather than the subagent",
        /read it for voice/.test(pInt) && /Rewrite it in place/.test(pInt));
      R.ok("I6 no em dash reaches the clipboard, on either kind",
        !pInt.includes("\u2014") && !pSch.includes("\u2014"));
      R.ok("I7 the scholarship prompt asks for the essay bank, not for housing",
        /essay bank/.test(pSch) && !/housing/.test(pSch), pSch.slice(0, 80));
      /* I8 to I11 hold the writing system that came over from career-ops on
         2026-08-24. The four questions are asked by Opus and not by the
         subagent, because a subagent cannot ask Joaquin anything and his answer
         to C is the only paragraph of the letter that is genuinely his. */
      R.ok("I8 Opus asks the four questions before it spawns anything",
        /before you spawn anything/.test(pInt) && /first week/.test(pInt) &&
        /D\. Tone/.test(pInt) && /wait for my answers/.test(pInt), pInt.slice(0, 80));
      R.ok("I9 the brief tells the subagent to run the gate and not to build on a block",
        /check_letter\.py/.test(pInt) && /Exit code 2 means do not build/.test(pInt) &&
        /There is no bypass/.test(pInt));
      R.ok("I10 the brief bans negative parallelism and dead AI vocabulary",
        /negative parallelism/i.test(pInt) && /dead AI vocabulary/i.test(pInt) &&
        /leverage/.test(pInt) && /seamless/.test(pInt));
      R.ok("I11 the brief no longer demands a number in every paragraph",
        !/[Ee]very body paragraph carries a/.test(pInt) &&
        /not put one in every paragraph on a cadence/.test(pInt));
      await ctx.close();
    }
  } finally {
    await browser.close();
    server.close();
  }

  process.exit(R.summary() ? 0 : 1);
})();
