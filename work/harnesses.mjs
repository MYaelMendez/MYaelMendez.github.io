// Harness licensing records inspected 2026-10-28. Discovery metadata is not a legal grant.
export const CHECKED_AT='2026-10-28';
export const HARNESSES=Object.freeze([
  {
    "id": "codex-cli",
    "name": "Codex CLI",
    "license": "Apache-2.0",
    "kind": "open",
    "source": "https://github.com/openai/codex/blob/main/LICENSE",
    "model": "Model licensing depends on the selected provider or local model; not covered by the CLI license.",
    "service": "Hosted Codex and API access have separate service terms and billing.",
    "status": "CLI not connected here. Separate hosted workshop: preparation available; execution blocked in the last budget test."
  },
  {
    "id": "openclaw",
    "name": "OpenClaw",
    "license": "MIT",
    "kind": "open",
    "source": "https://github.com/openclaw/openclaw/blob/main/LICENSE",
    "model": "Choose a model/provider separately and inspect its license and access terms.",
    "service": "Self-hosting and provider API charges are separate from the harness license.",
    "status": "Not installed or connected here."
  },
  {
    "id": "hermes",
    "name": "Hermes Agent",
    "license": "MIT",
    "kind": "open",
    "source": "https://github.com/NousResearch/hermes-agent/blob/main/LICENSE",
    "model": "Model licensing and provider access are separate choices.",
    "service": "Local runtime and any hosted service retain their own requirements and costs.",
    "status": "Not installed or connected here."
  },
  {
    "id": "deepseek-harness",
    "name": "DeepSeek Harness",
    "license": "MIT",
    "kind": "open",
    "source": "https://github.com/deepseek-ai/deepseek-harness/blob/master/LICENSE",
    "model": "The harness license does not license its selected model or API.",
    "service": "Desktop/self-hosted setup and any model service are separate.",
    "status": "Not installed or connected here."
  },
  {
    "id": "copilot-cli",
    "name": "Copilot CLI",
    "license": "Proprietary",
    "kind": "proprietary",
    "source": "https://github.com/github/copilot-cli/blob/main/LICENSE.md",
    "model": "Model/provider availability and terms depend on the configured service.",
    "service": "Copilot service terms and usage billing are separate. Its MIT-licensed SDK does not make the CLI open source.",
    "status": "Not installed or connected here."
  },
  {
    "id": "claude-code",
    "name": "Claude Code",
    "license": "Proprietary",
    "kind": "proprietary",
    "source": "https://github.com/anthropics/claude-code/blob/main/LICENSE.md",
    "model": "Model access and use remain subject to the applicable provider terms.",
    "service": "Anthropic commercial/service terms apply separately from this environment.",
    "status": "Not installed or connected here."
  }
].map(Object.freeze));
export function filterHarnesses(filter='open'){
 if(!['all','open','MIT','Apache-2.0','proprietary'].includes(filter))throw Error('Unknown license filter');
 return HARNESSES.filter(h=>filter==='all'||h.kind===filter||h.license===filter);
}
export function makeHarnessPlan(id,filter){
 const h=filterHarnesses(filter).find(h=>h.id===id);
 if(!h)throw Error('Harness is not in the selected license group');
 return {schema:'ae.harness-plan.v1',status:'proposed',harness:h.id,harnessLicense:h.license,licenseSource:h.source,licenseCheckedAt:CHECKED_AT,model:null,service:null,connection:'not_connected_by_selection',authority:{inherits:false,grants:[]}};
}
export function mountHarnessSelector(doc=document){
 const $=id=>doc.getElementById(id);
 if(!$('harness-license'))return;
 const filter=$('harness-license'),choice=$('harness-choice');
 const show=(id,text)=>{$(id).textContent=text;};
 function clearPlan(){show('harness-plan-state','Selection only · nothing installed, connected or executed.');$('harness-plan').hidden=true;show('harness-plan-json','');}
 function inspect(){
  clearPlan();
  const h=filterHarnesses(filter.value).find(h=>h.id===choice.value);
  if(!h)throw Error('Choose a listed harness');
  show('harness-name',h.name);show('harness-license-label',h.license+' · '+(h.kind==='open'?'open-source harness':'proprietary harness'));
  $('harness-source').href=h.source;show('harness-model',h.model);show('harness-service',h.service);show('harness-connection',h.status);
  $('harness-hosted').hidden=h.id!=='codex-cli';
 }
 function list(){
  const old=choice.value,items=filterHarnesses(filter.value);
  choice.replaceChildren();
  for(const h of items){const o=doc.createElement('option');o.value=h.id;o.textContent=h.name;choice.append(o);}
  choice.value=items.some(h=>h.id===old)?old:items[0].id;
  show('harness-count',items.length+' matching harnesses');
  inspect();
 }
 filter.addEventListener('change',list);choice.addEventListener('change',inspect);
 $('harness-select').addEventListener('click',()=>{
  const plan=makeHarnessPlan(choice.value,filter.value);
  show('harness-plan-json',JSON.stringify(plan,null,2));$('harness-plan').hidden=false;
  show('harness-plan-state','Added to this tab’s proposed plan. No runtime, credentials, spend or authority granted. Changing the selection clears this plan.');
 });
 list();$('harness-select').disabled=false;
}
if(typeof document!=='undefined')mountHarnessSelector();
