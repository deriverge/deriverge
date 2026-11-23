// Vydání Tapkasy na Google Play. Jen s Davidovým souhlasem pro konkrétní verzi.
//   node store/vydani/play.mjs status
//   node store/vydani/play.mjs publish <verze> <cesta k podepsanému .aab>
// Nahraje balíček, založí produkční vydání s poznámkami ze store/vydani/whats_new_<verze>.json
// (jazyk podle prvních dvou písmen jazyka stránky v obchodě) a odešle ho.
import fs from 'node:fs';
import path from 'node:path';
import { play, PKG, len } from '../tool/clients.mjs';
const R = new URL('../../', import.meta.url).pathname;
const api = await play();
const E = `/applications/${PKG}/edits`;
const [cmd, ver, aab] = process.argv.slice(2);
if (cmd === 'status') {
  const edit = api('POST', E, {}).id;
  const t = api('GET', `${E}/${edit}/tracks/production`);
  for (const r of t.releases || []) console.log(r.name, r.versionCodes, r.status, (r.releaseNotes || []).map((n) => n.language).join(','));
  api('DELETE', `${E}/${edit}`);
} else if (cmd === 'publish' && ver && aab) {
  const notes = JSON.parse(fs.readFileSync(`${R}store/vydani/whats_new_${ver}.json`, 'utf8'));
  const edit = api('POST', E, {}).id;
  const langs = (api('GET', `${E}/${edit}/listings`).listings || []).map((l) => l.language);
  const b = api('POST', `${E}/${edit}/bundles?uploadType=media`, undefined, { upload: path.resolve(aab) });
  console.log('nahráno, versionCode', b.versionCode);
  const releaseNotes = langs.map((language) => ({ language, text: notes[language.slice(0, 2)] })).filter((n) => n.text);
  for (const n of releaseNotes) if (len(n.text) > 500) throw new Error(`poznámka ${n.language} má ${len(n.text)} znaků`);
  const missing = langs.filter((l) => !notes[l.slice(0, 2)]);
  if (missing.length) throw new Error('chybí poznámky pro ' + missing.join(','));
  api('PUT', `${E}/${edit}/tracks/production`, { track: 'production', releases: [{ name: `${ver} (${b.versionCode})`, versionCodes: [String(b.versionCode)], status: 'completed', releaseNotes }] });
  const c = api('POST', `${E}/${edit}:commit`);
  console.log('odesláno, edit', c.id, 'jazyky poznámek:', releaseNotes.map((n) => n.language).join(','));
} else {
  console.log('použití: status | publish <verze> <aab>');
}
