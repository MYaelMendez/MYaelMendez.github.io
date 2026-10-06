#!/usr/bin/env python3
"""Storyboard → Code Mode: generate Three.js code from scene spec.

Reads scene_spec.json → generates Three.js HTML that renders
each key frame with the correct camera, geometry, lighting, effects.

Part of the Fleet Waves exponential loop:
  Prompt → Storyboard → Code → Render → Digest
"""
import json, sys, os, hashlib
from pathlib import Path

PIPELINE_DIR = Path(__file__).parent
OUT_DIR = PIPELINE_DIR / "storyboard_out"

GEOMETRY_MAP = {
    "sphere":     "new THREE.SphereGeometry({r},32,32)",
    "box":        "new THREE.BoxGeometry(1.5,1.5,1.5)",
    "torus":      "new THREE.TorusGeometry(1,0.4,16,100)",
    "torusknot":  "new THREE.TorusKnotGeometry(1,0.3,128,32)",
    "icosahedron":"new THREE.IcosahedronGeometry(1,0)",
    "octahedron": "new THREE.OctahedronGeometry(1,0)",
    "plane":      "new THREE.PlaneGeometry(10,10)",
    "cylinder":   "new THREE.CylinderGeometry(0.5,0.5,2,32)",
    "cone":       "new THREE.ConeGeometry(0.7,1.5,32)",
    "dodecahedron":"new THREE.DodecahedronGeometry(1,0)",
}


def _geo_code(obj):
    """Get geometry JS code for an object descriptor."""
    geo_type = obj.get("type", "torusknot")
    color = obj.get("color", "#D4AF37")
    metalness = obj.get("metalness", 0.95)
    roughness = obj.get("roughness", 0.05)
    ei = obj.get("emissiveIntensity", 0.2)

    if geo_type == "sphere":
        geo = "new THREE.SphereGeometry(1,32,32)"
    elif geo_type == "box":
        geo = "new THREE.BoxGeometry(1.5,1.5,1.5)"
    elif geo_type == "torus":
        geo = "new THREE.TorusGeometry(1,0.4,16,100)"
    elif geo_type == "torusknot":
        geo = "new THREE.TorusKnotGeometry(1,0.3,128,32)"
    elif geo_type == "icosahedron":
        geo = "new THREE.IcosahedronGeometry(1,0)"
    elif geo_type == "octahedron":
        geo = "new THREE.OctahedronGeometry(1,0)"
    elif geo_type == "plane":
        geo = "new THREE.PlaneGeometry(10,10)"
    elif geo_type == "cylinder":
        geo = "new THREE.CylinderGeometry(0.5,0.5,2,32)"
    elif geo_type == "cone":
        geo = "new THREE.ConeGeometry(0.7,1.5,32)"
    elif geo_type == "dodecahedron":
        geo = "new THREE.DodecahedronGeometry(1,0)"
    else:
        geo = "new THREE.TorusKnotGeometry(1,0.3,128,32)"

    return geo, color, metalness, roughness, ei


def _effects_js(effects):
    """Generate effects JS code."""
    code = ""
    has_bloom = "bloom" in effects
    if has_bloom:
        code += """
  var render = function(){composer.render();};
  var composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  composer.addPass(new UnrealBloomPass(new THREE.Vector2(1920,1080), 0.8, 0.4, 0.85));
  composer.addPass(new OutputPass());"""
    else:
        code += "var render = function(){renderer.render(scene,camera);};"
    return code, has_bloom


