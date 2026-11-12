# Texts for the Fixbill template pages (search intent pages with an in-browser generator).
# Choice of pages: docs/research/aso_a_konkurence_2026-11.md, section 7.3, in the Fixbill repo.
# Legal notes are written cautiously (state of November 2026) and every page says it is not legal advice.
# Section 7.4: no e-invoicing promises (no e-faktura, XRechnung, KSeF, VeriFactu, SDI, Peppol); "free" for the app
# always with the 5 documents a month limit. `body` and `app.p` are trusted HTML; everything else is escaped.
# No long dashes anywhere.

# Field tuples: (name, label, kind, placeholder, default, extra)
#   kind: text | area | date | sel ; for date, extra = days from today; for sel, extra = [(value, label)]

CS = dict(
    id='cs-faktura-vzor', lang='cs', html_lang='cs', path='cs/faktura-vzor/', phrase='faktura vzor',
    title='Faktura vzor 2026 zdarma: vyplnění online a uložení do PDF | Fixbill',
    desc='Vzor faktury zdarma k vyplnění přímo v prohlížeči, pro neplátce i plátce DPH, s povinnými údaji podle '
         'českých předpisů. Uložte jako PDF nebo vytiskněte, nic se nikam neodesílá.',
    h1='Vzor faktury zdarma k vyplnění online',
    lede='Vyplňte údaje, zkontrolujte náhled a fakturu si vytiskněte nebo uložte jako PDF. Vzor počítá s povinnými '
         'údaji pro neplátce i plátce DPH. Všechno se děje jen ve vašem prohlížeči, nic neodesíláme.',
    jump='Vyplnit fakturu', crumb='Fixbill',
    card='Faktura vzor', card_text='Vzor faktury pro neplátce i plátce DPH. Vyplníte online a uložíte jako PDF.',
    gen=dict(
        kind='invoice', locale='cs-CZ', currency='CZK', currencies=['CZK', 'EUR'], decComma=True, refFromNumber=True,
        dates=['issue', 'supply', 'due'], pay=['account', 'ref', 'method'],
        sign=None, made='Vytvořeno ve Fixbill · deriverge.com/fixbill',
        doc=dict(title='Faktura', no='č.', seller='Dodavatel', buyer='Odběratel', desc='Popis', qty='Množství',
                 unit='Jedn.', price='Cena za jedn.', priceNet='Cena bez DPH', amount='Celkem', amountNet='Bez DPH',
                 net='Základ daně', tax='DPH', total='Celkem k úhradě'),
        ui=dict(items='Položky', add='Přidat položku', remove='Odebrat položku', desc='Popis práce nebo zboží',
                qty='Množství', unit='Jednotka', price='Cena za jednotku', print='Vytisknout nebo uložit PDF',
                reset='Začít znovu', resetAsk='Smazat vyplněné údaje a vrátit ukázku?',
                preview='Náhled faktury',
                privacy='Údaje zůstávají jen ve vašem prohlížeči (uloží se pro příští návštěvu na tomto zařízení). '
                        'PDF uložíte v dialogu tisku volbou „Uložit jako PDF“.',
                noscript='Generátor potřebuje zapnutý JavaScript. Povinné údaje faktury najdete níže.'),
        groups=[
            ('Dodavatel (vy)', [
                ('s_name', 'Jméno nebo firma', 'text', 'Jan Novák', '', None),
                ('s_addr', 'Adresa sídla nebo místa podnikání', 'area', 'Ulice a číslo\nPSČ a obec', '', None),
                ('s_ids', 'IČO, případně DIČ', 'area', 'IČO: 12345678', '', None),
                ('s_extra', 'Zápis v rejstříku', 'text', '', 'Fyzická osoba zapsaná v živnostenském rejstříku.', None),
                ('s_contact', 'E-mail nebo telefon', 'text', 'name@example.com', '', None),
            ]),
            ('Odběratel', [
                ('b_name', 'Jméno nebo firma', 'text', 'Odběratel s.r.o.', '', None),
                ('b_addr', 'Adresa', 'area', 'Ulice a číslo\nPSČ a obec', '', None),
                ('b_ids', 'IČO, DIČ', 'area', 'IČO: 87654321', '', None),
            ]),
            ('Faktura', [
                ('number', 'Číslo faktury', 'text', '2026001', '2026001', None),
                ('issue', 'Datum vystavení', 'date', '', '', 0),
                ('supply', 'Datum uskutečnění plnění (DUZP)', 'date', '', '', 0),
                ('due', 'Datum splatnosti', 'date', '', '', 14),
                ('cur', 'Měna', 'sel', '', 'CZK', [('CZK', 'Kč (CZK)'), ('EUR', 'Euro (EUR)')]),
            ]),
            'items',
            ('DPH', [
                ('tax', 'Režim DPH', 'tax', '', '', None),
            ]),
            ('Platba', [
                ('account', 'Číslo účtu', 'text', '123456789/0100', '', None),
                ('ref', 'Variabilní symbol', 'text', 'doplní se z čísla faktury', '', None),
                ('method', 'Způsob úhrady', 'text', '', 'Převodem na účet', None),
                ('notes', 'Poznámka na faktuře', 'area', 'Například: Děkujeme za zakázku.', '', None),
            ]),
        ],
        tax=[('none', 'Neplátce DPH', 'Nejsem plátce DPH.', ''), ('21', 'Plátce DPH, sazba 21 %', '', ''),
             ('12', 'Plátce DPH, sazba 12 %', '', '')],
        items=[['Obklad stěn', '12', 'm²', '950'], ['Lepidlo a spárovací hmota', '1', 'ks', '2100'],
               ['Práce', '6', 'h', '650']],
    ),
    body='''
<h2>Povinné údaje na faktuře neplátce DPH</h2>
<p>Živnostník, který není plátcem DPH, vystavuje fakturu jako obchodní listinu podle § 435 občanského zákoníku a jako doklad pro svou evidenci. Na faktuře by mělo být:</p>
<ul>
<li>jméno a příjmení nebo název firmy, adresa sídla nebo místa podnikání a IČO,</li>
<li>údaj o zápisu v rejstříku: u živnostníka například „Fyzická osoba zapsaná v živnostenském rejstříku“, u firmy z obchodního rejstříku soud a spisová značka,</li>
<li>údaje o odběrateli: jméno nebo název, adresa, u firem IČO,</li>
<li>číslo faktury, datum vystavení a datum uskutečnění plnění,</li>
<li>co jste dodali (popis práce nebo zboží, množství) a částka k úhradě,</li>
<li>platební údaje: číslo účtu, variabilní symbol a datum splatnosti.</li>
</ul>
<p>Neplátce DPH na faktuře DPH neuvádí. Věta „Nejsem plátce DPH.“ zákon přímo nevyžaduje, ale zákazníkovi ušetří dotazy. Ve vzoru ji doplníte volbou „Neplátce DPH“.</p>

<h2>Co navíc musí mít faktura plátce DPH</h2>
<p>Plátce DPH vystavuje daňový doklad podle § 29 zákona o DPH. Kromě údajů výše na něm musí být:</p>
<ul>
<li>DIČ dodavatele a DIČ odběratele, pokud ho má,</li>
<li>evidenční číslo daňového dokladu,</li>
<li>datum uskutečnění zdanitelného plnění (DUZP), pokud se liší od data vystavení,</li>
<li>jednotková cena bez DPH a případná sleva,</li>
<li>základ daně, sazba daně a výše DPH v korunách.</li>
</ul>
<p>Od roku 2024 platí sazby 21 % a 12 %. Daňový doklad je potřeba vystavit nejpozději do 15 dnů od DUZP.</p>

<h2>Kdy se stáváte plátcem DPH</h2>
<p>Od roku 2025 se plátcem stáváte od 1. ledna následujícího roku, když obrat za kalendářní rok přesáhne 2 000 000 Kč. Pokud během roku přesáhne 2 536 500 Kč, jste plátcem už ode dne následujícího po překročení. Hodnoty si před rozhodnutím ověřte u finanční správy nebo u účetní.</p>

<h2>Aby faktura přišla zaplacená včas</h2>
<ul>
<li><strong>Variabilní symbol</strong> je nejčastěji číslo faktury. Vzor ho z čísla doplní sám, když pole necháte prázdné.</li>
<li><strong>Splatnost</strong> 14 dní je běžná. Mezi podnikateli platí, že lhůta delší než 60 dní musí být výslovně sjednaná a nesmí být vůči věřiteli hrubě nespravedlivá (§ 1963 občanského zákoníku).</li>
<li><strong>Číslování</strong> držte v jedné řadě bez mezer, například 2026001, 2026002.</li>
<li><strong>QR Platba</strong> zákazníkovi ušetří přepisování čísla účtu. V aplikaci Fixbill se na fakturu přidá sama, i s variabilním symbolem a částkou.</li>
</ul>
''',
    fine='Vzor je obecná pomůcka, ne právní ani daňová rada. Stav k listopadu 2026. Ve sporných případech se obraťte na '
         'účetní nebo daňového poradce.',
    app=dict(
        h2='Fakturujte rovnou z telefonu',
        p='Ve Fixbill máte stejnou fakturu za dvě minuty, i se vším, co papírový vzor neumí:',
        bullets=['QR Platba s variabilním symbolem na každé faktuře',
                 'zákazník podepíše nabídku na displeji a z nabídky uděláte fakturu jedním klepnutím (Pro)',
                 'párování plateb z výpisu banky (GPC, CAMT.053, MT940, CSV) nebo přes Fio (Pro)',
                 'upozornění na faktury po splatnosti a upomínka jedním klepnutím'],
        note='Zdarma 5 dokladů měsíčně. Data zůstávají v telefonu.'),
)

