// Vlastní produktové stránky Tapkasy (custom product pages) v App Store Connect: založení, propagační text, snímky,
// klíčová slova hledání a odeslání ke kontrole. Texty a slova: store/meta/cpp.mjs, snímky: store/shots/cpp-shots.mjs.
//
//   node store/tool/asc-cpp.mjs                      nanečisto: jen čte (GET) a vypíše stav a co by se změnilo
//   node store/tool/asc-cpp.mjs --go                 založí chybějící stránky, zapíše propagační text a snímky
//   … --keywords --go                                přiřadí klíčová slova (jen stránkám, jejichž minVersion je v prodeji)
//   … --submit --go                                  odešle stránky ke kontrole (jen když verze v prodeji nebo na cestě
//                                                    ke kontrole má vše, co stránka ukazuje, tj. je ≥ minVersion)
//   … --pages de-vereinsfest,cs-spolky               jen některé stránky
//   … --shots <složka>                               jiná kořenová složka snímků (výchozí T7, viz shots-common.mjs)
//
// Pravidla Applu, na která skript dbá:
//  - klíčová slova jde přiřadit jen z pole klíčových slov POSLEDNÍ SCHVÁLENÉ verze (seznam vrací /v1/apps/{id}/searchKeywords);
//  - během kontroly stránky nejde měnit snímky, propagační text ani klíčová slova;
//  - stránka se v hledání ukáže až po schválení, s klíčovými slovy a viditelná (visible).
// Nic jiného (texty verze, ceny, verze aplikace) skript nemění.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { asc, ASC_APP, len } from './clients.mjs';
import { CPP } from '../meta/cpp.mjs';
import { appstore } from '../meta/index.mjs';
import { SHOTS_DIR, AS_SETS, pngSize, listShots } from './shots-common.mjs';
import { PAGES } from '../shots/cpp-data.mjs';

const args = process.argv.slice(2);
const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
const GO = args.includes('--go'), KW = args.includes('--keywords'), SUBMIT = args.includes('--submit');
const only = (opt('--pages') || '').split(',').filter(Boolean);
const ROOT = path.join(opt('--shots') || SHOTS_DIR, 'cpp');
const SETS = { iphone69: AS_SETS.iphone69, ipad13: AS_SETS.ipad13 };
const EDITABLE = ['PREPARE_FOR_SUBMISSION', 'READY_FOR_REVIEW', 'REJECTED'];
const LOCKED = ['WAITING_FOR_REVIEW', 'IN_REVIEW'];
const api = await asc();
const call = async (method, p, body) => {
  if (method !== 'GET' && !GO) throw new Error('zápis bez --go: ' + method + ' ' + p);
  return api(method, p, body);
};
const log = (...a) => console.log(...a);
const cmpVer = (a, b) => { const x = a.split('.').map(Number), y = b.split('.').map(Number); for (let i = 0; i < 3; i++) if ((x[i] || 0) !== (y[i] || 0)) return (x[i] || 0) - (y[i] || 0); return 0; };
const md5 = (f) => crypto.createHash('md5').update(fs.readFileSync(f)).digest('hex');
let changes = 0;

// --- kontrola obsahu (bez sítě) ---
const meta = appstore({});
for (const p of CPP) {
  if (len(p.promotionalText) > 170) throw new Error(`${p.key}: propagační text má ${len(p.promotionalText)} znaků (max 170)`);
  if (/[—–]/.test(p.promotionalText)) throw new Error(`${p.key}: dlouhá pomlčka v propagačním textu`);
  const field = meta[p.locale].keywords.split(',');
  const miss = p.keywords.filter((k) => !field.includes(k));
  if (miss.length) throw new Error(`${p.key}: slova ${miss.join(', ')} nejsou v poli klíčových slov ${p.locale} (store/meta)`);
  if (!PAGES[p.key] || PAGES[p.key].as !== p.locale) throw new Error(`${p.key}: chybí snímky v store/shots/cpp-data.mjs nebo nesedí locale`);
}
const allKw = CPP.flatMap((p) => p.keywords.map((k) => p.locale + ':' + k));
if (new Set(allKw).size !== allKw.length) throw new Error('stejné klíčové slovo u dvou stránek stejného locale');

