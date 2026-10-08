#!/usr/bin/env python3
"""Reconcile source catalogs + bounded audit evidence into the æQR registry.
Offline and deterministic: availability never implies successful execution.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, quote, unquote
import argparse, hashlib, json, subprocess, xml.etree.ElementTree as ET
BASE='https://myaelmendez.github.io/'
GENERATED={'registry/index.html','registry/index.template.html'}
class Page(HTMLParser):
 def __init__(self):super().__init__();self.title='';self.intitle=False;self.refs=[];self.meta={};self.redirect=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='title':self.intitle=True
  if t=='meta':
   self.meta[a.get('name','')]=a.get('content','')
   if a.get('http-equiv','').lower()=='refresh':self.redirect=True
  for k in ['src','href','poster']:
   if k in a:self.refs.append((t,k,a[k]))
 def handle_endtag(self,t):
  if t=='title':self.intitle=False
 def handle_data(self,d):
  if self.intitle:self.title+=d

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def entry_id(kind,key):return kind+'-'+hashlib.sha256(key.encode()).hexdigest()[:16]
def resolve(root,url):
 p=root/unquote(urlsplit(url).path).lstrip('/')
 if p.is_dir():p=p/'index.html'
 return p

def build(root):
 source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
 audit=json.loads((root/'registry/evidence/page-audit.json').read_text());old={p['path']:p for p in audit['pages']}
 surfaces=json.loads((root/'surface-manifest.json').read_text())
 # The original catalog is kept as an input; the legacy manifest is a projection.
 source_catalog=root/'registry/source-surfaces.json'
 if source_catalog.exists():surfaces=json.loads(source_catalog.read_text())
 declared=json.loads((root/'.well-known/skills/index.json').read_text())
 mesh=json.loads((root/'skill-guide/capability-mesh.json').read_text())
 overrides=json.loads((root/'registry/overrides.json').read_text())
 entries=[];paths={}
 for p in sorted(root.rglob('*.html')):
  path=p.relative_to(root).as_posix()
  if '.git/'in path:continue
  if path in GENERATED:continue
  a=Page();text=p.read_text(errors='replace');a.feed(text);url=BASE+quote(path);h=digest(p);proof=old.get(path);matches=bool(proof and proof.get('source_sha256')==h)
  dependencies=[]
  for tag,attr,v in a.refs:
   if v.startswith(('#','data:','javascript:','mailto:','tel:')):continue
   target=urljoin(url,v);sp=urlsplit(target)
   if sp.scheme not in ['http','https']:continue
   if sp.netloc.lower()=='myaelmendez.github.io':
    exists=resolve(root,target).is_file();dependencies.append({'url':target,'role':'navigation'if tag=='a'else'asset','source_exists':exists,'availability':'source_present'if exists else'not_in_source'})
   elif tag!='a':dependencies.append({'url':target,'role':'external_asset','availability':'not_checked'})
  problems=[]
  if matches:
   problems.extend({'code':'js_syntax','detail':i['detail']}for i in proof['issues']if i['type']=='inline_js_syntax')
   problems.extend({'code':'broken_reference','url':r['url']}for r in audit['missing_references']if r['source']==path and r['http']['status']==404)
   problems.extend({'code':'missing_route','url':r['url']}for r in audit['literal_js_missing_targets']if r['source']==path and r['http']==404)
  o=overrides.get(path,{});purpose=o.get('purpose','yellow');kind=o.get('document_type','redirect'if a.redirect else'demo')
  e={'id':entry_id('page',path),'record_type':'surface','path':path,'name':a.title.strip()or path,'canonical_url':url,'purpose':purpose,'purpose_basis':o.get('basis','Discovery default; document type needs human classification.'),'document_type':kind,'dependencies':dependencies+[{'url':r['url'],'role':'backend_or_route','availability':'unavailable','http_status':404}for r in audit['literal_js_missing_targets']if matches and r['source']==path and r['http']==404],'authority':{'read':'public','execute':'human_approval','grants_authority':False},'source':{'revision':source_revision,'sha256':h},'verified_at':audit['audited_at']if matches else None,'availability':{'status':'available'if matches and proof['http']['status']==200 else'not_checked','http_status':proof['http']['status']if matches else None,'checked_at':audit['audited_at']if matches else None},'functional':{'status':'blocked'if problems else'not_verified','evidence':problems,'limits':['No browser execution or visual verification.','External dependency closure not checked.']},'capabilities':[],'skill_ids':[],'sitemap':kind!='embed'and path!='404.html'}
  entries.append(e);paths[path]=e
 # Preserve catalog declarations and point them at real source paths where possible.
 for surface in surfaces.get('surfaces',[]):
  u=urljoin(BASE,surface['url']);sp=urlsplit(u)
  if sp.netloc.lower()!='myaelmendez.github.io':continue
  p=resolve(root,u);path=p.relative_to(root).as_posix();e=paths.get(path)
  if not e:
   exists=p.is_file();e={'id':entry_id('resource',path),'record_type':'resource','path':path,'name':surface['name'],'canonical_url':u,'purpose':'yellow','purpose_basis':'Discovery of declared resource.','document_type':'spec','dependencies':[],'authority':{'read':'public','execute':'human_approval','grants_authority':False},'source':{'revision':source_revision,'sha256':digest(p)if exists else None},'verified_at':None,'availability':{'status':'source_present'if exists else'unavailable','http_status':None,'checked_at':None},'functional':{'status':'not_verified','evidence':[]},'capabilities':[],'skill_ids':[],'sitemap':False};entries.append(e);paths[path]=e
  e['legacy_surface_id']=surface['id'];e['capabilities']=surface.get('capabilities',[]);e['declared_agent_access']=surface.get('agent_access','read')
 # Skill cards address a registry detail, not fabricated on-site runtime endpoints.
 for source,records,kind in [('.well-known/skills/index.json',declared['items'],'declaration'),('skill-guide/capability-mesh.json',mesh['skills'],'skill')]:
  for item in records:
   key=item.get('id',item['name']);eid=entry_id(kind,source+':'+(item.get('cat','')+':'if kind=='skill'else'')+key)
   source_urls={k:v for k,v in item.items()if k.endswith('_url')or k=='skill_path'}
   e={'id':eid,'record_type':'skill'if kind=='skill'else item.get('type','skill'),'name':item.get('name',key),'canonical_url':BASE+'registry/#entry/'+eid,'purpose':'yellow','purpose_basis':'Discover a catalog declaration; execution is not verified.','document_type':'spec','dependencies':[{'role':'declared_runtime','tier':item.get('tier','unspecified'),'availability':'not_checked'}]if kind=='skill'else[],'authority':{'read':'public','execute':'human_approval','grants_authority':False},'source':{'catalog':source,'revision':source_revision,'catalog_generated_at':mesh.get('generated')if kind=='skill'else None,'references':source_urls},'verified_at':None,'availability':{'status':'not_checked','http_status':None,'checked_at':None},'functional':{'status':'not_verified','evidence':[]},'capabilities':item.get('stack',[]),'description':item.get('desc',item.get('description','')),'declared_status':item.get('status','catalogued'),'catalog_key':key,'category':item.get('cat'),'runtime_tier':item.get('tier'),'sitemap':False}
   entries.append(e)
   # Bind only exact reviewed relations. Similar names alone do not establish capability.
   for page,keys in overrides.get('_skill_bindings',{}).items():
    if key in keys and page in paths:paths[page]['skill_ids'].append(eid)
 # The generated catalog exists in source but awaits live verification.
 entries.append({'id':'aeqr-registry','record_type':'surface','path':'registry/index.html','name':'æQR · Skills, capabilities and kænbæn','canonical_url':BASE+'registry/','purpose':'yellow','purpose_basis':'Registry discovery and local work planning.','document_type':'tool','dependencies':[{'url':BASE+'registry/registry.json','role':'registry','availability':'source_present'},{'url':BASE+'assets/qrcode.js','role':'qr_encoder','availability':'source_present'}],'authority':{'read':'public','execute':'local_board_only','grants_authority':False},'source':{'revision':source_revision,'sha256':None,'generator':'scripts/build_aeqr_registry.py'},'verified_at':None,'availability':{'status':'not_checked','http_status':None,'checked_at':None},'functional':{'status':'not_verified','evidence':[]},'capabilities':['discover','qr-share','local-kanban'],'skill_ids':[e['id']for e in entries if e.get('catalog_key')in overrides.get('_skill_bindings',{}).get('registry/index.html',[])],'sitemap':True})
 ids=[e['id']for e in entries];assert len(ids)==len(set(ids));assert all(urlsplit(e['canonical_url']).scheme=='https'for e in entries)
 result={'schema_version':'1.0.0','namespace':'æææ.com','base_url':BASE,'source_revision':source_revision,'audit_revision':audit['source_revision'],'principle':'Context may propagate; authority does not.','purposes':{'yellow':'Discover','blue':'Engineer','green':'Govern'},'stores':declared.get('two_stores',{}),'kaizen':['audit','repair','verify','publish','audit'],'entries':entries}
 return result,surfaces

def write(root,result,surfaces):
 import html
 (root/'registry/registry.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 # Literal anchors remain navigable without JS, all derived from the registry.
 links='\n'.join('<li><a href="'+html.escape(e['canonical_url'],quote=True)+'">'+html.escape(e['name'])+'</a> <small>'+html.escape(e['functional']['status'])+'</small></li>'for e in result['entries']if e['record_type']=='surface')
 template=(root/'registry/index.template.html').read_text();(root/'registry/index.html').write_text(template.replace('<!-- REGISTRY_NAV -->',links))
 ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);sm=ET.Element('{'+ns+'}urlset')
 for url in sorted({e['canonical_url']for e in result['entries']if e['sitemap']}):
  node=ET.SubElement(sm,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=url
 ET.indent(sm);(root/'sitemap.xml').write_bytes(ET.tostring(sm,encoding='utf-8',xml_declaration=True))
 # Keep legacy consumers compatible, using the registry for all HTML surface URLs.
 projection=dict(surfaces);projection['version']='2.0.0';projection['registry']='/registry/registry.json';projection['description']='Compatibility projection of the æQR registry. Availability and functionality are separate; declared capabilities are not execution proof.'
 projection['categories']=surfaces.get('categories',[])+[{'id':k,'description':v}for k,v in result['purposes'].items()]
 projection['surfaces']=[{'id':e.get('legacy_surface_id',e['id']),'name':e['name'],'url':e['canonical_url'],'description':e.get('description',''),'category':next((s.get('category',e['purpose'])for s in surfaces.get('surfaces',[])if s['id']==e.get('legacy_surface_id')),e['purpose']),'capabilities':e['capabilities'],'agent_access':'read','registry_id':e['id'],'availability':e['availability']['status'],'functional_status':e['functional']['status'],'authority':e['authority']}for e in result['entries']if e['record_type']in ['surface','resource']]
 projection['surfaces'].extend({**s,'availability':'not_checked','functional_status':'not_verified'}for s in surfaces.get('surfaces',[])if s.get('external'))
 (root/'surface-manifest.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();r,s=build(args.root);write(args.root,r,s);print(f"{len(r['entries'])} registry entries; {sum(e['sitemap']for e in r['entries'])} sitemap destinations")
