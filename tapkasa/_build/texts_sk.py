# Slovak texts of the Tapkasa landing pages. Facts follow tapkasa/README.md and the app texts (version 1.0.8).
# No prices (they come from the stores), no fiscal promises (Tapkasa is not an eKasa client), no long dashes.

T = dict(
    html_lang='sk', hreflang='sk', og_locale='sk_SK', name='Slovenčina', currency='EUR',
    gp_badge='badge-googleplay-en.png', as_alt='Stiahnuť v App Store', gp_alt='Stiahnuť na Google Play',
    brand_sub='Pokladňa do vrecka', menu='Jazyk',
    try_btn='Vyskúšať v prehliadači',
    qr_alt='QR kód na stiahnutie aplikácie Tapkasa',
    qr_text='Namierte fotoaparát telefónu na kód a stiahnite si Tapkasu.',
    note='Zadarmo 10 zaplatených účtov denne. Bez registrácie.',
    sticky='Pokladňa do vrecka',
    ld_desc='Pokladňa do mobilu pre stánky, trhy, jarmoky a školské či spolkové akcie. Počíta výdavok, radí '
            'objednávky do poradia, eviduje vratné zálohy a funguje bez internetu. Dáta zostávajú v zariadení.',
    offer='Zadarmo 10 zaplatených účtov denne. Tapkasa Pro je predplatné v aplikácii (mesačné alebo ročné).',
    h_how='Ako to funguje',
    how=[
        ('Naťukajte si menu', 'Každá položka má názov, cenu a farbu. Zaberie to pár minút doma, alebo začnite '
                              's ukážkovým menu.'),
        ('Ťukajte na karty', 'Ťuknutie pridá kus, podržanie ho odoberie. Dole stále vidíte, koľko má zákazník '
                             'zaplatiť.'),
        ('Hotovosť alebo karta', 'Pri hotovosti Tapkasa vypočíta výdavok. Kartu prijmete na vlastnom termináli a '
                                 'v Tapkase platbu len označíte.'),
    ],
    h_feat='Čo Tapkasa vie',
    feats=[
        ('Výdavok bez počítania', 'Ťuknete na bankovku, ktorú ste dostali, a vidíte, koľko vrátiť.'),
        ('Poradie objednávok s číslami', 'Zaplatený účet dostane číslo a čaká v poradí, kým ho neoznačíte ako '
                                         'vydaný.'),
        ('Kasa a výdaj na dvoch telefónoch', 'Druhé zariadenie ukazuje objednávky a vie ich čítať nahlas. Prepojenie '
                                             'je súčasťou Tapkasa Pro.'),
        ('Funguje bez internetu', 'Všetko beží v telefóne. Dva iPhony alebo dva telefóny s Androidom sa spoja aj bez '
                                  'signálu.'),
        ('Vratné zálohy', 'Záloha na hrnček alebo pohár a jej vrátenie ako samostatné položky, v prehľade osobitne.'),
        ('Dáta zostávajú u vás', 'Žiadny účet ani cloud. Zálohu dát si uložíte do súboru, kam chcete.'),
    ],
    h_shots='Ako Tapkasa vyzerá',
    shot_alts=['Predajná obrazovka Tapkasy: farebné karty položiek s cenami a suma na zaplatenie',
               'Poradie objednávok s číslami na druhom telefóne',
               'Súhrn tržieb s rozpisom DPH'],
    h_not='Čo Tapkasa nie je',
    nots=[
        'Nie je to pokladnica eKasa klient ani iná certifikovaná pokladnica a nič neposiela finančnej správe. Súhrn '
        'tržieb z Tapkasy nie je pokladničný ani daňový doklad.',
        'Nespracúva platby kartou. Kartu prijímate na vlastnom termináli, Tapkasa si predaj len zapíše.',
        'Netlačí bločky ani lístky.',
    ],
    not_p='Hodí sa tam, kde povinnosť evidovať tržby v eKase nemáte, alebo ako pomôcka popri nej. Aké povinnosti '
          'platia pre vás, si overte u účtovníčky alebo na finančnej správe.',
    h_price='Koľko Tapkasa stojí',
    price=[
        'Zadarmo: celé menu, prehľady, vratné zálohy aj záloha dát na jednom zariadení a 10 zaplatených účtov denne. '
        'Účet, ktorým len vraciate zálohu, sa do limitu nepočíta.',
        'Tapkasa Pro: neobmedzený počet účtov a prepojenie kasy s výdajom. Je to predplatné na mesiac alebo na rok '
        'cez App Store alebo Google Play a noví predplatitelia majú 14 dní na skúšku zadarmo. Cenu vo svojej mene '
        'uvidíte v aplikácii pred nákupom, zrušiť ho môžete kedykoľvek v nastaveniach obchodu.',
        'Stánku stačí jedno predplatné: druhý telefón sa k zariadeniu s Tapkasa Pro pripojí zadarmo.',
    ],
    h_faq='Časté otázky',
    faq=[
        ('Je Tapkasa zadarmo?',
         'Áno, do 10 zaplatených účtov denne na jednom zariadení. Neobmedzené účtovanie a prepojenie dvoch zariadení '
         'odomyká predplatné Tapkasa Pro, ktoré si noví predplatitelia môžu 14 dní vyskúšať zadarmo.'),
        ('Je to registračná pokladnica alebo eKasa?',
         'Nie. Tapkasa predaje počíta a zaznamenáva, ale nie je certifikovaná pokladnica, neposiela dáta do systému '
         'eKasa a nevystavuje pokladničné ani daňové doklady.'),
        ('Kde sú moje dáta?',
         'Len vo vašom zariadení. Tapkasa nemá účty ani cloud. Zálohu si uložíte do súboru a na novom telefóne ju '
         'načítate.'),
        ('V akých jazykoch a menách funguje?',
         'V deviatich jazykoch (slovenčina, čeština, angličtina, nemčina, poľština, francúzština, taliančina, '
         'španielčina a portugalčina) a v 33 menách vrátane eura a českej koruny.'),
    ],
    cta_h='Vyskúšajte Tapkasu ešte pred akciou',
    h_more='Ďalšie návody',
    f_support='Podpora', f_privacy='Súkromie', f_terms='Podmienky', f_app='Otvoriť Tapkasu v prehliadači',
    f_langs='Jazyky', f_operator='Prevádzkovateľ',
    pages=dict(
        stall=dict(
            path='sk/', card='Pokladňa na stánok',
            title='Pokladňa na stánok do mobilu: predaj aj bez internetu | Tapkasa',
            desc='Pokladňa na stánok v telefóne: farebné karty položiek, výdavok vypočíta aplikácia, poradie '
                 'objednávok na druhom telefóne a vratné zálohy. Funguje bez internetu, 10 účtov denne zadarmo.',
            h1='Pokladňa na stánok, ktorá sa zmestí do vrecka',
            eyebrow='Pre iPhone, Android aj prehliadač',
            lede='Naťukáte menu, ťukáte na farebné karty a Tapkasa počíta: koľko zaplatiť, koľko vrátiť a koľko ste '
                 'za deň utŕžili. Bez registrácie, bez terminálu a bez internetu.',
            sections=[
                ('Ako to vyzerá na stánku',
                 '<p>Zákazník si vypýta dve varené vína a lokšu. Ťuknete dvakrát na víno, raz na lokšu a dole svieti '
                 'suma. Podá vám dvadsaťeurovku, ťuknete na 20 a Tapkasa ukáže, koľko vrátiť. Trvá to pár sekúnd a '
                 'nikto nepočíta z hlavy, ani brigádnik, ktorý stojí pri kase prvý raz.</p>'),
                ('Dva telefóny: kasa a výdaj',
                 '<p>Keď sa tvorí rad, jeden telefón účtuje a druhý ukazuje objednávky s číslami. Výdaj odškrtáva '
                 'hotové kusy a vie si objednávky nechať čítať nahlas, takže sa nemusíte pozerať na displej '
                 's rukami od cesta. Dva iPhony alebo dva telefóny s Androidom sa spoja napriamo aj bez internetu, '
                 'iPhone s Androidom potrebuje pripojenie.</p>'),
                ('Vratná záloha na hrnček alebo pohár',
                 '<p>Tlačidlom „+ Pridať zálohu“ si do menu pridáte položky Záloha a Vrátenie zálohy. Vrátený '
                 'hrnček sa z účtu odpočíta a v prehľade vidíte zálohy vybraté a vrátené osobitne, takže sa '
                 'nemiešajú s tržbou.</p>'),
                ('Večer viete, koľko ste utŕžili',
                 '<p>Prehľad ukáže tržbu spolu, hotovosť a karty osobitne a predané kusy po položkách. Súhrn tržieb '
                 'si uložíte ako PDF, napríklad pre účtovníčku.</p>'),
            ],
            faq=[
                ('Musím byť pripojený na internet?',
                 'Nie. Predaj, prehľady aj záloha dát bežia priamo v telefóne. Internet potrebujete len na '
                 'stiahnutie aplikácie, na nákup Tapkasa Pro a na spojenie iPhonu s Androidom.'),
                ('Zvládne pokladňu brigádnik alebo dobrovoľník?',
                 'Áno. Predaj je ťuknutie na farebnú kartu a voľba Hotovosť alebo Karta. Omylom pridaný kus sa '
                 'odoberie podržaním karty.'),
            ],
        ),
        xmas=dict(
            path='sk/pokladna-na-vianocne-trhy/', card='Pokladňa na vianočné trhy',
            title='Pokladňa na vianočné trhy: záloha na hrnček aj bez signálu | Tapkasa',
            desc='Pokladňa do mobilu na vianočné trhy a adventné jarmoky: varené víno na jedno ťuknutie, vratná '
                 'záloha na hrnček, výdavok vypočíta aplikácia. Funguje bez signálu, 10 účtov denne zadarmo.',
            h1='Pokladňa na vianočné trhy: varené víno, punč a záloha na hrnček',
            eyebrow='Vianočné trhy a adventné jarmoky',
            lede='Na námestí je plno, signál padá a pri stánku stojí rad. Tapkasa beží v telefóne aj bez internetu, '
                 'vypočíta výdavok a postráži zálohy na hrnčeky. Pripravenú ju máte za pár minút.',
            sections=[
                ('Záloha na hrnček bez zmätku',
                 '<p>V Menu ťuknite na „+ Pridať zálohu“ a zadajte sumu, napríklad 2 €. Tapkasa vytvorí dve položky: '
                 'Zálohu a Vrátenie zálohy. K vínu ťuknete zálohu, pri vrátení hrnčeka ťuknete vrátenie a suma sa '
                 'z účtu odpočíta. Keď zákazník len vracia hrnček, Tapkasa ukáže, koľko mu dať späť.</p>'
                 '<p>V prehľade sú zálohy vybraté a vrátené osobitne. Večer tak viete, koľko hrnčekov je ešte vonku '
                 'a aká je skutočná tržba.</p>'),
                ('Keď na námestí vypadne signál',
                 '<p>Predaj, vydávanie aj prehľad tržieb bežia priamo v telefóne. Tapkasa sa nikam neprihlasuje a nič '
                 'neoveruje, takže vás uprostred špičky nezastaví preťažená sieť ani minuté dáta.</p>'),
                ('Rad na varené víno a langoše',
                 '<p>Jeden telefón účtuje, druhý pri výdaji ukazuje objednávky s číslami a číta ich nahlas. Zákazník '
                 'dostane číslo a vy nemusíte cez stánok kričať, kto čo chcel. Dva iPhony alebo dva telefóny '
                 's Androidom sa spoja napriamo, bez Wi-Fi aj bez dát.</p>'),
                ('Tipy do mrazu',
                 '<ul><li>Ceny zaokrúhlite tak, aby sa dobre vydávalo: 2, 3, 5 €.</li>'
                 '<li>Menu si pripravte doma v teple a najpredávanejšie položky dajte hore.</li>'
                 '<li>Vezmite si powerbanku. Displej pri predaji nezhasína a v mraze batéria ubúda rýchlejšie.</li>'
                 '<li>Pred prvou sobotou si uložte zálohu dát do súboru.</li></ul>'),
            ],
            faq=[
                ('Počíta sa vrátenie zálohy do denného limitu zadarmo?',
                 'Nie. Účet, ktorým len vraciate zálohu, sa do limitu 10 zaplatených účtov denne nepočíta.'),
                ('Stačí na vianočné trhy verzia zadarmo?',
                 'Na malý stánok s pár predajmi denne áno. Na rušný trh sa hodí Tapkasa Pro: noví predplatitelia ho '
                 'majú prvých 14 dní zadarmo, čo pokryje dva adventné víkendy. Na blížiaci sa limit Tapkasa upozorní '
                 'vopred.'),
            ],
        ),
        club=dict(
            path='sk/pokladna-na-skolsku-akciu/', card='Pokladňa na školskú a spolkovú akciu',
            title='Pokladňa na školskú akciu a pre združenie do mobilu | Tapkasa',
            desc='Pokladňa do mobilu pre školy, občianske združenia, hasičov a farnosti: predaj na ťuknutie, výdavok '
                 'vypočíta aplikácia, večer presná tržba a súhrn v PDF pre pokladníka. Bez registrácie.',
            h1='Pokladňa na školskú akciu a pre občianske združenie',
            eyebrow='Plesy, dni detí, hasičské zábavy, školské jarmoky',
            lede='Pri kase sa striedajú dobrovoľníci a večer chce pokladník vedieť, koľko sa vybralo. Tapkasa '
                 'v telefóne stráži ceny, počíta výdavok a tržbu spočíta sama. Bez registrácie a bez zaúčania.',
            sections=[
                ('Kasu zvládne každý dobrovoľník',
                 '<p>Položky sú veľké farebné karty, takže obsluha nehľadá v zozname ani nepočíta z hlavy. Ťukne, čo '
                 'si zákazník vypýtal, zvolí Hotovosť alebo Karta a pri hotovosti vidí, koľko vrátiť. Striedanie pri '
                 'kase znamená len odovzdať telefón.</p>'),
                ('Večer presná tržba pre pokladníka',
                 '<p>Prehľad ukáže tržbu spolu, hotovosť a karty osobitne a koľko sa čoho predalo. Súhrn tržieb '
                 'pošlete ako PDF pokladníkovi alebo výboru. Po akcii zvolíte Uzavrieť akciu, tržba sa uloží do '
                 'archívu a nabudúce začínate od nuly.</p>'),
                ('Bez účtu, bez overovania, bez poplatkov',
                 '<p>Tapkasa nechce registráciu, IČO ani bankový účet a z tržby si nič neberie. Peniaze idú do vašej '
                 'pokladničky. Dáta zostávajú v telefóne, ktorý pri kase používate.</p>'),
                ('Väčšia akcia: bar a kuchyňa osobitne',
                 '<p>Na plese alebo hasičskej zábave môže jeden telefón účtovať pri bare a druhý ukazovať objednávky '
                 'v kuchyni. Stačí na to jedno predplatné Tapkasa Pro, ktoré majú noví predplatitelia 14 dní na '
                 'skúšku zadarmo.</p>'),
            ],
            faq=[
                ('Stačí na školský jarmok verzia zadarmo?',
                 'Na menšiu akciu áno: zadarmo je 10 zaplatených účtov denne. Keď čakáte viac zákazníkov, zapnite '
                 'si vopred Tapkasa Pro, noví predplatitelia majú 14 dní na skúšku zadarmo.'),
                ('Potrebuje združenie registráciu alebo overenie?',
                 'Nie. Tapkasu len stiahnete a otvoríte. Nezakladá sa žiadny účet a nič sa neoveruje.'),
            ],
        ),
    ),
)
