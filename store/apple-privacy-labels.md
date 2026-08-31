# App Store Connect — „App Privacy" (Privacy Nutrition Labels)

Přesné odpovědi pro dotazník App Store Connect → App → App Privacy.
Vyplňuje se před prvním odesláním k recenzi; bez něj nejde odeslat build.

## Výchozí fakta (z čeho odpovědi vycházejí)

1. Aplikace nemá účty, analytiku, reklamy ani sledování.
2. Prodejní data (položky, účtenky, archiv) zůstávají jen v zařízení —
   podle definice Apple se „nesbírají" (nejsou odesílána mimo zařízení).
3. Předplatné: RevenueCat SDK odesílá potvrzení o nákupu a **anonymní,
   aplikací vygenerovaný identifikátor uživatele** → to JE sběr dat
   (Purchases + Identifiers) a musí být deklarován.
4. Párování: obsah objednávek jde přes relay server; zprávy neobsahují
   osobní údaje, nejsou spojeny s identitou, provozovatel k nim nemá
   přístup a relay je maže nejdéle do 12 h. Uchování slouží výhradně
   k doručení zprávy druhému zařízení (= „to service the request"),
   proto to podle definice Apple nedeklarujeme jako sběr — viz
   zdůvodnění na konci souboru.

---

## Krok 1 — úvodní otázka

> **Do you or your third-party partners collect data from this app?**

**Odpověď: Yes** (kvůli RevenueCat — Purchases a Identifiers).

## Krok 2 — typy dat (zaškrtnout právě tyto)

| Kategorie | Typ dat | Sbírá se? |
|---|---|---|
| Contact Info | Name / Email / Phone / Address / Other | **Ne** |
| Health & Fitness | vše | **Ne** |
| Financial Info | Payment Info / Credit Info / Other | **Ne** (aplikace platby nezpracovává; nákup předplatného spadá pod Purchases níže) |
| Location | Precise / Coarse | **Ne** |
| Sensitive Info | — | **Ne** |
| Contacts | — | **Ne** |
| User Content | vše (Photos, Audio, Customer Support, Other…) | **Ne** |
| Browsing History | — | **Ne** |
| Search History | — | **Ne** |
| Identifiers | **User ID** | **ANO** |
| Identifiers | Device ID | **Ne** (RevenueCat se konfiguruje bez IDFA/IDFV sběru; neověřovat slepě — viz poznámka pod tabulkou) |
| Purchases | **Purchase History** | **ANO** |
| Usage Data | Product Interaction / Advertising Data / Other | **Ne** |
| Diagnostics | Crash Data / Performance Data / Other | **Ne** (žádný crash-reporting SDK) |
| Other Data | — | **Ne** |

> Poznámka k Device ID: v konfiguraci RevenueCat SDK ponechat výchozí
> anonymní App User ID a nesbírat IDFA (žádný AppTrackingTransparency).
> Pokud by se do buildu přidal jiný SDK, tabulku přehodnotit.

## Krok 3 — detail pro **Purchases → Purchase History**

- **Usage (k čemu):** zaškrtnout pouze **App Functionality**
  (ověření nároku na Tapkasa Pro).
  - Analytics: Ne · Product Personalization: Ne · Advertising: Ne · Other: Ne
- **Are the purchase history data linked to the user's identity?** → **No**
  (identifikátor je náhodný, bez vazby na jméno/e-mail/účet — účty neexistují).
- **Do you or your third-party partners use purchase history for tracking
  purposes?** → **No**.

## Krok 4 — detail pro **Identifiers → User ID**

- **Usage:** pouze **App Functionality** (anonymní RevenueCat App User ID
  pro obnovení a ověření předplatného).
- **Linked to the user's identity?** → **No**.
- **Used for tracking?** → **No**.

## Krok 5 — výsledný štítek

Na produktové stránce se zobrazí:

> **Data Not Linked to You:** Purchases, Identifiers

Nic v sekcích „Data Linked to You" ani „Data Used to Track You".

## Privacy manifest (technická poznámka pro build, mimo dotazník)

Xcode 15+ vyžaduje `PrivacyInfo.xcprivacy`. RevenueCat SDK (od v4.26)
dodává vlastní manifest; v manifestu aplikace deklarovat použití
`NSPrivacyAccessedAPICategoryUserDefaults` s důvodem `CA92.1`
(ukládání vlastních dat aplikace) — localStorage/WebView úložiště se
nedeklaruje, ale UserDefaults používá nativní obal. Tracking domains:
žádné.

---

## Zdůvodnění: proč se párování nedeklaruje jako „sběr dat"

Definice Apple (App privacy details on the App Store): data se „sbírají",
pokud jsou odesílána mimo zařízení **a** jsou přístupná vývojáři nebo
partnerům **déle, než je nezbytné k obsloužení daného požadavku v reálném
čase**. Zprávy párování:

- neobsahují osobní údaje ani identifikátory spojitelné s osobou
  (názvy zboží, počty, ceny, čísla objednávek, časy, náhodný kód),
- relay je drží jen po dobu potřebnou k doručení druhému zařízení
  (max. 12 h kvůli výpadkům spojení), pak jsou smazány,
- provozovatel aplikace k nim nemá přístup a nijak je nevyužívá.

Konzervativní alternativa, pokud by recenzent trval na deklaraci:
přidat **Other Data → Other Data Types**, Usage = App Functionality,
Linked = No, Tracking = No, s vysvětlením v Review Notes. Štítek by se
rozšířil, ale zůstal v „Data Not Linked to You".
