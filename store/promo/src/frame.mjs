import { mkdirSync } from 'node:fs';
import { applyMetrics } from './metrics.mjs';

const ROOT = '/Users/davidcaganek/Projekty_ClaudeCode/deriverge-web';
const SRC = `${ROOT}/store/screenshots`;
const TPL = `file://${ROOT}/store/promo/src/framed.html`;
const OUT = `${SRC}/framed`;

// mode -> [css šířka, css výška, prefix zdroje, obrazovky]
const SETS = {
  '67':   [645, 1398, 'iphone67', ['01-sell', '02-cash', '03-orders', '04-ticket', '05-history', '08-vat', '06-onboarding', '07-paywall']],
  'ipad': [1024, 1366, 'ipad129', ['01-sell', '02-cash', '03-orders', '04-ticket', '05-history', '08-vat']],
  'play': [540, 960, 'play', ['01-sell', '02-cash', '03-orders', '05-history', '08-vat', '07-paywall']],
  'ptab': [720, 1280, 'ptablet', ['01-sell', '02-cash', '03-orders', '05-history', '08-vat']],
};

// zdroj pro play/ptab jsou snímky iPhonu/iPadu, jen jiný poměr plátna
const SRCMAP = { play: 'iphone67', ptab: 'ipad129' };

export default async function ({ c, sleep }) {
  mkdirSync(OUT, { recursive: true });
  const only = process.env.ONLY;   // "mode:lang:shot" pro rychlou zkoušku
  const p = await c.newPage('about:blank');

  let n = 0;
  for (const lang of ['cs', 'en']) {
    for (const [mode, [w, h, prefix, shots]] of Object.entries(SETS)) {
      for (const shot of shots) {
        if (only && only !== `${mode}:${lang}:${shot}`) { continue; }
        const srcPrefix = SRCMAP[mode] || prefix;
        const img = encodeURIComponent(`file://${SRC}/${srcPrefix}-${lang}-${shot}.png`);
        await p.goto(`${TPL}?lang=${lang}&mode=${mode}&shot=${shot}&img=${img}`, 6000);
        if (!await applyMetrics(p, w, h, 2, false, sleep)) {
          console.log('POZOR: rozměry se nepodařilo nastavit', mode, lang, shot);
        }
        for (let i = 0; i < 40; i++) {
          if (await p.eval('window.__ready === true')) { break; }
          await sleep(150);
        }
        // po změně rozměrů je potřeba znovu rozmístit rám
        await p.run('window.__place && window.__place(); return 1;');
        await sleep(350);
        const geom = await p.run(`
          const d=document.getElementById('dev').getBoundingClientRect();
          return {vw:innerWidth, vh:innerHeight, dpr:devicePixelRatio,
                  dev:[Math.round(d.width),Math.round(d.height)]};`);
        console.log(prefix, lang, shot, JSON.stringify(geom));
        await p.shot(`${OUT}/${prefix}-${lang}-${shot}.png`);
        n++;
      }
    }
  }
  await p.s('Emulation.clearDeviceMetricsOverride');
  console.log('vykresleno snímků:', n, '->', OUT);
}
