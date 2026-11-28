#!/usr/bin/env python3
"""PrivateClient pc://key · owner passkey (Face ID) + væult (end-to-end encrypted).
The server stores only a public key and ciphertext. Secrets are encrypted on the device with a key
derived from the passkey's WebAuthn PRF output; the server can never decrypt them."""
import json, hashlib, hmac, os, re, time, threading, base64, secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
DATA = os.environ.get('PCKEY_DATA', '/var/lib/pckey'); RP_ID = os.environ.get('PCKEY_RP', 'privateclient.ai'); ORIGIN = 'https://' + RP_ID
lock = threading.Lock(); challenges = {}; sessions = {}
NAME = re.compile(r'^[A-Za-z0-9 ._:@/-]{1,64}$')
def b64d(x): return base64.urlsafe_b64decode(x + '=' * (-len(x) % 4))
def b64e(b): return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def P(n): return os.path.join(DATA, n)
def jload(n, d):
    try: return json.load(open(P(n)))
    except FileNotFoundError: return d
def jsave(n, o):
    t = P(n + '.tmp'); json.dump(o, open(t, 'w')); os.chmod(t, 0o600); os.replace(t, P(n))
def h(b): return hashlib.sha256(json.dumps(b, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
def witness(t, ev):
    with lock:
        c = jload('chain.json', []); prev = c[-1]['hash'] if c else 'GENESIS'
        b = {'type': t, **ev, 'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'prev': prev}; c.append({**b, 'hash': h(b)}); jsave('chain.json', c)
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
def take(cdj, kind):
    c = json.loads(cdj); ch = challenges.pop(c.get('challenge', ''), None)
    if not ch or ch[0] != kind or ch[1] < time.time(): raise ValueError('challenge')
    if c.get('origin') != ORIGIN or c.get('type') != ('webauthn.create' if kind == 'reg' else 'webauthn.get'): raise ValueError('origin')
def authdata(ad):
    if ad[:32] != hashlib.sha256(RP_ID.encode()).digest(): raise ValueError('rp')
    if not ad[32] & 1 or not ad[32] & 4: raise ValueError('user_verification')
class H(BaseHTTPRequestHandler):
    server_version = 'pckey/0.1'
    def log_message(self, *a): pass
    def send(self, code, obj, cookie=None):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json; charset=utf-8'); self.send_header('Cache-Control', 'no-store')
        if cookie is not None: self.send_header('Set-Cookie', f'pc_key={cookie}; Path=/key/api/; Max-Age={600 if cookie else 0}; HttpOnly; Secure; SameSite=Strict')
        self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def session(self):
        ck = self.headers.get('Cookie') or ''; m = re.search(r'pc_key=([A-Za-z0-9_-]+)', ck)
        s = sessions.get(m.group(1)) if m else None
        return s if s and s['exp'] > time.time() else None
    def do_GET(self):
        if self.path == '/key/api/status':
            o = jload('owner.json', {'creds': []}); s = self.session()
            return self.send(200, {'enrolled': bool(o['creds']), 'devices': [c['label'] for c in o['creds']], 'unlocked': bool(s), 'expires_in': int(s['exp'] - time.time()) if s else 0})
        if self.path == '/key/api/chain':
            c = jload('chain.json', []); ok, prev = True, 'GENESIS'
            for r in c:
                b = {k: v for k, v in r.items() if k != 'hash'}
                if b.get('prev') != prev or h(b) != r['hash']: ok = False; break
                prev = r['hash']
            return self.send(200, {'count': len(c), 'intact': ok, 'tail': c[-15:]})
        if self.path == '/key/api/vault':
            if not self.session(): return self.send(401, {'error': 'locked'})
            return self.send(200, {'items': jload('vault.json', {})})
        self.send(404, {'error': 'not found'})
    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0)
        if n <= 0 or n > 65536: return self.send(413, {'error': 'size'})
        if self.headers.get('Origin') not in (ORIGIN, None): return self.send(403, {'error': 'origin'})
        try: req = json.loads(self.rfile.read(n)); return self.route(req)
        except (ValueError, KeyError, TypeError) as e:
            witness('refused', {'action': self.path.rsplit('/', 1)[-1], 'reason': str(e)[:40]}); return self.send(403, {'error': str(e)[:60]})
    def route(self, req):
        p = self.path; o = jload('owner.json', {'creds': []})
        if p == '/key/api/begin':
            kind = 'reg' if req.get('kind') == 'reg' else 'get'
            if kind == 'reg':
                # first device needs the one-time enroll token; extra devices need an unlocked session
                if o['creds'] and not self.session(): raise ValueError('unlock_first')
                if not o['creds']:
                    t = jload('enroll.json', {}).get('token')
                    if not t or not hmac.compare_digest(t, str(req.get('enroll', ''))): raise ValueError('enroll_token')
            elif not o['creds']: return self.send(404, {'error': 'not_enrolled'})
            ch = b64e(secrets.token_bytes(32)); challenges[ch] = (kind, time.time() + 120)
            return self.send(200, {'challenge': ch, 'rpId': RP_ID, 'creds': [c['id'] for c in o['creds']]})
        if p == '/key/api/register':
            if o['creds'] and not self.session(): raise ValueError('unlock_first')
            if not o['creds']:
                t = jload('enroll.json', {}).get('token')
                if not t or not hmac.compare_digest(t, str(req.get('enroll', ''))): raise ValueError('enroll_token')
            take(b64d(req['clientDataJSON']), 'reg')
            att, _ = cbor(b64d(req['attestationObject'])); ad = att['authData']; authdata(ad)
            if not ad[32] & 64: raise ValueError('no_credential')
            L = int.from_bytes(ad[53:55], 'big'); cred = ad[55:55+L]; key, _ = cbor(ad, 55 + L)
            if key.get(3) != -7 or key.get(-1) != 1: raise ValueError('alg_es256_only')
            label = re.sub(r'[^\w ·.-]', '', str(req.get('label', 'iPhone')))[:40] or 'device'
            o['creds'].append({'id': b64e(cred), 'x': b64e(key[-2]), 'y': b64e(key[-3]), 'label': label, 'prf': bool(req.get('prf'))}); jsave('owner.json', o)
            if os.path.exists(P('enroll.json')): os.remove(P('enroll.json'))
            witness('owner.passkey', {'by': 'owner', 'authority': 'æ2', 'device': label, 'cred': b64e(cred)[:12]})
            return self.send(200, {'ok': True, 'devices': len(o['creds'])})
        if p == '/key/api/unlock':
            from cryptography.hazmat.primitives.asymmetric import ec
            from cryptography.hazmat.primitives import hashes
            cdj = b64d(req['clientDataJSON']); ad = b64d(req['authenticatorData']); take(cdj, 'get'); authdata(ad)
            c = next((c for c in o['creds'] if c['id'] == req.get('credId')), None)
            if not c: raise ValueError('unknown_key')
            pub = ec.EllipticCurvePublicNumbers(int.from_bytes(b64d(c['x']), 'big'), int.from_bytes(b64d(c['y']), 'big'), ec.SECP256R1()).public_key()
            try: pub.verify(b64d(req['signature']), ad + hashlib.sha256(cdj).digest(), ec.ECDSA(hashes.SHA256()))
            except Exception: raise ValueError('signature')
            tok = secrets.token_urlsafe(24); sessions[tok] = {'exp': time.time() + 600, 'device': c['label']}
            witness('owner.unlock', {'by': 'owner', 'device': c['label']})
            return self.send(200, {'ok': True, 'device': c['label'], 'expires_in': 600}, cookie=tok)
        s = self.session()
        if not s: return self.send(401, {'error': 'locked'})
        if p == '/key/api/lock':
            ck = re.search(r'pc_key=([A-Za-z0-9_-]+)', self.headers.get('Cookie') or ''); sessions.pop(ck.group(1), None) if ck else None
            return self.send(200, {'ok': True}, cookie='')
        if p == '/key/api/vault/put':
            name = str(req.get('name', ''))
            if not NAME.match(name): raise ValueError('bad_name')
            item = {'iv': str(req['iv'])[:32], 'ct': str(req['ct'])[:40000], 'kid': str(req.get('kid', ''))[:24], 'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
            if not re.match(r'^[A-Za-z0-9_-]+$', item['iv'] + item['ct']): raise ValueError('not_ciphertext')
            v = jload('vault.json', {}); v[name] = item; jsave('vault.json', v)
            witness('vault.put', {'by': 'owner', 'name': name, 'device': s['device']}); return self.send(200, {'ok': True, 'count': len(v)})
        if p == '/key/api/vault/delete':
            v = jload('vault.json', {}); name = str(req.get('name', ''))
            if v.pop(name, None) is None: raise ValueError('no_item')
            jsave('vault.json', v); witness('vault.delete', {'by': 'owner', 'name': name, 'device': s['device']}); return self.send(200, {'ok': True})
        if p == '/key/api/vault/reveal':
            witness('vault.reveal', {'by': 'owner', 'name': str(req.get('name', ''))[:64], 'device': s['device'], 'where': 'device_only'}); return self.send(200, {'ok': True})
        return self.send(404, {'error': 'not found'})
if __name__ == '__main__':
    os.makedirs(DATA, exist_ok=True); ThreadingHTTPServer(('127.0.0.1', 8791), H).serve_forever()
