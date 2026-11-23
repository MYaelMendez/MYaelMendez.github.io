import {AdapterError} from './adapter.mjs';
const ENDPOINT='https://api.openai.com/v1/responses';
const identifier=v=>typeof v==='string'&&/^[A-Za-z0-9._:-]{1,160}$/.test(v)?v:null;
function usage(v){if(!v)return null;const out={};for(const k of ['input_tokens','output_tokens','total_tokens'])if(Number.isSafeInteger(v[k])&&v[k]>=0)out[k]=v[k];return out;}
/** Server-only, fixed-destination, text-only Responses API adapter. */
export function createOpenAIProvider({apiKey,model,maxOutputTokens=768,timeoutMs=25000,fetchImpl=globalThis.fetch}={}){
  if(typeof apiKey!=='string'||!apiKey.trim()||/[\r\n]/.test(apiKey))throw Error('Server API key required');
  if(typeof model!=='string'||!/^[a-zA-Z0-9._:-]{1,120}$/.test(model))throw Error('Explicit server model required');
  if(!Number.isSafeInteger(maxOutputTokens)||maxOutputTokens<16||maxOutputTokens>2048)throw Error('Output limit must be 16-2048');
  if(!Number.isSafeInteger(timeoutMs)||timeoutMs<1||timeoutMs>30000)throw Error('Bounded timeout required');
  return async function respond({prompt}){
    let response;
    try{
      response=await fetchImpl(ENDPOINT,{method:'POST',redirect:'error',signal:AbortSignal.timeout(timeoutMs),headers:{Authorization:`Bearer ${apiKey}`,'Content-Type':'application/json'},body:JSON.stringify({model,input:[{role:'user',content:prompt}],instructions:'Help the human plan a composable widget environment. Return plain text. Do not claim to have sent messages, connected agents, executed code, published, or changed accounts. No tools are available.',max_output_tokens:maxOutputTokens,tools:[],tool_choice:'none',store:false,stream:false})});
      if(!response.ok){await response.body?.cancel();throw new AdapterError(502,'openai_request_failed');}
      const reader=response.body?.getReader();if(!reader)throw new AdapterError(502,'openai_response_invalid');
      let size=0,chunks=[];while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>1048576){await reader.cancel();throw new AdapterError(502,'openai_response_too_large');}chunks.push(value);}
      const all=new Uint8Array(size);let offset=0;for(const c of chunks){all.set(c,offset);offset+=c.length;}
      const data=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(all));
      if(!['completed','incomplete'].includes(data.status)||!Array.isArray(data.output))throw new AdapterError(502,'openai_response_invalid');
      let parts=[],refused=false;
      for(const item of data.output){if(item.type!=='message'||item.role!=='assistant'||!Array.isArray(item.content))continue;for(const c of item.content){if(c.type==='output_text'&&typeof c.text==='string')parts.push(c.text);if(c.type==='refusal'&&typeof c.refusal==='string'){refused=true;parts.push(c.refusal);}}}
      const text=parts.join('\n');if(!text||text.length>32000)throw new AdapterError(502,'openai_no_usable_text');
      return {text,status:refused?'refused':data.status,responseId:identifier(data.id),providerRequestId:identifier(response.headers.get('x-request-id')),model:identifier(data.model)||model,usage:usage(data.usage)};
    }catch(e){if(e instanceof AdapterError)throw e;throw new AdapterError(e?.name==='TimeoutError'||e?.name==='AbortError'?504:502,'openai_unavailable');}
  };
}
