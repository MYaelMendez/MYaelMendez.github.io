/* Open Sovereign origin contract. Navigation is not authorization. */
(function(root,factory){'use strict';var api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.AEOrigin=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
var VERSION='0.2.0',BASE='151c6b3a4dd85fadace959cb85bd3028e28c765e';
var ORIGIN='x0:y0:z0:\u00e6:\u00e6',PUBLIC='x0:y0:z:0:\u00e6:\u00e6:\u00e6';
var SITE='https://yael-mendez.teologia-7508.chatgpt.site/';
var aliases=Object.freeze(['\u00e6','$\u00e6','$ae','$mcp','&mcp','$mpc','&mpc','>_\u00e6\u00e6\u00e6://|||']);
var routes=Object.freeze([
 {id:'agents',symbol:'\ud83e\udd16',href:'./mcp/agents/',label:'Agentic Home'},
 {id:'keypad',symbol:'\u2328\ufe0f',href:'./mcp/',label:'Virtual Micro'},
 {id:'discover',symbol:'\ud83d\udd0d',href:'./mcp/discover/',label:'Capability discovery'},
 {id:'business',symbol:'\ud83c\udfed',href:'./cli/',label:'Business preparation'},
 {id:'doola',symbol:'\ud83e\udd1d',href:'./doola/',label:'doola handoff'}
].map(Object.freeze));
function normalize(value){
 if(typeof value!=='string'||value.length>256||/[\u0000-\u001f\u007f\u200b-\u200f\u202a-\u202e\u2060-\u206f]/.test(value))return null;
 return value.normalize('NFC').trim().toLowerCase().replace(/\ufe0f/g,'');
}
function resolve(value){
 var v=normalize(value);if(!v)return null;
 if(aliases.map(normalize).includes(v)||v==='origin'||v===ORIGIN||v===ORIGIN.replace(':z0:',':z:0:'))return {kind:'origin',address:ORIGIN,authorization:null};
 if(v===PUBLIC||v===PUBLIC.replace(':z:0:',':z0:')||v==='public'||v==='publish')return {kind:'public_review',address:PUBLIC,authorization:null};
 if(['$\u2764','@\u2764','$@\u2764'].includes(v))return {kind:'intention',address:ORIGIN,authorization:null};
 if(['$\ud83d\uddfa','@\ud83d\uddfa'].includes(v))return {kind:'atlas',authorization:null};
 if(['$\ud83e\udd16','@\ud83e\udd16'].includes(v))return {kind:'route_proposal',route:'agents',authorization:null};
 if(['$startabusiness','#startabusiness'].includes(v))return {kind:'route_proposal',route:'business',authorization:null};
 if(['$doola','/doola'].includes(v))return {kind:'route_proposal',route:'doola',authorization:null};
 return null;
}
function parseCoordinate(value){var v=normalize(value);if(!v)return null;var m=/^x(-?\d{1,3}):y(-?\d{1,3}):z(-?\d{1,3}):(?:\u00e6|ae)([0-3])$/.exec(v);return m?{x:Number(m[1]),y:Number(m[2]),z:Number(m[3]),a:Number(m[4])}:null;}
function safeURL(value,base){
 if(typeof value!=='string'||value.length>1024||/[\u0000-\u0020\u007f\\]/.test(value)||/^\/\//.test(value))return null;
 try{var b=new URL(base),u=new URL(value,b);if(u.username||u.password)return null;
 if(u.protocol!=='https:'&&!(u.protocol==='http:'&&u.origin===b.origin&&['localhost','127.0.0.1','[::1]'].includes(u.hostname)))return null;
 return u.href;}catch(_){return null;}
}
function inspectDestinations(c){
 if(!c||c.schema!=='ae.destination-contract.v1'||!Array.isArray(c.destinations)||c.destinations.length!==2)throw Error('Unsupported destination contract');
 var chat=c.destinations.find(function(d){return d&&d.id==='chat';}),site=c.destinations.find(function(d){return d&&d.id==='site';});
 if(!chat||!site||chat.auto_redirect!==false||chat.entry_url!==null||site.entry_url!==SITE||site.create_replacement!==false)throw Error('Peer destinations or pinned Site changed; review required');
 if(!c.authority||c.authority.inherit!==false||c.authority.this_file_is_an_authorization_grant!==false||c.authority.principal!=='human')throw Error('Authority must remain with the human');
 if(!c.handoff||c.handoff.copy_private_context!==false||c.handoff.transfer_credentials_or_grants!==false)throw Error('Private context and grants cannot travel');
 return Object.freeze({status:'source_contract_checked',chat_redirect:false,site_url:SITE,session_sync:'not_verified',authorization:null});
}
function publicDraft(label,destination,preference){
 if(typeof label!=='string'||!label.trim()||label.length>80||/[\u0000-\u001f\u007f\u202a-\u202e]/.test(label))throw Error('Use a public label of 1-80 characters');
 if(!destination||destination.status!=='source_contract_checked'||destination.site_url!==SITE)throw Error('Check the destination contract first');
 if(!['ae','codex'].includes(preference))throw Error('Unsupported executor preference');
 // An allowlisted projection, never a spread or serialization of private input.
 return {schema:'ae.public-environment-draft.v1',version:VERSION,name:label.trim(),origin:ORIGIN,public_address:PUBLIC,
 source:{repository:'MYaelMendez/MYaelMendez.github.io',inspected_base_revision:BASE},
 destinations:[{id:'chat',entry_url:null,auto_redirect:false},{id:'site',entry_url:SITE,session_sync:'not_verified'}],
 routes:routes.map(function(r){return {id:r.id,href:r.href,status:'source_reference_not_live_verification'};}),
 execution:{preference:preference,connection:'not_verified',dispatch:false},authority:{principal:'human',inherit:false,grant:null},
 publication:{status:'draft',deployment_authorized:false},witness:{kind:'local_preparation',external_success:false,cryptographic_attestation:false},purpose:'Return value to the human.'};
}
function chainReport(){return {chain:'vaeult',links:['custody','format','gate','authority','contract','dispatch','publish','delivery','adoption'],status:'not_verified',checks_performed:0,external_success:false,authorization:null};}
return Object.freeze({version:VERSION,baseRevision:BASE,origin:ORIGIN,publicAddress:PUBLIC,siteURL:SITE,aliases:aliases,routes:routes,normalize:normalize,resolve:resolve,parseCoordinate:parseCoordinate,safeURL:safeURL,inspectDestinations:inspectDestinations,publicDraft:publicDraft,chainReport:chainReport});
});
