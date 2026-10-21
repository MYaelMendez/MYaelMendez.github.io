# Studio Canvas Widget — WebGL 3D Stage

Widget de lienzo 3D para visualizaciones interactivas.

```javascript
import { useRef, useEffect } from 'react';

export function StudioCanvasWidget({ scene = 'default', controls = true }) {
  const canvasRef = useRef(null);
  const rendererRef = useRef(null);

  useEffect(() => {
    // Initialize WebGL renderer
    const canvas = canvasRef.current;
    rendererRef.current = new THREE.WebGLRenderer({ 
      canvas,
      antialias: true,
      alpha: true 
    });
    rendererRef.current.setSize(canvas.clientWidth, canvas.clientHeight);
    
    // Create stage
    const scene3d = new THREE.Scene();
    scene3d.background = new THREE.Color(0x050505);
    
    // Add lights (gold accent)
    const ambient = new THREE.AmbientLight(0xD4AF37, 0.3);
    scene3d.add(ambient);
    
    return () => rendererRef.current?.dispose();
  }, []);

  return (
    <div className="studio-canvas-wrapper">
      <canvas ref={canvasRef} className="studio-canvas" />
    </div>
  );
}

/* CSS */
.studio-canvas-wrapper {
  position: relative;
  width: 100%;
  height: 400px;
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 8px;
  background: #050505;
}
```