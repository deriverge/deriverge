import Foundation
import MultipeerConnectivity
import UIKit

/// Spojení mezi kasou a výdejem. Jde přímo mezi zařízeními po místní síti
/// nebo přes Bluetooth — nepotřebuje internet, router ani žádný server.
/// Obě zařízení se hledají samy, jakmile aplikace běží a jsou blízko sebe.
final class PeerLink: NSObject {

    /// Musí být stejné na obou zařízeních a max. 15 znaků [a-z0-9-].
    private static let service = "kasa-order"

    private let peerID = MCPeerID(displayName: UIDevice.current.name)
    private lazy var session: MCSession = {
        let s = MCSession(peer: peerID, securityIdentity: nil, encryptionPreference: .required)
        s.delegate = self
        return s
    }()
    private lazy var advertiser = MCNearbyServiceAdvertiser(
        peer: peerID, discoveryInfo: nil, serviceType: PeerLink.service)
    private lazy var browser = MCNearbyServiceBrowser(
        peer: peerID, serviceType: PeerLink.service)

    /// Volá se na hlavním vlákně, když dorazí data od protějšku.
    var onMessage: ((String) -> Void)?
    /// Volá se na hlavním vlákně při změně počtu připojených zařízení.
    var onPeerCount: ((Int) -> Void)?

    func start() {
        advertiser.delegate = self
        browser.delegate = self
        advertiser.startAdvertisingPeer()
        browser.startBrowsingForPeers()
    }

    func stop() {
        advertiser.stopAdvertisingPeer()
        browser.stopBrowsingForPeers()
        session.disconnect()
    }

    func send(_ json: String) {
        let peers = session.connectedPeers
        guard !peers.isEmpty, let data = json.data(using: .utf8) else { return }
        do {
            try session.send(data, toPeers: peers, with: .reliable)
        } catch {
            NSLog("Kasa: odeslání protějšku selhalo — \(error.localizedDescription)")
        }
    }

    private func announce() {
        let n = session.connectedPeers.count
        DispatchQueue.main.async { self.onPeerCount?(n) }
    }
}

extension PeerLink: MCSessionDelegate {
    func session(_ session: MCSession, peer peerID: MCPeerID, didChange state: MCSessionState) {
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
    /// Obě zařízení jsou naše, pozvání proto bereme bez ptaní.
    func advertiser(_ advertiser: MCNearbyServiceAdvertiser,
                    didReceiveInvitationFromPeer peerID: MCPeerID,
                    withContext context: Data?,
                    invitationHandler: @escaping (Bool, MCSession?) -> Void) {
        invitationHandler(true, session)
    }

    func advertiser(_ advertiser: MCNearbyServiceAdvertiser,
                    didNotStartAdvertisingPeer error: Error) {
        NSLog("Kasa: zařízení se nepodařilo zveřejnit — \(error.localizedDescription)")
    }
}

extension PeerLink: MCNearbyServiceBrowserDelegate {
    func browser(_ browser: MCNearbyServiceBrowser, foundPeer peerID: MCPeerID,
                 withDiscoveryInfo info: [String: String]?) {
        // Ať se dvě zařízení nezvou navzájem naráz, zve vždycky to "menší".
        // Při shodě jmen zvou obě — spojení se pak ustálí na jednom.
        guard !session.connectedPeers.contains(peerID) else { return }
        if self.peerID.displayName <= peerID.displayName {
            browser.invitePeer(peerID, to: session, withContext: nil, timeout: 20)
        }
    }

    func browser(_ browser: MCNearbyServiceBrowser, lostPeer peerID: MCPeerID) {
        announce()
    }

    func browser(_ browser: MCNearbyServiceBrowser, didNotStartBrowsingForPeers error: Error) {
        NSLog("Kasa: hledání druhého zařízení selhalo — \(error.localizedDescription)")
    }
}
