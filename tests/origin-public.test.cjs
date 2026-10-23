'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const A=require('../ae-origin.js');
const fixture=JSON.parse(fs.readFileSync(path.join(__dirname,'fixtures/destinations.json'),'utf8'));
function copy(){return structuredClone(fixture);}
for(const alias of A.aliases){test('alias '+alias+' opens origin without a grant',()=>{assert.deepEqual(A.resolve(alias),{kind:'origin',address:A.origin,authorization:null});});}
test('canonical user coordinates and tolerant z syntax remain distinct',()=>{
 assert.equal(A.origin,'x0:y0:z0:\u00e6:\u00e6');assert.equal(A.publicAddress,'x0:y0:z:0:\u00e6:\u00e6:\u00e6');
 assert.equal(A.resolve(A.origin).kind,'origin');assert.equal(A.resolve(A.publicAddress).kind,'public_review');
 assert.equal(A.resolve(A.publicAddress.replace(':z:0:',':z0:')).kind,'public_review');
});
test('heart is human intention, not health-agency routing',()=>{for(const s of ['$\u2764\ufe0f','@\u2764','$@\u2764\ufe0f'])assert.equal(A.resolve(s).kind,'intention');});
test('MCP is a case-insensitive local alias; unrelated protocol commands are not guessed',()=>{assert.equal(A.resolve('$MCP').kind,'origin');assert.equal(A.resolve('mcp://execute'),null);});
test('atlas and service aliases only propose source inspection/navigation',()=>{assert.equal(A.resolve('$\ud83d\uddfa\ufe0f').kind,'atlas');assert.equal(A.resolve('$doola').kind,'route_proposal');assert.equal(A.resolve('$startabusiness').authorization,null);assert.equal(A.resolve('@\ud83e\udd16').route,'agents');});
test('reject invisible controls, nonstrings and oversized commands',()=>{for(const x of [null,{},'$mcp\u0000','\u202e$mcp','a'.repeat(257)])assert.equal(A.resolve(x),null);});
test('numeric coordinates are bounded and never create permission',()=>{assert.deepEqual(A.parseCoordinate('x9:y-1:z0:ae3'),{x:9,y:-1,z:0,a:3});for(const s of ['x9999:y0:z0:ae0','x0:y0:z0:ae4','x0:y0:z0:ae-1','garbage x0:y0:z0:ae0'])assert.equal(A.parseCoordinate(s),null);});
test('URLs reject executable schemes, userinfo, spoofing and remote HTTP',()=>{for(const u of ['javascript:alert(1)','data:text/html,x','//evil.example/','https://u:p@example.com/','http://example.com/','https://example.com/\n','/\\evil.example/'])assert.equal(A.safeURL(u,'https://example.org/'),null);assert.equal(A.safeURL('./ae/','https://example.org/'),'https://example.org/ae/');assert.equal(A.safeURL('/ae/','http://127.0.0.1:4173/'),'http://127.0.0.1:4173/ae/');});
test('valid two-destination contract preserves chat and original Site',()=>{const d=A.inspectDestinations(copy());assert.equal(d.site_url,A.siteURL);assert.equal(d.chat_redirect,false);assert.equal(d.session_sync,'not_verified');assert.equal(d.authorization,null);});
test('fail closed on transferred authority, duplicate peers, changed Site or context sharing',()=>{
 const mutations=[c=>c.authority.inherit=true,c=>c.authority.principal='agent',c=>c.destinations[0].auto_redirect=true,c=>c.destinations[0].entry_url='https://example.com',c=>c.destinations[1].entry_url='https://evil.example',c=>c.handoff.copy_private_context=true,c=>c.handoff.transfer_credentials_or_grants=true,c=>c.destinations.push(c.destinations[1]),c=>c.destinations[0]=c.destinations[1]];
 for(const mutate of mutations){const c=copy();mutate(c);assert.throws(()=>A.inspectDestinations(c));}
});
test('public projection drops all additional private fields and claims',()=>{const c=copy();c.intent='PRIVATE-CANARY';c.token='SECRET-CANARY';c.grant={admin:true};const d=A.inspectDestinations(c);const p=A.publicDraft('My agency',d,'codex');const out=JSON.stringify(p);assert.ok(!out.includes('CANARY'));assert.equal(p.execution.dispatch,false);assert.equal(p.publication.deployment_authorized,false);assert.equal(p.authority.grant,null);assert.equal(p.witness.external_success,false);});
test('executor preference changes neither authority nor provider state',()=>{const d=A.inspectDestinations(copy()),a=A.publicDraft('test',d,'ae'),c=A.publicDraft('test',d,'codex');assert.deepEqual(a.authority,c.authority);assert.equal(c.execution.connection,'not_verified');assert.throws(()=>A.publicDraft('test',d,'unverified-runtime'));});
test('export label and contract are validated; no implied certification',()=>{const d=A.inspectDestinations(copy());for(const s of ['',null,'x'.repeat(81),'\u202ebad'])assert.throws(()=>A.publicDraft(s,d,'ae'));assert.throws(()=>A.publicDraft('test',null,'ae'));assert.equal(A.chainReport().checks_performed,0);assert.equal(A.chainReport().status,'not_verified');});
test('reproduce the observed origin helper initialization error',()=>{
 const original="var _tt=$('theme-toggle'); var $=function(id){return document.getElementById(id)};";
 assert.throws(()=>vm.runInNewContext(original,{document:{getElementById:()=>null}}),/is not a function/);
});
const web=fs.readFileSync(path.join(__dirname,'../webmcp.js'),'utf8');
function webContext(rejectAll=false){const accepted=[],ctx={window:{addEventListener(){}},document:{modelContext:{registerTool(t){if(rejectAll||t.name==='find_capability')throw Error('host rejected');accepted.push(t);}}},navigator:{},AbortController,setTimeout,clearTimeout,URL,location:{href:'https://example.org/',assign(){throw Error('unexpected navigation');}},fetch:async()=>({ok:true,text:async()=>fs.readFileSync(path.join(__dirname,'fixtures/manifest.json'),'utf8')})};vm.runInNewContext(web,ctx);return {ctx,accepted};}
test('WebMCP registration counts only host-accepted tools',()=>{const {ctx,accepted}=webContext();assert.equal(accepted.length,5);assert.equal(ctx.window.__aeWebmcp.tools.length,5);assert.equal(ctx.window.__aeWebmcp.complete,false);assert.equal(ctx.window.__aeWebmcp.errors.length,1);});
test('complete registration failure remains not registered',()=>{const {ctx}=webContext(true);assert.equal(ctx.window.__aeWebmcp.registered,false);assert.equal(ctx.window.__aeWebmcp.tools.length,0);});
test('WebMCP absent does not fabricate availability',()=>{const ctx={window:{},document:{},navigator:{}};vm.runInNewContext(web,ctx);assert.equal(ctx.window.__aeWebmcp.available,false);});
test('WebMCP open_surface never navigates and verify_chain never fabricates success',async()=>{const {accepted}=webContext();const res=await accepted.find(t=>t.name==='open_surface').execute({id:'aeqr'});const o=JSON.parse(res.content[0].text);assert.equal(o.navigation,'not_performed');assert.equal(o.authority,null);const chain=await accepted.find(t=>t.name==='verify_chain').execute();assert.equal(JSON.parse(chain.content[0].text).status,'not_verified');});
test('WebMCP invalid manifest fails closed',async()=>{const {ctx,accepted}=webContext();ctx.fetch=async()=>({ok:true,text:async()=>' {"capabilities":[{"id":"broken"}]}' });const res=await accepted.find(t=>t.name==='get_manifest').execute();assert.equal(res.isError,true);assert.equal(JSON.parse(res.content[0].text).status,'unavailable');});
