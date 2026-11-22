/* æ:// WebMCP layer — feature-detected registration of the homebase capability surface.
   Spec: W3C WebMCP. HTTPS / secure context required. Reads capability-manifest.json lazily.
   Current shape: registerTool. Legacy shapes (provideTools/provideContext) also supported. */
(function(){
  'use strict';
  var MC=null, shape='none';
  try{
    if(typeof navigator!=='undefined' && navigator.modelContext){MC=navigator.modelContext;}
    else if(typeof document!=='undefined' && document.modelContext){MC=document.modelContext;}
  }catch(e){}
  if(MC){
    if(typeof MC.registerTool==='function')shape='registerTool';
    else if(typeof MC.provideTools==='function')shape='provideTools';
    else if(typeof MC.provideContext==='function')shape='provideContext';
  }
  window.__aeWebmcp={available:!!MC,shape:shape,registered:false,tools:[]};
  if(!MC)return;

  var MANIFEST=null, CAPS=[], loadPromise=null;
  function ensure(){
    if(CAPS.length)return Promise.resolve();
    if(!loadPromise){loadPromise=fetch('capability-manifest.json',{cache:'no-cache'})
      .then(function(r){return r.json();})
      .then(function(M){MANIFEST=M;CAPS=M.capabilities||[];})
      .catch(function(e){console.warn('[æ://webmcp] manifest fetch failed',e);});}
    return loadPromise;
  }
  function text(o){return {content:[{type:'text',text:(typeof o==='string')?o:JSON.stringify(o,null,2)}]};}
  function fmt(c){return {address:c.address,name:c.name,id:c.id,url:c.url,category:c.category,layer:c.layer,layer_name:c.layer_name,capabilities:c.capabilities};}
  function find(q){q=String(q||'').toLowerCase();return CAPS.filter(function(c){return c.id===q||c.name.toLowerCase()===q||c.address===q||c.id.indexOf(q)>=0||c.name.toLowerCase().indexOf(q)>=0;})[0];}

  var TOOLS=[
    {name:'list_capabilities',
     description:'List every capability surface published at the æ:// homebase (myaelmendez.github.io). Returns {id,name,address,url,category,layer,layer_name,capabilities}. Optionally filter by authority layer (0 public, 1 published, 2 operator, 3 custody) or category.',
     inputSchema:{type:'object',properties:{layer:{type:'number',description:'authority layer 0-3'},category:{type:'string',description:'category id, e.g. secrets'}},required:[]},
     execute:function(a){a=a||{};return ensure().then(function(){return text(CAPS.filter(function(c){return (a.layer==null||c.layer===a.layer)&&(!a.category||c.category===a.category);}).map(fmt));});}},
    {name:'find_capability',
     description:'Discover æ:// capability surfaces by free-text query, matched against name, id, category, url and capability tags. Use to answer "does the homebase do X?".',
     inputSchema:{type:'object',properties:{query:{type:'string',description:'search text, e.g. cuda or vault'}},required:['query']},
     execute:function(a){var q=String((a&&a.query)||'').toLowerCase();return ensure().then(function(){return text(CAPS.filter(function(c){return c.id.indexOf(q)>=0||c.name.toLowerCase().indexOf(q)>=0||c.category.indexOf(q)>=0||c.url.toLowerCase().indexOf(q)>=0||(c.capabilities||[]).join(' ').indexOf(q)>=0;}).map(fmt));});}},
    {name:'open_surface',
     description:'Get the URL and address of a capability surface by id, name, or coordinate (x:y:z:æ). Navigates the page to it when same-origin.',
     inputSchema:{type:'object',properties:{id:{type:'string',description:'surface id, name, or coordinate'}},required:['id']},
     execute:function(a){return ensure().then(function(){var r=find(a&&a.id);if(!r)return text('no surface "'+((a&&a.id)||'')+'"');try{if(r.url&&r.url.charAt(0)==='/')location.href=r.url;}catch(e){}return text(fmt(r));});}},
    {name:'resolve_address',
     description:'Resolve a 4-space coordinate x:y:z:æ (x=category, y=item, z=depth, æ=authority) to the capability surface at that address.',
     inputSchema:{type:'object',properties:{address:{type:'string',description:'e.g. x10:y0:z0:æ3'}},required:['address']},
     execute:function(a){var m=String((a&&a.address)||'').match(/x?(-?\d+):y?(-?\d+):z?(-?\d+):æ?(-?\d+)/);if(!m)return Promise.resolve(text('bad address'));return ensure().then(function(){var r=CAPS.filter(function(c){var p=c.address.match(/x(-?\d+):y(-?\d+):z(-?\d+):æ(-?\d+)/);return p&&p[1]==m[1]&&p[2]==m[2]&&p[3]==m[3]&&p[4]==m[4];})[0];return text(r?fmt(r):'no surface at '+((a&&a.address)||''));});}},
    {name:'get_manifest',
     description:'Return the full æ:// capability manifest: homebase, operator, authority axis, and every capability surface.',
     inputSchema:{type:'object',properties:{},required:[]},
     execute:function(){return ensure().then(function(){return text(MANIFEST||{});});}},
    {name:'verify_chain',
     description:'Return the væult tool chain status — the eleven links vault→envelope→supervision→signing→pledge→kanban→push→alias→teach→transport→sms.',
     inputSchema:{type:'object',properties:{},required:[]},
     execute:function(){return Promise.resolve(text({chain:'væult',links:['vault','envelope','supervision','signing','pledge','kanban','push','alias','teach','transport','sms'],status:'11/11',note:'a thing not checked back is not a thing — verify with: python C:/æ/agents/væult_chain.py verify'}));}}
  ];

  function register(){
    try{
      if(shape==='registerTool'){TOOLS.forEach(function(t){try{MC.registerTool(t);}catch(e){}});}
      else if(shape==='provideTools'&&typeof MC.provideTools==='function'){MC.provideTools(TOOLS);}
      else if(shape==='provideContext'&&typeof MC.provideContext==='function'){MC.provideContext({tools:TOOLS});}
      window.__aeWebmcp.registered=true;
      window.__aeWebmcp.tools=TOOLS.map(function(t){return t.name;});
      console.log('[æ://webmcp] registered '+TOOLS.length+' tools via '+shape);
    }catch(e){console.warn('[æ://webmcp] register failed',e);}
  }
  register();
  ensure();
})();
