package com.deriverge.tapkasa;

import android.speech.tts.TextToSpeech;
import android.speech.tts.UtteranceProgressListener;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Tapkasa: čtení nahlas na Androidu. Webová speechSynthesis v Android WebView
 * mlčí (hlasy se nenačtou a promluva se zahodí), používáme proto systémové
 * TextToSpeech. Na iOS a na webu zůstává speechSynthesis.
 *
 * JS strana (mobile/bridge.js): window.__kasaSpeak(text, locale).
 */
@CapacitorPlugin(name = "Speak")
public class SpeakPlugin extends Plugin {

    private TextToSpeech tts;
    private boolean ready = false;
    /** Co přišlo, než se motor probral. Ztratit poděkování zákazníkovi by bylo horší než ho říct o vteřinu později. */
    private final List<String[]> queued = new ArrayList<>();
    private int seq = 0;

    @Override
    public void load() {
        tts = new TextToSpeech(getContext(), status -> {
            ready = status == TextToSpeech.SUCCESS;
            if (!ready) { return; }
            synchronized (queued) {
                for (String[] q : queued) { say(q[0], q[1]); }
                queued.clear();
            }
        });
    }

    @Override
    protected void handleOnDestroy() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
            tts = null;
        }
        super.handleOnDestroy();
    }

    @PluginMethod
    public void speak(PluginCall call) {
        String text = call.getString("text", "");
        String loc = call.getString("locale", "");
        if (text == null || text.trim().isEmpty()) { call.resolve(); return; }
        if (!ready) {
            synchronized (queued) {
                if (queued.size() < 5) { queued.add(new String[]{ text, loc == null ? "" : loc }); }
            }
            call.resolve();
            return;
        }
        say(text, loc == null ? "" : loc);
        call.resolve();
    }

    @PluginMethod
    public void stop(PluginCall call) {
        if (tts != null) { tts.stop(); }
        call.resolve();
    }

    /** Hlásí, zda je motor připravený a zda umí požadovaný jazyk. */
    @PluginMethod
    public void status(PluginCall call) {
        JSObject o = new JSObject();
        o.put("ready", ready);
        call.resolve(o);
    }

    private void say(String text, String loc) {
        if (tts == null) { return; }
        if (!loc.isEmpty()) {
            Locale want = Locale.forLanguageTag(loc);
            int res = tts.setLanguage(want);
            if (res == TextToSpeech.LANG_MISSING_DATA || res == TextToSpeech.LANG_NOT_SUPPORTED) {
                // jazyk v zařízení chybí; raději výchozí hlas než ticho
                tts.setLanguage(Locale.getDefault());
            }
        }
        tts.setSpeechRate(0.95f);
        seq += 1;
        tts.speak(text, TextToSpeech.QUEUE_ADD, null, "tapkasa-" + seq);
    }
}
