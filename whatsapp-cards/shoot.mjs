import pkg from '/opt/node22/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import path from 'node:path';

const dir = path.resolve('whatsapp-cards');
const file = 'file://' + path.join(dir, 'issue-019-cards.html');
const ids = ['card-1', 'card-2', 'card-3', 'card-4', 'card-5', 'card-6'];

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ deviceScaleFactor: 1 });
await page.goto(file, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

// wa = 1080×1080 square (WhatsApp gallery), ig = 1080×1350 portrait (Instagram 4:5)
for (const [fmt, cls] of [['wa', 'fmt-square'], ['ig', 'fmt-portrait']]) {
  await page.evaluate((c) => { document.body.className = c; }, cls);
  await page.waitForTimeout(500);
  for (const id of ids) {
    const el = await page.$('#' + id);
    const n = id.split('-')[1];
    const out = path.join(dir, `issue-019-${fmt}-${n}.png`);
    await el.screenshot({ path: out });
    console.log('wrote', out);
  }
}

await browser.close();
