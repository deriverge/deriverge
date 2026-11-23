// Vydání Tapkasy v App Store. Jen s Davidovým souhlasem pro danou verzi.
//   node store/vydani/asc.mjs status
//   node store/vydani/asc.mjs prep <verze>     založí verzi (když není) a zapíše „Co je nového“ ze store/vydani/whats_new_<verze>.json
//   node store/vydani/asc.mjs attach <verze>   připojí nejnovější zpracované sestavení té verze
//   node store/vydani/asc.mjs submit <verze>   odešle verzi ke kontrole
import fs from 'node:fs';
import { asc, ASC_APP } from '../tool/clients.mjs';
const api = await asc();
const APP = ASC_APP;
const [cmd, version] = process.argv.slice(2);
const versions = async () => (await api('GET', `/v1/apps/${APP}/appStoreVersions?limit=5&filter[platform]=IOS`)).data;
const find = async () => (await versions()).find((v) => v.attributes.versionString === version);
if (cmd === 'status') {
  for (const v of await versions()) {
    let build = '';
    try { const b = await api('GET', `/v1/appStoreVersions/${v.id}/build`); build = b.data ? 'build ' + b.data.attributes.version : 'bez sestavení'; } catch { build = '?'; }
    console.log(v.attributes.versionString, v.attributes.appStoreState, build);
  }
  const b = await api('GET', `/v1/builds?filter[app]=${APP}&limit=3&sort=-uploadedDate`);
  for (const x of b.data) console.log('sestavení', x.attributes.version, x.attributes.processingState, x.attributes.uploadedDate);
  const rs = await api('GET', `/v1/apps/${APP}/reviewSubmissions?limit=2`);
  for (const r of rs.data) console.log('kontrola', r.attributes.state, r.attributes.submittedDate);
} else if (cmd === 'prep') {
  const notes = JSON.parse(fs.readFileSync(new URL(`./whats_new_${version}.json`, import.meta.url), 'utf8'));
  let v = await find();
  if (!v) {
    v = (await api('POST', '/v1/appStoreVersions', { data: { type: 'appStoreVersions', attributes: { platform: 'IOS', versionString: version, releaseType: 'AFTER_APPROVAL' }, relationships: { app: { data: { type: 'apps', id: APP } } } } })).data;
    console.log('založena verze', version, v.id);
  }
  const locs = (await api('GET', `/v1/appStoreVersions/${v.id}/appStoreVersionLocalizations?limit=50`)).data;
  for (const l of locs) {
    const text = notes[l.attributes.locale.slice(0, 2)] || notes.en;
    await api('PATCH', `/v1/appStoreVersionLocalizations/${l.id}`, { data: { type: 'appStoreVersionLocalizations', id: l.id, attributes: { whatsNew: text } } });
    console.log(l.attributes.locale, text.length, 'znaků');
  }
} else if (cmd === 'attach') {
  const v = await find();
  const b = (await api('GET', `/v1/builds?filter[app]=${APP}&filter[preReleaseVersion.version]=${version}&limit=1&sort=-uploadedDate`)).data[0];
  if (!v || !b) throw new Error('Chybí verze nebo sestavení.');
  if (b.attributes.processingState !== 'VALID') throw new Error('Sestavení se ještě zpracovává: ' + b.attributes.processingState);
  if (b.attributes.usesNonExemptEncryption == null) await api('PATCH', `/v1/builds/${b.id}`, { data: { type: 'builds', id: b.id, attributes: { usesNonExemptEncryption: false } } });
  await api('PATCH', `/v1/appStoreVersions/${v.id}/relationships/build`, { data: { type: 'builds', id: b.id } });
  console.log('připojeno sestavení', b.attributes.version, 'k verzi', version);
} else if (cmd === 'submit') {
  const v = await find();
  if (!v) throw new Error('Verze neexistuje.');
  // Rozpracované odeslání (stav READY_FOR_REVIEW) se použije znovu, druhé vedle něj založit nejde.
  const open = (await api('GET', `/v1/apps/${APP}/reviewSubmissions?limit=10&filter[state]=READY_FOR_REVIEW&filter[platform]=IOS`)).data[0];
  const s = open || (await api('POST', '/v1/reviewSubmissions', { data: { type: 'reviewSubmissions', attributes: { platform: 'IOS' }, relationships: { app: { data: { type: 'apps', id: APP } } } } })).data;
  await api('POST', '/v1/reviewSubmissionItems', { data: { type: 'reviewSubmissionItems', relationships: { reviewSubmission: { data: { type: 'reviewSubmissions', id: s.id } }, appStoreVersion: { data: { type: 'appStoreVersions', id: v.id } } } } });
  const r = (await api('PATCH', `/v1/reviewSubmissions/${s.id}`, { data: { type: 'reviewSubmissions', id: s.id, attributes: { submitted: true } } })).data;
  console.log('odesláno ke kontrole:', r.attributes.state);
} else console.log('status | prep <verze> | attach <verze> | submit <verze>');
