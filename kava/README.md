# Kasa na stánek

Jednoduchá pokladna pro prodej na akci — karty položek, platba hotově nebo kartou,
přehled tržby. Jeden soubor, žádný backend, žádná registrace.

Po nasazení běží na `https://www.deriverge.com/kava/`.

## Jak se to ovládá

1. **Prodej** — klepnutím na kartu přidáš položku na účet, dalším klepnutím další kus.
   **Podržením karty na vteřinu** ta jedna položka z účtu zmizí — na kartě se
   při držení plní pruh, takže omylem to nejde. Zbytek účtu zůstane.
   Souhrn dole ukáže počet a částku; klepnutím na něj se účet rozbalí a jde upravovat
   po kusech. `+ Jiná částka` otevře klávesnici pro cokoliv mimo menu.
2. **Zaplatit** — vyskočí částka a dvě tlačítka. U *Hotově* si můžeš naťukat, co ti
   zákazník dal, a aplikace spočítá, kolik vrátit. Potvrdíš `Hotovo`.
   Špatně uložený účet jde hned vrátit tlačítkem *Vrátit zpět* v liště.
3. **Přehled** — tržba celkem, rozpad hotově/kartou, kolik kusů které položky se
   prodalo a za kolik, plus seznam účtenek (každou lze smazat).
   `Zobrazit souhrn` vyplivne text ke zkopírování. `Uzavřít akci` odloží tržbu do
   archivu a vynuluje kasu pro další prodej.
4. **Menu** — název akce, položky a ceny. Ukládá se průběžně. Změna ceny neovlivní
   už uložené účtenky.

## Data

Všechno zůstává v zařízení, nikam se nic neodesílá. Kasa si data drží ve třech
nezávislých kopiích, aby o ně restart ani vybitá baterie nepřipravily:

| Kde | Kdy se zapisuje | K čemu |
|---|---|---|
| `localStorage`, klíč `kavakasa.v1` | při každé změně | běžné čtení i zápis |
| IndexedDB `kavakasa` | při každé změně (se zpožděním 0,3 s) | záchrana, když prohlížeč localStorage zahodí |
| `Documents/kasa.json` | při každé změně | jen v nativní aplikaci, viz `../ios/` |

Při startu se kasa načte z localStorage. Když je prázdný, ale v IndexedDB něco
je, obnoví se odtamtud a napíše hlášku. V nativní aplikaci má přednost soubor.

Menu → **Záloha dat** vypíše celý obsah kasy jako text ke zkopírování a umí ho
zase načíst zpátky. To je poslední záchrana i způsob, jak data přenést jinam.

Co pořád platí:

- Data patří **jednomu zařízení**. Dvě obsluhy na dvou zařízeních = dvě
  oddělené statistiky, na konci se sčítají ručně.
- Nepoužívej anonymní okno — po zavření je pryč.
- Odinstalace z plochy nebo smazání dat webu smaže i tržbu.

## Offline

`sw.js` cachuje appku, takže po prvním otevření funguje i bez signálu. Prodeje se
ukládají lokálně, takže výpadek sítě prodej nezastaví.

## Instalace do zařízení

iPhone / iPad: otevřít v Safari → Sdílet → **Přidat na plochu**. Spustí se na
celou obrazovku bez adresního řádku, s vlastní ikonou a vlastním oknem
v přepínači aplikací. Android: Chrome → nabídka → **Přidat na plochu**.

Kdo chce opravdovou nativní aplikaci bez jakéhokoliv webu, najde ji v `../ios/` —
tentýž kód zabalený do iOS aplikace, kterou lze nahrát z Xcode přímo do iPadu.

## Rozvržení

Do 520 px dva sloupce karet, nad 700 px (iPad na výšku) čtyři a nad 1000 px
(iPad na šířku) pět, s většími kartami i písmem. Platební okno je na telefonu
lišta u spodní hrany, na tabletu vycentrovaný dialog.

## Struktura

| Soubor | K čemu |
|---|---|
| `index.html` | celá aplikace (styly, markup i logika) |
| `sw.js` | service worker pro offline režim |
| `manifest.webmanifest` | ikona a režim celé obrazovky po přidání na plochu |

Blok mezi `<!-- APP:START -->` a `<!-- APP:END -->` v `index.html` je samostatně
přenositelný — jde vložit kamkoliv jinam bez zbytku stránky.
