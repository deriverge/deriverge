# More Fixbill template pages (added 23 November 2026): same structure as texts_intent.py.
# Legal notes were checked against the statute texts and official guidance in force in November 2026
# (zakonyprolidi.cz, slov-lex.sk, gesetze-im-internet.de, entreprendre.service-public.gouv.fr, gov.uk,
# legislation.gov.uk, irs.gov, planalto.gov.br). They are written cautiously and every page says it is not
# legal advice. No e-invoicing promises: where e-invoicing is coming, the page says plainly that the template
# and the app do not produce it. "Free" for the app always with the 5 documents a month limit.
# `body` and `app.p` are trusted HTML; everything else is escaped. No long dashes anywhere.
from texts_intent import CS, DE, EN, FR, GB


def derive(base, **over):
    """A new generator config from a page in the same language: keeps labels, replaces what differs."""
    g = dict(base['gen'])
    for k in ('doc', 'ui'):
        if k in over:
            over[k] = dict(g[k], **over[k])
    g.update(over)
    return g


# ------------------------------------------------------------------------------------------------ Czech quote

CS_NABIDKA = dict(
    id='cs-cenova-nabidka', lang='cs', html_lang='cs', path='cs/cenova-nabidka-vzor/', phrase='cenová nabídka vzor',
    title='Cenová nabídka vzor zdarma: vyplnění online, PDF | Fixbill',
    desc='Vzor cenové nabídky pro řemeslníky a živnostníky k vyplnění v prohlížeči: položky práce a materiálu, DPH, '
         'platnost nabídky a podpis zákazníka. Uložte jako PDF, nic se nikam neodesílá.',
    h1='Vzor cenové nabídky k vyplnění online',
    lede='Vyplňte položky, zkontrolujte náhled a nabídku si vytiskněte nebo uložte jako PDF. Vzor počítá s DPH '
         'i bez ní, s platností nabídky a s místem pro podpis zákazníka. Všechno zůstává ve vašem prohlížeči.',
    jump='Vyplnit nabídku', crumb='Fixbill',
    card='Cenová nabídka vzor', card_text='Vzor cenové nabídky pro řemeslníky. Vyplníte online a uložíte jako PDF.',
    gen=derive(
        CS, kind='estimate', refFromNumber=False, dates=['issue', 'valid'], pay=['terms'],
        sign=['Datum a podpis zhotovitele', 'Nabídku přijímám: datum a podpis zákazníka'],
        doc=dict(title='Cenová nabídka', seller='Zhotovitel', buyer='Zákazník', total='Cena celkem'),
        ui=dict(preview='Náhled nabídky',
                noscript='Generátor potřebuje zapnutý JavaScript. Co má nabídka obsahovat, najdete níže.'),
        groups=[
            ('Zhotovitel (vy)', [
                ('s_name', 'Jméno nebo firma', 'text', 'Jan Novák', '', None),
                ('s_addr', 'Adresa sídla nebo místa podnikání', 'area', 'Ulice a číslo\nPSČ a obec', '', None),
                ('s_ids', 'IČO, případně DIČ', 'area', 'IČO: 12345678', '', None),
                ('s_contact', 'E-mail nebo telefon', 'text', 'name@example.com', '', None),
            ]),
            ('Zákazník', [
                ('b_name', 'Jméno nebo firma', 'text', 'Jméno zákazníka', '', None),
                ('b_addr', 'Adresa', 'area', 'Ulice a číslo\nPSČ a obec', '', None),
                ('site', 'Místo realizace (pokud se liší)', 'area', 'Adresa zakázky', '', None),
            ]),
            ('Nabídka', [
                ('number', 'Číslo nabídky', 'text', 'N2026-001', 'N2026-001', None),
                ('issue', 'Datum vystavení', 'date', '', '', 0),
                ('valid', 'Nabídka platí do', 'date', '', '', 30),
                ('start', 'Termín realizace', 'text', 'Například: zahájení do 14 dnů, práce asi 3 dny', '', None),
                ('cur', 'Měna', 'sel', '', 'CZK', [('CZK', 'Kč (CZK)'), ('EUR', 'Euro (EUR)')]),
            ]),
            'items',
            ('DPH', [
                ('tax', 'Režim DPH', 'tax', '', '', None),
            ]),
            ('Podmínky', [
                ('terms', 'Platební podmínky', 'text', '',
                 'Záloha 30 % při objednání, doplatek do 14 dnů po předání díla.', None),
                ('notes', 'Poznámka k nabídce', 'area', '',
                 'Cena je určena rozpočtem s výhradou, že se nezaručuje jeho úplnost. Práce a materiál nad rámec '
                 'nabídky provedeme až po odsouhlasení ceny zákazníkem.', None),
            ]),
        ],
        tax=[('none', 'Neplátce DPH', 'Nejsem plátce DPH.', ''), ('21', 'Plátce DPH, sazba 21 %', '', ''),
             ('12', 'Plátce DPH, sazba 12 %', '', ''),
             ('none-rc', 'Přenesená daňová povinnost (stavební práce mezi plátci)', 'Daň odvede zákazník.', '')],
        items=[['Demontáž starého obkladu a odvoz suti', '12', 'm²', '180'], ['Obklad stěn (práce)', '12', 'm²', '750'],
               ['Lepidlo a spárovací hmota (materiál)', '1', 'ks', '2100'], ['Doprava', '1', 'ks', '400']],
    ),
    body='''
<h2>Co má být v cenové nabídce</h2>
<p>Zákon cenové nabídce žádnou podobu nepředepisuje. Aby jí zákazník rozuměl a mohl ji porovnat s ostatními, měla by obsahovat:</p>
<ul>
<li>vaše jméno nebo firmu, adresu, IČO a kontakt,</li>
<li>jméno a adresu zákazníka a místo, kde se bude pracovat,</li>
<li>číslo nabídky, datum a do kdy nabídka platí,</li>
<li>popis prací a položky s množstvím, jednotkou a cenou, práci a materiál zvlášť,</li>
<li>cenu celkem a u plátce DPH základ, sazbu a daň,</li>
<li>termín zahájení a odhad doby prací,</li>
<li>platební podmínky a to, zda je cena pevná, nebo jde o rozpočet s výhradou.</li>
</ul>

<h2>Je cenová nabídka závazná?</h2>
<p>Pokud je z nabídky zřejmé, co a za kolik nabízíte, a že tím chcete být vázáni, jde o návrh smlouvy podle § 1732 občanského zákoníku. Když ho zákazník včas přijme, smlouva je uzavřená. Ve lhůtě, kterou v nabídce určíte pro přijetí, ji nemůžete odvolat, ledaže si to v ní vyhradíte (§ 1738). Proto se vyplatí platnost vždy uvést. Bez ní musí zákazník písemnou nabídku přijmout v době přiměřené povaze zakázky (§ 1735).</p>

<h2>Pevná cena, nebo rozpočet s výhradou?</h2>
<p>Je-li cena díla sjednaná pevnou částkou nebo odkazem na rozpočet, nemůžete později žádat víc jen proto, že práce stála víc úsilí nebo nákladů, než jste čekali (§ 2620 a § 2621 občanského zákoníku).</p>
<p>Jinak je to u rozpočtu daného s výhradou, že se nezaručuje jeho úplnost, nebo že je nezávazný (§ 2622). Když se při práci ukáže nutnost činností, které v rozpočtu nejsou a nedaly se předvídat, můžete žádat zvýšení ceny. Musíte to ale zákazníkovi oznámit bez zbytečného odkladu i s novou cenou, jinak nárok zaniká. Pokud žádáte zvýšení o víc než 10 % ceny podle rozpočtu, může zákazník od smlouvy odstoupit a zaplatí jen poměrnou část za to, co už je hotové. Ve vzoru je výhrada připravená v poznámce, upravte si ji podle zakázky.</p>

<h2>DPH v cenové nabídce</h2>
<p>Neplátce DPH uvádí konečné ceny. Plátce uvádí základ, sazbu a daň. Základní sazba je 21 %. Snížená sazba 12 % se týká mimo jiné stavebních a montážních prací na dokončených stavbách pro bydlení; podmínky si ověřte u účetní.</p>
<p>Děláte-li stavební nebo montážní práce pro jiného plátce DPH, uplatní se obvykle přenesení daňové povinnosti (§ 92e zákona o DPH): daň neúčtujete a na dokladu je věta „daň odvede zákazník“. Ve vzoru k tomu slouží volba „Přenesená daňová povinnost“.</p>

<h2>Když nabídku podepisujete u zákazníka doma</h2>
<p>Uzavřete-li smlouvu se spotřebitelem mimo své obchodní prostory, může od ní zpravidla do 14 dnů odstoupit (§ 1829 občanského zákoníku). O tomto právu ho musíte poučit, jinak se lhůta prodlužuje. Chce-li zákazník, abyste začali dřív, nechte si jeho výslovnou žádost potvrdit písemně. Výjimkou jsou mimo jiné naléhavé opravy, o které zákazník sám výslovně požádal.</p>

<h2>Jak z nabídky udělat zakázku</h2>
<ul>
<li>Pošlete ji ještě ten den, kdy jste byli na místě.</li>
<li>Nabídněte dvě varianty, třeba standardní a lepší materiál.</li>
<li>Usnadněte souhlas: podpis na místě je jistější než e-mail, na který nikdo neodpoví.</li>
<li>Přiložte fotky stavu před zahájením, ať je rozsah prací jasný.</li>
</ul>
''',
    fine='Vzor je obecná pomůcka, ne právní ani daňová rada. Stav k listopadu 2026. Ve sporných případech se obraťte na '
         'advokáta, účetní nebo daňového poradce.',
    app=dict(
        h2='Nabídka podepsaná ještě na místě',
        p='Ve Fixbill máte stejnou nabídku za dvě minuty v telefonu, i se vším, co papírový vzor neumí:',
        bullets=['zákazník podepíše nabídku na displeji a z nabídky uděláte fakturu jedním klepnutím (Pro)',
                 'položky z vlastního ceníku a fotky ze zakázky přímo v nabídce (fotky v Pro)',
                 'faktura s QR Platbou a variabilním symbolem',
                 'přehled, které nabídky zákazník přijal a které faktury jsou po splatnosti'],
        note='Zdarma 5 dokladů měsíčně. Data zůstávají v telefonu.'),
    faq=[
        ('Musí mít cenová nabídka razítko a podpis?',
         'Ne. Zákon formu nepředepisuje. Podpis zákazníka pod větou „Nabídku přijímám“ se ale hodí jako důkaz, že '
         'smlouva vznikla a s jakou cenou.'),
        ('Jak dlouho má nabídka platit?',
         'Běžně 14 až 30 dní. U zakázek s materiálem, jehož cena se rychle mění, zvolte kratší dobu a napište ji do '
         'nabídky.'),
        ('Můžu vzor použít zdarma i pro firmu?',
         'Ano. Vzor na této stránce je zdarma bez omezení a údaje neopouštějí váš prohlížeč. V aplikaci Fixbill je '
         'zdarma 5 dokladů měsíčně.'),
    ],
)

