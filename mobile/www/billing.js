/*
 * Tapkasa — adaptér fakturace (RevenueCat / nativní in-app nákupy).
 *
 * Vystavuje globál window.TapkasaBilling:
 *
 *   getEntitlement(): Promise<'free'|'pro'>   — aktuální úroveň předplatného
 *   purchase(product): Promise<'free'|'pro'>  — koupí 'monthly' | 'yearly'
 *                                               (nebo přímo ID produktu/balíčku)
 *   restore(): Promise<'free'|'pro'>          — obnoví dřívější nákupy
 *
 * Na nativní platformě používá @revenuecat/purchases-capacitor (RevenueCat
 * obaluje StoreKit 2 a Play Billing). V obyčejném prohlížeči, nebo když
 * plugin chybí, všechno tiše vrací 'free' — web zůstává plně funkční.
 *
 * Klíče API (RevenueCat → Project settings → API keys):
 *   iOS     "appl_..."  → REVENUECAT_API_KEY_IOS níže
 *   Android "goog_..."  → REVENUECAT_API_KEY_ANDROID níže
 * Entitlement v RevenueCat se musí jmenovat "pro" a obsahovat oba produkty
 * (měsíční a roční předplatné; ceny určuje obchod a paywall je bere odsud).
 * Balíčky v nabídce (offering) používají standardní identifikátory
 * $rc_monthly a $rc_annual. Zkušební doba se čte z nabídky (trialOf).
 *
 * Pas na akci (od 1.3.0): spotřebovatelný jednorázový nákup
 * tapkasa.pass.event72. Kupuje se přímo přes getProducts + purchaseStoreProduct,
 * takže v nabídce (offering) být nemusí. V RevenueCat (Product catalog →
 * Products) musí mít typ Consumable a NESMÍ být v entitlementu "pro":
 * spotřebovatelný produkt v entitlementu by ho podle RevenueCat odemkl
 * natrvalo. Na Androidu ho SDK po ověření samo spotřebuje (consumeAsync),
 * takže jde koupit znovu; na iOS je typ dán v App Store Connect (CONSUMABLE).
 * Kolik pasů je nevyužitých a kdy který běží, drží aplikace (index.html,
 * state.pass); sem patří jen nákup a seznam transakcí z CustomerInfo
 * (nonSubscriptionTransactions), které aplikaci předává __kasaPass.
 * Po přeinstalaci RevenueCat spotřebované nákupy obvykle nevrátí: má nové
 * anonymní ID, Apple spotřebované nákupy do obnovy nedává a Google Play
 * Billing 8 vrací jen nespotřebované. Co vrátí, aplikace připíše.
 */
