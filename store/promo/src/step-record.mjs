// Nahraje náhledové video pro App Store: skutečný průchod aplikací,
// zachytávaný přes CDP screencast. Výstup: složka snímků + časy, ze
// kterých ffmpeg složí video ve správném tempu.
import { mkdirSync, writeFileSync } from 'node:fs';
import { applyMetrics } from './metrics.mjs';

const APP = 'file:///Users/davidcaganek/Projekty_ClaudeCode/deriverge-web/tapkasa/index.html';
const SP = '/private/tmp/claude-501/-Users-davidcaganek/d1dda034-9e20-4115-87ea-73b807657514/scratchpad';

const seed = (lang) => {
  const cs = lang === 'cs';
  const P = (a, b) => (cs ? a : b);
  const N = (a, b) => (cs ? a : b);
  return {
    v: 3, setup: true, event: N('Sobotní trh', 'Saturday market'), mode: 'kasa', nextNo: 10,
    voice: false, pair: '', license: 'pro', lang, currency: cs ? 'CZK' : 'USD',
    payDay: '', payN: 0, vat: true, seller: {}, biz: '', tourDone: true,
    items: [
      { id: 'a', name: 'Espresso', price: P(50, 2), color: 'hneda', vat: 12 },
      { id: 'b', name: 'Cappuccino', price: P(70, 3), color: 'oranzova', vat: 12 },
      { id: 'c', name: 'Caffe latte', price: P(80, 3.5), color: 'zluta', vat: 12 },
      { id: 'd', name: 'Flat white', price: P(85, 3.5), color: 'grafit', vat: 12 },
      { id: 'e', name: N('Ledová káva', 'Iced coffee'), price: P(75, 3), color: 'nebeska', vat: 12 },
      { id: 'f', name: N('Čaj', 'Tea'), price: P(40, 1.5), color: 'zelena', vat: 12 },
      { id: 'g', name: N('Limonáda', 'Lemonade'), price: P(45, 2), color: 'limetka', vat: 12 },
      { id: 'h', name: N('Koláč', 'Cake'), price: P(55, 2.5), color: 'ruzova', vat: 21 },
    ],
    order: [],
    sales: [
      { id: 's8', no: 8, ts: Date.now() - 500000, method: 'cash', total: P(120, 5),
        lines: [{ name: 'Espresso', price: P(50, 2), qty: 1, color: 'hneda', vat: '12', ready: 1 },
                { name: N('Koláč', 'Cake'), price: P(55, 2.5), qty: 1, color: 'ruzova', vat: '21', ready: 1 }] },
      { id: 's9', no: 9, ts: Date.now() - 90000, method: 'card', total: P(150, 6.5), status: 'open',
        lines: [{ name: 'Cappuccino', price: P(70, 3), qty: 1, color: 'oranzova', vat: '12', ready: 1 },
                { name: N('Ledová káva', 'Iced coffee'), price: P(75, 3), qty: 1, color: 'nebeska', vat: '12', ready: 0 }] },
    ],
    archives: [],
  };
};

export default async function ({ c, sleep }) {
  const lang = process.env.LANGV || 'cs';
  const W = parseInt(process.env.VW || '443', 10);
  const H = parseInt(process.env.VH || '960', 10);
  const OUT = `${SP}/rec-${lang}-${W}x${H}`;
  mkdirSync(OUT, { recursive: true });

  const p = await c.newPage('about:blank');
  await p.goto(`${APP}?rec=0`, 8000);
  await applyMetrics(p, W, H, 2, true, sleep);
  await p.run(`
    localStorage.clear();
    try { indexedDB.deleteDatabase('kavakasa'); } catch (e) {}
    localStorage.setItem('kavakasa.v1', ${JSON.stringify(JSON.stringify(seed(lang)))});
    location.replace(${JSON.stringify(`${APP}?rec=1`)});
    return 1;`).catch(() => {});
  await sleep(2500);
  await applyMetrics(p, W, H, 2, true, sleep);
  await sleep(800);

  // ---- screencast ----
  const frames = [];
  let n = 0;
  c.handlers.set('Page.screencastFrame', (params, sessionId) => {
    const name = `f${String(n).padStart(4, '0')}.jpg`;
    writeFileSync(`${OUT}/${name}`, Buffer.from(params.data, 'base64'));
    frames.push({ name, t: params.metadata.timestamp });
    n += 1;
    c.send('Page.screencastFrameAck', { sessionId: params.sessionId }, sessionId).catch(() => {});
  });
  await p.s('Page.startScreencast', { format: 'jpeg', quality: 88, maxWidth: W * 2, maxHeight: H * 2, everyNthFrame: 1 });

  const tap = async (sel, ms) => {
    await p.run(`
      const e=document.querySelector('${sel}');
      if(e){
        e.scrollIntoView({block:'nearest'});
        e.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerId:1}));
        e.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerId:1}));
        e.click();
      }
      return !!e;`);
    await sleep(ms || 900);
  };
  const taps = async (sel, ix, ms) => {
    await p.run(`
      const e=document.querySelectorAll('${sel}')[${ix}];
      if(e){
        e.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerId:1}));
        e.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerId:1}));
        e.click();
      }
      return !!e;`);
    await sleep(ms || 900);
  };

  // ---- choreografie, cíl ~22 s ----
  await sleep(1300);                       // úvodní pohled na prodej
  await taps('.prod', 0, 700);             // espresso
  await taps('.prod', 1, 700);             // cappuccino
  await taps('.prod', 7, 900);             // koláč
  await tap('[data-pay]', 1300);           // zaplatit
  await tap('[data-method="cash"]', 1100); // hotově
  await tap('[data-note]', 1000);          // první bankovka
  await tap('[data-exact]', 900);          // přesně
  await tap('[data-commit]', 1400);        // hotovo
  await tap('[data-tab="orders"]', 1300);  // fronta
  await tap('.tk', 1200);                  // otevřít lístek
  await taps('[data-line]', 0, 800);       // odškrtnout
  await taps('[data-line]', 1, 800);
  await taps('[data-line]', 2, 800);
  await tap('[data-serve]', 1300);         // vydáno
  await tap('[data-tab="history"]', 1700); // přehled
  await tap('[data-docask]', 1300);        // daňový doklad
  await tap('[data-docmake]', 2200);       // sestavit
  await sleep(900);

  await p.s('Page.stopScreencast');
  await sleep(500);

  // časy snímků pro ffmpeg concat
  if (frames.length < 10) { console.log('CHYBA: málo snímků', frames.length); return; }
  const t0 = frames[0].t;
  let list = '';
  for (let i = 0; i < frames.length; i++) {
    const dur = i + 1 < frames.length ? frames[i + 1].t - frames[i].t : 0.5;
    list += `file '${OUT}/${frames[i].name}'\nduration ${Math.max(0.02, dur).toFixed(3)}\n`;
  }
  list += `file '${OUT}/${frames[frames.length - 1].name}'\n`;
  writeFileSync(`${OUT}/list.txt`, list);
  console.log('snímků:', frames.length, '| délka:', (frames[frames.length - 1].t - t0 + 0.5).toFixed(1), 's | ->', OUT);
}
