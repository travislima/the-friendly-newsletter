// Render one issue's social cards in both formats.
//
//   node card-source/shoot.mjs 025
//
// Writes 1080x1080 to whatsapp-cards/issue-NNN/ and 1080x1350 to
// instagram-cards/issue-NNN/. One HTML drives both via a body format class.
//
// Playwright and Chromium live in different places depending on the machine,
// so both are resolved at runtime rather than hardcoded. ESM ignores NODE_PATH,
// which is why the candidate paths are tried explicitly.
import path from 'node:path';
import fs from 'node:fs';
import { createRequire } from 'node:module';

const issue = process.argv[2];
if (!/^\d{3}$/.test(issue ?? '')) {
  console.error('usage: node card-source/shoot.mjs NNN   (e.g. 025)');
  process.exit(1);
}

// ---- find playwright ------------------------------------------------------
const PW_CANDIDATES = [
  '/opt/node22/lib/node_modules/playwright/index.js',   // container image
  '/usr/local/lib/node_modules/playwright/index.js',    // npm -g on macOS
  '/usr/local/lib/node_modules/playwright-core/index.js',
  'playwright',                                          // local node_modules
  'playwright-core',
];
let chromium = null;
for (const c of PW_CANDIDATES) {
  try {
    const mod = c.startsWith('/')
      ? (fs.existsSync(c) ? await import(c) : null)
      : await import(c);
    if (mod) { chromium = (mod.default ?? mod).chromium; if (chromium) break; }
  } catch { /* try the next one */ }
}
if (!chromium) {
  console.error('Could not find playwright. Install it with:\n' +
                '  npm install playwright-core\n' +
                'in this directory, or globally with npm install -g playwright-core.');
  process.exit(1);
}

// ---- find a browser binary ------------------------------------------------
const BROWSER_CANDIDATES = [
  '/opt/pw-browsers/chromium',                                                  // container image
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',               // macOS Chrome
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome',
];
const executablePath = BROWSER_CANDIDATES.find(p => fs.existsSync(p));
// No executablePath at all means "use whatever browser Playwright downloaded".

const root = process.cwd();
const src = path.join(root, 'card-source', `issue-${issue}-cards.html`);
if (!fs.existsSync(src)) { console.error(`missing ${src}`); process.exit(1); }

const targets = [
  { fmt: 'fmt-square',   dir: path.join(root, 'whatsapp-cards',  `issue-${issue}`) },
  { fmt: 'fmt-portrait', dir: path.join(root, 'instagram-cards', `issue-${issue}`) },
];
for (const t of targets) fs.mkdirSync(t.dir, { recursive: true });

const ids = ['card-1','card-2','card-3','card-4','card-5','card-6'];
const browser = await chromium.launch(executablePath ? { executablePath } : {});
const page = await browser.newPage({ deviceScaleFactor: 1 });
await page.goto('file://' + src, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
// The webfonts come off Google Fonts over the network. document.fonts.ready can
// resolve a beat before they actually paint, which silently ships fallback-font
// cards, so give them a moment before the first screenshot.
await page.waitForTimeout(1500);

for (const { fmt, dir } of targets) {
  await page.evaluate((c) => { document.body.className = c; }, fmt);
  await page.waitForTimeout(600);
  for (const id of ids) {
    const el = await page.$('#' + id);
    if (!el) { console.warn(`  missing #${id}`); continue; }
    const out = path.join(dir, `card-${id.split('-')[1]}.png`);
    await el.screenshot({ path: out });
    console.log('wrote', path.relative(root, out));
  }
}
await browser.close();
