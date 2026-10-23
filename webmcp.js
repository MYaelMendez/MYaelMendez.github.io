/* Optional read-only WebMCP adapter. Draft API reference checked 2026-10-19:
 * https://webmachinelearning.github.io/webmcp/ (2026-10-16 report).
 * Native document.modelContext first; legacy navigator fallback, registerTool only.
 * No server, plugin installation, authentication, execution or navigation implied.
 */
(function(){'use strict';
var MC=null,locationName='none';
try{if(document.modelContext&&typeof document.modelContext.registerTool==='function'){MC=document.modelContext;locationName='document';}else if(navigator.modelContext&&typeof navigator.modelContext.registerTool==='function'){MC=navigator.modelContext;locationName='navigator-compatibility';}}catch(_){}
var status={available:!!MC,shape:MC?'registerTool':'none',location:locationName,registered:false,complete:false,tools:[],errors:[]};window.__aeWebmcp=status;if(!MC)return;
var cache=null,inflight=null;
function safeURL(value){if(window.AEOrigin)return window.AEOrigin.safeURL(value,location.href);try{if(typeof value!=='string'||value.length>1024||/[\u0000-\u0020\u007f\\]/.test(value)||/^\/\//.test(value))return null;var u=new URL(value,location.href);return u.protocol==='https:'&&!u.username&&!u.password?u.href:null;}catch(_){return null;}}
function text(value,isError){return {isError:!!isError,content:[{type:'text',text:typeof value==='string'?value:JSON.stringify(value)}]};}
function ensure(){
 if(cache)return Promise.resolve(cache);if(inflight)return inflight;
 var abort=new AbortController(),timer=setTimeout(function(){abort.abort();},10000);
 inflight=fetch('./capability-manifest.json',{cache:'no-cache',credentials:'omit',referrerPolicy:'no-referrer',signal:abort.signal}).then(function(r){if(!r.ok)throw Error('Manifest request failed');return r.text();}).then(function(raw){
 if(raw.length>200000)throw Error('Manifest too large');var m=JSON.parse(raw);if(!m||!Array.isArray(m.capabilities)||m.capabilities.length>2000)throw Error('Unsupported manifest');var ids=new Set();
 var caps=m.capabilities.map(function(c){if(!c||['id','name','address','url','category'].some(function(k){return typeof c[k]!=='string'||c[k].length>1024;})||ids.has(c.id)||!safeURL(c.url)||!Number.isInteger(c.layer)||c.layer<0||c.layer>3)throw Error('Invalid capability record');ids.add(c.id);return {id:c.id,name:c.name,address:c.address,url:c.url,category:c.category,layer:c.layer,layer_name:typeof c.layer_name==='string'?c.layer_name:'',capabilities:Array.isArray(c.capabilities)?c.capabilities.filter(function(v){return typeof v==='string'&&v.length<256;}).slice(0,30):[],status:'source_description',authority:null};});
 cache={capabilities:caps,count:caps.length,verification:'source_only',authority:null};return cache;
 }).finally(function(){clearTimeout(timer);inflight=null;});return inflight;
}
function call(fn){return function(args){return ensure().then(function(m){return text(fn(args||{},m));}).catch(function(){return text({status:'unavailable',reason:'Manifest missing, invalid, or request failed. No result was verified.'},true);});};}
function query(value){if(typeof value!=='string'||!value.trim()||value.length>256)throw Error('Invalid query');return value.trim().toLowerCase();}
function find(q,m){return m.capabilities.find(function(c){return c.id.toLowerCase()===q||c.name.toLowerCase()===q||c.address.toLowerCase()===q;})||null;}
var tools=[
 {name:'list_capabilities',description:'Read public capability descriptions. Layers are navigation labels, not authority or verified execution.',inputSchema:{type:'object',properties:{layer:{type:'integer',minimum:0,maximum:3},category:{type:'string',maxLength:256}},additionalProperties:false},execute:call(function(a,m){return m.capabilities.filter(function(c){return (a.layer==null||c.layer===a.layer)&&(!a.category||c.category===a.category);});})},
 {name:'find_capability',description:'Search public source descriptions; no installation or invocation occurs.',inputSchema:{type:'object',properties:{query:{type:'string',minLength:1,maxLength:256}},required:['query'],additionalProperties:false},execute:call(function(a,m){var q=query(a.query);return m.capabilities.filter(function(c){return [c.id,c.name,c.category,c.url].concat(c.capabilities).join(' ').toLowerCase().includes(q);});})},
 {name:'open_surface',description:'Return a proposed surface URL for human selection. This tool does not navigate, authenticate, or execute.',inputSchema:{type:'object',properties:{id:{type:'string',minLength:1,maxLength:256}},required:['id'],additionalProperties:false},execute:call(function(a,m){var r=find(query(a.id),m);return r?{surface:r,navigation:'not_performed',authority:null}:{status:'not_found',authority:null};})},
 {name:'resolve_address',description:'Resolve a numeric x:y:z:ae navigation coordinate to a public source record. No permission is granted.',inputSchema:{type:'object',properties:{address:{type:'string',maxLength:128}},required:['address'],additionalProperties:false},execute:call(function(a,m){var q=query(a.address);if(!/^x-?\d{1,3}:y-?\d{1,3}:z-?\d{1,3}:(?:\u00e6|ae)[0-3]$/.test(q))return {status:'invalid_address'};q=q.replace(/:ae([0-3])$/,':\u00e6$1');return find(q,m)||{status:'not_found'};})},
 {name:'get_manifest',description:'Return the validated public capability projection, not private context or grants.',inputSchema:{type:'object',properties:{},additionalProperties:false},execute:call(function(a,m){return m;})},
 {name:'verify_chain',description:'Report the chain definition and that no external verification is implemented here. Does not claim a successful chain.',inputSchema:{type:'object',properties:{},additionalProperties:false},execute:function(){return Promise.resolve(text({chain:'vaeult',links:['custody','format','gate','authority','contract','dispatch','publish','delivery','adoption'],status:'not_verified',checks_performed:0,external_success:false,authority:null}));}}
];
var lifetime=new AbortController();window.addEventListener('pagehide',function(){lifetime.abort();},{once:true});
tools.forEach(function(t){t.annotations={readOnlyHint:true,untrustedContentHint:true,consequentialHint:false};try{MC.registerTool(t,{signal:lifetime.signal});status.tools.push(t.name);}catch(_){status.errors.push({tool:t.name,status:'registration_rejected'});}});
status.registered=status.tools.length>0;status.complete=status.tools.length===tools.length;
})();
