import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {Script} from 'node:vm';
const legacy=await readFile(new URL('../origin/index.html',import.meta.url),'utf8');
const home=await readFile(new URL('../index.html',import.meta.url),'utf8');
test('preserved terminal retains its atlas, controls and original destinations',()=>{for(const needle of ['base href="../"','id="mesh"','id="cmd"','id="theme-toggle"','id="env-toggle"','ae-atlas.js','webmcp.js','./mcp/agents/','./mcp/kinetic/'])assert.ok(legacy.includes(needle),needle);});
test('legacy helper is initialized before its first call and script parses',()=>{const script=[...legacy.matchAll(/<script(?: [^>]*)?>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(x=>x.includes('function resolve(q)'));new Script(script);assert.ok(script.indexOf('function $(id)')<script.indexOf("$('theme-toggle')"));});
test('homepage is the working glass surface with optional original Site and origin links',()=>{for(const needle of ['base href="./work/"','id="intent-form"','data-lane="build"','data-lane="inspect"','data-lane="review"','id="contributions"','../origin/','https://yael-mendez.teologia-7508.chatgpt.site/','No AI model or external runtime connected'])assert.ok(home.includes(needle),needle);assert.ok(!home.includes('http-equiv="refresh"'));});
