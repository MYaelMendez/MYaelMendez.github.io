export const palettes=Object.freeze(['light','dark','glass']);
export const normalizePalette=value=>palettes.includes(value)?value:'light';
export function tickerItems(state){
  const returned=state.workspaces.filter(w=>w.node?.status==='RETURNED').length;
  const root=state.nodes.find(n=>!n.parentId);
  return [`Intent: ${root?.status.toLowerCase()||'ready to begin'}`,`${returned} / 3 contributions returned`,`${state.events.length} local evidence events`,'Two local text tools','External agents: not connected','Human authority stays here'];
}
export function laneTicker(lane){
  const n=lane.node;
  return [lane.capability,n?`${n.status.toLowerCase()} · revision ${n.revision}`:'select context → prepare',n?.result?'local receipt available':'approval before execution'];
}
export function mountAppearance(doc=document,storage){
  if(storage===undefined)try{storage=globalThis.localStorage;}catch{}
  let palette='light';try{palette=normalizePalette(storage?.getItem('ae-work-palette'));}catch{}
  const buttons=[...doc.querySelectorAll('[data-palette-choice]')];
  const apply=value=>{palette=normalizePalette(value);doc.documentElement.dataset.palette=palette;for(const b of buttons)b.setAttribute('aria-pressed',String(b.dataset.paletteChoice===palette));try{storage?.setItem('ae-work-palette',palette);}catch{}};
  for(const b of buttons)b.addEventListener('click',()=>apply(b.dataset.paletteChoice));apply(palette);
  const motion=doc.getElementById('ticker-motion'), reduced=matchMedia('(prefers-reduced-motion: reduce)');let paused=reduced.matches;
  const update=()=>{doc.documentElement.dataset.tickersPaused=String(paused||doc.hidden);motion.setAttribute('aria-pressed',String(paused));motion.textContent=paused?'Resume tickers':'Pause tickers';};
  motion.addEventListener('click',()=>{paused=!paused;update();});reduced.addEventListener('change',e=>{paused=e.matches;update();});doc.addEventListener('visibilitychange',update);update();
}
