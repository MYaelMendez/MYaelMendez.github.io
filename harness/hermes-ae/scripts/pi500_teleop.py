"""Pi500 keyboard teleop client for the removable Asimov face.

Plain stdlib Python so it can be copied to a Raspberry Pi 500 keyboard and run
with `python3 pi500_teleop.py`. Motion keys require an arming flag AND a
per-command deadman prefix (`!`) so no stray keystroke can move the robot.
"""
import argparse, json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FACE = HERE / 'removable_face.py'
PY = sys.executable

HELP = """Asimov Pi500 teleop
  w/s  forward/back      a/d  turn left/right
  q/e  left/right arm    r/f  head up/down
  !key = deadman engaged (required for any motion)
  space = all stop       v = voice listen mode
  t = toggle native head viewport x/quit = exit
  help = show this map
"""


def call(action, **kwargs):
    payload = json.dumps({'action': action, **kwargs})
    p = subprocess.run([PY, str(FACE), payload], capture_output=True, text=True, timeout=300)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:
        return {'success': False, 'error': (p.stderr or p.stdout or 'no JSON')[-600:]}


def one(key, arm, deadman):
    r = call('teleop', key=key, arm=arm, deadman=deadman)
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r.get('success') else 1


def demo():
    seq = [('w', True, True), ('a', True, True), (' ', False, False), ('v', False, False)]
    out = []
    for key, arm, deadman in seq:
        r = call('teleop', key=key, arm=arm, deadman=deadman)
        out.append(r)
        print(json.dumps(r, ensure_ascii=False))
    return 0 if all(r.get('success') for r in out) else 1


def interactive():
    print(HELP)
    print('ARMED' if os.environ.get('PI500_ARM') == '1' else 'UNARMED (motion disabled)')
    while True:
        try:
            line = input('asimov> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not line:
            continue
        if line.lower() in ('quit', 'exit', 'x'):
            r = call('teleop', key='x', arm=False, deadman=False)
            print(json.dumps(r, ensure_ascii=False))
            return 0
        if line.lower() == 'help':
            print(HELP)
            continue
        deadman = line.startswith('!')
        key = line[1:] if deadman else line
        if key.lower() == 'v':
            text = input('transcribed text (ASR is external): ').strip()
            if text:
                print(json.dumps(call('voice', text=text, voice=os.environ.get('ASIMOV_VOICE', 'M2')), ensure_ascii=False))
            else:
                print(json.dumps(call('teleop', key='v', arm=False, deadman=False), ensure_ascii=False))
            continue
        r = call('teleop', key=key, arm=os.environ.get('PI500_ARM') == '1', deadman=deadman)
        print(json.dumps(r, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--key', help='single key: w/s/a/d/q/e/r/f/space/v/t/x')
    ap.add_argument('--arm', action='store_true', help='enable motion keys')
    ap.add_argument('--deadman', action='store_true', help='confirm deadman for one-shot motion')
    ap.add_argument('--demo', action='store_true', help='run a short safe demo sequence')
    ns = ap.parse_args()
    if ns.demo:
        return demo()
    if ns.key:
        return one(ns.key, ns.arm, ns.deadman)
    return interactive()


if __name__ == '__main__':
    raise SystemExit(main())
