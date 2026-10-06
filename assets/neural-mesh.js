// ═══════════════════════════════════════════════════════════════
// NEURAL MESH CANVAS — Three.js background for æ:// surfaces
// Gold (#D4AF37) on void (#050505) · neural-mesh · scanlines
// WebGL safe for GH Pages (~95%) · WebGPU when available
// ═══════════════════════════════════════════════════════════════
import * as THREE from './three.module.js';

export class NeuralMesh {
  constructor(canvas, opts = {}) {
    this.canvas = canvas;
    this.opts = {
      nodeCount: opts.nodeCount || 120,
      connectionDist: opts.connectionDist || 2.8,
      speed: opts.speed || 0.15,
      goldColor: opts.goldColor || 0xD4AF37,
      voidColor: opts.voidColor || 0x050505,
      glowIntensity: opts.glowIntensity || 0.6,
      interactive: opts.interactive !== false,
      ...opts
    };
    this.mouse = new THREE.Vector2(0, 0);
    this.time = 0;
    this._animId = null;
    this.init();
  }

  async init() {
    // ── Renderer: WebGPU first, WebGL fallback ──
    const isWebGPU = await this.detectWebGPU();
    if (isWebGPU) {
      try {
        const { WebGPURenderer } = await import('./three.module.js');
        this.renderer = new WebGPURenderer({ canvas: this.canvas, antialias: true, alpha: true });
        await this.renderer.init();
        this.backend = 'webgpu';
      } catch (e) {
        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true, alpha: true });
        this.backend = 'webgl';
      }
    } else {
      this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true, alpha: true });
      this.backend = 'webgl';
    }

    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setClearColor(this.opts.voidColor, 0.85);
    this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);

    // ── Scene ──
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(this.opts.voidColor, 0.035);

    // ── Camera ──
    this.camera = new THREE.PerspectiveCamera(60, this.canvas.clientWidth / this.canvas.clientHeight, 0.1, 100);
    this.camera.position.set(0, 0, 12);

    // ── Neural Mesh: nodes + connections ──
    this.buildMesh();

    // ── Lights ──
    const ambient = new THREE.AmbientLight(this.opts.goldColor, 0.3);
    this.scene.add(ambient);
    const point = new THREE.PointLight(this.opts.goldColor, 1.2, 30);
    point.position.set(5, 5, 8);
    this.scene.add(point);
    const point2 = new THREE.PointLight(0x00EAFF, 0.4, 25);
    point2.position.set(-6, -3, 5);
    this.scene.add(point2);

    // ── Interaction ──
    if (this.opts.interactive) {
      window.addEventListener('mousemove', (e) => {
        this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
      });
    }

    window.addEventListener('resize', () => this.resize());
    this.animate();
  }

  async detectWebGPU() {
    if (!navigator.gpu) return false;
    try {
      const adapter = await navigator.gpu.requestAdapter();
      return !!adapter;
    } catch {
      return false;
    }
  }

  buildMesh() {
    const { nodeCount, connectionDist, goldColor } = this.opts;

    // ── Nodes (particles) ──
    this.positions = new Float32Array(nodeCount * 3);
    this.velocities = new Float32Array(nodeCount * 3);
    this.basePositions = new Float32Array(nodeCount * 3);

    for (let i = 0; i < nodeCount; i++) {
      const i3 = i * 3;
      this.positions[i3] = (Math.random() - 0.5) * 16;
      this.positions[i3 + 1] = (Math.random() - 0.5) * 10;
      this.positions[i3 + 2] = (Math.random() - 0.5) * 12;
      this.basePositions[i3] = this.positions[i3];
      this.basePositions[i3 + 1] = this.positions[i3 + 1];
      this.basePositions[i3 + 2] = this.positions[i3 + 2];
      this.velocities[i3] = (Math.random() - 0.5) * 0.01;
      this.velocities[i3 + 1] = (Math.random() - 0.5) * 0.01;
      this.velocities[i3 + 2] = (Math.random() - 0.5) * 0.01;
    }

    const nodeGeo = new THREE.BufferGeometry();
    nodeGeo.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));

    // Gold glowing nodes
    const nodeMat = new THREE.PointsMaterial({
      color: goldColor,
      size: 0.12,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending,
      sizeAttenuation: true,
    });
    this.nodeMesh = new THREE.Points(nodeGeo, nodeMat);
    this.scene.add(this.nodeMesh);

    // ── Connections (lines between nearby nodes) ──
    this.connections = [];
    const maxConnections = nodeCount * 4;
    const linePositions = new Float32Array(maxConnections * 6);
    let lineIdx = 0;

    for (let i = 0; i < nodeCount; i++) {
      for (let j = i + 1; j < nodeCount; j++) {
        const dx = this.positions[i * 3] - this.positions[j * 3];
        const dy = this.positions[i * 3 + 1] - this.positions[j * 3 + 1];
        const dz = this.positions[i * 3 + 2] - this.positions[j * 3 + 2];
        const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

        if (dist < connectionDist && lineIdx < maxConnections) {
          this.connections.push({ i, j, baseDist: dist });
          linePositions[lineIdx * 6] = this.positions[i * 3];
          linePositions[lineIdx * 6 + 1] = this.positions[i * 3 + 1];
          linePositions[lineIdx * 6 + 2] = this.positions[i * 3 + 2];
          linePositions[lineIdx * 6 + 3] = this.positions[j * 3];
          linePositions[lineIdx * 6 + 4] = this.positions[j * 3 + 1];
          linePositions[lineIdx * 6 + 5] = this.positions[j * 3 + 2];
          lineIdx++;
        }
      }
    }

    this.linePositions = linePositions;
    this.lineIdx = lineIdx;
    this.maxConnections = maxConnections;

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    lineGeo.setDrawRange(0, lineIdx * 2);

    const lineMat = new THREE.LineBasicMaterial({
      color: goldColor,
      transparent: true,
      opacity: 0.15,
      blending: THREE.AdditiveBlending,
    });
    this.lineMesh = new THREE.LineSegments(lineGeo, lineMat);
    this.scene.add(this.lineMesh);

    // ── Central core (glowing sphere) ──
    const coreGeo = new THREE.SphereGeometry(0.5, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({
      color: goldColor,
      transparent: true,
      opacity: 0.3,
      blending: THREE.AdditiveBlending,
    });
    this.core = new THREE.Mesh(coreGeo, coreMat);
    this.scene.add(this.core);

    // ── Core glow ring ──
    const ringGeo = new THREE.RingGeometry(0.6, 0.8, 64);
    const ringMat = new THREE.MeshBasicMaterial({
      color: goldColor,
      transparent: true,
      opacity: 0.15,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
    });
    this.ring = new THREE.Mesh(ringGeo, ringMat);
    this.scene.add(this.ring);
  }

  updateMesh() {
    const { nodeCount, speed } = this.opts;
    const t = this.time;

    // ── Update node positions (gentle floating) ──
    for (let i = 0; i < nodeCount; i++) {
      const i3 = i * 3;
      this.positions[i3] += this.velocities[i3];
      this.positions[i3 + 1] += this.velocities[i3 + 1];
      this.positions[i3 + 2] += this.velocities[i3 + 2];

      // Gentle drift back to base
      this.positions[i3] += (this.basePositions[i3] - this.positions[i3]) * 0.005;
      this.positions[i3 + 1] += (this.basePositions[i3 + 1] - this.positions[i3 + 1]) * 0.005;
      this.positions[i3 + 2] += (this.basePositions[i3 + 2] - this.positions[i3 + 2]) * 0.005;

      // Mouse influence
      if (this.opts.interactive) {
        const dx = this.mouse.x * 4 - this.positions[i3];
        const dy = this.mouse.y * 3 - this.positions[i3 + 1];
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 4) {
          this.positions[i3] += dx * 0.003;
          this.positions[i3 + 1] += dy * 0.003;
        }
      }
    }

    this.nodeMesh.geometry.attributes.position.needsUpdate = true;

    // ── Update connection lines ──
    for (let c = 0; c < this.lineIdx; c++) {
      const { i, j } = this.connections[c];
      const c6 = c * 6;
      this.linePositions[c6] = this.positions[i * 3];
      this.linePositions[c6 + 1] = this.positions[i * 3 + 1];
      this.linePositions[c6 + 2] = this.positions[i * 3 + 2];
      this.linePositions[c6 + 3] = this.positions[j * 3];
      this.linePositions[c6 + 4] = this.positions[j * 3 + 1];
      this.linePositions[c6 + 5] = this.positions[j * 3 + 2];
    }
    this.lineMesh.geometry.attributes.position.needsUpdate = true;

    // ── Core pulse ──
    const pulse = 1 + Math.sin(t * 2) * 0.15;
    this.core.scale.setScalar(pulse);
    this.core.material.opacity = 0.2 + Math.sin(t * 2) * 0.1;
    this.ring.rotation.z = t * 0.3;
    this.ring.scale.setScalar(1 + Math.sin(t * 1.5) * 0.1);

    // ── Camera drift ──
    this.camera.position.x = Math.sin(t * 0.1) * 0.5 + this.mouse.x * 0.5;
    this.camera.position.y = Math.cos(t * 0.08) * 0.3 + this.mouse.y * 0.3;
    this.camera.lookAt(0, 0, 0);
  }

  animate() {
    this._animId = requestAnimationFrame(() => this.animate());
    this.time += this.opts.speed * 0.016;
    this.updateMesh();
    this.renderer.render(this.scene, this.camera);
  }

  resize() {
    const w = this.canvas.clientWidth;
    const h = this.canvas.clientHeight;
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(w, h);
  }

  destroy() {
    if (this._animId) cancelAnimationFrame(this._animId);
    window.removeEventListener('mousemove', this._onMouse);
    this.renderer.dispose();
  }
}

// ── Auto-init for canvas[data-neural-mesh] ──
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('canvas[data-neural-mesh]').forEach((canvas) => {
      const opts = {};
      if (canvas.dataset.nodeCount) opts.nodeCount = parseInt(canvas.dataset.nodeCount);
      if (canvas.dataset.speed) opts.speed = parseFloat(canvas.dataset.speed);
      if (canvas.dataset.glow) opts.glowIntensity = parseFloat(canvas.dataset.glow);
      new NeuralMesh(canvas, opts);
    });
  });
}
