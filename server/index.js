// Tapkasa sync relay
//
// Malý přeposílač zpráv, kompatibilní s podmnožinou protokolu ntfy, kterou
// aplikace Tapkasa používá pro párování dvou zařízení:
//
//   POST /<topic>                      tělo = text zprávy → uloží obálku
//                                      {id,time,event:"message",topic,message}
//                                      a vrátí ji jako JSON
//   GET  /<topic>/json?poll=1&since=…  řádkovaný JSON obálek (time >= since;
//                                      since je unix čas v sekundách, nebo
//                                      délka jako "60s"/"5m" = posledních N)
//   GET  /<topic>/sse?since=…          text/event-stream; nejdřív {event:"open"},
//                                      pak přehrání starších zpráv, pak živě
//   GET  /healthz                      {ok:true,topics:n}
//
// Zprávy žijí jen v paměti (výchozí 12 hodin, max 500 na téma). Relay data
// nijak nečte ani neukládá na disk — je to jen trubka mezi dvěma zařízeními.

import http from "node:http";
import crypto from "node:crypto";
import { pathToFileURL } from "node:url";

const TOPIC_RE = /^[A-Za-z0-9_-]{4,64}$/;
const DURATION_RE = /^(\d{1,9})(s|m|h|d)$/;
const DURATION_SEC = { s: 1, m: 60, h: 3600, d: 86400 };

const JSON_TYPE = "application/json";

function newId() {
  // 12 znaků [A-Za-z0-9_-], stejný tvar jako id z ntfy
  return crypto.randomBytes(9).toString("base64url");
}

