// Pas na akci (Tapkasa 1.3.0): jednorázový spotřebovatelný nákup tapkasa.pass.event72 v App Store a Google Play.
// Kredit, který po spuštění v aplikaci odemkne Tapkasa Pro na 72 hodin na jednom zařízení; nic se neobnovuje.
//
//   node store/tool/create-pass-products.mjs              nanečisto (výchozí): jen čte a vypíše, co by založil
//   node store/tool/create-pass-products.mjs --go         založí nebo doplní produkt v obou obchodech
//   … --only asc|play        jen jeden obchod
//   … --shot <soubor.png>    snímek pro kontrolu Applu (výchozí /Volumes/T7 4TB/ClaudeDev/tapkasa-pass-review.png, 1284×2778)
//   … --submit               (jen s --go) pošle nákup v App Store ke kontrole hned; jinak se v App Store Connect
//                            přidá k verzi 1.3.0 při jejím odeslání (sekce In-App Purchases and Subscriptions)
//
// Ceny: Česko 99 Kč (základ v App Store, ostatní země přepočte Apple), USA 2,99 $, všechny země s eurem 3,99 €.
// Google Play: tytéž tři ceny, ostatní země přepočte Google z 2,99 $ (pricing:convertRegionPrices).
// Spotřebovatelnost: App Store typ CONSUMABLE; Google Play typ nemá, nákup spotřebuje RevenueCat SDK, když má produkt
// v RevenueCat (Product catalog → Products) typ Consumable. Produkt NESMÍ být v entitlementu "pro" (odemkl by Pro natrvalo)
// a nemusí být v nabídce (offering): aplikace ho kupuje přímo (mobile/billing.js).
// Skript nic nevydává a ceny existujících produktů nemění; zápis (--go) jen se souhlasem majitele.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { asc, play, ASC_APP, PKG, len } from './clients.mjs';

const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null; };
const GO = args.includes('--go'), SUBMIT = args.includes('--submit') && GO;
const ONLY = opt('--only');
const SHOT = opt('--shot') || '/Volumes/T7 4TB/ClaudeDev/tapkasa-pass-review.png';
const PRODUCT = 'tapkasa.pass.event72';
const OPTION = 'event72';                    // purchaseOptionId v Google Play
const RV = 'regionsVersion.version=2026/01';
const PRICE = { CZK: 99, USD: 2.99, EUR: 3.99 };
const log = (...a) => console.log(...a);

