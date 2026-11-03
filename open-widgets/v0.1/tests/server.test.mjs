import test from 'node:test';import assert from 'node:assert/strict';import http from 'node:http';import {createServer} from '../server/dev-server.mjs';
test('static server exposes only frontend assets, not secrets or backend source',async t=>{
  const server=createServer({origin:'http://127.0.0.1:4173'});await new Promise(r=>server.listen(0,'127.0.0.1',r));t.after(()=>{server.closeAllConnections();return new Promise(r=>server.close(r));});const port=server.address().port;
  const get=p=>new Promise((resolve,reject)=>{http.get({host:'127.0.0.1',port,path:p,headers:{Host:'127.0.0.1:4173'}},res=>{res.resume();resolve({status:res.statusCode,headers:res.headers});}).on('error',reject);});
  for(const p of ['/','/garden.css','/garden.mjs','/model.mjs','/open-widgets/v0.1/']){const r=await get(p);assert.equal(r.status,200,p);assert(r.headers['content-security-policy'].includes("connect-src 'self'"));}
  for(const p of ['/.env','/server/openai.mjs','/package.json','/%2e%2e/.env','/private/config','/../README.md'])assert.equal((await get(p)).status,404,p);
  assert.equal((await fetch(`http://127.0.0.1:${port}/`)).status,403,'unexpected Host is blocked');
});
