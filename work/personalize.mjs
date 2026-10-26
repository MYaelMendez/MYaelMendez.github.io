export const PROFILE_KEY='ae-work-identity-v1';
const clean=(value,max)=>{
 if(typeof value!=='string'||value.trim().length>max||/[\u0000-\u001f\u007f]/u.test(value))throw Error('Use readable text within the field limits.');
 return value.trim();
};
export function normalizeProfile(raw){
 if(!raw||typeof raw!=='object'||Array.isArray(raw))throw Error('Invalid profile.');
 const name=clean(raw.name,80),purpose=clean(raw.purpose,280),domain=clean(raw.domain??'',253);
 if(!name||!purpose)throw Error('Add your workspace name and purpose.');
 let asciiDomain='';
 if(domain){try{if(/[\s/:?#@\\]/u.test(domain))throw Error();asciiDomain=new URL('https://'+domain).hostname;}catch{throw Error('Enter a domain name only, such as example.com.');}}
 if(domain&&!/^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$/i.test(asciiDomain))throw Error('Enter a domain name only, such as example.com. This is a label, not a domain connection.');
 return {name,purpose,domain:domain.toLowerCase()};
}
export function loadProfile(storage){try{const raw=storage?.getItem(PROFILE_KEY);return raw?normalizeProfile(JSON.parse(raw)):null;}catch{return null;}}
export function profileExport(profile){return {schema:'ae.workspace.personalization.v1',profile:normalizeProfile(profile),scope:'appearance_and_purpose_only',identityAuthenticated:false,domainVerified:false,authority:{principal:'human',inherits:false,grants:[]},runtimeConnections:[]};}
export function mountPersonalization(doc=document,storage){
 if(storage===undefined)try{storage=globalThis.localStorage;}catch{}
 const $=id=>doc.getElementById(id);let profile=loadProfile(storage);
 const paint=()=>{
  $('profile-output').textContent='';$('profile-export-view').hidden=true;
  $('brand-name').textContent=profile?.name||'æ Studio';
  $('brand-purpose').textContent=profile?.purpose||'Your identity. Your tools. Your environment.';
  $('brand-domain').textContent=profile?.domain||'';$('brand-domain').hidden=!profile?.domain;
  $('personalize-open').textContent=profile?'Personalize my enterprise →':'Make it mine →';
  doc.title='Work here 💬 · '+(profile?.name||'æ Studio');
  $('personalize-export').disabled=!profile;$('personalize-reset').disabled=!profile;
 };
 const populate=()=>{for(const field of ['name','purpose','domain'])$('profile-'+field).value=profile?.[field]||'';};
 $('personalize-open').onclick=()=>{const panel=$('personalize-panel');panel.hidden=!panel.hidden;$('personalize-open').setAttribute('aria-expanded',String(!panel.hidden));if(!panel.hidden){populate();$('profile-name').focus();}};
 $('personalize-form').onsubmit=e=>{e.preventDefault();try{
  profile=normalizeProfile(Object.fromEntries(['name','purpose','domain'].map(k=>[k,$('profile-'+k).value])));
  let saved=false;try{if(storage){storage.setItem(PROFILE_KEY,JSON.stringify(profile));saved=true;}}catch{}
  paint();$('personalize-status').textContent=saved?'Made yours in this browser. Your work and provider permissions are unchanged.':'Applied for this page only. Browser storage is unavailable; export your profile to keep it.';
 }catch(error){$('personalize-status').textContent=error.message;}};
 $('personalize-reset').onclick=()=>{profile=null;try{storage?.removeItem(PROFILE_KEY);}catch{}populate();paint();$('personalize-status').textContent='Local personalization removed. Your current workspace remains open.';};
 $('personalize-export').onclick=()=>{if(!profile)return;const text=JSON.stringify(profileExport(profile),null,2);$('profile-output').textContent=text;$('profile-export-view').hidden=false;$('personalize-status').textContent='Profile ready below. It contains your entered labels, no credentials or execution grants.';};
 paint();
}
