// Čeština (cs v App Store, cs-CZ v Google Play).
const LINKS = `Podmínky použití: https://www.deriverge.com/tapkasa/terms.html
Zásady ochrany soukromí: https://www.deriverge.com/tapkasa/privacy.html`;
export default {
  stores: { as: 'App Store', gp: 'Google Play' },
  as: {
    locale: 'cs',
    name: 'Tapkasa: Pokladna na stánek',
    subtitle: 'Vánoční trh, jarmark, festival',
    keywords: 'kasa,mobilní,svařák,punč,záloha,spolek,školní,akce,bufet,výdej,objednávky,offline,tržba,trhy,ples',
  },
  play: {
    locale: 'cs-CZ',
    title: 'Tapkasa: Pokladna na stánek',
    shortXmas: 'Pokladna na vánoční trhy a jarmark: zálohy na hrnky, fronta s čísly, i offline.',
    shortYear: 'Pokladna na stánek, trh a festival: vratné zálohy, fronta s čísly, i offline.',
  },
  promoXmas: 'Vánoční trh, jarmark nebo punč u školy? Naťukejte menu a účtujte bez registrace a bez internetu. Záloha na hrnek jedním ťuknutím, druhý telefon ukáže frontu s čísly.',
  promoYear: 'Prodáváte na trhu, jarmarku nebo festivalu? Naťukejte menu a účtujte bez registrace a bez internetu. Vratné zálohy jedním ťuknutím, druhý telefon ukáže frontu s čísly.',
  wn108: `• Vratné zálohy: záloha na hrnek nebo kelímek jako položka, vrácení jedním ťuknutím. Přehled ukazuje zálohy vybrané a vrácené zvlášť.
• Limit bez překvapení: na denní limit bezplatné verze aplikace upozorní předem.
• Nemáte na stánku signál? Rozpracovaný účet dokončíte i tak a jednou dostanete rezervu 10 plateb navíc.`,
  wn109: `Opravy a vyladění před sezónou trhů.

Nově od 1.0.8:
• Vratné zálohy: záloha na hrnek nebo kelímek jako položka, vrácení jedním ťuknutím.
• Na denní limit bezplatné verze aplikace upozorní předem.
• Nemáte na stánku signál? Rozpracovaný účet dokončíte i tak a jednou dostanete rezervu 10 plateb navíc.`,
  desc: (store) => `Pokladna na stánek, vánoční trh, jarmark, festival i spolkovou akci. Naťukáte menu a za dvě minuty prodáváte: bez registrace, bez účtu a bez internetu.

Tapkasa prodej počítá a eviduje, platby nezpracovává. Proto vám nic nezmrazí, nic neověřuje a nebere žádné poplatky z plateb. Hotovost jde do kasírky, karta přes váš vlastní terminál.

Druhý telefon ukáže frontu objednávek s čísly a přečte je nahlas. Vratná záloha na hrnek nebo kelímek je na jedno ťuknutí. Zdarma 10 plateb denně, na celý trh si Tapkasu Pro vyzkoušíte 14 dní zdarma.

PRODEJ NA TŘI ŤUKNUTÍ
• Každá položka je barevná karta. Obsluha ji pozná dřív, než přečte název.
• Ťuknutím přidáte kus na účet, podržením karty jeden kus zase uberete.
• „+ Jiná částka“ vyřeší cokoli mimo menu.
• Špatně uložený účet vrátíte jedním ťuknutím zpět.

HOTOVĚ I KARTOU
• U hotovosti naťukáte, kolik vám zákazník podal, a Tapkasa spočítá, kolik vrátit.
• U karty účtujete na svém vlastním terminálu a v pokladně částku jen potvrdíte.

VRATNÉ ZÁLOHY
• Záloha na hrnek na svařák nebo na kelímek je karta jako každá jiná, vrácení zálohy je karta se zápornou cenou.
• Vrácení se od účtu odečte. Účet jen s vrácením se nepočítá do denního limitu a ve frontě se nepřipravuje.
• V přehledu vidíte zvlášť zálohy vybrané a vrácené.

FRONTA OBJEDNÁVEK A VÝDEJ
• Zaplacený účet se zařadí do fronty jako objednávka s číslem.
• Druhý telefon nebo tablet přepnete do role Výdej: objednávky se na něm objeví samy, položky odškrtáváte a „Vydáno“ objednávku uzavře.
• Výdej umí nové objednávky číst nahlas.
• Dva iPhony nebo dva telefony s Androidem (13 a novějším) se propojí i bez internetu. iPhone s Androidem k propojení internet potřebuje.

PŘEHLED A UZÁVĚRKA
• Tržba celkem, hotově a kartou, prodané kusy po položkách.
• Souhrn tržeb za zvolené období jako PDF s vašimi údaji a rozpisem DPH.
• Více akcí vedle sebe, uzávěrka akce s archivem.
• 9 jazyků a 33 měn.

VAŠE DATA JSOU VAŠE
• Všechno zůstává ve vašem zařízení. Žádné účty, žádná analytika, žádné reklamy.
• Zálohu dat uložíte zdarma do souboru a kdykoli z ní pokladnu obnovíte, třeba na novém telefonu.
• Výpadek signálu prodej nezastaví.

ZDARMA A PRO
Zdarma: celá pokladna na jednom zařízení, 10 zaplacených účtů denně. Na blížící se limit aplikace upozorní předem. Když zrovna nemáte signál, rozpracovaný účet dokončíte i tak a jednou dostanete rezervu 10 plateb navíc.
Tapkasa Pro (předplatné): neomezené účtování a propojení s druhým zařízením. Stánku stačí jedno předplatné, výdej se připojí zdarma. Nový předplatitel má 14 dní na vyzkoušení zdarma. Předplatné se účtuje přes ${store} a zrušíte ho kdykoli v nastavení účtu.

CO TAPKASA NENÍ
• Nezpracovává platby a není platební terminál.
• Není fiskální pokladna (EET). Používejte ji tam, kde to předpisy dovolují: spolky, školní a farní akce, dobročinné prodeje, interní evidence.
• Nevede sklad ani účetnictví.

${LINKS}`,
};
