import Foundation
import Capacitor
import MultipeerConnectivity
import UIKit

// Tapkasa — párování dvou zařízení (kasa ↔ výdej) přes Multipeer Connectivity.
//
// Port ios/Kasa/PeerLink.swift do Capacitor pluginu. Spojení jde přímo mezi
// zařízeními po místní síti nebo přes Bluetooth — nepotřebuje internet,
// router ani server. Obě zařízení se najdou sama, jakmile aplikace běží
// a jsou blízko sebe.
//
// JS strana (mobile/bridge.js):
//   const PeerLink = Capacitor.registerPlugin("PeerLink");
//   PeerLink.start(); PeerLink.stop(); PeerLink.send({ json });
//   PeerLink.save({ json });                      // trvalé uložení stavu kasy
//   PeerLink.addListener("message",  ({ json }) => …);
//   PeerLink.addListener("peerCount", ({ n }) => …);

// MARK: - Trvalé úložiště stavu (port Store z ios/Kasa/KasaWebView.swift)

/// Stav kasy se neukládá do prohlížeče, ale do souboru v Documents přímo
/// v kontejneru aplikace. Přežije restart, vybitou baterii i aktualizaci
/// aplikace a bere se s sebou do zálohy zařízení.
enum KasaStore {
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
            NSLog("Tapkasa: data se nepodařilo uložit — \(error.localizedDescription)")
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

// MARK: - Multipeer spojení (port ios/Kasa/PeerLink.swift, beze změn logiky)

final class PeerLink: NSObject {

    /// Musí být stejné na obou zařízeních a max. 15 znaků [a-z0-9-].
    /// V Info.plist mu odpovídají NSBonjourServices _kasa-order._tcp/_udp.
    private static let service = "kasa-order"

    private let peerID = MCPeerID(displayName: UIDevice.current.name)

    /// Otisk téhle instance. Pátrač na iOS občas „najde" inzerenta z téhož
    /// zařízení; bez otisku si pak zařízení pošle pozvánku samo sobě, kód
    /// spárování pochopitelně sedí a vznikne spojení sám se sebou. Otisk
    /// putuje v discoveryInfo i v pozvánce a shoda znamená: to jsem já, ignorovat.
    private let inst = UUID().uuidString
    private lazy var session: MCSession = {
        let s = MCSession(peer: peerID, securityIdentity: nil, encryptionPreference: .required)
        s.delegate = self
        return s
    }()

    /// Kód spárování. Zařízení se hledají a spojují jen v rámci stejného kódu:
    /// bez něj by se na trhu propojily dvě sousední kasy různých prodejců
    /// a objednávky by si přetekly mezi firmami.
    private var room = ""
    private var advertiser: MCNearbyServiceAdvertiser?
    private var browser: MCNearbyServiceBrowser?
    private var retryTimer: Timer?

    override init() {
        super.init()
        // Po návratu do popředí se hledání obnoví. Sem patří i zavření
        // systémového dotazu na Místní síť: iOS nechá hledání spuštěné před
        // udělením oprávnění hluché, dokud se nespustí znovu.
        NotificationCenter.default.addObserver(self, selector: #selector(appDidBecomeActive),
                                               name: UIApplication.didBecomeActiveNotification, object: nil)
    }

    deinit {
        NotificationCenter.default.removeObserver(self)
        retryTimer?.invalidate()
    }

    @objc private func appDidBecomeActive() {
        retryIfLonely("foreground")
    }

    /// Volá se na hlavním vlákně, když dorazí data od protějšku.
    var onMessage: ((String) -> Void)?
    /// Volá se na hlavním vlákně při změně počtu připojených zařízení.
    var onPeerCount: ((Int) -> Void)?
    /// Diagnostika pro stránku: fáze (started, found, invited, session,
    /// browse-error, advertise-error) a detail. Bez ní se z telefonu nedá
    /// zjistit, kde se hledání zastavilo.
    var onState: ((String, String) -> Void)?

    private func state(_ phase: String, _ detail: String) {
        DispatchQueue.main.async { self.onState?(phase, detail) }
    }

