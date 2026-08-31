import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { mkdirSync } from 'node:fs';
const SP = '/tmp/claude-0/-home-user-deriverge/1455238e-1fdf-569a-95ff-a73d887ca0a6/scratchpad';
const SRC = '/home/user/deriverge/store/screenshots';
const OUT = `${SP}/promo/framed`;
mkdirSync(OUT, { recursive: true });

// mode -> [css šířka, css výška, prefix zdrojových snímků, seznam obrazovek]
const SETS = {
  '67':   [645, 1398, 'iphone67', ['01-sell','02-cash','03-orders','04-ticket','05-history','06-onboarding','07-paywall']],
  'ipad': [1024, 1366, 'ipad129',  ['01-sell','02-cash','03-orders','04-ticket','05-history']],
  'play': [540, 960,  'play',     ['01-sell','02-cash','03-orders','05-history','07-paywall']],
  'ptab': [720, 1280, 'ptablet',  ['01-sell','02-cash','03-orders','05-history']],
};

const b = await chromium.launch();
for (const lang of ['cs', 'en']) {
  for (const [mode, [w, h, prefix, shots]] of Object.entries(SETS)) {
    const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    const p = await c.newPage();
    for (const shot of shots) {
      const img = encodeURIComponent(`file://${SRC}/${prefix}-${lang}-${shot}.png`);
      await p.goto(`file://${SP}/promo/framed.html?lang=${lang}&mode=${mode}&shot=${shot}&img=${img}`);
      await p.waitForFunction(() => window.__ready === true);
      await p.waitForTimeout(250);
      await p.screenshot({ path: `${OUT}/${prefix}-${lang}-${shot}.png` });
    }
    await c.close();
  }
}
await b.close();
console.log('hotovo');
