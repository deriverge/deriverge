# Tapkasa, nativní obal (Capacitor)

„Pokladna do kapsy.“ Tenhle adresář balí webovou pokladnu `kava/index.html`
do nativních aplikací pro App Store a Google Play pomocí
[Capacitoru](https://capacitorjs.com) 8.

```
mobile/
├── package.json           závislosti (@capacitor/* 8.5.0, purchases-capacitor 13.4.2)
├── capacitor.config.ts    appId com.deriverge.tapkasa, appName Tapkasa, webDir www
├── sync-web.sh            kopíruje kava/index.html → www/ a přidá adaptéry
├── bridge.js              JS adaptér nativního mostu (párování, ukládání)
├── billing.js             JS adaptér fakturace (RevenueCat)
├── www-bridge.md          jak hooky webu mapují na Capacitor, čti při změnách mostu
├── ios-plugin/            zdroj pravdy pro nativní iOS kód
│   ├── PeerLinkPlugin.swift        Multipeer plugin + úložiště kasa.json
│   └── TapkasaViewController.swift registrace pluginu, boot skript, vzhled webview
├── www/                   zbuildovaný web (generuje sync-web.sh, je v repu, ať projekt hned běží)
├── ios/                   vygenerovaný Xcode projekt (npx cap add ios)
└── android/               vygenerovaný Android Studio projekt (npx cap add android)
```

Pozor: **starý adresář `ios/` v kořeni repa je původní SwiftUI aplikace**
a s tímhle projektem nesouvisí; Capacitor projekt je `mobile/ios/`.

## Co potřebuješ

- Node.js 20+ a npm (na vývojovém stroji)
- **iOS:** Mac s Xcode 15+ (doporučeno 16+), účet v Apple Developer Programu.
  CocoaPods netřeba, Capacitor 8 používá Swift Package Manager.
- **Android:** Android Studio (Ladybug nebo novější) s Android SDK 35+,
  JDK 21 (bundlovaný v Android Studiu stačí).

## Základní smyčka

```sh
cd mobile
npm install          # jen poprvé / po změně závislostí
./sync-web.sh        # kava/index.html + bridge.js + billing.js → www/
npx cap sync         # www/ → ios/ i android/, aktualizace nativních pluginů
npx cap open ios     # otevře Xcode
npx cap open android # otevře Android Studio
```

`./sync-web.sh` spouštějte po **každé** změně `kava/index.html`, `bridge.js`
nebo `billing.js`; `npx cap sync` po každém `sync-web.sh` nebo `npm install`.
Zdrojový `kava/index.html` se nikdy nemění, adaptéry se vkládají jen do
kopie v `www/`.

## iOS

Projekt `mobile/ios/App/App.xcodeproj` je už připravený:

- `PeerLinkPlugin.swift` a `TapkasaViewController.swift` jsou přidané
  v targetu App (kopie z `ios-plugin/`; při změně upravte **obojí**, nebo po
  úpravě v `ios-plugin/` soubory znovu zkopírujte do `ios/App/App/`).
  Kdyby ses někdy rozhodl smazat `ios/` a vygenerovat ho znovu
  (`npx cap add ios`), tyhle dva soubory, úpravu storyboardu a klíče
  v Info.plist musíš přidat znovu, `ios-plugin/` je proto zdroj pravdy.
- `Main.storyboard` má scénu s `customClass="TapkasaViewController"`
  (registruje plugin a vkládá `__KASA_BOOT__`, viz `www-bridge.md`).
- `Info.plist` už obsahuje klíče nutné pro Multipeer Connectivity:
  - `NSLocalNetworkUsageDescription`, česká věta pro dialog oprávnění,
  - `NSBonjourServices`, `_kasa-order._tcp` a `_kasa-order._udp`
    (musí odpovídat service typu `kasa-order` v pluginu).

Podpis a vydání:

1. V Xcode: target **App** → Signing & Capabilities → vyber svůj tým;
   bundle id je `com.deriverge.tapkasa` (musí existovat v App Store
   Connect / Identifiers).
2. Pro nákupy přidejte capability **In-App Purchase** (StoreKit); RevenueCat
   nic dalšího v projektu nepotřebuje.
3. Product → Archive → Distribute App → App Store Connect.

První spuštění na zařízení se zeptá na přístup k místní síti, bez povolení
párování kasa↔výdej nefunguje. Simulátor Multipeer neumí pořádně; párování
testuj na dvou fyzických zařízeních.

## Android

Projekt `mobile/android/` je standardní Gradle projekt (applicationId
`com.deriverge.tapkasa`). Lokální párování na Androidu zatím není, viz
sekce Android ve `www-bridge.md`; aplikace funguje jako pokladna a přes
relay, jen bez Multipeeru.

Podpis a vydání (Play App Signing):

1. Vytvoř **upload keystore** (jednou, a dobře ho zálohuj):

   ```sh
   keytool -genkey -v -keystore tapkasa-upload.keystore \
     -alias tapkasa -keyalg RSA -keysize 2048 -validity 10000
   ```

2. V `android/` vytvořte `keystore.properties` (necommitovat!):

   ```
   storeFile=/absolutni/cesta/tapkasa-upload.keystore
   storePassword=…
   keyAlias=tapkasa
   keyPassword=…
   ```

   a v `android/app/build.gradle` na něj napoj `signingConfigs.release`
   + `buildTypes.release.signingConfig` (standardní postup z dokumentace
   Androidu „Sign your app“).
3. Sestav bundle: `cd android && ./gradlew bundleRelease` →
   `android/app/build/outputs/bundle/release/app-release.aab`.
4. V Play Console založ aplikaci, zapni **Play App Signing** (Google drží
   podpisový klíč, vy nahráváte AAB podepsaný upload klíčem) a nahrajte AAB.

## RevenueCat (Free / Pro)

Free = 10 plateb denně na jednom zařízení; Pro = 4,99 USD/měsíc nebo
39,99 USD/rok přes nativní in-app nákupy. RevenueCat obaluje StoreKit 2
i Play Billing, nativní plugin `@revenuecat/purchases-capacitor` je
nainstalovaný a `npx cap sync` ho registruje v obou projektech sám.

Nastavení:

1. V RevenueCat založ projekt Tapkasa s aplikacemi pro App Store
   (com.deriverge.tapkasa) a Play Store.
2. Založ **entitlement `pro`** a připoj k němu oba produkty
   (měsíční a roční předplatné); v nabídce (offering) použijte standardní
   balíčky `$rc_monthly` a `$rc_annual`.
3. Veřejné SDK klíče vložte do `billing.js`:
   - `REVENUECAT_API_KEY_IOS` = `[DOPLŇ: appl_… klíč z RevenueCat]`
   - `REVENUECAT_API_KEY_ANDROID` = `[DOPLŇ: goog_… klíč z RevenueCat]`
   Jsou to *veřejné* klíče (public SDK keys), smí být v klientu; tajný
   (secret) klíč do aplikace nikdy nepatří.
4. Po úpravě `billing.js` znovu `./sync-web.sh && npx cap sync`.

Web pak volá `window.TapkasaBilling.getEntitlement() / purchase('monthly'|'yearly') / restore()`;
v prohlížeči (mimo aplikaci) všechno vrací `'free'`.

## Co v tomhle prostředí NEBYLO možné ověřit

Poctivě: scaffold vznikal v Linuxovém kontejneru bez Xcode a bez Android
SDK. Ověřené vs. neověřené:

**Proběhlo a je ověřené:**

- `npm install`, nainstalováno a potvrzeno `npm ls`:
  @capacitor/core + cli + ios + android 8.5.0,
  @revenuecat/purchases-capacitor 13.4.2, typescript (dev).
- `npx cap add ios`, `npx cap add android`, `npx cap sync`, oba nativní
  projekty vygenerované, web assets zkopírované, RevenueCat plugin
  detekován pro obě platformy.
- `./sync-web.sh`, `www/` vytvořeno, adaptéry vložené před `</body>`.
- Syntaxe `bridge.js` a `billing.js` (`node --check`), validita Info.plist.

**Neproběhlo (není tu čím):**

- **Kompilace Swiftu.** `PeerLinkPlugin.swift` a `TapkasaViewController.swift`
  jsou psané proti reálným hlavičkám Capacitoru 8.5.0 z `node_modules`,
  ale nikdy neprošly kompilátorem, první otevření v Xcode může chtít
  drobné opravy.
- **Ruční úpravy Xcode projektu.** Přidání obou .swift souborů do
  `project.pbxproj`, změna třídy ve storyboardu a klíče v Info.plist se
  dělaly editací textu, ne Xcodem. Po otevření zkontrolujte, že oba soubory
  jsou v targetu App (File Inspector → Target Membership) a projekt se
  builduje; kdyby byl pbxproj rozbitý, soubory z `ios-plugin/` přetáhni
  do Xcode ručně a úpravy storyboardu/Info.plist zopakuj podle této
  dokumentace.
- **Android build** (`./gradlew`), podpisy, generování AAB.
- **RevenueCat za běhu**, mapování odpovědí v `billing.js` je psané
  defenzivně (bere `{customerInfo}` i nezabalený objekt), ale skutečný
  nákup/restore je potřeba projet v sandboxu obou obchodů.
- **Multipeer za běhu**, logika je 1:1 port ověřeného
  `ios/Kasa/PeerLink.swift`, ale chování (dialog místní sítě, spojení dvou
  zařízení) chce test na dvou fyzických iOS zařízeních.

## Podpora

Kontakt: [DOPLŇ: podpůrný e-mail] · Provozovatel: [DOPLŇ: název firmy/OSVČ]