def generate_animation_html(spec, frames):
    """Generate a single Three.js HTML with all 5 frames as timeline animation."""
    mood = spec.get("mood", "void")
    colors = spec.get("colors", {"primary": "#D4AF37", "secondary": "#050505", "accent": "#D4AF37"})
    camera = spec.get("camera", {"fov": 55, "pos": [6, 4, 8]})
    objects = spec.get("objects", [{"type": "torusknot", "color": "#D4AF37", "metalness": 0.95, "roughness": 0.05}])
    effects = spec.get("effects", ["bloom"])
    particles = spec.get("particles", False)
    bg = spec.get("background", "#050505")
    duration = spec.get("duration", 6.0)

    # Build geometry initialization
    obj_init = ""
    obj_anim = ""
    for i, obj in enumerate(objects):
        geo, color, metalness, roughness, ei = _geo_code(obj)
        obj_init += "\n  var geo{i} = {geo};\n  var mat{i} = new THREE.MeshStandardMaterial({{color:'{color}',metalness:{m},roughness:{r},emissive:'{color}',emissiveIntensity:{ei}}});\n  var mesh{i} = new THREE.Mesh(geo{i}, mat{i});\n  scene.add(mesh{i});".format(
            i=i, geo=geo, color=color, m=metalness, r=roughness, ei=ei)
        obj_anim += "\n  mesh{i}.rotation.y = t * {speed};\n  mesh{i}.rotation.x = t * 0.2;".format(
            i=i, speed=0.3 + i * 0.1)

    # Effects
    effects_js, has_bloom = _effects_js(effects)

    # Particles
    particles_code = ""
    if particles:
        accent = colors.get("accent", "#D4AF37")
        particles_code = """
  var pGeo = new THREE.BufferGeometry();
  var pp = new Float32Array(300*3);
  for(var j=0;j<300;j++){{pp[j*3]=(Math.random()-.5)*8;pp[j*3+1]=(Math.random()-.5)*8;pp[j*3+2]=(Math.random()-.5)*8;}}
  pGeo.setAttribute('position',new THREE.BufferAttribute(pp,3));
  scene.add(new THREE.Points(pGeo,new THREE.PointsMaterial({{color:'""" + accent + """',size:0.04,transparent:true,opacity:0.6,blending:THREE.AdditiveBlending,depthWrite:false}})));"""

    # Camera keyframes
    cam_keyframes = ""
    for i, f in enumerate(frames):
        t = f["time"] / duration
        pos = f["camera"]["pos"]
        if i > 0:
            cam_keyframes += ",\n    "
        cam_keyframes += "{{time:" + str(t) + ",pos:[" + str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2]) + "]}}"

    primary = colors.get("primary", "#D4AF37")

    html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920,height=1080">
