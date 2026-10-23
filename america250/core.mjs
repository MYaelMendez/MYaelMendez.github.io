export function scenario({target, activation, retention, sales, margin, operating, compute}) {
  const values = [target, activation, retention, sales, margin, operating, compute];
  if (values.some(v => !Number.isFinite(v) || v < 0 || v > 1e12) || [activation, retention, margin].some(v => v > 1)) throw Error('Use finite, nonnegative assumptions; rates must be between 0 and 1.');
  const owners = target * activation * retention;
  const revenue = owners * sales;
  const grossProfit = revenue * margin;
  return {owners, revenue, grossProfit, surplus: grossProfit - owners * (operating + compute)};
}
export function task(intent, role, context) {
  if (!['build','research','review'].includes(role) || typeof intent !== 'string' || !intent.trim() || intent.length > 4000 || typeof context !== 'string' || !context.trim() || context.length > 16000) throw Error('Provide an intent and selected context within the limits.');
  return {schema:'ae.america250.task.v1',intent,role,selected_context:context};
}
export function validateReceipt(r) {
  if (!r || r.schema !== 'ae.america250.contribution.v1' || r.status !== 'pending_human_review' || !Array.isArray(r.grants) || r.grants.length || !['build','research','review'].includes(r.role)) throw Error('Unsupported receipt or authority fields.');
  const c = r.contribution;
  if (!c || typeof c.summary !== 'string' || !c.summary.trim() || c.summary.length > 2000 || typeof c.artifact !== 'string' || !c.artifact.trim() || c.artifact.length > 24000 || !Array.isArray(c.evidence) || c.evidence.length > 12) throw Error('Invalid contribution.');
  if (typeof r.intent !== 'string' || r.intent.length > 4000 || !/^[a-f0-9]{64}$/.test(r.task_hash)) throw Error('Invalid task reference.');
  for (const e of c.evidence) {
    const u = new URL(e.url);
    if (u.protocol !== 'https:' || u.username || u.password || typeof e.note !== 'string' || e.note.length > 2000 || e.verification !== 'reported_unverified') throw Error('Invalid evidence reference.');
  }
  // Select fields explicitly. Imported status, identities and evidence are untrusted.
  return {role:r.role,intent:r.intent,summary:c.summary,artifact:c.artifact,evidence:c.evidence.map(e=>({url:e.url,note:e.note})),taskHash:r.task_hash,review:'pending',reason:''};
}
