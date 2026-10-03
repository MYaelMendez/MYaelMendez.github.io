/* Shared neural mesh canvas for local sovereign surfaces. */
const HermesMesh = (() => {
  let canvas, ctx, width, height, nodes, raf, color = '#D4AF37';

  const createNodes = (count, w, h) => Array.from({ length: count }, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    vx: (Math.random() - 0.5) * 0.35,
    vy: (Math.random() - 0.5) * 0.35,
    r: Math.random() * 1.4 + 0.6,
  }));

  const resize = () => {
    const dpr = Math.max(1, window.devicePixelRatio || 1);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    nodes = createNodes(Math.floor((width * height) / 14000), width, height);
  };

  const draw = () => {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = color;
    ctx.strokeStyle = color;
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      a.x += a.vx; a.y += a.vy;
      if (a.x < 0 || a.x > width) a.vx *= -1;
      if (a.y < 0 || a.y > height) a.vy *= -1;
      ctx.globalAlpha = 0.18;
      ctx.beginPath();
      ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2);
      ctx.fill();
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 110) {
          ctx.globalAlpha = 0.07 * (1 - d / 110);
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }
    raf = requestAnimationFrame(draw);
  };

  const mount = (selectorOrEl, c = '#D4AF37') => {
    color = c;
    canvas = typeof selectorOrEl === 'string' ? document.querySelector(selectorOrEl) : selectorOrEl;
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    resize();
    draw();
    window.removeEventListener('resize', resize);
    window.addEventListener('resize', resize);
  };

  const unmount = () => {
    cancelAnimationFrame(raf);
    window.removeEventListener('resize', resize);
  };

  return { mount, unmount };
})();
