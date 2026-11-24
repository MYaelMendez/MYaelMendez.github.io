/* æ protocol — pet widget (the asimov-cad atlas).
   ONE renderer over pet/pet.json + picoasimov-atlas.webp, mounted by any window.
   Spec: https://myaelmendez.github.io/MECH-OS-BUILD-SPEC.md (S4.1)

       <div data-pet data-pet-label="asimov-cad"></div>

   Contract: same component, many windows. Reports its own live state in
   data-pet-state / data-pet-frames so a window never claims a pose it is not on.
   Source of truth for the atlas geometry is pet/pet.json (sha256 receipt there). */
(function () {
  'use strict';
  var STATES = ['idle', 'running-right', 'running-left', 'waving', 'jumping',
                'failed', 'waiting', 'running', 'review'];
  /* atlas geometry — 1536×1872 · 8 cols × 9 rows of 192×208 · 6 frames used */
  var ATLAS = { src: 'pet/picoasimov-atlas.webp', w: 1536, h: 1872, cw: 192, ch: 208, frames: 6 };

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function mount(el, opts) {
    if (!el) return null;
    opts = opts || {};
    var fps = opts.fps || 12;
    var state = 'idle', frame = 0, last = 0;

    el.classList.add('ae-pet');
    el.style.backgroundImage = 'url("' + ATLAS.src + '")';
    el.style.backgroundSize = ATLAS.w + 'px ' + ATLAS.h + 'px';
    el.style.width = ATLAS.cw + 'px';
    el.style.height = ATLAS.ch + 'px';
    el.setAttribute('role', 'img');
    el.setAttribute('aria-label', 'asimov-cad pet · ' + STATES.length + ' states');

    function rowOf(s) { var i = STATES.indexOf(s); return i < 0 ? 0 : i; }
    function draw() {
      el.style.backgroundPosition = (-frame * ATLAS.cw) + 'px ' + (-rowOf(state) * ATLAS.ch) + 'px';
    }
    function report() {
      el.setAttribute('data-pet-state', state);
      el.setAttribute('data-pet-frame', String(frame));
      el.setAttribute('data-pet-frames', String(ATLAS.frames));
    }
    function step(now) {
      if (now - last > 1000 / fps) { last = now; frame = (frame + 1) % ATLAS.frames; draw(); report(); }
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);

    function set(s) {
      if (STATES.indexOf(s) < 0) return false;
      state = s; frame = 0; draw(); report();
      if (opts.onChange) opts.onChange(s);
      return true;
    }
    el.addEventListener('click', function () { set('waving'); });
    el.tabIndex = 0;
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); set('waving'); }
    });

    /* an optional chip row: [data-pet-chips] with buttons carrying data-state */
    if (opts.chips) {
      opts.chips.addEventListener('click', function (e) {
        var b = e.target;
        while (b && b.tagName !== 'BUTTON' && b !== opts.chips) b = b.parentNode;
        if (b && b.getAttribute) set(b.getAttribute('data-state'));
      });
    }

    draw(); report();
    return { set: set, get: function () { return state; }, states: STATES };
  }

  function mountAll(scope) {
    var n = 0;
    (scope || document).querySelectorAll('[data-pet]').forEach(function (el) { mount(el); n++; });
    return { mounts: n };
  }

  window.aePetWidget = { mount: mount, mountAll: mountAll, states: STATES, atlas: ATLAS };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { mountAll() });
  } else { mountAll() }
})();