# ------------------------------------------------------------------------------------------------ Slovak invoice

_SK_UI = dict(items='Položky', add='Pridať položku', remove='Odstrániť položku', desc='Popis práce alebo tovaru',
              qty='Množstvo', unit='Jednotka', price='Cena za jednotku', print='Vytlačiť alebo uložiť PDF',
              reset='Začať odznova', resetAsk='Vymazať vyplnené údaje a vrátiť ukážku?', preview='Náhľad faktúry',
              privacy='Údaje zostávajú len vo vašom prehliadači (uložia sa pre ďalšiu návštevu na tomto zariadení). '
                      'PDF uložíte v dialógu tlače voľbou „Uložiť ako PDF“.',
              noscript='Generátor potrebuje zapnutý JavaScript. Povinné údaje faktúry nájdete nižšie.')
_SK_DOC = dict(title='Faktúra', no='č.', seller='Dodávateľ', buyer='Odberateľ', desc='Popis', qty='Množstvo',
               unit='Jedn.', price='Cena za jedn.', priceNet='Cena bez DPH', amount='Spolu', amountNet='Bez DPH',
               net='Základ dane', tax='DPH', total='Spolu na úhradu')
_SK_APP = dict(
    bullets=['zákazník podpíše ponuku na displeji a z ponuky spravíte faktúru jedným ťuknutím (Pro)',
             'QR kód s vaším vlastným odkazom na platbu cez PayPal alebo Stripe',
             'párovanie platieb z výpisu banky (CAMT.053, MT940, CSV) (Pro)',
             'upozornenie na faktúry po splatnosti a upomienka jedným ťuknutím'],
    note='Zadarmo 5 dokladov mesačne. Dáta zostávajú v telefóne.')

SK_FAKTURA = dict(
    id='sk-faktura-vzor', lang='sk', html_lang='sk', path='sk/faktura-vzor/', phrase='faktúra vzor',
    title='Faktúra vzor 2026 zadarmo: vyplnenie online, PDF | Fixbill',
    desc='Vzor faktúry zadarmo na vyplnenie priamo v prehliadači, pre neplatiteľov aj platiteľov DPH, s povinnými '
         'údajmi podľa slovenských predpisov. Uložte ako PDF, nič sa nikam neodosiela.',
    h1='Vzor faktúry zadarmo na vyplnenie online',
    lede='Vyplňte údaje, skontrolujte náhľad a faktúru si vytlačte alebo uložte ako PDF. Vzor počíta s údajmi pre '
         'neplatiteľov aj platiteľov DPH. Všetko sa deje len vo vašom prehliadači, nič neodosielame.',
    jump='Vyplniť faktúru', crumb='Fixbill',
    card='Faktúra vzor', card_text='Vzor faktúry pre neplatiteľov aj platiteľov DPH. Vyplníte online a uložíte ako '
                                   'PDF.',
    gen=dict(
        kind='invoice', locale='sk-SK', currency='EUR', currencies=['EUR', 'CZK'], decComma=True, refFromNumber=True,
        dates=['issue', 'supply', 'due'], pay=['account', 'ref', 'method'], sign=None,
        made='Vytvorené vo Fixbill · deriverge.com/fixbill', doc=_SK_DOC, ui=_SK_UI,
        groups=[
            ('Dodávateľ (vy)', [
                ('s_name', 'Meno alebo obchodné meno', 'text', 'Ján Novák', '', None),
                ('s_addr', 'Sídlo alebo miesto podnikania', 'area', 'Ulica a číslo\nPSČ a obec', '', None),
                ('s_ids', 'IČO, DIČ, prípadne IČ DPH', 'area', 'IČO: 12345678\nDIČ: 1234567890', '', None),
                ('s_extra', 'Zápis v registri', 'text', 'Zapísaný v živnostenskom registri, číslo 000-00000', '',
                 None),
                ('s_contact', 'E-mail alebo telefón', 'text', 'name@example.com', '', None),
            ]),
            ('Odberateľ', [
                ('b_name', 'Meno alebo obchodné meno', 'text', 'Odberateľ s.r.o.', '', None),
                ('b_addr', 'Adresa', 'area', 'Ulica a číslo\nPSČ a obec', '', None),
                ('b_ids', 'IČO, DIČ, IČ DPH', 'area', 'IČO: 87654321', '', None),
            ]),
            ('Faktúra', [
                ('number', 'Číslo faktúry', 'text', '2026001', '2026001', None),
                ('issue', 'Dátum vyhotovenia', 'date', '', '', 0),
                ('supply', 'Dátum dodania', 'date', '', '', 0),
                ('due', 'Dátum splatnosti', 'date', '', '', 14),
                ('cur', 'Mena', 'sel', '', 'EUR', [('EUR', 'Euro (EUR)'), ('CZK', 'Česká koruna (CZK)')]),
            ]),
            'items',
            ('DPH', [
                ('tax', 'Režim DPH', 'tax', '', '', None),
            ]),
            ('Platba', [
                ('account', 'IBAN', 'text', 'SK00 0000 0000 0000 0000 0000', '', None),
                ('ref', 'Variabilný symbol', 'text', 'doplní sa z čísla faktúry', '', None),
                ('method', 'Spôsob úhrady', 'text', '', 'Prevodom na účet', None),
                ('notes', 'Poznámka na faktúre', 'area', 'Napríklad: Ďakujeme za zákazku.', '', None),
            ]),
        ],
        tax=[('none', 'Neplatiteľ DPH', 'Nie som platiteľ DPH.', ''), ('23', 'Platiteľ DPH, sadzba 23 %', '', ''),
             ('19', 'Platiteľ DPH, sadzba 19 %', '', ''), ('5', 'Platiteľ DPH, sadzba 5 %', '', ''),
             ('none-rc', 'Prenesenie daňovej povinnosti (stavebné práce medzi platiteľmi)',
              'Prenesenie daňovej povinnosti.', '')],
        items=[['Obklad stien', '12', 'm²', '30'], ['Lepidlo a škárovacia hmota', '1', 'ks', '64,50'],
               ['Práca', '6', 'h', '28']],
    ),
    body='''
<h2>Povinné údaje na faktúre neplatiteľa DPH</h2>
<p>Živnostník, ktorý nie je platiteľom DPH, vystavuje faktúru ako účtovný doklad podľa § 10 zákona o účtovníctve. Mala by obsahovať:</p>
<ul>
<li>označenie dokladu, teda slovo faktúra a jej číslo,</li>
<li>vaše meno alebo obchodné meno, miesto podnikania a IČO, a údaj o zápise v registri s číslom zápisu (§ 3a Obchodného zákonníka), napríklad v živnostenskom registri,</li>
<li>meno alebo názov odberateľa a jeho adresu,</li>
<li>čo ste dodali: popis práce alebo tovaru, množstvo a cenu za jednotku alebo celkovú sumu,</li>
<li>dátum vyhotovenia a dátum dodania, ak sa líši,</li>
<li>platobné údaje: IBAN, variabilný symbol a dátum splatnosti.</li>
</ul>
<p>Vetu „Nie som platiteľ DPH.“ zákon nevyžaduje, ale zákazníkovi ušetrí otázky. Vo vzore ju doplníte voľbou „Neplatiteľ DPH“.</p>

<h2>Čo navyše musí mať faktúra platiteľa DPH</h2>
<p>Platiteľ vystavuje faktúru podľa § 74 zákona o DPH. Okrem údajov vyššie na nej musí byť:</p>
<ul>
<li>IČ DPH dodávateľa a IČ DPH odberateľa, ak ho má,</li>
<li>poradové číslo faktúry,</li>
<li>dátum dodania alebo prijatia platby, ak sa líši od dátumu vyhotovenia,</li>
<li>množstvo a druh tovaru alebo rozsah a druh služby,</li>
<li>jednotková cena bez dane, základ dane pre každú sadzbu, sadzba a výška dane v eurách.</li>
</ul>
<p>Od roku 2025 platia sadzby 23 %, 19 % a 5 %. Faktúru treba vyhotoviť do 15 dní od dodania alebo od prijatia platby vopred (§ 73).</p>

<h2>Kedy sa stávate platiteľom DPH</h2>
<p>Od roku 2025 sa platiteľom stávate od 1. januára nasledujúceho roka, keď váš obrat za kalendárny rok presiahne 50 000 €. Ak počas roka presiahne 62 500 €, ste platiteľom už dodaním, ktorým ste túto hranicu prekročili. Presné podmienky si overte na finančnej správe alebo u účtovníčky.</p>

<h2>Stavebné práce medzi platiteľmi</h2>
<p>Pri stavebných prácach pre iného platiteľa DPH sa spravidla uplatní prenesenie daňovej povinnosti (§ 69 ods. 12 písm. j) zákona o DPH). Daň neúčtujete a na faktúre je text „prenesenie daňovej povinnosti“. Vo vzore na to slúži voľba „Prenesenie daňovej povinnosti“.</p>

<h2>Elektronická faktúra od roku 2027</h2>
<p>Od 1. januára 2027 majú platitelia DPH pri tuzemských dodaniach pre podnikateľov vystavovať faktúry elektronicky v štruktúrovanom formáte. Neplatitelia ich vystavovať nemusia. Tento vzor ani aplikácia Fixbill takú elektronickú faktúru nevytvárajú: vzor je určený pre neplatiteľov DPH a pre faktúry súkromným zákazníkom. Kto a odkedy musí elektronické faktúry vedieť prijímať, si overte na stránke finančnej správy.</p>

<h2>Aby faktúra prišla zaplatená načas</h2>
<ul>
<li><strong>Variabilný symbol</strong> je najčastejšie číslo faktúry. Vzor ho z čísla doplní sám, keď pole necháte prázdne.</li>
<li><strong>Splatnosť</strong> 14 dní je bežná. Napíšte ju ako konkrétny dátum.</li>
<li><strong>Číslovanie</strong> držte v jednom rade bez medzier, napríklad 2026001, 2026002.</li>
</ul>
''',
    fine='Vzor je všeobecná pomôcka, nie právne ani daňové poradenstvo. Stav k novembru 2026. V sporných prípadoch sa '
         'obráťte na účtovníčku alebo daňového poradcu.',
    app=dict(
        h2='Fakturujte rovno z telefónu',
        p='Vo Fixbill máte rovnakú faktúru za dve minúty, aj s tým, čo papierový vzor nevie:',
        **_SK_APP),
    faq=[
        ('Musí byť na faktúre pečiatka a podpis?',
         'Pečiatka nie je povinná. Zákon o účtovníctve žiada podpisový záznam zodpovednej osoby na účtovnom doklade, '
         'ak overenie nezabezpečujete inak. Ako to riešiť pri elektronických dokladoch, vám povie účtovníčka.'),
        ('Môžem faktúru poslať e-mailom ako PDF?',
         'Áno, ak s tým odberateľ súhlasí, čo je dnes bežné. Od roku 2027 však pre platiteľov DPH pri tuzemských '
         'faktúrach medzi podnikateľmi platí povinná elektronická faktúra, ktorú tento vzor nevytvára.'),
        ('Je vzor naozaj zadarmo?',
         'Áno. Vzor na tejto stránke je zadarmo bez obmedzenia a údaje neopúšťajú váš prehliadač. V aplikácii Fixbill '
         'je zadarmo 5 dokladov mesačne.'),
    ],
)

