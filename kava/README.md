# Kasa na stánek

Jednoduchá pokladna pro prodej na akci — karty položek, platba hotově nebo kartou,
přehled tržby. Jeden soubor, žádný backend, žádná registrace.

Po nasazení běží na `https://www.deriverge.com/kava/`.

## Jak se to ovládá

1. **Prodej** — klepnutím na kartu přidáš položku na účet, dalším klepnutím další kus.
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

Všechno se ukládá do `localStorage` prohlížeče, klíč `kavakasa.v1`. Nikam se nic
neodesílá. Důsledky:

- Data patří **jednomu telefonu a jednomu prohlížeči**. Dvě obsluhy na dvou
  telefonech = dvě oddělené statistiky.
- Nepoužívej anonymní okno — po zavření je pryč.
- Odinstalace z plochy nebo smazání dat webu smaže i tržbu.

## Offline

`sw.js` cachuje appku, takže po prvním otevření funguje i bez signálu. Prodeje se
ukládají lokálně, takže výpadek sítě prodej nezastaví.

## Instalace do telefonu

iPhone: otevřít v Safari → Sdílet → **Přidat na plochu**. Spustí se na celou
obrazovku bez adresního řádku. Android: Chrome → nabídka → **Přidat na plochu**.

## Struktura

| Soubor | K čemu |
|---|---|
| `index.html` | celá aplikace (styly, markup i logika) |
| `sw.js` | service worker pro offline režim |
| `manifest.webmanifest` | ikona a režim celé obrazovky po přidání na plochu |

Blok mezi `<!-- APP:START -->` a `<!-- APP:END -->` v `index.html` je samostatně
přenositelný — jde vložit kamkoliv jinam bez zbytku stránky.
