#!/usr/bin/env python3
"""Builds the multilingual homepage of deriverge.com from _home/template.html and _home/i18n/<lang>.json.

  python3 _home/build.py            -> /index.html (English, x-default) and /<lang>/index.html for every translation

Live numbers (job index, public Apify actors and their groups) are read at build time from the public Apify API and
refreshed in the browser by /js/site.js. The folder starts with an underscore, so GitHub Pages does not publish it.
"""
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = 'https://deriverge.com'

# code, hreflang, og:locale, text direction, thousands separator for the static fallback numbers
LANGS = [
    ('en', 'en', 'en_US', 'ltr', ','), ('de', 'de', 'de_DE', 'ltr', '.'), ('fr', 'fr', 'fr_FR', 'ltr', ' '),
    ('es', 'es', 'es_ES', 'ltr', '.'), ('pt', 'pt', 'pt_BR', 'ltr', '.'), ('it', 'it', 'it_IT', 'ltr', '.'),
    ('nl', 'nl', 'nl_NL', 'ltr', '.'), ('pl', 'pl', 'pl_PL', 'ltr', ' '), ('cs', 'cs', 'cs_CZ', 'ltr', ' '),
    ('sk', 'sk', 'sk_SK', 'ltr', ' '), ('sv', 'sv', 'sv_SE', 'ltr', ' '), ('da', 'da', 'da_DK', 'ltr', '.'),
    ('nb', 'nb', 'nb_NO', 'ltr', ' '), ('fi', 'fi', 'fi_FI', 'ltr', ' '), ('tr', 'tr', 'tr_TR', 'ltr', '.'),
    ('id', 'id', 'id_ID', 'ltr', '.'), ('ja', 'ja', 'ja_JP', 'ltr', ','), ('ko', 'ko', 'ko_KR', 'ltr', ','),
    ('zh', 'zh-Hans', 'zh_CN', 'ltr', ','), ('ar', 'ar', 'ar_AR', 'rtl', ','), ('hi', 'hi', 'hi_IN', 'ltr', ','),
]

GROUPS = [  # order on the page, rule matched against the actor title
    ('jobs', r'job|career|iimjobs|unstop|internship|internshala|hiring|\bats\b|workday|greenhouse|lever|ashby|xing|seek'),
    ('sport', r'nhl|mlb|nba|nfl|ufc|tennis|f1|formula|golf|espn|sport|odds|kalshi|polymarket|soccer|football'),
    ('web', r'dns|whois|domain|url|link|sitemap|tech stack|http|pdf|article|rss|shopify|woocommerce|dedup|merge|phone|fuel'),
    ('companies', r'compan|register|registr|cnpj|vat|business|enrichment|tender|procurement'),
    ('content', r'news|substack|podcast|hacker news|trends|autocomplete|trending|github|craigslist|ads transparency'),
    ('events', r'event|meetup|luma|dice|resident advisor|eventbrite|festival|concert'),
    ('apps', r'app store|google play|steam|review'),
]


def get(url):
    for i in range(8):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.load(r)
        except Exception:  # noqa: BLE001 (the sandbox proxy sometimes cuts long responses)
            time.sleep(3)
    raise SystemExit(f'not readable: {url}')


def live_data():
    meta = get('https://api.apify.com/v2/key-value-stores/jletghbJMlxiI0vnm/records/meta.json')
    items = []
    for off in range(0, 400, 40):
        page = get(f'https://api.apify.com/v2/store?username=deriverge&limit=40&offset={off}')['data']['items']
        items += page
        if len(page) < 40:
            break
    groups = {k: [] for k, _ in GROUPS}
    order = sorted(items, key=lambda a: -((a.get('stats') or {}).get('totalUsers') or 0))
    for a in order:
        t = a['title'].lower()
        for k, rx in GROUPS:
            if re.search(rx, t):
                groups[k].append(a['title'])
                break
    return {'jobs': meta['jobs'], 'companies': meta['companies'], 'built': meta['generatedAt'], 'actors': len(items),
            'groups': groups}


def fmt(n, sep):
    return f'{n:,}'.replace(',', sep)


