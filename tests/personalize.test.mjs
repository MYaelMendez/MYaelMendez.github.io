import test from 'node:test';
import assert from 'node:assert/strict';
import {normalizeProfile,loadProfile,profileExport,PROFILE_KEY} from '../work/personalize.mjs';
test('personalization accepts bounded labels and normalizes a domain without granting ownership',()=>{
 const p=normalizeProfile({name:' My studio ',purpose:' Build useful tools ',domain:'Example.COM'});
 assert.deepEqual(p,{name:'My studio',purpose:'Build useful tools',domain:'example.com'});
 const out=profileExport(p);assert.equal(out.identityAuthenticated,false);assert.equal(out.domainVerified,false);assert.deepEqual(out.authority.grants,[]);assert.deepEqual(out.runtimeConnections,[]);
});
test('rejects missing, oversized or control-bearing identity fields and executable domains',()=>{
 for(const p of [null,[],{name:'',purpose:'x'},{name:'x'.repeat(81),purpose:'x'},{name:'x',purpose:'y'.repeat(281)},{name:'x\n',purpose:'y'},{name:'x',purpose:'y',domain:'https://example.com'},{name:'x',purpose:'y',domain:'javascript:alert(1)'},{name:'x',purpose:'y',domain:'a.com?token=x'}])assert.throws(()=>normalizeProfile(p));
});
test('stored profile corruption or inaccessible storage does not prevent startup',()=>{
 assert.equal(loadProfile({getItem(){throw Error('blocked');}}),null);assert.equal(loadProfile({getItem(){return '{bad';}}),null);
 const p={name:'Studio',purpose:'My purpose',domain:''};assert.deepEqual(loadProfile({getItem(k){assert.equal(k,PROFILE_KEY);return JSON.stringify(p);}}),p);
});
