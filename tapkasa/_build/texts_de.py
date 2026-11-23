# German texts of the Tapkasa landing pages. Facts follow tapkasa/README.md and the app texts (version 1.0.8).
# No prices (they come from the stores). Tapkasa has no TSE: every page says so plainly (audit/problemy_tapkasa.md,
# section 8.1). No long dashes.

T = dict(
    html_lang='de', hreflang='de', og_locale='de_DE', name='Deutsch', currency='EUR',
    gp_badge='badge-googleplay-en.png', as_alt='Laden im App Store', gp_alt='Jetzt bei Google Play',
    brand_sub='Kassieren mit dem Handy', menu='Sprache',
    try_btn='Im Browser ausprobieren',
    qr_alt='QR-Code zum Herunterladen der Tapkasa-App',
    qr_text='Handykamera auf den Code richten und Tapkasa laden.',
    note='Kostenlos für 10 bezahlte Bons pro Tag. Ohne Anmeldung.',
    sticky='Kassieren mit dem Handy',
    ld_desc='Kassen-App für Marktstand, Weihnachtsmarkt, Vereinsfest und Schulfest. Rechnet das Rückgeld aus, '
            'nummeriert Bestellungen, verwaltet Pfand und läuft ohne Internet. Die Daten bleiben auf dem Gerät. '
            'Keine TSE.',
    offer='Kostenlos für 10 bezahlte Bons pro Tag. Tapkasa Pro ist ein Abo in der App (monatlich oder jährlich).',
    h_how='So funktioniert es',
    how=[
        ('Angebot eintippen', 'Jeder Artikel bekommt Namen, Preis und Farbe. Das dauert zu Hause ein paar Minuten, '
                              'oder Sie starten mit dem Beispielmenü.'),
        ('Karten antippen', 'Tippen fügt ein Stück hinzu, langes Drücken nimmt eines weg. Unten steht immer, was der '
                            'Kunde zahlt.'),
        ('Bar oder Karte', 'Bei Barzahlung rechnet Tapkasa das Rückgeld aus. Kartenzahlungen nehmen Sie am eigenen '
                           'Terminal an und markieren sie in Tapkasa nur.'),
    ],
    h_feat='Was Tapkasa kann',
    feats=[
        ('Rückgeld ohne Kopfrechnen', 'Sie tippen auf den Schein, den Sie bekommen haben, und sehen das Rückgeld.'),
        ('Bestellungen mit Nummer', 'Jeder bezahlte Bon bekommt eine Nummer und wartet in der Liste, bis Sie ihn als '
                                    'ausgegeben markieren.'),
        ('Kasse und Ausgabe auf zwei Handys', 'Das zweite Gerät zeigt die Bestellungen und kann sie vorlesen. Das '
                                              'Koppeln gehört zu Tapkasa Pro.'),
        ('Läuft ohne Netz', 'Alles läuft auf dem Handy. Zwei iPhones oder zwei Android-Handys verbinden sich auch '
                            'ohne Internet.'),
        ('Pfand', 'Pfand für Tasse oder Becher und die Pfandrückgabe als eigene Artikel, in der Übersicht getrennt '
                  'vom Umsatz.'),
        ('Ihre Daten bleiben bei Ihnen', 'Kein Konto, keine Cloud. Eine Sicherung speichern Sie als Datei, wo Sie '
                                         'möchten.'),
    ],
    h_shots='So sieht Tapkasa aus',
    shot_alts=['Verkaufsbildschirm von Tapkasa: farbige Artikelkarten mit Preisen und der zu zahlende Betrag',
               'Bestellliste mit Nummern auf dem zweiten Handy',
               'Umsatzübersicht mit Steueraufstellung'],
    h_not='Was Tapkasa nicht ist',
    nots=[
        'Tapkasa hat keine technische Sicherheitseinrichtung (TSE) und ist kein zertifiziertes Kassensystem im Sinne '
        'der Kassensicherungsverordnung (Deutschland) oder der Registrierkassensicherheitsverordnung (Österreich). '
        'Die Umsatzübersicht ist kein Kassenbeleg und keine Rechnung.',
        'Tapkasa wickelt keine Kartenzahlungen ab. Karten nehmen Sie am eigenen Terminal an, Tapkasa notiert nur den '
        'Verkauf.',
        'Tapkasa druckt keine Bons und keine Wertmarken.',
    ],
    not_p='Ob Sie Tapkasa bei Ihrer Veranstaltung einsetzen können, etwa als Rechenhilfe neben einer offenen '
          'Ladenkasse, klären Sie bitte mit Ihrer Steuerberatung oder dem Finanzamt. Diese Seite ist keine '
          'Steuerberatung.',
    h_price='Was Tapkasa kostet',
    price=[
        'Kostenlos: das ganze Angebot, Übersichten, Pfand und Datensicherung auf einem Gerät, dazu 10 bezahlte Bons '
        'pro Tag. Ein Bon, mit dem Sie nur Pfand zurückgeben, zählt nicht zum Limit.',
        'Tapkasa Pro: unbegrenzt viele Bons und das Koppeln von Kasse und Ausgabe. Es ist ein Monats- oder Jahresabo '
        'über den App Store oder Google Play, neue Abonnenten testen 14 Tage kostenlos. Den Preis in Ihrer Währung '
        'sehen Sie in der App vor dem Kauf, kündigen können Sie jederzeit in den Einstellungen des Stores.',
        'Für einen Stand reicht ein Abo: Das zweite Handy verbindet sich kostenlos mit dem Gerät, das Tapkasa Pro '
        'hat.',
    ],
    h_faq='Häufige Fragen',
    faq=[
        ('Ist Tapkasa kostenlos?',
         'Ja, bis 10 bezahlte Bons pro Tag auf einem Gerät. Unbegrenztes Kassieren und das Koppeln zweier Geräte '
         'schaltet das Abo Tapkasa Pro frei, das neue Abonnenten 14 Tage kostenlos testen können.'),
        ('Ist Tapkasa eine TSE-Kasse oder Registrierkasse?',
         'Nein. Tapkasa zählt und notiert Ihre Verkäufe, hat aber keine TSE, ist kein zertifiziertes Kassensystem '
         'und stellt keine Belege oder Rechnungen aus.'),
        ('Wo liegen meine Daten?',
         'Nur auf Ihrem Gerät. Tapkasa hat keine Konten und keine Cloud. Eine Sicherung speichern Sie als Datei und '
         'laden sie auf einem neuen Handy wieder.'),
        ('Welche Sprachen und Währungen gibt es?',
         'Neun Sprachen (Deutsch, Englisch, Französisch, Italienisch, Spanisch, Portugiesisch, Polnisch, Tschechisch '
         'und Slowakisch) und 33 Währungen, darunter Euro und Schweizer Franken.'),
    ],
    cta_h='Probieren Sie Tapkasa vor dem Fest aus',
    h_more='Weitere Anleitungen',
    f_support='Support', f_privacy='Datenschutz', f_terms='Nutzungsbedingungen', f_app='Tapkasa im Browser öffnen',
    f_langs='Sprachen', f_operator='Betreiber',
    pages=dict(
        stall=dict(
            path='de/', card='Kassen-App für den Marktstand',
            title='Kassen-App für den Marktstand: kassieren ohne Netz | Tapkasa',
            desc='Kassieren am Marktstand mit dem Handy: farbige Artikelkarten, Rückgeld wird berechnet, '
                 'Bestellungen mit Nummer auf dem zweiten Handy, Pfand. Läuft ohne Internet, ohne Anmeldung. Keine '
                 'TSE.',
            h1='Kassieren am Marktstand, mit dem Handy in der Tasche',
            eyebrow='Für iPhone, Android und Browser',
            lede='Sie tippen Ihr Angebot ein, tippen auf farbige Karten und Tapkasa rechnet: was zu zahlen ist, wie '
                 'viel Rückgeld es gibt und was heute eingenommen wurde. Ohne Anmeldung, ohne Zusatzgerät und ohne '
                 'Internet.',
            sections=[
                ('So läuft es am Stand',
                 '<p>Eine Kundin bestellt zwei Glühwein und eine Bratwurst. Sie tippen zweimal auf Glühwein, einmal '
                 'auf Bratwurst, unten steht der Betrag. Sie bekommen einen Zwanziger, tippen auf 20 und Tapkasa '
                 'zeigt das Rückgeld. Das dauert Sekunden, und niemand rechnet im Kopf, auch nicht die Aushilfe in '
                 'ihrer ersten Schicht.</p>'),
                ('Zwei Handys: Kasse und Ausgabe',
                 '<p>Wenn sich eine Schlange bildet, kassiert ein Handy und das andere zeigt die Bestellungen mit '
                 'Nummer. An der Ausgabe haken Sie ab, was fertig ist, und lassen sich neue Bestellungen vorlesen, '
                 'damit Sie mit vollen Händen nicht aufs Display schauen müssen. Zwei iPhones oder zwei '
                 'Android-Handys verbinden sich direkt und ohne Internet, iPhone und Android zusammen brauchen eine '
                 'Verbindung.</p>'),
                ('Pfand auf Tasse oder Becher',
                 '<p>Mit „+ Pfand hinzufügen“ legen Sie zwei Artikel an: Pfand und Pfandrückgabe. Die zurückgegebene '
                 'Tasse wird vom Bon abgezogen, und in der Übersicht stehen eingenommenes und zurückgegebenes Pfand '
                 'getrennt vom Umsatz.</p>'),
                ('Abends wissen Sie, was in der Kasse sein muss',
                 '<p>Die Übersicht zeigt den Gesamtumsatz, bar und Karte getrennt, und die verkauften Stückzahlen je '
                 'Artikel. Die Umsatzübersicht speichern Sie als PDF, zum Beispiel für die Buchhaltung.</p>'),
            ],
            faq=[
                ('Brauche ich eine Internetverbindung?',
                 'Nein. Verkauf, Übersichten und Datensicherung laufen direkt auf dem Handy. Internet brauchen Sie '
                 'nur zum Laden der App, für den Kauf von Tapkasa Pro und um ein iPhone mit einem Android-Gerät zu '
                 'koppeln.'),
                ('Kommt eine Aushilfe damit zurecht?',
                 'Ja. Ein Verkauf ist ein Tipp auf eine farbige Karte und die Wahl Bar oder Karte. Ein versehentlich '
                 'getippter Artikel verschwindet durch langes Drücken.'),
            ],
        ),
        xmas=dict(
            path='de/weihnachtsmarkt/', card='Kassieren auf dem Weihnachtsmarkt',
            title='Kasse für den Weihnachtsmarkt: Pfand und Rückgeld per App | Tapkasa',
            desc='Kassieren auf dem Weihnachtsmarkt mit dem Handy: Glühwein mit einem Tipp, Tassenpfand, Rückgeld '
                 'wird berechnet. Läuft ohne Netz und ohne Anmeldung, 10 Bons pro Tag kostenlos. Keine TSE-Kasse.',
            h1='Kassieren auf dem Weihnachtsmarkt: Glühwein, Punsch und Tassenpfand',
            eyebrow='Weihnachtsmarkt, Adventsmarkt, Adventsbasar',
            lede='Der Platz ist voll, das Netz bricht zusammen und vor der Bude steht eine Schlange. Tapkasa läuft '
                 'auf dem Handy auch ohne Internet, rechnet das Rückgeld aus und behält das Tassenpfand im Blick. '
                 'Eingerichtet ist es in ein paar Minuten.',
            sections=[
                ('Tassenpfand ohne Durcheinander',
                 '<p>Im Menü tippen Sie auf „+ Pfand hinzufügen“ und geben den Betrag ein, zum Beispiel 3 €. Tapkasa '
                 'legt zwei Artikel an: Pfand und Pfandrückgabe. Zum Glühwein tippen Sie das Pfand dazu, bei der '
                 'Rückgabe der Tasse tippen Sie die Pfandrückgabe und der Betrag wird abgezogen. Bringt jemand nur '
                 'die Tasse zurück, zeigt Tapkasa, was Sie auszahlen.</p>'
                 '<p>In der Übersicht stehen eingenommenes und zurückgegebenes Pfand getrennt. So wissen Sie abends, '
                 'wie viele Tassen noch unterwegs sind und wie hoch der eigentliche Umsatz war.</p>'),
                ('Wenn auf dem Markt das Netz weg ist',
                 '<p>Verkauf, Rückgeld und Umsatzübersicht laufen direkt auf dem Handy. Tapkasa meldet sich nirgends '
                 'an und prüft nichts online. Ein überlastetes Netz oder aufgebrauchtes Datenvolumen hält Sie mitten '
                 'im Andrang also nicht auf.</p>'),
                ('Schlange vor dem Glühweinstand',
                 '<p>Ein Handy kassiert, das zweite zeigt an der Ausgabe die Bestellungen mit Nummer und liest sie '
                 'vor. Der Gast bekommt eine Nummer, und niemand ruft quer durch die Bude, wer was bestellt hat. '
                 'Zwei iPhones oder zwei Android-Handys verbinden sich direkt, ohne WLAN und ohne mobile '
                 'Daten.</p>'),
                ('Tipps für kalte Tage',
                 '<ul><li>Runden Sie die Preise so, dass sich leicht herausgeben lässt: 3, 4, 5 €.</li>'
                 '<li>Legen Sie das Angebot zu Hause im Warmen an und setzen Sie die Renner nach oben.</li>'
                 '<li>Nehmen Sie eine Powerbank mit. Das Display bleibt beim Verkauf an, und in der Kälte hält der '
                 'Akku kürzer.</li>'
                 '<li>Speichern Sie vor dem ersten Markttag eine Datensicherung als Datei.</li></ul>'),
            ],
            faq=[
                ('Zählt die Pfandrückgabe zum kostenlosen Tageslimit?',
                 'Nein. Ein Bon, mit dem Sie nur Pfand zurückgeben, zählt nicht zu den 10 bezahlten Bons pro Tag.'),
                ('Reicht die kostenlose Version für den Weihnachtsmarkt?',
                 'Für einen kleinen Stand mit wenigen Verkäufen am Tag ja. Bei viel Betrieb lohnt sich Tapkasa Pro: '
                 'Neue Abonnenten testen 14 Tage kostenlos, das deckt zwei Adventswochenenden ab. Tapkasa weist '
                 'rechtzeitig darauf hin, wenn das Limit näher rückt.'),
            ],
        ),
        club=dict(
            path='de/vereinsfest/', card='Kassieren beim Vereinsfest und Schulfest',
            title='Kasse fürs Vereinsfest: App für Helfer, ohne Anmeldung | Tapkasa',
            desc='Kassieren beim Vereinsfest, Schulfest oder Basar mit dem Handy: Helfer tippen die Artikel an, die '
                 'App rechnet das Rückgeld aus, der Kassenwart bekommt die Übersicht als PDF. Keine TSE-Kasse.',
            h1='Kassieren beim Vereinsfest und Schulfest',
            eyebrow='Vereinsfest, Schulfest, Basar, Feuerwehrfest',
            lede='An der Kasse wechseln sich Helfer ab, und am Abend will der Kassenwart wissen, was eingenommen '
                 'wurde. Tapkasa merkt sich auf dem Handy die Preise, rechnet das Rückgeld aus und zählt die '
                 'Einnahmen zusammen. Ohne Anmeldung und ohne Einweisung.',
            sections=[
                ('Jeder Helfer kommt damit zurecht',
                 '<p>Die Artikel sind große farbige Karten. Niemand sucht in einer Liste oder rechnet im Kopf. Man '
                 'tippt an, was bestellt wurde, wählt Bar oder Karte und sieht bei Barzahlung das Rückgeld. Beim '
                 'Schichtwechsel wird einfach das Handy weitergegeben.</p>'),
                ('Abends eine genaue Übersicht für den Kassenwart',
                 '<p>Die Übersicht zeigt den Gesamtumsatz, bar und Karte getrennt, und was wie oft verkauft wurde. '
                 'Die Umsatzübersicht schicken Sie als PDF an den Kassenwart oder den Vorstand. Nach dem Fest '
                 'wählen Sie „Event abschließen“: Die Einnahmen wandern ins Archiv und beim nächsten Mal beginnen '
                 'Sie bei null.</p>'),
                ('Kein Konto, keine Prüfung, keine Gebühren',
                 '<p>Tapkasa verlangt keine Registrierung, keine Vereinsunterlagen und keine Bankverbindung und '
                 'behält nichts von den Einnahmen ein. Das Geld liegt in Ihrer Kasse. Die Daten bleiben auf dem '
                 'Handy, mit dem kassiert wird.</p>'),
                ('Größere Feste: Theke und Küche getrennt',
                 '<p>Beim Sommerfest oder Feuerwehrfest kann ein Handy an der Theke kassieren, während ein zweites '
                 'in der Küche die Bestellungen zeigt. Dafür genügt ein Abo Tapkasa Pro, das neue Abonnenten 14 Tage '
                 'kostenlos testen.</p>'),
            ],
            faq=[
                ('Reicht die kostenlose Version für ein Schulfest?',
                 'Für ein kleines Fest ja: 10 bezahlte Bons pro Tag sind kostenlos. Wenn Sie mehr Gäste erwarten, '
                 'starten Sie vorher Tapkasa Pro; neue Abonnenten testen 14 Tage kostenlos.'),
                ('Muss sich der Verein registrieren?',
                 'Nein. Sie laden Tapkasa und öffnen die App. Es wird kein Konto angelegt und nichts geprüft.'),
            ],
        ),
    ),
)
