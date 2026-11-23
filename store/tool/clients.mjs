// Klienti obchodů pro Tapkasu. Klíče ani jejich čísla v tomto repozitáři nejsou (repozitář je veřejný web):
// klient App Store Connect se bere z Fixbillu, klient Google Play z VZT Montéra. Obojí čte klíče z domovské složky.
//   ASC_CLIENT=/cesta/asc.mjs  PLAY_CLIENT=/cesta/play.mjs  přepíše výchozí cesty.
import os from 'node:os';
export const ASC_APP = '6807075649';
export const PKG = 'com.deriverge.tapkasa';
const home = os.homedir();
export async function asc() {
  const m = await import(process.env.ASC_CLIENT || home + '/Projekty_ClaudeCode/fixbill/tool/asc/asc.mjs');
  return m.api;
}
export async function play() {
  const m = await import(process.env.PLAY_CLIENT || home + '/Projekty_ClaudeCode/vzduchotechnika_app/tool/play/play.mjs');
  return m.api;
}
/** Délka tak, jak ji počítají obchody (znaky Unicode, ne bajty). */
export const len = (s) => [...String(s || '')].length;
