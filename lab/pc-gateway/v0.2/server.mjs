// PC:// gateway v0.2 · la capa del principal
// First principles, zero dependencies (Node >= 18). One principal. Many agents.
// Context may propagate; authority does not. Evidence ≠ Authority.
import http from "node:http";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const ENV = process.env;
const CFG = {
  port: Number(ENV.PORT || 8787),
  dataDir: ENV.PC_DATA_DIR || "./data",
  principalKey: ENV.PC_PRINCIPAL_KEY || "",          // pc_sk_… full authority; lives only on the droplet
  sessionSecret: ENV.PC_SESSION_SECRET || "",        // HMAC secret for pc_ss_ sessions
  doolaBase: ENV.DOOLA_BASE || "https://api.test.doola.com",
  doolaKey: ENV.DOOLA_API_KEY || "",                 // dk_… never leaves this process
  doolaWebhookSecret: ENV.DOOLA_WEBHOOK_SECRET || "",
};
if (!CFG.principalKey || !CFG.sessionSecret) { console.error("PC_PRINCIPAL_KEY and PC_SESSION_SECRET are required"); process.exit(1); }
const LIVE = CFG.doolaBase === "https://api.doola.com";
fs.mkdirSync(CFG.dataDir, { recursive: true });
const F = (n) => path.join(CFG.dataDir, n);

// ---------- tiny JSON store ----------
const load = (n, d) => { try { return JSON.parse(fs.readFileSync(F(n), "utf8")); } catch { return d; } };
const save = (n, v) => { fs.writeFileSync(F(n) + ".tmp", JSON.stringify(v, null, 2)); fs.renameSync(F(n) + ".tmp", F(n)); };
const idem = load("idempotency.json", {});      // key -> {fp, status, body}
const actions = load("required-actions.json", {}); // id -> action
const revoked = new Set(load("revoked.json", []));

// ---------- 🧶 receipts: append-only SHA-256 chain ----------
const sha = (s) => crypto.createHash("sha256").update(s).digest("hex");
function lastHash() {
  try { const l = fs.readFileSync(F("receipts.jsonl"), "utf8").trim().split("\n").pop(); return l ? JSON.parse(l).hash : "GENESIS"; }
  catch { return "GENESIS"; }
}
function receipt(kind, actor, data) {
  const r = { at: new Date().toISOString(), kind, actor, data, prev: lastHash() };
  r.hash = sha(JSON.stringify({ at: r.at, kind, actor, data, prev: r.prev }));
  fs.appendFileSync(F("receipts.jsonl"), JSON.stringify(r) + "\n");
  return r;
}
function readReceipts() {
  try { return fs.readFileSync(F("receipts.jsonl"), "utf8").trim().split("\n").filter(Boolean).map((l) => JSON.parse(l)); } catch { return []; }
}
function verifyChain() {
  let prev = "GENESIS", n = 0;
  for (const r of readReceipts()) {
    const h = sha(JSON.stringify({ at: r.at, kind: r.kind, actor: r.actor, data: r.data, prev: r.prev }));
    if (r.prev !== prev || r.hash !== h) return { ok: false, brokenAt: n };
    prev = r.hash; n++;
  }
  return { ok: true, length: n, head: prev };
}

// ---------- manifest: what this principal's environment can do ----------
const HUMAN_ONLY = ["send_external", "pay", "change_route", "grant_authority", "formation.create_customer", "formation.create_company", "formation.resolve_action"];
const MANIFEST = {
  schema: "pc.manifest/0.2",
  scheme: "PC://",
  layer: "principal",
  principal: "æ.me",
  avatar: "Wilhælm T",
  status: LIVE ? "live" : "sandbox · DEMO",
  doctrine: ["Many agents. One principal.", "Context may propagate; authority does not.", "Evidence ≠ Authority."],
  capabilities: [
    { id: "capability://formation", provider: "doola", env: LIVE ? "live" : "test", provenance: "doola Partner API v1 (docs.doola.com)",
      agents_may: ["formation.read"], human_only: ["formation.create_customer", "formation.create_company", "formation.resolve_action"] },
  ],
  human_only: HUMAN_ONLY,
  receipts: "sha256-chain from GENESIS",
};

