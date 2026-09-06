import Foundation
import Capacitor
import StoreKit

// Tapkasa — žádost o hodnocení v App Store.
//
// Okno "Ohodnoťte aplikaci" vyvolává systém (SKStoreReviewController) a sám
// rozhoduje, jestli se vůbec ukáže: Apple je zobrazí nejvýš třikrát za rok
// a v TestFlightu vůbec. Kdy o ně požádat, řídí webová vrstva
// (tapkasa/index.html), tady se jen předává systému.
//
// JS strana (mobile/bridge.js):
//   Capacitor.Plugins.RateApp.request()

@objc(RateAppPlugin)
public class RateAppPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "RateAppPlugin"
    public let jsName = "RateApp"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "request", returnType: CAPPluginReturnPromise)
    ]

    @objc func request(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            if let scene = UIApplication.shared.connectedScenes
                .first(where: { $0.activationState == .foregroundActive }) as? UIWindowScene {
                SKStoreReviewController.requestReview(in: scene)
            }
            call.resolve()
        }
    }
}
