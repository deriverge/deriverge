# Play Console, formulář „Data safety" (Bezpečnost údajů)

Přesné odpovědi pro Play Console → App content → Data safety.
Bez vyplnění nejde publikovat. Odpovědi odpovídají skutečnému chování
aplikace: žádné účty, žádná analytika, žádné reklamy; jediný sběr dat je
ověření předplatného přes RevenueCat (potvrzení nákupu + anonymní,
aplikací vygenerovaný identifikátor). Párovací zprávy neobsahují osobní
údaje, relay je maže do 12 h a vývojář k nim nemá přístup, nespadají do
žádného z typů uživatelských dat formuláře (podrobně na konci souboru).

---

## Sekce „Data collection and security"

| Otázka | Odpověď |
|---|---|
| Does your app collect or share any of the required user data types? | **Yes** |
| Is all of the user data collected by your app encrypted in transit? | **Yes** (HTTPS všude, RevenueCat i relay) |
| Which of the following methods of account creation does your app support? | **My app does not allow users to create an account** |
| Do you provide a way for users to request that their data is deleted? | **Yes** → uvést kontakt/URL: [DOPLŇ: e-mail podpory nebo URL formuláře]. (Smazání anonymního identifikátoru a historie nákupů u RevenueCat na žádost; lokální data maže uživatel sám odinstalováním.) |

## Sekce „Data types", co zaškrtnout

Zaškrtnout **pouze** tyto dva typy; všechny ostatní (Location, Personal
info, Financial info, *Payment info*, Health, Messages, Photos, Audio,
Files, Calendar, Contacts, App activity, Web browsing, App info and
performance…) ponechat **nezaškrtnuté**.

### 1) Financial info → **Purchase history**

| Otázka | Odpověď |
|---|---|
| Is this data collected, shared, or both? | **Collected** (ne shared, RevenueCat je poskytovatel služby zpracovávající data jménem vývojáře, což se podle definice Play za „sharing" nepovažuje) |
| Is this data processed ephemerally? | **No** |
| Is this data required for your app, or can users choose whether it's collected? | **Users can choose whether this data is collected** (vzniká jen při nákupu předplatného, které je dobrovolné) |
| Why is this user data collected? | **App functionality** (ověření a obnovení nároku Tapkasa Pro), nic jiného |

### 2) Device or other IDs → **Device or other IDs**

| Otázka | Odpověď |
|---|---|
| Is this data collected, shared, or both? | **Collected** |
| Is this data processed ephemerally? | **No** |
| Required or optional? | **Data collection is required** (anonymní App User ID vzniká při startu SDK, uživatel jej nemůže vypnout) |
| Why is this user data collected? | **App functionality**, nic jiného |

> Pozn.: jde o náhodný identifikátor vygenerovaný aplikací (RevenueCat
> anonymous App User ID), ne o Advertising ID. Aplikace **nesmí** mít
> v manifestu oprávnění `com.google.android.gms.permission.AD_ID`
> (zkontrolovat výsledný merged manifest, některé SDK ho přidávají).

## Sekce „Data usage and handling", souhrn pro kontrolu

Výsledná karta v obchodě má vypadat takto:

- **Data shared with third parties:** No data shared
- **Data collected:** Financial info (Purchase history), Device or other IDs
- „Data is encrypted in transit" ✓
- „You can request that data be deleted" ✓

## Nezávislý bezpečnostní audit

| Otázka | Odpověď |
|---|---|
| Has your app undergone an independent security review? | **No** |

---

## Zdůvodnění: proč párovací zprávy nejsou ve formuláři

Formulář Data safety se ptá na **uživatelská data** (data o uživateli
nebo z jeho zařízení, která opouštějí zařízení a jsou vývojáři či třetím
stranám přístupná). Zprávy párování obsahují jen obsah objednávek
(názvy položek, počty, ceny, čísla objednávek, časy, náhodný párovací
kód), nic z toho není o uživateli ani o jeho identitě, vývojář k nim
přístup nemá a relay je po doručení (nejdéle 12 h) maže. Google navíc
z formuláře výslovně vyjímá přenosy, které jsou nezbytné k poskytnutí
funkce vyžádané uživatelem a zpracovávají se pomíjivě (ephemeral
processing). Kdyby recenze Play přesto deklaraci vyžadovala,
konzervativní volba je: **App activity → Other user-generated content**,
Collected, Processed ephemerally: **Yes**, Optional (párování je
volitelné), Purpose: App functionality.

## Konzistence

Odpovědi musí souhlasit se zásadami ochrany soukromí
(`store/privacy-policy-cs.md` / `-en.md`) a se štítky Apple
(`store/apple-privacy-labels.md`), všechny tři dokumenty deklarují
stejné dva sběry (historie nákupů + anonymní identifikátor) a nic víc.
Při přidání jakéhokoli SDK (crash reporting, analytika…) je nutné
aktualizovat všechny tři současně.
