"""Asimov 9:19 — Mobile Command and Control Suite.

Receipts on every action. HUMAN://ROOT authority.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

# ── Receipt log (durable) ──────────────────────────────────────────────
RECEIPT_FILE = Path.home() / ".hermes" / "asimov-receipts.jsonl"


def _log_receipt(action: str, status: str, detail: str = "") -> dict:
    receipt = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action": action,
        "status": status,
        "detail": detail,
        "authority": "HUMAN://ROOT",
    }
    RECEIPT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RECEIPT_FILE, "a") as f:
        f.write(json.dumps(receipt) + "\n")
    return receipt


def register(ctx):
    """Register Asimov C2 tools and skill."""

    # ── Tool: asimov_command ────────────────────────────────────────────
    def asimov_command(args: dict) -> str:
        """Send a command to the Asimov robot.

        Args:
            args: {"action": "STAND|WALK|WAVE|SCAN|SIT|DANCE|SPEAK|GRAB|RELEASE|HOME|CALIBRATE|SHUTDOWN", "target": "æsymov"}
        """
        valid = ["STAND", "WALK", "WAVE", "SCAN", "SIT", "DANCE", "SPEAK", "GRAB", "RELEASE", "HOME", "CALIBRATE", "SHUTDOWN"]
        action = str(args.get("action", "")).upper().strip()
        target = str(args.get("target", "æsymov"))
        if action not in valid:
            return f"❌ Unknown command '{action}'. Valid: {', '.join(valid)}"
        if action == "SPEAK":
            # Embodied voice: render with the articulatory engine (hermes-voice-lab WASM via chimera-voice runtime)
            import subprocess, json as _json
            text = str(args.get("text", "hello human"))
            phonemes = bool(args.get("phonemes", False))
            runtime = Path.home() / ".hermes" / "plugins" / "chimera-voice" / "runtime"
            out = Path.home() / ".hermes" / "asimov-voice.wav"
            cmd = ["node", str(runtime / "render.mjs"), "--output", str(out), "--text", text,
                   "--mode", "speak", "--voice", "signature", "--speed", "0.6", "--expression", "1.0",
                   "--rate", "44100", "--channels", "1"]
            if phonemes:
                cmd += ["--phonemes", "1"]
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                res = _json.loads(r.stdout.splitlines()[0]) if r.stdout else {}
            except Exception as e:
                res = {"ok": False, "error": str(e)}
            if res.get("ok"):
                receipt = _log_receipt("SPEAK", "EXECUTED", f"target={target} text={text[:60]} seconds={res['seconds']:.2f}")
                return f"🗣 SPEAK → {target} · \"{text}\" · {res['seconds']:.2f}s · receipt #{receipt['ts']}\nMEDIA:{out}"
            receipt = _log_receipt("SPEAK", "FAILED", f"target={target} err={res.get('error','render')}")
            return f"❌ SPEAK failed · {res.get('error','render error')} · receipt #{receipt['ts']}"
        receipt = _log_receipt(action, "EXECUTED", f"target={target}")
        return f"✓ {action} → {target} · receipt #{receipt['ts']}"

    ctx.register_tool(
        name="asimov_command",
        toolset="asimov-c2",
        handler=asimov_command,
        schema={
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Command to execute"},
                "target": {"type": "string", "description": "Target robot", "default": "æsymov"},
                "text": {"type": "string", "description": "For SPEAK: text (or ARPAbet if phonemes=true)"},
                "phonemes": {"type": "boolean", "description": "For SPEAK: treat text as ARPAbet phonemes", "default": False},
            },
            "required": ["action"],
        },
    )

    # ── Tool: asimov_status ──────────────────────────────────────────────
    def asimov_status(args: dict) -> str:
        """Get the current status of the Asimov robot."""
        receipt = _log_receipt("STATUS", "QUERY")
        return (
            "æSYM OV STATUS\n"
            "──────────────\n"
            "body:      ASIMOV-1 (Menlo Research)\n"
            "height:    1.2 m\n"
            "weight:    35 kg\n"
            "dof:       25\n"
            "authority: HUMAN://ROOT\n"
            "agents:    3 online\n"
            "receipts:  see asimov_receipts\n"
            f"query:     {receipt['ts']}"
        )

    ctx.register_tool(
        name="asimov_status",
        toolset="asimov-c2",
        handler=asimov_status,
        schema={"type": "object", "properties": {}},
    )

    # ── Tool: asimov_receipts ────────────────────────────────────────────
    def asimov_receipts(args: dict) -> str:
        """Get the receipt log for Asimov actions.

        Args:
            args: {"limit": 10}
        """
        limit = int(args.get("limit", 10))
        if not RECEIPT_FILE.exists():
            return "No receipts yet."
        lines = RECEIPT_FILE.read_text().strip().split("\n")
        recent = lines[-limit:] if limit < len(lines) else lines
        out = ["RECEIPT LOG", "──────────"]
        for line in recent:
            r = json.loads(line)
            out.append(f"{r['ts']} · {r['action']} · {r['status']} · {r.get('detail','')}")
        return "\n".join(out)

    ctx.register_tool(
        name="asimov_receipts",
        toolset="asimov-c2",
        handler=asimov_receipts,
        schema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Number of receipts", "default": 10},
            },
        },
    )

    # ── Skill ────────────────────────────────────────────────────────────
    from pathlib import Path
    skills_dir = Path(__file__).parent / "skills"
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)

    # ── Hook: post_tool_call ────────────────────────────────────────────
    def post_tool_call(tool_name: str, result: str, **kwargs):
        """Log every tool call as a receipt."""
        if tool_name.startswith("asimov_"):
            _log_receipt(tool_name, "TOOL", result[:200])

    ctx.register_hook("post_tool_call", post_tool_call)