// ---------- envelope ----------
function send(res, status, payload, error = null, extra = {}) {
  res.writeHead(status, { "content-type": "application/json; charset=utf-8", ...extra });
  res.end(JSON.stringify({ payload, error }));
}
const fail = (res, status, code, message) => send(res, status, null, { code, message });

// ---------- auth: two keys, two powers ----------
const b64u = (b) => Buffer.from(b).toString("base64url");
const eq = (a, b) => { const x = Buffer.from(String(a)), y = Buffer.from(String(b)); return x.length === y.length && crypto.timingSafeEqual(x, y); };
function mintSession(agent, caps, ttlSec) {
  const body = { sid: crypto.randomUUID(), agent, caps, exp: Math.floor(Date.now() / 1000) + ttlSec };
  const p = b64u(JSON.stringify(body));
  return { token: "pc_ss_" + p + "." + b64u(crypto.createHmac("sha256", CFG.sessionSecret).update(p).digest()), ...body };
}
function who(req) {
  const t = (req.headers.authorization || "").trim();
  if (!t) return null;
  if (t.startsWith("pc_sk_") && eq(t, CFG.principalKey)) return { role: "principal", id: "æ.me", caps: ["*"] };
  if (t.startsWith("pc_ss_")) {
    const [p, sig] = t.slice(6).split(".");
    const good = b64u(crypto.createHmac("sha256", CFG.sessionSecret).update(p || "").digest());
    if (!sig || !eq(sig, good)) return null;
    const s = JSON.parse(Buffer.from(p, "base64url").toString());
    if (s.exp < Date.now() / 1000 || revoked.has(s.sid)) return null;
    return { role: "agent", id: s.agent, sid: s.sid, caps: s.caps };
  }
  return null;
}
const can = (w, cap) => w && (w.caps.includes("*") || w.caps.includes(cap));

// ---------- doola capability (server-side only) ----------
async function doola(method, p, body, idemKey) {
  const h = { "content-type": "application/json" };
  if (CFG.doolaKey) h.authorization = CFG.doolaKey; // on Hark's sandbox the key is injected on the wire instead
  if (idemKey) h["idempotency-key"] = idemKey;
  const r = await fetch(CFG.doolaBase + p, { method, headers: h, body: body ? JSON.stringify(body) : undefined });
  const text = await r.text();
  let j; try { j = text ? JSON.parse(text) : { payload: null, error: null }; } catch { j = { payload: null, error: { code: "BAD_UPSTREAM", message: text.slice(0, 200) } }; }
  return { status: r.status, ...j };
}
const EXEC = {
  "formation.create_customer": (a) => doola("POST", "/v1/partner/customers", a.body, a.id),
  "formation.create_company": (a) => doola("POST", "/v1/partner/companies", a.body, a.id),
};

// ---------- body ----------
const readBody = (req) => new Promise((ok, no) => {
  const c = []; let n = 0;
  req.on("data", (d) => { n += d.length; if (n > 1e6) { no(new Error("too large")); req.destroy(); } else c.push(d); });
  req.on("end", () => ok(Buffer.concat(c))); req.on("error", no);
});

// ---------- docs for agents ----------
const LLMS = `# PC:// gateway · la capa del principal
> Agent Instructions
> Send your session token raw in the Authorization header (pc_ss_…). Never ask for the principal key.
> Every response is {payload, error}. Branch on error.code, never on the message.
> Every POST needs an Idempotency-Key header. Same key + same body replays the same answer.
> Consequential actions do not execute: they become a required action that only the principal resolves.
> Read state with GET; do not poll. Webhooks + reconciliation keep state fresh.

GET  /v1/manifest                      public: capabilities, authority, provenance
POST /v1/sessions                      principal only: {agent, caps[], ttl} -> pc_ss_ token
POST /v1/sessions/{sid}/revoke         principal only
GET  /v1/formation/references/{name}   caps: formation.read (states, state-fees, countries, naics-codes)
GET  /v1/formation/companies           caps: formation.read
POST /v1/formation/customers           any session -> required action (human_only)
POST /v1/formation/companies           any session -> required action (human_only)
GET  /v1/required-actions              caps: actions.read
POST /v1/required-actions/{id}/resolution  principal only: {decision: approve|deny}
POST /v1/webhooks/doola                X-Doola-Signature HMAC-SHA256 of raw body
POST /v1/reconcile                     principal only: sweep companies, write receipt
GET  /v1/receipts · /v1/receipts/verify  caps: receipts.read
`;

