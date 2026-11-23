#!/usr/bin/env python3
"""Builds the Fixbill pages on deriverge.com.

  /fixbill/                 English (x-default)       /fixbill/<lang>/   en-gb, cs, sk, de, fr, es, it, pl, pt
  /fixbill/<template>/...   template pages with an in-browser generator (texts_intent.py)

and replaces the /fixbill/ entries of /sitemap.xml (other entries stay as they are).
privacy.html, support.html and terms.html are hand-written and not touched (the stores link to them).

Run: python3 fixbill/_build/build.py
"""
import datetime as dt
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texts_lang import LANGS  # noqa: E402
from texts_intent import CS, DE, EN, ES, FR, GB, IT, PL  # noqa: E402
from texts_intent2 import (CS_NABIDKA, DE_RECHNUNG, EN_INVOICE, FR_FACTURE, GB_QUOTE, PT_ORCAMENTO,  # noqa: E402
                           SK_FAKTURA, SK_PONUKA)
from texts_extra import FAQ, LANG_EXTRA, PRO_PRICES, TPL_HEAD  # noqa: E402

PAGES = [EN, EN_INVOICE, GB, GB_QUOTE, CS, CS_NABIDKA, SK_FAKTURA, SK_PONUKA, DE, DE_RECHNUNG, FR, FR_FACTURE, ES,
         IT, PL, PT_ORCAMENTO]

FIX = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(FIX)
SITE = 'https://deriverge.com'
BASE = SITE + '/fixbill/'
AS = 'https://apps.apple.com/app/id6819481858'  # no provider token in the repo, so no ?pt=&ct= campaign
GP = 'https://play.google.com/store/apps/details?id=com.deriverge.fixbill'
MAIL = 'info@deriverge.com'
LEGAL_DATE = '2026-10-06'
ASSET_V = '2'  # bump when fixbill.css changes

e = html.escape
BY_CODE = {L['code']: L for L in LANGS}
for _L in LANGS:
    _x = LANG_EXTRA[_L['code']]
    _L.update(h_faq=_x[0], h_related=_x[1], qr_alt=_x[2], qr_text=_x[3], price_line=_x[4])
    if _L['code'] in TPL_HEAD:
        _L['h_tpl'], _L['tpl_sub'] = TPL_HEAD[_L['code']]
