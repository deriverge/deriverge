package com.deriverge.tapkasa;

import android.os.Bundle;
import android.webkit.WebView;

import androidx.activity.OnBackPressedCallback;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        // Lokální plugin (párování bez internetu) není npm balíček,
        // registruje se ručně, a to před startem mostu.
        registerPlugin(PeerLinkPlugin.class);
        registerPlugin(SpeakPlugin.class);
        registerPlugin(DocSharePlugin.class);
        super.onCreate(savedInstanceState);

        // Tlačítko či gesto Zpět nejdřív zavře otevřený panel, dialog nebo
        // průvodce (stránka to řeší v window.__kasaBack). Aplikaci opustí,
        // až když na stránce není co zavřít; dřív odešlo z pokladny i uprostřed
        // placení.
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                WebView web = getBridge() != null ? getBridge().getWebView() : null;
                if (web == null) { leave(); return; }
                web.evaluateJavascript(
                    "(function(){try{return window.__kasaBack&&window.__kasaBack()?'1':'0'}catch(e){return '0'}})()",
                    value -> { if (!"\"1\"".equals(value)) { leave(); } });
            }

            private void leave() {
                setEnabled(false);
                getOnBackPressedDispatcher().onBackPressed();
                setEnabled(true);
            }
        });
    }
}
