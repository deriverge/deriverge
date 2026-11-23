// Stáhne živý stav stránky Tapkasy v obou obchodech do store/live/ (jen čtení).
//   node store/tool/pull-live.mjs [appstore|play]
// App Store: App Store Connect API, jen GET. Google Play: veřejná stránka obchodu (rozhraní pro vývojáře
// neumí listing přečíst bez založení editu, tedy bez zápisu), proto bez přihlášení a bez klíče.
import fs from 'node:fs';
import { asc, ASC_APP, PKG, len } from './clients.mjs';
import { playPage, PLAY_WEB } from './play-public.mjs';
const OUT = new URL('../live/', import.meta.url).pathname;
const what = process.argv[2] || 'all';
const save = (name, obj) => { fs.writeFileSync(OUT + name, JSON.stringify(obj, null, 1) + '\n'); console.log('uloženo', OUT + name); };

async function appstore() {
  const api = await asc();
  const all = async (path) => { let out = [], next = path; while (next) { const r = await api('GET', next); out = out.concat(r.data); next = r.links && r.links.next; } return out; };
  const app = (await api('GET', `/v1/apps/${ASC_APP}?fields[apps]=name,bundleId,sku,primaryLocale`)).data.attributes;
  const versions = (await all(`/v1/apps/${ASC_APP}/appStoreVersions?limit=20`)).map((v) => ({ id: v.id, ...v.attributes }));
  const infos = [];
  for (const i of await all(`/v1/apps/${ASC_APP}/appInfos`)) {
    const locs = await all(`/v1/appInfos/${i.id}/appInfoLocalizations?limit=50`);
    let cats = {};
    try {
      const r = await api('GET', `/v1/appInfos/${i.id}?include=primaryCategory,secondaryCategory`);
      cats = { primary: r.data.relationships.primaryCategory?.data?.id || null, secondary: r.data.relationships.secondaryCategory?.data?.id || null };
    } catch (e) { cats = { error: e.message.slice(0, 200) }; }
    infos.push({ id: i.id, state: i.attributes.state || i.attributes.appStoreState, categories: cats,
      localizations: Object.fromEntries(locs.map((l) => [l.attributes.locale, { id: l.id, name: l.attributes.name, subtitle: l.attributes.subtitle, privacyPolicyUrl: l.attributes.privacyPolicyUrl }]).sort()) });
  }
  // Texty a snímky: verze v prodeji a případná rozpracovaná.
  const pick = versions.filter((v, i) => i === versions.findIndex((x) => x.appStoreState === 'READY_FOR_SALE') || !['READY_FOR_SALE', 'REPLACED_WITH_NEW_VERSION'].includes(v.appStoreState));
  const detail = [];
  for (const v of pick) {
    const locs = await all(`/v1/appStoreVersions/${v.id}/appStoreVersionLocalizations?limit=50`);
    const L = {};
    for (const l of locs) {
      const a = l.attributes;
      const sets = await all(`/v1/appStoreVersionLocalizations/${l.id}/appScreenshotSets?limit=50`);
      const shots = {};
      for (const s of sets) {
        const list = await all(`/v1/appScreenshotSets/${s.id}/appScreenshots?limit=50`);
        shots[s.attributes.screenshotDisplayType] = list.map((x) => ({ fileName: x.attributes.fileName, width: x.attributes.imageAsset?.width, height: x.attributes.imageAsset?.height, state: x.attributes.assetDeliveryState?.state, checksum: x.attributes.sourceFileChecksum }));
      }
      const previews = (await all(`/v1/appStoreVersionLocalizations/${l.id}/appPreviewSets?limit=50`)).map((s) => s.attributes.previewType);
      L[a.locale] = { id: l.id, description: a.description, keywords: a.keywords, promotionalText: a.promotionalText, whatsNew: a.whatsNew, supportUrl: a.supportUrl, marketingUrl: a.marketingUrl,
        lengths: { description: len(a.description), keywords: len(a.keywords), promotionalText: len(a.promotionalText), whatsNew: len(a.whatsNew) }, screenshots: shots, previews };
    }
    let build = null;
    try { const b = await api('GET', `/v1/appStoreVersions/${v.id}/build`); build = b.data ? { id: b.data.id, version: b.data.attributes.version, state: b.data.attributes.processingState } : null; } catch {}
    detail.push({ id: v.id, versionString: v.versionString, state: v.appStoreState, build, localizations: Object.fromEntries(Object.entries(L).sort()) });
  }
  const opt = async (path, map) => { try { return (await all(path)).map(map); } catch (e) { return { error: e.message.slice(0, 200) }; } };
  const builds = await opt(`/v1/builds?filter[app]=${ASC_APP}&limit=10&sort=-uploadedDate&include=preReleaseVersion`, (b) => ({ id: b.id, build: b.attributes.version, uploaded: b.attributes.uploadedDate, state: b.attributes.processingState, expired: b.attributes.expired }));
  const preRel = await opt(`/v1/apps/${ASC_APP}/preReleaseVersions?limit=10`, (p) => ({ id: p.id, version: p.attributes.version }));
  const events = await opt(`/v1/apps/${ASC_APP}/appEvents?limit=20`, (e) => ({ id: e.id, referenceName: e.attributes.referenceName, badge: e.attributes.badge, state: e.attributes.eventState }));
  const cpp = await opt(`/v1/apps/${ASC_APP}/appCustomProductPages?limit=20`, (p) => ({ id: p.id, name: p.attributes.name, visible: p.attributes.visible, url: p.attributes.url }));
  save('appstore.json', { pulled: new Date().toISOString(), source: 'App Store Connect API (GET)', app, versions: versions.map((v) => ({ id: v.id, versionString: v.versionString, state: v.appStoreState, created: v.createdDate })), appInfos: infos, versionDetail: detail, builds, preReleaseVersions: preRel, inAppEvents: events, customProductPages: cpp });
}

function playStore() {
  const listings = {};
  for (const k of Object.keys(PLAY_WEB)) { listings[k] = playPage(k); console.log('play', k, listings[k].title || listings[k].error); }
  save('play.json', { pulled: new Date().toISOString(), source: 'veřejná stránka play.google.com (bez přihlášení); jazyk bez vlastního listingu ukazuje výchozí nebo nejbližší jazyk', package: PKG, listings });
}
if (what === 'all' || what === 'appstore') await appstore();
if (what === 'all' || what === 'play') playStore();
