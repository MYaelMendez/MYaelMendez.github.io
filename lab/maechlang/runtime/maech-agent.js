/* mæchlæng · maech-agent.js · window.MAECH, the agent surface of the LAB (static, no server)
   "Make something agents want." Agents call the same Mech programs the humans see on the page.
   Mech: https://mech-lang.org · Corey Montella · Apache-2.0 · beta. mæchlæng is not affiliated with Mech.
   Needs runtime/maech-run.js (MaechRun) loaded first. No CDN.

   await MAECH.ready                                   → Mech version string (loads the vendored wasm once)
   MAECH.run(src)                                      → output string (fresh WasmMech per run; throws on Mech error)
   await MAECH.authority({agent, level, pk, wr})       → {state, granted, receipt, ...}
   await MAECH.face({md, armed, fault, stale, battery})→ ae.face/0.1 JSON
   MAECH.witness()                                     → this page's API Witness chain, from GENESIS
   await MAECH.verify()                                → re-hashes the chain: {ok, n}

   Doctrine: Evidence ≠ Authority · agents relay · only the human principal grants æ2/æ3, with pk && wr.
   pk on this LAB page is SIMULATED: any caller can pass pk:true, so a :Granted here is a demo, never authority.
   A real æ2/æ3 grant needs the principal's own passkey (WebAuthn, held by the human), outside this page. */
