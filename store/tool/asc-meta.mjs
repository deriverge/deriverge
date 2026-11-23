// Texty a snímky Tapkasy do App Store Connect pro verzi, kterou lze upravovat (PREPARE_FOR_SUBMISSION a podobné).
//
//   node store/tool/asc-meta.mjs                         nanečisto: jen čte (GET) a vypíše, co by se změnilo
//   node store/tool/asc-meta.mjs --go                    zapíše texty i snímky
//   … --create 1.0.9        když upravitelná verze není, založí ji (jen s --go)
//   … --whats-new 1.0.8     text „Co je nového“ pro 1.0.8 (výchozí 1.0.9). Když existuje store/vydani/whats_new_<verze>.json
//                           (konkrétní body od vydání), bere se z něj; texty ze store/meta jsou jen obecná záloha.
//   … --keep-whats-new      „Co je nového“ vůbec neměnit
//   … --season xmas|year    propagační text vánoční, nebo celoroční (výchozí podle data: 15. 11. až 26. 12. vánoční)
//   … --locales de,cs       jen některá locale (de bere de-DE, en obě anglická)
//   … --no-shots            jen texty      … --shots <složka>   jiná složka se snímky
//   … --promo-only          jen propagační text u verze v prodeji (jde bez kontroly Applu), např. návrat po Vánocích:
//                           node store/tool/asc-meta.mjs --promo-only --season year --go
//
// Zápis jen po výslovném souhlasu majitele s konkrétní verzí. Skript nic neodesílá ke kontrole.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { asc, ASC_APP, len } from './clients.mjs';
import { appstore, seasonNow, URLS } from '../meta/index.mjs';
import { SHOTS_DIR, AS_SETS, pngSize, listShots } from './shots-common.mjs';

const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null; };
const GO = args.includes('--go'), PROMO_ONLY = args.includes('--promo-only'), NO_SHOTS = args.includes('--no-shots') || PROMO_ONLY;
const season = opt('--season') || seasonNow(), wnVersion = opt('--whats-new') || '1.0.9', create = opt('--create');
const shotsRoot = path.join(opt('--shots') || SHOTS_DIR, 'appstore');
const want = (opt('--locales') || '').split(',').filter(Boolean);
const wanted = (loc) => !want.length || want.some((w) => loc === w || loc.startsWith(w + '-'));
if (!['xmas', 'year'].includes(season)) throw new Error('--season xmas|year');
const T = appstore({ season, version: wnVersion });
const KEEP_WN = args.includes('--keep-whats-new');
// „Co je nového“ s konkrétními body píše vydání (store/vydani/whats_new_<verze>.json, klíč = jazyk); má přednost před obecným textem.
const wnFile = new URL(`../vydani/whats_new_${wnVersion}.json`, import.meta.url);
const wnNotes = fs.existsSync(wnFile) ? JSON.parse(fs.readFileSync(wnFile, 'utf8')) : null;
for (const [loc, t] of Object.entries(T)) {
  if (wnNotes) t.whatsNew = wnNotes[loc.slice(0, 2)] || wnNotes.en;
  if (len(t.whatsNew) > 4000) throw new Error(`${loc}: Co je nového má ${len(t.whatsNew)} znaků`);
}
const EDITABLE = ['PREPARE_FOR_SUBMISSION', 'DEVELOPER_REJECTED', 'REJECTED', 'METADATA_REJECTED', 'INVALID_BINARY'];
const api = await asc();
// Pojistka: bez --go projde jen GET.
const call = async (method, p, body) => {
  if (method !== 'GET' && !GO) throw new Error('zápis bez --go: ' + method + ' ' + p);
  return api(method, p, body);
};
const cmpVer = (a, b) => { const x = a.split('.').map(Number), y = b.split('.').map(Number); for (let i = 0; i < 3; i++) if ((x[i] || 0) !== (y[i] || 0)) return (x[i] || 0) - (y[i] || 0); return 0; };
const log = (...a) => console.log(...a);
const show = (s) => String(s ?? '').replace(/\n/g, ' ⏎ ');
let changes = 0;
function diff(loc, field, was, now, max) {
  if ((was ?? '') === now) return false;
  changes++;
  const l = max ? ` (${len(now)}/${max})` : ` (${len(now)} znaků)`;
  if (len(now) > 200) log(`  ${loc} ${field}${l}: změna (${len(was)} → ${len(now)} znaků), začátek: ${show(now).slice(0, 110)}…`);
  else log(`  ${loc} ${field}${l}:\n      teď:  ${show(was) || '(prázdné)'}\n      nově: ${show(now)}`);
  return true;
}

