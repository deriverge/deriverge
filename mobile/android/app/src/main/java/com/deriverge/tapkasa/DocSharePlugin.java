package com.deriverge.tapkasa;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.Intent;
import android.net.Uri;
import android.util.Base64;

import androidx.activity.result.ActivityResult;
import androidx.core.content.FileProvider;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.ActivityCallback;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * Tapkasa: odeslání a uložení daňového dokladu (PDF) na Androidu.
 *
 * Android WebView neumí Web Share (navigator.share chybí), stažení přes
 * blob: odkaz bez DownloadListeneru tiše zahodí a mailto: přílohu nenese.
 * Výsledek byl, že „Poslat e-mailem“ otevřelo prázdnou zprávu a „Sdílet“
 * nenabídlo nic. Tady se PDF zapíše do cache aplikace, předá se přes
 * FileProvider (cache-path v res/xml/file_paths.xml) a otevře se:
 *   mode "mail"  – e-mailová aplikace s vyplněným předmětem a přiloženým PDF,
 *   mode "share" – systémová nabídka sdílení (Disk, Soubory, chat…),
 *   mode "save"  – systémový dialog „Uložit jako“ (Stažené soubory apod.).
 *
 * JS strana (mobile/bridge.js): window.__kasaShareFile({data, name, mime, subject, text, title, mode}).
 */
@CapacitorPlugin(name = "DocShare")
public class DocSharePlugin extends Plugin {


    @PluginMethod
    public void share(PluginCall call) {
        String data = call.getString("data", "");
        String name = safeName(call.getString("name", "doklad.pdf"));
        String mime = call.getString("mime", "application/pdf");
        String subject = call.getString("subject", "");
        String text = call.getString("text", "");
        String title = call.getString("title", "");
        String mode = call.getString("mode", "share");

        byte[] bytes;
        try {
            bytes = Base64.decode(data, Base64.DEFAULT);
        } catch (IllegalArgumentException e) {
            call.reject("bad data");
            return;
        }
        if (bytes == null || bytes.length == 0) {
            call.reject("empty file");
            return;
        }

        // Soubor jde vždy nejdřív do cache aplikace: sdílení z něj bere
        // content:// adresu a ukládání z něj kopíruje.
        File file;
        Uri uri;
        try {
            file = writeCache(name, bytes);
            uri = FileProvider.getUriForFile(getContext(), getContext().getPackageName() + ".fileprovider", file);
        } catch (Exception e) {
            call.reject("write failed: " + e.getMessage());
            return;
        }

        if ("save".equals(mode)) {
            // Capacitor si rozpracované volání při odchodu do systémového
            // dialogu ukládá do stavu aktivity. S PDF uvnitř (stovky kB)
            // Android shodil aplikaci na TransactionTooLargeException
            // a v Stažených zůstal prázdný soubor. Data proto z volání
            // odebereme a po návratu soubor zkopírujeme z cache; funguje
            // to i poté, co systém aplikaci mezitím ukončí.
            call.getData().remove("data");
            call.getData().put("file", name);
            Intent save = new Intent(Intent.ACTION_CREATE_DOCUMENT);
            save.addCategory(Intent.CATEGORY_OPENABLE);
            save.setType(mime);
            save.putExtra(Intent.EXTRA_TITLE, name);
            try {
                startActivityForResult(call, save, "saveResult");
            } catch (ActivityNotFoundException e) {
                call.reject("no file picker");
            }
            return;
        }

        Intent send = new Intent(Intent.ACTION_SEND);
        send.setType(mime);
        send.putExtra(Intent.EXTRA_STREAM, uri);
        if (!subject.isEmpty()) { send.putExtra(Intent.EXTRA_SUBJECT, subject); }
        if (!text.isEmpty()) { send.putExtra(Intent.EXTRA_TEXT, text); }
        // Bez ClipData některé aplikace oprávnění ke čtení přílohy nedostanou
        // a zprávu otevřou bez ní.
        send.setClipData(ClipData.newRawUri(name, uri));
        send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);

        Activity activity = getActivity();
        if ("mail".equals(mode)) {
            // Selektor mailto: omezí nabídku na e-mailové aplikace, ale akce
            // zůstává SEND, takže příloha jde s sebou.
            Intent mail = new Intent(send);
            // Typ musí pryč: systém hledá aplikaci podle selektoru, ale s typem
            // hlavního záměru, a filtr mailto: žádný typ nemá. S typem PDF se
            // pak e-mailová aplikace nenajde (ověřeno v emulátoru s Gmailem).
            // Příloha jde dál přes EXTRA_STREAM a ClipData.
            mail.setType(null);
            mail.setSelector(new Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:")));
            try {
                activity.startActivity(mail);
                call.resolve(result("mail"));
                return;
            } catch (ActivityNotFoundException e) {
                // žádná e-mailová aplikace: nabídneme obecné sdílení
            }
        }

        Intent chooser = Intent.createChooser(send, title.isEmpty() ? null : title);
        chooser.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        try {
            activity.startActivity(chooser);
            call.resolve(result("share"));
        } catch (ActivityNotFoundException e) {
            call.reject("no app to share with");
        }
    }

    @ActivityCallback
    private void saveResult(PluginCall call, ActivityResult result) {
        if (call == null) { return; }
        if (result.getResultCode() != Activity.RESULT_OK || result.getData() == null || result.getData().getData() == null) {
            call.resolve(result("cancel"));
            return;
        }
        File src = new File(new File(getContext().getCacheDir(), "doklady"), safeName(call.getString("file", "")));
        if (!src.isFile()) {
            call.reject("nothing to save");
            return;
        }
        Uri target = result.getData().getData();
        try (InputStream in = new FileInputStream(src);
             OutputStream out = getContext().getContentResolver().openOutputStream(target, "wt")) {
            if (out == null) {
                call.reject("cannot open target");
                return;
            }
            byte[] buf = new byte[16384];
            int n;
            while ((n = in.read(buf)) > 0) { out.write(buf, 0, n); }
            call.resolve(result("saved"));
        } catch (Exception e) {
            call.reject("save failed: " + e.getMessage());
        }
    }

    private File writeCache(String name, byte[] bytes) throws Exception {
        File dir = new File(getContext().getCacheDir(), "doklady");
        if (!dir.exists() && !dir.mkdirs()) { throw new Exception("no cache dir"); }
        File file = new File(dir, name);
        try (FileOutputStream out = new FileOutputStream(file)) {
            out.write(bytes);
        }
        return file;
    }

    private static JSObject result(String how) {
        JSObject r = new JSObject();
        r.put("result", how);
        return r;
    }

    /** Jen bezpečné znaky, ať název nemůže ukázat mimo složku s doklady. */
    private static String safeName(String name) {
        String n = name == null ? "" : name.replaceAll("[^A-Za-z0-9._-]", "-");
        if (n.isEmpty() || n.startsWith(".")) { n = "doklad" + n; }
        String low = n.toLowerCase();
        if (!low.endsWith(".pdf") && !low.endsWith(".json")) { n = n + ".pdf"; }
        return n;
    }
}
