#!/usr/bin/env python3
"""Parse a Fleet Waves creative prompt into a scene specification.

Input: natural language creative direction
Output: JSON scene spec with camera, lighting, objects, colors, effects
"""
import json, re, sys, os, hashlib
from pathlib import Path

PIPELINE_DIR = Path(__file__).parent
SPEC_OUT = PIPELINE_DIR / "storyboard_out" / "scene_spec.json"

# --- Keyword → parameter mapping ---
MOOD_COLORS = {
    "neon":     {"primary": "#00eaff", "secondary": "#050505", "accent": "#D4AF37"},
    "gold":     {"primary": "#D4AF37", "secondary": "#0a0a0a", "accent": "#00ff9d"},
    "cyber":    {"primary": "#ff0066", "secondary": "#050505", "accent": "#00eaff"},
    "ocean":    {"primary": "#0066ff", "secondary": "#000505", "accent": "#00ffcc"},
    "ember":    {"primary": "#ff6600", "secondary": "#050000", "accent": "#ffcc00"},
    "void":     {"primary": "#888888", "secondary": "#050505", "accent": "#D4AF37"},
    "matrix":   {"primary": "#00ff41", "secondary": "#000a00", "accent": "#00cc33"},
    "plasma":   {"primary": "#cc00ff", "secondary": "#050005", "accent": "#ff00aa"},
}

CAMERA_MAP = {
    "wide":     {"fov": 75, "pos": [8, 5, 10]},
    "close":    {"fov": 45, "pos": [3, 2, 5]},
    "top":      {"fov": 60, "pos": [0, 12, 0.1]},
    "orbit":    {"fov": 55, "pos": [6, 4, 8]},
    "dutch":    {"fov": 50, "pos": [5, 2, 6], "roll": 0.3},
    "hero":     {"fov": 40, "pos": [4, 3, 7]},
}

GEOMETRY_MAP = {
    "sphere":   {"type": "sphere", "args": [1, 32, 32]},
    "cube":     {"type": "box", "args": [1.5, 1.5, 1.5]},
    "torus":    {"type": "torus", "args": [1, 0.4, 16, 100]},
    "knot":     {"type": "torusknot", "args": [1, 0.3, 128, 32]},
    "icosa":    {"type": "icosahedron", "args": [1, 0]},
    "octa":     {"type": "octahedron", "args": [1, 0]},
    "plane":    {"type": "plane", "args": [10, 10]},
    "cylinder": {"type": "cylinder", "args": [0.5, 0.5, 2, 32]},
    "cone":     {"type": "cone", "args": [0.7, 1.5, 32]},
    "dodeca":   {"type": "dodecahedron", "args": [1, 0]},
}

EFFECTS_MAP = {
    "bloom":     {"pass": "UnrealBloomPass", "strength": 0.8, "radius": 0.4, "threshold": 0.85},
    "chromatic": {"pass": "ChromaticAberrationPass", "amount": 0.003},
    "scanline":  {"type": "scanline", "density": 0.5},
    "glitch":    {"type": "glitch", "intensity": 0.1},
    "fire":      {"type": "fire", "particles": 500},
    "water":     {"type": "water", "waves": 12},
    "neural":    {"type": "neural", "nodes": 200},
}

# --- Prompt parsing ---
def parse_prompt(prompt: str) -> dict:
    text = prompt.lower()
    spec = {
        "prompt": prompt,
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:12],
        "mood": "void",
        "camera": CAMERA_MAP["orbit"],
        "objects": [{"type": "torusknot", "color": "#D4AF37", "metalness": 0.95, "roughness": 0.05}],
        "effects": ["bloom"],
        "particles": True,
        "background": "#050505",
        "duration": 6.0,
        "fps": 30,
    }

    # Mood detection
    for mood, colors in MOOD_COLORS.items():
        if mood in text:
            spec["mood"] = mood
            spec["colors"] = colors
            break

    # Camera detection
    for cam_name, cam_params in CAMERA_MAP.items():
        if cam_name in text:
            spec["camera"] = cam_params
            break

    # Geometry detection
    obj_found = False
    for geo_name, geo_params in GEOMETRY_MAP.items():
        if geo_name in text:
            spec["objects"][0]["type"] = geo_params["type"]
            spec["objects"][0]["args"] = geo_params["args"]
            obj_found = True
            break

    # Effect detection
    spec["effects"] = []
    for eff_name in EFFECTS_MAP:
        if eff_name in text:
            spec["effects"].append(eff_name)

    # Particle detection
    spec["particles"] = any(w in text for w in ["particle", "stars", "dust", "snow", "fire"])

    # Duration
    dur_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:sec|s|seconds?|s)', text)
    if dur_match:
        spec["duration"] = float(dur_match.group(1))

    return spec


def spec_to_frames(spec: dict) -> list[dict]:
    """Generate 5 key frame specs from a scene spec."""
    frames = []
    moods = ["opening", "build", "peak", "fall", "resolve"]
    camera_offsets = [
        [0, 0, 0],      # opening — default
        [2, 1, 3],      # build — closer
        [0, 3, 0],      # peak — top angle
        [-2, -1, -3],   # fall — opposite
        [0, 0, 0],      # resolve — return
    ]

    for i, (mood, offset) in enumerate(zip(moods, camera_offsets)):
        t = i / 4.0  # 0.0, 0.25, 0.5, 0.75, 1.0
        cam = spec["camera"].copy()
        cam["pos"] = [
            spec["camera"]["pos"][0] + offset[0] + spec["camera"]["pos"][0] * t * 0.3,
            spec["camera"]["pos"][1] + offset[1],
            spec["camera"]["pos"][2] + offset[2],
        ]
        frames.append({
            "frame": i + 1,
            "mood": mood,
            "time": round(t * spec["duration"], 2),
            "camera": cam,
            "objects": spec["objects"],
            "effects": spec["effects"],
            "colors": spec.get("colors", MOOD_COLORS.get(spec["mood"], MOOD_COLORS["void"])),
            "particles": spec["particles"],
            "background": spec["background"],
        })
    return frames


def main():
    if len(sys.argv) < 2:
        print("Usage: storyboard.py <prompt> [output_dir]")
        print()
        print("Examples:")
        print('  storyboard.py "neon torus knot with bloom in wide shot"')
        print('  storyboard.py "gold icosahedron orbit camera 8 sec"')
        print('  storyboard.py "cyber sphere particles closeup"')
        sys.exit(1)

    prompt = sys.argv[1]
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else SPEC_OUT
    out_dir.mkdir(parents=True, exist_ok=True)

    spec = parse_prompt(prompt)
    frames = spec_to_frames(spec)

    result = {
        "spec": spec,
        "frames": frames,
        "version": "1.0.0",
        "source": "fleet-waves-prompt-parser",
    }

    out_path = out_dir / "scene_spec.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print(f"\n✅ Storyboard spec → {out_path}")
    print(f"   Prompt: {spec['prompt'][:60]}...")
    print(f"   Mood: {spec['mood']} | Objects: {len(spec['objects'])} | Frames: {len(frames)}")


if __name__ == "__main__":
    main()
