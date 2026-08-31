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

## Fáze 3, App Store Connect (2026-08-31, probíhá)

**Stav účtu, ověřeno**

- Tým: **deriverge s.r.o.**, Team ID `6XX9G3S468`.
- **Paid Apps Agreement: Active** (platnost 19. 8. 2026 až 19. 8. 2027).
- Bankovní účet ČSOB (1478), CZK: **Active**.
- Daňové formuláře W-8BEN a W-8BEN-E: **Active**.
- Smlouvy ani bankovní údaje jsme nevyplňovali, jen odečetli stav.

**Hotovo**

- **App ID zaregistrováno** v Apple Developer portálu: description
  `Tapkasa`, bundle `com.deriverge.tapkasa`, typ Explicit.
  Předtím na účtu existoval jen `cz.vztmonter.app`.
- **Aplikace založena** v App Store Connect:
  - název `Tapkasa - Pokladna do kapsy`,
  - platforma iOS, primární jazyk **čeština** (`cs`),
  - bundle `com.deriverge.tapkasa`, SKU `tapkasa-ios`,
  - **Apple ID aplikace `6807075649`**.
  - Poznámka: Apple vypsal hlášku, že nešlo uložit omezení přístupu
    uživatelů, takže aplikaci vidí všichni uživatelé účtu. Pro tento
    účet je to v pořádku, dá se změnit v App Information.
- **Subscription Group `Tapkasa Pro`** vytvořena, group ID `22348338`.
- **Předplatné `tapkasa.pro.monthly`** vytvořeno:
  - reference name `Tapkasa Pro Monthly`, Apple ID `6807076650`,
    perioda 1 měsíc,
  - **dostupnost: všech 175 zemí** (potvrzeno).
  - Volba všech zemí je záměrná. `monetization.md` chce trial ve všech
    zemích, zatímco omezení launche na CZ+SK podle `checklist.md` se
    nastavuje na úrovni aplikace (Pricing and Availability), ne produktu.
    Produkt tak nebude potřeba měnit při rozšíření do dalších zemí.

**Rozpracované, neuložené**

- Základní cena **4,99 USD** je vybraná a průvodce stojí otevřený na
  kroku „Price by Country or Region", kde se má Česku přepsat cena na
  **129 Kč**. Tento krok **není potvrzený**, cena tedy zatím uložená není.

**BLOKUJE: bezpečnostní klasifikátor zastavuje ovládání prohlížeče**

- Prostředí, ve kterém běžím, zablokovalo už dva kroky automatizace:
  1. odkrytí a přečtení **veřejných** SDK klíčů v RevenueCat,
  2. otevření nabídky cen u řádku Česko v App Store Connect.
- Druhý případ je úplně běžný krok formuláře, takže blokování není
  vázané na tajemství, ale na vzor „automatizované klikání v konzoli".
- Obcházet to nebudu. Bez uvolnění nejde dokončit ceny, lokalizace,
  trialy, App Privacy ani Google Play část.
- Uživatel byl požádán o rozhodnutí.

**Nedotčeno podle pravidel zadání**

- **DAC7** (Directive on Administrative Cooperation, 7th Amendment) hlásí
  v sekci Agreements „Missing Info". Je to daňový a reportovací formulář,
  ten podle pravidel nevyplňujeme. Uživatel ho musí doplnit sám,
  App Store Connect → Business → Agreements → Add Info.
- **Small Business Program**: přihlášení zatím neproběhlo, je to úkon
  v sekci Agreements. Zbývá udělat.

---

## Fáze 3b, App Store Connect, předplatná (2026-08-31)

Blok automatizace byl vyřešen. Uživatel přidal do `~/.claude/settings.json`
úzké pravidlo povolující jediný vstupní skript, přes který ovládám Chrome.

**Měsíční předplatné `tapkasa.pro.monthly`, Apple ID `6807076650`**

- Dostupnost: všech 175 zemí.
- Cena: **4,99 USD**, Česko **129,00 Kč**.
  Poznámka: automatický přepočet Applu vyšel přesně na 129 Kč, ruční
  úprava tedy nebyla potřeba. `monetization.md` očekával, že přepočet
  vyjde nehezky, aktuální kurzy to vyvrátily.
- Lokalizace:
  - Czech: „Tapkasa Pro, měsíční" / „Neomezené účtování a spárování
    druhého zařízení",
  - English (U.S.): „Tapkasa Pro Monthly" / „Unlimited sales and pairing
    a second device".
- **Introductory Offer**: Free, **2 weeks**, 175 zemí, od 1. 9. 2026,
  bez konce platnosti.
  Poznámka: Apple nedovolí začátek nabídky ke dnešnímu dni, nejbližší
  možný začátek byl 1. 9. 2026. Na spuštění to nemá vliv, aplikace bude
  vydaná později.

**Roční předplatné `tapkasa.pro.yearly`, Apple ID `6807087169`**

