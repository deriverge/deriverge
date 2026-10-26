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
| `window.__kasaSaveArchive(json)` | web → nativní | `bridge.js` volá `PeerLink.save({ json, file: "archive" })` → `kasa-archive.json` (od 1.0.6) |
| `window.__KASA_BOOT_ARCH__` | nativní → web, před startem stránky (iOS) | `TapkasaViewController` vloží obsah `kasa-archive.json` spolu s `__KASA_BOOT__` |
| `window.__kasaStore.read("main" \| "archive")` | web → nativní, synchronně (Android) | rozhraní přidané v `PeerLinkPlugin.load()`, čte `kasa.json` a `kasa-archive.json` |
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

Nativní `PeerLink` pro Android je v
`android/app/src/main/java/com/deriverge/tapkasa/PeerLinkPlugin.java`: Google
Nearby Connections (P2P_CLUSTER), Android 13 a novější, stejné JS rozhraní
jako na iOS (start/stop/send/save/status, události message/peerCount/state).
Na starším Androidu `status()` hlásí `supported: false` a párování jde přes
internetový přeposílač.

Ukládání: `save({ json })` zapisuje `kasa.json`, `save({ json, file: "archive" })`
`kasa-archive.json`, obojí přes dočasný soubor a přejmenování. `__KASA_BOOT__`
na Androidu není; místo něj plugin při načtení přidá do webview rozhraní
`window.__kasaStore` a stránka si při startu synchronně přečte
`__kasaStore.read("main")` a `__kasaStore.read("archive")`.

## Párování od 1.0.6

Kód má 8 znaků s kontrolním znakem. Stránka z něj odvodí (PBKDF2) klíč
AES-GCM a jméno místnosti `T2…`; `__kasaPeerLink(room)` tedy nativní vrstvě
předává odvozené jméno, ne kód, a zprávy přes `send` jsou zašifrované obálky
`{e:2,n,c}`. Nativní kód je jen přenáší, nic na něm měnit nebylo potřeba.
Starší kódy (5 znaků nebo vlastní) jdou dál bez šifrování pod kódem samotným.

## Fakturace (`billing.js`)

Stejný princip: globál `window.TapkasaBilling` s `getEntitlement()`,
`purchase(product)`, `restore()`. Na nativní platformě jde přes
`Capacitor.registerPlugin("Purchases")` (@revenuecat/purchases-capacitor,
nativní část registruje `npx cap sync` sám); v prohlížeči všechno vrací
`'free'`. Podrobnosti a klíče viz `README.md` a komentář v `billing.js`.
