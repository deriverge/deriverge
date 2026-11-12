/* Fixbill language pages: old #cs/#de/#fr links go to the real language URL, and a dismissible bar offers
   the visitor's own language. Nobody is redirected automatically (crawlers always get the page they asked for). */
(function () {
  'use strict';
  var PAGES = {
    'en': ['/fixbill/', 'Fixbill is also available in English.', 'Open the English page'],
    'en-gb': ['/fixbill/en-gb/', 'There is a UK version of this page.', 'Open the UK page'],
    'cs': ['/fixbill/cs/', 'Fixbill je k dispozici i v češtině.', 'Přejít na českou stránku'],
    'sk': ['/fixbill/sk/', 'Fixbill je dostupný aj v slovenčine.', 'Prejsť na slovenskú stránku'],
    'de': ['/fixbill/de/', 'Fixbill gibt es auch auf Deutsch.', 'Zur deutschen Seite'],
    'fr': ['/fixbill/fr/', 'Fixbill existe aussi en français.', 'Voir la page en français'],
    'es': ['/fixbill/es/', 'Fixbill también está en español.', 'Ver la página en español'],
    'it': ['/fixbill/it/', 'Fixbill è disponibile anche in italiano.', 'Vai alla pagina in italiano'],
    'pl': ['/fixbill/pl/', 'Fixbill jest dostępny także po polsku.', 'Przejdź do polskiej strony'],
    'pt': ['/fixbill/pt/', 'O Fixbill também está em português.', 'Ver a página em português']
  };
  var here = document.documentElement.getAttribute('data-page-lang');
  if (!here) return;

  // Links from before November 2026 used one URL with #cs, #de and #fr.
  if (here === 'en') {
    var h = (location.hash || '').slice(1).toLowerCase();
    if (h && PAGES[h] && h !== 'en') { location.replace(PAGES[h][0]); return; }
  }

  var off = false;
  try { off = localStorage.getItem('fixbill-lang-hint') === 'off'; } catch (e) { /* ignore */ }
  if (off) return;
  var want = null, langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
  for (var i = 0; i < langs.length && !want; i++) {
    var l = String(langs[i] || '').toLowerCase();
    var base = l.split('-')[0];
    if (l === 'en-gb' || l === 'en-ie') want = 'en-gb';
    else if (PAGES[base]) want = base;
  }
  if (!want || want === here || (want === 'en' && here === 'en-gb') || (want === 'en-gb' && here === 'en')) return;
  var p = PAGES[want];
  var bar = document.createElement('div');
  bar.className = 'hint';
  bar.setAttribute('role', 'region');
  bar.setAttribute('aria-label', p[1]);
  bar.lang = want === 'en-gb' ? 'en-GB' : want;
  var t = document.createElement('span');
  t.textContent = p[1] + ' ';
  var a = document.createElement('a');
  a.href = p[0];
  a.hreflang = bar.lang;
  a.textContent = p[2];
  t.appendChild(a);
  var x = document.createElement('button');
  x.type = 'button';
  x.textContent = '×';
  x.setAttribute('aria-label', 'Close');
  x.addEventListener('click', function () {
    bar.remove();
    try { localStorage.setItem('fixbill-lang-hint', 'off'); } catch (e) { /* ignore */ }
  });
  bar.appendChild(t);
  bar.appendChild(x);
  document.body.insertBefore(bar, document.body.firstChild);
})();
