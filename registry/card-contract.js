/* Portable board snapshots are context only. Never dispatch an action from a scan. */
(function(root){
 const stages=['audit','repair','verify','publish'];
 function validate(card,known){
  if(!card||typeof card!=='object'||Array.isArray(card)||card.v!==1)throw Error('Unsupported card snapshot.');
  if(typeof card.id!=='string'||!/^[a-zA-Z0-9-]{1,64}$/.test(card.id))throw Error('Invalid card identity.');
  if(typeof card.entry_id!=='string'||!known.has(card.entry_id))throw Error('This capability is not in the registry.');
  if(typeof card.title!=='string'||!card.title.trim()||card.title.length>80)throw Error('Title must be 1–80 characters.');
  if(!['yellow','blue','green'].includes(card.purpose)||!stages.includes(card.stage))throw Error('Invalid purpose or stage.');
  if(typeof card.notes!=='string'||card.notes.length>280)throw Error('Notes must be at most 280 characters.');
  return {v:1,id:card.id,entry_id:card.entry_id,title:card.title.trim(),purpose:card.purpose,stage:card.stage,notes:card.notes};
 }
 function encode(card,known){const c=validate(card,known);return btoa(String.fromCharCode(...new TextEncoder().encode(JSON.stringify(c)))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'')}
 function decode(text,known){if(typeof text!=='string'||text.length>2400||!/^[A-Za-z0-9_-]+$/.test(text))throw Error('Invalid QR snapshot.');const b=atob(text.replace(/-/g,'+').replace(/_/g,'/'));return validate(JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(Uint8Array.from(b,c=>c.charCodeAt(0)))),known)}
 const api={stages,validate,encode,decode};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.aeQRCard=api;
})(typeof window!=='undefined'?window:globalThis);
