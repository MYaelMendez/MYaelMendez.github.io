// Run with: NODE_PATH=/path/to/jsdom/node_modules node tests/teotech-journal.cjs
const {JSDOM}=require('jsdom');
const fs=require('node:fs');
const assert=require('node:assert/strict');
const path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'../teologia/aprender.html'),'utf8');
const key='teologia-aeqr-learning-v1';
const make=(saved,blocked=false)=>new JSDOM(html,{url:'https://myaelmendez.github.io/teologia/aprender.html',runScripts:'dangerously',beforeParse(w){if(saved)w.localStorage.setItem(key,saved);if(blocked)Object.defineProperty(w,'localStorage',{get(){throw new Error('storage unavailable')}})}});
const d=make();const w=d.window;
const input=(id,value)=>{const e=w.document.getElementById(id);e.value=value;e.dispatchEvent(new w.Event('input',{bubbles:true}))};
const click=id=>w.document.getElementById(id).click();
const records=()=>JSON.parse(w.localStorage.getItem(key));
(async()=>{
 click('complete');assert.match(w.document.getElementById('message').textContent,/Completa/);
 input('learned','QA learned');assert.equal(records().genesis.completed,false);
 await new Promise(r=>{w.addEventListener('hashchange',r,{once:true});w.location.hash='juan'});
 assert.equal(w.document.getElementById('learned').value,'');input('learned','QA Juan');
 await new Promise(r=>{w.addEventListener('hashchange',r,{once:true});w.location.hash='genesis'});
 assert.equal(w.document.getElementById('learned').value,'QA learned');
 input('built','QA practice');input('teach','QA teach');click('complete');assert.equal(records().genesis.completed,true);
 input('learned','QA revised');click('save');assert.equal(records().genesis.completed,true);assert.equal(w.document.activeElement.id,'save');
 let exported;w.Blob=class{constructor(parts){exported=JSON.parse(parts.join(''))}};w.URL.createObjectURL=()=> 'blob:qa';w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){};
 click('export');assert.equal(exported.schema,'teologia.learning.v1');assert.equal(exported.records.genesis.completed,true);assert.equal(exported.records.juan.learned,'QA Juan');
 const reload=make(w.localStorage.getItem(key));assert.equal(reload.window.document.getElementById('learned').value,'QA revised');reload.window.close();
 const blocked=make(null,true);const bw=blocked.window;const e=bw.document.getElementById('learned');e.value='offline note';e.dispatchEvent(new bw.Event('input',{bubbles:true}));assert.match(bw.document.getElementById('message').textContent,/en memoria/);blocked.window.close();w.close();
 console.log('PASS: required fields; input persistence; lesson isolation; completion preservation; focus; JSON contents; reload; unavailable storage');
})().catch(e=>{console.error(e);process.exitCode=1});
const portal=new JSDOM(fs.readFileSync(path.join(__dirname,'../teotech.html'),'utf8'),{runScripts:'dangerously'});
for(const button of portal.window.document.querySelectorAll('[data-qr]')){
 const panel=portal.window.document.getElementById(button.getAttribute('aria-controls'));
 assert.equal(panel.hidden,true);button.click();assert.equal(panel.hidden,false);assert.equal(button.getAttribute('aria-expanded'),'true');button.click();assert.equal(panel.hidden,true);
}
assert.equal(portal.window.document.querySelectorAll('svg').length,6);
const ids=[...portal.window.document.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(ids).size,ids.length);portal.window.close();
const hub=new JSDOM(fs.readFileSync(path.join(__dirname,'../teologia/index.html'),'utf8'));
assert(hub.window.document.querySelector('a[href="../teotech.html"]'));
assert(hub.window.document.querySelector('a[href="aprender.html"]'));
assert.equal(hub.window.document.querySelectorAll('.card[data-href]').length,6);hub.window.close();
console.log('PASS: six QR toggles; unique portal IDs; hub links restored; six current artifacts preserved');
