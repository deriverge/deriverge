# Texts for the Fixbill language pages (/fixbill/ and /fixbill/<lang>/).
# Facts come from the app repo (fixbill-rel120: l10n/store/*.json, lib/core/countries.dart, docs/PLAN-1.2.0.md).
# Payment QR codes: QR Platba (SPAYD) in CZ, EPC in DE, AT, FR, BE, LU, NL, FI, IE; elsewhere only the QR code
# of the user's own PayPal or Stripe payment link. Only `h1` may contain HTML (<em>); everything else is escaped.
# No long dashes anywhere.

ICONS = ('doc', 'pen', 'qr', 'bank', 'bell', 'stack', 'users', 'tag')

EN = dict(
    code='en', path='', hreflang='en', html_lang='en', og_locale='en_US', name='English', legal='en',
    gp_badge='badge-googleplay-en.png', as_alt='Download on the App Store', gp_alt='Get it on Google Play',
    currency='USD',
    title='Fixbill: Estimate & Invoice App for Contractors (iPhone, Android)',
    desc='Estimates and invoices on your phone for contractors: PDF in two minutes, client signature on screen, payment QR codes and reminders. Free for 5 documents a month.',
    og_title='Fixbill: estimates and invoices for contractors',
    og_desc='Write the estimate on site, let your client sign on screen, add a payment QR code and see who has paid. '
            'No account, your data stays on your phone.',
    brand_sub='Estimates and invoices', menu='Language',
    eyebrow='For iPhone and Android',
    h1='Estimates and invoices for contractors, done in <em>two minutes</em>',
    lede='Made for contractors, tradespeople and small businesses. Write the estimate on site, let your client sign it '
         'on your screen and send it before you leave. Turn it into an invoice with one tap and see who has paid.',
    note='Free for 5 documents a month. No account needed.',
    hero_alt='Example invoice in Fixbill: bathroom remodel, three items, total $1,926.50, unpaid, with a QR code for '
             'the payment link. The client signed the estimate on screen.',
    mock=dict(biz='Your business', doc='Invoice INV-1042', chip='Unpaid', job='Bathroom remodel',
              lines=[('Wall tile installation', '120 sq ft × $12.00', '$1,440.00'),
                     ('Tile adhesive and grout', '1 × $96.50', '$96.50'),
                     ('Labor', '6 h × $65.00', '$390.00')],
              total_label='Total', total='$1,926.50', pay_b='Scan to pay',
              pay_s='QR code for your PayPal or Stripe link', sign='Estimate signed by the client'),
    h_feat='Everything for the job, right on your phone',
    cards=[
        ('doc', False, 'Estimates and invoices as PDF',
         'Pick a client, add work and materials from your price list and send a clean PDF with your logo straight '
         'from the job: by e-mail, in a messenger or with any app you choose. Four document templates.'),
        ('pen', True, 'Signed on the spot',
         'Your client signs the estimate right on your screen. Add job photos, then turn the accepted estimate into '
         'an invoice with one tap.'),
        ('qr', False, 'Payment link and QR code',
         'Add your own PayPal or Stripe payment link and every invoice gets a scan-to-pay QR code, with no extra fees '
         'from us. In Germany, Austria, France, the Benelux, Finland and Ireland invoices can also carry an EPC bank '
         'transfer QR code, and in the Czech Republic a QR Platba code.'),
        ('bank', True, 'Bank payments matched for you',
         'Import a bank statement (CAMT.053, MT940 or CSV). Fixbill matches payments to invoices by reference and '
         'amount and asks you about anything uncertain. Partial payments and overpayments too. Your bank data never '
         'leaves your phone.'),
        ('bell', False, 'Know who owes you',
         'Unpaid, part-paid and overdue invoices at a glance, an alert when an invoice becomes overdue and a polite '
         'reminder with one tap.'),
        ('stack', False, 'Deposits, credit notes, recurring',
         'Proforma invoices for deposits, final invoices that deduct them, credit notes and recurring invoices. Export '
         'everything for your accountant as PDF and CSV. 34 languages, set up for 49 countries.'),
    ],
    h_tpl='Free templates you can fill in online',
    tpl_sub='No app needed: fill in the form, check the preview and save a PDF. Nothing is uploaded.',
    h_price='Fair pricing', price_sub='No weekly plans and no price rises while you subscribe.',
    plans=[
        ('Free', '5 documents a month', 'Estimates and invoices for free, every month. Each one carries a small '
         '“Created with Fixbill” footer.', False),
        ('Fixbill Pro', 'Monthly, yearly or once', 'Unlimited documents without the footer, client e-signatures, job '
         'photos, bank payment matching, recurring invoices and the full export for your accountant. Pay monthly, '
         'yearly or once for life. If a free trial is offered, you will see it before you buy.', True),
        ('Price promise', 'Your price stays the same', 'We will not raise the price of your subscription while it '
         'stays active. Cancel any time in your App Store or Google Play account.', False),
    ],
    priv_h='Your data stays on your phone',
    priv_p='Fixbill needs no account. Your business profile, clients, items, documents, photos, signatures and bank '
           'statements are stored only on your device. We never see them.',
    priv_link='Read the privacy policy',
    checks=['No account, no analytics, no ads, no tracking.',
            'Documents leave your phone only when you share them, to the app or service you pick.',
            'Backups are files you save wherever you choose.',
            'Company lookup sends only the number you look up to a public registry.'],
    cta_h='Get Fixbill', cta_sub='Questions? Write to {mail}.',
    f_support='Support', f_privacy='Privacy', f_terms='Terms of use', f_operator='Operator',
    f_templates='Free templates', f_langs='Languages', en_suffix='',
    offer='Free download with 5 documents a month. Fixbill Pro is an in-app purchase: monthly, yearly or a one-time '
          'lifetime purchase.',
    ld_desc='Estimate and invoice app for contractors and small businesses: PDF estimates and invoices, client '
            'signatures, payment QR codes, bank payment matching, reminders. Data stays on the device.',
)

