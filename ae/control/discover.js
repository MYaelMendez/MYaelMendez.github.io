/* æC2 discovery — the console as the estate's finding surface.
   Searches EVERY index that exists, not just the atlas:
     atlas   (ae-atlas.js)         addresses
     module  (codebase.json)       246 modules with paths + layers
     surface (qr_inventory.json)   html surfaces, agents, scenes, videos
     tool    (code-mode-tools.json)
     skill   (capability-mesh.json)
     manifest(capability-manifest.json / surface-manifest.json)
   Exposes window.aeFind(q) and window.aeIndexCounts() for other agents.
   Honest: it reports which indexes loaded and which failed. */
(function () {
  'use strict';

  var FILES = [
    { name: 'module', url: '../../codebase.json' },
    { name: 'surface', url: '../../qr_inventory.json' },
    { name: 'tool', url: '../../code-mode-tools.json' },
    { name: 'skill', url: '../../skill-guide/capability-mesh.json' },
    { name: 'manifest', url: '../../capability-manifest.json' },
    { name: 'mesh', url: '../../surface-manifest.json' }
  ];

  var cache = {}, failed = {}, index = [];

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function fetchJson(f) {
    if (cache[f.name] !== undefined) return Promise.resolve(cache[f.name]);
    return fetch(f.url, { cache: 'no-cache' })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (d) { cache[f.name] = d; return d; })
      .catch(function (e) { cache[f.name] = null; failed[f.name] = String(e); return null; });
  }

  function coord(s) { return 'x' + s.x + ':y' + s.y + ':z' + s.z + ':æ' + s.a; }

  function flatten() {
    var out = [];
    (window.AE_ATLAS || []).forEach(function (s) {
      out.push({ cat: 'atlas', name: s.name || '', coord: coord(s), path: s.path || '', desc: s.role || s.layer || '' });
    });

    var m = cache.module;
    if (m && m.modules) m.modules.forEach(function (x) {
      out.push({ cat: 'module', name: x.id || x.path, path: x.path || '', desc: x.desc || x.kind || '', layer: x.layer || '', address: x.address || '' });
    });

    var q = cache.surface;
    if (q) Object.keys(q).forEach(function (k) {
      (q[k] || []).forEach(function (v) {
        var n = typeof v === 'string' ? v : (v.name || v.path || JSON.stringify(v).slice(0, 40));
        out.push({ cat: k, name: n, path: typeof v === 'string' ? v : (v.path || ''), desc: '' });
      });
    });

    var t = cache.tool;
    if (t && t.capabilities) t.capabilities.forEach(function (x) {
      out.push({ cat: 'tool', name: x.name || '', desc: x.doc || x.mesh || '', path: '' });
    });

    var sk = cache.skill;
    if (sk && sk.skills) sk.skills.forEach(function (x) {
      out.push({ cat: 'skill', name: x.name || '', desc: x.desc || '', tier: x.tier || '', path: '' });
    });
    if (sk && sk.schemes) sk.schemes.forEach(function (x) {
      out.push({ cat: 'scheme', name: x.scheme || '', desc: x.desc || '', tier: x.tier || '', path: '' });
    });

    ['manifest', 'mesh'].forEach(function (k) {
      var d = cache[k];
      if (!d) return;
      var arr = d.capabilities || d.surfaces || [];
      arr.forEach(function (x) {
        out.push({
          cat: 'surface', name: x.name || x.id || '',
          path: x.url || '', desc: x.description || x.category || '',
          coord: x.address || ''
        });
      });
    });
    return out;
  }

  var ready = Promise.all(FILES.map(fetchJson)).then(function () {
    index = flatten();
    renderCounts();
  });
  window.aeReady = ready;

  function counts() {
    var by = {};
    index.forEach(function (x) { by[x.cat] = (by[x.cat] || 0) + 1; });
    return by;
  }

  function renderCounts() {
    var c = document.getElementById('discover-counts'), s = document.getElementById('discover-sub');
    var by = counts();
    var order = ['atlas', 'module', 'surface', 'skill', 'tool', 'scheme'];
    var known = order.filter(function (k) { return by[k]; }).map(function (k) { return k + ' ' + by[k]; });
    var extra = Object.keys(by).filter(function (k) { return order.indexOf(k) < 0; });
    if (c) c.textContent = known.join(' · ') + (extra.length ? ' · ' + extra.map(function (k) { return k + ' ' + by[k]; }).join(' · ') : '');
    if (s) {
      var ok = FILES.length - Object.keys(failed).length;
      s.textContent = index.length + ' resources · ' + ok + '/' + FILES.length + ' indexes' + (Object.keys(failed).length ? ' · ' + Object.keys(failed).join(', ') + ' FAILED' : '');
    }
  }

  function search(q) {
    q = (q || '').toLowerCase().trim();
    if (!q) return index.slice(0, 80);
    return index.filter(function (x) {
      return (x.name + ' ' + x.path + ' ' + x.desc + ' ' + (x.coord || '') + ' ' + (x.layer || '') +
        ' ' + (x.address || '') + ' ' + (x.tier || '') + ' ' + x.cat).toLowerCase().indexOf(q) >= 0;
    });
  }

  function render(q) {
    var box = document.getElementById('discover-results');
    if (!box) return;
    var hits = search(q);
    if (!index.length) { box.innerHTML = '<p class="empty">No indexes loaded.</p>'; return; }
    if (!hits.length) { box.innerHTML = '<p class="empty">0 matches for “' + esc(q) + '”.</p>'; return; }
    var show = hits.slice(0, 60);
    var h = show.map(function (x) {
      var link = x.path ? '<a href="../../' + esc(x.path.replace(/^\//, '')) + '" target="_blank" rel="noopener">↗</a>' : '';
      return '<div class="hit"><b>' + esc(x.name) + '</b><span class="tag">' + esc(x.cat) + '</span>' +
        (x.desc ? '<small>' + esc(String(x.desc).slice(0, 100)) + '</small>' : '') +
        (x.path ? '<code>' + esc(x.path) + '</code>' : '') + link + '</div>';
    }).join('');
    box.innerHTML = '<div class="hits">' + h + '</div>' +
      (hits.length > show.length ? '<p class="tiny">… ' + (hits.length - show.length) + ' more — refine the query.</p>' : '');
  }

  function mount() {
    var input = document.getElementById('discover-q');
    if (input) input.addEventListener('input', function () { render(input.value); });
    ready.then(function () { render(document.getElementById('discover-q').value); });
    window.aeFind = search;
    window.aeDiscover = render;
    window.aeIndexCounts = function () { return counts(); };
    window.aeIndexMeta = function () { return { total: index.length, counts: counts(), failed: Object.keys(failed) }; };
    if (!document.getElementById('discover-panel')) return;
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
