const assert=require('node:assert/strict'),c=require('../registry/card-contract.js');
const known=new Map([['entry-id',{}]]),card={v:1,id:'task-1',entry_id:'entry-id',title:'🍊 Cultivar æ',purpose:'green',stage:'verify',notes:'Evidencia 🟨🟦🟩'};
assert.deepEqual(c.decode(c.encode(card,known),known),card);
for(const change of [{v:2},{entry_id:'unknown'},{stage:'execute'},{purpose:'red'},{title:''},{notes:'x'.repeat(281)}])assert.throws(()=>c.validate({...card,...change},known));
assert.throws(()=>c.decode('bad/?',known));
assert.equal(c.validate({...card,url:'javascript:alert(1)',authority:'admin'},known).url,undefined);
const fs=require('fs'),qr=require('../assets/qrcode.js');const payload='https://myaelmendez.github.io/registry/#card/'+c.encode(card,known);const q=qr(0,'M');q.addData(payload);q.make();const n=q.getModuleCount(),size=(n+8)*4,bytes=Buffer.alloc(size*size*4,255);
for(let y=0;y<n;y++)for(let x=0;x<n;x++)if(q.isDark(y,x))for(let dy=0;dy<4;dy++)for(let dx=0;dx<4;dx++){const i=(((y+4)*4+dy)*size+(x+4)*4+dx)*4;bytes[i]=bytes[i+1]=bytes[i+2]=0}
if(process.env.AEQR_DECODER){const decode=require(process.env.AEQR_DECODER);assert.equal(decode(new Uint8ClampedArray(bytes),size,size).data,payload)}
console.log('PASS Unicode QR snapshot, known capability binding, strict input validation, and context-only whitelist'+(process.env.AEQR_DECODER?' · independent QR decode':''));