// Texty: App Store název ≤ 30 znaků a popis ≤ 45, Google Play název ≤ 55 a popis ≤ 200.
const TEXTS = {
  cs: { as: 'cs', gp: 'cs-CZ', name: 'Pas na akci', short: 'Pro na 72 hodin, bez předplatného',
    long: 'Jednorázový nákup: odemkne Tapkasa Pro na tomto zařízení na 72 hodin od spuštění. Nic se neobnovuje, nespuštěný pas nevyprší.' },
  sk: { as: 'sk', gp: 'sk', name: 'Pas na akciu', short: 'Pro na 72 hodín, bez predplatného',
    long: 'Jednorazový nákup: odomkne Tapkasa Pro na tomto zariadení na 72 hodín od spustenia. Nič sa neobnovuje, nespustený pas nevyprší.' },
  enUS: { as: 'en-US', gp: 'en-US', name: 'Event Pass', short: 'Pro for 72 hours, no subscription',
    long: 'One-time purchase: unlocks Tapkasa Pro on this device for 72 hours from when you start it. Nothing renews; an unstarted pass never expires.' },
  enGB: { as: 'en-GB', gp: 'en-GB', name: 'Event Pass', short: 'Pro for 72 hours, no subscription',
    long: 'One-time purchase: unlocks Tapkasa Pro on this device for 72 hours from when you start it. Nothing renews; an unstarted pass never expires.' },
  de: { as: 'de-DE', gp: 'de-DE', name: 'Event-Pass', short: 'Pro für 72 Stunden, ohne Abo',
    long: 'Einmalkauf: schaltet Tapkasa Pro auf diesem Gerät für 72 Stunden ab dem Start frei. Nichts verlängert sich, ein nicht gestarteter Pass verfällt nicht.' },
  fr: { as: 'fr-FR', gp: 'fr-FR', name: 'Pass événement', short: 'Pro pendant 72 heures, sans abonnement',
    long: 'Achat unique : débloque Tapkasa Pro sur cet appareil pendant 72 heures à partir du démarrage. Rien ne se renouvelle, un pass non démarré n’expire pas.' },
  es: { as: 'es-ES', gp: 'es-ES', name: 'Pase de evento', short: 'Pro durante 72 horas, sin suscripción',
    long: 'Compra única: desbloquea Tapkasa Pro en este dispositivo durante 72 horas desde que se activa. Nada se renueva y un pase sin activar no caduca.' },
  it: { as: 'it', gp: 'it-IT', name: 'Pass evento', short: 'Pro per 72 ore, senza abbonamento',
    long: 'Acquisto singolo: sblocca Tapkasa Pro su questo dispositivo per 72 ore dall’attivazione. Niente si rinnova e un pass non attivato non scade.' },
  pl: { as: 'pl', gp: 'pl-PL', name: 'Karnet na imprezę', short: 'Pro na 72 godziny, bez subskrypcji',
    long: 'Zakup jednorazowy: odblokowuje Tapkasa Pro na tym urządzeniu na 72 godziny od uruchomienia. Nic się nie odnawia, nieuruchomiony karnet nie wygasa.' },
  pt: { as: 'pt-PT', gp: 'pt-PT', name: 'Passe de evento', short: 'Pro durante 72 horas, sem subscrição',
    long: 'Compra única: desbloqueia a Tapkasa Pro neste dispositivo durante 72 horas a partir da ativação. Nada se renova e um passe por ativar não expira.' },
};
for (const [k, t] of Object.entries(TEXTS)) {
  if (len(t.name) > 30 || len(t.short) > 45 || len(t.long) > 200) throw new Error(`${k}: text je delší, než obchod dovolí`);
  if (/[—–]/.test(t.name + t.short + t.long)) throw new Error(`${k}: dlouhá pomlčka`);
}
const REVIEW_NOTE = [
  'Event Pass is a consumable in-app purchase. Each purchase is one credit that unlocks Tapkasa Pro (unlimited payments',
  'and pairing a second device) on this device for 72 hours from the moment the user starts it. Nothing renews automatically.',
  'Unused credits never expire; the app keeps them and shows the count in Menu > Tapkasa Pro.',
  'Where to find it: tap Menu > Tapkasa Pro > Unlock Pro, or record 10 payments in one day on the Sell tab; the offer',
  'appears at the daily free limit. "Start right after purchase" is on by default; otherwise the user starts the saved pass',
  'from Menu or from the pass badge in the header. The app needs no account and no login.',
].join(' ');

const money = (currencyCode, v) => { const u = Math.floor(v + 1e-9); return { currencyCode, units: String(u), nanos: Math.round((v - u) * 100) * 10000000 }; };
const num = (p) => Number(p.units || 0) + (p.nanos || 0) / 1e9;

