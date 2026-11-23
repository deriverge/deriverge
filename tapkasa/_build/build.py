#!/usr/bin/env python3
"""Builds the Tapkasa landing pages on deriverge.com (not the app: /tapkasa/index.html is never touched).

  Czech and English keep their old flat addresses (/tapkasa/pokladna.html, /tapkasa/pos.html, ...),
  the other languages live in /tapkasa/<lang>/ and /tapkasa/<lang>/<topic>/.

Texts are in texts_<lang>.py next to this file. The script also replaces the /tapkasa/ entries of /sitemap.xml
(other entries stay as they are). support.html, privacy.html and terms.html are hand-written (the stores link to them).

Run: python3 tapkasa/_build/build.py
"""
import datetime as dt
import html
import importlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TAP = os.path.dirname(HERE)
ROOT = os.path.dirname(TAP)
SITE = 'https://deriverge.com'
BASE = SITE + '/tapkasa/'
AS = 'https://apps.apple.com/app/id6807075649'  # no provider token in the repo, so no ?pt=&ct= campaign
GP = 'https://play.google.com/store/apps/details?id=com.deriverge.tapkasa'
MAIL = 'info@deriverge.com'
ASSET_V = '1'  # bump when landing.css or landing.js change: the app's service worker caches same-folder files
LEGAL_DATE = '2026-09-07'
CODES = ['cs', 'sk', 'en', 'de', 'pl', 'fr', 'it', 'es', 'pt']
TOPICS = ['stall', 'xmas', 'club', 'festival', 'fair']  # every language has the first three

# Tapkasa Pro prices per page language (currency, month, year) and the sentence under "What it costs".
# Store prices of 23 November 2026 (App Store and Google Play aligned that day). No Polish price is confirmed, so the
# Polish pages keep the general sentence only. Update together with the stores.
PRO_PRICES = {'cs': ('CZK', '129', '999'), 'en': ('USD', '4.99', '39.99'),
              **{c: ('EUR', '5.99', '44.99') for c in ('sk', 'de', 'fr', 'it', 'es', 'pt')}}
PRICE_LINE = {
    'cs': 'Tapkasa Pro stojí 129 Kč měsíčně nebo 999 Kč ročně (ceny v App Store a na Google Play v listopadu 2026). '
          'Platnou cenu vždy uvidíte před nákupem.',
    'sk': 'Tapkasa Pro stojí 5,99 € mesačne alebo 44,99 € ročne (ceny v App Store a na Google Play v novembri 2026). '
          'Platnú cenu vždy uvidíte pred nákupom.',
    'en': 'Tapkasa Pro costs $4.99 a month or $39.99 a year in the US (App Store and Google Play, November 2026; other '
          'countries differ). You always see the current price before you buy.',
    'de': 'Tapkasa Pro kostet 5,99 € im Monat oder 44,99 € im Jahr (Preise im App Store und bei Google Play, November '
          '2026). Den aktuellen Preis sehen Sie immer vor dem Kauf.',
    'fr': "Tapkasa Pro coûte 5,99 € par mois ou 44,99 € par an (prix sur l'App Store et Google Play en novembre 2026). "
          "Le prix en vigueur s'affiche toujours avant l'achat.",
    'it': "Tapkasa Pro costa 5,99 € al mese o 44,99 € all'anno (prezzi su App Store e Google Play a novembre 2026). "
          "Il prezzo aggiornato lo vedi sempre prima dell'acquisto.",
    'es': 'Tapkasa Pro cuesta 5,99 € al mes o 44,99 € al año (precios de App Store y Google Play en noviembre de '
          '2026). Siempre ves el precio vigente antes de comprar.',
    'pt': 'A Tapkasa Pro custa 5,99 € por mês ou 44,99 € por ano (preços na App Store e no Google Play em novembro de '
          '2026). Vê sempre o preço atual antes de comprar.',
}

e = html.escape
LANGS = {c: importlib.import_module('texts_' + c).T for c in CODES}

# One-line device switch in the head: phones see only their own store, computers both badges and a QR code.
OS_JS = ("<script>(function(d,u){d.classList.add(/android/i.test(u)?'os-android':(/iphone|ipad|ipod/i.test(u)||"
         "(/macintosh/i.test(u)&&navigator.maxTouchPoints>1))?'os-ios':'os-desktop')})"
         "(document.documentElement,navigator.userAgent)</script>")


