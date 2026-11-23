// Texty stránky Tapkasy v obchodech. Jeden soubor na jazyk (cs.mjs, de.mjs, …), tady se skládají podle locale obchodů.
// Sezóna: `xmas` (vánoční trhy, do 26. 12.) nebo `year` (celoroční). Volí se přepínačem --season u skriptů, výchozí je podle data.
import cs from './cs.mjs';
import sk from './sk.mjs';
import { us, gb } from './en.mjs';
import de from './de.mjs';
import fr from './fr.mjs';
import es from './es.mjs';
import it from './it.mjs';
import pl from './pl.mjs';
import pt from './pt.mjs';
export const LANGS = { cs, sk, 'en-US': us, 'en-GB': gb, de, fr, es, it, pl, pt };
export const URLS = { privacy: 'https://www.deriverge.com/tapkasa/privacy.html', support: 'https://deriverge.com/tapkasa/support.html', marketing: 'https://www.deriverge.com/tapkasa/' };
/** Vánoční texty platí od 15. 11. do 26. 12., jinak celoroční. */
export function seasonNow(d = new Date()) {
  const m = d.getMonth() + 1, day = d.getDate();
  return (m === 11 && day >= 15) || (m === 12 && day <= 26) ? 'xmas' : 'year';
}
/** App Store: locale → { name, subtitle, keywords, promotionalText, description, whatsNew }. */
export function appstore({ season = seasonNow(), version = '1.0.9' } = {}) {
  const out = {};
  for (const t of Object.values(LANGS)) {
    out[t.as.locale] = { name: t.as.name, subtitle: t.as.subtitle, keywords: t.as.keywords,
      promotionalText: season === 'xmas' ? t.promoXmas : t.promoYear,
      description: t.desc(t.stores.as), whatsNew: version === '1.0.8' ? t.wn108 : t.wn109 };
  }
  return out;
}
/** Google Play: jazyk → { title, shortDescription, fullDescription }. */
export function play({ season = seasonNow() } = {}) {
  const out = {};
  for (const t of Object.values(LANGS)) {
    if (!t.play) continue;
    out[t.play.locale] = { title: t.play.title, shortDescription: season === 'xmas' ? t.play.shortXmas : t.play.shortYear, fullDescription: t.desc(t.stores.gp) };
  }
  return out;
}
