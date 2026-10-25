#!/usr/bin/env python3
"""PrivateClient💸 · pc://pos server Witness (stdlib only).
Append-only, hash-chained receipts per shop. Paper money: no funds move here.
Agents may prepare; checkout.pay / socio.grant must come from a human (by != 'agent')."""
import json, hashlib, hmac, os, re, time, threading, base64, secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
DATA = os.environ.get('PCPOS_DATA', '/var/lib/pcpos')
ALLOWED = {'checkout.create', 'checkout.pay', 'refused', 'socio.grant'}
HUMAN_ONLY = {'checkout.pay', 'socio.grant'}
SHOP = re.compile(r'^instant-pos/[a-z0-9-]{1,40}$')
lock = threading.Lock()
RP_ID = os.environ.get('PCPOS_RP', 'privateclient.ai'); ORIGIN = 'https://' + RP_ID
challenges = {}  # challenge -> (shop, kind, expires)
def b64d(x): return base64.urlsafe_b64decode(x + '=' * (-len(x) % 4))
def b64e(b): return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def cbor(b, i=0):
    ib = b[i]; mt, ai = ib >> 5, ib & 31; i += 1
    if ai < 24: v = ai
    elif ai in (24, 25, 26, 27): n = 1 << (ai - 24); v = int.from_bytes(b[i:i+n], 'big'); i += n
    else: raise ValueError('cbor')
    if mt == 0: return v, i
    if mt == 1: return -1 - v, i
    if mt in (2, 3): d = b[i:i+v]; return (d if mt == 2 else d.decode()), i + v
    if mt == 4:
        a = []
        for _ in range(v): x, i = cbor(b, i); a.append(x)
        return a, i
    if mt == 5:
        m = {}
        for _ in range(v): k, i = cbor(b, i); x, i = cbor(b, i); m[k] = x
        return m, i
    if mt == 7: return {20: False, 21: True, 22: None}.get(ai), i
    raise ValueError('cbor')
def owner_file(shop): return os.path.join(DATA, shop.split('/')[1] + '.owner.json')
def secret():
    p = os.path.join(DATA, 'grant.key')
    if not os.path.exists(p):
        with open(p, 'wb') as f: f.write(secrets.token_bytes(32))
        os.chmod(p, 0o600)
    return open(p, 'rb').read()
def sign_grant(g):
    body = b64e(json.dumps(g, sort_keys=True, separators=(',', ':')).encode())
    return body + '.' + b64e(hmac.new(secret(), body.encode(), 'sha256').digest()[:16])
def check_grant(shop, tok):
    try:
        body, sig = tok.split('.')
        if not hmac.compare_digest(b64e(hmac.new(secret(), body.encode(), 'sha256').digest()[:16]), sig): return None, 'signature'
        g = json.loads(b64d(body))
    except Exception: return None, 'malformed'
    if g.get('shop') != shop: return None, 'other_shop'
    if time.time() * 1000 > g.get('x', 0): return None, 'expired'
    return g, None
def take_challenge(cdj, shop, kind):
    c = json.loads(cdj)
    ch = challenges.pop(c.get('challenge', ''), None)
    if not ch or ch[0] != shop or ch[1] != kind or ch[2] < time.time(): raise ValueError('challenge')
    if c.get('origin') != ORIGIN or c.get('type') != ('webauthn.create' if kind == 'reg' else 'webauthn.get'): raise ValueError('origin')
def check_authdata(ad):
    if ad[:32] != hashlib.sha256(RP_ID.encode()).digest(): raise ValueError('rp')
    if not ad[32] & 1 or not ad[32] & 4: raise ValueError('user_verification')
