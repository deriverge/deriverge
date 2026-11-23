// Nominace Tapkasy na featuring v App Storu (App Store Connect → Featuring → Nominations) přes API `nominations`.
//   node store/tool/asc-nomination.mjs            nanečisto: vypíše nominaci a existující nominace aplikace
//   node store/tool/asc-nomination.mjs --go       založí nominaci jako koncept, nebo koncept se stejným jménem upraví
//   … --submit --go                               koncept odešle Applu
// Odeslanou nominaci jde podle Applu dál upravit (datum, popis), jen ne typ a aplikace: --go ji upraví podle souboru.
// Pravidla Applu: nominovat nejméně 2 týdny a nejvýš 3 měsíce před datem zveřejnění. Popis jen pravdivý, bez čísel a ocenění.
// Datum zveřejnění = kdy už je v App Storu verze se vším, co popis slibuje (EET 2.0, daň a spropitné jsou od 1.2.0 / 1.1.0).
import { asc, ASC_APP, len } from './clients.mjs';
import { URLS } from '../meta/index.mjs';

const args = process.argv.slice(2);
const GO = args.includes('--go'), SUBMIT = args.includes('--submit');
const NOMINATION = {
  name: 'Tapkasa 1.2: EET 2.0 and holiday market tools',
  type: 'APP_ENHANCEMENTS',
  publishStartDate: '2026-12-14T08:00:00.000Z',
  publishEndDate: '2027-01-31T22:00:00.000Z',
  deviceFamilies: ['IPHONE', 'IPAD'],
  locales: ['cs', 'sk', 'de-DE', 'pl', 'en-GB', 'en-US'],
  territories: ['CZE', 'SVK', 'DEU', 'AUT', 'POL', 'GBR', 'USA'],
  supplementalMaterialsUris: [URLS.marketing],
  description: [
    'Tapkasa is a pocket cash register for market stalls, Christmas markets, festivals, school fairs and club events. Sellers type in their menu and start selling in about two minutes, with no account and no internet connection. The app never processes payments: stalls take cash or use their own card reader.',
    'What is new for the holiday season:',
    '- EET 2.0 for Czech sellers: the Czech electronic sales reporting starts on 1 January 2027. Tapkasa signs each sale on the phone and sends it; without signal, sales wait in a queue and go out on their own.',
    '- Refundable mug deposits for Christmas markets: deposit and return in one tap, kept apart from sales.',
    '- Numbered orders on a second phone: the counter reads new orders aloud. In the iPhone and iPad app the two devices can link without internet.',
    '- For US sellers: add sales tax at checkout and offer tips, both shown separately in the day summary.',
    'Tapkasa is made by a small independent developer in the Czech Republic and works in nine languages.',
  ].join('\n'),
  notes: 'EET 2.0 applies only to sellers in the Czech Republic and is off unless the seller turns it on. Deposits, the second-phone queue and the tax and tip options work in every supported region.',
};

const day = 86400000, start = Date.parse(NOMINATION.publishStartDate), now = Date.now();
// Lhůty platí pro odeslání; u už odeslané nominace (posun data, oprava popisu) se jen varuje.
const timing = start - now < 14 * day ? 'datum zveřejnění musí být nejméně 2 týdny dopředu' : start - now > 90 * day ? 'datum zveřejnění smí být nejvýš 3 měsíce dopředu' : '';
if (/[—–]/.test(NOMINATION.description + NOMINATION.notes)) throw new Error('dlouhá pomlčka v textu');
if (len(NOMINATION.description) > 4000) throw new Error(`popis má ${len(NOMINATION.description)} znaků`);

const api = await asc();
const call = async (method, p, body) => {
  if (method !== 'GET' && !GO) throw new Error('zápis bez --go: ' + method + ' ' + p);
  return api(method, p, body);
};
const log = (...a) => console.log(...a);
log(`Tapkasa → nominace na featuring | ${GO ? 'ZÁPIS (--go)' : 'nanečisto'}${SUBMIT ? ' | odeslat' : ''}`);
log(`${NOMINATION.type} „${NOMINATION.name}“, zveřejnění ${NOMINATION.publishStartDate.slice(0, 10)} až ${NOMINATION.publishEndDate.slice(0, 10)}, ${NOMINATION.territories.join(' ')}`);
log(`popis (${len(NOMINATION.description)} znaků):\n${NOMINATION.description}\npoznámka: ${NOMINATION.notes}`);

const existing = [];
for (const state of ['DRAFT', 'SUBMITTED']) existing.push(...(await call('GET', `/v1/nominations?filter[state]=${state}&filter[relatedApps]=${ASC_APP}&limit=50`)).data);
for (const n of existing) log(`  existující: ${n.id} ${n.attributes.state} ${n.attributes.type} „${n.attributes.name}“ ${String(n.attributes.publishStartDate).slice(0, 10)}`);
let nom = existing.find((n) => n.attributes.name === NOMINATION.name);
if (timing && nom?.attributes.state !== 'SUBMITTED') throw new Error(timing);
if (timing) log(`POZOR: ${timing}`);

const { territories, ...attrs } = NOMINATION;
const rel = {
  relatedApps: { data: [{ type: 'apps', id: ASC_APP }] },
  supportedTerritories: { data: territories.map((id) => ({ type: 'territories', id })) },
};
if (!GO) { log(`\nNanečisto: ${nom ? 'upravila by se nominace ' + nom.id + ' (' + nom.attributes.state + ')' : 'založil by se koncept'}${SUBMIT ? ' a odeslal' : ''}. Zápis: --go.`); process.exit(0); }
if (!nom) {
  nom = (await call('POST', '/v1/nominations', { data: { type: 'nominations', attributes: { ...attrs, submitted: false }, relationships: rel } })).data;
  log(`Koncept založen: ${nom.id}`);
} else {
  const sent = nom.attributes.state === 'SUBMITTED';
  const { type, ...rest } = attrs; // typ odeslané nominace měnit nejde
  // Apple chce u každé úpravy i `submitted` (nebo `archived`); koncept zůstane konceptem, dokud není --submit
  nom = (await call('PATCH', `/v1/nominations/${nom.id}`, { data: { type: 'nominations', id: nom.id, attributes: { ...(sent ? rest : attrs), submitted: sent || SUBMIT },
    relationships: { supportedTerritories: rel.supportedTerritories } } })).data;
  log(`Nominace ${nom.id} uložena, stav ${nom.attributes.state}${nom.attributes.submittedDate ? ", odesláno " + nom.attributes.submittedDate : ""}`);
}
if (SUBMIT && nom.attributes.state !== 'SUBMITTED') {
  nom = (await call('PATCH', `/v1/nominations/${nom.id}`, { data: { type: 'nominations', id: nom.id, attributes: { submitted: true } } })).data;
  log(`ODESLÁNO: ${nom.id}, stav ${nom.attributes.state}, ${nom.attributes.submittedDate || ''}`);
}
