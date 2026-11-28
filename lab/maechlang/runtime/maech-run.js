/* mæchlæng · maech-run.js · reactive bridge to the real Mech runtime (LAB)
   Mech: https://mech-lang.org · Corey Montella · Apache-2.0 · beta. mæchlæng is not affiliated with Mech.
   runtime/mech_wasm.js + mech_wasm_bg.wasm.gz are the unmodified Mech wasm build (see NOTICE). No CDN.
   Reactive like Mech: Δ input → re-run the whole program → Δ estado. Evidence ≠ Authority. */
(function (root) {
"use strict";
var AGENTS = ["hark-pro", "hermes", "codex"], PRINCIPAL = "yæl";
var AUTH_SRC = "-- mæchlæng · #Authority · æ0–æ3 as a Mech state machine\n-- RUNS on the real Mech runtime (mech-wasm, reports Version 0.3.5), vendored in runtime/.\n-- Mech: mech-lang.org · Corey Montella · Apache-2.0 · beta. mæchlæng is not affiliated with Mech.\n-- Evidence ≠ Authority. Many agents. One principal. Human stays root.\n\n<authority> := :æ0 | :æ1 | :æ2 | :æ3\n<verdict> := :granted | :evidence\n\nagents := {\"hark-pro\", \"hermes\", \"codex\"}\nprincipal := \"yæl\"\n\n-- ⟦inputs⟧ the page rewrites these four lines on every Δ input, then re-runs the whole program\nagent := \"hark-pro\"\nreq := 3u8\npk := false\nwr := false\n-- ⟦/inputs⟧\n\n#Authority(req<u8>, pk<bool>, wr<bool>) ⇒ <verdict>\n  ├ :Context(req<u8>, pk<bool>, wr<bool>)\n  ├ :Evidence(req<u8>, pk<bool>, wr<bool>)\n  ├ :Waiting(req<u8>)\n  └ :Granted(level<u8>).\n\n#Authority(req, pk, wr) → :Context(req, pk, wr)\n  -- æ0 public, æ1 published: an agent may · æ2 operator, æ3 custody: needs the principal\n  :Context(r, pk, wr)\n    ├ r < 2u8 → :Granted(r)\n    └ r > 1u8 → :Evidence(r, pk, wr)\n  -- guard: principal passkey + Witness receipt; otherwise wait (no agent grants æ2/æ3)\n  :Evidence(r, pk, wr)\n    ├ pk && wr → :Granted(r)\n    └ * → :Waiting(r)\n  :Waiting(r) ⇒ :evidence\n  :Granted(l) ⇒ :granted.\n\nstate := #Authority(req, pk, wr)\nout := {state: state, hi: req > 1u8, guard: pk && wr, known: agent ∈ agents}\nout\n";
var FACE_SRC = "-- mæchlæng · #Face · Asimov face moods as a Mech state machine\n-- Same rules as LutheranInstitute/Robot (branch ae-face) ae/face.py · read-only · robot authority æ1.\n-- RUNS on the real Mech runtime (mech-wasm, reports Version 0.3.5), vendored in runtime/.\n-- Mech: mech-lang.org · Corey Montella · Apache-2.0 · beta. mæchlæng is not affiliated with Mech.\n-- Rules run top to bottom, so safety wins.\n\n<mood> := :hold | :lost | :tired | :sleep | :think | :ready | :work\n\n-- ⟦inputs⟧ the page rewrites these five lines on every Δ input, then re-runs the whole program\nmd := \"STAND\"\nar := false\nft := false\nag := 0.05\nsc := 80.0\n-- ⟦/inputs⟧\n\n#Face(md<string>, ar<bool>, ft<bool>, ag<f64>, sc<f64>) ⇒ <mood>\n  ├ :Read(md<string>, ar<bool>, ft<bool>, ag<f64>, sc<f64>)\n  └ :Show(m<mood>).\n\n#Face(md, ar, ft, ag, sc) → :Read(md, ar, ft, ag, sc)\n  -- first match wins: fault latched > no fresh state > battery low > mode; unknown mode ⇒ :lost\n  :Read(md, ar, ft, ag, sc)\n    ├ ft ∨ md ⩵ \"FAULT_DAMP\" → :Show(:hold)\n    ├ ag > 0.5 → :Show(:lost)\n    ├ sc < 20.0 → :Show(:tired)\n    ├ md ⩵ \"DAMP\" → :Show(:sleep)\n    ├ md ⩵ \"STAND\" && ¬ar → :Show(:think)\n    ├ md ⩵ \"STAND\" && ar → :Show(:ready)\n    ├ md ⩵ \"MOVE\" → :Show(:work)\n    └ * → :Show(:lost)\n  :Show(m) ⇒ m.\n\nmood := #Face(md, ar, ft, ag, sc)\nmood\n";
var WASM_SHA256 = "6140624668517b9a08e814453f424cfdab418261dab40359aaae8b8e6da39b89";

/* ---------- JS mirror (same rules; used before the runtime loads and as a cross-check) ---------- */
function authEval(r, pk, wr) {
  var hi = r > 1, guard = pk === true && wr === true, granted = !hi || guard;
  var path = ["entry", hi ? "ctx-hi" : "ctx-lo"];
  if (hi) path.push(guard ? "ev-ok" : "ev-wait");
  path.push(granted ? "done" : "wait");
  return { state: granted ? "granted" : "evidence", hi: hi, guard: guard, path: path };
}
// one step, for the optional ▶ trace replay. s: null|"ctx"|"ev"|"gr"
function authStep(s, r, pk, wr) {
  if (s === null) return { s: "ctx", b: "entry" };
  if (s === "ctx") return r < 2 ? { s: "gr", b: "ctx-lo" } : { s: "ev", b: "ctx-hi" };
  if (s === "ev") return (pk === true && wr === true) ? { s: "gr", b: "ev-ok" } : { s: "ev", b: "ev-wait" };
  return { s: "gr", b: "done" };
}
function faceEval(md, ar, ft, ag, sc) {
  if (ft || md === "FAULT_DAMP") return { m: "hold", b: "ft" };
  if (ag > 0.5) return { m: "lost", b: "ag" };
  if (sc < 20) return { m: "tired", b: "sc" };
  if (md === "DAMP") return { m: "sleep", b: "damp" };
  if (md === "STAND") return ar ? { m: "ready", b: "ready" } : { m: "think", b: "think" };
  if (md === "MOVE") return { m: "work", b: "work" };
  return { m: "lost", b: "unk" };
}
function faceBranch(m, ag) {
  return { hold: "ft", lost: ag > 0.5 ? "ag" : "unk", tired: "sc", sleep: "damp", think: "think", ready: "ready", work: "work" }[m] || "";
}

/* ---------- program text ---------- */
// rewrite `name := value` lines inside the ⟦inputs⟧ block
function withInputs(src, vals) {
  var on = false;
  return src.split("\n").map(function (l) {
    if (l.indexOf("⟦inputs⟧") >= 0) { on = true; return l; }
    if (l.indexOf("⟦/inputs⟧") >= 0) { on = false; return l; }
    if (!on) return l;
    var m = /^([a-z][a-z0-9-]*) := /.exec(l);
    return (m && Object.prototype.hasOwnProperty.call(vals, m[1])) ? m[1] + " := " + vals[m[1]] : l;
  }).join("\n");
}
function authInputs(agent, r, pk, wr) {
  if (AGENTS.indexOf(agent) < 0) agent = AGENTS[0];
  r = Math.max(0, Math.min(3, r | 0));
  return { agent: JSON.stringify(agent), req: r + "u8", pk: String(pk === true), wr: String(wr === true) };
}
function faceInputs(md, ar, ft, ag, sc) {
  if (["DAMP", "STAND", "MOVE", "FAULT_DAMP"].indexOf(md) < 0) md = "UNKNOWN";
  sc = Math.max(0, Math.min(100, Math.round(+sc || 0)));
  return { md: JSON.stringify(md), ar: String(ar === true), ft: String(ft === true), ag: ag > 0.5 ? "0.9" : "0.05", sc: sc + ".0" };
}
var TAGS = {
  auth: [[/^#Authority\(req, pk, wr\) →/, "entry"], [/├ r < 2u8 →/, "ctx-lo"], [/└ r > 1u8 →/, "ctx-hi"],
         [/├ pk && wr →/, "ev-ok"], [/└ \* → :Waiting/, "ev-wait"], [/^\s+:Waiting\(r\) ⇒/, "wait"], [/^\s+:Granted\(l\) ⇒/, "done"],
         [/^(agent|req|pk|wr) := /, "in"]],
  face: [[/├ ft ∨/, "ft"], [/├ ag > 0\.5/, "ag"], [/├ sc < 20\.0/, "sc"], [/├ md ⩵ "DAMP"/, "damp"],
         [/&& ¬ar →/, "think"], [/&& ar →/, "ready"], [/├ md ⩵ "MOVE"/, "work"], [/└ \* → :Show\(:lost\)/, "unk"],
         [/^(md|ar|ft|ag|sc) := /, "in"]]
};
function lineTag(kind, line) {
  var t = TAGS[kind];
  for (var i = 0; i < t.length; i++) if (t[i][0].test(line)) return t[i][1];
  return "";
}
function parseAuth(out) {
  var s = String(out || "").replace(/\s+/g, " ");
  var st = /state<[^>]*>:\s*:(granted|evidence)\b/.exec(s), hi = /hi<bool>:\s*(true|false)/.exec(s),
      g = /guard<bool>:\s*(true|false)/.exec(s), k = /known<bool>:\s*(true|false)/.exec(s);
  if (!st || !hi || !g) return null;
  return { state: st[1], hi: hi[1] === "true", guard: g[1] === "true", known: k ? k[1] === "true" : null };
}
function parseFace(out) {
  var m = /^\s*:(hold|lost|tired|sleep|think|ready|work)\s*$/.exec(String(out || "").replace(/\s+/g, " "));
  return m ? m[1] : null;
}

/* ---------- the real Mech runtime (vendored mech-wasm) ---------- */
var mod = null, loading = null, version = null, broken = null;
function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (x) { return ("0" + x.toString(16)).slice(-2); }).join(""); }
function fetchWasm(url) {
  return fetch(url).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.arrayBuffer(); }).then(function (ab) {
    var b = new Uint8Array(ab);
    if (b[0] === 0x1f && b[1] === 0x8b) {
      if (typeof DecompressionStream === "undefined") throw new Error("este navegador no tiene DecompressionStream");
      return new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream("gzip"))).arrayBuffer();
    }
    return ab;
  }).then(function (ab) {
    if (!(root.crypto && crypto.subtle)) return ab;
    return crypto.subtle.digest("SHA-256", ab).then(function (h) {
      if (hex(h) !== WASM_SHA256) throw new Error("sha256 del wasm no coincide");
      return ab;
    });
  });
}
function useModule(m) { mod = m; version = parseVer(m.help_html && m.help_html()); return version; }
function parseVer(html) { var m = /Version:\s*([0-9][0-9a-z.\-]*)/.exec(String(html || "").replace(/<[^>]+>/g, " ")); return m ? m[1] : "?"; }
function load(base) {
  if (loading) return loading;
  loading = Promise.resolve().then(function () {
    if (typeof WebAssembly === "undefined") throw new Error("sin WebAssembly");
    var imp = new Function("u", "return import(u)");
    var abs = new URL(base, document.baseURI).href;
    return Promise.all([imp(abs + "mech_wasm.js"), fetchWasm(abs + "mech_wasm_bg.wasm.gz")]);
  }).then(function (r) {
    return r[0].default({ module_or_path: r[1] }).then(function () { return useModule(r[0]); });
  });
  loading.catch(function () { loading = null; });
  return loading;
}
function ready() { return !!mod && !broken; }
// run a whole Mech program on a fresh interpreter; returns {ok, out, err, ms}
function run(src) {
  var c = console, ol = c.log, oe = c.error, ow = c.warn, errs = [], out = "", t0 = Date.now(), w = null;
  c.log = function () {}; c.warn = function () {};
  c.error = function () { errs.push(Array.prototype.join.call(arguments, " ")); };
  try { w = new mod.WasmMech(); w.run_program(src); out = w.out_string(); }
  catch (e) { errs.push(String(e && e.message || e)); if (/unreachable|aliasing|RuntimeError/.test(String(e))) broken = String(e); }
  finally { try { if (w) w.free(); } catch (e2) {} c.log = ol; c.error = oe; c.warn = ow; }
  var ok = !errs.length && String(out).trim() !== "_" && String(out).trim() !== "";
  return { ok: ok, out: out, err: errs.join("\n").slice(0, 600), ms: Date.now() - t0 };
}

