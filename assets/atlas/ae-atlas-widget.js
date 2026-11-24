/* æ protocol — atlas widget.
   ONE renderer over window.AE_ATLAS (ae-atlas.js), mounted by any window.
   Spec: https://myaelmendez.github.io/MECH-OS-BUILD-SPEC.md (S4)

       <script src="ae-atlas.js"></script>
       <script src="assets/atlas/ae-atlas-widget.js"></script>
       <div id="atlas-a" data-atlas data-atlas-cat="media"></div>
       <div id="atlas-b" data-atlas data-atlas-limit="6" data-atlas-compact></div>

   Every instance reports its own count in its header, so a window never claims
   more addresses than it shows. No copy of the atlas body exists anywhere:
   this module is the only renderer. */
(function () {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function rows(list) {
    return list.map(function (a) {
      return '<li class="aw-row">' +
        '<span class="aw-name">' + esc(a.name) + '</span>' +
        '<span class="aw-url">' + esc(a.url) + '</span>' +
        (a.desc ? '<span class="aw-desc">' + esc(a.desc) + '</span>' : '') +
        '<span class="aw-cat">' + esc(a.cat || '') + '</span>' +
        '</li>';
    }).join('');
  }

  function render(el, opts) {
    var all = window.AE_ATLAS || [];
    var list = all.filter(function (a) {
      if (!opts.cat) return true;
      if (Array.isArray(opts.cat)) return opts.cat.indexOf(a.cat) >= 0;
      return a.cat === opts.cat;
    });
    var total = list.length;
    if (opts.limit && list.length > opts.limit) list = list.slice(0, opts.limit);
    el.setAttribute('data-atlas-count', String(total));
    el.setAttribute('data-atlas-shown', String(list.length));
    el.classList.add('ae-atlas');
    if (opts.compact) el.classList.add('ae-atlas-compact');
    el.innerHTML =
      '<div class="aw-head"><b>ATLAS</b><span class="aw-count">' +
      list.length + ' / ' + total + ' shown</span></div>' +
      '<ul class="aw-list">' + (list.length ? rows(list) :
        '<li class="aw-empty">no addresses match this lens</li>') + '</ul>';
    return { total: total, shown: list.length };
  }

  /* mount an element, or every [data-atlas] on the page */
  function mount(el, opts) {
    if (!el) return null;
    if (el instanceof Element && el.hasAttribute && el.hasAttribute('data-atlas')) {
      opts = opts || {};
      if (el.hasAttribute('data-atlas-cat')) opts.cat = el.getAttribute('data-atlas-cat');
      if (el.hasAttribute('data-atlas-limit')) opts.limit = parseInt(el.getAttribute('data-atlas-limit'), 10);
      if (el.hasAttribute('data-atlas-compact')) opts.compact = true;
    }
    return render(el, opts || {});
  }

  function mountAll(scope) {
    var n = 0, out = [];
    (scope || document).querySelectorAll('[data-atlas]').forEach(function (el) {
      out.push(mount(el)); n++;
    });
    return { mounts: n, counts: out };
  }

  window.aeAtlas = { mount: mount, mountAll: mountAll, count: function () { return (window.AE_ATLAS || []).length } };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { mountAll() });
  } else { mountAll() }
})();
