/* verify-upgrade.js -- round trip and fixed point. 8 assertions.
 *
 * The question this suite answers is the one that actually matters for the
 * artifact: if the page publishes itself, and the shell transforms what it
 * published, and the page then publishes again, does the document converge or
 * does it grow a wrapper every time?
 *
 * Run:  node verify-upgrade.js
 */
const fs = require("fs");
const path = require("path");
const os = require("os");
const { execFileSync } = require("child_process");
const { chromium } = require("playwright");
const A = require("./accdoc.js");
const H = require("./harness.js");

const FIX = process.env.ACC_FIX || "/tmp/acc-fixtures";
const REAL_SLUG = "int-kiewit-equipment-eng-intern";

/* Shell out to shell.py rather than reimplementing the transform here. One
 * definition of the transform, not two that can drift apart. */
function shellTransform(src) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "accsh-"));
  const i = path.join(dir, "in.html"), o = path.join(dir, "out.html");
  fs.writeFileSync(i, src);
  execFileSync("python3", [path.join(__dirname, "shell.py"), i, o, "--base", H.BASE], { stdio: "pipe" });
  return fs.readFileSync(o, "utf8");
}

async function publishOnce(browser, url, slug) {
  const { ctx, page } = await H.openPage(browser, url, "resolve");
  await page.evaluate(s => window.toggle(s), slug);
  await page.waitForTimeout(H.DEBOUNCE_WAIT);
  const pubs = await page.evaluate(() => window.__pub);
  await ctx.close();
  return pubs[0];
}

(async () => {
  const R = new H.Report("verify-upgrade.js");
  const browser = await chromium.launch(process.env.ACC_CHROMIUM?{executablePath:process.env.ACC_CHROMIUM}:{});
  const servers = [];
  try {
    const s1 = await H.serve(FIX); servers.push(s1.server);
    const gen1 = await publishOnce(browser, s1.url, REAL_SLUG);

    /* generation 2: what the shell would serve back after that publish */
    const served2 = shellTransform(gen1);
    const m2 = A.markerCounts(served2);
    R.ok("G1 after a shell round trip every marker still appears exactly once",
      Object.values(m2).every(v => v === 1), JSON.stringify(m2));

    const rebuilt2 = A.rebuild(served2);
    R.ok("G2 reconstruction of the served copy is byte-identical to what was published",
      rebuilt2 === gen1, `rebuilt ${rebuilt2.length} vs published ${gen1.length}`);

    const served3 = shellTransform(rebuilt2);
    const rebuilt3 = A.rebuild(served3);
    R.ok("G3 a third generation does not drift, so wrapper nesting cannot compound",
      rebuilt3 === rebuilt2, `gen3 ${rebuilt3.length} vs gen2 ${rebuilt2.length}`);

    const k2 = A.markupCounts(rebuilt2);
    R.ok("G4 the reconstruction carries exactly one html and one body wrapper",
      k2.html === 1 && k2.htmlClose === 1 && k2.body === 1 && k2.bodyClose === 1, JSON.stringify(k2));

    /* Everything outside the state block must be untouched by a state swap. */
    const base0 = fs.readFileSync(path.join(FIX, "index.html"), "utf8");
    const strip = s => { const a = s.indexOf(A.S_A), b = s.indexOf(A.S_B); return s.slice(0, a) + s.slice(b); };
    R.ok("G5 a state swap changes nothing outside the state block",
      strip(A.rebuild(base0)) === strip(gen1),
      `${strip(A.rebuild(base0)).length} vs ${strip(gen1).length}`);

    /* generation 2 in a clean browser, no localStorage at all */
    const dir2 = fs.mkdtempSync(path.join(os.tmpdir(), "accgen2-"));
    fs.writeFileSync(path.join(dir2, "index.html"), served2);
    const s2 = await H.serve(dir2); servers.push(s2.server);
    {
      const { ctx, page } = await H.openPage(browser, s2.url, "resolve");
      /* A ticked row leaves the Internships tab for the Applied archive, so look
       * on every tab rather than assuming which one holds it. Assuming cost a
       * false negative the first time this assertion was written. */
      const checked = await page.evaluate(async slug => {
        const find = () => document.querySelector(`input[type=checkbox][onchange*="${slug}"]`);
        let cb = find();
        if (!cb) {
          for (const b of Array.from(document.querySelectorAll("#nav button"))) {
            b.click();
            await new Promise(r => setTimeout(r, 30));
            cb = find();
            if (cb) break;
          }
        }
        return cb ? cb.checked : null;
      }, REAL_SLUG);
      R.ok("G6 the tick is present on a clean load with no localStorage", checked === true, String(checked));
      await page.waitForTimeout(H.DEBOUNCE_WAIT);
      const pubs = await page.evaluate(() => window.__pubCount);
      R.eq("G7 the second generation does not immediately republish itself", pubs, 0);
      await ctx.close();
    }

    /* a mutilated document must refuse to publish, not publish a guess */
    const dir3 = fs.mkdtempSync(path.join(os.tmpdir(), "accbad-"));
    fs.writeFileSync(path.join(dir3, "index.html"), base0.replace(A.B_B, "<!--not-a-marker-->"));
    const s3 = await H.serve(dir3); servers.push(s3.server);
    {
      const { ctx, page } = await H.openPage(browser, s3.url, "resolve");
      await page.evaluate(s => window.toggle(s), REAL_SLUG);
      await page.waitForTimeout(H.DEBOUNCE_WAIT);
      const pubs = await page.evaluate(() => window.__pubCount);
      const chip = ((await page.locator("#sync").textContent()) || "").trim();
      R.ok("G8 a missing document marker refuses to publish and says so",
        pubs === 0 && /save failed/.test(chip), `pubs=${pubs} chip=${chip}`);
      await ctx.close();
    }
  } finally {
    await browser.close();
    servers.forEach(s => s.close());
  }
  process.exit(R.summary() ? 0 : 1);
})();
