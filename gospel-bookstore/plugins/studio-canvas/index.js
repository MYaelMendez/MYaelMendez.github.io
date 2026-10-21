// Studio Canvas Widget — WebGL 3D Stage
// Interactive 3D visualization for ChatGPT

import { useRef, useEffect } from 'react';

const StudioCanvasWidget = ({ 
  scene = 'gospel-stage', 
  controls = true,
  width = '100%',
  height = '300px'
}) => {
  const canvasRef = useRef(null);
  const rendererRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);

  useEffect(() => {
    // Initialize Three.js scene
    const initThree = () => {
      const canvas = canvasRef.current;
      if (!canvas || canvas._initialized) return;
      canvas._initialized = true;

      // Scene
      sceneRef.current = new THREE.Scene();
      sceneRef.current.background = new THREE.Color(0x050505);

      // Camera
      cameraRef.current = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
      cameraRef.current.position.z = 5;

      // Renderer
      rendererRef.current = new THREE.WebGLRenderer({ 
        canvas,
        antialias: true,
        alpha: true 
      });
      rendererRef.current.setSize(canvas.clientWidth, canvas.clientHeight);
      rendererRef.current.setPixelRatio(window.devicePixelRatio);

      // Lights (gold accent theme)
      const ambientLight = new THREE.AmbientLight(0xD4AF37, 0.4);
      sceneRef.current.add(ambientLight);
      
      const directionalLight = new THREE.DirectionalLight(0xD4AF37, 0.6);
      directionalLight.position.set(1, 1, 1);
      sceneRef.current.add(directionalLight);

      // Default object (cross)
      const geometry = new THREE.BoxGeometry(1, 1, 1);
      const material = new THREE.MeshBasicMaterial({ 
        color: 0xD4AF37,
        transparent: true,
        opacity: 0.8
      });
      const cube = new THREE.Mesh(geometry, material);
      sceneRef.current.add(cube);

      // Animation loop
      const animate = () => {
        if (!sceneRef.current || !cameraRef.current) return;
        
        requestAnimationFrame(animate);
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
        
        if (rendererRef.current && sceneRef.current && cameraRef.current) {
          rendererRef.current.render(sceneRef.current, cameraRef.current);
        }
      };
      animate();
    };

    // Load Three.js from CDN
    const loadThree = async () => {
      if (window.THREE) {
        initThree();
        return;
      }

      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/three@0.158.0/build/three.min.js';
      script.onload = initThree;
      document.head.appendChild(script);
    };

    loadThree();

    return () => {
      if (rendererRef.current) {
        rendererRef.current.dispose();
      }
    };
  }, [scene]);

  return (
    <div style={{
      width,
      height,
      background: '#050505',
      borderRadius: '8px',
      overflow: 'hidden',
      border: '1px solid rgba(212,175,55,0.15)'
    }}>
      <canvas 
        ref={canvasRef} 
        style={{ width: '100%', height: '100%', display: 'block' }}
      />
    </div>
  );
};

// Simple CSS-based fallback if Three.js fails to load
const StudioCanvasFallback = () => (
  <div style={{
    width: '100%',
    height: '300px',
    background: 'linear-gradient(135deg, #050505 0%, #1a1a1a 100%)',
    border: '1px solid rgba(212,175,55,0.2)',
    borderRadius: '8px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'JetBrains Mono, monospace',
    color: '#e8e6df',
    flexDirection: 'column'
  }}>
    <div style={{ fontSize: '14px', color: '#D4AF37', marginBottom: '8px' }}>
      ✝️ Gospel Canvas
    </div>
    <div style={{ fontSize: '11px', color: '#6f6a5c' }}>
      WebGL 3D visualization
    </div>
  </div>
);

export { StudioCanvasWidget, StudioCanvasFallback };
export default StudioCanvasWidget;