export function createRelay(opts = {}) {
  const cfg = {
    retentionMs: opts.retentionMs ?? 12 * 60 * 60 * 1000,
    maxPerTopic: opts.maxPerTopic ?? 500,
    maxBodyBytes: opts.maxBodyBytes ?? 8 * 1024,
    rateLimit: opts.rateLimit ?? 120,          // zpráv…
    rateWindowMs: opts.rateWindowMs ?? 5 * 60 * 1000, // …za okno, na jednu IP
    heartbeatMs: opts.heartbeatMs ?? 30 * 1000,
    pruneIntervalMs: opts.pruneIntervalMs ?? 60 * 1000,
    now: opts.now ?? Date.now,
    log: opts.log ?? (() => {}),
  };

  // topic -> { messages: [obálky, od nejstarší], subs: Set<{req,res}> }
  const topics = new Map();
  // ip -> { tokens, last }  (token bucket)
  const buckets = new Map();
  // všichni SSE klienti napříč tématy (kvůli heartbeatu a vypnutí)
  const clients = new Set();

  function topicOf(name) {
    let t = topics.get(name);
    if (!t) {
      t = { messages: [], subs: new Set() };
      topics.set(name, t);
    }
    return t;
  }

  // ---------- rate limit ----------

  function clientIp(req) {
    const fly = req.headers["fly-client-ip"];
    if (typeof fly === "string" && fly) { return fly.trim(); }
    const xff = req.headers["x-forwarded-for"];
    if (typeof xff === "string" && xff) { return xff.split(",")[0].trim(); }
    return req.socket.remoteAddress || "unknown";
  }

  function allowPublish(ip) {
    const now = cfg.now();
    let b = buckets.get(ip);
    if (!b) {
      b = { tokens: cfg.rateLimit, last: now };
      buckets.set(ip, b);
    }
    b.tokens = Math.min(
      cfg.rateLimit,
      b.tokens + (now - b.last) * (cfg.rateLimit / cfg.rateWindowMs)
    );
    b.last = now;
    if (b.tokens < 1) { return false; }
    b.tokens -= 1;
    return true;
  }

  // ---------- since ----------

  // Vrací unix sekundy, null = bez přehrávání (parametr chybí),
  // undefined = nevalidní hodnota (→ 400).
  function parseSince(raw) {
    if (raw == null || raw === "") { return null; }
    if (raw === "all") { return 0; }
    if (/^\d{1,12}$/.test(raw)) { return Number(raw); }
    const m = DURATION_RE.exec(raw);
    if (m) {
      return Math.floor(cfg.now() / 1000) - Number(m[1]) * DURATION_SEC[m[2]];
    }
    return undefined;
  }

  // ---------- odpovědi ----------

  function baseHeaders(res) {
    res.setHeader("Access-Control-Allow-Origin", "*");
  }

  function sendJson(res, status, obj) {
    const body = JSON.stringify(obj) + "\n";
    res.writeHead(status, {
      "Content-Type": JSON_TYPE,
      "Content-Length": Buffer.byteLength(body),
    });
    res.end(body);
  }

  function sendError(res, httpStatus, code, message) {
    sendJson(res, httpStatus, { code, http: httpStatus, error: message });
  }

  // ---------- publikace ----------

  function publish(topicName, body, res) {
    const envelope = {
      id: newId(),
      time: Math.floor(cfg.now() / 1000),
      event: "message",
      topic: topicName,
      message: body,
    };
    const t = topicOf(topicName);
    t.messages.push(envelope);
    while (t.messages.length > cfg.maxPerTopic) { t.messages.shift(); }

    const line = "data: " + JSON.stringify(envelope) + "\n\n";
    for (const c of t.subs) {
      try { c.res.write(line); } catch { dropClient(c); }
    }
    sendJson(res, 200, envelope);
  }

  function handlePublish(req, res, topicName) {
    if (!allowPublish(clientIp(req))) {
      sendError(res, 429, 42901,
        "too many requests: message rate limit reached, try again later");
      req.resume();
      return;
    }
    const declared = Number(req.headers["content-length"]);
    if (Number.isFinite(declared) && declared > cfg.maxBodyBytes) {
      sendError(res, 413, 41301, "message too large");
      req.resume();
      return;
    }
    const chunks = [];
    let size = 0;
    let finished = false;
    req.on("data", (chunk) => {
      if (finished) { return; }
      size += chunk.length;
      if (size > cfg.maxBodyBytes) {
        finished = true;
        sendError(res, 413, 41301, "message too large");
        req.resume();
        // kdyby klient dál sypal data, po chvíli spojení utneme
        setTimeout(() => req.destroy(), 1000).unref?.();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => {
      if (finished) { return; }
      finished = true;
      publish(topicName, Buffer.concat(chunks).toString("utf8"), res);
    });
    req.on("error", () => { finished = true; });
  }

  // ---------- poll ----------

  function handlePoll(req, res, topicName, url) {
    const since = parseSince(url.searchParams.get("since"));
    if (since === undefined) {
      sendError(res, 400, 40008, "invalid since parameter");
      return;
    }
    const t = topics.get(topicName);
    let body = "";
    if (t && since !== null) {
      for (const env of t.messages) {
        if (env.time >= since) { body += JSON.stringify(env) + "\n"; }
      }
    }
    res.writeHead(200, {
      "Content-Type": "application/x-ndjson",
      "Content-Length": Buffer.byteLength(body),
    });
    res.end(body);
  }

  // ---------- SSE ----------

  function dropClient(c) {
    if (!clients.has(c)) { return; }
    clients.delete(c);
    const t = topics.get(c.topic);
    if (t) { t.subs.delete(c); }
    try { c.res.destroy(); } catch { /* už je pryč */ }
  }

  function handleSse(req, res, topicName, url) {
    const since = parseSince(url.searchParams.get("since"));
    if (since === undefined) {
      sendError(res, 400, 40008, "invalid since parameter");
      return;
    }
    res.writeHead(200, {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache",
      "X-Accel-Buffering": "no", // ať proxy proud nebufferuje
    });
    res.write("data: " + JSON.stringify({
      id: newId(),
      time: Math.floor(cfg.now() / 1000),
      event: "open",
      topic: topicName,
    }) + "\n\n");

    const t = topicOf(topicName);
    if (since !== null) {
      for (const env of t.messages) {
        if (env.time >= since) {
          res.write("data: " + JSON.stringify(env) + "\n\n");
        }
      }
    }

    const client = { req, res, topic: topicName };
    clients.add(client);
    t.subs.add(client);
    res.on("error", () => {});   // zavřený stream nesmí shodit proces
    req.on("error", () => {});
    res.on("close", () => dropClient(client));
  }

  // ---------- úklid ----------

  function prune() {
    const cutoff = Math.floor((cfg.now() - cfg.retentionMs) / 1000);
    for (const [name, t] of topics) {
      while (t.messages.length && t.messages[0].time < cutoff) {
        t.messages.shift();
      }
      if (!t.messages.length && !t.subs.size) { topics.delete(name); }
    }
    const staleBefore = cfg.now() - cfg.rateWindowMs * 2;
    for (const [ip, b] of buckets) {
      if (b.last < staleBefore) { buckets.delete(ip); }
    }
  }

  const pruneTimer = setInterval(prune, cfg.pruneIntervalMs);
  pruneTimer.unref?.();

  const heartbeatTimer = setInterval(() => {
    for (const c of clients) {
      try {
        // komentářový řádek: EventSource ho ignoruje, proxy díky němu
        // nechají spojení otevřené
        c.res.write(": keepalive\n\n");
      } catch {
        dropClient(c);
      }
    }
  }, cfg.heartbeatMs);
  heartbeatTimer.unref?.();

  // ---------- router ----------

  const server = http.createServer((req, res) => {
    baseHeaders(res);

    let url;
    try {
      url = new URL(req.url, "http://relay.local");
    } catch {
      sendError(res, 400, 40001, "invalid request");
      return;
    }
    const parts = url.pathname.split("/").filter(Boolean);

    if (req.method === "OPTIONS") {
      res.writeHead(204, {
        "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Max-Age": "86400",
      });
      res.end();
      return;
    }

    if (parts.length === 0) {
      if (req.method === "GET" || req.method === "HEAD") {
        sendJson(res, 200, { ok: true, service: "tapkasa-sync" });
      } else {
        sendError(res, 404, 40401, "not found");
      }
      return;
    }

    if (parts.length === 1 && parts[0] === "healthz" && req.method === "GET") {
      sendJson(res, 200, { ok: true, topics: topics.size });
      return;
    }

    // odsud dál jsou všechny cesty tvaru /<topic>[/json|/sse]
    const topicName = parts[0];
    const isTopicRoute =
      parts.length === 1 ||
      (parts.length === 2 && (parts[1] === "json" || parts[1] === "sse"));
    if (!isTopicRoute) {
      sendError(res, 404, 40401, "not found");
      return;
    }
    if (!TOPIC_RE.test(topicName)) {
      sendError(res, 400, 40009,
        "invalid topic: allowed are 4-64 characters [A-Za-z0-9_-]");
      req.resume();
      return;
    }

    if (parts.length === 1) {
      if (req.method === "POST" || req.method === "PUT") {
        handlePublish(req, res, topicName);
      } else {
        sendError(res, 404, 40401, "not found");
      }
      return;
    }

    if (req.method !== "GET") {
      sendError(res, 404, 40401, "not found");
      return;
    }
    if (parts[1] === "json") {
      handlePoll(req, res, topicName, url);
    } else {
      handleSse(req, res, topicName, url);
    }
  });

  // ať dlouhé SSE spojení nezabije žádný timeout na soketu
  server.setTimeout(0);

  function close(done) {
    clearInterval(pruneTimer);
    clearInterval(heartbeatTimer);
    for (const c of [...clients]) {
      try { c.res.end(); } catch { /* nevadí */ }
      dropClient(c);
    }
    server.close(() => { if (done) { done(); } });
    server.closeIdleConnections?.();
    server.closeAllConnections?.();
  }

  return { server, close, cfg, topics, prune };
}

// ---------- spuštění jako program ----------

const isMain =
  process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;

if (isMain) {
  const env = process.env;
  const num = (v, fallback) => {
    const n = Number(v);
    return Number.isFinite(n) && n > 0 ? n : fallback;
  };

  const relay = createRelay({
    rateLimit: num(env.RATE_LIMIT, 120),
    rateWindowMs: num(env.RATE_WINDOW_SEC, 300) * 1000,
    retentionMs: num(env.RETENTION_HOURS, 12) * 60 * 60 * 1000,
    maxPerTopic: num(env.MAX_PER_TOPIC, 500),
  });

  const port = num(env.PORT, 8080);
  relay.server.listen(port, () => {
    console.log(`tapkasa-sync relay listening on :${port}`);
  });

  let shuttingDown = false;
  const shutdown = (signal) => {
    if (shuttingDown) { return; }
    shuttingDown = true;
    console.log(`${signal} received, shutting down`);
    relay.close(() => process.exit(0));
    setTimeout(() => process.exit(0), 5000).unref();
  };
  process.on("SIGTERM", () => shutdown("SIGTERM"));
  process.on("SIGINT", () => shutdown("SIGINT"));
}
