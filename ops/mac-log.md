# Log Mac session, vydání Tapkasy

Zapisuje session běžící na Macu. Nejnovější záznam nahoře v rámci fáze,
fáze chronologicky.

---

## Fáze 1, Preflight (2026-08-31)

**Hotovo**

- `git pull` na `main` proběhl, pracovní strom je čistý, podklady ve
  `store/` i `mobile/` jsou na místě (screenshoty pro App Store i Play
  dotažené posledním pullem).
- `node -v` = **v22.18.0**, `npm -v` = 10.9.3. Požadavek 18+ splněn.
- `cd mobile && npm ci` proběhlo bez chyb, `node_modules/` je nainstalované.
- `./sync-web.sh` proběhlo, `mobile/www/index.html` má 237 443 B a obsahuje
  vložené `bridge.js` a `billing.js`.
- `npx cap sync ios` proběhlo úspěšně. Capacitor 8 řeší závislosti přes
  Swift Package Manager, CocoaPods tedy potřeba nejsou. Nalezen plugin
  `@revenuecat/purchases-capacitor@13.4.2`, zapsán `Package.swift`,
  web zkopírován do `mobile/ios/App/App/public`.
- Google Chrome je na Macu nainstalovaný a běží.

**BLOKUJE: Xcode není na Macu nainstalovaný**

- `xcodebuild -version` končí chybou, `xcode-select -p` ukazuje na
  `/Library/Developer/CommandLineTools`. To jsou jen Command Line Tools,
  ne plné Xcode. V `/Applications` žádné `Xcode.app` není.
- Důsledek: **úkol 4 (archiv a nahrání do TestFlightu) nejde provést**,
  a to ani cestou `xcodebuild`, ani otevřením projektu v Xcode.
- Potřeba od uživatele: nainstalovat Xcode 15+ z Mac App Store a poté
  v Xcode → Settings → Accounts přihlásit vývojářský tým. Na disku je
  volných 55 GB, na instalaci to stačí, ale stahování je řádově hodiny.
- Ověření týmu v Xcode (Settings → Accounts) proto zatím nebylo možné
  provést, je součástí stejného bloku.

**Poznámka: Android build se přeskakuje**

- Android SDK na Macu není (`~/Library/Android/sdk` neexistuje,
  `ANDROID_HOME` je prázdná, `sdkmanager`, `adb` ani `gradle` nejsou
  v cestě) a chybí i Java runtime.
- Podle zadání se tedy Android build přeskakuje. Konzolová část Google
  Play (úkol 5) tím dotčená není a udělá se.

**Čeká na uživatele**

- Instalace Xcode (viz blok výše).
- Restart Chromu s ladicím portem. Chrome právě běží bez
  `--remote-debugging-port`, a ten se za běhu přidat nedá. Aby zůstalo
  zachované přihlášení do konzolí, je potřeba Chrome ukončit a nechat ho
  spustit znovu s laděním. Uživatel byl požádán v terminálu.

---

## Fáze 2, RevenueCat (2026-08-31)

**Hotovo**

- Založen projekt **Tapkasa**, project ID `b0f25a13`
  (`https://app.revenuecat.com/projects/b0f25a13`). Kategorie Business,
  platforma Capacitor.
- Úvodního průvodce jsme vědomě přeskočili. Nabízel entitlement
  „Tapkasa Pro" a produkt `lifetime` navíc, což neodpovídá
  `store/monetization.md`. Nic z průvodce se nevytvořilo, projekt byl
  po přeskočení prázdný a vše je nastavené ručně.
- **App Store konfigurace**: název `Tapkasa iOS`, bundle
  `com.deriverge.tapkasa`, RevenueCat App ID `app5d60b87dab`.
- **Play Store konfigurace**: název `Tapkasa Android`, package
  `com.deriverge.tapkasa`, RevenueCat App ID `app0dee10a745`.
- **Entitlement** `pro`, display name „Tapkasa Pro", vytvořen.
- Apple klíče se **negenerovaly nové**. RevenueCat nabídl volbu
  „Select existing key" a připojily se stávající týmové klíče z účtu:
  - In-App Purchase key ID `4Z82Q5CHUN`,
  - App Store Connect API key ID `MTMP9A7SKR`,
  - Issuer ID `1ed9b87d-51a7-41b4-ab9d-c1b5e88a87fc`.
  Obojí jsou týmové klíče Apple, sdílení mezi aplikacemi je v pořádku.
  Žádný soubor `.p8` se nestahoval ani neukládal na disk.

**Zjištění k pořadí kroků**

- Zadání předpokládá RevenueCat jako první, ale formulář App Store
  konfigurace **nejde uložit bez In-App Purchase klíče**. Pořadí je tedy
  fakticky svázané s Apple stranou. Vyřešilo se použitím existujícího
  klíče, takže se nic nezdrželo.

**Čeká, nedokončené části RevenueCat**

- **Products** `tapkasa.pro.monthly` a `tapkasa.pro.yearly` zatím
  neexistují. Musí se nejdřív vytvořit v App Store Connect a Play
  Console, pak se do RevenueCat importují a připojí k entitlementu `pro`.
- **Offering** `default` s balíčky `$rc_monthly` a `$rc_annual` se
  nastaví až po importu produktů.
- **Service account JSON pro Google Play** není nahraný. Konfigurace
  Play aplikace šla uložit i bez něj, ale pro validaci transakcí je
  potřeba. Vyžaduje Google Cloud service account s rolí Android
  Publisher (viz `store/monetization.md`, sekce 1, bod 8).
- **Server notifications** (Apple V2, Google RTDN) zatím nenastavené.

**BLOKUJE: čtení veřejných SDK klíčů**

- Veřejné SDK klíče (`appl_...`, `goog_...`) jsou na stránce API keys
  maskované. Pokus o jejich odkrytí a přečtení zablokoval bezpečnostní
  klasifikátor prostředí, ve kterém běžím.
- Bez nich nejde dokončit bod zadání „klíče vložte do `mobile/billing.js`
  a commitněte do `main`".
- Jde o **veřejné** klienta klíče, ne o tajemství. Uživatel byl požádán,
  aby je buď předal, nebo akci povolil.

---
