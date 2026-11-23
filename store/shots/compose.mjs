// Zasadí nafocené obrazovky (capture.mjs) do grafiky a uloží snímky ve velikostech obchodů.
//   node store/shots/compose.mjs [--locales cs,de] [--out <složka>] [--only iphone69]
// Výstup:  <out>/appstore/<locale>/{iphone69,iphone65,ipad13}/NN-….png   a   <out>/play/<jazyk>/phone/NN-….png
// a přehled <out>/index.html. Texty titulků a nabídky jsou v data.mjs.
import fs from 'node:fs';
import path from 'node:path';
import { LOCALES, SHOT_NAMES, appText } from './data.mjs';
import { SHOTS_DIR, AS_SETS, PLAY_PHONE, pngSize } from '../tool/shots-common.mjs';
const { chromium } = await import(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const args = process.argv.slice(2);
const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
const OUT = opt('--out') || SHOTS_DIR;
const only = (opt('--locales') || '').split(',').filter(Boolean), onlySet = opt('--only');
const TPL = new URL('./frame.html', import.meta.url).href;
// plátna: [složka, šířka, výška, měřítko, druh zdrojových obrazovek]
const CANVAS = {
  iphone69: { w: AS_SETS.iphone69.w, h: AS_SETS.iphone69.h, dsf: 3, kind: 'phone' },
  iphone65: { w: AS_SETS.iphone65.w, h: AS_SETS.iphone65.h, dsf: 3, kind: 'phone' },
  ipad13: { w: AS_SETS.ipad13.w, h: AS_SETS.ipad13.h, dsf: 2, kind: 'tablet' },
  play: { w: PLAY_PHONE.w, h: PLAY_PHONE.h, dsf: 3, kind: 'phone' },
};
const TONES = ['red', 'green', 'yellow', 'blue', 'ink'];
const browser = await chromium.launch({ channel: 'chrome', headless: true });
let n = 0;
for (const [key, L] of Object.entries(LOCALES)) {
  if (only.length && !only.includes(key)) continue;
  const raw = (dev, name) => { const f = path.join(OUT, 'raw', key, `${dev}-${name}.png`); const s = pngSize(f); return { src: 'file://' + encodeURI(f), aspect: s.h / s.w, tablet: dev === 'tablet' }; };
  const st = JSON.parse(fs.readFileSync(path.join(OUT, 'raw', key, 'state.json'), 'utf8'));
  for (const [set, c] of Object.entries(CANVAS)) {
    if (onlySet && onlySet !== set) continue;
    if (set === 'play' && !L.play) continue;
    const dir = set === 'play' ? path.join(OUT, 'play', L.play, 'phone') : path.join(OUT, 'appstore', L.as, set);
    fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const dev = c.kind;
    const specs = [
      { layout: 'single', a: raw(dev, 'sell') },
      { layout: 'duo', a: raw('phone', 'kasa-after'), b: raw(dev, 'counter'), pills: [appText(L.lang, 'roleKasa', L.cur), appText(L.lang, 'roleVydej', L.cur)], bubble: appText(L.lang, 'speakNewOrder', L.cur).replace('{0}', st.lastNo) },
      { layout: 'duo', a: raw('phone', 'cash'), b: raw(dev, 'history') },
      { layout: 'single', a: raw(dev, 'deposit') },
      { layout: 'single', a: raw(dev, 'card') },
    ];
    const ctx = await browser.newContext({ viewport: { width: c.w / c.dsf, height: c.h / c.dsf }, deviceScaleFactor: c.dsf });
    for (const [i, s] of specs.entries()) {
      const p = await ctx.newPage();
      await p.addInitScript((spec) => { window.__SPEC = spec; }, { ...s, w: c.w, h: c.h, kind: c.kind, tone: TONES[i], lines: L.copy[i] });
      await p.goto(TPL);
      await p.waitForFunction('window.__ready === true', null, { timeout: 15000 });
      await p.waitForTimeout(150);
      const file = path.join(dir, SHOT_NAMES[i] + '.png');
      await p.screenshot({ path: file });
      const got = pngSize(file);
      if (got.w !== c.w || got.h !== c.h) throw new Error(`${file}: ${got.w}×${got.h}, čeká se ${c.w}×${c.h}`);
      await p.close(); n++;
    }
    await ctx.close();
    console.log(key, set, specs.length);
  }
}
await browser.close();
// přehled všech snímků
const rel = (f) => encodeURI(path.relative(OUT, f));
let html = '<!doctype html><html lang="cs"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tapkasa: snímky 2026-11</title><style>body{font-family:-apple-system,Helvetica,Arial,sans-serif;margin:0;padding:16px 24px 60px;background:#F4F2EE;color:#14110E}h2{margin:32px 0 6px;font-size:20px;border-top:1px solid #ddd;padding-top:16px}h3{font-size:13px;color:#6E6961;margin:14px 0 6px}.row{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px}.row img{height:360px;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.15)}.row.s img{height:150px}</style><h1>Tapkasa: obchodní snímky (listopad 2026)</h1><p>Obrazovky jsou ze skutečné aplikace (tapkasa/index.html), stav vznikl klepáním. Malá řada ukazuje první tři snímky ve velikosti výsledků hledání.</p>';
for (const [key, L] of Object.entries(LOCALES)) {
  const sets = [['appstore/' + L.as + '/iphone69', 'App Store iPhone 6,9" (1320×2868)'], ['appstore/' + L.as + '/iphone65', 'App Store iPhone 6,5" (1284×2778)'], ['appstore/' + L.as + '/ipad13', 'App Store iPad 13" (2064×2752)']];
  if (L.play) sets.push(['play/' + L.play + '/phone', 'Google Play telefon (1080×1920)']);
  if (!fs.existsSync(path.join(OUT, sets[0][0]))) continue;
  html += `<h2>${key} · ${L.cur}</h2>`;
  const first = fs.readdirSync(path.join(OUT, sets[0][0])).filter((f) => f.endsWith('.png')).sort();
  html += '<h3>Ve výsledcích hledání (první tři)</h3><div class="row s">' + first.slice(0, 3).map((f) => `<img src="${rel(path.join(OUT, sets[0][0], f))}">`).join('') + '</div>';
  for (const [d, title] of sets) {
    const dir = path.join(OUT, d); if (!fs.existsSync(dir)) continue;
    html += `<h3>${title}</h3><div class="row">` + fs.readdirSync(dir).filter((f) => f.endsWith('.png')).sort().map((f) => `<a href="${rel(path.join(dir, f))}" target="_blank"><img loading="lazy" src="${rel(path.join(dir, f))}"></a>`).join('') + '</div>';
  }
}
fs.writeFileSync(path.join(OUT, 'index.html'), html);
console.log('vykresleno', n, '->', OUT);
