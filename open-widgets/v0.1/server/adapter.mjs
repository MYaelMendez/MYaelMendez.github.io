import {timingSafeEqual, createHash, randomUUID} from 'node:crypto';

export class AdapterError extends Error {
  constructor(status,code){super(code);this.status=status;this.code=code;}
}
const fail=(status,code)=>{throw new AdapterError(status,code);};
export function headers(res){
  res.setHeader('Cache-Control','no-store');res.setHeader('X-Content-Type-Options','nosniff');
  res.setHeader('Referrer-Policy','no-referrer');res.setHeader('Cross-Origin-Resource-Policy','same-origin');
}
function send(res,status,body){headers(res);res.writeHead(status,{'Content-Type':'application/json; charset=utf-8'});res.end(JSON.stringify(body));}
const token=t=>typeof t==='string'&&/^[A-Za-z0-9_-]{32,128}$/.test(t);
const equal=(a,b)=>token(a)&&token(b)&&a.length===b.length&&timingSafeEqual(Buffer.from(a),Buffer.from(b));
export function validateRequest(value){
  if(!value||Array.isArray(value)||typeof value!=='object')fail(400,'invalid_request');
  if(Object.keys(value).sort().join(',')!=='approved,prompt,request_id')fail(400,'unknown_or_missing_fields');
  if(typeof value.request_id!=='string'||!/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i.test(value.request_id))fail(400,'invalid_request_id');
  if(value.approved!==true)fail(403,'approval_required');
  if(typeof value.prompt!=='string'||!value.prompt.trim()||value.prompt.length>2000||/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(value.prompt))fail(400,'invalid_prompt');
  return {request_id:value.request_id.toLowerCase(),prompt:value.prompt.trim(),approved:true};
}
async function body(req){
  if(req.headers['content-encoding'])fail(415,'encoding_not_supported');
  if(!/^application\/json(?:\s*;\s*charset=utf-8)?$/i.test(req.headers['content-type']||''))fail(415,'json_required');
  if(Number(req.headers['content-length'])>8192)fail(413,'request_too_large');
  return new Promise((resolve,reject)=>{
    let chunks=[],size=0,finished=false;
    const done=(err,value)=>{if(finished)return;finished=true;clearTimeout(timer);chunks=[];err?reject(err):resolve(value);};
    const timer=setTimeout(()=>done(new AdapterError(408,'body_timeout')),5000);
    req.on('data',chunk=>{if(finished)return;size+=chunk.length;if(size>8192){done(new AdapterError(413,'request_too_large'));return;}chunks.push(chunk);});
    req.on('end',()=>{if(finished)return;try{const text=new TextDecoder('utf-8',{fatal:true}).decode(Buffer.concat(chunks));done(null,JSON.parse(text));}catch{done(new AdapterError(400,'invalid_json'));}});
    req.on('error',()=>done(new AdapterError(400,'invalid_body')));
    req.on('aborted',()=>done(new AdapterError(400,'aborted_body')));
  });
}
/**
 * Host contract: authenticate(req) MUST independently verify a server session and
 * return {id, expiresAt, scopes:['ae:respond'], csrfToken} or null. No caller-supplied
 * identity/header is trusted here. The default authenticates nobody.
 * Quotas below are bounded single-process PILOT limits, not a distributed budget.
 */
export function createAdapter({origin='http://127.0.0.1:4173',enabled=false,authenticate=async()=>null,provider=null,now=Date.now,perMinute=6,maxCalls=50,maxConcurrent=2}={}){
  const url=new URL(origin);
  if(url.origin!==origin||url.username||url.password||!['https:','http:'].includes(url.protocol))throw Error('Use an exact origin');
  if(url.protocol==='http:'&&!['127.0.0.1','localhost','[::1]'].includes(url.hostname))throw Error('Nonlocal origins require HTTPS');
  for(const n of [perMinute,maxCalls,maxConcurrent])if(!Number.isSafeInteger(n)||n<1||n>1000)throw Error('Invalid pilot limit');
  const rates=new Map(),seen=new Map(),activeByUser=new Map();let active=0,calls=0;
  return async function handle(req,res){
    const requestId=randomUUID();
    try{
      if(req.headers.host!==url.host)fail(403,'host_not_allowed');
      if(req.headers.origin&&req.headers.origin!==origin)fail(403,'origin_not_allowed');
      if(req.headers['sec-fetch-site']&&!['same-origin','none'].includes(req.headers['sec-fetch-site']))fail(403,'cross_site_request');
      const sessionRoute=req.url==='/api/ae/session';
      if(!sessionRoute&&req.url!=='/api/ae/respond')fail(404,'not_found');
      if(req.method!==(sessionRoute?'GET':'POST'))fail(405,'method_not_allowed');
      if(!sessionRoute&&req.headers.origin!==origin)fail(403,'origin_required');
      if(!enabled||typeof provider!=='function')fail(503,'adapter_disabled');
      let s;try{s=await authenticate(req);}catch{fail(401,'authentication_required');}
      if(!s||typeof s.id!=='string'||!/^[A-Za-z0-9._:-]{1,100}$/.test(s.id)||!Number.isFinite(s.expiresAt)||s.expiresAt<=now()||!token(s.csrfToken))fail(401,'authentication_required');
      if(!Array.isArray(s.scopes)||!s.scopes.includes('ae:respond'))fail(403,'scope_required');
      if(sessionRoute){send(res,200,{ready:true,csrf_token:s.csrfToken,expires_at:s.expiresAt,capability:'text_only',provider_access:'not_tested_by_session_check'});return;}
      if(!equal(req.headers['x-ae-csrf'],s.csrfToken))fail(403,'csrf_required');
      const input=validateRequest(await body(req));
      const at=now();for(const [k,v] of rates)if(v.until<=at)rates.delete(k);for(const [k,expiry] of seen)if(expiry<=at)seen.delete(k);
      const key=createHash('sha256').update(s.id+'\0'+input.request_id).digest('hex');
      if(seen.has(key))fail(409,'request_already_attempted');
      if(calls>=maxCalls||seen.size>=1000)fail(429,'pilot_budget_exhausted');
      let rate=rates.get(s.id);
      if(!rate){if(rates.size>=1000)fail(429,'pilot_capacity');rate={count:0,until:at+60000};rates.set(s.id,rate);}
      if(rate.count>=perMinute)fail(429,'rate_limited');
      if(active>=maxConcurrent||activeByUser.has(s.id))fail(429,'busy');
      // Reserve before awaiting provider: duplicate/concurrent requests cannot race through.
      seen.set(key,at+300000);rate.count++;calls++;active++;activeByUser.set(s.id,true);
      try{
        const result=await provider({prompt:input.prompt,requestId:input.request_id});
        if(!result||typeof result.text!=='string'||result.text.length>32000||!['completed','incomplete','refused'].includes(result.status))fail(502,'invalid_provider_result');
        send(res,200,{text:result.text,status:result.status,receipt:{request_id:input.request_id,observed_at:new Date(now()).toISOString(),kind:'provider_response',provider:'openai',provider_response_id:result.responseId??null,provider_request_id:result.providerRequestId??null,model:result.model??null,usage:result.usage??null,tools_executed:false,publication:false,cryptographic_attestation:false}});
      }finally{active--;activeByUser.delete(s.id);}
    }catch(error){const safe=error instanceof AdapterError;send(res,safe?error.status:502,{error:safe?error.code:'adapter_request_failed',request_id:requestId});}
  };
}
