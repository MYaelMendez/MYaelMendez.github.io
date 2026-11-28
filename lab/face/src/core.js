/* æ æ æ face core · ae.face/0.1 · pure functions, shared by the kiosk and the SVG exporter */
const SCHEMA = "ae.face/0.1";
const STALE_S = 0.5, LOW_BATTERY = 20;
const ORDER = ["hold", "lost", "tired", "sleep", "think", "ready", "work"];
const MEANS = {
  hold: "fault latched: robot stays damped until firmware restart",
  lost: "no fresh state: the face cannot vouch for the robot",
  tired: "battery low",
  sleep: "DAMP: no actuator holds a position",
  think: "STAND, not armed yet",
  ready: "STAND, armed: MOVE is allowed",
  work: "MOVE: the walking policy balances the robot"
};
const SHORT = { hold: "fault", lost: "no fresh state", tired: "battery <20", sleep: "DAMP", think: "STAND, not armed", ready: "STAND, armed", work: "MOVE" };

/* ── geometry: one continuous Picasso line. Every mood has the SAME command structure,
      so the face can morph between moods (SMIL animate on d). viewBox 0 0 400 400 ── */
const P = {
  ready: { e: { h1: 22, h2: 14 }, B: [200, 150], lift: [0, 0], gaze: [0, 0], pr: 7,
    m: { ml: [160, 288], mr: [240, 288], top: [[182, 312], [218, 312]], bot: [[220, 328], [180, 328]] } },
  work: { e: { h1: 11, h2: 9, tin: 6 }, B: [200, 174], lift: [-4, -4], gaze: [5, 0], pr: 6,
    m: { ml: [150, 290], mr: [250, 290], top: [[180, 300], [220, 300]], bot: [[222, 324], [178, 324]] } },
  think: { e: { h1: 20, h2: 12 }, eL: { h1: 11, h2: 10 }, B: [200, 160], lift: [14, -2], gaze: [6, -7], pr: 6,
    m: { ml: [176, 298], mr: [234, 287], top: [[196, 301], [216, 297]], bot: null } },
  lost: { e: { h1: 25, h2: 20 }, B: [200, 144], lift: [6, 6], gaze: [0, 0], pr: 5,
    m: { ml: [166, 296], mr: [234, 296], top: [[188, 276], [212, 316]], bot: null } },
  tired: { e: { h1: 5, h2: 8, tout: 6 }, B: [200, 164], lift: [-10, -10], gaze: [0, 3], pr: 5,
    m: { ml: [168, 303], mr: [232, 303], top: [[190, 296], [210, 296]], bot: null } },
  sleep: { e: { h1: -7, h2: 7 }, B: [200, 160], lift: [-4, -4], gaze: [0, 0], pr: 0,
    m: { ml: [188, 298], mr: [212, 298], top: [[192, 288], [208, 288]], bot: [[208, 309], [192, 309]] } },
  hold: { x: true, B: [200, 178], lift: [-8, -8], gaze: [0, 0], pr: 0,
    m: { ml: [160, 300], mr: [240, 300], top: [[186, 322], [214, 278]], bot: null } }
};
const EYE = { R: { xo: 274, xi: 224, y: 198 }, L: { xo: 126, xi: 176, y: 198 } };
const f = n => Math.round(n * 10) / 10;
const pt = p => f(p[0]) + " " + f(p[1]);
function eye(side, p, closed) {
  const E = EYE[side], dx = E.xi - E.xo, y = E.y;
  if (p.x && !closed) { // hold: knotted X, still one stroke
    const o = [E.xo, y - 18], i = [E.xi, y + 18];
    return { o, s1: [[E.xo + dx * .33, y - 6], [E.xo + dx * .66, y + 6], i],
      s2: [[E.xi - dx * .05, y - 30], [E.xo + dx * .1, y + 30], [E.xo + dx * .04, y - 16]] };
  }
  let h = (side === "L" && p.eL) ? p.eL : (p.e || { h1: 0, h2: 0 });
  if (closed) h = { h1: -5, h2: 5, tout: h.tout || 0, tin: h.tin || 0 };
  const to = h.tout || 0, ti = h.tin || 0;
  const o = [E.xo, y + to * .5];
  return { o, s1: [[E.xo + dx * .25, y - h.h1 + to], [E.xo + dx * .75, y - h.h1 + ti], [E.xi, y + ti * .5]],
    s2: [[E.xo + dx * .75, y + h.h2 + ti * .3], [E.xo + dx * .25, y + h.h2 + to * .3], o] };
}
function facePath(mood, closed) {
  const p = P[mood] || P.lost, R = eye("R", p, closed), L = eye("L", p, closed), B = p.B, m = p.m;
  const C = (a, b, c) => " C" + pt(a) + " " + pt(b) + " " + pt(c);
  const re = R.s2[2], lo = L.o;
  const bot = m.bot || [m.top[1], m.top[0]];
  return "M128 392" +
    C([112, 340], [72, 300], [80, 228]) +          // left jaw
    C([86, 128], [146, 70], [205, 70]) +            // crown of the head
    C([282, 72], [330, 140], [322, 225]) +          // right temple
    C([318, 252], [298, 214], R.o) +                // cheek sweeps into the right eye
    C(R.s1[0], R.s1[1], R.s1[2]) + C(R.s2[0], R.s2[1], R.s2[2]) +
    C([re[0] + 14, re[1] - 62 - p.lift[0]], [B[0] + 34, B[1] - 6], B) +   // right brow
    C([B[0] - 34, B[1] - 6], [lo[0] - 14, lo[1] - 62 - p.lift[1]], lo) +  // left brow
    C(L.s1[0], L.s1[1], L.s1[2]) + C(L.s2[0], L.s2[1], L.s2[2]) +
    C([108, 228], [176, 234], [198, 212]) +         // under-eye into the nose
    C([210, 232], [180, 250], [202, 258]) +         // nose hook
    C([222, 264], [150, 266], m.ml) +               // to the mouth
    C(m.top[0], m.top[1], m.mr) + C(bot[0], bot[1], m.ml) +
    C([150, 334], [236, 350], [262, 392]);          // chin trail to the neck
}
function pupils(mood) {
  const p = P[mood] || P.lost;
  return [[EYE.R.xi + (EYE.R.xo - EYE.R.xi) / 2 + p.gaze[0], EYE.R.y + p.gaze[1]],
          [EYE.L.xo + (EYE.L.xi - EYE.L.xo) / 2 + p.gaze[0], EYE.L.y + p.gaze[1]], p.pr];
}

