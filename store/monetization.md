# Monetizace, Tapkasa Pro (konkrétní nastavení)

## Model (závazné parametry)

| | Free | Tapkasa Pro |
|---|---|---|
| Cena | zdarma | **$4.99/měsíc** nebo **$39.99/rok** |
| Zaplacené účty | **10 za kalendářní den** | neomezeně |
| Zařízení | jedno (párování zamčené) | párování kasa↔výdej odemčené |
| Vše ostatní (karty, fronta, přehled, archiv, záloha, offline) | ✓ | ✓ |

Nákup jde výhradně přes nativní in-app purchases (StoreKit 2 / Play
Billing), obojí zabalené přes **RevenueCat**. Žádná vlastní platební brána.

## Identifikátory (použít přesně takto, po vytvoření už nejdou změnit)

| Věc | Hodnota |
|---|---|
| RevenueCat entitlement | `pro` |
| Produkt měsíční (App Store i Play) | `tapkasa.pro.monthly` |
| Produkt roční (App Store i Play) | `tapkasa.pro.yearly` |
| Subscription group (Apple) | `Tapkasa Pro` |
| Play base plan id (měsíční / roční) | `monthly` / `yearly` |
| Play offer id (trial) | `trial14` |
| RevenueCat offering | `default` (balíčky `$rc_monthly`, `$rc_annual`) |

## Úvodní nabídka: 14 dní zdarma

Doporučení: **free trial 14 dní na obou produktech**. Důvody: prodejce
potřebuje trial přes celý víkend akce (7 dní by končilo uprostřed druhé
akce); 14 dní je standard, který Apple i Google podporují nativně a
RevenueCat ho zobrazí v paywallu automaticky. Trial je na Apple jednou na
subscription group (ne na produkt), na Play jednou na uživatele a produkt.

---

## 1) RevenueCat, postup

1. Založit účet na app.revenuecat.com → **Create project** „Tapkasa".
2. **Project settings → Apps**: přidat
   - *App Store* app: bundle ID `[DOPLŇ: reverse-DNS, např. com.firma.tapkasa]`,
   - *Play Store* app: package name (tentýž identifikátor).
3. Vygenerují se **public SDK keys** (jeden pro iOS, jeden pro Android), ty patří do klienta; secret keys nikam do aplikace nedávat.
4. **Entitlements**: nový entitlement, identifier přesně **`pro`**.
5. **Products**: po vytvoření produktů v obou konzolích (kroky 2 a 3 níže)
   je importovat/přidat: `tapkasa.pro.monthly` a `tapkasa.pro.yearly`
   z obou obchodů, a všechny čtyři připojit k entitlementu `pro`.
6. **Offerings**: offering `default`, balíčky `$rc_monthly` →
   `tapkasa.pro.monthly`, `$rc_annual` → `tapkasa.pro.yearly`. Označit
   `default` jako current.
7. **Apple credentials**: App Store Connect → Users and Access →
   Integrations → **In-App Purchase key** vygenerovat (.p8) a nahrát do
   RevenueCat (App settings → App Store Connect API). Přidat i App-Specific
   Shared Secret (fallback pro receipts).
8. **Google credentials**: Google Cloud service account s rolí
   „Pub/Sub + Android Publisher", JSON klíč nahrát do RevenueCat; v Play
   Console → Users and permissions dát service accountu přístup
   „View financial data" + „Manage orders and subscriptions".
9. **Server notifications**: zapnout App Store Server Notifications V2
   (URL z RevenueCat vložit do App Store Connect → App Information) a
   Google Real-time developer notifications (Pub/Sub topic z RevenueCat
   do Play Console → Monetization setup).
10. V aplikaci: `Purchases.configure(apiKey:)` s platform-specific public
    key, **anonymní App User ID nechat generovat SDK** (žádné vlastní ID, viz privacy štítky), gating: `customerInfo.entitlements["pro"].isActive`.

## 2) App Store Connect, postup

1. **Agreements, Tax, and Banking**: podepsat Paid Applications Agreement,
   vyplnit bankovní účet a daňové formuláře (bez toho IAP nejde ani testovat
   v review). `[DOPLŇ: bankovní a daňové údaje provozovatele]`
2. **Small Business Program, přihlásit se!** Snižuje provizi z 30 % na
   **15 %** pro vývojáře s příjmy do 1 M USD/rok. Není automatický:
   App Store Connect → Agreements → App Store Small Business Program →
   Enroll (schválení trvá pár dní; přihlásit před launchem, sazba se
   nepřiznává zpětně). Pozn.: u auto-renewable předplatných Apple po
   1 roce nepřetržitého předplatného snižuje provizi na 15 % i mimo
   program, s programem je 15 % od první platby.
