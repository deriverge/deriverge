/* Wayback Machine snapshot finder: first, latest and closest capture through the Availability API, plus direct links. */
(function () {
  'use strict';
  var DV = window.DV;
  var MAX = 20;
  var API = 'https://archive.org/wayback/available';
  var WB = 'https://web.archive.org/web/';
  var form = document.getElementById('wb-form');
  var out = document.getElementById('wb-results');
  var status = document.getElementById('wb-status');
  var btnCsv = document.getElementById('wb-csv');
  var lastRows = [];

  function normUrl(raw) {
    var s = String(raw || '').trim();
    if (!s) return null;
    var withProto = /^[a-z][a-z0-9+.-]*:\/\//i.test(s) ? s : 'http://' + s;
    var u;
    try { u = new URL(withProto); } catch (e) { return null; }
    if (!/^https?:$/.test(u.protocol) || !DV.toDomain(u.hostname)) return null;
    var path = u.pathname === '/' ? '' : u.pathname;
    return { url: u.hostname + path + u.search, host: u.hostname };
  }

  function ts(t) {
    if (!t) return '';
    var s = String(t);
    return s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8) + (s.length >= 12 ? ' ' + s.slice(8, 10) + ':' + s.slice(10, 12) : '');
  }

  function probe(url, stamp) {
    var q = API + '?url=' + encodeURIComponent(url) + (stamp ? '&timestamp=' + stamp : '');
    return DV.getJson(q, { timeout: 20000 }).then(function (res) {
      if (!res.ok || !res.json) return { error: res.error === 'timeout' ? 'timeout' : 'HTTP ' + res.status };
      var c = res.json.archived_snapshots && res.json.archived_snapshots.closest;
      if (!c || !c.available) return { none: true };
      return { timestamp: c.timestamp, url: String(c.url).replace(/^http:\/\//, 'https://'), status: c.status };
    });
  }

  /** A capture date from the API, or a direct Wayback link when the API reported none. */
  function cell(p, href, label) {
    if (p && p.timestamp) return '<a href="' + DV.esc(p.url) + '" target="_blank" rel="nofollow noopener">' + DV.esc(ts(p.timestamp)) + '</a>';
    var why = p && p.error ? 'the API did not answer (' + p.error + ')' : 'date not reported by the API';
    return '<a href="' + DV.esc(href) + '" target="_blank" rel="nofollow noopener">' + label + '</a><span class="sub">' + DV.esc(why) + '</span>';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var raw = DV.splitList(form.urls.value);
    var items = [], seen = {}, bad = 0;
    raw.forEach(function (x) { var n = normUrl(x); if (!n) { bad++; return; } if (!seen[n.url]) { seen[n.url] = 1; items.push(n); } });
    status.className = 'status';
    if (!items.length) { status.className = 'status err'; status.textContent = 'Enter a URL or domain such as example.com or example.com/pricing.'; return; }
    var note = '';
    if (items.length > MAX) { note += ' Only the first ' + MAX + ' were checked.'; items = items.slice(0, MAX); }
    if (bad) note += ' Skipped ' + bad + ' entr' + (bad === 1 ? 'y' : 'ies') + ' that are not web addresses.';
    var date = (form.date.value || '').replace(/-/g, '');
    var today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    var jobs = [];
    items.forEach(function (it, i) {
      jobs.push({ i: i, k: 'first', stamp: '19960101' });
      jobs.push({ i: i, k: 'latest', stamp: today });
      if (date) jobs.push({ i: i, k: 'date', stamp: date });
    });
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    var done = 0;
    status.innerHTML = '<span class="spin"></span> Asking the Wayback Machine...';
    DV.pool(jobs, 4, function (j) {
      return probe(items[j.i].url, j.stamp).then(function (r) { done++; status.innerHTML = '<span class="spin"></span> ' + done + ' of ' + jobs.length + ' lookups...'; return r; });
    }).then(function (res) {
      var by = items.map(function () { return {}; });
      jobs.forEach(function (j, n) { by[j.i][j.k] = res[n]; });
      lastRows = [];
      var h = '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>URL</th><th>First capture</th><th>Latest capture</th>' + (date ? '<th>Closest to ' + DV.esc(ts(date)) + '</th>' : '') + '<th>Browse</th></tr></thead><tbody>';
      var dates = 0;
      items.forEach(function (it, i) {
        var b = by[i];
        ['first', 'latest', 'date'].forEach(function (k) { if (b[k] && b[k].timestamp) dates++; });
        var links = '<a href="' + WB + '*/' + DV.esc(it.url) + '" target="_blank" rel="nofollow noopener">calendar</a> · ' +
          '<a href="' + WB + '*/' + DV.esc(it.host) + '/*" target="_blank" rel="nofollow noopener">all URLs of ' + DV.esc(it.host) + '</a>';
        h += '<tr><td class="v">' + DV.esc(it.url) + '</td><td>' + cell(b.first, WB + '1/' + it.url, 'open first capture') + '</td><td>' + cell(b.latest, WB + '2/' + it.url, 'open latest capture') + '</td>' +
          (date ? '<td>' + cell(b.date, WB + date + '/' + it.url, 'open closest capture') + '</td>' : '') + '<td>' + links + '</td></tr>';
        lastRows.push([it.url, b.first && b.first.timestamp ? ts(b.first.timestamp) : '', b.first && b.first.url || WB + '1/' + it.url, b.latest && b.latest.timestamp ? ts(b.latest.timestamp) : '', b.latest && b.latest.url || WB + '2/' + it.url, date ? (b.date && b.date.timestamp ? ts(b.date.timestamp) : '') : '', date ? (b.date && b.date.url || WB + date + '/' + it.url) : '', WB + '*/' + it.url]);
      });
      out.innerHTML = h + '</tbody></table></div>';
      btnCsv.hidden = false;
      status.textContent = 'Done: ' + items.length + ' URL' + (items.length === 1 ? '' : 's') + ' checked. ' + (dates ? 'The Availability API reported ' + dates + ' capture date' + (dates === 1 ? '' : 's') + '; the other links open the Wayback Machine directly.' : 'The Availability API reported no capture dates this time (it often skips archived pages); the links open the Wayback Machine directly.') + note;
    }).then(function () { btn.disabled = false; }, function () { btn.disabled = false; status.className = 'status err'; status.textContent = 'Something went wrong. Try again.'; });
  });

  btnCsv.addEventListener('click', function () {
    DV.downloadCsv('wayback-snapshots.csv', ['url', 'first_capture', 'first_capture_url', 'latest_capture', 'latest_capture_url', 'closest_capture', 'closest_capture_url', 'calendar_url'], lastRows);
  });
})();
