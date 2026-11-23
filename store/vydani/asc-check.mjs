// Kontrola verze před odesláním: texty, snímky a rozpracovaná odeslání. node store/vydani/asc-check.mjs <verze>
import { asc, ASC_APP } from '../tool/clients.mjs';
const api = await asc();
const version = process.argv[2];
const v = (await api('GET', `/v1/apps/${ASC_APP}/appStoreVersions?limit=5&filter[platform]=IOS`)).data.find((x) => x.attributes.versionString === version);
if (!v) throw new Error('Verze neexistuje.');
console.log(version, v.attributes.appStoreState, v.attributes.releaseType);
const locs = (await api('GET', `/v1/appStoreVersions/${v.id}/appStoreVersionLocalizations?limit=50`)).data;
for (const l of locs) {
  const a = l.attributes;
  const sets = (await api('GET', `/v1/appStoreVersionLocalizations/${l.id}/appScreenshotSets?include=appScreenshots&limit=20`));
  const counts = sets.data.map((s) => s.attributes.screenshotDisplayType.replace('APP_', '') + ':' + (s.relationships.appScreenshots.data || []).length).join(' ');
  console.log(a.locale, '| popis', (a.description || '').length, '| klíč. slova', (a.keywords || '').length, '| promo', (a.promotionalText || '').length, '| novinky', (a.whatsNew || '').length, '| podpora', a.supportUrl ? 'ano' : 'NE', '|', counts);
}
const rs = (await api('GET', `/v1/apps/${ASC_APP}/reviewSubmissions?limit=5&include=items`)).data;
for (const r of rs) console.log('odeslání', r.id, r.attributes.state, r.attributes.submittedDate, 'položek', (r.relationships.items?.data || []).length);
