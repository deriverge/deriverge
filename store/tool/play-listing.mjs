// Texty a snímky telefonu na stránce Tapkasy v Google Play.
//
//   node store/tool/play-listing.mjs                 nanečisto: porovná s veřejnou stránkou obchodu, rozhraní Play se nedotkne
//   node store/tool/play-listing.mjs --go            založí edit, zapíše texty a snímky, ověří a uloží (commit)
//   … --season xmas|year    krátký popis vánoční, nebo celoroční (výchozí podle data: 15. 11. až 26. 12. vánoční)
//   … --langs de-DE,cs-CZ   jen některé jazyky
//   … --no-shots            jen texty      … --shots <složka>   jiná složka se snímky
//   … --short-only          jen krátký popis, např. návrat po Vánocích:
//                           node store/tool/play-listing.mjs --short-only --season year --go
//
// Texty slibují vratné zálohy (od 1.0.8, versionCode 11). Se --go skript nejdřív ověří, že je v produkci aspoň tato verze;
// jinak skončí a nic neuloží. Zápis jen po výslovném souhlasu majitele.
import fs from 'node:fs';
import path from 'node:path';
import { play as playClient, PKG, len } from './clients.mjs';
import { play as texts, seasonNow } from '../meta/index.mjs';
import { playPage } from './play-public.mjs';
import { SHOTS_DIR, PLAY_PHONE, pngSize, listShots } from './shots-common.mjs';

const args = process.argv.slice(2);
const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null; };
const GO = args.includes('--go'), SHORT_ONLY = args.includes('--short-only'), NO_SHOTS = args.includes('--no-shots') || SHORT_ONLY;
const season = opt('--season') || seasonNow();
if (!['xmas', 'year'].includes(season)) throw new Error('--season xmas|year');
const shotsRoot = path.join(opt('--shots') || SHOTS_DIR, 'play');
const want = (opt('--langs') || '').split(',').filter(Boolean);
const MIN_CODE = 11; // 1.0.8
const T = texts({ season });
const show = (s) => String(s ?? '').replace(/\n/g, ' ⏎ ');
const log = (...a) => console.log(...a);
let changes = 0;
function diff(lang, field, was, now, max) {
  if ((was ?? '').trim() === now.trim()) return false;
  changes++;
  if (len(now) > 200) log(`  ${lang} ${field} (${len(now)}/${max}): změna (${len(was)} → ${len(now)} znaků), začátek: ${show(now).slice(0, 110)}…`);
  else log(`  ${lang} ${field} (${len(now)}/${max}):\n      teď:  ${show(was) || '(prázdné)'}\n      nově: ${show(now)}`);
  return true;
}
function shotsFor(lang) {
  const files = listShots(path.join(shotsRoot, lang, 'phone'));
  if (files.length > 8) throw new Error(`${lang}: víc než 8 snímků telefonu`);
  for (const f of files) { const s = pngSize(f); if (s.w !== PLAY_PHONE.w || s.h !== PLAY_PHONE.h) throw new Error(`${f}: ${s.w}×${s.h}, čeká se ${PLAY_PHONE.w}×${PLAY_PHONE.h}`); }
  return files;
}
log(`Tapkasa → Google Play | ${GO ? 'ZÁPIS (--go)' : 'nanečisto (veřejná stránka, bez přihlášení)'} | sezóna ${season}${SHORT_ONLY ? ' | jen krátký popis' : ''}`);
const langs = Object.keys(T).filter((l) => !want.length || want.includes(l));

if (!GO) {
  for (const lang of langs) {
    const t = T[lang], now = playPage(lang);
    log(`\n== ${lang}`);
    if (now.error) { log('  veřejná stránka se nenačetla:', now.error); continue; }
    if (!SHORT_ONLY) diff(lang, 'název', now.title, t.title, 30);
    diff(lang, 'krátký popis', now.shortDescription, t.shortDescription, 80);
    if (!SHORT_ONLY) diff(lang, 'úplný popis', now.fullDescription, t.fullDescription, 4000);
    if (!NO_SHOTS) {
      const files = shotsFor(lang);
      if (files.length) { changes++; log(`  ${lang} snímky telefonu: teď ${now.screenshots.length} na stránce (i s tablety), nově ${files.length}: ${files.map((f) => path.basename(f)).join(', ')}`); }
      else log(`  ${lang} snímky telefonu: žádné soubory, zůstanou, jak jsou`);
    }
  }
  log(`\nNanečisto: ${changes} změn proti veřejné stránce. Nic se nezapsalo. Zápis: přidat --go (ověří, že je v produkci aspoň 1.0.8).`);
  process.exit(0);
}

const api = await playClient();
const E = `/applications/${PKG}/edits`;
const edit = api('POST', E, {}).id;
try {
  const track = api('GET', `${E}/${edit}/tracks/production`);
  const codes = (track.releases || []).filter((r) => ['completed', 'inProgress'].includes(r.status)).flatMap((r) => (r.versionCodes || []).map(Number));
  const top = Math.max(0, ...codes);
  log('V produkci versionCode', top || 'žádný');
  if (top < MIN_CODE) throw new Error(`v produkci je versionCode ${top}, texty ale slibují vratné zálohy (od 1.0.8, versionCode ${MIN_CODE}). Nejdřív vydat 1.0.8 nebo novější.`);
  const existing = Object.fromEntries((api('GET', `${E}/${edit}/listings`).listings || []).map((l) => [l.language, l]));
  for (const lang of langs) {
    const t = T[lang], now = existing[lang];
    log(`\n== ${lang}${now ? '' : '  (NOVÝ jazyk)'}`);
    const body = SHORT_ONLY ? { shortDescription: t.shortDescription } : { title: t.title, shortDescription: t.shortDescription, fullDescription: t.fullDescription };
    let dirty = false;
    for (const k of Object.keys(body)) dirty = diff(lang, k, now?.[k], body[k], { title: 30, shortDescription: 80, fullDescription: 4000 }[k]) || dirty;
    if (dirty && now) api('PATCH', `${E}/${edit}/listings/${lang}`, body);
    else if (dirty) { if (SHORT_ONLY) throw new Error(lang + ': jazyk v obchodě není, --short-only ho nezaloží'); api('PUT', `${E}/${edit}/listings/${lang}`, { language: lang, ...body }); }
    if (NO_SHOTS) continue;
    const files = shotsFor(lang);
    if (!files.length) { log(`  ${lang} snímky telefonu: žádné soubory, zůstanou, jak jsou`); continue; }
    changes++;
    api('DELETE', `${E}/${edit}/listings/${lang}/phoneScreenshots`);
    for (const f of files) api('POST', `${E}/${edit}/listings/${lang}/phoneScreenshots`, undefined, { upload: f, contentType: 'image/png' });
    log(`  ${lang} snímky telefonu: nahráno ${files.length}`);
  }
  if (!changes) { api('DELETE', `${E}/${edit}`); log('\nŽádná změna, edit zrušen.'); process.exit(0); }
  api('POST', `${E}/${edit}:validate`);
  const c = api('POST', `${E}/${edit}:commit`);
  log(`\nULOŽENO, edit ${c.id}, změn ${changes}. Google změny ještě kontroluje, na stránce se objeví po schválení.`);
} catch (e) {
  log('NEPROŠLO, nic se neuložilo:', e.message.slice(0, 600));
  try { api('DELETE', `${E}/${edit}`); } catch { }
  process.exit(1);
}
