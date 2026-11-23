// Snímky vlastních produktových stránek: nafotí skutečnou aplikaci (tapkasa/index.html) podle průběhu v cpp-data.mjs
// a zasadí obrazovky do stejné grafiky jako výchozí snímky (frame.html).
//   node store/shots/cpp-shots.mjs [--pages de-weihnachtsmarkt,us-bake-sale] [--step capture|compose] [--out <složka>]
// Výstup: <out>/cpp/<stránka>/raw/{phone,tablet}-<obrazovka>.png
//         <out>/cpp/<stránka>/<locale>/{iphone69,ipad13}/NN-….png   a přehled <out>/cpp/index.html
// Potřebuje playwright-core (PLAYWRIGHT_CORE=/cesta/k/playwright-core/index.mjs) a Google Chrome. Aplikaci nemění.
import fs from 'node:fs';
import path from 'node:path';
import { APP_FILE, appText } from './data.mjs';
import { PAGES } from './cpp-data.mjs';
import { SHOTS_DIR, AS_SETS, pngSize } from '../tool/shots-common.mjs';
const { chromium } = await import(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const args = process.argv.slice(2);
const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
const ROOT = path.join(opt('--out') || SHOTS_DIR, 'cpp');
const only = (opt('--pages') || '').split(',').filter(Boolean), step = opt('--step') || 'all';
const DEV = { phone: { width: 440, height: 956, dsf: 3 }, tablet: { width: 1032, height: 1376, dsf: 2 } };
// Vlastní stránka: iPhone 6,9" a iPad 13" (aplikace iPad podporuje, výchozí stránka má obě sady).
const CANVAS = {
  iphone69: { ...AS_SETS.iphone69, dsf: 3, kind: 'phone' },
  ipad13: { ...AS_SETS.ipad13, dsf: 2, kind: 'tablet' },
};
const COLORS = ['cervena', 'oranzova', 'zluta', 'hneda', 'ruzova', 'zelena'];
const APP = 'file://' + APP_FILE;
// Angličtina s dolarem bere v aplikaci přednostně slova z EN_US (Register místo Till); jinak slovník jazyka.
let usDict = null;
function text(P, key) {
  if (P.lang === 'en' && P.cur === 'USD') {
    if (!usDict) {
      const src = fs.readFileSync(APP_FILE, 'utf8'), a = src.indexOf('var EN_US = {');
      usDict = a < 0 ? '' : src.slice(a, src.indexOf('\n  };', a));
    }
    const m = usDict.match(new RegExp(`\\n\\s*${key}: ("(?:[^"\\\\]|\\\\.)*")`));
    if (m) return JSON.parse(m[1]);
  }
  return appText(P.lang, key);
}
const browser = await chromium.launch({ channel: 'chrome', headless: true });

function itemsFor(P) {
  const it = P.goods.map(([name, price], i) => ({ id: 'g' + i, name, price, color: COLORS[i] }));
  if (P.dep) {
    it.push({ id: 'dep', name: text(P, 'depItem'), price: P.dep, color: 'nebeska', dep: true });
    it.push({ id: 'ret', name: text(P, 'depReturn'), price: -P.dep, color: 'grafit', dep: true });
  }
  return it;
}
const base = (P, mode, extra = {}) => ({ v: 3, setup: true, tourDone: true, event: P.event, mode, nextNo: 41, voice: true, pair: '', license: 'pro',
  lang: P.lang, currency: P.cur, payDay: '', payN: 0, vat: false, biz: '', items: itemsFor(P), order: [], sales: [], archives: [], ...(P.state || {}), ...extra });

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

async function capture(key, P) {
  const dir = path.join(ROOT, key, 'raw'); fs.mkdirSync(dir, { recursive: true });
  let phoneSales = null;
  for (const dev of Object.keys(DEV)) {
    const { ctx, p } = await open(dev, base(P, 'kasa'));
    let toast = false;
    const hideToast = async () => { if (toast) { await p.locator('[data-hidetoast]').first().click({ timeout: 800 }).catch(() => { }); toast = false; } };
    // Panel placení se vysouvá animací a první ťuknutí během ní aplikace záměrně nebere, proto po otevření panelu chvíli počkat.
    const tap = async (sel, n = 1) => { for (let i = 0; i < n; i++) { await p.locator(sel).first().click(); await p.waitForTimeout(/data-(pay|method)/.test(sel) ? 550 : 130); } };
    const h = {
      add: async (id, n = 1) => { await hideToast(); await tap(`[data-add="${id}"]`, n); },
      toggle: () => tap('[data-toggle]'),
      pay: async () => { await hideToast(); await tap('[data-pay]'); },
      tip: (pct) => tap(`[data-tip="${pct}"]`),
      method: (m) => tap(`[data-method="${m}"]`),
      notes: async (notes) => { for (const n of notes) await tap(`[data-note="${n}"]`); },
      commit: async () => { await tap('[data-commit]'); toast = true; },
      tab: async (t) => { await hideToast(); await tap(`[data-tab="${t}"]`); },
      shot: async (name, o = {}) => { if (!o.keepToast) await hideToast(); await p.waitForTimeout(450); await p.screenshot({ path: path.join(dir, `${dev}-${name}.png`) }); },
    };
    h.payCash = async (notes) => { await h.pay(); await h.method('cash'); await h.notes(notes); };
    h.payCard = async () => { await h.pay(); await h.method('card'); };
    h.payExact = async () => { await h.pay(); await h.method('cash'); await tap('[data-exact]'); await h.commit(); };
    await P.flow(h);
    const st = await p.evaluate(() => JSON.parse(localStorage.getItem('kavakasa.v1')));
    if (dev === 'phone') {
      phoneSales = { sales: st.sales, nextNo: st.nextNo, evId: st.evId };
      fs.writeFileSync(path.join(dir, 'state.json'), JSON.stringify({ lastNo: st.sales.map((x) => x.no).sort((x, y) => x - y)[3], total: st.sales.reduce((t, x) => t + x.total, 0),
        currency: P.cur, appVersion: (fs.readFileSync(APP_FILE, 'utf8').match(/APP_VERSION = "([^"]+)"/) || [])[1] }, null, 1));
    }
    console.log(key, dev, 'účtů', st.sales.length, 'tržba', st.sales.reduce((s, x) => s + x.total, 0), P.cur);
    await ctx.close();
  }
  // Výdej: druhé zařízení se stejnými prvními čtyřmi účty (ve skutečnosti je dostane párováním); první vydaný celý, druhý zčásti.
  if (!P.shots.some((s) => s.b === 'counter' || s.a === 'counter')) return;
  const sales = phoneSales.sales.slice().sort((x, y) => x.no - y.no).slice(0, 4).map((s, i) => {
    const c = JSON.parse(JSON.stringify(s));
    if (i === 0) c.lines.forEach((l) => { l.ready = l.qty; });
    if (i === 1) c.lines[0].ready = c.lines[0].qty;
    return c;
  });
  for (const dev of Object.keys(DEV)) {
    const { ctx, p } = await open(dev, base(P, 'vydej', { sales, nextNo: phoneSales.nextNo, evId: phoneSales.evId, license: '' }));
    await p.waitForTimeout(400);
    await p.screenshot({ path: path.join(dir, `${dev}-counter.png`) });
    await ctx.close();
  }
}

const TPL = new URL('./frame.html', import.meta.url).href;
async function compose(key, P) {
  const rawDir = path.join(ROOT, key, 'raw');
  const st = JSON.parse(fs.readFileSync(path.join(rawDir, 'state.json'), 'utf8'));
  // Druhé zařízení v páru je vždy telefon kasy (jako u výchozích snímků), pozadí podle plátna.
  const raw = (dev, name) => { const f = path.join(rawDir, `${dev}-${name}.png`); const s = pngSize(f); return { src: 'file://' + encodeURI(f), aspect: s.h / s.w, tablet: dev === 'tablet' }; };
  for (const [set, c] of Object.entries(CANVAS)) {
    const dir = path.join(ROOT, key, P.as, set);
    fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const ctx = await browser.newContext({ viewport: { width: c.w / c.dsf, height: c.h / c.dsf }, deviceScaleFactor: c.dsf });
    for (const [i, s] of P.shots.entries()) {
      const spec = { layout: s.layout, w: c.w, h: c.h, kind: c.kind, tone: s.tone, lines: s.lines };
      if (s.layout === 'single') spec.a = raw(c.kind, s.a);
      else { spec.a = raw('phone', s.a); spec.b = raw(c.kind, s.b); }
      if (s.pills) spec.pills = [text(P, 'roleKasa'), text(P, 'roleVydej')];
      if (s.bubble) spec.bubble = text(P, 'speakNewOrder').replace('{0}', st.lastNo);
      const p = await ctx.newPage();
      await p.addInitScript((x) => { window.__SPEC = x; }, spec);
      await p.goto(TPL);
      await p.waitForFunction('window.__ready === true', null, { timeout: 15000 });
      await p.waitForTimeout(150);
      const file = path.join(dir, `${String(i + 1).padStart(2, '0')}-${s.a}${s.b ? '-' + s.b : ''}.png`);
      await p.screenshot({ path: file });
      const got = pngSize(file);
      if (got.w !== c.w || got.h !== c.h) throw new Error(`${file}: ${got.w}×${got.h}, čeká se ${c.w}×${c.h}`);
      await p.close();
    }
    await ctx.close();
    console.log(key, set, P.shots.length);
  }
}

for (const [key, P] of Object.entries(PAGES)) {
  if (only.length && !only.includes(key)) continue;
  if (step === 'all' || step === 'capture') await capture(key, P);
  if (step === 'all' || step === 'compose') await compose(key, P);
}
await browser.close();
// přehled
const rel = (f) => encodeURI(path.relative(ROOT, f));
let html = '<!doctype html><html lang="cs"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tapkasa: vlastní produktové stránky</title><style>body{font-family:-apple-system,Helvetica,Arial,sans-serif;margin:0;padding:16px 24px 60px;background:#F4F2EE;color:#14110E}h2{margin:32px 0 6px;font-size:20px;border-top:1px solid #ddd;padding-top:16px}h3{font-size:13px;color:#6E6961;margin:14px 0 6px}.row{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px}.row img{height:360px;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.15)}</style><h1>Tapkasa: vlastní produktové stránky</h1>';
for (const [key, P] of Object.entries(PAGES)) {
  const sets = Object.keys(CANVAS).map((s) => path.join(ROOT, key, P.as, s)).filter((d) => fs.existsSync(d));
  if (!sets.length) continue;
  html += `<h2>${key} · ${P.as} · ${P.cur}</h2>`;
  for (const d of sets) html += `<h3>${path.basename(d)}</h3><div class="row">` + fs.readdirSync(d).filter((f) => f.endsWith('.png')).sort().map((f) => `<a href="${rel(path.join(d, f))}" target="_blank"><img loading="lazy" src="${rel(path.join(d, f))}"></a>`).join('') + '</div>';
}
fs.writeFileSync(path.join(ROOT, 'index.html'), html);
console.log('hotovo ->', ROOT);