EN_GB = dict(EN)
EN_GB.update(
    code='en-gb', path='en-gb/', hreflang='en-GB', html_lang='en-GB', og_locale='en_GB', name='English (UK)',
    currency='GBP',
    title='Quote and Invoice App for Tradesmen and Sole Traders | Fixbill',
    desc='Quotes and invoices on your phone for tradesmen and sole traders: PDF in two minutes, customer signature on screen and reminders. Free for 5 documents a month.',
    og_title='Fixbill: quotes and invoices for tradesmen',
    og_desc='Write the quote on site, let your customer sign on screen, add a payment link QR code and see who has '
            'paid. No account, your data stays on your phone.',
    brand_sub='Quotes and invoices',
    h1='Quotes and invoices for tradesmen, done in <em>two minutes</em>',
    lede='Made for tradesmen, sole traders and small firms. Write the quote on site, let your customer sign it on '
         'your screen and send it before you leave. Turn it into an invoice with one tap and see who has paid.',
    hero_alt='Example invoice in Fixbill: bathroom refit, three items, total £720.50, unpaid, with a QR code for the '
             'payment link. The customer signed the quote on screen.',
    mock=dict(biz='Your business', doc='Invoice INV-0042', chip='Unpaid', job='Bathroom refit',
              lines=[('Wall tiling', '12 m² × £34.00', '£408.00'),
                     ('Adhesive and grout', '1 × £72.50', '£72.50'),
                     ('Labour', '6 h × £40.00', '£240.00')],
              total_label='Total', total='£720.50', pay_b='Scan to pay',
              pay_s='QR code for your PayPal or Stripe link', sign='Quote signed by the customer'),
    cards=[
        ('doc', False, 'Quotes and invoices as PDF',
         'Pick a customer, add work and materials from your price list and send a clean PDF with your logo straight '
         'from the job: by e-mail, in a messenger or with any app you choose. Four document templates.'),
        ('pen', True, 'Signed on the spot',
         'Your customer signs the quote right on your screen. Add job photos, then turn the accepted quote into an '
         'invoice with one tap.'),
        ('qr', False, 'Payment link and QR code',
         'Add your own PayPal or Stripe payment link and every invoice gets a scan-to-pay QR code, with no extra fees '
         'from us. Your bank details go on the invoice too.'),
        ('bank', True, 'Bank payments matched for you',
         'Import a bank statement (CAMT.053, MT940 or CSV). Fixbill matches payments to invoices by reference and '
         'amount and asks you about anything uncertain. Part payments and overpayments too. Your bank data never '
         'leaves your phone.'),
        ('bell', False, 'Know who owes you',
         'Unpaid, part-paid and overdue invoices at a glance, an alert when an invoice becomes overdue and a polite '
         'reminder with one tap.'),
        ('stack', False, 'VAT, deposits and credit notes',
         'VAT with several rates, prices with or without VAT, reverse charge, and invoices if you are not VAT '
         'registered. Proforma invoices for deposits, credit notes, recurring invoices and an export for your '
         'accountant as PDF and CSV.'),
    ],
    plans=[
        ('Free', '5 documents a month', 'Quotes and invoices for free, every month. Each one carries a small '
         '“Created with Fixbill” footer.', False),
        ('Fixbill Pro', 'Monthly, yearly or once', 'Unlimited documents without the footer, customer e-signatures, '
         'job photos, bank payment matching, recurring invoices and the full export for your accountant. Pay monthly, '
         'yearly or once for life. If a free trial is offered, you will see it before you buy.', True),
        ('Price promise', 'Your price stays the same', 'We will not raise the price of your subscription while it '
         'stays active. Cancel any time in your App Store or Google Play account.', False),
    ],
    offer='Free download with 5 documents a month. Fixbill Pro is an in-app purchase: monthly, yearly or a one-time '
          'lifetime purchase.',
    ld_desc='Quote and invoice app for tradesmen and sole traders: PDF quotes and invoices, customer signatures, '
            'payment link QR codes, bank payment matching, reminders. Data stays on the device.',
)

CS = dict(
    code='cs', path='cs/', hreflang='cs', html_lang='cs', og_locale='cs_CZ', name='Čeština', legal='cs',
    gp_badge='badge-googleplay-cs.png', as_alt='Stáhnout v App Store', gp_alt='Nyní na Google Play', currency='CZK',
    title='Fixbill: faktury a cenové nabídky z mobilu pro OSVČ a řemeslníky',
    desc='Faktury a cenové nabídky v telefonu pro živnostníky a řemeslníky: PDF za dvě minuty, podpis zákazníka na displeji, QR platba a upomínky. Zdarma 5 dokladů měsíčně.',
    og_title='Fixbill: faktura a cenová nabídka za dvě minuty',
    og_desc='Nabídku napíšete na místě, zákazník ji podepíše na displeji, faktura má QR platbu a platby z banky se '
            'spárují samy. Bez účtu, data zůstávají v telefonu.',
    brand_sub='Nabídky a faktury', menu='Jazyk',
    eyebrow='Pro iPhone a Android',
    h1='Faktura a cenová nabídka za <em>dvě minuty</em>',
    lede='Pro řemeslníky, živnostníky a malé firmy. Nabídku napíšete přímo na místě, zákazník ji podepíše na displeji '
         'a fakturu z ní uděláte jedním klepnutím. Platby z banky si Fixbill spáruje sám.',
    note='Zdarma 5 dokladů měsíčně. Bez registrace.',
    hero_alt='Ukázka faktury ve Fixbill: rekonstrukce koupelny, tři položky, celkem 17 400 Kč, neuhrazeno, s QR kódem '
             'pro platbu. Nabídku zákazník podepsal na displeji.',
    mock=dict(biz='Vaše firma', doc='Faktura 20260042', chip='Neuhrazeno', job='Rekonstrukce koupelny',
              lines=[('Obklad stěn', '12 m² × 950 Kč', '11 400 Kč'),
                     ('Lepidlo a spárovací hmota', '1 × 2 100 Kč', '2 100 Kč'),
                     ('Práce', '6 h × 650 Kč', '3 900 Kč')],
              total_label='Celkem', total='17 400 Kč', pay_b='Naskenujte a zaplaťte',
              pay_s='QR Platba, převod na účet', sign='Nabídka podepsaná zákazníkem'),
    h_feat='Vše pro zakázku přímo v telefonu',
    cards=[
        ('doc', False, 'Nabídky a faktury v PDF',
         'Vyberete zákazníka, přidáte práci a materiál z ceníku a pošlete úhledné PDF s vaším logem rovnou ze zakázky: '
         'e-mailem, přes messenger nebo jinou aplikací. Čtyři šablony dokladů.'),
        ('pen', True, 'Podpis přímo na místě',
         'Zákazník podepíše nabídku na vašem displeji. Přidáte fotky ze zakázky a přijatou nabídku převedete na fakturu '
         'jedním klepnutím.'),
        ('qr', False, 'QR platba na každé faktuře',
         'Na faktuře je QR Platba s variabilním symbolem, zákazník ji jen naskenuje v bankovní aplikaci. Přidat můžete '
         'i vlastní odkaz na platbu přes PayPal nebo Stripe.'),
        ('bank', True, 'Párování plateb z banky',
         'Nahrajete výpis (GPC, CAMT.053, MT940 nebo CSV) nebo napojíte Fio vlastním tokenem. Platby se k fakturám '
         'přiřadí podle variabilního symbolu a částky, sporné vám Fixbill nabídne k potvrzení. Data z banky neopustí '
         'telefon.'),
        ('bell', False, 'Kdo vám dluží',
         'Hned vidíte neuhrazené, částečně zaplacené a faktury po splatnosti. Fixbill upozorní na fakturu po splatnosti '
         'a zdvořilou upomínku pošlete jedním klepnutím.'),
        ('stack', False, 'Zálohy, dobropisy a export pro účetní',
         'Zálohové faktury, daňové doklady k přijaté platbě, konečné faktury se zápočtem záloh, dobropisy a opakované '
         'faktury. Export pro účetní v PDF, ISDOC, XML pro POHODU a CSV. Firmy doplníte z ARES podle IČO.'),
    ],
    h_tpl='Vzory zdarma k vyplnění online',
    tpl_sub='Bez aplikace: vyplníte formulář, zkontrolujete náhled a uložíte PDF. Nic se nikam neodesílá.',
    h_price='Férové ceny', price_sub='Žádné týdenní plány a žádné zdražování, dokud předplatné trvá.',
    plans=[
        ('Zdarma', '5 dokladů měsíčně', 'Nabídky a faktury zdarma každý měsíc. Na každém dokladu je malá patička '
         '„Vytvořeno ve Fixbill“.', False),
        ('Fixbill Pro', 'Měsíčně, ročně nebo navždy', 'Neomezeně dokladů bez patičky, podpis zákazníka, fotky ze '
         'zakázky, párování plateb z banky, opakované faktury a úplný export pro účetní. Platíte měsíčně, ročně, nebo '
         'jednou navždy. Pokud je nabízeno zkušební období zdarma, uvidíte ho ještě před nákupem.', True),
        ('Cenový slib', 'Cena se vám nezmění', 'Cenu vašeho předplatného nezvýšíme, dokud zůstane aktivní. Zrušit ho '
         'můžete kdykoli v účtu App Store nebo Google Play.', False),
    ],
    priv_h='Data zůstávají ve vašem telefonu',
    priv_p='Fixbill nepotřebuje účet. Údaje o firmě, klienti, položky, doklady, fotky, podpisy i výpisy z banky jsou '
           'uložené jen ve vašem zařízení a my je nikdy nevidíme.',
    priv_link='Přečtěte si zásady ochrany soukromí',
    checks=['Žádný účet, analytika, reklamy ani sledování.',
            'Doklady opustí telefon, jen když je sami sdílíte, a to do aplikace nebo služby, kterou vyberete.',
            'Zálohy jsou soubory, které uložíte, kam chcete.',
            'Vyhledání firmy pošle do veřejného rejstříku jen hledané číslo.'],
    cta_h='Stáhněte si Fixbill', cta_sub='Máte dotaz? Napište na {mail}.',
    f_support='Podpora', f_privacy='Soukromí', f_terms='Podmínky použití', f_operator='Provozovatel',
    f_templates='Vzory zdarma', f_langs='Jazyky', en_suffix='',
    offer='Stažení zdarma, 5 dokladů měsíčně. Fixbill Pro je nákup v aplikaci: měsíčně, ročně nebo jednorázově navždy.',
    ld_desc='Aplikace na faktury a cenové nabídky pro živnostníky a řemeslníky: PDF doklady, podpis zákazníka, QR '
            'platba, párování plateb z výpisu, upomínky. Data zůstávají v telefonu.',
)

