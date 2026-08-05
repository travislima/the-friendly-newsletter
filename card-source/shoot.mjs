// Render one issue's social cards in both formats.
//
//   node card-source/shoot.mjs 020
//
// Writes 1080x1080 to whatsapp-cards/issue-NNN/ and 1080x1350 to
// instagram-cards/issue-NNN/. One HTML drives both via a body format class.
// Playwright lives at /opt/node22/lib/node_modules and ESM ignores NODE_PATH,
// so it is imported by absolute path. Chromium is at /opt/pw-browsers/chromium.
import pkg from '/opt/node22/lib/node_modules/playwright/index.js';
const { chromium } = pkg;
import path from 'node:path';
import fs from 'node:fs';

const issue = process.argv[2];
if (!/^\d{3}$/.test(issue ?? '')) {
  console.error('usage: node card-source/shoot.mjs NNN   (e.g. 020)');
  process.exit(1);
}

const root = process.cwd();
const src = path.join(root, 'card-source', `issue-${issue}-cards.html`);
if (!fs.existsSync(src)) { console.error(`missing ${src}`); process.exit(1); }

const targets = [
  { fmt: 'fmt-square',   dir: path.join(root, 'whatsapp-cards',  `issue-${issue}`) },
  { fmt: 'fmt-portrait', dir: path.join(root, 'instagram-cards', `issue-${issue}`) },
];
for (const t of targets) fs.mkdirSync(t.dir, { recursive: true });

const ids = ['card-1','card-2','card-3','card-4','card-5','card-6'];
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ deviceScaleFactor: 1 });
await page.goto('file://' + src, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

for (const { fmt, dir } of targets) {
  await page.evaluate((c) => { document.body.className = c; }, fmt);
  await page.waitForTimeout(500);
  for (const id of ids) {
    const el = await page.$('#' + id);
    if (!el) { console.warn(`  missing #${id}`); continue; }
    const out = path.join(dir, `card-${id.split('-')[1]}.png`);
    await el.screenshot({ path: out });
    console.log('wrote', path.relative(root, out));
  }
}
await browser.close();