# ------------------------------------------------------------------------------------------------ Slovak quote

SK_PONUKA = dict(
    id='sk-cenova-ponuka', lang='sk', html_lang='sk', path='sk/cenova-ponuka-vzor/', phrase='cenová ponuka vzor',
    title='Cenová ponuka vzor zadarmo: vyplnenie online, PDF | Fixbill',
    desc='Vzor cenovej ponuky pre remeselníkov a živnostníkov na vyplnenie v prehliadači: položky práce a materiálu, '
         'DPH, platnosť ponuky a podpis zákazníka. Uložte ako PDF, nič sa nikam neodosiela.',
    h1='Vzor cenovej ponuky na vyplnenie online',
    lede='Vyplňte položky, skontrolujte náhľad a ponuku si vytlačte alebo uložte ako PDF. Vzor počíta s DPH aj bez '
         'nej, s platnosťou ponuky a s miestom na podpis zákazníka. Všetko zostáva vo vašom prehliadači.',
    jump='Vyplniť ponuku', crumb='Fixbill',
    card='Cenová ponuka vzor', card_text='Vzor cenovej ponuky pre remeselníkov. Vyplníte online a uložíte ako PDF.',
    gen=dict(
        kind='estimate', locale='sk-SK', currency='EUR', currencies=['EUR', 'CZK'], decComma=True,
        refFromNumber=False, dates=['issue', 'valid'], pay=['terms'],
        sign=['Dátum a podpis zhotoviteľa', 'Ponuku prijímam: dátum a podpis zákazníka'],
        made='Vytvorené vo Fixbill · deriverge.com/fixbill',
        doc=dict(_SK_DOC, title='Cenová ponuka', seller='Zhotoviteľ', buyer='Zákazník', total='Cena spolu'),
        ui=dict(_SK_UI, preview='Náhľad ponuky',
                noscript='Generátor potrebuje zapnutý JavaScript. Čo má ponuka obsahovať, nájdete nižšie.'),
        groups=[
            ('Zhotoviteľ (vy)', [
                ('s_name', 'Meno alebo obchodné meno', 'text', 'Ján Novák', '', None),
                ('s_addr', 'Sídlo alebo miesto podnikania', 'area', 'Ulica a číslo\nPSČ a obec', '', None),
                ('s_ids', 'IČO, DIČ, prípadne IČ DPH', 'area', 'IČO: 12345678', '', None),
                ('s_contact', 'E-mail alebo telefón', 'text', 'name@example.com', '', None),
            ]),
            ('Zákazník', [
                ('b_name', 'Meno alebo obchodné meno', 'text', 'Meno zákazníka', '', None),
                ('b_addr', 'Adresa', 'area', 'Ulica a číslo\nPSČ a obec', '', None),
                ('site', 'Miesto realizácie (ak sa líši)', 'area', 'Adresa zákazky', '', None),
            ]),
            ('Ponuka', [
                ('number', 'Číslo ponuky', 'text', 'P2026-001', 'P2026-001', None),
                ('issue', 'Dátum vyhotovenia', 'date', '', '', 0),
                ('valid', 'Ponuka platí do', 'date', '', '', 30),
                ('start', 'Termín realizácie', 'text', 'Napríklad: začiatok do 14 dní, práce asi 3 dni', '', None),
                ('cur', 'Mena', 'sel', '', 'EUR', [('EUR', 'Euro (EUR)'), ('CZK', 'Česká koruna (CZK)')]),
            ]),
            'items',
            ('DPH', [
                ('tax', 'Režim DPH', 'tax', '', '', None),
            ]),
            ('Podmienky', [
                ('terms', 'Platobné podmienky', 'text', '',
                 'Záloha 30 % pri objednávke, doplatok do 14 dní po odovzdaní diela.', None),
                ('notes', 'Poznámka k ponuke', 'area', '',
                 'Cena je určená odhadom podľa obhliadky. Práce a materiál nad rámec ponuky vykonáme až po písomnom '
                 'odsúhlasení ceny zákazníkom.', None),
            ]),
        ],
        tax=[('none', 'Neplatiteľ DPH', 'Nie som platiteľ DPH.', ''), ('23', 'Platiteľ DPH, sadzba 23 %', '', ''),
             ('19', 'Platiteľ DPH, sadzba 19 %', '', ''), ('5', 'Platiteľ DPH, sadzba 5 %', '', ''),
             ('none-rc', 'Prenesenie daňovej povinnosti (stavebné práce medzi platiteľmi)',
              'Prenesenie daňovej povinnosti.', '')],
        items=[['Demontáž starého obkladu a odvoz sute', '12', 'm²', '8'], ['Obklad stien (práca)', '12', 'm²', '30'],
               ['Lepidlo a škárovacia hmota (materiál)', '1', 'ks', '64,50'], ['Doprava', '1', 'ks', '20']],
    ),
    body='''
<h2>Čo má byť v cenovej ponuke</h2>
<p>Zákon cenovej ponuke žiadnu podobu nepredpisuje. Aby jej zákazník rozumel a mohol ju porovnať s inými, mala by obsahovať:</p>
<ul>
<li>vaše meno alebo obchodné meno, adresu, IČO a kontakt,</li>
<li>meno a adresu zákazníka a miesto, kde sa bude pracovať,</li>
<li>číslo ponuky, dátum a dokedy ponuka platí,</li>
<li>popis prác a položky s množstvom, jednotkou a cenou, prácu a materiál osobitne,</li>
<li>cenu spolu a pri platiteľovi DPH základ, sadzbu a daň,</li>
<li>termín začatia a odhad trvania prác,</li>
<li>platobné podmienky a to, či je cena pevná, alebo ide o odhad.</li>
</ul>

<h2>Cena podľa rozpočtu, alebo odhadom?</h2>
<p>Pre zákazky so súkromnými zákazníkmi platí Občiansky zákonník. Ak je cena dohodnutá podľa rozpočtu, bez súhlasu zákazníka ju nemožno zvýšiť a práce mimo rozpočtu môžete účtovať len vtedy, keď ich zákazník písomne schválil alebo dodatočne písomne objednal (§ 635).</p>
<p>Ak je cena určená odhadom a ukáže sa, že ju bude treba podstatne prekročiť, musíte na to zákazníka bez meškania písomne upozorniť a oznámiť novú cenu, inak nemáte právo na zaplatenie rozdielu. Zákazník môže v takom prípade od zmluvy odstúpiť (§ 636). Napíšte preto do ponuky, o ktorý prípad ide.</p>
<p>Medzi podnikateľmi sa použije Obchodný zákonník (§ 547). Pri rozpočte bez záruky úplnosti alebo pri nezáväznom rozpočte možno žiadať primerané zvýšenie ceny, treba to však oznámiť bez zbytočného odkladu. Ak ide o zvýšenie o viac než 10 %, objednávateľ môže od zmluvy odstúpiť.</p>

<h2>DPH v cenovej ponuke</h2>
<p>Neplatiteľ DPH uvádza konečné ceny. Platiteľ uvádza základ, sadzbu a daň; základná sadzba je 23 %. Pri stavebných prácach pre iného platiteľa DPH sa spravidla uplatní prenesenie daňovej povinnosti a daň neúčtujete. Vo vzore na to slúži voľba „Prenesenie daňovej povinnosti“.</p>

<h2>Keď ponuku podpisujete u zákazníka doma</h2>
<p>Ak zmluvu so spotrebiteľom uzavriete mimo svojich prevádzkových priestorov, môže od nej spravidla do 14 dní odstúpiť (zákon č. 108/2024 Z. z. o ochrane spotrebiteľa). O tomto práve ho musíte poučiť, inak sa lehota predlžuje. Výnimkou sú okrem iného naliehavé opravy, o ktoré zákazník výslovne požiadal.</p>

<h2>Ako z ponuky spraviť zákazku</h2>
<ul>
<li>Pošlite ju ešte v deň obhliadky.</li>
<li>Ponúknite dva varianty, napríklad štandardný a lepší materiál.</li>
<li>Uľahčite súhlas: podpis na mieste je istejší než e-mail, na ktorý nikto neodpovie.</li>
<li>Priložte fotky stavu pred začatím, aby bol rozsah prác jasný.</li>
</ul>
''',
    fine='Vzor je všeobecná pomôcka, nie právne ani daňové poradenstvo. Stav k novembru 2026. V sporných prípadoch sa '
         'obráťte na advokáta, účtovníčku alebo daňového poradcu.',
    app=dict(
        h2='Ponuka podpísaná ešte na mieste',
        p='Vo Fixbill máte rovnakú ponuku za dve minúty v telefóne, aj s tým, čo papierový vzor nevie:',
        **_SK_APP),
    faq=[
        ('Je cenová ponuka záväzná?',
         'Ak je z ponuky jasné, čo a za koľko ponúkate, a zákazník ju včas prijme, vzniká zmluva. Preto do ponuky '
         'vždy napíšte, dokedy platí a či je cena pevná, alebo odhadom.'),
        ('Ako dlho má ponuka platiť?',
         'Bežne 14 až 30 dní. Pri zákazkách s materiálom, ktorého cena sa rýchlo mení, zvoľte kratší čas.'),
        ('Je vzor naozaj zadarmo?',
         'Áno. Vzor na tejto stránke je zadarmo bez obmedzenia a údaje neopúšťajú váš prehliadač. V aplikácii Fixbill '
         'je zadarmo 5 dokladov mesačne.'),
    ],
)

