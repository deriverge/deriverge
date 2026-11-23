# Polish texts of the Tapkasa landing pages (impersonal style, nobody is addressed with "ty").
# Facts follow tapkasa/README.md and the app texts (version 1.0.8). No prices, Tapkasa is not a fiscal cash register.
# No long dashes.

T = dict(
    html_lang='pl', hreflang='pl', og_locale='pl_PL', name='Polski', currency='PLN',
    gp_badge='badge-googleplay-en.png', as_alt='Pobierz z App Store', gp_alt='Pobierz z Google Play',
    brand_sub='Kasa w kieszeni', menu='Język',
    try_btn='Tapkasa w przeglądarce',
    qr_alt='Kod QR do pobrania aplikacji Tapkasa',
    qr_text='Wystarczy skierować aparat telefonu na kod, aby pobrać Tapkasę.',
    note='Za darmo 10 opłaconych rachunków dziennie. Bez rejestracji.',
    sticky='Kasa w kieszeni',
    ld_desc='Prosta kasa w telefonie na stoisko, jarmark, kiermasz i festyn szkolny. Liczy resztę, ustawia '
            'zamówienia w kolejce, obsługuje kaucje zwrotne i działa bez internetu. Dane zostają w urządzeniu. To '
            'nie jest kasa fiskalna.',
    offer='Za darmo 10 opłaconych rachunków dziennie. Tapkasa Pro to subskrypcja w aplikacji (miesięczna lub roczna).',
    h_how='Jak to działa',
    how=[
        ('Wpisanie menu', 'Każda pozycja ma nazwę, cenę i kolor. Zajmuje to kilka minut w domu, można też zacząć od '
                          'przykładowego menu.'),
        ('Stukanie w kafelki', 'Dotknięcie dodaje sztukę, przytrzymanie ją odejmuje. Na dole cały czas widać kwotę '
                               'do zapłaty.'),
        ('Gotówka albo karta', 'Przy gotówce Tapkasa liczy resztę. Kartę przyjmuje się na własnym terminalu, a '
                               'w Tapkasie płatność tylko się oznacza.'),
    ],
    h_feat='Co potrafi Tapkasa',
    feats=[
        ('Reszta bez liczenia w pamięci', 'Wystarczy dotknąć banknotu, który podał klient, i widać, ile wydać.'),
        ('Kolejka zamówień z numerami', 'Opłacony rachunek dostaje numer i czeka w kolejce, aż zostanie oznaczony '
                                        'jako wydany.'),
        ('Kasa i wydawka na dwóch telefonach', 'Drugie urządzenie pokazuje zamówienia i może czytać je na głos. '
                                               'Łączenie urządzeń jest częścią Tapkasa Pro.'),
        ('Działa bez internetu', 'Wszystko działa w telefonie. Dwa iPhone’y albo dwa telefony z Androidem łączą się '
                                 'nawet bez zasięgu.'),
        ('Kaucje zwrotne', 'Kaucja za kubek i jej zwrot jako osobne pozycje, w podsumowaniu pokazane oddzielnie od '
                           'utargu.'),
        ('Dane zostają na miejscu', 'Bez konta i bez chmury. Kopię zapasową zapisuje się do pliku w dowolnym '
                                    'miejscu.'),
    ],
    h_shots='Jak wygląda Tapkasa',
    shot_alts=['Ekran sprzedaży Tapkasy: kolorowe kafelki pozycji z cenami i kwota do zapłaty',
               'Kolejka zamówień z numerami na drugim telefonie',
               'Podsumowanie sprzedaży z rozbiciem na stawki VAT'],
    h_not='Czym Tapkasa nie jest',
    nots=[
        'To nie jest kasa fiskalna ani kasa wirtualna z homologacją. Tapkasa niczego nie wysyła do urzędów, a '
        'podsumowanie sprzedaży nie jest paragonem fiskalnym ani fakturą.',
        'Nie obsługuje płatności kartą. Kartę przyjmuje się na własnym terminalu, Tapkasa tylko zapisuje sprzedaż.',
        'Nie drukuje paragonów ani bloczków.',
    ],
    not_p='Sprawdza się tam, gdzie nie ma obowiązku ewidencji na kasie fiskalnej, albo jako pomoc obok niej. Jakie '
          'obowiązki dotyczą konkretnej sprzedaży, warto potwierdzić u księgowej lub w urzędzie skarbowym.',
    h_price='Ile kosztuje Tapkasa',
    price=[
        'Za darmo: całe menu, podsumowania, kaucje i kopia zapasowa na jednym urządzeniu oraz 10 opłaconych '
        'rachunków dziennie. Rachunek, którym tylko zwraca się kaucję, nie wlicza się do limitu.',
        'Tapkasa Pro: nieograniczona liczba rachunków i łączenie kasy z wydawką. To subskrypcja miesięczna lub '
        'roczna przez App Store albo Google Play, nowi subskrybenci mają 14 dni próby za darmo. Cenę w swojej '
        'walucie widać w aplikacji przed zakupem, a subskrypcję można anulować w każdej chwili w ustawieniach '
        'sklepu.',
        'Na jedno stoisko wystarczy jedna subskrypcja: drugi telefon łączy się z urządzeniem z Tapkasa Pro za '
        'darmo.',
    ],
    h_faq='Częste pytania',
    faq=[
        ('Czy Tapkasa jest darmowa?',
         'Tak, do 10 opłaconych rachunków dziennie na jednym urządzeniu. Nieograniczoną sprzedaż i łączenie dwóch '
         'urządzeń odblokowuje subskrypcja Tapkasa Pro, którą nowi subskrybenci mogą testować 14 dni za darmo.'),
        ('Czy to kasa fiskalna?',
         'Nie. Tapkasa liczy i zapisuje sprzedaż, ale nie jest kasą fiskalną, nie wysyła danych do urzędów i nie '
         'wystawia paragonów fiskalnych ani faktur.'),
        ('Gdzie są dane?',
         'Tylko w urządzeniu. Tapkasa nie ma kont ani chmury. Kopię zapasową można zapisać do pliku i wczytać na '
         'nowym telefonie.'),
        ('W jakich językach i walutach działa?',
         'W dziewięciu językach (polski, angielski, niemiecki, czeski, słowacki, francuski, włoski, hiszpański '
         'i portugalski) oraz w 33 walutach, w tym w złotych i euro.'),
    ],
    cta_h='Warto wypróbować Tapkasę jeszcze przed imprezą',
    h_more='Więcej poradników',
    f_support='Pomoc', f_privacy='Prywatność', f_terms='Regulamin', f_app='Tapkasa w przeglądarce',
    f_langs='Języki', f_operator='Operator',
    pages=dict(
        stall=dict(
            path='pl/', card='Kasa na stoisko',
            title='Kasa na stoisko w telefonie: sprzedaż bez internetu | Tapkasa',
            desc='Prosta kasa na stoisko w telefonie: kolorowe kafelki z cenami, aplikacja liczy resztę, kolejka '
                 'zamówień na drugim telefonie i kaucje za kubki. Działa bez internetu. To nie jest kasa fiskalna.',
            h1='Kasa na stoisko, która mieści się w kieszeni',
            eyebrow='Na iPhone’a, Androida i do przeglądarki',
            lede='Menu wpisuje się raz, potem wystarczy stukać w kolorowe kafelki, a Tapkasa liczy: ile do zapłaty, '
                 'ile reszty i jaki był utarg z całego dnia. Bez rejestracji, bez dodatkowego sprzętu i bez '
                 'internetu.',
            sections=[
                ('Jak to wygląda na stoisku',
                 '<p>Klient prosi o dwa grzańce i oscypka. Dwa dotknięcia grzańca, jedno oscypka i na dole ekranu '
                 'jest kwota. Klient podaje stówę, wystarczy dotknąć 100 i Tapkasa pokazuje resztę. Trwa to kilka '
                 'sekund i nikt nie liczy w pamięci, nawet osoba, która stoi za ladą pierwszy raz.</p>'),
                ('Dwa telefony: kasa i wydawka',
                 '<p>Kiedy robi się kolejka, jeden telefon przyjmuje pieniądze, a drugi pokazuje zamówienia '
                 'z numerami. Na wydawce odhacza się gotowe pozycje, a nowe zamówienia aplikacja może czytać na '
                 'głos, więc nie trzeba patrzeć na ekran z zajętymi rękami. Dwa iPhone’y albo dwa telefony '
                 'z Androidem łączą się bezpośrednio, bez internetu. iPhone z Androidem potrzebuje połączenia '
                 'z siecią.</p>'),
                ('Kaucja za kubek',
                 '<p>Przycisk „+ Dodaj kaucję” dodaje do menu dwie pozycje: Kaucja i Zwrot kaucji. Zwrócony kubek '
                 'odejmuje się od rachunku, a w podsumowaniu kaucje pobrane i zwrócone są pokazane osobno, więc '
                 'nie mieszają się z utargiem.</p>'),
                ('Wieczorem wiadomo, ile wpadło do kasy',
                 '<p>Podsumowanie pokazuje utarg łącznie, osobno gotówkę i karty oraz liczbę sprzedanych sztuk '
                 'każdej pozycji. Zestawienie sprzedaży można zapisać jako PDF, na przykład dla księgowej.</p>'),
            ],
            faq=[
                ('Czy potrzebny jest internet?',
                 'Nie. Sprzedaż, podsumowania i kopia zapasowa działają w telefonie. Internet jest potrzebny tylko '
                 'do pobrania aplikacji, zakupu Tapkasa Pro i połączenia iPhone’a z Androidem.'),
                ('Czy poradzi sobie pomocnik albo wolontariusz?',
                 'Tak. Sprzedaż to dotknięcie kolorowego kafelka i wybór: Gotówka albo Karta. Pozycję dodaną przez '
                 'pomyłkę usuwa się przytrzymaniem kafelka.'),
            ],
        ),
        xmas=dict(
            path='pl/jarmark-bozonarodzeniowy/', card='Kasa na jarmark bożonarodzeniowy',
            title='Kasa na jarmark bożonarodzeniowy: kaucja za kubek | Tapkasa',
            desc='Kasa w telefonie na jarmark bożonarodzeniowy i kiermasz świąteczny: grzaniec jednym dotknięciem, '
                 'kaucja za kubek, aplikacja liczy resztę. Działa bez zasięgu. To nie jest kasa fiskalna.',
            h1='Kasa na jarmark bożonarodzeniowy: grzaniec, pierniki i kaucja za kubek',
            eyebrow='Jarmarki bożonarodzeniowe i kiermasze świąteczne',
            lede='Na rynku tłum, sieć ledwo działa, a przed stoiskiem stoi kolejka. Tapkasa działa w telefonie bez '
                 'internetu, liczy resztę i pilnuje kaucji za kubki. Przygotowanie zajmuje kilka minut.',
            sections=[
                ('Kaucja za kubek bez bałaganu',
                 '<p>W Menu wystarczy dotknąć „+ Dodaj kaucję” i wpisać kwotę, na przykład 10 zł. Tapkasa tworzy dwie '
                 'pozycje: Kaucja i Zwrot kaucji. Do grzańca dodaje się kaucję, przy oddaniu kubka dotyka się zwrotu '
                 'i kwota odejmuje się od rachunku. Jeśli klient tylko oddaje kubek, Tapkasa pokazuje, ile mu '
                 'wypłacić.</p>'
                 '<p>W podsumowaniu kaucje pobrane i zwrócone są osobno. Wieczorem wiadomo, ile kubków jest jeszcze '
                 'u klientów i jaki był prawdziwy utarg.</p>'),
                ('Kiedy na rynku pada zasięg',
                 '<p>Sprzedaż, wydawanie reszty i podsumowanie działają w samym telefonie. Tapkasa nigdzie się nie '
                 'loguje i niczego nie sprawdza w sieci, więc przeciążona sieć albo wyczerpany pakiet danych nie '
                 'zatrzymają sprzedaży w środku szczytu.</p>'),
                ('Kolejka po grzańca i zapiekanki',
                 '<p>Jeden telefon kasuje, drugi na wydawce pokazuje zamówienia z numerami i czyta je na głos. '
                 'Klient dostaje numer i nikt nie musi krzyczeć przez całe stoisko, kto co zamówił. Dwa iPhone’y '
                 'albo dwa telefony z Androidem łączą się bezpośrednio, bez Wi-Fi i bez danych komórkowych.</p>'),
                ('Wskazówki na mróz',
                 '<ul><li>Ceny warto zaokrąglić tak, żeby łatwo wydawać resztę: 10, 15, 20 zł.</li>'
                 '<li>Menu najlepiej przygotować w domu, w cieple, a najlepiej sprzedające się pozycje ustawić na '
                 'górze.</li>'
                 '<li>Przyda się powerbank. Ekran podczas sprzedaży nie gaśnie, a na mrozie bateria rozładowuje się '
                 'szybciej.</li>'
                 '<li>Przed pierwszą sobotą dobrze zapisać kopię zapasową do pliku.</li></ul>'),
            ],
            faq=[
                ('Czy zwrot kaucji wlicza się do dziennego limitu wersji darmowej?',
                 'Nie. Rachunek, którym tylko zwraca się kaucję, nie wlicza się do limitu 10 opłaconych rachunków '
                 'dziennie.'),
                ('Czy na jarmark wystarczy wersja darmowa?',
                 'Na małe stoisko z kilkoma sprzedażami dziennie tak. Przy dużym ruchu przyda się Tapkasa Pro: nowi '
                 'subskrybenci mają pierwsze 14 dni za darmo, co pokrywa dwa adwentowe weekendy. O zbliżającym się '
                 'limicie Tapkasa uprzedza wcześniej.'),
            ],
        ),
        club=dict(
            path='pl/festyn-szkolny/', card='Kasa na festyn szkolny i kiermasz',
            title='Kasa na festyn szkolny i kiermasz: obsłuży ją wolontariusz | Tapkasa',
            desc='Kasa w telefonie na festyn szkolny, kiermasz i imprezę stowarzyszenia: wolontariusz stuka '
                 'w kafelki, aplikacja liczy resztę, skarbnik dostaje podsumowanie w PDF. Bez rejestracji.',
            h1='Kasa na festyn szkolny, kiermasz i imprezę stowarzyszenia',
            eyebrow='Festyny, kiermasze, bale, imprezy OSP i rad rodziców',
            lede='Przy kasie zmieniają się wolontariusze, a wieczorem skarbnik chce wiedzieć, ile zebrano. Tapkasa '
                 'w telefonie pamięta ceny, liczy resztę i sama sumuje utarg. Bez rejestracji i bez szkolenia.',
            sections=[
                ('Kasę obsłuży każdy wolontariusz',
                 '<p>Pozycje to duże kolorowe kafelki, więc nikt nie szuka na liście ani nie liczy w pamięci. '
                 'Wystarczy dotknąć tego, o co prosi klient, wybrać Gotówka albo Karta i przy gotówce widać, ile '
                 'wydać reszty. Zmiana przy kasie to po prostu przekazanie telefonu.</p>'),
                ('Wieczorem dokładne podsumowanie dla skarbnika',
                 '<p>Podsumowanie pokazuje utarg łącznie, osobno gotówkę i karty oraz ile czego sprzedano. '
                 'Zestawienie sprzedaży można wysłać jako PDF skarbnikowi albo zarządowi. Po imprezie wybiera się '
                 '„Zamknięcie imprezy”: utarg trafia do archiwum, a następnym razem zaczyna się od zera.</p>'),
                ('Bez konta, bez weryfikacji, bez prowizji',
                 '<p>Tapkasa nie wymaga rejestracji, numeru KRS ani konta bankowego i nie pobiera prowizji od '
                 'utargu. Pieniądze trafiają do własnej kasetki. Dane zostają w telefonie używanym przy kasie.</p>'),
                ('Większa impreza: bufet i kuchnia osobno',
                 '<p>Na balu albo festynie jeden telefon może kasować przy bufecie, a drugi pokazywać zamówienia '
                 'w kuchni. Wystarczy do tego jedna subskrypcja Tapkasa Pro, którą nowi subskrybenci testują 14 dni '
                 'za darmo.</p>'),
            ],
            faq=[
                ('Czy na szkolny kiermasz wystarczy wersja darmowa?',
                 'Na małą imprezę tak: 10 opłaconych rachunków dziennie jest za darmo. Przy większej liczbie gości '
                 'warto wcześniej włączyć Tapkasa Pro, nowi subskrybenci mają 14 dni próby za darmo.'),
                ('Czy stowarzyszenie musi się rejestrować?',
                 'Nie. Tapkasę wystarczy pobrać i otworzyć. Nie zakłada się konta i nic nie jest weryfikowane.'),
            ],
        ),
    ),
)