    /// Souhrn pro dotaz ze stránky.
    func status() -> [String: Any] {
        return [
            "room": room,
            "advertising": advertiser != nil,
            "browsing": browser != nil,
            "peers": session.connectedPeers.count,
            "name": peerID.displayName
        ]
    }

    /// Bez kódu se nikam nehlásíme ani nikoho nehledáme. Volání z pluginu
    /// přichází z jeho fronty; s hledáním i časovačem pracujeme jen na
    /// hlavním vlákně.
    func start(room newRoom: String) {
        DispatchQueue.main.async { self.startOnMain(room: newRoom) }
    }

    func stop() {
        DispatchQueue.main.async { self.stopOnMain() }
    }

    private func startOnMain(room newRoom: String) {
        let code = newRoom.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()
        if code == room && advertiser != nil { return }
        stopOnMain()
        room = code
        guard !code.isEmpty else { return }
        makeDiscovery()
        state("started", code)
        retryTimer?.invalidate()
        retryTimer = Timer.scheduledTimer(withTimeInterval: 20, repeats: true) { [weak self] _ in
            self?.retryIfLonely("timer")
        }
    }

    private func stopOnMain() {
        retryTimer?.invalidate()
        retryTimer = nil
        dropDiscovery()
        session.disconnect()
        announce()
    }

    private func makeDiscovery() {
        let a = MCNearbyServiceAdvertiser(
            peer: peerID, discoveryInfo: ["r": room, "i": inst], serviceType: PeerLink.service)
        let b = MCNearbyServiceBrowser(peer: peerID, serviceType: PeerLink.service)
        a.delegate = self
        b.delegate = self
        a.startAdvertisingPeer()
        b.startBrowsingForPeers()
        advertiser = a
        browser = b
    }

    private func dropDiscovery() {
        advertiser?.stopAdvertisingPeer()
        browser?.stopBrowsingForPeers()
        advertiser = nil
        browser = nil
    }

    /// Bez protějšku se hledání každých 20 s a při návratu do popředí
    /// spustí znovu. Spojené zařízení se nechává být.
    private func retryIfLonely(_ why: String) {
        guard !room.isEmpty, session.connectedPeers.isEmpty else { return }
        dropDiscovery()
        makeDiscovery()
        state("retry", why)
    }

    func send(_ json: String) {
        let peers = session.connectedPeers
        guard !peers.isEmpty, let data = json.data(using: .utf8) else { return }
        do {
            try session.send(data, toPeers: peers, with: .reliable)
        } catch {
            NSLog("Tapkasa: odeslání protějšku selhalo — \(error.localizedDescription)")
        }
    }

    private func announce() {
        let n = session.connectedPeers.count
        DispatchQueue.main.async { self.onPeerCount?(n) }
    }
}

extension PeerLink: MCSessionDelegate {
    func session(_ session: MCSession, peer peerID: MCPeerID, didChange state: MCSessionState) {
        let name: String
        switch state {
        case .connected: name = "connected"
        case .connecting: name = "connecting"
        default: name = "notConnected"
        }
        self.state("session", "\(peerID.displayName) \(name), n=\(session.connectedPeers.count)")
        announce()
    }

    func session(_ session: MCSession, didReceive data: Data, fromPeer peerID: MCPeerID) {
        guard let json = String(data: data, encoding: .utf8) else { return }
        DispatchQueue.main.async { self.onMessage?(json) }
    }

    func session(_ session: MCSession, didReceive stream: InputStream,
                 withName streamName: String, fromPeer peerID: MCPeerID) {}
    func session(_ session: MCSession, didStartReceivingResourceWithName resourceName: String,
                 fromPeer peerID: MCPeerID, with progress: Progress) {}
    func session(_ session: MCSession, didFinishReceivingResourceWithName resourceName: String,
                 fromPeer peerID: MCPeerID, at localURL: URL?, withError error: Error?) {}
}

extension PeerLink: MCNearbyServiceAdvertiserDelegate {
    /// Pozvání bereme jen od zařízení, které zná náš kód spárování.
    func advertiser(_ advertiser: MCNearbyServiceAdvertiser,
                    didReceiveInvitationFromPeer peerID: MCPeerID,
                    withContext context: Data?,
                    invitationHandler: @escaping (Bool, MCSession?) -> Void) {
        let raw = context.flatMap { String(data: $0, encoding: .utf8) } ?? ""
        let parts = raw.split(separator: "|", maxSplits: 1).map(String.init)
        let theirRoom = parts.first ?? ""
        let theirInst = parts.count > 1 ? parts[1] : ""
        let ok = !room.isEmpty && theirRoom == room && theirInst != inst
        state("invited", "\(peerID.displayName) \(ok ? "accepted" : "rejected")")
        invitationHandler(ok, session)
    }

