import {createWorkspace} from './session.mjs';
import {mountGlass} from './webgl.mjs';
const $=id=>document.getElementById(id);
const session=createWorkspace();
let active='build', busy=false, shownInput='';
const descriptions={build:['Build a draft','Format your selected brief into an unsent draft. No model generates text.'],inspect:['Inspect the text','Count the characters, words and lines in your selected input. No source verification or risk analysis is performed.'],review:['Review the contributions','Read the returned draft and text counts, then record your own judgment. This tool formats your notes; it does not evaluate them.']};
const make=(tag,value,parent)=>{const el=document.createElement(tag);if(value!==undefined)el.textContent=value;if(parent)parent.append(el);return el;};
function saveJSON(value){const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json'}));const link=make('a');link.href=url;link.download='ae-work-here-evidence.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
async function act(fn){if(busy)return;busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);try{await fn();}catch(e){$('notice').textContent=e.message;}finally{busy=false;await render();}}
async function render(){
  const s=await session.snapshot(), root=s.nodes.find(n=>!n.parentId);
  const terminal=root&&['RETURNED','CANCELLED','EXPIRED'].includes(root.status);
  const selected=s.workspaces.find(l=>l.id===active), node=selected.node;
  const returned=s.workspaces.filter(l=>l.node?.status==='RETURNED');
  $('begin').disabled=s.started||busy;$('intent').readOnly=s.started;$('brief').readOnly=s.started;
  for(const l of s.workspaces){$('state-'+l.id).textContent=l.node?`${l.node.status.toLowerCase()} · r${l.node.revision}`:terminal?'session closed':!s.started?'Awaiting intent':l.id==='review'&&returned.length<2?'Needs Build + Inspect':'Ready to prepare';}
  document.querySelectorAll('[data-lane]').forEach(b=>{b.disabled=busy;b.setAttribute('aria-pressed',String(b.dataset.lane===active));});
  $('workspace-title').textContent=descriptions[active][0];$('description').textContent=descriptions[active][1];$('capability').textContent=selected.capability+' · local';
  $('prepare-form').hidden=!!node;$('review-input').hidden=active!=='review';
  $('prepare').disabled=busy||!s.started||terminal||(active==='review'&&(!s.workspaces.find(l=>l.id==='build').node||s.workspaces.find(l=>l.id==='build').node.status!=='RETURNED'||s.workspaces.find(l=>l.id==='inspect').node?.status!=='RETURNED'));
  $('share').disabled=!s.started||terminal;$('notes').disabled=!s.started||terminal;
  $('task').hidden=!node;
  if(node){
    $('task-state').textContent=`${node.status} · revision ${node.revision} · deadline ${new Date(node.deadline).toLocaleTimeString()}`;
    const key=node.id+':'+node.revision;if(shownInput!==key){$('payload').value=node.payload.text??node.payload.body;shownInput=key;}
    const editable=!terminal&&['PROPOSED','QUEUED'].includes(node.status);
    $('payload').readOnly=!editable;
    const approval=s.approvals.findLast(a=>a.conversationId===node.id&&!a.revoked&&!a.consumed&&a.revision===node.revision&&a.expiresAt>Date.now());
    $('revise').disabled=busy||!editable;$('approve').disabled=busy||!editable;$('run').disabled=busy||terminal||node.status!=='QUEUED'||!approval;$('revoke').disabled=busy||terminal||!approval;
    $('task-output').textContent=node.result?JSON.stringify(node.result,null,2):'No output yet. Approve the exact revision, then run the local tool.';
  }
  $('return-count').textContent=`${returned.length} / 3 returned`;
  $('contributions').replaceChildren();
  for(const l of returned){const card=make('article');card.className='contribution '+l.id;make('h3',`${l.tile} ${l.label}`,card);make('pre',JSON.stringify(l.node.result,null,2),card);const receipt=s.events.findLast(e=>e.conversationId===l.node.id&&e.type==='result.returned');const info=make('p',`Local receipt ${receipt?.id||'unavailable'} · r${l.node.revision}`,card);info.className='receipt';$('contributions').append(card);}
  if(!returned.length){const p=make('p','Your contributions will return here with their local receipts.',$('contributions'));p.className='small';}
  $('rejoin').disabled=busy||!s.started||terminal||!returned.length;$('complete').disabled=busy||terminal||returned.length!==3;$('export').disabled=busy||!s.started;$('cancel').disabled=busy||!s.started||terminal;$('motion').disabled=false;
  $('completion').textContent=root?.status==='RETURNED'?'Intent completed locally. No external action was performed.':terminal?`Intent ${root.status.toLowerCase()}. Reload to begin a new session.`:'Completion requires Build, Inspect and your review notes to return.';
  $('event-count').textContent=`(${s.events.length} events)`;$('ledger').textContent=s.events.length?s.events.map(e=>`${e.sequence}. ${e.type} · ${e.hash.slice(0,12)}`).join('\n'):'No events yet.';
}
$('intent-form').addEventListener('submit',e=>{e.preventDefault();act(async()=>{await session.begin($('intent').value,$('brief').value);$('notice').textContent='Intent created in this tab. Select the brief explicitly for each contribution.';});});
document.querySelectorAll('[data-lane]').forEach(b=>b.addEventListener('click',()=>{if(busy)return;active=b.dataset.lane;$('share').checked=false;render().catch(e=>$('notice').textContent=e.message);}));
$('prepare-form').addEventListener('submit',e=>{e.preventDefault();act(async()=>{await session.prepare(active,{share:$('share').checked,notes:$('notes').value});$('notice').textContent='Contribution proposed. Inspect the exact input before approving it.';});});
$('revise').onclick=()=>act(async()=>{await session.revise(active,$('payload').value);$('notice').textContent='New revision saved. Previous approval is unusable; approve this revision again.';});
$('approve').onclick=()=>act(async()=>{
  const s=await session.snapshot(), n=s.workspaces.find(l=>l.id===active).node;
  if($('payload').value!==(n.payload.text??n.payload.body))throw Error('Save your edited input as a new revision before approving.');
  await session.approve(active);$('notice').textContent='Local approval recorded for this exact revision and payload. Valid for up to one minute.';
});
$('run').onclick=()=>act(async()=>{
  const s=await session.snapshot(), n=s.workspaces.find(l=>l.id===active).node;
  if($('payload').value!==(n.payload.text??n.payload.body))throw Error('Unsaved changes: save a revision and approve again before running.');
  await session.run(active);$('notice').textContent='Local tool returned a contribution and a receipt. No external action occurred.';
});
$('revoke').onclick=()=>act(async()=>{await session.revoke(active);$('notice').textContent='Local approval revoked.';});
$('rejoin').onclick=()=>act(async()=>{const result=await session.rejoin();$('notice').textContent=result.complete?'All contributions rejoined. You can complete this intent.':'Returned contributions rejoined; outstanding work remains.';});
$('complete').onclick=()=>act(async()=>{await session.complete();$('notice').textContent='Intent completed locally. Export the evidence if you wish to keep it.';});
$('cancel').onclick=()=>act(async()=>{await session.cancel();$('notice').textContent='Open local work cancelled. Returned contributions remain in the evidence.';});
$('export').onclick=()=>act(async()=>{saveJSON(await session.evidence());$('notice').textContent='Evidence exported with your selected text, local receipts, head and count. Keep it private when appropriate.';});
mountGlass($('world'),$('motion'),$('render-status'));
render().catch(e=>$('notice').textContent=e.message);
setInterval(()=>{if(!busy)render().catch(e=>$('notice').textContent=e.message);},15000);
