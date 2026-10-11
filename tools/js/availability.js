/* Bulk domain availability through registry RDAP (404 = no registration), DNS as a fallback. */
(function () {
  'use strict';
  var DV = window.DV, RDAP = window.RDAP;
  var MAX_NAMES = 20, MAX_CHECKS = 200;
  var form = document.getElementById('avail-form');
  var out = document.getElementById('avail-results');
  var status = document.getElementById('avail-status');
  var btnCsv = document.getElementById('avail-csv');
  var onlyFree = document.getElementById('avail-only-free');
  var lastRows = [], lastResults = [];

  function label(raw) {
    var s = String(raw).trim().toLowerCase().replace(/\s+/g, '');
    if (!s) return null;
    var host;
    try { host = new URL('http://' + s + '.com').hostname; } catch (e) { return null; }
    var l = host.slice(0, -4);
    return /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(l) ? l : null;
  }

  function dnsCheck(domain) {
    var url = 'https://cloudflare-dns.com/dns-query?name=' + encodeURIComponent(domain) + '&type=NS';
    return DV.getJson(url, { headers: { accept: 'application/dns-json' }, timeout: 10000 }).then(function (res) {
      if (!res.ok || !res.json) return { state: 'unknown' };
      if (res.json.Status === 3) return { state: 'nodns' };
      if (res.json.Status === 0) return { state: 'taken-dns' };
      return { state: 'unknown' };
    });
  }

  function check(domain) {
    return RDAP.lookup(domain).then(function (r) {
      if (r.state === 'registered') {
        var s = RDAP.summarize(r.data);
        return { domain: domain, result: 'taken', expires: s.expires, registrar: s.registrar, source: r.server + ' (RDAP)' };
      }
      if (r.state === 'free') return { domain: domain, result: 'free', source: r.server + ' (RDAP 404)' };
      return dnsCheck(domain).then(function (d) {
        var why = r.message || '';
        if (d.state === 'nodns') return { domain: domain, result: 'maybe', source: 'DNS only', note: why };
        if (d.state === 'taken-dns') return { domain: domain, result: 'taken', source: 'DNS only', note: why };
        return { domain: domain, result: 'unknown', source: '', note: why || 'No answer from the registry or DNS.' };
      });
    });
  }

  var LABEL = {
    free: '<span class="pill ok">likely available</span>',
    taken: '<span class="pill bad">registered</span>',
    maybe: '<span class="pill warn">no DNS, unconfirmed</span>',
    unknown: '<span class="pill dim">unknown</span>',
  };
  var TEXT = { free: 'likely available', taken: 'registered', maybe: 'no DNS, unconfirmed', unknown: 'unknown' };

  function render() {
    var rows = lastResults.filter(function (r) { return !onlyFree.checked || r.result === 'free' || r.result === 'maybe'; });
    if (!lastResults.length) { out.innerHTML = ''; return; }
    var h = '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Domain</th><th>Result</th><th>Expires</th><th>Registrar</th><th>Checked with</th></tr></thead><tbody>';
    if (!rows.length) h += '<tr><td colspan="5" class="empty">No available names in this list.</td></tr>';
    rows.forEach(function (r) {
      h += '<tr><td class="v">' + DV.esc(r.domain) + '</td><td>' + LABEL[r.result] + (r.note ? '<span class="sub">' + DV.esc(r.note) + '</span>' : '') + '</td><td class="nowrap">' + DV.esc(DV.fmtDate(r.expires)) + '</td><td>' + DV.esc(r.registrar || '') + '</td><td class="sub">' + DV.esc(r.source) + '</td></tr>';
    });
    out.innerHTML = h + '</tbody></table></div>';
  }

  onlyFree.addEventListener('change', render);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var entries = DV.unique(DV.splitList(form.names.value));
    var tlds = Array.prototype.slice.call(form.querySelectorAll('input[name="tld"]:checked')).map(function (x) { return x.value; });
    status.className = 'status';
    if (!entries.length) { status.className = 'status err'; status.textContent = 'Enter at least one name, for example mybrand or mybrand.io.'; return; }
    var note = '';
    if (entries.length > MAX_NAMES) { note += ' Only the first ' + MAX_NAMES + ' names were checked.'; entries = entries.slice(0, MAX_NAMES); }
    var domains = [], bad = [];
    entries.forEach(function (x) {
      if (x.indexOf('.') >= 0) {
        var d = DV.toDomain(x);
        if (d) domains.push(RDAP.registrable(d)); else bad.push(x);
      } else {
        var l = label(x);
        if (!l) { bad.push(x); return; }
        if (!tlds.length) { bad.push(x); return; }
        tlds.forEach(function (t) { domains.push(l + '.' + t); });
      }
    });
    domains = DV.unique(domains);
    if (bad.length) note += ' Skipped ' + bad.length + ' entr' + (bad.length === 1 ? 'y' : 'ies') + (tlds.length ? ' that are not valid names: ' : ' (pick at least one extension for bare names): ') + bad.slice(0, 3).join(', ') + (bad.length > 3 ? ', ...' : '') + '.';
    if (!domains.length) { status.className = 'status err'; status.textContent = 'Nothing to check.' + note; return; }
    if (domains.length > MAX_CHECKS) { note += ' Limited to ' + MAX_CHECKS + ' checks.'; domains = domains.slice(0, MAX_CHECKS); }
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    status.innerHTML = '<span class="spin"></span> Loading the registry list...';
    RDAP.loadBootstrap().then(function () {
      var done = 0;
      return DV.pool(domains, 4, function (d) {
        return check(d).then(function (r) { done++; status.innerHTML = '<span class="spin"></span> ' + done + ' of ' + domains.length + ' checked...'; return r; });
      });
    }).then(function (results) {
      lastResults = results;
      lastRows = results.map(function (r) { return [r.domain, TEXT[r.result], DV.fmtDate(r.expires), r.registrar || '', r.source, r.note || '']; });
      render();
      btnCsv.hidden = false;
      var free = results.filter(function (r) { return r.result === 'free'; }).length;
      status.textContent = 'Done: ' + results.length + ' checked, ' + free + ' likely available.' + note;
    }).catch(function (err) {
      status.className = 'status err';
      status.textContent = err && err.message ? err.message : 'Something went wrong. Try again.';
    }).then(function () { btn.disabled = false; });
  });

  btnCsv.addEventListener('click', function () {
    DV.downloadCsv('domain-availability.csv', ['domain', 'result', 'expires', 'registrar', 'checked_with', 'note'], lastRows);
  });
})();
