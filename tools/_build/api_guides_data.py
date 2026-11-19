"""Facts for the job board API guides (/tools/job-board-api/<ats>/), rendered by api_pages.py.

Every endpoint, parameter and field here comes from the vendor's own documentation (doc link per system, read on
19 November 2026) and from a real response of a public board fetched the same day. Our adapters in
datova_slevarna/actors/career-site-jobs/src/ats/index.ts call the same endpoints every day ("tips" are what they
taught us). No long dashes: the layout refuses them. {EXAMPLE} in curl and python is replaced by the example board.
"""

# Date the guides were last checked against the vendors' documentation and live responses.
CHECKED = '2026-11-19'

GUIDES = {
    'greenhouse': dict(
        h1='Greenhouse Job Board API',
        seo='Greenhouse Job Board API: Endpoints, Fields, Examples',
        desc='How to read any company\'s Greenhouse jobs with the public Job Board API: endpoint, parameters, fields, pay ranges and working curl and Python examples.',
        lede='Greenhouse publishes every job board through a read-only JSON API at boards-api.greenhouse.io.',
        hub_desc='All jobs in one response, descriptions and pay ranges on request',
        format_short='JSON response',
        doc=('Greenhouse Job Board API documentation', 'https://docs.greenhouse.io/job-board.html'),
        method='GET', url='https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs',
        auth='none for GET requests. A key is needed only to submit applications through the API.',
        format='JSON, an object with <code>jobs</code> and <code>meta.total</code>.',
        paging='none. One request returns every published job of the board.',
        params=[('content=true', 'adds the full job description (<code>content</code>, HTML-escaped), departments and offices to each job'),
                ('pay_transparency=true', 'adds <code>pay_input_ranges</code>, the pay ranges the employer publishes. Documented for the single-job endpoint; the list accepted it too in our tests')],
        other=[('GET /v1/boards/{board_token}/jobs/{job_id}', 'one job with its description; <code>?questions=true</code> adds the application questions and <code>?pay_transparency=true</code> the pay ranges'),
               ('GET /v1/boards/{board_token}/departments', 'departments, each with its jobs (<code>render_as=list</code> or <code>tree</code>)'),
               ('GET /v1/boards/{board_token}/offices', 'offices, each with its departments and jobs (<code>render_as=list</code> or <code>tree</code>)'),
               ('GET /v1/boards/{board_token}', 'the board\'s name and intro text')],
        example=('stripe', 'Stripe'),
        curl='curl "https://boards-api.greenhouse.io/v1/boards/{EXAMPLE}/jobs?content=true&pay_transparency=true"',
        python='''import html
import requests

r = requests.get(
    "https://boards-api.greenhouse.io/v1/boards/{EXAMPLE}/jobs",
    params={"content": "true", "pay_transparency": "true"},
    timeout=60,
)
r.raise_for_status()
for job in r.json()["jobs"]:
    description_html = html.unescape(job.get("content", ""))  # content arrives HTML-escaped
    print(job["id"], job["title"], job["location"]["name"], job["absolute_url"])''',
        response='''{
  "jobs": [
    {
      "id": 8172510,
      "internal_job_id": 3537063,
      "title": "Abuse Investigator",
      "company_name": "Stripe",
      "location": { "name": "Seattle, San Francisco, New York City" },
      "absolute_url": "https://stripe.com/jobs/search?gh_jid=8172510",
      "updated_at": "2026-11-19T12:12:24-05:00",
      "first_published": "2026-09-09T10:50:29-04:00",
      "language": "en",
      "content": "&lt;h2&gt;&lt;strong&gt;Who we are &lt;/strong&gt;&lt;/h2&gt;...",
      "departments": [{ "id": 81946, "name": "8611 Security Analytics" }],
      "offices": [{ "id": 65234, "name": "US" }],
      "pay_input_ranges": []
    }
  ],
  "meta": { "total": 771 }
}''',
        fields=[('id', 'job post ID; it is also the <code>gh_jid</code> in job links on the company\'s own site'),
                ('internal_job_id', 'ID of the job behind the post; one job can have several posts'),
                ('title', 'job title'),
                ('company_name', 'the board\'s company name (documented for the single-job endpoint, present in list responses too)'),
                ('location.name', 'location as one free-text string, often several cities'),
                ('absolute_url', 'job page; points to the company\'s own careers site when the board is embedded there'),
                ('first_published / updated_at', 'when the post went live and when it last changed (<code>first_published</code> is documented for the single job)'),
                ('content', 'description, HTML-escaped (only with <code>content=true</code>)'),
                ('departments[] / offices[]', 'department and office tree (only with <code>content=true</code>)'),
                ('pay_input_ranges[]', 'published pay ranges with <code>min_cents</code>, <code>max_cents</code>, <code>currency_type</code> and <code>title</code> (only with <code>pay_transparency=true</code>)')],
        id_name='board token',
        find='The board token is the last part of the board address: <code>job-boards.greenhouse.io/stripe</code> or <code>boards.greenhouse.io/stripe</code> means the token <code>stripe</code>. When a company embeds the board on its own site, the page loads <code>boards.greenhouse.io/embed/job_board/js?for=&lt;token&gt;</code> and job links end with <code>?gh_jid=&lt;id&gt;</code>.',
        tips=['<code>content</code> is HTML with the tags escaped (<code>&amp;lt;p&amp;gt;</code>): unescape it once before you render or strip it.',
              'With <code>content=true</code> a big board is several megabytes (Stripe: about 6 MB for 770 jobs). If you need only titles and locations, leave it off and call <code>/departments</code> for the department of each job.',
              'Pay ranges are published by fewer than half of the employers, mostly for US jobs where pay transparency laws apply. When missing, <code>pay_input_ranges</code> is an empty list.',
              'A board that no longer exists answers HTTP 404. A board with no openings answers 200 with an empty <code>jobs</code> list, so do not treat it as an error.',
              '<code>absolute_url</code> often leads to the company\'s own careers site, not to Greenhouse. Use it as the apply link; it is what the employer wants candidates to open.'],
        faq_key='No. GET requests to the Job Board API need no key. Greenhouse uses keys only for posting applications through the API and for its Harvest API, which is for the employer\'s own data.',
        faq_rate='The documentation gives no number; it says requests may be rate limited for security and traffic reasons. One request per board returns everything, so a daily read of a board is a single call. Keep your request rate modest.',
    ),
    'lever': dict(
        h1='Lever Postings API',
        seo='Lever Postings API: Endpoints, Fields, Examples',
        desc='How to read any company\'s Lever jobs with the public Postings API: endpoint, EU host, filters, pagination, fields and working curl and Python examples.',
        lede='Lever publishes every company\'s job site through the read-only Postings API at api.lever.co, with a separate host for accounts in the European Union.',
        hub_desc='JSON list with filters, full description in sections, EU host',
        format_short='JSON response',
        doc=('Lever Postings API on GitHub', 'https://github.com/lever/postings-api'),
        method='GET', url='https://api.lever.co/v0/postings/{site}?mode=json',
        auth='none for reading published postings. Applying through the API needs a key from the company.',
        format='JSON with <code>mode=json</code>: a list of postings. Without it the API answers with HTML for embedding.',
        paging='optional, with <code>skip</code> and <code>limit</code>. Without them one request returns every posting.',
        params=[('mode=json', 'answer as JSON (other modes return HTML or an iframe)'),
                ('skip, limit', 'page through the list'),
                ('location, commitment, team, department, level', 'filter by these categories; repeat a parameter to match any of several values (then case-sensitive)'),
                ('group=team', 'group postings by <code>location</code>, <code>commitment</code> or <code>team</code>')],
        other=[('GET /v0/postings/{site}/{posting_id}', 'one posting'),
               ('https://api.eu.lever.co/v0/postings/{site}', 'the same API for accounts hosted in the EU')],
        example=('palantir', 'Palantir Technologies'),
        curl='curl "https://api.lever.co/v0/postings/{EXAMPLE}?mode=json&limit=10"',
        python='''import requests

def lever_postings(site):
    # EU accounts live only on api.eu.lever.co; the US host answers 404 for them.
    for host in ("https://api.lever.co", "https://api.eu.lever.co"):
        r = requests.get(f"{host}/v0/postings/{site}", params={"mode": "json"}, timeout=60)
        if r.status_code != 404:
            r.raise_for_status()
            return r.json()
    return []

for p in lever_postings("{EXAMPLE}"):
    print(p["id"], p["text"], p["categories"].get("location"), p["hostedUrl"])''',
        response='''[
  {
    "id": "6ed76ce8-4156-4b60-b120-403538bd66cd",
    "text": "Administrative Business Partner",
    "categories": {
      "commitment": "Full-time",
      "location": "Singapore, Singapore",
      "team": "Administrative",
      "allLocations": ["Singapore, Singapore"]
    },
    "country": "SG",
    "workplaceType": "hybrid",
    "createdAt": 1786469891368,
    "descriptionPlain": "A World-Changing Company...",
    "lists": [{ "text": "Administrative Business Partner (Foundry)", "content": "<li>Provide administrative support...</li>" }],
    "additionalPlain": "Palantir is particularly interested in...",
    "hostedUrl": "https://jobs.lever.co/palantir/6ed76ce8-...",
    "applyUrl": "https://jobs.lever.co/palantir/6ed76ce8-.../apply"
  }
]''',
        fields=[('id', 'posting ID (UUID)'),
                ('text', 'job title'),
                ('categories.location / allLocations', 'main location and all locations of the posting'),
                ('categories.team, department, commitment', 'team, department and type of employment, as the company names them'),
                ('workplaceType', '<code>on-site</code>, <code>hybrid</code>, <code>remote</code> or <code>unspecified</code>'),
                ('country', 'country code of the posting'),
                ('createdAt', 'creation time in milliseconds since 1970; not in the documentation, but present in every response we have read'),
                ('description / descriptionPlain', 'opening part of the description, HTML and plain text'),
                ('lists[]', 'titled sections such as requirements, each with HTML list items in <code>content</code>'),
                ('additional / additionalPlain', 'closing part of the description'),
                ('salaryRange / salaryDescription', 'pay: <code>min</code>, <code>max</code>, <code>currency</code> and <code>interval</code>, plus a free-text note, when the company publishes pay'),
                ('hostedUrl / applyUrl', 'job page and application form')],
        id_name='site name',
        find='Lever describes the site name as usually the company name with no spaces. It is the first part of the path on the company\'s Lever job site: <code>jobs.lever.co/palantir</code> means <code>palantir</code>. A job site at <code>jobs.eu.lever.co/&lt;site&gt;</code> belongs to an EU account, and its postings are only on <code>api.eu.lever.co</code>.',
        tips=['The full description is in three parts: <code>description</code> (opening), <code>lists</code> (sections such as requirements, each with a title) and <code>additional</code>. Read only the first and you lose the requirements; join all three.',
              'EU accounts answer 404 on api.lever.co. Try the EU host when the US one says 404, or start with the EU host for job sites at jobs.eu.lever.co.',
              'The company name is not in the response. It is in the title of the job site page, <code>jobs.lever.co/&lt;site&gt;</code>.',
              '<code>createdAt</code> is in milliseconds, not seconds.',
              'Pay (<code>salaryRange</code>) appears only when the company enters it, mostly for jobs in US states with pay transparency laws.'],
        faq_key='No. Reading published postings needs no key. The apply endpoint of the Postings API needs a key that the company itself issues.',
        faq_rate='Lever documents a limit only for applications (2 per second, then HTTP 429), none for reading postings. One request returns all postings of a site, so a daily read is one call per company. Keep your request rate modest.',
    ),
    'ashby': dict(
        h1='Ashby Job Posting API',
        seo='Ashby Job Posting API: Endpoint, Fields, Examples',
        desc='How to read any company\'s Ashby jobs with the public Job Posting API: endpoint, compensation, fields and working curl and Python examples.',
        lede='Ashby publishes each company\'s job board through a public Job Posting API at api.ashbyhq.com.',
        hub_desc='All listed jobs with HTML and plain descriptions, compensation on request',
        format_short='JSON response',
        doc=('Ashby Public Job Posting API documentation', 'https://developers.ashbyhq.com/docs/public-job-posting-api'),
        method='GET', url='https://api.ashbyhq.com/posting-api/job-board/{JOB_BOARD_NAME}',
        auth='none. The job board API is public.',
        format='JSON, an object with <code>jobs</code> and <code>apiVersion</code>.',
        paging='none. One request returns every listed job.',
        params=[('includeCompensation=true', 'adds <code>compensation</code> to each job: a summary, the tiers and their components')],
        other=[],
        example=('openai', 'OpenAI'),
        curl='curl "https://api.ashbyhq.com/posting-api/job-board/{EXAMPLE}?includeCompensation=true"',
        python='''import requests

r = requests.get(
    "https://api.ashbyhq.com/posting-api/job-board/{EXAMPLE}",
    params={"includeCompensation": "true"},
    timeout=60,
)
r.raise_for_status()
for job in r.json()["jobs"]:
    pay = (job.get("compensation") or {}).get("scrapeableCompensationSalarySummary")
    print(job["id"], job["title"], job["location"], job["isRemote"], pay, job["jobUrl"])''',
        response='''{
  "apiVersion": "1",
  "jobs": [
    {
      "id": "8fb1615c-34bf-47c4-a1d1-b7b2f836bbd3",
      "title": "Technical Program Manager, Compute Infrastructure",
      "department": "Technical Program Management",
      "team": "Technical Program Management",
      "employmentType": "FullTime",
      "location": "San Francisco",
      "secondaryLocations": [],
      "isRemote": true,
      "workplaceType": "Hybrid",
      "isListed": true,
      "publishedAt": "2026-11-05T02:20:02.702+00:00",
      "jobUrl": "https://jobs.ashbyhq.com/openai/8fb1615c-...",
      "applyUrl": "https://jobs.ashbyhq.com/openai/8fb1615c-.../application",
      "descriptionHtml": "<h3><strong>About the Team</strong></h3>...",
      "descriptionPlain": "ABOUT THE TEAM...",
      "compensation": {
        "compensationTierSummary": "$207K - $285K • Offers Equity",
        "scrapeableCompensationSalarySummary": "$207K - $285K",
        "compensationTiers": [],
        "summaryComponents": []
      }
    }
  ]
}''',
        fields=[('id', 'job ID (UUID); not in the field table of the documentation, but present in responses'),
                ('title, department, team', 'title and where the job sits in the company'),
                ('employmentType', '<code>FullTime</code>, <code>PartTime</code>, <code>Intern</code>, <code>Contract</code> or <code>Temporary</code>'),
                ('location / secondaryLocations[]', 'main location and further locations'),
                ('isRemote / workplaceType', 'remote flag and <code>OnSite</code>, <code>Remote</code> or <code>Hybrid</code>'),
                ('address.postalAddress', 'structured address: locality, region, country'),
                ('publishedAt', 'when the job was last published'),
                ('isListed', '<code>false</code> for unlisted jobs, which Ashby says should be reachable only by direct link'),
                ('descriptionHtml / descriptionPlain', 'the full description in HTML and as plain text'),
                ('jobUrl / applyUrl', 'job page and application form'),
                ('compensation', 'summary and tiers of pay and equity (only with <code>includeCompensation=true</code>, and only when the company shows it)')],
        id_name='job board name',
        find='The job board name is the first part of the path on <code>jobs.ashbyhq.com</code>: <code>jobs.ashbyhq.com/openai</code> means <code>openai</code>. Job links on the company\'s own site carry <code>?ashby_jid=&lt;id&gt;</code>.',
        tips=['Ask for <code>includeCompensation=true</code>: <code>scrapeableCompensationSalarySummary</code> is a short pay range, and <code>compensationTierSummary</code> adds equity and bonus.',
              'A board answers HTTP 404 when the name does not exist. Names are case-sensitive in some boards; use the exact path from the job board address.',
              'The organisation name is not in the API response. It is on the job board page, which titles itself "&lt;Company&gt; Jobs".',
              'Big boards are large: OpenAI\'s 840 jobs with descriptions are about 15 MB. Cache the response and read each board once a day.'],
        faq_key='No. Ashby\'s Job Posting API is public and takes no key.',
        faq_rate='Ashby documents no rate limit for this API. One request returns the whole board, so a daily read is one call per company. Keep your request rate modest.',
    ),
    'smartrecruiters': dict(
        h1='SmartRecruiters Posting API',
        seo='SmartRecruiters Posting API: Endpoints, Fields, Examples',
        desc='How to read any company\'s SmartRecruiters jobs with the public Posting API: endpoints, pagination, filters, fields and working curl and Python examples.',
        lede='SmartRecruiters publishes every company\'s job postings through a public Posting API at api.smartrecruiters.com, in pages of up to 100.',
        hub_desc='Paged list of postings, the description in a second call per job',
        format_short='JSON response',
        doc=('SmartRecruiters Posting API documentation', 'https://developers.smartrecruiters.com/docs/posting-api'),
        method='GET', url='https://api.smartrecruiters.com/v1/companies/{companyIdentifier}/postings',
        auth='none for public postings.',
        format='JSON: <code>offset</code>, <code>limit</code>, <code>totalFound</code> and the postings in <code>content</code>.',
        paging='<code>limit</code> (up to 100) and <code>offset</code>. Read pages until one comes back with fewer than <code>limit</code> postings.',
        params=[('limit, offset', 'page size (up to 100) and position'),
                ('q', 'full-text search in the postings'),
                ('country, region, city', 'filter by location'),
                ('locationType', '<code>REMOTE</code>, <code>HYBRID</code>, <code>ONSITE</code> or <code>ANY</code>'),
                ('department', 'filter by department ID'),
                ('releasedAfter', 'only postings published after this time'),
                ('language', 'only postings in this language')],
        other=[('GET /v1/companies/{companyIdentifier}/postings/{postingId}', 'one posting with the full job ad in <code>jobAd.sections</code>, <code>applyUrl</code>, <code>postingUrl</code> and <code>compensation</code> when published')],
        example=('ubisoft2', 'Ubisoft'),
        curl='curl "https://api.smartrecruiters.com/v1/companies/{EXAMPLE}/postings?limit=100&offset=0"',
        python='''import requests

BASE = "https://api.smartrecruiters.com/v1/companies/{EXAMPLE}/postings"
postings, offset = [], 0
while True:
    page = requests.get(BASE, params={"limit": 100, "offset": offset}, timeout=60).json()
    postings += page["content"]
    if len(page["content"]) < 100:
        break
    offset += 100

for p in postings[:3]:
    detail = requests.get(f"{BASE}/{p['id']}", timeout=60).json()
    sections = detail["jobAd"]["sections"]  # companyDescription, jobDescription, qualifications, additionalInformation
    print(p["id"], p["name"], p["location"]["fullLocation"], list(sections))''',
        response='''{
  "offset": 0,
  "limit": 100,
  "totalFound": 248,
  "content": [
    {
      "id": "744000162541249",
      "name": "Sr Community Developer - Splinter Cell",
      "refNumber": "REF32379A",
      "company": { "identifier": "Ubisoft2", "name": "Ubisoft" },
      "releasedDate": "2026-11-19T15:20:12.252Z",
      "location": {
        "city": "Toronto", "region": "ON", "country": "ca",
        "remote": false, "hybrid": false,
        "fullLocation": "Toronto, ON, Canada"
      },
      "department": { "id": "13847731", "label": "Ubisoft" },
      "function": { "id": "marketing", "label": "Marketing" },
      "typeOfEmployment": { "id": "permanent", "label": "Full-time" },
      "experienceLevel": { "id": "mid_senior_level", "label": "Mid-Senior Level" },
      "language": { "code": "en", "label": "English" },
      "ref": "https://api.smartrecruiters.com/v1/companies/ubisoft2/postings/744000162541249"
    }
  ]
}''',
        fields=[('id / uuid', 'posting ID and its UUID'),
                ('name', 'job title'),
                ('refNumber', 'the employer\'s requisition number'),
                ('company.name / identifier', 'company name and identifier'),
                ('releasedDate', 'when the posting was published'),
                ('location', 'city, region, country code, remote and hybrid flags, <code>fullLocation</code>'),
                ('department, function, industry', 'each with an <code>id</code> and a <code>label</code>'),
                ('typeOfEmployment / experienceLevel', 'employment type and seniority'),
                ('ref', 'API address of the full posting'),
                ('jobAd.sections (detail call)', 'company description, job description, qualifications and additional information, each with a title and HTML text'),
                ('compensation (detail call)', '<code>min</code>, <code>max</code>, <code>currency</code> and <code>period</code>, when published')],
        id_name='company identifier',
        find='The company identifier is the first part of the path on the career page: <code>careers.smartrecruiters.com/Ubisoft2</code> or <code>jobs.smartrecruiters.com/Ubisoft2/&lt;id&gt;</code> means <code>Ubisoft2</code>. The API accepts it in any letter case.',
        tips=['The list has no description. Each posting needs a second call to <code>/postings/{id}</code> for <code>jobAd.sections</code>, so a company with 4,000 postings is 40 list pages and 4,000 detail calls. Fetch details only for the postings you keep.',
              'Large employers (Bosch, AECOM, Accor) list several thousand postings; stop paging when a page is short, not at a fixed page count.',
              'The country in <code>location.country</code> is a lowercase ISO code.',
              'An identifier that does not exist answers HTTP 404; a company without public postings answers 200 with an empty <code>content</code>.'],
        faq_key='No. Public postings are readable without a key. Keys are for the Customer APIs, which manage the company\'s own jobs and candidates.',
        faq_rate='SmartRecruiters documents general API limits of 10 requests per second and 8 at a time per credential, and states nothing separate for anonymous reads of the Posting API. Because descriptions need one call per posting, big companies take thousands of requests: spread them out and cache what you have read.',
    ),
    'recruitee': dict(
        h1='Recruitee Careers Site API',
        seo='Recruitee Careers Site API: Endpoint, Fields, Examples',
        desc='How to read any company\'s Recruitee jobs with the public Careers Site API: the offers endpoint, fields, pay and working curl and Python examples.',
        lede='Recruitee publishes each company\'s job offers through the Careers Site API at &lt;company&gt;.recruitee.com/api/offers/. Until 10 February 2027 it answers without a key; after that date every call needs a token that the company creates.',
        hub_desc='All published offers with text and pay; a company token required from 10 Feb 2027',
        format_short='JSON response',
        doc=('Recruitee Careers Site API documentation', 'https://docs.recruitee.com/reference/intro-to-careers-site-api'),
        method='GET', url='https://{company}.recruitee.com/api/offers/',
        auth='none until 10 February 2027. From then on every call needs the header <code>X-Careers-Sites-Token</code> with a token the company creates in Recruitee (Settings, Apps and plugins, Careers API tokens); calls without it get HTTP 401.',
        format='JSON, an object with <code>offers</code>.',
        paging='none. One request returns every published offer.',
        params=[('department', 'only offers of this department, by name'), ('tag', 'only offers with this tag, by name')],
        other=[('GET https://{company}.recruitee.com/api/offers/{id or slug}', 'one offer')],
        example=('transperfect', 'TransPerfect'),
        curl='curl "https://{EXAMPLE}.recruitee.com/api/offers/"',
        python='''import requests

r = requests.get("https://{EXAMPLE}.recruitee.com/api/offers/", timeout=60)
r.raise_for_status()
for o in r.json()["offers"]:
    text = (o.get("description") or "") + (o.get("requirements") or "")  # both HTML
    print(o["id"], o["title"], o["location"], o["remote"], o["careers_url"])''',
        response='''{
  "offers": [
    {
      "id": 2833977,
      "guid": "k391n",
      "slug": "pharmacovigilance-case-management-specialist",
      "title": "Pharmacovigilance Case Management Specialist",
      "status": "published",
      "department": "Translation",
      "location": "Remote job",
      "city": "Remote",
      "country": "Indonesia",
      "country_code": "ID",
      "remote": true,
      "hybrid": false,
      "on_site": false,
      "employment_type_code": "contract",
      "experience_code": "mid_level",
      "education_code": "bachelor_degree",
      "category_code": "healthcare",
      "salary": { "min": null, "max": null, "period": null, "currency": null },
      "created_at": "2026-11-19 14:00:16 UTC",
      "published_at": "2026-11-19 14:08:06 UTC",
      "description": "<p><strong>PV Case Management Specialist</strong>...",
      "requirements": null,
      "careers_url": "https://transperfect.com/o/pharmacovigilance-case-management-specialist",
      "careers_apply_url": "https://transperfect.com/o/pharmacovigilance-case-management-specialist/c/new"
    }
  ]
}''',
        fields=[('id / guid / slug', 'offer ID, short ID and the slug in its address'),
                ('title, department', 'job title and department'),
                ('location, city, country, country_code', 'location as text and in parts'),
                ('remote / hybrid / on_site', 'where the work happens'),
                ('employment_type_code, experience_code, education_code, category_code', 'Recruitee\'s codes for type, seniority, education and field'),
                ('salary', '<code>min</code>, <code>max</code>, <code>period</code> and <code>currency</code>, when published'),
                ('created_at / published_at', 'creation and publication time (UTC, with a space instead of the ISO "T")'),
                ('description / requirements', 'two HTML parts of the job text'),
                ('careers_url / careers_apply_url', 'job page and application form, on the company\'s own domain when it has one'),
                ('translations', 'the offer in other languages of the career site')],
        id_name='company subdomain',
        find='The company subdomain is the first part of <code>&lt;company&gt;.recruitee.com</code>. Many companies show the career site under their own domain; the job links then look like <code>&lt;domain&gt;/o/&lt;job-slug&gt;</code>, and the <code>recruitee.com</code> address still answers.',
        tips=['Plan for 10 February 2027: from that date the API needs a token from each company. If you read career sites of companies that are not your customers, you will need another way to their jobs.',
              'The job text is split into <code>description</code> and <code>requirements</code>; join them for the full text.',
              'Dates are UTC but written as <code>2026-11-19 14:08:06 UTC</code>, not ISO 8601. Parse them with that format.',
              'Every offer also carries its application form settings and a mailbox address for applications. If you republish jobs, do not copy that address; link to <code>careers_apply_url</code>.',
              'A big career site is large: TransPerfect\'s 770 offers are about 11 MB, mostly translations. Read it once a day.'],
        faq_key='Not until 10 February 2027. From that date Recruitee requires an <code>X-Careers-Sites-Token</code> header, created by the company in its Recruitee settings, and answers HTTP 401 without it.',
        faq_rate='Recruitee documents no limit for the Careers Site API. One request returns all offers, so a daily read is one call per company. Keep your request rate modest.',
    ),
    'personio': dict(
        h1='Personio XML Job Feed',
        seo='Personio XML Job Feed: Address, Fields, Examples',
        desc='How to read any company\'s Personio jobs from the public XML job feed: address, languages, fields, descriptions and working curl and Python examples.',
        lede='Personio publishes each company\'s open positions as a public XML feed at &lt;company&gt;.jobs.personio.de/xml, made for job boards and career pages.',
        hub_desc='XML feed of all positions with descriptions in sections',
        format_short='XML feed',
        doc=('Personio developer hub: XML job feed', 'https://developer.personio.de/v1.0/reference/get_xml'),
        method='GET', url='https://{company}.jobs.personio.de/xml',
        auth='none; Personio\'s FAQ says the feed needs no credentials. The company has to switch the feed on (Settings, Recruiting, Career Page, Activations).',
        format='XML: a <code>&lt;workzag-jobs&gt;</code> root with one <code>&lt;position&gt;</code> per job.',
        paging='none. The feed lists every published position.',
        params=[('language', '<code>de</code>, <code>en</code>, <code>fr</code>, <code>es</code>, <code>nl</code>, <code>it</code> or <code>pt</code>: positions in this language of the career page. Jobs not translated into it can come back without descriptions')],
        other=[('https://{company}.jobs.personio.com/xml', 'the same feed for accounts on the .com domain')],
        example=('1komma5grad', '1KOMMA5°'),
        curl='curl "https://{EXAMPLE}.jobs.personio.de/xml"',
        python='''import requests
import xml.etree.ElementTree as ET

r = requests.get("https://{EXAMPLE}.jobs.personio.de/xml", timeout=60)
r.raise_for_status()
for pos in ET.fromstring(r.content).iter("position"):
    sections = [d.findtext("value") or "" for d in pos.iter("jobDescription")]  # HTML per section
    print(pos.findtext("id"), pos.findtext("name"), pos.findtext("office"), pos.findtext("createdAt"))''',
        response='''<?xml version="1.0" encoding="UTF-8"?>
<workzag-jobs>
  <position>
    <id>2625533</id>
    <subcompany>1KOMMA5° Riederich GmbH</subcompany>
    <office>Riederich</office>
    <department>Projektkoordination</department>
    <recruitingCategory>1K5° Riederich</recruitingCategory>
    <name>(Junior) Technisches Auftragsmanagement / Projektkoordination (m/w/d)</name>
    <jobDescriptions>
      <jobDescription>
        <name>Deine Aufgaben</name>
        <value><![CDATA[<ul><li>...</li></ul>]]></value>
      </jobDescription>
    </jobDescriptions>
    <employmentType>permanent</employmentType>
    <seniority>entry-level</seniority>
    <schedule>full-time</schedule>
    <yearsOfExperience>1-2</yearsOfExperience>
    <keywords>Auftragsmanagement,Customer Support,Organisation</keywords>
    <occupation>general_and_other_project_and_program_management</occupation>
    <occupationCategory>project_and_program_management</occupationCategory>
    <createdAt>2026-05-06T09:48:17+00:00</createdAt>
  </position>
</workzag-jobs>''',
        response_lang='xml',
        fields=[('id', 'position ID; the job page is <code>/job/&lt;id&gt;</code>'),
                ('name', 'job title'),
                ('subcompany', 'the legal entity, for groups with several companies'),
                ('office / additionalOffices', 'main and further locations'),
                ('department, recruitingCategory', 'department and the company\'s own grouping'),
                ('jobDescriptions', 'the job text in titled sections, HTML in CDATA'),
                ('employmentType, schedule, seniority, yearsOfExperience', 'contract type, full or part time, level and experience'),
                ('keywords, occupation, occupationCategory', 'tags and Personio\'s occupation codes'),
                ('createdAt', 'when the position was created')],
        id_name='company subdomain',
        find='The company subdomain is the first part of the job page address: <code>1komma5grad.jobs.personio.de</code> means <code>1komma5grad</code>. Job links look like <code>&lt;company&gt;.jobs.personio.de/job/&lt;id&gt;</code>.',
        tips=['Without <code>language</code> the feed uses the company\'s default language and every position has its description. With <code>language=en</code>, positions written only in German came back with empty <code>&lt;jobDescriptions&gt;</code> in 36 of 37 cases we tested.',
              'A company with no open positions returns an empty <code>&lt;workzag-jobs&gt;&lt;/workzag-jobs&gt;</code>, not an error.',
              'A closed account redirects to personio.com. Treat a redirect away from <code>*.jobs.personio.de</code> as "no such company".',
              'Personio\'s robots.txt applies to the feed. Read it first and respect HTTP 429: Personio rate limits automated readers.',
              'There is no posting date apart from <code>createdAt</code>, the date the position was created in Personio.'],
        faq_key='No. The XML feed is public for every company that publishes jobs on a Personio career page. Personio\'s REST API, for the company\'s own HR data, needs credentials.',
        faq_rate='Personio documents no number. Its FAQ suggests job boards sync the feed at least once an hour; in practice it answers very fast readers with HTTP 429 and its robots.txt sets the rules for automated access. Back off when asked to.',
    ),
    'teamtailor': dict(
        h1='Teamtailor Jobs RSS Feed',
        seo='Teamtailor Jobs RSS Feed: Address, Fields, Examples',
        desc='How to read any company\'s Teamtailor jobs without an API key from the public RSS feed: address, fields, locations, remote status and working examples.',
        lede='Teamtailor publishes each company\'s open jobs as an RSS feed at &lt;company&gt;.teamtailor.com/jobs.rss. The Teamtailor API needs a key from the company; the feed does not.',
        hub_desc='RSS feed of open jobs with locations and remote status (the API needs a key)',
        format_short='RSS feed',
        doc=('Teamtailor help: RSS feed', 'https://support.teamtailor.com/en/articles/11171756'),
        method='GET', url='https://{company}.teamtailor.com/jobs.rss',
        auth='none for the RSS feed. The Teamtailor REST API needs a key that the company creates.',
        format='RSS 2.0 with Teamtailor\'s own <code>tt:</code> elements for locations and department.',
        paging='the first 100 jobs by default. <code>offset</code> skips jobs and <code>per_page</code> sets how many come back.',
        params=[('offset', 'skip this many jobs, for example <code>offset=100</code> for jobs 101 and on'),
                ('per_page', 'jobs per response, for example <code>per_page=200</code>')],
        other=[('https://api.teamtailor.com/v1/jobs', 'the REST API: a key from the company, an <code>X-Api-Version</code> header, 30 jobs per page at most and 50 requests per 10 seconds')],
        example=('polestar', 'Polestar'),
        curl='curl "https://{EXAMPLE}.teamtailor.com/jobs.rss"',
        python='''import requests
import xml.etree.ElementTree as ET

TT = "{https://teamtailor.com/locations}"
offset, items = 0, []
while True:  # the feed sends the first 100 jobs unless asked for more
    r = requests.get("https://{EXAMPLE}.teamtailor.com/jobs.rss", params={"offset": offset, "per_page": 100}, timeout=60)
    r.raise_for_status()
    page = list(ET.fromstring(r.content).iter("item"))
    items += page
    if len(page) < 100:
        break
    offset += 100

for item in items:
    places = [loc.findtext(TT + "name") for loc in item.iter(TT + "location")]
    print(item.findtext("title"), places, item.findtext("remoteStatus"), item.findtext("link"))''',
        response='''<rss version="2.0" xmlns:tt="https://teamtailor.com/locations">
  <channel>
    <title>Polestar</title>
    <link>https://polestar.teamtailor.com/jobs</link>
    <item>
      <title>Regional HR Business Partner | BeNeLux</title>
      <description>&lt;p&gt;&lt;strong&gt;The opportunity&lt;/strong&gt;...</description>
      <pubDate>Thu, 12 Nov 2026 13:57:12 +0100</pubDate>
      <link>https://polestar.teamtailor.com/jobs/8710722-regional-hr-business-partner-benelux</link>
      <remoteStatus>none</remoteStatus>
      <guid>14093550-daa8-41e6-8a60-0b9722d1d4db</guid>
      <company_name>Polestar</company_name>
      <tt:locations>
        <tt:location>
          <tt:name>Brussels, Belgium</tt:name>
          <tt:city>Brussels</tt:city>
          <tt:country>Belgium</tt:country>
        </tt:location>
      </tt:locations>
      <tt:department>Human Resources</tt:department>
    </item>
  </channel>
</rss>''',
        response_lang='xml',
        fields=[('title', 'job title'),
                ('description', 'full description, HTML escaped inside the XML'),
                ('pubDate', 'publication date in RSS format'),
                ('link', 'job page; the number at its start is the job ID'),
                ('guid', 'a stable unique ID of the job'),
                ('remoteStatus', 'remote status, for example <code>none</code>, <code>onsite</code> or <code>hybrid</code>'),
                ('company_name', 'company name (also the channel title)'),
                ('tt:locations / tt:location', 'each location with name, city, zip and country'),
                ('tt:department, tt:role', 'department and role')],
        id_name='company subdomain',
        find='The company subdomain is the first part of <code>&lt;company&gt;.teamtailor.com</code>. Many companies run the career site on their own domain; the <code>teamtailor.com</code> address still works, and the page source loads assets from <code>teamtailor-cdn.com</code>.',
        tips=['The feed stops at 100 jobs unless you page with <code>offset</code> and <code>per_page</code>. Big employers have more; read until a response comes back short.',
              'Teamtailor documents what the feed contains but not the element names; the names above are what the feeds send today.',
              'Locations are inside <code>tt:locations</code>, one <code>tt:location</code> each. Read all of them; jobs in several cities list several.',
              '<code>remoteStatus</code> is the most reliable remote signal in the feed. Do not guess remote work from the title.',
              'The feed has no pay field. Pay, when published, is in the description.',
              'Every Teamtailor career site has the feed, also those on a custom domain: <code>&lt;custom domain&gt;/jobs.rss</code> answers too.'],
        faq_key='Not for the RSS feed: it is public. The Teamtailor REST API does need a key, which only the company can create.',
        faq_rate='Teamtailor documents no limit for the RSS feed (its REST API allows 50 requests per 10 seconds). A company with up to 100 jobs is one call, bigger ones one call per 100 jobs. Keep your request rate modest.',
    ),
    'gem': dict(
        h1='Gem Job Board API',
        seo='Gem Job Board API: Endpoint, Fields, Examples',
        desc='How to read any company\'s Gem jobs with the public job board API: endpoint, fields, locations, workplace type and working curl and Python examples.',
        lede='Gem publishes each company\'s job board through a public API at api.gem.com, shaped much like Greenhouse\'s.',
        hub_desc='All job posts with HTML and plain descriptions and workplace type',
        format_short='JSON response',
        doc=('Gem help: the job board API', 'https://help.gem.com/databases/gem-help-center/the-job-board-api'),
        method='GET', url='https://api.gem.com/job_board/v0/{vanity_url_path}/job_posts/',
        auth='none for published job posts.',
        format='JSON: a list of job posts.',
        paging='none; Gem says the API does not use pagination. One request returns every published post.',
        params=[],
        other=[('GET /job_board/v0/{vanity_url_path}/job_posts/{id}', 'one job post; <code>questions=true</code> adds the application questions'),
               ('GET /job_board/v0/{vanity_url_path}/departments/', 'departments'),
               ('GET /job_board/v0/{vanity_url_path}/offices/', 'offices')],
        example=('coupa-software-inc-ats-1', 'Coupa Software'),
        curl='curl "https://api.gem.com/job_board/v0/{EXAMPLE}/job_posts/"',
        python='''import requests

r = requests.get("https://api.gem.com/job_board/v0/{EXAMPLE}/job_posts/", timeout=60)
r.raise_for_status()
for p in r.json():
    print(p["id"], p["title"], p["location"]["name"], p.get("location_type"), p["absolute_url"])''',
        response='''[
  {
    "id": "8a292102-f0b7-4e88-8fa5-a2fdfb027eca",
    "title": "Sr. Associate Sourcing Consultant",
    "absolute_url": "https://jobs.gem.com/coupa-software-inc-ats-1/8a292102-...",
    "location": { "name": "Pune City, India" },
    "location_type": "remote",
    "employment_type": "full_time",
    "departments": [{ "id": "992a0f0542384f1ee5ef51b7cf4ae6c4", "name": "Services" }],
    "offices": [{ "name": "Pune, India", "location": { "name": "Pune City, India" } }],
    "created_at": "2024-11-19T07:53:57.000Z",
    "first_published_at": "2025-07-24T22:41:13.194Z",
    "updated_at": "2025-07-24T22:41:13.194Z",
    "content": "<div>Coupa makes margins multiply...",
    "content_plain": "Coupa makes margins multiply..."
  }
]''',
        fields=[('id', 'job post ID'),
                ('title', 'job title'),
                ('absolute_url', 'job page with the application form'),
                ('location.name / offices[]', 'main location and offices'),
                ('location_type', 'workplace: <code>in_office</code>, <code>hybrid</code> or <code>remote</code>'),
                ('employment_type', 'for example <code>full_time</code>, <code>part_time</code>, <code>contract</code>, <code>intern</code>'),
                ('departments[]', 'department tree'),
                ('first_published_at / updated_at / created_at', 'publication, last change and creation time'),
                ('content / content_plain', 'the description in HTML and as plain text')],
        id_name='job board path',
        find='Gem calls it the vanity URL path. It is the first part of the path on <code>jobs.gem.com</code>: <code>jobs.gem.com/coupa-software-inc-ats-1</code> means <code>coupa-software-inc-ats-1</code>. Some IDs are a readable company name, others a generated one like this.',
        tips=['The company name is not a field. Use the board\'s page title, or the company named in the description.',
              '<code>location_type</code> is the clean remote signal; offices tell you where an on-site or hybrid job is.',
              'Posts stay published for a long time on some boards (the example above was first published in 2025). Use <code>updated_at</code> and your own first-seen date to judge freshness.',
              'Gem answers HTTP 429 when read too fast. Read each board once a day and back off when asked.'],
        faq_key='No. The job board API returns published job posts without a key; only submitting applications through it needs one.',
        faq_rate='Gem documents 20 requests per second with bursts of 500 per API key, and does not say what applies to reads without a key. It does answer fast readers with HTTP 429. One request returns all job posts of a board, so a daily read is one call per company.',
    ),
}

# Systems without a documented public job API: what the hub table says about them.
NO_PUBLIC_API = {
    'workday': 'No documented public job API. Each career site loads its own jobs.',
    'icims': 'No documented public job API for third parties. Jobs are on each portal\'s career pages.',
    'oracle': 'No documented public job API for third parties. Jobs are on each Oracle career site.',
    'paylocity': 'No documented public job API. Jobs are on each company\'s Paylocity career page.',
    'eightfold': 'No documented public job API. Jobs are on each Eightfold career site.',
    'softgarden': 'No documented public job API. Jobs are on each company\'s career site.',
    'applicantpro': 'No documented public job API. Jobs are on each company\'s ApplicantPro career site.',
    'bamboohr': 'No documented public job API. Jobs are on each company\'s BambooHR careers page.',
    'rippling': 'No documented public job API. Jobs are on each company\'s Rippling job board.',
    'hireology': 'No documented public job API. Jobs are on each company\'s Hireology career site.',
    'breezy': 'No documented public job API. The career site and an embed widget show the jobs; the v3 API needs the company\'s token.',
}
# Systems this page does not cover yet (not checked against their documentation): the hub says so instead of guessing.
NOT_COVERED = {'workable', 'jazzhr'}
