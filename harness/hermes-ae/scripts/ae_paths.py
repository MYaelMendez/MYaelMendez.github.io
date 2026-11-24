"""Shared paths for the bundled hermes-ae scripts.

All locations are configurable by environment so the repo stays portable.
Defaults assume a normal Hermes install under $HERMES_HOME.
"""
import os
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS.parent
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
RUNTIME = Path(os.environ.get("HERMES_AE_HOME", HERMES_HOME / "ae"))
ANIM = Path(os.environ.get("HERMES_AE_ANIM", RUNTIME / "asimov-anim"))
MODEL = Path(os.environ.get("HERMES_AE_MODEL", RUNTIME / "model"))
MESHES = Path(os.environ.get("HERMES_AE_MESHES", MODEL / "meshes"))
GALLERY_REPO = Path(os.environ.get("HERMES_AE_GALLERY", RUNTIME / "gallery"))
LEDGER = Path(os.environ.get("HERMES_AE_LEDGER", HERMES_HOME / "ae-receipts.jsonl"))
PY = os.environ.get("HERMES_AE_PYTHON", "/usr/local/bin/python3")

# Repo-local model manifests ship with the plugin; binary meshes and videos do not.
BUNDLED_MODEL = REPO_ROOT / "model"
BUNDLED_XML = BUNDLED_MODEL / "xml"
BUNDLED_URDF = BUNDLED_MODEL / "urdf"


def ensure_runtime():
    for p in (RUNTIME, ANIM, MODEL, GALLERY_REPO, LEDGER.parent):
        p.mkdir(parents=True, exist_ok=True)
