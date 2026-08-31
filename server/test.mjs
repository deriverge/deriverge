// Testy pro tapkasa-sync relay.
// Spuštění: node --test test.mjs   (nebo npm test)

import test from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import { once } from "node:events";
import { createRelay } from "./index.js";

const HOST = "127.0.0.1";

async function startRelay(t, opts = {}) {
  const relay = createRelay(opts);
  relay.server.listen(0, HOST);
  await once(relay.server, "listening");
  const port = relay.server.address().port;
  t.after(() => new Promise((resolve) => relay.close(resolve)));
  return { relay, port };
}

// Malý HTTP klient nad node:http (globální fetch schválně nepoužíváme).
function request(port, method, path, { body, headers } = {}) {
  return new Promise((resolve, reject) => {
    const req = http.request(
      { host: HOST, port, method, path, headers },
      (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => resolve({
          status: res.statusCode,
          headers: res.headers,
          text: Buffer.concat(chunks).toString("utf8"),
        }));
      }
    );
    req.on("error", reject);
    if (body != null) { req.write(body); }
    req.end();
  });
}

function ndjson(text) {
  return text.split("\n").filter((l) => l.trim()).map((l) => JSON.parse(l));
}

// SSE klient: otevře stream a umí počkat, až dorazí n datových událostí.
function openSse(port, path) {
  const events = [];
  const waiters = [];
  const client = {
    events,
    opened: null,
    close() { req.destroy(); },
    waitFor(n, timeoutMs = 5000) {
      return new Promise((resolve, reject) => {
        const check = () => {
          if (events.length >= n) { resolve(events.slice(0, n)); return true; }
          return false;
        };
        if (check()) { return; }
        const timer = setTimeout(
          () => reject(new Error(`timeout: got ${events.length}/${n} SSE events`)),
          timeoutMs
        );
        waiters.push(() => {
          if (check()) { clearTimeout(timer); return true; }
          return false;
        });
      });
    },
  };
  let buffer = "";
  const req = http.request({ host: HOST, port, method: "GET", path }, (res) => {
    client.response = res;
    res.setEncoding("utf8");
    res.on("data", (chunk) => {
      buffer += chunk;
      let idx;
      while ((idx = buffer.indexOf("\n\n")) !== -1) {
        const block = buffer.slice(0, idx);
        buffer = buffer.slice(idx + 2);
        for (const line of block.split("\n")) {
          if (line.startsWith("data:")) {
            events.push(JSON.parse(line.slice(5).trim()));
          }
        }
      }
      for (let i = waiters.length - 1; i >= 0; i--) {
        if (waiters[i]()) { waiters.splice(i, 1); }
      }
    });
  });
  req.on("error", () => {});
  req.end();
  client.opened = new Promise((resolve, reject) => {
    req.on("response", resolve);
    req.on("error", reject);
  });
  return client;
}

// ---------------------------------------------------------------------------

test("healthz reports ok and topic count", async (t) => {
  const { port } = await startRelay(t);
  let r = await request(port, "GET", "/healthz");
  assert.equal(r.status, 200);
  assert.deepEqual(JSON.parse(r.text), { ok: true, topics: 0 });

  await request(port, "POST", "/kasa-stanek-aaaaa", { body: '{"t":"hi"}' });
  r = await request(port, "GET", "/healthz");
  assert.deepEqual(JSON.parse(r.text), { ok: true, topics: 1 });
});

test("post + poll roundtrip returns the stored envelope", async (t) => {
  const { port } = await startRelay(t);
  const body = '{"t":"sync","event":"Trh","sales":[{"id":"s1","total":120}]}';

  const post = await request(port, "POST", "/kasa-stanek-abc12", { body });
  assert.equal(post.status, 200);
  assert.equal(post.headers["access-control-allow-origin"], "*");
  const env = JSON.parse(post.text);
  assert.equal(env.event, "message");
  assert.equal(env.topic, "kasa-stanek-abc12");
  assert.equal(env.message, body);
  assert.equal(typeof env.id, "string");
  assert.ok(env.id.length >= 8);
  assert.ok(Math.abs(env.time - Date.now() / 1000) < 5);

  const poll = await request(port, "GET", "/kasa-stanek-abc12/json?poll=1&since=60s");
  assert.equal(poll.status, 200);
  const got = ndjson(poll.text);
  assert.equal(got.length, 1);
  assert.deepEqual(got[0], env);

  // jiné téma zprávu nevidí
  const other = await request(port, "GET", "/kasa-stanek-jinde/json?poll=1&since=60s");
  assert.equal(other.status, 200);
  assert.equal(other.text, "");
});

