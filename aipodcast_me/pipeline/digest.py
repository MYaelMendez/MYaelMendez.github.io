#!/usr/bin/env python3
"""Digest — memory layer for the Fleet Waves exponential loop.

Records prompt → output mappings, scores outputs, generates
improved prompts for the next iteration.

Immutable append-only (CRI pattern): raw data never overwritten.
Published score = formula + data + version + provenance.

Part of the Fleet Waves exponential loop:
  Prompt → Storyboard → Code → Render → Digest
"""
import json, sys, os, hashlib, time
from pathlib import Path

PIPELINE_DIR = Path(__file__).parent
DIGEST_FILE = PIPELINE_DIR / "storyboard_out" / "digest.json"

SCORING = {
    "mood_complexity": {"weight": 0.2, "max": 10},
    "geometry_variety": {"weight": 0.2, "max": 10},
    "effect_count": {"weight": 0.15, "max": 10},
    "camera_diversity": {"weight": 0.15, "max": 10},
    "color_saturation": {"weight": 0.15, "max": 10},
    "particle_presence": {"weight": 0.1, "max": 10},
    "prompt_specificity": {"weight": 0.05, "max": 10},
}

MOOD_SCORES = {
    "neon": 9, "cyber": 9, "plasma": 8, "matrix": 8,
    "gold": 7, "ocean": 7, "ember": 7, "void": 5,
}

GEOMETRY_SCORES = {
    "torusknot": 9, "icosahedron": 8, "dodecahedron": 8,
    "octahedron": 7, "torus": 7, "sphere": 6,
    "box": 5, "cylinder": 5, "cone": 5, "plane": 4,
}

MOOD_COLORS = {
    "neon": {"primary": "#00eaff", "secondary": "#050505", "accent": "#D4AF37"},
    "gold": {"primary": "#D4AF37", "secondary": "#0a0a0a", "accent": "#00ff9d"},
    "cyber": {"primary": "#ff0066", "secondary": "#050505", "accent": "#00eaff"},
    "ocean": {"primary": "#0066ff", "secondary": "#000505", "accent": "#00ffcc"},
    "ember": {"primary": "#ff6600", "secondary": "#050000", "accent": "#ffcc00"},
    "void": {"primary": "#888888", "secondary": "#050505", "accent": "#D4AF37"},
    "matrix": {"primary": "#00ff41", "secondary": "#000a00", "accent": "#00cc33"},
    "plasma": {"primary": "#cc00ff", "secondary": "#050005", "accent": "#ff00aa"},
}

CAMERAS = [
    {"fov": 75, "pos": [8, 5, 10]},
    {"fov": 45, "pos": [3, 2, 5]},
    {"fov": 60, "pos": [0, 12, 0.1]},
    {"fov": 55, "pos": [6, 4, 8]},
    {"fov": 50, "pos": [5, 2, 6]},
]

EFFECTS_LIST = ["bloom", "chromatic", "scanline", "glitch", "fire", "water", "neural"]

GEOMETRY_LIST = list(GEOMETRY_SCORES.keys())


def score_output(spec, frames):
    """Score a generated output (0-100)."""
    mood = spec.get("mood", "void")
    objects = spec.get("objects", [])
    effects = spec.get("effects", [])
    camera = spec.get("camera", {})
    particles = spec.get("particles", False)
    prompt = spec.get("prompt", "")

    scores = {}

    # Mood complexity
    scores["mood_complexity"] = MOOD_SCORES.get(mood, 5) / 10 * SCORING["mood_complexity"]["max"]

    # Geometry variety
    geo_types = set(obj.get("type", "torusknot") for obj in objects)
    geo_score = min(len(geo_types) / 3 * 10, 10)
    for gt in geo_types:
        geo_score = max(geo_score, GEOMETRY_SCORES.get(gt, 5) / 10 * 10)
    scores["geometry_variety"] = geo_score

    # Effect count
    eff_score = min(len(effects) / 3 * 10, 10)
    scores["effect_count"] = eff_score

    # Camera diversity
    cam_score = 5
    for cam in CAMERAS:
        if camera.get("fov") == cam["fov"]:
            cam_score = 8
            break
    scores["camera_diversity"] = cam_score

    # Color saturation
    colors = spec.get("colors", MOOD_COLORS.get(mood, MOOD_COLORS["void"]))
    primary = colors.get("primary", "#888888")
    sat_score = 7 if primary != "#888888" else 4
    scores["color_saturation"] = sat_score

    # Particle presence
    scores["particle_presence"] = 10 if particles else 3

    # Prompt specificity
    words = len(prompt.split())
    spec_score = min(words / 5 * 10, 10)
    scores["prompt_specificity"] = spec_score

    # Weighted total
    total = 0
    for key, data in SCORING.items():
        total += scores.get(key, 0) * data["weight"]

    return {
        "total": round(total, 1),
        "components": {k: round(v, 1) for k, v in scores.items()},
        "max": 10,
    }