- Dostupnost: všech 175 zemí (varianta „1 Year Upfront").
- Cena: **39,99 USD**, Česko **999,00 Kč**.
  **Odchylka od zadání**: `monetization.md` chtěl 990 Kč. Apple takový
  price point nenabízí. Dostupné sousední body jsou 799 Kč a 999 Kč.
  Podle záložního pravidla v témže dokumentu („pokud 990 Kč není
  v nabídce, vzít 989 nebo 999 Kč, pořád pod hranicí 1 000 Kč") je
  nastaveno **999 Kč**. Proti 12 × 129 Kč = 1 548 Kč to je sleva 35 %.
- Lokalizace:
  - Czech: „Tapkasa Pro, roční",
  - English (U.S.): „Tapkasa Pro Yearly".
- Introductory Offer se nastavuje, výsledek doplním v dalším záznamu.

**Poznámka k variantě „Monthly with a 12-Month Commitment"**

- App Store Connect u ročního předplatného nově nabízí i tuto druhou
  variantu nákupu. Vědomě jsme ji nechali nenastavenou, v zadání není
  a vyžaduje OS 26.4+ a SDK 26.5+, což je mimo dosah současného buildu.

**Zbývá na App Store Connect**

- Review screenshot paywallu u obou předplatných (bez něj IAP uvíznou
  ve „Waiting for Review").
- Lokalizace subscription group „Tapkasa Pro" (display name).
- App Information: kategorie, age rating, content rights.
- App Privacy podle `store/apple-privacy-labels.md`.
- Pricing and Availability aplikace: Free, země CZ+SK.
- Verze 1.0: texty, screenshoty, klíčová slova, What's New, App Review
  Information, release option Manually release.
- Přihlášení do Small Business Programu.

---

## Fáze 4, Xcode (2026-08-31)

**Vyřešeno bez aktualizace macOS**

- Mac App Store nabízel jen verzi Xcode vyžadující novější systém, což
  uživatel dělat nechtěl kvůli stabilitě DaVinci Resolve.
- Řešením byla starší verze z developer.apple.com. Na disku se našel už
  stažený **Xcode 16.4**, přesunut z `~/Downloads` do `/Applications`.
- `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`
  spustil uživatel, licence byla přijata při prvním startu Xcode.
- Ověřeno: `xcodebuild -version` = **Xcode 16.4, build 16F6**,
  `xcode-select -p` = `/Applications/Xcode.app/Contents/Developer`.
- Balíček obsahuje `iPhoneOS.platform`, archiv na zařízení je tedy možný.
- Volitelné stahování (iOS 18.6 Simulator 8,86 GB, Predictive Code
  Completion Model 2,51 GB) uživatel na doporučení zrušil, pro archiv
  a TestFlight nejsou potřeba.

**Zbývá k iOS buildu**

- V Xcode → Settings → Accounts přihlásit Apple ID a vybrat tým
  deriverge s.r.o. (`6XX9G3S468`). Musí udělat uživatel.
- Nastavit v projektu `ITSAppUsesNonExemptEncryption = NO` a přidat
  `PrivacyInfo.xcprivacy`, doplnit veřejný RevenueCat klíč do
  `mobile/billing.js`.
- Archiv a nahrání do TestFlightu.

---

## Fáze 5, repozitář a iOS projekt (2026-08-31)

**Commitnuto a pushnuto do `main`**, commit `795b490`:

- `mobile/billing.js` a `mobile/www/billing.js`: doplněny **veřejné SDK
  klíče** projektu Tapkasa z RevenueCat. Jsou to public client keys,
  patří do klienta; žádný secret key se nikam nedával.
- `mobile/ios/App/App/Info.plist`: přidáno
  `ITSAppUsesNonExemptEncryption = NO`. Aplikace jede jen přes HTTPS,
  spadá pod výjimku, a odpadne dotaz na export compliance u každého
  nahrání buildu.
- `mobile/ios/App/App/PrivacyInfo.xcprivacy`: **nově vytvořený**
  privacy manifest podle `store/apple-privacy-labels.md`.
  `NSPrivacyTracking = false`, prázdné `NSPrivacyTrackingDomains`
  i `NSPrivacyCollectedDataTypes`, deklarován jen
  `NSPrivacyAccessedAPICategoryUserDefaults` s důvodem `CA92.1`.
- `mobile/ios/App/App.xcodeproj/project.pbxproj`: manifest přidán jako
  file reference i do Resources build phase, jinak by se do buildu
  vůbec nedostal.

**Zjištění**: ani `ITSAppUsesNonExemptEncryption`, ani privacy manifest
v repozitáři předtím nebyly, přestože je `store/checklist.md` fáze 2
bod 5 obojí vyžaduje. Doplněno.

Ověřeno, že projekt po zásahu do `project.pbxproj` stále načítá:
`xcodebuild -list -project App.xcodeproj` proběhlo a vyřešilo SPM
závislosti (capacitor-swift-pm 8.5.0, purchases-hybrid-common 18.32.1).

**Nezařazeno do commitu**

- `mobile/ios/App/App.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/`
  vzniklo při ověřování projektu. Je to `Package.resolved` se zámkem
  verzí SPM balíčků. Necháno neverzované, ať to není nevyžádaná změna;
  pro reprodukovatelnost buildu by dávalo smysl ho commitnout, ale to je
  rozhodnutí nad rámec zadání.

---