// ---------- router ----------
async function handle(req, res) {
  const url = new URL(req.url, "http://x");
  const p = url.pathname, m = req.method;
  const raw = m === "POST" ? await readBody(req) : Buffer.alloc(0);
  let body = null;
  if (raw.length && p !== "/v1/webhooks/doola") { try { body = JSON.parse(raw.toString()); } catch { return fail(res, 400, "BAD_JSON", "Body must be JSON"); } }

  if (m === "GET" && p === "/llms.txt") { res.writeHead(200, { "content-type": "text/plain; charset=utf-8" }); return res.end(LLMS); }
  if (m === "GET" && p === "/v1/manifest") return send(res, 200, MANIFEST);
  if (m === "GET" && p === "/health") return send(res, 200, { ok: true, env: LIVE ? "live" : "test", chain: verifyChain() });

  // webhooks: authenticated by signature, not by key
  if (m === "POST" && p === "/v1/webhooks/doola") {
    const sig = req.headers["x-doola-signature"];
    if (!CFG.doolaWebhookSecret || !sig) return fail(res, 401, "SIGNATURE_MISSING", "Missing webhook signature");
    const exp = crypto.createHmac("sha256", CFG.doolaWebhookSecret).update(raw).digest("hex");
    if (!eq(exp, sig)) return fail(res, 401, "SIGNATURE_INVALID", "Signature mismatch");
    const ev = JSON.parse(raw.toString());
    const r = receipt("webhook.doola", "doola", { eventName: ev.eventName, timestamp: ev.timestamp, companyId: ev.eventPayload?.companyId, requiredActionId: ev.eventPayload?.requiredActionId });
    return send(res, 200, { received: true, receipt: r.hash });
  }

  const w = who(req);
  if (!w) return fail(res, 401, "UNAUTHENTICATED", "Send a pc_ss_ session or the principal key in Authorization");

  // idempotency on every POST
  let ik = null, fp = null;
  if (m === "POST") {
    ik = req.headers["idempotency-key"];
    if (!ik) return fail(res, 400, "IDEMPOTENCY_KEY_REQUIRED", "Every POST needs an Idempotency-Key");
    fp = sha(m + p + raw.toString());
    const hit = idem[ik];
    if (hit) {
      if (hit.fp !== fp) return fail(res, 409, "IDEMPOTENCY_KEY_REUSED", "Key already used with a different request");
      res.writeHead(hit.status, { "content-type": "application/json; charset=utf-8", "idempotent-replay": "true" });
      return res.end(hit.body);
    }
    const orig = res.end.bind(res);
    res.end = (b) => { idem[ik] = { fp, status: res.statusCode, body: String(b) }; save("idempotency.json", idem); return orig(b); };
  }

  // sessions: the principal mints short, scoped, revocable power
  if (m === "POST" && p === "/v1/sessions") {
    if (w.role !== "principal") return fail(res, 403, "PRINCIPAL_ONLY", "Only the principal mints sessions");
    const caps = (body?.caps || []).filter((c) => c !== "*" && !HUMAN_ONLY.includes(c));
    const s = mintSession(String(body?.agent || "agent"), caps, Math.min(Number(body?.ttl || 3600), 86400));
    receipt("session.minted", w.id, { sid: s.sid, agent: s.agent, caps: s.caps, exp: s.exp });
    return send(res, 201, s);
  }
  let mm;
  if (m === "POST" && (mm = p.match(/^\/v1\/sessions\/([\w-]+)\/revoke$/))) {
    if (w.role !== "principal") return fail(res, 403, "PRINCIPAL_ONLY", "Only the principal revokes");
    revoked.add(mm[1]); save("revoked.json", [...revoked]);
    receipt("session.revoked", w.id, { sid: mm[1] });
    return send(res, 200, { revoked: mm[1] });
  }

  // formation reads: agents may
  if (m === "GET" && (mm = p.match(/^\/v1\/formation\/references\/(states|state-fees|countries|naics-codes)$/))) {
    if (!can(w, "formation.read")) return fail(res, 403, "CAPABILITY_MISSING", "Needs formation.read");
    const r = await doola("GET", "/v1/partner/references/" + mm[1] + url.search);
    return send(res, r.status, r.payload, r.error);
  }
  if (m === "GET" && p === "/v1/formation/companies") {
    if (!can(w, "formation.read")) return fail(res, 403, "CAPABILITY_MISSING", "Needs formation.read");
    const r = await doola("GET", "/v1/partner/companies" + url.search);
    return send(res, r.status, r.payload, r.error);
  }

  // formation writes: never executed by an agent; they become required actions
  if (m === "POST" && (mm = p.match(/^\/v1\/formation\/(customers|companies)$/))) {
    const kind = mm[1] === "customers" ? "formation.create_customer" : "formation.create_company";
    const a = { id: "ra_" + crypto.randomUUID(), kind, requestedBy: w.id, body, status: "PENDING", createdAt: new Date().toISOString() };
    actions[a.id] = a; save("required-actions.json", actions);
    receipt("action.requested", w.id, { id: a.id, kind, bodyHash: sha(JSON.stringify(body)) });
    return send(res, 202, { requiredAction: { id: a.id, kind, status: a.status }, message: "Waiting on the principal" });
  }
  if (m === "GET" && p === "/v1/required-actions") {
    if (!can(w, "actions.read")) return fail(res, 403, "CAPABILITY_MISSING", "Needs actions.read");
    const st = url.searchParams.get("status");
    return send(res, 200, Object.values(actions).filter((a) => !st || a.status === st).map(({ body, ...a }) => a));
  }
  if (m === "POST" && (mm = p.match(/^\/v1\/required-actions\/(ra_[\w-]+)\/resolution$/))) {
    if (w.role !== "principal") return fail(res, 403, "PRINCIPAL_ONLY", "Only the principal resolves required actions");
    const a = actions[mm[1]];
    if (!a) return fail(res, 404, "NOT_FOUND", "No such required action");
    if (a.status !== "PENDING") return fail(res, 409, "ALREADY_RESOLVED", "Action is " + a.status);
    if (body?.decision === "deny") {
      a.status = "DENIED"; save("required-actions.json", actions);
      receipt("action.denied", w.id, { id: a.id });
      return send(res, 200, { id: a.id, status: a.status });
    }
    if (body?.decision !== "approve") return fail(res, 400, "BAD_DECISION", "decision must be approve or deny");
    const r = await EXEC[a.kind](a);   // the action id is the upstream Idempotency-Key: retries never double-file
    a.status = r.error ? "FAILED" : "DONE"; a.result = r.payload; a.resolvedAt = new Date().toISOString();
    save("required-actions.json", actions);
    const rc = receipt("action." + a.status.toLowerCase(), w.id, { id: a.id, kind: a.kind, upstreamStatus: r.status, upstreamError: r.error?.code || null });
    return send(res, r.error ? 502 : 200, { id: a.id, status: a.status, result: r.payload, receipt: rc.hash }, r.error);
  }

  if (m === "POST" && p === "/v1/reconcile") {
    if (w.role !== "principal") return fail(res, 403, "PRINCIPAL_ONLY", "Only the principal reconciles");
    const r = await doola("GET", "/v1/partner/companies?size=100");
    const list = r.payload?.content || [];
    const rc = receipt("reconcile.doola", w.id, { total: r.payload?.total ?? null, companies: list.map((c) => ({ id: c.id || c.companyId, status: c.formationSubmissionStatus || c.status || null })) });
    return send(res, 200, { total: r.payload?.total ?? 0, receipt: rc.hash }, r.error);
  }

  if (m === "GET" && p === "/v1/receipts") {
    if (!can(w, "receipts.read")) return fail(res, 403, "CAPABILITY_MISSING", "Needs receipts.read");
    return send(res, 200, readReceipts().slice(-Number(url.searchParams.get("limit") || 50)));
  }
  if (m === "GET" && p === "/v1/receipts/verify") {
    if (!can(w, "receipts.read")) return fail(res, 403, "CAPABILITY_MISSING", "Needs receipts.read");
    return send(res, 200, verifyChain());
  }
  return fail(res, 404, "NOT_FOUND", "No route " + m + " " + p);
}

http.createServer((req, res) => handle(req, res).catch((e) => fail(res, 500, "INTERNAL", e.message)))
  .listen(CFG.port, "127.0.0.1", () => console.log(`PC:// gateway v0.2 on 127.0.0.1:${CFG.port} · doola ${LIVE ? "LIVE" : "test"}`));