log(`Tapkasa → App Store Connect | ${GO ? 'ZÁPIS (--go)' : 'nanečisto (jen čtení)'} | sezóna ${season} | Co je nového ${KEEP_WN ? 'beze změny' : wnVersion + (wnNotes ? ' ze store/vydani' : ' obecné ze store/meta')}${PROMO_ONLY ? ' | jen propagační text' : ''}`);
const versions = (await call('GET', `/v1/apps/${ASC_APP}/appStoreVersions?limit=20`)).data;
const live = versions.find((v) => v.attributes.appStoreState === 'READY_FOR_SALE');
let ver = versions.find((v) => EDITABLE.includes(v.attributes.appStoreState));
// Verze, která je na cestě do obchodu (čeká na kontrolu, je v kontrole, čeká na vydání): texty u ní měnit nejde a novou verzi vedle ní založit taky ne.
const INFLIGHT = ['WAITING_FOR_REVIEW', 'IN_REVIEW', 'READY_FOR_REVIEW', 'PENDING_DEVELOPER_RELEASE', 'PENDING_APPLE_RELEASE', 'PROCESSING_FOR_APP_STORE', 'ACCEPTED'];
const pending = versions.find((v) => INFLIGHT.includes(v.attributes.appStoreState));
log('Verze v prodeji:', live ? live.attributes.versionString : 'žádná', '| upravitelná:', ver ? `${ver.attributes.versionString} (${ver.attributes.appStoreState})` : 'žádná',
  pending ? `| na cestě: ${pending.attributes.versionString} (${pending.attributes.appStoreState})` : '');

if (PROMO_ONLY) {
  // Propagační text slibuje vratné zálohy, ty jsou až od 1.0.8. Zapisuje se proto jen k verzím 1.0.8 a novějším:
  // k verzi v prodeji (projeví se hned) a k verzi na cestě nebo rozpracované (projeví se s jejím vydáním).
  const targets = [live, pending, ver].filter((v) => v && cmpVer(v.attributes.versionString, '1.0.8') >= 0);
  if (!targets.length) {
    log(`STOP: v prodeji je ${live ? live.attributes.versionString : 'nic'} a žádná verze 1.0.8 nebo novější není založená. Propagační text slibuje vratné zálohy (od 1.0.8).`);
    process.exit(GO ? 1 : 0);
  }
  if (live && !targets.includes(live)) log(`Verze v prodeji ${live.attributes.versionString} zůstane beze změny (zálohy ještě neumí).`);
  for (const v of targets) {
    log(`\nVerze ${v.attributes.versionString} (${v.attributes.appStoreState})`);
    const locs = (await call('GET', `/v1/appStoreVersions/${v.id}/appStoreVersionLocalizations?limit=50`)).data;
    for (const l of locs) {
      const t = T[l.attributes.locale]; if (!t || !wanted(l.attributes.locale)) continue;
      if (diff(l.attributes.locale, 'propagační text', l.attributes.promotionalText, t.promotionalText, 170) && GO)
        await call('PATCH', `/v1/appStoreVersionLocalizations/${l.id}`, { data: { type: 'appStoreVersionLocalizations', id: l.id, attributes: { promotionalText: t.promotionalText } } });
    }
  }
  log(GO ? `\nHotovo, změn: ${changes}.` : `\nNanečisto: ${changes} změn. Zápis: přidat --go.`);
  process.exit(0);
}

