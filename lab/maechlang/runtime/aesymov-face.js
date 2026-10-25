/* æsymov · aesymov-face.js · the #Face · Asimov demo face, driven by the real Mech runtime (LAB · DEMO)
   Face: 🤖æsymov_face (lab/face/v1): helmet, copper visor, mood filament, 🧿 mind's eye; 7 moods,
   asymptotic easing (τ motor 0.18 s · τ mood 0.9 s), follows your pointer.
   Read-only, robot authority æ1: the face shows what Mech decided; it never moves a robot.
   Mood comes from face.mec run on Mech (mech-lang.org · Corey Montella · Apache-2.0 · beta) via maech-run.js.
   mæchlæng is not affiliated with Mech. No CDN. Evidence ≠ Authority · Human stays root. */
(function (root) {
"use strict";
var MOODS = ["hold", "lost", "tired", "sleep", "think", "ready", "work"];
var ES = { hold: "en espera · falla retenida", lost: "perdido · sin estado fresco", tired: "cansado · batería baja", sleep: "dormido · DAMP",
           think: "pensando · STAND sin armar", ready: "listo · STAND armado", work: "trabajando · MOVE" };
// same filament paths + colours as lab/face/v1
var FIL = {
  hold: ["M96 128 H144", "#ffb000"],
  lost: ["M98 128 q11 -16 22 0 t22 0 M112 140 h16", "#a78bfa"],
  tired: ["M96 126 Q120 142 144 126", "#8899aa"],
  sleep: ["M100 130 H112 M128 130 H140", "#3a6fe0"],
  think: ["M96 128 C106 108 116 148 126 128 S140 112 146 128", "#00f3ff"],
  ready: ["M98 128 L113 140 L144 114", "#39ff88"],
  work: ["M94 128 L102 116 L110 140 L118 116 L126 140 L134 116 L142 140 L148 128", "#ff6a3d"]
};
var POSTURE = { hold: [0, 0], lost: [14, -6], tired: [0, 10], sleep: [0, 16], think: [-6, -4], ready: [0, -3], work: [0, 4] };
var TAU = { motor: 0.18, mood: 0.9 };
// ▶ demo tour: the inputs that make Mech choose each mood (first match wins in face.mec)
var TOUR = [
  { m: "hold",  v: { md: "FAULT_DAMP", ar: false, ft: false, st: false, sc: 80 } },
  { m: "lost",  v: { md: "MOVE", ar: true, ft: false, st: true, sc: 80 } },
  { m: "tired", v: { md: "MOVE", ar: true, ft: false, st: false, sc: 12 } },
  { m: "sleep", v: { md: "DAMP", ar: false, ft: false, st: false, sc: 80 } },
  { m: "think", v: { md: "STAND", ar: false, ft: false, st: false, sc: 80 } },
  { m: "ready", v: { md: "STAND", ar: true, ft: false, st: false, sc: 80 } },
  { m: "work",  v: { md: "MOVE", ar: true, ft: false, st: false, sc: 80 } }
];

// static markup (also inlined in the pages, so the face is visible before any JS runs)
function svg(id) {
  id = id || "aeface";
  var c = FIL.think[1];
  return '<svg id="' + id + '" class="aeface" viewBox="40 6 160 252" role="img" aria-label="æsymov: solo la cara del Asimov 1. Casco negro, visor de cobre, filamento de ánimo y ojo de la mente 🧿 arriba. Solo lectura.">' +
    '<defs><radialGradient id="' + id + '-halo"><stop offset="0" data-k="h0" stop-color="' + c + '" stop-opacity=".22"/><stop offset="1" stop-color="' + c + '" stop-opacity="0"/></radialGradient></defs>' +
    '<g data-k="head">' +
    '<circle cx="120" cy="132" r="118" fill="url(#' + id + '-halo)"/>' +
    '<path d="M52 78 Q52 18 120 18 Q188 18 188 78 V176 Q188 246 120 250 Q52 246 52 176 Z" fill="#141416" stroke="#3a3a3e" stroke-width="2"/>' +
    '<path d="M60 70 Q66 30 120 28" fill="none" stroke="#fff" stroke-opacity=".08" stroke-width="10" stroke-linecap="round"/>' +
    '<rect x="66" y="96" width="108" height="64" rx="30" fill="#05060a" stroke="#b87333" stroke-width="2.5"/>' +
    '<path data-k="fil" d="' + FIL.think[0] + '" fill="none" stroke="' + c + '" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<path d="M52 176 Q60 232 120 240 Q180 232 188 176" fill="none" stroke="#b87333" stroke-opacity=".55" stroke-width="2"/>' +
    '<g fill="#b87333"><circle cx="54" cy="128" r="3"/><circle cx="186" cy="128" r="3"/><circle cx="86" cy="208" r="2.2"/><circle cx="154" cy="208" r="2.2"/></g>' +
    '<g data-k="nazar"><circle class="aenz" cx="120" cy="42" r="15" fill="none" stroke="#3a6fe0" stroke-width="1.5" opacity=".5"/>' +
    '<circle cx="120" cy="42" r="11" fill="#12348f" stroke="#b87333" stroke-width="1.8"/><circle cx="120" cy="42" r="8" fill="#fff"/>' +
    '<circle data-k="iris" cx="120" cy="42" r="5.6" fill="#5fa8ff"/><circle data-k="pupil" cx="120" cy="42" r="2.8" fill="#05060a"/></g>' +
    '</g></svg>';
}

/* ---------- face engine: asymptotic easing toward the mood's posture, or toward your pointer ---------- */
function face(el, o) {
  o = o || {};
  var d = document, q = function (k) { return el.querySelector('[data-k="' + k + '"]'); };
  var P = { head: q("head"), fil: q("fil"), h0: q("h0"), iris: q("iris"), pupil: q("pupil") };
  var reduce = !!(root.matchMedia && root.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var tgt = { mood: "think" }, st = { yaw: 0, pitch: 0, glow: 1 }, finger = null, fingerT = 0, raf = 0, last = 0, seen = true;
  var ease = function (x, t, dt, tau) { return x + (t - x) * (1 - Math.exp(-dt / tau)); };
  function paint() {
    var f = FIL[tgt.mood];
    P.fil.setAttribute("d", f[0]); P.fil.setAttribute("stroke", f[1]); P.h0.setAttribute("stop-color", f[1]);
    el.setAttribute("data-mood", tgt.mood);
  }
  function apply() {
    P.head.setAttribute("transform", "rotate(" + (st.yaw * 0.12).toFixed(2) + " 120 140) translate(0 " + (st.pitch * 0.25).toFixed(2) + ")");
    P.iris.setAttribute("cx", (120 + st.yaw * 0.06).toFixed(2)); P.iris.setAttribute("cy", (42 + st.pitch * 0.05).toFixed(2));
    P.pupil.setAttribute("cx", (120 + st.yaw * 0.09).toFixed(2)); P.pupil.setAttribute("cy", (42 + st.pitch * 0.07).toFixed(2));
    P.fil.setAttribute("opacity", st.glow.toFixed(2));
  }
  function goal(t) {
    var p = POSTURE[tgt.mood], now = (root.performance ? performance.now() : Date.now());
    var here = !reduce && finger && now - fingerT < 3000 && tgt.mood !== "sleep";
    var ty = here ? finger[0] : p[0], tp = here ? finger[1] : p[1];
    if (!reduce && !here) { ty += Math.sin(t / 1400) * 2; tp += Math.sin(t / 1100 + 1) * 1.2; }
    var tg = tgt.mood === "sleep" ? 0.25 : tgt.mood === "work" ? (reduce ? 1 : 0.75 + 0.25 * Math.abs(Math.sin(t / 90))) : 1;
    return [ty, tp, tg];
  }
  function frame(t) {
    raf = 0;
    var dt = Math.min(0.05, (t - (last || t)) / 1000) || 0.016; last = t;
    var g = goal(t);
    st.yaw = ease(st.yaw, g[0], dt, TAU.motor); st.pitch = ease(st.pitch, g[1], dt, TAU.motor); st.glow = ease(st.glow, g[2], dt, TAU.mood);
    apply();
    if (seen && !d.hidden) raf = root.requestAnimationFrame(frame);
  }
  function start() { if (reduce) return; if (!raf && seen && !d.hidden && root.requestAnimationFrame) { last = 0; raf = root.requestAnimationFrame(frame); } }
  function snap() { var g = goal(0); st.yaw = g[0]; st.pitch = g[1]; st.glow = g[2]; apply(); }
  function set(m) {
    if (!FIL[m]) return false;
    tgt.mood = m; paint();
    if (reduce) snap(); else start();
    return true;
  }
  // pointer follow (not with reduced motion; never while asleep)
  var track = o.track || el;
  if (track.addEventListener) {
    var mv = function (e) {
      var r = el.getBoundingClientRect(); if (!r.width) return;
      var x = (e.clientX - (r.left + r.width / 2)) / Math.max(r.width, 1), y = (e.clientY - (r.top + r.height / 2)) / Math.max(r.height, 1);
      finger = [Math.max(-30, Math.min(30, x * 60)), Math.max(-20, Math.min(20, y * 40))];
      fingerT = root.performance ? performance.now() : Date.now(); start();
    };
    track.addEventListener("pointermove", mv);
    track.addEventListener("pointerdown", mv);
    track.addEventListener("pointerleave", function () { finger = null; });
  }
  if (root.IntersectionObserver) new IntersectionObserver(function (es) { seen = es[0].isIntersecting; if (seen) start(); }).observe(el);
  d.addEventListener("visibilitychange", function () { if (!d.hidden) start(); });
  paint(); snap(); start();
  return { set: set, get mood() { return tgt.mood; }, reduce: reduce };
}

/* ---------- wire the top #Face block to maech-run.js (one Mech runtime for #Face and #Authority) ---------- */
function boot(o) {
  var d = document, $ = function (id) { return d.getElementById(id); };
  var host = $("aeface");
  var F = host ? face(host, { track: $("fxbox") || host }) : null;
  var means = $("fmeans"), tourBtn = $("ftour"), tourT = null, tourI = 0;
  var MR = root.MaechRun.mount({ base: o.base, autoload: o.autoload, onFace: function (x) {
    if (F) F.set(x.mood);
    if (means) means.textContent = ES[x.mood] || "";
    var box = $("fxbox"); if (box) box.setAttribute("data-mood", x.mood);
  } });
  var C = { md: $("fmd"), ar: $("far"), ft: $("fft"), st: $("fst"), sc: $("fsc") };
  function put(v) { C.md.value = v.md; C.ar.checked = v.ar; C.ft.checked = v.ft; C.st.checked = v.st; C.sc.value = v.sc; }
  function step() {
    var s = TOUR[tourI % TOUR.length]; tourI++;
    put(s.v);
    MR.faceNow("demo " + tourI + "/7 → :" + s.m, null, true);
    if (tourBtn) tourBtn.setAttribute("aria-label", "demo: " + s.m + " (" + tourI + " de 7)");
  }
  function stop() { if (tourT) { clearTimeout(tourT); tourT = null; } if (tourBtn) { tourBtn.textContent = F && F.reduce ? "▶ demo · paso a paso" : "▶ demo"; tourBtn.setAttribute("aria-pressed", "false"); } }
  if (tourBtn) {
    stop();
    tourBtn.onclick = function () {
      // reduced motion: no autoplay; each tap shows the next mood
      if (F && F.reduce) { if (tourI >= TOUR.length) tourI = 0; step(); tourBtn.textContent = tourI >= TOUR.length ? "▶ demo · otra vez" : "▶ demo · siguiente (" + (tourI + 1) + "/7)"; return; }
      if (tourT) { stop(); return; }
      tourI = 0; tourBtn.textContent = "⏹ demo"; tourBtn.setAttribute("aria-pressed", "true");
      (function tick() { step(); tourT = tourI < TOUR.length ? setTimeout(tick, 2200) : setTimeout(stop, 2200); })();
    };
  }
  // any human touch on a control ends the tour; the human stays root
  ["fmd", "far", "fft", "fst", "fsc"].forEach(function (id) { var e = $(id); if (e) { e.addEventListener("change", stop); e.addEventListener("input", stop); } });
  return { face: F, mech: MR, stop: stop, step: step };
}

var api = { MOODS: MOODS, ES: ES, FIL: FIL, POSTURE: POSTURE, TAU: TAU, TOUR: TOUR, svg: svg, face: face, boot: boot };
if (typeof module !== "undefined" && module.exports) module.exports = api; else root.AesymovFace = api;
})(typeof window !== "undefined" ? window : globalThis);