def generate_next_prompt(spec, score):
    """Generate an improved prompt for the next iteration.
    
    Uses the digest of what worked to mutate the prompt.
    """
    mood = spec.get("mood", "void")
    objects = spec.get("objects", [{"type": "torusknot"}])
    effects = spec.get("effects", ["bloom"])
    particles = spec.get("particles", False)

    # Build improved prompt
    parts = []

    # Mood (keep if score > 6, else try another)
    if score["total"] >= 7:
        parts.append(mood)
    else:
        better_moods = ["neon", "cyber", "plasma", "matrix", "gold", "ocean", "ember"]
        for m in better_moods:
            if m != mood:
                parts.append(m)
                break
        else:
            parts.append(mood)

    # Geometry (try variety)
    current_geo = objects[0].get("type", "torusknot") if objects else "torusknot"
    for geo in GEOMETRY_LIST:
        if geo != current_geo:
            parts.append(geo)
            break

    # Effects (add if missing)
    for eff in EFFECTS_LIST:
        if eff not in effects:
            parts.append(eff)
            break

    # Camera
    parts.append("wide shot")

    # Particles
    if not particles:
        parts.append("particles")

    prompt = " ".join(parts)
    return prompt


def digest(spec_path, output_dir=None):
    """Run the digest on a generation cycle.
    
    Args:
        spec_path: Path to scene_spec.json
        output_dir: Output directory (default: storyboard_out)
    
    Returns:
        dict with digest entry, score, and next prompt
    """
    spec_data = json.loads(Path(spec_path).read_text())
    spec = spec_data["spec"]
    frames = spec_data["frames"]

    out_dir = Path(output_dir) if output_dir else DIGEST_FILE.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Score the output
    score = score_output(spec, frames)

    # Generate next prompt
    next_prompt = generate_next_prompt(spec, score)

    # Build digest entry
    entry = {
        "timestamp": time.time(),
        "prompt": spec.get("prompt", ""),
        "prompt_hash": spec.get("prompt_hash", "unknown"),
        "mood": spec.get("mood", "void"),
        "score": score,
        "next_prompt": next_prompt,
        "files": [f["file"] for f in spec_data.get("files", [])],
        "version": "1.0.0",
        "source": "fleet-waves-digest",
    }

    # Load existing digest or create new
    digest_path = out_dir / "digest.json"
    if digest_path.exists():
        digest_data = json.loads(digest_path.read_text())
        digest_data["entries"].append(entry)
    else:
        digest_data = {
            "version": "1.0.0",
            "source": "fleet-waves-digest",
            "entries": [entry],
        }

    # Save (append-only)
    digest_path.write_text(json.dumps(digest_data, indent=2))

    return {
        "entry": entry,
        "score": score,
        "next_prompt": next_prompt,
        "digest_path": str(digest_path),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: digest.py <scene_spec.json> [output_dir]")
        print()
        print("Computes score, stores digest, generates next prompt.")
        sys.exit(1)

    spec_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print("=" * 60)
    print("FLEET WAVES — Digest: Memory for the exponential loop")
    print("=" * 60)

    result = digest(spec_path, output_dir)

    print("\nPrompt: {}".format(result["entry"]["prompt"]))
    print("Mood: {}".format(result["entry"]["mood"]))
    print("\nScore: {}/10".format(result["score"]["total"]))
    print("Components:")
    for k, v in result["score"]["components"].items():
        print("  {}: {:.1f}".format(k, v))

    print("\nNext prompt: {}".format(result["next_prompt"]))
    print("\nDigest -> {}".format(result["digest_path"]))
    print("=" * 60)


if __name__ == "__main__":
    main()