SK = dict(
    code='sk', path='sk/', hreflang='sk', html_lang='sk', og_locale='sk_SK', name='Slovenčina', legal=None,
    gp_badge='badge-googleplay-en.png', as_alt='Stiahnuť v App Store', gp_alt='Teraz na Google Play', currency='EUR',
    title='Fixbill: faktúry a cenové ponuky z mobilu pre živnostníkov',
    desc='Faktúry a cenové ponuky v telefóne pre živnostníkov a remeselníkov: PDF za dve minúty, podpis zákazníka na displeji a upomienky. Zadarmo 5 dokladov mesačne.',
    og_title='Fixbill: faktúra a cenová ponuka za dve minúty',
    og_desc='Ponuku napíšete na mieste, zákazník ju podpíše na displeji a z ponuky jedným ťuknutím urobíte faktúru. '
            'Bez účtu, dáta zostávajú v telefóne.',
    brand_sub='Ponuky a faktúry', menu='Jazyk',
    eyebrow='Pre iPhone a Android',
    h1='Faktúra a cenová ponuka za <em>dve minúty</em>',
    lede='Pre remeselníkov, živnostníkov a malé firmy. Ponuku napíšete priamo na mieste, zákazník ju podpíše na '
         'displeji a faktúru z nej urobíte jedným ťuknutím. Hneď vidíte, kto vám ešte nezaplatil.',
    note='Zadarmo 5 dokladov mesačne. Bez registrácie.',
    hero_alt='Ukážka faktúry vo Fixbill: rekonštrukcia kúpeľne, tri položky, spolu 592,50 €, neuhradená, s QR kódom '
             'odkazu na platbu. Ponuku zákazník podpísal na displeji.',
    mock=dict(biz='Vaša firma', doc='Faktúra 20260042', chip='Neuhradená', job='Rekonštrukcia kúpeľne',
              lines=[('Obklad stien', '12 m² × 30,00 €', '360,00 €'),
                     ('Lepidlo a škárovacia hmota', '1 × 64,50 €', '64,50 €'),
                     ('Práca', '6 h × 28,00 €', '168,00 €')],
              total_label='Spolu', total='592,50 €', pay_b='Naskenujte a zaplaťte',
              pay_s='QR kód s vaším odkazom na platbu', sign='Ponuka podpísaná zákazníkom'),
    h_feat='Všetko pre zákazku priamo v telefóne',
    cards=[
        ('doc', False, 'Ponuky a faktúry v PDF',
         'Vyberiete zákazníka, pridáte prácu a materiál z cenníka a pošlete úhľadné PDF s vaším logom priamo zo '
         'zákazky: e-mailom, cez messenger alebo inou aplikáciou. Štyri šablóny dokladov.'),
        ('pen', True, 'Podpis priamo na mieste',
         'Zákazník podpíše ponuku na vašom displeji. Pridáte fotky zo zákazky a prijatú ponuku premeníte na faktúru '
         'jedným ťuknutím.'),
        ('qr', False, 'Odkaz na platbu s QR kódom',
         'Pridajte vlastný odkaz na platbu cez PayPal alebo Stripe a každá faktúra dostane QR kód, ktorý zákazník len '
         'naskenuje. Žiadne poplatky navyše od nás.'),
        ('bank', True, 'Párovanie platieb z banky',
         'Nahráte výpis z banky (CAMT.053, MT940 alebo CSV). Platby sa k faktúram priradia podľa platobnej referencie '
         'a sumy, nejasné vám Fixbill ponúkne na potvrdenie. Dáta z banky neopustia telefón.'),
        ('bell', False, 'Kto vám dlží',
         'Hneď vidíte neuhradené, čiastočne zaplatené faktúry aj faktúry po splatnosti. Fixbill upozorní na faktúru '
         'po splatnosti a zdvorilú upomienku pošlete jedným ťuknutím.'),
        ('stack', False, 'Zálohy, dobropisy a export pre účtovníka',
         'Zálohové faktúry, konečné faktúry so zápočtom záloh, dobropisy a opakované faktúry. Export pre účtovníka '
         'v PDF a CSV. Pre platiteľov aj neplatiteľov DPH.'),
    ],
    h_tpl='', tpl_sub='',
    h_price='Férové ceny', price_sub='Žiadne týždenné plány a žiadne zdražovanie, kým predplatné trvá.',
    plans=[
        ('Zadarmo', '5 dokladov mesačne', 'Ponuky a faktúry zadarmo každý mesiac. Na každom doklade je malá pätička '
         '„Vytvorené vo Fixbill“.', False),
        ('Fixbill Pro', 'Mesačne, ročne alebo navždy', 'Neobmedzene dokladov bez pätičky, podpis zákazníka, fotky zo '
         'zákazky, párovanie platieb z banky, opakované faktúry a úplný export pre účtovníka. Platíte mesačne, ročne '
         'alebo raz navždy. Ak je ponúkané skúšobné obdobie zadarmo, uvidíte ho ešte pred nákupom.', True),
        ('Cenový sľub', 'Cena sa vám nezmení', 'Cenu vášho predplatného nezvýšime, kým zostane aktívne. Zrušiť ho '
         'môžete kedykoľvek v účte App Store alebo Google Play.', False),
    ],
    priv_h='Dáta zostávajú vo vašom telefóne',
    priv_p='Fixbill nepotrebuje účet. Údaje o firme, klienti, položky, doklady, fotky, podpisy aj výpisy z banky sú '
           'uložené len vo vašom zariadení a my ich nikdy nevidíme.',
    priv_link='Zásady ochrany súkromia (v angličtine)',
    checks=['Žiadny účet, analytika, reklamy ani sledovanie.',
            'Doklady opustia telefón, len keď ich sami zdieľate, a to do aplikácie alebo služby, ktorú vyberiete.',
            'Zálohy sú súbory, ktoré uložíte, kam chcete.',
            'Vyhľadanie firmy pošle do verejného registra len hľadané číslo.'],
    cta_h='Stiahnite si Fixbill', cta_sub='Máte otázku? Napíšte na {mail}.',
    f_support='Podpora', f_privacy='Súkromie', f_terms='Podmienky používania', f_operator='Prevádzkovateľ',
    f_templates='Vzory zadarmo', f_langs='Jazyky', en_suffix=' (EN)',
    offer='Stiahnutie zadarmo, 5 dokladov mesačne. Fixbill Pro je nákup v aplikácii: mesačne, ročne alebo jednorazovo '
          'navždy.',
    ld_desc='Aplikácia na faktúry a cenové ponuky pre živnostníkov a remeselníkov: PDF doklady, podpis zákazníka, '
            'odkaz na platbu s QR kódom, párovanie platieb, upomienky. Dáta zostávajú v telefóne.',
)