// --- verze aplikace: co je v prodeji a co je na cestě ke kontrole ---
const versions = (await call('GET', `/v1/apps/${ASC_APP}/appStoreVersions?filter[platform]=IOS&limit=20`)).data;
const sorted = (st) => versions.filter((v) => st.includes(v.attributes.appStoreState)).map((v) => v.attributes.versionString).sort(cmpVer);
const liveVer = sorted(['READY_FOR_SALE']).pop() || '0';
const flightVer = sorted(['WAITING_FOR_REVIEW', 'IN_REVIEW', 'PENDING_DEVELOPER_RELEASE', 'PENDING_APPLE_RELEASE', 'PROCESSING_FOR_APP_STORE', 'ACCEPTED']).pop();
log(`Tapkasa → vlastní produktové stránky | ${GO ? 'ZÁPIS (--go)' : 'nanečisto (jen čtení)'}${KW ? ' | klíčová slova' : ''}${SUBMIT ? ' | odeslání ke kontrole' : ''}`);
log(`Verze v prodeji: ${liveVer}${flightVer ? ` | na cestě: ${flightVer}` : ''}`);

const pages = (await call('GET', `/v1/apps/${ASC_APP}/appCustomProductPages?limit=50`)).data;
const kwCache = {};
async function assignable(locale) {
  if (!kwCache[locale]) kwCache[locale] = (await call('GET', `/v1/apps/${ASC_APP}/searchKeywords?filter[platform]=IOS&filter[locale]=${encodeURIComponent(locale)}&limit=200`)).data.map((d) => d.id);
  return kwCache[locale];
}

async function uploadShot(setId, file) {
  const bytes = fs.readFileSync(file);
  const shot = (await call('POST', '/v1/appScreenshots', { data: { type: 'appScreenshots', attributes: { fileName: 'tapkasa-cpp-' + path.basename(file), fileSize: bytes.length },
    relationships: { appScreenshotSet: { data: { type: 'appScreenshotSets', id: setId } } } } })).data;
  for (const [i, op] of shot.attributes.uploadOperations.entries()) {
    const tmp = path.join(process.env.TMPDIR || '/tmp', `tapkasa-cpp-${process.pid}-${i}`);
    fs.writeFileSync(tmp, bytes.subarray(op.offset, op.offset + op.length));
    const a = ['-sS', '-g', '-X', op.method, op.url, '--data-binary', '@' + tmp, '-w', '%{http_code}', '-o', '/dev/null'];
    for (const h of op.requestHeaders || []) a.push('-H', `${h.name}: ${h.value}`);
    const code = execFileSync('curl', a).toString().trim(); fs.unlinkSync(tmp);
    if (!code.startsWith('2')) throw new Error('nahrání části ' + i + ' HTTP ' + code);
  }
  // Apple občas hlásí nedokončené nahrání, i když části doběhly; po chvíli projde.
  for (let i = 0; ; i++) {
    try {
      await call('PATCH', `/v1/appScreenshots/${shot.id}`, { data: { type: 'appScreenshots', id: shot.id, attributes: { uploaded: true, sourceFileChecksum: crypto.createHash('md5').update(bytes).digest('hex') } } });
      break;
    } catch (e) { if (e.status !== 409 || i >= 5) throw e; await new Promise((r) => setTimeout(r, 5000)); }
  }
}

