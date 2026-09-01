# Review Notes, Tapkasa (pro App Review)

Text níže je připravený k vložení do App Store Connect → App Review
Information → Notes (anglicky, recenzenti česky nečtou). Za ním následuje
interní komentář, co a proč tam je. Stejný text (zkrácený dle potřeby)
použijte i v Play Console, pokud si recenze vyžádá doplnění.

---

## Text pro pole „Notes" (zkopírovat)

```
WHAT THE APP IS
Tapkasa is an offline point-of-sale app for one-off events: market
stalls, school fairs, festival bars. The seller types in their menu
(product cards with prices), taps cards to build a bill, records the
payment, and the bill joins a numbered order queue that staff tick off
as they prepare items. A stats tab shows the day's revenue.

The interface ships in nine languages (Czech, Slovak, English, German,
French, Spanish, Italian, Polish, Portuguese). The language is chosen on
first launch and can be changed any time in Menu. Screenshots on the
product page are Czech; if you prefer English, pick English on the first
screen. A short Czech glossary in case you keep the default: Prodej =
Sell, Objednávky = Orders, Přehled = Overview, Menu = Menu/Settings,
Zaplatit = Pay, Hotově = Cash, Kartou = Card, Hotovo = Done, Vydáno =
Served, Uzavřít akci = Close event.

THE APP DOES NOT PROCESS PAYMENTS
Tapkasa only RECORDS that a sale happened. Cash is physically handed
over at the stall; for cards, the seller charges the amount on their own
separate card terminal and merely confirms it in the app. There is no
payment processing, no card entry, no payment SDK, and no connection to
any payment provider. The cash keypad exists only to calculate the
change to hand back.

NO ACCOUNTS / NO DEMO CREDENTIALS
There is no login and no server-side account. The app is fully usable
the moment it launches; demo products are pre-filled.

SUGGESTED TEST FLOW (2 minutes)
1. On the Prodej (Sell) tab, tap a few colour cards, items appear on
   the bill at the bottom. Press and hold a card for 1 second to remove
   that item again (a progress bar fills while holding).
2. Tap Zaplatit (Pay) → Hotově (Cash) → tap banknote buttons to enter
   the amount received; the change to return is computed. Tap Hotovo.
3. Open Objednávky (Orders): the paid bill is queued under a number.
   Tap it, tick off the items, tap Vydáno (Served).
4. Open Přehled (Overview): revenue total, cash/card split, per-item
   stats. Menu tab: edit products, prices, card colours; data backup.

DEVICE PAIRING (optional feature)
Two devices can pair (roles: till and pickup) to share the order queue.
Full pairing needs two devices, but a single device is enough to verify
the feature: in Menu, tap "Vytvořit nový kód" (Create code), then
"Otestovat spojení" (Test connection), the app sends a test message
through the relay and reports the round trip, which exercises the whole
transport path. Pairing exchanges order contents only (item names,
quantities, prices, ticket numbers, timestamps); no personal data is
involved, messages are relayed transiently (deleted within 12 hours),
and the feature is off unless the user enables it.

IN-APP PURCHASE (subscription "Tapkasa Pro")
Free tier: full functionality on a single device, limited to 10 paid
bills per calendar day, and device pairing is locked. The Pro
subscription (auto-renewable: tapkasa.pro.monthly, tapkasa.pro.yearly,
14-day free trial) removes the daily limit and unlocks pairing.

To see the paywall: either record 10 bills (any items, cash, Hotovo)
and start an 11th payment, the paywall appears instead of the payment
sheet, or open Menu and tap the pairing section. Purchases are
processed by StoreKit via RevenueCat; sandbox purchases work as usual.

DATA & PRIVACY
No accounts, no analytics, no ads. All sales data stays on the device.
The only data leaving the device: (a) anonymized purchase validation via
RevenueCat, (b) the optional pairing messages described above.
```

---

## Interní komentář (nevkládat do formuláře)

### Proč je tam odstavec o platbách

Aby recenze nezařadila aplikaci mezi zpracovatele plateb (Guideline
3.1.5(a), fyzické zboží se smí platit mimo IAP; aplikace sama žádné
platby nezpracovává, jen je eviduje). Explicitně řečeno: žádné platební
SDK, žádné zadávání karet. To předchází žádostem o licence platební
instituce apod.

### Proč vysvětlujeme párování „na jednom zařízení"

Recenzent typicky testuje na jednom zařízení a funkci „vyžadující dvě
zařízení" by mohl označit za nefunkční. Text říká: (1) co párování
dělá, (2) že tlačítko **Otestovat spojení** ověří celou přenosovou
cestu bez druhého zařízení (zpráva odejde na relay a vrátí se zpět,
aplikace ukáže výsledek), (3) že druhé zařízení pouze zrcadlí frontu, nic dalšího by recenzent neviděl. Pokud by přesto chtěli dvě zařízení:
stejný build na druhém zařízení, Menu → opsat kód → Spojit.

### IAP gating, co musí souhlasit s realitou buildu

Popsané chování (10 zaplacených účtů/den zdarma, párování jen s Pro,
paywall při 11. platbě a při otevření párování) musí být v odevzdaném
buildu skutečně implementované. Před odesláním ověřit, že:

- limit se počítá na kalendářní den a resetuje o půlnoci lokálního času,
- paywall nabízí oba produkty + obnovu nákupů (Restore purchases, Apple ji vyžaduje, Guideline 3.8),
- na paywallu jsou cena, délka trvání, Restore purchases a odkazy na
  Privacy Policy a Terms of Use (EULA), bez nich bývá zamítnutí 3.1.2.
  Aplikace to už splňuje (odkazy vedou na
  `https://www.deriverge.com/tapkasa/privacy.html` a `…/terms.html`).
- **Pokud v konzolích zapnete 14denní trial** (doporučeno
  v `monetization.md`), doplňte na paywall i řádek o trialu („14 dní
  zdarma, potom {cena}“), nativní platební dialog ho sice ukáže sám,
  ale recenzenti chtějí zmínku i v aplikaci.

### Přílohy k recenzi

- App Review Information → kontakt: [DOPLŇ: jméno, telefon, e-mail].
- Demo účet: nechat pole prázdné + zaškrtnout, že přihlášení není třeba.
- Volitelně přiložit 30s screen-recording testovacího průchodu (body
  1-4 výše), u utilit v cizím jazyce výrazně zrychluje schválení.

### Poznámka pro Play Console

Google recenze obvykle poznámky nečte předem; stejné informace vložit
do App content → App access → „All functionality is available without
special access" + doplnit instrukce (formulář „Any other instructions")
textem výše, hlavně sekce o platbách a párování.