// ======================== App Store Connect ========================
async function appStore() {
  const call = await asc();
  log(`\n=== App Store Connect (aplikace ${ASC_APP}) ===`);
  const all = async (p) => { const out = []; let next = p; while (next) { const r = await call('GET', next); out.push(...r.data); next = r.links?.next || null; } return out; };
  const territories = await all('/v1/territories?limit=200');
  const eur = territories.filter((t) => t.attributes.currency === 'EUR').map((t) => t.id);
  log(`území: ${territories.length}, s eurem ${eur.length} (${eur.join(' ')})`);
  const found = (await call('GET', `/v1/apps/${ASC_APP}/inAppPurchasesV2?filter[productId]=${PRODUCT}&limit=50`)).data[0];
  let id = found?.id;
  log(found ? `produkt ${PRODUCT} existuje (${found.attributes.inAppPurchaseType}, stav ${found.attributes.state})` : `produkt ${PRODUCT} zatím není: založí se jako CONSUMABLE`);
  if (found && found.attributes.inAppPurchaseType !== 'CONSUMABLE') throw new Error('existující produkt není CONSUMABLE, uprav ručně');
  if (!id) {
    log(`  název pro tebe: "Tapkasa Event Pass 72 h", poznámka pro kontrolu: ${len(REVIEW_NOTE)} znaků`);
    if (!GO) {
      for (const t of Object.values(TEXTS)) log(`  ${t.as.padEnd(5)} ${t.name} · ${t.short}`);
      log(`  ceny: CZE ${PRICE.CZK} Kč (základ), USA ${PRICE.USD} $, ${eur.length} zemí s eurem ${PRICE.EUR} €, ostatní přepočte Apple`);
      log(`  dostupnost: všech ${territories.length} území, i nová`);
      log(`  snímek pro kontrolu: ${SHOT} ${fs.existsSync(SHOT) ? '(je připravený)' : '(CHYBÍ)'}`);
      return;
    }
    id = (await call('POST', '/v2/inAppPurchases', { data: { type: 'inAppPurchases',
      attributes: { name: 'Tapkasa Event Pass 72 h', productId: PRODUCT, inAppPurchaseType: 'CONSUMABLE', reviewNote: REVIEW_NOTE },
      relationships: { app: { data: { type: 'apps', id: ASC_APP } } } } })).data.id;
    log(`  založeno: ${id}`);
  }
  // lokalizace
  const locs = (await call('GET', `/v2/inAppPurchases/${id}/inAppPurchaseLocalizations?limit=50`)).data;
  for (const t of Object.values(TEXTS)) {
    const l = locs.find((x) => x.attributes.locale === t.as);
    if (l && l.attributes.name === t.name && l.attributes.description === t.short) continue;
    log(`  lokalizace ${t.as}: ${l ? 'upravit' : 'přidat'} → ${t.name} · ${t.short}`);
    if (!GO) continue;
    if (l) await call('PATCH', `/v1/inAppPurchaseLocalizations/${l.id}`, { data: { type: 'inAppPurchaseLocalizations', id: l.id, attributes: { name: t.name, description: t.short } } });
    else await call('POST', '/v1/inAppPurchaseLocalizations', { data: { type: 'inAppPurchaseLocalizations', attributes: { locale: t.as, name: t.name, description: t.short },
      relationships: { inAppPurchaseV2: { data: { type: 'inAppPurchases', id } } } } });
  }
  // ceny: základ Česko, ručně USA a země s eurem; jen když produkt žádný ceník nemá
  let hasPrices = false;
  try { hasPrices = (await call('GET', `/v1/inAppPurchasePriceSchedules/${id}/manualPrices?limit=1`)).data.length > 0; } catch (e) { if (e.status !== 404) throw e; }
  if (hasPrices) log('  ceník už existuje, nechávám ho být');
  else {
    const want = [['CZE', PRICE.CZK], ['USA', PRICE.USD], ...eur.map((t) => [t, PRICE.EUR])];
    const points = [];
    for (const [terr, price] of want) {
      const pts = await all(`/v2/inAppPurchases/${id}/pricePoints?filter[territory]=${terr}&limit=200`);
      const p = pts.find((x) => Math.abs(Number(x.attributes.customerPrice) - price) < 0.001);
      if (!p) throw new Error(`v ${terr} není cenový bod ${price}`);
      points.push({ terr, price, id: p.id });
    }
    log(`  ceník: ${points.map((p) => `${p.terr} ${p.price}`).join(', ')}; ostatní země přepočte Apple z CZE`);
    if (GO) {
      const refs = points.map((p, i) => ({ type: 'inAppPurchasePrices', id: '${p' + i + '}' }));
      const included = points.map((p, i) => ({ type: 'inAppPurchasePrices', id: '${p' + i + '}', attributes: { startDate: null },
        relationships: { inAppPurchaseV2: { data: { type: 'inAppPurchases', id } }, inAppPurchasePricePoint: { data: { type: 'inAppPurchasePricePoints', id: p.id } } } }));
      await call('POST', '/v1/inAppPurchasePriceSchedules', { data: { type: 'inAppPurchasePriceSchedules',
        relationships: { inAppPurchase: { data: { type: 'inAppPurchases', id } }, baseTerritory: { data: { type: 'territories', id: 'CZE' } },
          manualPrices: { data: refs } } }, included });
      log('  ceník uložen');
    }
  }
  // dostupnost: všude, i v nových zemích
  let avail = null;
  try { avail = (await call('GET', `/v2/inAppPurchases/${id}/inAppPurchaseAvailability`)).data; } catch (e) { if (e.status !== 404) throw e; }
  if (avail) log('  dostupnost už je nastavená');
  else {
    log(`  dostupnost: všech ${territories.length} území`);
    if (GO) await call('POST', '/v1/inAppPurchaseAvailabilities', { data: { type: 'inAppPurchaseAvailabilities', attributes: { availableInNewTerritories: true },
      relationships: { inAppPurchase: { data: { type: 'inAppPurchases', id } }, availableTerritories: { data: territories.map((t) => ({ type: 'territories', id: t.id })) } } } });
  }
  // snímek pro kontrolu
  let shot = null;
  try { shot = (await call('GET', `/v2/inAppPurchases/${id}/appStoreReviewScreenshot`)).data; } catch (e) { if (e.status !== 404) throw e; }
  if (shot) log(`  snímek pro kontrolu už je (${shot.attributes.fileName})`);
  else if (!fs.existsSync(SHOT)) log(`  snímek pro kontrolu CHYBÍ: ${SHOT}`);
  else {
    log(`  snímek pro kontrolu: ${SHOT}`);
    if (GO) await uploadShot(call, id, SHOT);
  }
  if (SUBMIT) { await call('POST', '/v1/inAppPurchaseSubmissions', { data: { type: 'inAppPurchaseSubmissions', relationships: { inAppPurchaseV2: { data: { type: 'inAppPurchases', id } } } } }); log('  odesláno ke kontrole'); }
}

