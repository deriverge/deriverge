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
