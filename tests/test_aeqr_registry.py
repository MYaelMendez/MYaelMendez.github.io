import importlib.util, unittest, tempfile, json, hashlib
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('registry_builder',ROOT/'scripts/build_aeqr_registry.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
class RegistryTests(unittest.TestCase):
 def fixture(self,root):
  for d in ['registry/evidence','.well-known/skills','skill-guide']:(root/d).mkdir(parents=True,exist_ok=True)
  (root/'sample.html').write_text('<title>Sample</title><script>broken js</script>')
  proof={'path':'sample.html','source_sha256':hashlib.sha256((root/'sample.html').read_bytes()).hexdigest(),'http':{'status':200},'issues':[{'type':'inline_js_syntax','detail':'invalid JS'}]}
  data={'registry/evidence/page-audit.json':{'source_revision':'base','audited_at':'2026-10-08T00:00:00Z','pages':[proof],'missing_references':[],'literal_js_missing_targets':[]},'surface-manifest.json':{'surfaces':[]},'.well-known/skills/index.json':{'items':[]},'skill-guide/capability-mesh.json':{'skills':[{'name':'same','cat':'one'},{'name':'same','cat':'two'}]},'registry/overrides.json':{}}
  for p,j in data.items():(root/p).write_text(json.dumps(j))
 def test_available_is_not_functional(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);self.fixture(root)
   with patch.object(builder.subprocess,'check_output',return_value='base'):r,_=builder.build(root)
   e=next(e for e in r['entries']if e.get('path')=='sample.html');self.assertEqual(e['availability']['status'],'available');self.assertEqual(e['functional']['status'],'blocked')
 def test_modified_source_invalidates_evidence(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);self.fixture(root);(root/'sample.html').write_text('<title>Repaired</title>')
   with patch.object(builder.subprocess,'check_output',return_value='base'):r,_=builder.build(root)
   e=next(e for e in r['entries']if e.get('path')=='sample.html');self.assertEqual(e['availability']['status'],'not_checked');self.assertIsNone(e['verified_at']);self.assertEqual(e['functional']['status'],'not_verified')
 def test_skill_identity_includes_category(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);self.fixture(root)
   with patch.object(builder.subprocess,'check_output',return_value='base'):r,_=builder.build(root)
   ids=[e['id']for e in r['entries']if e['record_type']=='skill'];self.assertEqual(len(ids),len(set(ids)))
 def test_generated_navigation_and_sitemap_use_registry(self):
  import xml.etree.ElementTree as ET
  r=json.loads((ROOT/'registry/registry.json').read_text());urls={e['canonical_url']for e in r['entries']if e['sitemap']}
  actual={n.text for n in ET.parse(ROOT/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')};self.assertEqual(urls,actual)
  nav=(ROOT/'registry/index.html').read_text()
  for e in r['entries']:
   if e['record_type']=='surface':self.assertIn(e['canonical_url'],nav)
if __name__=='__main__':unittest.main()