DE = dict(
    code='de', path='de/', hreflang='de', html_lang='de', og_locale='de_DE', name='Deutsch', legal='de',
    gp_badge='badge-googleplay-en.png', as_alt='Laden im App Store', gp_alt='Jetzt bei Google Play', currency='EUR',
    title='Rechnung schreiben App für Handwerker und Kleinunternehmer | Fixbill',
    desc='Rechnungen und Angebote per Handy für Handwerker: PDF in zwei Minuten, Unterschrift auf dem Display, GiroCode und Zahlungserinnerungen. 5 Dokumente im Monat kostenlos.',
    og_title='Fixbill: Rechnung und Angebot in zwei Minuten',
    og_desc='Angebot vor Ort schreiben, auf dem Display unterschreiben lassen, Rechnung mit GiroCode senden und sehen, '
            'wer bezahlt hat. Kein Konto, Ihre Daten bleiben auf dem Handy.',
    brand_sub='Angebote und Rechnungen', menu='Sprache',
    eyebrow='Für iPhone und Android',
    h1='Rechnung und Angebot in <em>zwei Minuten</em>',
    lede='Für Handwerker, Kleinunternehmer und kleine Betriebe. Schreiben Sie das Angebot vor Ort, lassen Sie es auf '
         'dem Display unterschreiben und machen Sie mit einem Tippen die Rechnung daraus. Wer bezahlt hat, sehen Sie '
         'sofort.',
    note='Kostenlos für 5 Dokumente pro Monat. Kein Konto nötig.',
    hero_alt='Beispielrechnung in Fixbill: Badsanierung, drei Positionen, gesamt 810,50 €, offen, mit Zahlungs-QR-Code. '
             'Das Angebot hat der Kunde auf dem Display unterschrieben.',
    mock=dict(biz='Ihre Firma', doc='Rechnung RE-2026-0042', chip='Offen', job='Badsanierung',
              lines=[('Wandfliesen verlegen', '12 m² × 38,00 €', '456,00 €'),
                     ('Fliesenkleber und Fugenmörtel', '1 × 84,50 €', '84,50 €'),
                     ('Arbeitszeit', '6 Std. × 45,00 €', '270,00 €')],
              total_label='Gesamt', total='810,50 €', pay_b='Scannen und bezahlen',
              pay_s='EPC-QR-Code (GiroCode), Überweisung in Euro', sign='Angebot vom Kunden unterschrieben'),
    h_feat='Alles für den Auftrag, direkt auf dem Handy',
    cards=[
        ('doc', False, 'Angebote und Rechnungen als PDF',
         'Kunden wählen, Arbeiten und Material aus der Preisliste eintragen und ein sauberes PDF mit Ihrem Logo direkt '
         'vom Einsatzort senden: per E-Mail, Messenger oder mit jeder App Ihrer Wahl. Vier Dokumentvorlagen.'),
        ('pen', True, 'Vor Ort unterschrieben',
         'Ihr Kunde unterschreibt das Angebot direkt auf Ihrem Display. Fotos vom Auftrag dazu, und aus dem '
         'angenommenen Angebot wird mit einem Tippen die Rechnung.'),
        ('qr', False, 'GiroCode und Zahlungslink',
         'Rechnungen tragen einen EPC-QR-Code (GiroCode) für die Überweisung, Ihr Kunde scannt ihn in seiner '
         'Banking-App. Dazu können Sie Ihren eigenen PayPal- oder Stripe-Zahlungslink hinzufügen.'),
        ('bank', True, 'Zahlungen automatisch zugeordnet',
         'Kontoauszug importieren (CAMT.053, MT940 oder CSV): Fixbill ordnet Zahlungen über Verwendungszweck und Betrag '
         'den Rechnungen zu und fragt bei Unklarem nach. Auch Teil- und Überzahlungen. Ihre Bankdaten verlassen nie '
         'das Handy.'),
        ('bell', False, 'Offene Posten im Blick',
         'Offene, teilweise bezahlte und überfällige Rechnungen auf einen Blick, ein Hinweis bei Überfälligkeit und '
         'eine freundliche Zahlungserinnerung mit einem Tippen.'),
        ('stack', False, 'Anzahlungen, Korrekturen, Serien',
         'Anzahlungsrechnungen, Schlussrechnungen mit Abzug der Anzahlungen, Rechnungskorrekturen und wiederkehrende '
         'Rechnungen. Kleinunternehmerregelung nach § 19 UStG und Reverse Charge. Export für den Steuerberater als PDF '
         'und CSV.'),
    ],
    h_tpl='Kostenlose Vorlagen zum Ausfüllen',
    tpl_sub='Ohne App: Formular ausfüllen, Vorschau prüfen, als PDF speichern. Es wird nichts hochgeladen.',
    h_price='Faire Preise', price_sub='Keine Wochen-Abos und keine Preiserhöhung, solange Ihr Abo läuft.',
    plans=[
        ('Kostenlos', '5 Dokumente pro Monat', 'Angebote und Rechnungen jeden Monat kostenlos. Jedes Dokument trägt '
         'eine kleine Fußzeile „Erstellt mit Fixbill“.', False),
        ('Fixbill Pro', 'Monatlich, jährlich oder einmalig', 'Unbegrenzt Dokumente ohne Fußzeile, '
         'Kundenunterschriften, Fotos vom Auftrag, Zahlungsabgleich, wiederkehrende Rechnungen und der komplette '
         'Export für den Steuerberater. Zahlen Sie monatlich, jährlich oder einmal für immer. Wird ein kostenloser '
         'Testzeitraum angeboten, sehen Sie das vor dem Kauf.', True),
        ('Preisversprechen', 'Ihr Preis bleibt gleich', 'Solange Ihr Abo aktiv ist, erhöhen wir seinen Preis nicht. '
         'Kündigen können Sie jederzeit in Ihrem App-Store- oder Google-Play-Konto.', False),
    ],
    priv_h='Ihre Daten bleiben auf Ihrem Handy',
    priv_p='Fixbill braucht kein Konto. Firmendaten, Kunden, Positionen, Dokumente, Fotos, Unterschriften und '
           'Kontoauszüge werden nur auf Ihrem Gerät gespeichert. Wir sehen sie nie.',
    priv_link='Zur Datenschutzerklärung',
    checks=['Kein Konto, keine Analyse, keine Werbung, kein Tracking.',
            'Dokumente verlassen Ihr Handy nur, wenn Sie sie teilen, und zwar an die App oder den Dienst Ihrer Wahl.',
            'Sicherungen sind Dateien, die Sie speichern, wo Sie möchten.',
            'Die Firmensuche sendet nur die gesuchte Nummer an ein öffentliches Register.'],
    cta_h='Fixbill laden', cta_sub='Fragen? Schreiben Sie an {mail}.',
    f_support='Hilfe', f_privacy='Datenschutz', f_terms='Nutzungsbedingungen', f_operator='Betreiber',
    f_templates='Kostenlose Vorlagen', f_langs='Sprachen', en_suffix='',
    offer='Kostenloser Download mit 5 Dokumenten pro Monat. Fixbill Pro ist ein In-App-Kauf: monatlich, jährlich oder '
          'einmalig für immer.',
    ld_desc='App für Angebote und Rechnungen für Handwerker und Kleinunternehmer: PDF, Kundenunterschrift, GiroCode, '
            'Zahlungsabgleich, Zahlungserinnerungen. Die Daten bleiben auf dem Gerät.',
)

