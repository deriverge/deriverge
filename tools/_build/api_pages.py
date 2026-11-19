"""Guides to the public job posting APIs of applicant tracking systems: /tools/job-board-api/ and one page per system
with a documented public API (api_guides_data.GUIDES). Imported by build.py, which passes its helpers in."""
import html
import json

from api_guides_data import CHECKED, GUIDES, NO_PUBLIC_API, NOT_COVERED

esc = html.escape


def code(text, lang):
    return f'<pre class="code" data-lang="{lang}"><code>{esc(text)}</code></pre>'


def fill(s, ex):
    return s.replace('{EXAMPLE}', ex)


def example_key(a, st):
    """The biggest board in our index that the guide's example can call (a real, public board)."""
    for r in st['top']:
        k = r['k']
        if a == 'lever' and k.startswith('eu:'):
            continue
        if k and '/' not in k and ' ' not in k:
            return k, r['name']
    return 'example', 'Example Inc.'


def build(h, by, stats, date, cn):
    """h: helpers from build.py (layout, section, faq_block, faq_ld, fmt_date, ATS, cta, actor, SITE)."""
    nice = h.fmt_date(date)
    ATS = h.ATS
    guides = [a for a in GUIDES if a in ATS]
    for a in guides:
        page_guide(h, a, stats[a], nice, date, guides)
    page_hub(h, guides, stats, nice, date)


def links_other(guides, current):
    return ''.join(f'<li><a href="/tools/job-board-api/{g}/">{esc(GUIDES[g]["h1"])}</a></li>' for g in guides if g != current)


