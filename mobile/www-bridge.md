# Most mezi webem a nativní vrstvou (Capacitor)

Webová aplikace `tapkasa/index.html` vznikla pro původní SwiftUI obal
(`ios/Kasa/KasaWebView.swift` + `ios/Kasa/PeerLink.swift`) a mluví s nativní
vrstvou přes pět hooků. Capacitor obal je obsluhuje **beze změny webu** —
`sync-web.sh` jen do kopie v `www/` přidá `<script src="bridge.js">` a
`<script src="billing.js">` před `</body>`.

## Mapování hooků

| Hook ve webu (`tapkasa/index.html`) | Směr | V Capacitoru to obsluhuje |
| --- | --- | --- |
| `window.webkit.messageHandlers.peer.postMessage(json)` | web → nativní | `bridge.js` podstrčí objekt `peer`, jehož `postMessage` volá `PeerLink.send({ json })` |
| `window.webkit.messageHandlers.kasa.postMessage(json)` | web → nativní | `bridge.js` podstrčí objekt `kasa`, jehož `postMessage` volá `PeerLink.save({ json })` → zápis do `Documents/kasa.json` |
| `window.__kasaPeer(json)` | nativní → web | událost pluginu `"message"` `{ json }`; `bridge.js` ji přeposílá do `window.__kasaPeer` |
| `window.__kasaPeerCount(n)` | nativní → web | událost pluginu `"peerCount"` `{ n }`; `bridge.js` ji přeposílá do `window.__kasaPeerCount` |
| `window.__KASA_BOOT__` | nativní → web, **před startem stránky** | `TapkasaViewController.webViewConfiguration(for:)` vloží `WKUserScript` (atDocumentStart) s obsahem `Documents/kasa.json` — `bridge.js` to řešit nemůže, protože `load()` ve webu čte hodnotu synchronně při spuštění |

## Jak to do sebe zapadá

1. **Nativní plugin** `ios-plugin/PeerLinkPlugin.swift` (kopie je i v
   `ios/App/App/`) — port `PeerLink` z původní aplikace: Multipeer
   Connectivity, service type `kasa-order`, šifrovaná session, automatické
   pozvání („zve vždycky to menší jméno“, pozvání se přijímá bez ptaní).
   JS API pluginu (jsName `PeerLink`):

   ```js
   const PeerLink = Capacitor.registerPlugin("PeerLink");
   await PeerLink.start();              // začni vysílat i hledat protějšky
   await PeerLink.stop();               // zastav a odpoj
   await PeerLink.send({ json });       // pošli JSON všem připojeným
   await PeerLink.save({ json });       // trvale ulož stav kasy do souboru
   PeerLink.addListener("message",   ({ json }) => { /* data od protějšku */ });
   PeerLink.addListener("peerCount", ({ n })    => { /* počet připojených */ });
   ```

2. **Registrace** — lokální plugin není npm balíček, proto ho registruje
   `ios-plugin/TapkasaViewController.swift` (podtřída `CAPBridgeViewController`)
   přes `bridge?.registerPluginInstance(PeerLinkPlugin())`. Storyboard
   `Main.storyboard` má na scéně `customClass="TapkasaViewController"`.
   Tentýž controller nastavuje papírové pozadí, vypíná pružení scrollu
   a vkládá boot skript s `__KASA_BOOT__`.

3. **JS adaptér** `bridge.js` — běží až po nativním bootu:
   - feature-detekce: bez `window.Capacitor.isNativePlatform()` nedělá nic
     (v prohlížeči si web vystačí s localStorage/IndexedDB a relayem);
   - podstrčí `window.webkit.messageHandlers.peer/kasa` (napřímo, nebo přes
     objekt s prototypem na původních handlerech, když je nativní objekt
     zamčený), takže nezměněný `index.html` posílá zprávy jako dřív;
   - přeposílá události `message`/`peerCount` do `__kasaPeer`/`__kasaPeerCount`;
   - volá `PeerLink.start()` hned po načtení (původní aplikace startovala
     spojení taky sama) a `stop()` na `pagehide`.

## Android

Nativní implementace `PeerLink` pro Android zatím **není** — Multipeer
Connectivity je jen na Apple platformách (androidí obdoba by stála na
Wi-Fi Direct / Nearby Connections). `bridge.js` s tím počítá: každé volání
pluginu chytá výjimku „not implemented“, takže aplikace na Androidu běží
normálně, jen bez lokálního párování — objednávky mezi zařízeními chodí
přes volitelný relay, jako ve webové verzi. Stav se ukládá do
localStorage/IndexedDB WebView (hook `kasa` a `__KASA_BOOT__` se neuplatní).

## Fakturace (`billing.js`)

Stejný princip: globál `window.TapkasaBilling` s `getEntitlement()`,
`purchase(product)`, `restore()`. Na nativní platformě jde přes
`Capacitor.registerPlugin("Purchases")` (@revenuecat/purchases-capacitor,
nativní část registruje `npx cap sync` sám); v prohlížeči všechno vrací
`'free'`. Podrobnosti a klíče viz `README.md` a komentář v `billing.js`.
