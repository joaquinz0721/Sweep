/* verify-upgrade2.js -- layout and reading position. 7 assertions.
 *
 * The page body must never scroll sideways. Measured before the fix: 1140px of
 * content in a 390px viewport. Every table now sits in its own horizontal
 * scroller, so a wide table scrolls inside its own box and the page around it
 * stays where he put it.
 *
 * Run:  node verify-upgrade2.js
 */
const fs = require("fs");
const path = require("path");
const os = require("os");
const { chromium } = require("playwright");
const H = require("./harness.js");

const FIX = process.env.ACC_FIX || "/tmp/acc-fixtures";
const REAL_SLUG = "int-kiewit-equipment-eng-intern";

(async () => {
  const R = new H.Report("verify-upgrade2.js");
  const browser = await chromium.launch(process.env.ACC_CHROMIUM?{executablePath:process.env.ACC_CHROMIUM}:{});
  const servers = [];
  try {
    const s1 = await H.serve(FIX); servers.push(s1.server);

    for (const w of [390, 760, 1440]) {
      const { ctx, page } = await H.openPage(browser, s1.url, "absent", { viewport: { width: w, height: 900 } });
      const m = await page.evaluate(() => ({
        sw: document.documentElement.scrollWidth,
        cw: document.documentElement.clientWidth,
        bsw: document.body.scrollWidth
      }));
      R.ok(`H${[390, 760, 1440].indexOf(w) + 1} zero horizontal overflow at ${w}px`,
        m.sw === m.cw && m.bsw <= m.cw, JSON.stringify(m));
      await ctx.close();
    }

    /* stacked cards under the breakpoint, a real table above it */
    {
      const { ctx, page } = await H.openPage(browser, s1.url, "absent", { viewport: { width: 390, height: 900 } });
      const s = await page.evaluate(() => {
        const td = document.querySelector(".tw td"), th = document.querySelector(".tw thead");
        return { td: td && getComputedStyle(td).display, thead: th && getComputedStyle(th).display };
      });
      R.ok("H4 under 700px rows become stacked cards and the header row is hidden",
        s.td === "block" && s.thead === "none", JSON.stringify(s));
      await ctx.close();
    }
    {
      const { ctx, page } = await H.openPage(browser, s1.url, "absent", { viewport: { width: 1440, height: 900 } });
      const s = await page.evaluate(() => {
        const td = document.querySelector(".tw td"), tw = document.querySelector(".tw");
        return { td: td && getComputedStyle(td).display, ox: tw && getComputedStyle(tw).overflowX };
      });
      R.ok("H5 above 700px it is a real table and the wide table scrolls inside .tw",
        s.td === "table-cell" && s.ox === "auto", JSON.stringify(s));
      await ctx.close();
    }

    /* the publish reloads the view, so the reading position is parked first */
    {
      const { ctx, page } = await H.openPage(browser, s1.url, "resolve");
      await page.evaluate(() => { const b = document.querySelectorAll("#nav button")[1]; if (b) b.click(); });
      await page.evaluate(() => window.scrollTo(0, 400));
      await page.evaluate(s => window.toggle(s), REAL_SLUG);
      await page.waitForTimeout(H.DEBOUNCE_WAIT);
      const ui = await page.evaluate(() => sessionStorage.getItem("acc_ui_v1"));
      let parsed = null; try { parsed = JSON.parse(ui); } catch (e) {}
      R.ok("H6 the reading position is parked in sessionStorage before the publish",
        !!parsed && typeof parsed.tab === "string" && typeof parsed.y === "number",
        String(ui).slice(0, 140));
      await ctx.close();
    }

    /* the JS guard has to carry mobile alone when the shell supplies the head */
    {
      const served = fs.readFileSync(path.join(FIX, "index.html"), "utf8");
      const stripped = served.replace(/<meta name="viewport"[^>]*>\s*/g, "");
      const dir = fs.mkdtempSync(path.join(os.tmpdir(), "accnovp-"));
      fs.writeFileSync(path.join(dir, "index.html"), stripped);
      const s2 = await H.serve(dir); servers.push(s2.server);
      const { ctx, page } = await H.openPage(browser, s2.url, "absent", { viewport: { width: 390, height: 900 } });
      const m = await page.evaluate(() => ({
        meta: !!document.querySelector("meta[name=viewport]"),
        sw: document.documentElement.scrollWidth,
        cw: document.documentElement.clientWidth
      }));
      R.ok("H7 with no viewport meta served, the JS guard adds one and 390px still does not scroll sideways",
        m.meta === true && m.sw === m.cw, JSON.stringify(m));
      await ctx.close();
    }
  } finally {
    await browser.close();
    servers.forEach(s => s.close());
  }
  process.exit(R.summary() ? 0 : 1);
})();
