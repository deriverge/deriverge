# Tapkasa, pokladna do kapsy

Pokladna pro prodej na stánku, trhu nebo akci, barevné karty položek, platba
hotově či kartou, fronta objednávek, přehled tržby. Jeden soubor, žádný backend,
žádná registrace. Dřívější „Kasa na stánek“, rozšířená na produkt pro App Store
a Google Play (nativní obal je v `../mobile/`, podklady pro obchody v `../store/`).

Webová verze běží na `https://www.deriverge.com/tapkasa/`.

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
  a párování více zařízení. Kód smí *vytvořit* jen Pro; *připojit se* ke kódu
  může kdokoliv, stánku stačí jedno předplatné.
- Instalace z doby před tarify (mají prodeje, archiv nebo párování) dostávají
  Pro trvale zdarma, nikomu nic nebereme.
- Nákup obstarává nativní most (`__kasaBuy`/`__kasaRestore`/`__kasaEntitlement`,
  ceníky `__KASA_PRICES__`, implementuje `../mobile/billing.js` přes
  RevenueCat). Na webu tlačítka jen odkáží do aplikace.
- Vývojářské odemčení: 7× klepnout na řádek verze v Menu (přepíná `pro-dev`).

## Jak se to ovládá

1. **Prodej**: klepnutím na kartu přidáte položku, podržením ji odeberete
   (karta při držení plní pruh). `+ Jiná částka` otevře klávesnici, u měn
   s haléři/centy se ťuká v setinách (125 → 1,25 €). Souhrn dole rozbalí účet.
2. **Zaplatit**: částka a dvě tlačítka. U *Hotově* naťukáte přijaté peníze
   (bankovky podle zvolené měny) a aplikace spočítá vrácení.
3. **Objednávky**: zaplacený účet se zařadí do fronty s číslem; položky se
   odškrtávají, `Vydáno` uzavře. V hlavičce je pořád vidět počet čekajících.
4. **Přehled**: tržba, rozpad hotově/kartou, prodané kusy, účtenky,
   `Uzavřít akci` archivuje a vynuluje. `Daňový doklad` sestaví souhrnný
   prodejní doklad za zvolené období (s údaji prodejce; jde poslat
   e-mailem, vytisknout nebo zkopírovat).
5. **Menu**: role zařízení (Kasa/Výdej), název akce, položky (ceny podle
   měny, 14 barev nebo vlastní barva z kolečka), párování, jazyk, měna, záloha dat.

## Dvě zařízení

Role se přepíná v Menu: **Kasa** účtuje, **Výdej** jen odškrtává frontu.
Objednávky se přenášejí:

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
a v nativní aplikaci `Documents/kasa.json` (vkládá se před start přes
`__KASA_BOOT__`). Migrace stavů zvládá všechny starší verze. Menu →
**Záloha dat** vypíše/načte celý stav jako text.

## Offline

`sw.js` (cache `kasa-v4`) cachuje jen sebe, ikony a písma; cizí adresy pouští
vždy na síť, párování nesmí dostávat odpovědi z cache. Navigace jde
network-first, offline z cache.

## Soubory

| Soubor | K čemu |
|---|---|
| `index.html` | celá aplikace (styly, markup, logika, všech 9 jazyků) |
| `sw.js` | service worker pro offline režim |
| `manifest.webmanifest` | instalace na plochu (ikony z `../design/`) |
| `icon-*.png`, `apple-touch-icon.png` | ikony aplikace |
| `privacy.html`, `terms.html` | zásady soukromí a podmínky (odkazuje na ně paywall) |

Blok mezi `<!-- APP:START -->` a `<!-- APP:END -->` je samostatně přenositelný.
