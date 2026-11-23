// Nafotí obrazovky skutečné aplikace (tapkasa/index.html) pro obchodní snímky. Stav vzniká klepáním v aplikaci:
// do úložiště se předem vloží jen nabídka stánku, jazyk a měna; účty, fronta i přehled vzniknou prodejem.
//   node store/shots/capture.mjs [--locales cs,de] [--out <složka>]
// Potřebuje playwright-core (PLAYWRIGHT_CORE=/cesta/k/playwright-core/index.mjs) a nainstalovaný Google Chrome.
// Aplikaci nemění, jen ji otevře ze souboru. Výstup: <out>/raw/<locale>/<zařízení>-<obrazovka>.png
import fs from 'node:fs';
import path from 'node:path';
import { LOCALES, APP_FILE, itemsFor } from './data.mjs';
import { SHOTS_DIR } from '../tool/shots-common.mjs';
const { chromium } = await import(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const args = process.argv.slice(2);
const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
const OUT = path.join(opt('--out') || SHOTS_DIR, 'raw');
const only = (opt('--locales') || '').split(',').filter(Boolean);
const DEV = { phone: { width: 440, height: 956, dsf: 3 }, tablet: { width: 1032, height: 1376, dsf: 2 } };
const APP = 'file://' + APP_FILE;
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const base = (L, mode, extra = {}) => ({ v: 3, setup: true, tourDone: true, event: L.event, mode, nextNo: 41, voice: true, pair: '', license: 'pro',
  lang: L.lang, currency: L.cur, payDay: '', payN: 0, vat: false, biz: '', items: itemsFor(L), order: [], sales: [], archives: [], ...extra });

async function open(dev, state) {
  const d = DEV[dev];
  const ctx = await browser.newContext({ viewport: { width: d.width, height: d.height }, deviceScaleFactor: d.dsf, isMobile: true, hasTouch: true });
  await ctx.addInitScript((s) => { try { if (!localStorage.getItem('kavakasa.v1')) localStorage.setItem('kavakasa.v1', s); } catch (e) { } }, JSON.stringify(state));
  const p = await ctx.newPage();
  p.on('pageerror', (e) => console.log('CHYBA STRÁNKY', e.message.slice(0, 200)));
  await p.goto(APP); await p.waitForTimeout(900);
  await p.evaluate(() => document.fonts && document.fonts.ready);
  return { ctx, p };
}
for (const [key, L] of Object.entries(LOCALES)) {
  if (only.length && !only.includes(key)) continue;
  const dir = path.join(OUT, key); fs.mkdirSync(dir, { recursive: true });
  let salesForCounter = null;
  for (const dev of Object.keys(DEV)) {
    const { ctx, p } = await open(dev, base(L, 'kasa'));
    const shot = async (name) => { await p.waitForTimeout(450); await p.screenshot({ path: path.join(dir, `${dev}-${name}.png`) }); };
    // Panel placení se vysouvá animací a první ťuknutí během ní aplikace záměrně nebere, proto po otevření panelu chvíli počkat.
    const tap = async (sel, n = 1) => { for (let i = 0; i < n; i++) { await p.locator(sel).first().click(); await p.waitForTimeout(/data-(pay|method)/.test(sel) ? 550 : 130); } };
    const add = (id, n = 1) => tap(`[data-add="${id}"]`, n);
    const hideToast = () => p.locator('[data-hidetoast]').first().click({ timeout: 800 }).catch(() => { });
    const payCash = async (notes) => { await tap('[data-pay]'); await tap('[data-method="cash"]'); for (const n of notes) await tap(`[data-note="${n}"]`); };
    // 1) účet se zálohou: dva horké nápoje, sladké a dva hrnky
    await add('g0', 2); await add('g2'); await add('dep', 2);
    await shot('sell');
    await payCash(L.cash);
    await shot('cash');
    await tap('[data-commit]'); await hideToast();
    // 2) druhý účet kartou
    await add('g1'); await add('g3');
    await tap('[data-pay]'); await tap('[data-method="card"]');
    await shot('card');
    await tap('[data-commit]'); await hideToast();
    // 3) a 4) další dva účty, ať je ve frontě co vydávat
    await add('g4', 2); await add('g2'); await add('dep', 2); await tap('[data-pay]'); await tap('[data-method="cash"]'); await tap('[data-exact]'); await tap('[data-commit]'); await hideToast();
    await add('g0'); await add('g5'); await tap('[data-pay]'); await tap('[data-method="cash"]'); await tap('[data-exact]'); await tap('[data-commit]');
    await shot('kasa-after');
    await hideToast();
    // 5) zákazník vrací hrnek a bere dva další nápoje: rozbalený účet se zápornou položkou
    await add('g0', 2); await add('ret');
    await tap('[data-toggle]');
    await shot('deposit');
    await tap('[data-pay]'); await tap('[data-method="cash"]'); await tap('[data-exact]'); await tap('[data-commit]'); await hideToast();
    await tap('[data-tab="history"]');
    await shot('history');
    const st = await p.evaluate(() => JSON.parse(localStorage.getItem('kavakasa.v1')));
    if (dev === 'phone') { salesForCounter = { sales: st.sales, nextNo: st.nextNo, evId: st.evId }; fs.writeFileSync(path.join(dir, 'state.json'), JSON.stringify({ lastNo: st.sales.map((x) => x.no).sort((x, y) => x - y)[3], total: st.sales.reduce((t, x) => t + x.total, 0), currency: L.cur, appVersion: (fs.readFileSync(APP_FILE, 'utf8').match(/APP_VERSION = "([^"]+)"/) || [])[1] }, null, 1)); }
    console.log(key, dev, 'účtů', st.sales.length, 'tržba', st.sales.reduce((s, x) => s + x.total, 0), L.cur);
    await ctx.close();
  }
  // Výdej: druhé zařízení se stejnými účty (ve skutečnosti je dostane párováním). První objednávka je připravená celá, druhá zčásti.
  // Výdej ukazuje stav ve chvíli, kdy kasa uložila čtvrtý účet (stejný okamžik jako snímek kasy vedle něj).
  const sales = salesForCounter.sales.slice().sort((x, y) => x.no - y.no).slice(0, 4).map((s, i) => {
    const c = JSON.parse(JSON.stringify(s));
    if (i === 0) c.lines.forEach((l) => { l.ready = l.qty; });
    if (i === 1) c.lines[0].ready = c.lines[0].qty;
    return c;
  });
  for (const dev of Object.keys(DEV)) {
    const { ctx, p } = await open(dev, base(L, 'vydej', { sales, nextNo: salesForCounter.nextNo, evId: salesForCounter.evId, license: '' }));
    await p.waitForTimeout(400);
    await p.screenshot({ path: path.join(dir, `${dev}-counter.png`) });
    await ctx.close();
  }
}
await browser.close();
console.log('nafoceno do', OUT);
