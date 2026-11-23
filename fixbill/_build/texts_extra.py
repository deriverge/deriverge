# Small per-language texts added on 23 November 2026: questions under the older template pages, section headings,
# the QR code caption and the price line of the language pages.
# Prices are the App Store prices from the app repo (lib/services/purchases.dart, demo offering, "ceny po vyrovnání
# Apple", 11 Nov 2026): CZ 49 / 399 / 1 499 Kč, euro area 1,99 / 17,99 / 69,99 €, UK £1.99 / £14.99 / £59.99,
# US $1.99 / $14.99 / $59.99, PL 9,99 / 69,99 / 299,99 zł, BR R$ 12,90 / 99,90 / 399,90. Update them here when
# the store prices change. No long dashes anywhere.

_FREE = {
    'en': ('Is the template really free?',
           'Yes. The template on this page is free with no limit and what you type never leaves your browser. In the '
           'Fixbill app, 5 documents a month are free.'),
    'cs': ('Je vzor opravdu zdarma?',
           'Ano. Vzor na této stránce je zdarma bez omezení a údaje neopouštějí váš prohlížeč. V aplikaci Fixbill je '
           'zdarma 5 dokladů měsíčně.'),
    'de': ('Ist die Vorlage wirklich kostenlos?',
           'Ja. Die Vorlage auf dieser Seite ist ohne Einschränkung kostenlos, Ihre Eingaben verlassen den Browser '
           'nicht. In der App Fixbill sind 5 Dokumente pro Monat kostenlos.'),
    'fr': ('Le modèle est-il vraiment gratuit ?',
           "Oui. Le modèle de cette page est gratuit sans limite et vos données ne quittent pas votre navigateur. "
           "Dans l'application Fixbill, 5 documents par mois sont gratuits."),
    'es': ('¿La plantilla es gratis de verdad?',
           'Sí. La plantilla de esta página es gratis y sin límite, y lo que escribes no sale de tu navegador. En la '
           'app Fixbill son gratis 5 documentos al mes.'),
    'it': ('Il modello è davvero gratis?',
           'Sì. Il modello di questa pagina è gratuito senza limiti e i dati che inserisci non escono dal browser. '
           "Nell'app Fixbill sono gratuiti 5 documenti al mese."),
    'pl': ('Czy wzór jest naprawdę darmowy?',
           'Tak. Wzór na tej stronie jest darmowy bez ograniczeń, a wpisane dane nie opuszczają przeglądarki. '
           'W aplikacji Fixbill za darmo jest 5 dokumentów miesięcznie.'),
}