// Lokalizace stránky: hlavní (texty, snímky a klíčová slova stránky) a u ne-českých stránek povinná česká záloha.
const CS_PRIMARY = 'cs';
function localesOf(p) {
  const shotsOf = (dir) => Object.fromEntries(Object.keys(SETS).map((folder) => [folder, path.join(dir, folder)]));
  const out = [{ locale: p.locale, promo: p.promotionalText, dirs: shotsOf(path.join(ROOT, p.key, p.locale)), keywords: p.keywords }];
  if (p.locale !== CS_PRIMARY) {
    if (p.cs === 'default') out.push({ locale: CS_PRIMARY, promo: meta.cs.promotionalText, dirs: shotsOf(path.join(opt('--shots') || SHOTS_DIR, 'appstore', 'cs')), keywords: [], fallback: 'výchozí česká stránka' });
    else {
      const src = CPP.find((x) => x.key === p.cs && x.locale === CS_PRIMARY);
      if (!src) throw new Error(`${p.key}: neznámá česká záloha ${p.cs}`);
      out.push({ locale: CS_PRIMARY, promo: src.promotionalText, dirs: shotsOf(path.join(ROOT, src.key, CS_PRIMARY)), keywords: [], fallback: 'česká stránka ' + src.key });
    }
  }
  for (const L of out) {
    L.files = {};
    for (const [folder, spec] of Object.entries(SETS)) {
      const f = listShots(L.dirs[folder]);
      if (f.length < 3 || f.length > 10) throw new Error(`${p.key} ${L.locale} ${folder}: ${f.length} snímků v ${L.dirs[folder]} (Apple 1 až 10, my 3 až 5; node store/shots/cpp-shots.mjs)`);
      for (const x of f) { const s = pngSize(x); if (s.w !== spec.w || s.h !== spec.h) throw new Error(`${x}: ${s.w}×${s.h}, čeká se ${spec.w}×${spec.h}`); }
      L.files[folder] = f;
    }
  }
  return out;
}

