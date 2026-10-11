// Aggregates the public job index into one record per company and ATS.
//
// Input (download first, all three are public records of key-value store jletghbJMlxiI0vnm):
//   meta.json           generatedAt of the index
//   index.jsonl.gz      one row per open job: a = ATS, s = slug, c = company, l = locations, u = job URL, h = website
//   companies.json.gz   one row per registry token: a, s (token), c (name or null), n
// Output: ats-agg.json, consumed by build.py.
//
// Countries come from countriesOf() in the datova_slevarna repo (career-site-jobs/src/enrich.ts), bundled here
// with esbuild on the fly, so the website uses the same location parser as the Apify actors.
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
await esbuild.build({
  entryPoints: [join(repo, 'actors/career-site-jobs/src/enrich.ts')],
  bundle: true, format: 'esm', platform: 'node', outfile: out, logLevel: 'error',
});
const { countriesOf } = await import(pathToFileURL(out).href);

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
  for (const cc of countriesOf(locs)) { c.countries.set(cc, (c.countries.get(cc) ?? 0) + 1); cj[cc] = (cj[cc] ?? 0) + 1; }
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
const meta = JSON.parse(readFileSync(join(dir, 'meta.json'), 'utf8'));
writeFileSync(join(dir, 'ats-agg.json'), JSON.stringify({ generatedAt: meta.generatedAt, rows, companies: result, countryJobs, atsRemote, countryNames }));
console.log(`rows ${rows}, companies ${result.length}`);
