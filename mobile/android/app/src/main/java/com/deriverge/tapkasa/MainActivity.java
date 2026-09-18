package com.deriverge.tapkasa;

import android.os.Bundle;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        // Lokální plugin (párování bez internetu) není npm balíček,
        // registruje se ručně, a to před startem mostu.
        registerPlugin(PeerLinkPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
