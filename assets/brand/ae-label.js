/* æ protocol — the white-label standard.
   ONE module, every surface. Include with:
       <script src="assets/brand/ae-label.js"></script>
   Contract: https://myaelmendez.github.io/AE-PROTOCOL.md

   - persists to localStorage['ae-label-v1']
   - applies --gold / --gold-hi from the visitor's accent
   - fills any [data-label-glyph] / [data-label-name] slot on the page
   - never touches facts, receipts or numbers; styles only
   - an empty glyph resets to the surface's own demo face. Nothing defaults to æ. */
(function () {
  'use strict';
  var KEY = 'ae-label-v1';

  function get() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null') } catch (e) { return null }
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function each(sel, fn) {
    var n = document.querySelectorAll(sel), i;
    for (i = 0; i < n.length; i++) fn(n[i]);
  }

  function apply(l) {
    var root = document.documentElement;
    if (!l || !l.glyph) { reset(); return false }
    try { localStorage.setItem(KEY, JSON.stringify(l)) } catch (e) {}
    root.style.setProperty('--gold', l.accent || '#D4AF37');
    root.style.setProperty('--gold-hi', l.accent || '#D4AF37');
    /* surfaces may also define their own accent variable — follow it if present */
    each(':root, :root[data-theme]', function () {});
    /* surfaces opt in to accent-following by declaring these variables */
    if (getComputedStyle(root).getPropertyValue('--secondary-color').trim()) {
      root.style.setProperty('--secondary-color', l.accent || '#D4AF37');
    }
    each('[data-label-glyph]', function (el) { el.textContent = l.glyph });
    each('[data-label-name]', function (el) { el.textContent = l.name || '' });
    document.body.setAttribute('data-labelled', '1');
    document.body.setAttribute('data-label-glyph', esc(l.glyph));
    document.body.setAttribute('data-label-name', esc(l.name || ''));
    return true;
  }

  function reset() {
    var root = document.documentElement;
    try { localStorage.removeItem(KEY) } catch (e) {}
    root.style.removeProperty('--gold');
    root.style.removeProperty('--gold-hi');
    each('[data-label-glyph]', function (el) { el.textContent = '' });
    each('[data-label-name]', function (el) { el.textContent = '' });
    document.body.removeAttribute('data-labelled');
    document.body.removeAttribute('data-label-glyph');
    document.body.removeAttribute('data-label-name');
  }

  function panel(mount) {
    /* a minimal, dependency-free control. Returns the created element. */
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'ae-label-btn';
    b.setAttribute('title', 'white-label this surface — æ protocol standard');
    b.textContent = '◈ LABEL';
    b.addEventListener('click', function () {
      var cur = get() || {}, g = '', n = '';
      g = window.prompt('your glyph (leave empty to restore)', cur.glyph || '');
      if (g === null) return;
      n = window.prompt('your name', cur.name || '') || '';
      if (!g) { reset() } else { apply({ glyph: g, name: n, accent: cur.accent || '#D4AF37' }) }
      document.dispatchEvent(new CustomEvent('ae-label'));
    });
    if (mount) mount.appendChild(b);
    return b;
  }

  window.aeLabel = { apply: apply, reset: reset, get: get, panel: panel, key: KEY };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { apply(get()) });
  } else { apply(get()) }
})();