test("since filtering: unix seconds and durations", async (t) => {
  let fakeNow = 1_756_600_000_000; // pevný výchozí čas v ms
  const { port } = await startRelay(t, { now: () => fakeNow });

  const p1 = await request(port, "POST", "/kasa-stanek-since", { body: "m1" });
  const t1 = JSON.parse(p1.text).time;
  fakeNow += 10 * 60 * 1000; // o 10 minut později
  const p2 = await request(port, "POST", "/kasa-stanek-since", { body: "m2" });
  const t2 = JSON.parse(p2.text).time;
  assert.equal(t2, t1 + 600);

  const msgs = async (since) =>
    ndjson((await request(port, "GET",
      `/kasa-stanek-since/json?poll=1&since=${since}`)).text)
      .map((e) => e.message);

  // unixové sekundy: time >= since (včetně hranice)
  assert.deepEqual(await msgs(t1), ["m1", "m2"]);
  assert.deepEqual(await msgs(t1 + 1), ["m2"]);
  assert.deepEqual(await msgs(t2 + 1), []);

  // délky: "posledních N"
  assert.deepEqual(await msgs("5m"), ["m2"]);
  assert.deepEqual(await msgs("1h"), ["m1", "m2"]);
  fakeNow += 10 * 60 * 1000; // dalších 10 minut ticho
  assert.deepEqual(await msgs("5m"), []);
  assert.deepEqual(await msgs("15m"), ["m2"]);
  assert.deepEqual(await msgs("1d"), ["m1", "m2"]);

  // nevalidní since → 400
  const bad = await request(port, "GET", "/kasa-stanek-since/json?poll=1&since=za-chvili");
  assert.equal(bad.status, 400);
});

test("SSE: open event, replay, live push, client cleanup", async (t) => {
  const { relay, port } = await startRelay(t);

  await request(port, "POST", "/kasa-stanek-sse01", { body: "stara" });

  const sse = openSse(port, "/kasa-stanek-sse01/sse?since=60s");
  const res = await sse.opened;
  assert.equal(res.statusCode, 200);
  assert.match(res.headers["content-type"], /^text\/event-stream/);
  assert.equal(res.headers["access-control-allow-origin"], "*");

  const [open, replay] = await sse.waitFor(2);
  assert.equal(open.event, "open");
  assert.equal(open.topic, "kasa-stanek-sse01");
  assert.equal(replay.event, "message");
  assert.equal(replay.message, "stara");

  await request(port, "POST", "/kasa-stanek-sse01", { body: "ziva" });
  const [, , live] = await sse.waitFor(3);
  assert.equal(live.event, "message");
  assert.equal(live.message, "ziva");

  // bez since se nic nepřehrává, jen open + živé zprávy
  const sse2 = openSse(port, "/kasa-stanek-sse01/sse");
  await sse2.opened;
  const [open2] = await sse2.waitFor(1);
  assert.equal(open2.event, "open");
  await request(port, "POST", "/kasa-stanek-sse01", { body: "dalsi" });
  const [, second] = await sse2.waitFor(2);
  assert.equal(second.message, "dalsi");
  assert.equal(sse2.events.length, 2); // žádné přehrané staré zprávy

  // po odpojení klienta relay odběratele zahodí
  sse.close();
  sse2.close();
  await new Promise((r) => setTimeout(r, 100));
  assert.equal(relay.topics.get("kasa-stanek-sse01").subs.size, 0);
});

test("CORS preflight and headers on responses", async (t) => {
  const { port } = await startRelay(t);
  const pre = await request(port, "OPTIONS", "/kasa-stanek-abc12");
  assert.equal(pre.status, 204);
  assert.equal(pre.headers["access-control-allow-origin"], "*");
  assert.match(pre.headers["access-control-allow-methods"], /POST/);
  assert.match(pre.headers["access-control-allow-methods"], /GET/);
  assert.equal(pre.headers["access-control-allow-headers"], "*");

  const poll = await request(port, "GET", "/kasa-stanek-abc12/json?poll=1&since=60s");
  assert.equal(poll.headers["access-control-allow-origin"], "*");
  const health = await request(port, "GET", "/healthz");
  assert.equal(health.headers["access-control-allow-origin"], "*");
});

