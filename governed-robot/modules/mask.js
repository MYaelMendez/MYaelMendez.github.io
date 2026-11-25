// mask.js — æ:// governed robot LED mask
// 32x28 matrix mapped onto a 512x448 front aperture (semicircular arch).
// Pure ES module: the only external surface is a canvas element passed to the
// constructor. Nothing is painted outside the arch; the camera port at
// (256, 312) r=34 is always cut with destination-out and must never be drawn.

export const COLS = 32;
export const ROWS = 28;
export const FW = 512;
export const FH = 448;

// Arch aperture: semicircle on top of a flat base. The dome ends at
// cx,r+... at y = topY + r = 260; below that the straight sides continue down
// to bottomY = 362, so the flat bottom sits low on the face.
export const AP = { cx: FW / 2, topY: 170, r: 140, bottomY: 345 };
// Camera port — open circle near bottom centre, never painted.
export const CAM = { cx: 256, cy: 315, r: 30 };

export const MODES = ['MIRROR', 'FACE', 'TEXT', 'TELEMETRY', 'QR / CODE', 'WARNING', 'OFF'];
export const STATES = ['IDLE', 'LISTENING', 'THINKING', 'SPEAKING', 'AWAITING APPROVAL', 'APPROVED', 'REFUSED', 'ERROR'];

export const NEON = {
  neon: '#00ff9f',
  cyan: '#70dcff',
  gold: '#D4AF37',
  magenta: '#ff00ff',
};

export const STATE_COLORS = {
  IDLE: NEON.cyan,
  LISTENING: NEON.neon,
  THINKING: NEON.magenta,
  SPEAKING: NEON.gold,
  'AWAITING APPROVAL': NEON.gold,
  APPROVED: NEON.neon,
  REFUSED: NEON.magenta,
  ERROR: '#ff2d55',
};

const BLACK = '#000000';
const BLINK_PERIOD = 3.8;
const QR_N = 25; // QR-like modules, odd so a centre column exists

export function clampBrightness(v) {
  if (!Number.isFinite(v)) return 1;
  return Math.max(0.15, Math.min(1.4, v));
}

export function inArch(x, y) {
  if (y < AP.topY - AP.r || y > AP.bottomY) return false;
  const dx = x - AP.cx;
  if (y <= AP.topY) {
    const dy = y - AP.topY;
    return dx * dx + dy * dy <= AP.r * AP.r;
  }
  return Math.abs(dx) <= AP.r;
}

// Geometry helper for the scene: traces the arch aperture outline.
export function archPath(ctx) {
  const { cx, topY, r, bottomY } = AP;
  ctx.beginPath();
  ctx.moveTo(cx - r, bottomY);
  ctx.lineTo(cx - r, topY);
  for (let i = 1; i < 48; i++) {
    const a = Math.PI - (i / 47) * Math.PI; // PI → 0 over the top
    ctx.lineTo(cx + r * Math.cos(a), topY - r * Math.sin(a));
  }
  ctx.lineTo(cx + r, bottomY);
  ctx.closePath();
}

// Geometry helper for the scene: traces the camera port hole.
export function camHolePath(ctx) {
  ctx.beginPath();
  ctx.arc(CAM.cx, CAM.cy, CAM.r, 0, Math.PI * 2, false);
}

