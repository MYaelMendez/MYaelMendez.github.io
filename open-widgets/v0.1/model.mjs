/** The widget tree is local data, never a capability grant. */
export const VERSION = '0.1.0';
export const ORIGIN = 'x0:y0:z0:\u00e6:\u00e6';
export const PUBLIC = 'x0:y0:z:0:\u00e6:\u00e6:\u00e6';
export const MAX_DEPTH = 6;
export const MAX_NODES = 80;
export const KINDS = Object.freeze(['note', 'counter', 'checklist', 'mixture']);
export const SCENES = Object.freeze([
  {id:'garden', symbol:'\ud83c\udf4a\ud83e\udda9', title:'MoW Garden', sub:'Grow \u00b7 Adapt \u00b7 Regenerate', drawers:['Orchard','Living Worlds','Nested Mixtures']},
  {id:'fleet', symbol:'\ud83e\udd16\ud83d\udce7\ud83e\udd16', title:'Agent Fleet', sub:'Many agents \u00b7 One principal', drawers:['Coordination','Communications','Witness']},
  {id:'factory', symbol:'\ud83e\udde9', title:'Widget Factory', sub:'Build environments within environments', drawers:['Discovery','Composer','Viewports']},
  {id:'public', symbol:'\ud83c\udf10', title:'Public Worlds', sub:'Review \u00b7 Fork \u00b7 Publish \u00b7 Teach', drawers:['Source','Destinations','Human value']}
]);
let sequence = 0;
function widget(kind='mixture', label=kind) {
  if (!KINDS.includes(kind)) throw Error('Unknown widget kind');
  return {id:`w-${++sequence}`, kind, label:label.slice(0,60), value:kind==='counter'?0:'', checked:false, children:[]};
}
export function createGarden() {
  return {version:VERSION, revision:0, active:0, retired:[], events:[], scenes:SCENES.map(s=>({...s,
    drawers:s.drawers.map((name,i)=>({name, open:i===0, widgets:[widget(i===0?'note':i===1?'counter':'mixture',name)]}))
  }))};
}
export function locate(garden,id) {
  function search(list,depth) {
    for (let i=0;i<list.length;i++) {
      const node=list[i];
      if(node.id===id)return {node,list,index:i,depth};
      const hit=search(node.children,depth+1);if(hit)return hit;
    }
    return null;
  }
  for(const s of garden.scenes)for(const d of s.drawers){const hit=search(d.widgets,0);if(hit)return hit;}
  return null;
}
export function countNodes(garden) {
  let n=0;function walk(nodes){for(const w of nodes){n++;walk(w.children);}}
  for(const s of garden.scenes)for(const d of s.drawers)walk(d.widgets);return n;
}
function record(garden,action,id) {
  garden.revision++;
  garden.events.push({action,widget_id:id,at:new Date().toISOString(),kind:'local_ui',external_action:false});
  if(garden.events.length>20)garden.events.shift();
}
export function addChild(garden,id,kind) {
  const found=locate(garden,id);if(!found)throw Error('Widget not found');
  if(found.depth>=MAX_DEPTH)throw Error('Rendering budget reached. Focus this world or fork a shallower mixture.');
  if(countNodes(garden)>=MAX_NODES)throw Error('Widget budget reached. Retire a component before growing more.');
  const child=widget(kind);found.node.children.push(child);record(garden,'nested',child.id);return child;
}
function template(node) {return {kind:node.kind,label:node.label,children:node.children.map(template)};}
function regrow(t) {const n=widget(t.kind,t.label);n.children=t.children.map(regrow);return n;}
function templateCount(t){return 1+t.children.reduce((n,c)=>n+templateCount(c),0);}
export function forkWidget(garden,id) {
  const f=locate(garden,id);if(!f)throw Error('Widget not found');
  const t=template(f.node);if(countNodes(garden)+templateCount(t)>MAX_NODES)throw Error('Widget budget reached');
  const copy=regrow(t);f.list.splice(f.index+1,0,copy);record(garden,'forked_without_private_state',copy.id);return copy;
}
export function retireWidget(garden,id) {
  const f=locate(garden,id);if(!f)throw Error('Widget not found');
  garden.retired.push(template(f.node));if(garden.retired.length>12)garden.retired.shift();
  f.list.splice(f.index,1);record(garden,'retired',id);
}
export function restoreWidget(garden,scene,drawer) {
  const t=garden.retired.at(-1);if(!t)throw Error('No retired component');
  if(countNodes(garden)+templateCount(t)>MAX_NODES)throw Error('Widget budget reached');
  const d=garden.scenes[scene]?.drawers[drawer];if(!d)throw Error('Unknown drawer');
  const copy=regrow(t);d.widgets.push(copy);garden.retired.pop();record(garden,'regrown_without_private_state',copy.id);return copy;
}
export function publicProjection(garden) {
  function project(w){return {id:w.id,kind:w.kind,label:w.label,children:w.children.map(project),grant:null};}
  return {schema:'ae.open-widgets.layout.v1',version:VERSION,source_revision:garden.revision,
    origin:ORIGIN,public_address:PUBLIC,viewport:{preferred:'9:16',adaptive:true},
    scenes:garden.scenes.map(s=>({id:s.id,title:s.title,drawers:s.drawers.map(d=>({name:d.name,widgets:d.widgets.map(project)}))})),
    authority:{principal:'human',inherit:false,grant:null},publication:{status:'draft_not_deployed'},
    connections:{openai:'not_established_by_export',agents:'not_connected'},private_state_included:false};
}
