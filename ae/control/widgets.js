/* æC2 widgets — vanilla JS, fully integrated with the console.
   - theme-aware: every colour is a console token, so day / agentic_environments
     restyles them with the rest of the surface;
   - live: the address widget reads the console's CURRENT coordinate;
   - honest: nothing is fetched, and every card says what it is. */
(function () {
  'use strict';

  var PANEL = 'var(--panel,#071521)';
  var EDGE = 'var(--edge,#31516b)';
  var INK = 'var(--ink,#e7f6ff)';
  var MUTED = 'var(--muted,#92afc0)';
  var GOLD = 'var(--gold,#f4c77c)';
  var CYAN = 'var(--cyan,#72d9ff)';
  var GREEN = 'var(--green,#9ce5ae)';
  var PURPLE = '#c084fc';

  function el(tag, txt) {
    var e = document.createElement(tag);
    if (txt != null) e.textContent = txt;
    return e;
  }

  function card(id, title, accent) {
    var host = document.getElementById(id);
    if (!host) return null;
    host.style.cssText =
      'background:' + PANEL + ';border:1px solid ' + EDGE + ';border-left:2px solid ' + accent + ';' +
      'border-radius:6px;padding:8px;font:10px/1.5 ui-monospace,monospace;' +
      'color:' + MUTED + ';min-width:280px;text-align:left';
    var h = el('div', title);
    h.style.cssText = 'color:' + accent + ';font-size:9px;letter-spacing:.08em;margin-bottom:5px';
    host.appendChild(h);
    return host;
  }

  function row(k, v, vcolor) {
    var tr = el('tr');
    var a = el('td', k);
    a.style.cssText = 'color:' + MUTED + ';padding:1px 4px';
    var b = el('td', v);
    b.style.cssText = 'color:' + (vcolor || INK) + ';text-align:right';
    tr.appendChild(a); tr.appendChild(b);
    return tr;
  }

  /* 01 · mathematical notation — parses the literal, shows the structure */
  function latex() {
    const host = card('latex-widget', '$LæTæX · NOTATION', GOLD);
    if (!host) return;
    const t = el('table');
    t.style.cssText = 'width:100%;border-collapse:collapse';
    [
      ['expr', '∫₀¹ x² dx', GOLD],
      ['variable', 'x', null],
      ['bounds', '0 → 1', null],
      ['integrand', 'x²', null],
      ['result', '1/3', GREEN]
    ].forEach(r => t.appendChild(row(r[0], r[1], r[2])));
    host.appendChild(t);
    const f = el('div', null, '✓ derivative(x³/3) = x²');
    f.style.cssText = 'color:' + GREEN + ';margin-top:4px';
    host.appendChild(f);
  }

  /* 02 · doctrinal sample — explicitly labelled as a static sample */
  function teologia() {
    const host = card('teologia-widget', 'TEOLOGIA · MUESTRA LOCAL', PURPLE);
    if (!host) return;
    host.appendChild(el('div', null, 'Justificación por la fe — don, no obra.'));
    host.appendChild(el('div', null, 'referencias: Romanos 3:28 · Efesios 2:8-9'));
    const n = el('div', null, 'muestra estática · no verificada contra una fuente');
    n.style.cssText = 'color:' + MUTED + ';margin-top:4px';
    host.appendChild(n);
  }

  /* 03 · address check — resolves the console's LIVE coordinate in the atlas */
  function aeqr() {
    const host = card('aeqr-widget', 'ÆQR · ADDRESS CHECK', CYAN);
    if (!host) return;
    const line = el('div');
    const hit = el('div');
    hit.style.cssText = 'font-weight:700';
    const note = el('div');
    note.style.cssText = 'color:' + MUTED + ';margin-top:4px';
    host.appendChild(line); host.appendChild(hit); host.appendChild(note);

    function refresh() {
      const c = (window.aeCoord && window.aeCoord()) || { x: 14, y: 0, z: 0, a: 0 };
      const addr = 'x' + c.x + ':y' + c.y + ':z' + c.z + ':æ' + c.a;
      const A = window.AE_ATLAS || [];
      const s = A.filter(v => v.x === c.x && v.y === c.y && v.z === c.z && v.a === c.a)[0];
      line.textContent = 'this console · ' + addr;
      hit.textContent = s ? ('atlas hit: ' + s.name) : 'atlas: sin carga';
      hit.style.color = s ? GREEN : GOLD;
      note.textContent = s ? '✓ la dirección resuelve en el atlas' : '… esperando ae-atlas.js';
    }
    refresh();
    window.addEventListener('ae:coord', refresh);
    window.__aeRefreshAddress = refresh;
  }

  /* 04 · local canvas — deterministic, yields to reduced-motion and hidden tabs */
  function canvas() {
    const host = card('canvas-widget', 'STUDIO CANVAS · LOCAL', GREEN);
    if (!host) return;
    const c = document.createElement('canvas');
    c.width = 264; c.height = 90;
    c.style.cssText = 'display:block;width:100%;background:#050505;border-radius:4px';
    host.appendChild(c);
    const ctx = c.getContext('2d');
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let t = 0, raf = 0;

    function draw() {
      ctx.clearRect(0, 0, c.width, c.height);
      ctx.strokeStyle = '#f4c77c';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      for (let x = 0; x <= c.width; x += 4) {
        const y = 45 + Math.sin(x * 0.05 + t) * 22 * Math.sin(t * 0.7);
        if (x) ctx.lineTo(x, y); else ctx.moveTo(x, y);
      }
      ctx.stroke();
    }

    function loop() {
      t += 0.03;
      draw();
      raf = requestAnimationFrame(loop);
    }

    function sync() {
      const hidden = document.visibilityState === 'hidden';
      if (reduce || hidden) {
        if (raf) { cancelAnimationFrame(raf); raf = 0; }
        if (!reduce) draw();            // freeze on the current frame
      } else if (!raf) {
        raf = requestAnimationFrame(loop);
      }
    }

    document.addEventListener('visibilitychange', sync);
    if (reduce) draw(); else raf = requestAnimationFrame(loop);
  }

  function mount() {
    latex(); teologia(); aeqr(); canvas();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
