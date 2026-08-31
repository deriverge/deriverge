# Tapkasa, store listing copy (English)

Secondary localization for App Store (en-US / en-GB) and Google Play (en-US).
All lengths verified; limits noted per field.

**Honesty note:** the app's interface is currently Czech-only. The English
listing says so explicitly, reviewers and buyers must not be surprised.

---

## App Store (App Store Connect)

### App name (30-char limit)

```
Tapkasa - Pop-up Point of Sale
```

*(Exactly 30 characters, at the limit; if the form rejects it, fall back to `Tapkasa - Pop-up POS` (20) or plain `Tapkasa` (7).)*

### Subtitle (30-char limit)

```
The pop-up point of sale
```

*(24 characters.)*

### Promotional text (170-char limit, editable without a new build)

```
A point of sale for market stalls, pop-ups and festivals. Colour cards, an order queue, revenue at a glance. Works offline, your data stays on your device.
```

*(156 characters.)*

### Keywords (100-char limit, comma-separated, no spaces after commas)

```
pos,register,till,cashier,market,stall,festival,vendor,popup,orders,offline,sales,checkout,counter
```

*(98 characters. Do not repeat "Tapkasa", "point" or "sale", the name and subtitle are indexed on their own.)*

### Category

- **Primary: Business**
- Secondary: Food & Drink (most target sellers run food/coffee stalls); Utilities as an alternative.
- *(We advise against "Shopping": on the App Store it targets consumers who shop, not sellers.)*

### Description (4,000-char limit; ~2,500 target)

```
Tapkasa is a point of sale that fits in your pocket, for the coffee stall, the school fair, the festival bar, the pop-up that lives for one weekend. Open the app, type in your menu, start selling. No sign-up, no account, no internet needed.

Tapkasa RECORDS sales, it does not process payments. You take cash into your cash box and cards on your own card terminal; Tapkasa does the counting, keeps the order queue moving and tells you at the end of the day how much you took.

A SALE IN THREE TAPS
• Every product is a colour card, staff recognise it before they can read the name. 14 curated colours, or mix your own on a colour wheel.
• Tap to add an item to the bill; press and hold for a second to take it off again. A progress bar fills while you hold, so it never happens by accident.
• "+ Custom amount" handles anything that is not on the menu.
• Saved the wrong bill? One tap undoes it.

CASH AND CARD
• For cash, type what the customer handed you and Tapkasa shows the change to give back.
• For card, you charge the amount on your own terminal and simply confirm it.

ORDER QUEUE
• A paid bill does not disappear, it joins the queue as a numbered order.
• Tick items off as you prepare them (multi-item lines count 1/2, 2/2); "Served" closes the order, and it can be reopened.
• The number of waiting orders is always visible in the header.

TWO DEVICES: TILL AND PICKUP
• Switch a second device to the Pickup role: it only receives orders and ticks them off, nobody can ring up a sale on it by mistake.
• Pairing takes a minute: one device creates a code, the other types it in.
• The pickup device can read new orders aloud, so staff never have to look at the screen.
• Bonus: the paired device keeps a copy of the sales, a free backup.

OVERVIEW AND CLOSE-OUT
• Total revenue, cash/card split, and pieces sold per product.
• Summary tax document for any period: with your business details, sent by e-mail or printed.
• Copy the summary as plain text, straight into a message to your accountant.
• "Close event" moves the takings into the archive and resets the till for the next event.

YOUR DATA IS YOURS
• Everything stays on your device, saved in two independent copies.
• No accounts, no analytics, no ads.
• The backup is plain text, copy it into your notes or an e-mail and restore from it any time.
• Works fully offline; losing signal never stops a sale.

FREE AND PRO
Free: the complete till on one device, up to 10 paid bills per day, enough for a small event.
Tapkasa Pro (subscription): unlimited bills and pairing of a second device. Billed through the App Store; cancel any time in your account settings.

Please note: the app's interface is currently in Czech. Tapkasa does not do bookkeeping or issue tax documents, it is a fast till for sales that are counted on a scrap of paper today.
```

*(2,705 characters, verified by script, see note at the end of this file.)*

### What's New in 1.0

```
The first release of Tapkasa, the pop-up point of sale:
• colour product cards and a sale in a few taps
• change calculator for cash payments
• order queue with a tick-off checklist
• Till and Pickup roles on two paired devices
• spoken order announcements
• revenue overview, copyable summary and an archive of closed events
• everything offline, data stays on your device
```

### Support & privacy URLs

- Support URL: `[DOPLŇ: support page URL, e.g. https://www.deriverge.com/tapkasa/]`
- Privacy policy URL: `[DOPLŇ: URL where store/privacy-policy-en.md is published]`

---

## Google Play (Play Console)

### App name (30-char limit)

```
Tapkasa - Pop-up Point of Sale
```

### Short description (80-char limit)

```
The pop-up point of sale for stalls, markets and festivals. Works offline.
```

*(74 characters.)*

### Full description (4,000-char limit)

Use the App Store description above, it fits the limit, and Play indexes
search terms from the description itself ("point of sale", "market stall",
"festival", "order queue" are all present). Single change: end the
subscription sentence with "…Billed through Google Play" instead of
"…through the App Store".

### Category and tags

- **App category: Business** *(not Shopping, that category is for consumer shopping apps)*
- Tags: Point of sale, Small business, Events

### Release notes 1.0

Same text as "What's New in 1.0" above (500-char limit; the text is ~370 characters, fits).

---

## Length verification note

All limited fields were counted programmatically: name 30/30 (at the limit, have the 20-char fallback ready), subtitle 24/30, promo 156/170, keywords 98/100, short description 74/80. Recount after any edit (Unicode length; the em dash counts as 1).
