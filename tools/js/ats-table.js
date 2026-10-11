/* Searchable, sortable list of the companies on one ATS, loaded from /tools/data/ats/<ats>.json. */
(function () {
  'use strict';
  var DV = window.DV, X = window.ATSX;
  var app = document.getElementById('ats-app');
  if (!app) return;
  var atsId = app.getAttribute('data-ats');
  var spec = X.ATS[atsId];
  var q = document.getElementById('ats-q');
  var sel = document.getElementById('ats-country');
  var openOnly = document.getElementById('ats-open');
  var tbody = document.getElementById('ats-tbody');
  var thead = document.getElementById('ats-thead');
  var count = document.getElementById('ats-count');
  var more = document.getElementById('ats-more');
  var csv = document.getElementById('ats-csv');
  var PAGE = 100;
  var data = null, view = [], shown = PAGE, sortKey = 'jobs', sortDir = -1, cap = null, hasSite = false;

  function jobsText(n) { return n ? DV.fmtInt(n) + (cap && n >= cap ? '+' : '') : '0'; }

  function header() {
    var cols = [['name', 'Company'], ['url', 'Careers page']];
    if (hasSite) cols.push(['site', 'Website']);
    cols.push(['country', 'Main country'], ['jobs', 'Open jobs']);
    thead.innerHTML = '<tr>' + cols.map(function (c) {
      var sortable = c[0] !== 'url' && c[0] !== 'site';
      var arrow = sortKey === c[0] ? '<span class="arrow">' + (sortDir < 0 ? '&darr;' : '&uarr;') + '</span>' : '';
      return '<th' + (c[0] === 'jobs' ? ' class="num sortable"' : sortable ? ' class="sortable"' : '') + (sortable ? ' data-sort="' + c[0] + '" tabindex="0" aria-sort="' + (sortKey === c[0] ? (sortDir < 0 ? 'descending' : 'ascending') : 'none') + '"' : '') + '>' + c[1] + arrow + '</th>';
    }).join('') + '</tr>';
  }

  function apply() {
    var term = (q.value || '').trim().toLowerCase();
    var cc = sel.value;
    view = data.rows.filter(function (r) {
      if (openOnly.checked && !r[3]) return false;
      if (cc && r[2] !== cc) return false;
      if (term && r[0].toLowerCase().indexOf(term) < 0 && r[1].toLowerCase().indexOf(term) < 0 && (!r[4] || r[4].toLowerCase().indexOf(term) < 0)) return false;
      return true;
    });
    var idx = { name: 0, country: 2, jobs: 3 }[sortKey];
    view.sort(function (a, b) {
      var x = a[idx], y = b[idx];
      if (sortKey === 'country') { x = x ? DV.countryName(x) : '~'; y = y ? DV.countryName(y) : '~'; }
      if (sortKey === 'jobs') return (x - y) * sortDir || a.i - b.i;
      return String(x).localeCompare(String(y)) * sortDir || b[3] - a[3];
    });
    shown = PAGE;
    render();
  }

  function render() {
    var cols = hasSite ? 5 : 4;
    var rows = view.slice(0, shown);
    var h = '';
    rows.forEach(function (r) {
      var url = spec.url(r[1]);
      h += '<tr><td>' + DV.esc(r[0]) + '</td><td><a href="' + DV.esc(url) + '" target="_blank" rel="nofollow noopener">' + DV.esc(X.shortUrl(url)) + '</a></td>';
      if (hasSite) h += '<td>' + (r[4] ? '<a href="' + DV.esc(r[4]) + '" target="_blank" rel="nofollow noopener">' + DV.esc(r[4].replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, '')) + '</a>' : '') + '</td>';
      h += '<td>' + DV.esc(r[2] ? DV.countryName(r[2]) : '') + '</td><td class="num">' + jobsText(r[3]) + '</td></tr>';
    });
    if (!rows.length) h = '<tr><td colspan="' + cols + '" class="empty">No company matches these filters.</td></tr>';
    tbody.innerHTML = h;
    count.textContent = DV.fmtInt(view.length) + ' of ' + DV.fmtInt(data.rows.length) + ' ' + (data.unit || 'companies');
    more.hidden = view.length <= shown;
    more.textContent = 'Show ' + Math.min(PAGE, view.length - shown) + ' more';
    header();
  }

  function init(json) {
    data = json;
    data.rows.forEach(function (r, i) { r.i = i; });
    cap = json.cap || null;
    hasSite = json.rows.some(function (r) { return r[4]; });
    var counts = {};
    json.rows.forEach(function (r) { if (r[2]) counts[r[2]] = (counts[r[2]] || 0) + 1; });
    var opts = Object.keys(counts).map(function (c) { return { c: c, n: DV.countryName(c), k: counts[c] }; });
    opts.sort(function (a, b) { return b.k - a.k || a.n.localeCompare(b.n); });
    sel.innerHTML = '<option value="">All countries</option>' + opts.map(function (o) { return '<option value="' + o.c + '">' + DV.esc(o.n) + ' (' + DV.fmtInt(o.k) + ')</option>'; }).join('');
    apply();
    app.classList.remove('is-loading');
  }

  var t = null;
  q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(apply, 120); });
  sel.addEventListener('change', apply);
  openOnly.addEventListener('change', apply);
  more.addEventListener('click', function () { shown += PAGE; render(); });
  function sortBy(el) {
    var k = el && el.getAttribute('data-sort');
    if (!k) return;
    if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = k === 'jobs' ? -1 : 1; }
    apply();
  }
  thead.addEventListener('click', function (e) { sortBy(e.target.closest('th')); });
  thead.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sortBy(e.target.closest('th')); } });
  csv.addEventListener('click', function () {
    if (!data) return;
    DV.downloadCsv('companies-using-' + atsId + '.csv', ['company', 'careers_page', 'website', 'main_country', 'open_jobs', 'ats'],
      view.map(function (r) { return [r[0], spec.url(r[1]), r[4] || '', r[2] || '', r[3], spec.name]; }));
  });

  DV.getJson(app.getAttribute('data-src'), { timeout: 30000 }).then(function (res) {
    if (res.ok && res.json && res.json.rows) init(res.json);
    else { tbody.innerHTML = '<tr><td colspan="4" class="empty">The company list could not be loaded. Reload the page to try again.</td></tr>'; count.textContent = ''; }
  });
})();
