/* Bulk DNS lookup over DNS-over-HTTPS (Cloudflare, Google fallback). Runs in the browser. */
(function () {
  'use strict';
  var DV = window.DV;
  var MAX = 20;
  var TYPES = { A: 1, AAAA: 28, CNAME: 5, MX: 15, NS: 2, TXT: 16, CAA: 257, SOA: 6 };
  var RCODE = { 0: 'NOERROR', 1: 'FORMERR', 2: 'SERVFAIL', 3: 'NXDOMAIN', 4: 'NOTIMP', 5: 'REFUSED' };
  var RESOLVERS = {
    cloudflare: { name: 'Cloudflare', url: function (n, t) { return 'https://cloudflare-dns.com/dns-query?name=' + encodeURIComponent(n) + '&type=' + t; }, headers: { accept: 'application/dns-json' } },
    google: { name: 'Google', url: function (n, t) { return 'https://dns.google/resolve?name=' + encodeURIComponent(n) + '&type=' + t; }, headers: {} },
  };

  var form = document.getElementById('dns-form');
  var out = document.getElementById('dns-results');
  var status = document.getElementById('dns-status');
  var btnCsv = document.getElementById('dns-csv');
  var lastRows = [];

  function txtValue(data) {
    var s = String(data);
    if (s.charAt(0) !== '"') return s;
    var parts = [], re = /"((?:[^"\\]|\\.)*)"/g, m;
    while ((m = re.exec(s))) parts.push(m[1].replace(/\\(.)/g, '$1'));
    return parts.length ? parts.join('') : s;
  }

  function query(name, type, resolverKey) {
    var order = resolverKey === 'google' ? ['google', 'cloudflare'] : ['cloudflare', 'google'];
    function attempt(i) {
      var r = RESOLVERS[order[i]];
      return DV.getJson(r.url(name, type), { headers: r.headers, timeout: 12000 }).then(function (res) {
        if (res.ok && res.json && typeof res.json.Status === 'number') return { json: res.json, resolver: r.name };
        if (i + 1 < order.length) return attempt(i + 1);
        return { error: res.error === 'timeout' ? 'The resolvers did not answer in time.' : 'The DNS resolvers could not be reached (HTTP ' + res.status + ').' };
      });
    }
    return attempt(0);
  }

  function values(json, typeName) {
    var code = typeName === 'DMARC' ? 16 : TYPES[typeName];
    var ans = (json.Answer || []).filter(function (a) { return a.type === code; });
    var rows = ans.map(function (a) {
      var v = code === 16 ? txtValue(a.data) : String(a.data);
      return { ttl: a.TTL, value: v, sort: code === 15 ? parseInt(v, 10) || 0 : 0 };
    });
    if (code === 15) rows.sort(function (x, y) { return x.sort - y.sort; });
    if (typeName === 'DMARC') rows = rows.filter(function (r) { return /^v=DMARC1/i.test(r.value); });
    return rows;
  }

  function render(results) {
    var html = '';
    lastRows = [];
    results.forEach(function (r) {
      var pill;
      if (r.nx) pill = '<span class="pill bad">NXDOMAIN, domain does not exist</span>';
      else if (r.error) pill = '<span class="pill warn">' + DV.esc(r.error) + '</span>';
      else pill = '<span class="pill ok">resolved</span>';
      html += '<article class="card-result"><header><h3>' + DV.esc(r.domain) + '</h3>' + pill + '</header>';
      if (r.rows.length) {
        html += '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Type</th><th class="num">TTL</th><th>Value</th></tr></thead><tbody>';
        r.rows.forEach(function (x) {
          if (x.none) {
            html += '<tr><td class="k">' + x.type + '</td><td class="num"></td><td class="empty">' + DV.esc(x.none) + '</td></tr>';
            lastRows.push([r.domain, x.type, '', '', x.none]);
          } else {
            html += '<tr><td class="k">' + x.type + '</td><td class="num">' + DV.fmtInt(x.ttl) + '</td><td class="v">' + DV.esc(x.value) + '</td></tr>';
            lastRows.push([r.domain, x.type, x.ttl, x.value, '']);
          }
        });
        html += '</tbody></table></div>';
      }
      html += '</article>';
    });
    out.innerHTML = html;
    btnCsv.hidden = !lastRows.length;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var raw = DV.splitList(form.domains.value);
    var domains = DV.unique(raw.map(DV.toDomain).filter(Boolean));
    var bad = raw.filter(function (x) { return !DV.toDomain(x); });
    var types = Array.prototype.slice.call(form.querySelectorAll('input[name="type"]:checked')).map(function (x) { return x.value; });
    status.className = 'status';
    if (!domains.length) { status.className = 'status err'; status.textContent = 'Enter at least one domain name, for example example.com.'; return; }
    if (!types.length) { status.className = 'status err'; status.textContent = 'Choose at least one record type.'; return; }
    var skipped = '';
    if (domains.length > MAX) { skipped = ' Only the first ' + MAX + ' domains are checked here; the rest were skipped.'; domains = domains.slice(0, MAX); }
    if (bad.length) skipped += ' Ignored ' + bad.length + ' entr' + (bad.length === 1 ? 'y' : 'ies') + ' that are not domain names: ' + bad.slice(0, 3).join(', ') + (bad.length > 3 ? ', ...' : '') + '.';
    var resolver = form.resolver.value;
    var jobs = [];
    domains.forEach(function (d) { types.forEach(function (t) { jobs.push({ d: d, t: t }); }); });
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    var done = 0;
    status.innerHTML = '<span class="spin"></span> Querying ' + jobs.length + ' records...';
    DV.pool(jobs, 6, function (j) {
      var name = j.t === 'DMARC' ? '_dmarc.' + j.d : j.d;
      var type = j.t === 'DMARC' ? 'TXT' : j.t;
      return query(name, type, resolver).then(function (res) {
        done++;
        status.innerHTML = '<span class="spin"></span> ' + done + ' of ' + jobs.length + ' records...';
        return res;
      });
    }).then(function (answers) {
      var by = {};
      jobs.forEach(function (j, i) {
        var a = answers[i] || {};
        var r = by[j.d] || (by[j.d] = { domain: j.d, rows: [], nx: false, error: null });
        if (a.error) { r.error = a.error; r.rows.push({ type: j.t, none: 'lookup failed' }); return; }
        var st = a.json.Status;
        if (st === 3 && j.t !== 'DMARC') { r.nx = true; }
        if (st !== 0 && st !== 3) { r.rows.push({ type: j.t, none: 'resolver answered ' + (RCODE[st] || st) }); return; }
        var vals = values(a.json, j.t);
        if (!vals.length) r.rows.push({ type: j.t, none: st === 3 && j.t !== 'DMARC' ? 'no such domain' : 'no records' });
        vals.forEach(function (v) { r.rows.push({ type: j.t, ttl: v.ttl, value: v.value }); });
      });
      render(domains.map(function (d) { return by[d]; }));
      status.className = 'status';
      status.textContent = 'Done: ' + domains.length + ' domain' + (domains.length === 1 ? '' : 's') + ', ' + jobs.length + ' queries through ' + RESOLVERS[resolver].name + ' DNS over HTTPS.' + skipped;
    }).then(function () { btn.disabled = false; }, function () { btn.disabled = false; });
  });

  btnCsv.addEventListener('click', function () {
    DV.downloadCsv('dns-records.csv', ['domain', 'type', 'ttl', 'value', 'note'], lastRows);
  });
})();
