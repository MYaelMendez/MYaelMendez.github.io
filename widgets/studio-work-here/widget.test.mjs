import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import vm from 'node:vm';
const html=readFileSync(new URL('./widget.html',import.meta.url),'utf8');
const manifest=JSON.parse(readFileSync(new URL('./manifest.json',import.meta.url),'utf8'));
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
// Minimal control fixture, not a browser, layout engine, or accessibility audit.
function fixture(){
 const nodes=[];
 for(const m of html.matchAll(/<([a-z][a-z0-9]*)\b([^>]*)>/g)){
  const attrs={};for(const x of m[2].matchAll(/([\w-]+)="([^"]*)"/g))attrs[x[1]]=x[2];
  const node={attrs,dataset:{},checked:false,disabled:/\bdisabled\b/.test(m[2]),value:'',textContent:'',setAttribute(k,v){this.attrs[k]=v;}};
  for(const[k,v]of Object.entries(attrs))if(k.startsWith('data-'))node.dataset[k.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=v;
  if(m[1]==='textarea')node.value=html.slice(m.index+m[0].length).split('</textarea>')[0];
  nodes.push(node);
 }
 const find=s=>nodes.filter(n=>s[0]==='#'?n.attrs.id===s.slice(1):s[0]==='.'?(n.attrs.class||'').split(' ').includes(s.slice(1)):Object.hasOwn(n.attrs,s.slice(1,-1)));
 const root={querySelector:s=>find(s)[0],querySelectorAll:find};
 vm.runInNewContext(script,{document:{getElementById:()=>root},Date});
 const q=id=>root.querySelector('#ae-h-'+id);
 const lane=id=>find('[data-lane]').find(n=>n.dataset.lane===id).onclick();
 const run=()=>{q('approval').checked=true;q('approval').onchange();q('run').onclick();};
 return {q,find,lane,run};
}
test('saved source matches the displayed chat fragment and standalone build',()=>{
 assert.equal(createHash('sha256').update(html).digest('hex'),manifest.source.sha256);
 assert(readFileSync(new URL('./index.html',import.meta.url),'utf8').includes(html));
 new vm.Script(script);
});
test('approval and dependency gates prevent premature contributions',()=>{
 const {q,lane,run}=fixture();assert(q('run').disabled);q('run').onclick();assert.equal(q('count').textContent,'0 / 3 returned');
 lane('inspect');run();assert(q('run').disabled);lane('review');run();assert(q('run').disabled);
});
test('build, inspect and human review return actual local output and events',()=>{
 const {q,lane,run}=fixture();q('intent').value='One useful enterprise';q('intent').oninput();run();
 assert.match(q('output').textContent,/One useful enterprise/);assert(!q('approval').checked);
 lane('inspect');run();assert.match(q('output').textContent,/words/);assert.match(q('output').textContent,/characters/);
 lane('review');q('notes').value='Review the resulting brief.';q('notes').oninput();run();
 assert.equal(q('count').textContent,'3 / 3 returned');assert.match(q('output').textContent,/Review the resulting brief/);
 assert.match(q('evidence').textContent,/review.returned/);
});
test('editing intent invalidates every returned contribution and approval',()=>{
 const {q,lane,run}=fixture();run();lane('inspect');run();q('intent').value='Different intent';q('intent').oninput();
 assert.equal(q('count').textContent,'0 / 3 returned');assert(q('run').disabled);assert(!q('approval').checked);
 assert.match(q('status').textContent,/cleared/);
});
test('nested navigation and theme changes preserve input; output remains text',()=>{
 const {q,find,run}=fixture();const text='<img src=x onerror=alert(1)>';q('intent').value=text;q('intent').oninput();
 for(const id of ['store','connections','work'])find('[data-page]').find(n=>n.dataset.page===id).onclick();
 q('theme').onchange({target:{value:'white'}});assert.equal(q('intent').value,text);run();assert(q('output').textContent.includes(text));
 assert(!/\.innerHTML\s*=/.test(script));
});
test('empty intent is rejected and this fragment contains no API transport',()=>{
 const {q,run}=fixture();q('intent').value='   ';q('intent').oninput();run();assert(q('run').disabled);
 assert(!/\b(fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(/.test(script));
 assert.match(html,/not a live embed/);assert.match(html,/does not synchronize/);
});
