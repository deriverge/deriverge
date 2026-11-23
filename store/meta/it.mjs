// Italština (it v App Store, it-IT v Google Play).
const LINKS = `Termini di utilizzo: https://www.deriverge.com/tapkasa/terms.html
Informativa sulla privacy: https://www.deriverge.com/tapkasa/privacy.html`;
export default {
  stores: { as: 'App Store', gp: 'Google Play' },
  as: {
    locale: 'it',
    name: 'Tapkasa: cassa per bancarelle',
    subtitle: 'Mercatini di Natale e sagre',
    keywords: 'registratore,mercatino,sagra,festa,chiosco,ordini,resto,cauzione,bicchiere,vendite,incassi,fiera,bar',
  },
  play: {
    locale: 'it-IT',
    title: 'Tapkasa: cassa per bancarelle',
    shortXmas: 'Cassa per mercatini di Natale e sagre: cauzioni, ordini numerati, offline.',
    shortYear: 'Cassa per bancarelle, sagre e feste: cauzioni, ordini numerati, anche offline.',
  },
  promoXmas: 'Mercatino di Natale, sagra o vin brulé? Scrivete il menu e incassate senza registrazione e senza internet. Cauzione con un tocco, ordini numerati su un secondo telefono.',
  promoYear: 'Mercatino, sagra o festa della scuola? Scrivete il menu e incassate senza registrazione e senza internet. Cauzione con un tocco, ordini numerati su un secondo telefono.',
  wn108: `• Cauzioni: la cauzione per tazza o bicchiere è un articolo come gli altri e si restituisce con un tocco. Gli incassi mostrano separate le cauzioni incassate e restituite.
• Limite senza sorprese: la versione gratuita avvisa per tempo prima del limite giornaliero.
• Niente rete alla bancarella? Potete comunque chiudere il conto aperto e ricevete una sola volta una riserva di 10 pagamenti.`,
  wn109: `Correzioni e rifiniture per la stagione dei mercatini.

Novità dalla 1.0.8:
• Cauzioni: la cauzione per tazza o bicchiere è un articolo come gli altri e si restituisce con un tocco.
• La versione gratuita avvisa per tempo prima del limite giornaliero.
• Niente rete alla bancarella? Potete comunque chiudere il conto aperto e ricevete una sola volta una riserva di 10 pagamenti.`,
  desc: (store) => `La cassa per bancarelle, mercatini di Natale, sagre, chioschi e feste di associazioni. Scrivete il menu e in due minuti incassate: senza registrazione, senza account, senza internet.

Tapkasa calcola e registra le vendite, ma non elabora pagamenti. Per questo non blocca e non verifica nulla e non applica commissioni sui pagamenti. I contanti vanno nella vostra cassetta, la carta passa dal vostro POS.

Un secondo telefono mostra gli ordini numerati e li legge ad alta voce. La cauzione per tazze e bicchieri si segna con un tocco. Gratis: 10 pagamenti al giorno. Per un intero mercatino provate Tapkasa Pro gratis per 14 giorni.

UNA VENDITA IN TRE TOCCHI
• Ogni articolo è una scheda colorata. Lo staff la riconosce prima ancora di leggere il nome.
• Un tocco aggiunge l’articolo al conto, tenendo premuto se ne toglie uno.
• «+ Altro importo» per tutto ciò che non è a menu.
• Un errore? Un tocco annulla l’ultimo conto.

CONTANTI E CARTA
• In contanti digitate quanto vi dà il cliente e Tapkasa mostra il resto.
• Con la carta incassate sul vostro POS e confermate soltanto l’importo.

CAUZIONI
• La cauzione per la tazza del vin brulé o per il bicchiere è una scheda come le altre, il reso della cauzione è una scheda con prezzo negativo.
• Il reso viene sottratto dal conto. Un conto con soli resi non rientra nel limite giornaliero e non finisce nella coda degli ordini.
• Negli incassi vedete separate le cauzioni incassate e quelle restituite ai clienti.

ORDINI E BANCO
• Ogni conto pagato diventa un ordine numerato.
• Un secondo telefono o tablet passa al ruolo Banco: gli ordini compaiono da soli, spuntate gli articoli e «Servito» chiude l’ordine.
• Il banco può leggere i nuovi ordini ad alta voce.
• Due iPhone o due telefoni Android (Android 13 o successivo) si collegano anche senza internet. Un iPhone e un Android hanno bisogno di internet per collegarsi.

INCASSI E CHIUSURA
• Incasso totale, contanti e carta, pezzi venduti per articolo.
• Riepilogo vendite in PDF per qualsiasi periodo, con i vostri dati e, se serve, il riepilogo IVA.
• Più eventi in parallelo, chiusura con archivio.
• 9 lingue e 33 valute.

I VOSTRI DATI SONO VOSTRI
• Tutto resta sul dispositivo. Niente account, niente analytics, niente pubblicità.
• Il backup si salva gratis in un file e si ripristina quando volete, anche su un telefono nuovo.
• Se cade la rete, continuate a vendere.

GRATIS E PRO
Gratis: la cassa completa su un dispositivo, 10 conti pagati al giorno. L’app avvisa per tempo prima del limite. Se in quel momento non c’è rete, potete comunque chiudere il conto aperto e ricevete una sola volta una riserva di 10 pagamenti.
Tapkasa Pro (abbonamento): incassi illimitati e collegamento di un secondo dispositivo. Basta un abbonamento per bancarella, il banco si collega gratis. I nuovi abbonati hanno 14 giorni di prova gratuita. Addebito tramite ${store}, disdicibile in ogni momento dalle impostazioni dell’account.

COSA TAPKASA NON È
• Non elabora pagamenti e non è un POS per carte.
• Non è un registratore telematico. Usatela dove le norme lo consentono: associazioni, feste scolastiche e benefiche, registri interni.
• Non gestisce magazzino né contabilità.

${LINKS}`,
};
