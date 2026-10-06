#!/usr/bin/env python3
"""Prompt-to-Storyboard Pipeline — Fleet Waves exponential loop, step 1.

Usage:
  storyboard.py "neon torus knot with bloom in wide shot"
  storyboard.py "gold icosahedron orbit camera 8 sec"
  storyboard.py "cyber sphere particles closeup"

Pipeline:
  1. Parse prompt -> scene_spec.json
  2. Generate 5 key frame specs
  3. Render storyboard.html (Three.js, 5 canvases)
  4. Output: storyboard_out/
"""
import json, os, sys, time, hashlib
from pathlib import Path

PIPELINE_DIR = Path(__file__).parent
SPEC_OUT = PIPELINE_DIR / "storyboard_out"


def main():
    if len(sys.argv) < 2:
        print("Usage: storyboard.py '<prompt>' [output_dir]")
        print()
        print("Examples:")
        print("  storyboard.py 'neon torus knot with bloom in wide shot'")
        print("  storyboard.py 'gold icosahedron orbit camera 8 sec'")
        print("  storyboard.py 'cyber sphere particles closeup'")
        sys.exit(1)

    prompt = sys.argv[1]
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else SPEC_OUT
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("FLEET WAVES — Prompt-to-Storyboard Pipeline v1.0.0")
    print("=" * 60)
    print()
    print("Prompt: {}".format(prompt))

    # Step 1: Parse prompt
    print("\n[1/4] Parsing prompt...")
    sys.path.insert(0, str(PIPELINE_DIR))
    from prompt_parser import parse_prompt, spec_to_frames

    spec = parse_prompt(prompt)
    frames = spec_to_frames(spec)
    print("  Mood: {}".format(spec["mood"]))
    print("  Camera: {}".format(spec["camera"]))
    print("  Objects: {}".format(spec["objects"]))
    print("  Effects: {}".format(spec["effects"]))
    print("  Frames: {}".format(len(frames)))

    # Save spec
    spec_path = out_dir / "scene_spec.json"
    spec_path.write_text(json.dumps({"spec": spec, "frames": frames, "version": "1.0.0", "source": "fleet-waves-pipeline"}, indent=2))
    print("  -> scene_spec.json")

    # Step 2: Render storyboard HTML
    print("\n[2/4] Building storyboard HTML...")
    from storyboard_renderer import build_storyboard_html
    html = build_storyboard_html(spec, frames)
    html_path = out_dir / "storyboard.html"
    html_path.write_text(html)
    print("  -> storyboard.html")

    # Step 3: Check Chrome CDP for frame capture
    print("\n[3/4] Checking Chrome CDP...")
    import urllib.request
    CHROME_DEBUG = 9222
    chrome_running = False
    try:
        with urllib.request.urlopen("http://127.0.0.1:{}/json/version".format(CHROME_DEBUG), timeout=2) as r:
            data = json.loads(r.read().decode())
            if data.get("webSocketDebuggerUrl"):
                chrome_running = True
                print("  Chrome CDP available")
    except Exception:
        pass

    if not chrome_running:
        print("  Chrome not in debug mode")
        print("  Open storyboard.html in browser to capture frames:")
        print("  file://{}".format(html_path))

    # Step 4: Summary
    print("\n[4/4] Summary")
    print("  Prompt hash: {}".format(spec["prompt_hash"]))
    print("  Output dir:  {}".format(out_dir))
    print("  Files:")
    for f in sorted(out_dir.iterdir()):
        print("    {} ({:,} bytes)".format(f.name, f.stat().st_size))

    print("\n" + "=" * 60)
    print("Storyboard complete — next step: render MP4 from frames")
    print("=" * 60)


if __name__ == "__main__":
    main()