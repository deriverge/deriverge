// Slovenčina (sk v App Store aj v Google Play).
const LINKS = `Podmienky použitia: https://www.deriverge.com/tapkasa/terms.html
Zásady ochrany súkromia: https://www.deriverge.com/tapkasa/privacy.html`;
export default {
  stores: { as: 'App Store', gp: 'Google Play' },
  as: {
    locale: 'sk',
    name: 'Tapkasa: Pokladňa na stánok',
    subtitle: 'Vianočný trh, jarmok, festival',
    keywords: 'kasa,punč,varené,víno,záloha,pohár,trhy,hody,burza,bufet,výdaj,objednávky,offline,tržba,škola,ples',
  },
  play: {
    locale: 'sk',
    title: 'Tapkasa: Pokladňa na stánok',
    shortXmas: 'Pokladňa na vianočné trhy a jarmok: zálohy na hrnčeky, čísla objednávok, offline',
    shortYear: 'Pokladňa na stánok, trh a festival: vratné zálohy, čísla objednávok, offline',
  },
  promoXmas: 'Vianočné trhy, jarmok alebo punč pri škole? Naťukajte menu a účtujte bez registrácie a internetu. Záloha na hrnček jedným ťuknutím, druhý telefón ukáže čísla objednávok.',
  promoYear: 'Predávate na trhu, jarmoku či festivale? Naťukajte menu a účtujte bez registrácie a internetu. Vratné zálohy jedným ťuknutím, druhý telefón ukáže čísla objednávok.',
  wn108: `• Vratné zálohy: záloha na hrnček alebo pohár ako položka, vrátenie jedným ťuknutím. Prehľad ukazuje zálohy vybrané a vrátené zvlášť.
• Limit bez prekvapenia: na denný limit bezplatnej verzie aplikácia upozorní vopred.
• Nemáte na stánku signál? Rozpracovaný účet dokončíte aj tak a raz dostanete rezervu 10 platieb navyše.`,
  wn109: `Opravy a vyladenie pred sezónou trhov.

Nové od 1.0.8:
• Vratné zálohy: záloha na hrnček alebo pohár ako položka, vrátenie jedným ťuknutím.
• Na denný limit bezplatnej verzie aplikácia upozorní vopred.
• Nemáte na stánku signál? Rozpracovaný účet dokončíte aj tak a raz dostanete rezervu 10 platieb navyše.`,
  desc: (store) => `Pokladňa na stánok, vianočné trhy, jarmok, festival aj spolkovú akciu. Naťukáte menu a o dve minúty predávate: bez registrácie, bez účtu a bez internetu.

Tapkasa predaj počíta a eviduje, platby nespracúva. Preto vám nič nezmrazí, nič neoveruje a neberie žiadne poplatky z platieb. Hotovosť ide do kasičky, karta cez váš vlastný terminál.

Druhý telefón ukáže rad objednávok s číslami a prečíta ich nahlas. Vratná záloha na hrnček alebo pohár je na jedno ťuknutie. Zadarmo 10 platieb denne, na celý trh si Tapkasu Pro vyskúšate 14 dní zadarmo.

PREDAJ NA TRI ŤUKNUTIA
• Každá položka je farebná karta. Obsluha ju spozná skôr, ako prečíta názov.
• Ťuknutím pridáte kus na účet, podržaním karty jeden kus zase uberiete.
• „+ Iná suma“ vyrieši čokoľvek mimo menu.
• Zle uložený účet vrátite jedným ťuknutím späť.

HOTOVOSŤ AJ KARTA
• Pri hotovosti naťukáte, koľko vám zákazník podal, a Tapkasa vypočíta, koľko vrátiť.
• Pri karte účtujete na svojom vlastnom termináli a v pokladni sumu iba potvrdíte.

VRATNÉ ZÁLOHY
• Záloha na hrnček na varené víno alebo na pohár je karta ako každá iná, vrátenie zálohy je karta so zápornou cenou.
• Vrátenie sa od účtu odpočíta. Účet len s vrátením sa nepočíta do denného limitu a v rade sa nepripravuje.
• V prehľade vidíte zvlášť zálohy vybrané a vrátené.

RAD OBJEDNÁVOK A VÝDAJ
• Zaplatený účet sa zaradí do radu ako objednávka s číslom.
• Druhý telefón alebo tablet prepnete do roly Výdaj: objednávky sa na ňom objavia samy, položky odškrtávate a „Vydané“ objednávku uzavrie.
• Výdaj vie nové objednávky čítať nahlas.
• Dva iPhony alebo dva telefóny s Androidom (13 a novším) sa prepoja aj bez internetu. iPhone s Androidom na prepojenie internet potrebuje.

PREHĽAD A UZÁVIERKA
• Tržba spolu, hotovosť a karta, predané kusy po položkách.
• Súhrn tržieb za zvolené obdobie ako PDF s vašimi údajmi a rozpisom DPH.
• Viac akcií vedľa seba, uzávierka akcie s archívom.
• 9 jazykov a 33 mien.

VAŠE DÁTA SÚ VAŠE
• Všetko zostáva vo vašom zariadení. Žiadne účty, žiadna analytika, žiadne reklamy.
• Zálohu dát uložíte zadarmo do súboru a kedykoľvek z nej pokladňu obnovíte, aj na novom telefóne.
• Výpadok signálu predaj nezastaví.

ZADARMO A PRO
Zadarmo: celá pokladňa na jednom zariadení, 10 zaplatených účtov denne. Na blížiaci sa limit aplikácia upozorní vopred. Keď práve nemáte signál, rozpracovaný účet dokončíte aj tak a raz dostanete rezervu 10 platieb navyše.
Tapkasa Pro (predplatné): neobmedzené účtovanie a prepojenie s druhým zariadením. Stánku stačí jedno predplatné, výdaj sa pripojí zadarmo. Nový predplatiteľ má 14 dní na vyskúšanie zadarmo. Predplatné sa účtuje cez ${store} a zrušíte ho kedykoľvek v nastaveniach účtu.

ČO TAPKASA NIE JE
• Nespracúva platby a nie je platobný terminál.
• Nie je registračná pokladnica (eKasa). Používajte ju tam, kde to predpisy dovoľujú: spolky, školské a farské akcie, dobročinné predaje, interná evidencia.
• Nevedie sklad ani účtovníctvo.

${LINKS}`,
};
