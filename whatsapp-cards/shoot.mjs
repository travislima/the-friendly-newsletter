import pkg from '/opt/node22/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import path from 'node:path';

const dir = path.resolve('whatsapp-cards');
const file = 'file://' + path.join(dir, 'issue-019-cards.html');

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ deviceScaleFactor: 1 });
await page.goto(file, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(600);

for (const id of ['card-1', 'card-2', 'card-3', 'card-4']) {
  const el = await page.$('#' + id);
  const n = id.split('-')[1];
  const out = path.join(dir, `issue-019-${n}.png`);
  await el.screenshot({ path: out });
  console.log('wrote', out);
}

await browser.close();
