package com.deriverge.tapkasa;

import android.Manifest;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;

import com.getcapacitor.JSObject;
import com.getcapacitor.PermissionState;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.annotation.PermissionCallback;
import com.google.android.gms.nearby.Nearby;
import com.google.android.gms.nearby.connection.AdvertisingOptions;
import com.google.android.gms.nearby.connection.ConnectionInfo;
import com.google.android.gms.nearby.connection.ConnectionLifecycleCallback;
import com.google.android.gms.nearby.connection.ConnectionResolution;
import com.google.android.gms.nearby.connection.ConnectionsClient;
import com.google.android.gms.nearby.connection.DiscoveredEndpointInfo;
import com.google.android.gms.nearby.connection.DiscoveryOptions;
import com.google.android.gms.nearby.connection.EndpointDiscoveryCallback;
import com.google.android.gms.nearby.connection.Payload;
import com.google.android.gms.nearby.connection.PayloadCallback;
import com.google.android.gms.nearby.connection.PayloadTransferUpdate;
import com.google.android.gms.nearby.connection.Strategy;

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

/**
 * Tapkasa: párování dvou a více zařízení (kasa a výdej) bez internetu přes
 * Google Nearby Connections (Wi-Fi a Bluetooth). Obdoba PeerLinkPlugin.swift
 * na iOS se stejným rozhraním pro stránku: start, stop, send, save, status
 * a události message, peerCount, state. Apple a Google protokoly si spolu
 * nerozumí, Android s iPhonem se bez internetu nepropojí.
 *
 * Bez oprávnění k poloze: podporujeme Android 13 a novější, kde stačí
 * NEARBY_WIFI_DEVICES a Bluetooth oprávnění s příznakem neverForLocation.
 * Starší Android hlásí supported=false a párování jde přes internet.
 */
@CapacitorPlugin(
    name = "PeerLink",
    permissions = {
        @Permission(alias = "nearby", strings = {
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.BLUETOOTH_ADVERTISE,
            Manifest.permission.BLUETOOTH_CONNECT,
            Manifest.permission.NEARBY_WIFI_DEVICES
        })
    }
)
public class PeerLinkPlugin extends Plugin {

    /** Musí být stejné na všech zařízeních. */
    private static final String SERVICE_ID = "com.deriverge.tapkasa.kasa-order";
    private static final long RETRY_MS = 20000;

    private final String inst = UUID.randomUUID().toString();
    private final Handler main = new Handler(Looper.getMainLooper());
    private final Set<String> connected = new HashSet<>();
    private final Set<String> pending = new HashSet<>();
    private ConnectionsClient client;
    private String room = "";
    private boolean advertising = false;
    private boolean discovering = false;
    private String pendingRoom = null;

    private final Runnable retry = new Runnable() {
        @Override public void run() {
            retryIfLonely("timer");
            main.postDelayed(this, RETRY_MS);
        }
    };

    private static boolean supported() {
        return Build.VERSION.SDK_INT >= 33;
    }

    private ConnectionsClient client() {
        if (client == null) { client = Nearby.getConnectionsClient(getContext()); }
        return client;
    }

    private String myName() {
        return room + "|" + inst;
    }

    private void state(String phase, String detail) {
        JSObject o = new JSObject();
        o.put("phase", phase);
        o.put("detail", detail == null ? "" : detail);
        notifyListeners("state", o);
    }

    private void announce() {
        JSObject o = new JSObject();
        o.put("n", connected.size());
        notifyListeners("peerCount", o);
    }

    // ---- volání ze stránky ------------------------------------------------

