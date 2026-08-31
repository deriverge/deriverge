# Zadání pro Claude session na Macu: vydání Tapkasy do obchodů

Jste ruce na Macu. Cloudová session připravila aplikaci i podklady;
vaším úkolem je nastavení obchodů a sestavení buildů. Uživatel sedí
u Macu, v prohlížeči je přihlášený do App Store Connect, Play Console
i RevenueCat a potvrdí dvoufázová ověření, když ho požádáte.

## Kontext

- Repozitář: `deriverge/deriverge`, větev `main` je aktuální (pracujte nad ní).
- Aplikace: `kava/index.html` (hotová pokladna Tapkasa, 9 jazyků, tarify
  Zdarma a Pro, testy zelené, běží na deriverge.com/kava/).
- Nativní obal: `mobile/` (Capacitor, bundle `com.deriverge.tapkasa`,
  RevenueCat adaptér v `mobile/billing.js`).
- Podklady: `store/checklist.md` (hlavní scénář), `store/monetization.md`
  (přesná ID, ceny, postupy krok za krokem), `store/listing-cs.md` a
  `store/listing-en.md` (texty), `store/screenshots/` (hotové snímky ve
  správných rozměrech), `store/apple-privacy-labels.md`,
  `store/google-data-safety.md`, `store/review-notes.md`.

## Úkoly v tomto pořadí

1. **Preflight**: `git pull`; ověřte `xcodebuild -version` (potřeba 15+),
   přihlášený tým v Xcode (Settings → Accounts), `node -v` (18+).
2. **RevenueCat** podle `store/monetization.md`, sekce 1: projekt Tapkasa,
   entitlement přesně `pro`, produkty `tapkasa.pro.monthly` a
   `tapkasa.pro.yearly`, offering `default` (balíčky `$rc_monthly`,
   `$rc_annual`). Veřejné SDK klíče (`appl_`, `goog_`) vložte do
   `mobile/billing.js` místo zástupných textů a commitněte do `main`.
3. **App Store Connect** podle `store/monetization.md` sekce 2 a checklistu:
   záznam aplikace (název `Tapkasa - Pokladna do kapsy`, bundle
   `com.deriverge.tapkasa`, primární jazyk čeština), subscription group
   Tapkasa Pro s oběma produkty ($4.99 a $39.99; pro Česko ruční ceny
   129 Kč a 990 Kč), 14denní free trial, texty z listingů, screenshoty ze
   `store/screenshots/`, App Privacy podle `apple-privacy-labels.md`,
   Privacy Policy URL `https://www.deriverge.com/kava/privacy.html`.
   Přihlaste účet do Small Business Programu.
4. **iOS build**: `cd mobile && npm ci && ./sync-web.sh && npx cap sync ios`,
   pak archiv a nahrání do TestFlightu (Xcode, nebo xcodebuild + App Store
   Connect API klíč; klíč uložte MIMO repozitář do
   `~/.appstoreconnect/private_keys`, do reportu pište jen cestu).
5. **Google Play** podle `store/monetization.md` sekce 3: záznam aplikace,
   obě předplatná (base plany `monthly`/`yearly`, offer `trial14`), ceny
   129 a 990 Kč pro CZ, Data safety podle `google-data-safety.md`, texty a
   snímky z listingů. Android build jen pokud je na Macu Android SDK;
   jinak poznamenejte a přeskočte.

## Pravidla

- Bankovní a daňové formuláře (Agreements, Payments profile) nevyplňujte;
  uživatele k nim jen naveďte a počkejte.
- Finální tlačítko odeslání k recenzi nemačkejte.
- Tajemství (.p8 klíče, keystore, service account JSON) nikdy do repozitáře.
- Texty směrem k uživateli pište vykáním a bez dlouhých pomlček.
- U přihlašování a 2FA požádejte uživatele přímo v terminálu.

## Reportování

Po každé dokončené fázi připište stručný záznam do `ops/mac-log.md` na
větvi `claude/mac-ops` a pushněte
(`git fetch origin claude/mac-ops && git checkout claude/mac-ops`; pro
práci na aplikaci se vracejte na `main`): co je hotové, co čeká na
uživatele, ID a cesty (nikdy obsah klíčů). Zásadní překážku uveďte
s prefixem `BLOKUJE:` a řekněte ji uživateli. Cloudová session log čte
a koordinuje další kroky.
