/* Bulk phone number validation with libphonenumber-js (max metadata), fully offline in the browser. */
(function () {
  'use strict';
  var DV = window.DV;
  var MAX = 50;
  var form = document.getElementById('phone-form');
  var out = document.getElementById('phone-results');
  var status = document.getElementById('phone-status');
  var btnCsv = document.getElementById('phone-csv');
  var select = form.country;
  var lastRows = [];

  var TYPE = {
    MOBILE: 'mobile', FIXED_LINE: 'fixed line', FIXED_LINE_OR_MOBILE: 'fixed line or mobile', TOLL_FREE: 'toll free',
    PREMIUM_RATE: 'premium rate', SHARED_COST: 'shared cost', VOIP: 'VoIP', PERSONAL_NUMBER: 'personal number',
    PAGER: 'pager', UAN: 'universal access number', VOICEMAIL: 'voicemail',
  };
  var REASON = {
    TOO_SHORT: 'too short for its country', TOO_LONG: 'too long for its country', INVALID_LENGTH: 'length does not fit any number type',
    INVALID_COUNTRY: 'no country found: add a + code or choose the default country', NOT_A_NUMBER: 'not a phone number',
    INVALID_NUMBER: 'right length, but the range is not assigned',
  };

  function lib() { return window.libphonenumber; }

  function fillCountries() {
    var L = lib();
    if (!L) return;
    var guess = ((navigator.language || 'en-US').split('-')[1] || 'US').toUpperCase();
    var list = L.getCountries().map(function (c) { return { c: c, n: DV.countryName(c) || c }; });
    list.sort(function (a, b) { return a.n.localeCompare(b.n); });
    var html = '<option value="">None (numbers must start with + or 00)</option>';
    list.forEach(function (x) {
      html += '<option value="' + x.c + '"' + (x.c === guess ? ' selected' : '') + '>' + DV.esc(x.n) + ' (+' + L.getCountryCallingCode(x.c) + ')</option>';
    });
    select.innerHTML = html;
  }

  function check(input, country) {
    var L = lib();
    var text = input.replace(/^\s*00(?=[1-9])/, '+');
    var p = null;
    try { p = L.parsePhoneNumberFromString(text, country || undefined); } catch (e) { p = null; }
    var lenErr = null;
    try { lenErr = L.validatePhoneNumberLength(text, country || undefined) || null; } catch (e) { lenErr = 'NOT_A_NUMBER'; }
    if (!p) return { input: input, valid: false, reason: lenErr || 'NOT_A_NUMBER' };
    var valid = p.isValid();
    return {
      input: input, valid: valid, possible: p.isPossible(),
      e164: p.number, international: p.formatInternational(), national: p.formatNational(),
      type: valid ? p.getType() || null : null, country: p.country || null, code: p.countryCallingCode,
      ext: p.ext || null,
      reason: valid ? null : (lenErr || 'INVALID_NUMBER'),
    };
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.className = 'status';
    if (!lib()) { status.className = 'status err'; status.textContent = 'The phone number library did not load. Check that cdn.jsdelivr.net is not blocked and reload the page.'; return; }
    var lines = String(form.numbers.value || '').split(/[\n\r;]+/).map(function (x) { return x.trim(); }).filter(Boolean);
    if (!lines.length) { status.className = 'status err'; status.textContent = 'Paste at least one phone number, one per line.'; return; }
    var note = '';
    if (lines.length > MAX) { note = ' Only the first ' + MAX + ' numbers were checked.'; lines = lines.slice(0, MAX); }
    var country = select.value;
    var res = lines.map(function (x) { return check(x, country); });
    lastRows = [];
    var h = '<div class="tbl-wrap"><table class="tbl"><thead><tr><th class="num">#</th><th>Input</th><th>Result</th><th>E.164</th><th>International</th><th>National</th><th>Type</th><th>Country</th></tr></thead><tbody>';
    res.forEach(function (r, i) {
      var pill = r.valid ? '<span class="pill ok">valid</span>' : r.possible ? '<span class="pill warn">possible, not valid</span>' : '<span class="pill bad">invalid</span>';
      var reason = r.reason ? '<span class="sub">' + DV.esc(REASON[r.reason] || r.reason) + '</span>' : '';
      var cname = r.country ? DV.countryName(r.country) : '';
      h += '<tr><td class="num">' + (i + 1) + '</td><td>' + DV.esc(r.input) + '</td><td>' + pill + reason + '</td><td class="v">' + DV.esc(r.valid ? r.e164 : '') + '</td><td>' + DV.esc(r.valid ? r.international : '') + '</td><td>' + DV.esc(r.valid ? r.national : '') + '</td><td>' + DV.esc(r.type ? TYPE[r.type] || r.type : '') + '</td><td>' + DV.esc(cname) + (r.country ? ' <span class="hint">' + r.country + ' +' + r.code + '</span>' : '') + '</td></tr>';
      lastRows.push([i + 1, r.input, r.valid ? 'valid' : 'invalid', r.valid ? r.e164 : '', r.valid ? r.international : '', r.valid ? r.national : '', r.type || '', r.country || '', cname, r.code || '', r.ext || '', r.reason || '']);
    });
    out.innerHTML = h + '</tbody></table></div>';
    btnCsv.hidden = false;
    var ok = res.filter(function (r) { return r.valid; }).length;
    status.textContent = 'Done: ' + ok + ' of ' + res.length + ' numbers are valid. Checked in your browser; nothing was sent anywhere.' + note;
  });

  btnCsv.addEventListener('click', function () {
    DV.downloadCsv('phone-numbers.csv', ['position', 'input', 'result', 'e164', 'international', 'national', 'line_type', 'country_code', 'country', 'calling_code', 'extension', 'invalid_reason'], lastRows);
  });

  if (lib()) fillCountries();
  else window.addEventListener('load', function () {
    if (lib()) fillCountries();
    else { status.className = 'status err'; status.textContent = 'The phone number library did not load. Check that cdn.jsdelivr.net is not blocked and reload the page.'; }
  });
})();
