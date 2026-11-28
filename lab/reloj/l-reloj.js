/* L:// reloj · Latin American world clock for the Instituto Luterano Latinoamericano.
   <l-reloj></l-reloj>  · attrs: zones="America/Chicago|Texas (sede),America/Guatemala|Guatemala" event="2026-10-20T08:30:00-05:00|Asamblea"
   No external assets. Uses Intl only. */
(()=>{
const DEF=[["America/Chicago","Texas · sede","🇺🇸"],["America/Mexico_City","México","🇲🇽"],["America/Guatemala","Guatemala","🇬🇹"],["America/El_Salvador","El Salvador","🇸🇻"],["America/Managua","Nicaragua","🇳🇮"],["America/Costa_Rica","Costa Rica","🇨🇷"],["America/Bogota","Colombia","🇨🇴"],["America/Lima","Perú","🇵🇪"]];
const off=(tz,d)=>{const p=new Intl.DateTimeFormat("en-US",{timeZone:tz,timeZoneName:"shortOffset"}).formatToParts(d).find(x=>x.type==="timeZoneName").value.replace("GMT","");return p||"+0"};
const hr=(tz,d)=>+new Intl.DateTimeFormat("en-US",{timeZone:tz,hour:"numeric",hourCycle:"h23"}).format(d);
class LReloj extends HTMLElement{
 connectedCallback(){
  const z=this.getAttribute("zones");this.Z=z?z.split(",").map(s=>{const[a,b,c]=s.split("|");return[a,b||a,c||""]}):DEF;
  const ev=this.getAttribute("event");this.E=ev?ev.split("|"):null;this.L=this.getAttribute("lang")||((document.documentElement.lang||"es").slice(0,2));
  this.attachShadow({mode:"open"}).innerHTML=`<style>
:host{display:block;font:15px/1.4 system-ui,-apple-system,sans-serif;color:var(--ink,#151515)}
.w{border:1px solid var(--bd,#d6ccb6);border-radius:16px;background:var(--fl,#fffaf0);overflow:hidden}
.h{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;font:600 12px ui-monospace,Menlo,monospace;letter-spacing:.12em;color:var(--c,#1f4fa3);text-transform:uppercase}
ul{list-style:none;margin:0;padding:0}
li{display:grid;grid-template-columns:1.6em 1fr auto auto;gap:8px;align-items:center;padding:9px 14px;border-top:1px solid var(--bd,#d6ccb6);min-height:44px}
li.s{background:color-mix(in srgb,var(--c,#1f4fa3) 10%,transparent)}li.s .n{font-weight:700}
.t{font:700 20px ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums}
.o{font:12px ui-monospace,Menlo,monospace;color:var(--dim,#5a554b);min-width:4.2em;text-align:right}
.d{font-size:12px;color:var(--dim,#5a554b)}
.e span{white-space:nowrap}.e{padding:10px 14px;border-top:1px solid var(--bd,#d6ccb6);font:600 13px ui-monospace,Menlo,monospace;color:var(--c,#1f4fa3)}
</style><div class="w" role="group" aria-label="Reloj latinoamericano"><div class="h"><span>L:// reloj LATAM</span><span id="d"></span></div><ul id="u"></ul><div class="e" id="e" hidden></div></div>`;
  this.tick();this.t=setInterval(()=>this.tick(),1000*15);
 }
 disconnectedCallback(){clearInterval(this.t)}
 tick(){
  const d=new Date(),R=this.shadowRoot,loc=this.L==="en"?"en-US":"es-MX";
  R.getElementById("d").textContent=new Intl.DateTimeFormat(loc,{timeZone:this.Z[0][0],weekday:"short",day:"numeric",month:"short"}).format(d);
  const base=new Intl.DateTimeFormat("en-CA",{timeZone:this.Z[0][0]}).format(d);
  R.getElementById("u").innerHTML=this.Z.map(([tz,n,f],i)=>{
   const h=hr(tz,d),day=new Intl.DateTimeFormat("en-CA",{timeZone:tz}).format(d),dd=day>base?(this.L==="en"?"tomorrow":"mañana"):day<base?(this.L==="en"?"yesterday":"ayer"):"";
   const t=new Intl.DateTimeFormat(loc,{timeZone:tz,hour:"numeric",minute:"2-digit"}).format(d);
   return `<li class="${i?"":"s"}"><span aria-hidden="true">${h>=6&&h<19?"☀️":"🌙"}</span><span class="n">${f} ${n}${dd?` <span class="d">· ${dd}</span>`:""}</span><span class="t">${t}</span><span class="o">UTC${off(tz,d)}</span></li>`}).join("");
  const e=R.getElementById("e");
  if(this.E){const at=new Date(this.E[0]),ms=at-d;e.hidden=false;
   if(ms>0){const hh=Math.floor(ms/36e5),mm=Math.floor(ms%36e5/6e4);e.innerHTML=`<span>⏳ ${this.E[1]||"Evento"}</span> · <span>${this.L==="en"?"in":"en"} ${hh} h ${mm} min</span><br>`+this.Z.map(([tz,n])=>`<span>${n.split(" ·")[0]} ${new Intl.DateTimeFormat(loc,{timeZone:tz,hour:"numeric",minute:"2-digit"}).format(at)}</span>`).slice(0,3).join(" · ")}
   else if(ms>-2*36e5)e.textContent=`🔴 ${this.E[1]||"Evento"} · ${this.L==="en"?"live now":"en vivo ahora"}`;else e.hidden=true}
 }
}
customElements.get("l-reloj")||customElements.define("l-reloj",LReloj);
})();
