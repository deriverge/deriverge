// Angličtina: en-US (USA; „cash register“, „booth“) a en-GB (Británie a celá Evropa jako druhý indexovaný jazyk; „till“, „stall“).
// Americká verze říká hned v úvodu, že aplikace prodej počítá a eviduje, karty nebere a daň k ceně nepřipočítává.
const LINKS = `Terms of Use: https://www.deriverge.com/tapkasa/terms.html
Privacy Policy: https://www.deriverge.com/tapkasa/privacy.html`;
const wn = (cup) => ({
  wn108: `• Deposits: add a ${cup} deposit as an item and return it with one tap. Your stats show deposits taken and paid back separately.
• No surprise at the limit: the free version tells you in good time before the daily limit.
• No signal at the stall? You can still finish the open sale and get a one-time reserve of 10 extra payments.`,
  wn109: `Fixes and polish for the market season.

New since 1.0.8:
• Deposits: add a ${cup} deposit as an item and return it with one tap.
• The free version tells you in good time before the daily limit.
• No signal at the stall? You can still finish the open sale and get a one-time reserve of 10 extra payments.`,
});
export const us = {
  stores: { as: 'the App Store', gp: 'Google Play' },
  as: {
    locale: 'en-US',
    name: 'Tapkasa: Booth Cash Register',
    subtitle: 'For craft fairs and bake sales',
    keywords: 'simple,vendor,market,stall,concession,stand,farmers,tracker,pos,offline,order,queue,fundraiser,tally',
  },
  play: {
    locale: 'en-US',
    title: 'Tapkasa: Booth Cash Register',
    shortXmas: 'Cash register for holiday bazaars and craft fairs. No card processing, offline.',
    shortYear: 'Cash register for bake sales and craft fairs. No card processing, works offline.',
  },
  // Propagační text je první, co člověk na stránce čte: hned řekne, co aplikace neumí (karty, daň navíc), ať si ji nestahují lidé, kteří čekají platební terminál s výpočtem daně.
  promoXmas: 'Holiday bazaar, bake sale or craft fair? Tap items, get the change, see your totals. No card processing (cash or your own reader), prices include tax. Works offline.',
  promoYear: 'Bake sale, fundraiser or craft fair? Tap items, get the change, see your totals. No card processing (cash or your own reader), prices include tax. Works offline.',
  ...wn('cup or mug'),
  desc: (store) => `A simple cash register for bake sales, school fundraisers, concession stands and craft fairs. It adds up each sale, works out the change and keeps your totals. It does not process cards and does not add sales tax: take cash, run cards on your own reader and enter prices with tax included.

Type in your menu and start ringing up sales in two minutes: no sign-up, no account, no internet. No money passes through the app, so there is nothing to verify, nothing that can be frozen and no transaction fees.

A second phone shows numbered orders and reads them aloud. Cup and mug deposits take one tap. Free for 10 sales a day; try Tapkasa Pro free for 14 days to cover a whole event.

SELL IN THREE TAPS
• Every item is a color card. Your helpers spot it faster than they can read the name.
• Tap to add an item to the sale; press and hold to take one off.
• "+ Other amount" covers anything that is not on the menu.
• Saved the wrong sale? One tap undoes it.

CASH AND CARD
• For cash, enter what the customer hands you and Tapkasa shows the change.
• For card, charge the amount on your own card reader and just confirm it in the app.

DEPOSITS
• A cup or mug deposit is a card like any other; the deposit return is a card with a negative price.
• A return is taken off the total. A sale with only returns does not count toward the daily limit and does not go to the order queue.
• Your stats show deposits taken and deposits paid back separately.

ORDER QUEUE AND COUNTER
• Every paid sale becomes a numbered order.
• Switch a second phone or tablet to the Counter role: orders appear on it by themselves, you tick items off and "Served" closes the order.
• The counter device can read new orders aloud.
• Two iPhones, or two Android phones (Android 13 or later), pair without internet. An iPhone and an Android phone need internet to pair.

TOTALS AND CLOSE-OUT
• Total sales, cash and card, items sold per product.
• Sales summary as a PDF for any period, with your business details and a breakdown of the tax included in your prices if you need one.
• Run several events side by side; closing an event moves it to the archive.
• 9 languages and 33 currencies.

YOUR DATA STAYS WITH YOU
• Everything stays on your device. No accounts, no analytics, no ads.
• Save a backup to a file for free and restore it any time, also on a new phone.
• Losing signal never stops a sale.

FREE AND PRO
Free: the full register on one device, 10 paid sales a day. The app tells you in good time before you reach the limit. If you have no signal at that moment, you can still finish the open sale and get a one-time reserve of 10 extra payments.
Tapkasa Pro (subscription): unlimited sales and pairing with a second device. One subscription covers the booth; the counter device connects for free. New subscribers get a 14-day free trial. Billed through ${store}; cancel any time in your account settings.

WHAT TAPKASA IS NOT
• It does not process payments and it is not a card reader.
• It does not add sales tax at checkout. Enter your prices with tax included.
• It is not a certified fiscal cash register. Use it where the rules allow: clubs, school and charity events, internal records.
• It does not track inventory or do bookkeeping.

${LINKS}`,
};
export const gb = {
  stores: { as: 'the App Store', gp: 'Google Play' },
  as: {
    locale: 'en-GB',
    name: 'Tapkasa: Market Stall Till',
    subtitle: 'Christmas markets, craft fairs',
    // Druhá polovina jsou německá slova: en-GB se indexuje i v Německu a Rakousku. Jen výrazy, které obchod našeptává (měření 23. 11.).
    keywords: 'cash,register,pos,fete,bake,sale,car,boot,school,vereinskasse,wechselgeld,rückgeldrechner,kassieren',
  },
  // Google Play: en-GB si bere texty en-US (obchod je dosadí sám), vlastní listing zatím nezakládáme.
  play: null,
  promoXmas: 'Christmas market, craft fair or school fete? Type in your menu and sell with no sign-up and no internet. Mug deposits in one tap, numbered orders on a second phone.',
  promoYear: 'Market stall, craft fair or school fete? Type in your menu and start selling with no sign-up and no internet. Cup deposits in one tap, numbered orders on a second phone.',
  ...wn('mug or cup'),
  desc: (store) => `A simple till for market stalls, Christmas markets, craft fairs and school fetes. It adds up each sale, works out the change and keeps your takings. It does not process card payments: cash goes in your cash box and cards go through your own card reader.

Type in your menu and start selling in two minutes: no sign-up, no account, no internet. No money passes through the app, so there is nothing to verify, nothing that can be frozen and no transaction fees.

A second phone shows numbered orders and reads them aloud. Mug and cup deposits take one tap. Free for 10 sales a day; try Tapkasa Pro free for 14 days to cover a whole market.

SELL IN THREE TAPS
• Every item is a colour card. Your helpers spot it faster than they can read the name.
• Tap to add an item to the sale; press and hold to take one off.
• "+ Other amount" covers anything that is not on the menu.
• Saved the wrong sale? One tap undoes it.

CASH AND CARD
• For cash, enter what the customer hands you and Tapkasa shows the change.
• For card, charge the amount on your own card reader and just confirm it in the app.

DEPOSITS
• A mug or cup deposit is a card like any other; the deposit return is a card with a negative price.
• A return is taken off the total. A sale with only returns does not count towards the daily limit and does not go to the order queue.
• Your stats show deposits taken and deposits paid back separately.

ORDER QUEUE AND COUNTER
• Every paid sale becomes a numbered order.
• Switch a second phone or tablet to the Counter role: orders appear on it by themselves, you tick items off and "Served" closes the order.
• The counter device can read new orders aloud.
• Two iPhones, or two Android phones (Android 13 or later), pair without internet. An iPhone and an Android phone need internet to pair.

TAKINGS AND CLOSE-OUT
• Total takings, cash and card, items sold per product.
• Sales summary as a PDF for any period, with your details and a VAT breakdown if you need one.
• Run several events side by side; closing an event moves it to the archive.
• 9 languages and 33 currencies.

YOUR DATA STAYS WITH YOU
• Everything stays on your device. No accounts, no analytics, no ads.
• Save a backup to a file for free and restore it any time, also on a new phone.
• Losing signal never stops a sale.

FREE AND PRO
Free: the full till on one device, 10 paid sales a day. The app tells you in good time before you reach the limit. If you have no signal at that moment, you can still finish the open sale and get a one-off reserve of 10 extra payments.
Tapkasa Pro (subscription): unlimited sales and pairing with a second device. One subscription covers the stall; the counter device connects for free. New subscribers get a 14-day free trial. Billed through ${store}; cancel any time in your account settings.

WHAT TAPKASA IS NOT
• It does not process payments and it is not a card reader.
• It is not a certified fiscal cash register. Use it where the rules allow: clubs, school and charity events, internal records.
• It does not do stock control or bookkeeping.

${LINKS}`,
};