3. **My Apps → Tapkasa → Monetization → Subscriptions**: vytvořit
   Subscription Group „Tapkasa Pro", v ní:
   - `tapkasa.pro.monthly`, duration 1 month, cena **$4.99** (Price
     Tier/Price Point 4.99 USD),
   - `tapkasa.pro.yearly`, duration 1 year, cena **$39.99**.
4. **Ceny pro Česko ručně**: automatický přepočet z USD vychází nehezky
   (149 Kč / 1 190 Kč apod.). V price scheduleru dát Czechia custom price:
   **129 Kč/měsíc** a **990 Kč/rok** (zvolit nejbližší dostupný price
   point; pokud 990 Kč není v nabídce, vzít 989 Kč nebo 999 Kč, pořád
   pod psychologickou hranicí 1 000 Kč). Roční cena 990 Kč = ~64 % slevy
   proti 12×129 Kč, to je hlavní prodejní argument paywallu.
5. **Introductory Offer** na obou produktech: type **Free trial**,
   duration **2 weeks**, všechny země, bez konce platnosti.
6. Ke každému předplatnému: localized display name
   (CS: „Tapkasa Pro, měsíční" / „Tapkasa Pro, roční",
   EN: „Tapkasa Pro Monthly" / „Tapkasa Pro Yearly"), description, a
   **review screenshot paywallu** (bez něj IAP visí ve „Waiting for
   Review").
7. První odeslání: IAP produkty přiložit k verzi 1.0 (checkbox na stránce
   verze), jinak je review neschválí spolu s aplikací.
8. **Sandbox tester** (Users and Access → Sandbox) na otestování nákupu,
   trialu (v sandboxu zrychlený) i obnovy.

## 3) Google Play Console, postup

1. **Payments profile**: Play Console → Setup → Payments profile, založit
   a propojit. `[DOPLŇ: fakturační údaje provozovatele]`
2. **Poznámka k provizi**: u **předplatných účtuje Google 15 % od první
   koruny automaticky** (od ledna 2022, bez přihlašování). Program
   „15 % na první 1 M USD/rok" se týká ostatních nákupů v aplikaci, pro čistě předplatitelský model Tapkasy není potřeba nic aktivovat,
   ale přihlášení v Play Console → Monetization setup ničemu nevadí a
   pokryje případné budoucí jednorázové produkty.
3. **Monetize → Products → Subscriptions**: vytvořit dvě předplatná:
   - product id `tapkasa.pro.monthly` → base plan `monthly`
     (auto-renewing, 1 month), cena **$4.99**;
   - product id `tapkasa.pro.yearly` → base plan `yearly`
     (auto-renewing, 1 year), cena **$39.99**.
4. **Ceny pro Česko**: Play dovoluje libovolné částky, nastavit u CZ
   přesně **129 Kč** a **990 Kč** (Set prices → upravit řádek Czechia;
   ceny jsou včetně DPH, Google ji odvádí).
5. **Offer** na každém base planu: offer id `trial14`, eligibility
   „New customer acquisition, never had this subscription", phase 1 =
   **Free trial, 14 days**.
6. Vše **Activate** (produkty, base plany i offery, neaktivní se v SDK
   nevrátí).
7. **License testing** (Play Console → Settings → License testing): přidat
   testerské účty, nákupy jsou zdarma a rychle se obnovují.
8. Produkty jsou dostupné až poté, co je aspoň jeden build s Billing
   permission nahraný na jakoukoli track (stačí internal testing).

## 4) Chování v aplikaci (gating, specifikace pro implementaci)

- Free limit: počítat **zaplacené účty** (uložené prodeje) za kalendářní
  den lokálního času; 11. pokus o `Zaplatit` otevře paywall místo výběru
  platby. Undo vrácené platby limit vrací (počítá se aktuální stav dne).
- Párování: sekce v Menu viditelná; **Vytvořit kód** otevře paywall,
  dokud není `pro` aktivní. **Připojit se** ke kódu zůstává zdarma, platí jen zařízení, které kód vytváří, stánku stačí jedno předplatné
  (napsáno i na paywallu a v Menu).
- Paywall: oba balíčky z offeringu `default`, zvýrazněný roční,
  **Restore purchases**, odkazy na Privacy Policy a Terms
  (Apple guideline 3.1.2 je vyžaduje), tohle všechno appka už má.
  Po zapnutí trialu v konzolích doplnit i řádek o trialu.
- Ztráta entitlementu (expirace) nesmí nic smazat, jen se vrátí limit
  a zamkne párování. Data uživatele zůstávají nedotčená.
- Offline: entitlement cache RevenueCat SDK platí i bez signálu; při
  nedostupnosti sítě nechat poslední známý stav (prodej na akci nesmí
  zablokovat výpadek internetu).

## 5) Kontrola konzistence

Ceny a limity v tomto souboru = zdroj pravdy. Musí sedět s:
`store/listing-cs.md` / `listing-en.md` (popis Free/Pro),
`store/review-notes.md` (IAP gating pro recenzi),
`store/checklist.md` (kroky před odesláním).
