import test from 'node:test';
import assert from 'node:assert/strict';
import {nextStep,starters} from '../work/guidance.mjs';
import {createWorkspace} from '../work/session.mjs';
test('guidance begins with editable material and advances only with actual work',async()=>{
 const w=createWorkspace();assert.equal(nextStep(await w.snapshot()).target,'intent');
 await w.begin(starters.enterprise.intent,starters.enterprise.brief);assert.equal(nextStep(await w.snapshot()).target,'share');
 await w.prepare('build',{share:true});assert.equal(nextStep(await w.snapshot()).target,'payload');
 await w.approve('build');assert.equal(nextStep(await w.snapshot()).target,'run');
 await w.run('build');assert.equal(nextStep(await w.snapshot()).lane,'inspect');
 await w.prepare('inspect',{share:true});await w.approve('inspect');await w.run('inspect');
 assert.equal(nextStep(await w.snapshot()).target,'notes');
 await w.prepare('review',{share:true,notes:'I reviewed the returned work.'});await w.approve('review');await w.run('review');
 assert.equal(nextStep(await w.snapshot()).target,'complete');await w.complete();assert.equal(nextStep(await w.snapshot()).target,'export');
});
test('expired approval is never presented as ready to run',async()=>{
 let clock=Date.now();const w=createWorkspace({now:()=>clock});await w.begin('Test','Text');await w.prepare('build',{share:true});await w.approve('build');clock+=61000;
 assert.equal(nextStep(await w.snapshot(),clock).target,'payload');
});