if (!ver && pending && !PROMO_ONLY) {
  log(`Verze ${pending.attributes.versionString} je ve stavu ${pending.attributes.appStoreState}: její texty teď měnit nejde a další verzi lze založit až po jejím vydání.`);
  if (GO) { log('STOP: počkat, až bude v prodeji, pak spustit znovu s --create <další verze>.'); process.exit(1); }
  log('Nanečisto porovnávám s texty této verze.');
} else if (!ver) {
  if (!create) log('Upravitelná verze není. Porovnávám s verzí v prodeji; pro zápis přidat --create <verze> (např. --create 1.0.9).');
  else if (GO) {
    ver = (await call('POST', '/v1/appStoreVersions', { data: { type: 'appStoreVersions', attributes: { platform: 'IOS', versionString: create },
      relationships: { app: { data: { type: 'apps', id: ASC_APP } } } } })).data;
    log('Založena verze', create, ver.id);
  } else log(`Nanečisto: založila by se verze ${create}; porovnávám s verzí v prodeji.`);
}
if (GO && !ver) { log('STOP: není co upravovat.'); process.exit(1); }
const target = ver || pending || live;
const targetVersion = ver ? ver.attributes.versionString : create || '(nová)';
if (ver && cmpVer(ver.attributes.versionString, '1.0.8') < 0) throw new Error('texty slibují vratné zálohy, verze musí být 1.0.8 nebo novější');
if (ver && ver.attributes.versionString !== wnVersion) log(`POZOR: upravitelná verze je ${ver.attributes.versionString}, ale „Co je nového“ se bere pro ${wnVersion} (přepínač --whats-new).`);

const infos = (await call('GET', `/v1/apps/${ASC_APP}/appInfos`)).data;
const info = infos.find((x) => EDITABLE.includes(x.attributes.appStoreState || x.attributes.state)) || infos[0];
const infoEditable = EDITABLE.includes(info.attributes.appStoreState || info.attributes.state);
const infoLocs = (await call('GET', `/v1/appInfos/${info.id}/appInfoLocalizations?limit=50`)).data;
let verLocs = (await call('GET', `/v1/appStoreVersions/${target.id}/appStoreVersionLocalizations?limit=50`)).data;
if (GO && !infoEditable) log('POZOR: název a podtitul lze měnit jen u rozpracované verze; appInfo je ve stavu', info.attributes.appStoreState || info.attributes.state);

