# tapkasa-sync, přeposílač pro párování zařízení Tapkasa

Malý server, přes který si dvě spárovaná zařízení s aplikací Tapkasa posílají
objednávky (kasa ↔ výdejní místo). Mluví stejným protokolem jako veřejná
služba [ntfy](https://ntfy.sh), přesněji její podmnožinou, kterou aplikace
používá, takže aplikace funguje beze změny kódu, jen se jí řekne jiná adresa.

Proč vlastní relay místo veřejného ntfy.sh: žádné cizí denní limity, žádná
cizí infrastruktura v cestě prodejním datům a plná kontrola nad dostupností.

## Co server dělá (a nedělá)

- Přijme zprávu (`POST /<téma>`), uloží ji **jen do paměti** a rozešle všem,
  kdo dané téma poslouchají. Na disk se nezapisuje nic.
- Zprávy žijí 12 hodin, na jedno téma se drží nejvýš 500 posledních zpráv.
- Témata jsou náhodné kódy tvaru `kasa-stanek-XXXXX` (povolené znaky
  `A-Za-z0-9_-`, délka 4-64). Kdo kód nezná, téma neuvidí.
- Limit 8 kB na zprávu (aplikace posílá zprávy o ~300-600 B) a 120 zpráv za
  5 minut na jednu IP adresu.
- Server data nečte, neanalyzuje, neloguje obsah, je to jen trubka.

### Protokol (ntfy-kompatibilní podmnožina)

| Endpoint | Popis |
| --- | --- |
| `POST /<téma>` | tělo = text zprávy; vrátí uloženou obálku `{id, time, event:"message", topic, message}` jako JSON |
| `GET /<téma>/json?poll=1&since=…` | řádkovaný JSON obálek s `time >= since`; `since` je unixový čas v sekundách, nebo délka jako `60s` / `5m` (= posledních N) |
| `GET /<téma>/sse?since=…` | `text/event-stream`: nejdřív `{event:"open"}`, pak přehrání starších zpráv podle `since`, pak živý tok; každých 30 s komentářový řádek, ať proxy spojení nezavírají |
| `GET /healthz` | `{ok:true, topics:n}`, pro health check |

CORS je povolený pro všechny (`Access-Control-Allow-Origin: *`), včetně
OPTIONS preflightů, aplikace běží i jako webová stránka z jiné domény.

## Spuštění lokálně

Stačí Node.js 22+, žádné závislosti se neinstalují:

```bash
cd server
node index.js                 # běží na http://localhost:8080
PORT=3000 node index.js       # jiný port
```

Rychlá zkouška z druhého terminálu:

```bash
curl http://localhost:8080/healthz
curl -d '{"t":"hi"}' http://localhost:8080/kasa-stanek-test1
curl 'http://localhost:8080/kasa-stanek-test1/json?poll=1&since=5m'
curl 'http://localhost:8080/kasa-stanek-test1/sse?since=5m'   # živý proud, ukonči Ctrl+C
```

Testy:

```bash
node --test test.mjs          # nebo: npm test
```

### Konfigurace přes proměnné prostředí

| Proměnná | Výchozí | Význam |
| --- | --- | --- |
| `PORT` | `8080` | port, na kterém server poslouchá |
| `RATE_LIMIT` | `120` | kolik zpráv smí jedna IP poslat za okno |
| `RATE_WINDOW_SEC` | `300` | délka okna rate limitu v sekundách |
| `RETENTION_HOURS` | `12` | jak dlouho zprávy žijí v paměti |
| `MAX_PER_TOPIC` | `500` | strop zpráv na jedno téma |

## Nasazení na Fly.io krok za krokem

1. **Nainstaluj `flyctl`** a přihlas se (účet vyžaduje platební kartu):

   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth signup        # nebo: fly auth login
   ```

2. **Vyber jméno aplikace.** V `fly.toml` je placeholder `tapkasa-sync`;
   jména jsou na Fly celosvětově unikátní, takže pokud je obsazené, přepiš
   řádek `app = "…"` na vlastní (např. `tapkasa-sync-prod`).

3. **Založ aplikaci a nasaď** (z adresáře `server/`):

   ```bash
   fly launch --copy-config --no-deploy   # převezme fly.toml, nic neměň
   fly deploy
   ```

4. **Zkontroluj, že běží:**

   ```bash
   fly status
   curl https://tapkasa-sync.fly.dev/healthz
   # → {"ok":true,"topics":0}
   ```

5. **Drž právě jeden stroj.** Relay má stav jen v paměti, takže dvě mašiny by
   znamenaly dvě oddělené fronty zpráv. `fly deploy` někdy založí dva stroje
   kvůli vysoké dostupnosti, srovnej to na jeden:

   ```bash
   fly scale count 1
   ```

### Vlastní doména (např. `sync.tapkasa.app`)

1. Vyžádej certifikát:

   ```bash
   fly certs add sync.tapkasa.app
   ```

2. U správce DNS domény přidejte záznam, který příkaz vypíše, typicky CNAME:

   ```
   sync  CNAME  tapkasa-sync.fly.dev.
   ```

   (Alternativně A/AAAA záznamy na adresy z `fly ips list`.)

3. Počkejte na vystavení certifikátu a ověřte:

   ```bash
   fly certs show sync.tapkasa.app
   curl https://sync.tapkasa.app/healthz
   ```

   Sdílená IPv4, kterou Fly přiděluje zdarma, pro vlastní doménu stačí, všechny prohlížeče i WebView umí SNI. Vyhrazenou IPv4 ($2/měs) netřeba.

### Nasměrování aplikace na vlastní relay

Aplikace čte seznam přeposílačů z `window.__KASA_RELAY__`, čárkami oddělené
základní adresy **končící lomítkem**. Když proměnná není nastavená, používá
veřejné `ntfy.sh` a `ntfy.envs.net`. V produkční verzi (webové i zabalené pro
App Store / Google Play) stačí před hlavní skript vložit:

```html
<script>
  window.__KASA_RELAY__ = "https://sync.tapkasa.app/,https://ntfy.sh/";
</script>
```

Aplikace posílá na všechny uvedené adresy naráz a poslouchá na všech, stačí,
aby v danou chvíli fungovala jedna. Nechat `ntfy.sh` jako druhou adresu je
tedy levná záloha pro případ výpadku vlastního relay; kdo ji nechce, uvede
jen vlastní doménu.

## Odhad nákladů

| Položka | Cena |
| --- | --- |
| 1× stroj `shared-cpu-1x`, 256 MB RAM, běží nonstop | ≈ $2/měs |
| Sdílená IPv4 + IPv6 | zdarma |
| Odchozí data (zprávy mají stovky bajtů) | prakticky $0 |
| **Celkem** | **≈ $2-3/měs (cca 50-70 Kč)** |

Pozor: stroj musí běžet pořád (`auto_stop_machines = "off"` ve `fly.toml`), uspání by zahodilo paměť se zprávami a rozpojilo otevřená SSE spojení. Proto
se neuplatní úspora "scale to zero".

## Provozní poznámky

- **Restart = prázdná paměť.** Po nasazení nové verze nebo restartu stroje
  zprávy z posledních hodin zmizí. Aplikaci to nevadí, obě zařízení drží
  vlastní úplnou kopii dat a po připojení si pošlou otevřené objednávky znovu
  (`hi` + dávka `sync` zpráv). Výpadek relay tedy nikdy neztratí prodeje.
- **Škálování:** jeden sdílený CPU zvládne řádově tisíce spárovaných dvojic;
  každá dvojice pošle jednotky zpráv za minutu. Kdyby bylo potřeba víc, řeší
  se to větším strojem (`fly scale vm`), ne více stroji.
- **Logy:** `fly logs`. Server loguje jen start a vypnutí, obsah zpráv ne.
- **Vypnutí:** na SIGTERM server přestane přijímat spojení, zavře SSE proudy
  a skončí, Fly ho tak umí nasadit bez tvrdého zabití.