    @PluginMethod
    public void start(PluginCall call) {
        String code = call.getString("room", "");
        code = code == null ? "" : code.trim().toUpperCase();
        if (!supported()) {
            state("unsupported", "Android " + Build.VERSION.RELEASE + ", potřeba 13+");
            call.resolve();
            return;
        }
        if (code.isEmpty()) {
            final String empty = code;
            main.post(() -> { stopOnMain(); room = empty; });
            call.resolve();
            return;
        }
        if (getPermissionState("nearby") == PermissionState.GRANTED) {
            final String c = code;
            main.post(() -> startOnMain(c));
            call.resolve();
        } else {
            pendingRoom = code;
            state("permission", "žádám o oprávnění Zařízení v okolí");
            requestPermissionForAlias("nearby", call, "onNearbyPermission");
        }
    }

    @PermissionCallback
    private void onNearbyPermission(PluginCall call) {
        final String code = pendingRoom == null ? "" : pendingRoom;
        pendingRoom = null;
        if (getPermissionState("nearby") == PermissionState.GRANTED) {
            main.post(() -> startOnMain(code));
        } else {
            state("permission-denied", "bez oprávnění Zařízení v okolí a Bluetooth to nejde");
        }
        call.resolve();
    }

    @PluginMethod
    public void stop(PluginCall call) {
        main.post(() -> { stopOnMain(); room = ""; });
        call.resolve();
    }

    @PluginMethod
    public void send(PluginCall call) {
        String json = call.getString("json");
        if (json == null) { call.reject("Chybí parametr 'json'"); return; }
        final String j = json;
        main.post(() -> {
            if (connected.isEmpty()) { return; }
            byte[] bytes = j.getBytes(StandardCharsets.UTF_8);
            if (bytes.length > ConnectionsClient.MAX_BYTES_DATA_SIZE) {
                state("send-error", "zpráva je příliš velká (" + bytes.length + " B)");
                return;
            }
            client().sendPayload(new ArrayList<>(connected), Payload.fromBytes(bytes));
        });
        call.resolve();
    }

    /** Záloha stavu kasy do souboru aplikace (na Androidu drží data i webview). */
    @PluginMethod
    public void save(PluginCall call) {
        String json = call.getString("json");
        if (json == null) { call.reject("Chybí parametr 'json'"); return; }
        try {
            File f = new File(getContext().getFilesDir(), "kasa.json");
            try (OutputStreamWriter w = new OutputStreamWriter(new FileOutputStream(f), StandardCharsets.UTF_8)) {
                w.write(json);
            }
        } catch (Exception e) {
            // záloha je jen pojistka, chyba nesmí shodit ukládání ve stránce
        }
        call.resolve();
    }

    @PluginMethod
    public void status(PluginCall call) {
        JSObject o = new JSObject();
        o.put("room", room);
        o.put("advertising", advertising);
        o.put("browsing", discovering);
        o.put("peers", connected.size());
        o.put("name", Build.MODEL);
        o.put("supported", supported());
        call.resolve(o);
    }

    @Override
    protected void handleOnResume() {
        super.handleOnResume();
        main.post(() -> retryIfLonely("foreground"));
    }

    // ---- hledání a spojení (hlavní vlákno) ---------------------------------

    private void startOnMain(String code) {
        if (code.equals(room) && (advertising || discovering)) { return; }
        stopOnMain();
        room = code;
        if (room.isEmpty()) { return; }
        beginDiscovery();
        state("started", room);
        main.removeCallbacks(retry);
        main.postDelayed(retry, RETRY_MS);
    }

    private void stopOnMain() {
        main.removeCallbacks(retry);
        endDiscovery();
        if (client != null) { client.stopAllEndpoints(); }
        connected.clear();
        pending.clear();
        announce();
    }

    private void beginDiscovery() {
        AdvertisingOptions ao = new AdvertisingOptions.Builder().setStrategy(Strategy.P2P_CLUSTER).build();
        DiscoveryOptions dopt = new DiscoveryOptions.Builder().setStrategy(Strategy.P2P_CLUSTER).build();
        client().startAdvertising(myName(), SERVICE_ID, lifecycle, ao)
            .addOnSuccessListener(v -> advertising = true)
            .addOnFailureListener(e -> { advertising = false; state("advertise-error", String.valueOf(e.getMessage())); });
        client().startDiscovery(SERVICE_ID, discovery, dopt)
            .addOnSuccessListener(v -> discovering = true)
            .addOnFailureListener(e -> { discovering = false; state("browse-error", String.valueOf(e.getMessage())); });
    }

