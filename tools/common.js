/* Shared helpers for the /tools/ pages. Loaded after config.js. No dependencies. */
(function () {
  'use strict';
  var cfg = window.DV_TOOLS || { AFFILIATE_PARAM: '', APIFY_USER: 'deriverge', UTM: {} };

  /** Apify Store link for one of our actors (or our profile when slug is empty), with UTM and affiliate parameters. */
  function actorUrl(slug, campaign) {
    var q = [];
    var utm = cfg.UTM || {};
    for (var k in utm) { if (Object.prototype.hasOwnProperty.call(utm, k)) q.push(k + '=' + encodeURIComponent(utm[k])); }
    if (campaign) q.push('utm_campaign=' + encodeURIComponent(campaign));
    var aff = (cfg.AFFILIATE_PARAM || '').replace(/^[?&]+/, '');
    if (aff) q.push(aff);
    return 'https://apify.com/' + cfg.APIFY_USER + (slug ? '/' + slug : '') + (q.length ? '?' + q.join('&') : '');
  }

  function applyActorLinks(root) {
    var links = (root || document).querySelectorAll('a[data-actor]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      a.href = actorUrl(a.getAttribute('data-actor'), a.getAttribute('data-campaign') || '');
      if (cfg.AFFILIATE_PARAM && !/\bsponsored\b/.test(a.rel)) a.rel = (a.rel ? a.rel + ' ' : '') + 'sponsored';
    }
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /** Domain from free text: URL, e-mail address or bare name. IDNs become punycode. Returns null when invalid. */
  function toDomain(raw) {
    var s = String(raw || '').trim().toLowerCase();
    if (!s) return null;
    s = s.replace(/^[a-z][a-z0-9+.-]*:\/\//, '');
    if (s.indexOf('@') >= 0 && s.indexOf('/') < 0) s = s.split('@').pop();
    s = s.split(/[\/?#\s]/)[0].replace(/:\d+$/, '').replace(/\.+$/, '');
    if (!s) return null;
    var host;
    try { host = new URL('http://' + s).hostname; } catch (e) { return null; }
    if (!/^(?=.{1,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9-]{2,63}$/.test(host)) return null;
    if (/^\d+(\.\d+){3}$/.test(host)) return null;
    return host;
  }

  /** Splits a pasted list on new lines, commas, semicolons and spaces. */
  function splitList(text) {
    return String(text || '').split(/[\n\r,;\t ]+/).map(function (x) { return x.trim(); }).filter(Boolean);
  }

  function unique(list) {
    var seen = {}, out = [];
    for (var i = 0; i < list.length; i++) { if (!seen[list[i]]) { seen[list[i]] = 1; out.push(list[i]); } }
    return out;
  }

  /** fetch with a timeout. Resolves to { ok, status, json, error }; never rejects. */
  function getJson(url, opts) {
    opts = opts || {};
    var ctrl = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, opts.timeout || 15000) : null;
    return fetch(url, { headers: opts.headers || {}, signal: ctrl ? ctrl.signal : undefined, cache: opts.cache || 'default' })
      .then(function (res) {
        return res.text().then(function (txt) {
          var json = null;
          try { json = txt ? JSON.parse(txt) : null; } catch (e) { json = null; }
          return { ok: res.ok, status: res.status, json: json };
        });
      })
      .catch(function (err) {
        var aborted = err && err.name === 'AbortError';
        return { ok: false, status: 0, json: null, error: aborted ? 'timeout' : 'network' };
      })
      .then(function (r) { if (timer) clearTimeout(timer); return r; });
  }

  /** Runs fn over items with at most `limit` at once. fn returns a promise. */
  function pool(items, limit, fn) {
    var i = 0, active = 0, done = 0, results = new Array(items.length);
    return new Promise(function (resolve) {
      if (!items.length) { resolve(results); return; }
      function next() {
        while (active < limit && i < items.length) {
          (function (idx) {
            active++;
            Promise.resolve(fn(items[idx], idx)).then(function (r) { results[idx] = r; }, function (e) { results[idx] = { error: e }; })
              .then(function () { active--; done++; if (done === items.length) resolve(results); else next(); });
          })(i++);
        }
      }
      next();
    });
  }

  function fmtInt(n) { return n == null ? '' : Number(n).toLocaleString('en-US'); }

  function fmtDate(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d)) return String(iso);
    return d.toISOString().slice(0, 10);
  }

  /** CSV download of rows (array of arrays). The file is built in the browser; nothing is uploaded. */
  function downloadCsv(filename, header, rows) {
    function cell(v) {
      var s = v == null ? '' : String(v);
      return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
    }
    var lines = [header.map(cell).join(',')];
    for (var i = 0; i < rows.length; i++) lines.push(rows[i].map(cell).join(','));
    var blob = new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  var regionNames = null;
  function countryName(code) {
    if (!code) return '';
    try {
      if (!regionNames && typeof Intl !== 'undefined' && Intl.DisplayNames) regionNames = new Intl.DisplayNames(['en'], { type: 'region' });
      return regionNames ? regionNames.of(code) : code;
    } catch (e) { return code; }
  }

  function fillGutter() {
    var gutter = document.querySelector('.gutter');
    var source = document.querySelector('.source');
    if (!gutter || !source) return;
    var lines = Math.max(60, Math.ceil(source.offsetHeight / 26.25) + 2);
    if (gutter.childElementCount >= lines) return;
    var out = '';
    for (var i = 1; i <= lines; i++) out += '<span>' + i + '</span>';
    gutter.innerHTML = out;
  }

  window.DV = {
    actorUrl: actorUrl, applyActorLinks: applyActorLinks, esc: esc, toDomain: toDomain, splitList: splitList,
    unique: unique, getJson: getJson, pool: pool, fmtInt: fmtInt, fmtDate: fmtDate, downloadCsv: downloadCsv,
    countryName: countryName, fillGutter: fillGutter,
  };

  function init() {
    applyActorLinks(document);
    fillGutter();
    if (typeof ResizeObserver !== 'undefined') {
      var src = document.querySelector('.source');
      if (src) new ResizeObserver(fillGutter).observe(src);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