(function () {
  "use strict";

  // Veřejné (public) SDK klíče projektu Tapkasa v RevenueCat.
  // Patří do klienta, nejsou to tajemství; secret keys se do aplikace nedávají.
  var REVENUECAT_API_KEY_IOS = "appl_UDkkqtyFetmsKJAMwyFYbSrterz";
  var REVENUECAT_API_KEY_ANDROID = "goog_CQNzyidxRPuTylazpgieisHqyBL";
  var ENTITLEMENT_ID = "pro";
  var PASS_ID = "tapkasa.pass.event72";

  var cap = window.Capacitor;
  var isNative = !!(cap && typeof cap.isNativePlatform === "function" && cap.isNativePlatform());

  // ---- záložní chování na webu -------------------------------------------
  function webFallback() {
    return {
      getEntitlement: function () { return Promise.resolve("free"); },
      purchase: function () { return Promise.resolve("free"); },
      purchasePass: function () { return Promise.resolve(null); },
      restore: function () { return Promise.resolve("free"); }
    };
  }

  if (!isNative) {
    window.TapkasaBilling = webFallback();
    return;
  }

  // Na nativní platformě háčky definujeme vždy. Když se most nepovede,
  // tlačítko koupě řekne skutečnou příčinu; obecná webová hláška by
  // problém jen maskovala (přesně to se stalo v TestFlightu).
  function fail(reason) {
    window.TapkasaBilling = webFallback();
    window.__kasaBillingError = reason;
    window.__kasaBuy = function () {
      // přeložená hláška z aplikace (index.html), technický důvod v závorce
      var msg = typeof window.__kasaT === "function" ? window.__kasaT("billSetupFail") : "Purchase could not be prepared.";
      alert(msg + " (" + reason + ")");
    };
    window.__kasaRestore = window.__kasaBuy;
  }

  // Vestavěný most Capacitoru vystavuje nativní pluginy v Capacitor.Plugins;
  // registerPlugin existuje jen v aplikacích, které si balí @capacitor/core.
  // Na zařízení je k dispozici právě jen Plugins, proto jde první.
  var Purchases = null;
  if (cap.Plugins && cap.Plugins.Purchases) {
    Purchases = cap.Plugins.Purchases;
  } else if (typeof cap.registerPlugin === "function") {
    try { Purchases = cap.registerPlugin("Purchases"); } catch (e) {}
  }
  if (!Purchases) {
    fail("nativní modul Purchases nenalezen; k dispozici: " +
         (cap.Plugins ? Object.keys(cap.Plugins).join(", ") : "žádné pluginy"));
    return;
  }

  var configured = null; // Promise — konfigurace proběhne jen jednou

  function apiKey() {
    var platform = typeof cap.getPlatform === "function" ? cap.getPlatform() : "";
    return platform === "android" ? REVENUECAT_API_KEY_ANDROID : REVENUECAT_API_KEY_IOS;
  }

  // Volání pluginu nemusí vrátit příslib: vestavěný most Capacitoru u metod
  // bez návratové hodnoty (configure) vrací undefined. Vše proto balíme do
  // Promise.resolve, ať se na výsledek dá vždycky navázat .then.
  function call(method, args) {
    try {
      return Promise.resolve(Purchases[method](args));
    } catch (e) {
      return Promise.reject(e);
    }
  }

  function ensureConfigured() {
    if (!configured) {
      configured = call("configure", { apiKey: apiKey() });
    }
    return configured;
  }

  // Odpovědi pluginu se mezi verzemi liší v obalu ({customerInfo} vs. přímo
  // objekt) — bereme obojí.
  function unwrapInfo(res) {
    return (res && res.customerInfo) || res || {};
  }

  function levelOf(info) {
    var active = info && info.entitlements && info.entitlements.active;
    return active && active[ENTITLEMENT_ID] ? "pro" : "free";
  }

  // CustomerInfo, nebo null (offline apod.: stav v aplikaci nechat být)
  function getInfo() {
    return ensureConfigured()
      .then(function () { return call("getCustomerInfo"); })
      .then(function (res) { return unwrapInfo(res); })
      .catch(function () { return null; });
  }

  function getEntitlement() {
    return getInfo().then(function (info) { return info ? levelOf(info) : null; });
  }

  // ---- pas na akci ----------------------------------------------------------
  // Transakce pasu z CustomerInfo: [{id, t}] (id = transactionIdentifier).
  function passTx(info) {
    var list = (info && info.nonSubscriptionTransactions) || [];
    var out = [];
    for (var i = 0; i < list.length; i++) {
      var x = list[i] || {};
      if (x.productIdentifier !== PASS_ID || !x.transactionIdentifier) { continue; }
      var t = Date.parse(x.purchaseDate || "");
      out.push({ id: String(x.transactionIdentifier), t: isNaN(t) ? 0 : t });
    }
    return out;
  }

  // Předá aplikaci transakce pasu. buy = id právě koupené transakce.
  // at = čas serveru RevenueCat (requestDate), aplikace podle něj hlídá hodiny.
  function pushPass(info, src, buyTx) {
    if (typeof window.__kasaPass !== "function" || !info) { return; }
    var tx = passTx(info);
    var buy = buyTx && buyTx.transactionIdentifier ? String(buyTx.transactionIdentifier) : "";
    if (buy && !tx.some(function (x) { return x.id === buy; })) { tx.push({ id: buy, t: Date.now() }); }
    var at = Date.parse(info.requestDate || "");
    try { window.__kasaPass({ tx: tx, src: src, buy: buy || null, at: isNaN(at) ? null : at }); } catch (e) {}
  }

  var passProduct = null;   // StoreProduct z getProducts, platí celé sezení
  function getPassProduct() {
    if (passProduct) { return Promise.resolve(passProduct); }
    return ensureConfigured()
      .then(function () { return call("getProducts", { productIdentifiers: [PASS_ID], type: "NON_SUBSCRIPTION" }); })
      .then(function (res) {
        var list = (res && res.products) || (Array.isArray(res) ? res : []);
        for (var i = 0; i < list.length; i++) {
          if (list[i] && list[i].identifier === PASS_ID) { passProduct = list[i]; return passProduct; }
        }
        throw new Error("Tapkasa: pas '" + PASS_ID + "' není v nabídce");
      });
  }

  // Nákup pasu: {info, tx} z obchodu. Chyby (i zrušení) jdou k volajícímu.
  function purchasePass() {
    return getPassProduct()
      .then(function (p) { return call("purchaseStoreProduct", { product: p }); })
      .then(function (res) { return { info: unwrapInfo(res), tx: (res && res.transaction) || null }; });
  }

  function findPackage(offering, product) {
    if (!offering || !Array.isArray(offering.availablePackages)) { return null; }
    var wanted = {
      monthly: "$rc_monthly",
      yearly: "$rc_annual",
      annual: "$rc_annual"
    }[product] || product;
    for (var i = 0; i < offering.availablePackages.length; i++) {
      var p = offering.availablePackages[i];
      if (p.identifier === wanted) { return p; }
      if (p.product && p.product.identifier === wanted) { return p; }
    }
    return null;
  }

  function purchase(product) {
    return ensureConfigured()
      .then(function () { return call("getOfferings"); })
      .then(function (res) {
        var current = (res && res.current) || null;
        var pkg = findPackage(current, product);
        if (!pkg) { throw new Error("Tapkasa: balíček '" + product + "' není v nabídce"); }
        return call("purchasePackage", { aPackage: pkg });
      })
      .then(function (res) { return levelOf(unwrapInfo(res)); });
      // Chybu (i zrušení nákupu uživatelem) necháváme doběhnout k volajícímu,
      // ať může ukázat vlastní hlášku; zrušení má userCancelled=true.
  }

  function restore() {
    return ensureConfigured()
      .then(function () { return call("restorePurchases"); })
      .then(function (res) {
        var info = unwrapInfo(res);
        pushPass(info, "restore");
        return levelOf(info);
      });
  }

  window.TapkasaBilling = {
    getEntitlement: getEntitlement,
    purchase: purchase,
    purchasePass: purchasePass,
    restore: restore
  };

  // ---- napojení na hooky aplikace ----------------------------------------
  // Aplikace (tapkasa/index.html) volá __kasaBuy/__kasaRestore a výsledek čeká
  // přes __kasaEntitlement('pro'|'free'); ceníky čte z __KASA_PRICES__.
  // Null (offline, neznámo) se nepředává — jinak by start bez signálu
  // smazal platné předplatné.

  // src říká aplikaci, odkud stav přišel: "buy" a "restore" zavřou paywall
  // a ukážou potvrzení, "start" jen tiše srovná uložený stav.
  function push(level, src) {
    if (level !== "pro" && level !== "free") { return; }
    if (typeof window.__kasaEntitlement === "function") {
      try { window.__kasaEntitlement(level, src || "start"); } catch (e) {}
    }
  }

  // Obchod už nákup potvrdil, ale entitlement se ještě nepropsal: zeptáme se
  // znovu, ať uživatel nezůstane na paywallu se zaplaceným předplatným.
  function settle(level, src) {
    if (level === "pro") { push("pro", src); return; }
    var tries = 0;
    (function again() {
      tries += 1;
      setTimeout(function () {
        getEntitlement().then(function (l) {
          if (l === "pro" || tries >= 4) { push(l || "free", src); } else { again(); }
        });
      }, 1500);
    })();
  }

  // StoreKit: "Tuto položku už máte předplacenou" (RevenueCat kód 6).
  // Jen podle kódu: dřív stačilo slovo "already" v jakékoli hlášce (třeba
  // "operace už probíhá" při dvojím ťuknutí) a spouštěla se obnova.
  function isAlreadyOwned(e) {
    return !!(e && e.code !== undefined && String(e.code) === "6");
  }

  function isCancel(e) {
    return !!(e && (e.userCancelled === true || (e.code !== undefined && String(e.code) === "1")));
  }

  // Chyba nákupu či obnovy se ukáže přeloženě v aplikaci (index.html);
  // alert s holou hláškou SDK zůstává jen pro případ, že hook chybí.
  function reportFail(kind, e) {
    var code = e && e.code !== undefined ? String(e.code) : "";
    var raw = String(e && e.message || e || "");
    if (typeof window.__kasaBillingFail === "function") {
      try { window.__kasaBillingFail(kind, code, raw); return; } catch (x) {}
    }
    var t = typeof window.__kasaT === "function" ? window.__kasaT("billFail", code || "?") : "";
    alert(t || (raw + (code ? " [" + code + "]" : "")));
  }

  // Dvojí ťuknutí na tarif dřív spustilo druhý nákup, který obchod odmítl
  // a kód ho vyložil jako "už zaplaceno".
  var busy = false;

  window.__kasaBuy = function (plan) {
    if (busy) { return; }
    busy = true;
    purchase(plan === "yearly" ? "yearly" : "monthly")
      .then(function (level) { busy = false; settle(level, "buy"); })
      .catch(function (e) {
        if (isCancel(e)) { busy = false; return; }
        if (isAlreadyOwned(e)) {
          restore()
            .then(function (level) { busy = false; settle(level, "restore"); })
            .catch(function (e2) { busy = false; reportFail("restore", e2); });
          return;
        }
        busy = false;
        reportFail(/není v nabídce/.test(String(e && e.message || "")) ? "offering" : "buy", e);
      });
  };

  // Pas na akci: kupuje se kdykoli znovu (spotřebovatelný nákup).
  window.__kasaBuyPass = function () {
    if (busy) { return; }
    busy = true;
    purchasePass()
      .then(function (r) { busy = false; pushPass(r.info, "buy", r.tx); })
      .catch(function (e) {
        busy = false;
        if (isCancel(e)) { return; }
        // Android: předchozí nákup pasu zůstal nespotřebovaný (aplikace
        // spadla uprostřed). Obnova ho zpracuje a aplikace ho připíše.
        if (isAlreadyOwned(e)) {
          busy = true;
          restore()
            .then(function () { busy = false; })
            .catch(function (e2) { busy = false; reportFail("pass", e2); });
          return;
        }
        reportFail(/není v nabídce/.test(String(e && e.message || "")) ? "offering" : "pass", e);
      });
  };

  window.__kasaRestore = function () {
    if (busy) { return; }
    busy = true;
    restore()
      .then(function (level) { busy = false; push(level, "restore"); })
      .catch(function (e) { busy = false; reportFail("restore", e); });
  };

  // Po startu: skutečný stav předplatného, pasy z RevenueCat a ceny v měně
  // obchodu. Návrat do popředí stav srovná znovu (nejvýš jednou za minutu):
  // pas schválený později (rodič, platba v hotovosti) se tak připíše bez
  // restartu aplikace.
  var syncedAt = 0;
  function syncInfo() {
    syncedAt = Date.now();
    getInfo().then(function (info) {
      if (!info) { return; }
      push(levelOf(info), "start");
      pushPass(info, "start");
    });
  }
  syncInfo();
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible" && Date.now() - syncedAt > 60000) { syncInfo(); }
  });

  // Ceny z obchodu. Po startu bez signálu se dřív už nenačetly a paywall
  // celé sezení ukazoval náhradní dolarové ceny; aplikace si je teď při
  // otevření paywallu vyžádá znovu (window.__kasaLoadPrices).
  var pricesLoading = false;
  function loadPrices() {
    if (pricesLoading) { return; }
    pricesLoading = true;
    // cena pasu z obchodu (priceString), nezávisle na nabídce předplatného
    getPassProduct()
      .then(function (p) {
        var ps = p && (p.priceString || p.price_string) || "";
        if (!ps) { return; }
        window.__KASA_PRICES__ = window.__KASA_PRICES__ || {};
        window.__KASA_PRICES__.pass = ps;
        if (typeof window.__kasaPricesChanged === "function") {
          try { window.__kasaPricesChanged(); } catch (e) {}
        }
      })
      .catch(function () {});
    ensureConfigured()
      .then(function () { return call("getOfferings"); })
      .then(function (res) {
        pricesLoading = false;
        var current = (res && res.current) || null;
        var monthly = findPackage(current, "monthly");
        var yearly = findPackage(current, "yearly");
        var ps = function (p) {
          return p && p.product && (p.product.priceString || p.product.price_string) || "";
        };
        var prices = { monthly: ps(monthly), yearly: ps(yearly), monthlyTrial: null, yearlyTrial: null };
        if (!prices.monthly && !prices.yearly) { return; }
        var publish = function () {
          var had = window.__KASA_PRICES__ || {};
          if (had.pass && !prices.pass) { prices.pass = had.pass; }
          window.__KASA_PRICES__ = prices;
          if (typeof window.__kasaPricesChanged === "function") {
            try { window.__kasaPricesChanged(); } catch (e) {}
          }
        };
        // Zkušební doba zdarma se na paywallu ukáže, jen když na ni má
        // uživatel nárok (pravidlo 3.1.2: délka zkoušky a cena po ní).
        var mt = trialOf(monthly), yt = trialOf(yearly);
        var isAndroid = typeof cap.getPlatform === "function" && cap.getPlatform() === "android";
        if (isAndroid || (!mt && !yt)) {
          // Google Play vrací jen nabídky, na které má uživatel nárok;
          // defaultOption je ta, kterou purchasePackage koupí.
          prices.monthlyTrial = mt;
          prices.yearlyTrial = yt;
          publish();
          return;
        }
        // iOS: nárok potvrdí StoreKit. Neznámý stav = bez zkoušky, ať
        // paywall neslibuje něco, co obchod nakonec nedá.
        publish();
        var ids = [];
        if (mt) { ids.push(mt.product); }
        if (yt) { ids.push(yt.product); }
        call("checkTrialOrIntroductoryPriceEligibility", { productIdentifiers: ids })
          .then(function (res) {
            var map = (res && res.eligibility) || res || {};
            var ok = function (t) {
              var e = t && map[t.product];
              return !!(e && Number(e.status) === 2);   // INTRO_ELIGIBILITY_STATUS_ELIGIBLE
            };
            prices.monthlyTrial = ok(mt) ? mt : null;
            prices.yearlyTrial = ok(yt) ? yt : null;
            if (prices.monthlyTrial || prices.yearlyTrial) { publish(); }
          })
          .catch(function () {});
      })
      .catch(function () { pricesLoading = false; });
  }

  // Zkušební doba zdarma u balíčku: {n, unit: "DAY"|"MONTH", product} nebo null.
  // Google Play: fáze zdarma ve výchozí nabídce. App Store: úvodní cena 0.
  function trialOf(pkg) {
    var p = pkg && pkg.product;
    if (!p) { return null; }
    var norm = function (unit, n) {
      unit = String(unit || "").toUpperCase();
      n = Number(n) || 0;
      if (n <= 0) { return null; }
      if (unit === "DAY") { return { n: n, unit: "DAY", product: p.identifier }; }
      if (unit === "WEEK") { return { n: n * 7, unit: "DAY", product: p.identifier }; }
      if (unit === "MONTH") { return { n: n, unit: "MONTH", product: p.identifier }; }
      if (unit === "YEAR") { return { n: n * 12, unit: "MONTH", product: p.identifier }; }
      return null;
    };
    var opt = p.defaultOption;
    if (opt && opt.freePhase && opt.freePhase.billingPeriod) {
      var bp = opt.freePhase.billingPeriod;
      return norm(bp.unit, (bp.value || 0) * (opt.freePhase.billingCycleCount || 1));
    }
    var ip = p.introPrice;
    if (ip && Number(ip.price) === 0) {
      return norm(ip.periodUnit, (ip.periodNumberOfUnits || 0) * (ip.cycles || 1));
    }
    return null;
  }
  window.__kasaLoadPrices = loadPrices;
  loadPrices();
})();
