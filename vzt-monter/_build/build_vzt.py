#!/usr/bin/env python3
"""Builds /vzt-monter/index.html (cs) and /vzt-monter/<lang>/index.html for sk, de, pl, en."""
import html, json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from vzt_texts import LANGS, NAMES

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://deriverge.com/vzt-monter/'
AS = 'https://apps.apple.com/app/id6806400438'
GP = 'https://play.google.com/store/apps/details?id=cz.vztmonter.app'
MAIL = 'info@deriverge.com'
SPIRO = [63, 80, 100, 125, 150, 160, 180, 200, 224, 250, 280, 300, 315, 355, 400, 450, 500, 560, 630, 710,
         800, 900, 1000, 1120, 1250]

e = html.escape


def fmt(L, x, d):
    s = f'{x:.{d}f}'
    if L['code'] != 'en':
        s = s.replace('.', ',')
    return s


# ---- the same formulas as vzt.js, for the values shown before the script runs ----
def offset(D, O, a, R):
    r = math.radians(a)
    arm = R * math.tan(r / 2)
    C = O / math.sin(r)
    return dict(C=C, A=O / math.tan(r), arm=arm, L=C - 2 * arm)


def huebscher(a, b):
    return 1.3 * (a * b) ** 0.625 / (a + b) ** 0.25


def friction(v, Dm, k):
    Re = v * Dm / 15.11e-6
    f = 64 / Re if Re < 2300 else 0.25 / math.log10(k / 1000 / (3.7 * Dm) + 5.74 / Re ** 0.9) ** 2
    return f / Dm * 1.2 / 2 * v * v


def elbow(D, R, T, n):
    a = T / (2 * (n - 1))
    t = math.tan(math.radians(a))
    return dict(alpha=a, joint=2 * a, full=n - 2, axis=2 * R * t, inner=2 * (R - D / 2) * t, outer=2 * (R + D / 2) * t,
                hAxis=R * t, hInner=(R - D / 2) * t, hOuter=(R + D / 2) * t)


def badges(L, pre):
    gp = L['gp_badge']
    return (f'<div class="badges">\n'
            f'        <a href="{AS}"><img class="as" src="{pre}badge-appstore.svg" alt="{e(L["as_alt"])}" width="144" height="48"></a>\n'
            f'        <a href="{GP}"><img class="gp" src="{pre}{gp}" alt="{e(L["gp_alt"])}" width="184" height="71"></a>\n'
            f'      </div>')


def app_cta(L, c):
    return (f'<div class="app-cta"><p><b>{e(c["cta_b"])}</b>{e(c["cta"])}</p>'
            f'<span class="links"><a href="{AS}">App Store</a><a href="{GP}">Google Play</a></span></div>')


def how(L, c):
    return f'<details class="how"><summary>{e(L["how_t"])}</summary><p>{c["how"]}</p></details>'


def field(name, label, value, fid, mode='decimal'):
    return (f'<div class="field"><label for="{fid}">{e(label)}</label>'
            f'<input id="{fid}" name="{name}" type="text" inputmode="{mode}" autocomplete="off" value="{e(value)}"></div>')


def select(name, label, opts, fid, cls=''):
    o = ''.join(f'<option value="{v}"{" selected" if sel else ""}>{e(t)}</option>' for v, t, sel in opts)
    c = f' {cls}' if cls else ''
    return f'<div class="field{c}"><label for="{fid}">{e(label)}</label><select id="{fid}" name="{name}">{o}</select></div>'


def res(key, label, value, main=False, hidden=False, shape=None):
    cls = ' class="main"' if main else ''
    hid = ' hidden' if hidden else ''
    sh = f' data-shape="{shape}"' if shape else ''
    return f'<li{cls}{sh}{hid}><span>{e(label)}</span><output data-out="{key}">{e(value)}</output></li>'


def diagram(L):
    return f'''<svg class="diagram" viewBox="0 0 420 166" role="img" aria-label="{e(L["off"]["aria"])}">
          <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 120H150L270 30H410" stroke-width="18" opacity=".13"/>
            <path d="M10 120H150L270 30H410" stroke-width="2"/>
            <path d="M171.6 93.8l9.6 12.8M238.8 43.4l9.6 12.8" stroke-width="2"/>
            <path d="M192 120A42 42 0 0 0 183.6 94.8" stroke-width="1.5"/>
            <path d="M394 30V120M388 30h12M388 120h12" stroke-width="1.2"/>
            <path d="M150 148H270M150 142v12M270 142v12" stroke-width="1.2"/>
          </g>
          <g fill="currentColor" font-size="16" font-weight="700" font-family="inherit">
            <text x="402" y="81">O</text>
            <text x="196" y="66">L</text>
            <text x="196" y="113">α</text>
            <text x="205" y="164">A</text>
          </g>
        </svg>'''


