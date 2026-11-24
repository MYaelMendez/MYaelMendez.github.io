"""Export a self-contained WebGL qpos viewer from the repo model + runtime trace.

Reads HERMES_AE_MESHES (or bundled/runtime default), model/urdf.json and
physics_free_trace.json, then writes webgl/qpos_viewer.html with embedded data.
No meshes or data files are fetched at runtime; only Three.js loads from CDN.
"""
import json, os, struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MESHES = Path(os.environ.get('HERMES_AE_MESHES',
                             Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes')) / 'ae' / 'model' / 'meshes'))
ANIM = Path(os.environ.get('HERMES_AE_ANIM',
                           Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes')) / 'ae' / 'asimov-anim'))
URDF = json.loads((ROOT / 'model' / 'urdf.json').read_text())
TRACE = json.loads((ANIM / 'physics_free_trace.json').read_text())
OUT = ROOT / 'webgl' / 'qpos_viewer.html'
SAMPLE = 180


def stl_points(path, limit):
    raw = path.read_bytes()
    n = struct.unpack('<I', raw[80:84])[0]
    tri = np.frombuffer(raw, dtype=np.uint8, offset=84, count=50 * n).reshape(n, 50)
    v = np.frombuffer(tri[:, 12:48].tobytes(), dtype='<f4').reshape(n, 3, 3)[:, 1:, :].reshape(-1, 3)
    step = max(1, len(v) // limit)
    return [[round(float(x), 5) for x in p] for p in v[::step]]


try:
    import numpy as np
except Exception as e:
    raise SystemExit(f'numpy required: {e}')

points = {}
for name, info in URDF['links'].items():
    p = MESHES / info['mesh']
    if p.exists():
        points[name] = stl_points(p, SAMPLE)

if not points:
    raise SystemExit(f'no meshes found under {MESHES}')

data = {
    'points': points,
    'links': list(URDF['links'].keys()),
    'joints': URDF['joints'],
    'qpos': TRACE['qpos'],
    'com': TRACE['com'],
    'joint_names': TRACE['joint_names'],
    'joint_refs': TRACE['joint_refs'],
    'model': TRACE['model'],
}

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>>_æ: Asimov qpos viewer</title>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js"}}
</script>
<style>
:root{--fg:#00ff9f;--bg:#030a07;--mut:#0a6647}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);font-family:ui-monospace,monospace}
#wrap{display:flex;gap:12px;padding:12px;height:100vh} #stage{flex:1;border:1px solid var(--mut)}
#side{width:260px;display:flex;flex-direction:column;gap:10px} h1{font-size:18px;margin:0}
button,input{font-family:inherit;background:#06160f;color:var(--fg);border:1px solid var(--mut);padding:6px}
#status{font-size:12px;line-height:1.6;color:#9fffd4;white-space:pre-wrap}
.small{font-size:11px;color:#69c9a3}
</style>
</head>
<body>
<div id="wrap"><div id="stage"></div><div id="side">
<h1>>_æ: ASIMOV</h1>
<div class="small">qpos viewer · Studio v2.2 trace<br>__MODEL__</div>
<button id="play">▶ PLAY</button>
<input id="scrub" type="range" min="0" max="215" value="0">
<div>
<button data-view="front">FRONT</button>
<button data-view="three">3/4</button>
<button data-view="wide">WIDE</button>
<button data-view="close">CLOSE</button>
</div>
<div id="status"></div>
<div class="small">HUMAN://ROOT · receipts on every action</div>
</div></div>
<script type="module">
import * as THREE from 'three';
const D=__DATA__;
const scene=new THREE.Scene(); scene.background=new THREE.Color(0x030a07);
const camera=new THREE.OrthographicCamera(-0.45,0.45,0.8,-0.8,0.01,100);
camera.position.set(0,0.65,3); camera.lookAt(0,0.65,0);
const renderer=new THREE.WebGLRenderer({antialias:true}); renderer.setPixelRatio(Math.min(devicePixelRatio,2));
document.getElementById('stage').appendChild(renderer.domElement);
function resize(){const w=document.getElementById('stage').clientWidth,h=document.getElementById('stage').clientHeight;renderer.setSize(w,h)}
addEventListener('resize',resize); resize();
scene.add(new THREE.HemisphereLight(0x00ff9f,0x020804,0.8));
const stage=new THREE.Group(); scene.add(stage);
const viewQ=new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0),THREE.MathUtils.degToRad(78))
  .multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(-Math.PI/2,0,0,'XYZ')));
stage.quaternion.copy(viewQ);
const groups={};
for(const n of D.links) groups[n]=new THREE.Group();
for(const j of D.joints){
  const p=groups[j.parent],c=groups[j.child];
  c.position.set(j.xyz[0],j.xyz[1],j.xyz[2]);
  p.add(c);
}
stage.add(groups['pelvis_link']);
const mat=new THREE.PointsMaterial({color:0x00ff9f,size:0.006,sizeAttenuation:true,transparent:true,opacity:0.85});
for(const n of D.links){
  const a=D.points[n]; if(!a||!a.length) continue;
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(a.flat(),3));
  groups[n].add(new THREE.Points(g,mat));
}
const qtmp=new THREE.Quaternion();
function setFrame(i){
  i=Math.max(0,Math.min(D.qpos.length-1,i));
  const q=D.qpos[i], base=q.slice(0,7);
  groups['pelvis_link'].position.set(base[0],base[1],base[2]);
  groups['pelvis_link'].quaternion.set(base[3],base[4],base[5],base[6]);
  for(let k=0;k<D.joint_names.length;k++){
    const name=D.joint_names[k], j=D.joints.find(x=>x.name===name); if(!j) continue;
    const angle=q[7+k]-D.joint_refs[k];
    const q0=new THREE.Quaternion().setFromEuler(new THREE.Euler(j.rpy[0],j.rpy[1],j.rpy[2],'XYZ'));
    const qa=new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(...j.axis),angle);
    groups[j.child].quaternion.copy(q0.multiply(qa));
  }
  const com=D.com[i], bx=base[0];
  document.getElementById('status').textContent=
    `frame ${i}/${D.qpos.length-1}\\nbase x ${bx.toFixed(3)} m\\nCOM x ${com[0].toFixed(3)} m\\nCOM z ${com[2].toFixed(3)} m\\nactive ${D.joint_names.filter((n,k)=>Math.abs(q[7+k]-D.joint_refs[k])>0.01).length}/25`;
  renderer.render(scene,camera);
}
let frame=0,playing=false,t0=performance.now();
const scrub=document.getElementById('scrub');
scrub.max=D.qpos.length-1;
scrub.oninput=()=>{frame=+scrub.value;setFrame(frame)};
document.getElementById('play').onclick=e=>{playing=!playing;e.target.textContent=playing?'❚❚ PAUSE':'▶ PLAY';t0=performance.now()};
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{
  const v=b.dataset.view;
  const yaw=v==='front'?90:78;
  stage.quaternion.setFromAxisAngle(new THREE.Vector3(0,1,0),THREE.MathUtils.degToRad(yaw))
    .multiply(new THREE.Quaternion().setFromEuler(new THREE.Euler(-Math.PI/2,0,0,'XYZ')));
  camera.zoom=v==='wide'?0.7:v==='close'?1.6:1; camera.updateProjectionMatrix(); setFrame(frame);
});
function loop(){const now=performance.now();if(playing&&now-t0>41.66){frame=(frame+1)%D.qpos.length;scrub.value=frame;t0=now;setFrame(frame)}requestAnimationFrame(loop)}
loop(); setFrame(0);
</script>
</body>
</html>
'''
html = html.replace('__DATA__', json.dumps(data, separators=(',', ':'))).replace('__MODEL__', data['model'])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html)
print(json.dumps({'success': True, 'output': str(OUT), 'bytes': OUT.stat().st_size,
                  'points': sum(len(v) for v in points.values()), 'frames': len(TRACE['qpos'])}))
