#!/usr/bin/env python3
"""Validate public aeSTATE v1 checkpoints without third-party dependencies."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent

def validate(state):
    required = {"schema", "id", "created_on", "environment", "source", "context", "witness", "next_action", "authority"}
    if not isinstance(state, dict) or set(state) != required:
        raise ValueError("Unexpected or missing top-level fields")
    if state["schema"] != "ae.state.v1" or not re.fullmatch(r"[a-z0-9-]+", state["id"]):
        raise ValueError("Invalid schema or ID")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", state["created_on"]):
        raise ValueError("Invalid date")
    if not isinstance(state["environment"], str) or not state["environment"].strip():
        raise ValueError("Empty environment")
    source = state["source"]
    if not isinstance(source, dict) or set(source) != {"repository", "pull_request", "observed_head"}:
        raise ValueError("Invalid source fields")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", source["repository"]):
        raise ValueError("Invalid repository")
    if type(source["pull_request"]) is not int or source["pull_request"] < 1:
        raise ValueError("Invalid PR number")
    if not re.fullmatch(r"[a-f0-9]{40}", source["observed_head"]):
        raise ValueError("Full immutable source revision required")
    context = state["context"]
    if not isinstance(context, dict) or set(context) != {"status", "summary", "blockers"}:
        raise ValueError("Invalid context")
    if context["status"] not in {"proposed", "prepared", "blocked", "verified"}:
        raise ValueError("Invalid state")
    if not isinstance(context["summary"], str) or not context["summary"].strip():
        raise ValueError("Summary required")
    if not isinstance(context["blockers"], list) or not all(isinstance(x, str) for x in context["blockers"]):
        raise ValueError("Invalid blockers")
    witness = state["witness"]
    if not isinstance(witness, dict) or set(witness) != {"url", "verification_scope"}:
        raise ValueError("Invalid witness")
    url = urlparse(witness["url"])
    if url.scheme != "https" or not url.hostname or url.username or url.password:
        raise ValueError("Evidence must be a noncredential HTTPS URL")
    if not isinstance(witness["verification_scope"], str) or not witness["verification_scope"].strip():
        raise ValueError("Evidence scope required")
    if not isinstance(state["next_action"], str) or not state["next_action"].strip():
        raise ValueError("Next action required")
    if state["authority"] != {"inherits": False, "requires_reauthorization": True}:
        raise ValueError("Authority cannot be inherited")
    serialized = json.dumps(state, ensure_ascii=False)
    if any(word in serialized.lower() for word in ('-----begin private key-----', 'ghp_', 'github_pat_', 'sk-proj-')):
        raise ValueError("Possible secret detected")
    return True

def main():
    files = sorted((ROOT / "checkpoints").glob("*.json"))
    if not files:
        raise ValueError("No checkpoints")
    for path in files:
        validate(json.loads(path.read_text(encoding="utf-8")))
        print("PASS", path.relative_to(ROOT))

if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