def page(lang, data, tr, en, langs_present):
    code, hreflang, og_locale, direction, sep = lang
    t = lambda k: html.escape(tr.get(k) or en[k], quote=True)  # noqa: E731
    path = '/' if code == 'en' else f'/{code}/'
    canonical = SITE + path
    alts = [l for l in LANGS if l[0] in langs_present]
    hreflang_links = '\n'.join(f'<link rel="alternate" hreflang="{l[1]}" href="{SITE}{"/" if l[0] == "en" else "/" + l[0] + "/"}">' for l in alts)
    hreflang_links += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    og_alt = '\n'.join(f'<meta property="og:locale:alternate" content="{l[2]}">' for l in alts if l[0] != code)
    menu = ''
    for l in alts:
        href = '/' if l[0] == 'en' else '/' + l[0] + '/'
        name = json.load(open(os.path.join(HERE, 'i18n', l[0] + '.json'), encoding='utf-8'))['_name']
        cur = ' aria-current="page"' if l[0] == code else ''
        menu += f'<li><a href="{href}" hreflang="{l[1]}" lang="{l[1]}" data-lang="{l[0]}"{cur}>{html.escape(name)}</a></li>'
    groups = ''.join(
        f'<li><b class="mono">{len(v)}</b><span>{t("data.g_" + k)}</span><small>{html.escape(", ".join(v[:4]))}</small></li>'
        for k, v in data['groups'].items() if v)
    built = dt.datetime.fromisoformat(data['built'].replace('Z', '+00:00'))
    services = [tr.get(k) or en[k] for k in ('services.mobile_title', 'services.web_title', 'services.data_title')]
    ld = [
        {'@context': 'https://schema.org', '@type': 'Organization', '@id': SITE + '/#org', 'name': 'deriverge s.r.o.',
         'alternateName': 'deriverge', 'url': SITE + '/', 'logo': SITE + '/android-chrome-512x512.png',
         'email': 'info@deriverge.com', 'vatID': 'CZ19456361', 'taxID': '19456361',
         'foundingDate': '2023-06-20', 'description': tr.get('meta.description') or en['meta.description'],
         'address': {'@type': 'PostalAddress', 'addressCountry': 'CZ'},
         'areaServed': 'Worldwide', 'knowsLanguage': ['en', 'cs'],
         'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s}} for s in services],
         'sameAs': ['https://apify.com/deriverge', 'https://www.postarna.cz/']},
        {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': 'deriverge',
         'inLanguage': hreflang, 'publisher': {'@id': SITE + '/#org'}},
        {'@context': 'https://schema.org', '@type': 'ItemList', 'name': tr.get('products.title') or en['products.title'], 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'item': {'@type': 'WebApplication', 'name': 'Poštárna', 'url': 'https://www.postarna.cz/',
             'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Web', 'publisher': {'@id': SITE + '/#org'}}},
            {'@type': 'ListItem', 'position': 2, 'item': {'@type': 'MobileApplication', 'name': 'Tapkasa', 'url': SITE + '/tapkasa/pokladna.html',
             'applicationCategory': 'BusinessApplication', 'operatingSystem': 'iOS, Android', 'installUrl': 'https://apps.apple.com/app/id6807075649',
             'publisher': {'@id': SITE + '/#org'}}},
            {'@type': 'ListItem', 'position': 3, 'item': {'@type': 'MobileApplication', 'name': 'SealSlim', 'url': SITE + '/sealslim/',
             'applicationCategory': 'UtilitiesApplication', 'operatingSystem': 'iOS, Android', 'installUrl': 'https://apps.apple.com/app/id6818619229',
             'publisher': {'@id': SITE + '/#org'}}},
            {'@type': 'ListItem', 'position': 4, 'item': {'@type': 'Dataset', 'name': tr.get('data.feed_title') or en['data.feed_title'],
             'url': SITE + '/tools/job-data-feed/', 'description': tr.get('data.feed_text') or en['data.feed_text'], 'creator': {'@id': SITE + '/#org'}}},
        ]},
    ]
    values = {
        'lang': hreflang, 'dir': direction, 'canonical': canonical, 'hreflang': hreflang_links, 'og_locale': og_locale,
        'og_alternates': og_alt, 'ld': json.dumps(ld, ensure_ascii=False).replace('</', '<\\/'), 'is_root': '1' if code == 'en' else '0',
        'lang_codes': ','.join(l[0] for l in alts), 'home': path, 'lang_label': code.upper(), 'langmenu': menu, 'groups': groups,
        'built_iso': data['built'], 'built_text': built.strftime('%Y-%m-%d %H:%M UTC'),
        'extra_fonts': ('<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">\n' if code == 'ar' else ''),
    }
    out = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    out = out.replace('{{postarna_preview}}', open(os.path.join(HERE, 'postarna-preview.html'), encoding='utf-8').read())
    out = out.replace('{{postarna_logo}}', open(os.path.join(HERE, 'postarna-logo.svg'), encoding='utf-8').read().replace('aria-label="Poštárna"', 'aria-hidden="true"'))
    out = re.sub(r'\{\{t:([a-z_.0-9]+)\}\}', lambda m: t(m.group(1)), out)
    out = re.sub(r'\{\{num:([a-z]+)\}\}', lambda m: fmt(data[m.group(1)], sep), out)
    out = re.sub(r'\{\{([a-z_]+)\}\}', lambda m: values[m.group(1)], out)
    for ch in ('—', '–'):
        if ch in out:
            i = out.index(ch)
            raise SystemExit(f'long dash in {code}: ...{out[max(0, i - 50):i + 20]}...')
    left = re.findall(r'\{\{[^}]+\}\}', out)
    if left:
        raise SystemExit(f'unfilled placeholders in {code}: {left[:5]}')
    target = os.path.join(ROOT, 'index.html') if code == 'en' else os.path.join(ROOT, code, 'index.html')
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(out)
    return path


