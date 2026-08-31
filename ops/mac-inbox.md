# Pokyny od koordinující session (aktualizace 1)

1. **Ověřte, na jaké Xcode Mac stačí, než ho uživatel začne stahovat**:
   `sw_vers` (verze macOS) a `sysctl hw.model` (model). Pro odeslání do
   App Store je dnes potřeba Xcode 15+ (ideálně 16), který vyžaduje
   novější macOS. Pokud macOS nestačí, zjistěte, zda jde na tomto
   modelu aktualizovat (Software Update), a napište to uživateli i do
   logu. Kdyby se ukázalo, že Xcode na tomto stroji nerozjedeme,
   napište do logu `BLOKUJE: Xcode neproveditelný` a build vyřešíme
   plánem B (cloudové sestavení přes Codemagic s App Store Connect API
   klíčem), ten zatím nespouštějte.
2. **Nečekejte na Xcode a pokračujte fázemi 2, 3 a 5** (RevenueCat,
   App Store Connect, Google Play Console): jsou čistě prohlížečové.
   Jakmile uživatel potvrdí restart Chromu s ladicím portem, jeďte.
3. Po vložení veřejných klíčů RevenueCat do `mobile/billing.js`
   commitněte do `main` a spusťte znovu `./sync-web.sh && npx cap sync ios`,
   ať je projekt připravený na build hned, jak Xcode bude.
4. V App Store Connect založte i **App Store Connect API klíč**
   (Users and Access → Integrations, role App Manager), uložte .p8 do
   `~/.appstoreconnect/private_keys` a do logu zapište Key ID a Issuer ID
   (ne obsah souboru). Hodí se pro nahrávání buildů i pro případný plán B.

# Pokyny od koordinující session (aktualizace 2)

- **Kontaktní e-mail podpory je `info@deriverge.com`.** Použijte ho všude,
  kde konzole chtějí veřejný kontakt: App Store Connect (App Information,
  Support URL https://www.deriverge.com/kava/, kontaktní e-mail
  info@deriverge.com), Google Play (Store listing → App support → e-mail,
  ten je veřejný). Aplikace i stránky privacy/terms už adresu nesou,
  na main je nový commit, udělejte git pull.

# Pokyny od koordinující session (aktualizace 3)

- Na main přibyly marketingové podklady párování: po git pull najdete
  `store/screenshots/pairing-*.png` (zařaďte jako druhý snímek v App Store
  Connect i Play, CZ a EN verze do příslušných lokalizací) a
  `design/feature-graphic-pairing-cs.png` (nahrajte jako feature graphic
  v Play místo původní). Reklamní spot `store/promo/*.mp4` do Play listing
  vyžaduje YouTube odkaz: požádejte uživatele, ať video nahraje na svůj
  YouTube kanál (nebo to s ním udělejte), a odkaz vložte do Store listing.
  Do App Store jako App Preview spot nenahrávejte, Apple tam chce záznam
  obrazovky aplikace.

# Pokyny od koordinující session (aktualizace 4)

Log přečten, skvělá práce. Reakce a další kroky:

1. **git pull na main**: přibyly finální spoty s odznaky obchodů
   v závěru (`store/promo/*.mp4`, přesná synchronizace zvuku), oficiální
   odznaky ke stažení (`store/promo/badges/`) a hlavně **tabletové
   snímky 9:16 pro Play**: `store/screenshots/ptablet-*.png`
   (1440x2560), přesně kvůli vámi nahlášenému poměru stran.
2. **RevenueCat roční balíček**: ruční krok podle vašeho návodu ať
   provede uživatel, potom označte offering `default` jako current.
3. **App Store Connect API klíč**: až uživatel zkopíruje
   `AuthKey_MTMP9A7SKR.p8` do `~/.appstoreconnect/private_keys`,
   ověřte ho (`xcrun altool --list-apps` nebo notarytool) a klíč
   `ABWJD553V4` nechte uživatele revokovat, ať neleží ladem.
4. **iOS build**: po přihlášení Apple ID v Xcode (uživatel) proveďte
   archiv a nahrání do TestFlightu klíčem `MTMP9A7SKR`.
5. **ASC verze 1.0**: při vyplňování médií zařaďte jako druhý snímek
   `store/screenshots/pairing-iphone67-cs.png` (a EN variantu do
   anglické lokalizace), iPad sekce dostane `pairing-ipad129-*`.
6. **Play grafika**: pokud file input dál odmítá vstup, nechte nahrání
   na uživateli přetažením; seznam souborů máte v logu, doplňte k němu
   `store/screenshots/pairing-play-cs.png` a tabletové `ptablet-*`.
7. **Trial u ročního předplatného**: dokončete i Introductory Offer
   (2 týdny) u `tapkasa.pro.yearly`, v logu chybí potvrzení.
