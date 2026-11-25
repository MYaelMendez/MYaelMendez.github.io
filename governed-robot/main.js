// >_æ://GOVERNED_ROBOT — 9:16 governed robot program
// One viewport: the semicircular face. Everything else is command chrome.
import { Authority } from './modules/authority.js';
import { MaskEngine, MODES, STATES, STATE_COLORS, FW, FH } from './modules/mask.js';
import { RobotScene } from './modules/scene.js';

const VERSION = '2.0.0';
const PROGRAMS = ['MIRROR', 'FACE', 'TEXT', 'OFF'];
const $ = id => document.getElementById(id);
const bootEl = $('boot'), logEl = $('bootlog');
const boot = line => { if (!logEl) return; logEl.textContent += line + '\n'; logEl.scrollTop = logEl.scrollHeight; };
const fail = err => { boot('ERROR ' + (err?.stack || err)); console.error('[governed-robot]', err); };

async function init() {
  boot('>_æ://GOVERNED_ROBOT v' + VERSION);
  boot('chain HUMAN://ROOT → æ://POLICY → robot://BODY → RECEIPT');
  boot('authority is not transferable · the face is the viewport');

  const gl = $('gl');
  const maskCanvas = document.createElement('canvas');
  maskCanvas.width = FW; maskCanvas.height = FH;
  const authority = new Authority();
  const mask = new MaskEngine(maskCanvas);
  mask.setMode('MIRROR'); mask.setState('IDLE');
  const scene = new RobotScene(gl);

  await scene.load('./assets/gltf/asimov-web.glb');
  scene.setMaskCanvas(maskCanvas);
  scene.resize();

  // command deck
  const progBox = $('programs');
  for (const p of PROGRAMS) {
    const b = document.createElement('button');
    b.className = 'program' + (p === 'MIRROR' ? ' on' : '');
    b.textContent = p; b.dataset.prog = p;
    b.onclick = async () => {
      mask.setMode(p);
      progBox.querySelectorAll('.program').forEach(x => x.classList.toggle('on', x.dataset.prog === p));
      $('hProg').textContent = p;
      const r = await authority.issue('mask.setProgram', { program: p, actor: 'wætz' });
      $('hReceipt').textContent = '#' + r.seq + ' ' + r.hash.slice(0, 16);
    };
    progBox.appendChild(b);
  }

  let si = 0;
  $('stateDot').style.background = STATE_COLORS.IDLE;
  $('stateDot').style.boxShadow = '0 0 8px ' + STATE_COLORS.IDLE;
  const stateEl = $('hState');
  const stateBar = stateEl.parentElement;
  stateBar.style.cursor = 'pointer';
  stateBar.title = 'cycle governed state';
  stateBar.onclick = async () => {
    si = (si + 1) % STATES.length;
    const s = STATES[si];
    mask.setState(s);
    stateEl.textContent = s;
    $('stateDot').style.background = STATE_COLORS[s];
    $('stateDot').style.boxShadow = '0 0 8px ' + STATE_COLORS[s];
    const r = await authority.issue('mask.setState', { state: s, actor: 'wætz' });
    $('hReceipt').textContent = '#' + r.seq + ' ' + r.hash.slice(0, 16);
  };

  // orbit + distance are direct manipulation, receipted once per gesture
  let drag = null;
  gl.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY }; gl.setPointerCapture(e.pointerId); });
  gl.addEventListener('pointermove', e => {
    if (!drag) return;
    scene.az += (e.clientX - drag.x) * 0.008;
    scene.el = Math.max(-1.1, Math.min(1.35, scene.el + (e.clientY - drag.y) * 0.006));
    drag = { x: e.clientX, y: e.clientY };
  });
  gl.addEventListener('pointerup', async () => {
    if (!drag) return; drag = null;
    const r = await authority.issue('viewport.orbit', { az: +scene.az.toFixed(3), el: +scene.el.toFixed(3), actor: 'wætz' });
    $('hReceipt').textContent = '#' + r.seq + ' ' + r.hash.slice(0, 16);
  });
  gl.addEventListener('wheel', e => {
    e.preventDefault();
    scene.setDistance(scene.getDistance() + Math.sign(e.deltaY) * 0.02);
  }, { passive: false });

  window.__ae = { scene, mask, authority, version: VERSION };

  const raf = (now) => {
    const dt = Math.min(0.1, Math.max(0.001, scene.clock.getDelta()));
    try { mask.draw(now); scene.update(now / 1000, dt); }
    catch (e) { boot('LOOP ' + (e?.message || e)); }
    requestAnimationFrame(raf);
  };
  requestAnimationFrame(raf);

  const r0 = await authority.issue('boot', { version: VERSION, program: 'MIRROR', state: 'IDLE', actor: 'wætz' });
  $('hReceipt').textContent = '#' + r0.seq + ' ' + r0.hash.slice(0, 16);
  boot('receipt #' + r0.seq + ' ' + r0.hash.slice(0, 12));
  boot('ready · HUMAN://ROOT in command');
  setTimeout(() => { bootEl.classList.add('done'); setTimeout(() => bootEl.remove(), 500); }, 900);
}

init().catch(fail);
