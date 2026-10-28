import test from 'node:test';
import assert from 'node:assert/strict';
import {HARNESSES,filterHarnesses,makeHarnessPlan} from '../work/harnesses.mjs';
test('license groups keep Codex open and do not mistake Copilot SDK for CLI',()=>{
 assert.deepEqual(filterHarnesses('MIT').map(h=>h.id),['openclaw','hermes','deepseek-harness']);
 assert.deepEqual(filterHarnesses('Apache-2.0').map(h=>h.id),['codex-cli']);
 assert.equal(filterHarnesses('open').length,4);
 assert.deepEqual(filterHarnesses('proprietary').map(h=>h.id),['copilot-cli','claude-code']);
 assert.equal(filterHarnesses('all').length,6);
 assert.throws(()=>filterHarnesses('free'),/Unknown/);
});
test('a proposed choice creates no provider connection or permission',()=>{
 const p=makeHarnessPlan('codex-cli','open');
 assert.equal(p.status,'proposed');assert.equal(p.model,null);assert.equal(p.service,null);
 assert.equal(p.connection,'not_connected_by_selection');assert.deepEqual(p.authority.grants,[]);
 assert.equal(p.authority.inherits,false);
 assert.throws(()=>makeHarnessPlan('claude-code','MIT'),/not in/);
 assert.throws(()=>makeHarnessPlan('unknown','all'),/not in/);
});
test('every harness has direct primary license evidence and separate model/service context',()=>{
 for(const h of HARNESSES){const u=new URL(h.source);assert.equal(u.hostname,'github.com');assert.equal(u.protocol,'https:');assert.ok(h.model&&h.service&&h.status);assert.ok(Object.isFrozen(h));}
});