def calc_offset(L, ids):
    c = L['off']
    D, O, a, k = 200, 500, 45, 1.0
    r = offset(D, O, a, k * D)
    mm = lambda x: fmt(L, x, 0) + ' mm'
    ang = [(15, '15°'), (22.5, fmt(L, 22.5, 1) + '°'), (30, '30°'), (45, '45°'), (60, '60°'), (90, '90°')]
    rk = [0.6, 1, 1.5, 2]
    p = 'off-'
    return f'''<form class="calc" id="{ids[0]}" data-calc="offset" novalidate>
      <h3>{e(c["h3"])}</h3>
      <p class="intro">{e(c["intro"])}</p>
      <div class="calc-body">
        <div>
          {diagram(L)}
          <div class="fields">
            {field("D", c["D"], "200", p + "D", "numeric")}
            {field("O", c["O"], "500", p + "O", "numeric")}
            {select("alpha", c["alpha"], [(v, t, v == a) for v, t in ang], p + "a")}
            {select("rk", c["rk"], [(v, t, v == k) for v, t in zip(rk, c["rk_opts"])], p + "rk")}
          </div>
        </div>
        <div>
          <ul class="results" aria-live="polite">
            {res("L", c["L"], mm(r["L"]), main=True)}
            {res("C", c["C"], mm(r["C"]))}
            {res("A", c["A"], mm(r["A"]))}
            {res("arm", c["arm"], mm(r["arm"]))}
            {res("R", c["R"], mm(k * D))}
          </ul>
          <p class="calc-msg" hidden></p>
          {how(L, c)}
        </div>
      </div>
      {app_cta(L, c)}
    </form>'''


def calc_velocity(L, ids):
    c = L['vel']
    Q, D = 1000, 315
    S = math.pi * (D / 2000) ** 2
    v = Q / 3600 / S
    dp = friction(v, D / 1000, 0.09)
    p = 'vel-'
    return f'''<form class="calc" id="{ids[1]}" data-calc="velocity" novalidate>
      <h3>{e(c["h3"])}</h3>
      <p class="intro">{e(c["intro"])}</p>
      <div class="calc-body">
        <div class="fields">
          {field("Q", c["Q"], "1000", p + "Q")}
          <div class="field wide"><span class="lbl" id="{p}shape">{e(c["shape"])}</span>
            <div class="seg" role="radiogroup" aria-labelledby="{p}shape">
              <label><input type="radio" name="shape" value="round" checked><span>{e(c["round"])}</span></label>
              <label><input type="radio" name="shape" value="rect"><span>{e(c["rect"])}</span></label>
            </div>
          </div>
          <div class="field" data-shape="round"><label for="{p}D">{e(c["D"])}</label><input id="{p}D" name="D" type="text" inputmode="numeric" autocomplete="off" value="315"></div>
          <div class="field" data-shape="rect" hidden><label for="{p}a">{e(c["a"])}</label><input id="{p}a" name="a" type="text" inputmode="numeric" autocomplete="off" value="400"></div>
          <div class="field" data-shape="rect" hidden><label for="{p}b">{e(c["b"])}</label><input id="{p}b" name="b" type="text" inputmode="numeric" autocomplete="off" value="200"></div>
        </div>
        <div>
          <ul class="results" aria-live="polite">
            {res("v", c["v"], fmt(L, v, 2) + " m/s", main=True)}
            {res("S", c["S"], fmt(L, S, 4) + " m²")}
            {res("dp", c["dp"], fmt(L, dp, 2) + " Pa/m")}
            {res("De", c["De"], "", hidden=True, shape="rect")}
          </ul>
          <p class="calc-msg" hidden></p>
          {how(L, c)}
        </div>
      </div>
      {app_cta(L, c)}
    </form>'''


def calc_rect(L, ids):
    c = L['rect']
    a, b = 400, 200
    De = huebscher(a, b)
    lo = max(s for s in SPIRO if s <= De)
    hi = min(s for s in SPIRO if s >= De)
    p = 'rect-'
    return f'''<form class="calc" id="{ids[2]}" data-calc="rect" novalidate>
      <h3>{e(c["h3"])}</h3>
      <p class="intro">{e(c["intro"])}</p>
      <div class="calc-body">
        <div class="fields">
          {field("a", c["a"], "400", p + "a", "numeric")}
          {field("b", c["b"], "200", p + "b", "numeric")}
        </div>
        <div>
          <ul class="results" aria-live="polite">
            {res("De", c["De"], fmt(L, De, 1) + " mm", main=True)}
            {res("spiro", c["spiro"], f"Ø{lo} / Ø{hi} mm")}
            {res("Darea", c["Darea"], fmt(L, 2 * math.sqrt(a * b / math.pi), 1) + " mm")}
            {res("S", c["S"], fmt(L, a * b / 1e6, 4) + " m²")}
          </ul>
          <p class="calc-msg" hidden></p>
          {how(L, c)}
        </div>
      </div>
      {app_cta(L, c)}
    </form>'''


