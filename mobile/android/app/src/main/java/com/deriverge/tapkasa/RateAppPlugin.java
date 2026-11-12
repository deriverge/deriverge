package com.deriverge.tapkasa;

import android.app.Activity;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.google.android.play.core.review.ReviewInfo;
import com.google.android.play.core.review.ReviewManager;
import com.google.android.play.core.review.ReviewManagerFactory;

/**
 * Tapkasa: žádost o hodnocení v Google Play (Play In-App Review API).
 * Obdoba RateAppPlugin.swift na iOS se stejným rozhraním pro stránku:
 *
 *   Capacitor.Plugins.RateApp.request()
 *
 * Okno vyvolává Google Play a sám rozhoduje, jestli se vůbec ukáže (kvóta
 * na uživatele, aplikace musí být nainstalovaná z Play, v debug buildu
 * z adb se neukáže). Výsledek se aplikaci nesděluje, proto request vždy
 * skončí úspěchem, i když okno nepřišlo; kdy o hodnocení požádat, řídí
 * webová vrstva (tapkasa/index.html, maybeAskReview).
 */
@CapacitorPlugin(name = "RateApp")
public class RateAppPlugin extends Plugin {

    private ReviewManager manager;
    /** Jedna žádost naráz; druhé ťuknutí během běžící by jen zdvojilo okno. */
    private volatile boolean busy = false;

    @Override
    public void load() {
        manager = ReviewManagerFactory.create(getContext());
    }

    @PluginMethod
    public void request(PluginCall call) {
        Activity activity = getActivity();
        if (manager == null || activity == null || busy) {
            call.resolve();
            return;
        }
        busy = true;
        activity.runOnUiThread(() -> manager.requestReviewFlow().addOnCompleteListener(task -> {
            if (!task.isSuccessful()) {
                // bez Play obchodu, offline nebo vyčerpaná kvóta: stránka jede dál
                busy = false;
                call.resolve();
                return;
            }
            ReviewInfo info = task.getResult();
            Activity current = getActivity();
            if (current == null || current.isFinishing()) {
                busy = false;
                call.resolve();
                return;
            }
            manager.launchReviewFlow(current, info).addOnCompleteListener(done -> {
                busy = false;
                call.resolve();
            });
        }));
    }
}
