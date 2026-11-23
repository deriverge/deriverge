// Němčina (de-DE v App Store, de-DE v Google Play). Platí i pro Rakousko a Švýcarsko, vlastní locale nemají.
const LINKS = `Nutzungsbedingungen: https://www.deriverge.com/tapkasa/terms.html
Datenschutzerklärung: https://www.deriverge.com/tapkasa/privacy.html`;
export default {
  stores: { as: 'den App Store', gp: 'Google Play' },
  as: {
    locale: 'de-DE',
    name: 'Tapkasa: Kasse für den Stand',
    subtitle: 'Weihnachtsmarkt, Verein, Pfand',
    keywords: 'festkasse,vereinsfest,marktstand,glühwein,basar,flohmarkt,rückgeld,kassa,punsch,kassen,app,einfache',
  },
  play: {
    locale: 'de-DE',
    title: 'Tapkasa: Kasse für Marktstände',
    shortXmas: 'Kasse für Weihnachtsmarkt und Vereinsfest: Pfand, Bestellnummern, ohne Internet.',
    shortYear: 'Kasse für Stand, Vereinsfest und Basar: Pfand, Bestellnummern, ohne Internet.',
  },
  promoXmas: 'Weihnachtsmarkt, Glühweinstand, Vereinsfest: Menü eintippen und kassieren, ohne Konto, ohne Netz. Tassenpfand mit einem Tipp, das zweite Handy zeigt die Bestellungen.',
  promoYear: 'Markt, Vereinsfest oder Basar: Menü eintippen und kassieren, ohne Konto und ohne Netz. Pfand mit einem Tipp, das zweite Handy zeigt die Bestellungen mit Nummer.',
  wn108: `• Pfand: Tassen- oder Becherpfand als Artikel, die Rückgabe mit einem Tipp. Die Übersicht zeigt eingenommenes und ausgezahltes Pfand getrennt.
• Limit ohne Überraschung: Die Gratisversion weist rechtzeitig auf das Tageslimit hin.
• Kein Netz am Stand? Den offenen Bon schließen Sie trotzdem ab und erhalten einmalig eine Reserve von 10 Zahlungen.`,
  wn109: `Fehlerbehebungen und Feinschliff für die Marktsaison.

Neu seit 1.0.8:
• Pfand: Tassen- oder Becherpfand als Artikel, die Rückgabe mit einem Tipp.
• Die Gratisversion weist rechtzeitig auf das Tageslimit hin.
• Kein Netz am Stand? Den offenen Bon schließen Sie trotzdem ab und erhalten einmalig eine Reserve von 10 Zahlungen.`,
  desc: (store) => `Die Kasse für Stand, Weihnachtsmarkt, Vereinsfest und Basar. Menü eintippen und in zwei Minuten kassieren: ohne Registrierung, ohne Konto, ohne Internet.

Tapkasa rechnet und erfasst Ihre Verkäufe, wickelt aber keine Zahlungen ab. Deshalb wird nichts eingefroren, nichts geprüft und es fallen keine Transaktionsgebühren an. Bargeld kommt in Ihre Geldkassette, Karten laufen über Ihr eigenes Terminal. Eine zertifizierte Kasse mit TSE ersetzt Tapkasa nicht.

Ein zweites Handy zeigt die Bestellungen mit Nummer und liest sie vor. Tassen- und Becherpfand buchen Sie mit einem Tipp. Kostenlos sind 10 Zahlungen pro Tag, für den ganzen Markt testen Sie Tapkasa Pro 14 Tage gratis.

VERKAUF IN DREI TIPPS
• Jeder Artikel ist eine Farbkarte. Das Team erkennt sie schneller, als es den Namen lesen kann.
• Antippen legt den Artikel auf den Bon, gedrückt halten nimmt ein Stück wieder herunter.
• „+ Anderer Betrag“ für alles, was nicht auf der Karte steht.
• Falsch gespeichert? Ein Tipp macht den letzten Bon rückgängig.

BAR UND KARTE
• Bei Barzahlung tippen Sie ein, was der Kunde gibt, und Tapkasa zeigt das Rückgeld.
• Bei Kartenzahlung kassieren Sie über Ihr eigenes Terminal und bestätigen nur den Betrag.

PFAND
• Das Pfand für Glühweintasse oder Becher ist eine Karte wie jede andere, die Pfandrückgabe eine Karte mit negativem Preis.
• Die Rückgabe wird vom Bon abgezogen. Ein Bon nur mit Rückgaben zählt nicht zum Tageslimit und erscheint nicht bei den Bestellungen.
• In der Übersicht stehen eingenommenes und ausgezahltes Pfand getrennt.

BESTELLUNGEN UND AUSGABE
• Jeder bezahlte Bon wird zur Bestellung mit Nummer.
• Ein zweites Handy oder Tablet wird zur Ausgabe: Bestellungen erscheinen dort von selbst, Sie haken Artikel ab und „Ausgegeben“ schließt die Bestellung.
• Die Ausgabe kann neue Bestellungen vorlesen.
• Zwei iPhones oder zwei Android-Handys (ab Android 13) koppeln sich auch ohne Internet. iPhone und Android zusammen brauchen dafür Internet.

ÜBERSICHT UND ABSCHLUSS
• Umsatz gesamt, bar und Karte, verkaufte Stücke je Artikel.
• Umsatzbericht als PDF für jeden Zeitraum, mit Ihren Angaben und auf Wunsch mit Umsatzsteuer-Aufstellung.
• Mehrere Events nebeneinander, Abschluss mit Archiv.
• 9 Sprachen und 33 Währungen.

IHRE DATEN GEHÖREN IHNEN
• Alles bleibt auf dem Gerät. Keine Konten, keine Analytik, keine Werbung.
• Die Datensicherung speichern Sie kostenlos als Datei und stellen daraus die Kasse wieder her, auch auf einem neuen Handy.
• Fällt das Netz aus, verkaufen Sie weiter.

GRATIS UND PRO
Gratis: die komplette Kasse auf einem Gerät, 10 bezahlte Bons pro Tag. Vor dem Limit weist die App rechtzeitig darauf hin. Haben Sie gerade kein Netz, schließen Sie den offenen Bon trotzdem ab und erhalten einmalig eine Reserve von 10 Zahlungen.
Tapkasa Pro (Abo): unbegrenzt kassieren und ein zweites Gerät koppeln. Pro Stand genügt ein Abo, die Ausgabe verbindet sich kostenlos. Neue Abonnenten testen 14 Tage gratis. Abrechnung über ${store}, jederzeit in den Kontoeinstellungen kündbar.

WAS TAPKASA NICHT IST
• Tapkasa wickelt keine Zahlungen ab und ist kein Kartenterminal.
• Tapkasa ist keine zertifizierte Registrierkasse (keine TSE, keine RKSV-Kasse). Nutzen Sie sie dort, wo es die Vorschriften erlauben: Vereinsfeste, Schul- und Wohltätigkeitsfeste, interne Aufzeichnungen.
• Keine Lagerverwaltung und keine Buchhaltung.

${LINKS}`,
};
