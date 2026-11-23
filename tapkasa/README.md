# Tapkasa, pokladna do kapsy

Pokladna pro prodej na stánku, trhu nebo akci, barevné karty položek, platba
hotově či kartou, fronta objednávek, přehled tržby. Jeden soubor, žádný backend,
žádná registrace. Dřívější „Kasa na stánek“, rozšířená na produkt pro App Store
a Google Play (nativní obal je v `../mobile/`, podklady pro obchody v `../store/`).

Webová verze běží na `https://www.deriverge.com/tapkasa/`. Aktuální verze
aplikace: **1.2.0**.

## První spuštění

Nová instalace projde dvoukrokovým úvodem: výběr jazyka (9 jazyků: čeština,
slovenština, angličtina, němčina, francouzština, španělština, italština,
polština, portugalština) a měny (33 měn, každá s vlastními bankovkami pro
vracení a počtem desetinných míst). Druhý krok vysvětlí ovládání a nabídne
ukázkové menu (kavárna), ukázkové menu z vánočního trhu (svařák, punč,
trdelník nebo místní obdoba, horká čokoláda, klobása, záloha na hrnek a její
vrácení; názvy podle jazyka, ceny podle měny), nebo prázdný start. U dolaru
(USD, CAD) nabídne jednou větou daň připočtenou při placení, výchozí zůstává
cena včetně daně. Jazyk i měnu jde kdykoliv změnit v Menu; existující
instalace úvod nikdy neuvidí.

## Tarify

- **Zdarma**: všechno na jednom zařízení, 10 zaplacených účtů denně.
  Počítadlo je v prodejní liště; o půlnoci se nuluje. Po vyčerpání jde
  rozpracovaný účet dokončit: se signálem jednou denně tento jeden účet,
  bez signálu (nebo když nákup selže) poprvé s rezervou +10 plateb na ten
  den (jednou za instalaci), potom jeden účet denně.
- **Tapkasa Pro** (předplatné přes App Store / Google Play): neomezené platby
  a párování více zařízení. Kód smí *vytvořit* jen Pro; *připojit se* může
  zařízení zdarma, objednávky ale začne brát až po pozdravu od zařízení s Pro
  (platí 30 dní, každý další pozdrav ho prodlouží). Stánku tak stačí jedno
  předplatné a dvě zařízení zdarma se spolu nespárují.
- Paywall ukazuje 14denní zkušební dobu jen tomu, kdo na ni má nárok
  (z RevenueCat, viz `../mobile/billing.js`).
- Instalace z doby před tarify (mají prodeje, archiv nebo párování) dostávají
  Pro trvale zdarma, nikomu nic nebereme.
- Nákup obstarává nativní most (`__kasaBuy`/`__kasaRestore`/`__kasaEntitlement`,
  ceníky `__KASA_PRICES__`, implementuje `../mobile/billing.js` přes
  RevenueCat). Na webu tlačítka jen odkáží do aplikace.

## Jak se to ovládá

1. **Prodej**: klepnutím na kartu přidáte kus, podržením jeden kus uberete
   (karta při držení plní pruh). `+ Jiná částka` otevře klávesnici, u měn
   s haléři/centy se ťuká v setinách (125 → 1,25 €). Souhrn dole rozbalí účet.
2. **Zaplatit**: částka a dvě tlačítka. U *Hotově* naťukáte přijaté peníze
   (bankovky podle zvolené měny) a aplikace spočítá vrácení; nedoplatek chce
   druhé, výslovné potvrzení. Částka k vrácení zůstane i v hlášce po zaplacení.
   S připočtenou daní ukáže účet i okno placení mezisoučet, daň a celkem.
   Se zapnutým spropitným nabídne Bez spropitného, 10, 15, 20 % (s částkou)
   a Jinou částku; počítá se z ceny zboží bez připočtené daně a bez záloh
   (americká etiketa radí z částky před daní) a u hotovosti se přičte
   k částce k zaplacení i k výpočtu vrácení.
3. **Objednávky**: zaplacený účet se zařadí do fronty s číslem; položky se
   odškrtávají, `Vydáno` uzavře, od dvou čekajících jde `Vydat vše`. V hlavičce
   je pořád vidět počet čekajících. Kdo vydává zboží hned při placení, frontu
   v Menu vypne (jen kasa bez spárovaného výdeje) a účty se ukládají rovnou
   jako vydané.
4. **Přehled**: tržba, rozpad hotově/kartou, prodané kusy, účtenky (posledních
   100, starší na tlačítko; z jiného dne s datem), `Uzavřít akci` archivuje
   a vynuluje. `Souhrn tržeb (PDF)` sestaví souhrn
   za zvolené období (s údaji prodejce a rozpisem DPH; jde poslat e-mailem,
   sdílet, uložit nebo zkopírovat). Není to daňový doklad ani účtenka pro
   zákazníka, Tapkasa není fiskální pokladna. Tržba je zboží včetně daně;
   připočtená daň a spropitné (mimo tržbu, hotově a kartou zvlášť) mají
   v přehledu, textu souhrnu, PDF i v uzavřené akci vlastní řádek.
