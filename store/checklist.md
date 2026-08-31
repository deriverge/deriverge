# Checklist publikace, Tapkasa (App Store + Google Play)

Kroky v pořadí, v jakém se reálně dělají. Značky: ☐ = udělat,
⚠ = častý důvod zamítnutí / zdržení.

---

## Fáze 0, Předpoklady (týdny předem, běží dlouho)

- ☐ **Apple Developer Program**, účet za 99 USD/rok
  ([DOPLŇ: jestli individual, nebo company, company vyžaduje D-U-N-S
  číslo a ověření právnické osoby, trvá 1-4 týdny]).
- ☐ **Google Play Console**, účet za 25 USD jednorázově.
  ⚠ Osobní účty založené po listopadu 2023 musí před produkčním
  vydáním projít **uzavřeným testem: min. 12 testerů nepřetržitě po
  14 dní**. Založit účet a spustit closed testing co nejdřív, tohle je
  kritická cesta harmonogramu.
- ☐ Rozhodnout identifikátor: `[DOPLŇ: reverse-DNS, např. com.firma.tapkasa]`
  - stejný jako bundle ID (iOS) i package name (Android); po publikaci
  na Play už nejde změnit.
- ☐ Zaregistrovat/potvrdit web pro podporu a privacy policy
  `[DOPLŇ: URL, např. https://www.deriverge.com/tapkasa/]` a vystavit tam
  `privacy-policy-cs.md` + `privacy-policy-en.md` jako HTML.
- ☐ Podepsat **Paid Applications Agreement** (App Store Connect →
  Agreements, Tax, and Banking) + bankovní účet + daňové formuláře.
  ⚠ Bez podepsané smlouvy IAP nefunguje ani pro review.
- ☐ Založit **Payments profile** v Play Console.
- ☐ Přihlásit se do **Apple Small Business Program** (15 % provize, viz `store/monetization.md`, schválení trvá dny).

## Fáze 1, Společné podklady

- ☐ Ikona aplikace: 1024×1024 px bez průhlednosti (Apple, do asset
  katalogu) + 512×512 px PNG (Play Store listing).
- ☐ Texty z `store/listing-cs.md` (primární čeština) a
  `store/listing-en.md` (angličtina), délky jsou už ověřené.
- ☐ **Screenshoty** (pořídit z reálné aplikace s ukázkovými daty; žádné
  vymyšlené UI, ⚠ Apple 2.3.3):
  - App Store iPhone **6,7″: 1290×2796 px** (na výšku), povinné,
    3-10 kusů; pokryje i menší telefony.
  - App Store iPad **12,9″: 2048×2732 px**, povinné, protože aplikace
    běží na iPadu (a pokladna na iPadu je hlavní use-case).
  - Google Play telefon: 2-8 kusů, doporučeně **1080×1920 px**
    (min. strana ≥ 320 px, max. 3840 px, poměr 9:16).
  - Google Play tablet 7″ a 10″: doporučené (bez nich Play neukáže
    tabletní listing pěkně), lze exportovat z iPadových podkladů
    v 2048×2732 / 1080×1920.
  - **Feature graphic (Play): 1024×500 px**, povinná pro listing.
  - Navržené scény: 1) prodejní mřížka s barevnými kartami, 2) platební
    okno s výpočtem vrácení, 3) fronta objednávek s čísly a chipy,
    4) otevřená objednávka s odškrtáváním, 5) přehled tržby,
    6) párování dvou zařízení (kasa + výdej vedle sebe).
- ☐ Volitelně: app preview video (App Store) / promo video YouTube (Play).

## Fáze 2, App Store (v tomto pořadí)

1. ☐ App Store Connect → **New App**: platforma iOS, název
   `Tapkasa - Pokladna do kapsy`, primární jazyk **čeština**, bundle ID,
   SKU `tapkasa-ios`.
2. ☐ Vytvořit **IAP předplatná** přesně podle `store/monetization.md`
   (skupina, produkty, ceny, CZ ceny, trial 14 dní, screenshoty IAP).
3. ☐ Vyplnit **App Information**: kategorie primární Business,
   sekundární Food & Drink; content rights; age rating dotazník
   (výsledek 4+, žádný závadný obsah, žádné loterie).
4. ☐ **App Privacy**, vyplnit přesně podle
   `store/apple-privacy-labels.md`; vložit URL privacy policy.
5. ☐ Nahrát build z Xcode (verze 1.0, build 1), v buildu:
   - ☐ `ITSAppUsesNonExemptEncryption = NO` v Info.plist (jen HTTPS →
     výjimka; ušetří dotaz na export compliance při každém buildu),
   - ☐ privacy manifest `PrivacyInfo.xcprivacy` (viz apple-privacy-labels.md),
   - ☐ RevenueCat public SDK key pro produkci, entitlement `pro` funkční.
6. ☐ **TestFlight**: interní testeři, projít celý flow (prodej, platba,
   fronta, párování dvou fyzických zařízení, nákup v sandboxu, restore,
   limit 10 účtů/den, obnova po přeinstalaci ze zálohy).
7. ☐ Verze 1.0 v App Store Connect: texty, klíčová slova, promo text,
   screenshoty, What's New, support URL, copyright
   `[DOPLŇ: © rok a držitel práv]`.
8. ☐ **App Review Information**: kontakt [DOPLŇ], „Sign-in not required",
   Notes = text ze `store/review-notes.md`; přiložit IAP k verzi.
9. ☐ Pricing: aplikace **Free**; dostupnost, minimálně Česko a
   Slovensko (⚠ doporučení: launch jen CZ+SK, rozšíření později, anglická lokalizace listingu je hotová, ale UI je česky).