async function uploadShot(call, id, file) {
  const bytes = fs.readFileSync(file);
  const s = (await call('POST', '/v1/inAppPurchaseAppStoreReviewScreenshots', { data: { type: 'inAppPurchaseAppStoreReviewScreenshots',
    attributes: { fileName: path.basename(file), fileSize: bytes.length }, relationships: { inAppPurchaseV2: { data: { type: 'inAppPurchases', id } } } } })).data;
  for (const [i, op] of s.attributes.uploadOperations.entries()) {
    const tmp = path.join(process.env.TMPDIR || '/tmp', `tapkasa-pass-${process.pid}-${i}`);
    fs.writeFileSync(tmp, bytes.subarray(op.offset, op.offset + op.length));
    const a = ['-sS', '-g', '-X', op.method, op.url, '--data-binary', '@' + tmp, '-w', '%{http_code}', '-o', '/dev/null'];
    for (const h of op.requestHeaders || []) a.push('-H', `${h.name}: ${h.value}`);
    const code = execFileSync('curl', a).toString().trim(); fs.unlinkSync(tmp);
    if (!code.startsWith('2')) throw new Error('nahrání části ' + i + ' HTTP ' + code);
  }
  for (let i = 0; ; i++) {
    try {
      await call('PATCH', `/v1/inAppPurchaseAppStoreReviewScreenshots/${s.id}`, { data: { type: 'inAppPurchaseAppStoreReviewScreenshots', id: s.id,
        attributes: { uploaded: true, sourceFileChecksum: crypto.createHash('md5').update(bytes).digest('hex') } } });
      break;
    } catch (e) { if (e.status !== 409 || i >= 5) throw e; await new Promise((r) => setTimeout(r, 5000)); }
  }
  log('  snímek nahrán');
}

