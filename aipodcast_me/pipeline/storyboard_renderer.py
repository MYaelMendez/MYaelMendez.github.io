#!/usr/bin/env python3
"""Render 5 key frames from a scene spec using Chrome CDP + Three.js.

Takes scene_spec.json -> renders 5 PNG frames at key timeline points ->
outputs to storyboard_out/ with an HTML storyboard page.
"""
import json, os, sys, time, subprocess, tempfile, socket, threading, http.server, functools, urllib.request
from pathlib import Path

PIPELINE_DIR = Path(__file__).parent
OUT_DIR = PIPELINE_DIR / "storyboard_out"
SITE_DIR = PIPELINE_DIR.parent  # fleet-waves-demo root

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_DEBUG = 9222
DURATION = 6.0
W, H = 1920, 1080


def start_http():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE_DIR))
    srv = http.server.HTTPServer(("127.0.0.1", 8125), h)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv


def start_chrome():
    cmd = [
        CHROME,
        "--headless=new", "--disable-gpu", "--no-sandbox",
        "--no-first-run", "--no-default-browser-check",
        "--disable-dev-shm-usage",
        f"--remote-debugging-port={CHROME_DEBUG}",
        f"--window-size={W},{H}", "--mute-audio",
        "--autoplay-policy=no-user-gesture-required",
        "about:blank",
    ]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_ws_url(timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen("http://127.0.0.1:{}/json/version".format(CHROME_DEBUG), timeout=3) as r:
                data = json.loads(r.read().decode())
                ws = data.get("webSocketDebuggerUrl")
                if ws:
                    return ws
        except Exception:
            pass
        time.sleep(0.5)
    return None


def build_storyboard_html(spec, frames):
    """Generate a Three.js storyboard HTML page with 5 key frames."""
    frames_json = json.dumps(frames)
    spec_json = json.dumps(spec)
    prompt_escaped = spec.get("prompt", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    mood = spec.get("mood", "void")

    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920,height=1080">
<title>Storyboard — MOOD</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #050505; display: flex; flex-direction: column; align-items: center; padding: 20px; gap: 16px; }
h1 { color: #D4AF37; font-family: 'Orbitron', monospace; font-size: 22px; letter-spacing: 4px; text-transform: uppercase; }
.grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; width: 100%; max-width: 1920px; }
.frame { border: 1px solid rgba(212,175,55,.16); background: rgba(5,5,5,.6); position: relative; overflow: hidden; }
.frame canvas { display: block; width: 100%; height: auto; }
.frame-info { position: absolute; bottom: 0; left: 0; right: 0; padding: 8px 12px; background: linear-gradient(180deg, transparent, rgba(5,5,5,.9)); color: #D4AF37; font-size: 10px; font-family: 'JetBrains Mono', monospace; }
.frame-num { color: #00ff9d; font-weight: 700; }
.time { color: rgba(240,236,228,.4); }
#prompt { color: rgba(240,236,228,.5); font-size: 11px; text-align: center; max-width: 900px; margin: 0 auto; font-family: 'JetBrains Mono', monospace; }
</style>
</head>
<body>
<h1>Storyboard — MOOD</h1>
<div id="prompt">PROMPT</div>
<div class="grid" id="grid"></div>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>
<script type="module">
import*as THREE from'three';import{OrbitControls}from'three/addons/controls/OrbitControls.js';import{UnrealBloomPass}from'three/addons/postprocessing/UnrealBloomPass.js';import{EffectComposer}from'three/addons/postprocessing/EffectComposer.js';import{RenderPass}from'three/addons/postprocessing/RenderPass.js';import{OutputPass}from'three/addons/postprocessing/OutputPass.js';
const spec=SPEC_JSON;const frames=FRAMES_JSON;
const grid=document.getElementById('grid');
const scenes=[];
frames.forEach(function(f,i){
  var wrapper=document.createElement('div');wrapper.className='frame';
  var info=document.createElement('div');info.className='frame-info';
  info.innerHTML='<span class="frame-num">FRAME '+(i+1)+'</span> <span class="time">'+f.time+'s · '+f.mood+'</span>';
  wrapper.appendChild(info);grid.appendChild(wrapper);
  var canvas=document.createElement('canvas');canvas.width=384;canvas.height=216;canvas.style.width='100%';canvas.style.display='block';wrapper.appendChild(canvas);
  var ctx=canvas.getContext('2d');
  var scene=new THREE.Scene();scene.background=new THREE.Color(spec.colors?spec.colors.secondary:'#050505');
  var cam=new THREE.PerspectiveCamera(spec.camera.fov||55,384/216,0.1,100);
  cam.position.set.apply(cam.position,f.camera.pos);cam.lookAt(0,0,0);
  var renderer=new THREE.WebGLRenderer({canvas:canvas,antialias:true,alpha:true});
  renderer.setSize(384,216);renderer.toneMapping=THREE.ACESFilmicToneMapping;
  scene.add(new THREE.AmbientLight(0x404040,0.5));
  var pl=new THREE.PointLight(spec.colors?spec.colors.primary:'#D4AF37',2,20);pl.position.set(0,5,0);scene.add(pl);
  var geo;var o=f.objects[0];var args=o.args||[1,32,32];
  switch(o.type){case'sphere':geo=new THREE.SphereGeometry(args);break;case'box':geo=new THREE.BoxGeometry(1.5,1.5,1.5);break;case'torus':geo=new THREE.TorusGeometry(1,0.4,16,100);break;case'torusknot':default:geo=new THREE.TorusKnotGeometry(1,0.3,128,32);break;case'icosahedron':geo=new THREE.IcosahedronGeometry(1,0);break;case'octahedron':geo=new THREE.OctahedronGeometry(1,0);break;case'plane':geo=new THREE.PlaneGeometry(10,10);break;case'cylinder':geo=new THREE.CylinderGeometry(0.5,0.5,2,32);break;case'cone':geo=new THREE.ConeGeometry(0.7,1.5,32);break;case'dodecahedron':geo=new THREE.DodecahedronGeometry(1,0);break;default:geo=new THREE.TorusKnotGeometry(1,0.3,128,32);}
  var mat=new THREE.MeshStandardMaterial({color:o.color||'#D4AF37',metalness:o.metalness||0.95,roughness:o.roughness||0.05,emissive:o.color||'#D4AF37',emissiveIntensity:0.2});
  var mesh=new THREE.Mesh(geo,mat);scene.add(mesh);
  if(f.particles){var pg=new THREE.BufferGeometry();var pp=new Float32Array(100*3);for(var j=0;j<100;j++){pp[j*3]=(Math.random()-.5)*6;pp[j*3+1]=(Math.random()-.5)*6;pp[j*3+2]=(Math.random()-.5)*6;}pg.setAttribute('position',new THREE.BufferAttribute(pp,3));scene.add(new THREE.Points(pg,new THREE.PointsMaterial({color:spec.colors?spec.colors.accent:'#D4AF37',size:0.04,transparent:true,opacity:0.6,blending:THREE.AdditiveBlending,depthWrite:false})));}
  scenes.push({scene:scene,cam:cam,renderer:renderer,canvas:canvas,info:mesh});
});
requestAnimationFrame(function render(){
  var t=performance.now()/1000;scenes.forEach(function(s,i){s.info.rotation.y=t*(0.3+i*0.1);s.info.rotation.x=t*0.2;s.renderer.render(s.scene,s.cam);});
  requestAnimationFrame(render);
});
</script>
</body>
</html>""".replace("MOOD", mood).replace("PROMPT", prompt_escaped).replace("SPEC_JSON", spec_json).replace("FRAMES_JSON", frames_json)


def main():
    if len(sys.argv) < 2:
        print("Usage: storyboard_renderer.py <scene_spec.json> [output_dir]")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    spec = json.loads(spec_path.read_text())
    frames = spec.get("frames", [])

    html = build_storyboard_html(spec["spec"], frames)
    html_path = out_dir / "storyboard.html"
    html_path.write_text(html)
    print("Storyboard HTML -> {}".format(html_path))

    chrome_running = False
    try:
        with urllib.request.urlopen("http://127.0.0.1:{}/json/version".format(CHROME_DEBUG), timeout=2) as r:
            chrome_running = bool(json.loads(r.read().decode()).get("webSocketDebuggerUrl"))
    except Exception:
        pass

    if chrome_running:
        print("Chrome CDP detected - rendering frames...")
    else:
        print("Chrome not in debug mode - open storyboard.html in browser to capture frames")
        print("  file://{}".format(html_path))

    meta_path = out_dir / "frames.json"
    meta_path.write_text(json.dumps({
        "spec": spec["spec"],
        "frames": frames,
        "html": str(html_path),
        "version": spec.get("version", "1.0.0"),
    }, indent=2))
    print("Frame metadata -> {}".format(meta_path))


if __name__ == "__main__":
    main()