const toSubmit = [];
for (const p of CPP) {
  if (only.length && !only.includes(p.key)) continue;
  log(`\n== ${p.key} (${p.locale}) „${p.name}“, platí od verze ${p.minVersion}`);
  const LOCS = localesOf(p);
  // stránka a její nejnovější verze
  let page = pages.find((x) => x.attributes.name === p.name), ver = null, locs = [];
  if (!page) {
    changes++;
    log(`  založit stránku, verzi a lokalizace ${LOCS.map((L) => L.locale).join(' + ')}`);
    if (GO) {
      const r = await call('POST', '/v1/appCustomProductPages', {
        data: { type: 'appCustomProductPages', attributes: { name: p.name },
          relationships: { app: { data: { type: 'apps', id: ASC_APP } }, appCustomProductPageVersions: { data: [{ type: 'appCustomProductPageVersions', id: '${v1}' }] } } },
        included: [
          { type: 'appCustomProductPageVersions', id: '${v1}', relationships: { appCustomProductPageLocalizations: { data: LOCS.map((L, i) => ({ type: 'appCustomProductPageLocalizations', id: '${l' + i + '}' })) } } },
          ...LOCS.map((L, i) => ({ type: 'appCustomProductPageLocalizations', id: '${l' + i + '}', attributes: { locale: L.locale, promotionalText: L.promo } })),
        ] });
      page = r.data;
      log(`  ZALOŽENO: stránka ${page.id}, ${page.attributes.url}`);
    }
  }
  if (page) {
    const vers = (await call('GET', `/v1/appCustomProductPages/${page.id}/appCustomProductPageVersions?limit=20`)).data;
    ver = vers.sort((a, b) => Number(b.attributes.version) - Number(a.attributes.version))[0];
    locs = (await call('GET', `/v1/appCustomProductPageVersions/${ver.id}/appCustomProductPageLocalizations?limit=50`)).data;
    log(`  stránka ${page.id} | verze ${ver.attributes.version} ${ver.attributes.state} | ${page.attributes.visible ? 'viditelná' : 'SKRYTÁ'} | ${page.attributes.url}`);
    const extra = locs.filter((l) => !LOCS.some((L) => L.locale === l.attributes.locale)).map((l) => l.attributes.locale);
    if (extra.length) log(`  další lokalizace na stránce: ${extra.join(', ')} (skript je nechává být)`);
  }
  const state = ver?.attributes.state || 'PREPARE_FOR_SUBMISSION';
  const editable = !ver || EDITABLE.includes(state);
  const liveOk = cmpVer(liveVer, p.minVersion) >= 0;
  for (const L of LOCS) {
    const tag = `  [${L.locale}${L.fallback ? ', záloha: ' + L.fallback : ''}]`;
    let loc = locs.find((l) => l.attributes.locale === L.locale);
    if (page && !loc) {
      changes++;
      log(`${tag} přidat lokalizaci`);
      if (GO && editable) loc = (await call('POST', '/v1/appCustomProductPageLocalizations', { data: { type: 'appCustomProductPageLocalizations', attributes: { locale: L.locale, promotionalText: L.promo },
        relationships: { appCustomProductPageVersion: { data: { type: 'appCustomProductPageVersions', id: ver.id } } } } })).data;
    }
    // propagační text (Apple ho dovolí měnit kdykoli, jen ne během kontroly)
    if (loc && (loc.attributes.promotionalText || '') !== L.promo) {
      changes++;
      log(`${tag} propagační text:\n      teď:  ${loc.attributes.promotionalText || '(prázdné)'}\n      nově: ${L.promo}`);
      if (GO && !LOCKED.includes(state)) await call('PATCH', `/v1/appCustomProductPageLocalizations/${loc.id}`, { data: { type: 'appCustomProductPageLocalizations', id: loc.id, attributes: { promotionalText: L.promo } } });
    } else if (!loc) log(`${tag} propagační text (${len(L.promo)}/170): ${L.promo}`);
    // snímky
    const sets = loc ? (await call('GET', `/v1/appCustomProductPageLocalizations/${loc.id}/appScreenshotSets?limit=20`)).data : [];
    for (const [folder, spec] of Object.entries(SETS)) {
      let set = sets.find((s) => s.attributes.screenshotDisplayType === spec.type);
      const old = set ? (await call('GET', `/v1/appScreenshotSets/${set.id}/appScreenshots?limit=50`)).data : [];
      const files = L.files[folder], sums = files.map(md5);
      if (old.length === sums.length && old.every((o, i) => o.attributes.sourceFileChecksum === sums[i])) { log(`${tag} snímky ${spec.type}: beze změny (${sums.length})`); continue; }
      changes++;
      log(`${tag} snímky ${spec.type}: teď ${old.length}, nově ${files.length} z ${L.dirs[folder]}`);
      if (!GO || !loc) continue;
      if (!editable) { log(`${tag} STOP snímky: verze stránky je ${state}, měnit jde jen v ${EDITABLE.join('/')}`); continue; }
      if (!set) set = (await call('POST', '/v1/appScreenshotSets', { data: { type: 'appScreenshotSets', attributes: { screenshotDisplayType: spec.type },
        relationships: { appCustomProductPageLocalization: { data: { type: 'appCustomProductPageLocalizations', id: loc.id } } } } })).data;
      for (const o of old) await call('DELETE', `/v1/appScreenshots/${o.id}`);
      for (const f of files) await uploadShot(set.id, f);
      log(`${tag} nahráno ${files.length} snímků ${spec.type}`);
    }
    // klíčová slova: viditelnost v hledání, proto až když je minVersion v prodeji; záloha žádná nemá
    const has = loc ? (await call('GET', `/v1/appCustomProductPageLocalizations/${loc.id}/relationships/searchKeywords?limit=50`)).data.map((d) => d.id) : [];
    const can = L.keywords.length ? await assignable(L.locale) : [];
    const ok = L.keywords.filter((k) => can.includes(k)), later = L.keywords.filter((k) => !can.includes(k));
    if (L.keywords.length || has.length) {
      log(`${tag} klíčová slova: přiřazená [${has.join(', ')}] | chci [${L.keywords.join(', ')}] | teď přiřaditelná ${ok.length ? '[' + ok.join(', ') + ']' : 'žádná'}${later.length ? ` | až po schválení verze s nimi: [${later.join(', ')}]` : ''}`);
      if (!liveOk) log(`${tag} klíčová slova čekají: v prodeji je ${liveVer}, stránka ukazuje funkce od ${p.minVersion}`);
    }
    const add = ok.filter((k) => !has.includes(k)), del = has.filter((k) => !L.keywords.includes(k));
    if (KW && liveOk && (add.length || del.length)) {
      changes++;
      log(`${tag} klíčová slova: přidat [${add.join(', ')}], odebrat [${del.join(', ')}]`);
      if (GO && loc) {
        if (LOCKED.includes(state)) log(`${tag} STOP klíčová slova: stránka je v kontrole, měnit je nejde`);
        else {
          if (add.length) await call('POST', `/v1/appCustomProductPageLocalizations/${loc.id}/relationships/searchKeywords`, { data: add.map((id) => ({ type: 'appKeywords', id })) });
          if (del.length) await call('DELETE', `/v1/appCustomProductPageLocalizations/${loc.id}/relationships/searchKeywords`, { data: del.map((id) => ({ type: 'appKeywords', id })) });
          log(`${tag} klíčová slova zapsána`);
        }
      }
    }
  }
  // ke kontrole: verze, se kterou se stránka posuzuje, musí umět vše, co stránka ukazuje
  if (SUBMIT) {
    const reviewVer = [liveVer, flightVer].filter(Boolean).sort(cmpVer).pop();
    if (!['PREPARE_FOR_SUBMISSION', 'REJECTED', 'READY_FOR_REVIEW'].includes(state)) log(`  ke kontrole: ne (stav ${state})`);
    else if (cmpVer(reviewVer, p.minVersion) < 0) log(`  ke kontrole: ČEKÁ, nejnovější verze ${reviewVer} je starší než ${p.minVersion}`);
    else toSubmit.push({ p, ver });
  }
}

