// >_æ:// governed robot — modules/authority.js
// Brand: >_æ:// governed robot · HUMAN://ROOT · receipts on every action · authority not transferable.
//
// Self-contained ES module (no dependencies). Runs in the browser and in Node.
// Ledger: append-only hash chain of receipts {seq, ts, actor, action, meta, prev, hash}.
// Hash: SHA-256 (crypto.subtle) over canonical JSON of {seq, ts, actor, action, meta, prev},
//       hex-encoded; `prev` links to the previous receipt hash, or 'GENESIS' for the first.
// Persistence: localStorage when available, in-process Map otherwise; written after every mutation.
//
// Quick use:
//   const auth = new Authority();                       // key 'æ.governed.ledger'
//   await auth.issue('mask.setProgram', { program: 'FACE' });
//   const req = await auth.request('led.strip');        // pending, NOT executed
//   await auth.approve(req.id);                         // executes + receipt
//   await auth.refuse(req.id, 'veto');                  // receipted refusal
//   auth.list(20); await auth.verify(); auth.clear();

export const ROLES = ['HUMAN://ROOT', 'æ://POLICY', 'robot://BODY'];
export const VERBS = ['read', 'render', 'plan', 'exec', 'sim', 'receipt', 'ledger', 'grant'];

const GENESIS = 'GENESIS';
const DEFAULT_KEY = 'æ.governed.ledger';
// 'wætz' is the robot's own signing hand (self-issued receipts, e.g. sim/exec telemetry).
const SELF_ACTORS = new Set([...ROLES, 'wætz']);

// --- storage ------------------------------------------------------------------
// localStorage is the primary sink. A module-level Map stands in when it is absent
// (Node, private mode, storage denied) so same-key instances still share the ledger.
const memStore = new Map();

function storageGet(key) {
  try {
    if (typeof localStorage !== 'undefined') {
      const raw = localStorage.getItem(key);
      if (raw != null) return raw;
    }
  } catch { /* storage denied — fall through to memory */ }
  return memStore.has(key) ? memStore.get(key) : null;
}

function storageSet(key, value) {
  memStore.set(key, value);
  try {
    if (typeof localStorage !== 'undefined') localStorage.setItem(key, value);
  } catch { /* quota/deny — memory copy still covers this process */ }
}

// --- helpers ------------------------------------------------------------------
// Non-crypto helper for fallback tests: FNV-1a 32-bit, 8 hex chars.
export function fnv(str) {
  let h = 0x811c9dc5;
  const s = String(str);
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h.toString(16).padStart(8, '0');
}

// Deep-copy meta so later caller-side mutation cannot silently alter the ledger.
function cloneMeta(meta) {
  if (meta == null) return {};
  try { return JSON.parse(JSON.stringify(meta)); } catch { return { ...meta }; }
}

// Deterministic SHA-256 hex of the canonical JSON. Falls back to a 64-char FNV
// composition only when crypto.subtle is unavailable (tests on old runtimes).
async function sha256Hex(value) {
  const json = JSON.stringify(value);
  try {
    if (globalThis.crypto && globalThis.crypto.subtle) {
      const bytes = new TextEncoder().encode(json);
      const digest = await globalThis.crypto.subtle.digest('SHA-256', bytes);
      return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
    }
  } catch { /* fall through to non-crypto mode */ }
  const a = fnv(json);
  const b = fnv(a + json);
  const c = fnv(b + json);
  const d = fnv(c + json);
  return (a + b + c + d).slice(0, 64).padEnd(64, '0');
}

// --- Authority ----------------------------------------------------------------
export class Authority {
  // Loads the persisted record (array of receipts, or {receipts, pending, ...})
  // from localStorage/storageKey when available.
  constructor(storageKey = DEFAULT_KEY) {
    this.storageKey = storageKey;
    this._handlers = {};
    this._seq = 1;      // next receipt sequence number
    this._reqSeq = 1;   // next pending-request id
    this.receipts = []; // the ledger (append-only)
    this.state = { authority: 'HUMAN://ROOT', status: 'IDLE', pending: null };
    this._load();
  }

  _load() {
    const raw = storageGet(this.storageKey);
    if (!raw) return;
    let rec;
    try { rec = JSON.parse(raw); } catch { return; }
    const list = Array.isArray(rec) ? rec : (rec && Array.isArray(rec.receipts) ? rec.receipts : null);
    if (!list) return;
    this.receipts = list.filter((r) => r && typeof r === 'object' && Number.isInteger(r.seq));
    const maxSeq = this.receipts.reduce((m, r) => Math.max(m, r.seq), 0);
    const hinted = Number(rec && rec.nextSeq) || 0;
    this._seq = Math.max(maxSeq + 1, hinted, 1);
    this._reqSeq = Number(rec && rec.nextReq) || 1;
    if (rec && rec.authority && SELF_ACTORS.has(rec.authority)) this.state.authority = rec.authority;
    if (rec && rec.pending && rec.pending.id != null) this.state.pending = rec.pending;
    this.state.status = this.state.pending ? 'PENDING' : 'IDLE';
  }

