#!/usr/bin/env python3
"""
qr_kanban.py — a physical kanban board, machine-managed by Roboflow supervision.

A camera watches a table. Cards on the table are QR codes. Each QR is a typed
æ:// envelope whose `route` payload names a kanban verb. Move a card, and the
board changes.

This is the physical→digital bridge:

    camera frame → supervision (detect + annotate) → cv2 QRCodeDetector
        → qr_envelope.decode → kanban dispatch → the task board moves

The board is the table. The cards are QR. The machine is the supervisor.

Why supervision (Roboflow) and not raw cv2: supervision gives us
  · Detections — a first-class box/label/confidence container
  · BoxAnnotator / LabelAnnotator — the on-frame HUD
  · a stable API that survives OpenCV churn
We still decode QR with cv2.QRCodeDetector because supervision does not
ship a QR reader; supervision supervises the detection + annotation layer.

The substrate is itself open sourceware: DENSO WAVE does not exercise its
patents against standard QR ("Everyone can use the QR Code freely as long as
following the standards for QR Codes in JIS or ISO"), and the symbology is
ISO/IEC 18004. We stay conformant and layer our envelope on top — so no layer
of this pipeline carries a royalty. See QR_OPENSOURCEWARE.md.

Usage:
    python qr_kanban.py card <VERB> <TASK_ID> [--out PATH]   mint a QR card
    python qr_kanban.py watch [--camera N] [--once]          run the supervisor
    python qr_kanban.py replay <IMAGE>                       one frame, no camera
    python qr_kanban.py board                                show the board
    python qr_kanban.py verbs                                list card verbs

Env:
    VAEULT_KANBAN_DB    path to kanban.db (default: the Hermes kanban home)
    VAEULT_CAMERA       camera index (default 0)
    VAEULT_COOLDOWN     seconds before the same card fires twice (default 8)
"""
from __future__ import annotations

import argparse
import os
import pathlib
import sqlite3
import subprocess
import sys
import time

AGENTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AGENTS))

# ── config ────────────────────────────────────────────────────────────────────

def _kanban_home() -> pathlib.Path:
    home = os.environ.get("HERMES_HOME")
    if home:
        return pathlib.Path(home)
    la = os.environ.get("LOCALAPPDATA")
    if la and (pathlib.Path(la) / "hermes").is_dir():
        return pathlib.Path(la) / "hermes"
    return pathlib.Path.home() / ".hermes"


# The kanban module resolves its own DB via HERMES_KANBAN_DB (see
# kanban_db.py: "HERMES_KANBAN_DB env var (pins the DB file path directly)").
# We honour that name first, then our own, then the module default.
KANBAN_DB = pathlib.Path(os.environ.get(
    "HERMES_KANBAN_DB",
    os.environ.get("VAEULT_KANBAN_DB", str(_kanban_home() / "kanban.db"))))
CAMERA = int(os.environ.get("VAEULT_CAMERA", "0"))
COOLDOWN = float(os.environ.get("VAEULT_COOLDOWN", "8"))

# ── the card vocabulary ───────────────────────────────────────────────────────
# Each card is a `route` envelope. The verb maps to a kanban CLI verb.
# `needs_id` cards act on one task; `board_wide` cards act on the board.

VERBS = {
    "claim":    {"needs_id": True,  "desc": "claim a task (start work)"},
    "complete": {"needs_id": True,  "desc": "mark a task done"},
    "block":    {"needs_id": True,  "desc": "mark a task blocked"},
    "unblock":  {"needs_id": True,  "desc": "clear a block"},
    "archive":  {"needs_id": True,  "desc": "archive a task"},
    "inspect":  {"needs_id": True,  "desc": "show a task (no mutation)"},
    "list":     {"needs_id": False, "desc": "print the whole board"},
    "init":     {"needs_id": False, "desc": "create kanban.db if missing"},
}


# ── kanban dispatch ───────────────────────────────────────────────────────────

