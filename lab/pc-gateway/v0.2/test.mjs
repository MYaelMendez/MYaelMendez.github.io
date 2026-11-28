// End-to-end test of the PC:// gateway against the doola sandbox.
// Usage: PC_PRINCIPAL_KEY=pc_sk_… PC_SESSION_SECRET=… DOOLA_WEBHOOK_SECRET=… node test.mjs [baseUrl]
import crypto from "node:crypto";
const B = process.argv[2] || "http://127.0.0.1:8787";
const PK = process.env.PC_PRINCIPAL_KEY, WS = process.env.DOOLA_WEBHOOK_SECRET;
const k = () => crypto.randomUUID();
async function call(method, p, auth, body, ik, extra = {}) {
  const h = { "content-type": "application/json", ...extra };
  if (auth) h.authorization = auth;
  if (ik) h["idempotency-key"] = ik;
  const r = await fetch(B + p, { method, headers: h, body: body === undefined ? undefined : (typeof body === "string" ? body : JSON.stringify(body)) });
  const j = await r.json().catch(() => null);
  return { s: r.status, j, replay: r.headers.get("idempotent-replay") };
}
let pass = 0, failN = 0;
const ok = (name, cond, info = "") => { cond ? pass++ : failN++; console.log((cond ? "✓ " : "✗ ") + name + (info ? "  · " + info : "")); };

const man = await call("GET", "/v1/manifest");
ok("manifest is public", man.s === 200 && man.j.payload.scheme === "PC://");
ok("no auth -> UNAUTHENTICATED", (await call("GET", "/v1/receipts")).j.error.code === "UNAUTHENTICATED");

const sk = k();
const sess = await call("POST", "/v1/sessions", PK, { agent: "hermes", caps: ["formation.read", "actions.read", "receipts.read", "*", "pay"], ttl: 600 }, sk);
ok("principal mints session", sess.s === 201, "caps=" + sess.j.payload.caps.join(","));
ok("session cannot carry * or human_only caps", !sess.j.payload.caps.includes("*") && !sess.j.payload.caps.includes("pay"));
const AG = sess.j.payload.token;
const again = await call("POST", "/v1/sessions", PK, { agent: "hermes", caps: ["formation.read", "actions.read", "receipts.read", "*", "pay"], ttl: 600 }, sk);
ok("idempotent replay returns same session", again.replay === "true" && again.j.payload.sid === sess.j.payload.sid);
ok("key reuse with different body -> 409", (await call("POST", "/v1/sessions", PK, { agent: "other" }, sk)).j.error.code === "IDEMPOTENCY_KEY_REUSED");
ok("POST without Idempotency-Key -> 400", (await call("POST", "/v1/sessions", PK, { agent: "x" })).j.error.code === "IDEMPOTENCY_KEY_REQUIRED");
ok("agent cannot mint sessions", (await call("POST", "/v1/sessions", AG, { agent: "x" }, k())).j.error.code === "PRINCIPAL_ONLY");

const fees = await call("GET", "/v1/formation/references/state-fees?entityType=LLC", AG);
const wy = fees.j.payload?.find?.((x) => x.state === "WY");
ok("agent reads doola state fees through PC://", fees.s === 200 && !!wy, "WY LLC = $" + (wy?.priceInCents / 100));

const req = await call("POST", "/v1/formation/customers", AG, { email: "pc-gateway-test@llm.store", firstName: "Wilhaelm", lastName: "Test", countryOfResidence: "USA" }, k());
ok("agent write becomes a required action (202)", req.s === 202, req.j.payload?.requiredAction?.id);
const raId = req.j.payload.requiredAction.id;
ok("agent cannot resolve it", (await call("POST", `/v1/required-actions/${raId}/resolution`, AG, { decision: "approve" }, k())).j.error.code === "PRINCIPAL_ONLY");
const pend = await call("GET", "/v1/required-actions?status=PENDING", AG);
ok("agent sees it pending", pend.j.payload.some((a) => a.id === raId));
const res = await call("POST", `/v1/required-actions/${raId}/resolution`, PK, { decision: "approve" }, k());
ok("principal approves -> doola sandbox executes", res.s === 200 && res.j.payload.status === "DONE", "customerId=" + (res.j.payload.result?.id || res.j.payload.result?.doolaCustomerId || JSON.stringify(res.j.error)));
ok("cannot resolve twice", (await call("POST", `/v1/required-actions/${raId}/resolution`, PK, { decision: "approve" }, k())).j.error.code === "ALREADY_RESOLVED");

const ev = JSON.stringify({ eventName: "company_formation_completed", eventPayload: { companyId: "test-co" }, timestamp: Date.now() });
const sig = crypto.createHmac("sha256", WS).update(ev).digest("hex");
ok("signed webhook accepted", (await call("POST", "/v1/webhooks/doola", null, ev, null, { "x-doola-signature": sig })).s === 200);
ok("forged webhook rejected", (await call("POST", "/v1/webhooks/doola", null, ev, null, { "x-doola-signature": "00" + sig.slice(2) })).j.error.code === "SIGNATURE_INVALID");

const rec = await call("POST", "/v1/reconcile", PK, {}, k());
ok("principal reconciles with doola", rec.s === 200, "companies=" + rec.j.payload.total);

await call("POST", `/v1/sessions/${sess.j.payload.sid}/revoke`, PK, {}, k());
ok("revoked session is dead", (await call("GET", "/v1/receipts/verify", AG)).j.error.code === "UNAUTHENTICATED");
const v = await call("GET", "/v1/receipts/verify", PK);
ok("receipt chain verifies from GENESIS", v.j.payload.ok, "length=" + v.j.payload.length);

console.log(`\n${pass} passed · ${failN} failed`);
process.exit(failN ? 1 : 0);