DE = dict(
    id='de-kostenvoranschlag', lang='de', html_lang='de', path='de/kostenvoranschlag-vorlage/',
    phrase='Kostenvoranschlag Vorlage',
    title='Kostenvoranschlag Vorlage kostenlos: online ausfüllen, als PDF speichern | Fixbill',
    desc='Kostenlose Kostenvoranschlag Vorlage für Handwerker: online ausfüllen, Vorschau prüfen und als PDF speichern. '
         'Mit den wichtigen Angaben, Hinweisen zu § 649 BGB und zur Kleinunternehmerregelung.',
    h1='Kostenvoranschlag Vorlage für Handwerker',
    lede='Füllen Sie die Vorlage direkt im Browser aus, prüfen Sie die Vorschau und speichern Sie den '
         'Kostenvoranschlag als PDF oder drucken Sie ihn aus. Ihre Eingaben bleiben auf Ihrem Gerät, wir senden nichts.',
    jump='Vorlage ausfüllen', crumb='Fixbill',
    card='Kostenvoranschlag Vorlage', card_text='Kostenvoranschlag für Handwerker online ausfüllen und als PDF '
                                                'speichern.',
    gen=dict(
        kind='estimate', locale='de-DE', currency='EUR', currencies=['EUR', 'CHF'], decComma=True, refFromNumber=False,
        dates=['issue', 'valid'], pay=['terms'],
        sign=['Ort, Datum, Unterschrift Auftragnehmer', 'Auftrag erteilt: Ort, Datum, Unterschrift Kunde'],
        made='Erstellt mit Fixbill · deriverge.com/fixbill',
        doc=dict(title='Kostenvoranschlag', no='Nr.', seller='Auftragnehmer', buyer='Kunde', desc='Leistung',
                 qty='Menge', unit='Einheit', price='Einzelpreis', priceNet='Einzelpreis netto', amount='Gesamt',
                 amountNet='Gesamt netto', net='Summe netto', tax='USt.', total='Gesamtbetrag'),
        ui=dict(items='Positionen', add='Position hinzufügen', remove='Position entfernen',
                desc='Leistung oder Material', qty='Menge', unit='Einheit', price='Einzelpreis',
                print='Drucken oder als PDF speichern', reset='Neu beginnen',
                resetAsk='Alle Eingaben löschen und das Beispiel wiederherstellen?', preview='Vorschau',
                privacy='Ihre Eingaben bleiben im Browser (für den nächsten Besuch auf diesem Gerät gespeichert). Als '
                        'PDF speichern Sie im Druckdialog mit „Als PDF speichern“.',
                noscript='Für den Generator wird JavaScript benötigt. Die Pflichtangaben finden Sie weiter unten.'),
        groups=[
            ('Ihr Betrieb', [
                ('s_name', 'Firma oder Name', 'text', 'Fliesen Muster', '', None),
                ('s_addr', 'Anschrift', 'area', 'Straße und Hausnummer\nPLZ und Ort', '', None),
                ('s_ids', 'Steuernummer oder USt-IdNr.', 'text', 'USt-IdNr. DE123456789', '', None),
                ('s_contact', 'Telefon oder E-Mail', 'text', 'name@example.com', '', None),
            ]),
            ('Kunde', [
                ('b_name', 'Name', 'text', 'Name des Kunden', '', None),
                ('b_addr', 'Anschrift', 'area', 'Straße und Hausnummer\nPLZ und Ort', '', None),
                ('site', 'Ausführungsort (falls anders)', 'area', 'Baustelle', '', None),
            ]),
            ('Kostenvoranschlag', [
                ('number', 'Nummer', 'text', 'KV-2026-001', 'KV-2026-001', None),
                ('issue', 'Datum', 'date', '', '', 0),
                ('valid', 'Gültig bis', 'date', '', '', 30),
                ('start', 'Ausführungszeitraum', 'text', 'z. B. KW 48, ca. 3 Arbeitstage', '', None),
                ('cur', 'Währung', 'sel', '', 'EUR', [('EUR', 'Euro (EUR)'), ('CHF', 'Franken (CHF)')]),
            ]),
            'items',
            ('Umsatzsteuer', [
                ('tax', 'Umsatzsteuer', 'tax', '', '', None),
            ]),
            ('Bedingungen', [
                ('terms', 'Zahlungsbedingungen', 'text', '', 'Zahlbar innerhalb von 14 Tagen nach Rechnungsstellung.',
                 None),
                ('notes', 'Hinweis', 'area', '',
                 'Dieser Kostenvoranschlag ist unverbindlich und kostenlos. Zeichnet sich eine wesentliche '
                 'Überschreitung ab, informieren wir Sie umgehend.', None),
            ]),
        ],
        tax=[('19', '19 % Umsatzsteuer', '', ''), ('7', '7 % Umsatzsteuer', '', ''),
             ('none', 'Kleinunternehmer (§ 19 UStG)', 'Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.', '')],
        items=[['Alte Fliesen entfernen und entsorgen (Arbeitszeit)', '12', 'm²', '18'],
               ['Wandfliesen verlegen (Arbeitszeit)', '12', 'm²', '38'],
               ['Fliesenkleber und Fugenmörtel (Material)', '1', 'pauschal', '84,50']],
    ),
    body='''
<h2>Was in einen Kostenvoranschlag gehört</h2>
<p>Eine feste Form schreibt das Gesetz nicht vor. Damit Ihr Kunde den Kostenvoranschlag versteht und mit anderen vergleichen kann, sollten diese Angaben drinstehen:</p>
<ul>
<li>Name, Anschrift und Kontaktdaten Ihres Betriebs, Steuernummer oder USt-IdNr.,</li>
<li>Name und Anschrift des Kunden und der Ort der Ausführung,</li>
<li>Datum, eine Nummer und wie lange der Kostenvoranschlag gilt,</li>
<li>eine klare Beschreibung der Arbeiten,</li>
<li>Positionen mit Menge, Einheit und Einzelpreis, Arbeitszeit und Material getrennt,</li>
<li>Nettosumme, Umsatzsteuer und Gesamtbetrag,</li>
<li>der Hinweis, ob der Kostenvoranschlag unverbindlich oder verbindlich ist,</li>
<li>der voraussichtliche Ausführungszeitraum und die Zahlungsbedingungen.</li>
</ul>

<h2>Unverbindlich, verbindlich oder Festpreis?</h2>
<p>Ein Kostenvoranschlag ist im Normalfall eine fachliche Schätzung, keine Preisgarantie. Zeigt sich, dass die Kosten den Voranschlag wesentlich überschreiten werden, müssen Sie das dem Kunden unverzüglich mitteilen. Er darf den Vertrag dann kündigen und schuldet nur die bis dahin erbrachte Leistung (§ 649 BGB). Wo „wesentlich“ beginnt, regelt das Gesetz nicht. In der Rechtsprechung werden oft etwa 15 bis 20 Prozent genannt, es kommt aber auf den Einzelfall an.</p>
<p>Übernehmen Sie dagegen die Gewähr für die Kosten (verbindlicher Kostenvoranschlag oder Festpreis), können Sie später in der Regel nicht mehr verlangen, auch wenn die Arbeit aufwendiger wird. Schreiben Sie deshalb ausdrücklich dazu, was gilt.</p>

<h2>Darf ein Kostenvoranschlag etwas kosten?</h2>
<p>Nur wenn Sie das vorher mit dem Kunden vereinbart haben. Nach § 632 Abs. 3 BGB ist ein Kostenvoranschlag im Zweifel nicht zu vergüten. Viele Betriebe vereinbaren für aufwendige Voranschläge eine Gebühr und rechnen sie bei Auftragserteilung an.</p>

<h2>Umsatzsteuer und Kleinunternehmer</h2>
<p>Üblich sind 19 Prozent Umsatzsteuer. Als Kleinunternehmer nach § 19 UStG weisen Sie keine Umsatzsteuer aus und vermerken das, zum Beispiel mit „Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.“ In der Vorlage wählen Sie dafür „Kleinunternehmer“.</p>
<p>Tipp für Privatkunden: Lohnkosten für Handwerkerleistungen im Haushalt können Kunden zum Teil von der Steuer absetzen (§ 35a EStG). Weisen Sie Arbeitszeit und Material deshalb getrennt aus, im Kostenvoranschlag und später in der Rechnung.</p>
''',
    fine='Diese Vorlage ist eine allgemeine Hilfe und keine Rechts- oder Steuerberatung. Stand November 2026. Im '
         'Zweifel fragen Sie Ihren Steuerberater oder Ihre Handwerkskammer.',
    app=dict(
        h2='Angebot und Rechnung direkt vom Handy',
        p='Mit Fixbill schreiben Sie den Kostenvoranschlag vor Ort in zwei Minuten und haben mehr als eine Vorlage:',
        bullets=['Ihr Kunde unterschreibt das Angebot auf dem Display, daraus wird mit einem Tippen die Rechnung (Pro)',
                 'Rechnungen mit GiroCode (EPC-QR-Code) für die Überweisung',
                 'Zahlungsabgleich per Kontoauszug (CAMT.053, MT940, CSV) (Pro)',
                 'Hinweis bei überfälligen Rechnungen und Zahlungserinnerung mit einem Tippen'],
        note='Kostenlos für 5 Dokumente pro Monat. Ihre Daten bleiben auf dem Handy.'),
)

