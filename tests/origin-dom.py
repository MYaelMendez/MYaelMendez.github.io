"""Run actual scripts in Chromium with in-memory fixtures (no network).

Not a full HTTP/browser integration test. External fetches and browser storage
are replaced by explicit test doubles because navigation is restricted here.
"""
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'evidence'
OUT.mkdir(exist_ok=True)
html=(ROOT/'index.html').read_text()
html=re.sub(r'<link\b[^>]*>', '', html)
html=re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', html)
css=(ROOT/'origin-scene.css').read_text()+'\n'+(ROOT/'ae-origin.css').read_text()
html=html.replace('</head>','<base href="https://ae-preview.test/"><style>'+css+'</style></head>')
contract=json.loads((ROOT/'tests/fixtures/destinations.json').read_text())
manifest=json.loads((ROOT/'tests/fixtures/manifest.json').read_text())
records=[]
def check(name,condition):
    if not condition: raise AssertionError(name)
    records.append({'test':name,'result':'pass'})
def load(page, broken=False, preference=None):
    page.set_content(html)
    page.evaluate('''(data)=>{
      window.__requests=[]; window.__store=data.preference?{'ae-executor-preference-v1':data.preference}:{};
      Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>window.__store[k]||null,setItem:(k,v)=>{window.__store[k]=String(v)}}});
      window.fetch=async (url)=>{window.__requests.push(String(url));
        if(String(url).includes('ae-destinations')){if(data.broken)return {ok:false};return {ok:true,text:async()=>JSON.stringify(data.contract)};}
        if(String(url).includes('capability-manifest'))return {ok:true,text:async()=>JSON.stringify(data.manifest)};
        throw Error('Unexpected fixture request');
      };
      window.__downloads=[];
      URL.createObjectURL=(blob)=>{window.__downloads.push(blob);return 'blob:local-test'};
      URL.revokeObjectURL=()=>{};
      HTMLAnchorElement.prototype.click=function(){if(!this.download)throw Error('Unexpected navigation');};
    }''',{'contract':contract,'manifest':manifest,'broken':broken,'preference':preference})
    for name in ['tests/fixtures/atlas.js','ae-origin.js','ae-origin-ui.js','origin-console.js','webmcp.js']:
        page.add_script_tag(content=(ROOT/name).read_text())
    page.wait_for_function("!document.querySelector('#destination-state').textContent.includes('Checking')")
try:
  with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    for w,h in [(360,640),(390,844),(1440,900)]:
      context=browser.new_context(viewport={'width':w,'height':h},reduced_motion='reduce')
      context.route('**/*',lambda r:r.abort())
      page=context.new_page(); errors=[]
      page.on('pageerror',lambda e:errors.append(str(e)))
      load(page)
      check(f'{w} no startup error',not errors)
      check(f'{w} atlas source items and face preserved',page.locator('.door').count()==3 and page.locator('#glyph svg').count()==1)
      check(f'{w} no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
      check(f'{w} reduced motion',page.locator('html').get_attribute('data-motion')=='paused')
      check(f'{w} default ae preference',page.locator('#executor-choice').input_value()=='ae')
      def cmd(value):
        page.locator('#cmd').fill(value);page.locator('#cmd').press('Enter')
      cmd('$MCP')
      check(f'{w} MCP local origin without navigation',page.url=='about:blank' and page.locator('#origin-tab').get_attribute('aria-pressed')=='true')
      cmd('$\u2764\ufe0f')
      check(f'{w} heart selects human intention',page.locator('#human-intent').evaluate('(e)=>e===document.activeElement'))
      cmd('<img src=x onerror="window.__xss=1">')
      check(f'{w} text-only command output',page.locator('#log img').count()==0 and page.evaluate('window.__xss===undefined'))
      cmd('scan')
      check(f'{w} no invented verified chain', '0 external checks' in page.locator('#log').inner_text())
      page.locator('#human-intent').fill('PRIVATE-CANARY: not for export')
      page.locator('#executor-choice').select_option('codex')
      cmd('x0:y0:z:0:\u00e6:\u00e6:\u00e6')
      check(f'{w} public address selects review only',page.locator('#public-pane').is_visible() and page.locator('#public-export').is_disabled())
      page.locator('#public-label').fill('A public agency')
      page.locator('#public-preview').click()
      draft=json.loads(page.locator('#public-record').inner_text())
      check(f'{w} public projection excludes intention and authority','CANARY' not in json.dumps(draft) and draft['authority']['grant'] is None and not draft['publication']['deployment_authorized'])
      page.locator('#public-reviewed').check()
      page.locator('#public-label').fill('A changed public agency')
      check(f'{w} edit invalidates review',page.locator('#public-export').is_disabled() and not page.locator('#public-reviewed').is_checked())
      page.locator('#public-preview').click();page.locator('#public-reviewed').check();page.locator('#public-export').click()
      output=page.evaluate('async()=>await window.__downloads[0].text()')
      check(f'{w} actual generated Blob remains unprivileged draft','CANARY' not in output and json.loads(output)['execution']['preference']=='codex')
      check(f'{w} intention never saved or used in fetch URL','CANARY' not in page.evaluate('JSON.stringify(window.__store)') and not any('CANARY' in u for u in page.evaluate('window.__requests')))
      page.locator('#theme-toggle').click()
      check(f'{w} existing theme works',page.locator('html').get_attribute('data-theme')=='day')
      page.locator('#theme-toggle').click()
      page.locator('#glyph').press('Enter')
      check(f'{w} living face keyboard interaction works',page.locator('#glyph').get_attribute('aria-expanded')=='true')
      page.locator('#glyph').press('Enter');page.locator('#origin-tab').click()
      page.locator('#origin-clear').click()
      check(f'{w} private clear resets review',page.locator('#human-intent').input_value()=='' and page.locator('#public-export').is_disabled())
      page.screenshot(path=str(OUT/f'origin-{w}.png'),full_page=True)
      check(f'{w} full journey has no script errors',not errors)
      context.close()
    context=browser.new_context(viewport={'width':390,'height':844})
    context.route('**/*',lambda r:r.abort())
    page=context.new_page();load(page,broken=True)
    check('failed contract disables public preview and Site handoff',page.locator('#public-preview').is_disabled() and page.locator('#origin-site').is_hidden())
    context.close();browser.close()
finally:
 OUT.joinpath('dom-tests.json').write_text(json.dumps({'suite':'offline Chromium DOM with fetch/storage/download fixtures','count':len(records),'checks':records,'limits':['No HTTP integration (browser administrator blocks navigation)','No real Safari/device test','No real localStorage persistence or native file download tested','No production deployment, provider calls, or OpenAI Site test']},indent=2))
print(json.dumps({'passed':len(records),'viewports':['360x640','390x844','1440x900'],'mode':'in-memory fixtures'}))