FAQ = {
    'en-estimate-template': [
        ('Is an estimate legally binding?',
         'An estimate is your best calculation, not a fixed price, unless you call it a quote or a fixed bid. Once '
         'the client signs it, the scope and terms on it become part of your agreement, so write clearly how changes '
         'are handled.'),
        ('How long should an estimate be valid?',
         '30 days is common. If material prices are moving quickly, choose a shorter period and print the date on '
         'the estimate.'),
        _FREE['en'],
    ],
    'en-gb-tradesman-invoice': [
        ('Do I need to be VAT registered to send an invoice?',
         'No. If you are not VAT registered you invoice without VAT and must not show any. The template has a “Not '
         'VAT registered” option.'),
        ('What payment terms can I set?',
         'Whatever you agree with your customer; 14 or 30 days is common. Put the terms and a due date on every '
         'invoice.'),
        _FREE['en'],
    ],
    'cs-faktura-vzor': [
        ('Musí být na faktuře razítko a podpis?',
         'Ne. Razítko ani podpis zákon u faktury nevyžaduje. Důležité jsou údaje o dodavateli, odběrateli, plnění '
         'a ceně.'),
        ('Může neplátce DPH vystavit fakturu?',
         'Ano. Faktura neplátce je běžný obchodní a účetní doklad, jen na ní není DPH. Ve vzoru zvolte „Neplátce '
         'DPH“.'),
        _FREE['cs'],
    ],
    'de-kostenvoranschlag': [
        ('Wie lange ist ein Kostenvoranschlag gültig?',
         'So lange, wie Sie es darauf angeben. Üblich sind zwei bis vier Wochen. Bei stark schwankenden '
         'Materialpreisen wählen Sie besser eine kürzere Frist.'),
        ('Was ist der Unterschied zwischen Kostenvoranschlag und Angebot?',
         'Ein Angebot ist in der Regel verbindlich: Nimmt der Kunde es an, gilt der Preis. Ein Kostenvoranschlag ist '
         'im Normalfall eine unverbindliche Schätzung der voraussichtlichen Kosten.'),
        _FREE['de'],
    ],
    'fr-devis-artisan': [
        ('Un devis signé engage-t-il le client ?',
         "Oui. Un devis daté et signé par le client avec la mention « Bon pour accord » vaut contrat : il engage le "
         "client comme l'artisan sur les travaux et sur le prix."),
        ('Le devis est-il gratuit ?',
         "En principe oui, sauf si vous avez prévenu le client, avant de l'établir, qu'il serait payant. Indiquez "
         "sur le devis s'il est gratuit ou payant."),
        _FREE['fr'],
    ],
    'es-presupuesto-obra': [
        ('¿Un presupuesto firmado es vinculante?',
         'Sí. Cuando el cliente lo acepta y lo firma, el presupuesto obliga a las dos partes al precio y a los '
         'trabajos descritos. Los cambios deben acordarse por escrito antes de hacerlos.'),
        ('¿Cuánto tiempo es válido un presupuesto?',
         'El que indiques en el documento. Lo habitual son 30 días; con precios de materiales inestables conviene '
         'un plazo más corto.'),
        _FREE['es'],
    ],
    'it-preventivo-edile': [
        ('Il preventivo firmato è vincolante?',
         'Sì. Con la firma per accettazione il preventivo diventa un accordo sul prezzo e sui lavori descritti. Le '
         'variazioni vanno concordate per iscritto prima di eseguirle.'),
        ('Quanto dura la validità di un preventivo?',
         'Quella che indichi nel documento. Di solito 30 giorni; con prezzi dei materiali instabili conviene un '
         'termine più breve.'),
        _FREE['it'],
    ],
    'pl-kosztorys-wzor': [
        ('Czy kosztorys jest wiążący?',
         'To zależy od umowy. Przy wynagrodzeniu ryczałtowym cena jest stała. Przy wynagrodzeniu kosztorysowym może '
         'się zmienić, jeśli trzeba wykonać prace nieprzewidziane w zestawieniu, o czym należy uprzedzić '
         'zamawiającego.'),
        ('Jak długo ważna jest wycena?',
         'Tak długo, jak wskazano w dokumencie. Zwykle 14 do 30 dni; przy szybko zmieniających się cenach materiałów '
         'lepiej podać krótszy termin.'),
        _FREE['pl'],
    ],
}

