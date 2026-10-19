/* deriverge.com: language routing, live numbers, reveals and the hero "convergence" canvas. No dependencies. */
(function () {
  'use strict';
  var doc = document.documentElement;
  var body = document.body;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var lang = doc.lang || 'en';
  var rtl = doc.dir === 'rtl';

  // ── language: the root page sends a first-time visitor to their language ─
  var available = (body.getAttribute('data-langs') || 'en').split(',');
  var saved = null;
  try { saved = localStorage.getItem('dv-lang'); } catch (e) { /* storage blocked */ }
  function pick() {
    var list = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || 'en'];
    for (var i = 0; i < list.length; i++) {
      var l = String(list[i]).toLowerCase(), base = l.split('-')[0];
      if (base === 'no' || base === 'nn') base = 'nb';
      if (available.indexOf(base) >= 0) return base;
    }
    return 'en';
  }
  if (body.getAttribute('data-root') === '1') {
    var want = saved && available.indexOf(saved) >= 0 ? saved : pick();
    if (want !== 'en') { location.replace('/' + want + '/' + location.hash); return; }
  }
  var langLinks = document.querySelectorAll('.langsel a[data-lang]');
  for (var li = 0; li < langLinks.length; li++) {
    langLinks[li].addEventListener('click', function () { try { localStorage.setItem('dv-lang', this.getAttribute('data-lang')); } catch (e) { /* storage blocked */ } });
  }
  document.addEventListener('click', function (ev) {
    var open = document.querySelector('.langsel[open]');
    if (open && !open.contains(ev.target)) open.removeAttribute('open');
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { var open = document.querySelector('.langsel[open]'); if (open) { open.removeAttribute('open'); open.querySelector('summary').focus(); } }
  });

  // Hidden start states apply only once the browser is really painting frames, so content is never stuck invisible.
  if (!reduceMotion && window.requestAnimationFrame) {
    requestAnimationFrame(function () { doc.classList.add('anim'); });
    setTimeout(function () { doc.classList.add('anim-done'); }, 3000);
  }

  // Headline words enter one by one (CSS does the motion); languages without spaces enter as one piece.
  var title = document.querySelector('.hero-title');
  if (title) {
    var text = title.textContent.trim(), words = text.split(/\s+/);
    title.setAttribute('aria-label', text);
    title.innerHTML = words.map(function (w, j) { return '<span class="w" aria-hidden="true" style="--w:' + j + '">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>'; }).join(' ');
  }

  // ── live numbers from the public job index and Apify Store ─────────────
  var locale = lang === 'ar' ? 'ar-u-nu-latn' : lang === 'hi' ? 'hi-IN-u-nu-latn' : lang;
  var built = document.querySelector('[data-live="built"]');
  var live = { jobs: 0, companies: 0, built: built ? built.getAttribute('data-iso') : '', actors: 0 };
  var shown = { jobs: 0, companies: 0 };
  function readNum(key) { var n = document.querySelector('[data-live="' + key + '"]'); return n ? parseInt(n.textContent.replace(/\D/g, ''), 10) || 0 : 0; }
  live.jobs = shown.jobs = readNum('jobs'); live.companies = shown.companies = readNum('companies'); live.actors = readNum('actors');
  function fmtNum(x) { try { return Math.round(x).toLocaleString(locale); } catch (e) { return String(Math.round(x)); } }
  function fmtBuilt(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return '';
    try {
      return new Intl.DateTimeFormat(locale, { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone: 'UTC' }).format(d) + ' UTC';
    } catch (e) { return d.toISOString().slice(0, 16).replace('T', ' ') + ' UTC'; }
  }
  function renderLive() {
    var nodes = document.querySelectorAll('[data-live]');
    for (var q = 0; q < nodes.length; q++) {
      var key = nodes[q].getAttribute('data-live');
      if (key === 'built') nodes[q].textContent = fmtBuilt(live.built);
      else if (key === 'actors') nodes[q].textContent = fmtNum(live.actors);
      else if (key in shown) nodes[q].textContent = fmtNum(shown[key]);
    }
  }
  function countTo(target) {
    if (reduceMotion) { shown.jobs = target.jobs; shown.companies = target.companies; renderLive(); return; }
    var from = { jobs: shown.jobs, companies: shown.companies }, t0 = performance.now(), dur = 1400;
    (function stepN(now) {
      var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      shown.jobs = from.jobs + (target.jobs - from.jobs) * e;
      shown.companies = from.companies + (target.companies - from.companies) * e;
      renderLive();
      if (p < 1) requestAnimationFrame(stepN);
    })(t0);
  }
  function loadLive() {
    if (!document.querySelector('[data-live]') || !window.fetch) return;
    renderLive();
    var meta = fetch('https://api.apify.com/v2/key-value-stores/jletghbJMlxiI0vnm/records/meta.json').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    var store = fetch('https://api.apify.com/v2/store?username=deriverge&limit=1').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    Promise.all([meta, store]).then(function (res) {
      var m = res[0], s = res[1];
      if (s && s.data && s.data.total) live.actors = s.data.total;
      if (m && m.jobs && m.companies) {
        live.built = m.generatedAt || live.built;
        if (m.jobs !== live.jobs || m.companies !== live.companies) { live.jobs = m.jobs; live.companies = m.companies; shown.jobs = m.jobs * 0.97; shown.companies = m.companies * 0.97; }
      }
      countTo({ jobs: live.jobs, companies: live.companies });
    });
  }

  // ── header, reveals, spotlight ──────────────────────────────────────────
  var head = document.querySelector('.site-head:not(.site-head--page)');
  if (head) {
    var onScroll = function () { head.classList.toggle('is-solid', window.scrollY > 24); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
  var revealables = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    for (var r = 0; r < revealables.length; r++) io.observe(revealables[r]);
  } else {
    for (var r2 = 0; r2 < revealables.length; r2++) revealables[r2].classList.add('is-in');
  }
  var spots = document.querySelectorAll('.tile, .data-card');
  for (var s2 = 0; s2 < spots.length; s2++) {
    spots[s2].addEventListener('pointermove', function (ev) {
      var b = this.getBoundingClientRect();
      this.style.setProperty('--mx', (ev.clientX - b.left) + 'px');
      this.style.setProperty('--my', (ev.clientY - b.top) + 'px');
    });
  }

  // ── hero canvas: many streams converging into one beam ──────────────────
  function heroFlow(canvas) {
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    var W = 0, H = 0, dpr = 1, F = { x: 0, y: 0 }, S = 1, parts = [], running = false, visible = true, raf = 0;
    var mouse = { x: -9999, y: -9999, active: false }, near = 0, T = 0, pulses = [], nextPulse = 2.2;
    var colors, TAIL = 16;

    function hexToRgb(h) {
      h = h.trim().replace('#', '');
      if (h.length === 3) h = h.split('').map(function (c) { return c + c; }).join('');
      var v = parseInt(h, 16);
      return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
    }
    function readColors() {
      var cs = getComputedStyle(doc);
      colors = { bg: hexToRgb(cs.getPropertyValue('--bg') || '#0c0c0f'), cool: hexToRgb(cs.getPropertyValue('--cool') || '#8fb0ff'),
                 warm: hexToRgb(cs.getPropertyValue('--warm') || '#e9b26a'), ink: hexToRgb(cs.getPropertyValue('--ink') || '#eeede9') };
      colors.light = (colors.bg[0] + colors.bg[1] + colors.bg[2]) / 3 > 128;
    }
    function rgba(c, a) { return 'rgba(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ',' + Math.max(0, Math.min(1, a)).toFixed(3) + ')'; }
    function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
    function rnd(a, b) { return a + Math.random() * (b - a); }
    function ease(u) { return u <= 0 ? 0 : u >= 1 ? 1 : 1 - Math.pow(1 - u, 2.6); }

    function spawn(p, initial) {
      p.y0 = rnd(-0.15, 1.15) * H;
      p.u = initial ? Math.random() * 1.4 : rnd(-0.08, 0);
      p.v = rnd(0.0009, 0.0022);
      p.k = rnd(1.2, 3.2);
      p.ph = rnd(0, Math.PI * 2);
      p.amp = rnd(0.02, 0.09) * H;
      p.off = 0;
      p.lane = rnd(-1, 1);
      p.hx = []; p.hy = [];
    }
    function resize() {
      var b = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = Math.max(1, b.width); H = Math.max(1, b.height);
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var narrow = W < 720;
      F.x = narrow ? W * 0.7 : W * 0.78;
      F.y = narrow ? H * 0.17 : H * 0.44;
      S = narrow ? 0.62 : Math.min(1.25, Math.max(0.8, W / 1500));
      var target = Math.round(Math.min(1300, Math.max(300, (W * H) / (narrow ? 1600 : 1300))));
      while (parts.length < target) { var p = {}; spawn(p, true); parts.push(p); }
      parts.length = target;
      readColors();
      for (var w = 0; w < 40; w++) step(1 / 60, false);
      draw();
    }

    // ── simulation ───────────────────────────────────────────────────────
    function step(dt, withMouse) {
      T += dt;
      var x0 = -0.04 * W;
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        p.u += p.v * (dt * 60);
        var x, y;
        if (p.u < 1) {
          var e = ease(p.u);
          x = x0 + (F.x - x0) * p.u;
          y = p.y0 + (F.y - p.y0) * e + Math.sin(p.u * Math.PI * p.k + p.ph) * p.amp * (1 - e);
        } else {
          var past = (p.u - 1) / 0.45;
          x = F.x + (W * 1.06 - F.x) * past;
          y = F.y + p.lane * 1.6 * (1 - past * 0.6);
          if (x > W * 1.05) { spawn(p, false); continue; }
        }
        if (withMouse && mouse.active) {
          var dx = x - mouse.x, dy = y - mouse.y, d2 = dx * dx + dy * dy, R = 150;
          if (d2 < R * R) { var d = Math.sqrt(d2) || 1; p.off += (dy / d) * (1 - d / R) * 2.2; }
        }
        p.off *= 0.94;
        p.hx.push(x); p.hy.push(y + p.off);
        if (p.hx.length > TAIL) { p.hx.shift(); p.hy.shift(); }
      }
      if (withMouse) {
        var md = mouse.active ? Math.hypot(mouse.x - F.x, mouse.y - F.y) : 9999;
        near += ((md < 220 * S ? 1 - md / (220 * S) : 0) - near) * 0.06;
      }
      if (T > nextPulse) { pulses.push({ t0: T }); nextPulse = T + rnd(2.6, 4.2); }
      while (pulses.length && T - pulses[0].t0 > 2.4) pulses.shift();
    }

    // ── drawing ──────────────────────────────────────────────────────────
    function drawStreams() {
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i], n = p.hx.length;
        if (n < 2) continue;
        var t = p.u < 1 ? ease(p.u) : 1;
        var c = p.u < 1 ? mix(colors.cool, colors.warm, Math.pow(t, 1.6)) : mix(colors.warm, colors.ink, Math.min(1, (p.u - 1) * 3));
        var a = p.u < 1 ? 0.16 + 0.62 * t : 0.8 * (1 - Math.max(0, (p.u - 1.2) / 0.3));
        if (colors.light) a *= 0.9;
        var mid = Math.max(1, n - 6);
        // Older half of the tail, faint.
        ctx.strokeStyle = rgba(c, a * 0.35); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(p.hx[0], p.hy[0]);
        for (var j = 1; j <= mid; j++) ctx.lineTo(p.hx[j], p.hy[j]);
        ctx.stroke();
        // Newest part, bright.
        ctx.strokeStyle = rgba(c, a); ctx.lineWidth = 1.25;
        ctx.beginPath(); ctx.moveTo(p.hx[mid], p.hy[mid]);
        for (var k = mid + 1; k < n; k++) ctx.lineTo(p.hx[k], p.hy[k]);
        ctx.stroke();
      }
    }

    function drawCore() {
      var glowOp = colors.light ? 'source-over' : 'lighter';
      var R = 40 * S * (1 + 0.07 * Math.sin(T * 1.4) + 0.22 * near);
      var spin = 1 + near * 1.8;
      ctx.save();
      ctx.translate(F.x, F.y);
      ctx.globalCompositeOperation = glowOp;

      // Halo and nucleus.
      var halo = ctx.createRadialGradient(0, 0, 0, 0, 0, R * 3.2);
      halo.addColorStop(0, rgba(colors.warm, colors.light ? 0.16 : 0.2 + 0.1 * near));
      halo.addColorStop(0.35, rgba(mix(colors.warm, colors.cool, 0.5), colors.light ? 0.06 : 0.07));
      halo.addColorStop(1, rgba(colors.cool, 0));
      ctx.fillStyle = halo;
      ctx.beginPath(); ctx.arc(0, 0, R * 3.2, 0, Math.PI * 2); ctx.fill();
      var core = ctx.createRadialGradient(-R * 0.18, -R * 0.2, 0, 0, 0, R * 0.62);
      core.addColorStop(0, rgba(colors.light ? colors.warm : [255, 246, 230], 0.95));
      core.addColorStop(0.45, rgba(colors.warm, 0.75));
      core.addColorStop(1, rgba(colors.warm, 0));
      ctx.fillStyle = core;
      ctx.beginPath(); ctx.arc(0, 0, R * 0.62, 0, Math.PI * 2); ctx.fill();

      // Probability cloud: points that never stay in one place.
      for (var q = 0; q < 110; q++) {
        var ang = Math.random() * Math.PI * 2, rr = Math.abs((Math.random() + Math.random() + Math.random() - 1.5)) * R * 2.4;
        ctx.fillStyle = rgba(mix(colors.cool, colors.warm, Math.random()), (colors.light ? 0.35 : 0.5) * (1 - rr / (R * 3.6)));
        ctx.fillRect(Math.cos(ang) * rr, Math.sin(ang) * rr * 0.8, 1.2, 1.2);
      }

      // Three shells that tilt and breathe, each with an electron.
      for (var s = 0; s < 3; s++) {
        var a = R * (1.75 + s * 0.42);
        var tilt = 0.4 + 0.24 * Math.sin(T * (0.35 + s * 0.11) + s * 2.1);
        var b = a * tilt;
        var rot = s * (Math.PI / 3) + T * (0.08 + s * 0.035) * spin;
        ctx.save();
        ctx.rotate(rot);
        var g = ctx.createLinearGradient(-a, 0, a, 0);
        g.addColorStop(0, rgba(colors.cool, colors.light ? 0.25 : 0.32));
        g.addColorStop(0.5, rgba(colors.ink, colors.light ? 0.18 : 0.12));
        g.addColorStop(1, rgba(colors.warm, colors.light ? 0.3 : 0.38));
        ctx.strokeStyle = g; ctx.lineWidth = 0.9;
        ctx.beginPath(); ctx.ellipse(0, 0, a, b, 0, 0, Math.PI * 2); ctx.stroke();
        var ph = T * (1.1 + s * 0.42) * spin + s * 1.7;
        for (var tr = 6; tr >= 0; tr--) {
          var pp = ph - tr * 0.07, ex = Math.cos(pp) * a, ey = Math.sin(pp) * b;
          var front = Math.sin(pp) > 0 ? 1 : 0.55;
          ctx.fillStyle = rgba(tr === 0 ? colors.ink : mix(colors.cool, colors.warm, tr / 6), (tr === 0 ? 0.95 : 0.4 * (1 - tr / 7)) * front);
          var rad = tr === 0 ? 2.1 * S + 0.6 : 1.2 * S;
          ctx.beginPath(); ctx.arc(ex, ey, rad, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore();
      }

      // A pulse each time a batch of streams arrives.
      for (var u = 0; u < pulses.length; u++) {
        var age = (T - pulses[u].t0) / 2.4, pr = R * (1.2 + age * 5.5);
        ctx.strokeStyle = rgba(mix(colors.warm, colors.cool, age), (colors.light ? 0.28 : 0.35) * (1 - age));
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.ellipse(0, 0, pr, pr * 0.82, 0, 0, Math.PI * 2); ctx.stroke();
      }
      ctx.restore();
      ctx.globalCompositeOperation = 'source-over';
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);
      drawStreams();
      drawCore();
    }

    var last = 0;
    function loop(now) {
      if (!running) return;
      var dt = last ? Math.min(0.05, (now - last) / 1000) : 1 / 60;
      last = now;
      step(dt, true);
      draw();
      raf = requestAnimationFrame(loop);
    }
    function start() { if (running || reduceMotion || !visible || document.hidden) return; running = true; last = 0; raf = requestAnimationFrame(loop); }
    function stop() { running = false; cancelAnimationFrame(raf); }

    resize();
    if (reduceMotion) return;
    var ro = 'ResizeObserver' in window ? new ResizeObserver(function () { resize(); }) : null;
    if (ro) ro.observe(canvas); else window.addEventListener('resize', resize);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; visible ? start() : stop(); }).observe(canvas);
    }
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function () { readColors(); draw(); });
    var hero = canvas.parentElement;
    hero.addEventListener('pointermove', function (ev) { var b = canvas.getBoundingClientRect(); mouse.x = rtl ? b.right - ev.clientX : ev.clientX - b.left; mouse.y = ev.clientY - b.top; mouse.active = true; });
    hero.addEventListener('pointerleave', function () { mouse.active = false; });
    start();
  }

  // ── start ───────────────────────────────────────────────────────────────
  loadLive();
  var canvas = document.getElementById('flow');
  if (canvas) heroFlow(canvas);
})();