# ------------------------------------------------------------------------------------------------ German invoice

DE_RECHNUNG = dict(
    id='de-rechnung-kleinunternehmer', lang='de', html_lang='de', path='de/rechnung-kleinunternehmer/',
    phrase='Rechnungsvorlage Kleinunternehmer',
    title='Rechnungsvorlage für Kleinunternehmer (§ 19 UStG), kostenlos | Fixbill',
    desc='Kostenlose Rechnungsvorlage für Kleinunternehmer: online ausfüllen, Vorschau prüfen und als PDF speichern. '
         'Mit den Pflichtangaben nach § 34a UStDV und dem Hinweis auf § 19 UStG.',
    h1='Rechnungsvorlage für Kleinunternehmer',
    lede='Füllen Sie die Rechnung direkt im Browser aus, prüfen Sie die Vorschau und speichern Sie sie als PDF oder '
         'drucken Sie sie aus. Der Hinweis auf die Kleinunternehmerregelung ist schon enthalten. Ihre Eingaben '
         'bleiben auf Ihrem Gerät.',
    jump='Rechnung ausfüllen', crumb='Fixbill',
    card='Rechnungsvorlage Kleinunternehmer', card_text='Rechnung nach § 19 UStG online ausfüllen und als PDF '
                                                        'speichern.',
    gen=derive(
        DE, kind='invoice', refFromNumber=False, dates=['issue', 'supply', 'due'], pay=['account', 'ref', 'terms'],
        sign=None,
        doc=dict(title='Rechnung', seller='Rechnungssteller', buyer='Rechnungsempfänger', total='Rechnungsbetrag'),
        ui=dict(preview='Vorschau der Rechnung'),
        groups=[
            ('Ihr Betrieb', [
                ('s_name', 'Vollständiger Name oder Firma', 'text', 'Max Muster Fliesenlegerbetrieb', '', None),
                ('s_addr', 'Anschrift', 'area', 'Straße und Hausnummer\nPLZ und Ort', '', None),
                ('s_ids', 'Steuernummer, USt-IdNr. oder Kleinunternehmer-IdNr.', 'text', 'Steuernummer 12/345/67890',
                 '', None),
                ('s_contact', 'Telefon oder E-Mail', 'text', 'name@example.com', '', None),
            ]),
            ('Kunde', [
                ('b_name', 'Vollständiger Name oder Firma', 'text', 'Name des Kunden', '', None),
                ('b_addr', 'Anschrift', 'area', 'Straße und Hausnummer\nPLZ und Ort', '', None),
            ]),
            ('Rechnung', [
                ('number', 'Rechnungsnummer', 'text', '2026-001', '2026-001', None),
                ('issue', 'Rechnungsdatum', 'date', '', '', 0),
                ('supply', 'Leistungsdatum', 'date', '', '', 0),
                ('due', 'Zahlbar bis', 'date', '', '', 14),
                ('cur', 'Währung', 'sel', '', 'EUR', [('EUR', 'Euro (EUR)'), ('CHF', 'Franken (CHF)')]),
            ]),
            'items',
            ('Umsatzsteuer', [
                ('tax', 'Umsatzsteuer', 'tax', '', '', None),
            ]),
            ('Zahlung', [
                ('account', 'Bankverbindung', 'area', 'Kontoinhaber\nIBAN DE00 0000 0000 0000 0000 00', '', None),
                ('ref', 'Verwendungszweck', 'text', 'Rechnung 2026-001', '', None),
                ('terms', 'Zahlungsbedingungen', 'text', '', 'Zahlbar ohne Abzug bis zum genannten Datum.', None),
                ('notes', 'Hinweis', 'area', 'Zum Beispiel: Vielen Dank für Ihren Auftrag.', '', None),
            ]),
        ],
        tax=[('none', 'Kleinunternehmer (§ 19 UStG)', 'Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.', ''),
             ('19', '19 % Umsatzsteuer', '', ''), ('7', '7 % Umsatzsteuer', '', '')],
        items=[['Wandfliesen verlegen (Arbeitszeit)', '12', 'm²', '38'],
               ['Fliesenkleber und Fugenmörtel (Material)', '1', 'pauschal', '84,50'],
               ['Anfahrt', '1', 'pauschal', '25']],
    ),
    body='''
<h2>Pflichtangaben auf der Rechnung eines Kleinunternehmers</h2>
<p>Seit 2025 regelt § 34a der Umsatzsteuer-Durchführungsverordnung, was auf der Rechnung eines Kleinunternehmers stehen muss:</p>
<ul>
<li>Ihr vollständiger Name und Ihre vollständige Anschrift sowie Name und Anschrift des Kunden,</li>
<li>Ihre Steuernummer, Umsatzsteuer-Identifikationsnummer oder Kleinunternehmer-Identifikationsnummer,</li>
<li>das Ausstellungsdatum,</li>
<li>Menge und Art der gelieferten Gegenstände oder Umfang und Art der Leistung,</li>
<li>das Entgelt in einer Summe, mit dem Hinweis, dass die Steuerbefreiung für Kleinunternehmer gilt.</li>
</ul>
<p>Eine fortlaufende Rechnungsnummer und das Leistungsdatum verlangt § 34a nicht ausdrücklich. Beides gehört trotzdem auf jede Rechnung: Die Nummer brauchen Sie für eine ordentliche Buchführung, das Leistungsdatum erspart Rückfragen. Umsatzsteuer weisen Sie nicht aus.</p>

<h2>Wie lautet der Hinweis auf § 19 UStG?</h2>
<p>Einen festen Wortlaut gibt es nicht. Üblich ist zum Beispiel „Gemäß § 19 UStG wird keine Umsatzsteuer berechnet.“ In der Vorlage ist dieser Satz voreingestellt, wenn Sie „Kleinunternehmer“ wählen.</p>

<h2>Wer ist Kleinunternehmer?</h2>
<p>Seit 2025 gilt: Ihr Gesamtumsatz lag im vorangegangenen Kalenderjahr nicht über 25.000 Euro und überschreitet im laufenden Jahr 100.000 Euro nicht (§ 19 UStG). Wird die Grenze von 100.000 Euro im laufenden Jahr überschritten, endet die Befreiung sofort, schon für den Umsatz, mit dem Sie die Grenze überschreiten. Ab dann stellen Sie Rechnungen mit Umsatzsteuer aus; in der Vorlage wählen Sie dafür 19 % oder 7 %.</p>

<h2>E-Rechnung, PDF oder Papier?</h2>
<p>Kleinunternehmer müssen auch gegenüber Geschäftskunden keine E-Rechnung im strukturierten Format ausstellen. Empfangen können müssen sie E-Rechnungen aber seit dem 1. Januar 2025. Eine Rechnung auf Papier ist immer möglich. Eine PDF-Rechnung per E-Mail setzt voraus, dass der Empfänger damit einverstanden ist; eine besondere Form ist dafür nicht vorgeschrieben. Diese Vorlage erzeugt ein PDF oder einen Ausdruck, keine E-Rechnung.</p>

<h2>Kleinbetragsrechnung bis 250 Euro</h2>
<p>Bei Rechnungen bis 250 Euro Gesamtbetrag genügen nach § 33 UStDV Ihr Name und Ihre Anschrift, das Datum, Menge und Art der Leistung und der Betrag mit dem Hinweis auf die Steuerbefreiung.</p>

<h2>Tipps für Handwerkerrechnungen an Privatkunden</h2>
<ul>
<li><strong>Arbeitszeit und Material getrennt:</strong> Privatkunden können 20 Prozent der Arbeitskosten für Handwerkerleistungen im Haushalt von der Steuer abziehen, höchstens 1.200 Euro im Jahr (§ 35a EStG). Dafür brauchen sie eine Rechnung und müssen überweisen, Barzahlung zählt nicht.</li>
<li><strong>Aufbewahren:</strong> Ihre Rechnungen bewahren Sie acht Jahre auf (§ 14b UStG).</li>
<li><strong>Zahlungsziel:</strong> Nennen Sie ein konkretes Datum statt „14 Tage“.</li>
</ul>
''',
    fine='Diese Vorlage ist eine allgemeine Hilfe und keine Rechts- oder Steuerberatung. Stand November 2026. Im '
         'Zweifel fragen Sie Ihren Steuerberater.',
    app=dict(
        h2='Rechnung direkt vom Handy',
        p='Mit Fixbill schreiben Sie dieselbe Rechnung in zwei Minuten und haben mehr als eine Vorlage:',
        bullets=['Rechnungen mit GiroCode (EPC-QR-Code) für die Überweisung',
                 'Ihr Kunde unterschreibt das Angebot auf dem Display, daraus wird mit einem Tippen die Rechnung (Pro)',
                 'Zahlungsabgleich per Kontoauszug (CAMT.053, MT940, CSV) (Pro)',
                 'Hinweis bei überfälligen Rechnungen und Zahlungserinnerung mit einem Tippen'],
        note='Kostenlos für 5 Dokumente pro Monat. Ihre Daten bleiben auf dem Handy. Fixbill erstellt PDF-Rechnungen, '
             'keine E-Rechnungen.'),
    faq=[
        ('Darf ich als Kleinunternehmer Umsatzsteuer ausweisen?',
         'Nein. Wer als Kleinunternehmer Umsatzsteuer auf der Rechnung ausweist, schuldet sie dem Finanzamt. Schreiben '
         'Sie stattdessen den Hinweis auf § 19 UStG.'),
        ('Brauche ich eine Rechnungsnummer?',
         '§ 34a UStDV verlangt sie für Kleinunternehmer nicht ausdrücklich. Für eine nachvollziehbare Buchführung '
         'sollten Sie Ihre Rechnungen trotzdem fortlaufend nummerieren.'),
        ('Ist die Vorlage wirklich kostenlos?',
         'Ja. Die Vorlage auf dieser Seite ist ohne Einschränkung kostenlos, Ihre Eingaben verlassen den Browser nicht. '
         'In der App Fixbill sind 5 Dokumente pro Monat kostenlos.'),
    ],
)