  _persist() {
    storageSet(this.storageKey, JSON.stringify({
      v: 1,
      receipts: this.receipts,
      pending: this.state.pending,
      authority: this.state.authority,
      nextSeq: this._seq,
      nextReq: this._reqSeq,
    }));
  }

  _setState(patch) {
    this.state = { ...this.state, ...patch };
    this._persist();
  }

  _takePending(id) {
    const pending = this.state.pending;
    if (!pending || String(pending.id) !== String(id)) throw new Error(`UNKNOWN_REQUEST: ${id}`);
    return pending;
  }

  // Execute `action` immediately and return its receipt.
  // actor defaults to state.authority; meta.actor may override ('wætz' for self-signing).
  async issue(action, meta = {}) {
    if (typeof action !== 'string' || !action) throw new Error('ACTION_REQUIRED');
    const clean = cloneMeta(meta);
    const actor = clean.actor != null ? clean.actor : this.state.authority;
    delete clean.actor; // actor is a first-class receipt field, not buried in meta
    if (!SELF_ACTORS.has(actor)) throw new Error(`UNSIGNED_ACTOR: ${actor}`);
    const seq = this._seq++;
    const prev = this.receipts.length ? this.receipts[this.receipts.length - 1].hash : GENESIS;
    const body = { seq, ts: Date.now(), actor, action, meta: clean, prev };
    const hash = await sha256Hex(body);
    const receipt = { ...body, hash };
    this.receipts.push(receipt);
    this._persist();
    this.emit('receipt', receipt);
    return receipt;
  }

  // Approve a pending request: the requested action executes and is receipted.
  async approve(id) {
    const request = this._takePending(id);
    const receipt = await this.issue(request.action, {
      ...request.meta,
      requestId: request.id,
      decision: 'approved',
      decidedBy: this.state.authority,
    });
    this._setState({ status: 'IDLE', pending: null });
    this.emit('approved', { request, receipt });
    return receipt;
  }

  // Refuse a pending request: no execution, but the refusal is receipted.
  async refuse(id, reason = '') {
    const request = this._takePending(id);
    const note = String(reason ?? '');
    const receipt = await this.issue('refuse', {
      requestId: request.id,
      requestedAction: request.action,
      reason: note,
    });
    this._setState({ status: 'IDLE', pending: null });
    this.emit('refused', { request, reason: note, receipt });
    return receipt;
  }

  // Create a pending request. Does NOT execute anything until approve().
  async request(action, meta = {}) {
    if (typeof action !== 'string' || !action) throw new Error('ACTION_REQUIRED');
    const pending = {
      id: this._reqSeq++,
      action,
      meta: cloneMeta(meta),
      ts: Date.now(),
      requestedBy: this.state.authority,
    };
    this._setState({ status: 'PENDING', pending });
    return pending;
  }

  // Most recent receipts (copies), newest last; default 20.
  list(limit = 20) {
    const n = Number.isFinite(limit) ? Math.max(0, Math.floor(limit)) : 20;
    if (n === 0) return [];
    return this.receipts.slice(-n).map((r) => ({ ...r, meta: cloneMeta(r.meta) }));
  }

  // Recompute the whole chain; true only if every hash and link is intact.
  async verify() {
    try {
      let prev = GENESIS;
      for (let i = 0; i < this.receipts.length; i++) {
        const r = this.receipts[i];
        if (!r || typeof r !== 'object') return false;
        if (r.seq !== i + 1) return false;
        if (r.prev !== prev) return false;
        if (typeof r.hash !== 'string' || !/^[0-9a-f]{64}$/.test(r.hash)) return false;
        const expect = await sha256Hex({
          seq: r.seq, ts: r.ts, actor: r.actor, action: r.action, meta: r.meta, prev: r.prev,
        });
        if (expect !== r.hash) return false;
        prev = r.hash;
      }
      return true;
    } catch {
      return false;
    }
  }

  // Reset the ledger and state. Emits 'cleared'.
  clear() {
    this.receipts = [];
    this._seq = 1;
    this._reqSeq = 1;
    this._setState({ authority: 'HUMAN://ROOT', status: 'IDLE', pending: null });
    this.emit('cleared', { ts: Date.now() });
  }

  // Subscribe; returns an unsubscribe function.
  on(event, cb) {
    if (typeof cb !== 'function') throw new Error('HANDLER_REQUIRED');
    (this._handlers[event] ||= []).push(cb);
    return () => {
      const arr = this._handlers[event];
      const i = arr ? arr.indexOf(cb) : -1;
      if (i >= 0) arr.splice(i, 1);
    };
  }

  // Publish to subscribers. Listener errors never break the ledger.
  emit(event, payload) {
    const handlers = this._handlers[event];
    if (!handlers || !handlers.length) return 0;
    let n = 0;
    for (const cb of [...handlers]) {
      try { cb(payload); n++; } catch { /* isolate listener failures */ }
    }
    return n;
  }
}
