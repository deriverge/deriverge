/* Tapkasa landing pages: which store button to show, and the right campaign on store links.
   The class on <html> is set by a one-line script in the head (no flash); this file only does the extras. */
(function () {
  'use strict';
  var d = document.documentElement;
  // Language hint: a dismissible bar offers the visitor's own language. Nobody is redirected.
  var alt = document.querySelectorAll('link[rel="alternate"][hreflang]');
  var here = (d.getAttribute('lang') || '').toLowerCase().split('-')[0];
  var off = false;
  try { off = localStorage.getItem('tapkasa-lang-hint') === 'off'; } catch (e) { /* ignore */ }
  if (!off && alt.length) {
    var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
    var want = null, href = null;
    for (var i = 0; i < langs.length && !want; i++) {
      var base = String(langs[i] || '').toLowerCase().split('-')[0];
      for (var j = 0; j < alt.length; j++) {
        if (alt[j].getAttribute('hreflang') === base) { want = base; href = alt[j].getAttribute('href'); break; }
      }
    }
    var item = want && want !== here ? document.querySelector('.lang a[hreflang="' + want + '"]') : null;
    if (item && href) {
      var bar = document.createElement('div');
      bar.className = 'hint';
      bar.lang = want;
      var a = document.createElement('a');
      a.href = href.replace(/^https?:\/\/[^/]+/, '');
      a.hreflang = want;
      a.textContent = 'Tapkasa: ' + item.textContent;
      var x = document.createElement('button');
      x.type = 'button';
      x.textContent = '×';
      x.setAttribute('aria-label', 'Close');
      x.addEventListener('click', function () {
        bar.remove();
        try { localStorage.setItem('tapkasa-lang-hint', 'off'); } catch (e) { /* ignore */ }
      });
      bar.appendChild(a);
      bar.appendChild(x);
      document.body.insertBefore(bar, document.body.firstChild);
    }
  }
})();
