// Optional ambient projection, adapted from cockpit/cockpit.js. No task state in the GPU.
export function mountGlass(canvas,button,status){
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');let paused=reduced.matches,frameId=null,gl;
  const label=()=>{button.textContent=paused?'Resume ambient motion':'Pause ambient motion';button.setAttribute('aria-pressed',String(paused));};label();
  try{gl=canvas.getContext('webgl',{alpha:false,antialias:false});if(!gl)throw Error('WebGL unavailable');
    const compile=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error('Shader compilation failed');return s;};
    const vertex='attribute vec2 position;void main(){gl_Position=vec4(position,0.,1.);}';
    const fragment='precision mediump float;uniform vec2 resolution;uniform float time;void main(){vec2 uv=gl_FragCoord.xy/resolution;vec2 p=uv-.5;p.x*=resolution.x/resolution.y;float d=length(p);float ripple=.5+.5*sin(d*27.-time*.7);float glow=exp(-d*4.)*(.04+.035*ripple);float grid=pow(max(0.,sin(p.x*50.)*sin(p.y*50.)),14.)*.03;vec3 c=vec3(.035,.043,.06)+vec3(.92,.69,.26)*(glow+grid);gl_FragColor=vec4(c,1.);}';
    const program=gl.createProgram();gl.attachShader(program,compile(gl.VERTEX_SHADER,vertex));gl.attachShader(program,compile(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error('Shader link failed');gl.useProgram(program);
    const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
    const a=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,2,gl.FLOAT,false,0,0);const resolution=gl.getUniformLocation(program,'resolution'),time=gl.getUniformLocation(program,'time');
    function draw(t){frameId=null;if(document.hidden)return;const d=Math.min(devicePixelRatio||1,2),w=Math.max(1,Math.floor(canvas.clientWidth*d)),h=Math.max(1,Math.floor(canvas.clientHeight*d));if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h);}gl.uniform2f(resolution,w,h);gl.uniform1f(time,paused?0:t/1000);gl.drawArrays(gl.TRIANGLES,0,6);if(!paused)frameId=requestAnimationFrame(draw);}
    const refresh=()=>{if(frameId!==null)cancelAnimationFrame(frameId);frameId=null;if(!document.hidden)frameId=requestAnimationFrame(draw);};
    button.onclick=()=>{paused=!paused;label();refresh();};reduced.addEventListener('change',e=>{paused=e.matches;label();refresh();});document.addEventListener('visibilitychange',refresh);window.addEventListener('resize',refresh);canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();if(frameId!==null)cancelAnimationFrame(frameId);button.disabled=true;status.textContent='WebGL context lost. Static glass and all local tools remain available.';});
    status.textContent='WebGL ambient background initialized. Workspaces remain accessible HTML controls, not isolated runtimes.';refresh();
  }catch{canvas.hidden=true;button.hidden=true;status.textContent='WebGL unavailable. Static glass and all local tools remain available.';}
}