# code: (FAQ heading, heading above other templates in the same language, QR alt, QR caption, price line)
LANG_EXTRA = {
    'en': ('Questions people ask', 'More free templates', 'QR code to download Fixbill',
           'Scan with your phone camera to get Fixbill.',
           'Fixbill Pro costs $1.99 a month, $14.99 a year or $59.99 once for lifetime access (App Store prices in '
           'the US, November 2026; Google Play and other countries may differ slightly). You always see the current '
           'price before you buy.'),
    'en-gb': ('Questions people ask', 'More free templates', 'QR code to download Fixbill',
              'Scan with your phone camera to get Fixbill.',
              'Fixbill Pro costs £1.99 a month, £14.99 a year or £59.99 once for lifetime access (App Store prices '
              'in the UK, November 2026; Google Play may differ slightly). You always see the current price before '
              'you buy.'),
    'cs': ('Časté otázky', 'Další vzory zdarma', 'QR kód ke stažení aplikace Fixbill',
           'Namiřte fotoaparát telefonu na kód a stáhněte si Fixbill.',
           'Fixbill Pro stojí 49 Kč měsíčně, 399 Kč ročně, nebo 1 499 Kč jednorázově navždy (ceny v App Store '
           'v listopadu 2026, na Google Play se mohou mírně lišit). Platnou cenu vždy uvidíte před nákupem.'),
    'sk': ('Časté otázky', 'Ďalšie vzory zadarmo', 'QR kód na stiahnutie aplikácie Fixbill',
           'Namierte fotoaparát telefónu na kód a stiahnite si Fixbill.',
           'Fixbill Pro stojí 1,99 € mesačne, 17,99 € ročne alebo 69,99 € jednorazovo navždy (ceny v App Store '
           'v novembri 2026, na Google Play sa môžu mierne líšiť). Platnú cenu vždy uvidíte pred nákupom.'),
    'de': ('Häufige Fragen', 'Weitere kostenlose Vorlagen', 'QR-Code zum Herunterladen von Fixbill',
           'Handykamera auf den Code richten und Fixbill laden.',
           'Fixbill Pro kostet 1,99 € im Monat, 17,99 € im Jahr oder einmalig 69,99 € für immer (Preise im App Store, '
           'November 2026; bei Google Play können sie leicht abweichen). Den aktuellen Preis sehen Sie immer vor dem '
           'Kauf.'),
    'fr': ('Questions fréquentes', 'Autres modèles gratuits', 'Code QR pour télécharger Fixbill',
           "Visez le code avec l'appareil photo de votre téléphone pour télécharger Fixbill.",
           "Fixbill Pro coûte 1,99 € par mois, 17,99 € par an ou 69,99 € une fois pour toutes (prix sur l'App Store "
           "en novembre 2026 ; ils peuvent varier légèrement sur Google Play). Le prix en vigueur s'affiche toujours "
           "avant l'achat."),
    'es': ('Preguntas frecuentes', 'Más plantillas gratis', 'Código QR para descargar Fixbill',
           'Apunta con la cámara del móvil al código para descargar Fixbill.',
           'Fixbill Pro cuesta 1,99 € al mes, 17,99 € al año o 69,99 € una sola vez para siempre (precios del App '
           'Store en España en noviembre de 2026; en Google Play y en otros países pueden variar). Siempre ves el '
           'precio vigente antes de comprar.'),
    'it': ('Domande frequenti', 'Altri modelli gratuiti', 'Codice QR per scaricare Fixbill',
           'Inquadra il codice con la fotocamera del telefono per scaricare Fixbill.',
           "Fixbill Pro costa 1,99 € al mese, 17,99 € all'anno oppure 69,99 € una volta sola per sempre (prezzi su "
           "App Store a novembre 2026; su Google Play possono variare leggermente). Il prezzo aggiornato lo vedi "
           "sempre prima dell'acquisto."),
    'pl': ('Częste pytania', 'Więcej darmowych wzorów', 'Kod QR do pobrania aplikacji Fixbill',
           'Wystarczy skierować aparat telefonu na kod, aby pobrać Fixbill.',
           'Fixbill Pro kosztuje 9,99 zł miesięcznie, 69,99 zł rocznie albo 299,99 zł jednorazowo na zawsze (ceny '
           'w App Store w listopadzie 2026 r.; w Google Play mogą się nieznacznie różnić). Aktualną cenę zawsze '
           'widać przed zakupem.'),
    'pt': ('Perguntas frequentes', 'Mais modelos grátis', 'QR code para baixar o Fixbill',
           'Aponte a câmera do celular para o código e baixe o Fixbill.',
           'O Fixbill Pro custa R$ 12,90 por mês, R$ 99,90 por ano ou R$ 399,90 uma única vez, para sempre (preços '
           'na App Store no Brasil em novembro de 2026; no Google Play podem variar um pouco). O preço atual aparece '
           'sempre antes da compra.'),
}

# Structured data: Pro prices per language page (monthly, yearly, lifetime) in the page's currency.
PRO_PRICES = {
    'en': ('USD', '1.99', '14.99', '59.99'), 'en-gb': ('GBP', '1.99', '14.99', '59.99'),
    'cs': ('CZK', '49', '399', '1499'), 'pl': ('PLN', '9.99', '69.99', '299.99'),
    'pt': ('BRL', '12.90', '99.90', '399.90'),
    'sk': ('EUR', '1.99', '17.99', '69.99'), 'de': ('EUR', '1.99', '17.99', '69.99'),
    'fr': ('EUR', '1.99', '17.99', '69.99'), 'es': ('EUR', '1.99', '17.99', '69.99'),
    'it': ('EUR', '1.99', '17.99', '69.99'),
}

# Template section on the Slovak and Portuguese language pages (they had no template until now).
TPL_HEAD = {
    'sk': ('Vzory zadarmo na vyplnenie online',
           'Bez aplikácie: vyplníte formulár, skontrolujete náhľad a uložíte PDF. Nič sa nikam neodosiela.'),
    'pt': ('Modelos grátis para preencher online',
           'Sem aplicativo: preencha o formulário, confira a prévia e salve o PDF. Nada é enviado.'),
}
