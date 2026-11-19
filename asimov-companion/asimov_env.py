"""Environment perception for the Asimov browser companion.

`observe` is always allowed by æ policy — perception grants nothing. This feeds
the companion REAL machine state so the robot is aware of where it is running,
not a decorative status light.

Serves on 8162 (the scene server is 8161):
    GET /env      everything the robot can perceive
    GET /health   liveness

Every value is measured at request time. Nothing is cached stale, nothing is
invented, and a source that fails reports `unavailable` rather than a guess.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
PORT = int(os.environ.get('ASIMOV_ENV_PORT', '8162'))
START = time.time()


def _run(cmd, timeout=8):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding='utf-8', timeout=timeout)
        return p.stdout.strip() if p.returncode == 0 else None
    except Exception:
        return None


def gpu():
    out = _run(['nvidia-smi',
                '--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,pstate',
                '--format=csv,noheader,nounits'])
    if not out:
        return {'available': False}
    f = [x.strip() for x in out.splitlines()[0].split(',')]
    try:
        return {'available': True, 'name': f[0], 'util_pct': int(f[1]),
                'mem_used_mib': int(f[2]), 'mem_total_mib': int(f[3]),
                'temp_c': int(f[4]), 'pstate': f[5]}
    except Exception:
        return {'available': False, 'raw': out[:120]}


def memory():
    try:
        import ctypes

        class MS(ctypes.Structure):
            _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
        s = MS()
        s.dwLength = ctypes.sizeof(MS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s))
        return {'available': True, 'load_pct': s.dwMemoryLoad,
                'total_gb': round(s.ullTotalPhys / 1e9, 1),
                'free_gb': round(s.ullAvailPhys / 1e9, 1)}
    except Exception:
        return {'available': False}


def ledgers():
    out = {}
    for name in ('ae-receipts.jsonl', 'tiny-voca-receipts.jsonl',
                 'render-jobs.jsonl', 'sound-receipts.jsonl', 'moh-receipts.jsonl'):
        p = H / name
        if p.exists():
            try:
                out[name.replace('.jsonl', '')] = sum(
                    1 for l in p.read_text(encoding='utf-8').splitlines() if l.strip())
            except Exception:
                pass
    return out


def renders():
    d = H / 'cache' / 'scratch' / 'ae-renders'
    if not d.exists():
        return {'available': False}
    jobs = []
    for p in sorted(d.glob('*.json'), key=lambda x: x.stat().st_mtime, reverse=True)[:4]:
        try:
            j = json.loads(p.read_text(encoding='utf-8'))
            jobs.append({'job': j.get('job_id'), 'state': j.get('state'),
                         'gate': (j.get('gate') or {}).get('calidad')})
        except Exception:
            pass
    return {'available': True, 'recent': jobs}


def films():
    site = Path(os.environ.get('AE_SITE', r'C:\æ\github-pages'))
    if not site.exists():
        return {'available': False}
    n = len(list(site.glob('*.mp4')))
    return {'available': True, 'published': n}


def environment():
    return {
        'scheme': 'asimov://observe',
        'authority': 'HUMAN://ROOT',
        'grants': False,
        'note': 'perception only. Observing grants nothing.',
        'at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'uptime_s': round(time.time() - START, 1),
        'host': {'node': os.environ.get('COMPUTERNAME', 'unknown'),
                 'platform': os.name, 'cpus': os.cpu_count()},
        'gpu': gpu(),
        'memory': memory(),
        'ledgers': ledgers(),
        'renders': renders(),
        'films': films(),
        'tools': {'ffmpeg': bool(shutil.which('ffmpeg'))},
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.startswith('/env'):
            body = json.dumps(environment(), ensure_ascii=False).encode('utf-8')
        elif self.path.startswith('/health'):
            body = b'{"ok":true}'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    print(f'  asimov perception on http://127.0.0.1:{PORT}/env')
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
