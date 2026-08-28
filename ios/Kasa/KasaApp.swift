import SwiftUI
import UIKit

@main
struct KasaApp: App {
    var body: some Scene {
        WindowGroup {
            KasaWebView()
                .ignoresSafeArea()
                .onAppear {
                    // u stánku se čeká mezi zákazníky — obrazovka nesmí zhasínat
                    UIApplication.shared.isIdleTimerDisabled = true
                }
        }
    }
}