FR = dict(
    code='fr', path='fr/', hreflang='fr', html_lang='fr', og_locale='fr_FR', name='Français', legal='fr',
    gp_badge='badge-googleplay-en.png', as_alt="Télécharger dans l'App Store", gp_alt='Disponible sur Google Play',
    currency='EUR',
    title='Application devis et facture pour artisans et auto-entrepreneurs | Fixbill',
    desc="Devis et factures sur votre téléphone pour artisans : PDF en deux minutes, signature du client à l'écran et relances. Gratuit pour 5 documents par mois.",
    og_title='Fixbill : devis et factures en deux minutes',
    og_desc="Rédigez le devis sur le chantier, faites-le signer sur l'écran, ajoutez un QR code de paiement et voyez "
            "qui a payé. Sans compte, vos données restent sur votre téléphone.",
    brand_sub='Devis et factures', menu='Langue',
    eyebrow='Pour iPhone et Android',
    h1='Devis et factures en <em>deux minutes</em>, sur le chantier',
    lede="Pour les artisans, les auto-entrepreneurs et les petites entreprises. Rédigez le devis sur place, faites-le "
         "signer sur votre écran et transformez-le en facture d'un geste. Vous voyez tout de suite qui a payé.",
    note='Gratuit pour 5 documents par mois. Sans compte.',
    hero_alt="Exemple de facture dans Fixbill : rénovation de salle de bains, trois lignes, total 810,50 €, à payer, "
             "avec un QR code de paiement. Le client a signé le devis sur l'écran.",
    mock=dict(biz='Votre entreprise', doc='Facture F2026-0042', chip='À payer', job='Rénovation de salle de bains',
              lines=[('Pose de faïence murale', '12 m² × 38,00 €', '456,00 €'),
                     ('Colle et joints', '1 × 84,50 €', '84,50 €'),
                     ("Main-d'œuvre", '6 h × 45,00 €', '270,00 €')],
              total_label='Total', total='810,50 €', pay_b='Scannez pour payer',
              pay_s='QR code EPC, virement en euros', sign='Devis signé par le client'),
    h_feat='Tout pour le chantier, dans votre téléphone',
    cards=[
        ('doc', False, 'Devis et factures en PDF',
         "Choisissez un client, ajoutez travaux et fournitures depuis vos tarifs et envoyez un PDF soigné avec votre "
         "logo depuis le chantier : par e-mail, par messagerie ou avec l'application de votre choix. Quatre modèles."),
        ('pen', True, 'Signé sur place',
         "Votre client signe le devis directement sur votre écran. Ajoutez des photos du chantier, puis transformez le "
         "devis accepté en facture d'un geste."),
        ('qr', False, 'QR code et lien de paiement',
         "Vos factures portent un QR code EPC pour le virement : votre client le scanne dans son application bancaire. "
         "Vous pouvez aussi ajouter votre propre lien de paiement PayPal ou Stripe."),
        ('bank', True, 'Paiements bancaires rapprochés',
         "Importez un relevé (CAMT.053, MT940 ou CSV) : Fixbill rapproche les paiements des factures par référence et "
         "montant et vous demande de confirmer les cas douteux. Paiements partiels et trop-perçus compris. Vos données "
         "bancaires ne quittent jamais le téléphone."),
        ('bell', False, 'Suivi des impayés',
         "Factures impayées, payées en partie ou en retard d'un coup d'œil, une alerte en cas de retard et une relance "
         "polie en un geste."),
        ('stack', False, 'Acomptes, avoirs, récurrentes',
         "Factures d'acompte, factures de solde avec déduction des acomptes, avoirs et factures récurrentes. Franchise "
         "en base (art. 293 B du CGI) et autoliquidation. Export pour le comptable en PDF et CSV."),
    ],
    h_tpl='Modèles gratuits à remplir en ligne',
    tpl_sub="Sans application : remplissez le formulaire, vérifiez l'aperçu et enregistrez un PDF. Rien n'est envoyé.",
    h_price='Des prix justes', price_sub="Pas de formule à la semaine, pas de hausse de prix tant que vous êtes abonné.",
    plans=[
        ('Gratuit', '5 documents par mois', 'Devis et factures gratuits chaque mois. Chaque document porte une petite '
         'mention « Créé avec Fixbill » en pied de page.', False),
        ('Fixbill Pro', "Au mois, à l'année ou à vie", "Documents illimités sans pied de page, signature du client, "
         "photos du chantier, rapprochement bancaire, factures récurrentes et export complet pour le comptable. Payez "
         "au mois, à l'année ou une seule fois à vie. Si un essai gratuit est proposé, vous le verrez avant l'achat.",
         True),
        ('Prix garanti', 'Votre prix ne bouge pas', "Nous n'augmenterons pas le prix de votre abonnement tant qu'il "
         "reste actif. Résiliez quand vous voulez depuis votre compte App Store ou Google Play.", False),
    ],
    priv_h='Vos données restent sur votre téléphone',
    priv_p="Fixbill ne demande aucun compte. Profil de l'entreprise, clients, articles, documents, photos, signatures "
           "et relevés bancaires sont stockés uniquement sur votre appareil. Nous ne les voyons jamais.",
    priv_link='Lire la politique de confidentialité',
    checks=["Pas de compte, pas d'analytique, pas de publicité, pas de suivi.",
            "Un document ne quitte votre téléphone que si vous le partagez, vers l'application ou le service de votre "
            "choix.",
            'Les sauvegardes sont des fichiers que vous enregistrez où vous voulez.',
            "La recherche d'entreprise n'envoie que le numéro recherché à un registre public."],
    cta_h='Télécharger Fixbill', cta_sub='Une question ? Écrivez à {mail}.',
    f_support='Assistance', f_privacy='Confidentialité', f_terms="Conditions d'utilisation", f_operator='Éditeur',
    f_templates='Modèles gratuits', f_langs='Langues', en_suffix='',
    offer="Téléchargement gratuit avec 5 documents par mois. Fixbill Pro est un achat intégré : au mois, à l'année ou "
          "en achat unique à vie.",
    ld_desc="Application de devis et factures pour artisans et auto-entrepreneurs : PDF, signature du client, QR code "
            "de paiement, rapprochement bancaire, relances. Les données restent sur l'appareil.",
)