FR = dict(
    id='fr-devis-artisan', lang='fr', html_lang='fr', path='fr/modele-devis-artisan/', phrase='modèle devis artisan',
    title='Modèle de devis artisan gratuit : à remplir en ligne, en PDF | Fixbill',
    desc="Modèle de devis gratuit pour artisan avec les mentions obligatoires : SIRET, assurance, TVA, durée de "
         "validité, bon pour accord. Remplissez-le en ligne et enregistrez-le en PDF, rien n'est envoyé.",
    h1='Modèle de devis gratuit pour artisan',
    lede="Remplissez le devis dans votre navigateur, vérifiez l'aperçu et enregistrez-le en PDF ou imprimez-le. Les "
         "mentions obligatoires sont prévues. Rien n'est envoyé : vos données restent sur votre appareil.",
    jump='Remplir le devis', crumb='Fixbill',
    card='Modèle de devis artisan', card_text="Devis avec les mentions obligatoires, à remplir en ligne et à "
                                              "enregistrer en PDF.",
    gen=dict(
        kind='estimate', locale='fr-FR', currency='EUR', currencies=['EUR', 'CHF'], decComma=True,
        refFromNumber=False, dates=['issue', 'valid'], pay=['terms'],
        sign=["Date et signature de l'entreprise", 'Bon pour accord : date et signature du client'],
        made='Créé avec Fixbill · deriverge.com/fixbill',
        doc=dict(title='Devis', no='n°', seller='Entreprise', buyer='Client', desc='Désignation', qty='Qté',
                 unit='Unité', price='Prix unitaire', priceNet='Prix unitaire HT', amount='Total', amountNet='Total HT',
                 net='Total HT', tax='TVA', total='Total TTC'),
        ui=dict(items='Prestations', add='Ajouter une ligne', remove='Supprimer la ligne',
                desc='Désignation des travaux ou fournitures', qty='Quantité', unit='Unité', price='Prix unitaire',
                print='Imprimer ou enregistrer en PDF', reset='Recommencer',
                resetAsk="Effacer les données saisies et revenir à l'exemple ?", preview='Aperçu du devis',
                privacy='Vos données restent dans votre navigateur (gardées pour votre prochaine visite sur cet '
                        'appareil). Pour un PDF, choisissez « Enregistrer au format PDF » dans la fenêtre '
                        "d'impression.",
                noscript='Le générateur a besoin de JavaScript. Les mentions obligatoires sont décrites plus bas.'),
        groups=[
            ('Votre entreprise', [
                ('s_name', 'Nom ou raison sociale', 'text', 'Martin Rénovation', '', None),
                ('s_addr', 'Adresse', 'area', 'Rue\nCode postal et ville', '', None),
                ('s_ids', 'SIRET, n° de TVA, immatriculation', 'area', 'SIRET 123 456 789 00012', '', None),
                ('s_extra', 'Assurance professionnelle', 'area',
                 'Assureur, n° de contrat, couverture géographique', '', None),
                ('s_contact', 'Téléphone ou e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Client', [
                ('b_name', 'Nom', 'text', 'Nom du client', '', None),
                ('b_addr', 'Adresse', 'area', 'Rue\nCode postal et ville', '', None),
                ('site', 'Adresse du chantier (si différente)', 'area', 'Adresse du chantier', '', None),
            ]),
            ('Devis', [
                ('number', 'Numéro', 'text', 'D-2026-001', 'D-2026-001', None),
                ('issue', 'Date du devis', 'date', '', '', 0),
                ('valid', "Valable jusqu'au", 'date', '', '', 30),
                ('start', 'Début et durée des travaux', 'text', 'Début le 1er décembre, durée 3 jours', '', None),
                ('cur', 'Devise', 'sel', '', 'EUR', [('EUR', 'Euro (EUR)'), ('CHF', 'Franc suisse (CHF)')]),
            ]),
            'items',
            ('TVA', [
                ('tax', 'Taux de TVA', 'tax', '', '', None),
            ]),
            ('Conditions', [
                ('terms', 'Conditions de paiement', 'text', '',
                 'Acompte de 30 % à la signature, solde à la fin des travaux.', None),
                ('notes', 'Mentions', 'area', '', 'Devis gratuit. Tout travail non prévu au présent devis fera '
                 "l'objet d'un avenant signé.", None),
            ]),
        ],
        tax=[('20', 'TVA 20 %', '', ''), ('10', 'TVA 10 % (travaux dans un logement de plus de 2 ans)', '', ''),
             ('5.5', 'TVA 5,5 % (rénovation énergétique)', '', ''),
             ('none', 'Franchise en base (micro-entreprise)', 'TVA non applicable, art. 293 B du CGI', '')],
        items=[["Dépose de l'ancienne faïence", '12', 'm²', '15'], ['Pose de faïence murale', '12', 'm²', '38'],
               ['Colle et joints', '1', 'forfait', '84,50'], ['Frais de déplacement', '1', 'forfait', '30']],
    ),
    body='''
<h2>Quand le devis est obligatoire</h2>
<p>Pour les prestations de dépannage, de réparation et d'entretien dans le bâtiment et l'équipement de la maison, un devis détaillé est obligatoire avant les travaux dès que le montant estimé dépasse 150 € TTC (arrêté du 24 janvier 2017). En dessous de ce montant, le client peut le demander. Pour tous les autres travaux, le devis reste vivement conseillé : une fois signé par le client, il vaut contrat.</p>

<h2>Les mentions à faire figurer</h2>
<ul>
<li>la date du devis et sa durée de validité,</li>
<li>le nom ou la raison sociale, l'adresse et le statut de l'entreprise, le numéro SIREN ou SIRET et l'immatriculation (RCS ou registre national des entreprises),</li>
<li>le numéro de TVA intracommunautaire si vous en avez un,</li>
<li>le nom et l'adresse du client, et l'adresse du chantier si elle est différente,</li>
<li>la date de début et la durée estimée des travaux,</li>
<li>le décompte détaillé : pour chaque prestation, la désignation, la quantité et le prix unitaire, la main-d'œuvre et les frais de déplacement s'il y en a,</li>
<li>le total HT, le taux et le montant de la TVA et le total TTC,</li>
<li>le caractère gratuit ou payant du devis,</li>
<li>pour les travaux soumis à la garantie décennale : l'assurance professionnelle, les coordonnées de l'assureur et la couverture géographique,</li>
<li>un espace « Bon pour accord » avec la date et la signature du client.</li>
</ul>

<h2>Quel taux de TVA sur un devis de travaux ?</h2>
<p>Le taux normal est de 20 %. Les travaux d'amélioration, de transformation, d'aménagement ou d'entretien dans un logement achevé depuis plus de deux ans peuvent relever du taux de 10 %, et certains travaux de rénovation énergétique du taux de 5,5 %. Ces taux réduits sont soumis à conditions : vérifiez-les, ainsi que les justificatifs à conserver, avant de les appliquer.</p>
<p>En franchise en base de TVA (micro-entreprise), vous ne facturez pas de TVA et vous indiquez « TVA non applicable, art. 293 B du CGI ». Dans le modèle, choisissez « Franchise en base ».</p>

<h2>Signature et délai de rétractation</h2>
<p>Le devis signé avec la mention « Bon pour accord » engage les deux parties. Si le contrat est conclu au domicile du client, celui-ci dispose en principe de 14 jours pour se rétracter, avec des exceptions, par exemple pour des réparations urgentes qu'il a lui-même demandées. Si le client veut que les travaux commencent pendant ce délai, demandez-lui de le confirmer par écrit.</p>
''',
    fine="Ce modèle est une aide générale, pas un conseil juridique ou fiscal. État au mois de novembre 2026. En cas de "
         "doute, renseignez-vous auprès de votre chambre de métiers ou de votre comptable.",
    app=dict(
        h2='Le devis signé sur le chantier',
        p='Avec Fixbill, le même devis est prêt en deux minutes sur votre téléphone, avec ce que le papier ne fait pas :',
        bullets=["votre client signe le devis sur l'écran, puis il devient facture d'un geste (Pro)",
                 'factures avec QR code EPC pour le virement',
                 'rapprochement des paiements à partir de votre relevé bancaire (CAMT.053, MT940, CSV) (Pro)',
                 'alerte en cas de retard de paiement et relance en un geste'],
        note='Gratuit pour 5 documents par mois. Vos données restent sur votre téléphone.'),
)

IT = dict(
    id='it-preventivo-edile', lang='it', html_lang='it', path='it/modello-preventivo-edile/',
    phrase='preventivo lavori edili',
    title='Modello preventivo lavori edili gratis: compila online e salva in PDF | Fixbill',
    desc='Modello di preventivo per lavori edili e ristrutturazioni da compilare online: voci di computo, oneri della '
         'sicurezza, IVA, tempi e firma per accettazione. Salva in PDF, nessun dato inviato.',
    h1='Modello di preventivo per lavori edili',
    lede="Compila il preventivo nel browser, controlla l'anteprima e salvalo in PDF o stampalo. I dati restano sul tuo "
         "dispositivo: non inviamo nulla.",
    jump='Compila il preventivo', crumb='Fixbill',
    card='Modello preventivo lavori edili', card_text='Preventivo edile da compilare online e salvare in PDF.',
    gen=dict(
        kind='estimate', locale='it-IT', currency='EUR', currencies=['EUR', 'CHF'], decComma=True,
        refFromNumber=False, dates=['issue', 'valid'], pay=['terms'],
        sign=["Data e firma dell'impresa", 'Per accettazione: data e firma del cliente'],
        made='Creato con Fixbill · deriverge.com/fixbill',
        doc=dict(title='Preventivo', no='n.', seller='Impresa', buyer='Cliente', desc='Descrizione', qty='Q.tà',
                 unit='U.m.', price='Prezzo unitario', priceNet='Prezzo unitario', amount='Importo',
                 amountNet='Imponibile', net='Totale imponibile', tax='IVA', total='Totale'),
        ui=dict(items='Voci', add='Aggiungi voce', remove='Rimuovi voce', desc='Descrizione del lavoro o materiale',
                qty='Quantità', unit='Unità di misura', price='Prezzo unitario', print='Stampa o salva in PDF',
                reset='Ricomincia', resetAsk="Cancellare i dati inseriti e tornare all'esempio?",
                preview='Anteprima del preventivo',
                privacy='I dati restano nel tuo browser (salvati per la prossima visita su questo dispositivo). Per il '
                        'PDF scegli «Salva come PDF» nella finestra di stampa.',
                noscript='Il generatore richiede JavaScript. Le voci da inserire sono descritte più sotto.'),
        groups=[
            ('La tua impresa', [
                ('s_name', 'Ragione sociale o nome', 'text', 'Edil Rossi', '', None),
                ('s_addr', 'Sede', 'area', 'Via e numero\nCAP e comune', '', None),
                ('s_ids', 'Partita IVA e codice fiscale', 'area', 'P. IVA 01234567890', '', None),
                ('s_contact', 'Telefono o e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Cliente', [
                ('b_name', 'Nome', 'text', 'Nome del cliente', '', None),
                ('b_addr', 'Indirizzo', 'area', 'Via e numero\nCAP e comune', '', None),
                ('site', 'Indirizzo del cantiere (se diverso)', 'area', 'Indirizzo del cantiere', '', None),
            ]),
            ('Preventivo', [
                ('number', 'Numero', 'text', '2026/001', '2026/001', None),
                ('issue', 'Data', 'date', '', '', 0),
                ('valid', 'Valido fino al', 'date', '', '', 30),
                ('start', 'Tempi di esecuzione', 'text', 'Inizio lavori entro 15 giorni, durata 5 giorni', '', None),
                ('cur', 'Valuta', 'sel', '', 'EUR', [('EUR', 'Euro (EUR)'), ('CHF', 'Franco svizzero (CHF)')]),
            ]),
            'items',
            ('IVA', [
                ('tax', 'Aliquota IVA', 'tax', '', '', None),
            ]),
            ('Condizioni', [
                ('terms', 'Modalità di pagamento', 'text', '', '30% alla firma, saldo a fine lavori.', None),
                ('notes', 'Note', 'area', '', 'Sono esclusi i lavori non indicati nel presente preventivo. Eventuali '
                 'varianti saranno concordate per iscritto.', None),
            ]),
        ],
        tax=[('22', 'IVA 22%', '', ''), ('10', 'IVA 10% (manutenzione su abitazioni)', '', ''),
             ('4', 'IVA 4%', '', ''),
             ('none', 'Regime forfettario (senza IVA)', "Operazione senza applicazione dell'IVA ai sensi dell'art. 1, "
              "commi 54-89, L. 190/2014 (regime forfettario).", '')],
        items=[['Demolizione rivestimento esistente e smaltimento', '12', 'm²', '18'],
               ['Posa rivestimento bagno', '12', 'm²', '35'], ['Collante e stucco', '1', 'a corpo', '70'],
               ['Oneri per la sicurezza', '1', 'a corpo', '50']],
    ),
    body='''
<h2>Cosa scrivere in un preventivo edile</h2>
<p>La legge non impone un modello unico, ma un preventivo chiaro evita contestazioni. Di solito contiene:</p>
<ul>
<li>i dati dell'impresa: ragione sociale o nome, sede, partita IVA e codice fiscale,</li>
<li>i dati del cliente e l'indirizzo del cantiere,</li>
<li>data, numero e validità del preventivo,</li>
<li>la descrizione dei lavori e le voci di computo con unità di misura, quantità e prezzo unitario,</li>
<li>gli oneri per la sicurezza, se previsti, indicati a parte,</li>
<li>il totale imponibile, l'aliquota e l'importo IVA e il totale,</li>
<li>i tempi di esecuzione e le modalità di pagamento (acconto, stati di avanzamento, saldo),</li>
<li>lo spazio per la firma per accettazione del cliente.</li>
</ul>

<h2>Il preventivo firmato è un contratto</h2>
<p>Quando il cliente lo firma per accettazione, il preventivo diventa un contratto d'appalto (art. 1655 e seguenti del codice civile). Le variazioni ai lavori vanno concordate (art. 1659 e 1660 c.c.). Se i costi di materiali o manodopera cambiano per circostanze imprevedibili e fanno variare il prezzo di oltre un decimo, si può chiedere una revisione per la parte che supera il decimo (art. 1664 c.c.). Descrivete con precisione cosa è incluso e cosa no.</p>

<h2>IVA nei lavori edili</h2>
<p>L'aliquota ordinaria è il 22%. Per molti interventi di manutenzione ordinaria e straordinaria su abitazioni si applica il 10%, con regole particolari per i cosiddetti beni significativi (ad esempio caldaie, infissi e sanitari). Per alcune costruzioni, come la prima casa, può valere il 4%. In regime forfettario non si applica l'IVA. Verifica sempre l'aliquota corretta con il tuo commercialista.</p>

<h2>Bonus edilizi e pagamenti</h2>
<p>Se il cliente vuole usare una detrazione fiscale per i lavori, di solito deve pagare con bonifico parlante, che riporta la causale, il codice fiscale di chi usa la detrazione e la partita IVA dell'impresa. Le regole sui bonus cambiano spesso: indicate nel preventivo che le condizioni vanno verificate al momento dei lavori.</p>
<p>Questo modello serve per il preventivo e non sostituisce la fattura.</p>
''',
    fine="Questo modello è un aiuto generale, non una consulenza legale o fiscale. Aggiornato a novembre 2026. Nei casi "
         "dubbi rivolgiti al tuo commercialista o alla tua associazione di categoria.",
    app=dict(
        h2='Il preventivo firmato in cantiere',
        p='Con Fixbill lo stesso preventivo è pronto in due minuti sul telefono, con quello che un modello non fa:',
        bullets=['il cliente firma il preventivo sul tuo schermo (Pro)',
                 'foto del cantiere allegate al preventivo (Pro)',
                 'link di pagamento PayPal o Stripe con QR code sul documento',
                 'avviso alla scadenza e sollecito gentile con un tocco'],
        note='Gratis fino a 5 documenti al mese. I dati restano sul telefono.'),
)

GB = dict(
    id='en-gb-tradesman-invoice', lang='en-gb', html_lang='en-GB', path='en-gb/tradesman-invoice-template/',
    phrase='tradesman invoice template',
    title='Tradesman Invoice Template (UK): Free, Fill In Online and Save as PDF | Fixbill',
    desc='Free invoice template for tradesmen and sole traders in the UK. Fill it in online, with or without VAT, '
         'check the preview and save it as a PDF. Nothing is uploaded.',
    h1='Free invoice template for tradesmen',
    lede='Fill in the invoice in your browser, check the preview and save it as a PDF or print it. It works for sole '
         'traders and limited companies, VAT registered or not. Your details stay on your device.',
    jump='Fill in the invoice', crumb='Fixbill',
    card='Tradesman invoice template (UK)', card_text='Invoice for sole traders and small firms, with or without VAT. '
                                                      'Fill in online, save as PDF.',
    gen=dict(
        kind='invoice', locale='en-GB', currency='GBP', currencies=['GBP', 'EUR'], decComma=False,
        refFromNumber=False, dates=['issue', 'supply', 'due'], pay=['account', 'ref', 'terms'],
        sign=None, made='Created with Fixbill · deriverge.com/fixbill',
        doc=dict(title='Invoice', no='No.', seller='From', buyer='Bill to', desc='Description', qty='Qty',
                 unit='Unit', price='Unit price', priceNet='Unit price excl. VAT', amount='Amount',
                 amountNet='Net', net='Subtotal (excl. VAT)', tax='VAT', total='Total due'),
        ui=dict(items='Work and materials', add='Add a line', remove='Remove line', desc='Description',
                qty='Qty', unit='Unit', price='Unit price', print='Print or save as PDF', reset='Start again',
                resetAsk='Clear what you typed and bring back the example?', preview='Invoice preview',
                privacy='Your details stay in your browser (kept for your next visit on this device). To get a PDF, '
                        'choose “Save as PDF” in the print dialog.',
                noscript='The generator needs JavaScript. What an invoice must include is listed below.'),
        groups=[
            ('Your business', [
                ('s_name', 'Your name or business name', 'text', 'J. Smith Plumbing', '', None),
                ('s_addr', 'Business address', 'area', 'Street\nTown and postcode', '', None),
                ('s_ids', 'VAT number or company number (if any)', 'area', 'VAT reg. no. GB123456789', '', None),
                ('s_contact', 'Phone or e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Customer', [
                ('b_name', 'Customer name', 'text', 'Customer or company name', '', None),
                ('b_addr', 'Customer address', 'area', 'Street\nTown and postcode', '', None),
                ('site', 'Job address (if different)', 'area', 'Job address', '', None),
            ]),
            ('Invoice', [
                ('number', 'Invoice number', 'text', 'INV-0001', 'INV-0001', None),
                ('issue', 'Invoice date', 'date', '', '', 0),
                ('supply', 'Date of work (tax point)', 'date', '', '', 0),
                ('due', 'Payment due', 'date', '', '', 14),
                ('cur', 'Currency', 'sel', '', 'GBP', [('GBP', 'Pound (GBP)'), ('EUR', 'Euro (EUR)')]),
            ]),
            'items',
            ('VAT', [
                ('tax', 'VAT', 'tax', '', '', None),
            ]),
            ('Payment', [
                ('account', 'Bank details', 'area', 'Account name\nSort code 00-00-00\nAccount number 12345678', '',
                 None),
                ('ref', 'Payment reference', 'text', 'INV-0001', '', None),
                ('terms', 'Payment terms', 'text', '', 'Payment within 14 days of the invoice date.', None),
                ('notes', 'Notes', 'area', 'For example: Thank you for your business.', '', None),
            ]),
        ],
        tax=[('none', 'Not VAT registered', '', ''), ('20', 'VAT 20% (standard rate)', '', ''),
             ('5', 'VAT 5% (reduced rate)', '', ''), ('0', 'VAT 0% (zero rate)', '', '')],
        items=[['Remove old wall tiles and dispose', '6', 'h', '40'],
               ['Supply and fit bathroom wall tiles', '12', 'm²', '34'],
               ['Tile adhesive and grout', '1', 'item', '72.50']],
    ),
    body='''
<h2>What a UK invoice must include</h2>
<p>GOV.UK sets out what an invoice has to show. For a tradesman that means:</p>
<ul>
<li>a unique invoice number,</li>
<li>your business name and address (as a sole trader, your own name and any business name you use),</li>
<li>the customer's name or business name and address,</li>
<li>a clear description of the work and materials,</li>
<li>the date the work was done (date of supply) and the date of the invoice,</li>
<li>the amount charged for each item and the total amount due.</li>
</ul>
<p>A limited company must use its full name as it appears on the certificate of incorporation. If you show the names of your directors, you have to show all of them.</p>

<h2>When you are VAT registered</h2>
<p>A VAT invoice also needs your VAT registration number, the time of supply (tax point), the VAT rate for each item, the amount of VAT, and the totals with and without VAT. The standard rate is 20%. Some building work, such as installing certain energy saving materials or converting and renovating empty homes, can have a reduced or zero rate. Check HMRC's guidance for the job before you use it.</p>
<p>You must register for VAT when your taxable turnover goes over £90,000 in a rolling 12 month period (threshold from April 2024).</p>
<p>If you are a VAT registered subcontractor working for a VAT registered contractor under CIS, the construction domestic reverse charge may apply. The invoice then says that the customer accounts for the VAT, instead of you charging it.</p>

<h2>Getting paid on time</h2>
<ul>
<li><strong>Payment terms:</strong> put them on every invoice, for example 14 or 30 days.</li>
<li><strong>Bank details:</strong> account name, sort code and account number, and ask customers to use the invoice number as the payment reference.</li>
<li><strong>Late payment:</strong> with business customers you can usually claim statutory interest of 8% above the Bank of England base rate plus a fixed sum for each late invoice.</li>
<li><strong>Card payments:</strong> in the Fixbill app you can add your own PayPal or Stripe payment link, and the invoice gets a QR code to pay it.</li>
</ul>
''',
    fine='This template is general help, not legal or tax advice. Last checked November 2026. If in doubt, ask your '
         'accountant or check GOV.UK.',
    app=dict(
        h2='Invoice from the van, not the kitchen table',
        p='With Fixbill the same invoice takes two minutes on your phone, plus what a template cannot do:',
        bullets=['your customer signs the quote on your screen, then it becomes the invoice with one tap (Pro)',
                 'a QR code for your own PayPal or Stripe payment link',
                 'bank payments matched from your statement (CAMT.053, MT940, CSV) (Pro)',
                 'an alert when an invoice is overdue and a polite reminder with one tap'],
        note='Free for 5 documents a month. Your data stays on your phone.'),
)

ES = dict(
    id='es-presupuesto-obra', lang='es', html_lang='es', path='es/modelo-presupuesto-obra/',
    phrase='presupuesto de obra plantilla',
    title='Modelo de presupuesto de obra gratis: plantilla para rellenar online | Fixbill',
    desc='Plantilla de presupuesto de obra y reforma gratis: partidas con mediciones, IVA, plazo, forma de pago y firma '
         'de aceptación. Rellénala online y guárdala en PDF sin enviar tus datos.',
    h1='Modelo de presupuesto de obra y reforma',
    lede='Rellena el presupuesto en tu navegador, revisa la vista previa y guárdalo en PDF o imprímelo. Tus datos se '
         'quedan en tu dispositivo: no enviamos nada.',
    jump='Rellenar el presupuesto', crumb='Fixbill',
    card='Modelo de presupuesto de obra', card_text='Plantilla de presupuesto para obras y reformas, online y en PDF.',
    gen=dict(
        kind='estimate', locale='es-ES', currency='EUR', currencies=['EUR'], decComma=True, refFromNumber=False,
        dates=['issue', 'valid'], pay=['terms'],
        sign=['Fecha y firma de la empresa', 'Aceptado: fecha y firma del cliente'],
        made='Creado con Fixbill · deriverge.com/fixbill',
        doc=dict(title='Presupuesto', no='n.º', seller='Empresa', buyer='Cliente', desc='Partida', qty='Cant.',
                 unit='Ud.', price='Precio unitario', priceNet='Precio unitario', amount='Importe',
                 amountNet='Importe', net='Base imponible', tax='IVA', total='Total'),
        ui=dict(items='Partidas', add='Añadir partida', remove='Quitar partida', desc='Descripción de la partida',
                qty='Cantidad', unit='Unidad', price='Precio unitario', print='Imprimir o guardar en PDF',
                reset='Empezar de nuevo', resetAsk='¿Borrar los datos y volver al ejemplo?',
                preview='Vista previa del presupuesto',
                privacy='Tus datos se quedan en el navegador (guardados para tu próxima visita en este dispositivo). '
                        'Para el PDF, elige «Guardar como PDF» en la ventana de impresión.',
                noscript='El generador necesita JavaScript. Lo que debe incluir un presupuesto está más abajo.'),
        groups=[
            ('Tu empresa', [
                ('s_name', 'Nombre o razón social', 'text', 'Reformas García', '', None),
                ('s_addr', 'Domicilio', 'area', 'Calle y número\nCódigo postal y localidad', '', None),
                ('s_ids', 'NIF', 'text', 'NIF 12345678Z', '', None),
                ('s_contact', 'Teléfono o correo', 'text', 'name@example.com', '', None),
            ]),
            ('Cliente', [
                ('b_name', 'Nombre', 'text', 'Nombre del cliente', '', None),
                ('b_addr', 'Domicilio', 'area', 'Calle y número\nCódigo postal y localidad', '', None),
                ('site', 'Dirección de la obra (si es otra)', 'area', 'Dirección de la obra', '', None),
            ]),
            ('Presupuesto', [
                ('number', 'Número', 'text', 'P-2026-001', 'P-2026-001', None),
                ('issue', 'Fecha', 'date', '', '', 0),
                ('valid', 'Válido hasta', 'date', '', '', 30),
                ('start', 'Plazo de ejecución', 'text', 'Inicio en 15 días, duración 5 días laborables', '', None),
            ]),
            'items',
            ('Impuestos', [
                ('tax', 'Tipo de IVA', 'tax', '', '', None),
            ]),
            ('Condiciones', [
                ('terms', 'Forma de pago', 'text', '', '30 % al aceptar, 40 % a mitad de obra y 30 % al terminar.',
                 None),
                ('notes', 'Observaciones', 'area', '', 'No incluye trabajos no descritos en este presupuesto. '
                 'Cualquier cambio se acordará por escrito.', None),
            ]),
        ],
        tax=[('21', 'IVA 21 %', '', ''), ('10', 'IVA 10 % (reforma de vivienda, con requisitos)', '', ''),
             ('7', 'IGIC 7 % (Canarias)', '', 'IGIC')],
        items=[['Demolición de alicatado existente y retirada de escombros', '12', 'm²', '14'],
               ['Alicatado de paredes de baño', '12', 'm²', '32'],
               ['Cemento cola y material de rejuntado', '1', 'ud', '68,50'],
               ['Mano de obra de fontanería', '4', 'h', '35']],
    ),
    body='''
<h2>Qué debe incluir un presupuesto de obra</h2>
<ul>
<li>tus datos: nombre o razón social, NIF y domicilio,</li>
<li>los datos del cliente y la dirección de la obra,</li>
<li>la fecha, un número y el plazo de validez del presupuesto,</li>
<li>la descripción de los trabajos por partidas, con medición, unidad y precio unitario,</li>
<li>materiales y mano de obra, y el desplazamiento si lo cobras,</li>
<li>la base imponible, el tipo y la cuota de IVA y el total,</li>
<li>el plazo de ejecución y la forma de pago (por ejemplo, un anticipo, pagos según avance la obra y la liquidación final),</li>
<li>un espacio para la fecha y la firma de aceptación del cliente.</li>
</ul>

<h2>Presupuesto previo y validez</h2>
<p>En reparaciones y servicios a domicilio, la normativa de consumo de muchas comunidades autónomas obliga a ofrecer al cliente un presupuesto previo por escrito, al que puede renunciar de forma expresa. Si cobras por hacer el presupuesto, avísalo antes. Indica siempre cuánto tiempo es válido: algunas comunidades fijan un plazo mínimo cuando no se dice nada.</p>
<p>El presupuesto aceptado y firmado obliga a las dos partes. Cualquier cambio en los trabajos o en el precio debe acordarse por escrito antes de hacerlo.</p>

<h2>IVA en obras y reformas</h2>
<p>El tipo general es el 21 %. Las obras de renovación y reparación de una vivienda particular pueden ir al 10 % si se cumplen varios requisitos: entre otros, que el cliente sea un particular que no actúa como empresario, que la vivienda se terminara hace al menos dos años y que los materiales que aportas no superen el 40 % de la base imponible. Compruébalo con tu gestor antes de aplicarlo. En Canarias se aplica el IGIC en lugar del IVA.</p>

<h2>Consejos para que te acepten el presupuesto</h2>
<ul>
<li>Divide la obra en partidas claras: el cliente compara mejor y discute menos.</li>
<li>Deja claro lo que no está incluido, por ejemplo licencias, contenedor o pintura.</li>
<li>Envíalo el mismo día de la visita, cuando el cliente todavía tiene la obra en la cabeza.</li>
<li>Añade fotos del estado actual para evitar malentendidos.</li>
</ul>
''',
    fine='Esta plantilla es una ayuda general, no asesoramiento legal ni fiscal. Revisada en noviembre de 2026. Si tienes '
         'dudas, consulta a tu gestor o a la oficina de consumo de tu comunidad.',
    app=dict(
        h2='El presupuesto firmado en la obra',
        p='Con Fixbill el mismo presupuesto está listo en dos minutos en el móvil, con lo que una plantilla no hace:',
        bullets=['el cliente firma el presupuesto en tu pantalla y lo conviertes en factura con un toque (Pro)',
                 'enlace de pago de PayPal o Stripe con código QR en el documento',
                 'cobros del banco conciliados a partir del extracto (CAMT.053, MT940, CSV) (Pro)',
                 'aviso de facturas vencidas y recordatorio amable con un toque'],
        note='Gratis hasta 5 documentos al mes. Tus datos se quedan en tu móvil.'),
)

PL = dict(
    id='pl-kosztorys-wzor', lang='pl', html_lang='pl', path='pl/kosztorys-wzor/', phrase='kosztorys wzór, wycena usługi',
    title='Kosztorys wzór do wypełnienia online za darmo (PDF) | Fixbill',
    desc='Darmowy wzór kosztorysu i wyceny usługi do wypełnienia w przeglądarce: pozycje z obmiarem, robocizna i '
         'materiały, VAT, termin i akceptacja klienta. Zapisz jako PDF, dane nie są nigdzie wysyłane.',
    h1='Wzór kosztorysu remontu do wypełnienia',
    lede='Wypełnij kosztorys lub wycenę usługi w przeglądarce, sprawdź podgląd i zapisz PDF albo wydrukuj. Dane '
         'zostają na Twoim urządzeniu, niczego nie wysyłamy.',
    jump='Wypełnij kosztorys', crumb='Fixbill',
    card='Kosztorys wzór', card_text='Kosztorys i wycena usługi do wypełnienia online i zapisania w PDF.',
    gen=dict(
        kind='estimate', locale='pl-PL', currency='PLN', currencies=['PLN', 'EUR'], decComma=True,
        refFromNumber=False, dates=['issue', 'valid'], pay=['terms'],
        sign=['Data i podpis wykonawcy', 'Akceptuję: data i podpis klienta'],
        made='Utworzono w Fixbill · deriverge.com/fixbill',
        doc=dict(title='Kosztorys', no='nr', seller='Wykonawca', buyer='Zamawiający', desc='Opis pozycji',
                 qty='Ilość', unit='J.m.', price='Cena jedn.', priceNet='Cena jedn. netto', amount='Wartość',
                 amountNet='Wartość netto', net='Razem netto', tax='VAT', total='Razem brutto'),
        ui=dict(items='Pozycje', add='Dodaj pozycję', remove='Usuń pozycję', desc='Opis pracy lub materiału',
                qty='Ilość', unit='Jednostka', price='Cena jednostkowa', print='Drukuj lub zapisz PDF',
                reset='Zacznij od nowa', resetAsk='Usunąć wpisane dane i przywrócić przykład?',
                preview='Podgląd kosztorysu',
                privacy='Dane zostają w przeglądarce (zapisane na następną wizytę na tym urządzeniu). PDF zapiszesz '
                        'w oknie drukowania, wybierając „Zapisz jako PDF”.',
                noscript='Generator wymaga JavaScriptu. Co powinien zawierać kosztorys, opisujemy niżej.'),
        groups=[
            ('Wykonawca', [
                ('s_name', 'Imię i nazwisko lub nazwa firmy', 'text', 'Usługi Remontowe Kowalski', '', None),
                ('s_addr', 'Adres', 'area', 'Ulica i numer\nKod pocztowy i miejscowość', '', None),
                ('s_ids', 'NIP', 'text', 'NIP 123-456-78-90', '', None),
                ('s_contact', 'Telefon lub e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Zamawiający', [
                ('b_name', 'Imię i nazwisko lub nazwa', 'text', 'Dane klienta', '', None),
                ('b_addr', 'Adres', 'area', 'Ulica i numer\nKod pocztowy i miejscowość', '', None),
                ('site', 'Adres wykonania prac (jeśli inny)', 'area', 'Adres budowy', '', None),
            ]),
            ('Kosztorys', [
                ('number', 'Numer', 'text', 'K/2026/001', 'K/2026/001', None),
                ('issue', 'Data', 'date', '', '', 0),
                ('valid', 'Ważny do', 'date', '', '', 30),
                ('start', 'Termin wykonania', 'text', 'Rozpoczęcie do 2 tygodni, czas pracy 5 dni', '', None),
                ('cur', 'Waluta', 'sel', '', 'PLN', [('PLN', 'Złoty (PLN)'), ('EUR', 'Euro (EUR)')]),
            ]),
            'items',
            ('VAT', [
                ('tax', 'Stawka VAT', 'tax', '', '', None),
            ]),
            ('Warunki', [
                ('terms', 'Warunki płatności', 'text', '', 'Zaliczka 30% przed rozpoczęciem, reszta po odbiorze prac.',
                 None),
                ('notes', 'Uwagi', 'area', '', 'Kosztorys orientacyjny. Ostateczna kwota zależy od obmiaru po wykonaniu '
                 'prac. Nie obejmuje prac nieujętych w zestawieniu.', None),
            ]),
        ],
        tax=[('23', 'VAT 23%', '', ''), ('8', 'VAT 8% (remont lokalu mieszkalnego, z warunkami)', '', ''),
             ('none', 'Zwolnienie z VAT (art. 113)', 'Zwolnienie z VAT na podstawie art. 113 ust. 1 ustawy o VAT.',
              '')],
        items=[['Skucie starych płytek z wywozem gruzu', '12', 'm²', '45'],
               ['Układanie płytek ściennych', '12', 'm²', '120'], ['Klej i fuga', '1', 'kpl.', '280'],
               ['Biały montaż (robocizna)', '6', 'rbh', '90']],
    ),
    body='''
<h2>Co powinien zawierać kosztorys lub wycena</h2>
<ul>
<li>dane wykonawcy: imię i nazwisko lub nazwę firmy, adres i NIP,</li>
<li>dane klienta i adres wykonania prac,</li>
<li>datę, numer i termin ważności oferty,</li>
<li>opis prac i pozycje z jednostką, ilością (obmiarem) i ceną jednostkową,</li>
<li>robociznę i materiały osobno, a także sprzęt i transport, jeśli je liczysz,</li>
<li>wartość netto, stawkę i kwotę VAT oraz wartość brutto,</li>
<li>termin wykonania i warunki płatności, na przykład zaliczkę i płatność końcową,</li>
<li>miejsce na akceptację i podpis klienta.</li>
</ul>

<h2>Wynagrodzenie kosztorysowe czy ryczałtowe</h2>
<p>Kodeks cywilny rozróżnia dwa sposoby ustalenia ceny. Przy wynagrodzeniu kosztorysowym (art. 629 k.c.) cena wynika z zestawienia planowanych prac i przewidywanych kosztów, więc ostateczna kwota może się zmienić. Jeśli kosztorys przygotował wykonawca, podwyższenia może żądać tylko za prace dodatkowe, których mimo należytej staranności nie dało się przewidzieć, i nigdy za prace wykonane bez zgody klienta (art. 630 k.c.). Gdy potrzebne jest znaczne podwyższenie, klient może niezwłocznie odstąpić od umowy, płacąc za wykonaną część (art. 631 k.c.).</p>
<p>Przy wynagrodzeniu ryczałtowym (art. 632 k.c.) kwota jest stała, nawet jeśli pracy było więcej. Zapisz na dokumencie, którą formę wybierasz.</p>

<h2>Stawka VAT przy remontach</h2>
<p>Podstawowa stawka VAT to 23%. Dla robót budowlanych, remontowych i modernizacyjnych w budownictwie objętym społecznym programem mieszkaniowym, czyli między innymi w lokalach mieszkalnych do 150 m² i domach do 300 m², można zastosować 8%, z wyjątkami. Jeśli korzystasz ze zwolnienia podmiotowego (art. 113 ustawy o VAT), nie doliczasz VAT. Przed zastosowaniem obniżonej stawki sprawdź warunki z księgowym.</p>

<h2>Jak przygotować wycenę, którą klient przyjmie</h2>
<ul>
<li>Rozbij prace na pozycje z obmiarem w m², mb albo sztukach.</li>
<li>Zapisz, czego wycena nie obejmuje, na przykład wywozu gruzu czy materiałów klienta.</li>
<li>Napisz wprost, czy kosztorys jest orientacyjny, czy cena jest ryczałtowa.</li>
<li>Wyślij wycenę jeszcze tego samego dnia, gdy klient pamięta oględziny.</li>
</ul>
''',
    fine='Wzór jest ogólną pomocą, a nie poradą prawną ani podatkową. Stan na listopad 2026. W razie wątpliwości zapytaj '
         'księgowego.',
    app=dict(
        h2='Wycena podpisana na miejscu',
        p='Z Fixbill ta sama wycena jest gotowa w dwie minuty w telefonie, razem z tym, czego wzór nie zrobi:',
        bullets=['klient podpisuje wycenę na Twoim ekranie (Pro)',
                 'zdjęcia z budowy dołączone do wyceny (Pro)',
                 'link do płatności PayPal lub Stripe z kodem QR na dokumencie',
                 'powiadomienie o terminie płatności i uprzejme przypomnienie jednym dotknięciem'],
        note='Za darmo do 5 dokumentów miesięcznie. Dane zostają w telefonie.'),
)

EN = dict(
    id='en-estimate-template', lang='en', html_lang='en', path='estimate-template/',
    phrase='estimate template for contractors',
    title='Free Estimate Template for Contractors: Fill In Online, Save as PDF | Fixbill',
    desc='Free contractor estimate template you can fill in online: line items, labor and materials, sales tax, terms '
         'and a client signature line. Save as PDF or print. Nothing is uploaded.',
    h1='Free estimate template for contractors',
    lede='Fill in the estimate in your browser, check the preview and save it as a PDF or print it. Your details stay '
         'on your device: nothing is uploaded.',
    jump='Fill in the estimate', crumb='Fixbill',
    card='Estimate template for contractors', card_text='Contractor estimate with line items, tax and a signature '
                                                        'line. Fill in online, save as PDF.',
    gen=dict(
        kind='estimate', locale='en-US', currency='USD', currencies=['USD', 'CAD'], decComma=False,
        refFromNumber=False, dates=['issue', 'valid'], pay=['terms'],
        sign=['Contractor signature and date', 'Accepted by client: signature and date'],
        made='Created with Fixbill · deriverge.com/fixbill',
        doc=dict(title='Estimate', no='No.', seller='Contractor', buyer='Client', desc='Description', qty='Qty',
                 unit='Unit', price='Unit price', priceNet='Unit price', amount='Amount', amountNet='Amount',
                 net='Subtotal', tax='Sales tax', total='Total'),
        ui=dict(items='Line items', add='Add a line', remove='Remove line', desc='Description', qty='Qty',
                unit='Unit', price='Unit price', print='Print or save as PDF', reset='Start over',
                resetAsk='Clear what you typed and bring back the example?', preview='Estimate preview',
                privacy='Your details stay in your browser (kept for your next visit on this device). To get a PDF, '
                        'choose “Save as PDF” in the print dialog.',
                noscript='The generator needs JavaScript. What to put on an estimate is listed below.'),
        groups=[
            ('Your business', [
                ('s_name', 'Business name', 'text', 'Smith Remodeling LLC', '', None),
                ('s_addr', 'Address', 'area', 'Street\nCity, State ZIP', '', None),
                ('s_ids', 'License number (if required)', 'text', 'License #123456', '', None),
                ('s_contact', 'Phone or e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Client', [
                ('b_name', 'Client name', 'text', 'Client name', '', None),
                ('b_addr', 'Client address', 'area', 'Street\nCity, State ZIP', '', None),
                ('site', 'Job address (if different)', 'area', 'Job address', '', None),
            ]),
            ('Estimate', [
                ('number', 'Estimate number', 'text', 'EST-1001', 'EST-1001', None),
                ('issue', 'Date', 'date', '', '', 0),
                ('valid', 'Valid until', 'date', '', '', 30),
                ('start', 'Estimated start and duration', 'text', 'Start within 2 weeks, about 4 working days', '',
                 None),
                ('cur', 'Currency', 'sel', '', 'USD', [('USD', 'US dollar (USD)'), ('CAD', 'Canadian dollar (CAD)')]),
            ]),
            'items',
            ('Tax', [
                ('tax', 'Sales tax', 'tax', '', '', None),
                ('taxrate', 'Tax rate in %', 'text', '8.25', '', None),
            ]),
            ('Terms', [
                ('terms', 'Payment terms', 'text', '', '30% deposit to schedule, balance due on completion.', None),
                ('notes', 'Scope, exclusions and changes', 'area', '',
                 'Price based on the scope above. Permits and hidden damage are not included. Any change to the scope '
                 'will be agreed in writing before the work is done.', None),
            ]),
        ],
        tax=[('none', 'No sales tax', '', ''), ('custom', 'Add sales tax', '', '')],
        items=[['Remove existing wall tile and haul away', '120', 'sq ft', '2.50'],
               ['Install wall tile, bathroom', '120', 'sq ft', '12'],
               ['Tile adhesive and grout', '1', 'lot', '96.50'], ['Plumbing labor', '4', 'h', '85']],
    ),
    body='''
<h2>What to put on a contractor estimate</h2>
<ul>
<li>your business name, address and phone or e-mail, and your contractor license number if your state requires it on estimates and contracts,</li>
<li>the client's name and the job address,</li>
<li>an estimate number, the date and how long the price is valid,</li>
<li>the scope of work as line items with quantity, unit and unit price, with labor and materials shown separately,</li>
<li>the subtotal, sales tax if it applies, and the total,</li>
<li>the payment schedule: deposit, progress payments and final payment,</li>
<li>exclusions and assumptions, for example permits, disposal or hidden damage,</li>
<li>a signature line so the client can accept the estimate.</li>
</ul>

<h2>Estimate, quote or bid?</h2>
<p>An estimate is your best calculation of what the job will cost, and the final price can change if the job changes. A quote or fixed bid is a firm price for a defined scope. Write on the document which one it is, and say how you will handle changes, for example with a written change order the client signs before extra work starts.</p>

<h2>Sales tax, deposits and cancellation</h2>
<p>Whether you charge sales tax on labor, on materials or on both depends on your state and sometimes on the type of job. Check with your state's revenue department or your accountant.</p>
<p>Some states limit the deposit a home improvement contractor can take. California, for example, caps the down payment on home improvement contracts at $1,000 or 10% of the contract price, whichever is less. The FTC Cooling-Off Rule can also give customers three days to cancel some sales made at their home. Check which rules apply where you work.</p>

<h2>Tips to win more jobs</h2>
<ul>
<li>Send the estimate the same day as the site visit.</li>
<li>Add photos of the current state so the scope is clear.</li>
<li>Offer options, for example standard and premium materials, so the client chooses between your prices rather than between contractors.</li>
<li>Make it easy to say yes: a signature on the spot beats a printout on the fridge.</li>
</ul>
''',
    fine='This template is general information, not legal or tax advice. Last checked November 2026. Rules differ by '
         'state; when in doubt, ask your accountant or your state licensing board.',
    app=dict(
        h2='Estimate on site, signed before you leave',
        p='With Fixbill the same estimate takes two minutes on your phone, plus what a template cannot do:',
        bullets=['your client signs the estimate on your screen, then it becomes an invoice with one tap (Pro)',
                 'a scan-to-pay QR code for your own PayPal or Stripe payment link',
                 'bank payments matched from your statement (CAMT.053, MT940, CSV) (Pro)',
                 'an alert when an invoice is overdue and a polite reminder with one tap'],
        note='Free for 5 documents a month. Your data stays on your phone.'),
)

PAGES = [EN, GB, CS, DE, FR, ES, IT, PL]