/* ── protocol: validate + derive. Safety wins: the highest-priority mood among the
      reported mood and the mood derived from fields is the one shown. Read-only. ── */
function parseTs(j) {
  if (typeof j.ts === "number") return j.ts > 1e12 ? j.ts / 1000 : j.ts;
  if (typeof j.at === "string") { const t = Date.parse(j.at); if (!isNaN(t)) return t / 1000; }
  return null;
}
function validate(j) {
  const err = [], warn = [];
  if (!j || typeof j !== "object" || Array.isArray(j)) return { ok: false, err: ["not a JSON object"], warn };
  if (j.schema !== SCHEMA) err.push('schema must be "' + SCHEMA + '"');
  if (j.authority !== undefined && j.authority !== "æ1") err.push("authority must be æ1 (a face reads published state; it holds no operator authority)");
  if (j.mood !== undefined && ORDER.indexOf(j.mood) < 0) err.push("mood must be one of " + ORDER.join(", "));
  if (j.battery !== undefined && j.battery !== null && (typeof j.battery !== "number" || j.battery < 0 || j.battery > 100)) err.push("battery must be 0–100 or null");
  if (j.armed !== undefined && j.armed !== null && typeof j.armed !== "boolean") err.push("armed must be true, false or null");
  if (j.mode !== undefined && ["DAMP", "STAND", "MOVE", "FAULT_DAMP"].indexOf(j.mode) < 0) warn.push("unknown mode " + JSON.stringify(j.mode) + " reads as lost");
  if (j.mood === undefined && j.mode === undefined) err.push("needs mood or mode");
  ["command", "cmd", "action", "set", "move", "arm", "control"].forEach(k => { if (k in j) warn.push('ignored "' + k + '": the face never controls the robot'); });
  return { ok: err.length === 0, err, warn };
}
function derive(j, nowS, maxAge) {
  maxAge = maxAge == null ? STALE_S : maxAge;
  const c = [];
  if (j.fault === true || j.faulted === true || j.mode === "FAULT_DAMP") c.push("hold");
  const ts = parseTs(j);
  if (j.stale === true || (typeof j.age_ms === "number" && j.age_ms > maxAge * 1000) || (ts != null && nowS != null && nowS - ts > maxAge)) c.push("lost");
  if (typeof j.battery === "number" && j.battery < LOW_BATTERY) c.push("tired");
  if (j.mode === "DAMP") c.push("sleep");
  else if (j.mode === "STAND") c.push(j.armed ? "ready" : "think");
  else if (j.mode === "MOVE") c.push("work");
  else if (j.mode !== undefined) c.push("lost");
  if (ORDER.indexOf(j.mood) >= 0) c.push(j.mood);
  if (!c.length) c.push("lost");
  return c.sort((a, b) => ORDER.indexOf(a) - ORDER.indexOf(b))[0];
}
function demoState(mood) {
  const base = { schema: SCHEMA, who: "asimov", authority: "æ1", mood, means: SHORT[mood], mode: "STAND", armed: false, battery: 80, stale: false };
  if (mood === "hold") Object.assign(base, { mode: "FAULT_DAMP", fault: true });
  if (mood === "lost") base.stale = true;
  if (mood === "tired") Object.assign(base, { battery: 14 });
  if (mood === "sleep") base.mode = "DAMP";
  if (mood === "ready") base.armed = true;
  if (mood === "work") Object.assign(base, { mode: "MOVE", armed: true, battery: 72 });
  return base;
}
if (typeof module !== "undefined") module.exports = { SCHEMA, ORDER, MEANS, SHORT, P, facePath, pupils, validate, derive, demoState, parseTs };
