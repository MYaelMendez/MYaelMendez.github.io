export const HF_MODELS='https://huggingface.co/api/models?sort=downloads&direction=-1&limit=6';
export function validateRegistry(value){
  if(value?.schema!=='ae.store.sources.v1'||!Array.isArray(value.entries)||value.entries.length>30)throw Error('Unsupported source registry');
  const ids=new Set();
  return value.entries.map(e=>{const u=new URL(e.url);if(u.protocol!=='https:'||u.username||u.password||!['huggingface.co','llm.store'].includes(u.hostname)||!['models','datasets','spaces','indexes'].includes(e.category)||typeof e.id!=='string'||ids.has(e.id)||typeof e.label!=='string'||typeof e.description!=='string'||typeof e.icon!=='string'||typeof e.source!=='string')throw Error('Invalid discovery source');ids.add(e.id);return {...e,url:u.href};});
}
export function modelCards(raw){
  if(!Array.isArray(raw))throw Error('Invalid public model index');
  const seen=new Set();
  return raw.slice(0,6).map(m=>{const id=m?.id||m?.modelId;if(typeof id!=='string'||id.length>180||!/^[-\w.]+(?:\/[-\w.]+)?$/.test(id)||id.split('/').some(p=>p==='.'||p==='..')||seen.has(id))throw Error('Invalid model identifier');seen.add(id);return {id,label:id,icon:'◉',category:'models',source:'Hugging Face public API',url:'https://huggingface.co/'+id.split('/').map(encodeURIComponent).join('/'),description:typeof m.pipeline_tag==='string'?m.pipeline_tag.slice(0,100):'Open the model card to inspect its task and license.',status:'metadata_only'};});
}
export async function loadPublicModels(fetchImpl=fetch){
  const r=await fetchImpl(HF_MODELS,{credentials:'omit',referrerPolicy:'no-referrer',signal:AbortSignal.timeout(10000)});
  if(!r.ok)throw Error('Public model index returned HTTP '+r.status);
  const reader=r.body.getReader(),chunks=[];let size=0;
  try{while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>131072)throw Error('Index response too large');chunks.push(value);}}finally{await reader.cancel().catch(()=>{});}
  const data=new Uint8Array(size);let offset=0;for(const c of chunks){data.set(c,offset);offset+=c.length;}
  return modelCards(JSON.parse(new TextDecoder().decode(data)));
}
export async function mountStore(doc=document){
  const $=id=>doc.getElementById(id);let registry=[],models=[],filter='all',query='';
  const text=(tag,value,parent)=>{const n=doc.createElement(tag);n.textContent=value;parent.append(n);return n;};
  function render(){const entries=[...registry,...models].filter(e=>(filter==='all'||e.category===filter)&&[e.label,e.description,e.source].join(' ').toLowerCase().includes(query));$('store-grid').replaceChildren();for(const e of entries){const card=doc.createElement('article');card.className='nano-widget';text('span',e.category.toUpperCase(),card).className='nano-kind';const a=text('a',`${e.icon} ${e.label} ↗`,card);a.href=e.url;a.target='_blank';a.rel='noopener noreferrer';text('p',e.description,card);text('span',`${e.source} · ${e.status==='metadata_only'?'metadata only':'external link'}`,card).className='nano-state';$('store-grid').append(card);}if(!entries.length)text('p','No matching tiles. Try another filter.',$('store-grid'));for(const b of doc.querySelectorAll('[data-store-filter]'))b.setAttribute('aria-pressed',String(b.dataset.storeFilter===filter));$('store-count').textContent=`${entries.length} discovery tiles`;
    const track=$('store-ticker'),v=`llm.store　 ·　 ${registry.length} source links　 ·　 ${models.length} public model cards loaded　 ·　 Discover first. Connect explicitly.　 ·　 `;track.replaceChildren();text('span',v,track);text('span',v,track).setAttribute('aria-hidden','true');}
  for(const b of doc.querySelectorAll('[data-store-filter]'))b.onclick=()=>{filter=b.dataset.storeFilter;render();};
  $('store-search').addEventListener('input',()=>{query=$('store-search').value.trim().toLowerCase();render();});
  $('load-models').onclick=async()=>{const button=$('load-models');button.disabled=true;$('store-status').textContent='Fetching six public model cards from Hugging Face…';try{models=await loadPublicModels();$('store-status').textContent=`Retrieved ${models.length} public model cards at ${new Date().toISOString()}. Metadata only; no inference connected.`;render();}catch(e){$('store-status').textContent='Model feed unavailable: '+e.message+'. Source links remain available.';}finally{button.disabled=false;}};
  try{const r=await fetch(new URL('store-registry.json',import.meta.url));if(!r.ok)throw Error('Registry unavailable');registry=validateRegistry(await r.json());$('store-status').textContent='Source links loaded. Public model metadata is fetched only when you choose “Load public models”.';render();}catch(e){$('store-status').textContent=e.message;}
}
