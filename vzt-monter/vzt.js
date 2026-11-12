/* VZT Montér web calculators. Same formulas as the app (vzduchotechnika_app/src/calc). Texts come from window.VZT_L10N. */
(function () {
  'use strict';

  var RHO = 1.2;            // air density, kg/m3
  var NU = 15.11e-6;        // kinematic viscosity of air at 20 °C, m2/s
  var K_ROUND = 0.09;       // roughness of spiral galvanised duct, mm
  var K_RECT = 0.15;        // roughness of rectangular galvanised duct, mm
  var ANGLES = [15, 22.5, 30, 45, 60, 90];
  var SPIRO = [63, 80, 100, 125, 150, 160, 180, 200, 224, 250, 280, 300, 315, 355, 400, 450, 500, 560, 630, 710,
    800, 900, 1000, 1120, 1250];

  function rad(d) { return d * Math.PI / 180; }

  // Planar offset on round duct: C = O / sin a, A = O / tan a, arm = R * tan(a/2), L = C - 2 * arm.
  function offset(D, O, alphaDeg, R) {
    var a = rad(alphaDeg);
    var arm = R * Math.tan(a / 2);
    var C = O / Math.sin(a);
    var A = O / Math.tan(a);
    var L = C - 2 * arm;
    var r = { C: C, A: A, arm: arm, L: L, ok: L >= 0, suggest: null };
    if (!r.ok) {
      // Largest standard angle below the input that still gives L >= 0 (same rule as the app).
      for (var i = 0; i < ANGLES.length; i++) {
        var d = ANGLES[i];
        if (d >= alphaDeg) continue;
        var t = rad(d);
        if (O / Math.sin(t) - 2 * R * Math.tan(t / 2) >= 0) r.suggest = d;
      }
    }
    return r;
  }

  // Huebscher: equivalent round diameter of an a x b duct with the same friction loss at the same flow.
  function huebscher(a, b) { return 1.3 * Math.pow(a * b, 0.625) / Math.pow(a + b, 0.25); }

  // Darcy-Weisbach with Swamee-Jain friction factor (laminar 64/Re below Re 2300). v m/s, Dm m, k mm -> Pa/m.
  function frictionPerM(v, Dm, kMm) {
    var Re = v * Dm / NU;
    var f = Re < 2300 ? 64 / Re : 0.25 / Math.pow(Math.log10(kMm / 1000 / (3.7 * Dm) + 5.74 / Math.pow(Re, 0.9)), 2);
    return f / Dm * RHO / 2 * v * v;
  }

  // Q m3/h through a round duct D mm or a rectangular a x b mm duct.
  function velocity(Q, shape, D, a, b) {
    var S, Dh, k, De = null;
    if (shape === 'rect') {
      S = a * b / 1e6; Dh = 2 * a * b / (a + b) / 1000; k = K_RECT; De = huebscher(a, b);
    } else {
      S = Math.PI * Math.pow(D / 2000, 2); Dh = D / 1000; k = K_ROUND;
    }
    var v = Q / (3600 * S);
    return { v: v, S: S, dp: frictionPerM(v, Dh, k), De: De };
  }

  function nearestSpiro(D) {
    var lo = null, hi = null;
    for (var i = 0; i < SPIRO.length; i++) {
      if (SPIRO[i] <= D) lo = SPIRO[i];
      if (SPIRO[i] >= D && hi === null) hi = SPIRO[i];
    }
    return { lo: lo, hi: hi };
  }

  function rectToRound(a, b) {
    var De = huebscher(a, b);
    return { De: De, Darea: 2 * Math.sqrt(a * b / Math.PI), S: a * b / 1e6, spiro: nearestSpiro(De) };
  }

  // Segmented elbow of n pieces including two half segments: a = T / (2 (n - 1)).
  function elbow(D, R, totalDeg, n) {
    var joints = Math.max(1, n - 1);
    var alpha = totalDeg / (2 * joints);
    var t = Math.tan(rad(alpha));
    return {
      alpha: alpha, joint: 2 * alpha, full: Math.max(0, n - 2),
      axis: 2 * R * t, inner: 2 * (R - D / 2) * t, outer: 2 * (R + D / 2) * t,
      hAxis: R * t, hInner: (R - D / 2) * t, hOuter: (R + D / 2) * t
    };
  }

  var api = { offset: offset, huebscher: huebscher, frictionPerM: frictionPerM, velocity: velocity,
    nearestSpiro: nearestSpiro, rectToRound: rectToRound, elbow: elbow };

  if (typeof module !== 'undefined' && module.exports) { module.exports = api; return; }
  if (typeof document === 'undefined') return;

  // ---- page binding ----
  var T = window.VZT_L10N || {};
  var lang = document.documentElement.lang || 'en';
  var fmtCache = {};
  function fmt(x, digits) {
    var key = String(digits);
    if (!fmtCache[key]) fmtCache[key] = new Intl.NumberFormat(lang, { minimumFractionDigits: digits, maximumFractionDigits: digits });
    return fmtCache[key].format(x);
  }
  function num(form, name) {
    var el = form.elements[name];
    if (!el) return NaN;
    var s = String(el.value).trim().replace(/\s/g, '').replace(',', '.');
    if (s === '') return NaN;
    return Number(s);
  }
  function pos(x) { return isFinite(x) && x > 0; }
  function sub(s, map) { return String(s || '').replace(/\{(\w+)\}/g, function (m, k) { return map[k] != null ? map[k] : m; }); }

  function setOut(form, values, msg, bad) {
    var outs = form.querySelectorAll('[data-out]');
    for (var i = 0; i < outs.length; i++) {
      var k = outs[i].getAttribute('data-out');
      outs[i].textContent = values && values[k] != null ? values[k] : '';
    }
    var m = form.querySelector('.calc-msg');
    if (m) { m.textContent = msg || ''; m.hidden = !msg; m.classList.toggle('bad', !!bad); }
    var box = form.querySelector('.results');
    if (box) box.classList.toggle('is-empty', !values);
  }

  var runners = {
    offset: function (f) {
      var D = num(f, 'D'), O = num(f, 'O'), al = num(f, 'alpha'), k = num(f, 'rk');
      if (!pos(D) || !pos(O) || !pos(al) || al > 90 || !pos(k)) return setOut(f, null, T.invalid, true);
      var r = offset(D, O, al, k * D);
      var mm = ' mm';
      var vals = { C: fmt(r.C, 0) + mm, A: fmt(r.A, 0) + mm, arm: fmt(r.arm, 0) + mm, R: fmt(k * D, 0) + mm,
        L: fmt(r.L, 0) + mm };
      var msg = '';
      if (!r.ok) msg = r.suggest !== null ? sub(T.offsetSuggest, { a: fmt(al, al % 1 ? 1 : 0), s: fmt(r.suggest, r.suggest % 1 ? 1 : 0) })
        : sub(T.offsetNone, { a: fmt(al, al % 1 ? 1 : 0) });
      setOut(f, vals, msg, !r.ok);
    },
    velocity: function (f) {
      var shape = f.elements.shape.value;
      var rect = shape === 'rect';
      var rows = f.querySelectorAll('[data-shape]');
      for (var i = 0; i < rows.length; i++) rows[i].hidden = rows[i].getAttribute('data-shape') !== shape;
      var Q = num(f, 'Q'), D = num(f, 'D'), a = num(f, 'a'), b = num(f, 'b');
      if (!pos(Q) || (rect ? !(pos(a) && pos(b)) : !pos(D))) return setOut(f, null, T.invalid, true);
      var r = velocity(Q, shape, D, a, b);
      setOut(f, { v: fmt(r.v, 2) + ' m/s', S: fmt(r.S, 4) + ' m²', dp: fmt(r.dp, 2) + ' Pa/m',
        De: r.De ? fmt(r.De, 1) + ' mm' : '' }, '', false);
    },
    rect: function (f) {
      var a = num(f, 'a'), b = num(f, 'b');
      if (!pos(a) || !pos(b)) return setOut(f, null, T.invalid, true);
      var r = rectToRound(a, b);
      var lo = r.spiro.lo, hi = r.spiro.hi, sp;
      if (lo === null && hi === null) sp = '';
      else if (lo === hi) sp = 'Ø' + lo + ' mm';
      else if (lo === null) sp = 'Ø' + hi + ' mm';
      else if (hi === null) sp = 'Ø' + lo + ' mm';
      else sp = 'Ø' + lo + ' / Ø' + hi + ' mm';
      setOut(f, { De: fmt(r.De, 1) + ' mm', spiro: sp, Darea: fmt(r.Darea, 1) + ' mm', S: fmt(r.S, 4) + ' m²' }, '', false);
    },
    elbow: function (f) {
      var D = num(f, 'D'), R = num(f, 'R'), th = num(f, 'theta'), n = num(f, 'n');
      if (!pos(D) || !pos(R) || !pos(th) || th > 180 || !(n >= 2 && n <= 8)) return setOut(f, null, T.invalid, true);
      if (R <= D / 2) return setOut(f, null, sub(T.elbowRadius, { min: fmt(D / 2, 0) }), true);
      var r = elbow(D, R, th, Math.round(n));
      var mm = ' mm';
      setOut(f, { alpha: fmt(r.alpha, 2) + '°', joint: fmt(r.joint, 2) + '°', make: sub(T.elbowMake, { full: r.full }),
        axis: fmt(r.axis, 0) + mm, inner: fmt(r.inner, 0) + mm, outer: fmt(r.outer, 0) + mm,
        hAxis: fmt(r.hAxis, 0) + mm, hInner: fmt(r.hInner, 0) + mm, hOuter: fmt(r.hOuter, 0) + mm }, '', false);
    }
  };

  var forms = document.querySelectorAll('form[data-calc]');
  for (var i = 0; i < forms.length; i++) {
    (function (f) {
      var run = runners[f.getAttribute('data-calc')];
      if (!run) return;
      f.addEventListener('input', function () { run(f); });
      f.addEventListener('change', function () { run(f); });
      f.addEventListener('submit', function (e) { e.preventDefault(); run(f); });
      run(f);
    })(forms[i]);
  }
})();
