// Vlastní produktové stránky Tapkasy v App Store (custom product pages). Každá stránka má jedno locale, vlastní
// propagační text, snímky (store/shots/cpp-data.mjs) a klíčová slova, pro která se ukáže v hledání místo výchozí stránky.
//
// Klíčová slova: Apple dovolí přiřadit jen slova z pole klíčových slov POSLEDNÍ SCHVÁLENÉ verze (ne z názvu ani
// podtitulu). Níže jsou slova z pole verze 1.0.9 (store/meta/<jazyk>.mjs); každé slovo patří jen jedné stránce.
// `minVersion`: od které verze aplikace platí všechno, co stránka ukazuje a slibuje. Klíčová slova (= viditelnost
// v hledání) a odeslání ke kontrole skript pustí, až bude tato verze schválená.
// `cs`: Apple chce u každé vlastní stránky i lokalizaci v hlavním jazyce aplikace (čeština). U německých a americké
// stránky je to jen záloha bez klíčových slov (hledání ji nepoužije): 'default' = snímky a propagační text výchozí
// české stránky (vánoční trh), 'cs-spolky' = snímky a text české stránky pro spolky a školy (nejbližší téma).
export const CPP = [
  {
    key: 'de-weihnachtsmarkt',
    name: 'Weihnachtsmarkt mit Pfand',
    locale: 'de-DE',
    minVersion: '1.0.9', // Pfand od 1.0.8, osmimístný párovací kód a poctivý stav spojení od 1.0.9
    keywords: ['glühwein', 'punsch'],
    cs: 'default',
    promotionalText: 'Glühwein, Punsch und Tassenpfand: Menü eintippen und kassieren, ohne Konto und ohne Internet. Pfand mit einem Tipp, Bestellnummern auf dem zweiten Handy.',
  },
  {
    key: 'de-vereinsfest',
    name: 'Vereinsfest',
    locale: 'de-DE',
    minVersion: '1.0.9',
    keywords: ['vereinsfest', 'festkasse', 'basar'],
    cs: 'cs-spolky',
    promotionalText: 'Vereinsfest, Schulfest oder Basar: Ein Handy ist die Festkasse, das zweite die Ausgabe mit Bestellnummern. Rückgeld sofort, Übersicht am Abend, ohne Konto.',
  },
  {
    key: 'cs-spolky',
    name: 'Spolky a školní akce',
    locale: 'cs',
    minVersion: '1.0.9',
    keywords: ['spolek', 'školní', 'ples', 'akce'],
    promotionalText: 'Ples, jarmark nebo školní akce: jeden telefon účtuje, druhý vydává objednávky podle čísel. Vrácení spočítá sám, tržbu sečte na konci. Bez registrace.',
  },
  {
    key: 'us-bake-sale',
    name: 'Bake sale & school fundraiser',
    locale: 'en-US',
    minVersion: '1.1.0', // daň připočtená při placení a spropitné od 1.1.0
    keywords: ['fundraiser', 'concession', 'tally'],
    cs: 'cs-spolky',
    promotionalText: 'Bake sale, PTO fundraiser or church fair? Tap items, get the change, see your totals. Prices include tax, or add sales tax at checkout. Optional tips. No card processing.',
  },
];