for _P in PAGES:
    _P.setdefault('faq', FAQ.get(_P['id'], []))

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
        return {k: fr_spaces(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return type(obj)(fr_spaces(v) for v in obj)
    return obj


for i, L in enumerate(LANGS):
    if L['code'] == 'fr':
        LANGS[i] = BY_CODE['fr'] = fr_spaces(L)
for i, P in enumerate(PAGES):
    if P['lang'] == 'fr':
        PAGES[i] = fr_spaces(P)


def gp_link(campaign, medium='landing'):
    return f'{GP}&referrer=utm_source%3Dweb%26utm_medium%3D{medium}%26utm_campaign%3D{campaign}'


def badges(L, campaign, qr=True):
    """Store buttons: phones see their own store (class on <html>), computers both and a QR code to /fixbill/get/."""
    cs = L['gp_badge'].endswith('-cs.png')  # the Czech Google Play artwork has no side padding
    gp_cls, gp_w, gp_h = ('gp cs', 162, 63) if cs else ('gp', 184, 71)
    code = (f'\n      <p class="dl-qr"><img src="/fixbill/qr-get.svg" alt="{e(L["qr_alt"])}" width="88" height="88" '
            f'loading="lazy"><span>{e(L["qr_text"])}</span></p>') if qr else ''
    return (f'<div class="badges">\n'
            f'        <a class="s-as" href="{AS}"><img class="as" src="/fixbill/badge-appstore.svg" '
            f'alt="{e(L["as_alt"])}" width="144" height="48"></a>\n'
            f'        <a class="s-gp" href="{e(gp_link(campaign))}"><img class="{gp_cls}" '
            f'src="/fixbill/{L["gp_badge"]}" alt="{e(L["gp_alt"])}" width="{gp_w}" height="{gp_h}"></a>\n'
            f'      </div>{code}')


SPRITE = '''<svg class="sprite" aria-hidden="true" focusable="false">
  <symbol id="i-doc" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/></g></symbol>
  <symbol id="i-qr" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><path d="M14 14h2v2h-2zM18 18h2v2h-2zM14 19.5v.5M19.5 14h.5"/></g></symbol>
  <symbol id="i-pen" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 4l4.5 4.5L9 19H4.5v-4.5z"/><path d="M12.5 6.5L17 11M13 21h7"/></g></symbol>
  <symbol id="i-users" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20v-.5A5.5 5.5 0 0 1 8 14h2a5.5 5.5 0 0 1 5.5 5.5v.5M16 4.6a3.5 3.5 0 0 1 0 6.8M18.5 14.2a5.5 5.5 0 0 1 3 4.9v.9"/></g></symbol>
  <symbol id="i-bell" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 1.5h-15z"/><path d="M10 21a2 2 0 0 0 4 0"/></g></symbol>
  <symbol id="i-bank" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 4l9 5.5zM5 10v8M9.7 10v8M14.3 10v8M19 10v8M3 20.5h18"/></g></symbol>
  <symbol id="i-stack" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="3" width="12" height="15" rx="2"/><path d="M5 7v12a2 2 0 0 0 2 2h9M10 8h6M10 12h6"/></g></symbol>
  <symbol id="i-tag" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 12.2V4.5a1 1 0 0 1 1-1h7.7l8.3 8.3a1.5 1.5 0 0 1 0 2.1l-6.4 6.4a1.5 1.5 0 0 1-2.1 0z"/><circle cx="8" cy="8" r="1.4"/></g></symbol>
  <symbol id="i-globe" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></g></symbol>
  <symbol id="qr" viewBox="0 0 25 25"><path fill="currentColor" shape-rendering="crispEdges" d="M0 0h7v1H0zM8 0h1v1H8zM13 0h1v1H13zM18 0h7v1H18zM0 1h1v1H0zM6 1h1v1H6zM9 1h4v1H9zM14 1h3v1H14zM18 1h1v1H18zM24 1h1v1H24zM0 2h1v1H0zM2 2h3v1H2zM6 2h1v1H6zM8 2h3v1H8zM12 2h5v1H12zM18 2h1v1H18zM20 2h3v1H20zM24 2h1v1H24zM0 3h1v1H0zM2 3h3v1H2zM6 3h1v1H6zM8 3h3v1H8zM12 3h1v1H12zM14 3h1v1H14zM16 3h1v1H16zM18 3h1v1H18zM20 3h3v1H20zM24 3h1v1H24zM0 4h1v1H0zM2 4h3v1H2zM6 4h1v1H6zM8 4h2v1H8zM12 4h1v1H12zM15 4h1v1H15zM18 4h1v1H18zM20 4h3v1H20zM24 4h1v1H24zM0 5h1v1H0zM6 5h1v1H6zM9 5h2v1H9zM12 5h5v1H12zM18 5h1v1H18zM24 5h1v1H24zM0 6h7v1H0zM8 6h1v1H8zM10 6h1v1H10zM12 6h1v1H12zM14 6h1v1H14zM16 6h1v1H16zM18 6h7v1H18zM8 7h1v1H8zM10 7h4v1H10zM15 7h2v1H15zM1 8h1v1H1zM6 8h1v1H6zM8 8h1v1H8zM12 8h1v1H12zM15 8h1v1H15zM17 8h6v1H17zM24 8h1v1H24zM1 9h1v1H1zM3 9h1v1H3zM8 9h1v1H8zM10 9h4v1H10zM16 9h1v1H16zM19 9h1v1H19zM21 9h4v1H21zM0 10h2v1H0zM3 10h1v1H3zM5 10h2v1H5zM8 10h5v1H8zM16 10h1v1H16zM20 10h1v1H20zM24 10h1v1H24zM1 11h4v1H1zM13 11h1v1H13zM16 11h1v1H16zM19 11h3v1H19zM24 11h1v1H24zM0 12h3v1H0zM4 12h1v1H4zM6 12h2v1H6zM13 12h2v1H13zM16 12h7v1H16zM24 12h1v1H24zM1 13h5v1H1zM9 13h1v1H9zM11 13h2v1H11zM14 13h3v1H14zM18 13h1v1H18zM21 13h1v1H21zM24 13h1v1H24zM1 14h1v1H1zM6 14h1v1H6zM10 14h1v1H10zM12 14h3v1H12zM18 14h1v1H18zM21 14h1v1H21zM23 14h1v1H23zM1 15h5v1H1zM8 15h1v1H8zM11 15h5v1H11zM18 15h5v1H18zM24 15h1v1H24zM2 16h1v1H2zM6 16h2v1H6zM9 16h1v1H9zM11 16h1v1H11zM13 16h1v1H13zM15 16h6v1H15zM22 16h3v1H22zM10 17h1v1H10zM13 17h4v1H13zM20 17h2v1H20zM23 17h1v1H23zM0 18h7v1H0zM8 18h1v1H8zM10 18h2v1H10zM14 18h3v1H14zM18 18h1v1H18zM20 18h1v1H20zM23 18h1v1H23zM0 19h1v1H0zM6 19h1v1H6zM14 19h1v1H14zM16 19h1v1H16zM20 19h2v1H20zM23 19h2v1H23zM0 20h1v1H0zM2 20h3v1H2zM6 20h1v1H6zM10 20h5v1H10zM16 20h6v1H16zM24 20h1v1H24zM0 21h1v1H0zM2 21h3v1H2zM6 21h1v1H6zM9 21h1v1H9zM11 21h5v1H11zM20 21h2v1H20zM23 21h2v1H23zM0 22h1v1H0zM2 22h3v1H2zM6 22h1v1H6zM10 22h2v1H10zM13 22h2v1H13zM16 22h2v1H16zM21 22h1v1H21zM23 22h2v1H23zM0 23h1v1H0zM6 23h1v1H6zM11 23h4v1H11zM19 23h6v1H19zM0 24h7v1H0zM8 24h3v1H8zM14 24h1v1H14zM17 24h1v1H17zM19 24h6v1H19z"/></symbol>
  <symbol id="sig" viewBox="0 0 120 40"><path fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" d="M4 30c8-10 14-20 19-19 6 1-6 21 0 21s12-22 19-21c6 1-5 17 1 17 5 0 8-9 13-9 4 0 2 7 7 7 6 0 10-6 17-7 8-1 14 1 36-3"/></symbol>
</svg>'''


def url_of(L):
    return BASE + L['path']


def ld(obj):
    return ('<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1)
            .replace('</', '<\\/') + '\n</script>')


def publisher():
    return {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': SITE + '/'}


def app_ld(L, url):
    return {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'Fixbill',
        'operatingSystem': 'iOS, Android', 'applicationCategory': 'BusinessApplication',
        'inLanguage': L['hreflang'], 'description': L['ld_desc'], 'url': url,
        'downloadUrl': AS, 'installUrl': GP, 'sameAs': [AS, GP], 'image': BASE + 'icon-512.png',
        'offers': offers(L),
        'publisher': publisher(),
    }


def offers(L):
    cur, month, year, life = PRO_PRICES[L['code']]
    out = [{'@type': 'Offer', 'price': '0', 'priceCurrency': cur, 'description': L['offer']}]
    for name, price in (('Fixbill Pro (1 month)', month), ('Fixbill Pro (1 year)', year),
                        ('Fixbill Pro (lifetime)', life)):
        out.append({'@type': 'Offer', 'name': name, 'price': price, 'priceCurrency': cur,
                    'category': 'in-app purchase'})
    return out


def head(*, lang, title, desc, url, og_title, og_desc, og_locale, alternates, extra_ld, page_lang=None,
         scripts=()):
    alt = ''.join(f'\n<link rel="alternate" hreflang="{h}" href="{u}">' for h, u in alternates)
    og_alt = ''
    if alternates:
        og_alt = ''.join(f'\n<meta property="og:locale:alternate" content="{L["og_locale"]}">'
                         for L in LANGS if L['og_locale'] != og_locale)
    data = f' data-page-lang="{page_lang}"' if page_lang else ''
    js = ''.join(f'\n<script src="{s}" defer></script>' for s in scripts)
    if len(title) > 65 and title.endswith(' | Fixbill'):
        title = title[:-len(' | Fixbill')]  # the search phrase matters more than the brand in a long title
    return f'''<!DOCTYPE html>
<html lang="{lang}"{data}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">{alt}
<link rel="icon" type="image/png" sizes="192x192" href="/fixbill/icon-192.png">
<link rel="apple-touch-icon" href="/fixbill/icon-192.png">
<meta name="apple-itunes-app" content="app-id=6819481858">
<meta name="theme-color" content="#F5F7FB" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A0F18" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Fixbill">
<meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(og_desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Fixbill">
<meta property="og:locale" content="{og_locale}">{og_alt}
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/fixbill/fixbill.css?v={ASSET_V}">
{OS_JS}{js}
{extra_ld}
</head>'''


def legal_links(L):
    a = L['legal']
    suf = '' if a else L['en_suffix']
    h = (lambda p: f'/fixbill/{p}.html#{a}') if a else (lambda p: f'/fixbill/{p}.html')
    return (f'<a href="{h("support")}">{e(L["f_support"])}{suf}</a> &middot; '
            f'<a href="{h("privacy")}">{e(L["f_privacy"])}{suf}</a> &middot; '
            f'<a href="{h("terms")}">{e(L["f_terms"])}{suf}</a>')


def lang_links(current):
    out = []
    for L in LANGS:
        if L['code'] == current:
            out.append(f'<strong aria-current="page">{e(L["name"])}</strong>')
        else:
            out.append(f'<a href="/fixbill/{L["path"]}" lang="{L["html_lang"]}" hreflang="{L["hreflang"]}">'
                       f'{e(L["name"])}</a>')
    return ' &middot; '.join(out)


def template_links():
    return ' &middot; '.join(f'<a href="/fixbill/{P["path"]}" lang="{P["html_lang"]}">{e(P["card"])}</a>'
                             for P in PAGES)


def footer(L):
    return f'''  <footer>
    <p>{legal_links(L)}</p>
    <p>{e(L["f_templates"])}: {template_links()}</p>
    <p>{e(L["f_langs"])}: {lang_links(L["code"])}</p>
    <p>{e(L["f_operator"])}: <a href="/">deriverge s.r.o.</a> &middot; <a href="mailto:{MAIL}">{MAIL}</a></p>
  </footer>'''


def lang_menu(L):
    items = []
    for M in LANGS:
        if M['code'] == L['code']:
            items.append(f'<li><strong aria-current="page">{e(M["name"])}</strong></li>')
        else:
            items.append(f'<li><a href="/fixbill/{M["path"]}" lang="{M["html_lang"]}" hreflang="{M["hreflang"]}">'
                         f'{e(M["name"])}</a></li>')
    return (f'<details class="lang"><summary aria-label="{e(L["menu"])}: {e(L["name"])}"><svg aria-hidden="true">'
            f'<use href="#i-globe"/></svg>{e(L["name"])}</summary>\n      <ul>{"".join(items)}</ul></details>')


def brand(L, href):
    return (f'<a class="brand" href="{href}"><img class="logo" src="/fixbill/icon-192.png" alt="" width="46" '
            f'height="46"><span><b>Fixbill</b><small>{e(L["brand_sub"])}</small></span></a>')


def templates_for(L):
    if L['code'] in ('en', 'en-gb'):
        return [P for P in PAGES if P['lang'] in ('en', 'en-gb')]
    return [P for P in PAGES if P['lang'] == L['code']]


# ---------------------------------------------------------------- language pages

def lang_page(L):
    url = url_of(L)
    alternates = [(M['hreflang'], url_of(M)) for M in LANGS] + [('x-default', BASE)]
    m = L['mock']
    camp = 'fixbill-' + L['code']
    lines = '\n'.join(f'          <li><span>{e(a)}<small>{e(b)}</small></span><b>{e(c)}</b></li>'
                      for a, b, c in m['lines'])
    cards = []
    for i, (icon, pro, h, p) in enumerate(L['cards']):
        a = ' a' if i % 2 else ''
        badge = '<span class="pro">PRO</span>' if pro else ''
        cards.append(f'    <div class="card"><span class="ic{a}"><svg aria-hidden="true"><use href="#i-{icon}"/></svg>'
                     f'</span><h3>{e(h)}{badge}</h3><p>{e(p)}</p></div>')
    plans = '\n'.join(f'    <div class="plan{" hi" if hi else ""}"><p class="k">{e(k)}</p><h3>{e(h)}</h3><p>{e(p)}</p>'
                      f'</div>' for k, h, p, hi in L['plans'])
    checks = '\n'.join(f'      <li>{e(c)}</li>' for c in L['checks'])
    tpls = templates_for(L)
    tpl_html = ''
    if tpls and L['h_tpl']:
        cards_t = '\n'.join(
            f'    <a class="card" href="/fixbill/{P["path"]}"{"" if P["html_lang"].lower() == L["html_lang"].lower() else " lang=" + chr(34) + P["html_lang"] + chr(34)}>'
            f'<span class="ic"><svg aria-hidden="true"><use href="#i-doc"/></svg></span><h3>{e(P["card"])}</h3>'
            f'<p>{e(P["card_text"])}</p><span class="go">{e(P["jump"])} &rarr;</span></a>' for P in tpls)
        tpl_html = f'''
  <h2>{e(L["h_tpl"])}</h2>
  <p class="sub">{e(L["tpl_sub"])}</p>
  <div class="grid">
{cards_t}
  </div>
'''
    priv_href = f'/fixbill/privacy.html#{L["legal"]}' if L['legal'] else '/fixbill/privacy.html'
    cta_sub = e(L['cta_sub']).replace('{mail}', f'<a href="mailto:{MAIL}">{MAIL}</a>')
    out = head(lang=L['html_lang'], title=L['title'], desc=L['desc'], url=url, og_title=L['og_title'],
               og_desc=L['og_desc'], og_locale=L['og_locale'], alternates=alternates, extra_ld=ld(app_ld(L, url)),
               page_lang=L['code'], scripts=['/fixbill/fixbill.js'])
    out += f'''
<body>
{SPRITE}
<div class="page">
  <header class="top">
    {brand(L, "/fixbill/" + L["path"])}
    <nav aria-label="{e(L["menu"])}">{lang_menu(L)}</nav>
  </header>
<main>
  <section class="hero">
    <div>
      <p class="eyebrow">{e(L["eyebrow"])}</p>
      <h1>{L["h1"]}</h1>
      <p class="lede">{e(L["lede"])}</p>
      {badges(L, camp)}
      <p class="note">{e(L["note"])}</p>
    </div>
    <div class="hero-art" role="img" aria-label="{e(L["hero_alt"])}">
      <div class="mock">
        <div class="m-top"><div class="m-biz"><i class="m-logo"></i><span><b>{e(m["biz"])}</b><small>{e(m["doc"])}</small></span></div><span class="chip">{e(m["chip"])}</span></div>
        <p class="m-job">{e(m["job"])}</p>
        <ul class="m-lines">
{lines}
        </ul>
        <div class="m-total"><span>{e(m["total_label"])}</span><b>{e(m["total"])}</b></div>
        <div class="m-pay"><svg class="qr"><use href="#qr"/></svg><span><b>{e(m["pay_b"])}</b><small>{e(m["pay_s"])}</small></span></div>
      </div>
      <div class="m-sign"><svg><use href="#sig"/></svg><span>{e(m["sign"])}</span></div>
    </div>
  </section>

  <h2>{e(L["h_feat"])}</h2>
  <div class="grid">
{chr(10).join(cards)}
  </div>
{tpl_html}
  <h2>{e(L["h_price"])}</h2>
  <p class="sub">{e(L["price_sub"])}</p>
  <div class="plans">
{plans}
  </div>
  <p class="price-line">{e(L["price_line"])}</p>

  <section class="private">
    <div>
      <h2>{e(L["priv_h"])}</h2>
      <p>{e(L["priv_p"])}</p>
      <p><a href="{priv_href}">{e(L["priv_link"])}</a></p>
    </div>
    <ul class="checks">
{checks}
    </ul>
  </section>

  <div class="cta">
    <img class="appicon" src="/fixbill/icon-512.png" alt="" width="96" height="96">
    <h2>{e(L["cta_h"])}</h2>
    <p class="sub">{cta_sub}</p>
    {badges(L, camp + '-cta', qr=False)}
    <p class="note">{e(L["note"])}</p>
  </div>
</main>
{footer(L)}
</div>
</body>
</html>
'''
    return out


# ---------------------------------------------------------------- template pages

def field(f, G):
    name, label, kind, ph, default, extra = f
    wide = kind == 'area' or name in ('s_name', 'b_name', 'start', 'terms', 's_extra', 'method', 'tax', 'notes')
    cls = ' class="w"' if wide else ''
    attrs = f'name="{name}" id="f-{name}" data-f data-label="{e(label)}"'
    if ph:
        attrs += f' placeholder="{e(ph)}"'
    if kind == 'text':
        mode = ' inputmode="decimal"' if name == 'taxrate' else ''
        ctl = f'<input type="text" {attrs} value="{e(default)}"{mode}>'
    elif kind == 'area':
        rows = 3 if '\n' in (ph or default or '') or name == 'notes' else 2
        ctl = f'<textarea {attrs} rows="{rows}">{e(default)}</textarea>'
    elif kind == 'date':
        ctl = f'<input type="date" {attrs} data-off="{extra}">'
    elif kind == 'sel':
        opts = ''.join(f'<option value="{e(v)}"{" selected" if v == default else ""}>{e(t)}</option>'
                       for v, t in extra)
        ctl = f'<select {attrs}>{opts}</select>'
    elif kind == 'tax':
        opts = ''.join(f'<option value="{e(v)}"{f" data-note={chr(34)}{e(n)}{chr(34)}" if n else ""}'
                       f'{f" data-tax={chr(34)}{e(t)}{chr(34)}" if t else ""}>{e(lbl)}</option>'
                       for v, lbl, n, t in G['tax'])
        ctl = f'<select {attrs}>{opts}</select>'
    else:
        raise ValueError(kind)
    return f'<label{cls}>{e(label)}{ctl}</label>'


def gen_html(P):
    G = P['gen']
    U = G['ui']
    parts = []
    for grp in G['groups']:
        if grp == 'items':
            parts.append(f'''      <fieldset>
        <legend>{e(U["items"])}</legend>
        <div id="gen-items" class="items"></div>
        <div class="gen-actions"><button type="button" class="btn" id="gen-add">+ {e(U["add"])}</button></div>
      </fieldset>''')
            continue
        legend, fs = grp
        inner = '\n          '.join(field(f, G) for f in fs)
        parts.append(f'''      <fieldset>
        <legend>{e(legend)}</legend>
        <div class="gf">
          {inner}
        </div>
      </fieldset>''')
    cfg = dict(id=P['id'], locale=G['locale'], currency=G['currency'], decComma=G['decComma'],
               refFromNumber=G['refFromNumber'], dates=G['dates'], pay=G['pay'], sign=G['sign'], made=G['made'],
               doc=G['doc'], ui={k: U[k] for k in ('desc', 'qty', 'unit', 'price', 'remove', 'resetAsk')},
               items=G['items'])
    cfg_json = json.dumps(cfg, ensure_ascii=False).replace('</', '<\\/')
    return f'''  <section class="gen" id="gen" aria-label="{e(P["jump"])}">
    <form class="gen-form" id="gen-form" autocomplete="off" novalidate>
{chr(10).join(parts)}
      <div class="gen-actions">
        <button type="button" class="btn primary gen-print">{e(U["print"])}</button>
        <button type="button" class="btn" id="gen-reset">{e(U["reset"])}</button>
      </div>
      <p class="gen-note">{e(U["privacy"])}</p>
    </form>
    <div class="gen-side">
      <div class="gen-actions"><button type="button" class="btn primary gen-print">{e(U["print"])}</button></div>
      <div id="gen-doc" role="region" aria-label="{e(U["preview"])}"><noscript><p>{e(U["noscript"])}</p></noscript></div>
    </div>
    <script type="application/json" id="gen-cfg">{cfg_json}</script>
  </section>'''


def intent_page(P):
    L = BY_CODE[P['lang']]
    url = BASE + P['path']
    lang_url = url_of(L)
    camp = 'tpl-' + P['id']
    data = [
        {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': P['h1'], 'url': url,
         'description': P['desc'], 'inLanguage': P['html_lang'], 'applicationCategory': 'BusinessApplication',
         'operatingSystem': 'Any', 'browserRequirements': 'Requires JavaScript',
         'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': P['gen']['currency']},
         'publisher': publisher()},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Fixbill', 'item': lang_url},
            {'@type': 'ListItem', 'position': 2, 'name': P['card'], 'item': url}]},
    ]
    a = P['app']
    bullets = '\n'.join(f'        <li>{e(b)}</li>' for b in a['bullets'])
    faq_html = ''
    if P['faq']:
        data.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': P['html_lang'],
                     'mainEntity': [{'@type': 'Question', 'name': q,
                                     'acceptedAnswer': {'@type': 'Answer', 'text': t}} for q, t in P['faq']]})
        items = '\n'.join(f'    <details><summary>{e(q)}</summary><p>{e(t)}</p></details>' for q, t in P['faq'])
        faq_html = f'''
  <section class="faq">
    <h2>{e(L["h_faq"])}</h2>
{items}
  </section>
'''
    others = [Q for Q in templates_for(L) if Q['id'] != P['id']]
    related = ''
    if others:
        links = '\n'.join(
            f'    <li><a href="/fixbill/{Q["path"]}"'
            f'{"" if Q["html_lang"] == P["html_lang"] else " lang=" + chr(34) + Q["html_lang"] + chr(34)}>'
            f'{e(Q["card"])}</a></li>' for Q in others)
        related = f'''
  <nav class="related" aria-label="{e(L["h_related"])}">
    <h2>{e(L["h_related"])}</h2>
    <ul>
{links}
    </ul>
  </nav>
'''
    out = head(lang=P['html_lang'], title=P['title'], desc=P['desc'], url=url, og_title=P['h1'], og_desc=P['desc'],
               og_locale=L['og_locale'], alternates=[], extra_ld=ld(data), scripts=['/fixbill/gen.js'])
    out += f'''
<body class="tpl">
{SPRITE}
<div class="page">
  <header class="top">
    {brand(L, "/fixbill/" + L["path"])}
    <span class="top-apps"><a class="top-app d" href="#app">Fixbill App</a><a class="top-app i" href="{AS}">App Store</a><a class="top-app a" href="{e(gp_link(camp + '-top'))}">Google Play</a></span>
  </header>
<main>
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/fixbill/{L["path"]}">{e(P["crumb"])}</a> &rsaquo; <span>{e(P["card"])}</span></nav>
  <section class="intro">
    <h1>{e(P["h1"])}</h1>
    <p class="lede">{e(P["lede"])}</p>
    <a class="jump" href="#gen">{e(P["jump"])}</a>
  </section>

{gen_html(P)}

  <article class="prose">
{P["body"].strip()}
    <p class="fine">{e(P["fine"])}</p>
  </article>
{faq_html}
  <section class="app-box" id="app">
    <div>
      <h2>{e(a["h2"])}</h2>
      <p>{e(a["p"])}</p>
      <ul>
{bullets}
      </ul>
      {badges(L, camp)}
      <p class="note">{e(a["note"])}</p>
    </div>
    <img class="appicon" src="/fixbill/icon-512.png" alt="" width="96" height="96">
  </section>
{related}</main>
{footer(L)}
</div>
</body>
</html>
'''
    return out


