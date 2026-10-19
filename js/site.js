/* deriverge.com: language switch, live numbers, reveals and the hero "convergence" canvas. No dependencies. */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Hidden start states apply only once the browser is really painting frames, so content is never stuck invisible.
  if (!reduceMotion && window.requestAnimationFrame) {
    requestAnimationFrame(function () { doc.classList.add('anim'); });
    setTimeout(function () { doc.classList.add('anim-done'); }, 3000);
  }
  var lang = 'cs';

  // ── language ────────────────────────────────────────────────────────────
  var i18n = document.querySelectorAll('[data-en]');
  for (var i = 0; i < i18n.length; i++) i18n[i].setAttribute('data-cs', i18n[i].textContent);
  var langButtons = document.querySelectorAll('.lang-btn');

  function setLang(next, animate) {
    lang = next === 'en' ? 'en' : 'cs';
    for (var k = 0; k < i18n.length; k++) {
      var v = i18n[k].getAttribute('data-' + lang);
      if (v !== null) i18n[k].textContent = v;
    }
    doc.lang = lang;
    for (var m = 0; m < langButtons.length; m++) {
      var on = langButtons[m].getAttribute('data-lang') === lang;
      langButtons[m].classList.toggle('is-active', on);
      langButtons[m].setAttribute('aria-pressed', on ? 'true' : 'false');
    }
    splitTitle(animate);
    renderLive();
    try { localStorage.setItem('dv-lang', lang); } catch (e) { /* storage blocked */ }
  }
  for (var n = 0; n < langButtons.length; n++) {
    langButtons[n].addEventListener('click', function () { setLang(this.getAttribute('data-lang'), true); });
  }

  // Headline words enter one by one (CSS does the motion).
  var title = document.querySelector('.hero-title');
  function splitTitle(animate) {
    if (!title) return;
    var words = title.textContent.trim().split(/\s+/);
    title.setAttribute('aria-label', title.textContent.trim());
    title.innerHTML = words.map(function (w, j) {
      return '<span class="w" aria-hidden="true" style="--w:' + j + (animate === false ? ';animation:none;opacity:1;transform:none;filter:none' : '') + '">' + w.replace(/</g, '&lt;') + '</span>';
    }).join(' ');
  }

  // ── live numbers from the public job index and Apify Store ─────────────
  var live = { jobs: 1740189, companies: 47967, built: '2026-10-19T03:23:44.517Z', actors: 85, fresh: false };
  var shown = { jobs: live.jobs, companies: live.companies };
  function fmtNum(x) { return Math.round(x).toLocaleString(lang === 'cs' ? 'cs-CZ' : 'en-GB'); }
  function fmtBuilt(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return '';
    var hh = String(d.getUTCHours()).padStart(2, '0') + ':' + String(d.getUTCMinutes()).padStart(2, '0') + ' UTC';
    if (lang === 'cs') return d.getUTCDate() + '. ' + (d.getUTCMonth() + 1) + '. ' + d.getUTCFullYear() + ', ' + hh;
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }) + ', ' + hh;
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
    var from = { jobs: shown.jobs * 0.9, companies: shown.companies * 0.9 }, t0 = performance.now(), dur = 1400;
    (function step(now) {
      var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      shown.jobs = from.jobs + (target.jobs - from.jobs) * e;
      shown.companies = from.companies + (target.companies - from.companies) * e;
      renderLive();
      if (p < 1) requestAnimationFrame(step);
    })(t0);
  }
  function loadLive() {
    if (!document.querySelector('[data-live]') || !window.fetch) return;
    var meta = fetch('https://api.apify.com/v2/key-value-stores/jletghbJMlxiI0vnm/records/meta.json').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    var store = fetch('https://api.apify.com/v2/store?username=deriverge&limit=1').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    Promise.all([meta, store]).then(function (res) {
      var m = res[0], s = res[1];
      if (m && m.jobs && m.companies) { live.jobs = m.jobs; live.companies = m.companies; live.built = m.generatedAt || live.built; live.fresh = true; }
      if (s && s.data && s.data.total) live.actors = s.data.total;
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
    var W = 0, H = 0, dpr = 1, F = { x: 0, y: 0 }, parts = [], running = false, visible = true, raf = 0;
    var mouse = { x: -9999, y: -9999, active: false };
    var colors;

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
    function rnd(a, b) { return a + Math.random() * (b - a); }
    function spawn(p, initial) {
      p.y0 = rnd(-0.15, 1.15) * H;
      p.u = initial ? Math.random() * 1.4 : rnd(-0.08, 0);
      p.v = rnd(0.0009, 0.0022);
      p.k = rnd(1.2, 3.2);
      p.ph = rnd(0, Math.PI * 2);
      p.amp = rnd(0.02, 0.09) * H;
      p.off = 0;
      p.px = null; p.py = null;
      p.lane = rnd(-1, 1);
    }
    function resize() {
      var b = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = Math.max(1, b.width); H = Math.max(1, b.height);
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var narrow = W < 720;
      F.x = narrow ? W * 0.62 : W * 0.72;
      F.y = narrow ? H * 0.2 : H * 0.44;
      var target = Math.round(Math.min(1500, Math.max(320, (W * H) / (narrow ? 1500 : 1150))));
      while (parts.length < target) { var p = {}; spawn(p, true); parts.push(p); }
      parts.length = target;
      readColors();
      ctx.fillStyle = 'rgb(' + colors.bg.join(',') + ')';
      ctx.fillRect(0, 0, W, H);
      // Draw a settled picture right away; the loop continues from here.
      for (var w = 0; w < 120; w++) frame();
    }
    function ease(u) { return u <= 0 ? 0 : u >= 1 ? 1 : 1 - Math.pow(1 - u, 2.6); }
    function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }

    function frame() {
      // Fading the previous frame leaves short trails.
      ctx.globalCompositeOperation = 'source-over';
      ctx.fillStyle = 'rgba(' + colors.bg.join(',') + ',0.085)';
      ctx.fillRect(0, 0, W, H);
      var x0 = -0.04 * W;
      ctx.lineWidth = 1;
      ctx.lineCap = 'round';
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        p.u += p.v;
        var x, y, t;
        if (p.u < 1) {
          var e = ease(p.u);
          x = x0 + (F.x - x0) * p.u;
          y = p.y0 + (F.y - p.y0) * e + Math.sin(p.u * Math.PI * p.k + p.ph) * p.amp * (1 - e);
          t = e;
        } else {
          var past = (p.u - 1) / 0.45;
          x = F.x + (W * 1.06 - F.x) * past;
          y = F.y + p.lane * 1.6 * (1 - past * 0.6);
          t = 1;
          if (x > W * 1.05) { spawn(p, false); p.px = null; continue; }
        }
        if (mouse.active) {
          var dx = x - mouse.x, dy = y - mouse.y, d2 = dx * dx + dy * dy, R = 150;
          if (d2 < R * R) { var d = Math.sqrt(d2) || 1, f = (1 - d / R); p.off += (dy / d) * f * 2.2; }
        }
        p.off *= 0.94;
        y += p.off;
        if (p.px !== null) {
          var c = p.u < 1 ? mix(colors.cool, colors.warm, Math.pow(t, 1.6)) : mix(colors.warm, colors.ink, Math.min(1, (p.u - 1) * 3));
          var a = p.u < 1 ? 0.10 + 0.5 * t : 0.7 * (1 - Math.max(0, (p.u - 1.2) / 0.3));
          ctx.strokeStyle = 'rgba(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ',' + a.toFixed(3) + ')';
          ctx.beginPath(); ctx.moveTo(p.px, p.py); ctx.lineTo(x, y); ctx.stroke();
        }
        p.px = x; p.py = y;
      }
      // The point where the streams meet.
      ctx.globalCompositeOperation = colors.light ? 'source-over' : 'lighter';
      var g = ctx.createRadialGradient(F.x, F.y, 0, F.x, F.y, 30);
      g.addColorStop(0, 'rgba(' + colors.warm.join(',') + ',0.07)');
      g.addColorStop(1, 'rgba(' + colors.warm.join(',') + ',0)');
      ctx.fillStyle = g;
      ctx.fillRect(F.x - 30, F.y - 30, 60, 60);
      ctx.globalCompositeOperation = 'source-over';
    }
    function loop() { if (!running) return; frame(); raf = requestAnimationFrame(loop); }
    function start() { if (running || reduceMotion || !visible || document.hidden) return; running = true; raf = requestAnimationFrame(loop); }
    function stop() { running = false; cancelAnimationFrame(raf); }

    resize();
    if (reduceMotion) { for (var s = 0; s < 160; s++) frame(); return; }
    var ro = 'ResizeObserver' in window ? new ResizeObserver(function () { resize(); }) : null;
    if (ro) ro.observe(canvas); else window.addEventListener('resize', resize);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; visible ? start() : stop(); }).observe(canvas);
    }
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function () { readColors(); });
    var hero = canvas.parentElement;
    hero.addEventListener('pointermove', function (ev) { var b = canvas.getBoundingClientRect(); mouse.x = ev.clientX - b.left; mouse.y = ev.clientY - b.top; mouse.active = true; });
    hero.addEventListener('pointerleave', function () { mouse.active = false; });
    start();
  }

  // ── start ───────────────────────────────────────────────────────────────
  var saved = null;
  try { saved = localStorage.getItem('dv-lang'); } catch (e) { /* storage blocked */ }
  if (!saved) saved = /^(cs|sk)/i.test(navigator.language || '') ? 'cs' : 'en';
  setLang(saved, true);
  loadLive();
  var canvas = document.getElementById('flow');
  if (canvas) heroFlow(canvas);
})();