// -- 5x7 glyphs for LED text ------------------------------------------------
const GLYPHS = {
  A: ['01110', '10001', '10001', '11111', '10001', '10001', '10001'],
  B: ['11110', '10001', '10001', '11110', '10001', '10001', '11110'],
  C: ['01111', '10000', '10000', '10000', '10000', '10000', '01111'],
  D: ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
  E: ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
  F: ['11111', '10000', '10000', '11110', '10000', '10000', '10000'],
  G: ['01111', '10000', '10000', '10111', '10001', '10001', '01111'],
  H: ['10001', '10001', '10001', '11111', '10001', '10001', '10001'],
  I: ['11111', '00100', '00100', '00100', '00100', '00100', '11111'],
  J: ['00111', '00010', '00010', '00010', '00010', '10010', '01100'],
  K: ['10001', '10010', '10100', '11000', '10100', '10010', '10001'],
  L: ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
  M: ['10001', '11011', '10101', '10101', '10001', '10001', '10001'],
  N: ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
  O: ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
  P: ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
  Q: ['01110', '10001', '10001', '10001', '10101', '10011', '01111'],
  R: ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
  S: ['01111', '10000', '10000', '01110', '00001', '00001', '11110'],
  T: ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
  U: ['10001', '10001', '10001', '10001', '10001', '10001', '01110'],
  V: ['10001', '10001', '10001', '10001', '10001', '01010', '00100'],
  W: ['10001', '10001', '10001', '10101', '10101', '11011', '10001'],
  X: ['10001', '10001', '01010', '00100', '01010', '10001', '10001'],
  Y: ['10001', '10001', '01010', '00100', '00100', '00100', '00100'],
  Z: ['11111', '00001', '00010', '00100', '01000', '10000', '11111'],
  0: ['01110', '10001', '10011', '10101', '11001', '10001', '01110'],
  1: ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
  2: ['01110', '10001', '00001', '00010', '00100', '01000', '11111'],
  3: ['11110', '00001', '00001', '01110', '00001', '00001', '11110'],
  4: ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
  5: ['11111', '10000', '11110', '00001', '00001', '10001', '01110'],
  6: ['01110', '10000', '10000', '11110', '10001', '10001', '01110'],
  7: ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
  8: ['01110', '10001', '10001', '01110', '10001', '10001', '01110'],
  9: ['01110', '10001', '10001', '01111', '00001', '00001', '01110'],
  '>': ['10000', '01000', '00100', '00010', '00100', '01000', '10000'],
  '<': ['00001', '00010', '00100', '01000', '00100', '00010', '00001'],
  '/': ['00001', '00010', '00010', '00100', '01000', '01000', '10000'],
  ':': ['00000', '00100', '00100', '00000', '00100', '00100', '00000'],
  '.': ['00000', '00000', '00000', '00000', '00000', '01100', '01100'],
  ',': ['00000', '00000', '00000', '00000', '01100', '00100', '01000'],
  '-': ['00000', '00000', '00000', '11111', '00000', '00000', '00000'],
  '_': ['00000', '00000', '00000', '00000', '00000', '00000', '11111'],
  '+': ['00000', '00100', '00100', '11111', '00100', '00100', '00000'],
  '!': ['00100', '00100', '00100', '00100', '00100', '00000', '00100'],
  '?': ['01110', '10001', '00001', '00010', '00100', '00000', '00100'],
  '*': ['00000', '10101', '01110', '11111', '01110', '10101', '00000'],
  '#': ['01010', '11111', '01010', '01010', '01010', '11111', '01010'],
  '=': ['00000', '00000', '11111', '00000', '11111', '00000', '00000'],
  "'": ['00100', '00100', '01000', '00000', '00000', '00000', '00000'],
  '"': ['01010', '01010', '10100', '00000', '00000', '00000', '00000'],
  '(': ['00010', '00100', '01000', '01000', '01000', '00100', '00010'],
  ')': ['01000', '00100', '00010', '00010', '00010', '00100', '01000'],
  '[': ['01110', '01000', '01000', '01000', '01000', '01000', '01110'],
  ']': ['01110', '00010', '00010', '00010', '00010', '00010', '01110'],
  '%': ['11001', '11010', '00010', '00100', '01000', '01011', '10011'],
  '&': ['01100', '10010', '10100', '01000', '10101', '10010', '01101'],
  '@': ['01110', '10001', '10111', '10101', '10111', '10000', '01110'],
  ' ': ['00000', '00000', '00000', '00000', '00000', '00000', '00000'],
};

// -- deterministic hashing --------------------------------------------------
function hash32(str, seed) {
  let h = (seed | 0) || 0x9e3779b9;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = (h >>> 0) & 0xffffffff;
    h = (h * 0x01000193) >>> 0;
    h ^= h >>> 13;
  }
  return h >>> 0;
}

// xorshift PRNG — cheap, deterministic, enough for QR-like noise.
function makeRng(seed) {
  let s = seed >>> 0 || 1;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >>> 17;
    s ^= s << 5; s >>>= 0;
    return s / 4294967296;
  };
}

