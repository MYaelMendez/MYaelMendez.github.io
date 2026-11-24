// CDP capture: drive __renderFrame(i,total) and screenshot the 720x1280 stage.
// Chrome must be launched with --force_high_performance_gpu so ANGLE/D3D11
// selects the RTX rather than the Intel iGPU.
import fs from 'node:fs';
import path from 'node:path';

const PORT = Number(process.env.CDP_PORT || 9333);
const URL_ = process.env.SCENE_URL || 'http://127.0.0.1:8161/index.html';
const OUT = process.env.FRAMES_DIR || './frames';
const TOTAL = Number(process.env.FRAMES || 240);
const START = Number(process.env.START_FRAME || 0);

fs.mkdirSync(OUT, {recursive: true});

const tabs = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
let page = tabs.find(t => t.type === 'page');
if (!page) {
  page = await (await fetch(`http://127.0.0.1:${PORT}/json/new?${encodeURIComponent(URL_)}`)).json();
}
const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0;
const pending = new Map();
function send(method, params = {}) {
  return new Promise((res, rej) => {
    const n = ++id;
    pending.set(n, {res, rej});
    ws.send(JSON.stringify({id: n, method, params}));
  });
}
ws.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) {
    const {res, rej} = pending.get(m.id);
    pending.delete(m.id);
    m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
  }
};
await new Promise(r => ws.onopen = r);

await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride',
  {width: 720, height: 1280, deviceScaleFactor: 1, mobile: false});
await send('Page.navigate', {url: URL_});
await new Promise(r => setTimeout(r, 3500));

// wait for the meshes
for (let i = 0; i < 60; i++) {
  const r = await send('Runtime.evaluate',
    {expression: 'window.__ready === true', returnByValue: true});
  if (r.result?.value === true) break;
  await new Promise(r => setTimeout(r, 500));
}
const info = await send('Runtime.evaluate',
  {expression: 'JSON.stringify(window.__info ? window.__info() : {})', returnByValue: true});
console.log('  scene:', info.result?.value);

const t0 = Date.now();
for (let i = START; i < START + TOTAL; i++) {
  await send('Runtime.evaluate',
    {expression: `window.__renderFrame(${i}, ${TOTAL})`, returnByValue: true});
  const shot = await send('Page.captureScreenshot',
    {format: 'png', clip: {x: 0, y: 0, width: 720, height: 1280, scale: 1},
     captureBeyondViewport: false});
  fs.writeFileSync(path.join(OUT, `f${String(i).padStart(5, '0')}.png`),
                   Buffer.from(shot.data, 'base64'));
  if ((i - START) % 48 === 0) console.log(`  ${i - START}/${TOTAL}`);
}
const el = (Date.now() - t0) / 1000;
console.log(`  ${TOTAL} frames in ${el.toFixed(1)}s  (${(el / TOTAL * 1000).toFixed(0)} ms/frame)`);
fs.writeFileSync(path.join(OUT, '..', 'capture.json'),
  JSON.stringify({frames: TOTAL, seconds: el, ms_per_frame: el / TOTAL * 1000}, null, 2));
ws.close();
process.exit(0);
