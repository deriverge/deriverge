/* RDAP (WHOIS) lookup in the browser: registrar, dates, status, nameservers. No contact data is read. */
(function () {
  'use strict';
  var DV = window.DV, RDAP = window.RDAP;
  var MAX = 20;
  var form = document.getElementById('whois-form');
  var out = document.getElementById('whois-results');
  var status = document.getElementById('whois-status');
  var btnCsv = document.getElementById('whois-csv');
  var lastRows = [];

  var STATUS_NOTE = {
    'client transfer prohibited': 'transfer lock set by the registrar',
    'server transfer prohibited': 'transfer lock set by the registry',
    'client delete prohibited': 'delete lock set by the registrar',
    'server delete prohibited': 'delete lock set by the registry',
    'client update prohibited': 'update lock set by the registrar',
    'server update prohibited': 'update lock set by the registry',
    'client hold': 'not in DNS, held by the registrar',
    'server hold': 'not in DNS, held by the registry',
    'redemption period': 'expired, can still be restored',
    'pending delete': 'about to be deleted and released',
    'auto renew period': 'renewed automatically, grace period',
    'active': 'no locks or holds',
  };

  function row(k, v) { return v ? '<dt>' + k + '</dt><dd>' + v + '</dd>' : ''; }

  function card(domain, r) {
    var h = '<article class="card-result"><header><h3>' + DV.esc(domain) + '</h3>';
    if (r.state === 'registered') {
      var s = RDAP.summarize(r.data);
      var left = RDAP.daysUntil(s.expires);
      var pill = left != null && left < 0 ? '<span class="pill bad">expired</span>' : left != null && left <= 30 ? '<span class="pill warn">expires in ' + left + ' days</span>' : '<span class="pill ok">registered</span>';
      h += pill + '</header><div class="body"><dl class="kv">';
      var regLine = s.registrar ? DV.esc(s.registrar) + (s.registrarId ? ' <span class="hint">IANA ID ' + DV.esc(s.registrarId) + '</span>' : '') : '<span class="empty">not published by the registry</span>';
      if (s.registrarUrl && /^https?:\/\//i.test(s.registrarUrl)) regLine += '<br><a href="' + DV.esc(s.registrarUrl) + '" rel="nofollow noopener" target="_blank">' + DV.esc(s.registrarUrl.replace(/^https?:\/\//, '').replace(/\/$/, '')) + '</a>';
      h += row('Registrar', regLine);
      h += row('Created', s.created ? DV.fmtDate(s.created) + ' <span class="hint">' + RDAP.age(s.created) + ' ago</span>' : '');
      h += row('Expires', s.expires ? DV.fmtDate(s.expires) + (left != null ? ' <span class="hint">' + (left >= 0 ? 'in ' + left + ' days' : Math.abs(left) + ' days ago') + '</span>' : '') : '');
      h += row('Last changed', s.updated ? DV.fmtDate(s.updated) : '');
      h += row('Status', s.status.length ? s.status.map(function (x) {
        var n = STATUS_NOTE[String(x).toLowerCase()];
        return DV.esc(x) + (n ? ' <span class="hint">' + n + '</span>' : '');
      }).join('<br>') : '');
      h += row('Nameservers', s.nameservers.length ? s.nameservers.map(DV.esc).join('<br>') : '');
      h += row('DNSSEC', s.dnssec || '');
      h += row('Source', DV.esc(r.server) + ' <span class="hint">registry RDAP</span>');
      h += '</dl></div>';
      lastRows.push([domain, 'registered', s.registrar || '', s.registrarId || '', DV.fmtDate(s.created), DV.fmtDate(s.expires), DV.fmtDate(s.updated), s.status.join(' | '), s.nameservers.join(' | '), s.dnssec || '', r.server]);
    } else if (r.state === 'free') {
      h += '<span class="pill info">not registered</span></header><div class="body">The registry (' + DV.esc(r.server) + ') has no record of this domain, so it is most likely available. Check it with the <a href="/tools/domain-availability-checker/">domain availability checker</a> or at a registrar.</div>';
      lastRows.push([domain, 'not registered', '', '', '', '', '', '', '', '', r.server]);
    } else {
      var msg = r.message || 'Lookup failed.';
      var more = r.state === 'nordap' || r.state === 'blocked' ? ' The Apify actor falls back to the classic WHOIS service for these registries.' : '';
      h += '<span class="pill warn">' + (r.state === 'error' ? 'no answer' : 'not available in the browser') + '</span></header><div class="body">' + DV.esc(msg + more) + '</div>';
      lastRows.push([domain, r.state === 'error' ? 'error' : 'unsupported', '', '', '', '', '', '', '', '', msg]);
    }
    return h + '</article>';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var raw = DV.splitList(form.domains.value);
    var hosts = raw.map(DV.toDomain);
    var bad = raw.filter(function (x, i) { return !hosts[i]; });
    var domains = DV.unique(hosts.filter(Boolean).map(RDAP.registrable));
    status.className = 'status';
    if (!domains.length) { status.className = 'status err'; status.textContent = 'Enter a domain name such as example.com.'; return; }
    var note = '';
    if (domains.length > MAX) { note = ' Only the first ' + MAX + ' domains were checked.'; domains = domains.slice(0, MAX); }
    if (bad.length) note += ' Ignored ' + bad.length + ' entr' + (bad.length === 1 ? 'y' : 'ies') + ' that are not domain names.';
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    status.innerHTML = '<span class="spin"></span> Finding the registry servers...';
    RDAP.loadBootstrap().then(function () {
      var done = 0;
      status.innerHTML = '<span class="spin"></span> Asking the registries...';
      return DV.pool(domains, 4, function (d) {
        return RDAP.lookup(d).then(function (r) { done++; status.innerHTML = '<span class="spin"></span> ' + done + ' of ' + domains.length + '...'; return r; });
      });
    }).then(function (results) {
      lastRows = [];
      out.innerHTML = domains.map(function (d, i) { return card(d, results[i]); }).join('');
      btnCsv.hidden = !lastRows.length;
      status.textContent = 'Done: ' + domains.length + ' domain' + (domains.length === 1 ? '' : 's') + ' checked directly with the registries.' + note;
    }).catch(function (err) {
      status.className = 'status err';
      status.textContent = err && err.message ? err.message : 'Something went wrong. Try again.';
    }).then(function () { btn.disabled = false; });
  });

  btnCsv.addEventListener('click', function () {
    DV.downloadCsv('rdap-whois.csv', ['domain', 'result', 'registrar', 'registrar_iana_id', 'created', 'expires', 'last_changed', 'status', 'nameservers', 'dnssec', 'source'], lastRows);
  });
})();
