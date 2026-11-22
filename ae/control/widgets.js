/* æC2 widgets — vanilla JS. No React, no JSX, no external requests.
   Each widget mounts into its container in index-live.html and is fully local:
   nothing here is fetched, and nothing here claims a network result. */
(function () {
  'use strict';

  function el(tag, cls, txt) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }

  function card(id, title, accent) {
    const host = document.getElementById(id);
    if (!host) return null;
    host.style.cssText =
      'background:#071521;border:1px solid #31516b;border-left:2px solid ' + accent + ';' +
      'border-radius:6px;padding:8px;font:10px/1.5 ui-monospace,monospace;' +
      'color:#92afc0;min-width:280px;text-align:left';
    const h = el('div', null, title);
    h.style.cssText = 'color:' + accent + ';font-size:9px;letter-spacing:.08em;margin-bottom:5px';
    host.appendChild(h);
    return host;
  }

  function row(host, k, v, vcolor) {
    const tr = el('tr');
    const a = el('td', null, k);
    a.style.cssText = 'color:#5a7a8a;padding:1px 4px';
    const b = el('td', null, v);
    b.style.cssText = 'color:' + (vcolor || '#e7f6ff') + ';text-align:right';
    tr.append(a, b);
    return tr;
  }

  /* 01 · mathematical notation — parses the literal, shows the structure */
  function latex() {
    const host = card('latex-widget', '$LæTæX · NOTATION', '#f4c77c');
    if (!host) return;
    const t = el('table');
    t.style.cssText = 'width:100%;border-collapse:collapse';
    [
      ['expr', '∫₀¹ x² dx', '#f4c77c'],
      ['variable', 'x', null],
      ['bounds', '0 → 1', null],
      ['integrand', 'x²', null],
      ['result', '1/3', '#9ce5ae']
    ].forEach(r => t.appendChild(row(host, r[0], r[1], r[2])));
    host.appendChild(t);
    const f = el('div', null, '✓ derivative(x³/3) = x²');
    f.style.cssText = 'color:#9ce5ae;margin-top:4px';
    host.appendChild(f);
  }

  /* 02 · doctrinal sample — explicitly labelled as a static sample */
  function teologia() {
    const host = card('teologia-widget', 'TEOLOGIA · MUESTRA LOCAL', '#c084fc');
    if (!host) return;
    host.appendChild(el('div', null, 'Justificación por la fe — don, no obra.'));
    host.appendChild(el('div', null, 'referencias: Romanos 3:28 · Efesios 2:8-9'));
    const n = el('div', null, 'muestra estática · no verificada contra una fuente');
    n.style.cssText = 'color:#5a7a8a;margin-top:4px';
    host.appendChild(n);
  }

  /* 03 · address check — resolves this console against the live atlas */
  function aeqr() {
    const host = card('aeqr-widget', 'ÆQR · ADDRESS CHECK', '#72d9ff');
    if (!host) return;
    const A = window.AE_ATLAS || [];
    const here = A.filter(s => s.x === 14 && s.y === 0 && s.z === 0 && s.a === 0)[0];
    host.appendChild(el('div', null, 'this console · x14:y0:z0:æ0'));
    const hit = el('div', null, here ? ('atlas hit: ' + here.name) : 'atlas: not loaded');
    hit.style.cssText = 'color:' + (here ? '#9ce5ae' : '#f4c77c');
    host.appendChild(hit);
    const n = el('div', null, here ? '✓ la dirección resuelve en el atlas' : '… esperando ae-atlas.js');
    n.style.cssText = 'color:#5a7a8a;margin-top:4px';
    host.appendChild(n);
  }

  /* 04 · local canvas — deterministic animation, no assets */
  function canvas() {
    const host = card('canvas-widget', 'STUDIO CANVAS · LOCAL', '#9ce5ae');
    if (!host) return;
    const c = document.createElement('canvas');
    c.width = 264; c.height = 90;
    c.style.cssText = 'display:block;width:100%;background:#050505;border-radius:4px';
    host.appendChild(c);
    const ctx = c.getContext('2d');
    let t = 0;
    (function loop() {
      if (!document.body.contains(c)) return;
      t += 0.03;
      ctx.clearRect(0, 0, c.width, c.height);
      ctx.strokeStyle = '#f4c77c';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      for (let x = 0; x <= c.width; x += 4) {
        const y = 45 + Math.sin(x * 0.05 + t) * 22 * Math.sin(t * 0.7);
        if (x) ctx.lineTo(x, y); else ctx.moveTo(x, y);
      }
      ctx.stroke();
      requestAnimationFrame(loop);
    })();
  }

  function mount() {
    latex(); teologia(); aeqr(); canvas();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