<title>Storyboard Animation — MOOD — DURATION s</title>
<style>*{margin:0;padding:0}body{background:BGC;overflow:hidden}canvas{display:block}#info{position:fixed;top:16px;left:16px;z-index:10;color:#D4AF37;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase}#time{position:fixed;bottom:16px;left:16px;z-index:10;color:#00ff9d;font-family:'JetBrains Mono',monospace;font-size:14px}</style>
</head>
<body>
<div id="info">Storyboard — MOOD — NFRAMES frames</div>
<div id="time">0.00s</div>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>
<script type="module">
import*as THREE from'three';import{OrbitControls}from'three/addons/controls/OrbitControls.js';import{EffectComposer}from'three/addons/postprocessing/EffectComposer.js';import{RenderPass}from'three/addons/postprocessing/RenderPass.js';import{UnrealBloomPass}from'three/addons/postprocessing/UnrealBloomPass.js';import{OutputPass}from'three/addons/postprocessing/OutputPass.js';
var scene=new THREE.Scene();scene.background=new THREE.Color('BGC');
var camera=new THREE.PerspectiveCamera(FOV,1920/1080,0.1,100);
camera.position.set(CPOS);
var renderer=new THREE.WebGLRenderer({antialias:true});renderer.setSize(1920,1080);renderer.toneMapping=THREE.ACESFilmicToneMapping;document.body.appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0x404040,0.5));
var pl=new THREE.PointLight('PRIMARY',2,20);pl.position.set(0,5,0);scene.add(pl);
OBJ_INIT
PARTICLES
var keyframes=[CAMKEYS];
var currentFrame=0;
function getCamPos(t){{if(keyframes.length<2)return keyframes[0].pos;for(var i=0;i<keyframes.length-1;i++){{if(t>=keyframes[i].time&&t<=keyframes[i+1].time){{var frac=(t-keyframes[i].time)/(keyframes[i+1].time-keyframes[i].time);return keyframes[i].pos.map(function(v,j){{return v+(keyframes[i+1].pos[j]-v)*frac;}});}}}}return keyframes[keyframes.length-1].pos;}}
EFFECTS
var controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
function animate(){{requestAnimationFrame(animate);var t=performance.now()/1000;var dur=DURATION;var normT=t%dur;var pos=getCamPos(normT);camera.position.set(pos[0],pos[1],pos[2]);camera.lookAt(0,0,0);OBJ_ANIM controls.update();render();document.getElementById('time').textContent=normT.toFixed(2)+'s';}}
animate();
</script>
</body>
</html>""".replace("MOOD", mood).replace("DURATION", str(duration)).replace("NFRAMES", str(len(frames))).replace(
        "BGC", bg).replace("FOV", str(camera.get("fov", 55))).replace(
        "CPOS", str(camera["pos"][0]) + "," + str(camera["pos"][1]) + "," + str(camera["pos"][2])).replace(
        "PRIMARY", primary).replace("OBJ_INIT", obj_init).replace(
        "PARTICLES", particles_code).replace("CAMKEYS", cam_keyframes).replace(
        "EFFECTS", effects_js).replace("OBJ_ANIM", obj_anim)

    return html


def generate_frame_html(frame_spec, frame_idx):
    """Generate a single-frame Three.js HTML."""
    mood = frame_spec.get("mood", "void")
    colors = frame_spec.get("colors", {"primary": "#D4AF37", "secondary": "#050505", "accent": "#D4AF37"})
    cam = frame_spec.get("camera", {"fov": 55, "pos": [6, 4, 8]})
    objects = frame_spec.get("objects", [{"type": "torusknot", "color": "#D4AF37", "metalness": 0.95, "roughness": 0.05}])
    effects = frame_spec.get("effects", ["bloom"])
    particles = frame_spec.get("particles", False)
    bg = frame_spec.get("background", "#050505")
    time_val = frame_spec.get("time", 0.0)

    obj_codes = []
    for i, obj in enumerate(objects):
        geo, color, metalness, roughness, ei = _geo_code(obj)
        obj_codes.append("""
  var geo""" + str(i) + """ = """ + geo + """;
  var mat""" + str(i) + """ = new THREE.MeshStandardMaterial({color:'""" + color + """',metalness:""" + str(metalness) + """,roughness:""" + str(roughness) + """,emissive:'""" + color + """',emissiveIntensity:""" + str(ei) + """});
  var mesh""" + str(i) + """ = new THREE.Mesh(geo""" + str(i) + """, mat""" + str(i) + """);
  scene.add(mesh""" + str(i) + """);""")

    obj_code = "\n".join(obj_codes)
    effects_js, _ = _effects_js(effects)

    particles_code = ""
    if particles:
        accent = colors.get("accent", "#D4AF37")
        particles_code = """
  var pGeo = new THREE.BufferGeometry();
  var pp = new Float32Array(200*3);
  for(var j=0;j<200;j++){{pp[j*3]=(Math.random()-.5)*6;pp[j*3+1]=(Math.random()-.5)*6;pp[j*3+2]=(Math.random()-.5)*6;}}
  pGeo.setAttribute('position',new THREE.BufferAttribute(pp,3));
  scene.add(new THREE.Points(pGeo,new THREE.PointsMaterial({color:'""" + accent + """',size:0.04,transparent:true,opacity:0.6,blending:THREE.AdditiveBlending,depthWrite:false})));"""

    html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920,height=1080">
<title>Frame N — MOOD — TIME s</title>
<style>*{margin:0;padding:0}body{background:BGC;overflow:hidden}canvas{display:block}</style>
</head>
<body>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>
<script type="module">
import*as THREE from'three';import{OrbitControls}from'three/addons/controls/OrbitControls.js';import{EffectComposer}from'three/addons/postprocessing/EffectComposer.js';import{RenderPass}from'three/addons/postprocessing/RenderPass.js';import{UnrealBloomPass}from'three/addons/postprocessing/UnrealBloomPass.js';import{OutputPass}from'three/addons/postprocessing/OutputPass.js';
var scene=new THREE.Scene();scene.background=new THREE.Color('BGC');
var camera=new THREE.PerspectiveCamera(FOV,1920/1080,0.1,100);
camera.position.set(CPOS);
var renderer=new THREE.WebGLRenderer({antialias:true});renderer.setSize(1920,1080);renderer.toneMapping=THREE.ACESFilmicToneMapping;document.body.appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0x404040,0.5));
var pl=new THREE.PointLight('PRIMARY',2,20);pl.position.set(0,5,0);scene.add(pl);
OBJ_CODE
PARTICLES
var render;
EFFECTS
var controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
function animate(){requestAnimationFrame(animate);controls.update();render();}
animate();
</script>
</body>
</html>""".replace("MOOD", mood).replace("TIME", str(time_val)).replace("N", str(frame_idx + 1)).replace(
        "BGC", bg).replace("FOV", str(cam.get("fov", 55))).replace(
        "CPOS", str(cam["pos"][0]) + "," + str(cam["pos"][1]) + "," + str(cam["pos"][2])).replace(
        "PRIMARY", colors.get("primary", "#D4AF37")).replace(
        "OBJ_CODE", obj_code).replace("PARTICLES", particles_code).replace("EFFECTS", effects_js)

    return html


