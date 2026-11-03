import http from 'node:http';
import {readFile} from 'node:fs/promises';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';
import {createAdapter,headers} from './adapter.mjs';
import {createOpenAIProvider} from './openai.mjs';
const root=fileURLToPath(new URL('../',import.meta.url));
const files={'index.html':'text/html; charset=utf-8','garden.css':'text/css; charset=utf-8','garden.mjs':'text/javascript; charset=utf-8','model.mjs':'text/javascript; charset=utf-8'};
/** Serves only four public assets. Never the repository, server code or .env. */
export function createServer({origin='http://127.0.0.1:4173',adapter=createAdapter({origin})}={}){
  const host=new URL(origin).host;
  const server=http.createServer(async(req,res)=>{
    if(req.url?.startsWith('/api/ae/')){await adapter(req,res);return;}
    headers(res);
    res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'");
    if(req.headers.host!==host){res.writeHead(403);res.end('Host not allowed');return;}
    if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);res.end();return;}
    const pathname=(req.url||'/').split('?')[0];
    let name=pathname==='/'?'index.html':pathname.replace(/^\/open-widgets\/v0\.1\//,'').replace(/^\//,'');
    if(pathname==='/open-widgets/v0.1/')name='index.html';
    if(!Object.hasOwn(files,name)){res.writeHead(404);res.end('Not found');return;}
    try{const bytes=await readFile(path.join(root,name));res.writeHead(200,{'Content-Type':files[name]});res.end(req.method==='HEAD'?undefined:bytes);}catch{res.writeHead(500);res.end('Asset unavailable');}
  });
  server.requestTimeout=10000;server.headersTimeout=10000;server.keepAliveTimeout=3000;
  return server;
}
async function start(){
  const port=Number(process.env.PORT||4173);if(!Number.isInteger(port)||port<1024||port>65535)throw Error('PORT must be 1024-65535');
  const origin=`http://127.0.0.1:${port}`;let adapter=createAdapter({origin});
  if(process.env.AE_OPENAI_ENABLED==='true'){
    if(!process.env.AE_AUTH_MODULE||!path.isAbsolute(process.env.AE_AUTH_MODULE))throw Error('A reviewed absolute AE_AUTH_MODULE path is required; there is no auth bypass');
    const auth=await import(pathToFileURL(process.env.AE_AUTH_MODULE).href);
    if(typeof auth.authenticate!=='function')throw Error('Host module must export authenticate(req)');
    const provider=createOpenAIProvider({apiKey:process.env.OPENAI_API_KEY,model:process.env.OPENAI_MODEL});
    adapter=createAdapter({origin,enabled:true,authenticate:auth.authenticate,provider});
  }
  createServer({origin,adapter}).listen(port,'127.0.0.1',()=>console.log(`MoW Garden at ${origin} / adapter ${process.env.AE_OPENAI_ENABLED==='true'?'configured; authentication still required':'disabled'}`));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))start().catch(()=>{console.error('Startup refused. Check server-only configuration and authentication contract. No secrets logged.');process.exitCode=1;});