def page_guide(h, a, st, nice, date, guides):
    g = GUIDES[a]
    name = h.ATS[a]['name']
    path, camp = f'/tools/job-board-api/{a}/', f'job-board-api-{a}'
    ex, ex_name = g['example'] if g.get('example') else example_key(a, st)
    rows = ''.join(f'<tr><td><code>{esc(p)}</code></td><td>{d}</td></tr>' for p, d in g['params'])
    params = (f'<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Parameter</th><th>What it does</th></tr></thead><tbody>{rows}</tbody></table></div>'
              if g['params'] else '<p>The feed takes no query parameters.</p>')
    other = ''.join(f'<li><code>{esc(e)}</code>: {d}</li>' for e, d in g.get('other', []))
    endpoint = f'''      <div class="prose">
        <p><code>{esc(g["method"])} {esc(g["url"])}</code></p>
        <ul>
          <li><strong>Authentication:</strong> {g["auth"]}</li>
          <li><strong>Format:</strong> {g["format"]}</li>
          <li><strong>Pagination:</strong> {g["paging"]}</li>
        </ul>
      </div>
      {params}
      {f'<div class="prose" style="margin-top:22px"><p>Other endpoints of the same API:</p><ul>{other}</ul></div>' if other else ''}
      <p class="note">Source: <a href="{esc(g["doc"][1])}" target="_blank" rel="noopener">{esc(g["doc"][0])}</a>. Checked {h.fmt_date(CHECKED)}.</p>'''
    examples = f'''      <div class="prose"><p>The board of <strong>{esc(ex_name)}</strong>, a {esc(name)} board from our index, as an example. Replace <code>{esc(ex)}</code> with the board you need.</p></div>
      <p class="code-label">curl</p>
      {code(fill(g["curl"], ex), "shell")}
      <p class="code-label">Python</p>
      {code(fill(g["python"], ex), "python")}
      <p class="code-label">Response (shortened)</p>
      {code(g["response"], g.get("response_lang", "json"))}'''
    frows = ''.join(f'<tr><td><code>{esc(f)}</code></td><td>{d}</td></tr>' for f, d in g['fields'])
    fields = f'<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Field</th><th>Meaning</th></tr></thead><tbody>{frows}</tbody></table></div>'
    find = f'''      <div class="prose">
        <p>{g["find"]}</p>
        <p>Our <a href="/tools/companies-using-{a}/">list of {st["companies"]:,} companies using {esc(name)}</a> shows the careers address of each one, and the address contains the identifier. The list is free to search and download as CSV.</p>
      </div>'''
    tips = '<div class="prose"><ul>' + ''.join(f'<li>{t}</li>' for t in g['tips']) + '</ul></div>'
    acts = [s for s in (f'{a}-jobs-scraper', 'career-site-jobs-search') if h.actor(s)['public']]
    scale = ''
    if acts:
        main = acts[0]
        title = h.actor(main)['title'] or main
        points = [f'Every open job of any {esc(name)} board, or a search across all {st["jobs"]:,} {esc(name)} jobs in our daily index without knowing a single board',
                  f'One schema for all {len(h.ATS)} systems: title, company, locations, remote, department, pay where published, full description, apply link',
                  'Filters for country, seniority, remote, salary and skills; new-only runs for daily schedules',
                  'API, webhooks and CSV, Excel or JSON export']
        also = [(s, h.actor(s)['title'] or s, 'jobs') for s in acts[1:]]
        scale = h.cta(campaign=camp, slug=main, name=title, unit='jobs', points=points, also=also, kicker='// skip the plumbing',
                      lead=f'The API answers one company at a time. <strong>{esc(title)}</strong> reads any {esc(name)} board for you, or searches every {esc(name)} job we know of.')
    faq = [
        (f'Does the {name} job board API need an API key?', f'<p>{g["faq_key"]}</p>'),
        (f'Is there a rate limit?', f'<p>{g["faq_rate"]}</p>'),
        (f'Can I get all {name} jobs, from every company, at once?',
         f'<p>No. The API answers for one company per request, and {esc(name)} publishes no list of its customers. Our index reads {st["with_jobs"]:,} {esc(name)} boards with open jobs every day ({st["jobs"]:,} jobs on {nice}); you can search all of them through our Apify actor or get them as a daily <a href="/tools/job-data-feed/">job data feed</a>.</p>'),
        (f'Is it allowed to use the {name} job board API?',
         f'<p>The API exists so that companies can show their jobs on their own sites and so that job boards can list them. It returns only what the employer has published. Read {esc(name)}\'s documentation and terms for your use, keep request rates modest and link back to the original job for applications.</p>'),
    ]
    body = '\n'.join([
        h.section('// the endpoint', f'The {name} job board endpoint', endpoint, hid='endpoint'),
        h.section('// try it', 'Request and response', examples, hid='example'),
        h.section('// the data', 'Fields of a job', fields, hid='fields'),
        h.section('// which board', f'Finding a company\'s {g["id_name"]}', find, hid='find'),
        h.section('// in practice', 'What we learned reading it every day', tips, hid='tips'),
        scale,
        h.section('// questions', 'Frequently asked questions', h.faq_block(faq), hid='faq'),
        h.section('// other systems', 'Public job APIs of other applicant tracking systems',
                  f'      <ul class="linklist">{links_other(guides, a)}<li><a href="/tools/job-board-api/">All {len(h.ATS)} systems compared</a></li></ul>', hid='other'),
    ])
    article = {'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': g['seo'], 'url': h.SITE + path,
               'description': g['desc'], 'dateModified': date, 'proficiencyLevel': 'Beginner',
               'author': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': h.SITE + '/'},
               'publisher': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': h.SITE + '/'}}
    lede = (f'{g["lede"]} '
            f'Our index calls it for <strong>{st["with_jobs"]:,}</strong> companies a day and holds <strong>{st["jobs"]:,}</strong> open {esc(name)} jobs ({nice}).')
    h.layout(path=path, title=g['seo'], desc=g['desc'], tab=f'{a}-api.md', kicker=f'// developer guide · checked {h.fmt_date(CHECKED)}',
             h1=g['h1'], lede=lede, body=body, campaign=camp, ld=[article, h.faq_ld(faq)],
             trail=[('deriverge', '/'), ('Tools', '/tools/'), ('Job board APIs', '/tools/job-board-api/'), (g['h1'], path)])


def page_hub(h, guides, stats, nice, date):
    path, camp = '/tools/job-board-api/', 'job-board-api'
    ATS = h.ATS
    order = sorted(ATS, key=lambda a: -stats[a]['jobs'])
    rows = ''
    for a in order:
        s = stats[a]
        name = ATS[a]['name']
        if a in GUIDES:
            g = GUIDES[a]
            api = f'<a href="/tools/job-board-api/{a}/">Yes, {esc(g["format_short"])}</a>'
            key = 'No'
            desc = esc(g['hub_desc'])
        elif a in NOT_COVERED:
            api = 'Not covered yet'
            key = '-'
            desc = 'We have not checked this system\'s documentation yet.'
        else:
            api = 'None documented'
            key = '-'
            desc = esc(NO_PUBLIC_API.get(a, 'No documented public job API. Jobs are on each company\'s career site.'))
        rows += (f'<tr><td><a href="/tools/companies-using-{a}/">{esc(name)}</a></td><td>{api}</td><td>{key}</td><td>{desc}</td>'
                 f'<td class="num">{s["with_jobs"]:,}</td><td class="num">{s["jobs"]:,}</td></tr>')
    total_j = sum(stats[a]['jobs'] for a in ATS)
    table = f'''      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>System</th><th>Public job API</th><th>Key</th><th>What you get</th><th class="num">Companies with jobs</th><th class="num">Open jobs</th></tr></thead><tbody>{rows}</tbody></table></div>
      <p class="note">Companies and jobs: what our index read from each system on {nice}. "Public job API" means the vendor documents a read-only endpoint or feed of a company\'s published jobs.</p>'''
    guide_list = ''.join(f'<li><a href="/tools/job-board-api/{a}/">{esc(GUIDES[a]["h1"])}</a><span>{esc(GUIDES[a]["format_short"])}</span></li>' for a in guides)
    why = f'''      <div class="prose">
        <p>An applicant tracking system (ATS) is where a company posts its jobs and collects applications. Most of them publish each company\'s open jobs on a career site, and {len(guides)} of the {len(ATS)} systems we read also document a public endpoint that returns those jobs as JSON, XML or RSS, made for career pages and job boards. Every guide links to the vendor\'s documentation and was checked against it and against a live response on the date shown.</p>
        <p>Three things are the same everywhere:</p>
        <ul>
          <li><strong>One company per request.</strong> Every endpoint takes a company identifier (board token, site name, subdomain). No vendor publishes a list of its customers, so finding the boards is the real work. Our free lists of <a href="/tools/companies-using-ats/">companies by ATS</a> give you the identifiers.</li>
          <li><strong>Only published jobs.</strong> The endpoints return what the employer chose to show candidates: no applicants, no internal data, no personal data beyond what is in the job text.</li>
          <li><strong>Different shapes.</strong> Field names, locations, dates and pay come in a different form from each system, and some send descriptions only on a second call. The guides below show each one.</li>
        </ul>
      </div>'''
    faq = [
        ('Which ATS have a public job posting API?',
         '<p>' + ', '.join(esc(ATS[a]['name']) for a in guides) + ' document a public endpoint for a company\'s published jobs (Recruitee only until 10 February 2027, when it starts requiring a token from each company). '
         + ', '.join(esc(ATS[a]['name']) for a in ATS if a not in GUIDES and a not in NOT_COVERED) + ' document no public job API for third parties; their jobs are on each company\'s career site.</p>'),
        ('Do I need an API key?', '<p>Not for reading published jobs from the endpoints in these guides, with one coming exception: Recruitee requires a token created by each company from 10 February 2027. Keys are needed for the other APIs of each system, which are meant for the employer itself.</p>'),
        ('How do I get jobs from all companies on all systems?',
         f'<p>Call each company\'s board, normalise the fields and repeat every day, or use an index that does it. Ours reads {sum(stats[a]["with_jobs"] for a in ATS):,} career sites on {len(ATS)} systems daily ({total_j:,} open jobs on {nice}); search it through our Apify actor or take it as a daily <a href="/tools/job-data-feed/">job data feed</a>.</p>'),
    ]
    acts = [s for s in ('career-site-jobs-search',) if h.actor(s)['public']]
    scale = ''
    if acts:
        title = h.actor(acts[0])['title'] or acts[0]
        scale = h.cta(campaign=camp, slug=acts[0], name=title, unit='jobs', kicker='// all systems, one schema',
                      lead=f'<strong>{esc(title)}</strong> searches every job in our daily index across all {len(ATS)} systems, with one set of fields.',
                      points=[f'{total_j:,} open jobs from {sum(stats[a]["with_jobs"] for a in ATS):,} career sites, rebuilt every day',
                              'Filter by title, country, seniority, remote, salary, skills and visa sponsorship',
                              'Full description and the apply link of the employer, no contacts',
                              'Schedules with new jobs only, API and CSV, Excel or JSON export'])
    body = '\n'.join([
        h.section('// compared', f'Public job APIs of {len(ATS)} applicant tracking systems', table, hid='table'),
        h.section('// guides', 'Guides with endpoints, fields and examples', f'      <ul class="linklist">{guide_list}</ul>', hid='guides'),
        h.section('// before you start', 'How these APIs work', why, hid='how'),
        scale,
        h.section('// questions', 'Frequently asked questions', h.faq_block(faq), hid='faq'),
    ])
    title = f'Job Posting APIs of {len(ATS)} ATS: Greenhouse, Lever, Ashby and More'
    if len(title) > 62:
        title = f'Public Job Posting APIs of {len(ATS)} Applicant Tracking Systems'
    desc = (f'Which applicant tracking systems publish a public job API: endpoints, keys and formats for Greenhouse, Lever, Ashby, '
            f'SmartRecruiters and {len(guides) - 4} more, with guides and examples.')
    ld = [{'@context': 'https://schema.org', '@type': 'TechArticle', 'headline': title, 'url': h.SITE + path, 'description': desc, 'dateModified': date,
           'publisher': {'@type': 'Organization', 'name': 'deriverge s.r.o.', 'url': h.SITE + '/'}}, h.faq_ld(faq)]
    h.layout(path=path, title=title, desc=desc, tab='job-board-api.md', kicker=f'// developer guides · {nice}', h1='Job board APIs',
             lede=(f'Which applicant tracking systems let you read a company\'s open jobs through a public API, and how. '
                   f'{len(guides)} of the {len(ATS)} systems in our index document one; the guides show the endpoint, the fields and working requests.'),
             body=body, campaign=camp, ld=ld, trail=[('deriverge', '/'), ('Tools', '/tools/'), ('Job board APIs', path)])
