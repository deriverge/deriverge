# English texts of the Tapkasa landing pages. Facts follow tapkasa/README.md and the app texts (version 1.0.8).
# No prices (they come from the stores), no fiscal promises, no long dashes. `sections` bodies are trusted HTML.

T = dict(
    html_lang='en', hreflang='en', og_locale='en_US', name='English', currency='USD',
    gp_badge='badge-googleplay-en.png', as_alt='Download on the App Store', gp_alt='Get it on Google Play',
    brand_sub='Pocket POS', menu='Language',
    try_btn='Try it in your browser',
    qr_alt='QR code to download the Tapkasa app',
    qr_text='Point your phone camera at the code to get Tapkasa.',
    note='Free for 10 paid bills a day. No sign-up.',
    sticky='Pocket POS for stalls',
    ld_desc='A simple point of sale on your phone for market stalls, craft fairs, school events and fundraisers. It '
            'works out change, queues orders, tracks cup deposits and works offline. Data stays on the device.',
    offer='Free for 10 paid bills a day. Tapkasa Pro is an in-app subscription (monthly or yearly).',
    h_how='How it works',
    how=[
        ('Type in your menu', 'Each item gets a name, a price and a colour. It takes a few minutes at home, or start '
                              'from the sample menu.'),
        ('Tap the cards', 'A tap adds one, a long press takes one off. The amount due is always at the bottom.'),
        ('Cash or card', 'For cash, Tapkasa works out the change. Take cards on your own reader and just mark the '
                         'sale as card in Tapkasa.'),
    ],
    h_feat='What Tapkasa does',
    feats=[
        ('Change without mental maths', 'Tap the note you were handed and see what to give back.'),
        ('Numbered order queue', 'Every paid bill gets a number and waits in the queue until you mark it as served.'),
        ('Till and pickup on two phones', 'A second device shows the orders and can read them aloud. Linking devices '
                                          'is part of Tapkasa Pro.'),
        ('Works with no signal', 'Everything runs on the phone. Two iPhones or two Android phones link up even '
                                 'without internet.'),
        ('Refundable deposits', 'A cup or mug deposit and its return as separate items, kept apart from your sales in '
                                'the totals.'),
        ('Your data stays with you', 'No account and no cloud. Save a backup file wherever you like.'),
    ],
    h_shots='What Tapkasa looks like',
    shot_alts=['Tapkasa selling screen: coloured item cards with prices and the amount due',
               'Numbered order queue on a second phone',
               'Sales summary with a tax breakdown'],
    h_not='What Tapkasa is not',
    nots=[
        'It is not a certified or fiscal cash register and it reports nothing to tax authorities. The sales summary '
        'is not a tax invoice or a customer receipt.',
        'It does not process card payments. You take cards on your own reader and Tapkasa only records the sale.',
        'It does not print receipts or tickets.',
    ],
    not_p='For stalls, fairs and occasional selling that is usually all you need. Check with your accountant or tax '
          'office which rules apply to you.',
    h_price='What it costs',
    price=[
        'Free: the whole menu, totals, deposits and data backup on one device, with 10 paid bills a day. A bill that '
        'only returns a deposit does not count towards the limit.',
        'Tapkasa Pro: unlimited bills and linking the till with a pickup device. It is a monthly or yearly '
        'subscription through the App Store or Google Play, with a 14-day free trial for new subscribers. You see '
        'the price in your currency in the app before you buy, and you can cancel any time in your store account.',
        'One subscription is enough for a stall: the second phone joins a device with Tapkasa Pro for free.',
    ],
    h_faq='Questions people ask',
    faq=[
        ('Is Tapkasa free?',
         'Yes, for up to 10 paid bills a day on one device. Unlimited bills and linking two devices need the Tapkasa '
         'Pro subscription, which new subscribers can try free for 14 days.'),
        ('Is it a certified or fiscal cash register?',
         'No. Tapkasa counts and records your sales, but it is not a certified register, sends nothing to tax '
         'authorities and does not issue tax invoices.'),
        ('Where is my data?',
         'Only on your device. Tapkasa has no accounts and no cloud. You can save a backup file and load it on a new '
         'phone.'),
        ('Which languages and currencies does it support?',
         'Nine languages (English, German, French, Spanish, Italian, Portuguese, Polish, Czech and Slovak) and 33 '
         'currencies, each with its own notes for working out change.'),
    ],
    cta_h='Try Tapkasa before your next event',
    h_more='More guides',
    f_support='Support', f_privacy='Privacy', f_terms='Terms', f_app='Open Tapkasa in the browser',
    f_langs='Languages', f_operator='Operator',
    pages=dict(
        stall=dict(
            path='pos.html', card='Market stall POS',
            title='Market Stall POS App: Sell With No Signal | Tapkasa',
            desc='A simple POS for your market stall, on your phone: coloured item cards, change worked out for you, '
                 'a numbered order queue on a second phone and cup deposits. Works offline, free for 10 bills a day.',
            h1='A market stall POS that fits in your pocket',
            eyebrow='For iPhone, Android and the browser',
            lede='Type in your menu, tap the coloured cards and Tapkasa does the counting: what to charge, what '
                 'change to give and what you took today. No sign-up, no hardware and no internet needed.',
            sections=[
                ('What it looks like at the stall',
                 '<p>A customer asks for two mulled wines and a pastry. You tap mulled wine twice, the pastry once, '
                 'and the amount is at the bottom of the screen. They hand you a twenty, you tap 20 and Tapkasa shows '
                 'the change. It takes a few seconds and nobody does sums in their head, not even a helper on their '
                 'first shift.</p>'),
                ('Two phones: till and pickup',
                 '<p>When a queue builds up, one phone takes the money and the other shows the orders with numbers. '
                 'The pickup phone ticks off what is ready and can read new orders aloud, so you do not have to look '
                 'at a screen with your hands full. Two iPhones or two Android phones link directly with no '
                 'internet; an iPhone and an Android phone need a connection.</p>'),
                ('Deposits on cups and mugs',
                 '<p>The “+ Add deposit” button adds two items to your menu: Deposit and Deposit return. A returned '
                 'cup is taken off the bill, and the totals show deposits taken and returned separately, so they '
                 'never get mixed up with your sales.</p>'),
                ('Know your takings at the end of the day',
                 '<p>The overview shows total sales, cash and card separately, and how many of each item you sold. '
                 'You can save a sales summary as a PDF, for example for your bookkeeper.</p>'),
            ],
            faq=[
                ('Do I need an internet connection?',
                 'No. Selling, totals and backups all run on the phone. You only need internet to download the app, '
                 'to buy Tapkasa Pro and to link an iPhone with an Android phone.'),
                ('Can a helper or volunteer use it?',
                 'Yes. A sale is a tap on a coloured card and a choice of Cash or Card. An item added by mistake '
                 'comes off with a long press.'),
            ],
        ),
        xmas=dict(
            path='christmas-market-till.html', card='Christmas market and craft fair till',
            title='Christmas Market and Craft Fair Till App | Tapkasa',
            desc='A till on your phone for Christmas markets and craft fairs: one tap per item, mug deposits, change '
                 'worked out for you. Works with no signal, no sign-up, free for 10 bills a day.',
            h1='A till for Christmas markets and craft fairs',
            eyebrow='Christmas markets, craft fairs, winter fêtes',
            lede='The square is packed, the mobile network is struggling and there is a queue at your stall. Tapkasa '
                 'runs on your phone with no internet, works out the change and keeps track of mug deposits. You can '
                 'set it up in a few minutes.',
            sections=[
                ('Mug deposits without the muddle',
                 '<p>In Menu, tap “+ Add deposit” and enter the amount. Tapkasa creates two items: Deposit and '
                 'Deposit return. Add the deposit with the mulled wine, tap the return when the mug comes back and '
                 'it is taken off the bill. If a customer is only returning a mug, Tapkasa shows how much to hand '
                 'back.</p><p>The totals list deposits taken and returned separately, so at closing time you know '
                 'how many mugs are still out and what your real sales were.</p>'),
                ('When the signal drops',
                 '<p>Selling, change and totals all run on the phone itself. Tapkasa does not log in anywhere and '
                 'does not check anything online, so a busy network or a used-up data plan cannot stop you in the '
                 'middle of the rush.</p>'),
                ('Handmade goods and one-off prices',
                 '<p>Save your regular items as coloured cards. For a one-off piece that is not on the menu, tap '
                 '“+ Other amount”, type the price and carry on. At the end of the day the overview shows what sold '
                 'and how many.</p>'),
                ('Tips for a cold day',
                 '<ul><li>Round your prices so change is easy.</li>'
                 '<li>Set up the menu at home in the warm and put your best sellers at the top.</li>'
                 '<li>Bring a power bank. The screen stays on while you sell, and batteries drain faster in the '
                 'cold.</li>'
                 '<li>Save a backup file before your first market day.</li></ul>'),
            ],
            faq=[
                ('Do deposit returns count towards the free daily limit?',
                 'No. A bill that only returns a deposit does not count towards the 10 paid bills a day.'),
                ('Is the free version enough for a Christmas market?',
                 'For a small stall with a handful of sales a day, yes. For a busy market Tapkasa Pro makes sense: '
                 'new subscribers get the first 14 days free, which covers two market weekends. Tapkasa warns you '
                 'before you reach the limit.'),
            ],
        ),
        club=dict(
            path='bake-sale-cash-register.html', card='Bake sale and school fair cash register',
            title='Bake Sale and School Fair Cash Register App | Tapkasa',
            desc='A cash register on your phone for bake sales, school fairs and fundraisers: volunteers tap the '
                 'items, the app works out change and the treasurer gets the totals as a PDF. No sign-up.',
            h1='A cash register for bake sales, school fairs and fundraisers',
            eyebrow='PTA events, club nights, church fêtes, charity stalls',
            lede='Volunteers take turns at the table and the treasurer wants to know what came in. Tapkasa keeps the '
                 'prices, works out the change and adds up the takings on a phone. No sign-up and no training.',
            sections=[
                ('Any volunteer can run it',
                 '<p>Items are big coloured cards, so nobody scrolls through a list or does sums in their head. Tap '
                 'what the customer asked for, choose Cash or Card, and for cash the screen shows the change. '
                 'Changing shifts means handing over the phone.</p>'),
                ('Exact totals for the treasurer',
                 '<p>The overview shows total sales, cash and card separately, and how many of each item were sold. '
                 'Send the sales summary to the treasurer or the committee as a PDF. After the event, tap Close '
                 'event: the takings go to the archive and next time you start from zero.</p>'),
                ('No account, no verification, no fees',
                 '<p>Tapkasa asks for no registration, no charity number and no bank details, and it takes no cut '
                 'of what you raise. The money goes into your cash box. The data stays on the phone you use at the '
                 'table.</p>'),
                ('Bigger events: bar and kitchen',
                 '<p>At a dance or a summer fair one phone can take payments at the bar while another shows the '
                 'orders in the kitchen. One Tapkasa Pro subscription covers it, and new subscribers get a 14-day '
                 'free trial.</p>'),
            ],
            faq=[
                ('Is the free version enough for a school bake sale?',
                 'For a small sale, yes: 10 paid bills a day are free. If you expect more customers, start Tapkasa '
                 'Pro beforehand; new subscribers get a 14-day free trial.'),
                ('Does our club or PTA need to register?',
                 'No. You download Tapkasa and open it. There is no account to create and nothing to verify.'),
            ],
        ),
        festival=dict(
            path='festival-pos.html', card='Festival POS',
            title='Festival POS App: Order Queue on a Second Phone | Tapkasa',
            desc='A POS on your phone for festival stalls and food trucks: fast ordering, a numbered order queue, '
                 'till and pickup on two phones even with no internet. Try it in your browser right now.',
            h1='A festival POS that keeps the queue moving',
            eyebrow='Festivals, food trucks, gigs',
            lede='At a festival, speed is everything. Tapkasa cuts a sale down to a few taps, puts paid orders in a '
                 'numbered queue and links the till with the pickup point even where there is no signal.',
            sections=[
                ('An order in a few seconds',
                 '<p>Your menu is on coloured cards with the best sellers at the top. Tap what the customer asked '
                 'for and the amount is at the bottom. For cash, tap the note and Tapkasa shows the change.</p>'),
                ('Numbers instead of shouting',
                 '<p>Every paid bill gets a number. The pickup phone shows what to prepare, ticks off what is ready '
                 'and can read new orders aloud.</p>'),
                ('A field with no signal',
                 '<p>Two iPhones or two Android phones link directly, with no Wi-Fi and no mobile data. An iPhone '
                 'paired with an Android phone needs internet, so keep that in mind when you choose your '
                 'devices.</p>'),
                ('Cup deposits',
                 '<p>Add a cup deposit and its return as two items with the “+ Add deposit” button. The return is '
                 'taken off the bill and the totals keep deposits apart from sales.</p>'),
            ],
            faq=[
                ('Does linking two phones work without internet?',
                 'Between two iPhones or between two Android devices, yes, directly. An iPhone and an Android '
                 'device only link over the internet.'),
                ('Can I take card payments?',
                 'Yes, on your own card reader. In Tapkasa you just mark the sale as Card so that cash and card '
                 'totals add up.'),
            ],
        ),
    ),
)