def calc_elbow(L, ids):
    c = L['elb']
    D, R, T, n = 200, 300, 90, 4
    r = elbow(D, R, T, n)
    mm = lambda x: fmt(L, x, 0) + ' mm'
    p = 'elb-'
    return f'''<form class="calc" id="{ids[3]}" data-calc="elbow" novalidate>
      <h3>{e(c["h3"])}</h3>
      <p class="intro">{e(c["intro"])}</p>
      <div class="calc-body">
        <div class="fields">
          {field("D", c["D"], "200", p + "D", "numeric")}
          {field("R", c["R"], "300", p + "R", "numeric")}
          {field("theta", c["theta"], "90", p + "t")}
          {select("n", c["n"], [(i, str(i), i == n) for i in range(2, 9)], p + "n")}
        </div>
        <div>
          <ul class="results" aria-live="polite">
            {res("alpha", c["alpha"], fmt(L, r["alpha"], 2) + "°", main=True)}
            {res("joint", c["joint"], fmt(L, r["joint"], 2) + "°")}
            {res("make", c["make"], c["make_t"].replace("{full}", str(r["full"])))}
            {res("axis", c["axis"], mm(r["axis"]))}
            {res("inner", c["inner"], mm(r["inner"]))}
            {res("outer", c["outer"], mm(r["outer"]))}
            {res("hAxis", c["hAxis"], mm(r["hAxis"]))}
            {res("hInner", c["hInner"], mm(r["hInner"]))}
            {res("hOuter", c["hOuter"], mm(r["hOuter"]))}
          </ul>
          <p class="calc-msg" hidden></p>
          {how(L, c)}
        </div>
      </div>
      {app_cta(L, c)}
    </form>'''


LOGO = ('<svg viewBox="0 0 100 100" fill="none" stroke="#15120E" aria-hidden="true">'
        '<path d="M17 32H40L64 60H83" stroke-width="13"/><path d="M17 22v20M83 50v20" stroke-width="6"/></svg>')


