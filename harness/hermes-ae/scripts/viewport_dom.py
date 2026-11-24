"""Read-only DOM awareness for the hermes-agent Asimov viewport harness.

Connects to a Chrome DevTools Protocol target and projects the live page into a
small structured snapshot: viewport, landmarks, controls, headings, data-slot
hooks, focus, selection, and an optional selector probe. It never mutates the
page. Each read writes a HUMAN://ROOT receipt with a digest of the projection.
"""
import argparse, hashlib, importlib.util, json, sys, urllib.request
from pathlib import Path
import asyncio
import websockets

REPO_ROOT = Path(__file__).resolve().parents[1]

EXPRESSION = r'''(() => {
  const vis = el => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return {
      tag: el.tagName.toLowerCase(),
      role: el.getAttribute('role') || '',
      id: el.id || '',
      cls: (el.className && typeof el.className === 'string') ? el.className.slice(0, 120) : '',
      slot: el.getAttribute('data-slot') || '',
      text: (el.innerText || el.textContent || '').trim().slice(0, 180),
      href: el.getAttribute('href') || '',
      rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
      visible: !!(r.width && r.height) && s.display !== 'none' && s.visibility !== 'hidden' && Number(s.opacity) > 0
    };
  };
  const pick = (sel, n) => Array.from(document.querySelectorAll(sel)).slice(0, n).map(vis).filter(x => x.visible);
  const focus = document.activeElement && document.activeElement !== document.body ? vis(document.activeElement) : null;
  const selection = String(window.getSelection() || '').trim().slice(0, 200);
  const probe = window.__AE_DOM_PROBE__ ? vis(document.querySelector(window.__AE_DOM_PROBE__)) : null;
  return {
    title: document.title || '',
    url: location.href,
    viewport: {w: innerWidth, h: innerHeight, scrollX, scrollY},
    document: {w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight},
    focus,
    selection,
    landmarks: pick('header,nav,main,aside,footer,[role="main"],[role="navigation"]', 24),
    controls: pick('button,a[href],input,textarea,select,[role="button"]', 48),
    headings: pick('h1,h2,h3,h4', 24),
    slots: pick('[data-slot]', 48),
    probe
  };
})()'''


async def cdp_eval(ws_url, expression):
    async with websockets.connect(ws_url, max_size=4_000_000) as ws:
        await ws.send(json.dumps({
            'id': 1,
            'method': 'Runtime.evaluate',
            'params': {'expression': expression, 'returnByValue': True, 'awaitPromise': True},
        }))
        while True:
            msg = json.loads(await ws.recv())
            if msg.get('id') != 1:
                continue
            if 'error' in msg:
                raise RuntimeError(msg['error'])
            res = msg.get('result', {})
            if res.get('exceptionDetails'):
                raise RuntimeError(res['exceptionDetails'].get('text', 'evaluation failed'))
            return res.get('result', {}).get('value')


def discover(endpoint, match):
    url = endpoint.rstrip('/')
    if url.endswith('/json/list'):
        list_url = url
    else:
        list_url = url + '/json/list'
    with urllib.request.urlopen(list_url, timeout=5) as r:
        targets = json.loads(r.read().decode())
    pages = [t for t in targets if t.get('type') == 'page']
    if match:
        pages = [t for t in pages if match.lower() in (t.get('url', '') + ' ' + t.get('title', '')).lower()]
    if not pages:
        raise SystemExit(f'no page target found at {list_url} (match={match!r})')
    return pages[0]


def receipt(detail):
    spec = importlib.util.spec_from_file_location('ae', REPO_ROOT / '__init__.py')
    if spec is None or spec.loader is None:
        raise SystemExit('cannot load ae plugin')
    ae = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ae)
    return ae._receipt('VIEWPORT://DOM_AWARENESS', detail)


def main():
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    endpoint = args.get('endpoint') or 'http://127.0.0.1:9222'
    match = args.get('match', '')
    selector = args.get('selector', '')
    expr = f'window.__AE_DOM_PROBE__={json.dumps(selector)};{EXPRESSION}' if selector else EXPRESSION
    try:
        target = discover(endpoint, match)
        payload = asyncio.run(cdp_eval(target['webSocketDebuggerUrl'], expr))
        if not isinstance(payload, dict):
            raise RuntimeError('CDP returned a non-object projection')
        payload = {
            'title': payload.get('title', ''),
            'url': payload.get('url', ''),
            'viewport': payload.get('viewport', {}),
            'document': payload.get('document', {}),
            'focus': payload.get('focus'),
            'selection': payload.get('selection', ''),
            'landmarks': payload.get('landmarks', [])[:24],
            'controls': payload.get('controls', [])[:48],
            'headings': payload.get('headings', [])[:24],
            'slots': payload.get('slots', [])[:48],
            'probe': payload.get('probe'),
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        detail = {'authority': 'HUMAN://ROOT', 'target_url': payload['url'], 'digest': digest,
                  'counts': {'landmarks': len(payload['landmarks']), 'controls': len(payload['controls']),
                             'headings': len(payload['headings']), 'slots': len(payload['slots'])},
                  'selector': selector, 'read_only': True, 'success': True}
    except Exception as exc:
        payload = {'error': f'{type(exc).__name__}: {exc}'}
        digest = hashlib.sha256(payload['error'].encode()).hexdigest()
        detail = {'authority': 'HUMAN://ROOT', 'digest': digest, 'read_only': True,
                  'success': False, 'error': payload['error']}
    rec = receipt(detail)
    print(json.dumps({'success': detail['success'], 'target': payload.get('url'),
                      'endpoint': endpoint, 'digest': digest, 'dom': payload,
                      'receipt': rec['hash'], 'authority': 'HUMAN://ROOT'}))


if __name__ == '__main__':
    main()
