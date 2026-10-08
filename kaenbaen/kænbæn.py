"""
kænbæn — shared system memory.
Every agent reads this before acting. No agent acts without reading kænbæn first.
"""
import json
import os
from pathlib import Path

KÆNBÆN_DIR = Path("C:/æ/kænbæn")

def load_system_map() -> dict:
    """Load system-map.json — what exists, where, how to verify."""
    path = KÆNBÆN_DIR / "system-map.json"
    if not path.exists():
        raise FileNotFoundError(f"kænbæn system-map not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def load_capability_contracts() -> dict:
    """Load capability-contracts.json — what each agent can do."""
    path = KÆNBÆN_DIR / "capability-contracts.json"
    if not path.exists():
        raise FileNotFoundError(f"kænbæn capability-contracts not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def load_verification_gates() -> dict:
    """Load verification-gates.json — what verifies each artifact."""
    path = KÆNBÆN_DIR / "verification-gates.json"
    if not path.exists():
        raise FileNotFoundError(f"kænbæn verification-gates not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def load_genesis_chain() -> dict:
    """Load genesis-chain.json — the immutable receipt chain."""
    path = KÆNBÆN_DIR / "genesis-chain.json"
    if not path.exists():
        raise FileNotFoundError(f"kænbæn genesis-chain not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def get_fleet_targets() -> list[str]:
    """Get the list of paths the fleet should scan."""
    sm = load_system_map()
    targets = []
    # Core fleet targets — these are the real paths the cron scans
    core = ["vscoder/src", "site", "github-pages", "hermes-fork", "agents", "threejs-curriculum"]
    for t in core:
        targets.append(t)
    # AEE targets (conditional — only if they exist)
    aee = sm.get("surfaces", {}).get("aee", {})
    for t in aee.get("targets", []):
        targets.append(t)
    return targets

def get_known_debts() -> list[str]:
    """Get the list of known debts — things the system knows are broken."""
    sm = load_system_map()
    return sm.get("known_debts", [])

def get_capture_config() -> dict:
    """Get capture pipeline configuration."""
    sm = load_system_map()
    return sm.get("surfaces", {}).get("capture", {})

def get_verification_gate(artifact_type: str) -> dict | None:
    """Get the verification gate for a given artifact type."""
    gates = load_verification_gates()
    return gates.get("gates", {}).get(artifact_type)

def verify_before_act(agent_name: str, action: str) -> bool:
    """
    Gate: every agent must read kænbæn before acting.
    Returns True if the agent is allowed to act.
    """
    try:
        load_system_map()
        load_capability_contracts()
        return True
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    print("=== kænbæn — system memory ===")
    sm = load_system_map()
    print(f"System: {sm.get('system')}")
    print(f"Version: {sm.get('version')}")
    print(f"Surfaces: {list(sm.get('surfaces', {}).keys())}")
    print(f"Known debts: {len(sm.get('known_debts', []))}")
    
    cc = load_capability_contracts()
    print(f"Agents: {list(cc.get('agents', {}).keys())}")
    
    vg = load_verification_gates()
    print(f"Gates: {list(vg.get('gates', {}).keys())}")
    
    gc = load_genesis_chain()
    print(f"Genesis: {gc.get('genesis', {}).get('receipt')}")
    print(f"Chain length: {len(gc.get('chain', []))}")
    
    print(f"\nFleet targets: {get_fleet_targets()}")
    print(f"Debts: {get_known_debts()}")