def page(L):
    code = L['code']
    pre = '' if code == 'cs' else '../'
    url = BASE + L['path']
    tags = {'f': L['tag_free'], 'p': L['tag_pro']}

    alts = '\n'.join(f'<link rel="alternate" hreflang="{x["code"]}" href="{BASE + x["path"]}">' for x in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}en/">'
    og_alt = '\n'.join(f'<meta property="og:locale:alternate" content="{x["og_locale"]}">' for x in LANGS if x is not L)

    # cs page is at the root: links from cs go to "sk/", from others to "../sk/" or "../" for cs.
    nav = ' '.join(
        f'<strong aria-current="page">{NAMES[x["code"]]}</strong>' if x is L else
        f'<a href="{(pre + x["path"]) or "./"}" lang="{x["code"]}" hreflang="{x["code"]}">{NAMES[x["code"]]}</a>'
        for x in LANGS)

    shots = ['03-sablona', '04-trasa', '07-denik']
    feature_list = [f[0] for f in L['feats'][:7]]
    ld = {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'VZT Montér',
        'operatingSystem': 'iOS, Android', 'applicationCategory': 'UtilitiesApplication',
        'applicationSubCategory': 'HVAC ductwork calculator',
        'description': L['og_desc'], 'inLanguage': code, 'url': url,
        'image': BASE + 'icon-512.png',
        'screenshot': [BASE + f'img/{code}-{s}.jpg' for s in ['01-odskok'] + shots],
        'featureList': feature_list,
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': L['currency']},
        'sameAs': [AS, GP],
        'publisher': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': 'https://deriverge.com/'},
    }
    ld_json = json.dumps(ld, ensure_ascii=False, indent=2)

    l10n = {
        'invalid': L['invalid'], 'offsetSuggest': L['off']['suggest'], 'offsetNone': L['off']['none'],
        'elbowMake': L['elb']['make_t'], 'elbowRadius': L['elb']['radius'],
    }

    feats = '\n'.join(
        f'    <div class="card"><h3>{e(t)}' + ''.join(f' <span class="tag{" pro" if k == "p" else ""}">{e(tags[k])}</span>' for k in kinds)
        + f'</h3><p>{e(txt)}</p></div>' for t, kinds, txt in L['feats'])

    gallery = '\n'.join(
        f'    <li><figure><img src="{pre}img/{code}-{s}.jpg" alt="{e(cap)}" width="540" height="960" loading="lazy"><figcaption>{e(cap)}</figcaption></figure></li>'
        for s, cap in zip(shots, L['caps']))

    anchor = L['anchor']
    privacy = f'<a href="{pre}soukromi.html#{anchor}">'
    support = f'<a href="{pre}podpora.html#{anchor}">'
    mail = f'<a href="mailto:{MAIL}">{MAIL}</a>'

    def faq_a(s):
        return e(s).replace('{privacy}', privacy).replace('{support}', support).replace('{/a}', '</a>').replace('{mail}', mail)

    faq = '\n'.join(f'    <h3>{e(q)}</h3>\n    <p>{faq_a(a)}</p>' for q, a in L['faq'])
    jump = ' '.join(f'<a href="#{i}">{e(t)}</a>' for i, t in zip(L['ids'], L['jump']))

    return f'''<!DOCTYPE html>
<html lang="{code}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(L["title"])}</title>
<meta name="description" content="{e(L["desc"])}">
<link rel="canonical" href="{url}">
{alts}
<link rel="icon" type="image/png" sizes="192x192" href="{pre}icon-192.png">
<link rel="apple-touch-icon" href="{pre}icon-192.png">
<meta name="theme-color" content="#F1F2F4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E0F11" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="VZT Montér">
<meta property="og:title" content="{e(L["og_title"])}">
<meta property="og:description" content="{e(L["og_desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/og-{code}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{L["og_locale"]}">
{og_alt}
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{pre}vzt.css">
<script type="application/ld+json">
{ld_json}
</script>
</head>
<body>
<div class="page">
  <header class="top">
    <a class="brand" href="{(pre + L["path"]) or "./"}"><span class="logo">{LOGO}</span><span><b>VZT Montér</b><small>{e(L["brand_sub"])}</small></span></a>
    <nav class="langs" aria-label="{e(L["nav"])}">{nav}</nav>
  </header>

  <main>
  <section class="hero">
    <div>
      <p class="eyebrow">{e(L["eyebrow"])}</p>
      <h1>{e(L["h1"])}</h1>
      <p class="lede">{e(L["lede"])}</p>
      {badges(L, pre)}
      <p class="note">{e(L["note"])}</p>
    </div>
    <img class="shot" src="{pre}img/{code}-01-odskok.jpg" alt="{e(L["hero_alt"])}" width="540" height="960" fetchpriority="high">
  </section>

  <nav class="jump" aria-label="{e(L["jump_label"])}"><span>{e(L["jump_label"])}</span> {jump}</nav>

  <section aria-labelledby="calc-h">
    <h2 id="calc-h">{e(L["calc_h2"])}</h2>
    <p class="sub">{e(L["calc_sub"])}</p>
    {calc_offset(L, L["ids"])}
    {calc_velocity(L, L["ids"])}
    {calc_rect(L, L["ids"])}
    {calc_elbow(L, L["ids"])}
  </section>

  <h2>{e(L["feat_h2"])}</h2>
  <p class="sub">{e(L["feat_sub"])}</p>
  <div class="grid">
{feats}
  </div>

  <h2>{e(L["gal_h2"])}</h2>
  <ul class="shots">
{gallery}
  </ul>

  <h2>{e(L["price_h2"])}</h2>
  <div class="plans">
    <div class="plan"><p class="k">{e(L["free_k"])}</p><h3>{e(L["free_h3"])}</h3><ul>{"".join(f"<li>{e(i)}</li>" for i in L["free_items"])}</ul></div>
    <div class="plan pro"><p class="k">{e(L["pro_k"])}</p><h3>{e(L["pro_h3"])}</h3><ul>{"".join(f"<li>{e(i)}</li>" for i in L["pro_items"])}</ul><p>{e(L["pro_p"])}</p></div>
  </div>

  <h2>{e(L["faq_h2"])}</h2>
  <div class="faq">
{faq}
  </div>

  <div class="cta">
    <img class="appicon" src="{pre}icon-512.png" alt="" width="96" height="96" loading="lazy">
    <h2>{e(L["cta_h2"])}</h2>
    <p class="sub">{e(L["cta_sub"])}</p>
    {badges(L, pre)}
  </div>
  </main>

  <footer>{support}{e(L["f_support"])}</a> &middot; {privacy}{e(L["f_privacy"])}</a> &middot; {nav}<br>{e(L["f_operator"])} <a href="/">deriverge s.r.o.</a> &middot; {mail}</footer>
</div>
<script>window.VZT_L10N = {json.dumps(l10n, ensure_ascii=False)};</script>
<script src="{pre}vzt.js" defer></script>
</body>
</html>
'''


for L in LANGS:
    d = os.path.join(OUT, L['path'])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(page(L))
    print('wrote', os.path.join(d, 'index.html'))
