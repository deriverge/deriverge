// Snímky vlastních produktových stránek (store/meta/cpp.mjs): nabídka stánku, nastavení, průběh prodeje a titulky.
// Zboží [název, cena] → položky g0…g5 v tomto pořadí; `dep` je cena zálohy (položky dep a ret), bez `dep` stánek zálohy nemá.
// Průběh `flow(h)` klepe ve skutečné aplikaci a fotí obrazovky (h.shot('jméno')); obrazovka `counter` (výdej na druhém
// zařízení) vzniká sama z prvních čtyř účtů. `shots`: co se z obrazovek složí, layout single/duo, barva a tři řádky titulku.
export const PAGES = {
  'de-weihnachtsmarkt': {
    lang: 'de', cur: 'EUR', as: 'de-DE', event: 'Weihnachtsmarkt',
    goods: [['Glühwein', 4], ['Kinderpunsch', 3], ['Lebkuchen', 2.5], ['Bratwurst', 4.5], ['Eierpunsch', 4.5], ['Kakao', 3]], dep: 3,
    async flow(h) {
      await h.add('g0', 2); await h.add('g1'); await h.add('dep', 3);
      await h.shot('sell');
      await h.payCash([20]); await h.shot('cash'); await h.commit();
      await h.add('g3'); await h.add('g5'); await h.payCard(); await h.shot('card'); await h.commit();
      await h.add('g4', 2); await h.add('dep', 2); await h.payExact();
      await h.add('g0'); await h.add('g2'); await h.payExact(); await h.shot('kasa-after', { keepToast: true });
      // Gast bringt eine Tasse zurück und nimmt zwei neue Glühwein: Pfand wird verrechnet
      await h.add('g0', 2); await h.add('ret'); await h.toggle(); await h.shot('deposit');
      await h.payExact();
      await h.tab('history'); await h.shot('history');
    },
    shots: [
      { layout: 'single', a: 'sell', tone: 'red', lines: ['Kasse für den', 'Glühweinstand', 'Ohne Konto · ohne Internet'] },
      { layout: 'single', a: 'deposit', tone: 'blue', lines: ['Tasse zurück?', 'Pfand mit einem Tipp', 'Pfand rein, Pfand raus, getrennt gezählt'] },
      { layout: 'duo', a: 'kasa-after', b: 'counter', pills: true, bubble: true, tone: 'green', lines: ['Bestellnummern', 'auf dem zweiten Handy', 'Die Ausgabe liest Bestellungen vor'] },
      { layout: 'duo', a: 'cash', b: 'history', tone: 'yellow', lines: ['Rückgeld berechnet,', 'Umsatz gezählt', 'Bar und Karte, Übersicht am Abend'] },
      { layout: 'single', a: 'card', tone: 'ink', lines: ['Bar oder Karte', 'am eigenen Terminal', 'Keine Zahlungsabwicklung, nichts wird eingefroren'] },
    ],
  },
  'de-vereinsfest': {
    lang: 'de', cur: 'EUR', as: 'de-DE', event: 'Vereinsfest',
    goods: [['Bratwurst', 3], ['Pommes', 2.5], ['Kuchen', 1.5], ['Steak im Brötchen', 4.5], ['Bier', 3], ['Apfelschorle', 2]], dep: 1,
    async flow(h) {
      await h.add('g0', 2); await h.add('g1'); await h.add('g4', 2); await h.add('dep', 2);
      await h.shot('sell');
      await h.payCash([20]); await h.shot('cash'); await h.commit();
      await h.add('g3'); await h.add('g5'); await h.payCard(); await h.shot('card'); await h.commit();
      await h.add('g2', 3); await h.add('g5'); await h.payExact();
      await h.add('g0'); await h.add('g4'); await h.add('dep'); await h.payExact(); await h.shot('kasa-after', { keepToast: true });
      await h.add('g2', 2); await h.payExact();
      await h.tab('history'); await h.shot('history');
    },
    shots: [
      { layout: 'duo', a: 'kasa-after', b: 'counter', pills: true, bubble: true, tone: 'green', lines: ['Zwei Handys:', 'Kasse und Ausgabe', 'Die Ausgabe liest Bestellungen vor'] },
      { layout: 'single', a: 'sell', tone: 'red', lines: ['Festkasse für', 'Vereins- und Schulfest', 'Menü eintippen, sofort kassieren'] },
      { layout: 'duo', a: 'cash', b: 'history', tone: 'yellow', lines: ['Rückgeld berechnet,', 'Kasse gezählt', 'Bar und Karte, Übersicht am Abend'] },
      { layout: 'single', a: 'card', tone: 'ink', lines: ['Bar oder Karte', 'am eigenen Terminal', 'Keine Zahlungsabwicklung, nichts wird eingefroren'] },
    ],
  },
  'cs-spolky': {
    lang: 'cs', cur: 'CZK', as: 'cs', event: 'Školní jarmark',
    goods: [['Punč', 30], ['Káva', 40], ['Bábovka', 30], ['Chlebíček', 35], ['Perník', 25], ['Limonáda', 30]], dep: 50,
    async flow(h) {
      await h.add('g0', 2); await h.add('g2'); await h.add('dep', 2);
      await h.shot('sell');
      await h.payCash([200]); await h.shot('cash'); await h.commit();
      await h.add('g1'); await h.add('g3'); await h.payCard(); await h.shot('card'); await h.commit();
      await h.add('g4', 2); await h.add('g5'); await h.payExact();
      await h.add('g0'); await h.add('g2'); await h.payExact(); await h.shot('kasa-after', { keepToast: true });
      await h.add('g0', 2); await h.add('ret'); await h.toggle(); await h.shot('deposit');
      await h.payExact();
      await h.tab('history'); await h.shot('history');
    },
    shots: [
      { layout: 'duo', a: 'kasa-after', b: 'counter', pills: true, bubble: true, tone: 'green', lines: ['Výdej na', 'druhém telefonu', 'Objednávky s čísly, výdej je přečte nahlas'] },
      { layout: 'single', a: 'sell', tone: 'red', lines: ['Pokladna na ples,', 'jarmark i školní akci', 'Bez registrace · bez internetu'] },
      { layout: 'duo', a: 'cash', b: 'history', tone: 'yellow', lines: ['Vrácení spočítá,', 'tržbu sečte', 'Hotově i kartou, přehled na konci dne'] },
      { layout: 'single', a: 'deposit', tone: 'blue', lines: ['Záloha na hrnek', 'jedním ťuknutím', 'Zálohy vybrané a vrácené vidíte zvlášť'] },
      { layout: 'single', a: 'card', tone: 'ink', lines: ['Hotově, nebo kartou', 'na vlastním terminálu', 'Platby nezpracovává, proto nic nezmrazí'] },
    ],
  },
  'us-bake-sale': {
    lang: 'en', cur: 'USD', as: 'en-US', event: 'PTO bake sale',
    goods: [['Brownie', 2], ['Cookie', 1], ['Cupcake', 3], ['Pie slice', 4], ['Lemonade', 2], ['Coffee', 2]],
    state: { taxAdd: true, taxRate: '8.25', tips: true },
    async flow(h) {
      await h.add('g0', 2); await h.add('g2'); await h.add('g4', 2);
      await h.shot('sell');
      await h.pay(); await h.tip(10); await h.shot('method');
      await h.method('cash'); await h.notes([20]); await h.shot('cash'); await h.commit();
      await h.add('g1', 3); await h.add('g5'); await h.payCard(); await h.shot('card'); await h.commit();
      await h.add('g3'); await h.add('g5'); await h.payExact();
      await h.add('g2'); await h.add('g4'); await h.payExact(); await h.shot('kasa-after', { keepToast: true });
      await h.add('g0'); await h.add('g1', 2); await h.payExact();
      await h.tab('history'); await h.shot('history');
    },
    shots: [
      { layout: 'single', a: 'sell', tone: 'red', lines: ['Bake sale', 'cash register', 'No sign-up · works offline'] },
      { layout: 'single', a: 'method', tone: 'green', lines: ['Sales tax and tips', 'added at checkout', 'Or keep prices tax-inclusive'] },
      { layout: 'duo', a: 'cash', b: 'history', tone: 'yellow', lines: ['Change worked out,', 'every dollar counted', 'Sales tax and tips shown separately'] },
      { layout: 'single', a: 'card', tone: 'ink', lines: ['Cash, or card on', 'your own reader', 'The app never handles your money'] },
      { layout: 'duo', a: 'kasa-after', b: 'counter', pills: true, bubble: true, tone: 'blue', lines: ['Numbered orders', 'on a second phone', 'The counter reads new orders aloud'] },
    ],
  },
};
