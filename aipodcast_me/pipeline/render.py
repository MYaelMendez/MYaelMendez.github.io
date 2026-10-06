#!/usr/bin/env python3
"""Storyboard → MP4 render via PIL + ffmpeg.

Generates frames from scene spec using PIL (no Chrome needed).
Encodes with ffmpeg libx264 (NVENC blocked, driver 592 < 610).

Pipeline:
  storyboard.py → scene_spec.json
  codegen.py → storyboard_animation.html
  render.py → storyboard.mp4
"""
import json, sys, os, math, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

PIPELINE_DIR = Path(__file__).parent
OUT_DIR = PIPELINE_DIR / "storyboard_out"
W, H = 1920, 1080
FPS = 30


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_geometry(draw, geo_type, cx, cy, size, color, frame_idx, total_frames):
    """Draw a geometric shape."""
    if geo_type == "sphere":
        r = int(size * 80)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=color)
    elif geo_type == "box":
        s = int(size * 100)
        draw.rectangle([cx-s, cy-s, cx+s, cy+s], fill=color, outline=color)
    elif geo_type == "torus":
        r = int(size * 80)
        for i in range(3):
            rr = r + i * 15
            draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], outline=color, width=3)
    elif geo_type == "torusknot":
        r = int(size * 70)
        # Draw torus knot as interleaved rings
        for i in range(6):
            angle = i * math.pi / 3
            ox = int(cx + r * math.cos(angle))
            oy = int(cy + r * math.sin(angle))
            draw.ellipse([ox-15, oy-15, ox+15, oy+15], fill=color)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=2)
    elif geo_type == "icosahedron":
        r = int(size * 80)
        # Draw icosahedron as diamond shapes
        for i in range(5):
            angle = i * math.pi * 2 / 5
            ox = int(cx + r * math.cos(angle))
            oy = int(cy + r * math.sin(angle))
            draw.polygon([(cx, cy), (ox, oy),
                         (cx + int(r*0.3*math.cos(angle+math.pi/5)),
                          cy + int(r*0.3*math.sin(angle+math.pi/5)))],
                         outline=color, fill=color)
    elif geo_type == "octahedron":
        r = int(size * 80)
        draw.polygon([(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)],
                     fill=color, outline=color)
    elif geo_type == "plane":
        s = int(size * 200)
        draw.rectangle([cx-s, cy-s, cx+s, cy+s], outline=color, width=2)
    elif geo_type == "cylinder":
        r = int(size * 50)
        h = int(size * 120)
        draw.ellipse([cx-r, cy-h, cx+r, cy+h], outline=color, width=3)
    elif geo_type == "cone":
        r = int(size * 60)
        h = int(size * 130)
        draw.polygon([(cx, cy-h), (cx-r, cy+h), (cx+r, cy+h)],
                     fill=color, outline=color)
    elif geo_type == "dodecahedron":
        r = int(size * 80)
        # Draw dodecahedron as pentagon arrangement
        for i in range(5):
            angle = i * math.pi * 2 / 5 - math.pi/2
            ox = int(cx + r * 0.6 * math.cos(angle))
            oy = int(cy + r * 0.6 * math.sin(angle))
            draw.regular_polygon((ox, oy, int(r*0.5)), 5, fill=color, outline=color)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=2)
    else:
        r = int(size * 70)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=color)


def draw_particles(draw, cx, cy, count, color, frame_idx, total_frames):
    """Draw particle effect."""
    import random
    random.seed(frame_idx * 137 + 42)
    for _ in range(count):
        angle = random.random() * math.pi * 2
        dist = random.random() * 300 + 50
        px = int(cx + dist * math.cos(angle))
        py = int(cy + dist * math.sin(angle))
        size = random.randint(2, 6)
        draw.ellipse([px-size, py-size, px+size, py+size], fill=color)


def draw_scanlines(draw, frame_idx, total_frames):
    """Draw CRT scanlines overlay."""
    for y in range(0, H, 4):
        alpha = int(30 + 10 * math.sin(frame_idx * 0.5 + y * 0.01))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha), width=1)


def draw_vignette(draw, cx, cy, max_r):
    """Draw vignette effect."""
    for r in range(max_r, 0, -5):
        alpha = int(255 * (1 - r / max_r) * 0.5)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(0, 0, 0, alpha), width=5)


