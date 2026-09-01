// Nafotí obrazovky aplikace pro obchodní snímky. Stav se nasazuje přímo do
// localStorage, aby na snímcích byla vždycky stejná, vyladěná data.
import { applyMetrics } from './metrics.mjs';

const APP = 'file:///Users/davidcaganek/Projekty_ClaudeCode/deriverge-web/tapkasa/index.html';
const OUT = '/Users/davidcaganek/Projekty_ClaudeCode/deriverge-web/store/screenshots';

const DEV = {
  iphone67: { w: 430, h: 932, dsf: 3 },
  ipad129:  { w: 1024, h: 1366, dsf: 2 },
};

function seed(lang, mode, opts) {
  opts = opts || {};
  const cs = lang === 'cs';
  const N = (a, b) => (cs ? a : b);
  const P = (a, b) => (cs ? a : b);
  const items = [
    { id: 'a', name: 'Espresso',            price: P(50, 2),   color: 'hneda',    vat: cs ? 12 : 20 },
    { id: 'b', name: 'Cappuccino',          price: P(70, 3),   color: 'oranzova', vat: cs ? 12 : 20 },
    { id: 'c', name: 'Caffe latte',         price: P(80, 3.5), color: 'zluta',    vat: cs ? 12 : 20 },
    { id: 'd', name: 'Flat white',          price: P(85, 3.5), color: 'grafit',   vat: cs ? 12 : 20 },
    { id: 'e', name: N('Ledová káva', 'Iced coffee'), price: P(75, 3), color: 'nebeska', vat: cs ? 12 : 20 },
    { id: 'f', name: N('Čaj', 'Tea'),       price: P(40, 1.5), color: 'zelena',   vat: cs ? 12 : 20 },
    { id: 'g', name: N('Limonáda', 'Lemonade'), price: P(45, 2), color: 'limetka', vat: cs ? 12 : 20 },
    { id: 'h', name: N('Koláč', 'Cake'),    price: P(55, 2.5), color: 'ruzova',   vat: cs ? 21 : 20 },
  ];
  const L = (n, p, q, r, c, v) => ({ name: n, price: p, qty: q, ready: r, color: c, vat: String(v) });
  const T0 = Date.now();   // doklad se staví za dnešek, časy musí být dnešní
  const sales = [
    { id: 's09', no: 9,  ts: T0 - 1500000, updatedAt: T0 - 1500000, method: 'cash', total: P(190, 8),
      lines: [L('Cappuccino', P(70, 3), 1, 1, 'oranzova', cs ? 12 : 20), L(items[7].name, P(55, 2.5), 1, 1, 'ruzova', cs ? 21 : 20), L('Espresso', P(50, 2), 1, 1, 'hneda', cs ? 12 : 20)] },
    { id: 's10', no: 10, ts: T0 - 900000, updatedAt: T0 - 900000, method: 'card', total: P(160, 6.5), status: 'open',
      lines: [L(items[4].name, P(75, 3), 1, 1, 'nebeska', cs ? 12 : 20), L('Caffe latte', P(80, 3.5), 1, 0, 'zluta', cs ? 12 : 20)] },
    { id: 's11', no: 11, ts: T0 - 420000, updatedAt: T0 - 420000, method: 'card', total: P(150, 6.5), status: 'open',
      lines: [L('Cappuccino', P(70, 3), 1, 1, 'oranzova', cs ? 12 : 20), L(items[4].name, P(75, 3), 1, 0, 'nebeska', cs ? 12 : 20)] },
    { id: 's12', no: 12, ts: T0 - 60000, updatedAt: T0 - 60000, method: 'cash', total: P(180, 7.5), status: 'open',
      lines: [L('Espresso', P(50, 2), 2, 1, 'hneda', cs ? 12 : 20), L('Caffe latte', P(80, 3.5), 1, 0, 'zluta', cs ? 12 : 20)] },
  ];
  return {
    v: 3, setup: true, event: N('Sobotní trh', 'Saturday market'), mode,
    nextNo: 13, voice: true, pair: 'KQ7RD', license: opts.free ? '' : 'pro', lang,
    currency: cs ? 'CZK' : 'USD', payDay: '', payN: 0,
    vat: true,
    biz: N('Kavárna Na Rohu s.r.o.\nIČ 12345678\nDIČ CZ12345678\nNáměstí 1, Praha',
           'Corner Coffee Ltd.\nCompany No. 12345678\nVAT ID GB123456789\n1 Market Square, London'),
    items,
    order: mode === 'kasa'
      ? [{ ref: 'a', name: 'Espresso', price: P(50, 2), qty: 2, color: 'hneda', vat: String(cs ? 12 : 20) },
         { ref: 'b', name: 'Cappuccino', price: P(70, 3), qty: 1, color: 'oranzova', vat: String(cs ? 12 : 20) },
         { ref: 'h', name: items[7].name, price: P(55, 2.5), qty: 1, color: 'ruzova', vat: String(cs ? 21 : 20) }]
      : [],
    sales, archives: [],
  };
}

