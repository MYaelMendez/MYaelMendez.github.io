"""
Asimov simulator — frame-by-frame renderer.

Takes time as input, computes joint angles, renders frames via Three.js
headless (or PIL fallback), then encodes to MP4/GIF via ffmpeg.

Pure function: jointAngles(t) → full configuration
"""
import subprocess
import shutil
import pathlib
import json
import numpy as np
from PIL import Image

W, H = 720, 1280
FPS = 30
CRF = 20
CODEC = "libx264"
PIX_FMT = "yuv420p"
FASTRESTART = "+faststart"

# ── Joint angle model ────────────────────────────────────────────
# Pure function: time → joint angles
def joint_angles(t):
    """Compute joint angles from time. Pure function of t."""
    j = {}
    gait = (np.sin(t * 4.0) + 1) * 0.5
    j['left_hip_pitch_joint'] = np.sin(t * 2.0) * 0.3
    j['left_knee_joint'] = np.sin(t * 2.0 - 1.0) * 0.5
    j['left_ankle_pitch_joint'] = np.sin(t * 2.0 - 2.0) * 0.2
    j['right_hip_pitch_joint'] = -np.sin(t * 2.0) * 0.3
    j['right_knee_joint'] = -np.sin(t * 2.0 - 1.0) * 0.5
    j['right_ankle_pitch_joint'] = -np.sin(t * 2.0 - 2.0) * 0.2
    j['waist_yaw_joint'] = np.sin(t * 1.5) * 0.15
    j['neck_yaw_joint'] = np.sin(t * 1.0 + 0.5) * 0.1
    j['neck_pitch_joint'] = np.sin(t * 1.0 + 1.0) * 0.05
    j['right_shoulder_pitch_joint'] = np.sin(t * 2.0 + 1.5) * 0.25
    j['right_elbow_joint'] = np.sin(t * 2.0 + 2.5) * 0.2
    j['left_shoulder_pitch_joint'] = np.sin(t * 2.0 - 1.5) * 0.25
    j['left_elbow_joint'] = np.sin(t * 2.0 - 2.5) * 0.2
    return j

def compute_sensors(t):
    """Compute derived sensor values from time."""
    angles = joint_angles(t)
    power = sum(abs(angles[k]) * 0.35 for k in angles) + 12.0
    instability = sum(abs(np.sin(a * 10)) * 0.01 for a in angles.values())
    return {
        'joints_active': sum(1 for a in angles.values() if abs(a) > 0.01),
        'power': power + 12.0,
        'reaction': 18.5 + np.sin(t * 7) * 3.2 + instability * 10,
        'thermal': 42 + power * 1.8 + np.sin(t * 3) * 2,
        'instability': instability,
    }

