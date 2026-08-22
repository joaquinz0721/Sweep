/* shots.js -- render the board at three widths so a human can actually look.
 * A green assertion run is not a substitute for looking at the page. */
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const H = require("./harness.js");
const FIX = process.env.ACC_FIX || "/tmp/acc-fixtures";
const OUT = process.env.ACC_SHOTS || "/tmp/acc-shots";

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const { server, url } = await H.serve(FIX);
  const browser = await chromium.launch(process.env.ACC_CHROMIUM?{executablePath:process.env.ACC_CHROMIUM}:{});
  for (const w of [390, 760, 1440]) {
    const { ctx, page } = await H.openPage(browser, url, "absent", { viewport: { width: w, height: 1100 } });
    const f = path.join(OUT, `board-${w}.png`);
    await page.screenshot({ path: f, fullPage: false });
    console.log("wrote", f);
    await ctx.close();
  }
  await browser.close(); server.close();
})();
