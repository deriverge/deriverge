/* Career site addresses and URL patterns of the applicant tracking systems in our data. */
(function () {
  'use strict';
  function enc(s) { return encodeURIComponent(s); }
  var ATS = {
    greenhouse: { name: 'Greenhouse', url: function (k) { return 'https://job-boards.greenhouse.io/' + enc(k); } },
    lever: { name: 'Lever', url: function (k) { return k.indexOf('eu:') === 0 ? 'https://jobs.eu.lever.co/' + enc(k.slice(3)) : 'https://jobs.lever.co/' + enc(k); } },
    workday: { name: 'Workday', url: function (k) { return 'https://' + k; } },
    ashby: { name: 'Ashby', url: function (k) { return 'https://jobs.ashbyhq.com/' + enc(k); } },
    bamboohr: { name: 'BambooHR', url: function (k) { return 'https://' + k + '.bamboohr.com/careers'; } },
    workable: { name: 'Workable', url: function (k) { return 'https://apply.workable.com/' + enc(k) + '/'; } },
    smartrecruiters: { name: 'SmartRecruiters', url: function (k) { return 'https://careers.smartrecruiters.com/' + enc(k); } },
    recruitee: { name: 'Recruitee', url: function (k) { return 'https://' + k + '.recruitee.com/'; } },
    teamtailor: { name: 'Teamtailor', url: function (k) { return 'https://' + k + '.teamtailor.com/jobs'; } },
    personio: { name: 'Personio', url: function (k) { return 'https://' + k + '.jobs.personio.de/'; } },
    breezy: { name: 'Breezy HR', url: function (k) { return 'https://' + k + '.breezy.hr/'; } },
    rippling: { name: 'Rippling', url: function (k) { return 'https://ats.rippling.com/' + enc(k) + '/jobs'; } },
    icims: { name: 'iCIMS', url: function (k) { return 'https://' + k + '/jobs'; } },
    oracle: {
      name: 'Oracle Recruiting Cloud',
      url: function (k) { var i = k.indexOf('/sites/'); return i < 0 ? 'https://' + k : 'https://' + k.slice(0, i) + '/hcmUI/CandidateExperience/en/sites/' + k.slice(i + 7); },
    },
  };

  /** Short label of a careers URL for tables: no scheme, no trailing slash. */
  function shortUrl(u) { return u.replace(/^https?:\/\//, '').replace(/\/$/, '').replace('/hcmUI/CandidateExperience/en/sites/', '/.../'); }

  /** Systems recognised from a careers or job link. `inData` marks the 14 systems this site lists companies for. */
  var DETECT = [
    { id: 'greenhouse', test: function (u) { return /(^|\.)greenhouse\.io$/.test(u.hostname) || /[?&]gh_jid=/.test(u.search); } },
    { id: 'lever', test: function (u) { return /(^|\.)lever\.co$/.test(u.hostname) || /[?&]lever-(source|origin)/.test(u.search); } },
    { id: 'workday', test: function (u) { return /\.myworkdayjobs\.com$|\.myworkdaysite\.com$|(^|\.)workday\.com$/.test(u.hostname); } },
    { id: 'ashby', test: function (u) { return /(^|\.)ashbyhq\.com$/.test(u.hostname) || /[?&]ashby_jid=/.test(u.search); } },
    { id: 'bamboohr', test: function (u) { return /\.bamboohr\.com$/.test(u.hostname); } },
    { id: 'workable', test: function (u) { return /(^|\.)workable\.com$/.test(u.hostname); } },
    { id: 'smartrecruiters', test: function (u) { return /(^|\.)smartrecruiters\.com$/.test(u.hostname); } },
    { id: 'recruitee', test: function (u) { return /\.recruitee\.com$/.test(u.hostname); } },
    { id: 'teamtailor', test: function (u) { return /\.teamtailor\.com$|(^|\.)teamtailor-cdn\.com$/.test(u.hostname); } },
    { id: 'personio', test: function (u) { return /\.jobs\.personio\.(de|com)$/.test(u.hostname); } },
    { id: 'breezy', test: function (u) { return /\.breezy\.hr$/.test(u.hostname); } },
    { id: 'rippling', test: function (u) { return /^ats\.rippling\.com$/.test(u.hostname); } },
    { id: 'icims', test: function (u) { return /\.icims\.com$/.test(u.hostname); } },
    { id: 'oracle', test: function (u) { return /\.oraclecloud\.com$/.test(u.hostname) && /CandidateExperience|hcmUI|hcmRestApi/i.test(u.pathname); } },
    { id: 'jobvite', name: 'Jobvite', test: function (u) { return /(^|\.)jobvite\.com$/.test(u.hostname); } },
    { id: 'taleo', name: 'Oracle Taleo', test: function (u) { return /(^|\.)taleo\.net$/.test(u.hostname); } },
    { id: 'successfactors', name: 'SAP SuccessFactors', test: function (u) { return /successfactors\.(com|eu)$|(^|\.)sapsf\.(com|eu)$/.test(u.hostname); } },
    { id: 'jazzhr', name: 'JazzHR', test: function (u) { return /(^|\.)applytojob\.com$/.test(u.hostname); } },
    { id: 'paylocity', name: 'Paylocity', test: function (u) { return /recruiting\.paylocity\.com$/.test(u.hostname); } },
    { id: 'ukg', name: 'UKG (UltiPro)', test: function (u) { return /(^|\.)ultipro\.com$|(^|\.)ukg\.net$/.test(u.hostname); } },
    { id: 'adp', name: 'ADP Workforce Now', test: function (u) { return /workforcenow\.adp\.com$|myjobs\.adp\.com$/.test(u.hostname); } },
    { id: 'dayforce', name: 'Dayforce', test: function (u) { return /dayforcehcm\.com$/.test(u.hostname); } },
    { id: 'pinpoint', name: 'Pinpoint', test: function (u) { return /\.pinpointhq\.com$/.test(u.hostname); } },
    { id: 'join', name: 'JOIN', test: function (u) { return /^join\.com$/.test(u.hostname); } },
  ];

  function detect(raw) {
    var s = String(raw || '').trim();
    if (!s) return null;
    var u;
    try { u = new URL(/^[a-z][a-z0-9+.-]*:\/\//i.test(s) ? s : 'https://' + s); } catch (e) { return null; }
    if (!/^[a-z0-9.-]+\.[a-z0-9-]{2,}$/i.test(u.hostname)) return null;
    u = { hostname: u.hostname.toLowerCase(), pathname: u.pathname, search: u.search };
    for (var i = 0; i < DETECT.length; i++) {
      if (DETECT[i].test(u)) {
        var id = DETECT[i].id;
        return { id: id, name: ATS[id] ? ATS[id].name : DETECT[i].name, inData: !!ATS[id] };
      }
    }
    return { id: null };
  }

  window.ATSX = { ATS: ATS, shortUrl: shortUrl, detect: detect };
})();
