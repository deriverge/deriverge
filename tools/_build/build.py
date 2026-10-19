#!/usr/bin/env python3
"""Builds the /tools/ section of deriverge.com: tool pages, ATS data pages and their JSON files.

Steps (the folder _build is not published, GitHub Pages' Jekyll skips folders that start with _):

  1. Download the public job index records into a work folder:
       for k in meta.json companies.json.gz index.jsonl.gz; do
         curl -s -o "$W/$k" "https://api.apify.com/v2/key-value-stores/jletghbJMlxiI0vnm/records/$k"; done
  2. node tools/_build/ats-aggregate.mjs "$W"          -> $W/ats-agg.json
  3. python3 tools/_build/build.py "$W/ats-agg.json"   -> tools/**/index.html, tools/data/ats/*.json

Actor prices and visibility are read live from https://api.apify.com/v2/acts/deriverge~<slug> (public actors only).
Actors that are not public yet use PRICE_FALLBACK below and are still linked from the tool pages; the ATS pages link
only to public actors, so re-running the build after a publication adds the new links.
"""
import datetime as dt
import html
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
SITE = 'https://deriverge.com'
APIFY_USER = 'deriverge'
UTM = [('utm_source', 'deriverge.com'), ('utm_medium', 'tool')]
# The Apify affiliate parameter lives in tools/config.js (one place for the browser and this build).
_cfg = open(os.path.join(TOOLS, 'config.js'), encoding='utf-8').read()
AFFILIATE = re.search(r"AFFILIATE_PARAM:\s*'([^']*)'", _cfg).group(1).lstrip('?&')
REL = 'noopener sponsored' if AFFILIATE else 'noopener'
OG_IMAGE = 'https://raw.githubusercontent.com/deriverge/deriverge/main/pictures/deriverge_logo-long.jpg'
LIBPHONE = ('https://cdn.jsdelivr.net/npm/libphonenumber-js@1.13.14/bundle/libphonenumber-max.js',
            'sha384-TL6PuziRMu9wcvBemTwYbdAy214PjKbUVuk16nYuoNHRBVrFQfPJP4H+qMUqRvyl')

# Free plan price per event (USD) for actors the public API does not show yet. From the datova_slevarna pricing
# scripts (reprice-2.py, create-utility-actors.py, create-wayback.py) on 11 October 2026.
PRICE_FALLBACK = {
    'dns-records-lookup': 0.0008,
    'domain-availability-checker': 0.0005,
    'phone-number-validator': 0.00055,
    'wayback-machine-scraper': 0.0004,
}

esc = html.escape


# ── Apify ──────────────────────────────────────────────────────────────────────────────────────────────────────────
_actor_cache = {}


def actor(slug):
    """{'public': bool, 'price': USD per event on the Free plan or None, 'title': str|None}."""
    if slug in _actor_cache:
        return _actor_cache[slug]
    info = {'public': False, 'price': None, 'title': None}
    d = None
    for attempt in range(8):
        if attempt:
            time.sleep(1.5 * attempt)
        try:
            with urllib.request.urlopen(f'https://api.apify.com/v2/acts/{APIFY_USER}~{slug}', timeout=60) as r:
                d = json.load(r)['data']
            break
        except urllib.error.HTTPError as ex:
            print(f'  {slug}: not readable from the public API ({ex})', file=sys.stderr)
            break
        except Exception as ex:  # connection reset, timeout: the API sometimes drops a request
            print(f'  {slug}: attempt {attempt + 1} failed ({ex!r})', file=sys.stderr)
    else:
        raise SystemExit(f'The Apify API did not answer for {slug}; run the build again.')
    try:
        if d is None:
            raise KeyError('no data')
        info['public'] = bool(d.get('isPublic'))
        info['title'] = d.get('title')
        pis = d.get('pricingInfos') or []
        last = pis[-1] if pis else {}
        events = ((last.get('pricingPerEvent') or {}).get('actorChargeEvents') or {})
        prim = [e for e in events.values() if e.get('isPrimaryEvent')] or [e for k, e in events.items() if 'start' not in k]
        if prim:
            e = prim[0]
            tier = (e.get('eventTieredPricingUsd') or {}).get('FREE') or {}
            info['price'] = tier.get('tieredEventPriceUsd', e.get('eventPriceUsd'))
    except (KeyError, ValueError, TypeError):
        pass
    if info['price'] is None:
        info['price'] = PRICE_FALLBACK.get(slug)
    _actor_cache[slug] = info
    print(f'  actor {slug}: public={info["public"]} price={info["price"]}', file=sys.stderr)
    return info


def per1000(slug):
    p = actor(slug)['price']
    return f'${p * 1000:,.2f}' if p is not None else None


def actor_href(slug, campaign):
    q = UTM + [('utm_campaign', campaign)]
    return (f'https://apify.com/{APIFY_USER}' + (f'/{slug}' if slug else '') + '?' + urllib.parse.urlencode(q)
            + (f'&{AFFILIATE}' if AFFILIATE else ''))


def actor_link(slug, campaign, text, cls='btn'):
    return (f'<a class="{cls}" data-actor="{esc(slug)}" data-campaign="{esc(campaign)}" href="{esc(actor_href(slug, campaign))}" '
            f'target="_blank" rel="{REL}">{text}</a>')


# ── page chrome ────────────────────────────────────────────────────────────────────────────────────────────────────
def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def faq_block(items):
    out = ['<div class="faq">']
    for q, a in items:
        out.append(f'<details><summary>{esc(q)}</summary><div class="a">{a}</div></details>')
    out.append('</div>')
    return '\n'.join(out)


def faq_ld(items):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in items]}


def crumbs_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + p} for i, (n, p) in enumerate(trail)]}


def webapp_ld(name, path, desc, category='DeveloperApplication'):
    return {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': name, 'url': SITE + path,
            'description': desc, 'applicationCategory': category, 'operatingSystem': 'Any (runs in a web browser)',
            'browserRequirements': 'Requires JavaScript', 'isAccessibleForFree': True,
            'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
            'publisher': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': SITE + '/'}}


DISCLOSURE = (' Links to Apify carry our affiliate code: if you become a paying Apify customer, Apify pays us a commission'
              ' at no extra cost to you.') if AFFILIATE else ''

FOOTER = '''<div class="foot-brand"><a class="brand" href="/"><span class="br">&lt;/</span>deriverge<span class="br">&gt;</span></a></div>
<div class="foot-text">  <p>Free tools by <a href="/">deriverge s.r.o.</a>, a software studio in the Czech Republic. Our data actors are in <a data-actor="" data-campaign="{campaign}" href="{store}" target="_blank" rel="{rel}">Apify Store</a>.{disclosure}</p>
  <p>Questions or a company listed by mistake: <a href="mailto:info@deriverge.com">info@deriverge.com</a>. The tools are provided as is, without warranty.</p>
</div>'''


def kick(k):
    """Section labels are written like code comments ('// data'); the page shows them without the slashes."""
    return re.sub(r'^//\s*', '', k)


def layout(*, path, title, desc, tab, kicker, h1, lede, body, ld, campaign, scripts=(), trail=None, head_extra=''):
    url = SITE + path
    trail = trail or [('deriverge', '/'), ('Tools', '/tools/')] + ([(h1, path)] if path != '/tools/' else [])
    lds = list(ld) + [crumbs_ld(trail)]
    ld_html = '\n'.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=1)}\n</script>' for x in lds)
    crumbs = '<a href="/tools/">tools</a>'
    if len(trail) > 3:
        crumbs += f'<span class="sep">/</span><a href="{trail[2][1]}">{esc(trail[2][0].lower())}</a>'
    cur = (lambda p: ' aria-current="page"' if path == p else '')
    script_tags = '\n'.join(scripts)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..700&family=Geist:wght@300..700&family=Geist+Mono:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<link rel="stylesheet" href="/tools/tools.css">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="deriverge">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
{head_extra}{ld_html}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head site-head--page">
  <div class="wrap">
    <a class="brand" href="/" aria-label="deriverge home"><span class="br">&lt;/</span>deriverge<span class="br">&gt;</span></a>
    <div class="crumb">{crumbs}</div>
    <nav class="nav" aria-label="Main"><a class="nav-link" href="/tools/"{cur('/tools/')}>Tools</a><a class="nav-link" href="/tools/job-data-feed/"{cur('/tools/job-data-feed/')}>Job data feed</a><a class="nav-link" href="/#contact">Contact</a></nav>
  </div>
</header>
<main id="main" class="page">
  <div class="wrap">
    <header class="hero hero--tool">
      <p class="cmt">{esc(kick(kicker))}</p>
      <h1 class="h1-tool">{esc(h1)}</h1>
      <p class="lede">{lede}</p>
    </header>
{body}
  </div>
</main>
<footer class="site-foot site-foot--tools">
  <div class="wrap">
{FOOTER.format(campaign=esc(campaign), store=esc(actor_href('', campaign)), rel=REL, disclosure=DISCLOSURE)}
  </div>
