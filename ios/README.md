# Kasa jako nativní aplikace pro iPad / iPhone

Tenhle adresář dělá z kasy skutečnou aplikaci, která se instaluje na zařízení —
žádná webová stránka, žádný server, nic online. Appka nese celý svůj obsah
uvnitř a data si ukládá do souboru ve svém úložišti.

## Co k tomu potřebuješ

**Mac s Xcode.** Bez něj se iOS aplikace na zařízení nedostane — Apple jinou
cestu nemá. Xcode je zdarma z Mac App Storu.

Ke stažení do zařízení stačí **obyčejné Apple ID zdarma**, ale podpis pak platí
**7 dní** a po týdnu je potřeba appku z Xcode znovu nahrát (data zůstanou).
S placeným Apple Developer Programem (2 400 Kč / rok) platí podpis **rok**.

Pokud Mac po ruce není, použij verzi z `kava/` přidanou na plochu — chová se
stejně, jen se jednou musí načíst z internetu. Viz `kava/README.md`.

## Postup s XcodeGen (rychlejší)

```sh
brew install xcodegen
cd ios
./copy-web.sh
xcodegen generate
open Kasa.xcodeproj
```

## Postup bez XcodeGen (ruční, ~5 minut)

1. `cd ios && ./copy-web.sh`
2. Xcode → **File → New → Project → iOS → App**
   - Product Name: `Kasa`
   - Interface: **SwiftUI**, Language: **Swift**
   - Ulož kamkoliv mimo tenhle adresář.
3. Ve vytvořeném projektu **smaž** vygenerované `ContentView.swift`
   i `KasaApp.swift` (Move to Trash).
4. Přetáhni do projektu soubory `ios/Kasa/KasaApp.swift`,
   `ios/Kasa/KasaWebView.swift` a `ios/Kasa/Resources/index.html`.
   V dialogu zaškrtni **Copy items if needed** a **Add to target: Kasa**.
5. Klikni na `index.html` a v pravém panelu ověř, že má zaškrtnutou
   **Target Membership → Kasa**. Bez toho se appka spustí s prázdnou obrazovkou.
6. V nastavení targetu → **General**:
   - Supported Destinations: iPhone i iPad
   - Device Orientation: zapni na výšku i na šířku
7. **Signing & Capabilities** → Team: tvoje Apple ID.

## Nahrání do iPadu

1. Připoj iPad kabelem, odemkni ho a potvrď **Trust This Computer**.
2. V Xcode nahoře vyber jako cíl svůj iPad a dej **Run** (⌘R).
3. Při prvním spuštění iPad podpis odmítne. Jdi v něm do
   **Nastavení → Obecné → VPN a správa zařízení**, vyber svůj profil
   a dej **Důvěřovat**.
4. Appka je na ploše. Kabel ani Xcode už k jejímu spouštění nejsou potřeba.

iPad 5. generace (iPadOS 16.7) je v pohodě — projekt cílí na iOS 15 a výš.

## Kde jsou data

V souboru `Documents/kasa.json` uvnitř kontejneru aplikace. Zapisuje se při
každé změně účtu. Znamená to, že:

- restart, vybitá baterie ani zavření aplikace o data nepřipraví,
- data se berou s sebou do zálohy iPadu (iCloud i zálohy přes počítač),
- smaže je jedině odinstalace aplikace.

Navíc si kasa v Menu umí vypsat zálohu jako text, který jde zkopírovat
kamkoliv a kdykoliv z něj obnovit.

## Po úpravě appky

`kava/index.html` je zdroj pravdy. Když se v něm něco změní:

```sh
cd ios && ./copy-web.sh
```

a v Xcode znovu **Run**.

## Co vědět

Aplikace si tahá písma Archivo a JetBrains Mono z Google Fonts. Když je iPad
offline, vykreslí se systémovým písmem — kasa funguje úplně stejně, jen vypadá
o kousek obyčejněji. Kdyby to vadilo, dají se písma zabalit dovnitř.

Swift kód jsem nemohl zkompilovat — v prostředí, kde vznikal, není macOS.
Web uvnitř otestovaný je, obal je krátký a přímočarý, ale první build v Xcode
je zároveň jeho první ostrý test.