// ======================== Google Play ========================
async function googlePlay() {
  const api = await play();
  log(`\n=== Google Play (${PKG}) ===`);
  let found = null;
  try { found = api('GET', `/applications/${PKG}/oneTimeProducts/${PRODUCT}`); } catch (e) { if (e.status !== 404) throw e; }
  log(found ? `produkt ${PRODUCT} existuje (${(found.purchaseOptions || []).map((o) => `${o.purchaseOptionId}:${o.state}`).join(' ')})` : `produkt ${PRODUCT} zatím není: založí se`);
  // ceny: přepočet Googlu z dolaru, k tomu pevně Česko, USA a eurozóna
  const conv = api('POST', `/applications/${PKG}/pricing:convertRegionPrices`, { price: money('USD', PRICE.USD) }).convertedRegionPrices;
  const configs = Object.values(conv).map((c) => {
    const cur = c.price.currencyCode;
    const price = c.regionCode === 'CZ' ? money('CZK', PRICE.CZK) : cur === 'EUR' ? money('EUR', PRICE.EUR) : cur === 'USD' && c.regionCode === 'US' ? money('USD', PRICE.USD) : c.price;
    return { regionCode: c.regionCode, price, availability: 'AVAILABLE' };
  }).sort((a, b) => a.regionCode.localeCompare(b.regionCode));
  const show = ['CZ', 'SK', 'DE', 'AT', 'US', 'GB', 'PL', 'CH', 'HU', 'JP', 'BR'].map((r) => { const x = configs.find((c) => c.regionCode === r); return x ? `${r} ${num(x.price).toFixed(2)} ${x.price.currencyCode}` : `${r} -`; });
  log(`  ceny v ${configs.length} zemích, např. ${show.join(', ')}`);
  const listings = Object.values(TEXTS).map((t) => ({ languageCode: t.gp, title: t.name, description: t.long }));
  log(`  texty: ${listings.map((l) => l.languageCode).join(', ')}`);
  if (found) { log('  produkt už existuje: ceny ani texty skript nepřepisuje'); return; }
  if (!GO) return;
  const body = { packageName: PKG, productId: PRODUCT, listings,
    purchaseOptions: [{ purchaseOptionId: OPTION, buyOption: { legacyCompatible: true, multiQuantityEnabled: false },
      regionalPricingAndAvailabilityConfigs: configs,
      newRegionsConfig: { usdPrice: money('USD', PRICE.USD), eurPrice: money('EUR', PRICE.EUR), availability: 'AVAILABLE' } }] };
  const r = api('PATCH', `/applications/${PKG}/oneTimeProducts/${PRODUCT}?allowMissing=true&updateMask=listings,purchaseOptions&${RV}`, body);
  log(`  založeno: ${(r.purchaseOptions || []).map((o) => `${o.purchaseOptionId}:${o.state}`).join(' ')}`);
  const a = api('POST', `/applications/${PKG}/oneTimeProducts/${PRODUCT}/purchaseOptions:batchUpdateStates`,
    { requests: [{ activatePurchaseOptionRequest: { packageName: PKG, productId: PRODUCT, purchaseOptionId: OPTION } }] });
  log(`  aktivováno: ${JSON.stringify(a).slice(0, 200)}`);
}

log(GO ? 'REŽIM ZÁPISU (--go)' : 'NANEČISTO: nic se nezapíše (zápis přepínačem --go)');
if (ONLY !== 'play') await appStore();
if (ONLY !== 'asc') await googlePlay();
log('\nHotovo. V RevenueCat ještě: produkt tapkasa.pass.event72 v obou aplikacích s typem Consumable, bez entitlementu "pro".');
