import {readFile,readdir} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
const base=path.resolve(import.meta.dirname,'..');
async function walk(dir){const out=[];for(const e of await readdir(dir,{withFileTypes:true})){if(e.name==='node_modules')continue;const p=path.join(dir,e.name);if(e.isDirectory())out.push(...await walk(p));else if(p.endsWith('.mjs'))out.push(p);}return out;}
for(const file of await walk(base)){const r=spawnSync(process.execPath,['--check',file],{encoding:'utf8'});if(r.status!==0){console.error(r.stderr);process.exit(1);}}
const html=await readFile(path.join(base,'index.html'),'utf8');
for(const match of html.matchAll(/(?:src|href)="(?!#|https?:)([^"]+)"/g))await readFile(path.join(base,match[1]));
for(const file of ['index.html','garden.mjs','model.mjs','garden.css']){
  const s=await readFile(path.join(base,file),'utf8');
  if(/sk-[A-Za-z0-9_-]{20,}|eval\s*\(|innerHTML|api\.openai\.com/.test(s))throw Error('Forbidden client pattern in '+file);
}
console.log('Syntax, relative assets and client-boundary source checks passed.');
