// Veřejná stránka Tapkasy v Google Play (bez přihlášení): název, krátký a úplný popis, snímky.
import { execFileSync } from 'node:child_process';
import { PKG, len } from './clients.mjs';
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36';
/** Jazyk listingu → [hl, gl] veřejné stránky. */
export const PLAY_WEB = { 'cs-CZ': ['cs', 'CZ'], sk: ['sk', 'SK'], 'en-US': ['en-US', 'US'], 'en-GB': ['en-GB', 'GB'], 'de-DE': ['de', 'DE'], 'pl-PL': ['pl', 'PL'], 'fr-FR': ['fr', 'FR'], 'it-IT': ['it', 'IT'], 'es-ES': ['es', 'ES'], 'es-419': ['es-419', 'MX'], 'pt-PT': ['pt-PT', 'PT'], 'pt-BR': ['pt-BR', 'BR'] };
const text = (h) => String(h || '').replace(/<br\s*\/?>/g, '\n').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
export function playPage(lang) {
  const [hl, gl] = PLAY_WEB[lang];
  const html = execFileSync('curl', ['-sS', '-L', '--compressed', '--max-time', '40', '-A', UA, `https://play.google.com/store/apps/details?id=${PKG}&hl=${hl}&gl=${gl}`], { maxBuffer: 64 * 1024 * 1024 }).toString();
  const m = html.match(/AF_initDataCallback\(\{key: 'ds:5'[\s\S]*?data:([\s\S]*?), sideChannel: \{\}\}\);<\/script>/);
  if (!m) return { error: 'ds:5 nenalezeno', bytes: html.length };
  const d = JSON.parse(m[1])[1][2];
  const g = (o, ...p) => p.reduce((a, k) => (a == null ? a : a[k]), o);
  const o = { title: g(d, 0, 0), shortDescription: text(g(d, 73, 0, 1)), fullDescription: text(g(d, 72, 0, 1)), released: g(d, 10, 0), iapPriceRange: g(d, 19, 0),
    installs: g(d, 13, 0), ratings: g(d, 51, 2, 1) || 0, score: g(d, 51, 0, 1) || null, genre: g(d, 79, 0, 0, 0),
    icon: g(d, 95, 0, 3, 2), featureGraphic: g(d, 96, 0, 3, 2), video: g(d, 100, 0, 0, 3, 2) || null,
    screenshots: (g(d, 78, 0) || []).map((s) => ({ url: g(s, 3, 2), width: g(s, 2, 1), height: g(s, 2, 0) })) };
  o.lengths = { title: len(o.title), shortDescription: len(o.shortDescription), fullDescription: len(o.fullDescription) };
  return o;
}