def render_frame(spec, frame_spec, frame_idx, output_dir):
    """Render a single frame as PNG."""
    colors = frame_spec.get("colors", {"primary": "#D4AF37", "secondary": "#050505", "accent": "#D4AF37"})
    mood = frame_spec.get("mood", "void")
    bg = frame_spec.get("background", "#050505")
    objects = frame_spec.get("objects", [{"type": "torusknot", "color": "#D4AF37"}])
    effects = frame_spec.get("effects", ["bloom"])
    particles = frame_spec.get("particles", False)
    time_val = frame_spec.get("time", 0.0)

    # Create image
    img = Image.new("RGBA", (W, H), hex_to_rgb(bg))
    draw = ImageDraw.Draw(img, "RGBA")

    # Background gradient
    primary_rgb = hex_to_rgb(colors.get("primary", "#D4AF37"))
    secondary_rgb = hex_to_rgb(colors.get("secondary", "#050505"))
    for y in range(H):
        t = y / H
        r = int(secondary_rgb[0] * (1-t) + primary_rgb[0] * t * 0.1)
        g = int(secondary_rgb[1] * (1-t) + primary_rgb[1] * t * 0.1)
        b = int(secondary_rgb[2] * (1-t) + primary_rgb[2] * t * 0.1)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Central glow
    cx, cy = W // 2, H // 2
    glow_r = 400
    for r in range(glow_r, 0, -10):
        alpha = int(30 * (1 - r / glow_r))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(primary_rgb[0], primary_rgb[1], primary_rgb[2], alpha))

    # Draw objects
    for i, obj in enumerate(objects):
        geo_type = obj.get("type", "torusknot")
        color = hex_to_rgb(obj.get("color", "#D4AF37"))
        size = 0.5 + i * 0.15
        # Animate position
        angle = time_val * 0.5 + i * math.pi * 2 / len(objects)
        ox = int(cx + 150 * math.cos(angle))
        oy = int(cy + 150 * math.sin(angle * 0.7))
        draw_geometry(draw, geo_type, ox, oy, size, color, frame_idx, 5)

    # Draw particles
    if particles:
        accent_rgb = hex_to_rgb(colors.get("accent", "#D4AF37"))
        draw_particles(draw, cx, cy, 100, accent_rgb + (180,), frame_idx, 5)

    # Bloom effect (simple blur)
    if "bloom" in effects:
        img = img.filter(ImageFilter.GaussianBlur(radius=3))

    # Scanlines
    draw_scanlines(draw, frame_idx, 5)

    # Vignette
    draw_vignette(draw, cx, cy, 700)

    # Save frame
    fname = "frame_{:06d}.png".format(frame_idx)
    fpath = output_dir / fname
    img.save(str(fpath))
    return fpath


def render_video(spec_path, output_path, duration=6.0, fps=FPS):
    """Render storyboard spec to MP4."""
    spec_data = json.loads(Path(spec_path).read_text())
    spec = spec_data["spec"]
    frames = spec_data["frames"]

    out_dir = OUT_DIR / "frames"
    out_dir.mkdir(exist_ok=True)

    # Clean old frames
    for f in out_dir.glob("frame_*.png"):
        f.unlink()

    duration = spec.get("duration", duration)
    total_frames = int(duration * fps)

    print("Generating {} frames @ {}fps ({}s)...".format(total_frames, fps, duration))

    for i in range(total_frames):
        t = i / fps
        # Find current frame spec (interpolate between key frames)
        frame_spec = frames[0]
        for j, f in enumerate(frames):
            if t <= f["time"]:
                frame_spec = f
                break
            if j == len(frames) - 1:
                frame_spec = frames[-1]

        render_frame(spec, frame_spec, i, out_dir)
        if (i + 1) % 30 == 0:
            print("  Frame {}/{}".format(i + 1, total_frames))

    print("[4/5] Encoding MP4 with ffmpeg...")
    ffmpeg = r"C:\Users\yaelm\AppData\Local\hermes\tools\ffmpeg-9.0.1-win32-x64\bin\ffmpeg.exe"
    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", str(out_dir / "frame_%06d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "23",
        "-movflags", "+faststart",
        str(output_path),
    ]
    import subprocess
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print("  ffmpeg error: {}".format(result.stderr[-300:]))
        return None

    size_kb = output_path.stat().st_size / 1024 if output_path.exists() else 0
    return {"path": str(output_path), "size_kb": size_kb, "frames": total_frames}


def main():
    if len(sys.argv) < 2:
        print("Usage: render.py <scene_spec.json> [output.mp4] [--duration=N] [--fps=N]")
        sys.exit(1)

    spec_path = sys.argv[1]
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(spec_path).parent / "storyboard.mp4"

    duration = 6.0
    fps = FPS
    for arg in sys.argv[2:]:
        if arg.startswith("--duration="):
            duration = float(arg.split("=")[1])
        elif arg.startswith("--fps="):
            fps = int(arg.split("=")[1])

    print("=" * 60)
    print("FLEET WAVES — Render: Storyboard → MP4")
    print("=" * 60)
    print("Input:  {}".format(spec_path))
    print("Output: {}".format(output_path))
    print("Duration: {}s @ {}fps".format(duration, fps))
    print()

    result = render_video(spec_path, output_path, duration, fps)

    if result:
        print("\nRendered: {} ({:.1f} KB, {} frames)".format(
            result["path"], result["size_kb"], result["frames"]))
    else:
        print("\nRender failed")
        sys.exit(1)


if __name__ == "__main__":
    main()