# Platební terminály: jak Tapkasu do budoucna propojit

Úvaha k požadavku „napárovat s terminály, nebo třeba s ČSOB v telefonu".
Dnes Tapkasa platby jen zaznamenává (obsluha částku naťuká na terminál a
v aplikaci potvrdí). Cíl: aby po klepnutí na „Kartou" částka sama doletěla
do terminálu a potvrzení se samo vrátilo.

## Tři úrovně integrace (od nejsnazší)

**1. Předání částky do aplikace terminálu na tomtéž telefonu (app-to-app)**

Aplikace typu „telefon jako terminál" (softPOS): v Česku ČSOB SmartPOS,
GP tom od Global Payments, mezinárodně SumUp, Viva Terminal a další.
Část z nich umí přijmout částku odkazem nebo mezi-aplikačním voláním a
vrátit výsledek zpět. Tapkasa by po klepnutí na „Kartou" otevřela aplikaci
terminálu s předvyplněnou částkou a po zaplacení by se vrátila s potvrzením.

- Náročnost: malá (deep link + návratová adresa), bez certifikací.
- Podmínka: ověřit u konkrétního poskytovatele, zda app-to-app rozhraní
  nabízí a za jakých podmínek (u ČSOB SmartPOS a GP tom se ptát přímo,
  podmínky se mění; SumUp a Viva mají rozhraní dokumentovaná veřejně).
- V aplikaci na to už je místo: krok „Kartou" má jediný potvrzovací bod,
  stačí do něj zavěsit most `window.__kasaTerminal` po vzoru mostu pro
  nákupy (`__kasaBuy`).

**2. Platební SDK přímo v Tapkase (telefon prodejce = terminál)**

SumUp, Viva a Stripe (Tap to Pay) nabízejí SDK, které z iPhonu nebo
Androidu udělá bezkontaktní terminál přímo uvnitř naší aplikace. Zákazník
přiloží kartu k telefonu s Tapkasou, potvrzení přijde samo.

- Náročnost: střední. SDK řeší certifikace za nás, u Apple je navíc
  potřeba povolení Tap to Pay on iPhone.
- Peníze tečou přes poskytovatele SDK (má vlastní sazby), Tapkasa se jich
  nedotýká. Pozor: mění se odpovědi v App Review a privacy štítcích
  (přibývá platební SDK), texty v `review-notes.md` by se musely upravit.
- Obchodně nejzajímavější: „pokladna i terminál v jedné aplikaci".

**3. Propojení s bankovními terminály na pultě (ECR protokol)**

Klasické terminály (v ČR nejčastěji od Global Payments pro ČSOB a KB)
umějí režim „pokladna posílá částku po síti" (ECR/LAN). Vyžaduje smlouvu
s poskytovatelem terminálů a jejich protokol, obvykle v partnerském
programu.

- Náročnost: největší, ale cílí na zavedené provozy s vlastním terminálem.
- Dává smysl až podle poptávky od zákazníků.

## Doporučené pořadí

1. Po vydání 1.0 oslovit Global Payments (GP tom, terminály ČSOB/KB) a
   ČSOB SmartPOS s dotazem na app-to-app a partnerský program; mezitím
   nasadit úroveň 1 pro SumUp (celoevropsky rozšířené u stánkařů).
2. Podle ohlasů zvážit úroveň 2 (SumUp SDK nebo Stripe Tap to Pay) jako
   placenou funkci vedle Tapkasa Pro.
3. Úroveň 3 řešit až s konkrétním větším zákazníkem.

Technická příprava v aplikaci je společná pro všechny úrovně: jeden most
`window.__kasaTerminal(amount, currency, cb)` v kroku „Kartou", stejný
vzor jako u nákupů a párování. Do té doby se nic nemění.
