// Měření hledání v obchodech (veřejná rozhraní, bez přihlášení): pořadí Tapkasy, síla konkurence a našeptávač.
//   node store/tool/search-rank.mjs [itunes|hints|play|all] [--countries cz,de] → store/aso/search-<datum>.json
// iTunes Search API snese asi 20 dotazů za minutu, proto pauzy. Pořadí z API je blízké, ne totožné s hledáním v telefonu.
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { ASC_APP, PKG } from './clients.mjs';
const DAY = new Date().toISOString().slice(0, 10);
const OUT = new URL(`../aso/search-${DAY}.json`, import.meta.url).pathname;
const args = process.argv.slice(2);
const what = args.find((a) => !a.startsWith('--') && args[args.indexOf(a) - 1] !== '--countries') || 'all';
const only = args.includes('--countries') ? args[args.indexOf('--countries') + 1].split(',') : null;
const sleep = (ms) => execFileSync('sleep', [String(ms / 1000)]);
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36';
// země: [storefront Apple, hl pro Play, výrazy]
export const M = {
  cz: [143489, 'cs', ['pokladna', 'pokladna na stánek', 'kasa', 'jarmark', 'vánoční trh', 'festival', 'mobilní pokladna', 'stánek', 'pokladna zdarma', 'výdej objednávek', 'svařák', 'spolek', 'školní akce', 'vratná záloha']],
  sk: [143496, 'sk', ['pokladňa', 'pokladňa na stánok', 'kasa', 'jarmok', 'vianočné trhy', 'festival', 'mobilná pokladňa', 'stánok', 'varené víno', 'pokladňa offline']],
  de: [143443, 'de', ['kasse', 'kassensystem verein', 'vereinsfest', 'weihnachtsmarkt', 'bonkasse', 'vereinskasse', 'festkasse', 'kassen app', 'flohmarkt kasse', 'pfand', 'marktstand', 'glühwein', 'basar', 'einfache kasse']],
  at: [143445, 'de', ['kasse', 'vereinskasse', 'vereinsfest', 'weihnachtsmarkt', 'bonkasse', 'festkasse', 'kassen app', 'punschstand', 'kassa', 'punsch', 'christkindlmarkt']],
  pl: [143478, 'pl', ['kasa', 'kasa na stoisko', 'kiermasz', 'jarmark', 'kasa mobilna', 'stoisko', 'festyn', 'jarmark świąteczny', 'stragan', 'kaucja', 'kiermasz szkolny']],
  gb: [143444, 'en-GB', ['market stall pos', 'craft fair', 'bake sale', 'cash register', 'till', 'christmas market', 'pos', 'till app', 'market stall', 'school fair', 'school fete', 'car boot sale', 'fete']],
  us: [143441, 'en-US', ['market stall pos', 'craft fair', 'bake sale', 'cash register', 'pos', 'craft fair pos', 'vendor pos', 'farmers market', 'concession stand', 'simple cash register', 'booth', 'vendor', 'craft show', 'cash register app', 'fundraiser']],
  fr: [143442, 'fr', ['caisse marché', 'kermesse', 'buvette', 'caisse enregistreuse', 'caisse', 'marché de noël', 'caisse association', 'brocante']],
  it: [143450, 'it', ['cassa sagra', 'mercatino', 'cassa', 'registratore di cassa', 'sagra', 'mercatino di natale', 'cassa bar', 'bancarella']],
  es: [143454, 'es', ['caja mercadillo', 'feria', 'tpv', 'caja registradora', 'mercadillo', 'tpv puesto', 'caja', 'mercadillo navideño']],
  pt: [143453, 'pt-PT', ['caixa registadora', 'feira', 'banca', 'pos', 'caixa', 'mercado de natal', 'quermesse', 'ponto de venda']],
  br: [143503, 'pt-BR', ['caixa registradora', 'pdv', 'feira', 'quermesse', 'frente de caixa', 'caixa', 'bazar', 'festa junina']],
};
const curl = (a) => execFileSync('curl', ['-sS', '-L', '--compressed', '--max-time', '40', ...a], { maxBuffer: 128 * 1024 * 1024 }).toString();
const median = (a) => { if (!a.length) return null; const s = [...a].sort((x, y) => x - y); const m = s.length >> 1; return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2); };
const res = fs.existsSync(OUT) ? JSON.parse(fs.readFileSync(OUT)) : { day: DAY, itunes: {}, hints: {}, play: {} };
const save = () => fs.writeFileSync(OUT, JSON.stringify(res, null, 1) + '\n');
const countries = Object.keys(M).filter((c) => !only || only.includes(c));

