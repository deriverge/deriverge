import Foundation
import Capacitor
import MessageUI
import UIKit

// Tapkasa — odeslání a uložení daňového dokladu (PDF) na iOS.
//
// Web Share v WKWebView se nedá spolehlivě použít se soubory a stažení přes
// blob: odkaz bez delegáta stahování tiše nic neudělá; mailto: přílohu nenese.
// Tady PDF zapíšeme do dočasné složky a otevřeme:
//   mode "mail"  – Mail s vyplněným předmětem a přiloženým PDF
//                  (bez nastaveného účtu v Mailu nabídka sdílení),
//   mode "share" – systémová nabídka sdílení (Uložit do Souborů, AirDrop…),
//   mode "save"  – dialog Soubory „Uložit“.
//
// JS strana (mobile/bridge.js): window.__kasaShareFile({data, name, mime, subject, text, title, mode}).

@objc(DocSharePlugin)
public class DocSharePlugin: CAPPlugin, CAPBridgedPlugin, MFMailComposeViewControllerDelegate, UIDocumentPickerDelegate {
    public let identifier = "DocSharePlugin"
    public let jsName = "DocShare"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "share", returnType: CAPPluginReturnPromise)
    ]

    private var pendingCall: CAPPluginCall?

    @objc func share(_ call: CAPPluginCall) {
        let data = call.getString("data") ?? ""
        let name = DocSharePlugin.safeName(call.getString("name") ?? "doklad.pdf")
        let mime = call.getString("mime") ?? "application/pdf"
        let subject = call.getString("subject") ?? ""
        let text = call.getString("text") ?? ""
        let mode = call.getString("mode") ?? "share"

        guard let bytes = Data(base64Encoded: data, options: .ignoreUnknownCharacters), !bytes.isEmpty else {
            call.reject("bad data")
            return
        }

        let dir = FileManager.default.temporaryDirectory.appendingPathComponent("doklady", isDirectory: true)
        let url = dir.appendingPathComponent(name)
        do {
            try FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
            try bytes.write(to: url, options: .atomic)
        } catch {
            call.reject("write failed: \(error.localizedDescription)")
            return
        }

        DispatchQueue.main.async {
            guard let host = self.bridge?.viewController else {
                call.reject("no view controller")
                return
            }

            if mode == "mail", MFMailComposeViewController.canSendMail() {
                let mail = MFMailComposeViewController()
                mail.mailComposeDelegate = self
                if !subject.isEmpty { mail.setSubject(subject) }
                if !text.isEmpty { mail.setMessageBody(text, isHTML: false) }
                mail.addAttachmentData(bytes, mimeType: mime, fileName: name)
                self.pendingCall = call
                host.present(mail, animated: true)
                return
            }

            if mode == "save" {
                let picker = UIDocumentPickerViewController(forExporting: [url], asCopy: true)
                picker.delegate = self
                self.pendingCall = call
                host.present(picker, animated: true)
                return
            }

            var items: [Any] = [url]
            if mode == "mail" && !text.isEmpty { items.append(text) }
            let sheet = UIActivityViewController(activityItems: items, applicationActivities: nil)
            if let pop = sheet.popoverPresentationController {
                // iPad: nabídka musí mít kotvu, jinak aplikace spadne
                pop.sourceView = host.view
                pop.sourceRect = CGRect(x: host.view.bounds.midX, y: host.view.bounds.maxY - 80, width: 1, height: 1)
                pop.permittedArrowDirections = []
            }
            sheet.completionWithItemsHandler = { _, completed, _, _ in
                call.resolve(["result": completed ? "share" : "cancel"])
            }
            host.present(sheet, animated: true)
        }
    }

    public func mailComposeController(_ controller: MFMailComposeViewController,
                                      didFinishWith result: MFMailComposeResult, error: Error?) {
        controller.dismiss(animated: true)
        let how: String
        switch result {
        case .sent: how = "mail"
        case .saved: how = "draft"
        case .cancelled: how = "cancel"
        default: how = "failed"
        }
        pendingCall?.resolve(["result": how])
        pendingCall = nil
    }

    public func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
        pendingCall?.resolve(["result": "saved"])
        pendingCall = nil
    }

    public func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
        pendingCall?.resolve(["result": "cancel"])
        pendingCall = nil
    }

    /// Jen bezpečné znaky, ať název nemůže ukázat mimo složku s doklady.
    static func safeName(_ raw: String) -> String {
        var n = String(raw.unicodeScalars.map { c -> Character in
            let ok = CharacterSet.alphanumerics.contains(c) && c.isASCII || c == "." || c == "_" || c == "-"
            return ok ? Character(c) : "-"
        })
        if n.isEmpty || n.hasPrefix(".") { n = "doklad" + n }
        let low = n.lowercased()
        if !low.hasSuffix(".pdf") && !low.hasSuffix(".json") { n += ".pdf" }
        return n
    }
}