def render_frame(t, width=W, height=H):
    """Render a single frame as a PIL image (PIL fallback for headless)."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (width, height), (4, 4, 12))
    draw = ImageDraw.Draw(img)

    angles = joint_angles(t)
    s = compute_sensors(t)

    # Background grid
    for i in range(0, width, 40):
        draw.line([(i, 0), (i, height)], fill=(8, 8, 18), width=1)
    for i in range(0, height, 40):
        draw.line([(0, i), (width, i)], fill=(8, 8, 18), width=1)

    # Robot silhouette (simplified polygon from joint angles)
    # Body center
    cx, cy = width // 2, height // 2
    scale = 1.3

    # Legs
    for side in [-1, 1]:
        hip = side * 30 * scale
        knee = hip + side * 10 * scale
        ankle = knee + side * 15 * scale

        # Hip angle
        hip_angle = angles.get('left_hip_pitch_joint', 0) if side == -1 else angles.get('right_hip_pitch_joint', 0)
        # Knee angle
        knee_angle = angles.get('left_knee_joint', 0) if side == -1 else angles.get('right_knee_joint', 0)
        # Ankle angle
        ankle_angle = angles.get('left_ankle_pitch_joint', 0) if side == -1 else angles.get('right_ankle_pitch_joint', 0)

        # Draw leg segments
        draw.line([(cx, cy), (cx + hip, cy + hip_angle * 10)], fill=(0, 234, 255), width=3)
        draw.line([(cx + hip, cy + hip_angle * 10), (cx + knee, cy + knee_angle * 10)], fill=(0, 234, 255), width=3)
        draw.line([(cx + knee, cy + knee_angle * 10), (cx + ankle, cy + ankle_angle * 10)], fill=(0, 234, 255), width=3)

    # Arms
    for side in [-1, 1]:
        shoulder = side * 25 * scale
        elbow = shoulder + side * 8 * scale
        wrist = elbow + side * 12 * scale

        shoulder_angle = angles.get('right_shoulder_pitch_joint', 0) if side == 1 else angles.get('left_shoulder_pitch_joint', 0)
        elbow_angle = angles.get('right_elbow_joint', 0) if side == 1 else angles.get('left_elbow_joint', 0)

        draw.line([(cx, cy + 20), (cx + shoulder, cy + 20 + shoulder_angle * 8)], fill=(0, 234, 255), width=3)
        draw.line([(cx + shoulder, cy + 20 + shoulder_angle * 8), (cx + elbow, cy + 20 + elbow_angle * 8)], fill=(0, 234, 255), width=3)
        draw.line([(cx + elbow, cy + 20 + elbow_angle * 8), (cx + wrist, cy + 20 + wrist * 0.5)], fill=(0, 234, 255), width=3)

    # Torso
    draw.ellipse([cx - 30, cy - 40, cx + 30, cy + 40], fill=(0, 234, 255))

    # Head
    draw.ellipse([cx - 12, cy - 80, cx + 12, cy - 56], fill=(0, 234, 255))
    # Eyes
    draw.ellipse([cx - 6, cy - 75, cx - 2, cy - 70], fill=(255, 255, 255), width=2)
    draw.ellipse([cx + 2, cy - 75, cx + 6, cy - 70], fill=(255, 255, 255), width=2)

    # Instruments overlay
    y = 12
    draw.text((16, y), f"Joints: {s['joints_active']}/25", fill=(180, 255, 234))
    y += 20
    draw.text((16, y), f"Power: {s['power']:.1f} W", fill=(255, 34, 68))
    y += 20
    draw.text((16, y), f"Reaction: {s['reaction']:.1f} ms", fill=(0, 234, 255))
    y += 20
    draw.text((16, y), f"Thermal: {s['thermal']:.1f} °C", fill=(255, 100, 100))
    y += 20
    draw.text((16, y), f"Instability: {s['instability']:.2f}", fill=(255, 200, 100))

    # Title
    draw.text((width//2 - 100, 12), "æsymov · 25 DOF", fill=(0, 234, 255))

    return img

def render_frames(t_start, t_end, output_dir, fps=30):
    """Render all frames and save as PNG sequence."""
    outdir = pathlib.Path(output_dir)
    if outdir.exists():
        import shutil
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    n_frames = int((t_end - t_start) * fps)
    for i in range(n_frames):
        t = t_start + i / fps
        img = render_frame(t)
        img.save(outdir / f"{i:05d}.png")
        if (i + 1) % 100 == 0:
            print(f"  rendered {i+1}/{n_frames} frames")

    return outdir, n_frames

def encode_to_mp4(frames_dir, output, fps=FPS, duration=8):
    """Encode PNG sequence to MP4 via ffmpeg."""
    out = pathlib.Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "%05d.png"),
        "-c:v", CODEC,
        "-pix_fmt", PIX_FMT,
        "-movflags", FASTRESTART,
        "-crf", str(CRF),
        str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        return {"success": False, "error": r.stderr[-500:]}
    return {"success": True, "output": str(out), "frames": fps * duration}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        import json
        frames_dir, n = render_frames(0, 8, "/tmp/asimov-cad-frames")
        result = encode_to_mp4(frames_dir, "/tmp/asimov-cad-demo.mp4")
        print(json.dumps(result, indent=2))
    else:
        frames_dir, n = render_frames(0, 8, "/tmp/asimov-cad-frames")
        print(f"Rendered {n} frames to {frames_dir}")
