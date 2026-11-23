# Czech texts of the Tapkasa landing pages. Facts follow tapkasa/README.md and the app texts (version 1.0.8).
# No prices (they come from the stores), no fiscal promises, no long dashes. `sections` bodies are trusted HTML.

T = dict(
    html_lang='cs', hreflang='cs', og_locale='cs_CZ', name='Čeština', currency='CZK',
    gp_badge='badge-googleplay-cs.png', as_alt='Stáhnout v App Store', gp_alt='Nyní na Google Play',
    brand_sub='Pokladna do kapsy', menu='Jazyk',
    try_btn='Vyzkoušet v prohlížeči',
    qr_alt='QR kód ke stažení aplikace Tapkasa',
    qr_text='Namiřte fotoaparát telefonu na kód a stáhněte si Tapkasu.',
    note='Zdarma 10 zaplacených účtů denně. Bez registrace.',
    sticky='Pokladna do kapsy',
    ld_desc='Pokladna do mobilu pro stánky, trhy, jarmarky a spolkové akce. Počítá vrácení, řadí objednávky do '
            'fronty, eviduje vratné zálohy a funguje bez internetu. Data zůstávají v zařízení.',
    offer='Zdarma 10 zaplacených účtů denně. Tapkasa Pro je předplatné v aplikaci (měsíční nebo roční).',
    h_how='Jak to funguje',
    how=[
        ('Naťukejte si menu', 'Každá položka má název, cenu a barvu. Zabere to pár minut doma, nebo začněte '
                              's ukázkovým menu.'),
        ('Ťukejte na karty', 'Ťuknutí přidá kus, podržení ho odebere. Dole pořád vidíte, kolik má zákazník zaplatit.'),
        ('Hotově, nebo kartou', 'U hotovosti Tapkasa spočítá vrácení. Kartu vezmete na vlastním terminálu a '
                                'v Tapkase platbu jen označíte.'),
    ],
    h_feat='Co Tapkasa umí',
    feats=[
        ('Vrácení bez počítání', 'Ťuknete na bankovku, kterou jste dostali, a vidíte, kolik vrátit.'),
        ('Fronta objednávek s čísly', 'Zaplacený účet dostane číslo a čeká ve frontě, dokud ho neoznačíte jako vydaný.'),
        ('Kasa a výdej na dvou telefonech', 'Druhé zařízení ukazuje objednávky a umí je číst nahlas. Propojení je '
                                            'součástí Tapkasa Pro.'),
        ('Funguje bez internetu', 'Všechno běží v telefonu. Dva iPhony nebo dva telefony s Androidem se spojí i bez '
                                  'signálu.'),
        ('Vratné zálohy', 'Záloha na hrnek nebo kelímek a její vrácení jako samostatné položky, v přehledu zvlášť.'),
        ('Data zůstávají u vás', 'Žádný účet ani cloud. Zálohu dat si uložíte do souboru, kam chcete.'),
    ],
    h_shots='Jak Tapkasa vypadá',
    shot_alts=['Prodejní obrazovka Tapkasy: barevné karty položek s cenami a částka k zaplacení',
               'Fronta objednávek s čísly na druhém telefonu',
               'Souhrn tržeb s rozpisem DPH'],
    h_not='Co Tapkasa není',
    nots=[
        'Není to fiskální ani certifikovaná pokladna a nic neposílá úřadům. Souhrn tržeb z Tapkasy není daňový '
        'doklad ani účtenka pro zákazníka.',
        'Nezpracovává platby kartou. Kartu berete na vlastním terminálu, Tapkasa si prodej jen zapíše.',
        'Netiskne účtenky ani lístky.',
    ],
    not_p='Na stánky, jarmarky a příležitostný prodej to obvykle stačí. Jaké povinnosti máte právě vy, si ověřte '
          'u účetní nebo na finančním úřadě.',
    h_price='Kolik Tapkasa stojí',
    price=[
        'Zdarma: celé menu, přehledy, vratné zálohy i záloha dat na jednom zařízení a 10 zaplacených účtů denně. '
        'Účet, kterým jen vracíte zálohu, se do limitu nepočítá.',
        'Tapkasa Pro: neomezený počet účtů a propojení kasy s výdejem. Je to předplatné na měsíc nebo na rok přes '
        'App Store nebo Google Play a noví předplatitelé mají 14 dní na zkoušku zdarma. Cenu ve své měně uvidíte '
        'v aplikaci před nákupem, zrušit ho můžete kdykoli v nastavení obchodu.',
        'Stánku stačí jedno předplatné: druhý telefon se k zařízení s Tapkasa Pro připojí zdarma.',
    ],
    h_faq='Časté otázky',
    faq=[
        ('Je Tapkasa zdarma?',
         'Ano, do 10 zaplacených účtů denně na jednom zařízení. Neomezené účtování a propojení dvou zařízení odemyká '
         'předplatné Tapkasa Pro, které si noví předplatitelé mohou 14 dní vyzkoušet zdarma.'),
        ('Je to registrační nebo fiskální pokladna?',
         'Ne. Tapkasa prodeje počítá a zaznamenává, ale není certifikovaná pokladna, neposílá data úřadům a '
         'nevystavuje daňové doklady.'),
        ('Kde jsou moje data?',
         'Jen ve vašem zařízení. Tapkasa nemá účty ani cloud. Zálohu si uložíte do souboru a na novém telefonu ji '
         'načtete.'),
        ('V jakých jazycích a měnách funguje?',
         'V devíti jazycích (čeština, slovenština, angličtina, němčina, polština, francouzština, italština, '
         'španělština a portugalština) a ve 33 měnách včetně korun a eur.'),
    ],
    cta_h='Vyzkoušejte Tapkasu ještě před akcí',
    h_more='Další návody',
    f_support='Podpora', f_privacy='Soukromí', f_terms='Podmínky', f_app='Otevřít Tapkasu v prohlížeči',
    f_langs='Jazyky', f_operator='Provozovatel',
    pages=dict(
        stall=dict(
            path='pokladna.html', card='Pokladna na stánek',
            title='Pokladna na stánek do mobilu: prodej i bez internetu | Tapkasa',
            desc='Pokladna na stánek v telefonu: barevné karty položek, vrácení spočítá aplikace, fronta objednávek '
                 'na druhém telefonu a vratné zálohy. Funguje bez internetu, 10 účtů denně zdarma.',
            h1='Pokladna na stánek, která se vejde do kapsy',
            eyebrow='Pro iPhone, Android i prohlížeč',
            lede='Naťukáte menu, ťukáte na barevné karty a Tapkasa počítá: kolik zaplatit, kolik vrátit a kolik jste '
                 'za den utržili. Bez registrace, bez terminálu a bez internetu.',
            sections=[
                ('Jak to vypadá na stánku',
                 '<p>Zákazník si řekne dva svařáky a trdelník. Ťuknete dvakrát na svařák, jednou na trdelník a dole '
                 'svítí částka. Dá vám pětistovku, ťuknete na 500 a Tapkasa ukáže, kolik vrátit. Trvá to pár vteřin '
                 'a nikdo nepočítá z hlavy, ani brigádník, který stojí u kasy poprvé.</p>'),
                ('Dva telefony: kasa a výdej',
                 '<p>Když se tvoří fronta, jeden telefon účtuje a druhý ukazuje objednávky s čísly. Výdej odškrtává '
                 'hotové kusy a umí si objednávky nechat číst nahlas, takže se nemusíte dívat na displej s rukama '
                 'od těsta. Dva iPhony nebo dva telefony s Androidem se spojí napřímo i bez internetu, iPhone '
                 's Androidem potřebuje připojení.</p>'),
                ('Vratná záloha na hrnek nebo kelímek',
                 '<p>Tlačítkem „+ Přidat zálohu“ si do menu přidáte položky Záloha a Vrácení zálohy. Vrácený hrnek '
                 'se z účtu odečte a v přehledu vidíte zálohy vybrané a vrácené zvlášť, takže se nepletou do '
                 'tržby.</p>'),
                ('Večer víte, kolik jste utržili',
                 '<p>Přehled ukáže tržbu celkem, hotovost a karty zvlášť a prodané kusy po položkách. Souhrn tržeb '
                 'si uložíte jako PDF, třeba pro účetní.</p>'),
            ],
            faq=[
                ('Musím být připojený k internetu?',
                 'Ne. Prodej, přehledy i záloha dat běží přímo v telefonu. Internet potřebujete jen ke stažení '
                 'aplikace, k nákupu Tapkasa Pro a ke spojení iPhonu s Androidem.'),
                ('Zvládne pokladnu brigádník nebo dobrovolník?',
                 'Ano. Prodej je ťuknutí na barevnou kartu a volba Hotově nebo Kartou. Omylem přidaný kus se odebere '
                 'podržením karty.'),
            ],
        ),
        xmas=dict(
            path='pokladna-na-vanocni-trh.html', card='Pokladna na vánoční trhy',
            title='Pokladna na vánoční trhy: záloha na hrnek i bez signálu | Tapkasa',
            desc='Pokladna do mobilu na vánoční trhy a adventní jarmarky: svařák na jedno ťuknutí, vratná záloha na '
                 'hrnek, vrácení spočítá aplikace. Funguje bez signálu, 10 účtů denně zdarma.',
            h1='Pokladna na vánoční trhy: svařák, punč a záloha na hrnek',
            eyebrow='Vánoční trhy a adventní jarmarky',
            lede='Na náměstí je plno, signál padá a u stánku stojí fronta. Tapkasa běží v telefonu i bez internetu, '
                 'spočítá vrácení a ohlídá zálohy na hrnky. Připravenou ji máte za pár minut.',
            sections=[
                ('Záloha na hrnek bez zmatku',
                 '<p>V Menu ťukněte na „+ Přidat zálohu“ a zadejte částku, třeba 50 Kč. Tapkasa vytvoří dvě položky: '
                 'Zálohu a Vrácení zálohy. Ke svařáku ťuknete zálohu, při vrácení hrnku ťuknete vrácení a částka se '
                 'z účtu odečte. Když zákazník jen vrací hrnek, Tapkasa ukáže, kolik mu dát zpátky.</p>'
                 '<p>V přehledu jsou zálohy vybrané a vrácené zvlášť. Večer tak víte, kolik hrnků je ještě venku '
                 'a kolik je skutečná tržba.</p>'),
                ('Když na náměstí spadne signál',
                 '<p>Prodej, vracení i přehled tržeb běží přímo v telefonu. Tapkasa se nikam nepřihlašuje a nic '
                 'neověřuje, takže vás uprostřed špičky nezastaví přetížená síť ani vyčerpaná data.</p>'),
                ('Fronta na svařák a langoše',
                 '<p>Jeden telefon účtuje, druhý u výdeje ukazuje objednávky s čísly a čte je nahlas. Zákazník '
                 'dostane číslo a vy nemusíte přes stánek křičet, kdo co chtěl. Dva iPhony nebo dva telefony '
                 's Androidem se spojí napřímo, bez Wi-Fi i bez dat.</p>'),
                ('Tipy do mrazu',
                 '<ul><li>Ceny zaokrouhlete tak, ať se dobře vrací: 50, 60, 80 Kč.</li>'
                 '<li>Menu nachystejte doma v teple a nejprodávanější položky dejte nahoru.</li>'
                 '<li>Vezměte powerbanku. Displej při prodeji nezhasíná a v mrazu baterie ubývá rychleji.</li>'
                 '<li>Před první sobotou si uložte zálohu dat do souboru.</li></ul>'),
            ],
            faq=[
                ('Počítá se vrácení zálohy do denního limitu zdarma?',
                 'Ne. Účet, kterým jen vracíte zálohu, se do limitu 10 zaplacených účtů denně nepočítá.'),
                ('Stačí na vánoční trh verze zdarma?',
                 'Na malý stánek s pár prodeji denně ano. Na rušný trh se hodí Tapkasa Pro: noví předplatitelé ho '
                 'mají prvních 14 dní zdarma, což pokryje dva adventní víkendy. Na blížící se limit Tapkasa '
                 'upozorní předem.'),
            ],
        ),
        club=dict(
            path='pokladna-pro-spolek.html', card='Pokladna pro spolek a školní akci',
            title='Pokladna pro spolek a školní akci: zvládne ji dobrovolník | Tapkasa',
            desc='Pokladna do mobilu pro spolky, školy, hasiče a farnosti: prodej na ťuknutí, vrácení spočítá '
                 'aplikace, večer přesná tržba a souhrn v PDF pro pokladníka. Bez registrace.',
            h1='Pokladna pro spolek a školní akci',
            eyebrow='Plesy, dětské dny, hasičské zábavy, školní jarmarky',
            lede='U kasy se střídají dobrovolníci a večer chce pokladník vědět, kolik se vybralo. Tapkasa v telefonu '
                 'hlídá ceny, počítá vrácení a tržbu sečte sama. Bez registrace a bez zaučování.',
            sections=[
                ('Kasu zvládne každý dobrovolník',
                 '<p>Položky jsou velké barevné karty, takže obsluha nehledá v seznamu ani nepočítá z hlavy. Ťukne, '
                 'co si zákazník řekl, zvolí Hotově nebo Kartou a u hotovosti vidí, kolik vrátit. Střídání u kasy '
                 'znamená jen předat telefon.</p>'),
                ('Večer přesná tržba pro pokladníka',
                 '<p>Přehled ukáže tržbu celkem, hotovost a karty zvlášť a kolik se čeho prodalo. Souhrn tržeb '
                 'pošlete jako PDF pokladníkovi nebo výboru. Po akci zvolíte Uzavřít akci, tržba se uloží do '
                 'archivu a příště začínáte od nuly.</p>'),
                ('Bez účtu, bez ověřování, bez poplatků',
                 '<p>Tapkasa nechce registraci, IČO ani bankovní účet a z tržby si nic nebere. Peníze jdou do vaší '
                 'kasičky. Data zůstávají v telefonu, který u kasy používáte.</p>'),
                ('Větší akce: bar a kuchyň zvlášť',
                 '<p>Na plese nebo hasičské zábavě může jeden telefon účtovat u baru a druhý ukazovat objednávky '
                 'v kuchyni. Stačí na to jedno předplatné Tapkasa Pro, které mají noví předplatitelé 14 dní na '
                 'zkoušku zdarma.</p>'),
            ],
            faq=[
                ('Stačí na školní jarmark verze zdarma?',
                 'Na menší akci ano: zdarma je 10 zaplacených účtů denně. Když čekáte víc zákazníků, zapněte si '
                 'předem Tapkasa Pro, noví předplatitelé mají 14 dní na zkoušku zdarma.'),
                ('Potřebuje spolek registraci nebo ověření?',
                 'Ne. Tapkasu jen stáhnete a otevřete. Nezakládá se žádný účet a nic se neověřuje.'),
            ],
        ),
        festival=dict(
            path='pokladna-na-festival.html', card='Pokladna na festival',
            title='Pokladna na festival: fronta objednávek a dva telefony | Tapkasa',
            desc='Pokladna do mobilu pro stánek na festivalu: rychlé účtování, fronta objednávek s čísly, kasa a '
                 'výdej na dvou telefonech i bez internetu. Vyzkoušejte ji hned v prohlížeči.',
            h1='Pokladna na festival: ať fronta ubývá',
            eyebrow='Festivaly, food trucky, koncerty',
            lede='Na festivalu rozhoduje rychlost. Tapkasa zkrátí účtování na pár ťuknutí, zaplacené objednávky '
                 'řadí do fronty s čísly a kasu s výdejem propojí i tam, kde není signál.',
            sections=[
                ('Objednávka za pár vteřin',
                 '<p>Menu máte na barevných kartách, nejprodávanější položky nahoře. Ťuknete, co si zákazník řekl, '
                 'a dole vidíte částku. U hotovosti ťuknete na bankovku a Tapkasa ukáže vrácení.</p>'),
                ('Čísla místo křičení',
                 '<p>Každý zaplacený účet dostane číslo. Výdej na druhém telefonu vidí, co má připravit, odškrtává '
                 'hotové kusy a nové objednávky si může nechat číst nahlas.</p>'),
                ('Louka bez signálu',
                 '<p>Dva iPhony nebo dva telefony s Androidem se propojí napřímo, bez Wi-Fi a bez dat. Kombinace '
                 'iPhonu s Androidem potřebuje internet, počítejte s tím při výběru zařízení.</p>'),
                ('Kelímky na zálohu',
                 '<p>Zálohu na kelímek a její vrácení si přidáte jako dvě položky tlačítkem „+ Přidat zálohu“. '
                 'Vrácení se z účtu odečte a v přehledu jsou zálohy vedené zvlášť od tržby.</p>'),
            ],
            faq=[
                ('Funguje propojení dvou telefonů bez internetu?',
                 'Mezi dvěma iPhony nebo dvěma zařízeními s Androidem ano, napřímo. iPhone s Androidem se spojí jen '
                 'přes internet.'),
                ('Můžu brát platby kartou?',
                 'Ano, na vlastním terminálu. V Tapkase platbu jen označíte jako Kartou, aby v přehledu seděla '
                 'hotovost i karty.'),
            ],
        ),
        fair=dict(
            path='pokladna-na-jarmark.html', card='Pokladna na jarmark a farmářský trh',
            title='Pokladna na jarmark a farmářský trh do mobilu | Tapkasa',
            desc='Pokladna do mobilu na jarmark, farmářský nebo řemeslný trh: vlastní položky i jiná částka, vrácení '
                 'spočítá aplikace, večer tržba po položkách. Bez internetu a bez registrace.',
            h1='Pokladna na jarmark a farmářský trh',
            eyebrow='Řemeslné jarmarky, farmářské a bleší trhy',
            lede='Prodáváte med, keramiku nebo koláče a nechcete tahat pokladnu ani platit paušál. Tapkasa '
                 'v telefonu si pamatuje ceny, spočítá vrácení a večer ukáže, co se prodávalo nejvíc.',
            sections=[
                ('Vlastní zboží i jiná částka',
                 '<p>Nejčastější zboží si uložte jako barevné karty. Na kus, který v menu není, je tlačítko „+ Jiná '
                 'částka“: naťukáte cenu a účtujete dál.</p>'),
                ('Víte, co se prodává',
                 '<p>Přehled ukáže prodané kusy po položkách. Po pár trzích vidíte, čeho vzít víc a co zůstává '
                 'ležet.</p>'),
                ('Hotově i kartou',
                 '<p>U hotovosti ťuknete na bankovku, kterou jste dostali, a vidíte, kolik vrátit. Pokud máte '
                 'vlastní terminál, platbu kartou v Tapkase jen označíte a v přehledu ji uvidíte zvlášť.</p>'),
                ('Jeden trh, jedna uzávěrka',
                 '<p>Tlačítkem Uzavřít akci tržbu uložíte do archivu a na dalším trhu začínáte od nuly. Souhrn '
                 'tržeb za zvolené období vytvoříte jako PDF.</p>'),
            ],
            faq=[
                ('Vyplatí se Tapkasa i na jeden trh do roka?',
                 'Ano. Verze zdarma nic nestojí a nemá žádný paušál, 10 zaplacených účtů denně malému stánku často '
                 'stačí.'),
                ('Umí Tapkasa DPH?',
                 'Souhrn tržeb v PDF obsahuje údaje prodejce a rozpis DPH. Není to ale daňový doklad ani účtenka pro '
                 'zákazníka.'),
            ],
        ),
    ),
)
