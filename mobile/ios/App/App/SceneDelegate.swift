import UIKit
import Capacitor

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }

        window = UIWindow(windowScene: windowScene)
        // Okno se staví programově, storyboard se nepoužije. Musí to být
        // náš TapkasaViewController: jen ten registruje PeerLink (párování
        // bez internetu), RateApp a předává uložený stav kasy. S obecným
        // CAPBridgeViewController se nic z toho nespustilo.
        window?.rootViewController = TapkasaViewController()
        window?.makeKeyAndVisible()

        SceneDelegateProxy.shared.scene(scene, willConnectTo: session, options: connectionOptions)
    }

    // Kasa a výdej musí svítit celou akci: zhasnutý iPad přeruší spojení
    // bez internetu a objednávky nedorazí. Webové zámky obrazovky na
    // starších iOS nefungují, proto nativně.
    func sceneDidBecomeActive(_ scene: UIScene) {
        UIApplication.shared.isIdleTimerDisabled = true
    }

    func sceneWillResignActive(_ scene: UIScene) {
        UIApplication.shared.isIdleTimerDisabled = false
    }

    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        SceneDelegateProxy.shared.scene(scene, openURLContexts: URLContexts)
    }

    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        SceneDelegateProxy.shared.scene(scene, continue: userActivity)
    }
}
