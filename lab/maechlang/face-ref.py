#!/usr/bin/env python3
"""face-ref.py · Python reference for lab/maechlang/face-v2.mec (mæchlæng #Face v2).

Same rules as the Mech boceto, top to bottom, so safety wins.
mæchlæng is written in Mech (mech-lang.org, Corey Montella, Apache-2.0, beta v0.3.5);
mæchlæng is NOT affiliated with Mech. This Python file IS run; the .mec is a sketch.
Record kind: ae.face/0.1 · robot authority æ1 (read-only face, never commands motors).
"""
import json, sys

MOODS = ["hold", "lost", "tired", "sleep", "think", "ready", "work"]

# face-table: mood, means, eyes, mouth, motion  (mirrors the Mech table)
FACE_TABLE = [
    ("hold",  "fault latched · human must clear", "▮ ▮", "━━━", "frozen"),
    ("lost",  "no fresh state (age > 0.5 s)",     "? ?", "～～", "scan"),
    ("tired", "battery below 20 %",               "◡ ◡", "‿",   "droop"),
    ("sleep", "DAMP · motors soft",               "─ ─", "·",   "breathe"),
    ("think", "STAND · not armed",                "◔ ◔", "─",   "drift"),
    ("ready", "STAND · armed",                    "◉ ◉", "‿",   "blink"),
    ("work",  "MOVE · executing",                 "◎ ◎", "▬",   "track"),
]

# the Mech rule line each mood comes from (shown in the demo)
RULES = {
    "hold":  'ft ∨ md ⩵ "FAULT_DAMP" → :Show(:hold)',
    "lost":  "ag > 0.5 → :Show(:lost)",
    "tired": "sc < 20 → :Show(:tired)",
    "sleep": 'md ⩵ "DAMP" → :Show(:sleep)',
    "think": 'md ⩵ "STAND" ∧ ¬ar → :Show(:think)',
    "ready": 'md ⩵ "STAND" ∧ ar → :Show(:ready)',
    "work":  'md ⩵ "MOVE" → :Show(:work)',
}

def face(md, ar, ft, ag, sc):
    """#Face: mode, armed, faulted, age (s), battery (%) -> mood. First match wins."""
    if ft or md == "FAULT_DAMP": return "hold"
    if ag > 0.5:                 return "lost"
    if sc < 20:                  return "tired"
    if md == "DAMP":             return "sleep"
    if md == "STAND" and not ar: return "think"
    if md == "STAND" and ar:     return "ready"
    if md == "MOVE":             return "work"
    return "lost"                # unknown mode: treat as no trustworthy state

# #Idle micro-state machine: motion = state. One tick = 0.1 s.
PERIOD = {"frozen": 0, "scan": 8, "droop": 30, "breathe": 25, "drift": 15, "blink": 40, "track": 6}

def idle(motion, t):
    """Returns the micro state at tick t: :Open, :Blink (1 tick), or :Still (frozen)."""
    p = PERIOD[motion]
    if p == 0: return "Still"
    return "Blink" if t % p == p - 1 else "Open"

def record(md, ar, ft, ag, sc):
    m = face(md, ar, ft, ag, sc)
    row = next(r for r in FACE_TABLE if r[0] == m)
    return {"kind": "ae.face/0.1", "mood": m, "means": row[1], "eyes": row[2],
            "mouth": row[3], "motion": row[4], "rule": RULES[m],
            "in": {"mode": md, "armed": ar, "faulted": ft, "age": ag, "battery": sc},
            "authority": "æ1"}

CASES = [  # (md, ar, ft, ag, sc) -> expected
    (("MOVE", True, True, 0.05, 80), "hold"),        # fault beats everything
    (("FAULT_DAMP", False, False, 0.05, 80), "hold"),
    (("MOVE", True, False, 0.9, 80), "lost"),        # stale beats battery/mode
    (("STAND", True, False, 0.05, 12), "tired"),
    (("DAMP", False, False, 0.05, 80), "sleep"),
    (("STAND", False, False, 0.05, 80), "think"),
    (("STAND", True, False, 0.05, 80), "ready"),
    (("MOVE", True, False, 0.05, 80), "work"),
]

def selftest():
    ok = 0
    for args, want in CASES:
        got = face(*args); good = got == want; ok += good
        print(f"{'✓' if good else '✗'} #Face{args} ⇒ :{got}  (want :{want})")
    seen = {face(*a) for a, _ in CASES}
    cov = seen == set(MOODS) and [r[0] for r in FACE_TABLE] == MOODS
    print(f"{'✓' if cov else '✗'} all 7 moods covered: {' > '.join(MOODS)}")
    blinks = [idle("blink", t) for t in range(40)].count("Blink")
    bi = blinks == 1 and idle("frozen", 7) == "Still"
    print(f"{'✓' if bi else '✗'} #Idle: blink once per 40 ticks, hold stays :Still")
    print(json.dumps(record("MOVE", True, False, 0.05, 80), ensure_ascii=False))
    passed = ok == len(CASES) and cov and bi
    print(f"{ok}/{len(CASES)} cases · {'PASS' if passed else 'FAIL'}")
    return passed

if __name__ == "__main__":
    sys.exit(0 if selftest() else 1)
