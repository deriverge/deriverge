/*
 * Tapkasa — adaptér nativního mostu pro Capacitor.
 *
 * Webová aplikace (tapkasa/index.html) mluví s nativní vrstvou přes hooky
 * z původní SwiftUI aplikace:
 *
 *   ven z webu:  window.webkit.messageHandlers.peer.postMessage(json)  — pošli objednávku protějšku
 *                window.webkit.messageHandlers.kasa.postMessage(json)  — ulož stav do souboru
 *   do webu:     window.__kasaPeer(json)      — přišla data od protějšku
 *                window.__kasaPeerCount(n)    — změnil se počet připojených zařízení
 *                window.__KASA_BOOT__         — uložený stav, vložený PŘED spuštěním stránky
 *
 * Tento soubor je přeloží na volání Capacitor pluginu "PeerLink"
 * (mobile/ios-plugin/PeerLinkPlugin.swift), aniž by se tapkasa/index.html
 * musel jakkoli měnit. V obyčejném prohlížeči (bez Capacitoru) neudělá nic.
 *
 * __KASA_BOOT__ tento skript neřeší — ten musí existovat dřív, než se stránka
 * spustí, proto ho vkládá nativní kód (WKUserScript v TapkasaViewController).
 */
(function () {
  "use strict";

  var cap = window.Capacitor;
  var isNative = !!(cap && typeof cap.isNativePlatform === "function" && cap.isNativePlatform());
  if (!isNative || typeof cap.registerPlugin !== "function") {
    return; // čistý web — aplikace si vystačí s localStorage/IndexedDB
  }

  var PeerLink;
  try {
    PeerLink = cap.registerPlugin("PeerLink");
  } catch (e) {
    return;
  }

  function callSafe(method, args) {
    // Na platformě bez nativní implementace (dnes Android) plugin vyhodí
    // "not implemented" — to je v pořádku, aplikace běží dál bez párování.
    try {
      var p = PeerLink[method](args);
      if (p && typeof p.catch === "function") { p.catch(function () {}); }
    } catch (e) {}
  }

  // ---- ven z webu: napodobíme handlery, které index.html očekává ----------

  var peerHandler = {
    postMessage: function (json) { callSafe("send", { json: String(json) }); }
  };
  var kasaHandler = {
    postMessage: function (json) { callSafe("save", { json: String(json) }); }
  };

  function installHandlers() {
    try {
      // 1) zkusíme handlery přidat rovnou na existující objekt WebKitu
      window.webkit = window.webkit || {};
      window.webkit.messageHandlers = window.webkit.messageHandlers || {};
      window.webkit.messageHandlers.peer = peerHandler;
      window.webkit.messageHandlers.kasa = kasaHandler;
      if (window.webkit.messageHandlers.peer === peerHandler) { return; }
    } catch (e) {}
    try {
      // 2) nativní objekt je zamčený — podstrčíme vlastní, který přes
      //    prototyp pořád vidí původní handlery (např. Capacitorův "bridge")
      var real = (window.webkit && window.webkit.messageHandlers) || {};
      var shim = Object.create(real);
      shim.peer = peerHandler;
      shim.kasa = kasaHandler;
      window.webkit = { messageHandlers: shim };
    } catch (e) {}
  }

  installHandlers();

  // ---- do webu: nativní události přeposíláme do funkcí stránky ------------

  PeerLink.addListener("message", function (ev) {
    var json = ev && typeof ev.json === "string" ? ev.json : "";
    if (json && typeof window.__kasaPeer === "function") {
      window.__kasaPeer(json);
    }
  });

  PeerLink.addListener("peerCount", function (ev) {
    var n = ev && typeof ev.n === "number" ? ev.n : 0;
    if (typeof window.__kasaPeerCount === "function") {
      window.__kasaPeerCount(n);
    }
  });

  // Původní aplikace spouštěla hledání protějšku hned po startu — uděláme totéž.
  callSafe("start");

  // Při ukončení aplikace síť poctivě zavřeme (na iOS se stránka jen zmrazí,
  // pagehide je tam spolehlivější než beforeunload).
  window.addEventListener("pagehide", function () { callSafe("stop"); });
})();
