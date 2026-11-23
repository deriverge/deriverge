# Italian texts of the Tapkasa landing pages. Facts follow tapkasa/README.md and the app texts (version 1.0.8).
# No prices, Tapkasa is not a "registratore telematico" and issues no fiscal documents. No long dashes.

T = dict(
    html_lang='it', hreflang='it', og_locale='it_IT', name='Italiano', currency='EUR',
    gp_badge='badge-googleplay-en.png', as_alt='Scarica su App Store', gp_alt='Disponibile su Google Play',
    brand_sub='La cassa in tasca', menu='Lingua',
    try_btn='Prova nel browser',
    qr_alt="Codice QR per scaricare l'app Tapkasa",
    qr_text='Inquadra il codice con la fotocamera del telefono per scaricare Tapkasa.',
    note='Gratis fino a 10 conti pagati al giorno. Senza registrazione.',
    sticky='La cassa in tasca',
    ld_desc='Una cassa semplice sul telefono per bancarelle, mercatini di Natale, sagre e feste della scuola. '
            'Calcola il resto, mette in coda gli ordini, gestisce le cauzioni e funziona senza internet. I dati '
            'restano sul dispositivo.',
    offer="Gratis fino a 10 conti pagati al giorno. Tapkasa Pro è un abbonamento nell'app (mensile o annuale).",
    h_how='Come funziona',
    how=[
        ('Inserisci il menu', 'Ogni articolo ha un nome, un prezzo e un colore. Bastano pochi minuti a casa, oppure '
                              'parti dal menu di esempio.'),
        ('Tocca le schede', 'Un tocco aggiunge un pezzo, una pressione lunga lo toglie. In basso vedi sempre quanto '
                            'deve pagare il cliente.'),
        ('Contanti o carta', 'Con i contanti Tapkasa calcola il resto. La carta la incassi sul tuo POS e in Tapkasa '
                             'segni soltanto il pagamento.'),
    ],
    h_feat='Cosa fa Tapkasa',
    feats=[
        ('Il resto senza fare i conti', 'Tocchi la banconota che hai ricevuto e vedi quanto restituire.'),
        ('Coda degli ordini con i numeri', 'Ogni conto pagato riceve un numero e resta in coda finché non lo segni '
                                           'come consegnato.'),
        ('Cassa e banco su due telefoni', 'Il secondo dispositivo mostra gli ordini e può leggerli ad alta voce. Il '
                                          'collegamento fa parte di Tapkasa Pro.'),
        ('Funziona senza rete', 'Tutto gira sul telefono. Due iPhone o due telefoni Android si collegano anche senza '
                                'internet.'),
        ('Cauzioni', 'La cauzione per la tazza o il bicchiere e il suo reso sono articoli separati, distinti dalle '
                     'vendite nel riepilogo.'),
        ('I dati restano tuoi', 'Niente account e niente cloud. Salvi una copia di backup in un file, dove vuoi.'),
    ],
    h_shots="Com'è fatta Tapkasa",
    shot_alts=['Schermata di vendita di Tapkasa: schede colorate degli articoli con i prezzi e il totale da pagare',
               'Coda degli ordini con i numeri sul secondo telefono',
               "Riepilogo delle vendite con il dettaglio dell'IVA"],
    h_not='Cosa Tapkasa non è',
    nots=[
        "Non è un registratore telematico né un software fiscale certificato e non invia nulla all'Agenzia delle "
        'Entrate. Il riepilogo delle vendite non è uno scontrino, un documento commerciale o una fattura.',
        'Non gestisce i pagamenti con carta. La carta la incassi sul tuo POS, Tapkasa annota solo la vendita.',
        'Non stampa scontrini né buoni.',
    ],
    not_p="È adatta dove non c'è l'obbligo di memorizzazione telematica dei corrispettivi, oppure come aiuto accanto "
          'al registratore. Verifica i tuoi obblighi con il commercialista.',
    h_price='Quanto costa',
    price=[
        'Gratis: tutto il menu, i riepiloghi, le cauzioni e il backup dei dati su un dispositivo, con 10 conti '
        'pagati al giorno. Un conto che contiene solo il reso di una cauzione non rientra nel limite.',
        "Tapkasa Pro: conti illimitati e collegamento tra cassa e banco. È un abbonamento mensile o annuale tramite "
        "App Store o Google Play, con 14 giorni di prova gratuita per i nuovi abbonati. Il prezzo nella tua valuta "
        "lo vedi nell'app prima dell'acquisto e puoi disdire quando vuoi dalle impostazioni dello store.",
        'Per una bancarella basta un abbonamento: il secondo telefono si collega gratis al dispositivo con Tapkasa '
        'Pro.',
    ],
    h_faq='Domande frequenti',
    faq=[
        ('Tapkasa è gratis?',
         "Sì, fino a 10 conti pagati al giorno su un dispositivo. I conti illimitati e il collegamento di due "
         "dispositivi richiedono l'abbonamento Tapkasa Pro, che i nuovi abbonati possono provare gratis per 14 "
         "giorni."),
        ('È un registratore di cassa fiscale?',
         'No. Tapkasa conta e registra le vendite, ma non è un registratore telematico, non invia dati al fisco e '
         'non emette scontrini né fatture.'),
        ('Dove sono i miei dati?',
         'Solo sul tuo dispositivo. Tapkasa non ha account né cloud. Puoi salvare un backup in un file e caricarlo '
         'su un telefono nuovo.'),
        ('In quali lingue e valute funziona?',
         'In nove lingue (italiano, inglese, tedesco, francese, spagnolo, portoghese, polacco, ceco e slovacco) e in '
         '33 valute, tra cui euro e franco svizzero.'),
    ],
    cta_h="Prova Tapkasa prima dell'evento",
    h_more='Altre guide',
    f_support='Assistenza', f_privacy='Privacy', f_terms="Condizioni d'uso", f_app='Apri Tapkasa nel browser',
    f_langs='Lingue', f_operator='Gestore',
    pages=dict(
        stall=dict(
            path='it/', card='Cassa per bancarella',
            title='Cassa per bancarella sul telefono, anche senza rete | Tapkasa',
            desc='Una cassa semplice per la tua bancarella, sul telefono: schede colorate degli articoli, resto '
                 'calcolato, ordini numerati su un secondo telefono, cauzioni. Funziona senza internet.',
            h1='La cassa della bancarella che sta in tasca',
            eyebrow='Per iPhone, Android e browser',
            lede='Inserisci il menu, tocchi le schede colorate e Tapkasa fa i conti: quanto incassare, quanto resto '
                 'dare e quanto hai venduto oggi. Senza registrazione, senza altri apparecchi e senza internet.',
            sections=[
                ('Come va al banco',
                 '<p>Un cliente chiede due vin brulé e una crêpe. Tocchi due volte il vin brulé, una volta la crêpe '
                 'e in basso compare il totale. Ti dà una banconota da 20, tocchi 20 e Tapkasa mostra il resto. '
                 'Bastano pochi secondi e nessuno fa i conti a mente, nemmeno chi è al banco per la prima '
                 'volta.</p>'),
                ('Due telefoni: cassa e banco',
                 '<p>Quando si forma la fila, un telefono incassa e l’altro mostra gli ordini con il numero. Al '
                 'banco spunti quello che è pronto e puoi farti leggere i nuovi ordini ad alta voce, senza guardare '
                 'lo schermo con le mani occupate. Due iPhone o due telefoni Android si collegano direttamente, '
                 'senza internet. Un iPhone con un Android ha bisogno della connessione.</p>'),
                ('La cauzione per tazza o bicchiere',
                 '<p>Il pulsante «+ Aggiungere cauzione» crea due articoli: Cauzione e Reso cauzione. La tazza '
                 'restituita viene sottratta dal conto e nel riepilogo le cauzioni incassate e rese compaiono a '
                 'parte, senza mescolarsi alle vendite.</p>'),
                ('La sera sai quanto hai incassato',
                 '<p>Il riepilogo mostra il totale delle vendite, contanti e carta separati e i pezzi venduti per '
                 'articolo. Puoi salvare il riepilogo in PDF, per esempio per il commercialista.</p>'),
            ],
            faq=[
                ('Serve la connessione a internet?',
                 "No. Vendita, riepiloghi e backup funzionano sul telefono. Internet serve solo per scaricare l'app, "
                 'acquistare Tapkasa Pro e collegare un iPhone con un Android.'),
                ('Può usarla un aiutante o un volontario?',
                 'Sì. Una vendita è un tocco su una scheda colorata e la scelta Contanti o Carta. Un articolo '
                 'aggiunto per errore si toglie con una pressione lunga.'),
            ],
        ),
        xmas=dict(
            path='it/mercatino-di-natale/', card='Cassa per mercatino di Natale',
            title='Cassa per mercatino di Natale: cauzione tazza e resto | Tapkasa',
            desc='Una cassa sul telefono per il mercatino di Natale: vin brulé con un tocco, cauzione della tazza, '
                 'resto calcolato. Funziona senza rete e senza registrazione, 10 conti al giorno gratis.',
            h1='Una cassa per il mercatino di Natale: vin brulé, dolci e cauzione della tazza',
            eyebrow="Mercatini di Natale e dell'Avvento",
            lede='La piazza è piena, la rete non regge e davanti alla casetta c’è la fila. Tapkasa funziona sul '
                 'telefono anche senza internet, calcola il resto e tiene il conto delle cauzioni delle tazze. Si '
                 'prepara in pochi minuti.',
            sections=[
                ('La cauzione della tazza senza confusione',
                 '<p>Nel Menu tocca «+ Aggiungere cauzione» e inserisci l’importo, per esempio 2 €. Tapkasa crea due '
                 'articoli: Cauzione e Reso cauzione. Con il vin brulé aggiungi la cauzione, quando torna la tazza '
                 'tocchi il reso e l’importo viene sottratto dal conto. Se il cliente riporta soltanto la tazza, '
                 'Tapkasa mostra quanto restituirgli.</p>'
                 '<p>Nel riepilogo le cauzioni incassate e rese sono separate. La sera sai quante tazze sono ancora '
                 'in giro e qual è il vero incasso.</p>'),
                ('Quando in piazza cade la rete',
                 '<p>Vendita, resto e riepilogo girano direttamente sul telefono. Tapkasa non fa nessun accesso e '
                 'non controlla nulla online: una rete sovraccarica o i giga finiti non ti fermano nel momento di '
                 'punta.</p>'),
                ('La fila per il vin brulé',
                 '<p>Un telefono incassa, il secondo al banco mostra gli ordini con il numero e li legge ad alta '
                 'voce. Il cliente riceve un numero e nessuno deve gridare da una parte all’altra della casetta. '
                 'Due iPhone o due telefoni Android si collegano direttamente, senza Wi-Fi e senza dati.</p>'),
                ('Consigli per il freddo',
                 '<ul><li>Arrotonda i prezzi per dare il resto facilmente: 3, 4, 5 €.</li>'
                 '<li>Prepara il menu a casa, al caldo, e metti in alto gli articoli più venduti.</li>'
                 '<li>Porta un power bank. Lo schermo resta acceso durante la vendita e con il freddo la batteria '
                 'dura meno.</li>'
                 '<li>Salva un backup in un file prima del primo giorno di mercatino.</li></ul>'),
            ],
            faq=[
                ('Il reso della cauzione conta nel limite gratuito giornaliero?',
                 'No. Un conto che contiene solo il reso di una cauzione non rientra nei 10 conti pagati al '
                 'giorno.'),
                ('La versione gratuita basta per un mercatino di Natale?',
                 "Per una piccola bancarella con poche vendite al giorno, sì. Per un mercatino affollato conviene "
                 "Tapkasa Pro: i nuovi abbonati hanno 14 giorni gratis, cioè due fine settimana dell'Avvento. "
                 'Tapkasa avvisa in anticipo quando il limite si avvicina.'),
            ],
        ),
        club=dict(
            path='it/festa-della-scuola/', card='Cassa per festa della scuola e sagra',
            title='Cassa per festa della scuola, sagra e associazione | Tapkasa',
            desc="Una cassa sul telefono per la festa della scuola, la sagra o l'evento dell'associazione: i "
                 'volontari toccano gli articoli, il resto è calcolato, il tesoriere riceve il totale in PDF.',
            h1="Una cassa per la festa della scuola, la sagra e l'associazione",
            eyebrow='Feste della scuola, sagre, pro loco, oratori',
            lede='Alla cassa si alternano i volontari e la sera il tesoriere vuole sapere quanto è entrato. Tapkasa '
                 'ricorda i prezzi, calcola il resto e somma l’incasso su un telefono. Senza registrazione e senza '
                 'formazione.',
            sections=[
                ('La sa usare ogni volontario',
                 '<p>Gli articoli sono grandi schede colorate: nessuno cerca in un elenco o fa i conti a mente. Si '
                 'tocca quello che chiede il cliente, si sceglie Contanti o Carta e con i contanti lo schermo '
                 'mostra il resto. Per il cambio turno basta passare il telefono.</p>'),
                ('La sera un totale preciso per il tesoriere',
                 '<p>Il riepilogo mostra il totale delle vendite, contanti e carta separati e quanti pezzi sono '
                 'stati venduti. Invialo in PDF al tesoriere o al direttivo. Dopo la festa scegli «Chiudere '
                 'l’evento»: l’incasso va in archivio e la volta dopo riparti da zero.</p>'),
                ('Niente account, niente verifiche, niente commissioni',
                 '<p>Tapkasa non chiede registrazione, codice fiscale dell’associazione o conto bancario e non '
                 'trattiene nulla dall’incasso. I soldi vanno nella vostra cassetta. I dati restano sul telefono '
                 'usato alla cassa.</p>'),
                ('Eventi più grandi: bar e cucina separati',
                 '<p>A una sagra o a una festa di paese un telefono può incassare al bar mentre un altro mostra gli '
                 'ordini in cucina. Basta un solo abbonamento Tapkasa Pro, con 14 giorni di prova gratuita per i '
                 'nuovi abbonati.</p>'),
            ],
            faq=[
                ('La versione gratuita basta per la festa della scuola?',
                 'Per una festa piccola, sì: 10 conti pagati al giorno sono gratis. Se aspettate più persone, '
                 'attivate prima Tapkasa Pro; i nuovi abbonati hanno 14 giorni di prova gratuita.'),
                ("L'associazione deve registrarsi?",
                 'No. Si scarica Tapkasa e si apre. Non si crea nessun account e non viene verificato nulla.'),
            ],
        ),
    ),
)
