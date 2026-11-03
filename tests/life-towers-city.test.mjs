import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Script} from 'node:vm';
const towers=readFileSync('ae/control/towers/index.html','utf8');
const city=readFileSync('ae/control/city/index.html','utf8');
function script(html){const m=html.match(/<script type="module">([\s\S]*?)<\/script>/);assert.ok(m,'module script exists');return m[1]}
test('both laboratory pages parse as JavaScript',()=>{new Script(script(towers));new Script(script(city))});
test('life towers preserve twelve destinations and five workspaces',()=>{for(const name of ['HOME','HEALTH','LEARN','FAITH','BUILD','BU$INE$$','ECONOMY','IMPACT','MOVE','CONSTRUCT','WITNESS','GOVERN'])assert.ok(towers.includes(name),name);for(const name of ['Principal','Environments','Agents','Orchestrate','Witness'])assert.ok(towers.includes(name),name)});
test('read-only pilot has no privileged command dispatch',()=>{assert.ok(towers.includes('api.github.com/repos/'));assert.ok(!towers.includes('Authorization:'));assert.ok(!towers.includes('DELETE'));assert.ok(towers.includes('external_write:false'))});
test('city has deterministic 364-cell genome and fallback',()=>{assert.ok(city.includes('Uint8Array(364)'));assert.ok(city.includes('Float32Array(364*5)'));assert.ok(city.includes("function fallback(reason)"));assert.ok(city.includes("ctx2=canvas.getContext('2d')"));assert.ok(!city.includes('Math.random()'))});