</footer>
<script src="/tools/config.js"></script>
<script src="/tools/common.js"></script>
{script_tags}
</body>
</html>
'''
    for ch in ('—', '–'):
        if ch in doc:
            i = doc.index(ch)
            raise SystemExit(f'Long dash in {path}: ...{doc[max(0, i - 60):i + 20]}...')
    out = os.path.join(TOOLS, path.strip('/').removeprefix('tools').strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)
    PAGES.append((path, title))
    return out


PAGES = []


def section(kicker, title, inner, cls='block', hid=None):
    hid = hid or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return f'''    <section class="{cls}" aria-labelledby="h-{hid}">
      <p class="cmt">{esc(kick(kicker))}</p>
      <h2 id="h-{hid}" class="h2">{esc(title)}</h2>
{inner}
    </section>'''


def cta(*, campaign, slug, name, points, unit, also=(), kicker='// run it at scale', lead=None):
    price = per1000(slug)
    pts = ''.join(f'<li>{p}</li>' for p in points)
    price_html = f'<p class="price">From <b>{price}</b> per 1,000 {esc(unit)}, pay only for results. Apify\'s free plan includes $5 of monthly credit.</p>' if price else ''
    also_html = ''
    if also:
        bits = []
        for s, label, u in also:
            p = per1000(s)
            bits.append(f'{actor_link(s, campaign, esc(label), cls="")}' + (f' (from {p} per 1,000 {esc(u)})' if p else ''))
        also_html = '<p class="more">Also: ' + ' · '.join(bits) + '</p>'
    lead = lead or f'The same job runs as <strong>{esc(name)}</strong> in Apify Store when one browser tab is not enough.'
    return f'''    <aside class="block cta" aria-label="{esc(name)} on Apify">
      <p class="cmt">{esc(kick(kicker))}</p>
      <h2>{esc(name)} on Apify</h2>
      <p>{lead}</p>
      <ul>{pts}</ul>
      {price_html}
      <div class="cta-row">{actor_link(slug, campaign, 'Open ' + esc(name) + ' on Apify &rarr;')}</div>
      {also_html}
    </aside>'''


TOOL_LINKS = [
    ('/tools/bulk-dns-lookup/', 'Bulk DNS lookup', 'A, MX, TXT, NS, CAA for 20 domains'),
    ('/tools/rdap-whois-lookup/', 'RDAP WHOIS lookup', 'registrar, expiry, nameservers'),
    ('/tools/domain-availability-checker/', 'Domain availability checker', '20 names across TLDs'),
    ('/tools/wayback-machine-snapshots/', 'Wayback Machine snapshot finder', 'first, latest and closest capture'),
    ('/tools/phone-number-validator/', 'Phone number validator', '50 numbers, E.164 and type'),
    ('/tools/companies-using-ats/', 'Which ATS do companies use?', '14 systems compared'),
]


def more_tools(current):
    items = ''.join(f'<li><a href="{p}">{esc(n)}</a><span>{esc(d)}</span></li>' for p, n, d in TOOL_LINKS if p != current)
    return section('// more free tools', 'More free tools', f'      <ul class="linklist">{items}</ul>', hid='more-tools')


def btn_csv(id_):
    return f'<button type="button" class="btn btn--ghost" id="{id_}" hidden>Download CSV</button>'


# ── tool pages ─────────────────────────────────────────────────────────────────────────────────────────────────────
def page_dns():
    path, camp = '/tools/bulk-dns-lookup/', 'bulk-dns-lookup'
    title = 'Bulk DNS Lookup: A, MX, TXT, NS and CAA for 20 Domains'
    desc = ('Free bulk DNS lookup: A, AAAA, MX, TXT, NS, CNAME, CAA, SOA and DMARC records for up to 20 domains at once, '
            'in your browser over DNS over HTTPS.')
    types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'CAA', 'SOA']
    checks = ''.join(f'<label class="check"><input type="checkbox" name="type" value="{t}" checked> {t}</label>' for t in types)
    checks += '<label class="check"><input type="checkbox" name="type" value="DMARC" checked> DMARC</label>'
    tool = f'''    <section class="block block--tight" aria-label="DNS lookup tool">
      <form class="panel" id="dns-form" novalidate>
        <div class="field">
          <label class="label" for="dns-domains"><span class="key">domains</span>: one per line, up to 20 (URLs and e-mail addresses work too)</label>
          <textarea id="dns-domains" name="domains" spellcheck="false" autocapitalize="off" placeholder="example.com&#10;github.com&#10;https://www.wikipedia.org/wiki/DNS"></textarea>
        </div>
        <div class="field"><span class="label"><span class="key">records</span></span><div class="checks">{checks}</div></div>
        <div class="field" style="max-width:320px">
          <label class="label" for="dns-resolver"><span class="key">resolver</span></label>
          <select id="dns-resolver" name="resolver"><option value="cloudflare">Cloudflare (1.1.1.1)</option><option value="google">Google Public DNS (8.8.8.8)</option></select>
        </div>
        <div class="actions"><button type="submit" class="btn">Look up records</button>{btn_csv('dns-csv')}<span class="hint">Your list goes straight from this page to the resolver. We do not see it.</span></div>
        <p class="status" id="dns-status" role="status" aria-live="polite"></p>
      </form>
      <div class="results" id="dns-results"></div>
    </section>'''
    explain = section('// what the records mean', 'What each record type tells you', '''      <div class="tbl-wrap"><table class="tbl tbl--fit"><thead><tr><th>Record</th><th>What it holds</th></tr></thead><tbody>
        <tr><td class="k">A, AAAA</td><td>The IPv4 and IPv6 addresses the name points to, so a browser knows which server to contact.</td></tr>
        <tr><td class="k">CNAME</td><td>An alias: the name is another name in disguise, for example <code>www</code> pointing to a CDN host. A CNAME cannot sit on the bare domain, so <code>example.com</code> usually has none.</td></tr>
        <tr><td class="k">MX</td><td>The mail servers for the domain, lowest priority number first. No MX usually means the domain does not receive e-mail.</td></tr>
        <tr><td class="k">NS</td><td>The nameservers that hold the domain's records. They show which DNS provider the domain uses.</td></tr>
        <tr><td class="k">TXT</td><td>Free text: the SPF record (<code>v=spf1</code>) listing who may send mail for the domain, and verification codes for Google, Microsoft, Atlassian and others.</td></tr>
        <tr><td class="k">CAA</td><td>Which certificate authorities may issue TLS certificates for the domain. No CAA record means any authority may.</td></tr>
        <tr><td class="k">SOA</td><td>The zone's primary nameserver, the administrator mailbox, the serial number and the refresh timers.</td></tr>
        <tr><td class="k">DMARC</td><td>A TXT record at <code>_dmarc.example.com</code> that tells receivers what to do with mail failing SPF and DKIM: <code>p=none</code>, <code>quarantine</code> or <code>reject</code>.</td></tr>
      </tbody></table></div>
      <div class="prose" style="margin-top:22px">
        <p>The lookup asks a public resolver over <strong>DNS over HTTPS</strong>, the same answers <code>dig</code> or <code>nslookup</code> would give from that resolver. Answers are cached for the TTL shown, in seconds, so a record you changed a minute ago may still show its old value until the TTL runs out.</p>
        <p><code>www.example.com</code> and <code>example.com</code> are separate names with separate records. Enter both if you need both.</p>
      </div>''', hid='records')
    faq = [
        ('How do I check the DNS records of many domains at once?',
         '<p>Paste up to 20 domains above, one per line, choose the record types and press <strong>Look up records</strong>. Every domain gets its own table and <strong>Download CSV</strong> saves all of them in one file. For hundreds or thousands of domains, use DNS Records Lookup on Apify, which returns one row per hostname.</p>'),
        ('What does NXDOMAIN mean?',
         '<p>The resolver says the name does not exist in DNS. Either the domain is not registered, its registration has lapsed, or the subdomain was never created.</p>'),
        ('Why do I still see an old record after changing it?',
         '<p>Resolvers keep each answer for its TTL. Until that time runs out they may return the old value. Try the other resolver: Cloudflare and Google cache independently, so one of them may already have the new record.</p>'),
        ('Is the list of domains sent to deriverge?',
         '<p>No. This page has no server behind it. Your browser sends each question directly to Cloudflare (<code>cloudflare-dns.com</code>) or Google (<code>dns.google</code>) over HTTPS.</p>'),
        ('How do I find the mail provider of a domain?',
         '<p>Look at the MX records: <code>aspmx.l.google.com</code> means Google Workspace, <code>*.mail.protection.outlook.com</code> means Microsoft 365. DNS Records Lookup on Apify names the provider for you in a <code>mailProvider</code> field, next to the SPF record and the DMARC policy.</p>'),
        ('Can I check DNS records on a schedule?',
         '<p>Yes, with the Apify actor. Run it daily or hourly on the same list and keep only the domains whose records changed, then send them to a spreadsheet, a webhook or Slack.</p>'),
    ]
    body = '\n'.join([
        tool,
        cta(campaign=camp, slug='dns-records-lookup', name='DNS Records Lookup', unit='hostnames', points=[
            'Thousands of hostnames per run, one clean row each: A, AAAA, CNAME, MX, NS, TXT, SOA and CAA',
            'SPF record, DMARC policy and the mail provider read from MX (Google Workspace, Microsoft 365, Zoho and others)',
            'Scheduled runs that return only the domains whose records changed',
            'API, webhooks and integrations; export to CSV, Excel or JSON',
        ], also=[('domain-whois-dns-lookup', 'Domain WHOIS and DNS Lookup', 'domains')]),
        explain,
        section('// questions', 'Frequently asked questions', faq_block(faq), hid='faq'),
        more_tools(path),
    ])
    layout(path=path, title=title, desc=desc, tab='bulk-dns-lookup.js', kicker='// free tool · runs in your browser',
           h1='Bulk DNS lookup', campaign=camp,
           lede='Check the DNS records of up to 20 domains at once: A, AAAA, MX, TXT, NS, CNAME, CAA and SOA, plus the DMARC policy. Queries go from your browser straight to Cloudflare or Google over DNS over HTTPS.',
           body=body, ld=[webapp_ld('Bulk DNS lookup', path, desc), faq_ld(faq)],
           scripts=['<script src="/tools/js/dns.js" defer></script>'])


def page_whois():
    path, camp = '/tools/rdap-whois-lookup/', 'rdap-whois-lookup'
    title = 'RDAP WHOIS Lookup: Registrar, Expiry Date and Nameservers'
    desc = ('Free RDAP WHOIS lookup for up to 20 domains: registrar, creation and expiry dates, status codes, nameservers '
            'and DNSSEC, live from the registry.')
    tool = f'''    <section class="block block--tight" aria-label="RDAP WHOIS lookup tool">
      <form class="panel" id="whois-form" novalidate>
        <div class="field">
          <label class="label" for="whois-domains"><span class="key">domains</span>: one per line, up to 20</label>
          <textarea id="whois-domains" name="domains" spellcheck="false" autocapitalize="off" placeholder="example.com&#10;wikipedia.org&#10;bbc.co.uk"></textarea>
        </div>
        <div class="actions"><button type="submit" class="btn">Look up</button>{btn_csv('whois-csv')}<span class="hint">Subdomains are checked as their registered domain: www.shop.example.co.uk becomes example.co.uk.</span></div>
        <p class="status" id="whois-status" role="status" aria-live="polite"></p>
      </form>
      <div class="results" id="whois-results"></div>
    </section>'''
    statuses = [
        ('clientTransferProhibited', 'The registrar locked transfers to another registrar. Normal for most domains; it protects against hijacking.'),
        ('serverTransferProhibited', 'The registry locked transfers, often for high-value domains or during a dispute.'),
        ('clientDeleteProhibited, clientUpdateProhibited', 'The registrar blocked deletion or changes. Also a normal protection.'),
        ('clientHold, serverHold', 'The domain is not published in DNS, so websites and e-mail on it stop working. Often unpaid renewal or a legal issue.'),
        ('autoRenewPeriod', 'The registry renewed the domain automatically and the registrar can still cancel the renewal.'),
        ('redemptionPeriod', 'The domain expired and was deleted by the registrar. The holder can still restore it, usually for a fee.'),
        ('pendingDelete', 'The domain will be released within days. After that, anyone can register it.'),
    ]
    rows = ''.join(f'<tr><td class="k">{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in statuses)
    explain = section('// how it works', 'RDAP, the successor of WHOIS', f'''      <div class="prose">
        <p><strong>RDAP</strong> (Registration Data Access Protocol) is the structured, JSON based replacement for the old text WHOIS service. ICANN requires it from every generic top-level domain, and many country registries offer it too. This page loads the official IANA list of RDAP servers, then your browser asks the registry of each domain directly.</p>
        <p>It works for <code>.com</code>, <code>.net</code>, <code>.org</code>, <code>.io</code>, <code>.ai</code>, <code>.app</code>, <code>.dev</code>, <code>.xyz</code>, <code>.uk</code>, <code>.fr</code>, <code>.nl</code>, <code>.cz</code>, <code>.ch</code>, <code>.us</code>, <code>.ca</code>, <code>.au</code>, <code>.br</code> and more than a thousand other extensions. Registries without public RDAP, such as <code>.eu</code>, <code>.it</code>, <code>.es</code>, <code>.se</code>, <code>.at</code>, <code>.jp</code>, <code>.co</code> and <code>.me</code>, and <code>.de</code>, whose RDAP server refuses requests from web pages, need the classic WHOIS service, which the Apify actor uses.</p>
        <p><strong>No personal data.</strong> The page reads only the registrar, dates, status codes, nameservers and DNSSEC. Registrant, administrative and technical contacts are never read or displayed, even where a registry publishes them.</p>
      </div>
      <h3 class="h3">Domain status codes explained</h3>
      <div class="tbl-wrap"><table class="tbl tbl--fit"><thead><tr><th>Status</th><th>Meaning</th></tr></thead><tbody>{rows}</tbody></table></div>''', hid='rdap')
    faq = [
        ('What is the difference between RDAP and WHOIS?',
         '<p>Both return the registration record of a domain. WHOIS is plain text in a different layout for every registry, over its own network port. RDAP uses HTTPS and JSON with fixed field names, so dates, status codes and nameservers mean the same thing everywhere.</p>'),
        ('How do I find when a domain expires?',
         '<p>Enter it above and read <strong>Expires</strong>. The date comes from the registry, so it reflects the last renewal the registrar reported. A domain past its date can still be in the auto-renew grace period.</p>'),
        ('Why is the owner of the domain not shown?',
         '<p>Since GDPR most registries hide the registrant, and this page never shows contact data even where it is published. To reach an owner, use the registrar\'s contact form or the abuse address of the registrar.</p>'),
        ('Why does my .de, .eu or .co domain not work here?',
         '<p>These registries either have no public RDAP server or block requests made from web pages. The WHOIS Domain Lookup actor on Apify falls back to WHOIS for them.</p>'),
        ('How old is a domain?',
         '<p>The <strong>Created</strong> line shows the registration date and the age. If a domain was deleted and registered again, the date is the new registration, not the first one ever.</p>'),
        ('Can I monitor expiry dates of many domains?',
         '<p>Yes, with the Apify actor: schedule it on your list and keep only the domains whose registrar, status, nameservers or expiry changed, or filter domains expiring within a number of days.</p>'),
    ]
    body = '\n'.join([
        tool,
        cta(campaign=camp, slug='whois-domain-lookup', name='WHOIS Domain Lookup', unit='domains', points=[
            'Thousands of domains, URLs or e-mail addresses per run, one row each',
            'RDAP with a WHOIS fallback for .de, .eu, .it, .jp and other registries without RDAP',
            'Registrar, creation and expiry dates, domain age, status codes, nameservers and DNSSEC',
            'Scheduled runs that return only changed domains; API and CSV, Excel or JSON export',
        ], also=[('domain-whois-dns-lookup', 'Domain WHOIS and DNS Lookup', 'domains')]),
        explain,
        section('// questions', 'Frequently asked questions', faq_block(faq), hid='faq'),
        more_tools(path),
    ])
    layout(path=path, title=title, desc=desc, tab='rdap-whois-lookup.js', kicker='// free tool · runs in your browser',
           h1='RDAP WHOIS lookup', campaign=camp,
           lede='Find the registrar of a domain, when it was registered and when it expires, its status codes and nameservers. Your browser asks the registry\'s own RDAP server, the modern replacement for WHOIS, for up to 20 domains at once.',
           body=body, ld=[webapp_ld('RDAP WHOIS lookup', path, desc), faq_ld(faq)],
           scripts=['<script src="/tools/js/rdap-core.js" defer></script>', '<script src="/tools/js/whois.js" defer></script>'])


AVAIL_TLDS = [('com', True), ('net', True), ('org', True), ('io', True), ('ai', True), ('app', True), ('dev', True),
              ('xyz', False), ('tech', False), ('online', False), ('store', False), ('site', False), ('info', False),
              ('biz', False), ('cloud', False), ('us', False), ('ca', False), ('uk', False), ('co.uk', False),
              ('com.au', False), ('fr', False), ('nl', False), ('ch', False), ('cz', False), ('de', False)]


def page_availability():
    path, camp = '/tools/domain-availability-checker/', 'domain-availability-checker'
    title = 'Bulk Domain Availability Checker: 20 Names Across TLDs'
    desc = ('Check up to 20 domain names across .com, .io, .ai, .dev and 20 more extensions at once, straight from the '
            'registries over RDAP. Free, no signup.')
    tl = ''.join(f'<label class="check"><input type="checkbox" name="tld" value="{t}"{" checked" if on else ""}> .{t}</label>' for t, on in AVAIL_TLDS)
    tool = f'''    <section class="block block--tight" aria-label="Domain availability checker">
      <form class="panel" id="avail-form" novalidate>
        <div class="field">
          <label class="label" for="avail-names"><span class="key">names</span>: up to 20, one per line. A bare name is paired with every extension below; a full domain is checked as it is.</label>
          <textarea id="avail-names" name="names" spellcheck="false" autocapitalize="off" placeholder="brightpath&#10;northwind labs&#10;mybrand.io"></textarea>
        </div>
        <div class="field"><span class="label"><span class="key">extensions</span></span><div class="checks">{tl}</div></div>
        <div class="actions"><button type="submit" class="btn">Check availability</button>{btn_csv('avail-csv')}<label class="check"><input type="checkbox" id="avail-only-free"> show only available</label></div>
        <p class="status" id="avail-status" role="status" aria-live="polite"></p>
      </form>
      <div class="results" id="avail-results"></div>
    </section>'''
    explain = section('// read this before you buy', 'What "likely available" means', '''      <div class="prose">
        <p>Each check asks the registry of the extension over <strong>RDAP</strong>. When the registry answers <strong>404 Not Found</strong>, it has no registration record for the name, which almost always means you can register it. It is still not a guarantee:</p>
        <ul>
          <li>Registries reserve or block some names (brands, geographic names, short or offensive words). They may answer 404 and still refuse the registration.</li>
          <li>Premium names are unregistered but sold at a higher price. RDAP does not show prices.</li>
          <li>A name can be registered by someone else seconds after the check.</li>
        </ul>
        <p>A name shown as <strong>registered</strong> has a record at the registry; the table adds the expiry date and registrar where the registry shares them. For <code>.de</code> and other registries that do not answer web pages, the page falls back to DNS: <strong>no DNS, unconfirmed</strong> means the name has no nameservers, which is a good sign but not proof. Always confirm at a registrar before you rely on a name.</p>
        <p>Your searches go from your browser to the registries and Cloudflare DNS. We do not see or store them.</p>
      </div>''', hid='caveat')
    faq = [
        ('How does the checker know if a domain is available?',
         '<p>It asks the registry that runs the extension, for example Verisign for <code>.com</code>, over RDAP. A 404 answer means there is no registration record for the name.</p>'),
        ('Can I check one name across many extensions?',
         '<p>Yes. Type the bare name, such as <code>brightpath</code>, and tick the extensions you want. Each name is paired with every ticked extension, up to 200 checks in one go.</p>'),
        ('Is it safe to search for my idea here?',
         '<p>The page has no server of its own. Each question goes from your browser directly to the registry, so no reseller sees your list. We cannot see it either.</p>'),
        ('Does it show prices or premium domains?',
         '<p>No. Registries do not publish prices over RDAP, and premium names look like any other unregistered name. Check the price at a registrar.</p>'),
        ('Why are .co, .me and .eu missing?',
         '<p>Their registries have no public RDAP server, so a web page cannot ask them. Enter a full domain such as <code>name.eu</code> to get a DNS based hint, or use the Apify actor, which asks WHOIS servers too.</p>'),
        ('How can I check thousands of names?',
         '<p>Use Domain Availability Checker on Apify: a list of names times a list of extensions, one row per combination, with the method that decided each answer.</p>'),
    ]
    body = '\n'.join([
        tool,
        cta(campaign=camp, slug='domain-availability-checker', name='Domain Availability Checker', unit='name checks', points=[
            'Thousands of name and extension combinations per run, one row each',
            'RDAP plus WHOIS for registries without RDAP, such as .de, .eu and .it, with DNS as the last resort',
            'Registrar, registration and expiry dates for names that are taken',
            'Schedules to watch names you want, API and CSV, Excel or JSON export',
        ], also=[('whois-domain-lookup', 'WHOIS Domain Lookup', 'domains')]),
        explain,
        section('// questions', 'Frequently asked questions', faq_block(faq), hid='faq'),
        more_tools(path),
    ])
    layout(path=path, title=title, desc=desc, tab='domain-availability-checker.js', kicker='// free tool · runs in your browser',
           h1='Bulk domain availability checker', campaign=camp,
           lede='Type up to 20 names, pick the extensions and see which domains are still unregistered. Every answer comes straight from the registry over RDAP, and your searches never pass through a reseller.',
           body=body, ld=[webapp_ld('Bulk domain availability checker', path, desc), faq_ld(faq)],
           scripts=['<script src="/tools/js/rdap-core.js" defer></script>', '<script src="/tools/js/availability.js" defer></script>'])


def page_wayback():
    path, camp = '/tools/wayback-machine-snapshots/', 'wayback-machine-snapshots'
    title = 'Wayback Machine Snapshot Finder: First and Latest Capture'
    desc = ('Find the first, latest and closest-to-date Wayback Machine snapshots of up to 20 URLs, with direct links '
            'to every archived copy. Free, in your browser.')
    tool = f'''    <section class="block block--tight" aria-label="Wayback Machine snapshot finder">
      <form class="panel" id="wb-form" novalidate>
        <div class="field">
          <label class="label" for="wb-urls"><span class="key">urls</span>: pages or domains, one per line, up to 20</label>
          <textarea id="wb-urls" name="urls" spellcheck="false" autocapitalize="off" placeholder="example.com&#10;nytimes.com&#10;https://www.apple.com/iphone/"></textarea>
        </div>
        <div class="field" style="max-width:260px">
          <label class="label" for="wb-date"><span class="key">closest to date</span> (optional)</label>
          <input type="date" id="wb-date" name="date" min="1996-01-01">
        </div>
        <div class="actions"><button type="submit" class="btn">Find snapshots</button>{btn_csv('wb-csv')}</div>
        <p class="status" id="wb-status" role="status" aria-live="polite"></p>
      </form>
      <div class="results" id="wb-results"></div>
    </section>'''
    explain = section('// how it works', 'How the snapshot finder works', '''      <div class="prose">
        <p>The Internet Archive's <strong>Wayback Machine</strong> has saved copies of web pages since 1996. For every URL this page asks the archive's <strong>Availability API</strong> three questions: the capture closest to 1 January 1996 (the first one), the capture closest to today (the latest one) and, if you pick a date, the capture closest to that date.</p>
        <p>The Availability API returns one capture per question and only captures that loaded successfully, and it often reports nothing even for well archived pages. When it does, the cell links straight to the Wayback Machine, which jumps to the first, latest or closest capture itself. <strong>calendar</strong> shows all captures by day and <strong>all URLs</strong> lists every archived address under the domain.</p>
        <p><strong>Why no count of captures per year here?</strong> Counts and full lists come from the archive's CDX API, which does not accept requests from other websites' pages, so a browser tool cannot read it. The calendar view in the Wayback Machine shows the same information visually.</p>
      </div>''', hid='how')
    faq = [
        ('How do I find when a website was first archived?',
         '<p>Enter the domain above. <strong>First capture</strong> shows the date of the oldest snapshot when the Availability API reports it; otherwise <strong>open first capture</strong> takes you to the oldest capture in the Wayback Machine, where the date is in the address and the toolbar.</p>'),
        ('How do I see a website as it looked on a specific date?',
         '<p>Pick the date in <strong>closest to date</strong>. The table links the snapshot nearest to that day; the Wayback Machine may pick a capture a few days or months away when nothing was saved on that day.</p>'),
        ('Why is there no date for a page that is archived?',
         '<p>The Availability API answers from a separate index, skips captures that were redirects or errors and is sometimes slow to answer at all. The links in the table still open the right capture, and the <strong>calendar</strong> shows every capture the Wayback Machine has.</p>'),
        ('How do I list every archived page of a domain?',
         '<p>The <strong>all URLs</strong> link opens that list in the Wayback Machine. The Wayback Machine shows the first and last capture of each URL in that list.</p>'),
        ('How many snapshots does a site have per year?',
         '<p>The calendar view in the Wayback Machine shows it visually. The Internet Archive also documents its CDX API for researchers who need the counts as data.</p>'),
        ('Is this tool free?',
         '<p>Yes. It runs in your browser against the Internet Archive\'s public API. Consider supporting the Internet Archive, which keeps the Wayback Machine running.</p>'),
    ]
    body = '\n'.join([
        tool,
        # Bez odkazu na placený actor: podmínky archive.org dovolují přístup jen zdarma a pro vědu a výzkum (11. 10. 2026).
        explain,
        section('// questions', 'Frequently asked questions', faq_block(faq), hid='faq'),
        more_tools(path),
    ])
    layout(path=path, title=title, desc=desc, tab='wayback-machine-snapshots.js', kicker='// free tool · runs in your browser',
           h1='Wayback Machine snapshot finder', campaign=camp,
           lede='See when a page or domain was first saved by the Internet Archive, its most recent capture and the capture closest to a date you choose, for up to 20 URLs at once, with direct links to every archived copy.',
           body=body, ld=[webapp_ld('Wayback Machine snapshot finder', path, desc, 'UtilitiesApplication'), faq_ld(faq)],
           scripts=['<script src="/tools/js/wayback.js" defer></script>'])


def page_phone():
    path, camp = '/tools/phone-number-validator/', 'phone-number-validator'
    title = 'Bulk Phone Number Validator: E.164 Format, Type and Country'
    desc = ('Validate up to 50 phone numbers at once: valid or not, E.164 and national format, country and line type '
            '(mobile, landline, toll free). Offline and free.')
    tool = f'''    <section class="block block--tight" aria-label="Phone number validator">
      <form class="panel" id="phone-form" novalidate>
        <div class="field">
          <label class="label" for="phone-numbers"><span class="key">numbers</span>: one per line, up to 50, any format</label>
          <textarea id="phone-numbers" name="numbers" spellcheck="false" placeholder="+44 20 7946 0958&#10;(201) 555-0123&#10;0049 1512 3456789&#10;+420 601 123 456"></textarea>
        </div>
        <div class="field" style="max-width:420px">
          <label class="label" for="phone-country"><span class="key">default country</span>: for numbers written without + or 00</label>
          <select id="phone-country" name="country"><option value="US">United States (+1)</option></select>
        </div>
        <div class="actions"><button type="submit" class="btn">Validate numbers</button>{btn_csv('phone-csv')}<span class="hint">Checked in your browser with Google's libphonenumber rules. Nothing is uploaded.</span></div>
        <p class="status" id="phone-status" role="status" aria-live="polite"></p>
      </form>
      <div class="results" id="phone-results"></div>
    </section>'''
    types = [('Mobile', 'A mobile range, such as UK 07 or German 015x.'),
             ('Fixed line', 'A geographic landline range.'),
             ('Fixed line or mobile', 'The United States, Canada and a few other countries share ranges, so the type cannot be told from the number.'),
             ('Toll free', 'Free to call, such as 800 in the US or 0800 in the UK.'),
             ('Premium rate, shared cost', 'Numbers that cost the caller more, or split the cost with the receiver.'),
             ('VoIP, personal number, UAN', 'Internet telephony ranges, follow-me numbers and company-wide access numbers.')]
    rows = ''.join(f'<tr><td class="k">{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in types)
    explain = section('// what the result means', 'Valid, E.164 and line types', f'''      <div class="prose">
        <p><strong>Valid</strong> means the number has the right length and falls into a range the country's regulator has assigned, according to Google's <strong>libphonenumber</strong> data. It does not mean the line is switched on or that someone answers: no offline check can know that.</p>
        <p><strong>E.164</strong> is the international format used by databases, CRMs and SMS gateways: a plus sign, the country code and the number without spaces or a leading zero, for example <code>+442079460958</code>. Store numbers this way and they compare and deduplicate cleanly.</p>
        <p>A number that starts with <code>+</code> or <code>00</code> carries its own country. Numbers without it are read as numbers of the <strong>default country</strong>.</p>
      </div>
      <h3 class="h3">Line types</h3>
      <div class="tbl-wrap"><table class="tbl tbl--fit"><thead><tr><th>Type</th><th>Meaning</th></tr></thead><tbody>{rows}</tbody></table></div>''', hid='meaning')
    faq = [
        ('How do I validate a list of phone numbers?',
         '<p>Paste up to 50 numbers above, one per line, set the default country for numbers without a + code and press <strong>Validate numbers</strong>. <strong>Download CSV</strong> saves the results.</p>'),
        ('What is E.164 format?',
         '<p>The international standard for writing phone numbers: <code>+</code>, country code, then the national number without the leading zero, up to 15 digits in total. <code>020 7946 0958</code> in the UK becomes <code>+442079460958</code>.</p>'),
        ('Does valid mean the number is in use?',
         '<p>No. It means the number could exist: right length, assigned range. Checking whether a line is active needs a live network lookup (HLR), which no offline validator does.</p>'),
        ('Why is a US number shown as "fixed line or mobile"?',
         '<p>In the North American Numbering Plan mobile and landline numbers share the same area codes, so the type cannot be read from the number itself.</p>'),
        ('Are my numbers uploaded anywhere?',
         '<p>No. The validation library is loaded into the page and every check happens on your device. You can disconnect from the internet after the page has loaded and it still works.</p>'),
        ('How can I validate thousands of numbers?',
         '<p>Use Phone Number Validator on Apify. It takes lists or another run\'s dataset, adds the original carrier and time zones, and gives a reason for every invalid number.</p>'),
    ]
    body = '\n'.join([
        tool,
        cta(campaign=camp, slug='phone-number-validator', name='Phone Number Validator', unit='phone numbers', points=[
            'Thousands of numbers per run, from a list or straight from another run\'s dataset',
            'E.164, international and national format, country, line type and a reason for every invalid number',
            'The carrier the range was assigned to and the number\'s time zones',
            'Skip duplicates, API and CSV, Excel or JSON export',
        ]),
        explain,
        section('// questions', 'Frequently asked questions', faq_block(faq), hid='faq'),
        more_tools(path),
    ])
    layout(path=path, title=title, desc=desc, tab='phone-number-validator.js', kicker='// free tool · runs offline in your browser',
           h1='Bulk phone number validator', campaign=camp,
           lede='Paste up to 50 phone numbers in any format. Each is checked against Google\'s libphonenumber rules and returned in E.164, international and national format, with its line type and country. Nothing leaves your browser.',
           body=body, ld=[webapp_ld('Bulk phone number validator', path, desc, 'BusinessApplication'), faq_ld(faq)],
           scripts=[f'<script src="{LIBPHONE[0]}" integrity="{LIBPHONE[1]}" crossorigin="anonymous" defer></script>',
                    '<script src="/tools/js/phone.js" defer></script>'])


# ── ATS data ───────────────────────────────────────────────────────────────────────────────────────────────────────
ATS = {
    'greenhouse': dict(name='Greenhouse',
        about='Greenhouse is a recruiting platform from New York, common among venture-backed technology companies and scale-ups. Its job boards live at job-boards.greenhouse.io and publish a public JSON API, which is how every company on this list is read.',
        signs=['Apply links go to <code>boards.greenhouse.io/&lt;token&gt;</code> or <code>job-boards.greenhouse.io/&lt;token&gt;</code>.',
               'Job links on the company\'s own site end with <code>?gh_jid=&lt;number&gt;</code>.',
               'The page source loads <code>boards.greenhouse.io/embed/job_board/js?for=&lt;token&gt;</code>.'],
        api='https://boards-api.greenhouse.io/v1/boards/&lt;token&gt;/jobs'),
    'lever': dict(name='Lever',
        about='Lever is a recruiting platform from San Francisco that combines an applicant tracking system with a candidate CRM. Boards live at jobs.lever.co, or at jobs.eu.lever.co for accounts hosted in the European Union.',
        signs=['Apply links go to <code>jobs.lever.co/&lt;company&gt;</code> or <code>jobs.eu.lever.co/&lt;company&gt;</code>.',
               'Job links end with a long identifier, such as <code>/&lt;company&gt;/0b1c2d3e-...</code>.'],
        api='https://api.lever.co/v0/postings/&lt;company&gt;?mode=json'),
    'workday': dict(name='Workday',
        about='Workday Recruiting is part of Workday\'s HR suite for large employers. Each employer has its own tenant at &lt;tenant&gt;.wd&lt;N&gt;.myworkdayjobs.com, often with several career sites per tenant, one per brand, region or audience. Workday names the legal entity of each job, so a group can appear under one of its subsidiaries. Where that entity does not match the career site, the brand from the site address comes first, as in Medtronic (CVS Covidien Sales LLC); the careers address always identifies the employer.',
        signs=['Apply links go to <code>&lt;tenant&gt;.wd1.myworkdayjobs.com/&lt;site&gt;</code> (wd1, wd3, wd5, wd103 and others).',
               'Job links contain <code>/job/&lt;location&gt;/&lt;title&gt;_&lt;requisition ID&gt;</code>.'],
        api='https://&lt;tenant&gt;.wd5.myworkdayjobs.com/wday/cxs/&lt;tenant&gt;/&lt;site&gt;/jobs (POST)'),
    'ashby': dict(name='Ashby',
        about='Ashby is an all-in-one recruiting platform popular with fast-growing startups. Job boards live at jobs.ashbyhq.com and most of them link to the company website, which is where the website column comes from.',
        signs=['Apply links go to <code>jobs.ashbyhq.com/&lt;company&gt;</code>.',
               'Job links on the company\'s own site carry <code>?ashby_jid=&lt;id&gt;</code>.'],
        api='https://api.ashbyhq.com/posting-api/job-board/&lt;company&gt;'),
    'bamboohr': dict(name='BambooHR',
        about='BambooHR is HR software for small and medium-sized businesses with a built-in applicant tracking module. Each customer\'s career page lives at &lt;company&gt;.bamboohr.com/careers.',
        signs=['The career page is <code>&lt;company&gt;.bamboohr.com/careers</code>.',
               'Embedded job lists load <code>&lt;company&gt;.bamboohr.com/js/embed.js</code>.'],
        api='https://&lt;company&gt;.bamboohr.com/careers/list'),
    'workable': dict(name='Workable',
        about='Workable is recruiting software for small and mid-sized employers. Each account has a career page at apply.workable.com/&lt;account&gt;.',
        signs=['The career page is <code>apply.workable.com/&lt;account&gt;/</code>.',
               'Job links look like <code>apply.workable.com/&lt;account&gt;/j/&lt;shortcode&gt;/</code>.'],
        api='https://apply.workable.com/api/v1/widget/accounts/&lt;account&gt;'),
    'smartrecruiters': dict(name='SmartRecruiters',
        about='SmartRecruiters is a talent acquisition platform used by large and mid-sized employers. Company career pages live at careers.smartrecruiters.com/&lt;Company&gt; and individual jobs at jobs.smartrecruiters.com.',
        signs=['The career page is <code>careers.smartrecruiters.com/&lt;Company&gt;</code>.',
               'Job links look like <code>jobs.smartrecruiters.com/&lt;Company&gt;/&lt;id&gt;</code>.'],
        api='https://api.smartrecruiters.com/v1/companies/&lt;Company&gt;/postings'),
    'recruitee': dict(name='Recruitee',
        about='Recruitee is collaborative hiring software from the Netherlands, used mostly by European small and mid-sized companies. Career sites live at &lt;company&gt;.recruitee.com, often behind the employer\'s own domain.',
        signs=['The career site is <code>&lt;company&gt;.recruitee.com</code>.',
               'Job links look like <code>&lt;company&gt;.recruitee.com/o/&lt;job-slug&gt;</code>.'],
        api='https://&lt;company&gt;.recruitee.com/api/offers/'),
    'teamtailor': dict(name='Teamtailor',
        about='Teamtailor is an employer branding and recruiting platform from Sweden, strongest in the Nordics. Career sites live at &lt;company&gt;.teamtailor.com or on the employer\'s own domain.',
        signs=['The career site is <code>&lt;company&gt;.teamtailor.com/jobs</code>, or a custom domain with jobs under <code>/jobs/&lt;id&gt;-&lt;title&gt;</code>.',
               'The page source loads assets from <code>teamtailor-cdn.com</code>.'],
        api='https://&lt;company&gt;.teamtailor.com/jobs.rss'),
    'personio': dict(name='Personio',
        about='Personio is HR software from Munich for small and mid-sized companies in Europe, with recruiting built in. Job pages live at &lt;company&gt;.jobs.personio.de or .com.',
        signs=['Job pages are at <code>&lt;company&gt;.jobs.personio.de</code> or <code>&lt;company&gt;.jobs.personio.com</code>.',
               'Job links look like <code>/job/&lt;number&gt;</code>.'],
        api='https://&lt;company&gt;.jobs.personio.de/xml'),
    'breezy': dict(name='Breezy HR',
        about='Breezy HR is recruiting software for small businesses. Each company\'s career site lives at &lt;company&gt;.breezy.hr.',
        signs=['The career site is <code>&lt;company&gt;.breezy.hr</code>.',
               'Job links look like <code>&lt;company&gt;.breezy.hr/p/&lt;id&gt;-&lt;title&gt;</code>.'],
        api='https://&lt;company&gt;.breezy.hr/json'),
    'rippling': dict(name='Rippling',
        about='Rippling\'s recruiting module is part of its HR, IT and payroll platform. Job boards live at ats.rippling.com/&lt;company&gt;/jobs.',
        signs=['The job board is <code>ats.rippling.com/&lt;company&gt;/jobs</code>.',
               'Job links look like <code>ats.rippling.com/&lt;company&gt;/jobs/&lt;uuid&gt;</code>.'],
        api='https://ats.rippling.com/api/v2/board/&lt;company&gt;/jobs'),
    'icims': dict(name='iCIMS',
        about='iCIMS is an enterprise talent acquisition platform used by large US employers, hospitals and universities. Employers run one or more portals at &lt;portal&gt;.icims.com. iCIMS lists rarely include locations, so the main country is often unknown.',
        signs=['The portal is <code>&lt;portal&gt;.icims.com</code>, often <code>careers-&lt;company&gt;.icims.com</code>.',
               'Job links look like <code>/jobs/&lt;id&gt;/&lt;title&gt;/job</code>.'],
        api=None),
    'oracle': dict(name='Oracle Recruiting Cloud',
        about='Oracle Recruiting Cloud is part of Oracle Fusion Cloud HCM, used by large enterprises, banks and public institutions. Career sites live on Oracle Cloud hosts such as &lt;pod&gt;.fa.&lt;region&gt;.oraclecloud.com.',
        signs=['The career site is <code>&lt;pod&gt;.fa.&lt;region&gt;.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1</code>.',
               'Job links contain <code>/job/&lt;number&gt;</code>.'],
        api='https://&lt;pod&gt;.fa.&lt;region&gt;.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions'),
}
# Per-site limits of the job index: a board at the limit has at least that many jobs.
CAPS = {'workday': 1000, 'oracle': 1600, 'smartrecruiters': 4000, 'icims': 1500, 'greenhouse': 5000}
MULTI_SITE = ('workday', 'oracle', 'icims')
JUNK_NAME = re.compile(r'^(test\w*|demo|sandbox|example)$', re.I)


def careers_url(a, k):
    q = urllib.parse.quote
    return {
        'greenhouse': lambda: f'https://job-boards.greenhouse.io/{q(k)}',
        'lever': lambda: f'https://jobs.eu.lever.co/{q(k[3:])}' if k.startswith('eu:') else f'https://jobs.lever.co/{q(k)}',
        'workday': lambda: f'https://{k}',
        'ashby': lambda: f'https://jobs.ashbyhq.com/{q(k)}',
        'bamboohr': lambda: f'https://{k}.bamboohr.com/careers',
        'workable': lambda: f'https://apply.workable.com/{q(k)}/',
        'smartrecruiters': lambda: f'https://careers.smartrecruiters.com/{q(k)}',
        'recruitee': lambda: f'https://{k}.recruitee.com/',
        'teamtailor': lambda: f'https://{k}.teamtailor.com/jobs',
        'personio': lambda: f'https://{k}.jobs.personio.de/',
        'breezy': lambda: f'https://{k}.breezy.hr/',
        'rippling': lambda: f'https://ats.rippling.com/{q(k)}/jobs',
        'icims': lambda: f'https://{k}/jobs',
        'oracle': lambda: (f'https://{k.split("/sites/")[0]}/hcmUI/CandidateExperience/en/sites/{k.split("/sites/")[1]}' if '/sites/' in k else f'https://{k}'),
    }[a]()


def short_url(u):
    return re.sub(r'/$', '', re.sub(r'^https?://', '', u)).replace('/hcmUI/CandidateExperience/en/sites/', '/.../')


def strip_code(n):
    """Workday and Oracle names often start with an internal entity code: 'JP05 Nihon Pall Ltd.', '13-5674085 Merrill
    Lynch', 'FR_3317 EES', '27210002985V Thermo Fisher'. Drop it when the rest is still a real name ('3M Company' stays)."""
    m = re.match(r'^\(?([A-Z0-9_-]+)\)?\s+(.+)$', n)
    if not m:
        return n
    code, rest = m.group(1), m.group(2)
    digits = sum(ch.isdigit() for ch in code)
    coded = (digits >= 2 and any(ch.isalpha() for ch in code)) or re.fullmatch(r'\d{2,}-\d{3,}', code)
    if coded and (len(rest) >= 6 or ' ' in rest):
        return rest
    return n


def employer_key(a, r):
    """One employer can run several career sites: Workday tenants, Oracle hosts, iCIMS portals with one name."""
    if a == 'workday':
        return r['k'].split('.')[0]
    if a == 'oracle':
        return r['k'].split('/')[0]
    if a == 'icims':
        return r['name'].lower()
    return r['k']


def top_unique(a, rows, n=15):
    seen, out = set(), []
    for r in rows:
        k = employer_key(a, r)
        if r['jobs'] and k not in seen:
            seen.add(k)
            out.append(r)
            if len(out) == n:
                break
    return out


def _norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def workday_brand(key):
    """Brand of a Workday tenant from its address: danaher.wd1.../DanaherJobs -> 'Danaher', cvshealth/CVS_Health_Careers ->
    'CVS Health'. Falls back to the capitalised tenant when it is long enough to be a name, else None."""
    host, _, site = key.partition('/')
    tenant = host.split('.')[0].lower()
    out, j = [], 0
    for ch in site:
        if j >= len(tenant):
            break
        if ch in '_-':
            out.append(' ')
        elif ch.lower() == tenant[j]:
            out.append(ch)
            j += 1
        else:
            break
    brand = re.sub(r'\s+', ' ', ''.join(out)).strip()
    if j >= 3:
        return brand.capitalize() if brand.islower() else brand
    return tenant.capitalize() if len(tenant) >= 5 else None


def workday_label(name, key):
    """Workday names are the legal entity of a sample job ('Signify Health LLC' on the CVS Health site). When the name
    does not mention the tenant, lead with the brand: 'CVS Health (Signify Health LLC)'."""
    tenant = key.split('.')[0].lower()
    brand = workday_brand(key)
    n = _norm(name)
    if not brand or (len(tenant) >= 3 and tenant in n) or _norm(brand) in n:
        return name
    first = _norm(name.split()[0]) if name.split() else ''
    if len(first) >= 4 and first in _norm(brand):
        return name
    return f'{brand} ({name})'


def clean_name(a, name, key):
    n = (name or '').strip()
    # The site uses no long dashes, company names included: 'Emma \u2013 The Sleep Company' -> 'Emma - The Sleep Company'.
    n = re.sub(r'\s+[\u2013\u2014]\s+', ' - ', n).replace('\u2014', ' - ').replace('\u2013', '-')
    if a in ('workday', 'oracle'):
        n = re.sub(r'^\([^)]{1,40}\)\s+(?=\S.{5,})', '', n)  # '(USA) Ecolab Production LLC'
        n = strip_code(n)
        n = re.sub(r'\s+(Career Sites?|Careers? Site|Candidate Experience page)$', '', n, flags=re.I)
    if not n:
        n = key.split('/')[0].split('.')[0].removeprefix('eu:')
    if a == 'workday':
        n = workday_label(n, key)
    return n


def load_ats(agg_path):
    agg = json.load(open(agg_path, encoding='utf-8'))
    date = agg['generatedAt'][:10]
    by = {a: [] for a in ATS}
    for c in agg['companies']:
        if c['a'] not in ATS:
            continue
        name = clean_name(c['a'], c['name'], c['k'])
        if JUNK_NAME.match(name):
            continue
        site = c.get('site') or ''
        if site and not re.match(r'^https?://[^\s/]+\.[^\s/]+', site):
            site = ''
        by[c['a']].append({'name': name, 'k': c['k'], 'cc': c['country'], 'jobs': c['jobs'], 'site': site, 'nc': c.get('nCountries') or 0})
    stats = {}
    for a, rows in by.items():
        # Boards at the index limit tie on jobs; the one hiring in more countries is likely the bigger one.
        rows.sort(key=lambda r: (-r['jobs'], -r['nc'], r['name'].lower()))
        # Employers: sites of one employer merged; main country = country of its biggest site.
        emp = {}
        for r in rows:
            e = emp.setdefault(employer_key(a, r), {'jobs': 0, 'cc': None, 'best': -1})
            e['jobs'] += r['jobs']
            if r['jobs'] > e['best'] and r['cc']:
                e['cc'], e['best'] = r['cc'], r['jobs']
        emps = list(emp.values())
        with_jobs = [e for e in emps if e['jobs']]
        known = [e for e in with_jobs if e['cc']]
        cc_companies = {}
        for e in known:
            cc_companies[e['cc']] = cc_companies.get(e['cc'], 0) + 1
        stats[a] = {
            'companies': len(emps), 'sites': len(rows), 'with_jobs': len(with_jobs), 'jobs': sum(r['jobs'] for r in rows),
            'median': statistics.median([e['jobs'] for e in with_jobs]) if with_jobs else 0,
            'known_cc': len(known),
            'top_cc': sorted(cc_companies.items(), key=lambda x: -x[1]),
            'country_jobs': sorted(agg['countryJobs'].get(a, {}).items(), key=lambda x: -x[1]),
            'top': top_unique(a, rows),
            'cap': CAPS.get(a),
            'emp_cc': {k: e['cc'] for k, e in emp.items() if e['jobs'] and e['cc']},
        }
    return by, stats, date, agg['countryNames']


def write_ats_json(by, date):
    out_dir = os.path.join(TOOLS, 'data', 'ats')
    os.makedirs(out_dir, exist_ok=True)
    sizes = {}
    for a, rows in by.items():
        data = {'ats': a, 'name': ATS[a]['name'], 'updated': date, 'cap': CAPS.get(a), 'unit': 'career sites' if a in MULTI_SITE else 'companies',
                'columns': ['company', 'key', 'country', 'openJobs', 'website'],
                'rows': [[r['name'], r['k'], r['cc'] or '', r['jobs']] + ([r['site']] if r['site'] else []) for r in rows]}
        p = os.path.join(out_dir, f'{a}.json')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        sizes[a] = os.path.getsize(p)
    return sizes


def fmt_date(iso):
    d = dt.date.fromisoformat(iso)
    return f'{d.day} {d.strftime("%B %Y")}'


def jobs_txt(n, cap):
    return f'{n:,}+' if cap and n >= cap else f'{n:,}'


def bars(items, total, cn, unit_total=None):
    if not items:
        return '<p class="note">No location data for this system.</p>'
    mx = items[0][1]
    li = ''.join(
        f'<li><span>{esc(cn.get(c, c))}</span><span class="bar"><i style="width:{max(2, round(100 * n / mx))}%"></i></span>'
        f'<span class="n">{n:,}<small>{round(100 * n / total) if total else 0}%</small></span></li>' for c, n in items)
    return f'<ul class="bars">{li}</ul>'


def ats_job_actors(a):
    """Public actors to link from an ATS page: the system's own scraper if public, then the two cross-ATS actors."""
    out = []
    own = f'{a}-jobs-scraper'
    if actor(own)['public']:
        out.append(own)
    for s in ('career-site-jobs-search', 'greenhouse-lever-workday-jobs-scraper'):
        if actor(s)['public']:
            out.append(s)
    return out


def ats_cta(a, camp):
    name = ATS[a]['name']
    acts = ats_job_actors(a)
    if not acts:
        return ''
    main = acts[0]
    title = actor(main)['title'] or main
    if main == f'{a}-jobs-scraper':
        points = [f'Every open job from any {esc(name)} board, read live: title, department, locations, pay range when published, full description',
                  f'Give it board links, tokens or company domains, or leave it empty to search all {esc(name)} jobs in our daily index',
                  'Filters for country, seniority, remote, salary, skills and visa sponsorship; new-only mode for daily runs',
                  'API, webhooks and CSV, Excel or JSON export']
        unit = 'jobs'
        lead = f'Need the jobs behind these companies? <strong>{esc(title)}</strong> reads them straight from {esc(name)}.'
    else:
        points = [f'Search more than a million open jobs from 40,000+ company career sites on 14 systems, {esc(name)} included',
                  'Filter by title, country, seniority, remote, salary, skills and visa sponsorship',
                  'Each match is re-read on its board, with the full description and apply link',
                  'Schedules with new jobs only, API and CSV, Excel or JSON export']
        unit = 'jobs'
        lead = f'Need the jobs behind these companies? <strong>{esc(title)}</strong> searches every {esc(name)} board in this list, and 13 other systems.'
    also = [(s, actor(s)['title'] or s, 'jobs') for s in acts[1:]]
    return cta(campaign=camp, slug=main, name=title, unit=unit, points=points, also=also, kicker='// get the jobs', lead=lead)


def ats_links(current):
    return ''.join(f'<li><a href="/tools/companies-using-{a}/">{esc(ATS[a]["name"])}</a></li>' for a in ORDER if a != current)


ORDER = []


def page_ats(a, rows, st, date, cn):
    name = ATS[a]['name']
    path, camp = f'/tools/companies-using-{a}/', f'companies-using-{a}'
    nice_date = fmt_date(date)
    title = f'Companies Using {name}: List of {st["companies"]:,} Employers'
    if len(title) > 62:
        title = f'Companies Using {name}: {st["companies"]:,} Employers'
    top_names = [r['name'] for r in st['top'][:3]]
    desc = (f'{st["companies"]:,} companies that use {name} for hiring, with careers pages, main country and '
            f'{st["jobs"]:,} open jobs. Search, sort and download the list.')
    known_pct = round(100 * st['known_cc'] / st['with_jobs']) if st['with_jobs'] else 0
    if st['sites'] > st['companies']:
        found = f'We found <strong>{st["companies"]:,}</strong> companies that hire on {esc(name)}, with {st["sites"]:,} public career sites between them. '
    else:
        found = f'We found <strong>{st["companies"]:,}</strong> companies with a public career site on {esc(name)}. '
    lede = (found +
            f'<strong>{st["with_jobs"]:,}</strong> of them list <strong>{st["jobs"]:,}</strong> open jobs in our index of {nice_date}. '
            f'Search the list, sort it and open any company\'s careers page.')
    tc = st['top_cc']
    top_country = f'{cn.get(tc[0][0], tc[0][0])}' if tc else 'unknown'
    top_share = round(100 * tc[0][1] / st['known_cc']) if tc and st['known_cc'] else 0
    stats_html = f'''      <ul class="stats">
        <li class="stat"><b>{st["companies"]:,}</b><span>companies on {esc(name)}</span></li>
        <li class="stat"><b>{st["with_jobs"]:,}</b><span>with open jobs now</span></li>
        <li class="stat"><b>{st["jobs"]:,}</b><span>open jobs in total</span></li>
        <li class="stat"><b>{round(st["median"]):,}</b><span>median open jobs per company</span></li>
        <li class="stat"><b>{top_share}%</b><span>hire mainly in {esc(top_country)}</span></li>
      </ul>'''
    top_rows = ''.join(
        f'<tr><td class="num">{i + 1}</td><td>{esc(r["name"])}</td><td><a href="{esc(careers_url(a, r["k"]))}" target="_blank" rel="nofollow noopener">{esc(short_url(careers_url(a, r["k"])))}</a></td>'
        f'<td>{esc(cn.get(r["cc"], r["cc"] or ""))}</td><td class="num">{jobs_txt(r["jobs"], st["cap"])}</td></tr>' for i, r in enumerate(st['top']))
    cap_note = f'<p class="note">Our index reads up to {st["cap"]:,} jobs per {esc(name)} site, so the largest boards show {st["cap"]:,}+.</p>' if st['cap'] else ''
    top_block = f'''      <div class="tbl-wrap"><table class="tbl"><thead><tr><th class="num">#</th><th>Company</th><th>Careers page</th><th>Main country</th><th class="num">Open jobs</th></tr></thead><tbody>{top_rows}</tbody></table></div>
      {cap_note}'''
    cc_block = (bars(tc[:10], st['known_cc'], cn) +
                f'<p class="note">Share of the {st["known_cc"]:,} companies with open jobs whose main hiring country we could read from job locations ({known_pct}% of them).</p>')
    cj = st['country_jobs'][:10]
    cj_total = sum(n for _, n in st['country_jobs'])
    cj_block = bars(cj, cj_total, cn) + '<p class="note">Open jobs by country of the job location. A job listed in two countries counts in both.</p>'
    table = f'''      <div id="ats-app" class="is-loading" data-ats="{a}" data-src="/tools/data/ats/{a}.json">
        <div class="panel" style="margin-bottom:14px">
          <div class="row">
            <div class="grow"><label class="label" for="ats-q"><span class="key">search</span>: company, careers address or website</label><input type="search" id="ats-q" placeholder="Type a company name" autocomplete="off"></div>
            <div class="grow" style="max-width:300px"><label class="label" for="ats-country"><span class="key">country</span></label><select id="ats-country"><option value="">All countries</option></select></div>
          </div>
          <div class="actions" style="margin-top:14px"><label class="check"><input type="checkbox" id="ats-open"> only companies with open jobs</label><span class="hint" id="ats-count">Loading the list...</span><button type="button" class="btn btn--ghost" id="ats-csv">Download CSV</button></div>
        </div>
        <div class="tbl-wrap"><table class="tbl"><thead id="ats-thead"><tr><th>Company</th><th>Careers page</th><th>Main country</th><th class="num">Open jobs</th></tr></thead><tbody id="ats-tbody"><tr><td colspan="4" class="empty"><span class="spin"></span> Loading {st["sites"]:,} {"career sites" if a in MULTI_SITE else "companies"}...</td></tr></tbody></table></div>
        <div class="actions"><button type="button" class="btn btn--ghost" id="ats-more" hidden>Show more</button></div>
        <noscript><p class="note">The full list needs JavaScript. The raw data is at <a href="/tools/data/ats/{a}.json">/tools/data/ats/{a}.json</a>.</p></noscript>
      </div>'''
    signs = ''.join(f'<li>{s}</li>' for s in ATS[a]['signs'])
    api = ATS[a]['api']
    howto = f'''      <div class="prose">
        <p>Open any job on the company\'s careers page and look where the <strong>Apply</strong> button leads. A company uses {esc(name)} when:</p>
        <ul>{signs}</ul>
        {f'<p>The public job feed of a {esc(name)} board is at <code>{api}</code>. It needs no key and is what our index reads every day.</p>' if api else f'<p>{esc(name)} has no public job feed, so our index reads the job list pages of each portal.</p>'}
        <p>Not sure which system a link belongs to? Paste it into the <a href="/tools/companies-using-ats/#detect">ATS detector</a>, or search the company by name on the <a href="/tools/companies-using-ats/#find">ATS overview</a>.</p>
      </div>'''
    about = f'''      <div class="prose">
        <p>{ATS[a]["about"]}</p>
        <p><strong>How this list is made.</strong> We find {esc(name)} career sites in the public Common Crawl web archive and read each board\'s public job list every day for our job index. A company is listed when its board answered with a company name; companies with a live board but no openings today are included with 0 jobs. The main country is the country with most of the company\'s job locations. This is a sample of employers we could find, not {esc(name)}\'s full customer list. The list holds company names and public career pages only, no personal data. If your company should not be here, write to <a href="mailto:info@deriverge.com">info@deriverge.com</a>.</p>
      </div>'''
    big = ', '.join(esc(n) for n in top_names)
    faq = [
        (f'How many companies use {name}?',
         f'<p>We know of {st["companies"]:,} companies with a public {esc(name)} career site, and {st["with_jobs"]:,} of them had open jobs on {nice_date}. {esc(name)}\'s real customer count is higher: many employers keep their board unlisted or hire without a public board.</p>'),
        (f'Which big companies use {name}?',
         f'<p>By open jobs on {nice_date}, the largest {esc(name)} employers in our data are {big}. The table above ranks the top 15 and the full list sorts by open jobs.</p>'),
        (f'How can I tell if a company uses {name}?',
         '<p>Click <strong>Apply</strong> on one of its jobs and check the address. ' + strip_tags(ATS[a]['signs'][0]) + '</p>'),
        (f'Can I download the list of companies using {name}?',
         '<p>Yes. <strong>Download CSV</strong> above the table saves the rows that match your search and filters: company, careers page, website where known, main country and open jobs.</p>'),
        (f'How do I get all open jobs from {name} companies?',
         f'<p>Run a job scraper on Apify: it reads every job from the boards you choose, or searches all {esc(name)} jobs in our daily index, with titles, locations, descriptions and apply links.</p>'),
        ('How fresh is this data?',
         f'<p>The job index behind this page is rebuilt every day. This page shows the index of {nice_date}.</p>'),
    ]
    body = '\n'.join([
        section('// at a glance', f'{name} in numbers', stats_html, hid='numbers'),
        section('// biggest employers', f'Biggest {name} employers by open jobs', top_block, hid='top'),
        f'''    <section class="block" aria-label="Countries">
      <div class="two">
        <div><p class="cmt">// where they hire</p><h2 class="h2">Top countries by companies</h2>{cc_block}</div>
        <div><p class="cmt">// where the jobs are</p><h2 class="h2">Top countries by open jobs</h2>{cj_block}</div>
      </div>
    </section>''',
        section('// the full list', f'All companies using {name}', table, hid='list'),
        ats_cta(a, camp),
        section('// check it yourself', f'How to tell if a company uses {name}', howto, hid='howto'),
        section('// about the data', f'About {name} and this list', about, hid='about'),
        section('// questions', 'Frequently asked questions', faq_block(faq), hid='faq'),
        section('// other systems', 'Companies using other applicant tracking systems',
                f'      <ul class="linklist">{ats_links(a)}<li><a href="/tools/companies-using-ats/">Compare all 14 systems</a></li></ul>', hid='other'),
    ])
    dataset = {'@context': 'https://schema.org', '@type': 'Dataset', 'name': f'Companies using {name}',
               'description': f'{st["companies"]:,} companies with a public {name} career site, with careers page URL, main hiring country and number of open jobs, built from public career sites by deriverge.',
               'url': SITE + path, 'dateModified': date, 'creator': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': SITE + '/'},
               'isAccessibleForFree': True, 'keywords': [f'companies using {name}', f'{name} customers', 'applicant tracking system', 'ATS'],
               'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'application/json', 'contentUrl': f'{SITE}/tools/data/ats/{a}.json'}]}
    layout(path=path, title=title, desc=desc, tab=f'companies-using-{a}.json', kicker=f'// free data · updated {nice_date}',
           h1=f'Companies using {name}', lede=lede, body=body, campaign=camp,
           ld=[dataset, faq_ld(faq)],
           trail=[('deriverge', '/'), ('Tools', '/tools/'), ('ATS', '/tools/companies-using-ats/'), (f'Companies using {name}', path)],
           scripts=['<script src="/tools/js/ats-common.js" defer></script>', '<script src="/tools/js/ats-table.js" defer></script>'])


EUROPE = {'GB', 'DE', 'FR', 'NL', 'SE', 'ES', 'IT', 'IE', 'BE', 'CH', 'AT', 'DK', 'NO', 'FI', 'PL', 'PT', 'CZ', 'GR', 'RO', 'HU'}


def page_compare(by, stats, date, cn):
    path, camp = '/tools/companies-using-ats/', 'companies-using-ats'
    nice_date = fmt_date(date)
    total_c = sum(s['companies'] for s in stats.values())
    total_j = sum(s['jobs'] for s in stats.values())
    by_comp = sorted(ATS, key=lambda a: -stats[a]['companies'])
    by_jobs = sorted(ATS, key=lambda a: -stats[a]['jobs'])
    title = f'Which Companies Use Which ATS: {total_c:,} Employers, 14 Systems'
    desc = (f'Which ATS do companies use? {total_c:,} employers on Greenhouse, Workday, Lever, Ashby, BambooHR and 9 more '
            f'systems compared, plus a lookup for any company.')
    rows = ''
    for a in by_comp:
        s = stats[a]
        main = cn.get(s['top_cc'][0][0], s['top_cc'][0][0]) if s['top_cc'] else ''
        rows += (f'<tr><td><a href="/tools/companies-using-{a}/">{esc(ATS[a]["name"])}</a></td><td class="num">{s["companies"]:,}</td>'
                 f'<td class="num">{s["with_jobs"]:,}</td><td class="num">{s["jobs"]:,}</td><td class="num">{round(s["median"]):,}</td><td>{esc(main)}</td></tr>')
    table = f'''      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>System</th><th class="num">Companies</th><th class="num">With open jobs</th><th class="num">Open jobs</th><th class="num">Median jobs</th><th>Main country</th></tr></thead><tbody>{rows}</tbody></table></div>
      <p class="note">Median jobs = median open jobs per company with at least one opening. Main country = the country most of the system\'s employers hire in. Data of {nice_date}.</p>'''
    comp_bars = bars([(ATS[a]['name'], stats[a]['companies']) for a in by_comp], total_c, {})
    jobs_bars = bars([(ATS[a]['name'], stats[a]['jobs']) for a in by_jobs], total_j, {})
    # Leading systems per country, by companies whose main hiring country it is.
    per_cc = {}
    for a in ATS:
        for cc in stats[a]['emp_cc'].values():
            per_cc.setdefault(cc, {}).setdefault(a, 0)
            per_cc[cc][a] += 1
    countries = sorted(per_cc, key=lambda c: -sum(per_cc[c].values()))[:14]
    crow = ''
    for c in countries:
        tot = sum(per_cc[c].values())
        top3 = sorted(per_cc[c].items(), key=lambda x: -x[1])[:3]
        cells = ''.join(f'<td>{esc(ATS[a]["name"])} <span class="hint">{round(100 * n / tot)}%</span></td>' for a, n in top3)
        cells += '<td></td>' * (3 - len(top3))
        crow += f'<tr><td>{esc(cn.get(c, c))}</td><td class="num">{tot:,}</td>{cells}</tr>'
    cc_table = f'''      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Country</th><th class="num">Companies</th><th>Most used</th><th>Second</th><th>Third</th></tr></thead><tbody>{crow}</tbody></table></div>
      <p class="note">Companies with open jobs, counted in the country where most of their jobs are. Shares are within each country.</p>'''
    eu = {}
    for c in EUROPE:
        for a, n in per_cc.get(c, {}).items():
            eu[a] = eu.get(a, 0) + n
    eu_top = sorted(eu.items(), key=lambda x: -x[1])[:3]
    us_top = sorted(per_cc.get('US', {}).items(), key=lambda x: -x[1])[:3]
    leaders = []
    for c in ('DE', 'SE', 'NL', 'GB', 'FR'):
        if per_cc.get(c):
            a_top = max(per_cc[c].items(), key=lambda x: x[1])[0]
            leaders.append(f'{esc(ATS[a_top]["name"])} in {esc(cn.get(c, c))}')
    find = f'''      <div id="find" data-ats="{",".join(by_comp)}">
        <form class="panel" id="find-form" novalidate>
          <label class="label" for="find-q"><span class="key">company</span>: name or website, for example Stripe or notion.so</label>
          <input type="search" id="find-q" placeholder="Type a company name" autocomplete="off">
          <p class="status" id="find-status" role="status" aria-live="polite">Searches every company on these pages. The lists load when you start typing.</p>
        </form>
        <div class="results" id="find-results"></div>
      </div>'''
    detect = '''      <form class="panel" id="detect-form" novalidate>
        <label class="label" for="detect-url"><span class="key">link</span>: a job posting, an Apply button target or a careers page</label>
        <div class="row"><div class="grow"><input type="text" id="detect-url" name="url" spellcheck="false" autocapitalize="off" placeholder="https://job-boards.greenhouse.io/acme/jobs/4012345"></div><button type="submit" class="btn">Detect ATS</button></div>
        <p class="status" id="detect-result" role="status" aria-live="polite"></p>
      </form>'''
    sign_rows = ''.join(f'<tr><td><a href="/tools/companies-using-{a}/">{esc(ATS[a]["name"])}</a></td><td>{ATS[a]["signs"][0]}</td></tr>' for a in by_comp)
    guide = f'''      <div class="prose">
        <ol>
          <li>Open the company\'s careers page and click any job.</li>
          <li>Look at the address of the job, or of its <strong>Apply</strong> button. Most systems host the application form on their own domain, even when the job list sits on the company website.</li>
          <li>If the address stays on the company domain, open the page source (Ctrl+U or Cmd+Option+U) and search for the names below. Embedded job boards load a script from their system.</li>
        </ol>
      </div>
      <div class="tbl-wrap"><table class="tbl tbl--fit"><thead><tr><th>System</th><th>Tell-tale sign</th></tr></thead><tbody>{sign_rows}</tbody></table></div>'''
    method = f'''      <div class="prose">
        <p>The companies come from public career sites only. We find job boards of 14 applicant tracking systems in the Common Crawl web archive and read each board\'s public job list every day for a job index of over a million openings. A company is counted when its board answered with a company name. Counts reflect what we could discover, which favours systems with public, crawlable boards: this is <strong>not a market share estimate</strong>, and enterprise systems such as Workday, Oracle and iCIMS are undercounted by companies but strong by jobs.</p>
        <p>No personal data is collected: company names, career page addresses and job counts only.</p>
      </div>'''
    faq = [
        ('What is the most popular applicant tracking system?',
         f'<p>In our data the most common system by number of companies is {esc(ATS[by_comp[0]]["name"])} ({stats[by_comp[0]]["companies"]:,} companies), followed by {esc(ATS[by_comp[1]]["name"])} and {esc(ATS[by_comp[2]]["name"])}. By open jobs, {esc(ATS[by_jobs[0]]["name"])} leads with {stats[by_jobs[0]]["jobs"]:,}, because its customers are large employers. Our counts reflect public, discoverable boards, so treat them as a sample rather than market share.</p>'),
        ('Which ATS do large companies use?',
         f'<p>The systems with the most open jobs per company are {", ".join(esc(ATS[a]["name"]) for a in sorted(ATS, key=lambda a: -stats[a]["median"])[:3])}. Large enterprises mostly run Workday, Oracle Recruiting Cloud, SmartRecruiters or iCIMS; startups favour Greenhouse, Lever and Ashby.</p>'),
        ('Which ATS is most used in Europe?',
         f'<p>Among companies hiring mainly in European countries, the most common systems in our data are {", ".join(esc(ATS[a]["name"]) for a, _ in eu_top)}. Each country has its own leader: ' + ', '.join(leaders[:-1]) + ' and ' + leaders[-1] + ', as the table above shows.</p>'),
        ('Which ATS is most used in the United States?',
         f'<p>Among companies hiring mainly in the United States, the most common systems in our data are {", ".join(esc(ATS[a]["name"]) for a, _ in us_top)}.</p>'),
        ('How do I find out which ATS a company uses?',
         '<p>Search the company above, or paste one of its job links into the detector. By hand: open a job and check where the Apply button leads, such as boards.greenhouse.io, jobs.lever.co or myworkdayjobs.com.</p>'),
        ('Can I get the jobs from all these companies?',
         '<p>Yes. Career Site and ATS Jobs API on Apify searches the daily index behind these pages, more than a million open jobs from all 14 systems, and re-reads each match live with its full description.</p>'),
    ]
    stats_html = f'''      <ul class="stats">
        <li class="stat"><b>{total_c:,}</b><span>companies</span></li>
        <li class="stat"><b>14</b><span>applicant tracking systems</span></li>
        <li class="stat"><b>{total_j:,}</b><span>open jobs on {nice_date}</span></li>
        <li class="stat"><b>{len(per_cc)}</b><span>countries with hiring companies</span></li>
      </ul>'''
    body = '\n'.join([
        section('// at a glance', 'The data in numbers', stats_html, hid='numbers'),
        section('// lookup', 'Find which ATS a company uses', find, hid='find'),
        section('// compare', 'All 14 systems compared', table, hid='compare'),
        f'''    <section class="block" aria-label="Charts">
      <div class="two">
        <div><p class="cmt">// by companies</p><h2 class="h2">Companies per system</h2>{comp_bars}</div>
        <div><p class="cmt">// by open jobs</p><h2 class="h2">Open jobs per system</h2>{jobs_bars}</div>
      </div>
    </section>''',
        section('// by country', 'Most used ATS by country', cc_table, hid='countries'),
        cta(campaign=camp, slug='career-site-jobs-search', name=actor('career-site-jobs-search')['title'] or 'Career Site Jobs Search', unit='jobs', kicker='// get the jobs',
            lead='Every company on these pages feeds one daily job index. <strong>Career Site and ATS Jobs API</strong> lets you query it, and the <a href="/tools/job-data-feed/">job data feed</a> delivers all of it daily.',
            points=['More than a million open jobs from 40,000+ career sites on all 14 systems',
                    'Filter by title, country, seniority, remote, salary, skills and visa sponsorship',
                    'Each match re-read on its board with the full description and apply link',
                    'Schedules with new jobs only, API and CSV, Excel or JSON export'],
            also=[(s, actor(s)['title'] or s, 'jobs') for s in ('greenhouse-lever-workday-jobs-scraper', 'greenhouse-jobs-scraper', 'workday-jobs-scraper', 'lever-jobs-scraper', 'ashby-jobs-scraper') if actor(s)['public']]),
        section('// detector', 'Detect the ATS from a job link', detect, hid='detect'),
        section('// by hand', 'How to check which ATS a company uses', guide, hid='howto'),
        section('// method', 'How the data is collected', method, hid='method'),
        section('// questions', 'Frequently asked questions', faq_block(faq), hid='faq'),
        section('// per system', 'Company lists per system', f'      <ul class="linklist">{ats_links(None)}</ul>', hid='lists'),
    ])
    dataset = {'@context': 'https://schema.org', '@type': 'Dataset', 'name': 'Companies by applicant tracking system',
               'description': f'{total_c:,} companies and the applicant tracking system behind their public career site, across 14 systems, with careers page, main hiring country and open jobs. Built from public career sites by deriverge.',
               'url': SITE + path, 'dateModified': date, 'creator': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': SITE + '/'},
               'isAccessibleForFree': True, 'keywords': ['ATS market share', 'applicant tracking system', 'companies using ATS'],
               'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'application/json', 'contentUrl': f'{SITE}/tools/data/ats/{a}.json'} for a in by_comp]}
    layout(path=path, title=title, desc=desc, tab='companies-using-ats.json', kicker=f'// free data · updated {nice_date}',
           h1='Which ATS do companies use?', campaign=camp,
           lede=f'{total_c:,} companies and the applicant tracking system behind their career site: Greenhouse, Workday, Lever, Ashby, BambooHR and 9 more. Compare the systems, see who leads in each country and look up any company.',
           body=body, ld=[dataset, faq_ld(faq), webapp_ld('ATS detector and company lookup', path, desc, 'BusinessApplication')],
           trail=[('deriverge', '/'), ('Tools', '/tools/'), ('Which ATS do companies use?', path)],
           scripts=['<script src="/tools/js/ats-common.js" defer></script>', '<script src="/tools/js/ats-compare.js" defer></script>'])
    return total_c, total_j


def page_index(stats, total_c, total_j, date):
    path, camp = '/tools/', 'tools-index'
    title = 'Free Data Tools: DNS, WHOIS, Domains, Wayback, Phone, ATS'
    desc = ('Free browser tools: bulk DNS lookup, RDAP WHOIS, domain availability, Wayback Machine snapshots, phone '
            f'validation and {total_c:,} companies listed by ATS.')
    tools = [
        ('/tools/bulk-dns-lookup/', 'Bulk DNS lookup', 'A, AAAA, MX, TXT, NS, CNAME, CAA, SOA and DMARC for up to 20 domains, over DNS over HTTPS.', 'dns-records-lookup'),
        ('/tools/rdap-whois-lookup/', 'RDAP WHOIS lookup', 'Registrar, creation and expiry dates, status codes and nameservers, straight from the registry.', 'whois-domain-lookup'),
        ('/tools/domain-availability-checker/', 'Domain availability checker', 'Up to 20 names across .com, .io, .ai, .dev and 20 more extensions, checked with the registries.', 'domain-availability-checker'),
        ('/tools/wayback-machine-snapshots/', 'Wayback Machine snapshot finder', 'First, latest and closest-to-date captures of up to 20 URLs, with links to every archived copy.', None),  # bez placeného actoru, viz page_wayback
        ('/tools/phone-number-validator/', 'Phone number validator', 'Up to 50 numbers: valid or not, E.164, national format, line type and country, offline.', 'phone-number-validator'),
        ('/tools/companies-using-ats/', 'Which ATS do companies use?', f'{total_c:,} companies on 14 applicant tracking systems, a company lookup and an ATS detector.', 'career-site-jobs-search'),
    ]
    cards = ''
    for i, (p, n, d, s) in enumerate(tools):
        price = per1000(s) if s else None
        meta = f'Bulk version on Apify from {price} per 1,000' if price else ''
        cards += f'<li><a class="card" href="{p}"><span class="card-idx">{i + 1:02d}</span><h3>{esc(n)}</h3><p>{esc(d)}</p><span class="card-meta">{esc(meta)}</span></a></li>'
    ats_list = ''.join(f'<li><a href="/tools/companies-using-{a}/">Companies using {esc(ATS[a]["name"])}</a><span>{stats[a]["companies"]:,}</span></li>' for a in ORDER)
    body = '\n'.join([
        section('// tools', 'Tools', f'      <ul class="cards">{cards}</ul>', hid='tools'),
        section('// data', 'Companies by applicant tracking system', f'''      <div class="prose"><p>Lists of employers per ATS, built from {total_j:,} open jobs on public career sites. Search, sort and download each list.</p></div>
      <ul class="linklist">{ats_list}</ul>
      <div class="prose"><p>Need every job, every day? The <a href="/tools/job-data-feed/">job data feed</a> delivers the whole index as a daily file.</p></div>''', hid='data'),
        section('// why free', 'How these tools work', '''      <div class="prose">
        <p>Every tool runs in your browser and talks directly to the public source: DNS resolvers, domain registries, the Internet Archive. There is no server of ours in between, no signup and no tracking of what you look up.</p>
        <p>Each tool does one small job well. When you need thousands of rows, a schedule, an API or an export into your own systems, the same job runs as an actor in <a data-actor="" data-campaign="tools-index" href="''' + esc(actor_href('', 'tools-index')) + '''" target="_blank" rel="''' + REL + '''">our Apify Store profile</a>, where you pay only for the results you get.</p>
      </div>''', hid='how'),
    ])
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Free data tools', 'url': SITE + path, 'description': desc,
           'publisher': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': SITE + '/'},
           'hasPart': [{'@type': 'WebPage', 'name': n, 'url': SITE + p} for p, n, _, _ in tools]}]
    layout(path=path, title=title, desc=desc, tab='index.js', kicker='// free tools · no signup', h1='Free data tools', campaign=camp,
           lede='Small, fast tools for domains, DNS, web archives, phone numbers and hiring data. They run in your browser, and each one has a bulk version on Apify for when you need thousands of rows.',
           body=body, ld=ld, trail=[('deriverge', '/'), ('Tools', '/tools/')])