# ------------------------------------------------------------------------------------------------ UK quote

GB_QUOTE = dict(
    id='en-gb-builders-quote', lang='en-gb', html_lang='en-GB', path='en-gb/builders-quote-template/',
    phrase='builders quote template',
    title='Builders Quote Template (UK): Free, Fill In Online | Fixbill',
    desc='Free quote template for builders and tradesmen in the UK. Fill it in online with labour, materials and VAT, '
         'add your terms, and save it as a PDF for your customer to sign. Nothing is uploaded.',
    h1='Free quote template for builders and tradesmen',
    lede='Fill in the quote in your browser, check the preview and save it as a PDF or print it. It has room for '
         'labour and materials, VAT if you are registered, how long the price stands and a signature for the customer. '
         'Your details stay on your device.',
    jump='Fill in the quote', crumb='Fixbill',
    card='Builders quote template (UK)', card_text='Quote for building work and home improvements, with or without '
                                                   'VAT. Fill in online, save as PDF.',
    gen=derive(
        GB, kind='estimate', dates=['issue', 'valid'], pay=['terms'],
        sign=['Signed for the business, date', 'Accepted by the customer: signature and date'],
        doc=dict(title='Quote', seller='From', buyer='Customer', total='Total price'),
        ui=dict(preview='Quote preview',
                noscript='The generator needs JavaScript. What to put in a quote is listed below.'),
        groups=[
            ('Your business', [
                ('s_name', 'Your name or business name', 'text', 'J. Smith Building Services', '', None),
                ('s_addr', 'Business address', 'area', 'Street\nTown and postcode', '', None),
                ('s_ids', 'VAT number or company number (if any)', 'area', 'VAT reg. no. GB123456789', '', None),
                ('s_contact', 'Phone or e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Customer', [
                ('b_name', 'Customer name', 'text', 'Customer name', '', None),
                ('b_addr', 'Customer address', 'area', 'Street\nTown and postcode', '', None),
                ('site', 'Job address (if different)', 'area', 'Job address', '', None),
            ]),
            ('Quote', [
                ('number', 'Quote number', 'text', 'Q-0001', 'Q-0001', None),
                ('issue', 'Date', 'date', '', '', 0),
                ('valid', 'Price valid until', 'date', '', '', 30),
                ('start', 'Start date and how long it will take', 'text', 'Start w/c 7 December, about 4 working days',
                 '', None),
                ('cur', 'Currency', 'sel', '', 'GBP', [('GBP', 'Pound (GBP)'), ('EUR', 'Euro (EUR)')]),
            ]),
            'items',
            ('VAT', [
                ('tax', 'VAT', 'tax', '', '', None),
            ]),
            ('Terms', [
                ('terms', 'Payment terms', 'text', '',
                 'Deposit of 25% on acceptance, balance within 7 days of completion.', None),
                ('notes', 'What is and is not included', 'area', '',
                 'This is a fixed price for the work described above. Anything not listed, and any problems that '
                 'could not be seen at the survey, will be priced and agreed in writing before the extra work is '
                 'done.', None),
            ]),
        ],
        items=[['Strip out existing bathroom suite and tiles, dispose of waste', '1', 'item', '380'],
               ['Supply and fit wall tiles', '12', 'm²', '34'],
               ['Tile adhesive and grout', '1', 'item', '72.50'], ['Plumbing labour', '6', 'h', '45']],
    ),
    body='''
<h2>Quote or estimate?</h2>
<p>A quote is a fixed price for a defined job. An estimate is your best guess, and the final bill can turn out higher. Customers are told to ask for a quote for exactly that reason, so say clearly at the top which one this is. If you give a quote, describe the work precisely and say what happens when something unexpected turns up, because you cannot simply charge more later.</p>

<h2>What to put in a builder's quote</h2>
<ul>
<li>your name or business name, address and contact details, and your VAT number if you are registered,</li>
<li>the customer's name and address, and the address of the job,</li>
<li>a quote number, the date and how long the price is valid,</li>
<li>a clear description of the work, with labour and materials broken down,</li>
<li>what is not included, for example making good, skips, scaffolding or building control fees,</li>
<li>the total price, and the VAT if you charge it,</li>
<li>the start date and how long the job should take,</li>
<li>payment terms: deposit, stage payments and when the balance is due,</li>
<li>a place for the customer to sign and date their acceptance.</li>
</ul>

<h2>Why the price, the dates and the scope belong in writing</h2>
<p>Under the Consumer Rights Act 2015 you must carry out the work with reasonable care and skill. If no price was agreed, the customer only has to pay a reasonable price, and if no time was agreed, the work must be done within a reasonable time. A written quote with a price, a start date and a duration removes those arguments before they start. What you tell a customer about the job can also become part of the contract, so keep the description accurate.</p>

<h2>VAT on building work</h2>
<p>You must register for VAT when your taxable turnover goes over £90,000 in a rolling 12 month period. If you are not registered, do not show VAT at all. If you are, the standard rate is 20%. Some work has a reduced or zero rate: for example, the installation of certain energy saving materials in homes is zero rated until 31 March 2027. Check HMRC's guidance for the job before you rely on a lower rate.</p>
<p>The construction domestic reverse charge only applies between VAT registered businesses under CIS. It does not apply when you work for a homeowner.</p>

<h2>Quotes agreed at the customer's home</h2>
<p>If the contract is made at the customer's home or away from your business premises, a consumer usually has 14 days to cancel under the Consumer Contracts Regulations 2013. You must give them written information about this right. If you do not, the cancellation period can run for up to a year longer. If the customer wants you to start within the 14 days, get that request in writing, on paper or by e-mail. There are exceptions, for example for urgent repairs the customer asked you to come out for, so check which rules apply to your job.</p>

<h2>Tips to win the job</h2>
<ul>
<li>Send the quote the same day as the survey.</li>
<li>Offer options, for example standard and premium tiles, so the customer chooses between your prices.</li>
<li>Add photos of the current state so the scope is clear.</li>
<li>Make it easy to say yes: a signature on the spot beats a printout on the fridge.</li>
</ul>
''',
    fine='This template is general help, not legal or tax advice. Last checked November 2026. If in doubt, ask your '
         'accountant or trade association, or check GOV.UK.',
    app=dict(
        h2='Quote on site, signed before you leave',
        p='With Fixbill the same quote takes two minutes on your phone, plus what a template cannot do:',
        bullets=['your customer signs the quote on your screen, then it becomes the invoice with one tap (Pro)',
                 'work and materials from your own price list, and job photos on the quote (photos in Pro)',
                 'a QR code for your own PayPal or Stripe payment link on the invoice',
                 'see which quotes were accepted and which invoices are overdue'],
        note='Free for 5 documents a month. Your data stays on your phone.'),
    faq=[
        ('Is a quote legally binding?',
         'Once the customer accepts a quote, you have a contract at that price for the work described. That is why '
         'the description, the exclusions and how long the price stands matter.'),
        ('How long should a quote be valid?',
         '30 days is common. If material prices are moving quickly, choose a shorter period and say so on the quote.'),
        ('Is the template really free?',
         'Yes. The template on this page is free with no limit and what you type never leaves your browser. In the '
         'Fixbill app, 5 documents a month are free.'),
    ],
)

# ------------------------------------------------------------------------------------------------ US invoice

EN_INVOICE = dict(
    id='en-invoice-template', lang='en', html_lang='en', path='invoice-template/',
    phrase='invoice template',
    title='Free Invoice Template for Contractors: Fill In Online | Fixbill',
    desc='Free invoice template for contractors and small businesses. Fill it in online, add sales tax if you charge '
         'it, check the preview and save it as a PDF. Nothing is uploaded.',
    h1='Free invoice template you can fill in online',
    lede='Fill in the invoice in your browser, check the preview and save it as a PDF or print it. Add labor and '
         'materials line by line, sales tax if it applies, and how you want to be paid. Your details stay on your '
         'device.',
    jump='Fill in the invoice', crumb='Fixbill',
    card='Invoice template', card_text='Invoice for contractors and small businesses. Fill in online, save as PDF.',
    gen=derive(
        EN, kind='invoice', dates=['issue', 'supply', 'due'], pay=['terms', 'account'], sign=None,
        doc=dict(title='Invoice', seller='From', buyer='Bill to', total='Amount due'),
        ui=dict(preview='Invoice preview',
                noscript='The generator needs JavaScript. What to put on an invoice is listed below.'),
        groups=[
            ('Your business', [
                ('s_name', 'Business name', 'text', 'Smith Remodeling LLC', '', None),
                ('s_addr', 'Address', 'area', 'Street\nCity, State ZIP', '', None),
                ('s_ids', 'License number (if required)', 'text', 'License #123456', '', None),
                ('s_contact', 'Phone or e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Client', [
                ('b_name', 'Client name', 'text', 'Client name', '', None),
                ('b_addr', 'Billing address', 'area', 'Street\nCity, State ZIP', '', None),
                ('site', 'Job address (if different)', 'area', 'Job address', '', None),
            ]),
            ('Invoice', [
                ('number', 'Invoice number', 'text', 'INV-1001', 'INV-1001', None),
                ('issue', 'Invoice date', 'date', '', '', 0),
                ('supply', 'Work completed on', 'date', '', '', 0),
                ('due', 'Due date', 'date', '', '', 15),
                ('cur', 'Currency', 'sel', '', 'USD', [('USD', 'US dollar (USD)'), ('CAD', 'Canadian dollar (CAD)')]),
            ]),
            'items',
            ('Tax', [
                ('tax', 'Sales tax', 'tax', '', '', None),
                ('taxrate', 'Tax rate in %', 'text', '8.25', '', None),
            ]),
            ('Payment', [
                ('terms', 'Payment terms', 'text', '', 'Net 15. Please pay by the due date.', None),
                ('account', 'How to pay', 'area', 'Check payable to Smith Remodeling LLC\nor bank transfer details',
                 '', None),
                ('notes', 'Notes', 'area', 'For example: Thank you for your business.', '', None),
            ]),
        ],
        items=[['Install wall tile, bathroom', '120', 'sq ft', '12'],
               ['Tile adhesive and grout', '1', 'lot', '96.50'], ['Plumbing labor', '4', 'h', '85']],
    ),
    body='''
<h2>What to put on a contractor invoice</h2>
<p>No federal law prescribes what an invoice must look like, but a complete invoice gets paid faster and holds up if there is a dispute. Include:</p>
<ul>
<li>your business name, address and phone or e-mail, and your license number if your state requires it on your paperwork,</li>
<li>the client's name and billing address, and the job address if it is different,</li>
<li>a unique invoice number and the invoice date,</li>
<li>when the work was done, and a reference to the estimate or contract it belongs to,</li>
<li>each item of labor and materials with quantity, unit price and amount,</li>
<li>the subtotal, any sales tax, deposits already paid and the amount due,</li>
<li>the due date, payment terms and how to pay you.</li>
</ul>

<h2>Sales tax</h2>
<p>Whether you charge sales tax on labor, on materials or on both depends on your state and sometimes on the type of job. Some states tax neither on real property improvements, others tax materials only. Check with your state's revenue department or your accountant, then pick “Add sales tax” in the template and enter your rate.</p>

<h2>Payment terms, deposits and late fees</h2>
<ul>
<li><strong>Terms:</strong> “Due on receipt”, “Net 15” or “Net 30” are the usual choices. A specific due date is clearer than any of them.</li>
<li><strong>Deposits and progress payments:</strong> show what the client has already paid and subtract it, so the amount due is never in question. Some states limit the deposit a home improvement contractor can take.</li>
<li><strong>Late fees:</strong> you can generally only charge them if the client agreed to them beforehand, in the estimate or contract, and some states limit the amount.</li>
<li><strong>Lien rights:</strong> many states give contractors a mechanic's lien for unpaid work, with strict notice and filing deadlines. If a large invoice is going unpaid, check the deadlines in your state early.</li>
</ul>

<h2>Invoicing business clients</h2>
<p>A business that pays you for services may ask you for a Form W-9 and report the payments to the IRS on Form 1099-NEC. For payments made in 2026 the reporting threshold is $2,000 in the year. It was $600 for earlier years. You report all your income either way, so keep your invoices numbered and filed.</p>

<h2>Tips to get paid faster</h2>
<ul>
<li>Send the invoice the day the job is finished.</li>
<li>Describe the work the way the estimate did, so the client recognizes every line.</li>
<li>Offer an easy way to pay. In the Fixbill app you can add your own PayPal or Stripe payment link and the invoice gets a scan-to-pay QR code.</li>
<li>Follow up politely the day after the due date.</li>
</ul>
''',
    fine='This template is general information, not legal or tax advice. Last checked November 2026. Rules differ by '
         'state; when in doubt, ask your accountant.',
    app=dict(
        h2='Invoice from the job site',
        p='With Fixbill the same invoice takes two minutes on your phone, plus what a template cannot do:',
        bullets=['turn a signed estimate into an invoice with one tap (Pro)',
                 'a scan-to-pay QR code for your own PayPal or Stripe payment link',
                 'bank payments matched from your statement (CAMT.053, MT940, CSV) (Pro)',
                 'an alert when an invoice is overdue and a polite reminder with one tap'],
        note='Free for 5 documents a month. Your data stays on your phone.'),
    faq=[
        ('What is the difference between an estimate and an invoice?',
         'An estimate tells the client what the job should cost before you start. An invoice asks for payment for '
         'work you have done. The invoice should match the estimate plus any changes the client approved.'),
        ('Do I need an invoice number?',
         'No law requires one for most small businesses, but a unique number on every invoice makes bookkeeping, '
         'payment references and tax time much easier.'),
        ('Is the template really free?',
         'Yes. The template on this page is free with no limit and what you type never leaves your browser. In the '
         'Fixbill app, 5 documents a month are free.'),
    ],
)

# ------------------------------------------------------------------------------------------------ French invoice

FR_FACTURE = dict(
    id='fr-facture-auto-entrepreneur', lang='fr', html_lang='fr', path='fr/facture-auto-entrepreneur/',
    phrase='facture auto-entrepreneur modèle',
    title='Modèle de facture auto-entrepreneur gratuit, à remplir en ligne | Fixbill',
    desc="Modèle de facture gratuit pour auto-entrepreneur et micro-entrepreneur : mentions obligatoires, mention EI, "
         "TVA non applicable, pénalités de retard. Remplissez-le en ligne et enregistrez-le en PDF.",
    h1='Modèle de facture auto-entrepreneur',
    lede="Remplissez la facture dans votre navigateur, vérifiez l'aperçu et enregistrez-la en PDF ou imprimez-la. Les "
         "mentions obligatoires du micro-entrepreneur sont prévues. Rien n'est envoyé : vos données restent sur votre "
         "appareil.",
    jump='Remplir la facture', crumb='Fixbill',
    card='Modèle de facture auto-entrepreneur', card_text='Facture avec les mentions obligatoires du '
                                                          'micro-entrepreneur, à remplir en ligne et à enregistrer '
                                                          'en PDF.',
    gen=derive(
        FR, kind='invoice', dates=['issue', 'supply', 'due'], pay=['account', 'method', 'terms'], sign=None,
        doc=dict(title='Facture', seller='Émetteur', buyer='Client', total='Net à payer'),
        ui=dict(preview='Aperçu de la facture'),
        groups=[
            ('Votre entreprise', [
                ('s_name', 'Nom et prénom, suivis de « EI »', 'text', 'Camille Martin EI', '', None),
                ('s_addr', 'Adresse', 'area', 'Rue\nCode postal et ville', '', None),
                ('s_ids', 'SIREN ou SIRET', 'area', 'SIRET 123 456 789 00012', '', None),
                ('s_extra', 'Assurance professionnelle (si obligatoire)', 'area',
                 'Assureur, n° de contrat, couverture géographique', '', None),
                ('s_contact', 'Téléphone ou e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Client', [
                ('b_name', 'Nom ou raison sociale', 'text', 'Nom du client', '', None),
                ('b_addr', 'Adresse', 'area', 'Rue\nCode postal et ville', '', None),
                ('b_ids', 'SIREN (client professionnel)', 'text', 'SIREN 987 654 321', '', None),
            ]),
            ('Facture', [
                ('number', 'Numéro', 'text', 'F-2026-001', 'F-2026-001', None),
                ('issue', "Date d'émission", 'date', '', '', 0),
                ('supply', 'Date de la prestation', 'date', '', '', 0),
                ('due', "Date d'échéance", 'date', '', '', 30),
                ('cur', 'Devise', 'sel', '', 'EUR', [('EUR', 'Euro (EUR)'), ('CHF', 'Franc suisse (CHF)')]),
            ]),
            'items',
            ('TVA', [
                ('tax', 'TVA', 'tax', '', '', None),
            ]),
            ('Paiement', [
                ('account', 'IBAN', 'text', 'FR76 0000 0000 0000 0000 0000 000', '', None),
                ('method', 'Mode de paiement', 'text', '', 'Virement bancaire', None),
                ('terms', 'Retard de paiement (clients professionnels)', 'area', '',
                 "En cas de retard de paiement : pénalités au taux de trois fois le taux d'intérêt légal et indemnité "
                 "forfaitaire de 40 € pour frais de recouvrement. Pas d'escompte pour paiement anticipé.", None),
                ('notes', 'Mentions complémentaires', 'area', 'Par exemple : Merci de votre confiance.', '', None),
            ]),
        ],
        tax=[('none', 'Franchise en base (micro-entrepreneur)', 'TVA non applicable, art. 293 B du CGI', ''),
             ('20', 'TVA 20 %', '', ''), ('10', 'TVA 10 %', '', ''), ('5.5', 'TVA 5,5 %', '', '')],
        items=[['Pose de faïence murale', '12', 'm²', '38'], ['Colle et joints', '1', 'forfait', '84,50'],
               ['Frais de déplacement', '1', 'forfait', '30']],
    ),
    body='''
<h2>Les mentions obligatoires de la facture</h2>
<ul>
<li>la date d'émission et un numéro unique, dans une suite chronologique sans trou,</li>
<li>la date de la vente ou de la prestation,</li>
<li>votre nom et prénom précédés ou suivis de la mention « EI » ou « Entrepreneur individuel », votre adresse et votre numéro SIREN ou SIRET,</li>
<li>le nom et l'adresse du client,</li>
<li>la désignation précise de chaque prestation ou produit, la quantité et le prix unitaire hors taxe,</li>
<li>le total à payer et, si vous êtes redevable de la TVA, le taux et le montant de la taxe,</li>
<li>la date d'échéance du paiement et les conditions d'escompte,</li>
<li>pour un client professionnel : le taux des pénalités de retard et l'indemnité forfaitaire de 40 € pour frais de recouvrement,</li>
<li>pour les artisans soumis à une assurance professionnelle obligatoire : les références du contrat, les coordonnées de l'assureur et la couverture géographique.</li>
</ul>

<h2>La mention de TVA en franchise en base</h2>
<p>En franchise en base, vous ne facturez pas de TVA et la facture doit le dire. La formule habituelle est « TVA non applicable, art. 293 B du CGI » ; elle est préremplie dans le modèle quand vous choisissez « Franchise en base ». La TVA est en cours de recodification dans le code des impositions sur les biens et services (CIBS) et la référence légale à citer change en conséquence : vérifiez la formulation en vigueur sur entreprendre.service-public.gouv.fr avant d'envoyer vos premières factures de l'année.</p>
<p>En 2026, la franchise s'applique jusqu'à 37 500 € de chiffre d'affaires pour les prestations de services et 85 000 € pour les ventes. Au-delà, vous facturez la TVA : choisissez alors le taux dans le modèle.</p>

<h2>Facturer un particulier</h2>
<p>Pour une prestation de services à un particulier, une note est obligatoire à partir de 25 € TTC, et en dessous si le client la demande. Les mentions sur les pénalités de retard et l'indemnité de 40 € ne concernent que les clients professionnels : vous pouvez vider ce champ pour un particulier.</p>

<h2>Facture électronique : ce qui change</h2>
<p>Depuis le 1er septembre 2026, toutes les entreprises doivent pouvoir recevoir des factures électroniques. Les micro-entreprises, y compris en franchise en base de TVA, devront en émettre pour leurs clients professionnels établis en France à partir du 1er septembre 2027, en passant par une plateforme agréée. À cette date s'ajoutent aussi de nouvelles mentions, dont le SIREN du client et la nature de l'opération (livraison de biens, prestation de services ou les deux).</p>
<p>Ce modèle produit un PDF ou une impression, pas une facture électronique au sens de cette réforme, et l'application Fixbill non plus. Il reste adapté aux factures adressées aux particuliers, qui ne sont pas concernées par l'obligation.</p>

<h2>Être payé à temps</h2>
<ul>
<li>Indiquez une date d'échéance précise plutôt que « à réception ».</li>
<li>Demandez un acompte à la commande et déduisez-le sur la facture finale.</li>
<li>Reprenez sur la facture les lignes du devis signé : le client les reconnaît tout de suite.</li>
</ul>
''',
    fine="Ce modèle est une aide générale, pas un conseil juridique ou fiscal. État au mois de novembre 2026. En cas de "
         "doute, renseignez-vous auprès de votre chambre de métiers ou de votre comptable.",
    app=dict(
        h2='La facture depuis le chantier',
        p='Avec Fixbill, la même facture est prête en deux minutes sur votre téléphone, avec ce que le papier ne fait '
          'pas :',
        bullets=["votre client signe le devis sur l'écran, puis il devient facture d'un geste (Pro)",
                 'factures avec QR code EPC pour le virement',
                 'rapprochement des paiements à partir de votre relevé bancaire (CAMT.053, MT940, CSV) (Pro)',
                 'alerte en cas de retard de paiement et relance en un geste'],
        note='Gratuit pour 5 documents par mois. Vos données restent sur votre téléphone. Fixbill produit des '
             'factures PDF, pas des factures électroniques.'),
    faq=[
        ('Un auto-entrepreneur doit-il écrire « EI » sur ses factures ?',
         "Oui. La mention « EI » ou « Entrepreneur individuel » doit figurer avant ou après votre nom sur vos "
         "factures et documents professionnels."),
        ('Puis-je envoyer ma facture en PDF par e-mail ?',
         "Oui pour un particulier. Pour les clients professionnels établis en France, les micro-entreprises devront "
         "émettre des factures électroniques via une plateforme agréée à partir du 1er septembre 2027."),
        ('Le modèle est-il vraiment gratuit ?',
         "Oui. Le modèle de cette page est gratuit sans limite et vos données ne quittent pas votre navigateur. Dans "
         "l'application Fixbill, 5 documents par mois sont gratuits."),
    ],
)

# ------------------------------------------------------------------------------------------------ Brazilian quote

PT_ORCAMENTO = dict(
    id='pt-orcamento-servico', lang='pt', html_lang='pt-BR', path='pt/modelo-orcamento-servico/',
    phrase='modelo de orçamento de serviço',
    title='Modelo de orçamento de serviço grátis para preencher online | Fixbill',
    desc='Modelo de orçamento de serviço para autônomos, MEI e prestadores: mão de obra, materiais, prazo, condições '
         'de pagamento e validade. Preencha online e salve em PDF, nada é enviado.',
    h1='Modelo de orçamento de serviço para preencher online',
    lede='Preencha o orçamento no navegador, confira a prévia e salve em PDF ou imprima. O modelo já separa mão de '
         'obra e materiais e tem espaço para prazos, condições de pagamento e a aprovação do cliente. Seus dados ficam '
         'no seu aparelho.',
    jump='Preencher o orçamento', crumb='Fixbill',
    card='Modelo de orçamento de serviço', card_text='Orçamento com mão de obra, materiais, prazo e validade. Preencha '
                                                     'online e salve em PDF.',
    gen=dict(
        kind='estimate', locale='pt-BR', currency='BRL', currencies=['BRL'], decComma=True, refFromNumber=False,
        dates=['issue', 'valid'], pay=['terms'],
        sign=['Assinatura do prestador e data', 'Aprovado pelo cliente: assinatura e data'],
        made='Criado com o Fixbill · deriverge.com/fixbill',
        doc=dict(title='Orçamento', no='nº', seller='Prestador', buyer='Cliente', desc='Descrição', qty='Qtd.',
                 unit='Un.', price='Valor unitário', priceNet='Valor unitário', amount='Total', amountNet='Total',
                 net='Subtotal', tax='Imposto', total='Valor total'),
        ui=dict(items='Serviços e materiais', add='Adicionar item', remove='Remover item',
                desc='Descrição do serviço ou material', qty='Quantidade', unit='Unidade', price='Valor unitário',
                print='Imprimir ou salvar em PDF', reset='Começar de novo',
                resetAsk='Apagar o que você preencheu e voltar ao exemplo?', preview='Prévia do orçamento',
                privacy='Seus dados ficam no navegador (guardados para a próxima visita neste aparelho). Para gerar o '
                        'PDF, escolha “Salvar como PDF” na janela de impressão.',
                noscript='O gerador precisa de JavaScript. O que colocar no orçamento está descrito abaixo.'),
        groups=[
            ('Sua empresa', [
                ('s_name', 'Nome ou razão social', 'text', 'Silva Reformas', '', None),
                ('s_addr', 'Endereço', 'area', 'Rua e número\nCEP, cidade e UF', '', None),
                ('s_ids', 'CNPJ ou CPF', 'text', 'CNPJ 00.000.000/0001-00', '', None),
                ('s_contact', 'Telefone ou e-mail', 'text', 'name@example.com', '', None),
            ]),
            ('Cliente', [
                ('b_name', 'Nome', 'text', 'Nome do cliente', '', None),
                ('b_addr', 'Endereço', 'area', 'Rua e número\nCEP, cidade e UF', '', None),
                ('site', 'Local do serviço (se for outro)', 'area', 'Endereço da obra', '', None),
            ]),
            ('Orçamento', [
                ('number', 'Número', 'text', 'ORC-2026-001', 'ORC-2026-001', None),
                ('issue', 'Data', 'date', '', '', 0),
                ('valid', 'Válido até', 'date', '', '', 10),
                ('start', 'Início e término previstos', 'text', 'Início em 1º de dezembro, término em 5 dias úteis',
                 '', None),
            ]),
            'items',
            ('Condições', [
                ('terms', 'Condições de pagamento', 'text', '',
                 '50% na aprovação e 50% na conclusão, por Pix ou transferência.', None),
                ('notes', 'Observações', 'area', '',
                 'Serviços e materiais não previstos neste orçamento serão orçados à parte e só serão executados '
                 'depois da aprovação do cliente.', None),
            ]),
        ],
        tax=[],
        items=[['Retirada do revestimento antigo e descarte (mão de obra)', '12', 'm²', '25'],
               ['Assentamento de revestimento (mão de obra)', '12', 'm²', '85'],
               ['Argamassa e rejunte (material)', '1', 'un', '180']],
    ),
    body='''
<h2>O que o orçamento de serviço precisa ter</h2>
<p>O Código de Defesa do Consumidor (art. 40) obriga o prestador a entregar ao consumidor um orçamento prévio que discrimine:</p>
<ul>
<li>o valor da mão de obra,</li>
<li>os materiais e equipamentos que serão usados,</li>
<li>as condições de pagamento,</li>
<li>as datas de início e de término do serviço.</li>
</ul>
<p>Além disso, vale colocar os dados da sua empresa (nome, CNPJ ou CPF, telefone), os dados do cliente, o local do serviço, a validade do orçamento e um campo para a aprovação com data e assinatura.</p>

<h2>Validade e aprovação</h2>
<p>Salvo combinação diferente, o orçamento vale por dez dias a contar do recebimento pelo consumidor (art. 40, § 1º). Por isso o modelo já sugere dez dias no campo “Válido até”; se você quiser outro prazo, escreva no orçamento.</p>
<p>Depois de aprovado, o orçamento obriga as duas partes e só pode ser alterado por negociação entre elas (art. 40, § 2º). O consumidor também não responde por acréscimos decorrentes da contratação de terceiros que não estavam previstos (art. 40, § 3º). Na prática: descreva bem o que está incluído, e antes de fazer qualquer serviço extra, mande um novo orçamento e espere a aprovação.</p>

<h2>Por que pedir a aprovação por escrito</h2>
<p>O Código proíbe executar serviços sem orçamento prévio e sem autorização expressa do consumidor (art. 39, VI). Uma assinatura no orçamento, ou um “aprovado” por mensagem guardada, é a sua prova de que o cliente concordou com o serviço e com o preço.</p>

<h2>Orçamento não é nota fiscal</h2>
<p>O orçamento é a proposta. Depois do serviço, a nota fiscal segue as regras do seu município e do seu regime. O MEI que presta serviços emite a NFS-e pelo emissor nacional: a nota é obrigatória quando o cliente é empresa e, para pessoa física, quando o cliente pede. Este modelo e o aplicativo Fixbill não emitem nota fiscal.</p>

<h2>Dicas para fechar mais serviços</h2>
<ul>
<li>Envie o orçamento no mesmo dia da visita.</li>
<li>Ofereça duas opções, por exemplo material padrão e material superior.</li>
<li>Coloque fotos do local para deixar o escopo claro.</li>
<li>Facilite o “sim”: a assinatura na hora vale mais do que um PDF esquecido no celular.</li>
</ul>
''',
    fine='Este modelo é uma ajuda geral e não substitui orientação jurídica ou contábil. Situação em novembro de 2026. '
         'Em caso de dúvida, fale com seu contador ou com o Procon.',
    app=dict(
        h2='Orçamento assinado antes de você sair da obra',
        p='Com o Fixbill, o mesmo orçamento fica pronto em dois minutos no celular, com o que um modelo não faz:',
        bullets=['o cliente assina o orçamento direto na sua tela (Pro)',
                 'itens da sua tabela de preços e fotos do serviço no orçamento (fotos no Pro)',
                 'QR code do seu próprio link de pagamento do PayPal ou Stripe',
                 'aviso de vencimento e lembrete educado com um toque'],
        note='Grátis até 5 documentos por mês. Seus dados ficam no celular.'),
    faq=[
        ('Por quanto tempo vale um orçamento?',
         'Se o orçamento não disser outra coisa, vale por dez dias a contar do recebimento pelo consumidor, conforme '
         'o Código de Defesa do Consumidor. Você pode combinar outro prazo e escrevê-lo no orçamento.'),
        ('Posso cobrar mais do que o valor orçado?',
         'Depois de aprovado, o orçamento só muda por acordo entre você e o cliente. Para um serviço extra, envie um '
         'novo orçamento e espere a aprovação antes de executar.'),
        ('O modelo é grátis mesmo?',
         'Sim. O modelo desta página é grátis, sem limite, e o que você digita não sai do seu navegador. No aplicativo '
         'Fixbill, 5 documentos por mês são grátis.'),
    ],
)

MORE_PAGES = [EN_INVOICE, GB_QUOTE, CS_NABIDKA, SK_FAKTURA, SK_PONUKA, DE_RECHNUNG, FR_FACTURE, PT_ORCAMENTO]
