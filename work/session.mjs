import {createPrimitives, verifyEvidence} from './primitives.mjs';
export const lanes = Object.freeze([
  Object.freeze({id:'build', label:'Build', tile:'🔳', capability:'draft.compose'}),
  Object.freeze({id:'inspect', label:'Inspect', tile:'🟥', capability:'text.inspect'}),
  Object.freeze({id:'review', label:'Review', tile:'⬜', capability:'draft.compose'})
]);
export function createWorkspace({now=()=>Date.now()}={}) {
  const principalId='human:local-tab';
  const runtime=createPrimitives({principalId,maxOpen:3,maxDepth:1,maxNodes:4,now});
  const ids=new Map(), approvals=new Map();
  let root=null, serial=Promise.resolve();
  const lane=id=>{const value=lanes.find(l=>l.id===id);if(!value)throw Error('Unknown workspace');return value;};
  async function get(id){lane(id);if(!ids.has(id))throw Error('Prepare this contribution first.');return runtime.inspect(ids.get(id));}
  const api={
    async begin(intent,brief) {
      if(root)throw Error('This session already has an intent.');
      root=await runtime.createRoot({intent,context:[{id:'brief',text:brief,source:'human:provided-in-this-tab'}],ttlMs:3600000});
      return root;
    },
    async prepare(id,{share,notes=''}={}) {
      const l=lane(id);if(!root)throw Error('Begin your intent first.');
      if(ids.has(id))throw Error('This contribution already exists.');
      if(share!==true)throw Error('Select the brief explicitly before preparing a contribution.');
      if(id==='review') {
        for(const required of ['build','inspect'])if(!ids.has(required)||(await get(required)).status!=='RETURNED')throw Error('Build and Inspect must return before review.');
        if(typeof notes!=='string'||!notes.trim())throw Error('Add your own review notes after reading the contributions.');
      }
      const body=id==='review'?notes:root.contextRefs[0].text;
      const node=await runtime.proposeChild({parentId:root.id,intent:l.label+' contribution',capability:l.capability,
        payload:l.capability==='text.inspect'?{text:body}:{title:id==='review'?'Human review notes':root.intent,body},contextIds:['brief'],ttlMs:300000});
      ids.set(id,node.id);return node;
    },
    async approve(id){const n=await get(id);approvals.set(id,await runtime.approveLocal(n.id,{actor:principalId}));},
    async run(id){const n=await get(id);const result=await runtime.executeLocal(n.id,approvals.get(id));approvals.delete(id);return result;},
    async revise(id,body){const n=await get(id);const payload=n.capability==='text.inspect'?{text:body}:{title:n.payload.title,body};
      const result=await runtime.revise(n.id,{payload});approvals.delete(id);return result;},
    async revoke(id){if(!approvals.has(id))throw Error('No local approval to revoke.');await runtime.revokeLocal(approvals.get(id));approvals.delete(id);},
    async rejoin(){if(!root)throw Error('Begin your intent first.');return runtime.rejoin(root.id);},
    async complete(){if(ids.size!==3)throw Error('All three contributions must return first.');return runtime.completeRoot({actor:principalId});},
    async cancel(){if(!root)throw Error('Begin your intent first.');await runtime.cancel(root.id,{actor:principalId});approvals.clear();},
    async snapshot(){const s=await runtime.exportEvidence();return {...s,workspaces:lanes.map(l=>({...l,node:s.nodes.find(n=>n.id===ids.get(l.id))||null})),started:!!root};},
    async evidence(){const s=await runtime.exportEvidence();if(!await verifyEvidence(s.events,s.anchor))throw Error('Local evidence integrity check failed.');return s;}
  };
  return Object.freeze(Object.fromEntries(Object.entries(api).map(([name,fn])=>[name,(...args)=>{
    const result=serial.then(()=>fn(...args));serial=result.catch(()=>{});return result;
  }])));
}