async function uploadShot(setId, file) {
  const bytes = fs.readFileSync(file);
  const shot = (await call('POST', '/v1/appScreenshots', { data: { type: 'appScreenshots', attributes: { fileName: 'tapkasa-' + path.basename(file), fileSize: bytes.length },
    relationships: { appScreenshotSet: { data: { type: 'appScreenshotSets', id: setId } } } } })).data;
  for (const [i, op] of shot.attributes.uploadOperations.entries()) {
    const tmp = path.join(process.env.TMPDIR || '/tmp', `tapkasa-shot-${process.pid}-${i}`);
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

for (const [locale, t] of Object.entries(T)) {
  if (!wanted(locale)) continue;
  log(`\n== ${locale}${infoLocs.some((l) => l.attributes.locale === locale) ? '' : '  (NOVÁ lokalizace)'}`);
  // název a podtitul
  const il = infoLocs.find((l) => l.attributes.locale === locale);
  const infoAttrs = { name: t.name, subtitle: t.subtitle, privacyPolicyUrl: URLS.privacy };
  const a = diff(locale, 'název', il?.attributes.name, t.name, 30), b = diff(locale, 'podtitul', il?.attributes.subtitle, t.subtitle, 30);
  const c = il && (il.attributes.privacyPolicyUrl || '') !== URLS.privacy ? diff(locale, 'zásady soukromí', il.attributes.privacyPolicyUrl, URLS.privacy) : false;
  if (GO && (a || b || c || !il)) {
    if (il) await call('PATCH', `/v1/appInfoLocalizations/${il.id}`, { data: { type: 'appInfoLocalizations', id: il.id, attributes: infoAttrs } });
    else await call('POST', '/v1/appInfoLocalizations', { data: { type: 'appInfoLocalizations', attributes: { locale, ...infoAttrs }, relationships: { appInfo: { data: { type: 'appInfos', id: info.id } } } } });
  }
  // texty verze
  let vl = verLocs.find((l) => l.attributes.locale === locale);
  if (GO && !vl) { // založení lokalizace appInfo zakládá i lokalizaci verze
    verLocs = (await call('GET', `/v1/appStoreVersions/${target.id}/appStoreVersionLocalizations?limit=50`)).data;
    vl = verLocs.find((l) => l.attributes.locale === locale);
  }
  const va = vl?.attributes || {};
  const verAttrs = { description: t.description, keywords: t.keywords, promotionalText: t.promotionalText, whatsNew: t.whatsNew, supportUrl: URLS.support, marketingUrl: URLS.marketing };
  if (KEEP_WN) delete verAttrs.whatsNew;
  const lim = { description: 4000, keywords: 100, promotionalText: 170, whatsNew: 4000 };
  const names = { description: 'popis', keywords: 'klíčová slova', promotionalText: 'propagační text', whatsNew: 'co je nového', supportUrl: 'podpora', marketingUrl: 'web' };
  let dirty = false;
  for (const k of Object.keys(verAttrs)) dirty = diff(locale, names[k], va[k], verAttrs[k], lim[k]) || dirty;
  if (GO && (dirty || !vl)) {
    if (vl) await call('PATCH', `/v1/appStoreVersionLocalizations/${vl.id}`, { data: { type: 'appStoreVersionLocalizations', id: vl.id, attributes: verAttrs } });
    else vl = (await call('POST', '/v1/appStoreVersionLocalizations', { data: { type: 'appStoreVersionLocalizations', attributes: { locale, ...verAttrs }, relationships: { appStoreVersion: { data: { type: 'appStoreVersions', id: target.id } } } } })).data;
  }
  // snímky
  if (NO_SHOTS) continue;
  const sets = vl ? (await call('GET', `/v1/appStoreVersionLocalizations/${vl.id}/appScreenshotSets?limit=50`)).data : [];
  for (const [folder, spec] of Object.entries(AS_SETS)) {
    const files = listShots(path.join(shotsRoot, locale, folder));
    if (!files.length) { log(`  ${locale} snímky ${folder}: žádné soubory, sada ${spec.type} zůstane, jak je`); continue; }
    if (files.length > 10) throw new Error(`${locale} ${folder}: víc než 10 snímků`);
    for (const f of files) { const s = pngSize(f); if (s.w !== spec.w || s.h !== spec.h) throw new Error(`${f}: ${s.w}×${s.h}, čeká se ${spec.w}×${spec.h}`); }
    let set = sets.find((s) => s.attributes.screenshotDisplayType === spec.type);
    const old = set ? (await call('GET', `/v1/appScreenshotSets/${set.id}/appScreenshots?limit=50`)).data : [];
    const sums = files.map((f) => crypto.createHash('md5').update(fs.readFileSync(f)).digest('hex'));
    const same = old.length === files.length && old.every((o, i) => o.attributes.sourceFileChecksum === sums[i]);
    if (same) { log(`  ${locale} snímky ${spec.type}: beze změny (${files.length})`); continue; }
    changes++;
    log(`  ${locale} snímky ${spec.type} (${spec.w}×${spec.h}): teď ${old.length} [${old.map((o) => o.attributes.fileName).join(', ')}]\n      nově ${files.length}: ${files.map((f) => path.basename(f)).join(', ')}`);
    if (!GO) continue;
    if (!set) set = (await call('POST', '/v1/appScreenshotSets', { data: { type: 'appScreenshotSets', attributes: { screenshotDisplayType: spec.type }, relationships: { appStoreVersionLocalization: { data: { type: 'appStoreVersionLocalizations', id: vl.id } } } } })).data;
    for (const o of old) await call('DELETE', `/v1/appScreenshots/${o.id}`);
    for (const f of files) await uploadShot(set.id, f);
  }
}
log(GO ? `\nHotovo: verze ${targetVersion}, změn ${changes}. Ke kontrole se nic neodeslalo.` : `\nNanečisto: ${changes} změn proti ${ver ? 'rozpracované verzi ' + targetVersion : pending ? 'verzi na cestě ' + pending.attributes.versionString : 'verzi v prodeji ' + (live ? live.attributes.versionString : '')}. Nic se nezapsalo. Zápis: přidat --go${ver ? '' : ' --create <verze>'}.`);
