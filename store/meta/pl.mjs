// Polština (pl v App Store, pl-PL v Google Play). Bez tykání: neosobní tvary.
const LINKS = `Warunki korzystania: https://www.deriverge.com/tapkasa/terms.html
Polityka prywatności: https://www.deriverge.com/tapkasa/privacy.html`;
export default {
  stores: { as: 'App Store', gp: 'Google Play' },
  as: {
    locale: 'pl',
    name: 'Tapkasa: kasa na stoisko',
    subtitle: 'Jarmark świąteczny, kiermasz',
    keywords: 'mobilna,stragan,targ,festyn,sprzedaż,zamówienia,kolejka,reszta,kaucja,kubek,grzaniec,utarg,offline',
  },
  play: {
    locale: 'pl-PL',
    title: 'Tapkasa: kasa na stoisko',
    shortXmas: 'Kasa na jarmark świąteczny i kiermasz: kaucje, numery zamówień, bez internetu.',
    shortYear: 'Kasa na stoisko, kiermasz i festyn: kaucje, numery zamówień, bez internetu.',
  },
  promoXmas: 'Jarmark świąteczny, kiermasz czy grzaniec? Wystarczy wpisać menu i sprzedawać bez rejestracji i internetu. Kaucja jednym stuknięciem, numery zamówień na drugim telefonie.',
  promoYear: 'Targ, kiermasz albo festyn? Wystarczy wpisać menu i sprzedawać bez rejestracji i internetu. Kaucja jednym stuknięciem, numery zamówień na drugim telefonie.',
  wn108: `• Kaucje: kaucja za kubek lub kufel jako pozycja, zwrot jednym stuknięciem. Utarg pokazuje osobno kaucje pobrane i zwrócone.
• Limit bez niespodzianek: darmowa wersja z wyprzedzeniem uprzedza o dziennym limicie.
• Brak zasięgu na stoisku? Otwarty rachunek i tak można dokończyć, a jednorazowo dostaje się rezerwę 10 płatności.`,
  wn109: `Poprawki i dopracowanie przed sezonem jarmarków.

Nowe od wersji 1.0.8:
• Kaucje: kaucja za kubek lub kufel jako pozycja, zwrot jednym stuknięciem.
• Darmowa wersja z wyprzedzeniem uprzedza o dziennym limicie.
• Brak zasięgu na stoisku? Otwarty rachunek i tak można dokończyć, a jednorazowo dostaje się rezerwę 10 płatności.`,
  desc: (store) => `Kasa na stoisko, jarmark świąteczny, kiermasz, festyn i imprezę stowarzyszenia. Wystarczy wpisać menu i po dwóch minutach można sprzedawać: bez rejestracji, bez konta i bez internetu.

Tapkasa liczy i zapisuje sprzedaż, ale nie obsługuje płatności. Dlatego niczego nie blokuje, niczego nie weryfikuje i nie pobiera prowizji od płatności. Gotówka trafia do kasetki, a karta przechodzi przez własny terminal sprzedawcy.

Drugi telefon pokazuje kolejkę zamówień z numerami i odczytuje je na głos. Kaucję za kubek lub kufel dodaje się jednym stuknięciem. Za darmo 10 płatności dziennie, a na cały jarmark Tapkasa Pro można wypróbować za darmo przez 14 dni.

SPRZEDAŻ W TRZY STUKNIĘCIA
• Każda pozycja to kolorowa karta. Obsługa rozpoznaje ją szybciej, niż zdąży przeczytać nazwę.
• Stuknięcie dodaje sztukę do rachunku, przytrzymanie karty zdejmuje jedną sztukę.
• „+ Inna kwota” załatwia wszystko spoza menu.
• Pomyłka? Jedno stuknięcie cofa ostatni rachunek.

GOTÓWKA I KARTA
• Przy gotówce wpisuje się kwotę otrzymaną od klienta, a Tapkasa pokazuje resztę.
• Przy karcie płatność przyjmuje własny terminal, a w kasie wystarczy potwierdzić kwotę.

KAUCJE
• Kaucja za kubek na grzańca lub za kufel to karta jak każda inna, a zwrot kaucji to karta z ujemną ceną.
• Zwrot odejmuje się od rachunku. Rachunek z samymi zwrotami nie liczy się do dziennego limitu i nie trafia do kolejki.
• W utargu widać osobno kaucje pobrane i zwrócone klientom.

KOLEJKA ZAMÓWIEŃ I WYDAWKA
• Opłacony rachunek trafia do kolejki jako zamówienie z numerem.
• Drugi telefon lub tablet przełącza się w rolę Wydawka: zamówienia pojawiają się na nim same, pozycje się odhacza, a „Wydano” zamyka zamówienie.
• Wydawka może odczytywać nowe zamówienia na głos.
• Dwa iPhone’y albo dwa telefony z Androidem (13 lub nowszym) łączą się także bez internetu. iPhone z Androidem potrzebują do połączenia internetu.

UTARG I ZAMKNIĘCIE
• Utarg razem, gotówka i karta, sprzedane sztuki według pozycji.
• Podsumowanie sprzedaży w PDF za dowolny okres, z danymi sprzedawcy i w razie potrzeby z rozbiciem VAT.
• Kilka imprez obok siebie, zamknięcie imprezy z archiwum.
• 9 języków i 33 waluty.

DANE ZOSTAJĄ U SPRZEDAWCY
• Wszystko zostaje na urządzeniu. Bez kont, bez analityki, bez reklam.
• Kopię zapasową zapisuje się za darmo do pliku i w każdej chwili można z niej odtworzyć kasę, także na nowym telefonie.
• Brak zasięgu nie zatrzymuje sprzedaży.

ZA DARMO I PRO
Za darmo: pełna kasa na jednym urządzeniu, 10 opłaconych rachunków dziennie. Aplikacja z wyprzedzeniem uprzedza o zbliżającym się limicie. Gdy akurat nie ma zasięgu, otwarty rachunek i tak można dokończyć, a jednorazowo dostaje się rezerwę 10 płatności.
Tapkasa Pro (subskrypcja): sprzedaż bez limitu i połączenie z drugim urządzeniem. Na stoisko wystarczy jedna subskrypcja, wydawka łączy się za darmo. Nowi subskrybenci mają 14 dni próbnych za darmo. Rozliczenie przez ${store}, subskrypcję można anulować w każdej chwili w ustawieniach konta.

CZYM TAPKASA NIE JEST
• Nie obsługuje płatności i nie jest terminalem płatniczym.
• Nie jest kasą fiskalną. Można jej używać tam, gdzie pozwalają na to przepisy: stowarzyszenia, festyny szkolne i charytatywne, ewidencja wewnętrzna.
• Nie prowadzi magazynu ani księgowości.

${LINKS}`,
};
