// Srovná ceny v Google Play s cenami v App Store (David schválil 23. 11. 2026 pro Tapkasu a VZT Montér).
// Cena pro zemi Play se bere z App Store podle měny: má-li měna v App Store jedinou cenu, použije se ta;
// u dolaru cena USA, u eura cena Německa; měny, které App Store nemá, přepočte Google z dolarové ceny.
//   node store/vydani/ceny-jako-ios.mjs tapkasa|vzt [--go]      (bez --go jen vypíše, co by změnil)
import { asc, play } from '../tool/clients.mjs';
const ascApi = await asc();
const playApi = await play();
const GO = process.argv.includes('--go');
const RV = 'regionsVersion.version=2026/01';
const APPS = {
  tapkasa: { pkg: 'com.deriverge.tapkasa', ascApp: '6807075649', subs: { 'tapkasa.pro.monthly': 'tapkasa.pro.monthly', 'tapkasa.pro.yearly': 'tapkasa.pro.yearly' } },
  vzt: { pkg: 'cz.vztmonter.app', ascApp: '6806400438', oneTime: { 'cz.vztmonter.app.pro': 'cz.vztmonter.app.pro' } },
};
const app = APPS[process.argv[2]];
if (!app) { console.log('použití: tapkasa|vzt [--go]'); process.exit(1); }
const money = (currencyCode, v) => { const u = Math.floor(v + 1e-9); return { currencyCode, units: String(u), nanos: Math.round((v - u) * 100) * 10000000 }; };
const num = (p) => Number(p.units || 0) + (p.nanos || 0) / 1e9;
async function all(path) {
  const data = [], included = [];
  let next = path;
  while (next) { const r = await ascApi('GET', next); data.push(...r.data); included.push(...(r.included || [])); next = r.links?.next || null; }
  return { data, included };
}
/** Ceny App Store po měnách: { CZK: Set(129), USD: Set(4.99, …) } a ceny USA a Německa. */
function byCurrency(rows, pointType, rel) {
  const terr = Object.fromEntries(rows.included.filter((x) => x.type === 'territories').map((t) => [t.id, t.attributes.currency]));
  const pts = Object.fromEntries(rows.included.filter((x) => x.type === pointType).map((p) => [p.id, Number(p.attributes.customerPrice)]));
  const today = new Date().toISOString().slice(0, 10);
  const latest = {};
  for (const d of rows.data) {
    const t = d.relationships.territory?.data?.id; const start = d.attributes.startDate || '0000';
    if (!t || start > today) continue;
    if (!latest[t] || start >= latest[t].start) latest[t] = { start, price: pts[d.relationships[rel].data.id] };
  }
  const cur = {};
  for (const [t, v] of Object.entries(latest)) (cur[terr[t]] ||= new Set()).add(v.price);
  return { cur, usa: latest.USA?.price, deu: latest.DEU?.price, n: Object.keys(latest).length };
}
function resolve(ios, google) {
  const how = { stejná: 0, usa: 0, německo: 0, přepočet: 0 }; const out = {};
  for (const [code, v] of Object.entries(google)) {
    const c = v.price.currencyCode; const set = ios.cur[c];
    if (c === 'USD') { out[code] = money('USD', ios.usa); how.usa++; }
    else if (c === 'EUR') { out[code] = money('EUR', ios.deu); how.německo++; }
    else if (set && set.size === 1) { out[code] = money(c, [...set][0]); how.stejná++; }
    else { out[code] = v.price; how.přepočet++; }
  }
  return { out, how };
}
const show = (cfgs, pick) => ['CZ', 'US', 'DE', 'GB', 'PL', 'CH', 'HU', 'JP', 'BR'].map((c) => { const x = cfgs.find((y) => y.regionCode === c); return x ? `${c} ${num(pick(x)).toFixed(2)} ${pick(x).currencyCode}` : c + ' -'; }).join(', ');

