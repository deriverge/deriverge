import UIKit
import Capacitor
import WebKit

/// Registrace pluginu PeerLink a chování webview po vzoru původní
/// ios/Kasa/KasaWebView.swift. Ve storyboardu (App/Base.lproj/Main.storyboard)
/// musí mít scéna customClass="TapkasaViewController" customModule="App".
class TapkasaViewController: CAPBridgeViewController {

    override open func capacitorDidLoad() {
        // Lokální plugin není npm balíček, proto se registruje ručně.
        bridge?.registerPluginInstance(PeerLinkPlugin())
        // Pojistka pro nákupy: kdyby automatická registrace RevenueCat
        // pluginu (packageClassList) selhala, zkusíme třídu doregistrovat
        // sami. Přímý import modulu nejde — shodil optimalizátor Swiftu
        // v Xcode Cloud, proto vyhledání třídy za běhu.
        if bridge?.plugin(withName: "Purchases") == nil,
           let cls = NSClassFromString("PurchasesPlugin") as? CAPPlugin.Type {
            bridge?.registerPluginType(cls)
        }

        guard let web = bridge?.webView else { return }
        // Pokladna je "papír", ne stránka — nemá pružit ani uhýbat klávesnici.
        web.scrollView.bounces = false
        web.scrollView.contentInsetAdjustmentBehavior = .never
        // Papírové pozadí (#FBFAF7), ať start nebliká bílou.
        let paper = UIColor(red: 0.984, green: 0.980, blue: 0.969, alpha: 1)
        web.backgroundColor = paper
        web.scrollView.backgroundColor = paper
        web.isOpaque = false
    }

    override open func webViewConfiguration(for instanceConfiguration: InstanceConfiguration) -> WKWebViewConfiguration {
        let config = super.webViewConfiguration(for: instanceConfiguration)
        // Uložený stav kasy se stránce předává dřív, než se spustí její kód —
        // window.__KASA_BOOT__ čte load() v index.html synchronně při startu.
        config.userContentController.addUserScript(WKUserScript(
            source: "window.__KASA_BOOT__ = \(KasaStore.jsLiteral(KasaStore.read()));",
            injectionTime: .atDocumentStart,
            forMainFrameOnly: true))
        return config
    }
}