10. ☐ Release option: **Manually release this version** (kontrola po
    schválení, pak ruční vydání).
11. ☐ Submit for Review. Typicky 24-48 h. Po schválení: Release.

## Fáze 3, Google Play (v tomto pořadí)

1. ☐ Play Console → **Create app**: název `Tapkasa - Pokladna do kapsy`,
   výchozí jazyk čeština, App (ne hra), Free.
   ⚠ „Free" je na Play nevratné, nikdy nejde přepnout na placenou
   aplikaci (IAP jsou v pořádku).
2. ☐ **App content** (vše je povinné před vydáním):
   - ☐ Privacy policy URL,
   - ☐ App access: „All functionality available without special access"
     + instrukce z `store/review-notes.md` (sekce párování a IAP),
   - ☐ Ads: **No ads**,
   - ☐ Content rating dotazník (IARC) → kategorie utility/nástroj,
     výsledek 3+/E,
   - ☐ Target audience: 18+ (pracovní nástroj; nevybírat děti),
   - ☐ **Data safety**: vyplnit přesně podle `store/google-data-safety.md`,
   - ☐ Government app: No; Financial features: **No / None of these**
     (aplikace platby nezpracovává, jen eviduje; ⚠ špatná odpověď tady
     spouští požadavky na licence),
   - ☐ Health: No.
3. ☐ **Monetize → Subscriptions** podle `store/monetization.md`
   (produkty, base plany, offer `trial14`, CZ ceny 129/990 Kč).
4. ☐ Store listing: texty z `store/listing-cs.md` + EN překlad,
   ikona 512×512, feature graphic 1024×500, screenshoty, kategorie
   Business, kontaktní e-mail `[DOPLŇ]`.
5. ☐ Podepisování: **Play App Signing** (výchozí), nechat Google
   spravovat klíč; nahrát **AAB** (ne APK).
6. ☐ **Internal testing**: nahrát AAB, ověřit billing s license testery
   (nákup, trial, restore, limit).
7. ☐ **Closed testing**: ⚠ u osobního účtu po 11/2023 povinně 12+
   testerů / 14 dní, spustit hned, jak existuje první funkční AAB.
8. ☐ Po splnění: žádost o **production access** (dotazník o testování).
9. ☐ Production release: nahrát AAB, release notes, země (CZ+SK, případně
   EU), **Managed publishing** zapnout (ruční vydání po schválení).
10. ☐ Odeslat k recenzi. První recenze může trvat až 7 dní; další bývají
    rychlejší.

## Fáze 4, Po vydání

- ☐ Ověřit produkční nákup malou skutečnou platbou na obou platformách
  (a hned zrušit).
- ☐ Zkontrolovat, že se odbití trialu a obnovy propisují do RevenueCat
  (Charts → Active subscriptions).
- ☐ Nastavit odpovědi na recenze (obě konzole umí notifikace).
- ☐ Propagační text App Store lze měnit bez nové verze, využít pro
  sezónní akce (festivalová sezóna, vánoční trhy).
- ☐ Archivovat přesné odeslané texty a odpovědi formulářů (kopii tohoto
  adresáře `store/` označit tagem verze).
- ☐ Při jakékoli změně SDK nebo datových toků aktualizovat současně:
  privacy policy, Apple štítky, Play Data safety (viz upozornění
  v `store/google-data-safety.md`).

---

## Rychlá tabulka grafických rozměrů

| Podklad | Rozměr | Povinné |
|---|---|---|
| App Store ikona | 1024×1024 px | ano (v buildu) |
| App Store iPhone 6,7″ screenshot | 1290×2796 px | ano |
| App Store iPad 12,9″ screenshot | 2048×2732 px | ano (aplikace běží na iPadu) |
| Play ikona | 512×512 px PNG | ano |
| Play feature graphic | 1024×500 px | ano |
| Play telefon screenshot | 1080×1920 px (min. 320, max. 3840) | ano (2-8 ks) |
| Play tablet 7″/10″ screenshot | do 3840 px, doporučeno 2048×2732 | doporučené |

## Prezentace párování (doplněno)

- `store/screenshots/pairing-*.png`: marketingový snímek „Kasa a výdej.
  Propojené." v rozměrech pro App Store (1290x2796, 2048x2732) i Play
  (1080x1920), česky a anglicky. Doporučené zařazení: druhý snímek v pořadí.
- `design/feature-graphic-pairing-cs.png` (1024x500): nová feature graphic
  pro Play s motivem propojení.
- `store/promo/tapkasa-spot-*.mp4`: reklamní spot s hudbou (25 s, na výšku
  1080x1920 i na šířku 1920x1080, CZ + EN). Použití: Play listing (nahrát
  na YouTube a vložit odkaz), web, sociální sítě. POZOR: jako App Preview
  na App Store použít nejde (Apple vyžaduje záznam obrazovky aplikace),
  tam patří jen snímky, případně později nahrávka z aplikace.
- Zdrojové soubory spotu a grafik: `store/promo/src/` (ad.html, promo.html,
  music.html + skripty), hudba `store/promo/music.wav`.
- `store/promo/badges/`: oficiální odznaky „Download on the App Store"
  (SVG, Apple zveřejňuje česky jen přes svůj generátor po přihlášení,
  do té doby platí anglická verze) a „Získejte/Rozjeďte to na Google Play"
  (CZ i EN PNG). Odznaky patří na web, do videí a inzerce; do snímků
  obrazovky v obchodech se nevkládají. Spot je má v závěrečné scéně.
