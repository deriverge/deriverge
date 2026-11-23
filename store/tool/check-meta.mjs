// Kontrola textů obchodů (store/meta): délky, opakovaná slova v názvu, podtitulu a klíčových slovech, značky konkurence,
// dlouhé pomlčky, kontakty. Nic nikam neposílá.   node store/tool/check-meta.mjs [--print]
import { LANGS, appstore, play } from '../meta/index.mjs';
import { len } from './clients.mjs';
const BRANDS = ['square', 'sumup', 'zettle', 'paypal', 'shopify', 'loyverse', 'storyous', 'dotykacka', 'dotykačka', 'namarkuj', 'tunder', 'quickbon', 'ready2order', 'kassenhelfer', 'orderassist', 'cashbox', 'lightspeed', 'izettle', 'clover', 'toast', 'stripe', 'salesplay', 'kyte', 'elementary', 'profi účtenka', 'ecopos', 'mkasa', 'lilka', 'boothlog', 'boothtap', 'fairpulse', 'tactill', 'bartill', 'kassemo', 'hellocash', 'kash'];
const STOP = new Set(['a', 'i', 'na', 'pro', 'the', 'for', 'and', 'für', 'den', 'und', 'de', 'di', 'e', 'y', 'et', 'pour', 'per', 'para', 'aj', 'do', 'of', 'la', 'le', 'il', '&']);
const words = (s) => s.toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(Boolean);
let bad = 0;
const err = (...a) => { bad++; console.log('CHYBA', ...a); };
const print = process.argv.includes('--print');
const common = (where, text) => {
  if (/[—–]/.test(text.replace(/\d–\d/g, ''))) err(where, 'dlouhá pomlčka');
  if (/mojekafe/i.test(text)) err(where, 'mojekafe');
  if (/\+?\d[\d ]{8,}\d/.test(text)) err(where, 'vypadá jako telefon');
  for (const m of text.matchAll(/[\w.+-]+@[\w.-]+/g)) if (m[0] !== 'info@deriverge.com') err(where, 'cizí e-mail', m[0]);
  const low = ' ' + text.toLowerCase() + ' ';
  for (const b of BRANDS) if (new RegExp(`[^\\p{L}]${b}[^\\p{L}]`, 'u').test(low)) err(where, 'značka konkurence:', b);
  if (/\{STORE\}|\$\{|undefined|TODO|DOPLŇ/.test(text)) err(where, 'nedoplněný zástupný text');
  if (/\s$|^\s/.test(text)) err(where, 'mezera na začátku nebo konci');
};
for (const season of ['xmas', 'year']) for (const version of ['1.0.8', '1.0.9']) {
  const A = appstore({ season, version });
  for (const [loc, t] of Object.entries(A)) {
    const w = `App Store ${loc} [${season} ${version}]`;
    const lim = { name: 30, subtitle: 30, keywords: 100, promotionalText: 170, description: 4000, whatsNew: 4000 };
    for (const [k, max] of Object.entries(lim)) { if (len(t[k]) > max) err(w, k, len(t[k]), '>', max); if (!t[k]) err(w, k, 'prázdné'); common(w + ' ' + k, t[k]); }
    if (!t.name.startsWith('Tapkasa')) err(w, 'název nezačíná jménem aplikace (pravidlo 10)');
    if (/, | ,/.test(t.keywords)) err(w, 'mezera u čárky v klíčových slovech');
    const kw = t.keywords.split(',');
    const seen = new Map();
    const add = (word, src) => { if (STOP.has(word)) return; if (seen.has(word) && !(seen.get(word) === src && src !== 'keywords')) err(w, `slovo „${word}“ dvakrát (${seen.get(word)} a ${src})`); seen.set(word, src); };
    for (const x of words(t.name)) add(x, 'název');
    for (const x of words(t.subtitle)) add(x, 'podtitul');
    for (const k of kw) for (const x of words(k)) add(x, 'keywords');
    if (len(t.whatsNew) > 500) err(w, 'Co je nového přes 500 znaků (nevejde se do poznámek Google Play)');
    if (season === 'xmas' && version === '1.0.9') console.log(`${loc.padEnd(6)} název ${String(len(t.name)).padStart(2)}/30  podtitul ${String(len(t.subtitle)).padStart(2)}/30  klíč. slova ${String(len(t.keywords)).padStart(3)}/100  promo vánoční ${len(t.promotionalText)}/170, celoroční ${len(appstore({ season: 'year', version })[loc].promotionalText)}/170  popis ${len(t.description)}/4000  novinky 1.0.8 ${len(appstore({ season, version: '1.0.8' })[loc].whatsNew)}, 1.0.9 ${len(t.whatsNew)}`);
    if (print && season === 'xmas' && version === '1.0.9') console.log(JSON.stringify({ name: t.name, subtitle: t.subtitle, keywords: t.keywords, promo: t.promotionalText }, null, 1));
  }
}
for (const season of ['xmas', 'year']) {
  const P = play({ season });
  for (const [loc, t] of Object.entries(P)) {
    const w = `Google Play ${loc} [${season}]`;
    const lim = { title: 30, shortDescription: 80, fullDescription: 4000 };
    for (const [k, max] of Object.entries(lim)) { if (len(t[k]) > max) err(w, k, len(t[k]), '>', max); common(w + ' ' + k, t[k]); }
    if (/App Store/.test(t.fullDescription)) err(w, 'popis pro Play zmiňuje App Store');
    if (season === 'xmas') console.log(`Play ${loc.padEnd(6)} název ${len(t.title)}/30  krátký vánoční ${len(t.shortDescription)}/80, celoroční ${len(play({ season: 'year' })[loc].shortDescription)}/80  popis ${len(t.fullDescription)}/4000`);
  }
}
for (const t of Object.values(LANGS)) if (/Google Play/.test(t.desc(t.stores.as))) err(t.as.locale, 'popis pro App Store zmiňuje Google Play');
console.log(bad ? `\n${bad} chyb` : '\nVše v pořádku.');
process.exit(bad ? 1 : 0);