    private void endDiscovery() {
        if (client != null) {
            client.stopAdvertising();
            client.stopDiscovery();
        }
        advertising = false;
        discovering = false;
    }

    /** Bez protějšku se hledání obnoví; spojená zařízení se nechávají být. */
    private void retryIfLonely(String why) {
        if (room.isEmpty() || !connected.isEmpty() || !pending.isEmpty()) { return; }
        endDiscovery();
        beginDiscovery();
        state("retry", why);
    }

    private static String roomOf(String endpointName) {
        if (endpointName == null) { return ""; }
        int i = endpointName.indexOf('|');
        return i < 0 ? endpointName : endpointName.substring(0, i);
    }

    private static String instOf(String endpointName) {
        if (endpointName == null) { return ""; }
        int i = endpointName.indexOf('|');
        return i < 0 ? "" : endpointName.substring(i + 1);
    }

    private final EndpointDiscoveryCallback discovery = new EndpointDiscoveryCallback() {
        @Override public void onEndpointFound(String endpointId, DiscoveredEndpointInfo info) {
            String name = info.getEndpointName();
            state("found", roomOf(name));
            if (room.isEmpty() || !room.equals(roomOf(name))) { return; }
            String theirInst = instOf(name);
            if (theirInst.equals(inst)) { return; }            // našli jsme sami sebe
            if (connected.contains(endpointId) || pending.contains(endpointId)) { return; }
            // zve jen zařízení s menším otiskem, ať se obě nezvou naráz
            if (inst.compareTo(theirInst) < 0) {
                pending.add(endpointId);
                client().requestConnection(myName(), endpointId, lifecycle)
                    .addOnFailureListener(e -> { pending.remove(endpointId); state("invite-error", String.valueOf(e.getMessage())); });
            }
        }

        @Override public void onEndpointLost(String endpointId) {
            state("lost", endpointId);
        }
    };

    private final ConnectionLifecycleCallback lifecycle = new ConnectionLifecycleCallback() {
        @Override public void onConnectionInitiated(String endpointId, ConnectionInfo info) {
            boolean ok = !room.isEmpty() && room.equals(roomOf(info.getEndpointName()))
                && !inst.equals(instOf(info.getEndpointName()));
            state("invited", (info.isIncomingConnection() ? "příchozí " : "odchozí ") + (ok ? "accepted" : "rejected"));
            if (ok) {
                pending.add(endpointId);
                client().acceptConnection(endpointId, payloads);
            } else {
                client().rejectConnection(endpointId);
            }
        }

        @Override public void onConnectionResult(String endpointId, ConnectionResolution result) {
            pending.remove(endpointId);
            if (result.getStatus().isSuccess()) {
                connected.add(endpointId);
                state("session", "connected, n=" + connected.size());
            } else {
                state("session", "failed " + result.getStatus().getStatusCode() + ", n=" + connected.size());
            }
            announce();
        }

        @Override public void onDisconnected(String endpointId) {
            connected.remove(endpointId);
            pending.remove(endpointId);
            state("session", "disconnected, n=" + connected.size());
            announce();
        }
    };

    private final PayloadCallback payloads = new PayloadCallback() {
        @Override public void onPayloadReceived(String endpointId, Payload payload) {
            if (payload.getType() != Payload.Type.BYTES || payload.asBytes() == null) { return; }
            String json = new String(payload.asBytes(), StandardCharsets.UTF_8);
            JSObject o = new JSObject();
            o.put("json", json);
            notifyListeners("message", o);
        }

        @Override public void onPayloadTransferUpdate(String endpointId, PayloadTransferUpdate update) {}
    };
}
