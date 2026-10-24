// Browser/Node reference runtime. Fixed local capabilities only; no provider execution.
import {sha256Hex} from './sha256.mjs';
const uuid = () => {
  if (crypto.randomUUID) return crypto.randomUUID();
  const bytes = crypto.getRandomValues(new Uint8Array(16)); bytes[6]=(bytes[6]&15)|64;bytes[8]=(bytes[8]&63)|128;
  const hex=[...bytes].map(n=>n.toString(16).padStart(2,'0')).join('');
  return `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20)}`;
};
const clone = value => structuredClone(value);
const terminal = new Set(['RETURNED', 'CANCELLED', 'EXPIRED']);
const text = (value, name, max = 20000) => {
  if (typeof value !== 'string' || !value.trim() || value.length > max) throw new Error(`Invalid ${name}`);
  return value;
};
const integer = (value, min, max, name) => {
  if (!Number.isSafeInteger(value) || value < min || value > max) throw new Error(`Invalid ${name}`);
  return value;
};
const canonical = value => {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
};
export async function digest(value) {
  const bytes = new TextEncoder().encode(canonical(value));
  if (!crypto.subtle) return sha256Hex(bytes);
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(n => n.toString(16).padStart(2, '0')).join('');
}
export const capabilities = Object.freeze([
  Object.freeze({id: 'text.inspect', label: 'Inspect text', effect: 'local', description: 'Count words, lines and characters in selected text.'}),
  Object.freeze({id: 'draft.compose', label: 'Compose a draft', effect: 'local', description: 'Format a title and body into an unsent local draft.'})
]);
function validatePayload(capability, payload) {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) throw new Error('Invalid payload');
  const keys = Object.keys(payload).sort().join(',');
  if (capability === 'text.inspect' && keys === 'text') return {text: text(payload.text, 'text')};
  if (capability === 'draft.compose' && keys === 'body,title') return {title: text(payload.title, 'title', 200), body: text(payload.body, 'body')};
  throw new Error('Unsupported local capability or payload');
}
const perform = (capability, payload) => capability === 'text.inspect'
  ? {characters: [...payload.text].length, words: payload.text.trim().split(/\s+/u).length, lines: payload.text.split(/\r?\n/u).length}
  : {draft: `${payload.title}\n\n${payload.body}`, sent: false};

export async function verifyEvidence(events, {head, count} = {}) {
  try {
  if (!Array.isArray(events) || !Number.isSafeInteger(count) || count !== events.length || typeof head !== 'string') return false;
  let previous = '';
  for (let i = 0; i < events.length; i++) {
    const {hash, ...body} = events[i];
    if (body.sequence !== i + 1 || body.previousHash !== previous || hash !== await digest(body)) return false;
    previous = hash;
  }
  return previous === head;
  } catch { return false; }
}