export default async function ({ c, sleep }) {
  const p = await c.newPage('about:blank');

  let bust = 0;
  async function boot(dev, lang, mode, fresh, opts) {
    const d = DEV[dev];
    // jiná adresa při každém načtení: prohlížeč jinak stejný odkaz přeskočí
    await p.goto(`${APP}?r=${++bust}`, 6000);
    if (!await applyMetrics(p, d.w, d.h, d.dsf, true, sleep)) {
      console.log('POZOR: rozměry se nepodařilo nastavit', dev);
    }
    // Aplikace si stav zrcadlí i do IndexedDB a odtud ho po vymazání
    // localStorage zase obnoví. Smazat je proto potřeba obojí a hned odejít,
    // ať běžící stránka nestihne zapsat stav zpátky.
    await p.run(`
      localStorage.clear();
      try { indexedDB.deleteDatabase('kavakasa'); } catch (e) {}
      location.replace(${JSON.stringify(`${APP}?r=${++bust}`)});
      return 1;`).catch(() => {});
    await sleep(2200);
    if (!fresh) {
      await p.run(`
        localStorage.setItem('kavakasa.v1', ${JSON.stringify(JSON.stringify(seed(lang, mode, opts)))});
        location.replace(${JSON.stringify(`${APP}?r=${++bust}`)});
        return 1;`).catch(() => {});
      await sleep(2200);
    }
    // po posledním přechodu rozměry ještě jednou ověřit
    if (!await applyMetrics(p, d.w, d.h, d.dsf, true, sleep)) {
      console.log('POZOR: rozměry po načtení nesedí', dev);
    }
    await sleep(400);
  }

  const tab = (name) => `
    const t=[...document.querySelectorAll('[data-tab]')].find(e=>e.dataset.tab==='${name}');
    if(t)t.click(); return !!t;`;

  let n = 0;
  const grab = async (dev, lang, shot) => {
    await sleep(700);
    await p.shot(`${OUT}/${dev}-${lang}-${shot}.png`);
    n++;
  };

  for (const lang of ['cs', 'en']) {
    for (const dev of ['iphone67', 'ipad129']) {

      // 01 prodej
      await boot(dev, lang, 'kasa', false);
      await grab(dev, lang, '01-sell');

      // 02 platba hotově
      await p.run(`const b=document.querySelector('[data-pay]'); if(b)b.click(); return 1;`);
      await sleep(900);
      await p.run(`const b=document.querySelector('[data-method="cash"]'); if(b)b.click(); return 1;`);
      await grab(dev, lang, '02-cash');

      // 03 objednávky
      await boot(dev, lang, 'kasa', false);
      await p.run(tab('orders'));
      await grab(dev, lang, '03-orders');

      // 04 výdej jednoho lístku
      await p.run(`const b=document.querySelector('[data-ticket]'); if(b)b.click(); return 1;`);
      await grab(dev, lang, '04-ticket');

      // 05 přehled
      await boot(dev, lang, 'kasa', false);
      await p.run(tab('history'));
      await grab(dev, lang, '05-history');

      // 08 daňový doklad s rozpisem DPH
      await p.run(`const b=document.querySelector('[data-docask]'); if(b)b.click(); return 1;`);
      await sleep(900);
      await p.run(`const b=document.querySelector('[data-docmake]'); if(b)b.click(); return 1;`);
      await sleep(700);
      // doklad je delší než okno, srolovat na rozpis DPH, kvůli kterému snímek je
      await p.run(`
        const a=document.getElementById('dump'); if(!a) return 'bez pole';
        const t=a.value||''; const i=t.search(/Rozpis DPH|VAT breakdown/);
        if(i<0) return 'rozpis nenalezen';
        const before=t.slice(0,i).split('\\n').length;
        const lh=parseFloat(getComputedStyle(a).lineHeight)||18;
        a.scrollTop=Math.max(0,(before-3)*lh);
        return {before, lh, scrollTop:a.scrollTop, max:a.scrollHeight};`).then(r=>console.log('doklad', dev, lang, JSON.stringify(r)));
      await grab(dev, lang, '08-vat');

      // 06 úvod (jen telefon)
      if (dev === 'iphone67') {
        await boot(dev, lang, 'kasa', true);
        // úvod startuje v jazyce prohlížeče, pro anglickou sadu ho přepneme
        if (lang === 'en') {
          await p.run(`
            const l=document.querySelector('[data-oblang="en"]'); if(l)l.click();
            return 1;`);
          await sleep(500);
          await p.run(`
            const c=document.querySelector('[data-obcur="USD"]'); if(c)c.click();
            return 1;`);
          await sleep(500);
        }
        await grab(dev, lang, '06-onboarding');

        // 07 předplatné: bez tarifu, jinak se nabídka vůbec nezobrazí
        await boot(dev, lang, 'kasa', false, { free: true });
        await p.run(tab('menu'));
        await sleep(500);
        // ceny doplníme ručně: bez nativního mostu by v české verzi svítily dolary
        await p.run(lang === 'cs'
          ? `window.__KASA_PRICES__={monthly:'129 Kč',yearly:'999 Kč'}; return 1;`
          : `window.__KASA_PRICES__={monthly:'$4.99',yearly:'$39.99'}; return 1;`);
        await p.run(`const b=document.querySelector('[data-paywall]'); if(b)b.click(); return 1;`);
        await grab(dev, lang, '07-paywall');
      }
    }
  }

  await p.s('Emulation.clearDeviceMetricsOverride');
  console.log('nafoceno:', n);
}