5. **Menu**: na kase nejdřív název akce a položky (ceny podle měny, nová
   položka dostane první volnou ze 14 barev, nebo vlastní barva z kolečka;
   Enter vede z názvu na cenu a na další řádek), pak fronta, údaje prodejce,
   daň, spropitné, role zařízení (Kasa/Výdej) s párováním a hlasem, jazyk,
   měna, záloha dat. Daň: „Ceny zahrnují daň“ (výchozí; plátce DPH zadává
   sazby u položek a souhrn rozpočítá základ a daň), nebo „Daň se připočte
   při placení“ s jednou sazbou na zařízení (až tři desetinná místa); u položky
   jde daň vypnout tlačítkem vedle ceny, vratné zálohy se nedaní, dokud je
   někdo nezapne. Daň se počítá z celého účtu a zaokrouhluje jednou na
   desetinná místa měny, polovina nahoru. Spropitné je výchozí vypnuté.
   Ukázkové menu z vánočního trhu jde nahrát i tady.
   Poděkování nahlas na kase a čtení objednávek na výdeji mají každé vlastní
   přepínač; poděkování je u nové instalace vypnuté.

Angličtina s dolarem dostane americké výrazy (Register, sales tax, color,
ZIP code, booth); jinak platí britský slovník. Čas se píše podle jazyka
zařízení (v USA „4:27 PM“).

## Dvě zařízení

Role se přepíná v Menu: **Kasa** účtuje, **Výdej** jen odškrtává frontu.
Se spárovaným druhým zařízením má role v hlavičce tečku: zelená, když se
protějšek ozývá, červená, když objednávky teď nikam nedojdou.
Když se výdej přepne zpátky na kasu, účtenky cizí kasy se odloží stranou
(`state.held`) a do tržby se nepočítají; při návratu na výdej se vrátí do fronty.

Párovací kód (od 1.0.6) má 8 znaků s kontrolním znakem, zobrazuje se jako
`ABCD-EFGH`. Z kódu se přes PBKDF2 odvodí klíč AES-GCM, název tématu
přeposílače (`tk2-…`) a jméno pro nativní hledání (`T2…`), takže přeposílač
ani zařízení v okolí kód nevidí a obsah nepřečtou. Připojit jde jen ke kódu
stejného tvaru. Starší kódy (5 znaků) fungují dál po staru, bez šifrování;
starší verze aplikace se s novým kódem nespojí a aplikace radí aktualizovat
druhé zařízení. Kopii menu a údajů prodejce musí odesílající zařízení
potvrdit. Objednávky se přenášejí:

- **na webu** delta-protokolem přes dvojici veřejných ntfy přeposílačů
  (`ntfy.sh` + `ntfy.envs.net`; posílá se na oba, poslouchá na obou, duplicity
  se zahazují podle id). SSE s adaptivním dopolováním, prezenční „hello“,
  poctivý stav spojení a vestavěný test přeposílače v Menu. Vlastní server
  je v `../server/`, nasazený se zapne přes `window.__KASA_RELAY__`
  (čárkami oddělený seznam základních adres).
- **v nativní aplikaci** navíc Multipeer Connectivity napřímo, bez internetu
  (`../mobile/ios-plugin/`).

Sloučení podle `id` a novějšího `updatedAt`, na pořadí zpráv nezáleží,
výpadek se dorovná. Výdej má díky tomu kopii prodejů (záloha mimo iPad).

Od 1.1.0 nese účtenka volitelná pole `tax`, `taxRate`, `taxBase` (připočtená
daň) a `tip` (spropitné), řádek `tx` (0 bez daně, 1 s daní); převzetí menu
nese `taxAdd`, `taxRate`, `tips` a `tx` u položek. Starší verze je ignorují
a `total` (zboží s daní, bez spropitného) jim sedí; když účtenku po
odškrtnutí vrátí, kasa o daň ani spropitné nepřijde, a od starší verze
převzaté menu nechá vlastní nastavení daně a spropitného.

## EET 2.0 (Česko, od 1.2.0)

Evidence tržeb podle zákona č. 180/2026 Sb. Jen u měny CZK a jen na kase;
jinde se nic nezobrazuje a bez zapnutí se nic neposílá. V Menu jde EET
zapnout, nebo zvolit „EET se mě netýká“ (krátký přehled výjimek a odkaz na
eet.gov.cz). Průvodce vede přes DIS+ (MOJE daně): evidenční jednotka,
pokladní certifikát `.p12` s heslem, označení pokladny (výchozí `TK-xxxx`,
každé účtující zařízení jiné), mezní doba odezvy 2, 5 nebo 10 s.
Testovací certifikát (vydavatel „playground“) posílá do testovacího
prostředí, ostrý do produkčního.