ES = dict(
    code='es', path='es/', hreflang='es', html_lang='es', og_locale='es_ES', name='Español', legal=None,
    gp_badge='badge-googleplay-en.png', as_alt='Descárgalo en el App Store', gp_alt='Disponible en Google Play',
    currency='EUR',
    title='Fixbill: app para hacer presupuestos y facturas de obras y reformas',
    desc='Presupuestos y facturas desde el móvil para autónomos y reformas: PDF en dos minutos, firma del cliente en pantalla y recordatorios. Gratis hasta 5 documentos al mes.',
    og_title='Fixbill: presupuestos de obra en dos minutos',
    og_desc='Haz el presupuesto en la obra, deja que el cliente lo firme en tu pantalla y envíaselo en PDF antes de '
            'irte. Sin cuenta, tus datos se quedan en tu móvil.',
    brand_sub='Presupuestos y facturas', menu='Idioma',
    eyebrow='Para iPhone y Android',
    h1='Presupuestos de obra en <em>dos minutos</em>, desde el móvil',
    lede='Para autónomos, profesionales de obras y reformas y pequeñas empresas. Haz el presupuesto en la visita, deja '
         'que el cliente lo firme en tu pantalla y conviértelo en factura con un toque. Ves al momento quién te ha '
         'pagado.',
    note='Gratis hasta 5 documentos al mes. Sin registro.',
    hero_alt='Ejemplo de presupuesto en Fixbill: reforma de baño, tres partidas, total 662,50 €, aceptado, con el '
             'código QR del enlace de pago. El cliente lo firmó en la pantalla.',
    mock=dict(biz='Tu empresa', doc='Presupuesto P-2026-042', chip='Aceptado', job='Reforma de baño',
              lines=[('Alicatado de paredes', '12 m² × 32,00 €', '384,00 €'),
                     ('Cemento cola y rejuntado', '1 × 68,50 €', '68,50 €'),
                     ('Mano de obra', '6 h × 35,00 €', '210,00 €')],
              total_label='Total', total='662,50 €', pay_b='Escanea y paga',
              pay_s='Código QR de tu enlace de pago', sign='Presupuesto firmado por el cliente'),
    h_feat='Todo para la obra, en tu móvil',
    cards=[
        ('doc', False, 'Presupuestos y facturas en PDF',
         'Elige al cliente, añade trabajos y materiales de tu lista de precios y envía un PDF limpio con tu logo desde '
         'la obra: por correo, por mensajería o con la app que prefieras. Cuatro plantillas.'),
        ('pen', True, 'Firmado en la obra',
         'Tu cliente firma el presupuesto en tu pantalla. Añade fotos de la obra y convierte el presupuesto aceptado en '
         'factura con un toque.'),
        ('qr', False, 'Enlace de pago con QR',
         'Añade tu propio enlace de pago de PayPal o Stripe y cada documento lleva un código QR para pagar. Sin '
         'comisiones extra por nuestra parte.'),
        ('bank', True, 'Cobros del banco conciliados',
         'Importa un extracto (CAMT.053, MT940 o CSV): Fixbill asigna los cobros a las facturas por referencia e '
         'importe y te pregunta por los dudosos. También pagos parciales y en exceso. Tus datos bancarios no salen del '
         'móvil.'),
        ('bell', False, 'Quién te debe',
         'Facturas pendientes, cobradas en parte y vencidas de un vistazo, un aviso cuando una vence y un recordatorio '
         'amable con un toque.'),
        ('stack', False, 'Anticipos, rectificativas, recurrentes',
         'Facturas de anticipo, facturas finales que descuentan los anticipos, facturas rectificativas y facturas '
         'recurrentes. Exportación para tu gestor en PDF y CSV.'),
    ],
    h_tpl='Plantillas gratis para rellenar online',
    tpl_sub='Sin app: rellena el formulario, revisa la vista previa y guarda un PDF. No se envía nada.',
    h_price='Precios justos', price_sub='Sin planes semanales y sin subidas de precio mientras sigas suscrito.',
    plans=[
        ('Gratis', '5 documentos al mes', 'Presupuestos y facturas gratis cada mes. Cada documento lleva un pequeño pie '
         '«Creado con Fixbill».', False),
        ('Fixbill Pro', 'Mensual, anual o para siempre', 'Documentos ilimitados sin pie, firma del cliente, fotos de la '
         'obra, conciliación bancaria, facturas recurrentes y exportación completa para tu gestor. Paga cada mes, cada '
         'año o una sola vez para siempre. Si hay una prueba gratis, la verás antes de comprar.', True),
        ('Precio garantizado', 'Tu precio no cambia', 'No subiremos el precio de tu suscripción mientras siga activa. '
         'Cancélala cuando quieras en tu cuenta de App Store o Google Play.', False),
    ],
    priv_h='Tus datos se quedan en tu móvil',
    priv_p='Fixbill no necesita cuenta. Los datos de tu negocio, clientes, conceptos, documentos, fotos, firmas y '
           'extractos bancarios se guardan solo en tu dispositivo. Nosotros nunca los vemos.',
    priv_link='Política de privacidad (en inglés)',
    checks=['Sin cuenta, sin analítica, sin anuncios y sin seguimiento.',
            'Los documentos solo salen del móvil cuando tú los compartes, con la app o el servicio que elijas.',
            'Las copias de seguridad son archivos que guardas donde quieras.',
            'La búsqueda de empresas solo envía a un registro público el número que buscas.'],
    cta_h='Descarga Fixbill', cta_sub='¿Tienes dudas? Escribe a {mail}.',
    f_support='Ayuda', f_privacy='Privacidad', f_terms='Condiciones de uso', f_operator='Responsable',
    f_templates='Plantillas gratis', f_langs='Idiomas', en_suffix=' (EN)',
    offer='Descarga gratis con 5 documentos al mes. Fixbill Pro es una compra dentro de la app: mensual, anual o un '
          'pago único para siempre.',
    ld_desc='App de presupuestos y facturas para autónomos de obras y reformas: PDF, firma del cliente, enlace de pago '
            'con QR, conciliación bancaria, recordatorios. Los datos se quedan en el dispositivo.',
)