def codegen(spec_path, output_dir=None, mode="animation"):
    """Generate Three.js code from a scene spec."""
    spec_data = json.loads(Path(spec_path).read_text())
    spec = spec_data["spec"]
    frames = spec_data["frames"]

    out_dir = Path(output_dir) if output_dir else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {"spec": spec, "mode": mode, "files": []}

    if mode == "frames":
        for i, frame in enumerate(frames):
            html = generate_frame_html(frame, i)
            fname = "frame_{:02d}_{}.html".format(i + 1, frame["mood"])
            fpath = out_dir / fname
            fpath.write_text(html)
            results["files"].append({"file": fname, "mood": frame["mood"], "time": frame["time"]})
    else:
        html = generate_animation_html(spec, frames)
        fname = "storyboard_animation.html"
        fpath = out_dir / fname
        fpath.write_text(html)
        results["files"].append({"file": fname, "frames": len(frames), "duration": spec.get("duration", 6.0)})

    results["prompt_hash"] = spec.get("prompt_hash", "unknown")
    results["mood"] = spec.get("mood", "void")

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: codegen.py <scene_spec.json> [output_dir] [--frames|--animation]")
        print()
        print("Options:")
        print("  --frames      Generate 5 separate frame HTML files")
        print("  --animation   Generate single timeline animation (default)")
        sys.exit(1)

    mode = "frames" if "--frames" in sys.argv else "animation"
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    spec_path = args[0] if len(args) > 0 else None
    output_dir = args[1] if len(args) > 1 else None
    if not spec_path:
        print('Usage: codegen.py <scene_spec.json> [output_dir] [--frames|--animation]')
        sys.exit(1)

    print("=" * 60)
    print("FLEET WAVES — Code Mode: Storyboard → Three.js")
    print("=" * 60)

    results = codegen(spec_path, output_dir, mode)

    print("\nMode: {}".format(mode))
    print("Mood: {}".format(results["mood"]))
    print("Prompt hash: {}".format(results["prompt_hash"]))
    print("\nGenerated files:")
    for f in results["files"]:
        print("  - {}".format(f["file"]))

    out_dir = Path(output_dir) if output_dir else OUT_DIR
    meta_path = out_dir / "codegen.json"
    meta_path.write_text(json.dumps(results, indent=2))
    print("\nMetadata -> {}".format(meta_path))
    print("=" * 60)


if __name__ == "__main__":
    main()