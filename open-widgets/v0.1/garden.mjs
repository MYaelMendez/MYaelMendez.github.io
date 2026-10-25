import {createGarden, locate, addChild, forkWidget, retireWidget, restoreWidget, publicProjection, KINDS, ORIGIN, MAX_DEPTH} from './model.mjs';
const garden=createGarden();
const $=id=>document.getElementById(id);
const make=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;};
const glyphs={note:'\u270e',counter:'\u2317',checklist:'\u2611',mixture:'\ud83e\udde9'};
const button=(text,fn,key)=>{const e=make('button','',text);e.type='button';e.onclick=fn;if(key)e.dataset.focus=key;return e;};
const hosts=[];let focusId=null,returnFocus=null,reviewSnapshot=null,session=null,busy=false;
function feedback(text){$('feedback').textContent=text;}
function invalidateExport(){reviewSnapshot=null;$('export-consent').checked=false;$('download').disabled=true;}
function mutate(fn){try{fn();invalidateExport();refresh();feedback('Local composition updated. No external action.');}catch(e){feedback(e.message);}}
function widgetView(w,depth=0){
  const box=make('article','widget');box.dataset.widgetId=w.id;
  const heading=make('div','widget-title');heading.append(make('strong','',glyphs[w.kind]+' '+w.label),make('span','',w.id));box.append(heading);
  if(w.kind==='note'){
    const input=make('textarea');input.value=w.value;input.maxLength=500;input.placeholder='A private note in this tab...';input.setAttribute('aria-label',w.label+' private note');input.dataset.focus=w.id+'-note';
    input.addEventListener('input',()=>{w.value=input.value;});box.append(input);
  }else if(w.kind==='counter'){
    const row=make('div','count-row'),out=make('output','',String(w.value));out.setAttribute('aria-label',w.label+' count');
    row.append(button('\u2212',()=>{w.value=Math.max(-9999,w.value-1);out.textContent=w.value;},w.id+'-minus'),out,button('+',()=>{w.value=Math.min(9999,w.value+1);out.textContent=w.value;},w.id+'-plus'));box.append(row);
  }else if(w.kind==='checklist'){
    const label=make('label','check'),check=make('input');check.type='checkbox';check.checked=w.checked;check.dataset.focus=w.id+'-check';check.onchange=()=>{w.checked=check.checked;};label.append(check,make('span','','Reviewed locally. Not an execution grant.'));box.append(label);
  }else{box.append(make('p','caption','A mixture can hold any local widget, including another mixture.'));}
  const controls=make('div','widget-tools');
  controls.append(button('Focus',()=>openFocus(w.id),w.id+'-focus'),button('Fork',()=>mutate(()=>forkWidget(garden,w.id)),w.id+'-fork'),button('Retire',()=>mutate(()=>retireWidget(garden,w.id)),w.id+'-retire'));box.append(controls);
  const nest=make('div','nest-row'),choose=make('select');choose.setAttribute('aria-label','Child widget type for '+w.id);choose.dataset.focus=w.id+'-type';
  for(const kind of KINDS){const option=make('option','',glyphs[kind]+' '+kind);option.value=kind;choose.append(option);}choose.value='mixture';
  const add=button('+ Nest',()=>mutate(()=>addChild(garden,w.id,choose.value)),w.id+'-nest');
  const realDepth=locate(garden,w.id)?.depth??depth;add.disabled=realDepth>=MAX_DEPTH;nest.append(choose,add);box.append(nest);
  if(realDepth>=MAX_DEPTH)box.append(make('p','caption','Renderer budget reached; focus or fork to keep work usable.'));
  if(w.children.length){const children=make('div','children');for(const child of w.children)children.append(widgetView(child,depth+1));box.append(children);}
  return box;
}
function refresh(){
  const active=document.activeElement?.dataset.focus;
  const positions=hosts.map(h=>h.closest('.scene-inside').scrollTop);
  hosts.forEach((host,k)=>{const d=garden.scenes[Math.floor(k/3)].drawers[k%3];host.replaceChildren(...d.widgets.map(w=>widgetView(w)));host.closest('.scene-inside').scrollTop=positions[k];});
  if(focusId){const found=locate(garden,focusId);if(found){$('focus-host').replaceChildren(widgetView(found.node));}else{$('focus-dialog').close();focusId=null;}}
  $('regrow').disabled=!garden.retired.length;
  $('events').textContent=garden.events.length?garden.events.map(e=>`${e.at} / ${e.action} / ${e.widget_id} / local only`).join('\n'):'No events.';
  if(active){const scope=$('focus-dialog').open?$('focus-host'):document;[...scope.querySelectorAll('[data-focus]')].find(e=>e.dataset.focus===active)?.focus({preventScroll:true});}
}
function openFocus(id){focusId=id;returnFocus=document.activeElement;const f=locate(garden,id);if(!f)return;$('focus-title').textContent='Enter '+f.node.label+' / '+id;$('focus-host').replaceChildren(widgetView(f.node));if(!$('focus-dialog').open)$('focus-dialog').showModal();}
$('close-focus').onclick=()=>$('focus-dialog').close();
$('focus-dialog').addEventListener('close',()=>{focusId=null;refresh();if(returnFocus?.isConnected)returnFocus.focus({preventScroll:true});});
function markScene(i){garden.active=i;$('scene-counter').textContent=`${i+1} / 4`;$('previous').disabled=i===0;$('next').disabled=i===3;[...$('scene-tabs').children].forEach((b,n)=>b.setAttribute('aria-current',String(i===n)));}
function go(i){i=Math.max(0,Math.min(3,i));markScene(i);const root=$('carousel'),target=root.children[i];root.scrollTo({left:target.offsetLeft-root.children[0].offsetLeft,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});}
for(const [i,s] of garden.scenes.entries()){
  const scene=make('article','scene');scene.dataset.scene=s.id;scene.setAttribute('aria-label',s.title);scene.setAttribute('aria-roledescription','slide');
  const top=make('div','scene-top');top.append(make('span','','\u00e6\u00e6\u00e6://STUDIO'),make('span','',`0${i+1} / 04 \u00b7 9:16`));scene.append(top);
  const hero=make('div','scene-hero');hero.append(make('div','scene-symbol',s.symbol),make('h2','',s.title),make('p','',s.sub));scene.append(hero);
  const inside=make('div','scene-inside');
  if(s.id==='fleet')inside.append(make('p','new-scene-note','Coordination sketch. No agents or email accounts connected.'));
  if(s.id==='public')inside.append(make('p','new-scene-note','Review locally. No repository write or deployment.'));
  s.drawers.forEach((d,j)=>{const drawer=make('details','drawer');drawer.open=d.open;drawer.addEventListener('toggle',()=>{d.open=drawer.open;});drawer.append(make('summary','',`${['\u25c9','\u25c7','\u2727'][j]} ${d.name}`));const host=make('div','drawer-host');hosts.push(host);drawer.append(host);inside.append(drawer);});
  scene.append(inside);const foot=make('div','scene-footer');foot.append(make('span','',ORIGIN),make('span','','\u2764\ufe0f HUMAN://ROOT'));scene.append(foot);$('carousel').append(scene);
  const tab=button(s.symbol,()=>go(i));tab.className='scene-tab';tab.setAttribute('aria-label',s.title+' scene');$('scene-tabs').append(tab);
}
$('previous').onclick=()=>go(garden.active-1);$('next').onclick=()=>go(garden.active+1);
let scrollTimer;$('carousel').addEventListener('scroll',()=>{clearTimeout(scrollTimer);scrollTimer=setTimeout(()=>{const root=$('carousel'),left=root.getBoundingClientRect().left;const distances=[...root.children].map(e=>Math.abs(e.getBoundingClientRect().left-left));markScene(distances.indexOf(Math.min(...distances)));},100);},{passive:true});
$('carousel').addEventListener('keydown',e=>{if(e.target!==e.currentTarget)return;if(e.key==='ArrowRight'){e.preventDefault();go(garden.active+1);}if(e.key==='ArrowLeft'){e.preventDefault();go(garden.active-1);}});
$('seed').onclick=()=>{$('seed-output').textContent='Local seed\n'+($('intention').value.trim()||'Grow a human-directed environment.')+'\n\nChoose a drawer. Nest a note, counter, checklist or mixture. Model and agent bindings remain unconnected.';};
$('regrow').onclick=()=>mutate(()=>restoreWidget(garden,garden.active,0));
$('clear-intention').onclick=()=>{$('intention').value='';$('seed-output').textContent='Intention cleared from this tab.';$('ai-output').textContent='No model output.';$('api-consent').checked=false;updateAsk();};
$('intention').oninput=()=>{$('api-consent').checked=false;updateAsk();};
$('review').onclick=()=>{reviewSnapshot=JSON.stringify(publicProjection(garden),null,2);$('export-preview').textContent=reviewSnapshot;$('export-consent').checked=false;$('download').disabled=true;$('export-dialog').showModal();};
$('close-export').onclick=()=>$('export-dialog').close();
$('export-consent').onchange=()=>{$('download').disabled=!$('export-consent').checked||!reviewSnapshot;};
$('download').onclick=()=>{
  if(!$('export-consent').checked||reviewSnapshot!==JSON.stringify(publicProjection(garden),null,2)){invalidateExport();feedback('Layout changed; review again.');return;}
  const url=URL.createObjectURL(new Blob([reviewSnapshot+'\n'],{type:'application/json'}));const a=make('a');a.href=url;a.download='ae-open-widgets-layout.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);feedback('Reviewed layout downloaded. Nothing was published.');
};
function updateAsk(){$('ask').disabled=busy||!session||!$('api-consent').checked||!$('intention').value.trim();}
function lockAPI(message){session=null;$('api-consent').disabled=true;$('api-consent').checked=false;$('adapter-badge').textContent='LOCKED';$('api-status').textContent=message;updateAsk();}
$('api-consent').onchange=updateAsk;
$('check-adapter').onclick=async()=>{
  lockAPI('Checking same-origin adapter...');$('check-adapter').disabled=true;
  try{const r=await fetch('/api/ae/session',{credentials:'same-origin',cache:'no-store',redirect:'error',signal:AbortSignal.timeout(10000)});const data=await r.json();
    if(!r.ok||data.ready!==true||typeof data.csrf_token!=='string'||data.csrf_token.length<32||!Number.isFinite(data.expires_at))throw Error('locked');
    session=data;$('api-consent').disabled=false;$('adapter-badge').textContent='SESSION CHECKED';$('api-status').textContent='Authorized session found. No model call yet. Review your intention and approve each request.';updateAsk();
  }catch{lockAPI('Adapter unavailable, disabled, or unauthenticated. Local widgets remain usable.');}
  finally{$('check-adapter').disabled=false;}
};
$('ask').onclick=async()=>{
  if($('ask').disabled)return;
  if(Date.now()>=session.expires_at){lockAPI('Session expired. Check it again.');return;}
  const prompt=$('intention').value.trim(),csrf=session.csrf_token;busy=true;updateAsk();$('check-adapter').disabled=true;$('api-status').textContent='Sending only the approved intention. No automatic retry.';
  try{const r=await fetch('/api/ae/respond',{method:'POST',credentials:'same-origin',cache:'no-store',redirect:'error',headers:{'Content-Type':'application/json','X-AE-CSRF':csrf},body:JSON.stringify({request_id:crypto.randomUUID(),prompt,approved:true}),signal:AbortSignal.timeout(35000)});
    const data=await r.json();if(!r.ok||typeof data.text!=='string'||data.text.length>32000||!data.receipt)throw Error('adapter failed');
    $('ai-output').textContent=data.text;$('api-status').textContent=`Provider response: ${data.status}. Receipt ${data.receipt.request_id}. No tools, publication or agent actions executed.`;
  }catch{$('ai-output').textContent='No verified model output. The request may have reached the provider; inspect server records before a manual retry.';lockAPI('Request failed or authorization expired. No automatic retry.');}
  finally{busy=false;$('api-consent').checked=false;$('check-adapter').disabled=false;updateAsk();}
};
markScene(0);refresh();