- **Podpis v telefonu, bez serveru.** Formát podle „Popisu datového
  rozhraní“ v1.2 a XSD 4.1: SOAP 1.1, WS-Security, exc-c14n, SHA-256,
  RSA-SHA256 (WebCrypto). `.p12` od CA EET je ve starém tvaru (klíč
  3DES, certifikáty RC2-40, MAC HMAC-SHA1); čte ho vlastní kód v `EETX`
  (DER, SHA-1, PKCS#12 KDF, DES, RC2, PBES2 přes WebCrypto). Služba EET
  povoluje CORS, posílá se přímo z WebView.
- **Klíč** je v IndexedDB `tapkasa-eet` jako neexportovatelný CryptoKey,
  vedle něj zašifrovaný `.p12` (i v localStorage `tapkasa.eet.p12`) pro
  odemčení heslem, kdyby klíč zmizel. Heslo se neukládá; stav ani záloha
  dat klíč nenesou (jen veřejný certifikát).
- **Fronta** `state.eet.q`: každý zaplacený účet dostane záznam s vlastním
  pořadovým číslem zařízení, časem a částkou (zboží, připočtená daň
  i spropitné; vratná záloha je v tržbě, její vrácení je záporná tržba;
  účet za nulu jde jako dvě zprávy). Data se už nemění, opakované zaslání
  má novou hlavičku (`prvni_zaslani=false`). Odesílá se hned, pak
  s prodlevou 15 s až 5 min, hned po startu, po návratu do popředí
  a po návratu signálu. Potvrzené (POK) jdou do `state.eet.log` (posledních
  400). Hlavička ukazuje počet neodeslaných, Přehled odeslané a čekající,
  účtenka svůj stav a POK. Upozornění po 36 a 48 hodinách.
- **Storno**: vrácení účtu k úpravě, smazání účtenky nebo objednávky
  a smazání účtu z druhého zařízení pošle zápornou tržbu s časem vrácení.
  Účet nese značku `eet` (pořadové číslo); párovací zprávy ji nenesou.
- **Dvě zařízení**: výdej nic neodesílá, nastavení EET se nekopíruje.
  Obnova zálohy na telefonu s EET nechá jeho nastavení a převezme
  neodeslané tržby; na telefonu bez EET převezme nastavení a chce znovu
  nahrát `.p12`.
- **Certifikát** platí 366 dní; 30 dní předem upozornění, od 14 dní
  v liště. Obnova přes rozhraní CA EET (`caeetapi_jwt.yml`, JWT RS256)
  s potvrzením převzetí až po uložení nového klíče; když nevyjde
  (CORS, síť), návod na ruční vydání v DIS+.

## Data

Tři nezávislé kopie: `localStorage` (`kavakasa.v1`), IndexedDB (`kavakasa`)
a v nativní aplikaci soubor `kasa.json` (iOS ho vkládá před start přes
`__KASA_BOOT__`, Android ho stránka čte přes `__kasaStore`). Archiv
uzavřených akcí má od 1.0.6 vlastní kopii (`kavakasa.v1.arch`, IndexedDB
`archives`, `kasa-archive.json`) a zapisuje se jen při změně; hlavní stav
nese `archIds`. Ukládání se odkládá o 400 ms, zaplacení, uzávěrka, obnova
zálohy a skrytí aplikace se ukládají hned. Migrace stavů zvládá všechny
starší verze, stav z 1.0.5 se navíc jednou odloží do IndexedDB (`pre106`).
Menu → **Záloha dat** vypíše/načte celý stav jako text nebo soubor.

## Offline

`sw.js` (cache `kasa-v6`) cachuje jen sebe, ikony a přibalená písma; cizí
adresy pouští vždy na síť, párování nesmí dostávat odpovědi z cache. Navigace jde
network-first, offline z cache; do cache se ukládá jen aplikace sama, úvodní stránky
ve stejné složce (`pokladna.html`, `pos.html`, `de/` …) jdou rovnou na síť.

## Soubory

| Soubor | K čemu |
|---|---|
| `index.html` | celá aplikace (styly, markup, logika, všech 9 jazyků) |
| `sw.js` | service worker pro offline režim |
| `manifest.webmanifest` | instalace na plochu (ikony z `../design/`) |
| `icon-*.png`, `apple-touch-icon.png` | ikony aplikace |
| `fonts/` | písma Archivo a JetBrains Mono (woff2) s licencemi SIL OFL 1.1; Google Fonts se nepoužívají |
| `privacy.html`, `terms.html` | zásady soukromí a podmínky (odkazuje na ně paywall) |

Blok mezi `<!-- APP:START -->` a `<!-- APP:END -->` je samostatně přenositelný.