def append(shop, t, ev):
    with lock:
        c = read(shop); prev = c[-1]['hash'] if c else 'GENESIS'
        body = {'type': t, **ev, 'shop': shop, 'server_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'prev': prev}
        rec = {**body, 'hash': h(body)}
        with open(path(shop), 'a') as f: f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    return rec, len(c) + 1

def path(shop): return os.path.join(DATA, shop.split('/')[1] + '.jsonl')
def read(shop):
    try:
        with open(path(shop)) as f: return [json.loads(l) for l in f if l.strip()]
    except FileNotFoundError: return []
def h(body): return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
def verify(chain):
    prev = 'GENESIS'
    for r in chain:
        b = {k: v for k, v in r.items() if k != 'hash'}
        if b.get('prev') != prev or h(b) != r.get('hash'): return False
        prev = r['hash']
    return True
class H(BaseHTTPRequestHandler):
    server_version = 'pcpos/0.1'
    def log_message(self, *a): pass
    def send(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path.startswith('/pos/api/owner'):
            from urllib.parse import urlparse, parse_qs
            shop = (parse_qs(urlparse(self.path).query).get('shop') or [''])[0]
            if not SHOP.match(shop): return self.send(400, {'error': 'bad shop'})
            return self.send(200, {'passkey': os.path.exists(owner_file(shop))})
        if self.path.startswith('/pos/api/health'): return self.send(200, {'ok': True, 'service': 'pc://pos', 'money': 'paper'})
        if self.path.startswith('/pos/api/chain'):
            from urllib.parse import urlparse, parse_qs
            shop = (parse_qs(urlparse(self.path).query).get('shop') or [''])[0]
            if not SHOP.match(shop): return self.send(400, {'error': 'bad shop'})
            c = read(shop); return self.send(200, {'shop': shop, 'count': len(c), 'intact': verify(c), 'tail': c[-20:]})
        self.send(404, {'error': 'not found'})
    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0)
        if n <= 0 or n > 16384: return self.send(413, {'error': 'size'})
        try: req = json.loads(self.rfile.read(n))
        except Exception: return self.send(400, {'error': 'json'})
        shop = req.get('shop', '')
        if not SHOP.match(shop): return self.send(400, {'error': 'bad shop'})
        try: return self.route(shop, req)
        except (ValueError, KeyError, TypeError) as e:
            append(shop, 'refused', {'action': self.path.rsplit('/', 1)[-1], 'reason': 'passkey_' + str(e)[:40]})
            return self.send(403, {'error': str(e)})
    def route(self, shop, req):
        p = self.path
        if p == '/pos/api/witness':
            ev = req.get('ev') or {}
            if not isinstance(ev, dict): return self.send(400, {'error': 'bad ev'})
            t = ev.get('type')
            if t not in ALLOWED: t, ev = 'refused', {'action': str(t)[:40], 'reason': 'unknown_event (default deny)'}
            elif t == 'socio.grant': t, ev = 'refused', {'action': t, 'reason': 'socio.grant requires owner passkey'}
            elif t in HUMAN_ONLY and ev.get('by') == 'agent': ev = {'action': t, 'reason': f'{t} is human_only'}; t = 'refused'
            tok = ev.pop('socio_token', None)
            if t == 'checkout.pay' and ev.get('split'):
                g, why = check_grant(shop, tok or '')
                if not g: ev['split'] = None; ev['split_rejected'] = why
                else:
                    tot = float(ev.get('total') or 0)
                    ev['split'] = {'socio': g['n'], 'grant': g['gid'], 'rate_pct': g['r'], 'socio_usd': round(tot * g['r'] / 100, 2), 'store_usd': round(tot * (1 - g['r'] / 100), 2), 'verified': 'server'}
            ev = {k: v for k, v in ev.items() if k not in ('hash', 'prev', 'server_at', 'type')}
            rec, cnt = append(shop, t, ev)
            return self.send(200, {'ok': True, 'hash': rec['hash'], 'type': t, 'count': cnt, 'split': ev.get('split')})
        if p == '/pos/api/passkey/begin':
            kind = 'reg' if req.get('kind') == 'reg' else 'get'
            own = os.path.exists(owner_file(shop))
            if kind == 'reg':
                if own: return self.send(409, {'error': 'owner_exists'})
                tokf = owner_file(shop).replace('.owner.json', '.enroll')
                if not os.path.exists(tokf) or not hmac.compare_digest(open(tokf).read().strip(), str(req.get('enroll', ''))): raise ValueError('enroll_token')
            elif not own: return self.send(404, {'error': 'no_owner_passkey'})
            ch = b64e(secrets.token_bytes(32)); challenges[ch] = (shop, kind, time.time() + 120)
            out = {'challenge': ch, 'rpId': RP_ID}
            if kind == 'get': out['credId'] = json.load(open(owner_file(shop)))['cred']
            return self.send(200, out)
        if p == '/pos/api/passkey/register':
            tokf = owner_file(shop).replace('.owner.json', '.enroll')
            if os.path.exists(owner_file(shop)): return self.send(409, {'error': 'owner_exists'})
            if not os.path.exists(tokf) or not hmac.compare_digest(open(tokf).read().strip(), str(req.get('enroll', ''))): raise ValueError('enroll_token')
            take_challenge(b64d(req['clientDataJSON']), shop, 'reg')
            att, _ = cbor(b64d(req['attestationObject'])); ad = att['authData']; check_authdata(ad)
            if not ad[32] & 64: raise ValueError('no_credential')
            L = int.from_bytes(ad[53:55], 'big'); cred = ad[55:55+L]; key, _ = cbor(ad, 55 + L)
            if key.get(3) != -7 or key.get(-1) != 1: raise ValueError('alg_es256_only')
            json.dump({'cred': b64e(cred), 'x': b64e(key[-2]), 'y': b64e(key[-3]), 'name': str(req.get('name', 'dueño'))[:60]}, open(owner_file(shop), 'w'))
            os.remove(tokf)
            rec, cnt = append(shop, 'owner.passkey', {'by': 'owner', 'authority': 'æ2', 'cred': b64e(cred)[:12], 'alg': 'ES256'})
            return self.send(200, {'ok': True, 'count': cnt})
        if p == '/pos/api/socio/grant':
            from cryptography.hazmat.primitives.asymmetric import ec
            from cryptography.hazmat.primitives import hashes
            cdj = b64d(req['clientDataJSON']); ad = b64d(req['authenticatorData'])
            take_challenge(cdj, shop, 'get'); check_authdata(ad)
            o = json.load(open(owner_file(shop)))
            if req.get('credId') != o['cred']: raise ValueError('wrong_key')
            pub = ec.EllipticCurvePublicNumbers(int.from_bytes(b64d(o['x']), 'big'), int.from_bytes(b64d(o['y']), 'big'), ec.SECP256R1()).public_key()
            try: pub.verify(b64d(req['signature']), ad + hashlib.sha256(cdj).digest(), ec.ECDSA(hashes.SHA256()))
            except Exception: raise ValueError('signature')
            g0 = req.get('grant') or {}
            g = {'shop': shop, 'n': str(g0.get('n', 'Socio'))[:60], 'r': max(1, min(50, int(g0.get('r', 10)))), 'x': int(time.time() * 1000) + max(1, min(365, int(g0.get('d', 90)))) * 86400000, 'gid': secrets.token_hex(6)}
            tok = sign_grant(g)
            rec, cnt = append(shop, 'socio.grant', {'by': 'owner', 'authority': 'æ2', 'passkey': o['cred'][:12], 'socio': g['n'], 'rate_pct': g['r'], 'expires': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(g['x'] / 1000)), 'grant': g['gid']})
            return self.send(200, {'ok': True, 'token': tok, 'grant': g, 'count': cnt})
        if p == '/pos/api/socio/verify':
            g, why = check_grant(shop, str(req.get('token', '')))
            if not g:
                append(shop, 'refused', {'action': 'socio.attach', 'reason': why})
                return self.send(200, {'ok': False, 'reason': why})
            return self.send(200, {'ok': True, 'grant': g})
        return self.send(404, {'error': 'not found'})

if __name__ == '__main__':
    os.makedirs(DATA, exist_ok=True)
    ThreadingHTTPServer(('127.0.0.1', 8790), H).serve_forever()
