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
