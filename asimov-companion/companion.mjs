// Hermes drives the Asimov browser companion over CDP.
// Usage: node companion.mjs status|state|say|pose|move|ledger [args...]
const PORT = Number(process.env.CDP_PORT || 9333);
const [cmd, ...args] = process.argv.slice(2);

const tabs = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const page = tabs.find(t => t.type === 'page' && t.url.includes('8161'))
          || tabs.find(t => t.type === 'page');
if (!page) { console.log(JSON.stringify({ok:false, reason:'no page'})); process.exit(1); }

const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0; const pending = new Map();
const send = (m, p={}) => new Promise((res, rej) => {
  const n = ++id; pending.set(n, {res, rej});
  ws.send(JSON.stringify({id:n, method:m, params:p}));
});
ws.onmessage = e => { const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { const q = pending.get(m.id); pending.delete(m.id);
    m.error ? q.rej(new Error(JSON.stringify(m.error))) : q.res(m.result); } };
await new Promise(r => ws.onopen = r);
await send('Runtime.enable');

const J = JSON.stringify;
let expr;
switch (cmd) {
  case 'status': expr = 'window.asimov.status()'; break;
  case 'state':  expr = `window.asimov.setState(${J(args[0]||'IDLE')}, ${J(args[1]||null)})`; break;
  case 'say':    expr = `window.asimov.say(${J(args)})`; break;
  case 'pose':   expr = `window.asimov.pose(${Number(args[0]||0)})`; break;
  case 'move':   expr = 'window.asimov.move()'; break;
  case 'ledger': expr = 'window.asimov.ledger()'; break;
  case 'live':   expr = `(()=>{window.asimov._live=${args[0]!=='off'};return {live:window.asimov._live};})()`; break;
  default:       expr = 'window.asimov.status()';
}
const r = await send('Runtime.evaluate',
  {expression: `JSON.stringify(${expr})`, returnByValue: true, awaitPromise: true});
const v = r.result?.value;
try { console.log(J(JSON.parse(v), null, 2)); }
catch { console.log(v ?? J(r)); }
ws.close(); process.exit(0);
