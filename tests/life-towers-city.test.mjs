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

test('WebGPU creates an initial depth attachment before drawing',()=>{assert.ok(city.includes("depth=device.createTexture({size:[canvas.width,canvas.height]"));assert.ok(city.indexOf("depth=device.createTexture({size:[canvas.width,canvas.height]")<city.indexOf('requestAnimationFrame(frame)'))});

test('existing Control links to tower workspace and isolated city laboratory',()=>{const control=readFileSync('ae/control/index.html','utf8');assert.ok(control.includes('href="towers/?tower=6"'));assert.ok(control.includes('href="city/"'));assert.ok(control.includes("entry.href='towers/?tower='"));assert.ok(control.includes("name==='BUSINESS'?'BU$INE$$':name"))});