# ---------------------------------------------------------------- sitemap

def update_sitemap(today):
    p = os.path.join(ROOT, 'sitemap.xml')
    xml = open(p, encoding='utf-8').read()
    pat = re.compile(r'[ \t]*<url>\s*<loc>https://deriverge\.com/fixbill/[^<]*</loc>.*?</url>\n?', re.S)
    first = pat.search(xml)
    if not first:
        raise SystemExit('sitemap.xml has no /fixbill/ entry to replace')
    pos = first.start()
    xml = pat.sub('', xml)
    blocks = []
    alt = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{M["hreflang"]}" href="{url_of(M)}"/>' for M in LANGS)
    alt += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    for L in LANGS:
        blocks.append(f'  <url>\n    <loc>{url_of(L)}</loc>\n    <lastmod>{today}</lastmod>\n'
                      f'    <priority>{"0.8" if L["code"] == "en" else "0.7"}</priority>{alt}\n  </url>\n')
    for P in PAGES:
        blocks.append(f'  <url><loc>{BASE}{P["path"]}</loc><lastmod>{today}</lastmod><priority>0.7</priority></url>\n')
    for name, prio in (('support', '0.5'), ('privacy', '0.3'), ('terms', '0.3')):
        blocks.append(f'  <url><loc>{BASE}{name}.html</loc><lastmod>{LEGAL_DATE}</lastmod>'
                      f'<priority>{prio}</priority></url>\n')
    xml = xml[:pos] + ''.join(blocks) + xml[pos:]
    open(p, 'w', encoding='utf-8').write(xml)


