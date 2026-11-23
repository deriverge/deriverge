// Obsah obchodních snímků Tapkasy: nabídka vánočního stánku a titulky pro každé locale.
// Zboží [název, cena] v pořadí: horký nápoj 1, horký nápoj 2, sladké, slané, nápoj 3, nápoj 4. Záloha je cena hrnku nebo kelímku.
// Názvy karet zálohy a hlášení „Nová objednávka číslo“ se berou přímo ze slovníků aplikace (tapkasa/index.html).
import fs from 'node:fs';
export const APP_FILE = new URL('../../tapkasa/index.html', import.meta.url).pathname;
export const LOCALES = {
  cs: { lang: 'cs', cur: 'CZK', as: 'cs', play: 'cs-CZ', event: 'Vánoční trh', cash: [500],
    goods: [['Svařák', 60], ['Punč', 70], ['Trdelník', 90], ['Klobása', 120], ['Horká čokoláda', 65], ['Čaj', 40]], dep: 50,
    copy: [['Pokladna na stánek', 'za 2 minuty', 'Bez registrace · bez internetu'], ['Fronta s čísly', 'na druhém telefonu', 'Výdej přečte objednávky nahlas'],
      ['Vrácení spočítá,', 'tržbu sečte', 'Hotově i kartou, přehled na konci dne'], ['Záloha na hrnek', 'jedním ťuknutím', 'Zálohy vybrané a vrácené vidíte zvlášť'],
      ['Hotově, nebo kartou', 'na vlastním terminálu', 'Platby nezpracovává, proto nic nezmrazí']] },
  sk: { lang: 'sk', cur: 'EUR', as: 'sk', play: 'sk', event: 'Vianočné trhy', cash: [20],
    goods: [['Varené víno', 3], ['Punč', 3.5], ['Trdelník', 4.5], ['Klobása', 5.5], ['Horúca čokoláda', 3], ['Čaj', 2]], dep: 2,
    copy: [['Pokladňa na stánok', 'za 2 minúty', 'Bez registrácie · bez internetu'], ['Objednávky s číslami', 'na druhom telefóne', 'Výdaj ich prečíta nahlas'],
      ['Vrátenie vypočíta,', 'tržbu spočíta', 'Hotovosť aj karta, prehľad na konci dňa'], ['Záloha na hrnček', 'jedným ťuknutím', 'Zálohy vybrané a vrátené vidíte zvlášť'],
      ['Hotovosť alebo karta', 'na vlastnom termináli', 'Platby nespracúva, preto nič nezmrazí']] },
  'en-US': { lang: 'en', cur: 'USD', as: 'en-US', play: 'en-US', event: 'Holiday market', cash: [20, 10],
    goods: [['Hot cider', 4], ['Hot cocoa', 3], ['Pretzel', 5], ['Bratwurst', 7], ['Kettle corn', 6], ['Coffee', 3]], dep: 5,
    copy: [['Booth cash register', 'ready in 2 minutes', 'No sign-up · works offline'], ['Numbered orders', 'on a second phone', 'The counter reads new orders aloud'],
      ['Change worked out,', 'sales added up', 'Cash and card totals at a glance'], ['Cup deposits', 'in one tap', 'Deposits taken and paid back, shown apart'],
      ['Cash, or card on', 'your own reader', 'The app never handles your money']] },
  'en-GB': { lang: 'en', cur: 'GBP', as: 'en-GB', play: 'en-GB', event: 'Christmas market', cash: [20],
    goods: [['Mulled wine', 5], ['Hot chocolate', 3.5], ['Mince pies', 3], ['Bratwurst', 6], ['Crêpe', 4.5], ['Tea', 2]], dep: 3,
    copy: [['Market stall till', 'ready in 2 minutes', 'No sign-up · works offline'], ['Numbered orders', 'on a second phone', 'The counter reads new orders aloud'],
      ['Change worked out,', 'takings added up', 'Cash and card totals at a glance'], ['Mug deposits', 'in one tap', 'Deposits taken and paid back, shown apart'],
      ['Cash, or card on', 'your own reader', 'The app never handles your money']] },
  de: { lang: 'de', cur: 'EUR', as: 'de-DE', play: 'de-DE', event: 'Weihnachtsmarkt', cash: [20],
    goods: [['Glühwein', 4], ['Kinderpunsch', 3], ['Waffel', 3.5], ['Bratwurst', 4.5], ['Kakao', 3], ['Tee', 2.5]], dep: 3,
    copy: [['Kasse für den Stand', 'in 2 Minuten', 'Ohne Konto · ohne Internet'], ['Bestellnummern', 'auf dem zweiten Handy', 'Die Ausgabe liest Bestellungen vor'],
      ['Rückgeld berechnet,', 'Umsatz gezählt', 'Bar und Karte, Übersicht am Abend'], ['Tassenpfand', 'mit einem Tipp', 'Pfand eingenommen und ausgezahlt, getrennt'],
      ['Bar oder Karte', 'am eigenen Terminal', 'Keine Zahlungsabwicklung, nichts wird eingefroren']] },
  fr: { lang: 'fr', cur: 'EUR', as: 'fr-FR', play: 'fr-FR', event: 'Marché de Noël', cash: [20],
    goods: [['Vin chaud', 4], ['Chocolat chaud', 3], ['Crêpe', 3.5], ['Bretzel', 3], ['Gaufre', 4], ['Thé', 2]], dep: 1,
    copy: [['Caisse pour stand', 'en 2 minutes', 'Sans inscription · sans internet'], ['Commandes numérotées', 'sur un second téléphone', 'Le comptoir les lit à voix haute'],
      ['Monnaie calculée,', 'recette comptée', 'Espèces et carte, bilan en fin de journée'], ['Consigne du gobelet', 'en un geste', 'Consignes encaissées et rendues, à part'],
      ['Espèces ou carte', 'sur votre terminal', 'Aucun paiement traité, rien n’est bloqué']] },
  es: { lang: 'es', cur: 'EUR', as: 'es-ES', play: 'es-ES', event: 'Mercadillo navideño', cash: [20],
    goods: [['Chocolate caliente', 3], ['Vino caliente', 3.5], ['Churros', 4], ['Bocadillo', 5], ['Castañas', 3], ['Café', 1.5]], dep: 1,
    copy: [['Caja para su puesto', 'en 2 minutos', 'Sin registro · sin internet'], ['Pedidos numerados', 'en un segundo móvil', 'La barra los lee en voz alta'],
      ['Cambio calculado,', 'ventas sumadas', 'Efectivo y tarjeta, resumen al cierre'], ['Depósito del vaso', 'con un toque', 'Depósitos cobrados y devueltos, aparte'],
      ['Efectivo o tarjeta', 'en su propio datáfono', 'No procesa pagos, no bloquea nada']] },
  it: { lang: 'it', cur: 'EUR', as: 'it', play: 'it-IT', event: 'Mercatino di Natale', cash: [20],
    goods: [['Vin brulé', 4], ['Cioccolata calda', 3.5], ['Frittelle', 4], ['Panino', 6], ['Caldarroste', 4], ['Tè', 2]], dep: 2,
    copy: [['Cassa per bancarelle', 'in 2 minuti', 'Senza registrazione · senza internet'], ['Ordini numerati', 'su un secondo telefono', 'Il banco li legge ad alta voce'],
      ['Resto calcolato,', 'incasso sommato', 'Contanti e carta, riepilogo a fine giornata'], ['Cauzione della tazza', 'con un tocco', 'Cauzioni incassate e restituite, separate'],
      ['Contanti o carta', 'sul vostro POS', 'Non elabora pagamenti, non blocca nulla']] },
  pl: { lang: 'pl', cur: 'PLN', as: 'pl', play: 'pl-PL', event: 'Jarmark świąteczny', cash: [100],
    goods: [['Grzaniec', 18], ['Gorąca czekolada', 15], ['Gofry', 16], ['Kiełbasa', 25], ['Oscypek', 12], ['Herbata', 8]], dep: 10,
    copy: [['Kasa na stoisko', 'w 2 minuty', 'Bez rejestracji · bez internetu'], ['Numery zamówień', 'na drugim telefonie', 'Wydawka czyta je na głos'],
      ['Reszta policzona,', 'utarg podliczony', 'Gotówka i karta, podsumowanie na koniec dnia'], ['Kaucja za kubek', 'jednym stuknięciem', 'Kaucje pobrane i zwrócone osobno'],
      ['Gotówka albo karta', 'na własnym terminalu', 'Nie obsługuje płatności, niczego nie blokuje']] },
  pt: { lang: 'pt', cur: 'EUR', as: 'pt-PT', play: 'pt-PT', event: 'Mercado de Natal', cash: [20],
    goods: [['Vinho quente', 3], ['Chocolate quente', 3], ['Filhós', 2.5], ['Bifana', 4.5], ['Castanhas', 3], ['Café', 1]], dep: 1,
    copy: [['Caixa para a banca', 'em 2 minutos', 'Sem registo · sem internet'], ['Pedidos numerados', 'num segundo telemóvel', 'O balcão lê-os em voz alta'],
      ['Troco calculado,', 'receita somada', 'Dinheiro e cartão, resumo ao fim do dia'], ['Caução do copo', 'com um toque', 'Cauções cobradas e devolvidas, à parte'],
      ['Dinheiro ou cartão', 'no seu terminal', 'Não processa pagamentos, não bloqueia nada']] },
};
export const SHOT_NAMES = ['01-stanek-za-2-minuty', '02-fronta-a-vydej', '03-vraceni-a-trzba', '04-vratna-zaloha', '05-hotove-nebo-kartou'];
const COLORS = ['cervena', 'oranzova', 'zluta', 'hneda', 'ruzova', 'zelena'];
/** Text ze slovníku aplikace (I18N.<lang>.<key>), čte se ze souboru aplikace. */
let appSrc = null;
export function appText(lang, key) {
  appSrc = appSrc || fs.readFileSync(APP_FILE, 'utf8');
  const a = appSrc.indexOf(`I18N.${lang} = {`); if (a < 0) throw new Error('slovník ' + lang);
  const b = appSrc.indexOf('\n  };', a);
  const m = appSrc.slice(a, b).match(new RegExp(`\\n\\s*${key}: ("(?:[^"\\\\]|\\\\.)*")`));
  if (!m) throw new Error(`chybí ${lang}.${key}`);
  return JSON.parse(m[1]);
}
/** Položky stánku: šest druhů zboží, záloha a vrácení zálohy (stejně je zakládá tlačítko „+ Přidat zálohu“). */
export function itemsFor(L) {
  const it = L.goods.map(([name, price], i) => ({ id: 'g' + i, name, price, color: COLORS[i] }));
  it.push({ id: 'dep', name: appText(L.lang, 'depItem'), price: L.dep, color: 'nebeska', dep: true });
  it.push({ id: 'ret', name: appText(L.lang, 'depReturn'), price: -L.dep, color: 'grafit', dep: true });
  return it;
}