function itunes() {
  for (const cc of countries) for (const term of M[cc][2]) {
    const key = cc + '|' + term; if (res.itunes[key]) continue;
    let j = null;
    for (let i = 0; i < 4 && !j; i++) {
      try { j = JSON.parse(curl([`https://itunes.apple.com/search?term=${encodeURIComponent(term)}&country=${cc}&entity=software&limit=200`])); } catch { sleep(20000); }
    }
    if (!j) { console.log('itunes', key, 'CHYBA'); continue; }
    const r = j.results || [];
    const pos = r.findIndex((x) => String(x.trackId) === ASC_APP);
    const top = r.slice(0, 10);
    res.itunes[key] = { results: r.length, rank: pos < 0 ? null : pos + 1, top10MedianRatings: median(top.map((x) => x.userRatingCount || 0)), top10MaxRatings: Math.max(0, ...top.map((x) => x.userRatingCount || 0)),
      top5: top.slice(0, 5).map((x) => `${x.trackName} (${x.userRatingCount || 0})`) };
    console.log('itunes', key, 'rank', res.itunes[key].rank, 'med', res.itunes[key].top10MedianRatings, '|', res.itunes[key].top5.slice(0, 3).join(' ; '));
    save(); sleep(3200);
  }
}
function hints() {
  for (const cc of countries) for (const term of M[cc][2]) {
    const key = cc + '|' + term; if (res.hints[key]) continue;
    let xml = '';
    try { xml = curl(['-H', `X-Apple-Store-Front: ${M[cc][0]},29`, `https://search.itunes.apple.com/WebObjects/MZSearchHints.woa/wa/hints?clientApplication=Software&term=${encodeURIComponent(term)}`]); } catch { }
    const list = [...xml.matchAll(/<key>term<\/key>\s*<string>([^<]*)<\/string>/g)].map((m) => m[1].replace(/&amp;/g, '&'));
    res.hints[key] = { exact: list.map((s) => s.toLowerCase()).includes(term.toLowerCase()), position: list.map((s) => s.toLowerCase()).indexOf(term.toLowerCase()) + 1 || null, hints: list };
    console.log('hints', key, res.hints[key].exact ? 'ANO' : 'ne', '|', list.slice(0, 6).join(' ; '));
    save(); sleep(700);
  }
}
const detailCache = {};
function playDetail(id, hl, gl) {
  if (detailCache[id]) return detailCache[id];
  let o = { installs: null, ratings: null };
  try {
    const html = curl(['-A', UA, `https://play.google.com/store/apps/details?id=${id}&hl=en&gl=${gl}`]);
    const m = html.match(/AF_initDataCallback\(\{key: 'ds:5'[\s\S]*?data:([\s\S]*?), sideChannel: \{\}\}\);<\/script>/);
    if (m) { const d = JSON.parse(m[1])[1][2]; o = { title: d[0]?.[0], installs: d[13]?.[1] ?? null, ratings: d[51]?.[2]?.[1] ?? 0 }; }
  } catch { }
  sleep(400);
  return (detailCache[id] = o);
}
function play() {
  for (const cc of countries) for (const term of M[cc][2]) {
    const key = cc + '|' + term; if (res.play[key]) continue;
    let html = '';
    try { html = curl(['-A', UA, `https://play.google.com/store/search?q=${encodeURIComponent(term)}&c=apps&gl=${cc.toUpperCase()}&hl=${M[cc][1]}`]); } catch { }
    const ids = []; for (const m of html.matchAll(/\/store\/apps\/details\?id=([A-Za-z0-9_.]+)/g)) if (!ids.includes(m[1])) ids.push(m[1]);
    const pos = ids.indexOf(PKG);
    const top = ids.slice(0, 5).map((id) => ({ id, ...playDetail(id, M[cc][1], cc.toUpperCase()) }));
    res.play[key] = { results: ids.length, rank: pos < 0 ? null : pos + 1, top5MedianInstalls: median(top.map((t) => t.installs || 0)), top5MedianRatings: median(top.map((t) => t.ratings || 0)), top5: top.map((t) => `${t.title || t.id} (${t.installs ?? '?'}+ / ${t.ratings ?? '?'} hodn.)`) };
    console.log('play', key, 'rank', res.play[key].rank, 'z', ids.length, 'medInst', res.play[key].top5MedianInstalls, '|', res.play[key].top5.slice(0, 3).join(' ; '));
    save(); sleep(1200);
  }
}
if (import.meta.url === 'file://' + process.argv[1]) {
  if (what === 'all' || what === 'hints') hints();
  if (what === 'all' || what === 'play') play();
  if (what === 'all' || what === 'itunes') itunes();
  save(); console.log('hotovo', OUT);
}