def write(rel, text):
    if '\u2014' in text or '\u2013' in text:
        raise SystemExit(f'long dash in {rel}')
    path = os.path.join(FIX, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', os.path.relpath(path, ROOT))


def get_page():
    """/fixbill/get/: the QR code target. Phones go straight to their store, anything else gets both buttons."""
    L = BY_CODE['en']
    gp = gp_link('get', 'qr')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Get Fixbill</title>
<meta name="description" content="Download Fixbill for iPhone or Android.">
<meta name="robots" content="noindex, follow">
<meta name="apple-itunes-app" content="app-id=6819481858">
<link rel="icon" type="image/png" sizes="192x192" href="/fixbill/icon-192.png">
<link rel="stylesheet" href="/fixbill/fixbill.css?v={ASSET_V}">
<script>(function(u){{if(/android/i.test(u))location.replace("{gp}");else if(/iphone|ipad|ipod/i.test(u)||(/macintosh/i.test(u)&&navigator.maxTouchPoints>1))location.replace("{AS}")}})(navigator.userAgent)</script>
</head>
<body>
<div class="page">
  <header class="top">
    {brand(L, "/fixbill/")}
  </header>
<main>
  <section class="intro">
    <h1>Get Fixbill</h1>
    <p class="lede">Pick your store.</p>
    {badges(L, 'get', qr=False).replace('utm_medium%3Dlanding', 'utm_medium%3Dqr')}
    <p class="note">{e(L["note"])}</p>
  </section>
</main>
  <footer>
    <p><a href="/fixbill/">Fixbill</a> &middot; <a href="/fixbill/support.html">Support</a> &middot; <a href="/">deriverge s.r.o.</a> &middot; <a href="mailto:{MAIL}">{MAIL}</a></p>
  </footer>
</div>
</body>
</html>
'''


def main():
    seen = {}
    for L in LANGS:
        seen[L['title']] = L['code']
    for P in PAGES:
        if P['title'] in seen or P['desc'] in seen:
            raise SystemExit(f'duplicate title or description: {P["id"]}')
        seen[P['title']] = seen[P['desc']] = P['id']
    write('get/index.html', get_page())
    for L in LANGS:
        write(L['path'] + 'index.html', lang_page(L))
    for P in PAGES:
        write(P['path'] + 'index.html', intent_page(P))
    update_sitemap(dt.date.today().isoformat())
    print('sitemap.xml updated')


if __name__ == '__main__':
    main()
