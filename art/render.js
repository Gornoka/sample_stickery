// Renders SVG files to transparent 512x512 PNGs. Usage: node render.js jobs.txt (lines: "<svg>\t<png>").
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = fs.readFileSync(process.argv[2], 'utf8').trim().split('\n').map(l => l.split('\t'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 512, height: 512 }, deviceScaleFactor: 1 });
  for (const [src, out] of jobs) {
    await page.setContent(`<html><body style="margin:0;background:transparent">${fs.readFileSync(src, 'utf8')}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: 512, height: 512 } });
  }
  await browser.close();
})();
