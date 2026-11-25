// scene.js — the governed Asimov head: one upright shell, one semicircular face viewport.
import * as THREE from 'three';
import { GLTFLoader } from '../assets/vendor/GLTFLoader.js';
import { AP, CAM, FW, FH, archPath } from './mask.js';

const ORANGE = 0xff6a00;

export class RobotScene {
  constructor(canvas) {
    this.THREE = THREE;
    this.canvas = canvas;
    this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: 'high-performance' });
    this.renderer.setPixelRatio(Math.min(1.75, window.devicePixelRatio || 1));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.1;
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x040706);
    this.camera = new THREE.PerspectiveCamera(38, 9 / 16, 0.01, 40);
    this.target = new THREE.Vector3(0, 0, 0);
    this.distance = 0.42;
    this.az = 0; this.el = 0; this.autoRotate = false;
    this.clock = new THREE.Clock();
    this.headMesh = null; this.maskMesh = null; this.mirrorMesh = null;
    this.earMeshes = []; this.maskBaseW = 0.168; this.maskBaseH = 0.132;
    this._buildLights();
    this._buildRoom();
    this._buildEnvMap();
    this.resize();
  }

  _buildLights() {
    const s = this.scene;
    s.add(new THREE.HemisphereLight(0xfff0cf, 0x06120c, 0.85));
    const key = new THREE.DirectionalLight(0xffe0a0, 2.0); key.position.set(0.8, 1.2, 1.4); s.add(key);
    const rim = new THREE.DirectionalLight(0x00ff9f, 1.1); rim.position.set(-1.2, 0.5, -1.0); s.add(rim);
    const fill = new THREE.DirectionalLight(0x70dcff, 0.55); fill.position.set(-0.8, -0.3, 1.2); s.add(fill);
  }

  _buildRoom() {
    const s = this.scene;
    const grid = new THREE.GridHelper(2.4, 24, 0x1d4a5f, 0x0d2430);
    grid.position.y = -0.28; grid.material.transparent = true; grid.material.opacity = 0.5; s.add(grid);
    const floor = new THREE.Mesh(
      new THREE.CircleGeometry(0.62, 64),
      new THREE.MeshStandardMaterial({ color: 0x0a0f0c, metalness: 0.42, roughness: 0.66 })
    );
    floor.rotation.x = -Math.PI / 2; floor.position.y = -0.281; s.add(floor);
    const pedestal = new THREE.Mesh(
      new THREE.CylinderGeometry(0.10, 0.135, 0.16, 48),
      new THREE.MeshStandardMaterial({ color: 0x141a18, metalness: 0.72, roughness: 0.34 })
    );
    pedestal.position.y = -0.20; s.add(pedestal);
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(0.20, 0.0035, 10, 72),
      new THREE.MeshBasicMaterial({ color: 0x00ff9f, transparent: true, opacity: 0.5 })
    );
    ring.rotation.x = Math.PI / 2; ring.position.y = -0.272; s.add(ring);
  }

  _buildEnvMap() {
    const pmrem = new THREE.PMREMGenerator(this.renderer);
    const env = new THREE.Scene();
    env.add(new THREE.Mesh(
      new THREE.SphereGeometry(10, 24, 16),
      new THREE.MeshBasicMaterial({ color: 0x24343d, side: THREE.BackSide })
    ));
    const strip = (color, x, y, z, w, h) => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color, side: THREE.DoubleSide }));
      m.position.set(x, y, z); m.lookAt(0, 0, 0); env.add(m);
    };
    strip(0xffffff, -2, 3, 4, 6, 3);
    strip(0x00ff9f, -5, 2.5, 2, 5, 2);
    strip(0x70dcff, 5, -1, 2, 5, 2);
    strip(0xffb000, 0, 5, -3, 6, 3);
    this.envMap = pmrem.fromScene(env, 0.06).texture;
    pmrem.dispose();
  }

  async load(url = './assets/gltf/asimov-web.glb') {
    const gltf = await new GLTFLoader().loadAsync(url);
    const root = gltf.scene;
    let head = null;
    root.traverse(o => {
      if (!o.isMesh) return;
      o.material = new THREE.MeshStandardMaterial({
        color: ORANGE, metalness: 0.58, roughness: 0.26,
        emissive: 0xff3d00, emissiveIntensity: 0.30, side: THREE.DoubleSide
      });
      if (o.name === 'neck_pitch_link') head = o;
    });
    if (!head) throw new Error('neck_pitch_link not found in GLB');
    this.headMesh = head;

    // The GLB is Z-up. Upright it about X so the head rests on its neck and
    // the face points toward the viewer (+Z). No decorative yaw.
    const fix = new THREE.Group();
    fix.rotation.x = -Math.PI / 2;
    // Bake the node placement out: vertices are authored in the GLB frame.
    head.position.set(0, 0, 0); head.rotation.set(0, 0, 0); head.scale.set(1, 1, 1);
    fix.add(head);
    this.scene.add(fix);
    this.fix = fix;

    this.scene.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(head);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());

    this.size = size;
    this.maskBaseW = size.x * 1.04;
    this.maskBaseH = size.y * 0.98;
    const mountY = -0.145;
    fix.position.set(-center.x, mountY - box.min.y, -center.z);
    this.scene.updateMatrixWorld(true);
    // Local geometry centre in the upright rig, for the overlay group.
    head.geometry.computeBoundingBox();
    const localCenter = head.geometry.boundingBox.getCenter(new THREE.Vector3());
    this.target.set(0, mountY + size.y / 2, 0);
    this.camera.position.set(0, this.target.y, this.distance);
    this.camera.lookAt(this.target);

    this._buildFace(size, localCenter);
    return this.headInfo();
  }

  _faceCarrierGeometry(size) {
    const geo = new THREE.PlaneGeometry(this.maskBaseW, this.maskBaseH, 40, 34);
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i), y = pos.getY(i);
      pos.setZ(i, -0.006 * (Math.pow(x / (this.maskBaseW * 0.5), 2) + Math.pow(y / (this.maskBaseH * 0.5), 2)));
    }
    geo.computeVertexNormals();
    return geo;
  }

  _archAlphaCanvas() {
    const c = document.createElement('canvas'); c.width = FW; c.height = FH;
    const g = c.getContext('2d');
    g.fillStyle = '#000'; g.fillRect(0, 0, FW, FH);
    g.fillStyle = '#fff';
    archPath(g); g.fill();
    g.globalCompositeOperation = 'destination-out';
    g.beginPath(); g.arc(CAM.cx, CAM.cy, CAM.r, 0, Math.PI * 2); g.fill();
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  }

  _buildFace(size, localCenter = new THREE.Vector3()) {
    const geo = this._faceCarrierGeometry(size);
    const z = size.z / 2 + 0.010;
    // Counter-rotate the overlay rig so it cancels the head's -90° upright tilt:
    // overlays stay in the head's local face frame and face +Z in world.
    const face = new THREE.Group();
    face.rotation.x = Math.PI / 2;
    face.position.copy(localCenter);
    this.fix.add(face);
    this.faceGroup = face;

    // Reflective faceplate: arch alpha-masked mirror, camera port open.
    const mirrorMat = new THREE.MeshStandardMaterial({
      color: 0xf4f8ff, metalness: 1.0, roughness: 0.055,
      envMap: this.envMap, envMapIntensity: 1.5,
      transparent: true, alphaMap: this._archAlphaCanvas(),
      side: THREE.DoubleSide, depthWrite: false
    });
    this.mirrorMesh = new THREE.Mesh(geo.clone(), mirrorMat);
    this.mirrorMesh.position.set(0, 0, z);
    this.mirrorMesh.renderOrder = 1;
    face.add(this.mirrorMesh);

    // LED/content layer: additive, transparent outside the arch.
    this.maskTexture = new THREE.CanvasTexture(document.createElement('canvas'));
    this.maskTexture.colorSpace = THREE.SRGBColorSpace;
    this.maskTexture.anisotropy = 4;
    const maskMat = new THREE.MeshBasicMaterial({
      map: this.maskTexture, transparent: true, depthWrite: false,
      blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false
    });
    this.maskMesh = new THREE.Mesh(geo.clone(), maskMat);
    this.maskMesh.position.set(0, 0, z + 0.0015);
    this.maskMesh.renderOrder = 2;
    face.add(this.maskMesh);
  }

  setMaskCanvas(canvas) {
    if (!this.maskTexture) return;
    this.maskTexture.image = canvas;
    this.maskTexture.needsUpdate = true;
  }

  setWire(v) { if (this.headMesh) this.headMesh.material.wireframe = !!v; }
  setShellVisible(v) { if (this.headMesh) this.headMesh.visible = !!v; }
  setShellColor(hex) { if (this.headMesh) { this.headMesh.material.color.set(hex); this.headMesh.material.emissive.set(hex).multiplyScalar(0.28); } }
  setDistance(d) { this.distance = Math.max(0.18, Math.min(1.2, d)); }
  getDistance() { return this.distance; }
  setAutoRotate(v) { this.autoRotate = !!v; }
  setCamera(name) {
    const presets = {
      front: [0, 0], 'threequarter': [35, -4], side: [82, -2],
      close: [0, 0], top: [0, 82], orbit: [28, 8]
    };
    const p = presets[name] || [0, 0];
    this.az = p[0] * Math.PI / 180; this.el = p[1] * Math.PI / 180;
    if (name === 'close') this.distance = 0.30;
    if (name === 'top') this.distance = 0.34;
  }
  setTransform({ yaw = 0, pitch = 0, roll = 0, posX = 0, posY = 0, posZ = 0, scale = 1 } = {}) {
    if (!this.fix) return;
    this.fix.rotation.set(-Math.PI / 2 + pitch * Math.PI / 180, yaw * Math.PI / 180, roll * Math.PI / 180);
    this.fix.position.x = posX; this.fix.position.z = posZ;
    this.fix.position.y += posY;
    this.fix.scale.setScalar(scale);
  }

  screenToHead(clientX, clientY) {
    if (!this.headMesh) return null;
    const r = this.canvas.getBoundingClientRect();
    const ndc = new THREE.Vector2(((clientX - r.left) / r.width) * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1);
    const ray = new THREE.Raycaster(); ray.setFromCamera(ndc, this.camera);
    const hit = ray.intersectObject(this.headMesh, false)[0];
    if (!hit) return null;
    const n = hit.face ? hit.face.normal.clone().transformDirection(hit.object.matrixWorld) : new THREE.Vector3(0, 0, 1);
    return { point: hit.point.toArray(), normal: n.toArray() };
  }

  headInfo() {
    if (!this.headMesh) return null;
    const box = new THREE.Box3().setFromObject(this.headMesh);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    let tris = 0;
    this.headMesh.geometry?.index ? tris = this.headMesh.geometry.index.count / 3 : tris = this.headMesh.geometry.attributes.position.count / 3;
    return { size: { x: +size.x.toFixed(4), y: +size.y.toFixed(4), z: +size.z.toFixed(4) }, center: center.toArray(), triangles: Math.round(tris) };
  }

  resize() {
    const w = this.canvas.clientWidth || window.innerWidth;
    const h = this.canvas.clientHeight || window.innerHeight;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = w / h; this.camera.updateProjectionMatrix();
  }

  update(t, dt) {
    if (this.autoRotate) this.az += dt * 0.25;
    const d = this.distance, cy = Math.cos(this.el), sy = Math.sin(this.el);
    this.camera.position.set(
      this.target.x + d * cy * Math.sin(this.az),
      this.target.y + d * sy,
      this.target.z + d * cy * Math.cos(this.az)
    );
    this.camera.lookAt(this.target);
    if (this.maskTexture) this.maskTexture.needsUpdate = true;
    this.renderer.render(this.scene, this.camera);
  }
}
