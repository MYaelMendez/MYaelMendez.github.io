/* aether.js — shared sovereign surface runtime (gold-on-void chassis)
 * Imported by every ae:// web surface. Provides:
 *   Aether.toast(msg)            transient bottom toast
 *   Aether.QR.render(str,canvas) render a QR (uses vendored qrcode.js)
 *   Aether.scanCamera(video,predicate,onMatch)  camera scan w/ jsQR
 *   Aether.mesh()                start the neural-mesh canvas background
 *   Aether.lanIP()               best-guess LAN IP for manifests
 *   Aether.tokenHex(n)           ephemeral token
 * Depends on: assets/qrcode.js (qrcode-generator, MIT) and assets/jsQR.js (MIT).
 */
window.Aether = (() => {
  const $ = (s) => document.querySelector(s);

  function tokenHex(n) {
    let s = "";
    const h = "0123456789abcdef";
    for (let i = 0; i < n; i++) s += h[Math.floor(Math.random() * 16)];
    return s;
  }

  function toast(m) {
    let t = $("#toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "toast";
      t.className = "toast";
      document.body.appendChild(t);
    }
    t.textContent = m;
    t.classList.add("show");
    setTimeout(() => t.classList.remove("show"), 1800);
  }

  const QR = {
    render(str, canvas, scale = 6) {
      const qr = qrcode(0, "M");
      qr.addData(str);
      qr.make();
      const N = qr.getModuleCount();
      canvas.width = N * scale;
      canvas.height = N * scale;
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#fff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#000";
      for (let r = 0; r < N; r++)
        for (let c = 0; c < N; c++)
          if (qr.isDark(r, c)) ctx.fillRect(c * scale, r * scale, scale, scale);
    },
  };

  function lanIP() {
    return location.hostname &&
      location.hostname !== "localhost" &&
      location.hostname !== "127.0.0.1"
      ? location.hostname
      : "0.0.0.0";
  }

  /* camera scan: calls onMatch(data) when jsQR decodes a matching string */
  function scanCamera(video, predicate, onMatch) {
    let stream = null;
    return {
      async start() {
        try {
          stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: "environment" },
          });
          video.srcObject = stream;
          await video.play();
          const poll = () => {
            if (!stream || !video.videoWidth) {
              requestAnimationFrame(poll);
              return;
            }
            const c = document.createElement("canvas");
            c.width = video.videoWidth;
            c.height = video.videoHeight;
            const ctx = c.getContext("2d");
            ctx.drawImage(video, 0, 0);
            let res = null;
            try {
              const img = ctx.getImageData(0, 0, c.width, c.height);
              res = jsQR(img.data, c.width, c.height);
            } catch (e) {}
            if (res && res.data && predicate(res.data)) {
              onMatch(res.data);
              this.stop();
              return;
            }
            requestAnimationFrame(poll);
          };
          poll();
        } catch (e) {
          toast("camera denied — use paste");
        }
      },
      stop() {
        if (stream) {
          stream.getTracks().forEach((t) => t.stop());
          stream = null;
        }
      },
    };
  }

  /* neural mesh canvas background */
  function mesh() {
    const cv = $("#mesh");
    if (!cv) return;
    const cx = cv.getContext("2d");
    let W, H, pts;
    function resize() {
      W = cv.width = innerWidth;
      H = cv.height = innerHeight;
      pts = Array.from({ length: 60 }, () => [
        Math.random() * W,
        Math.random() * H,
        Math.random() * 0.4 + 0.1,
        Math.random() * 0.4 + 0.1,
      ]);
    }
    addEventListener("resize", resize);
    resize();
    (function loop() {
      cx.clearRect(0, 0, W, H);
      cx.strokeStyle = "rgba(212,175,55,.05)";
      cx.fillStyle = "rgba(212,175,55,.5)";
      for (const p of pts) {
        p[0] += p[2];
        p[1] += p[3];
        if (p[0] < 0 || p[0] > W) p[2] *= -1;
        if (p[1] < 0 || p[1] > H) p[3] *= -1;
        cx.beginPath();
        cx.arc(p[0], p[1], 1.2, 0, 7);
        cx.fill();
      }
      for (let i = 0; i < pts.length; i++)
        for (let j = i + 1; j < pts.length; j++) {
          const a = pts[i],
            b = pts[j];
          const d = Math.hypot(a[0] - b[0], a[1] - b[1]);
          if (d < 120) {
            cx.globalAlpha = ((120 - d) / 120) * 0.12;
            cx.beginPath();
            cx.moveTo(a[0], a[1]);
            cx.lineTo(b[0], b[1]);
            cx.stroke();
          }
        }
      cx.globalAlpha = 1;
      requestAnimationFrame(loop);
    })();
  }

  return { $, tokenHex, toast, QR, lanIP, scanCamera, mesh };
})();

/* expose $ globally — every ae:// surface destructures `const {$, Aether} = window`
   and expects a global querySelector helper. Without this, handlers never bind
   (e.g. SAVE on the secret bridge silently no-ops). */
window.$ = (s) => document.querySelector(s);