/* ---------- Witness: h(n) = sha256(h(n-1) + "|" + evento), from GENESIS ---------- */
function Witness() { this.head = null; this.n = 0; this.q = Promise.resolve(); }
Witness.ok = function () { return !!(root.crypto && crypto.subtle && root.TextEncoder); };
Witness.sha = function (t) { return crypto.subtle.digest("SHA-256", new TextEncoder().encode(t)).then(hex); };
Witness.prototype.append = function (evt) {
  var self = this;
  if (!Witness.ok()) return Promise.resolve(null);
  self.q = self.q.then(function () {
    var p = self.head ? Promise.resolve(self.head) : Witness.sha("GENESIS");
    return p.then(function (prev) {
      return Witness.sha(prev + "|" + JSON.stringify(evt)).then(function (h) { self.head = h; self.n += 1; return { n: self.n, h: h }; });
    });
  });
  return self.q;
};

/* ---------- UI: both simulators, reactive (no step-only flow) ---------- */
function mount(o) {
  var d = document, $ = function (id) { return d.getElementById(id); };
  var W = new Witness(), HASH = Witness.ok();
  var reduce = root.matchMedia && root.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var eng = $("eng"), rx = $("rx");
  function el(t, c, x) { var e = d.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function renderCode(pre, kind, src, on, bad, changed) {
    pre.textContent = "";
    src.split("\n").forEach(function (l) {
      var s = el("span", "", l || " "), t = lineTag(kind, l);
      if (t) s.setAttribute("data-b", t);
      if (t && on.indexOf(t) >= 0) s.className = (t === bad ? "no" : "hl");
      if (t === "in" && changed && l.indexOf(changed + " := ") === 0) s.className = "chg";
      pre.appendChild(s);
    });
  }
  function log(box, t) { if (!box) return; box.textContent += t + "\n"; var L = box.textContent.split("\n"); if (L.length > 80) box.textContent = L.slice(-80).join("\n"); box.scrollTop = box.scrollHeight; }
  function pulse(t) { if (!rx) return; rx.textContent = t; rx.classList.remove("blip"); void rx.offsetWidth; if (!reduce) rx.classList.add("blip"); }
  function engLabel() {
    if (!eng) return;
    if (ready()) eng.textContent = "motor: Mech " + version + " · runtime real (wasm, vendorizado, sin CDN) ✓";
    else if (broken) eng.textContent = "motor: espejo JS · el runtime Mech falló (" + broken.slice(0, 60) + ")";
    else if (loading) eng.textContent = "motor: espejo JS · cargando runtime Mech…";
    else eng.textContent = "motor: espejo JS · runtime Mech no cargado";
  }
  function badge(id, how, ms) {
    var b = $(id); if (!b) return;
    if (how === "mech") { b.textContent = "✓ ejecutado en Mech " + version + " · " + ms + " ms"; b.className = "sk ok"; }
    else if (how === "diff") { b.textContent = "⚠ Mech y el espejo JS difieren · manda Mech"; b.className = "sk bad"; }
    else if (how === "err") { b.textContent = "⚠ Mech devolvió error · se muestra el espejo JS"; b.className = "sk bad"; }
    else { b.textContent = "espejo JS · aún no ejecutado en Mech en este navegador"; b.className = "sk"; }
  }

  /* #Authority */
  var A = { agent: $("agent"), req: $("req"), pk: $("pk"), wr: $("wr"), code: $("acode"), log: $("alog"), rc: $("rc") };
  var aLast = null, aTimer = null, lastSrc = "";
  function setS(s) { ["ctx", "ev", "gr"].forEach(function (k) { var e = $("s-" + k); if (e) e.classList.toggle("on", k === s); }); }
  function authNow(reason, changed) {
    if (aTimer) { clearTimeout(aTimer); aTimer = null; }
    var agent = A.agent.value, r = +A.req.value, pk = A.pk.checked, wr = A.wr.checked && HASH;
    var mir = authEval(r, pk, wr), res = mir, how = "js", ms = 0;
    var src = withInputs(AUTH_SRC, authInputs(agent, r, pk, wr)); lastSrc = src;
    if (ready()) {
      var x = run(src), p = x.ok ? parseAuth(x.out) : null; ms = x.ms;
      if (p) { how = (p.state === mir.state && p.hi === mir.hi && p.guard === mir.guard) ? "mech" : "diff";
        var path = ["entry", p.hi ? "ctx-hi" : "ctx-lo"]; if (p.hi) path.push(p.guard ? "ev-ok" : "ev-wait"); path.push(p.state === "granted" ? "done" : "wait");
        res = { state: p.state, hi: p.hi, guard: p.guard, path: path }; }
      else how = "err";
      engLabel();
    }
    renderCode(A.code, "auth", src, res.path, "ev-wait", changed);
    setS(res.state === "granted" ? "gr" : (res.hi ? "ev" : "ctx"));
    badge("abadge", how, ms);
    var st = res.state === "granted" ? ":Granted(æ" + r + ")" : ":Evidence → :Waiting(æ" + r + ")";
    var why = res.state === "granted" ? (res.hi ? "pk && wr ✓" : "r < 2u8 · un agente puede") :
      "falta " + [!pk ? "pk (passkey)" : "", !wr ? "wr (Witness)" : ""].filter(Boolean).join(" + ");
    pulse("reactivo: Δ " + reason + " → " + st);
    var key = [agent, r, pk, wr].join("|");
    if (key === aLast && reason !== "runtime Mech listo") return;
    aLast = key;
    W.append({ t: "authority", agente: agent, principal: PRINCIPAL, req: "æ" + r, pk: pk, wr: wr, estado: res.state, rama: res.path.join(">"),
               motor: how === "mech" ? "mech " + version : "espejo-js", at: new Date().toISOString() }).then(function (w) {
      var tail = w ? "\n   witness #" + w.n + " " + w.h.slice(0, 16) + "…" : "";
      log(A.log, "Δ " + reason + " · " + agent + " pide æ" + r + " ⇒ " + st + " · " + why + (how === "mech" ? " · Mech " + ms + " ms" : " · espejo JS") + tail);
      if (A.rc) A.rc.textContent = w ? "Witness #" + w.n + ": " + w.h : "Witness: este navegador no ofrece crypto.subtle; sin recibo no hay wr.";
    });
  }
  function onA(name) { return function () { stopTrace(); if (name === "wr" && A.wr.checked && !HASH) { A.wr.checked = false; } authNow(name, { agent: "agent", req: "req", pk: "pk", wr: "wr" }[name]); }; }
  ["agent", "req", "pk", "wr"].forEach(function (k) { A[k].addEventListener("change", onA(k)); });
  if (!HASH) { A.wr.disabled = true; }

  /* ▶ trace replay (optional; does not change state) */
  var tr = null, trBtn = $("trace");
  function stopTrace() { if (tr) { clearTimeout(tr); tr = null; } if (trBtn) trBtn.textContent = "▶ trace"; }
  if (trBtn) trBtn.onclick = function () {
    if (tr) { stopTrace(); authNow("trace ⏹"); return; }
    var r = +A.req.value, pk = A.pk.checked, wr = A.wr.checked && HASH, s = null, seen = [], i = 0;
    trBtn.textContent = "⏹ trace";
    log(A.log, "▶ trace · #Authority(" + r + "u8, " + pk + ", " + wr + ")");
    (function tick() {
      var n = authStep(s, r, pk, wr); s = n.s; seen.push(n.b);
      var end = n.b === "done" || n.b === "ev-wait";
      if (end) seen.push(n.b === "done" ? "done" : "wait");
      renderCode(A.code, "auth", lastSrc, seen, "ev-wait"); setS(s);
      log(A.log, "   " + (++i) + " · " + n.b + " → :" + ({ ctx: "Context", ev: "Evidence", gr: "Granted" })[s]);
      if (end || i > 6) { tr = setTimeout(function () { tr = null; stopTrace(); }, reduce ? 0 : 700); return; }
      tr = setTimeout(tick, reduce ? 0 : 700);
    })();
  };

  /* #Face */
  var F = { md: $("fmd"), ar: $("far"), ft: $("fft"), st: $("fst"), sc: $("fsc"), code: $("fcode"), log: $("flog") };
  var FP = { hold: "M60 70l20 20M80 70l-20 20M120 70l20 20M140 70l-20 20|M60 140h80", lost: "M60 80h20M120 80h20|M70 140q30 -10 60 0", tired: "M58 82q12 8 24 0M118 82q12 8 24 0|M70 142h60", sleep: "M58 80q12 10 24 0M118 80q12 10 24 0|M85 140q15 6 30 0", think: "M70 72v18M130 72v18|M75 140h40", ready: "M70 70v22M130 70v22|M65 132q35 22 70 0", work: "M60 80q10 -14 20 0M120 80q10 -14 20 0|M60 128q40 34 80 0" };
  var MEANS = { hold: "fault latched", lost: "no fresh state", tired: "battery low", sleep: "DAMP", think: "STAND, not armed", ready: "STAND, armed", work: "MOVE" };
  var NS = "http://www.w3.org/2000/svg", fLast = null;
  function faceNow(reason, changed, receipt) {
    var md = F.md.value, ar = F.ar.checked, ft = F.ft.checked, ag = F.st.checked ? 0.9 : 0.05, sc = +F.sc.value;
    if ($("fscv")) $("fscv").textContent = sc;
    var mir = faceEval(md, ar, ft, ag, sc), m = mir.m, how = "js", ms = 0;
    var src = withInputs(FACE_SRC, faceInputs(md, ar, ft, ag, sc));
    if (ready()) { var x = run(src), p = x.ok ? parseFace(x.out) : null; ms = x.ms; if (p) { how = p === mir.m ? "mech" : "diff"; m = p; } else how = "err"; engLabel(); }
    var b = faceBranch(m, ag);
    renderCode(F.code, "face", src, [b], "", changed);
    badge("fbadge", how, ms);
    var g = $("fg");
    if (g) {
      g.textContent = "";
      FP[m].split("|").forEach(function (dd) { var e = d.createElementNS(NS, "path"); e.setAttribute("d", dd); g.appendChild(e); });
      var t = d.createElementNS(NS, "text"); t.setAttribute("x", "100"); t.setAttribute("y", "40"); t.setAttribute("text-anchor", "middle"); t.setAttribute("font-size", "22"); t.setAttribute("stroke", "none"); t.setAttribute("fill", "currentColor"); t.setAttribute("font-family", "monospace"); t.textContent = "æ æ æ"; g.appendChild(t);
    }
    if ($("fmood")) $("fmood").textContent = ":" + m;
    var rec = { schema: "ae.face/0.1", who: "asimov", authority: "æ1", mood: m, means: MEANS[m], mode: md, armed: ar, faulted: ft, battery: sc, stale: ag > 0.5, motor: how === "mech" ? "mech " + version : "espejo-js" };
    $("fjson").textContent = JSON.stringify(rec);
    pulse("reactivo: Δ " + reason + " → :" + m);
    // hook: the big æsymov face (runtime/aesymov-face.js) animates to the mood Mech chose
    if (typeof o.onFace === "function") { try { o.onFace({ mood: m, branch: b, how: how, ms: ms, rec: rec, reason: reason }); } catch (eh) {} }
    if (!receipt) return;
    var key = [md, ar, ft, ag, sc].join("|");
    if (key === fLast && reason !== "runtime Mech listo") return;
    fLast = key;
    W.append({ t: "face", mood: m, mode: md, armed: ar, faulted: ft, stale: ag > 0.5, battery: sc, rama: b, motor: rec.motor, at: new Date().toISOString() }).then(function (w) {
      log(F.log, "Δ " + reason + " ⇒ :" + m + " (" + MEANS[m] + ")" + (how === "mech" ? " · Mech " + ms + " ms" : " · espejo JS") + (w ? " · witness #" + w.n + " " + w.h.slice(0, 16) + "…" : ""));
      if ($("frc")) $("frc").textContent = w ? "Witness #" + w.n + " · " + w.h.slice(0, 24) + "…" : "Witness: sin crypto.subtle en este navegador";
    });
  }
  var FN = { fmd: "md", far: "ar", fft: "ft", fst: "ag", fsc: "sc" };
  ["fmd", "far", "fft", "fst"].forEach(function (id) { $(id).addEventListener("change", function () { faceNow(FN[id], FN[id], true); }); });
  F.sc.addEventListener("input", function () { faceNow("sc", "sc", false); });
  F.sc.addEventListener("change", function () { faceNow("sc", "sc", true); });

  /* runtime */
  var lb = $("loadmech");
  function boot() {
    engLabel();
    load(o.base).then(function () {
      engLabel(); if (lb) lb.hidden = true;
      authNow("runtime Mech listo"); faceNow("runtime Mech listo", null, true);
    }, function (e) {
      if (eng) eng.textContent = "motor: espejo JS · runtime Mech no disponible aquí (" + String(e && e.message || e).slice(0, 80) + ")";
      if (lb) { lb.hidden = false; lb.textContent = "↻ reintentar runtime Mech"; }
    });
    engLabel();
  }
  if (lb) lb.onclick = function () { lb.hidden = true; boot(); };
  log(A.log, "cadena Witness desde GENESIS · principal " + PRINCIPAL + " · agentes {" + AGENTS.join(", ") + "}");
  authNow("inicio"); faceNow("inicio", null, true);
  var save = root.navigator && navigator.connection && navigator.connection.saveData;
  if (o.autoload === false || save) { if (lb) { lb.hidden = false; } engLabel(); }
  else setTimeout(boot, 50);
  return { authNow: authNow, faceNow: faceNow, boot: boot, witness: W };
}

var api = { AGENTS: AGENTS, PRINCIPAL: PRINCIPAL, AUTH_SRC: AUTH_SRC, FACE_SRC: FACE_SRC, WASM_SHA256: WASM_SHA256,
  authEval: authEval, authStep: authStep, faceEval: faceEval, faceBranch: faceBranch, withInputs: withInputs,
  authInputs: authInputs, faceInputs: faceInputs, lineTag: lineTag, parseAuth: parseAuth, parseFace: parseFace,
  load: load, useModule: useModule, ready: ready, run: run, Witness: Witness, mount: mount,
  version: function () { return version; } };
if (typeof module !== "undefined" && module.exports) module.exports = api; else root.MaechRun = api;
})(typeof window !== "undefined" ? window : globalThis);