def update_sitemap(paths_present, today):
    """Replaces the homepage entries of /sitemap.xml with one entry per language, each listing all alternates."""
    p = os.path.join(ROOT, 'sitemap.xml')
    xml = open(p, encoding='utf-8').read()
    if 'xmlns:xhtml' not in xml:
        xml = xml.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    xml = re.sub(r'\n[ \t]*<url><loc>https://deriverge\.com/</loc>[^\n]*</url>', '', xml)
    xml = re.sub(r'\n  <url>\n    <loc>https://deriverge\.com/(?:[a-z]{2}/)?</loc>.*?\n  </url>', '', xml, flags=re.S)
    alts = [l for l in LANGS if l[0] in paths_present]
    links = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l[1]}" href="{SITE}{"/" if l[0] == "en" else "/" + l[0] + "/"}"/>' for l in alts)
    links += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
    blocks = ''.join(f'\n  <url>\n    <loc>{SITE}{"/" if l[0] == "en" else "/" + l[0] + "/"}</loc>\n    <lastmod>{today}</lastmod>'
                     f'\n    <priority>{"1.0" if l[0] == "en" else "0.9"}</priority>{links}\n  </url>' for l in alts)
    xml = xml.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">' + blocks, 1)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(xml)


def main():
    en = json.load(open(os.path.join(HERE, 'i18n', 'en.json'), encoding='utf-8'))
    present = [l[0] for l in LANGS if os.path.exists(os.path.join(HERE, 'i18n', l[0] + '.json'))]
    data = live_data()
    print(f"index {data['jobs']:,} jobs, {data['companies']:,} companies; {data['actors']} public actors")
    for lang in LANGS:
        if lang[0] not in present:
            continue
        tr = json.load(open(os.path.join(HERE, 'i18n', lang[0] + '.json'), encoding='utf-8'))
        missing = [k for k in en if k not in tr]
        if missing and '--allow-missing' not in sys.argv:
            raise SystemExit(f'{lang[0]}: missing keys {missing[:5]}')
        if missing:
            print(f'  {lang[0]}: {len(missing)} keys fall back to English (test build only)')
        print(' ', page(lang, data, tr, en, present))
    update_sitemap(present, dt.date.today().isoformat())


if __name__ == '__main__':
    main()