// -- Face geometry ----------------------------------------------------------
// 2x2-cell eye blocks, gaze offset, blink closure.
const EYE_CELLS = { left: [8, 9], right: [23, 9] }; // [col,row]
const EYE_SIZE = 2;
const MOUTH_ROW = 16;
const MOUTH_COLS = Array.from({ length: 14 }, (_, i) => 9 + i);

export class MaskEngine {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.mode = 'MIRROR';
    this.program = null;
    this.state = 'IDLE';
    this.text = '';
    this.brightness = 1;
    this.gaze = { x: 0, y: 0 };
    this.blinkValue = 0; // 0 open .. 1 closed
    this._autoBlink = true;
    this.cellW = FW / COLS;   // 16
    this.cellH = FH / ROWS;   // 16
    this._lastT = -1;
  }

  setProgram(p) {
    if (p == null) this.program = null;
    else if (typeof p === 'object') this.program = p;
    else this.program = { type: String(p), text: String(p) };
    return this.program;
  }

  setMode(m) {
    if (m == null) return this.mode;
    const up = String(m).toUpperCase();
    this.mode = MODES.includes(up) ? up : this.mode;
    return this.mode;
  }

  setState(s) {
    this.state = STATES.includes(s) ? s : this.state;
    return this.state;
  }

  setText(t) {
    this.text = t == null ? '' : String(t);
    return this.text;
  }

  setBrightness(v) {
    this.brightness = clampBrightness(v);
    return this.brightness;
  }

  setGaze(x, y) {
    const gx = Number.isFinite(x) ? Math.max(-4, Math.min(4, x)) : 0;
    const gy = Number.isFinite(y) ? Math.max(-2.5, Math.min(2.5, y)) : 0;
    this.gaze = { x: gx, y: gy };
    return this.gaze;
  }

  // v: 0..1 explicit closure. With no argument, run the autonomous blink clock.
  blink(v) {
    if (v == null) {
      this._autoBlink = true;
      return this.blinkValue;
    }
    this._autoBlink = false;
    this.blinkValue = Number.isFinite(v) ? Math.max(0, Math.min(1, v)) : 0;
    return this.blinkValue;
  }

  getCanvas() { return this.canvas; }
  getContext() { return this.ctx; }

  clear() {
    const c = this.ctx;
    if (!c) return;
    c.save();
    c.globalCompositeOperation = 'source-over';
    c.clearRect(0, 0, FW, FH);
    c.restore();
  }

  // -- rendering ------------------------------------------------------------
  draw(t) {
    const c = this.ctx;
    if (!c) return;
    const now = Number.isFinite(t) ? t : (typeof performance !== 'undefined' ? performance.now() : Date.now());
    if (this._lastT < 0) this._lastT = now;
    const dt = Math.max(0, Math.min(100, now - this._lastT));
    this._lastT = now;

    if (this._autoBlink) {
      // single smooth closure every BLINK_PERIOD seconds
      const phase = (now / 1000) % BLINK_PERIOD;
      const w = 0.12 * BLINK_PERIOD;
      let b = 0;
      if (phase < w) b = phase / w;
      else if (phase < 2 * w) b = 1 - (phase - w) / w;
      this.blinkValue = b;
    }

    this.clear();
    const b = this.brightness;

    // OFF leaves only a faint idle matrix — never fully blank metal.
    if (this.mode === 'OFF') {
      this.drawIdleMatrix(now, 0.12 * b);
      return;
    }

    if (this.mode === 'MIRROR') return; // true mirror: nothing drawn

    // Everything light-like is clipped to the arch, then the camera hole is
    // subtracted with destination-out — it is never painted, in any mode.
    c.save();
    archPath(c);
    c.clip();

    switch (this.mode) {
      case 'FACE': this.drawFace(now, b); break;
      case 'TEXT': this.drawText(now, b); break;
      case 'TELEMETRY': this.drawTelemetry(now, b); break;
      case 'QR / CODE': this.drawQr(now, b); break;
      case 'WARNING': this.drawWarning(now, b); break;
      default: this.drawFace(now, b);
    }

    c.restore(); // end arch clip

    // Camera port: absolute cut, independent of clip state.
    c.save();
    c.globalCompositeOperation = 'destination-out';
    camHolePath(c);
    c.fill();
    c.restore();

    // Thin ring around the port so the opening reads as machined, not painted.
    c.save();
    c.strokeStyle = this.dim(this.stateColor(), 0.22 * b);
    c.lineWidth = 1.5;
    camHolePath(c);
    c.stroke();
    c.restore();
  }

  stateColor() {
    return STATE_COLORS[this.state] || NEON.neon;
  }

  dim(hex, k) {
    const n = parseInt(hex.slice(1), 16);
    const r = Math.round(((n >> 16) & 255) * k);
    const g = Math.round(((n >> 8) & 255) * k);
    const bl = Math.round((n & 255) * k);
    return `rgb(${r},${g},${bl})`;
  }

  cellCenter(col, row) {
    return [(col + 0.5) * this.cellW, (row + 0.5) * this.cellH];
  }

  // Round LED socket. Only called inside the arch clip.
  led(col, row, color, intensity) {
    if (col < 0 || col >= COLS || row < 0 || row >= ROWS) return;
    const [x, y] = this.cellCenter(col, row);
    if (!inArch(x, y)) return;
    const r = Math.min(this.cellW, this.cellH) * 0.34;
    const c = this.ctx;
    c.save();
    c.globalAlpha = Math.max(0, Math.min(1, intensity == null ? 1 : intensity));
    c.fillStyle = color;
    c.beginPath();
    c.arc(x, y, r, 0, Math.PI * 2, false);
    c.fill();
    c.restore();
  }

  // A soft halo only on the brightest features (state eyes, warning core):
  // shadowBlur stays off the per-LED loop, which is where perf would die.
  glowDot(x, y, r, color, alpha) {
    const c = this.ctx;
    c.save();
    c.globalAlpha = alpha;
    c.shadowColor = color;
    c.shadowBlur = 14;
    c.fillStyle = color;
    c.beginPath();
    c.arc(x, y, r, 0, Math.PI * 2, false);
    c.fill();
    c.restore();
  }

  drawIdleMatrix(now, k) {
    const color = this.dim(NEON.cyan, k);
    for (let row = 0; row < ROWS; row++) {
      for (let col = 0; col < COLS; col++) {
        if (((col * 7 + row * 11) % 13) === 0) continue;
        this.led(col, row, color, 1);
      }
    }
  }

  drawFace(now, b) {
    const base = this.stateColor();
    const gx = Math.round(this.gaze.x);
    const gy = Math.round(this.gaze.y);
    const blink = this.blinkValue;

    // eye sockets: subtle darker wells behind the LEDs
    for (const key of ['left', 'right']) {
      const [ec, er] = EYE_CELLS[key];
      const [x, y] = this.cellCenter(ec + 0.5, er + 0.5);
      this.ctx.save();
      this.ctx.globalAlpha = 0.16 * b;
      this.ctx.fillStyle = BLACK;
      this.ctx.beginPath();
      this.ctx.arc(x, y, this.cellW * 1.25, 0, Math.PI * 2, false);
      this.ctx.fill();
      this.ctx.restore();
    }

    // eyes — 2x2 cells each, shifted by gaze, vertically squashed when blinking
    const rows = blink > 0.85 ? 1 : EYE_SIZE;
    const eyeIntensity = 1 - 0.55 * blink;
    for (const key of ['left', 'right']) {
      const [ec, er] = EYE_CELLS[key];
      for (let dc = 0; dc < EYE_SIZE; dc++) {
        for (let dr = 0; dr < rows; dr++) {
          const col = ec + dc + gx;
          const row = er + dr + gy;
          this.led(col, row, base, eyeIntensity * b);
        }
      }
      // one halo at the eye centroid, not four shadows per eye
      if (blink < 0.5) {
        const [ex, ey] = this.cellCenter(ec + 0.5 + gx, er + 0.5 + gy);
        if (inArch(ex, ey)) this.glowDot(ex, ey, this.cellW * 0.55, base, 0.35 * b * (1 - blink));
      }
    }

    // mouth — neutral line that responds to state
    let mouth = new Array(MOUTH_COLS.length).fill(false);
    const st = this.state;
    if (st === 'SPEAKING') {
      const amp = 1.6;
      for (let i = 0; i < MOUTH_COLS.length; i++) {
        const wave = Math.sin(now / 90 + i * 0.55) * amp;
        const r = MOUTH_ROW + Math.round(wave + this.gaze.y);
        if (r >= 0 && r < ROWS) this.led(MOUTH_COLS[i], r, base, 0.9 * b);
      }
      mouth = null;
    } else if (st === 'APPROVED') {
      for (let i = 0; i < MOUTH_COLS.length; i++) {
        const lift = Math.round(Math.sin((i / (MOUTH_COLS.length - 1)) * Math.PI) * 2);
        this.led(MOUTH_COLS[i], MOUTH_ROW - lift, base, 0.95 * b);
      }
      mouth = null;
    } else if (st === 'REFUSED' || st === 'ERROR') {
      for (let i = 0; i < MOUTH_COLS.length; i++) {
        const dip = Math.round(Math.sin((i / (MOUTH_COLS.length - 1)) * Math.PI) * 2);
        this.led(MOUTH_COLS[i], MOUTH_ROW + dip, st === 'ERROR' ? STATE_COLORS.ERROR : base, 0.95 * b);
      }
      mouth = null;
    } else if (st === 'THINKING') {
      const shift = Math.round(Math.sin(now / 260) * 4);
      for (let i = 2; i < MOUTH_COLS.length - 2; i++) this.led(MOUTH_COLS[i], MOUTH_ROW, base, 0.7 * b);
      this.led(MOUTH_COLS[3] + shift, MOUTH_ROW, base, 0.9 * b);
      mouth = null;
    } else if (st === 'AWAITING APPROVAL') {
      for (let i = 0; i < MOUTH_COLS.length; i++) this.led(MOUTH_COLS[i], MOUTH_ROW, base, (0.45 + 0.35 * Math.sin(now / 300 + i)) * b);
      mouth = null;
    } else if (mouth) {
      // IDLE / LISTENING: flat neutral line with a slow breath
      const a = (0.65 + 0.2 * Math.sin(now / 900)) * b;
      for (let i = 0; i < MOUTH_COLS.length; i++) this.led(MOUTH_COLS[i], MOUTH_ROW, base, a);
    }

    // dim socket matrix behind the face, inside the arch only
    this.drawSocketField(b, 0.10);
  }

  // faint unlit-LED grid so the panel reads as hardware between lit pixels
  drawSocketField(b, k) {
    const color = this.dim(NEON.cyan, k);
    for (let row = 0; row < ROWS; row++) {
      for (let col = 0; col < COLS; col++) {
        this.led(col, row, color, 1);
      }
    }
  }

  textRows() {
    const raw = (this.text || '').toUpperCase().replace(/\s+/g, ' ').trim();
    if (!raw) return [];
    const maxChars = 12; // 12 * (5 + 1) = 72px wide at 6px cells -> fits 32 cols? no: use cell-based fit
    const out = [];
    let line = '';
    for (const word of raw.split(' ')) {
      const next = line ? line + ' ' + word : word;
      if (next.length > maxChars && line) { out.push(line); line = word; }
      else line = next;
    }
    if (line) out.push(line);
    return out.slice(0, 4);
  }

  drawText(now, b) {
    const base = this.stateColor();
    const lines = this.textRows();
    if (!lines.length) { this.drawSocketField(b, 0.08); return; }

    // LED-pixel font: each glyph pixel is one matrix cell.
    const gw = 6; // 5 px + 1 gap
    const gh = 8; // 7 px + 1 gap
    const lineH = 7;
    const textBlockH = lines.length * lineH;
    let row0 = Math.round(MOUTH_ROW - 4 - textBlockH / 2);
    row0 = Math.max(1, Math.min(row0, ROWS - textBlockH - 1));

    for (let li = 0; li < lines.length; li++) {
      const s = lines[li];
      const w = s.length * gw - 1;
      let col0 = Math.round((COLS - w) / 2);
      col0 = Math.max(0, Math.min(col0, COLS - w));
      const rr = row0 + li * lineH;
      for (let ci = 0; ci < s.length; ci++) {
        const g = GLYPHS[s[ci]] || GLYPHS['?'];
        for (let gy = 0; gy < 7; gy++) {
          for (let gx = 0; gx < 5; gx++) {
            if (g[gy][gx] !== '1') continue;
            const flicker = 0.82 + 0.18 * Math.sin(now / 1400 + (ci * 7 + gx) * 1.7 + gy);
            this.led(col0 + ci * gw + gx, rr + gy, base, flicker * b);
          }
        }
      }
    }
    this.drawSocketField(b, 0.06);
  }

  drawTelemetry(now, b) {
    const base = this.stateColor();
    const accent = NEON.cyan;
    const mid = 14;
    const span = 9;

    // scrolling waveform from a deterministic pseudo-signal
    for (let col = 0; col < COLS; col++) {
      const ph = now / 240 - col * 0.55;
      const v =
        Math.sin(ph) * 0.6 +
        Math.sin(ph * 2.7 + 1.3) * 0.28 +
        Math.sin(ph * 6.1 + 0.7) * 0.12;
      const row = mid + Math.round(v * span);
      if (row < 0 || row >= ROWS) continue;
      this.led(col, row, base, 0.95 * b);
      // faint echo trace above/below for an oscilloscope feel
      if (row - 2 >= 0) this.led(col, row - 2, accent, 0.18 * b);
      if (row + 2 < ROWS) this.led(col, row + 2, accent, 0.18 * b);
    }

    // ECG-style heartbeat marker that sweeps left->right
    const sweep = Math.floor((now / 1400) * COLS) % COLS;
    for (let i = 0; i < 4; i++) {
      const ccol = (sweep + i) % COLS;
      const spike = i === 1 ? -5 : i === 2 ? 3 : 0;
      this.led(ccol, mid + spike, NEON.gold, 0.9 * b);
    }

    // level bars along the bottom, state-tinted
    for (let i = 0; i < 6; i++) {
      const h = 1 + Math.round((Math.sin(now / 500 + i * 0.9) * 0.5 + 0.5) * 3);
      for (let k = 0; k < h; k++) {
        this.led(3 + i * 2, ROWS - 1 - k, i % 2 ? accent : base, 0.7 * b);
      }
    }
    this.drawSocketField(b, 0.05);
  }

  // Deterministic QR-like pattern: 25x25 modules with finder squares,
  // timing strips and seeded data noise. Same text -> same code.
  qrMatrix(text) {
    const seedStr = text == null || text === '' ? 'æ://' : String(text);
    const rng = makeRng(hash32(seedStr, 0x5bd1e995));
    const n = QR_N;
    const m = Array.from({ length: n }, () => new Array(n).fill(false));

    const finder = (r0, c0) => {
      for (let r = -1; r <= 7; r++) {
        for (let c = -1; c <= 7; c++) {
          const rr = r0 + r, cc = c0 + c;
          if (rr < 0 || rr >= n || cc < 0 || cc >= n) continue;
          const edge = r === -1 || r === 7 || c === -1 || c === 7;
          const ring = r === 0 || r === 6 || c === 0 || c === 6;
          const core = r >= 2 && r <= 4 && c >= 2 && c <= 4;
          m[rr][cc] = edge ? false : ring || core;
        }
      }
    };
    finder(0, 0);
    finder(0, n - 7);
    finder(n - 7, 0);

    // timing patterns
    for (let i = 8; i < n - 8; i++) {
      m[6][i] = i % 2 === 0;
      m[i][6] = i % 2 === 0;
    }
    // alignment-ish block
    for (let r = n - 9; r <= n - 5; r++) {
      for (let c = n - 9; c <= n - 5; c++) {
        const ring = r === n - 9 || r === n - 5 || c === n - 9 || c === n - 5;
        const core = r === n - 7 && c === n - 7;
        m[r][c] = ring || core;
      }
    }

    // data noise, skipping finder/timing regions
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const inFinder =
          (r < 8 && c < 8) || (r < 8 && c >= n - 8) || (r >= n - 8 && c < 8);
        const inTiming = r === 6 || c === 6;
        const inAlign = r >= n - 9 && r <= n - 5 && c >= n - 9 && c <= n - 5;
        if (inFinder || inTiming || inAlign) continue;
        m[r][c] = rng() < 0.46;
      }
    }
    return m;
  }

  drawQr(now, b) {
    const base = this.stateColor();
    const m = this.qrMatrix(this.text);
    const n = QR_N;
    const cell = Math.floor(Math.min(FW, FH) / (n + 6)); // quiet-zone padding
    const gw = cell * n;
    const ox = Math.round(AP.cx - gw / 2);
    const oy = Math.round(AP.topY + 40);
    const c = this.ctx;

    // quiet zone + plate
    c.save();
    c.globalAlpha = 0.9;
    c.fillStyle = this.dim('#ffffff', 0.06 * b);
    c.fillRect(ox - cell * 2, oy - cell * 2, gw + cell * 4, gw + cell * 4);
    c.restore();

    const pulse = 0.75 + 0.25 * Math.sin(now / 700);
    for (let r = 0; r < n; r++) {
      const py = oy + r * cell;
      if (py > AP.bottomY - cell) break;
      for (let q = 0; q < n; q++) {
        if (!m[r][q]) continue;
        const px = ox + q * cell;
        if (!inArch(px + cell / 2, py + cell / 2)) continue;
        const main = r < 8 && q < 8 || r < 8 && q >= n - 8 || r >= n - 8 && q < 8;
        c.globalAlpha = (main ? 0.95 : 0.7) * pulse * b;
        c.fillStyle = main ? NEON.gold : base;
        c.fillRect(px, py, cell - 1, cell - 1);
      }
    }
    c.globalAlpha = 1;

    // label under the code
    const label = (this.text || 'æ://').slice(0, 18);
    if (label) {
      c.save();
      c.fillStyle = this.dim(base, 0.55 * b);
      c.font = '10px "JetBrains Mono", monospace';
      c.textAlign = 'center';
      c.textBaseline = 'middle';
      c.fillText(label.toUpperCase(), AP.cx, Math.min(AP.bottomY - 14, oy + gw + cell * 2));
      c.restore();
    }
  }

  drawWarning(now, b) {
    const amber = NEON.gold;
    const alert = this.state === 'ERROR' ? STATE_COLORS.ERROR : NEON.magenta;
    const cx = AP.cx;
    const cy = 200;
    const R = 92;
    const p = 0.5 + 0.5 * Math.sin(now / 220); // hazard pulse

    // triangle outline
    this.ctx.save();
    this.ctx.strokeStyle = amber;
    this.ctx.lineWidth = 5;
    this.ctx.globalAlpha = (0.55 + 0.45 * p) * b;
    this.ctx.shadowColor = amber;
    this.ctx.shadowBlur = 16;
    this.ctx.beginPath();
    this.ctx.moveTo(cx, cy - R);
    this.ctx.lineTo(cx + R * 0.92, cy + R * 0.72);
    this.ctx.lineTo(cx - R * 0.92, cy + R * 0.72);
    this.ctx.closePath();
    this.ctx.stroke();
    this.ctx.restore();

    // exclamation built from matrix cells
    const col = Math.round(cx / this.cellW - 0.5);
    const topRow = Math.round((cy - R * 0.5) / this.cellH);
    for (let i = 0; i < 6; i++) this.led(col, topRow + i, alert, (0.7 + 0.3 * p) * b);
    this.led(col, topRow + 8, alert, (0.7 + 0.3 * p) * b);

    // scanning hazard bar under the triangle
    const barY = Math.round((cy + R * 0.8) / this.cellH);
    for (let i = 0; i < 12; i++) {
      const on = ((i + Math.floor(now / 120)) % 12) < 6;
      this.led(Math.round(cx / this.cellW) - 6 + i, barY, amber, on ? 0.85 * b : 0.12 * b);
    }

    this.drawSocketField(b, 0.06);
  }
}