def fr_spaces(obj):
    """French typography: no-break space before : ; ? ! and inside guillemets."""
    if isinstance(obj, str):
        for a, b in ((' :', ' :'), (' ;', ' ;'), (' ?', ' ?'), (' !', ' !'),
                     ('« ', '« '), (' »', ' »')):
            obj = obj.replace(a, b)
        return obj
    if isinstance(obj, dict):
        return {k: (v if k in ('path', 'html_lang', 'hreflang', 'og_locale', 'gp_badge') else fr_spaces(v))
                for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return type(obj)(fr_spaces(v) for v in obj)
    return obj


LANGS['fr'] = fr_spaces(LANGS['fr'])
PRICE_LINE['fr'] = fr_spaces(PRICE_LINE['fr'])


def url(path):
    return BASE + path


def href(path):
    return '/tapkasa/' + path


def gp_link(campaign, medium='landing'):
    return f'{GP}&referrer=utm_source%3Dweb%26utm_medium%3D{medium}%26utm_campaign%3D{campaign}'


def ld(obj):
    return ('<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1)
            .replace('</', '<\\/') + '\n</script>')


def get_block(L, campaign):
    cs = L['gp_badge'].endswith('-cs.png')  # the Czech badge artwork has no side padding
    return f'''<div class="get">
        <div class="stores">
          <a class="as" href="{AS}"><img src="/tapkasa/badge-appstore.svg" alt="{e(L["as_alt"])}" width="156" height="52"></a>
          <a class="gp{" cs" if cs else ""}" href="{e(gp_link(campaign))}"><img src="/tapkasa/{L["gp_badge"]}" alt="{e(L["gp_alt"])}" width="{175 if cs else 199}" height="{68 if cs else 77}"></a>
        </div>
        <a class="btn try" href="/tapkasa/">{e(L["try_btn"])}</a>
      </div>
      <p class="qr"><img src="/tapkasa/qr-get.svg" alt="{e(L["qr_alt"])}" width="92" height="92" loading="lazy"><span>{e(L["qr_text"])}</span></p>'''


def lang_menu(code, topic):
    items = []
    for c in CODES:
        M = LANGS[c]
        if topic not in M['pages']:
            continue
        if c == code:
            items.append(f'<li><strong aria-current="page">{e(M["name"])}</strong></li>')
        else:
            items.append(f'<li><a href="{href(M["pages"][topic]["path"])}" lang="{M["html_lang"]}" '
                         f'hreflang="{M["hreflang"]}">{e(M["name"])}</a></li>')
    if len(items) < 2:
        return ''
    L = LANGS[code]
    return (f'<nav aria-label="{e(L["menu"])}"><details class="lang"><summary aria-label="{e(L["menu"])}: '
            f'{e(L["name"])}">{e(L["name"])}</summary><ul>{"".join(items)}</ul></details></nav>')


def offers(code):
    L = LANGS[code]
    out = [{'@type': 'Offer', 'price': '0', 'priceCurrency': L['currency'], 'description': L['offer']}]
    if code in PRO_PRICES:
        cur, month, year = PRO_PRICES[code]
        out += [{'@type': 'Offer', 'name': f'Tapkasa Pro ({n})', 'price': v, 'priceCurrency': cur,
                 'category': 'in-app subscription'} for n, v in (('1 month', month), ('1 year', year))]
    return out


def page(code, topic):
    L = LANGS[code]
    P = L['pages'][topic]
    u = url(P['path'])
    home = L['pages']['stall']
    campaign = f'tapkasa-{code}-{topic}'
    alts = [(LANGS[c]['hreflang'], url(LANGS[c]['pages'][topic]['path'])) for c in CODES if topic in LANGS[c]['pages']]
    alt_html = ''
    if len(alts) > 1:
        alts.append(('x-default', url(LANGS['en']['pages'][topic]['path'])))
        alt_html = ''.join(f'\n<link rel="alternate" hreflang="{h}" href="{x}">' for h, x in alts)
    faq = list(P['faq']) + list(L['faq'])
    data = [
        {'@context': 'https://schema.org', '@type': 'MobileApplication', 'name': 'Tapkasa',
         'operatingSystem': 'iOS, Android', 'applicationCategory': 'BusinessApplication',
         'inLanguage': L['hreflang'], 'description': L['ld_desc'], 'url': u, 'downloadUrl': AS, 'installUrl': GP,
         'sameAs': [AS, GP], 'image': BASE + 'icon-512.png',
         'offers': offers(code),
         'publisher': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': SITE + '/'}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': L['hreflang'], 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]},
    ]
    crumbs = ''
    if topic != 'stall':
        data.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Tapkasa', 'item': url(home['path'])},
            {'@type': 'ListItem', 'position': 2, 'name': P['card'], 'item': u}]})
        crumbs = (f'\n  <nav class="crumbs" aria-label="Breadcrumb"><a href="{href(home["path"])}">Tapkasa</a> '
                  f'&rsaquo; <span>{e(P["card"])}</span></nav>')
    sections = '\n'.join(f'    <h2>{e(h)}</h2>\n    {body}' for h, body in P['sections'])
    steps = '\n'.join(f'    <li><h3>{e(h)}</h3><p>{e(p)}</p></li>' for h, p in L['how'])
    feats = '\n'.join(f'    <div class="card"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in L['feats'])
    nots = '\n'.join(f'      <li>{e(n)}</li>' for n in L['nots'])
    price = '\n'.join(f'    <p>{e(p)}</p>' for p in L['price'])
    if code in PRICE_LINE:
        price += f'\n    <p><strong>{e(PRICE_LINE[code])}</strong></p>'
    shots = '\n'.join(f'    <img src="/tapkasa/{f}" alt="{e(a)}" width="369" height="800" loading="lazy">'
                      for f, a in zip(('shot-prodej.png', 'shot-fronta.png', 'shot-dph.png'), L['shot_alts']))
    faq_html = '\n'.join(f'    <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    more = '\n'.join(f'    <li><a href="{href(L["pages"][t]["path"])}">{e(L["pages"][t]["card"])}</a></li>'
                     for t in TOPICS if t in L['pages'] and t != topic)
    anchor = '#' + code
    foot_langs = ' &middot; '.join(
        f'<a href="{href(LANGS[c]["pages"]["stall"]["path"])}" lang="{LANGS[c]["html_lang"]}" '
        f'hreflang="{LANGS[c]["hreflang"]}">{e(LANGS[c]["name"])}</a>' for c in CODES if c != code)
    og_type = 'website' if topic == 'stall' else 'article'
    return f'''<!DOCTYPE html>
<html lang="{L["html_lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(P["title"])}</title>
<meta name="description" content="{e(P["desc"])}">
<link rel="canonical" href="{u}">{alt_html}
<link rel="icon" type="image/png" sizes="192x192" href="/tapkasa/icon-192.png">
<link rel="apple-touch-icon" href="/tapkasa/apple-touch-icon.png">
<meta name="apple-itunes-app" content="app-id=6807075649">
<meta name="theme-color" content="#FBFAF7">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Tapkasa">
<meta property="og:title" content="{e(P["h1"])}">
<meta property="og:description" content="{e(P["desc"])}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{BASE}og.png">
<meta property="og:image:width" content="1024">
<meta property="og:image:height" content="500">
<meta property="og:image:alt" content="Tapkasa">
<meta property="og:locale" content="{L["og_locale"]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/tapkasa/landing.css?v={ASSET_V}">
{OS_JS}
<script src="/tapkasa/landing.js?v={ASSET_V}" defer></script>
{ld(data)}
</head>
<body>
<div class="page">
  <header class="top">
    <a class="brand" href="{href(home["path"])}"><span class="logo" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span><b>Tapkasa</b><small>{e(L["brand_sub"])}</small></span></a>
    {lang_menu(code, topic)}
  </header>
<main>{crumbs}
  <section class="hero">
    <div>
      <p class="eyebrow">{e(P["eyebrow"])}</p>
      <h1>{e(P["h1"])}</h1>
      <p class="lede">{e(P["lede"])}</p>
      {get_block(L, campaign)}
      <p class="note">{e(L["note"])}</p>
    </div>
    <div class="heroimg"><img src="/tapkasa/shot-prodej.png" alt="{e(L["shot_alts"][0])}" width="369" height="800" fetchpriority="high"></div>
  </section>

  <article class="prose">
{sections}
  </article>

  <h2>{e(L["h_how"])}</h2>
  <ol class="steps">
{steps}
  </ol>

  <h2>{e(L["h_feat"])}</h2>
  <div class="grid">
{feats}
  </div>

  <h2>{e(L["h_shots"])}</h2>
  <div class="shots">
{shots}
  </div>

  <section class="isnot">
    <h2>{e(L["h_not"])}</h2>
    <ul>
{nots}
    </ul>
    <p>{e(L["not_p"])}</p>
  </section>

  <h2>{e(L["h_price"])}</h2>
  <div class="prose">
{price}
  </div>

  <h2>{e(L["h_faq"])}</h2>
  <div class="faq">
{faq_html}
  </div>

  <section class="cta">
    <h2>{e(L["cta_h"])}</h2>
    {get_block(L, campaign + '-cta')}
    <p class="note">{e(L["note"])}</p>
  </section>

  <h2>{e(L["h_more"])}</h2>
  <ul class="more">
{more}
  </ul>
</main>
  <footer>
    <p><a href="/tapkasa/support.html{anchor}">{e(L["f_support"])}</a> &middot; <a href="/tapkasa/privacy.html{anchor}">{e(L["f_privacy"])}</a> &middot; <a href="/tapkasa/terms.html{anchor}">{e(L["f_terms"])}</a> &middot; <a href="/tapkasa/">{e(L["f_app"])}</a></p>
    <p>{e(L["f_langs"])}: {foot_langs}</p>
    <p>{e(L["f_operator"])}: <a href="/">deriverge s.r.o.</a> &middot; <a href="mailto:{MAIL}">{MAIL}</a></p>
  </footer>
</div>
<div class="sticky"><span><b>Tapkasa</b><small>{e(L["sticky"])}</small></span><a class="btn primary" href="{e(gp_link(campaign + "-bar"))}">Google Play</a></div>
</body>
</html>
'''


def update_sitemap(today):
    p = os.path.join(ROOT, 'sitemap.xml')
    xml = open(p, encoding='utf-8').read()
    pat = re.compile(r'[ \t]*<url>\s*<loc>https://deriverge\.com/tapkasa/[^<]*</loc>.*?</url>\n?', re.S)
    first = pat.search(xml)
    if not first:
        raise SystemExit('sitemap.xml has no /tapkasa/ entry to replace')
    pos = first.start()
    xml = pat.sub('', xml)
    blocks = []
    for topic in TOPICS:
        have = [c for c in CODES if topic in LANGS[c]['pages']]
        alt = ''
        if len(have) > 1:
            alt = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{LANGS[c]["hreflang"]}" '
                          f'href="{url(LANGS[c]["pages"][topic]["path"])}"/>' for c in have)
            alt += (f'\n    <xhtml:link rel="alternate" hreflang="x-default" '
                    f'href="{url(LANGS["en"]["pages"][topic]["path"])}"/>')
        for c in have:
            prio = '0.9' if topic == 'stall' and c in ('cs', 'en') else '0.8' if topic in ('stall', 'xmas') else '0.7'
            blocks.append(f'  <url>\n    <loc>{url(LANGS[c]["pages"][topic]["path"])}</loc>\n    <lastmod>{today}</lastmod>\n'
                          f'    <priority>{prio}</priority>{alt}\n  </url>\n')
    blocks.append(f'  <url><loc>{BASE}</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>\n')
    for name, prio in (('support', '0.5'), ('privacy', '0.3'), ('terms', '0.3')):
        blocks.append(f'  <url><loc>{BASE}{name}.html</loc><lastmod>{LEGAL_DATE}</lastmod>'
                      f'<priority>{prio}</priority></url>\n')
    xml = xml[:pos] + ''.join(blocks) + xml[pos:]
    open(p, 'w', encoding='utf-8').write(xml)


def write(rel, text):
    if '—' in text or '–' in text:
        i = max(text.find('—'), text.find('–'))
        raise SystemExit(f'long dash in {rel}: ...{text[max(0, i - 60):i + 20]}...')
    for bad in ('mojekafe', 'href="tel:'):
        if bad in text:
            raise SystemExit(f'{bad} in {rel}')
    if rel in ('index.html', 'support.html', 'privacy.html', 'terms.html', 'get.html'):
        raise SystemExit(f'refusing to overwrite {rel}')
    path = os.path.join(TAP, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', os.path.relpath(path, ROOT))


def main():
    seen = {}
    for code in CODES:
        for topic, P in LANGS[code]['pages'].items():
            if topic not in TOPICS:
                raise SystemExit(f'unknown topic {topic} in {code}')
            for k in ('title', 'desc'):
                if P[k] in seen:
                    raise SystemExit(f'duplicate {k}: {code}/{topic} and {seen[P[k]]}')
                seen[P[k]] = f'{code}/{topic}'
            rel = P['path'] + ('index.html' if P['path'].endswith('/') else '')
            write(rel, page(code, topic))
    update_sitemap(dt.date.today().isoformat())
    print('sitemap.xml updated')


if __name__ == '__main__':
    main()
