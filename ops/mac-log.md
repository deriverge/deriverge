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

## Fáze 6, RevenueCat katalog (2026-08-31)

**Hotovo**

- **Produkty importovány** z App Store Connect do konfigurace
  `Tapkasa iOS` (`app5d60b87dab`): `tapkasa.pro.monthly`
  a `tapkasa.pro.yearly`. Stav u obou je „Missing Metadata", což je
  normální, dokud aplikace neprojde review.
- **Entitlement `pro`**: připojeny **oba produkty** (v přehledu
  „2 products").
- **Offering `default`** vytvořen, display name
  „The standard set of packages", REST ID `ofrnga3369cd6e7`.
  Obsahuje balíček **`$rc_monthly` → `tapkasa.pro.monthly`**.

**BLOKUJE: balíček `$rc_annual` se nepodařilo přidat**

- Offering má zatím jen 1 balíček. Roční chybí.
- Formulář offeringu v RevenueCat se při přidání druhého balíčku chová
  nestabilně: po kliknutí na „New Package" vymaže popis prvního balíčku,
  novému balíčku přiřadí produkt prvního a uložení pak tiše neprojde
  (zůstane na `/edit`, bez chybové hlášky a bez toastu).
- Vyzkoušeno osm variant: klik na Save, `form.requestSubmit()`,
  různá pořadí vyplňování, dopsání všech polí obou balíčků před
  uložením. Výsledek stejný.
- Do funkčního stavu se nezasáhlo, `$rc_monthly` zůstává správně
  nastavený.

**Doporučený ruční krok (30 sekund)**

1. `https://app.revenuecat.com/projects/b0f25a13/product-catalog/offerings/ofrnga3369cd6e7`
2. Edit → New Package
3. Identifier **Annual** (odpovídá `$rc_annual`), Description `Annual`
4. U aplikace Tapkasa iOS vybrat produkt **Tapkasa Pro Yearly**
   (`tapkasa.pro.yearly`)
5. Zkontrolovat, že prvnímu balíčku zůstalo Description `Monthly`
   a produkt `Tapkasa Pro Monthly`, a teprve pak Save.

**Ještě zbývá v RevenueCat**

- Označit offering `default` jako **current**.
- Po založení Play produktů je naimportovat do konfigurace
  `Tapkasa Android` (`app0dee10a745`) a připojit k `pro`, plus doplnit
  je do obou balíčků offeringu.
- Nahrát **service account JSON** pro Google Play.
- Zapnout **server notifications** (Apple V2, Google RTDN).

---

## Fáze 7, Google Play (2026-08-31)

**Přihlášení**

- Kopie profilu Chromu si nepřenesla Google session, Play Console
  přesměrovávala na marketingovou stránku. Uživatel se přihlásil ručně
  v ovládaném Chromu, pak už konzole funguje.
- Vývojářský účet **deriverge s.r.o.**, ID `5046049502424745320`.

**Hotovo**

- **Aplikace vytvořena**: název `Tapkasa - Pokladna do kapsy`,
  package **`com.deriverge.tapkasa`**, výchozí jazyk **Čeština (cs-CZ)**,
  typ Aplikace, cena **Za 0 Kč**, všechny tři deklarace potvrzeny.
  - **Play app ID `4976431302400174530`**, stav Koncept.
  - Před odesláním proběhla kontrola všech polí, protože package name
    i volba Zdarma jsou na Play nevratné.
- **Záznam v obchodě, texty uloženy** (Uložit jako koncept, Play potvrdil
  „Změna byla uložena"):
  - Název: `Tapkasa - Pokladna do kapsy` (27/30),
  - Stručný popis: 73/80 znaků,
  - Úplný popis: 2 521/4 000 znaků, převzatý z `store/listing-cs.md`
    s předepsanou úpravou „účtuje přes **Google Play**" místo App Store.

**BLOKUJE: předplatná vyžadují účet obchodníka Google Payments**

- Stránka Monetizace → Předplatné hlásí „Chybí požadavky na přístup
  k této stránce" a nabízí jen „Založit účet obchodníka".
- Bez toho **nejde vytvořit ani jedno předplatné**, tedy ani base plany
  `monthly`/`yearly`, ani offer `trial14`, ani CZ ceny.
- Je to Payments profile, který podle pravidel zadání nevyplňujeme.
  Uživatel byl navedený. Ověření u Googlu trvá, je to kritická cesta.

**BLOKUJE: nahrání grafiky do záznamu v obchodě**

- Ikona, hlavní grafika ani snímky obrazovky se nepodařilo nahrát.
- Tlačítko „Přidat podklady" neotevírá nativní dialog, ale vytvoří
  v DOM skrytý `input[type=file]`. Soubor se do něj **prokazatelně
  vloží** (`files.length = 1`, správný název), ale Angular v konzoli
  na `change` ani `input` událost nereaguje a UI zůstane beze změny.
- Vyzkoušeno: `Page.setInterceptFileChooserDialog` (funguje na testovacím
  inputu, ale tlačítko chooser nevyvolá), `DOM.setFileInputFiles` na
  nalezený input, ruční dispatch `input` i `change`.
- Ruční cesta pro uživatele, soubory jsou připravené v repozitáři:
  - Ikona: `design/png/icon-512.png` (512×512)
  - Hlavní grafika: `design/png/feature-graphic-1024x500.png`
  - Telefon: `store/screenshots/play-cs-0{1,2,3,5,7}-*.png` (1080×1920)

**Poznámka ke snímkům pro tablety**

- Play u 7" a 10" tabletu vyžaduje poměr stran 16:9 nebo 9:16.
  Připravené iPad snímky `ipad129-*` mají 2048×2732, což je poměr 3:4
  a do zadaného rozmezí nespadá. Před nahráním je bude potřeba
  přeexportovat, jinak je Play odmítne.

**Zbývá na Play (až po účtu obchodníka)**

- Obě předplatná, base plany, offer `trial14`, ceny 129 a 990 Kč.
- App content: privacy policy URL, App access, Ads, content rating,
  target audience, Data safety podle `store/google-data-safety.md`,
  Government/Financial/Health otázky.
- Grafika záznamu, tablet snímky.
- Play App Signing, AAB, internal testing, closed testing (12 testerů,
  14 dní), production access.

---

## Fáze 8, App Store Connect, nastavení aplikace (2026-08-31)

**Hotovo**

- **App Information**:
  - Podtitul `Kasa pro stánky a festivaly` (27/30). Zvolena tato varianta,
    protože název už obsahuje „Pokladna do kapsy", přesně jak radí
    `store/listing-cs.md`.
  - Primární kategorie **Business**, sekundární **Food & Drink**.
  - **Content Rights**: „Does not use third-party content".
  - Poznámka: App Store Connect u ukládání vypsal obecné
    „Sorry, something went wrong". Po znovunačtení stránky jsou ale
    všechny hodnoty uložené, hláška patřila k jiné části stránky.
- **Age Ratings vyplněny**, všech 6 stran dotazníku, všude odpověď
  „None" nebo „No" (rodičovská kontrola, web, UGC, sociální sítě,
  zprávy, reklamy, vulgarita, horor, návykové látky, zdravotní obsah,
  sexuální obsah, násilí, hazard, loot boxy).
  - **Výsledek: 4+ pro 172 zemí**, s regionálními variantami
    (Brazílie ALL, Korea 00+, Vietnam). Odpovídá očekávání checklistu.
  - Napoprvé se dotazník neuložil, protože skript klikal na Save
    v hlavičce stránky místo Next v dialogu a nedošel k závěrečnému
    potvrzení. Opraveno omezením hledání tlačítek na oblast dialogu.

**Odchylka: dostupnost aplikace je 175 zemí, ne CZ+SK**

- `store/checklist.md` požaduje **minimálně** Česko a Slovensko
  a **doporučuje** launch jen CZ+SK. Nastaveno je 175 zemí.
- Průvodce „Set Up Availability" nenabídl seznam zemí se zaškrtávátky
  ani odkaz „None", takže se prošel s výchozím výběrem všech zemí.
  Následné „Manage" ukazuje jen přehled bez možnosti editace.
- Požadované minimum je splněno. Zúžení na CZ+SK je jednoduchá změna,
  kterou lze udělat kdykoli před vydáním, ale je to i **obchodní
  rozhodnutí** (UI je česky, anglický listing je hotový), proto se
  nechává na uživateli.

**Zbývá na App Store Connect**

- **Cena aplikace**: v Price Schedule zvolit **Free**. Tlačítko
  „Add Pricing" se automatizací nepodařilo otevřít. Je to jeden výběr
  v rozbalovacím seznamu.
- **App Privacy** podle `store/apple-privacy-labels.md`.
- **Review screenshot paywallu** u obou předplatných, jinak IAP uvíznou
  ve „Waiting for Review". Soubor je připravený:
  `store/screenshots/iphone67-cs-07-paywall.png` (1290×2796).
- **Lokalizace subscription group** „Tapkasa Pro" (display name).
- **Verze 1.0**: promo text, popis, klíčová slova, screenshoty
  (iPhone 6,7" a iPad 12,9"), What's New, support URL, copyright.
- **App Review Information**: kontakt, „Sign-in not required",
  Notes ze `store/review-notes.md`, přiložit IAP k verzi.
- **Release option**: Manually release this version.
- **Small Business Program**: přihlásit v Agreements.

---

## Fáze 9, pokyny z inboxu (2026-08-31)

Přečten `ops/mac-inbox.md`, aktualizace 1 a 2. Vyhodnocení bod po bodu.

**Bod 1, Xcode** — vyřešeno dřív, viz fáze 4. macOS 15.7.3 Sequoia,
Xcode 16.4 běží, plán B (Codemagic) není potřeba.

**Bod 2, pokračovat fázemi 2, 3 a 5** — uděláno, viz fáze 2, 3, 6, 7, 8.

**Bod 3, po vložení klíčů znovu sync** — hotovo:
- `git pull` na `main` stáhl commit `ed2a63e`
  („Add a support contact row and address across the app and web"),
- `./sync-web.sh` proběhlo, `mobile/www/index.html` má nyní 238 053 B,
- `npx cap sync ios` proběhlo, plugin
  `@revenuecat/purchases-capacitor@13.4.2`, `Package.swift` přepsán,
- ověřeno, že veřejné RevenueCat klíče v `mobile/billing.js`
  i `mobile/www/billing.js` merge přežily.

**Bod 4, App Store Connect API klíč** — částečně, s komplikací:

- Vytvořen nový klíč **`Tapkasa Build Upload`**, **Key ID `ABWJD553V4`**,
  role **App Manager**, Issuer ID `1ed9b87d-51a7-41b4-ab9d-c1b5e88a87fc`.
- **Soubor `.p8` se nepodařilo stáhnout.** Apple zobrazí potvrzovací
  dialog „Download API Key" (klíč lze stáhnout jen jednou); klik na
  potvrzení nevyvolal žádnou událost stahování a v historii Chromu
  položka není. Odkaz Download u řádku ale zmizel.
- **Náhradní řešení**: na účtu už existuje klíč **`RevenueCat API`,
  Key ID `MTMP9A7SKR`, role App Manager**, a jeho soubor
  `AuthKey_MTMP9A7SKR.p8` je stažený v `~/Downloads` (257 B, 28. 8. 2026).
  Pro nahrávání buildů plně stačí.
- **Zkopírovat ho na cílové místo se nepodařilo**: macOS blokuje procesu
  přístup do `~/Downloads` (`Operation not permitted`, ochrana soukromí
  TCC). Uživatel byl požádán, ať to udělá sám:
  `mkdir -p ~/.appstoreconnect/private_keys && cp ~/Downloads/AuthKey_MTMP9A7SKR.p8 ~/.appstoreconnect/private_keys/ && chmod 600 ~/.appstoreconnect/private_keys/AuthKey_MTMP9A7SKR.p8`
- Adresář `~/.appstoreconnect/private_keys` je založený s právy 700.
- **Doporučení**: klíč `Tapkasa Build Upload` (`ABWJD553V4`) je bez
  staženého souboru nepoužitelný. Buď ho stáhnout ručně, nebo revokovat,
  ať na účtu nezůstává viset.
- Obsah žádného klíče se nikam nezapisoval ani nevypisoval.

**Bod 5, kontaktní e-mail `info@deriverge.com`** — zatím nepoužit.
Pole, kam patří, jsou v dosud nevyplněných sekcích:
App Store Connect → App Review Information a verze 1.0 (Support URL
`https://www.deriverge.com/kava/`), Google Play → Store listing →
App support. Doplní se s nimi.

---

## Fáze 10, iOS build (2026-08-31)

**Apple ID v Xcode**

- Uživatel přidal účet. Ověřeno nepřímo: v `com.apple.dt.Xcode` existuje
  `DVTDeveloperAccountManagerAppleIDLists` se záznamem.
- `security find-identity -v -p codesigning` hlásí **0 identit**.
  Certifikát ještě nevznikl, což je normální; Xcode ho vyrobí při prvním
  buildu s `-allowProvisioningUpdates`.

**Projekt připraven k podpisu**

- Do `mobile/ios/App/App.xcodeproj/project.pbxproj` doplněno
  `DEVELOPMENT_TEAM = 6XX9G3S468;` do obou konfigurací (Debug i Release).
- Ostatní nastavení už sedělo: `CODE_SIGN_STYLE = Automatic`,
  `PRODUCT_BUNDLE_IDENTIFIER = com.deriverge.tapkasa`,
  `MARKETING_VERSION = 1.0`, `CURRENT_PROJECT_VERSION = 1`.

**BLOKUJE (řeší se): chybí iOS platform support**

- `xcodebuild archive` končí na
  `Found no destinations for the scheme 'App' and action archive`.
- Příčina: destinace „Any iOS Device" je označená jako nezpůsobilá
  s hláškou `iOS 18.5 is not installed. To use with Xcode, first
  download and install the platform`.
- Matoucí je, že `xcodebuild -showsdks` iOS 18.5 SDK **vypisuje**
  a `iPhoneOS18.5.sdk` na disku je. Adresář `iPhoneOS.platform` má ale
  jen **183 MB**, což je zjevně jen stub. Xcode 16 stahuje device
  support zvlášť od aplikace.
- Obejít to přes `-sdk iphoneos` nejde, destination resolution to
  zkontroluje dřív.

**Chyba v mém dřívějším doporučení**

- Uživateli jsem doporučil zrušit stahování platformy s tím, že pro
  archiv a TestFlight není potřeba. **To bylo špatně.** Bez ní Xcode 16.4
  build pro iOS zařízení vůbec nespustí. Stálo to zbytečný čas.
- Nyní běží `xcodebuild -downloadPlatform iOS`, řádově GB a hodiny.
- (Predictive Code Completion Model, 2,51 GB, opravdu potřeba není,
  ten je čistě komfortní.)

**Po dokončení stažení**

- `xcodebuild archive` s `-allowProvisioningUpdates`, pak export
  a nahrání do TestFlightu.
- K nahrání je připravený App Store Connect API klíč `MTMP9A7SKR`
  (role App Manager); jeho `.p8` je zatím jen v `~/Downloads`, protože
  macOS blokuje procesu přístup do té složky.

---

## Fáze 10b, iOS build hotový, nahrání odmítnuto (2026-08-31)

**Build proběhl úspěšně**

- Po doinstalování iOS platform support (`xcodebuild -downloadPlatform iOS`)
  se objevila destinace „Any iOS Device".
- Do projektu doplněno `DEVELOPMENT_TEAM = 6XX9G3S468`.
- `xcodebuild archive -allowProvisioningUpdates` → **ARCHIVE SUCCEEDED**.
  Xcode si sám vytvořil vývojářský certifikát a profil
  `iOS Team Provisioning Profile: com.deriverge.tapkasa`.
- `xcodebuild -exportArchive` (method `app-store-connect`) →
  **EXPORT SUCCEEDED**, `App.ipa`, 6 257 651 B.
  - certifikát **Cloud Managed Apple Distribution**, platnost do 31. 8. 2027,
  - profil `iOS Team Store Provisioning Profile: com.deriverge.tapkasa`,
  - entitlements `application-identifier = 6XX9G3S468.com.deriverge.tapkasa`,
    **`beta-reports-active = true`** (připraveno pro TestFlight),
  - architektura `arm64`,
  - **`PrivacyInfo.xcprivacy` je v balíčku**, zařazení do Xcode projektu
    tedy fungovalo.

**Poznámka k autentizaci**

- Nahrávání **nepotřebovalo** App Store Connect API klíč. `xcodebuild`
  s `destination = upload` použil účet přihlášený v Xcode a k Applu se
  dostal bez problémů. Nedostupnost `.p8` v `~/Downloads` je tedy pro
  tuhle cestu bezpředmětná.

## BLOKUJE: Xcode neproveditelný

- Nahrání do App Store Connect Apple **odmítl při validaci**:

  > SDK version issue. This app was built with the iOS 18.5 SDK.
  > All iOS and iPadOS apps must be built with the iOS 26 SDK or later,
  > included in Xcode 26 or later, in order to be uploaded to
  > App Store Connect or submitted for distribution.
  > (ID: 16ac4bcf-718b-44dd-8afa-e7488856ac26)

- Řetěz omezení, který z toho plyne:
  - Apple vyžaduje **iOS 26 SDK**, ten je jen v **Xcode 26+**,
  - Xcode 26 vyžaduje **macOS 26 (Tahoe)**,
  - na Macu běží **macOS 15.7.3 Sequoia** a uživatel ho aktualizovat
    nechce kvůli stabilitě DaVinci Resolve.
- Xcode 16.4 tedy na tomto stroji **staví i podepisuje správně**, ale
  výsledek je pro App Store nepoužitelný. Lokální cesta je uzavřená,
  dokud se nezmění macOS.

**Doporučení pro koordinující session**

- Nastal přesně případ z inboxu, bod 1. Podle pokynu **plán B
  (Codemagic) nespouštím**, čeká se na rozhodnutí.
- Pro plán B bude potřeba App Store Connect API klíč. Použitelný je
  `MTMP9A7SKR` (role App Manager), soubor `AuthKey_MTMP9A7SKR.p8` leží
  v `~/Downloads`. Pozor: prostředí, ve kterém běžím, do té složky
  nemá přístup (TCC), takže ho tam musí vzít uživatel ručně přes Finder.
  Klíč `ABWJD553V4` je bez staženého souboru nepoužitelný.
- Alternativy k Codemagic, kdyby přišly v úvahu: druhý Mac s macOS 26,
  macOS 26 na externím disku nebo v druhém APFS volume (DaVinci by
  zůstal nedotčený na stávajícím systému), nebo Xcode Cloud.

---

## Fáze 11, Xcode Cloud (2026-08-31)

**Zásadní oprava předchozího závěru**

- Dřívější závěr „Xcode neproveditelný" platil jen pro **App Store**
  verzi Xcode. Ověřeno na xcodereleases.com:
  - **Xcode 26.0 až 26.3 vyžaduje macOS 15.6+**, tedy běží i na
    tomto stroji (macOS 15.7.3),
  - teprve **Xcode 26.4+ vyžaduje macOS 26.2+**.
  - Mac App Store nabízí jen nejnovější verzi, proto hlásil nutnost
    aktualizace systému.
- Lokální cesta tedy uzavřená není, stačilo by stáhnout Xcode 26.3
  z developer.apple.com. Necháváme jako záložní plán.

**Uvolnění místa** (se souhlasem uživatele)

- `/Library/Developer/CoreSimulator` mělo **30 GB**, z toho 19 GB
  runtime iOS 18.6, který stáhl `-downloadPlatform iOS`. Pro archiv
  není potřeba. Smazáno přes `xcrun simctl runtime delete all`.
- Smazán Xcode 16.4 (4,9 GB), DerivedData (880 MB), SPM cache.
- Volné místo: **15 GB → 34 GB**.

**Xcode Cloud rozjetý**

- Workflow **Default** na větvi `main` existuje. Prvotní hláška
  `CI.SCM.Error.RepositoryNotAccessible` byla přechodná, GitHub App
  „Xcode Cloud" má na účtu `deriverge` přístup ke **všem repozitářům**
  a repozitář patří témuž účtu, takže práva jsou v pořádku.
- **První build spadl** na chybějícím `Package.resolved`:
  > a resolved file is required when automatic dependency resolution is
  > disabled and should be placed at .../xcshareddata/swiftpm/Package.resolved
- **Příčina byla moje**: soubor jsem ve fázi 5 vědomě nezařadil do
  commitu s odůvodněním, že je to nad rámec zadání. Xcode Cloud staví
  s vypnutým automatickým resolvem a bez něj build nespustí.
- Opraveno commitem `f9258e7`, `Package.resolved` je nyní verzovaný
  (capacitor-swift-pm 8.5.0, purchases-hybrid-common 18.32.1,
  RevenueCat 5.85.0). Vedlejším přínosem je reprodukovatelný build.
- Push sám build nespustil, workflow má manuální start condition.
  **Build spuštěn ručně 31. 8. 2026 22:35**, workflow Default,
  větev `main`, stav Queued.

**Poznámka k jinému projektu uživatele**

- Aplikace VZT Montér se do TestFlightu dostala přes **EAS Build od
  Expo**, tedy také cloudové sestavení, ne lokální Xcode. Potvrzuje to
  správnost cloudové cesty. Pro Tapkasu je ale přirozenější Xcode Cloud,
  protože jde o Capacitor, ne Expo projekt.

**Dostupnost aplikace, upřesnění**

- Uživatel výslovně potvrdil, že chce prodávat **celosvětově**.
  Ověřeno, že App Store Connect má **175 zemí**, žádná změna nebyla
  potřeba. Doporučení „launch jen CZ+SK" pochází ze
  `store/checklist.md` řádek 79, ne od uživatele.

---

## Fáze 12, TestFlight, App Privacy a přesun webu (2026-08-31)

**TestFlight, interní testeři**

- Vytvořena interní skupina **Interní testeři**.
- Přidáni `info@deriverge.com` a **`caganekdavid@gmail.com`**.
- Zdržení mělo konkrétní příčinu: účet `caganekdavid@gmail.com` měl
  v App Store Connect přístup **jen k aplikaci VZT Montér**, Tapkasu
  neviděl, a proto se v nabídce testerů nezobrazoval. Doplněn přístup
  k Tapkase přes Users and Access → Manage apps.
- Pozvánka do týmu byla nejdřív nepřijatá, byla odeslána znovu
  a uživatel ji potvrdil. Role Developer.

**Xcode Cloud, doručení do TestFlightu**

- Buildy 7 a 8 skončily zeleně, ale **do TestFlightu nedorazily**.
  Příčina: workflow Default měl u akce Archive
  `Distribution Preparation = None`, tedy jen archivoval.
- Přepnuto na **TestFlight (Internal Testing Only)** a uloženo.
- Potvrzený toolchain Xcode Cloud: **Xcode 26.6 (17F113)** na
  **macOS Tahoe 26.6.2**. To je iOS 26 SDK, který Apple pro nahrání
  vyžaduje a lokální Xcode 16.4 nabídnout nemohl.
- Buildy 9 (23:07) a 10 (23:29) běží. Workflow reaguje i na push do
  `main`, build 10 se spustil sám.

**App Privacy**

- Nastavena **Privacy Policy URL**.
- Dotazník o sběru dat rozpracovaný, odpovědi podle
  `store/apple-privacy-labels.md`: sběr Ano, typy pouze
  Identifiers → User ID a Purchases → Purchase History, obojí
  App Functionality, nespojené s identitou, bez trackingu.

**Přesun webu z `/kava/` na `/tapkasa/`** (commit `dc41997`)

- Na žádost uživatele, `/kava/` byl pozůstatek pracovního názvu.
- Složka `kava/` přejmenována na `tapkasa/`, přepsáno **40 výskytů
  ve 20 souborech**: manifest, service worker, `bridge.js`,
  `billing.js`, `sync-web.sh`, `capacitor.config.ts`, `copy-web.sh`,
  `ci_post_clone.sh`, READMEs, `store/review-notes.md`,
  `store/promo/src/pcap.mjs`.
- Na `/kava/` ponechána **přesměrování** (`index.html`, `privacy.html`,
  `terms.html`), aby už rozeslané odkazy a případné nainstalované PWA
  nespadly.
- **Záměrně nezměněn** localStorage klíč `kavakasa.v1` ani název
  IndexedDB databáze. Přejmenování by uživatelům osiřelo uložená data.
- Ověřeno živě: `/tapkasa/` a `/tapkasa/privacy.html` vrací 200,
  `/kava/` přesměrovává.
- `sync-web.sh` a `npx cap sync ios` proběhly znovu.
- Privacy Policy URL v App Store Connect aktualizována na
  `https://www.deriverge.com/tapkasa/privacy.html`.

**Poznámka k propagačnímu spotu**

- V `store/promo/` jsou čtyři verze spotu (cs/en, na výšku i na šířku),
  26,4 s, 1080×1920 a 1920×1080, vyrobené druhou session.
- **Do obchodů se nehodí ani jeden.** App Store App Preview musí být
  záznam obrazovky bez rámečků zařízení a bez odkazů na jiné obchody;
  spot má maketu iPhonu a iPadu a končí na badgích App Store i Google
  Play. Google Play přijímá promo video **jen jako odkaz na YouTube**
  a badge App Store je proti jejich pravidlům.
- Video je ale nepovinné, vydání to neblokuje. Použitelné je pro web,
  sociální sítě a reklamu.

---

## Fáze 13, noční směna (2026-09-01)

**Build je v TestFlightu**

- Build **10** (spuštěný 23:29) skončil zeleně a TestFlight ho přijal,
  stav **„Ready to Test, expires in 90 days"**. Trvání buildu 11 minut.
- Toolchain Xcode Cloud: Xcode 26.6, macOS Tahoe 26.6.2.
- Ve skupině Interní testeři jsou `caganekdavid@gmail.com`
  a `info@deriverge.com`.

**BLOKUJE: App Store Connect se odhlásil**

- Session v kopii profilu vypršela, ASC přesměrovává na přihlášení.
- Znovupřihlášení vyžaduje Apple ID a **dvoufázové ověření uživatele**,
  který spí. Vše na Apple straně je tím pádem do rána zastavené:
  dokončení App Privacy, verze 1.0, review screenshoty, Small Business
  Program, cena Free.
- Ostatní session **žijí**: YouTube Studio (kanál deriverge s.r.o.),
  Play Console, RevenueCat.

**YouTube, nahrána všechna čtyři videa**

- Kanál `UC8MKQOvIahw1esBCKGti0wA`, účet info@deriverge.com.
- Záložka Videa: `tapkasa spot cs 1920x1080`, `tapkasa spot en 1920x1080`.
- Záložka Shorty: `tapkasa spot cs 1080x1920`, `tapkasa spot en 1080x1920`.
  YouTube zařadil verze na výšku automaticky jako Shorts (svislé video
  do 60 s).
- Všechna jsou zatím **koncepty**, tedy nikde veřejně nevisí.

**Co se u videí nepodařilo**

- **Název a popis nejdou vyplnit automatizací.** Pole YouTube Studia
  jsou `contenteditable` uvnitř webové komponenty a neberou ani
  `Input.insertText` přes CDP, ani výběr rozsahu s následným vložením.
  Zkoušeno šestkrát ve třech variantách. Zůstávají automatické názvy
  podle souboru.
- **Vznikly dva duplikáty Shorts.** První pokus o nahrání verzí na výšku
  vypadal jako neúspěšný, protože se v seznamu Videa neobjevily; ve
  skutečnosti byly celou dobu pod Shorts. Opakováním tedy vznikly dvě
  kopie navíc. Smazat je automatizací nešlo, kontextové menu řádku se
  zobrazuje až při najetí myší.

**Co zbývá u videí (ruční, pár minut)**

1. Ve Studiu doplnit název a popis, u obou dlouhých videí i u Shorts.
   Návrh názvu: „Tapkasa — pokladna do kapsy pro stánky, trhy a festivaly".
2. Zvolit viditelnost. Pro odkaz v Google Play stačí Nezveřejněné.
3. Smazat dva duplicitní Shorts.
4. Odkaz na české video na šířku vložit do Play Console → Store listing
   → Promo video.

**Poznámka k použitelnosti v obchodech, platí i nadále**

- Spot se **nehodí jako App Store App Preview** (rámečky zařízení,
  badge Google Play). Do App Store se tedy nenahrává nic.
- Pro Google Play je použitelný pouze jako **odkaz na YouTube**;
  badge App Storu ve videu je proti pravidlům Play o propagaci jiných
  platforem, je to riziko při kontrole.
- Video je v obou obchodech **nepovinné**, vydání neblokuje.

---

## Fáze 14, konec noční směny (2026-09-01)

**Google Play, pokus o App content**

- Sekce „Obsah aplikace" se v konzoli nepodařilo otevřít.
  `/app/{id}/app-content` přesměrovává na seznam aplikací, v levé
  navigaci položka není a rozbalení „Nastavení aplikace → Zobrazit
  úkoly" na dashboardu nereagovalo.
- Nezkoušelo se dál, protože celá Play větev stejně čeká na **účet
  obchodníka Google Payments**, bez kterého nejdou předplatná a bez
  nich nemá smysl aplikaci dokončovat.
- Potvrzeno ale, že **texty záznamu v obchodě jsou uložené**: Přehled
  publikování hlásí „Byl zadán název aplikace (Tapkasa - Pokladna do
  kapsy) a všechny další povinné informace."

**Souhrn toho, co je hotové**

| Oblast | Stav |
|---|---|
| RevenueCat projekt, aplikace, entitlement `pro`, produkty | hotovo |
| RevenueCat offering `default` | jen balíček `$rc_monthly` |
| Apple App ID `com.deriverge.tapkasa` | hotovo |
| ASC aplikace `6807075649` | hotovo |
| Obě předplatná: ceny, CZ ceny, lokalizace, trialy | hotovo |
| App Information, kategorie, Content Rights, Age Rating 4+ | hotovo |
| Privacy Policy URL | hotovo, `/tapkasa/privacy.html` |
| App Privacy dotazník | rozpracováno |
| Dostupnost 175 zemí | hotovo, potvrzeno uživatelem |
| iOS build, archiv, podpis | hotovo přes Xcode Cloud |
| **TestFlight, Ready to Test** | **hotovo** |
| Interní testeři | hotovo |
| Web přesunut na `/tapkasa/` | hotovo |
| Repozitář: klíče, privacy manifest, export compliance | hotovo |
| Play aplikace + texty listingu | hotovo |
| Play grafika, předplatná, App content | blokováno |
| YouTube, 4 videa nahraná | hotovo, jako koncepty |

**Otevřené blokace pro uživatele**

1. **App Store Connect je odhlášený**, znovupřihlášení vyžaduje 2FA.
2. **Účet obchodníka Google Payments**, bez něj nejdou Play předplatná.
3. **DAC7** formulář v ASC → Business → Agreements.
4. **Small Business Program**, přihlásit v ASC → Agreements.

---

## Fáze 15, opravy aplikace a nasazení (2026-09-01)

**Opravena chyba: probliknutí platebního panelu**

- Hlášení uživatele: při ťuknutí na bankovku celý panel na okamžik
  zmizel a zase se objevil, na iPhonu i iPadu.
- Příčina nalezena v `tapkasa/index.html`: `render()` volal
  `paint("sheetSlot", renderSheet())`. Při každé změně částky se
  změnilo HTML, takže se nahradil celý slot a zanikl i znovu vznikl
  obal `.scrim` a `.sheet`. Oba mají vstupní animace
  (`@keyframes fade` z nulového krytí, `@keyframes rise`), které se tím
  přehrály znovu. To bylo to probliknutí.
- Řešení: `renderSheet()` rozdělen na `sheetInner()` (obsah) a obal.
  Nová funkce `paintSheet()` přepisuje jen vnitřek už existujícího
  panelu, dokud je otevřený stejný krok; obal se tvoří pouze při
  otevření nebo změně kroku. Na `.scrim` přidán `data-step` pro
  porovnání.
- Ověřeno v prohlížeči automatizovaným testem: uzel `.scrim` přežije
  opakovaná ťuknutí, přijatá částka roste 1 → 2 → 3 Kč, konzole čistá.
- Commit `d579e09`.

**Zkráceno poděkování zákazníkovi**

- `sayThanks()` říkal „Děkujeme za objednávku." plus „Užijte si {název
  akce}.". Název akce se opakoval u každého účtu. Nově zazní jen první
  věta. Překlady `speakEnjoy` ponechány nevyužité pro případný návrat.

**Dotaz uživatele: jde vypnout čtení objednávek**

- Ano, funkce už existuje. Přepínač `state.voice` v Menu hlídá obojí:
  čtení nových objednávek na výdeji i poděkování na kase. Nic se
  nedoplňovalo.

**Nasazeno do TestFlightu**

- Push do `main` spustil Xcode Cloud sám. **Build 11**, vytvořen
  1. 9. 2026 9:09, stav **Ready to Test**, skupina Internal.
- V TestFlightu jsou nyní buildy 9, 10 a 11, všechny Ready to Test.
  Build 11 je ten s opravami.

**Loga deriverge pro profil vývojáře**

- Vyrobena z `pictures/deriverge_logo-long.jpg`, aby seděla značka:
  - `design/deriverge/deriverge-icon-512.png`, samotné `d` vyříznuté
    z wordmarku (x 514-622, y 118-279 v originále), 512×512, RGB bez
    alfa kanálu,
  - `design/deriverge/deriverge-header-4096x2304.png`, celé
    `</deriverge>` včetně tagline.
  - Pozadí `#18171d` vzorkované přímo z původního loga.
- Commit `0fec915`.

## BLOKUJE: nahrávání souborů do konzolí nejde automatizovat

- Ověřeno **třikrát nezávisle**:
  1. Google Play, grafika záznamu v obchodě,
  2. Google Play, profil vývojáře (ikona a záhlaví),
  3. App Store Connect, snímky obrazovky verze 1.0.
- Ve všech případech `DOM.setFileInputFiles` soubor do inputu vloží
  (v Play šlo ověřit `files.length = 1` se správným názvem), ale
  aplikace konzole na událost nereaguje a nahrání neproběhne.
  Zkoušeno i `Page.setInterceptFileChooserDialog` (funguje na testovacím
  inputu, ale tlačítka konzolí chooser nevyvolají) a ruční dispatch
  `input` i `change`.
- **Závěr: obrázky a snímky musí do obou konzolí přetáhnout uživatel.**
  Texty, formuláře, přepínače a dotazníky automatizovat jde, soubory ne.

**Připravené soubory k ručnímu nahrání**

| Kam | Soubor |
|---|---|
| Play → profil vývojáře → ikona | `design/deriverge/deriverge-icon-512.png` |
| Play → profil vývojáře → záhlaví | `design/deriverge/deriverge-header-4096x2304.png` |
| Play → záznam v obchodě → ikona | `design/png/icon-512.png` |
| Play → záznam v obchodě → hlavní grafika | `design/png/feature-graphic-1024x500.png` |
| Play → snímky telefonu | `store/screenshots/play-cs-0{1,2,3,5,7}-*.png` |
| ASC → verze 1.0 → snímky iPhone | `store/screenshots/iphone67-cs-*.png` |
| ASC → verze 1.0 → snímky iPad | `store/screenshots/ipad129-cs-*.png` |

---