IT = dict(
    code='it', path='it/', hreflang='it', html_lang='it', og_locale='it_IT', name='Italiano', legal=None,
    gp_badge='badge-googleplay-en.png', as_alt="Scarica su App Store", gp_alt='Disponibile su Google Play',
    currency='EUR',
    title='Fixbill: app per preventivi edili e artigiani (iPhone, Android)',
    desc='Preventivi in PDF dal telefono per artigiani e imprese edili: pronti in due minuti, firma del cliente sullo schermo e promemoria. Gratis fino a 5 documenti al mese.',
    og_title='Fixbill: preventivi in due minuti',
    og_desc='Scrivi il preventivo in cantiere, fallo firmare sullo schermo e invialo in PDF prima di andare via. Senza '
            'account, i tuoi dati restano sul telefono.',
    brand_sub='Preventivi in PDF', menu='Lingua',
    eyebrow='Per iPhone e Android',
    h1='Preventivi in <em>due minuti</em>, direttamente in cantiere',
    lede='Per artigiani, imprese edili e piccole attività. Scrivi il preventivo durante il sopralluogo, fallo firmare '
         'al cliente sul tuo schermo e invialo in PDF prima di andare via.',
    note='Gratis fino a 5 documenti al mese. Senza registrazione.',
    hero_alt='Esempio di preventivo in Fixbill: rifacimento bagno, tre voci, totale 718,00 €, accettato, con il QR code '
             'del link di pagamento. Il cliente lo ha firmato sullo schermo.',
    mock=dict(biz='La tua impresa', doc='Preventivo 2026/042', chip='Accettato', job='Rifacimento bagno',
              lines=[('Posa rivestimento', '12 m² × 35,00 €', '420,00 €'),
                     ('Collante e stucco', '1 × 70,00 €', '70,00 €'),
                     ('Manodopera', '6 h × 38,00 €', '228,00 €')],
              total_label='Totale', total='718,00 €', pay_b='Inquadra e paga',
              pay_s='QR code del tuo link di pagamento', sign='Preventivo firmato dal cliente'),
    h_feat='Tutto per il cantiere, sul telefono',
    cards=[
        ('doc', False, 'Preventivi in PDF',
         "Scegli il cliente, aggiungi lavori e materiali dal tuo listino e invia un PDF pulito con il tuo logo "
         "direttamente dal cantiere: per e-mail, in chat o con l'app che preferisci. Quattro modelli di documento."),
        ('pen', True, 'Firmato sul posto',
         'Il cliente firma il preventivo direttamente sul tuo schermo. Aggiungi le foto del cantiere per mostrare '
         'esattamente cosa farai.'),
        ('qr', False, 'Link di pagamento con QR',
         'Aggiungi il tuo link di pagamento PayPal o Stripe e il documento riceve un QR code per pagare. Nessuna '
         'commissione extra da parte nostra.'),
        ('bell', False, 'Incassi sotto controllo',
         "Pagato, pagato in parte o scaduto: tutto a colpo d'occhio, con un avviso alla scadenza e un sollecito gentile "
         "con un tocco."),
        ('users', False, 'Un listino che impara',
         'Il listino impara da ogni preventivo e ogni cliente ha i suoi documenti e totali. Funziona anche offline in '
         'cantiere, con backup su file.'),
        ('tag', False, 'IVA come serve a te',
         'Più aliquote IVA, prezzi con o senza IVA e la dicitura del regime forfettario sul documento.'),
    ],
    h_tpl='Modelli gratuiti da compilare online',
    tpl_sub="Senza app: compila il modulo, controlla l'anteprima e salva un PDF. Non inviamo nulla.",
    h_price='Prezzi onesti', price_sub='Niente abbonamenti settimanali e nessun aumento finché resti abbonato.',
    plans=[
        ('Gratis', '5 documenti al mese', 'Preventivi gratis ogni mese. Ogni documento ha un piccolo piè di pagina '
         '«Creato con Fixbill».', False),
        ('Fixbill Pro', 'Mensile, annuale o per sempre', 'Documenti illimitati senza piè di pagina, firma del cliente, '
         "foto del cantiere e tutti e quattro i modelli. Paghi al mese, all'anno o una volta per sempre. Se c'è una "
         "prova gratuita, la vedi prima dell'acquisto.", True),
        ('Prezzo garantito', 'Il tuo prezzo non cambia', 'Non aumenteremo il prezzo del tuo abbonamento finché resta '
         'attivo. Puoi disdirlo quando vuoi dal tuo account App Store o Google Play.', False),
    ],
    priv_h='I tuoi dati restano sul telefono',
    priv_p="Fixbill non richiede un account. Dati dell'impresa, clienti, voci, documenti, foto e firme sono salvati "
           "solo sul tuo dispositivo. Noi non li vediamo mai.",
    priv_link='Informativa sulla privacy (in inglese)',
    checks=['Nessun account, nessuna analisi, niente pubblicità né tracciamento.',
            "I documenti lasciano il telefono solo quando li condividi tu, con l'app o il servizio che scegli.",
            'I backup sono file che salvi dove vuoi.',
            "La ricerca di un'impresa invia a un registro pubblico solo il numero cercato."],
    cta_h='Scarica Fixbill', cta_sub='Domande? Scrivi a {mail}.',
    f_support='Assistenza', f_privacy='Privacy', f_terms="Condizioni d'uso", f_operator='Gestore',
    f_templates='Modelli gratuiti', f_langs='Lingue', en_suffix=' (EN)',
    offer="Download gratuito con 5 documenti al mese. Fixbill Pro è un acquisto in app: mensile, annuale o una tantum "
          "per sempre.",
    ld_desc='App per preventivi per artigiani e imprese edili: PDF, firma del cliente, link di pagamento con QR code, '
            'promemoria. I dati restano sul dispositivo.',
)

PL = dict(
    code='pl', path='pl/', hreflang='pl', html_lang='pl', og_locale='pl_PL', name='Polski', legal=None,
    gp_badge='badge-googleplay-en.png', as_alt='Pobierz z App Store', gp_alt='Pobierz z Google Play', currency='PLN',
    title='Fixbill: aplikacja do wyceny i kosztorysów dla fachowców',
    desc='Wyceny i kosztorysy w PDF z telefonu dla fachowców: gotowe w dwie minuty, podpis klienta na ekranie i przypomnienia. Za darmo do 5 dokumentów miesięcznie.',
    og_title='Fixbill: wycena i kosztorys w dwie minuty',
    og_desc='Przygotuj wycenę u klienta, daj ją podpisać na ekranie i wyślij PDF, zanim wyjdziesz. Bez konta, dane '
            'zostają w Twoim telefonie.',
    brand_sub='Wyceny i kosztorysy', menu='Język',
    eyebrow="Na iPhone'a i Androida",
    h1='Wycena i kosztorys w <em>dwie minuty</em>, prosto z telefonu',
    lede='Dla fachowców, ekip remontowych i małych firm. Przygotuj wycenę podczas oględzin, daj ją klientowi do podpisu '
         'na ekranie i wyślij PDF, zanim wyjdziesz.',
    note='Za darmo do 5 dokumentów miesięcznie. Bez zakładania konta.',
    hero_alt='Przykładowa wycena w Fixbill: remont łazienki, trzy pozycje, razem 2 260,00 zł, zaakceptowana, z kodem QR '
             'linku do płatności. Klient podpisał ją na ekranie.',
    mock=dict(biz='Twoja firma', doc='Wycena W/2026/042', chip='Zaakceptowana', job='Remont łazienki',
              lines=[('Układanie płytek', '12 m² × 120,00 zł', '1 440,00 zł'),
                     ('Klej i fuga', '1 × 280,00 zł', '280,00 zł'),
                     ('Robocizna', '6 h × 90,00 zł', '540,00 zł')],
              total_label='Razem', total='2 260,00 zł', pay_b='Zeskanuj i zapłać',
              pay_s='Kod QR Twojego linku do płatności', sign='Wycena podpisana przez klienta'),
    h_feat='Wszystko do zlecenia w telefonie',
    cards=[
        ('doc', False, 'Wyceny i kosztorysy w PDF',
         'Wybierz klienta, dodaj prace i materiały z cennika i wyślij czytelny PDF z logo prosto z budowy: e-mailem, '
         'komunikatorem albo dowolną aplikacją. Cztery szablony dokumentów.'),
        ('pen', True, 'Podpis na miejscu',
         'Klient podpisuje wycenę bezpośrednio na Twoim ekranie. Dodaj zdjęcia z budowy, żeby pokazać, co dokładnie '
         'zrobisz.'),
        ('qr', False, 'Link do płatności z kodem QR',
         'Dodaj własny link do płatności PayPal lub Stripe, a dokument dostanie kod QR do zapłaty. Bez dodatkowych '
         'opłat z naszej strony.'),
        ('bell', False, 'Płatności pod kontrolą',
         'Zapłacone, częściowo zapłacone i po terminie: wszystko widać od razu, z powiadomieniem o terminie i uprzejmym '
         'przypomnieniem jednym dotknięciem.'),
        ('users', False, 'Cennik, który się uczy',
         'Cennik uczy się z każdej wyceny, a każdy klient ma swoje dokumenty i sumy. Działa offline na budowie, '
         'z kopią zapasową w pliku.'),
        ('tag', False, 'Stawki VAT i zwolnienie',
         'Kilka stawek VAT, ceny netto lub brutto i adnotacja o zwolnieniu z art. 113 ustawy o VAT na dokumencie.'),
    ],
    h_tpl='Darmowe wzory do wypełnienia online',
    tpl_sub='Bez aplikacji: wypełnij formularz, sprawdź podgląd i zapisz PDF. Nic nie jest wysyłane.',
    h_price='Uczciwe ceny', price_sub='Bez planów tygodniowych i bez podwyżek, dopóki masz subskrypcję.',
    plans=[
        ('Za darmo', '5 dokumentów miesięcznie', 'Wyceny za darmo co miesiąc. Na każdym dokumencie jest mała stopka '
         '„Utworzono w Fixbill”.', False),
        ('Fixbill Pro', 'Miesięcznie, rocznie lub na zawsze', 'Bez limitu dokumentów i bez stopki, podpis klienta, '
         'zdjęcia z budowy i wszystkie cztery szablony. Płacisz co miesiąc, co rok albo raz na zawsze. Jeśli jest '
         'darmowy okres próbny, zobaczysz go przed zakupem.', True),
        ('Gwarancja ceny', 'Twoja cena się nie zmieni', 'Nie podniesiemy ceny Twojej subskrypcji, dopóki jest aktywna. '
         'Anulujesz ją w każdej chwili w koncie App Store lub Google Play.', False),
    ],
    priv_h='Twoje dane zostają w telefonie',
    priv_p='Fixbill nie wymaga konta. Dane firmy, klienci, pozycje, dokumenty, zdjęcia i podpisy są zapisane tylko na '
           'Twoim urządzeniu. Nigdy ich nie widzimy.',
    priv_link='Polityka prywatności (po angielsku)',
    checks=['Bez konta, analityki, reklam i śledzenia.',
            'Dokumenty opuszczają telefon tylko wtedy, gdy sam je udostępnisz, do wybranej aplikacji lub usługi.',
            'Kopie zapasowe to pliki, które zapisujesz, gdzie chcesz.',
            'Wyszukiwanie firmy wysyła do publicznego rejestru tylko szukany numer.'],
    cta_h='Pobierz Fixbill', cta_sub='Masz pytanie? Napisz na {mail}.',
    f_support='Pomoc', f_privacy='Prywatność', f_terms='Warunki korzystania', f_operator='Operator',
    f_templates='Darmowe wzory', f_langs='Języki', en_suffix=' (EN)',
    offer='Pobranie za darmo, 5 dokumentów miesięcznie. Fixbill Pro to zakup w aplikacji: miesięcznie, rocznie lub '
          'jednorazowo na zawsze.',
    ld_desc='Aplikacja do wycen i kosztorysów dla fachowców: PDF, podpis klienta, link do płatności z kodem QR, '
            'przypomnienia. Dane zostają na urządzeniu.',
)

