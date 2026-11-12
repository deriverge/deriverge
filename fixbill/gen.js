/* Fixbill template generator: fills a quote or invoice in the browser and prints it (Save as PDF).
   Nothing is sent anywhere. The form is rendered by fixbill/_build/build.py, the page config sits in #gen-cfg. */
(function () {
  'use strict';
  var cfgEl = document.getElementById('gen-cfg');
  var form = document.getElementById('gen-form');
  var out = document.getElementById('gen-doc');
  if (!cfgEl || !form || !out) return;
  var C = JSON.parse(cfgEl.textContent);
  var D = C.doc, U = C.ui;
  var KEY = 'fixbill-gen:' + C.id;
  var itemsBox = document.getElementById('gen-items');

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function isoDay(off) {
    var d = new Date();
    d.setDate(d.getDate() + (off || 0));
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
  }
  function num(s) {
    s = String(s == null ? '' : s).replace(/[\s  ']/g, '');
    var c = s.lastIndexOf(','), p = s.lastIndexOf('.');
    if (c >= 0 && p >= 0) s = c > p ? s.replace(/\./g, '').replace(',', '.') : s.replace(/,/g, '');
    else if (c >= 0) s = (!C.decComma && /^\d{1,3}(,\d{3})+$/.test(s)) ? s.replace(/,/g, '') : s.replace(',', '.');
    var n = parseFloat(s);
    return isFinite(n) ? n : 0;
  }
  function r2(x) { return Math.round((x + Number.EPSILON) * 100) / 100; }

  var fields = Array.prototype.slice.call(form.querySelectorAll('[data-f]'));
  var byName = {};
  fields.forEach(function (el) { byName[el.name] = el; });

  // Defaults: values rendered into the form, dates relative to today, example items from the config.
  fields.forEach(function (el) {
    if (el.dataset.off != null && !el.value) el.value = isoDay(parseInt(el.dataset.off, 10));
  });
  var defaults = { f: {}, items: C.items.map(function (i) { return { d: i[0], q: i[1], u: i[2], p: i[3] }; }) };
  fields.forEach(function (el) { defaults.f[el.name] = el.value; });

  var state = JSON.parse(JSON.stringify(defaults));
  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (saved && saved.f && saved.items) state = saved;
  } catch (e) { /* storage blocked: work without it */ }
  // Keep fresh dates when the saved draft has none.
  Object.keys(defaults.f).forEach(function (k) { if (state.f[k] == null) state.f[k] = defaults.f[k]; });
  fields.forEach(function (el) { el.value = state.f[el.name] != null ? state.f[el.name] : el.value; });
  if (byName.tax && byName.tax.selectedIndex < 0) byName.tax.selectedIndex = 0;

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
  }

  // ---- item rows ----
  function input(cls, val, label, mode) {
    var i = document.createElement('input');
    i.type = 'text';
    i.className = cls;
    i.value = val == null ? '' : val;
    i.setAttribute('aria-label', label);
    i.placeholder = label;
    if (mode) i.inputMode = mode;
    return i;
  }
  function drawItems() {
    itemsBox.textContent = '';
    state.items.forEach(function (it, idx) {
      var row = document.createElement('div');
      row.className = 'item';
      var d = input('d', it.d, U.desc);
      var q = input('q', it.q, U.qty, 'decimal');
      var u = input('u', it.u, U.unit);
      var p = input('p', it.p, U.price, 'decimal');
      var x = document.createElement('button');
      x.type = 'button';
      x.textContent = '×';
      x.setAttribute('aria-label', U.remove);
      x.title = U.remove;
      [d, q, u, p].forEach(function (el, k) {
        el.addEventListener('input', function () {
          state.items[idx][['d', 'q', 'u', 'p'][k]] = el.value;
          update();
        });
      });
      x.addEventListener('click', function () {
        state.items.splice(idx, 1);
        if (!state.items.length) state.items.push({ d: '', q: '1', u: '', p: '' });
        drawItems();
        update();
      });
      row.appendChild(d); row.appendChild(q); row.appendChild(u); row.appendChild(p); row.appendChild(x);
      itemsBox.appendChild(row);
    });
  }

  // ---- document ----
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function val(name) { return state.f[name] == null ? '' : String(state.f[name]).trim(); }
  function phText(name) {
    var f = byName[name];
    return f ? (f.placeholder || f.dataset.label || '') : '';
  }
  // Value or a grey placeholder (hidden in print).
  function v(tag, cls, name) {
    var t = val(name);
    if (t) return el(tag, cls, t);
    var e = el(tag, cls);
    e.appendChild(el('span', 'ph', phText(name)));
    return e;
  }
  function date(name) {
    var t = val(name);
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(t);
    if (!m) return t;
    try { return new Intl.DateTimeFormat(C.locale).format(new Date(+m[1], +m[2] - 1, +m[3])); }
    catch (e) { return t; }
  }
  function money(x) {
    var cur = val('cur') || C.currency;
    try { return new Intl.NumberFormat(C.locale, { style: 'currency', currency: cur }).format(x); }
    catch (e) { return x.toFixed(2) + ' ' + cur; }
  }
  function qty(x) {
    try { return new Intl.NumberFormat(C.locale, { maximumFractionDigits: 3 }).format(x); }
    catch (e) { return String(x); }
  }
  function taxInfo() {
    var s = byName.tax;
    if (!s) return { rate: 0, none: true, note: '', label: D.tax };
    var o = s.options[s.selectedIndex] || s.options[0];
    if (o.value === 'none') return { rate: 0, none: true, note: o.dataset.note || '', label: D.tax };
    var rate = o.value === 'custom' ? num(val('taxrate')) : num(o.value);
    return { rate: rate, none: false, note: o.dataset.note || '', label: o.dataset.tax || D.tax };
  }
  function party(title, prefix) {
    var s = el('section');
    s.appendChild(el('h3', null, title));
    s.appendChild(v('p', 'nm', prefix + 'name'));
    ['addr', 'ids', 'extra', 'contact'].forEach(function (k) {
      if (byName[prefix + k]) {
        var t = val(prefix + k);
        if (t || k === 'addr') s.appendChild(v('p', 'pre', prefix + k));
      }
    });
    return s;
  }
  function render() {
    var tax = taxInfo();
    var paper = el('div', 'paper');
    var head = el('header', 'd-head');
    var left = el('div');
    left.appendChild(el('h2', 'd-title', D.title));
    var no = el('p', 'd-no', D.no + ' ');
    no.appendChild(val('number') ? document.createTextNode(val('number')) : el('span', 'ph', phText('number')));
    left.appendChild(no);
    head.appendChild(left);
    var dl = el('dl', 'd-dates');
    C.dates.forEach(function (k) {
      if (!byName[k] || !val(k)) return;
      dl.appendChild(el('dt', null, byName[k].dataset.label));
      dl.appendChild(el('dd', null, date(k)));
    });
    head.appendChild(dl);
    paper.appendChild(head);

    var parties = el('div', 'd-parties');
    parties.appendChild(party(D.seller, 's_'));
    parties.appendChild(party(D.buyer, 'b_'));
    paper.appendChild(parties);

    ['site', 'start'].forEach(function (k) {
      if (byName[k] && val(k)) {
        var b = el('div', 'd-block');
        b.appendChild(el('h3', null, byName[k].dataset.label));
        b.appendChild(el('p', 'pre', val(k)));
        paper.appendChild(b);
      }
    });

    var tbl = el('table', 'd-items');
    var thead = el('thead'), tr = el('tr');
    [D.desc, D.qty, D.unit, tax.none ? D.price : D.priceNet, tax.none ? D.amount : D.amountNet].forEach(function (h) {
      tr.appendChild(el('th', null, h));
    });
    thead.appendChild(tr);
    tbl.appendChild(thead);
    var tb = el('tbody'), net = 0;
    state.items.forEach(function (it) {
      if (!String(it.d || '').trim() && !String(it.p || '').trim()) return;
      var q = num(it.q), p = num(it.p), line = r2(q * p);
      net = r2(net + line);
      var r = el('tr');
      r.appendChild(el('td', null, it.d || ''));
      r.appendChild(el('td', null, qty(q)));
      r.appendChild(el('td', null, it.u || ''));
      r.appendChild(el('td', null, money(p)));
      r.appendChild(el('td', null, money(line)));
      tb.appendChild(r);
    });
    tbl.appendChild(tb);
    paper.appendChild(tbl);

    var tot = el('div', 'd-tot');
    function row(a, b, cls) {
      var d = el('div', cls);
      d.appendChild(el('span', null, a));
      d.appendChild(el('span', null, b));
      tot.appendChild(d);
    }
    if (tax.none) {
      row(D.total, money(net), 'big');
    } else {
      var t = r2(net * tax.rate / 100);
      row(D.net, money(net));
      row(tax.label + ' ' + qty(tax.rate) + (/^(en|it|pl)/.test(C.locale) ? '%' : '\u00a0%'), money(t));
      row(D.total, money(r2(net + t)), 'big');
    }
    paper.appendChild(tot);
    if (tax.note) paper.appendChild(el('p', 'd-taxnote', tax.note));

    var pay = el('dl', 'd-pay'), any = false;
    C.pay.forEach(function (k) {
      var t = val(k);
      if (k === 'ref' && !t && C.refFromNumber) t = val('number').replace(/\D/g, '');
      if (!byName[k] || !t) return;
      any = true;
      var w = el('div');
      w.appendChild(el('dt', null, byName[k].dataset.label));
      w.appendChild(el('dd', null, k === 'due' ? date(k) : t));
      pay.appendChild(w);
    });
    if (any) paper.appendChild(pay);

    if (val('notes')) paper.appendChild(el('p', 'd-notes', val('notes')));

    if (C.sign) {
      var sg = el('div', 'd-sign');
      C.sign.forEach(function (label) {
        var box = el('section');
        box.appendChild(el('div'));
        box.appendChild(el('p', null, label));
        sg.appendChild(box);
      });
      paper.appendChild(sg);
    }
    paper.appendChild(el('p', 'd-made', C.made));
    out.textContent = '';
    out.appendChild(paper);
  }

  function update() {
    fields.forEach(function (f) { state.f[f.name] = f.value; });
    if (byName.taxrate) byName.taxrate.closest('label').hidden = !(byName.tax && byName.tax.value === 'custom');
    save();
    render();
  }

  form.addEventListener('input', function (e) { if (e.target.dataset.f != null || e.target.name) update(); });
  form.addEventListener('change', update);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  document.getElementById('gen-add').addEventListener('click', function () {
    state.items.push({ d: '', q: '1', u: '', p: '' });
    drawItems();
    update();
    var rows = itemsBox.querySelectorAll('.item .d');
    if (rows.length) rows[rows.length - 1].focus();
  });
  document.getElementById('gen-reset').addEventListener('click', function () {
    if (!window.confirm(U.resetAsk)) return;
    state = JSON.parse(JSON.stringify(defaults));
    fields.forEach(function (f) { f.value = state.f[f.name]; });
    try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ }
    drawItems();
    update();
  });

  // Printing: the print stylesheet shows only the document; the title becomes the PDF file name.
  var oldTitle = document.title;
  window.addEventListener('beforeprint', function () {
    render();
    document.title = (D.title + ' ' + val('number')).trim();
  });
  window.addEventListener('afterprint', function () { document.title = oldTitle; });
  Array.prototype.forEach.call(document.querySelectorAll('.gen-print'), function (b) {
    b.addEventListener('click', function () { window.print(); });
  });

  drawItems();
  update();
})();