def _kanban_cli() -> list[str] | None:
    """Locate a runnable kanban CLI. Returns the argv prefix or None."""
    # 1. an installed `hermes` on PATH
    import shutil
    h = shutil.which("hermes")
    if h:
        return [h, "kanban"]
    # 2. the in-tree module (dev checkout)
    for root in (pathlib.Path(r"C:\æ\hermes-pr-cuda"),
                 pathlib.Path(r"C:\æ\hermes-fork")):
        if (root / "hermes_cli" / "kanban.py").exists():
            return [sys.executable, "-m", "hermes_cli.kanban"]
    return None


def _kanban_module():
    """Import the in-tree kanban module (dev checkout) or None."""
    for root in (pathlib.Path(r"C:\æ\hermes-pr-cuda"),
                 pathlib.Path(r"C:\æ\hermes-fork")):
        if (root / "hermes_cli" / "kanban.py").exists():
            if str(root) not in sys.path:
                sys.path.insert(0, str(root))
            try:
                import hermes_cli.kanban as k
                return k
            except Exception:
                continue
    return None


def dispatch(verb: str, task_id: str | None = None, dry: bool = False) -> dict:
    """Run one kanban operation. Never raises — returns a result dict.

    Prefers the in-process `run_slash(rest) -> str` entry (a string in, a
    string out — no subprocess, no argv guessing). Falls back to a shell
    `hermes kanban <verb>` when only an installed CLI is present.
    """
    spec = VERBS.get(verb)
    if not spec:
        return {"ok": False, "verb": verb, "error": f"unknown verb '{verb}'"}
    if spec["needs_id"] and not task_id:
        return {"ok": False, "verb": verb, "error": f"verb '{verb}' needs a task id"}

    rest = verb + (f" {task_id}" if task_id else "")

    if dry:
        return {"ok": True, "verb": verb, "task_id": task_id, "dry": True, "rest": rest}

    # 1. in-process: run_slash(rest) -> str
    k = _kanban_module()
    if k is not None and hasattr(k, "run_slash"):
        try:
            out = k.run_slash(rest)
            text = out if isinstance(out, str) else str(out)
            low = text.lower()
            failed = ("error" in low) or ("not found" in low) or ("unknown" in low)
            return {"ok": not failed, "verb": verb, "task_id": task_id,
                    "stdout": text.strip()[:400], "in_process": True}
        except Exception as e:
            return {"ok": False, "verb": verb, "task_id": task_id, "error": str(e)}

    # 2. installed CLI
    argv = _kanban_cli()
    if argv is None:
        return {"ok": False, "verb": verb, "error": "no kanban entry point found"}
    try:
        r = subprocess.run(list(argv) + [verb] + ([task_id] if task_id else []),
                           capture_output=True, text=True, timeout=30)
        return {"ok": r.returncode == 0, "verb": verb, "task_id": task_id,
                "rc": r.returncode, "stdout": r.stdout.strip()[:400],
                "stderr": r.stderr.strip()[:400]}
    except Exception as e:
        return {"ok": False, "verb": verb, "error": str(e)}


def board() -> list[dict]:
    """Read the board directly from SQLite (read-only, no CLI needed)."""
    if not KANBAN_DB.exists():
        return []
    try:
        con = sqlite3.connect(f"file:{KANBAN_DB}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT id, title, status, assignee, priority FROM tasks "
            "WHERE status NOT IN ('archived') ORDER BY priority DESC, created_at"
        ).fetchall()
        con.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


# ── cards ─────────────────────────────────────────────────────────────────────