    func advertiser(_ advertiser: MCNearbyServiceAdvertiser,
                    didNotStartAdvertisingPeer error: Error) {
        NSLog("Tapkasa: zařízení se nepodařilo zveřejnit — \(error.localizedDescription)")
        state("advertise-error", error.localizedDescription)
    }
}

extension PeerLink: MCNearbyServiceBrowserDelegate {
    func browser(_ browser: MCNearbyServiceBrowser, foundPeer peerID: MCPeerID,
                 withDiscoveryInfo info: [String: String]?) {
        // Ať se dvě zařízení nezvou navzájem naráz, zve vždycky jen jedno:
        // to s menším otiskem. Jména zařízení jsou na novějším iOS často
        // stejná ("iPhone"), otisky nikdy.
        state("found", "\(peerID.displayName) r=\(info?["r"] ?? "-")")
        guard !room.isEmpty, info?["r"] == room else { return }
        let theirInst = info?["i"] ?? ""
        guard theirInst != inst else { return }   // našli jsme sami sebe
        guard !session.connectedPeers.contains(peerID) else { return }
        let iInvite = theirInst.isEmpty ? (self.peerID.displayName <= peerID.displayName) : (inst < theirInst)
        if iInvite {
            browser.invitePeer(peerID, to: session,
                               withContext: (room + "|" + inst).data(using: .utf8), timeout: 20)
        }
    }

    func browser(_ browser: MCNearbyServiceBrowser, lostPeer peerID: MCPeerID) {
        state("lost", peerID.displayName)
        announce()
    }

    func browser(_ browser: MCNearbyServiceBrowser, didNotStartBrowsingForPeers error: Error) {
        NSLog("Tapkasa: hledání druhého zařízení selhalo — \(error.localizedDescription)")
        state("browse-error", error.localizedDescription)
    }
}

// MARK: - Capacitor plugin

@objc(PeerLinkPlugin)
public class PeerLinkPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "PeerLinkPlugin"
    public let jsName = "PeerLink"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "start", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "stop", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "send", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "save", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "status", returnType: CAPPluginReturnPromise)
    ]

    private let link = PeerLink()

    override public func load() {
        link.onMessage = { [weak self] json in
            self?.notifyListeners("message", data: ["json": json])
        }
        link.onPeerCount = { [weak self] count in
            self?.notifyListeners("peerCount", data: ["n": count])
        }
        link.onState = { [weak self] phase, detail in
            self?.notifyListeners("state", data: ["phase": phase, "detail": detail])
        }
    }

    deinit { link.stop() }

    /// Očekává parametr `room` s kódem spárování. Prázdný kód spojení vypne.
    @objc func start(_ call: CAPPluginCall) {
        link.start(room: call.getString("room") ?? "")
        call.resolve()
    }

    @objc func stop(_ call: CAPPluginCall) {
        link.stop()
        call.resolve()
    }

    /// Diagnostika: co modul právě dělá.
    @objc func status(_ call: CAPPluginCall) {
        call.resolve(link.status())
    }

    /// Pošle JSON všem připojeným protějškům. Bez protějšku se zpráva
    /// zahodí — stejně jako v původní aplikaci; web má vlastní frontu.
    @objc func send(_ call: CAPPluginCall) {
        guard let json = call.getString("json") else {
            call.reject("Chybí parametr 'json'")
            return
        }
        link.send(json)
        call.resolve()
    }

    /// Trvale uloží stav kasy (mapování na původní messageHandlers.kasa).
    @objc func save(_ call: CAPPluginCall) {
        guard let json = call.getString("json") else {
            call.reject("Chybí parametr 'json'")
            return
        }
        KasaStore.write(json)
        call.resolve()
    }
}
