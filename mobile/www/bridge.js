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
  if (!isNative) {
    return; // čistý web — aplikace si vystačí s localStorage/IndexedDB
  }

  // Diagnostika párování pro stránku (Menu > Propojená zařízení): stačí
  // otevřít aplikaci a přečíst, kde se hledání zastavilo.
  var diag = window.__kasaPeerDiag = { plugin: false, log: [] };
  function dlog(text) {
    diag.log.push(new Date().toTimeString().slice(0, 8) + " " + text);
    if (diag.log.length > 12) { diag.log.shift(); }
    if (typeof window.__kasaPeerState === "function") {
      try { window.__kasaPeerState(diag); } catch (e) {}
    }
  }

  // Vestavěný most vystavuje pluginy v Capacitor.Plugins; registerPlugin
  // mají jen aplikace s vlastním balíčkem @capacitor/core. Zkoušíme obojí.
  var PeerLink = null;
  if (cap.Plugins && cap.Plugins.PeerLink) {
    PeerLink = cap.Plugins.PeerLink;
  } else if (typeof cap.registerPlugin === "function") {
    try { PeerLink = cap.registerPlugin("PeerLink"); } catch (e) {}
  }
  // Žádost o hodnocení v App Store: okno vyvolává systém, my jen předáme
  // podnět. Kdy o ně požádat, rozhoduje aplikace (index.html) přes hook
  // window.__kasaAskReview; bez nativního modulu hook nevznikne a web
  // se chová jako dřív.
  var RateApp = null;
  if (cap.Plugins && cap.Plugins.RateApp) {
    RateApp = cap.Plugins.RateApp;
  } else if (typeof cap.registerPlugin === "function") {
    try { RateApp = cap.registerPlugin("RateApp"); } catch (e) {}
  }
  if (RateApp) {
    window.__kasaAskReview = function () {
      // most u metod bez návratové hodnoty vrací undefined, ne příslib
      try { Promise.resolve(RateApp.request()).catch(function () {}); } catch (e) {}
    };
  }

  // Čtení nahlas: v Android WebView webová speechSynthesis mlčí, nativní
  // modul Speak používá systémové TextToSpeech. Na iOS hook nevzniká
  // a stránka si vystačí se speechSynthesis.
  var Speak = null;
  if (cap.Plugins && cap.Plugins.Speak) {
    Speak = cap.Plugins.Speak;
  } else if (typeof cap.registerPlugin === "function") {
    try { Speak = cap.registerPlugin("Speak"); } catch (e) {}
  }
  if (Speak && typeof cap.getPlatform === "function" && cap.getPlatform() === "android") {
    window.__kasaSpeak = function (text, locale) {
      try { Promise.resolve(Speak.speak({ text: String(text), locale: String(locale || "") })).catch(function () {}); } catch (e) {}
    };
  }

  // Daňový doklad (PDF): e-mail s přílohou, sdílení a uložení do souborů.
  // Web Share ani stažení přes blob: v Android WebView nefungují a mailto:
  // přílohu nenese, proto nativní modul DocShare na obou platformách.
  // Hook vrací příslib s {result: "mail"|"share"|"saved"|"cancel"}.
  var DocShare = null;
  if (cap.Plugins && cap.Plugins.DocShare) {
    DocShare = cap.Plugins.DocShare;
  } else if (typeof cap.registerPlugin === "function") {
    try { DocShare = cap.registerPlugin("DocShare"); } catch (e) {}
  }
  if (DocShare) {
    window.__kasaShareFile = function (opts) {
      try {
        return Promise.resolve(DocShare.share(opts || {}));
      } catch (e) {
        return Promise.reject(e);
      }
    };
    window.__kasaSaveFile = true;
  }

  if (!PeerLink) {
    dlog("modul PeerLink nenalezen; pluginy: " + (cap.Plugins ? Object.keys(cap.Plugins).join(", ") : "žádné"));
    return; // párování zůstane na internetovém přeposílači
  }
  diag.plugin = true;

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

  // Přímé hooky pro stránku: nespoléhají na to, že se podstrčení handlerů
  // do objektu WebKitu povedlo. Stránka je zkouší jako první.
  window.__kasaPeerSend = function (json) { callSafe("send", { json: String(json) }); };
  window.__kasaSave = function (json) { callSafe("save", { json: String(json) }); };

  // ---- do webu: nativní události přeposíláme do funkcí stránky ------------

  PeerLink.addListener("message", function (ev) {
    var json = ev && typeof ev.json === "string" ? ev.json : "";
    if (json && typeof window.__kasaPeer === "function") {
      window.__kasaPeer(json);
    }
  });

  PeerLink.addListener("state", function (ev) {
    dlog((ev && ev.phase) + ": " + (ev && ev.detail));
  });

  PeerLink.addListener("peerCount", function (ev) {
    var n = ev && typeof ev.n === "number" ? ev.n : 0;
    dlog("spojená zařízení: " + n);
    if (typeof window.__kasaPeerCount === "function") {
      window.__kasaPeerCount(n);
    }
  });

  // Hledání protějšku se spouští až s kódem spárování, ne hned po startu:
  // bez kódu by se spojila kterákoli dvě zařízení v dosahu. Kód dodá stránka,
  // jakmile ho zná, a při každé jeho změně znovu.
  window.__kasaPeerLink = function (room) {
    var r = typeof room === "string" ? room : "";
    dlog("start(" + (r || "bez kódu") + ")");
    try {
      Promise.resolve(PeerLink.start({ room: r }))
        .then(function () { return PeerLink.status(); })
        .then(function (st) {
          st = st || {};
          diag.supported = st.supported !== false;
          dlog("stav: kód " + (st.room || "žádný") + ", hledám " + (st.browsing ? "ano" : "ne") + ", spojeno " + (st.peers || 0) +
               (st.supported === false ? ", bez podpory (potřeba Android 13+)" : ""));
          // skutečný počet spojení i po znovunačtení stránky, jinak by
          // stránka myslela, že nikdo není, a zprávy by jen odkládala
          if (typeof st.peers === "number" && typeof window.__kasaPeerCount === "function") {
            window.__kasaPeerCount(st.peers);
          }
        })
        .catch(function (e) { dlog("chyba: " + String(e && e.message || e)); });
    } catch (e) { dlog("výjimka: " + String(e && e.message || e)); }
  };

  // Hned po startu zjistíme, zda je přímé spojení na tomto zařízení
  // podporované (Android 13+), ať stránka ukáže správnou radu.
  try {
    Promise.resolve(PeerLink.status()).then(function (st) {
      st = st || {};
      diag.supported = st.supported !== false;
      dlog("modul připraven" + (st.supported === false ? ", bez podpory (potřeba Android 13+)" : ""));
    }).catch(function () {});
  } catch (e) {}

  // Stránka se načetla dřív než tenhle soubor, kód spárování si tedy
  // vyzvedneme sami; při každé další změně nám ho pošle sama.
  if (typeof window.__kasaRoom === "function") {
    window.__kasaPeerLink(window.__kasaRoom());
  }

  // Při ukončení aplikace síť poctivě zavřeme (na iOS se stránka jen zmrazí,
  // pagehide je tam spolehlivější než beforeunload).
  window.addEventListener("pagehide", function () { callSafe("stop"); });
})();
