/* Refactored living origin. All controls stay local until a human follows a link. */
(function(){'use strict';
// Function declaration is available BEFORE theme controls use it (fixes root boot).
function $(id){return document.getElementById(id);}
var A=window.AEOrigin;if(!A||!$('cmd'))return;
var ATLAS=Array.isArray(window.AE_ATLAS)?window.AE_ATLAS.filter(function(s){return s&&typeof s.id==='string'&&typeof s.name==='string'&&typeof s.cat==='string'&&A.safeURL(s.url,document.baseURI)&&[s.x,s.y,s.z,s.a].every(Number.isInteger)&&s.a>=0&&s.a<=3;}):[];
var AXCOL=['var(--gold)','var(--cyan)','var(--neon)','var(--purple)'],AXNAME=['public','published','operator','custody'];
var S={x:0,y:0,z:0,a:0},TLOG=[],TCOORD='',tickOffset=0;
function paused(){return window.aeMotionPaused?window.aeMotionPaused():document.hidden||matchMedia('(prefers-reduced-motion: reduce)').matches;}
function log(text,cls){var span=document.createElement('span');span.className=['ok','g','c'].includes(cls)?cls:'';span.textContent=String(text)+'\n';$('log').append(span);while($('log').childNodes.length>120)$('log').firstChild.remove();$('log').scrollTop=$('log').scrollHeight;}
function coordOf(s){return 'x'+s.x+':y'+s.y+':z'+s.z+':\u00e6'+s.a;}
function atCoord(){return ATLAS.find(function(s){return ['x','y','z','a'].every(function(k){return s[k]===S[k];});})||null;}
function tickRender(){
 var values=[[TCOORD,'coord']].concat(TLOG);$('tstream').replaceChildren();
 for(var copy=0;copy<2;copy++){var g=document.createElement('span');g.className='tgrp';if(copy)g.setAttribute('aria-hidden','true');values.forEach(function(v){var s=document.createElement('span');s.className='tm '+(['coord','ok','g','c','p'].includes(v[1])?v[1]:'');s.textContent=v[0];g.append(s);});$('tstream').append(g);}
}
function tickPush(msg,cls){TLOG.push([String(msg),cls||'']);if(TLOG.length>12)TLOG.shift();tickRender();}
function render(){
 ['x','y','z'].forEach(function(k){$('c'+k).textContent=String(S[k]);});$('ca').textContent=String(S.a);
 var hit=atCoord();$('where').textContent=hit?hit.name+' / '+AXNAME[hit.a]+' navigation layer':coordOf(S)+' / navigation only';
 TCOORD=coordOf(S)+(hit?' / '+hit.name:' / origin map');tickRender();
}
function setHash(){history.replaceState(null,'','#'+encodeURIComponent(coordOf(S)));}
function parseHash(){
 var text;try{text=decodeURIComponent(location.hash.slice(1));}catch(_){log('Invalid encoded address.','c');return;}
 if(!text)return;var entry=A.resolve(text);if(entry&&window.AEOriginUI&&window.AEOriginUI.handle(entry))return;
 var state=A.parseCoordinate(text);if(state){S=state;render();}
}
function proposeURL(s){var safe=A.safeURL(s.url,document.baseURI);if(!safe){log('Blocked unsafe destination.','c');return;}var link=document.createElement('a');link.href=safe;link.textContent='Open '+s.name+' \u2197';if(new URL(safe).origin!==location.origin){link.target='_blank';link.rel='noopener noreferrer';}$('log').append(link,document.createTextNode('\n'));$('log').scrollTop=$('log').scrollHeight;}
function resolveSurface(q){
 q=q.toLowerCase().replace(/^(?:\u00e6|\u00e6\u00e6\u00e6|ae):\/\//,'');if(!q)return null;
 var c=A.parseCoordinate(q);if(c)return ATLAS.find(function(s){return ['x','y','z','a'].every(function(k){return s[k]===c[k];});})||null;
 return ATLAS.find(function(s){return s.id===q||s.name.toLowerCase()===q;})||ATLAS.find(function(s){return [s.id,s.name,s.cat].some(function(v){return v.toLowerCase().includes(q);});})||null;
}
function buildMesh(){
 $('mesh').replaceChildren();ATLAS.slice().sort(function(a,b){return a.a-b.a||a.x-b.x||a.y-b.y||a.z-b.z;}).forEach(function(s){
 var link=document.createElement('a');link.className='door';link.style.setProperty('--ac',AXCOL[s.a]);link.href=A.safeURL(s.url,document.baseURI);
 var ax=document.createElement('span');ax.className='ax';ax.textContent=coordOf(s);var b=document.createElement('b');b.textContent=s.name;var d=document.createElement('small');d.textContent=String(s.desc||'');link.append(ax,b,d);
 link.addEventListener('click',function(){S={x:s.x,y:s.y,z:s.z,a:s.a};render();});$('mesh').append(link);
 });$('meshstate').textContent=ATLAS.length+' source addresses';
}
function run(raw){
 var c=A.normalize(raw);if(!c){log('Enter a command of at most 256 characters without hidden control characters.','c');return;}
 log('> '+String(raw).trim(),'g');
 var entry=A.resolve(raw);if(entry){if(entry.kind==='atlas'){c='atlas';}else if(window.AEOriginUI&&window.AEOriginUI.handle(entry)){log('Local '+entry.kind+' selected. No authority granted.','c');return;}}
 if(c==='help'){['$ae / $mcp / &mcp / $\u00e6: one local origin',' $\u2764\ufe0f: human intention, not a health-only workflow','origin / public: local preparation or public review','atlas / $\ud83d\uddfa\ufe0f: list source addresses','goto x9:y0:z0:\u00e60: move; layers never grant permissions','scan / verify: report evidence limits, not simulated success','A surface name proposes a link. Select it to navigate.'].forEach(function(s){log(s,'c');});}
 else if(c==='atlas'||c==='ls'){ATLAS.forEach(function(s){log('  '+coordOf(s)+'  '+s.name);});}
 else if(c==='scan'||c==='verify'){var w=window.__aeWebmcp;log('Atlas: '+ATLAS.length+' source entries. Destinations not probed.','c');log('Chain verification: '+A.chainReport().status+'; 0 external checks.','c');log('WebMCP: '+(w&&w.registered?w.tools.length+' tools accepted by detected host':'not registered in this host')+'.','c');tickPush('source inspection only / no external verification','c');}
 else if(c==='whoami'){log('Human principal is required. Identity is not authenticated by this page.','c');}
 else if(c.startsWith('goto ')){var state=A.parseCoordinate(c.slice(5));if(state){S=state;render();setHash();log('Moved to '+coordOf(S)+'; permissions unchanged.','c');}else log('Invalid coordinate. Use x/y/z integers -999..999 and layer 0..3.','c');}
 else{var hit=resolveSurface(c);if(hit){S={x:hit.x,y:hit.y,z:hit.z,a:hit.a};render();setHash();log('Source match: '+hit.name+'; not a live capability test.','c');proposeURL(hit);}else log('No bound entry. Try help or atlas. Plugin execution is not inferred from a symbol.','c');}
}
var theme='night',env='default';try{theme=localStorage.getItem('ae-theme')==='day'?'day':'night';env=localStorage.getItem('ae-env')==='agentic_environments'?'agentic_environments':'default';}catch(_){}
function applyTheme(){document.documentElement.dataset.theme=theme;document.querySelector('meta[name=theme-color]').content=theme==='day'?'#f5f2ea':'#050505';try{localStorage.setItem('ae-theme',theme);}catch(_){}}
function applyEnv(){document.documentElement.dataset.env=env;try{localStorage.setItem('ae-env',env);}catch(_){}}
applyTheme();applyEnv();$('theme-toggle').addEventListener('click',function(){theme=theme==='night'?'day':'night';applyTheme();tickPush('theme: '+theme);});$('env-toggle').addEventListener('click',function(){env=env==='default'?'agentic_environments':'default';applyEnv();tickPush('appearance: '+env);});
function submit(){var raw=$('cmd').value;$('cmd').value='';run(raw);}
$('go').addEventListener('click',submit);$('cmd').addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();submit();}});
document.addEventListener('keydown',function(e){
 if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();$('cmd').focus();return;}
 var t=e.target;if(e.metaKey||e.ctrlKey||e.altKey||t&&(t.isContentEditable||t.closest('input,textarea,select,button,a,[role=button]')))return;
 var k=e.key.toLowerCase(),action={a:['x',-1],arrowleft:['x',-1],d:['x',1],arrowright:['x',1],w:['y',1],arrowup:['y',1],s:['y',-1],arrowdown:['y',-1],q:['z',-1],e:['z',1],z:['a',-1],x:['a',1]}[k];
 if(!action)return;e.preventDefault();S[action[0]]=Math.max(action[0]==='a'?0:-999,Math.min(action[0]==='a'?3:999,S[action[0]]+action[1]));render();setHash();
});
window.addEventListener('hashchange',parseHash);
// Existing living-face interactions, keyboard-accessible and motion-aware.
var g=$('glyph'),cta=$('cta'),tr=$('cta-track');
var announcements=['Private Client / explore','One principal. Many agents.','Where the loop returns value to the human.'];
for(var c=0;c<2;c++){var group=document.createElement('span');group.className='h';if(c)group.setAttribute('aria-hidden','true');announcements.forEach(function(text){var a=document.createElement('a');a.href='https://privateclient.ai';a.target='_blank';a.rel='noopener noreferrer';a.textContent=text;if(c)a.tabIndex=-1;group.append(a);});tr.append(group);}
function toggle(){var on=cta.classList.toggle('grown');g.setAttribute('aria-expanded',String(on));}
g.addEventListener('click',toggle);g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}});
var rt;function react(){if(paused())return;g.classList.add('react');clearTimeout(rt);rt=setTimeout(function(){g.classList.remove('react');},640);}
new MutationObserver(react).observe($('log'),{childList:true,subtree:true});
function dock(){var r=$('cmd').getBoundingClientRect(),b=g.getBoundingClientRect();g.dataset.dockDx=String(Math.round(r.left-b.right));g.dataset.dockOk=b.left<=r.left&&Math.abs(b.top+b.height/2-r.top-r.height/2)<16?'1':'0';}
window.addEventListener('resize',dock);window.aeGlyph={dock:dock,react:react,state:function(){return {docked:g.classList.contains('docked'),left:g.getBoundingClientRect().left,cmdLeft:$('cmd').getBoundingClientRect().left};}};
window.addEventListener('mousemove',function(e){if(paused())return;var r=g.getBoundingClientRect(),dx=(e.clientX-r.left-r.width/2)/Math.max(r.width,1),dy=(e.clientY-r.top-r.height/2)/Math.max(r.height,1),len=Math.max(1,Math.hypot(dx,dy));var t='translate('+(dx/len*3.4).toFixed(2)+','+(dy/len*3.4).toFixed(2)+')';$('eyeL').setAttribute('transform',t);$('eyeR').setAttribute('transform',t);},{passive:true});
document.addEventListener('mouseleave',function(){$('eyeL').removeAttribute('transform');$('eyeR').removeAttribute('transform');});
// Pause JS motion as well as CSS, including when the tab is hidden.
var canvas=$('grid'),ctx=canvas.getContext('2d'),frame=0,lastTime=0;
function fit(){var dpr=Math.min(2,devicePixelRatio||1);canvas.width=innerWidth*dpr;canvas.height=innerHeight*dpr;if(ctx)ctx.setTransform(dpr,0,0,dpr,0,0);draw();dock();}
function draw(){if(!ctx)return;var w=innerWidth,h=innerHeight,hy=h*.46,cs=getComputedStyle(document.documentElement);ctx.clearRect(0,0,w,h);ctx.strokeStyle=cs.getPropertyValue('--grid-neon');ctx.lineWidth=1;for(var i=-12;i<=12;i++){ctx.beginPath();ctx.moveTo(w/2+i*46,hy);ctx.lineTo(w/2+i*220,h);ctx.stroke();}for(var j=0;j<14;j++){var y=hy+(h-hy)*j/14+(frame%60)*.4;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}ctx.strokeStyle=cs.getPropertyValue('--grid-gold');ctx.beginPath();ctx.moveTo(w/2,0);ctx.lineTo(w/2,h);ctx.stroke();}
window.addEventListener('resize',fit);new MutationObserver(draw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme','data-env']});
function animate(t){if(!paused()&&t-lastTime>32){frame+=.4;draw();tickOffset-=.4;var half=$('tstream').scrollWidth/2;if(half>0&&-tickOffset>=half)tickOffset+=half;$('tstream').style.transform='translateX('+tickOffset+'px)';lastTime=t;}requestAnimationFrame(animate);}
render();buildMesh();fit();requestAnimationFrame(animate);parseHash();
log('Open Sovereign / origin initialized.','g');log(ATLAS.length+' atlas source entries; connections not verified.','c');log('Context may propagate; authority does not.','c');log('Type help, $mcp, $\u2764\ufe0f or public.');
tickPush('origin loaded / no external authority','c');tickPush('map layers do not grant access','g');
var abort=new AbortController(),timer=setTimeout(function(){abort.abort();},10000);
fetch('./capability-manifest.json',{cache:'no-cache',credentials:'omit',referrerPolicy:'no-referrer',signal:abort.signal}).then(function(r){if(!r.ok)throw Error('manifest unavailable');return r.text();}).then(function(text){if(text.length>200000)throw Error('manifest too large');var m=JSON.parse(text);if(!m||!Array.isArray(m.capabilities))throw Error('manifest invalid');tickPush(m.capabilities.length+' capability descriptions / source only','c');}).catch(function(){tickPush('capability manifest unavailable / no verified counts','c');}).finally(function(){clearTimeout(timer);});
window.travel=function(event,id){var s=ATLAS.find(function(x){return x.id===id;});if(!s)return false;S={x:s.x,y:s.y,z:s.z,a:s.a};render();return true;};
})();
