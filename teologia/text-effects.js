/* ═══════════════════════════════════════════════════════════════
   text-effects.js — deterministic, frame-driven text reveal engine.
   teologia.ai video scenes.

   WHY frame-driven: the capture harness (render.mjs) drives every
   frame via window.__renderFrame(i, total) then screenshots. CSS
   @keyframes do NOT advance frame-by-frame, so all text motion must
   be computed from `i`. Same i → same visual, every run.

   USAGE (inside a scene, after DOM is built):
     window.__renderFrame = function(i, total){
       ... your 3D updates ...
       TE.render(i, total);           // drives all .te-* elements
       renderer.render(scene, camera);
     };
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  // clamp helper
  function cl(v, a, b) { return v < a ? a : v > b ? b : v; }
  // 0→1 ease
  function smooth(t) { t = cl(t, 0, 1); return t * t * (3 - 2 * t); }
  function easeOutCubic(t) { t = cl(t, 0, 1); return 1 - Math.pow(1 - t, 3); }

  // Gather elements once (cached per scene build)
  let cache = null;
  function gather() {
    if (cache) return cache;
    cache = {
      glyph:   document.querySelector('.te-glyph'),
      title:   document.querySelector('.te-title'),
      tagline: document.querySelector('.te-tagline'),
      orn:     document.querySelector('.te-orn'),
      lines:   Array.from(document.querySelectorAll('.te-line')),
      ref:     document.querySelector('.te-ref'),
      badge:   document.querySelector('.te-badge'),
    };
    return cache;
  }

  // Frame budget: reveal completes over the first ~45% of the clip.
  // Staggered so each element lands a beat after the previous.
  const TE = {
    reset: function () { cache = null; },

    render: function (i, total) {
      const c = gather();
      const T = Math.max(1, total - 1);
      const t = i / T;                 // 0..1 overall
      const revealEnd = 0.45;          // finish the intro by 45%
      const p = cl(t / revealEnd, 0, 1);   // 0..1 intro progress

      // ── Glyph: scale-in + pop, then settle ──
      if (c.glyph) {
        const gp = smooth(p / 0.22);
        const s = 0.5 + 0.5 * gp + (1 - gp) * 0.06 * Math.sin(i * 0.4);
        c.glyph.style.opacity = gp.toFixed(3);
        c.glyph.style.transform = `scale(${s.toFixed(3)})`;
      }

      // ── Title: fade + letter-spacing contract + shimmer sweep ──
      if (c.title) {
        const tp = smooth((p - 0.08) / 0.24);
        c.title.style.opacity = tp.toFixed(3);
        const ls = 16 - 6 * tp;                    // 16px → 10px
        c.title.style.letterSpacing = ls.toFixed(2) + 'px';
        // shimmer position: sweep once across the reveal, then hold off-frame
        const sweep = 130 - 260 * easeOutCubic(cl((p - 0.15) / 0.5, 0, 1));
        c.title.style.setProperty('--te-shimmer', sweep.toFixed(1) + '%');
      }

      // ── Tagline ──
      if (c.tagline) {
        const gp = smooth((p - 0.20) / 0.20);
        c.tagline.style.opacity = gp.toFixed(3);
      }

      // ── Ornament: scaleX grow ──
      if (c.orn) {
        const op = smooth((p - 0.24) / 0.22);
        c.orn.style.opacity = op.toFixed(3);
        c.orn.style.transform = `scaleX(${op.toFixed(3)})`;
      }

      // ── Verse lines: staggered translateY + blur + opacity ──
      const n = c.lines.length || 1;
      const lineStart = 0.30;         // where lines begin
      const lineSpan = 0.30;          // total stagger window
      for (let k = 0; k < c.lines.length; k++) {
        const el = c.lines[k];
        if (el.classList.contains('te-gap')) continue;
        const start = lineStart + (k / n) * lineSpan;
        const lp = smooth((p - start) / 0.20);
        el.style.opacity = lp.toFixed(3);
        el.style.transform = `translateY(${(30 * (1 - lp)).toFixed(1)}px)`;
        el.style.filter = `blur(${(9 * (1 - lp)).toFixed(2)}px)`;
      }

      // ── Reference line ──
      if (c.ref) {
        const rp = smooth((p - 0.72) / 0.22);
        c.ref.style.opacity = rp.toFixed(3);
      }

      // ── Badge ──
      if (c.badge) {
        const bp = smooth((p - 0.80) / 0.20);
        c.badge.style.opacity = bp.toFixed(3);
      }
    },
  };

  window.TE = TE;
})();