for (const [playId, iosId] of Object.entries(app.subs || {})) {
  const g = await ascApi('GET', `/v1/apps/${app.ascApp}/subscriptionGroups?include=subscriptions&limit=10`);
  const s = (g.included || []).find((x) => x.type === 'subscriptions' && x.attributes.productId === iosId);
  const ios = byCurrency(await all(`/v1/subscriptions/${s.id}/prices?include=subscriptionPricePoint,territory&limit=200`), 'subscriptionPricePoints', 'subscriptionPricePoint');
  const sub = playApi('GET', `/applications/${app.pkg}/subscriptions/${playId}`);
  for (const bp of sub.basePlans) {
    const conv = playApi('POST', `/applications/com.deriverge.tapkasa/pricing:convertRegionPrices`, { price: money('USD', ios.usa) }).convertedRegionPrices;
    const { out, how } = resolve(ios, conv);
    console.log(`\n${playId} / ${bp.basePlanId}: App Store ${ios.n} zemí, USA ${ios.usa} $, Německo ${ios.deu} €`);
    console.log(' teď :', show(bp.regionalConfigs, (x) => x.price));
    bp.regionalConfigs = bp.regionalConfigs.map((c) => ({ ...c, price: out[c.regionCode] || c.price }));
    bp.otherRegionsConfig = { ...(bp.otherRegionsConfig || {}), usdPrice: money('USD', ios.usa), eurPrice: money('EUR', ios.deu) };
    console.log(' nově:', show(bp.regionalConfigs, (x) => x.price), '|', JSON.stringify(how));
  }
  if (GO) { const r = playApi('PATCH', `/applications/${app.pkg}/subscriptions/${playId}?updateMask=basePlans&${RV}`, sub); console.log(' uloženo:', r.basePlans.map((b) => `${b.basePlanId}:${b.state}`).join(' ')); }
}
for (const [playId, iosId] of Object.entries(app.oneTime || {})) {
  const l = await ascApi('GET', `/v1/apps/${app.ascApp}/inAppPurchasesV2?limit=50`);
  const p = l.data.find((x) => x.attributes.productId === iosId);
  const rows = { data: [], included: [] };
  for (const kind of ['manualPrices', 'automaticPrices']) { const r = await all(`/v1/inAppPurchasePriceSchedules/${p.id}/${kind}?include=inAppPurchasePricePoint,territory&limit=200`); rows.data.push(...r.data); rows.included.push(...r.included); }
  const ios = byCurrency(rows, 'inAppPurchasePricePoints', 'inAppPurchasePricePoint');
  const prod = (playApi('GET', `/applications/${app.pkg}/oneTimeProducts`).oneTimeProducts || []).find((x) => x.productId === playId);
  for (const o of prod.purchaseOptions) {
    const conv = playApi('POST', `/applications/com.deriverge.tapkasa/pricing:convertRegionPrices`, { price: money('USD', ios.usa) }).convertedRegionPrices;
    const { out, how } = resolve(ios, conv);
    console.log(`\n${playId} / ${o.purchaseOptionId}: App Store ${ios.n} zemí, USA ${ios.usa} $, Německo ${ios.deu} €`);
    console.log(' teď :', show(o.regionalPricingAndAvailabilityConfigs, (x) => x.price));
    o.regionalPricingAndAvailabilityConfigs = o.regionalPricingAndAvailabilityConfigs.map((c) => ({ ...c, price: out[c.regionCode] || c.price }));
    if (o.newRegionsConfig) o.newRegionsConfig = { ...o.newRegionsConfig, usdPrice: money('USD', ios.usa), eurPrice: money('EUR', ios.deu) };
    console.log(' nově:', show(o.regionalPricingAndAvailabilityConfigs, (x) => x.price), '|', JSON.stringify(how));
  }
  if (GO) { const r = playApi('PATCH', `/applications/${app.pkg}/onetimeproducts/${playId}?updateMask=purchaseOptions&${RV}`, prod); console.log(' uloženo:', r.purchaseOptions.map((o) => `${o.purchaseOptionId}:${o.state}`).join(' ')); }
}