def mint_card(verb: str, task_id: str | None, out: str | None = None) -> dict:
    """Create a QR card for a verb (+ optional task id)."""
    import qr_envelope as qe
    if verb not in VERBS:
        return {"ok": False, "error": f"unknown verb '{verb}'"}

    payload = {"cmd": f"kanban://{verb}" + (f" {task_id}" if task_id else ""),
               "verb": verb}
    if task_id:
        payload["task_id"] = task_id
    envelope = qe.encode("route", payload)

    try:
        import qrcode
    except ImportError:
        return {"ok": False, "error": "qrcode not installed"}

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=3)
    qr.add_data(envelope)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    dest = pathlib.Path(out) if out else (AGENTS / ".." / "secrets" / "qr" / f"card-{verb}-{task_id or 'board'}.png")
    dest = pathlib.Path(os.path.abspath(str(dest)))
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)
    return {"ok": True, "verb": verb, "task_id": task_id, "envelope": envelope,
            "path": str(dest), "version": qr.version}


def read_card(image, upscale: float = 1.5) -> list[dict]:
    """Decode every æ:// route card in an image (numpy array or path).

    UPSCALING MATTERS. cv2.QRCodeDetector.detectAndDecodeMulti misses cards on
    a dense multi-card frame at native resolution: on a 2x2 board of 260px
    cards it found 3/4 at 1.0x and 4/4 at 1.5x. The detector's internal
    binarizer needs more pixels per module once several QRs share a frame.
    We therefore upscale by default (1.5x) before detection. Measured, not
    guessed — see the note in the module docstring.

    Pass upscale=1.0 to disable when the frame is already high-resolution.
    """
    import cv2
    import numpy as np
    import qr_envelope as qe

    if isinstance(image, (str, pathlib.Path)):
        img = cv2.imread(str(image))
    else:
        img = image
    if img is None:
        return []

    if upscale and upscale != 1.0:
        img = cv2.resize(img, None, fx=upscale, fy=upscale,
                         interpolation=cv2.INTER_CUBIC)

    detector = cv2.QRCodeDetector()
    ok, decoded, points, _ = detector.detectAndDecodeMulti(img)
    cards = []
    if not ok or decoded is None:
        return cards
    for i, text in enumerate(decoded):
        if not text or not qe.is_envelope(text):
            continue
        try:
            kind, payload = qe.decode(text)
        except ValueError:
            continue
        if kind != "route":
            continue
        cards.append({
            "envelope": text,
            "verb": payload.get("verb") or payload.get("cmd", "").replace("kanban://", "").split()[0],
            "task_id": payload.get("task_id"),
            "box": points[i].tolist() if points is not None and i < len(points) else None,
        })
    return cards


# ── the supervisor ────────────────────────────────────────────────────────────

def supervise(frame, sv, np) -> tuple[object, list[dict]]:
    """Annotate a frame with supervision, and return the decoded cards.

    supervision owns the DETECTION + ANNOTATION layer; cv2 owns the QR read.
    """
    import cv2

    cards = read_card(frame)
    annotated = frame.copy()

    if cards:
        # Build a supervision Detections from the QR boxes so the annotators
        # (and anything downstream that consumes Detections) see them as
        # first-class objects. Boxes come from cv2's quad points.
        boxes, confs, labels = [], [], []
        for c in cards:
            if not c.get("box"):
                continue
            xs = [p[0] for p in c["box"]]
            ys = [p[1] for p in c["box"]]
            boxes.append([min(xs), min(ys), max(xs), max(ys)])
            confs.append(1.0)
            labels.append(c["verb"])

        if boxes:
            det = sv.Detections(
                xyxy=np.array(boxes, dtype=float),
                confidence=np.array(confs, dtype=float),
                class_id=np.arange(len(boxes)),
            )
            annotated = sv.BoxAnnotator(thickness=3).annotate(annotated, det)
            annotated = sv.LabelAnnotator(text_scale=0.7, text_thickness=2).annotate(
                annotated, det, labels=labels)

    # a HUD line with the machine's state
    import supervision as _sv
    hud = f"væult kanban supervisor · {len(cards)} card(s) · {_sv.__version__}"
    cv2.putText(annotated, hud, (14, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 200, 0), 2, cv2.LINE_AA)
    return annotated, cards