export function createPrimitives({principalId, maxDepth = 3, maxOpen = 4, maxNodes = 64, now = () => Date.now()} = {}) {
  text(principalId, 'principal', 200);
  integer(maxDepth, 1, 8, 'depth limit'); integer(maxOpen, 1, 16, 'open task limit'); integer(maxNodes, 2, 256, 'node limit');
  const nodes = new Map(), tokens = new WeakMap(), approvals = [], events = [];
  let rootId = null, serial = Promise.resolve();
  const exclusive = work => { const result = serial.then(work); serial = result.catch(() => {}); return result; };
  const get = id => { const node = nodes.get(id); if (!node) throw new Error('Unknown conversation'); return node; };
  const timestamp = () => new Date(now()).toISOString();
  const view = node => clone(node);
  const correlationId = uuid();
  async function record(type, node, payload = {}) {
    const body = {id: uuid(), sequence: events.length + 1, type, conversationId: node.id, parentId: node.parentId,
      principalId, correlationId, occurredAt: timestamp(), previousHash: events.at(-1)?.hash || '', payload: clone(payload)};
    const event = {...body, hash: await digest(body)}; events.push(event); return event;
  }
  async function expire() {
    for (const node of nodes.values()) {
      if (!terminal.has(node.status) && node.deadline <= now()) {node.status = 'EXPIRED'; await record('conversation.expired', node);}
    }
  }
  async function live(id) {
    await expire(); const node = get(id);
    for (let ancestor = node; ancestor; ancestor = ancestor.parentId ? get(ancestor.parentId) : null) {
      if (terminal.has(ancestor.status)) throw new Error(`Conversation ${ancestor.status.toLowerCase()}`);
    }
    return node;
  }
  const action = node => ({id: node.id, principalId, correlationId, revision: node.revision, capability: node.capability, payload: node.payload, contextRefs: node.contextRefs, deadline: node.deadline});
  const snapshot = () => ({mode: 'local-reference', principalId, correlationId, limits: {maxDepth, maxOpen, maxNodes}, nodes: [...nodes.values()].map(view), approvals: clone(approvals),
    events: clone(events), anchor: {head: events.at(-1)?.hash || '', count: events.length}});
  return Object.freeze({
    createRoot: ({intent, context = [], ttlMs = 600000} = {}) => exclusive(async () => {
      if (rootId) throw new Error('Root already exists');
      text(intent, 'intent', 1000); integer(ttlMs, 1, 3600000, 'TTL');
      if (!Array.isArray(context) || context.length > 16) throw new Error('Invalid context');
      const refs = context.map(ref => ({id: text(ref?.id, 'context id', 100), text: text(ref?.text, 'context text'), source: text(ref?.source, 'context source', 1000)}));
      if (new Set(refs.map(ref => ref.id)).size !== refs.length) throw new Error('Duplicate context id');
      const node = {id: uuid(), parentId: null, principalId, intent, status: 'RUNNING', revision: 1, depth: 0, deadline: now() + ttlMs, contextRefs: refs, children: [], result: null};
      rootId = node.id; nodes.set(node.id, node); await record('intent.created', node); return view(node);
    }),
    proposeChild: ({parentId, intent, capability, payload, contextIds = [], ttlMs = 300000} = {}) => exclusive(async () => {
      const parent = await live(parentId); text(intent, 'intent', 1000); integer(ttlMs, 1, 3600000, 'TTL');
      if (parent.depth >= maxDepth) throw new Error('Depth limit reached');
      if (nodes.size >= maxNodes) throw new Error('Node limit reached');
      if ([...nodes.values()].filter(n => n.parentId && !terminal.has(n.status)).length >= maxOpen) throw new Error('Open task limit reached');
      if (!Array.isArray(contextIds) || new Set(contextIds).size !== contextIds.length) throw new Error('Invalid context selection');
      const refs = contextIds.map(id => {const ref = parent.contextRefs.find(r => r.id === id); if (!ref) throw new Error('Context unavailable to parent'); return clone(ref);});
      const normalized = validatePayload(capability, clone(payload));
      const node = {id: uuid(), parentId, principalId, intent, capability, payload: normalized, contextRefs: refs, depth: parent.depth + 1,
        deadline: Math.min(parent.deadline, now() + ttlMs), revision: 1, status: 'PROPOSED', children: [], result: null};
      nodes.set(node.id, node); parent.children.push(node.id); await record('conversation.proposed', node, {capability, contextIds}); return view(node);
    }),
    revise: (id, {payload, intent} = {}) => exclusive(async () => {
      const node = await live(id); if (!node.parentId || !['PROPOSED', 'QUEUED'].includes(node.status)) throw new Error('Cannot revise this state');
      const normalized = validatePayload(node.capability, clone(payload)); const nextIntent = intent === undefined ? node.intent : text(intent, 'intent', 1000);
      node.payload = normalized; node.intent = nextIntent; node.revision++; node.status = 'PROPOSED';
      await record('conversation.revised', node, {revision: node.revision}); return view(node);
    }),
    approveLocal: (id, {actor, ttlMs = 60000} = {}) => exclusive(async () => {
      const node = await live(id);
      if (actor !== principalId) throw new Error('Principal mismatch');
      if (!node.parentId || !['PROPOSED', 'QUEUED'].includes(node.status)) throw new Error('Cannot approve this state');
      integer(ttlMs, 1, 300000, 'approval TTL');
      const hash = await digest(action(node)); const token = Object.freeze({});
      const approval = {id: uuid(), conversationId: id, actor, revision: node.revision, payloadHash: hash,
        expiresAt: Math.min(now() + ttlMs, node.deadline), consumed: false, revoked: false, mode: 'local-confirmation'};
      tokens.set(token, approval); approvals.push(approval); node.status = 'QUEUED'; await record('approval.recorded', node, {approvalId: approval.id, payloadHash: hash}); return token;
    }),
    revokeLocal: token => exclusive(async () => {
      const approval = tokens.get(token); if (!approval || approval.consumed || approval.revoked) throw new Error('Invalid approval');
      approval.revoked = true; await record('approval.revoked', get(approval.conversationId), {approvalId: approval.id});
    }),
    executeLocal: (id, token) => exclusive(async () => {
      const node = await live(id); const approval = tokens.get(token);
      const hash = node.parentId ? await digest(action(node)) : null;
      if (node.children.some(childId => get(childId).status !== 'RETURNED') || node.status !== 'QUEUED' || !approval || approval.conversationId !== id || approval.revoked || approval.consumed || approval.expiresAt <= now() ||
          approval.revision !== node.revision || approval.payloadHash !== hash) {
        await record('execution.denied', node, {reason: 'Missing, expired, revoked, consumed or mismatched local approval'}); throw new Error('Valid local approval required');
      }
      approval.consumed = true; node.status = 'RUNNING'; await record('execution.started', node, {approvalId: approval.id});
      const result = perform(node.capability, node.payload); node.result = clone(result); node.status = 'RETURNED';
      const receipt = await record('result.returned', node, {capability: node.capability, revision: node.revision, result, evidence: 'locally-computed', externalEffects: false});
      return {node: view(node), result: clone(result), receipt: clone(receipt)};
    }),
    cancel: (id, {actor} = {}) => exclusive(async () => {
      if (actor !== principalId) throw new Error('Principal mismatch');
      const target = get(id); if (terminal.has(target.status)) throw new Error('Already terminal');
      const descend = new Set([id]); for (const n of nodes.values()) if (descend.has(n.parentId)) descend.add(n.id);
      for (const nid of descend) {const n = get(nid); if (!terminal.has(n.status)) {n.status = 'CANCELLED'; await record('conversation.cancelled', n);}}
      return view(target);
    }),
    rejoin: id => exclusive(async () => {
      await expire(); const parent = get(id);
      const children = parent.children.map(get); const results = children.map(child => ({id: child.id, intent: child.intent, status: child.status, result: clone(child.result),
        evidenceRef: events.findLast(e => e.conversationId === child.id && e.type === 'result.returned')?.id || null}));
      await record('results.rejoined', parent, {children: results.map(c => ({id: c.id, status: c.status, evidenceRef: c.evidenceRef}))});
      return {parentId: id, complete: children.length > 0 && children.every(c => c.status === 'RETURNED'), children: results};
    }),
    completeRoot: ({actor} = {}) => exclusive(async () => {
      if (actor !== principalId) throw new Error('Principal mismatch');
      const root = await live(rootId); const children = root.children.map(get);
      if (!children.length || [...nodes.values()].some(child => child.parentId && child.status !== 'RETURNED')) throw new Error('All descendants must return first');
      root.result = children.map(child => ({id: child.id, result: clone(child.result)})); root.status = 'RETURNED';
      await record('intent.completed', root, {childIds: root.children}); return view(root);
    }),
    inspect: id => exclusive(async () => {await expire(); return view(get(id));}),
    exportEvidence: () => exclusive(async () => {await expire(); return snapshot();})
  });
}

