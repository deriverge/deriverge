# Zásady ochrany soukromí, Tapkasa

**Účinnost od:** [DOPLŇ: datum zveřejnění]
**Provozovatel aplikace:** [DOPLŇ: jméno / název provozovatele a adresa]
**Kontakt:** [DOPLŇ: e-mail podpory]

Tapkasa je pokladní aplikace pro zaznamenávání prodeje na stáncích a akcích.
Tyto zásady popisují úplně a pravdivě, jak aplikace nakládá s daty. Krátká
verze: **žádné účty, žádná analytika, žádné reklamy, žádné sledování.
Prodejní data zůstávají ve vašem zařízení.**

## 1. Co aplikace neshromažďuje

- Nevyžaduje ani neumožňuje založení účtu. Nezná vaše jméno, e-mail ani
  telefonní číslo.
- Neobsahuje žádné analytické, reklamní ani marketingové nástroje třetích
  stran a nesbírá statistiky používání.
- Nezjišťuje polohu, nepřistupuje ke kontaktům, fotografiím ani jiným datům
  v zařízení.
- Nezpracovává platby ani platební údaje. Hotovost a platby kartou přijímáte
  mimo aplikaci (kartu na vlastním platebním terminálu); Tapkasa prodej pouze
  zaznamená. Údaje o platebních kartách vašich zákazníků aplikací nikdy
  neprocházejí.
- Nezaznamenává žádné údaje o vašich zákaznících. Účtenka v aplikaci obsahuje
  jen názvy položek, počty kusů, ceny, způsob platby (hotově/kartou) a čas.

## 2. Data uložená ve vašem zařízení

Aplikace ukládá výhradně do úložiště vašeho zařízení:

- váš seznam položek s cenami a barvami, název akce a nastavení,
- uložené účtenky, frontu objednávek a archiv uzavřených akcí.

Tato data se nikam neodesílají (jedinou výjimkou je volitelné párování,
viz bod 3). Držíme je ve více kopiích v úložišti aplikace, aby je restart
nebo vybitá baterie nezničily. Máte je plně pod kontrolou:

- **Smazání:** položky a účtenky lze mazat přímo v aplikaci; odinstalování
  aplikace smaže všechna její data trvale.
- **Záloha:** funkce „Záloha dat“ zobrazí obsah kasy jako text, který si sami
  zkopírujete, kam chcete. Kam zálohu uložíte, je jen na vás; provozovatel
  k ní nemá přístup.

## 3. Volitelné párování dvou zařízení

Můžete spárovat dvě vlastní zařízení (role „kasa“ a „výdej“), aby sdílela
frontu objednávek. Párování je **vypnuté, dokud ho sami nezapnete** vytvořením
nebo zadáním párovacího kódu.

Při zapnutém párování si zařízení posílají **jen obsah objednávek**: názvy
položek, ceny, počty kusů, čísla objednávek, celkové částky, způsob platby
(hotově/kartou), stav vydání, časové značky a název akce. Zprávy dále nesou
náhodně vygenerovaný párovací kód a náhodný identifikátor relace zařízení.
**Neobsahují žádné osobní údaje**, žádná jména, kontakty, polohu ani údaje
o zákaznících.

Zprávy putují šifrovaným spojením (HTTPS) přes přeposílací (relay) server,
který je doručí druhému zařízení. Přeposílací server zprávy krátkodobě
uchovává, aby je druhé zařízení stihlo vyzvednout i po výpadku spojení, **nejdéle 12 hodin**, poté jsou smazány. Provozovatel aplikace zprávy nečte,
neukládá ani k nim nemá přístup. Párování kdykoli ukončíte tlačítkem
„Odpojit“; od té chvíle se nic neodesílá.

## 4. Předplatné Tapkasa Pro

Předplatné se sjednává a účtuje výhradně přes **Apple App Store** nebo
**Google Play** podle platformy. Platební údaje (číslo karty apod.)
zpracovává Apple, resp. Google podle vlastních zásad ochrany soukromí;
provozovatel Tapkasy je nikdy nevidí.

K ověření, zda je předplatné aktivní, aplikace používá službu
**RevenueCat** (RevenueCat, Inc.), která zpracovává potvrzení o nákupu
z App Store / Google Play spolu s **náhodným, anonymním identifikátorem
vygenerovaným aplikací**. Tento identifikátor není spojen s vaším jménem,
e-mailem ani jiným údajem o vaší osobě. RevenueCat vystupuje jako
zpracovatel; jeho zásady: https://www.revenuecat.com/privacy

## 5. Právní základ a vaše práva (GDPR)

Aplikace je navržena tak, aby provozovatel žádné osobní údaje uživatelů
neshromažďoval. Prodejní data existují jen ve vašem zařízení, kde je sami
spravujete a mažete, tím jsou práva na přístup, opravu i výmaz naplněna
přímo ve vašich rukou. Jediné údaje zpracovávané mimo zařízení jsou:

- přechodné zprávy párování (bod 3), bez osobních údajů, smazané do 12 hodin;
  právní základ: plnění smlouvy (poskytnutí funkce, kterou jste si zapnuli),
- anonymní identifikátor a potvrzení nákupu pro ověření předplatného (bod 4);
  právní základ: plnění smlouvy.

S dotazem nebo žádostí týkající se soukromí se obraťte na
[DOPLŇ: e-mail podpory]. Máte rovněž právo podat stížnost u dozorového
úřadu, v ČR je jím Úřad pro ochranu osobních údajů (www.uoou.gov.cz).

## 6. Děti

Aplikace je pracovní nástroj pro prodejce a není určena dětem. Žádná data
o uživatelích v žádném věku neshromažďuje.

## 7. Změny těchto zásad

Při změně funkcí, které by se dotkly nakládání s daty, tyto zásady
aktualizujeme a změníme datum účinnosti. Aktuální znění je vždy dostupné na
[DOPLŇ: URL zveřejněných zásad].