def watch(camera: int, once: bool, execute: bool, dry: bool):
    import cv2
    import numpy as np
    import supervision as sv

    cap = cv2.VideoCapture(camera)
    if not cap.isOpened():
        print(f"  ✗ cannot open camera {camera}")
        return

    last_fire: dict[str, float] = {}
    print(f"  væult kanban supervisor — camera {camera}, cooldown {COOLDOWN}s")
    print(f"  board: {KANBAN_DB}")
    print(f"  supervision {sv.__version__} · cv2 {cv2.__version__}")
    print("  q to quit\n")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            annotated, cards = supervise(frame, sv, np)

            now = time.time()
            for c in cards:
                key = f"{c['verb']}:{c.get('task_id')}"
                if now - last_fire.get(key, 0) < COOLDOWN:
                    continue
                last_fire[key] = now
                if not execute:
                    print(f"  [seen] {c['verb']} {c.get('task_id') or ''} (dry)")
                    continue
                r = dispatch(c["verb"], c.get("task_id"), dry=dry)
                mark = "✓" if r.get("ok") else "✗"
                detail = r.get("stdout") or r.get("error") or r.get("stderr") or ""
                print(f"  [{mark}] {c['verb']} {c.get('task_id') or ''}  {detail[:60]}")

            cv2.imshow("væult kanban supervisor", annotated)
            if once:
                cv2.waitKey(0)
                break
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(description="QR kanban machine, supervised by Roboflow supervision")
    sub = ap.add_subparsers(dest="cmd")

    p_card = sub.add_parser("card", help="mint a QR card")
    p_card.add_argument("verb", choices=sorted(VERBS))
    p_card.add_argument("task_id", nargs="?", default=None)
    p_card.add_argument("--out", default=None)

    p_watch = sub.add_parser("watch", help="run the camera supervisor")
    p_watch.add_argument("--camera", type=int, default=CAMERA)
    p_watch.add_argument("--once", action="store_true", help="single frame")
    p_watch.add_argument("--execute", action="store_true", help="actually dispatch")
    p_watch.add_argument("--dry", action="store_true", help="print the command only")

    p_replay = sub.add_parser("replay", help="decode one image, no camera")
    p_replay.add_argument("image")

    sub.add_parser("board", help="show the board")
    sub.add_parser("verbs", help="list card verbs")

    args = ap.parse_args(argv[1:])

    if args.cmd == "card":
        r = mint_card(args.verb, args.task_id, args.out)
        if r["ok"]:
            print(f"  ✓ card '{r['verb']}' v{r['version']} -> {r['path']}")
            print(f"  {r['envelope'][:70]}...")
        else:
            print(f"  ✗ {r['error']}")

    elif args.cmd == "watch":
        watch(args.camera, args.once, args.execute, args.dry)

    elif args.cmd == "replay":
        import supervision as sv
        import numpy as np
        import cv2
        frame = cv2.imread(args.image)
        if frame is None:
            print(f"  ✗ cannot read {args.image}")
            return
        annotated, cards = supervise(frame, sv, np)
        print(f"  {len(cards)} card(s):")
        for c in cards:
            print(f"    {c['verb']:10s} {c.get('task_id') or ''}")
        out = str(pathlib.Path(args.image).with_suffix(".annotated.png"))
        cv2.imwrite(out, annotated)
        print(f"  annotated -> {out}")

    elif args.cmd == "board":
        rows = board()
        if not rows:
            print("  board empty (or kanban.db not found)")
            return
        print(f"  {'STATUS':10s} {'ID':12s} {'ASSIGNEE':12s} TITLE")
        for r in rows:
            print(f"  {r['status']:10s} {r['id'][:12]:12s} {(r['assignee'] or '-')[:12]:12s} {r['title'][:40]}")

    elif args.cmd == "verbs":
        for v, s in sorted(VERBS.items()):
            print(f"  {v:10s} {'<task-id>' if s['needs_id'] else '(board)':10s} {s['desc']}")

    else:
        ap.print_help()


if __name__ == "__main__":
    main(sys.argv)