if (SUBMIT && toSubmit.length) {
  changes++;
  log(`\nOdeslat ke kontrole: ${toSubmit.map((x) => x.p.key).join(', ')}`);
  if (GO && toSubmit.some((x) => !x.ver)) throw new Error('stránka bez verze, nejdřív spustit bez --submit');
  if (GO) {
    const drafts = (await call('GET', `/v1/reviewSubmissions?filter[app]=${ASC_APP}&filter[platform]=IOS&filter[state]=READY_FOR_REVIEW&limit=10`)).data;
    // koncept bez verze aplikace použít, jinak založit nový (verzi aplikace do něj skript nikdy nepřidává)
    let sub = null;
    for (const d of drafts) {
      const items = (await call('GET', `/v1/reviewSubmissions/${d.id}/items?limit=50&include=appStoreVersion`)).data;
      if (!items.some((it) => it.relationships?.appStoreVersion?.data)) { sub = d; break; }
    }
    if (!sub) sub = (await call('POST', '/v1/reviewSubmissions', { data: { type: 'reviewSubmissions', attributes: { platform: 'IOS' }, relationships: { app: { data: { type: 'apps', id: ASC_APP } } } } })).data;
    log(`  podání ${sub.id}`);
    const inSub = (await call('GET', `/v1/reviewSubmissions/${sub.id}/items?limit=50&include=appCustomProductPageVersion`)).data
      .map((it) => it.relationships?.appCustomProductPageVersion?.data?.id).filter(Boolean);
    for (const { p, ver } of toSubmit) {
      if (inSub.includes(ver.id)) { log(`  ${p.key}: už v podání`); continue; }
      await call('POST', '/v1/reviewSubmissionItems', { data: { type: 'reviewSubmissionItems', relationships: {
        reviewSubmission: { data: { type: 'reviewSubmissions', id: sub.id } }, appCustomProductPageVersion: { data: { type: 'appCustomProductPageVersions', id: ver.id } } } } });
      log(`  ${p.key}: přidáno (verze stránky ${ver.id})`);
    }
    const r = await call('PATCH', `/v1/reviewSubmissions/${sub.id}`, { data: { type: 'reviewSubmissions', id: sub.id, attributes: { submitted: true } } });
    log(`  ODESLÁNO ke kontrole: podání ${sub.id}, stav ${r.data.attributes.state}`);
  }
}
log(GO ? `\nHotovo, změn: ${changes}.` : `\nNanečisto: ${changes} změn. Zápis: přidat --go (klíčová slova --keywords, odeslání --submit).`);
