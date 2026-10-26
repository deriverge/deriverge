# Tapkasa, pokladna do kapsy

Pokladna pro prodej na stánku, trhu nebo akci, barevné karty položek, platba
hotově či kartou, fronta objednávek, přehled tržby. Jeden soubor, žádný backend,
žádná registrace. Dřívější „Kasa na stánek“, rozšířená na produkt pro App Store
a Google Play (nativní obal je v `../mobile/`, podklady pro obchody v `../store/`).

Webová verze běží na `https://www.deriverge.com/tapkasa/`. Aktuální verze
aplikace: **1.0.6**.

## První spuštění

Nová instalace projde dvoukrokovým úvodem: výběr jazyka (9 jazyků: čeština,
slovenština, angličtina, němčina, francouzština, španělština, italština,
polština, portugalština) a měny (33 měn, každá s vlastními bankovkami pro
vracení a počtem desetinných míst). Druhý krok vysvětlí ovládání a nabídne
ukázkové menu, nebo prázdný start. Jazyk i měnu jde kdykoliv změnit v Menu;
existující instalace úvod nikdy neuvidí.

## Tarify

- **Zdarma**: všechno na jednom zařízení, 10 zaplacených účtů denně.
  Počítadlo je v prodejní liště; o půlnoci se nuluje.
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
   druhé, výslovné potvrzení.
3. **Objednávky**: zaplacený účet se zařadí do fronty s číslem; položky se
   odškrtávají, `Vydáno` uzavře. V hlavičce je pořád vidět počet čekajících.
4. **Přehled**: tržba, rozpad hotově/kartou, prodané kusy, účtenky,
   `Uzavřít akci` archivuje a vynuluje. `Souhrn tržeb (PDF)` sestaví souhrn
   za zvolené období (s údaji prodejce a rozpisem DPH; jde poslat e-mailem,
   sdílet, uložit nebo zkopírovat). Není to daňový doklad ani účtenka pro
   zákazníka, Tapkasa není fiskální pokladna.
5. **Menu**: role zařízení (Kasa/Výdej), název akce, položky (ceny podle
   měny, 14 barev nebo vlastní barva z kolečka), párování, jazyk, měna, záloha dat.

## Dvě zařízení

Role se přepíná v Menu: **Kasa** účtuje, **Výdej** jen odškrtává frontu.
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

`sw.js` (cache `kasa-v5`) cachuje jen sebe, ikony a přibalená písma; cizí
adresy pouští vždy na síť, párování nesmí dostávat odpovědi z cache. Navigace jde
network-first, offline z cache.

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
