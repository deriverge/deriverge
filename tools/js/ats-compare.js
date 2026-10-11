/* ATS overview page: find a company's ATS in our lists, and recognise the ATS from a careers link. */
(function () {
  'use strict';
  var DV = window.DV, X = window.ATSX;
  var box = document.getElementById('find');
  if (box) {
    var ids = box.getAttribute('data-ats').split(',');
    var input = document.getElementById('find-q');
    var out = document.getElementById('find-results');
    var st = document.getElementById('find-status');
    var all = null, loading = null;

    var load = function () {
      if (all) return Promise.resolve(all);
      if (loading) return loading;
      st.innerHTML = '<span class="spin"></span> Loading ' + ids.length + ' company lists...';
      loading = Promise.all(ids.map(function (id) {
        return DV.getJson('/tools/data/ats/' + id + '.json', { timeout: 30000 }).then(function (r) { return { id: id, json: r.ok ? r.json : null }; });
      })).then(function (lists) {
        all = [];
        var failed = 0;
        lists.forEach(function (l) {
          if (!l.json) { failed++; return; }
          l.json.rows.forEach(function (r) { all.push({ ats: l.id, name: r[0], low: r[0].toLowerCase(), key: r[1], cc: r[2], jobs: r[3], site: r[4] || '', cap: l.json.cap || null }); });
        });
        st.textContent = DV.fmtInt(all.length) + ' companies loaded.' + (failed ? ' ' + failed + ' list' + (failed === 1 ? '' : 's') + ' failed to load.' : '');
        return all;
      });
      return loading;
    };

    var search = function () {
      var term = (input.value || '').trim().toLowerCase().replace(/^https?:\/\/(www\.)?/, '').replace(/\/.*$/, '');
      if (term.length < 2) { out.innerHTML = ''; return; }
      load().then(function (rows) {
        var exact = [], starts = [], contains = [];
        for (var i = 0; i < rows.length; i++) {
          var r = rows[i];
          var site = r.site.toLowerCase();
          if (r.low === term || r.key.toLowerCase() === term) exact.push(r);
          else if (r.low.indexOf(term) === 0 || (site && site.indexOf(term) >= 0)) starts.push(r);
          else if (r.low.indexOf(term) >= 0 || r.key.toLowerCase().indexOf(term) >= 0) contains.push(r);
        }
        var byJobs = function (a, b) { return b.jobs - a.jobs; };
        var hits = exact.sort(byJobs).concat(starts.sort(byJobs), contains.sort(byJobs));
        var total = hits.length;
        hits = hits.slice(0, 25);
        if (!hits.length) { out.innerHTML = '<p class="note">No company named like "' + DV.esc(input.value.trim()) + '" in our lists. Paste one of its job links into the detector below instead.</p>'; return; }
        var h = '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Company</th><th>ATS</th><th>Careers page</th><th class="num">Open jobs</th></tr></thead><tbody>';
        hits.forEach(function (r) {
          var url = X.ATS[r.ats].url(r.key);
          h += '<tr><td>' + DV.esc(r.name) + (r.cc ? '<span class="sub">' + DV.esc(DV.countryName(r.cc)) + '</span>' : '') + '</td><td><a href="/tools/companies-using-' + r.ats + '/">' + DV.esc(X.ATS[r.ats].name) + '</a></td><td><a href="' + DV.esc(url) + '" target="_blank" rel="nofollow noopener">' + DV.esc(X.shortUrl(url)) + '</a></td><td class="num">' + DV.fmtInt(r.jobs) + (r.cap && r.jobs >= r.cap ? '+' : '') + '</td></tr>';
        });
        out.innerHTML = h + '</tbody></table></div>' + (total > hits.length ? '<p class="note">Showing 25 of ' + DV.fmtInt(total) + ' matches. Type more of the name to narrow it down.</p>' : '');
      });
    };
    var t = null;
    input.addEventListener('focus', load, { once: true });
    input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(search, 180); });
    document.getElementById('find-form').addEventListener('submit', function (e) { e.preventDefault(); search(); });
  }

  var det = document.getElementById('detect-form');
  if (det) {
    var res = document.getElementById('detect-result');
    det.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = det.url.value;
      var r = X.detect(v);
      if (!r) { res.className = 'status err'; res.textContent = 'That does not look like a web address. Paste the full link of a job or careers page.'; return; }
      res.className = 'status';
      if (!r.id) { res.innerHTML = 'No known ATS in this address. Many companies show jobs on their own domain: open one job and look at the link of its <strong>Apply</strong> button, which usually points to the ATS.'; return; }
      if (r.inData) res.innerHTML = 'This link belongs to <strong>' + DV.esc(r.name) + '</strong>. See <a href="/tools/companies-using-' + r.id + '/">all companies using ' + DV.esc(r.name) + '</a>.';
      else res.innerHTML = 'This link belongs to <strong>' + DV.esc(r.name) + '</strong>. We do not list companies for this system yet.';
    });
  }
})();
