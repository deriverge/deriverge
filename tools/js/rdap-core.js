/* RDAP helpers shared by the WHOIS and availability tools. Registry servers come from the IANA bootstrap file. */
(function () {
  'use strict';
  var DV = window.DV;
  var BOOTSTRAP_URL = 'https://data.iana.org/rdap/dns.json';
  // Registry RDAP servers that work but are missing from the IANA file (verified, all send CORS headers).
  var KNOWN = {
    io: 'https://rdap.identitydigital.services/rdap/',
    ch: 'https://rdap.nic.ch/',
    li: 'https://rdap.nic.ch/',
    us: 'https://rdap.nic.us/',
    no: 'https://rdap.norid.no/',
    si: 'https://rdap.register.si/',
  };
  // Registries with RDAP that refuse requests from web pages (no CORS headers): checked through DNS instead.
  var NO_BROWSER = { de: 'DENIC' };
  // Common second-level registration suffixes, so www.shop.co.uk is checked as shop.co.uk.
  var SLD = ('co.uk org.uk me.uk ltd.uk plc.uk net.uk ac.uk gov.uk sch.uk com.au net.au org.au edu.au gov.au id.au ' +
    'com.br net.br org.br co.nz net.nz org.nz co.za org.za co.jp ne.jp or.jp ac.jp com.mx org.mx com.ar com.tr co.in ' +
    'net.in org.in firm.in com.sg com.hk com.cn net.cn org.cn co.kr com.tw com.my co.id co.il com.ua com.co com.pe ' +
    'com.ph com.vn com.pk com.ng com.eg com.sa co.th in.th com.es com.pt com.gr co.at or.at co.hu com.pl net.pl org.pl').split(' ');

  var bootstrap = null, loading = null;

  function loadBootstrap() {
    if (bootstrap) return Promise.resolve(bootstrap);
    if (loading) return loading;
    try {
      var cached = sessionStorage.getItem('dv-rdap-bootstrap');
      if (cached) { bootstrap = JSON.parse(cached); return Promise.resolve(bootstrap); }
    } catch (e) { /* storage unavailable */ }
    loading = DV.getJson(BOOTSTRAP_URL, { timeout: 15000 }).then(function (res) {
      loading = null;
      if (!res.ok || !res.json || !res.json.services) throw new Error('The IANA list of registry servers could not be loaded. Try again in a minute.');
      var map = {};
      res.json.services.forEach(function (svc) {
        var urls = svc[1] || [];
        var base = urls.filter(function (u) { return /^https:/.test(u); })[0] || urls[0];
        if (!base) return;
        if (!/\/$/.test(base)) base += '/';
        (svc[0] || []).forEach(function (tld) { map[String(tld).toLowerCase()] = base; });
      });
      bootstrap = map;
      try { sessionStorage.setItem('dv-rdap-bootstrap', JSON.stringify(map)); } catch (e) { /* ignore */ }
      return map;
    });
    return loading;
  }

  function tldOf(domain) { return domain.split('.').pop(); }

  /** Registered domain from a host name: www.shop.example.co.uk -> example.co.uk. */
  function registrable(host) {
    var labels = host.split('.');
    if (labels.length <= 2) return host;
    var last2 = labels.slice(-2).join('.');
    if (SLD.indexOf(last2) >= 0) return labels.slice(-3).join('.');
    return last2;
  }

  function serverFor(domain) {
    var tld = tldOf(domain);
    if (NO_BROWSER[tld]) return { blocked: NO_BROWSER[tld] };
    var base = KNOWN[tld] || (bootstrap && bootstrap[tld]);
    return base ? { base: base } : { none: true };
  }

  /** One RDAP lookup. Resolves { state: 'registered' | 'free' | 'nordap' | 'blocked' | 'error', data, server, message }. */
  function lookup(domain) {
    var srv = serverFor(domain);
    if (srv.blocked) return Promise.resolve({ state: 'blocked', message: 'The .' + tldOf(domain) + ' registry (' + srv.blocked + ') does not allow lookups from a web page.' });
    if (srv.none) return Promise.resolve({ state: 'nordap', message: 'The .' + tldOf(domain) + ' registry has no public RDAP server.' });
    var url = srv.base + 'domain/' + encodeURIComponent(domain);
    return DV.getJson(url, { headers: { accept: 'application/rdap+json' }, timeout: 15000 }).then(function (res) {
      var host = srv.base.replace(/^https?:\/\//, '').split('/')[0];
      if (res.status === 200 && res.json) return { state: 'registered', data: res.json, server: host };
      if (res.status === 404) return { state: 'free', server: host };
      if (res.status === 429) return { state: 'error', server: host, message: 'The registry is rate limiting requests (HTTP 429). Wait a minute and try again.' };
      if (res.status === 0) return { state: 'error', server: host, message: res.error === 'timeout' ? 'The registry did not answer within 15 seconds.' : 'The registry could not be reached from this browser.' };
      return { state: 'error', server: host, message: 'The registry answered HTTP ' + res.status + '.' };
    });
  }

  function vcardField(entity, key) {
    var arr = entity && entity.vcardArray && entity.vcardArray[1];
    if (!arr) return null;
    for (var i = 0; i < arr.length; i++) if (arr[i][0] === key) return arr[i][3];
    return null;
  }

  function findRole(entities, role) {
    for (var i = 0; i < (entities || []).length; i++) {
      var e = entities[i];
      if ((e.roles || []).indexOf(role) >= 0) return e;
    }
    return null;
  }

  /**
   * The public registry facts of an RDAP domain object. Registrant, admin, tech and billing contacts are never read,
   * so no personal data reaches the page even when a registry publishes it.
   */
  function summarize(d) {
    var ev = {};
    (d.events || []).forEach(function (e) { if (e.eventAction && e.eventDate && !ev[e.eventAction]) ev[e.eventAction] = e.eventDate; });
    var reg = findRole(d.entities, 'registrar');
    var ianaId = null;
    if (reg) (reg.publicIds || []).forEach(function (p) { if (/iana/i.test(p.type || '')) ianaId = p.identifier; });
    var regUrl = reg ? vcardField(reg, 'url') : null;
    if (reg && !regUrl) (reg.links || []).forEach(function (l) { if (!regUrl && l.rel === 'about' && /^https?:/.test(l.href || '')) regUrl = l.href; });
    var ns = (d.nameservers || []).map(function (n) { return String(n.ldhName || n.unicodeName || '').toLowerCase().replace(/\.$/, ''); }).filter(Boolean);
    var dnssec = d.secureDNS ? (d.secureDNS.delegationSigned === true ? 'signed' : d.secureDNS.delegationSigned === false ? 'unsigned' : null) : null;
    return {
      name: String(d.ldhName || '').toLowerCase(),
      registrar: reg ? (vcardField(reg, 'fn') || (reg.handle && !/^\d+$/.test(reg.handle) ? reg.handle : null)) : null,
      registrarId: ianaId,
      registrarUrl: regUrl,
      created: ev.registration || null,
      updated: ev['last changed'] || null,
      expires: ev.expiration || null,
      status: (d.status || []).slice(),
      nameservers: ns,
      dnssec: dnssec,
    };
  }

  function age(iso) {
    if (!iso) return '';
    var t = new Date(iso);
    if (isNaN(t)) return '';
    var days = Math.floor((Date.now() - t.getTime()) / 86400000);
    if (days < 0) return '';
    var y = Math.floor(days / 365.25);
    return y >= 1 ? y + ' year' + (y === 1 ? '' : 's') + ', ' + Math.floor(days - y * 365.25) + ' days' : days + ' days';
  }

  function daysUntil(iso) {
    if (!iso) return null;
    var t = new Date(iso);
    return isNaN(t) ? null : Math.ceil((t.getTime() - Date.now()) / 86400000);
  }

  window.RDAP = { loadBootstrap: loadBootstrap, lookup: lookup, summarize: summarize, registrable: registrable, serverFor: serverFor, tldOf: tldOf, age: age, daysUntil: daysUntil, KNOWN: KNOWN, NO_BROWSER: NO_BROWSER };
})();
