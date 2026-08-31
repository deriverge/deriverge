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
 * (měsíční 4,99 USD, roční 39,99 USD). Balíčky v nabídce (offering) používají
 * standardní identifikátory $rc_monthly a $rc_annual.
 */
(function () {
  "use strict";

  // Veřejné (public) SDK klíče projektu Tapkasa v RevenueCat.
  // Patří do klienta, nejsou to tajemství; secret keys se do aplikace nedávají.
  var REVENUECAT_API_KEY_IOS = "appl_UDkkqtyFetmsKJAMwyFYbSrterz";
  var REVENUECAT_API_KEY_ANDROID = "goog_CQNzyidxRPuTylazpgieisHqyBL";
  var ENTITLEMENT_ID = "pro";

  var cap = window.Capacitor;
  var isNative = !!(cap && typeof cap.isNativePlatform === "function" && cap.isNativePlatform());

  // ---- záložní chování na webu -------------------------------------------
  function webFallback() {
    return {
      getEntitlement: function () { return Promise.resolve("free"); },
      purchase: function () { return Promise.resolve("free"); },
      restore: function () { return Promise.resolve("free"); }
    };
  }

  if (!isNative || typeof cap.registerPlugin !== "function") {
    window.TapkasaBilling = webFallback();
    return;
  }

  var Purchases;
  try {
    Purchases = cap.registerPlugin("Purchases");
  } catch (e) {
    window.TapkasaBilling = webFallback();
    return;
  }

  var configured = null; // Promise — konfigurace proběhne jen jednou

  function apiKey() {
    var platform = typeof cap.getPlatform === "function" ? cap.getPlatform() : "";
    return platform === "android" ? REVENUECAT_API_KEY_ANDROID : REVENUECAT_API_KEY_IOS;
  }

  function ensureConfigured() {
    if (!configured) {
      configured = Purchases.configure({ apiKey: apiKey() });
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

  function getEntitlement() {
    return ensureConfigured()
      .then(function () { return Purchases.getCustomerInfo(); })
      .then(function (res) { return levelOf(unwrapInfo(res)); })
      .catch(function () { return null; }); // offline apod. — stav v aplikaci nechat být
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
      .then(function () { return Purchases.getOfferings(); })
      .then(function (res) {
        var current = (res && res.current) || null;
        var pkg = findPackage(current, product);
        if (!pkg) { throw new Error("Tapkasa: balíček '" + product + "' není v nabídce"); }
        return Purchases.purchasePackage({ aPackage: pkg });
      })
      .then(function (res) { return levelOf(unwrapInfo(res)); });
      // Chybu (i zrušení nákupu uživatelem) necháváme doběhnout k volajícímu,
      // ať může ukázat vlastní hlášku; zrušení má userCancelled=true.
  }

  function restore() {
    return ensureConfigured()
      .then(function () { return Purchases.restorePurchases(); })
      .then(function (res) { return levelOf(unwrapInfo(res)); });
  }

  window.TapkasaBilling = {
    getEntitlement: getEntitlement,
    purchase: purchase,
    restore: restore
  };

  // ---- napojení na hooky aplikace ----------------------------------------
  // Aplikace (tapkasa/index.html) volá __kasaBuy/__kasaRestore a výsledek čeká
  // přes __kasaEntitlement('pro'|'free'); ceníky čte z __KASA_PRICES__.
  // Null (offline, neznámo) se nepředává — jinak by start bez signálu
  // smazal platné předplatné.

  function push(level) {
    if (level !== "pro" && level !== "free") { return; }
    if (typeof window.__kasaEntitlement === "function") {
      try { window.__kasaEntitlement(level); } catch (e) {}
    }
  }

  function isCancel(e) {
    return !!(e && (e.userCancelled === true ||
      (e.code !== undefined && String(e.code) === "1") ||
      /cancel/i.test(String(e && e.message || ""))));
  }

  window.__kasaBuy = function (plan) {
    purchase(plan === "yearly" ? "yearly" : "monthly")
      .then(push)
      .catch(function (e) {
        if (!isCancel(e)) { alert(String(e && e.message || e)); }
      });
  };

  window.__kasaRestore = function () {
    restore()
      .then(push)
      .catch(function (e) { alert(String(e && e.message || e)); });
  };

  // Po startu: skutečný stav předplatného + ceny v měně obchodu.
  getEntitlement().then(push);

  ensureConfigured()
    .then(function () { return Purchases.getOfferings(); })
    .then(function (res) {
      var current = (res && res.current) || null;
      var monthly = findPackage(current, "monthly");
      var yearly = findPackage(current, "yearly");
      var ps = function (p) {
        return p && p.product && (p.product.priceString || p.product.price_string) || "";
      };
      var prices = { monthly: ps(monthly), yearly: ps(yearly) };
      if (prices.monthly || prices.yearly) {
        window.__KASA_PRICES__ = prices;
        // překreslit otevřený paywall s cenami z obchodu
        return getEntitlement().then(push);
      }
    })
    .catch(function () {});
})();