(function (root) {
"use strict";
var LIVE = "https://lutheraninstitute.github.io/aeee-lab/lab/maechlang/";
var MOODS = ["hold", "lost", "tired", "sleep", "think", "ready", "work"];
var MODES = ["DAMP", "STAND", "MOVE", "FAULT_DAMP"];
var MEANS = { hold: "fault latched", lost: "no fresh state", tired: "battery low", sleep: "DAMP", think: "STAND, not armed", ready: "STAND, armed", work: "MOVE" };
var DOCTRINE = "Evidence ≠ Authority. Many agents. One principal. Human stays root. Agents relay context and evidence; only the human principal grants æ2/æ3, and only with pk && wr (principal passkey + Witness receipt).";
var PK_NOTE = "pk is simulated on this LAB page: any caller can pass pk:true. A :Granted here is a demo, not authority. A real æ2/æ3 grant needs the human principal's own passkey (WebAuthn), outside this page.";

function create(o) {
  o = o || {};
  var MR = o.MR || root.MaechRun;
  if (!MR) throw new Error("MAECH needs runtime/maech-run.js (MaechRun) loaded first");
  var base = o.base || "runtime/";
  var readyP = null, chain = [], q = Promise.resolve(), hasHash = MR.Witness.ok();

  function ready() {
    if (!readyP) {
      readyP = (o.ready ? Promise.resolve(o.ready) : MR.load(base)).then(function () { return MR.version(); });
      readyP.catch(function () { readyP = null; });
    }
    return readyP;
  }
  function engine() { return MR.ready() ? "mech " + MR.version() : "espejo-js"; }

  // run a whole Mech program on a fresh interpreter; returns Mech's output string
  function run(src) {
    if (typeof src !== "string") throw new TypeError("MAECH.run(src): src must be a Mech program string");
    if (!MR.ready()) throw new Error("Mech runtime not loaded yet: await MAECH.ready first");
    var x = MR.run(src);
    if (!x.ok) throw new Error("Mech error: " + (x.err || String(x.out).trim() || "empty output"));
    return x.out;
  }

  // Witness: h(n) = sha256(h(n-1) + "|" + JSON(event)), from sha256("GENESIS")
  function append(evt) {
    if (!hasHash) return Promise.resolve(null);
    q = q.then(function () {
      var p = chain.length ? Promise.resolve(chain[chain.length - 1].h) : MR.Witness.sha("GENESIS");
      return p.then(function (prev) {
        return MR.Witness.sha(prev + "|" + JSON.stringify(evt)).then(function (h) {
          var e = { n: chain.length + 1, prev: prev, h: h, event: evt }; chain.push(e);
          return { n: e.n, h: h, prev: prev };
        });
      });
    });
    return q;
  }
  function witness() { return JSON.parse(JSON.stringify(chain)); }
  function verify() {
    if (!hasHash) return Promise.resolve({ ok: false, n: 0, why: "no crypto.subtle" });
    var c = witness();
    return MR.Witness.sha("GENESIS").then(function (g) {
      var p = Promise.resolve({ ok: true, prev: g });
      c.forEach(function (e) {
        p = p.then(function (s) {
          if (!s.ok) return s;
          return MR.Witness.sha(s.prev + "|" + JSON.stringify(e.event)).then(function (h) {
            return (h === e.h && e.prev === s.prev) ? { ok: true, prev: h } : { ok: false, prev: h, at: e.n };
          });
        });
      });
      return p.then(function (s) { return s.ok ? { ok: true, n: c.length, head: c.length ? s.prev : null } : { ok: false, n: c.length, at: s.at }; });
    });
  }

  function settle() { return ready().then(null, function () { return null; }); }

  // #Authority · agent asks for level æ0–æ3; only booleans count for pk/wr (no truthy tricks)
  function authority(a) {
    a = a || {};
    var agent = a.agent == null ? "hark-pro" : String(a.agent), level = a.level == null ? 3 : a.level;
    if (!/^[a-z0-9][a-z0-9-]{0,31}$/.test(agent)) return Promise.reject(new TypeError("agent: lowercase kebab-case, 1–32 chars [a-z0-9-]"));
    if (typeof level === "string") level = +String(level).replace(/^æ/, "");
    if (!(level === 0 || level === 1 || level === 2 || level === 3)) return Promise.reject(new TypeError("level: 0, 1, 2 or 3 (æ0 public · æ1 published · æ2 operator · æ3 custody)"));
    var pk = a.pk === true, wr = a.wr === true;
    return settle().then(function () {
      var mir = MR.authEval(level, pk, wr), res = { state: mir.state, hi: mir.hi, guard: mir.guard, known: MR.AGENTS.indexOf(agent) >= 0 }, how = "espejo-js", ms = 0, err = null;
      if (MR.ready()) {
        var vals = { agent: JSON.stringify(agent), req: level + "u8", pk: String(pk), wr: String(wr) };
        var x = MR.run(MR.withInputs(MR.AUTH_SRC, vals)), p = x.ok ? MR.parseAuth(x.out) : null; ms = x.ms;
        if (p) { res = p; how = (p.state === mir.state && p.hi === mir.hi && p.guard === mir.guard) ? "mech " + MR.version() : "mech-mirror-diff"; }
        else err = x.err || "unparsed Mech output";
      }
      // belt and braces: whatever any engine says, æ2/æ3 is never granted without pk && wr
      var granted = res.state === "granted" && (level < 2 || (pk && wr));
      var fsm = granted ? ":Granted(æ" + level + ")" : ":Waiting(æ" + level + ")";
      var evt = { t: "authority", via: "MAECH", agent: agent, principal: MR.PRINCIPAL, level: "æ" + level, pk: pk, wr: wr,
                  state: granted ? "granted" : "evidence", engine: how, simulated: level > 1, at: new Date().toISOString() };
      return append(evt).then(function (w) {
        return { state: granted ? "granted" : "evidence", granted: granted, fsm: fsm, level: level, agent: agent, known: res.known,
                 principal: MR.PRINCIPAL, needs: granted ? [] : [!pk ? "pk" : "", !wr ? "wr" : ""].filter(Boolean),
                 engine: how, ms: ms, error: err, simulated: level > 1, authority: level > 1 ? "none: LAB simulation" : "æ" + level,
                 note: level > 1 ? PK_NOTE : "æ0/æ1 need no principal: an agent may.",
                 receipt: w ? { schema: "ae.witness/0.1", n: w.n, h: w.h, prev: w.prev, event: evt } : null };
      });
    });
  }

  // #Face · Asimov mood from robot state; read-only, robot authority æ1
  function face(f, opt) {
    f = f || {};
    var md = f.md == null ? "STAND" : String(f.md).toUpperCase(), ar = f.armed === true, ft = f.fault === true, stale = f.stale === true;
    var sc = f.battery == null ? 80 : +f.battery;
    if (!isFinite(sc)) return Promise.reject(new TypeError("battery: number 0–100"));
    sc = Math.max(0, Math.min(100, Math.round(sc)));
    var mdIn = MODES.indexOf(md) >= 0 ? md : "UNKNOWN", ag = stale ? 0.9 : 0.05;
    return settle().then(function () {
      var m = MR.faceEval(mdIn, ar, ft, ag, sc).m, how = "espejo-js", ms = 0, err = null;
      if (MR.ready()) {
        var x = MR.run(MR.withInputs(MR.FACE_SRC, MR.faceInputs(mdIn, ar, ft, ag, sc))), p = x.ok ? MR.parseFace(x.out) : null; ms = x.ms;
        if (p) { how = p === m ? "mech " + MR.version() : "mech-mirror-diff"; m = p; } else err = x.err || "unparsed Mech output";
      }
      var rec = { schema: "ae.face/0.1", who: "asimov", authority: "æ1", mood: m, means: MEANS[m], mode: mdIn, armed: ar, faulted: ft,
                  battery: sc, stale: stale, motor: how, ms: ms, error: err, readonly: true };
      if (opt && opt.show) show(mdIn, ar, ft, stale, sc);
      return append({ t: "face", via: "MAECH", mood: m, mode: mdIn, armed: ar, faulted: ft, stale: stale, battery: sc, engine: how, at: new Date().toISOString() }).then(function (w) {
        rec.witness = w ? { n: w.n, h: w.h } : null; return rec;
      });
    });
  }
  // optional: put the same inputs on the page's #Face controls so the big face shows it too (read-only demo)
  function show(md, ar, ft, st, sc) {
    var d = root.document; if (!d || !d.getElementById) return;
    var C = { fmd: md, far: ar, fft: ft, fst: st, fsc: sc };
    Object.keys(C).forEach(function (id) {
      var e = d.getElementById(id); if (!e) return;
      if (typeof C[id] === "boolean") e.checked = C[id]; else if (id !== "fmd" || MODES.indexOf(md) >= 0) e.value = C[id];
    });
    var e = d.getElementById("fmd"); if (e && e.dispatchEvent && root.Event) e.dispatchEvent(new root.Event("change"));
  }

  var API = [
    "await MAECH.ready  → Mech version (loads runtime/mech_wasm_bg.wasm.gz once, sha256-checked)",
    "MAECH.run(src)  → output string · fresh WasmMech per run · throws on Mech error",
    "await MAECH.authority({agent:'hark-pro', level:3, pk:false, wr:false})  → {state, granted, fsm, needs, receipt}",
    "await MAECH.face({md:'STAND', armed:true, fault:false, stale:false, battery:80})  → ae.face/0.1 JSON · add {show:true} as 2nd arg to drive the page face",
    "MAECH.witness()  → API Witness chain [{n, prev, h, event}] from sha256('GENESIS')",
    "await MAECH.verify()  → {ok, n, head}"
  ];
  var M = {
    name: "mæchlæng LAB", version: "0.1.0", live: LIVE, manifest: LIVE + "agent.json", llms: LIVE + "llms.txt",
    doctrine: DOCTRINE, pkNote: PK_NOTE, moods: MOODS.slice(), modes: MODES.slice(), agents: MR.AGENTS.slice(), principal: MR.PRINCIPAL,
    run: run, authority: authority, face: face, witness: witness, verify: verify, engine: engine, api: API.slice(),
    help: function () { return "mæchlæng · window.MAECH (LAB)\n" + DOCTRINE + "\n" + PK_NOTE + "\n\n" + API.join("\n") + "\n\nmanifest: " + LIVE + "agent.json\nllms.txt: " + LIVE + "llms.txt"; },
    contact: "point your agents at me 🪡"
  };
  Object.defineProperty(M, "ready", { enumerable: true, get: ready });
  return M;
}

var exp = { create: create, DOCTRINE: DOCTRINE, PK_NOTE: PK_NOTE, MOODS: MOODS, MODES: MODES, MEANS: MEANS, LIVE: LIVE };
if (typeof module !== "undefined" && module.exports) { module.exports = exp; return; }
root.MaechAgent = exp;
// browser: install window.MAECH, resolving the runtime folder from this script's own URL
try {
  var me = root.document && root.document.currentScript, src = me && me.src;
  var base = src ? src.replace(/[^\/]*$/, "") : "runtime/";
  root.MAECH = create({ base: base });
} catch (e) { if (root.console) console.warn("MAECH:", e && e.message); }
})(typeof window !== "undefined" ? window : globalThis);