def floor_round(n):
    """Rounds a count down for 'more than' claims: 1,740,189 -> 1,700,000, 47,967 -> 47,000, 540,470 -> 540,000."""
    step = 100_000 if n >= 1_000_000 else 10_000 if n >= 100_000 else 1_000
    return n // step * step


def page_job_feed():
    path, camp = '/tools/job-data-feed/', 'job-data-feed'
    try:
        with urllib.request.urlopen('https://api.apify.com/v2/key-value-stores/jletghbJMlxiI0vnm/records/meta.json', timeout=60) as r:
            meta = json.load(r)
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f'job index meta.json not readable: {e}')
    jobs, comps, totals = meta['jobs'], meta['companies'], meta['totals']
    built = fmt_date(meta['generatedAt'][:10])
    j, c = f'{floor_round(jobs):,}', f'{floor_round(comps):,}'
    title = 'Job Data Feed: Daily Open Jobs from Company Career Sites'
    desc = (f'A daily feed of more than {j} open jobs from the career sites of more than {c} companies on 14 applicant '
            'tracking systems, as a file or an API. Free sample, monthly plans.')
    rows = ''.join(f'<tr><td class="k">{esc(ATS[a]["name"])}</td><td>more than {floor_round(n):,}</td></tr>'
                   for a, n in sorted(totals.items(), key=lambda x: -x[1]))
    fields = [
        ('title, company, companyWebsite', 'The job title as the employer wrote it, the employer and its website when the system shows it.'),
        ('ats, careerSiteUrl, url, applyUrl', 'The applicant tracking system, the career site, the job page and the apply link on the employer\'s own site.'),
        ('locations, countries, workArrangement', 'Locations as listed, ISO country codes, and <code>remote</code>, <code>hybrid</code> or <code>onsite</code>.'),
        ('employmentType, seniority, jobCategory, department', 'Full time, part time, contract, temporary, internship and more; level from intern to executive; one of 21 job categories; the department when listed.'),
        ('postedAt, firstSeenAt', 'The posting date when the system has one, and the day our index first saw the job.'),
        ('salaryMin, salaryMax, salaryCurrency, salaryPeriod', 'Pay as numbers when the ad states it, with yearly equivalents in <code>salaryYearlyMin</code> and <code>salaryYearlyMax</code>.'),
        ('skills, experienceYearsMin, educationLevel, visaSponsorship, language', 'Read from the description: skills, years of experience, education, visa sponsorship and the language of the ad.'),
        ('description', 'The full text of the ad, on request. It is the employer\'s text and can name a hiring manager.'),
    ]
    field_rows = ''.join(f'<tr><td class="k"><code>{esc(k)}</code></td><td>{v}</td></tr>' for k, v in fields)
    mail = ('mailto:info@deriverge.com?subject=' + urllib.parse.quote('Job data feed') + '&body=' + urllib.parse.quote(
        'Company:\nWhat the data is for:\nCountries, systems or job categories you need:\nDelivery (daily file or API) and format (JSON Lines or CSV):\n'))
    body = '\n'.join([
        section('// what you get', 'What is in the feed', f'''      <div class="prose">
        <p>Every open job our index finds on the public career sites of more than {c} companies, on 14 applicant tracking systems from Workday to Recruitee. The build of {built} held {jobs:,} open jobs. Each job is one record with the fields below; there is no candidate data and no recruiter contact list.</p>
      </div>
      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Fields</th><th>What they hold</th></tr></thead><tbody>{field_rows}</tbody></table></div>''', hid='fields'),
        section('// coverage', 'Open jobs per system', f'''      <div class="tbl-wrap"><table class="tbl tbl--fit"><thead><tr><th>System</th><th>Open jobs, {esc(built)}</th></tr></thead><tbody>{rows}</tbody></table></div>
      <div class="prose"><p>Boards on ten of the systems are read every day. Workday, Workable, Personio and iCIMS boards are read in rotation, each within one to three days. We read only the job boards that employers publish, without logins, and leave out career sites whose <code>robots.txt</code> disallows the job feed.</p></div>''', hid='coverage'),
        section('// delivery', 'How the feed is delivered', '''      <div class="prose">
        <ul>
          <li>Every morning a gzipped JSON Lines file (CSV on request) with all open jobs of your feed, at a private download link.</li>
          <li>Next to it, the jobs added and the jobs closed since the day before, so you can update your database without comparing files.</li>
          <li>A filtered feed keeps only the countries, systems, job categories or title keywords you choose.</li>
        </ul>
      </div>''', hid='delivery'),
        section('// pricing', 'Plans', '''      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Plan</th><th>What it includes</th><th>Price</th></tr></thead><tbody>
        <tr><td class="k">Filtered feed</td><td>Daily file of up to 200,000 open jobs chosen by country, system, job category or title keywords, with added and closed files.</td><td>from $299 per month</td></tr>
        <tr><td class="k">Full feed</td><td>Daily file of every open job in the index, with added and closed files and descriptions on request.</td><td>$799 per month</td></tr>
        <tr><td class="k">Custom</td><td>Other fields, a feed for named companies, or files in your own storage.</td><td>on request</td></tr>
      </tbody></table></div>
      <div class="prose"><p>Billed monthly by invoice from deriverge s.r.o., a Czech company with an EU VAT number. You can cancel at the end of any month.</p></div>''', hid='plans'),
        f'''    <aside class="block cta" aria-label="Start a job data feed">
      <p class="cmt">// start</p>
      <h2>Get a sample of your feed</h2>
      <p>Download the free sample: 1,050 real jobs added to the index in the three days before {esc(built)}, 75 from each system, without descriptions. Then write to us with what you need, and we reply with a sample of your exact feed and an offer, usually within one or two working days.</p>
      <div class="cta-row"><a class="btn" href="/tools/data/job-feed-sample.jsonl.gz" download>Download the sample (JSON Lines, gzip)</a> <a class="btn btn--ghost" href="{esc(mail)}">Ask for a feed</a></div>
      <p class="more">Prefer to pay per request? The same index is behind {actor_link('career-site-jobs-search', camp, 'Career Site and ATS Jobs API on Apify', cls='')} and our <a href="https://rapidapi.com/David%C4%8Cag%C3%A1nek/api/job-search-career-sites-and-ats" target="_blank" rel="noopener">Job Search API on RapidAPI</a>.</p>
    </aside>''',
    ])
    faq = [
        ('Where do the jobs come from?',
         '<p>From the public job boards that employers run on their applicant tracking systems, such as Workday, Greenhouse or Lever. Most career sites on our list were found through their addresses in the public Common Crawl web archive.</p>'),
        ('How fresh is the feed?',
         '<p>The index is rebuilt every night. Boards on ten systems are read daily and the other four in rotation within one to three days, so a new posting reaches the feed within three days.</p>'),
        ('Does the feed contain personal data?',
         '<p>No candidate data and no lists of recruiters. Descriptions are the employer\'s own text and can name a hiring manager or a contact; leave descriptions out if you do not need them.</p>'),
        ('Can I show the jobs on my own site?',
         '<p>You decide how you use the data and are responsible for using it lawfully and in line with the employers\' terms. Every record links to the job and apply page on the employer\'s own site. We remove any company from your feed on request.</p>'),
    ]
    body += '\n' + section('// faq', 'Questions', faq_block(faq), hid='faq')
    ld = [{'@context': 'https://schema.org', '@type': 'Dataset', 'name': 'Job data feed from company career sites', 'url': SITE + path,
           'description': desc, 'isAccessibleForFree': False,
           'creator': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': SITE + '/'},
           'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'application/x-ndjson', 'contentUrl': SITE + '/tools/data/job-feed-sample.jsonl.gz', 'name': 'Free sample'}]},
          faq_ld(faq)]
    layout(path=path, title=title, desc=desc, tab='job-data-feed', kicker='// data feed · for job boards and HR tech', h1='Job data feed',
           lede=f'Every open job from the career sites of more than {c} companies on 14 applicant tracking systems, delivered daily as one file. For job boards, HR tech products and labour market research.',
           body=body, ld=ld, campaign=camp)


def update_sitemap(date):
    """Replaces the /tools/ entries of the shared sitemap.xml and leaves every other entry as it is."""
    p = os.path.join(os.path.dirname(TOOLS), 'sitemap.xml')
    xml = open(p, encoding='utf-8').read()
    xml = re.sub(r'\n[ \t]*<url><loc>https://deriverge\.com/tools/[^<]*</loc>.*?</url>', '', xml)
    lines = []
    for path, _ in PAGES:
        pr = '0.8' if path in ('/tools/', '/tools/companies-using-ats/') or not path.startswith('/tools/companies-using-') else '0.7'
        lines.append(f'  <url><loc>{SITE}{path}</loc><lastmod>{date}</lastmod><priority>{pr}</priority></url>')
    xml = xml.replace('</urlset>', '\n'.join(lines) + '\n</urlset>')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(xml)


def main():
    agg = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get('TMPDIR', '/tmp'), 'ats-agg.json')
    by, stats, date, cn = load_ats(agg)
    ORDER.extend(sorted(ATS, key=lambda a: -stats[a]['companies']))
    sizes = write_ats_json(by, date)
    page_dns()
    page_whois()
    page_availability()
    page_wayback()
    page_phone()
    for a in ORDER:
        page_ats(a, by[a], stats[a], date, cn)
    total_c, total_j = page_compare(by, stats, date, cn)
    page_job_feed()
    page_index(stats, total_c, total_j, date)
    print('JSON sizes (KB):', {a: round(s / 1024) for a, s in sizes.items()}, 'total', round(sum(sizes.values()) / 1024), 'KB')
    update_sitemap(dt.date.today().isoformat())
    with open(os.path.join(HERE, 'pages.json'), 'w') as f:
        json.dump({'date': date, 'pages': PAGES}, f, indent=1)
    for p, t in PAGES:
        print(f'{len(t):3d}  {p}  {t}')


if __name__ == '__main__':
    main()
