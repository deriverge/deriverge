import SwiftUI
import UIKit
import WebKit

/// Kasa běží jako webová stránka zabalená do nativní aplikace, ale data
/// nedrží prohlížeč — ta se ukládají do souboru v Documents přímo v kontejneru
/// aplikace. Přežijí tedy restart, vybitou baterii i aktualizaci aplikace
/// a berou se s sebou do zálohy iPadu.
enum Store {
    static var url: URL {
        FileManager.default
            .urls(for: .documentDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("kasa.json")
    }

    static func read() -> String {
        (try? String(contentsOf: url, encoding: .utf8)) ?? ""
    }

    static func write(_ json: String) {
        do {
            try json.write(to: url, atomically: true, encoding: .utf8)
        } catch {
            NSLog("Kasa: data se nepodařilo uložit — \(error.localizedDescription)")
        }
    }

    /// Text jako platný javascriptový literál, aby šel bezpečně vložit do stránky.
    static func jsLiteral(_ text: String) -> String {
        guard let data = try? JSONSerialization.data(withJSONObject: [text]),
              let wrapped = String(data: data, encoding: .utf8),
              wrapped.count >= 2 else { return "\"\"" }
        return String(wrapped.dropFirst().dropLast())   // ["..."] → "..."
            .replacingOccurrences(of: "\u{2028}", with: "\\u2028")
            .replacingOccurrences(of: "\u{2029}", with: "\\u2029")
    }
}

/// Most mezi stránkou a zařízením: ukládání do souboru a posílání
/// objednávek druhému zařízení.
final class Bridge: NSObject, WKScriptMessageHandler {
    weak var web: WKWebView?
    let link = PeerLink()

    override init() {
        super.init()
        link.onMessage = { [weak self] json in
            self?.callJS("window.__kasaPeer", Store.jsLiteral(json))
        }
        link.onPeerCount = { [weak self] count in
            self?.callJS("window.__kasaPeerCount", String(count))
        }
        link.start()
    }

    deinit { link.stop() }

    private func callJS(_ fn: String, _ arg: String) {
        guard let web = web else { return }
        web.evaluateJavaScript("if (typeof \(fn) === 'function') { \(fn)(\(arg)); }") { _, error in
            if let error = error { NSLog("Kasa: \(fn) selhalo — \(error.localizedDescription)") }
        }
    }

    func userContentController(_ controller: WKUserContentController,
                               didReceive message: WKScriptMessage) {
        guard let json = message.body as? String else { return }
        switch message.name {
        case "kasa": Store.write(json)
        case "peer": link.send(json)
        default: break
        }
    }
}

struct KasaWebView: UIViewRepresentable {
    func makeCoordinator() -> Bridge { Bridge() }

    func makeUIView(context: Context) -> WKWebView {
        let controller = WKUserContentController()

        // uložená data předáme stránce dřív, než se vůbec spustí její kód
        controller.addUserScript(WKUserScript(
            source: "window.__KASA_BOOT__ = \(Store.jsLiteral(Store.read()));",
            injectionTime: .atDocumentStart,
            forMainFrameOnly: true))
        controller.add(context.coordinator, name: "kasa")
        controller.add(context.coordinator, name: "peer")

        let config = WKWebViewConfiguration()
        config.userContentController = controller
        config.allowsInlineMediaPlayback = true

        let web = WKWebView(frame: .zero, configuration: config)
        web.scrollView.bounces = false
        web.scrollView.contentInsetAdjustmentBehavior = .never
        web.backgroundColor = UIColor(red: 0.984, green: 0.980, blue: 0.969, alpha: 1)
        web.scrollView.backgroundColor = web.backgroundColor
        web.isOpaque = false
        context.coordinator.web = web

        if let index = Bundle.main.url(forResource: "index", withExtension: "html") {
            web.loadFileURL(index, allowingReadAccessTo: index.deletingLastPathComponent())
        } else {
            NSLog("Kasa: index.html není v aplikaci — spusť ios/copy-web.sh a přidej ho do targetu.")
        }
        return web
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