test("body limit: payload over 8 KB gets 413", async (t) => {
  const { port } = await startRelay(t);

  const ok = await request(port, "POST", "/kasa-stanek-limit", {
    body: "x".repeat(8 * 1024),
  });
  assert.equal(ok.status, 200);

  const big = await request(port, "POST", "/kasa-stanek-limit", {
    body: "x".repeat(8 * 1024 + 1),
  });
  assert.equal(big.status, 413);
  const err = JSON.parse(big.text);
  assert.equal(err.http, 413);
  assert.ok(err.error);

  // velká zpráva se nesměla uložit
  const poll = await request(port, "GET", "/kasa-stanek-limit/json?poll=1&since=60s");
  assert.equal(ndjson(poll.text).length, 1);
});

test("rate limit: token bucket per IP, 429 with ntfy-like JSON, refills", async (t) => {
  let fakeNow = 1_756_600_000_000;
  const { port } = await startRelay(t, {
    now: () => fakeNow,
    rateLimit: 3,
    rateWindowMs: 60_000,
  });

  for (let i = 0; i < 3; i++) {
    const r = await request(port, "POST", "/kasa-stanek-rate1", { body: "m" + i });
    assert.equal(r.status, 200, `message ${i} should pass`);
  }
  const blocked = await request(port, "POST", "/kasa-stanek-rate1", { body: "m3" });
  assert.equal(blocked.status, 429);
  const err = JSON.parse(blocked.text);
  assert.equal(err.http, 429);
  assert.equal(typeof err.code, "number");
  assert.match(err.error, /rate limit/);
  assert.equal(blocked.headers["access-control-allow-origin"], "*");

  // po třetině okna se doplní jeden token
  fakeNow += 20_000;
  const again = await request(port, "POST", "/kasa-stanek-rate1", { body: "m4" });
  assert.equal(again.status, 200);
  const andBlocked = await request(port, "POST", "/kasa-stanek-rate1", { body: "m5" });
  assert.equal(andBlocked.status, 429);
});

test("topic validation: bad names get 400, unknown routes 404", async (t) => {
  const { port } = await startRelay(t);

  assert.equal((await request(port, "POST", "/abc", { body: "x" })).status, 400);
  assert.equal((await request(port, "GET", "/ab!/json?poll=1&since=60s")).status, 400);
  assert.equal((await request(port, "GET", "/%C5%99eka/json?poll=1")).status, 400);
  assert.equal(
    (await request(port, "POST", "/" + "a".repeat(65), { body: "x" })).status,
    400
  );

  // 64 znaků je ještě v pořádku
  assert.equal(
    (await request(port, "POST", "/" + "a".repeat(64), { body: "x" })).status,
    200
  );

  assert.equal((await request(port, "GET", "/kasa-stanek-abc12/nope")).status, 404);
  assert.equal((await request(port, "GET", "/kasa-stanek-abc12")).status, 404);
  assert.equal((await request(port, "DELETE", "/kasa-stanek-abc12")).status, 404);
});

test("per-topic cap keeps only the newest messages", async (t) => {
  const { port } = await startRelay(t, { maxPerTopic: 3 });
  for (let i = 1; i <= 5; i++) {
    await request(port, "POST", "/kasa-stanek-cap01", { body: "m" + i });
  }
  const poll = await request(port, "GET", "/kasa-stanek-cap01/json?poll=1&since=all");
  const got = ndjson(poll.text).map((e) => e.message);
  assert.deepEqual(got, ["m3", "m4", "m5"]);
});

test("retention pruning drops expired messages and empty topics", async (t) => {
  let fakeNow = 1_756_600_000_000;
  const { relay, port } = await startRelay(t, {
    now: () => fakeNow,
    retentionMs: 60 * 60 * 1000,   // 1 h kvůli testu
    pruneIntervalMs: 3_600_000,    // interval tu prakticky neběží, tikáme ručně
  });

  await request(port, "POST", "/kasa-stanek-old01", { body: "stara" });
  fakeNow += 2 * 60 * 60 * 1000; // o 2 hodiny později
  await request(port, "POST", "/kasa-stanek-new01", { body: "nova" });

  let health = JSON.parse((await request(port, "GET", "/healthz")).text);
  assert.equal(health.topics, 2);

  relay.prune(); // ruční tik úklidu

  // stará zpráva je pryč i s prázdným tématem, nová zůstala
  health = JSON.parse((await request(port, "GET", "/healthz")).text);
  assert.equal(health.topics, 1);
  const old = await request(port, "GET", "/kasa-stanek-old01/json?poll=1&since=all");
  assert.equal(old.text, "");
  const fresh = await request(port, "GET", "/kasa-stanek-new01/json?poll=1&since=all");
  assert.equal(ndjson(fresh.text).map((e) => e.message).join(), "nova");
});
