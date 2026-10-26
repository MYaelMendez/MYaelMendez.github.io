export const starters=Object.freeze({
 enterprise:{intent:'Introduce my enterprise',brief:'We help [people] accomplish [purpose].\nOur first useful contribution is [result].\nThe next action I can take is [action].'},
 learning:{intent:'Shape a learning resource',brief:'Who is learning: [audience]\nWhat they should understand: [topic]\nOne activity they can try: [exercise]'},
 project:{intent:'Plan my next contribution',brief:'Purpose: [why this matters]\nCurrent work: [what exists]\nNext contribution: [one concrete artifact]\nEvidence to check: [how I will review it]'}
});
export function nextStep(state,now=Date.now()){
 const root=state.nodes.find(n=>!n.parentId);
 if(!state.started)return {title:'What will you build today?',detail:'Choose a starting point, or bring your own intent. Nothing runs until you review it.',label:'Start building →',target:'intent'};
 if(root&&['RETURNED','CANCELLED','EXPIRED'].includes(root.status))return {title:root.status==='RETURNED'?'Your work has returned.':'This session is closed.',detail:'Export your evidence before reloading. Work stays in this tab.',label:'Keep the evidence →',target:'export'};
 const lane=state.workspaces.find(l=>l.node?.status!=='RETURNED');
 if(!lane)return {title:'Three contributions. Your next decision.',detail:'Review the returned work, then complete your intent.',label:'Review and complete →',target:'complete'};
 const node=lane.node;
 if(node&&['CANCELLED','EXPIRED'].includes(node.status))return {title:lane.label+' needs a new session.',detail:'Keep your evidence before reloading. Closed work cannot be approved again.',label:'Keep the evidence →',target:'export',lane:lane.id};
 if(!node)return {title:'Next: '+lane.label.toLowerCase()+'.',detail:lane.id==='review'?'Read the two contributions, write your judgment, and explicitly select the context.':'Select the brief you want to use, then prepare a contribution.',label:lane.id==='review'?'Write your review →':'Choose context →',target:lane.id==='review'?'notes':'share',lane:lane.id};
 const approval=state.approvals.findLast(a=>a.conversationId===node.id&&!a.revoked&&!a.consumed&&a.revision===node.revision&&a.expiresAt>now);
 return approval?{title:'Your '+lane.label.toLowerCase()+' task is approved.',detail:'Run the bounded local tool to return a contribution and receipt.',label:'Go to the approved task →',target:'run',lane:lane.id}:{title:'Review your '+lane.label.toLowerCase()+' input.',detail:'Read the exact payload. Approve this revision when you are ready.',label:'Review this task →',target:'payload',lane:lane.id};
}
