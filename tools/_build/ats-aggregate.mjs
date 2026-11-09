// Aggregates the public job index into one record per company and ATS.
//
// Input (download first, all three are public records of key-value store jletghbJMlxiI0vnm):
//   meta.json           generatedAt of the index
//   index.jsonl.gz      one row per open job: a = ATS, s = slug, c = company, l = locations, u = job URL, h = website
//   companies.json.gz   one row per registry token: a, s (token), c (name or null), n
// Output: ats-agg.json (companies per ATS) and jobs-agg.json (jobs per country, for the job postings data pages),
// both consumed by build.py.
//
// Countries, job categories, seniority and remote come from enrich.ts in the datova_slevarna repo
// (career-site-jobs/src/enrich.ts), bundled here with esbuild on the fly, so the website uses the same parsers as
// the Apify actors.
//
//   node tools/_build/ats-aggregate.mjs <dir with index.jsonl.gz and companies.json.gz> [path to datova_slevarna]
import { createReadStream, readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { createGunzip, gunzipSync } from 'node:zlib';
import { createInterface } from 'node:readline';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const dir = resolve(process.argv[2] ?? '.');
const repo = resolve(process.argv[3] ?? join(process.env.HOME, 'Projekty_ClaudeCode/datova_slevarna'));

const require = createRequire(join(repo, 'package.json'));
const esbuild = require('esbuild');
const out = join(mkdtempSync(join(process.env.TMPDIR ?? tmpdir(), 'enrich-')), 'enrich.mjs');
const src = join(repo, 'actors/career-site-jobs/src');
await esbuild.build({
  stdin: { contents: `export * from './enrich.ts'; export { CITY_COUNTRY } from './city-countries.ts';`, resolveDir: src, loader: 'ts' },
  bundle: true, format: 'esm', platform: 'node', outfile: out, logLevel: 'error',
});
const { countriesOf, jobCategoryOf, seniorityOf, workArrangementOf, CITY_COUNTRY } = await import(pathToFileURL(out).href);

/** Board key per ATS: the token the careers URL is built from on the website. */
function boardKey(r) {
  const a = r.a;
  let u;
  try { u = new URL(r.u); } catch { u = null; }
  if (a === 'workday') {
    if (r.g && r.g.includes('/')) return r.g;
    if (!u) return null;
    const segs = u.pathname.split('/').filter(Boolean);
    const site = /^[a-z]{2}-[A-Z]{2}$/i.test(segs[0] ?? '') ? segs[1] : segs[0];
    return site ? `${u.host.toLowerCase()}/${site}` : null;
  }
  if (a === 'icims') return r.g && r.g.includes('.') ? r.g.toLowerCase() : (u ? u.host.toLowerCase() : null);
  if (a === 'oracle') {
    if (r.g && r.g.includes('/sites/')) return r.g;
    if (!u) return null;
    const m = /\/sites\/([^/]+)/.exec(u.pathname);
    return m ? `${u.host.toLowerCase()}/sites/${m[1]}` : null;
  }
  const slug = (r.g ?? r.s ?? '').trim();
  if (!slug) return null;
  if (a === 'lever' && u && u.host === 'jobs.eu.lever.co') return `eu:${slug.toLowerCase()}`;
  if (a === 'ashby') return slug; // Ashby tokens may contain spaces and capitals
  return slug.toLowerCase();
}

const companies = new Map(); // `${a}|${key}` -> record
const countryJobs = {}; // ATS -> ISO2 -> open jobs located there (a job in two countries counts in both)
const atsRemote = {}; // ATS -> remote jobs
function rec(a, key) {
  const id = `${a}|${key}`;
  let r = companies.get(id);
  if (!r) { r = { a, k: key, names: new Map(), jobs: 0, countries: new Map(), sites: new Map(), remote: 0 }; companies.set(id, r); }
  return r;
}

// ── Jobs per country for the job postings data pages (jobs-agg.json) ──
// REMOTE collects every remote job, whatever its country. `latest` keeps the newest jobs of each country: the page
// shows a few and the free CSV sample holds the rest.
const meta = JSON.parse(readFileSync(join(dir, 'meta.json'), 'utf8'));
const genDay = meta.generatedAt.slice(0, 10);
const since7 = new Date(Date.parse(genDay) - 6 * 86_400_000).toISOString().slice(0, 10); // the last 7 days, today included
const LATEST = 300;
const cstat = new Map();
const glob = { jobs: 0, remote: 0, new7: 0, cat: {}, sen: {}, employers: new Set() };
function cs(cc) {
  let s = cstat.get(cc);
  if (!s) { s = { jobs: 0, remote: 0, new7: 0, emp: new Map(), cat: {}, sen: {}, ats: {}, city: new Map(), cc: {}, latest: [], floor: null }; cstat.set(cc, s); }
  return s;
}
const inc = (o, k) => { o[k] = (o[k] ?? 0) + 1; };
/** Newest first: day first seen, then posting date, then key so the order is stable. */
const cmp = (x, y) => (y.f ?? '').localeCompare(x.f ?? '') || (y.p ?? '').localeCompare(x.p ?? '') || x.k.localeCompare(y.k);
function keepLatest(s, job) {
  if (s.floor && cmp(job, s.floor) >= 0) return;
  s.latest.push(job);
  if (s.latest.length >= LATEST * 3) { s.latest.sort(cmp); s.latest.length = LATEST; s.floor = s.latest[LATEST - 1]; }
}
/** Known cities of one country in a location: 'Munich, Bavaria, Germany', 'Germany, Munich, Otl-Aicher-Strasse', 'Austin, TX'. */
function citiesIn(loc, cc, seen) {
  for (const part of loc.split(/\s*[,;]\s*|\s+-\s+/)) {
    const orig = part.trim().replace(/\s+\d{3,6}(?:-\d{4})?$/, '').replace(/^\d{4,6}\s+/, '');
    const low = orig.toLowerCase();
    if (low.length >= 3 && CITY_COUNTRY[low] === cc && !seen.has(low)) { seen.set(low, orig); return; }
  }
}

const rl = createInterface({ input: createReadStream(join(dir, 'index.jsonl.gz')).pipe(createGunzip()), crlfDelay: Infinity });
let rows = 0;
for await (const line of rl) {
  if (!line) continue;
  const r = JSON.parse(line);
  rows++;
  const key = boardKey(r);
  if (!key) continue;
  const c = rec(r.a, key);
  c.jobs++;
  if (r.c) c.names.set(r.c, (c.names.get(r.c) ?? 0) + 1);
  if (r.h) c.sites.set(r.h, (c.sites.get(r.h) ?? 0) + 1);
  if (r.r === true || r.w === 'remote') { c.remote++; atsRemote[r.a] = (atsRemote[r.a] ?? 0) + 1; }
  const locs = (r.l ?? '').split(' | ').filter(Boolean);
  const cj = countryJobs[r.a] ??= {};
  const ccs = countriesOf(locs);
  for (const cc of ccs) { c.countries.set(cc, (c.countries.get(cc) ?? 0) + 1); cj[cc] = (cj[cc] ?? 0) + 1; }

  const id = `${r.a}|${key}`;
  const wa = workArrangementOf({ workplaceType: r.w, remote: r.r, locations: locs, title: r.t }, false);
  const cat = jobCategoryOf(r.t, r.d) ?? 'other';
  const sen = seniorityOf(r.t);
  const isNew = (r.f ?? '') >= since7;
  glob.jobs++; glob.employers.add(id); inc(glob.cat, cat); inc(glob.sen, sen);
  if (wa === 'remote') glob.remote++;
  if (isNew) glob.new7++;
  const job = { k: r.k, t: r.t, c: r.c, a: r.a, b: key, l: r.l, f: r.f, p: r.p, u: r.u, wa, cat, sen };
  for (const cc of wa === 'remote' ? [...ccs, 'REMOTE'] : ccs) {
    const s = cs(cc);
    s.jobs++;
    if (wa === 'remote') s.remote++;
    if (isNew) s.new7++;
    s.emp.set(id, (s.emp.get(id) ?? 0) + 1);
    inc(s.cat, cat); inc(s.sen, sen); inc(s.ats, r.a);
    if (cc === 'REMOTE') for (const x of ccs) inc(s.cc, x);
    else {
      const seen = new Map();
      for (const loc of locs) citiesIn(loc, cc, seen);
      for (const [low, orig] of seen) {
        const e = s.city.get(low) ?? { n: 0, spell: new Map() };
        e.n++; e.spell.set(orig, (e.spell.get(orig) ?? 0) + 1);
        s.city.set(low, e);
      }
    }
    keepLatest(s, job);
  }
}

// Registry companies without open jobs today still use the system; keep the ones whose board answered with a name.
const reg = JSON.parse(gunzipSync(readFileSync(join(dir, 'companies.json.gz'))).toString('utf8'));
const regName = new Map();
for (const x of reg) {
  let key = x.s;
  if (x.a !== 'ashby' && x.a !== 'workday' && x.a !== 'oracle') key = key.toLowerCase();
  if (x.c) regName.set(`${x.a}|${key}`, x.c);
  if (!companies.has(`${x.a}|${key}`) && !companies.has(`${x.a}|eu:${key}`) && x.c) rec(x.a, key).names.set(x.c, 1);
}

const top = (m) => { let best = null, n = -1; for (const [k, v] of m) if (v > n) { best = k; n = v; } return best; };
const result = [];
for (const [id, c] of companies) {
  const name = top(c.names) ?? regName.get(id) ?? null;
  const countries = [...c.countries.entries()].sort((x, y) => y[1] - x[1]);
  result.push({
    a: c.a, k: c.k, name, jobs: c.jobs, remote: c.remote,
    country: countries[0]?.[0] ?? null, countryJobs: countries[0]?.[1] ?? 0, nCountries: countries.length,
    countries: Object.fromEntries(countries.slice(0, 6)),
    site: top(c.sites),
  });
}
// English country names for the static pages (the browser does the same with Intl.DisplayNames).
const names = new Intl.DisplayNames(['en'], { type: 'region' });
const countryNames = {};
for (const per of Object.values(countryJobs)) for (const cc of Object.keys(per)) { try { countryNames[cc] = names.of(cc); } catch { countryNames[cc] = cc; } }
writeFileSync(join(dir, 'ats-agg.json'), JSON.stringify({ generatedAt: meta.generatedAt, rows, companies: result, countryJobs, atsRemote, countryNames }));
console.log(`rows ${rows}, companies ${result.length}`);

// Countries with at least 300 jobs (and REMOTE); the build decides which ones get a page.
const nameOf = new Map(result.map((x) => [`${x.a}|${x.k}`, x.name]));
const countries = {};
for (const [cc, s] of cstat) {
  if (s.jobs < 300) continue;
  if (cc !== 'REMOTE' && !countryNames[cc]) { try { countryNames[cc] = names.of(cc); } catch { countryNames[cc] = cc; } }
  s.latest.sort(cmp);
  const top = [...s.emp.entries()].sort((x, y) => y[1] - x[1]).slice(0, 40).map(([id, n]) => {
    const [a, ...k] = id.split('|');
    return [nameOf.get(id) ?? null, a, k.join('|'), n];
  });
  const cities = [...s.city.values()].sort((x, y) => y.n - x.n).slice(0, 12)
    .map((e) => [[...e.spell.entries()].sort((x, y) => y[1] - x[1])[0][0], e.n]);
  countries[cc] = {
    jobs: s.jobs, remote: s.remote, new7: s.new7, employers: s.emp.size, cat: s.cat, sen: s.sen, ats: s.ats, cities, top,
    cc: cc === 'REMOTE' ? s.cc : undefined,
    latest: s.latest.slice(0, LATEST).map(({ k, ...j }) => j),
  };
}
writeFileSync(join(dir, 'jobs-agg.json'), JSON.stringify({
  generatedAt: meta.generatedAt, since7,
  global: { jobs: glob.jobs, remote: glob.remote, new7: glob.new7, employers: glob.employers.size, countries: cstat.size - (cstat.has('REMOTE') ? 1 : 0), cat: glob.cat, sen: glob.sen },
  countries, countryNames,
}));
console.log(`jobs-agg: ${Object.keys(countries).length} countries with 300+ jobs`);