PT = dict(
    code='pt', path='pt/', hreflang='pt', html_lang='pt-BR', og_locale='pt_BR', name='Português', legal=None,
    gp_badge='badge-googleplay-en.png', as_alt='Baixar na App Store', gp_alt='Disponível no Google Play',
    currency='BRL',
    title='Fixbill: app de orçamento de serviço para autônomos e prestadores',
    desc='Orçamentos de serviço em PDF pelo celular para autônomos: prontos em dois minutos, assinatura do cliente na tela e lembretes. Grátis até 5 documentos por mês.',
    og_title='Fixbill: orçamento de serviço em dois minutos',
    og_desc='Faça o orçamento na visita, peça a assinatura do cliente na tela e envie o PDF antes de sair. Sem conta, '
            'seus dados ficam no celular.',
    brand_sub='Orçamentos de serviço', menu='Idioma',
    eyebrow='Para iPhone e Android',
    h1='Orçamento de serviço em <em>dois minutos</em>, direto do celular',
    lede='Para autônomos, prestadores de serviço e pequenas empresas. Faça o orçamento durante a visita, peça a '
         'assinatura do cliente na tela e envie o PDF antes de ir embora.',
    note='Grátis até 5 documentos por mês. Sem cadastro.',
    hero_alt='Exemplo de orçamento no Fixbill: reforma de banheiro, três itens, total R$ 1.560,00, aprovado, com o QR '
             'code do link de pagamento. O cliente assinou na tela.',
    mock=dict(biz='Sua empresa', doc='Orçamento 2026-042', chip='Aprovado', job='Reforma de banheiro',
              lines=[('Assentamento de revestimento', '12 m² × R$ 85,00', 'R$ 1.020,00'),
                     ('Argamassa e rejunte', '1 × R$ 180,00', 'R$ 180,00'),
                     ('Mão de obra', '6 h × R$ 60,00', 'R$ 360,00')],
              total_label='Total', total='R$ 1.560,00', pay_b='Escaneie e pague',
              pay_s='QR code do seu link de pagamento', sign='Orçamento assinado pelo cliente'),
    h_feat='Tudo para o serviço, no seu celular',
    cards=[
        ('doc', False, 'Orçamentos em PDF',
         'Escolha o cliente, adicione serviços e materiais da sua tabela de preços e envie um PDF caprichado com a sua '
         'logo direto da obra: por e-mail, aplicativo de mensagens ou qualquer outro app. Quatro modelos de documento.'),
        ('pen', True, 'Assinado na hora',
         'O cliente assina o orçamento direto na sua tela. Adicione fotos do serviço para mostrar exatamente o que você '
         'vai fazer.'),
        ('qr', False, 'Link de pagamento com QR code',
         'Adicione seu próprio link de pagamento do PayPal ou Stripe e o documento ganha um QR code para pagar. Sem '
         'taxas extras da nossa parte.'),
        ('bell', False, 'Recebimentos sob controle',
         'Pago, pago em parte ou vencido: tudo num relance, com aviso de vencimento e um lembrete educado com um toque.'),
        ('users', False, 'Tabela de preços que aprende',
         'A tabela de preços aprende com cada orçamento e cada cliente tem seus documentos e totais. Funciona offline '
         'na obra, com backup em arquivo.'),
        ('tag', False, 'Com a cara da sua empresa',
         'Sua logo e suas cores em quatro modelos de documento. No Pro, também a sua assinatura e o seu carimbo.'),
    ],
    h_tpl='', tpl_sub='',
    h_price='Preço justo', price_sub='Sem planos semanais e sem aumento de preço enquanto você for assinante.',
    plans=[
        ('Grátis', '5 documentos por mês', 'Orçamentos grátis todo mês. Cada documento leva um pequeno rodapé '
         '“Criado com o Fixbill”.', False),
        ('Fixbill Pro', 'Mensal, anual ou vitalício', 'Documentos ilimitados sem rodapé, assinatura do cliente, fotos '
         'do serviço e todos os quatro modelos. Pague por mês, por ano ou uma única vez para sempre. Se houver um '
         'período de teste grátis, você verá antes da compra.', True),
        ('Preço garantido', 'Seu preço não muda', 'Não aumentaremos o preço da sua assinatura enquanto ela estiver '
         'ativa. Cancele quando quiser na sua conta da App Store ou do Google Play.', False),
    ],
    priv_h='Seus dados ficam no seu celular',
    priv_p='O Fixbill não precisa de conta. Dados da empresa, clientes, itens, documentos, fotos e assinaturas ficam '
           'salvos apenas no seu aparelho. Nós nunca os vemos.',
    priv_link='Política de privacidade (em inglês)',
    checks=['Sem conta, sem análise, sem anúncios e sem rastreamento.',
            'Os documentos só saem do celular quando você os compartilha, com o app ou serviço que escolher.',
            'Os backups são arquivos que você salva onde quiser.',
            'Funciona sem internet, mesmo na obra.'],
    cta_h='Baixe o Fixbill', cta_sub='Dúvidas? Escreva para {mail}.',
    f_support='Suporte', f_privacy='Privacidade', f_terms='Termos de uso', f_operator='Responsável',
    f_templates='Modelos grátis', f_langs='Idiomas', en_suffix=' (EN)',
    offer='Download grátis com 5 documentos por mês. O Fixbill Pro é uma compra no app: mensal, anual ou vitalícia com '
          'pagamento único.',
    ld_desc='App de orçamento de serviço para autônomos e prestadores: PDF, assinatura do cliente, link de pagamento '
            'com QR code, lembretes. Os dados ficam no aparelho.',
)

LANGS = [EN, EN_GB, CS, SK, DE, FR, ES, IT, PL, PT]
