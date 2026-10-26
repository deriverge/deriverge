# Tapkasa, nativní obal (Capacitor)

„Pokladna do kapsy.“ Tenhle adresář balí webovou pokladnu `tapkasa/index.html`
do nativních aplikací pro App Store a Google Play pomocí
[Capacitoru](https://capacitorjs.com) 8. Aktuální verze: **1.0.6**
(Android versionCode 9).

```
mobile/
├── package.json           závislosti (@capacitor/* 8.5.0, purchases-capacitor 13.4.2)
├── capacitor.config.ts    appId com.deriverge.tapkasa, appName Tapkasa, webDir www
├── sync-web.sh            kopíruje tapkasa/index.html, písma a ikony do www/ a přidá adaptéry
├── bridge.js              JS adaptér nativního mostu (párování, ukládání, hlas, PDF, hodnocení)
├── billing.js             JS adaptér fakturace (RevenueCat, ceny a zkušební doba)
├── www-bridge.md          jak hooky webu mapují na Capacitor, čti při změnách mostu
├── ios-plugin/            zdroj pravdy pro nativní iOS kód
│   ├── PeerLinkPlugin.swift        Multipeer + úložiště kasa.json a kasa-archive.json
│   ├── DocSharePlugin.swift        PDF e-mailem, sdílením a do souborů
│   ├── RateAppPlugin.swift         systémová žádost o hodnocení
│   └── TapkasaViewController.swift registrace pluginů, boot skript, vzhled webview
├── www/                   zbuildovaný web (generuje sync-web.sh, je v repu, ať projekt hned běží)
├── ios/                   Xcode projekt (npx cap add ios)
└── android/               Android Studio projekt (npx cap add android)
    └── app/src/main/java/com/deriverge/tapkasa/
        ├── MainActivity.java       registrace pluginů, tlačítko Zpět
        ├── PeerLinkPlugin.java     Nearby Connections + úložiště kasa.json a kasa-archive.json
        ├── SpeakPlugin.java        čtení nahlas přes systémové TextToSpeech
        └── DocSharePlugin.java     PDF e-mailem, sdílením a do souborů
```

Pozor: **starý adresář `ios/` v kořeni repa je původní SwiftUI aplikace**
a s tímhle projektem nesouvisí; Capacitor projekt je `mobile/ios/`.

## Co potřebujete

- Node.js 20+ a npm
- **iOS:** Xcode 16+ a účet v Apple Developer Programu. CocoaPods netřeba,
  Capacitor 8 používá Swift Package Manager. Na Davidově Macu Xcode není,
  iOS se překládá v Xcode Cloud (push na main s cestami `mobile/` nebo `tapkasa/`).
- **Android:** Android SDK 35+ a JDK 21.

## Základní smyčka

```sh
cd mobile
npm install          # jen poprvé / po změně závislostí
./sync-web.sh        # tapkasa/index.html + fonts/ + bridge.js + billing.js → www/
npx cap sync         # www/ → ios/ i android/, aktualizace nativních pluginů
```

`./sync-web.sh` spouštějte po **každé** změně `tapkasa/index.html`, písem,
`bridge.js` nebo `billing.js`; `npx cap sync` po každém `sync-web.sh` nebo
`npm install`. Zdrojový `tapkasa/index.html` se nemění, adaptéry se vkládají
jen do kopie v `www/`.

## Ukládání dat

Stav kasy má tři nezávislé kopie: localStorage, IndexedDB a soubor
v kontejneru aplikace. Od 1.0.6 je archiv uzavřených akcí zvlášť
(`kasa-archive.json`, localStorage `kavakasa.v1.arch`, IndexedDB `archives`)
a zapisuje se jen při změně; hlavní stav (`kasa.json`) nese seznam id archivů.
Ukládání se odkládá o 400 ms, okamžitě se ukládá zaplacení, uzávěrka,
obnova zálohy a skrytí aplikace.

- **iOS:** `KasaStore` v `PeerLinkPlugin.swift` zapisuje atomicky, při startu
  oba soubory vloží `TapkasaViewController` jako `__KASA_BOOT__`
  a `__KASA_BOOT_ARCH__`.
- **Android:** `PeerLinkPlugin.save` zapisuje přes dočasný soubor
  a přejmenování, stránka soubory při startu čte synchronně přes
  `window.__kasaStore.read("main" | "archive")`.

Stav ze starší verze (archiv vložený v hlavním stavu) se převede sám; původní
text se jednou odloží do IndexedDB pod klíč `pre106`.

## iOS

Projekt `mobile/ios/App/App.xcodeproj`:

- Soubory z `ios-plugin/` jsou v targetu App jako kopie v `ios/App/App/`;
  při změně upravte **obojí**. Kdybyste `ios/` generovali znovu
  (`npx cap add ios`), soubory, úpravu storyboardu a klíče v Info.plist je
  potřeba přidat znovu, `ios-plugin/` je proto zdroj pravdy.
- `Main.storyboard` má scénu s `customClass="TapkasaViewController"`.
- `Info.plist` má klíče pro Multipeer Connectivity:
  `NSLocalNetworkUsageDescription` (lokalizovaná věta v `*.lproj/InfoPlist.strings`)
  a `NSBonjourServices` `_kasa-order._tcp` a `_kasa-order._udp`
  (musí odpovídat service typu `kasa-order` v pluginu).
- Verze: `MARKETING_VERSION` v `project.pbxproj`, Info.plist ji jen přebírá.

První spuštění se zeptá na přístup k místní síti, bez povolení párování bez
internetu nefunguje. Simulátor Multipeer neumí pořádně; testujte na dvou
fyzických zařízeních.

## Android

Projekt `mobile/android/` je standardní Gradle projekt (applicationId
`com.deriverge.tapkasa`, versionCode a versionName v `app/build.gradle`).

Párování bez internetu jde přes Google Nearby Connections (P2P_CLUSTER) na
Androidu 13 a novějším; stačí oprávnění Zařízení v okolí a Bluetooth
s `neverForLocation`, poloha se nepoužívá. Starší Android páruje jen přes
internetový přeposílač. iPhone s Androidem se bez internetu nespojí
(Multipeer a Nearby si nerozumí).

Sestavení:

```sh
cd android
./gradlew assembleDebug     # ladicí APK (WebView jde ladit přes chrome://inspect)
./gradlew bundleRelease     # AAB pro Google Play
```

Release AAB se podepisuje upload klíčem, který je mimo repo; Google drží
podpisový klíč (Play App Signing). Hesla a klíče do repa nepatří.

## RevenueCat (Free / Pro)

Free = 10 zaplacených účtů denně na jednom zařízení; Pro = neomezené účty
a vytvoření párovacího kódu, měsíční nebo roční předplatné přes nativní
nákupy. Ceny určuje obchod a paywall je bere z RevenueCat
(App Store 129 Kč / 999 Kč, Google Play 159,99 Kč / 1 199,99 Kč, v jiných
měnách podle obchodu). Zkušební dobu 14 dní ukáže paywall jen tomu, kdo na
ni má nárok (`trialOf` a `checkTrialOrIntroductoryPriceEligibility`
v `billing.js`).

- Entitlement `pro`, nabídka se standardními balíčky `$rc_monthly`
  a `$rc_annual`.
- Veřejné SDK klíče (`appl_…`, `goog_…`) jsou v `billing.js`; smí být
  v klientu. Tajný (secret) klíč do aplikace nikdy nepatří.
- Testovací nákupy jsou v RevenueCat vidět až po zapnutí přepínače
  Sandbox data.

Web volá `__kasaBuy`, `__kasaRestore`, výsledek přichází přes
`__kasaEntitlement`, ceny přes `__KASA_PRICES__`. V prohlížeči (mimo
aplikaci) tlačítka jen odkážou do aplikace.

## Testování

- **Web:** `tapkasa/` přes jakýkoli statický server; dvě zařízení jdou
  simulovat dvěma oddělenými profily prohlížeče a vlastním přeposílačem
  ze `server/` (`window.__KASA_RELAY__`).
- **Android:** ladicí build v emulátoru nebo na zařízení.
- **iOS:** build z Xcode Cloud přes TestFlight.

## Podpora

Kontakt: info@deriverge.com · Provozovatel: deriverge s.r.o.
