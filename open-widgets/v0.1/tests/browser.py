"""Optional browser regression suite. Requires Python playwright + Chromium.
Runs a loopback server with the OpenAI adapter disabled; live upstream is never used.
"""
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import time
import urllib.request
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get('AE_TEST_OUTPUT', str(ROOT / 'test-results')))
OUT.mkdir(parents=True, exist_ok=True)
PORT = '4173'
OFFLINE = os.environ.get('AE_BROWSER_OFFLINE') == '1'
BASE = 'https://mow-garden.test' if OFFLINE else 'http://127.0.0.1:' + PORT
server = None if OFFLINE else subprocess.Popen(['node', 'server/dev-server.mjs'], cwd=ROOT,
    env={**os.environ, 'PORT': PORT, 'AE_OPENAI_ENABLED': 'false'},
    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
checks = []
def mount(context):
    pass

def load_page(page):
    if not OFFLINE:
        page.goto(BASE)
        return
    # No URL navigation: admin policy in some runners disables it. Test DOM only
    # with exact CSS and flattened local modules; HTTP behavior has Node tests.
    html=(ROOT/'index.html').read_text()
    html=re.sub(r'<link rel="stylesheet"[^>]+>', '', html)
    html=re.sub(r'<script type="module"[^>]+></script>', '', html)
    page.set_content(html)
    page.add_style_tag(content=(ROOT/'garden.css').read_text())
    model=(ROOT/'model.mjs').read_text().replace('export ', '')
    app=(ROOT/'garden.mjs').read_text().split('\n',1)[1]
    page.add_script_tag(type='module',content=model+'\n'+app)
    page.evaluate("""() => {
      window.fetch=async()=>new Response(JSON.stringify({error:'adapter_disabled'}),{status:503,headers:{'Content-Type':'application/json'}});
      if(!crypto.randomUUID)crypto.randomUUID=()=> '11111111-1111-4111-8111-111111111111';
    }""")

try:
    for _ in range(0 if OFFLINE else 60):
        try:
            urllib.request.urlopen(BASE, timeout=1).close()
            break
        except Exception:
            time.sleep(0.1)
    with sync_playwright() as p:
        chromium = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
        browser = p.chromium.launch(**({'executable_path': chromium} if chromium else {}),
            headless=True, args=['--no-sandbox'])
        for label, width, height in [('mobile',390,844),('narrow',320,700),('landscape',844,390),('desktop',1440,1000)]:
            context = browser.new_context(viewport={'width':width,'height':height}, reduced_motion='reduce', accept_downloads=True)
            mount(context)
            page = context.new_page()
            errors, external = [], []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('request', lambda r: external.append(r.url) if not r.url.startswith(BASE) else None)
            load_page(page)
            expect(page.locator('.scene')).to_have_count(4)
            expect(page.locator('.widget')).to_have_count(12)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), label + ': document overflow'
            box = page.locator('.scene').first.bounding_box()
            assert abs(box['width']/box['height']-9/16)<0.01, label + ': scene ratio'
            page.screenshot(path=str(OUT / (label+'.png')), full_page=True)
            note=page.locator('.scene[data-scene="garden"] textarea').first
            note.fill('PRIVATE-NOTE-KEEP-OUT-OF-EXPORT')
            page.locator('#next').click()
            expect(page.locator('#scene-counter')).to_have_text('2 / 4')
            page.locator('#previous').click()
            expect(note).to_have_value('PRIVATE-NOTE-KEEP-OUT-OF-EXPORT')
            first=page.locator('.scene[data-scene="garden"] .widget').first
            first.locator('select').first.select_option('counter')
            first.get_by_role('button', name='+ Nest', exact=True).first.click()
            expect(page.locator('.scene[data-scene="garden"] .children .widget')).to_have_count(1)
            child=page.locator('.scene[data-scene="garden"] .children .widget').first
            child.get_by_role('button',name='+',exact=True).click()
            expect(child.locator('output')).to_have_text('1')
            child.get_by_role('button',name='Focus',exact=True).click()
            expect(page.locator('#focus-dialog')).to_be_visible()
            expect(page.locator('#focus-host output')).to_have_text('1')
            page.locator('#focus-host').get_by_role('button',name='+',exact=True).click()
            page.keyboard.press('Escape')
            expect(child.locator('output')).to_have_text('2')
            first.get_by_role('button',name='Fork',exact=True).first.click()
            garden=page.locator('.scene[data-scene="garden"]')
            notes=garden.locator('textarea')
            expect(notes).to_have_count(2)
            expect(notes.nth(1)).to_have_value('')
            garden.locator('.drawer-host > .widget').nth(1).get_by_role('button',name='Retire',exact=True).first.click()
            page.locator('#regrow').click()
            expect(garden.locator('textarea').nth(1)).to_have_value('')
            page.locator('#review').click()
            preview=page.locator('#export-preview').inner_text()
            assert 'PRIVATE-NOTE' not in preview
            data=json.loads(preview)
            assert data['private_state_included'] is False and data['authority']['grant'] is None
            expect(page.locator('#download')).to_be_disabled()
            page.locator('#export-consent').check()
            with page.expect_download() as event:
                page.locator('#download').click()
            exported=json.loads(Path(event.value.path()).read_text())
            assert exported==data
            page.locator('#close-export').click()
            page.locator('#intention').fill('<img src=x onerror="alert(1)">')
            page.locator('#seed').click()
            expect(page.locator('#seed-output img')).to_have_count(0)
            page.locator('.api-drawer summary').click()
            page.locator('#check-adapter').click()
            expect(page.locator('#api-status')).to_contain_text('unavailable, disabled, or unauthenticated')
            expect(page.locator('#ask')).to_be_disabled()
            expect(page.locator('#api-consent')).to_be_disabled()
            assert not errors, (label,errors)
            assert not external, (label,external)
            checks.append({'viewport':label,'size':[width,height],'result':'pass','transport':'offline DOM, flattened local modules' if OFFLINE else 'loopback HTTP','page_errors':errors,'external_requests':external})
            context.close()
        # Client-to-adapter interaction is tested with browser-local fixtures only.
        context=browser.new_context(viewport={'width':1200,'height':900})
        mount(context)
        page=context.new_page()
        load_page(page)
        page.route('**/api/ae/session',lambda route:route.fulfill(json={'ready':True,'csrf_token':'a'*43,'expires_at':int(time.time()*1000)+60000}))
        sent=[]
        def respond(route):
            sent.append(route.request.post_data_json)
            assert route.request.headers['x-ae-csrf']=='a'*43
            route.fulfill(json={'text':'<b>Text, not executable HTML</b>','status':'completed','receipt':{'request_id':'test-browser'}})
        page.route('**/api/ae/respond',respond)
        if OFFLINE:
            page.evaluate("""() => {
              window.testSent=[];
              window.fetch=async(url,options)=> {
                if(url.endsWith('/session'))return new Response(JSON.stringify({ready:true,csrf_token:'a'.repeat(43),expires_at:Date.now()+60000}),{headers:{'Content-Type':'application/json'}});
                window.testSent.push(JSON.parse(options.body));
                return new Response(JSON.stringify({text:'<b>Text, not executable HTML</b>',status:'completed',receipt:{request_id:'test-browser'}}),{headers:{'Content-Type':'application/json'}});
              };
            }""")
        page.locator('.api-drawer summary').click()
        page.locator('#check-adapter').click()
        expect(page.locator('#api-consent')).to_be_enabled()
        page.locator('#intention').fill('Build a local garden')
        page.locator('#api-consent').check()
        page.locator('#intention').fill('Build a local classroom')
        expect(page.locator('#api-consent')).not_to_be_checked()
        page.locator('#api-consent').check()
        page.locator('#ask').click()
        expect(page.locator('#ai-output')).to_have_text('<b>Text, not executable HTML</b>')
        expect(page.locator('#ai-output b')).to_have_count(0)
        expect(page.locator('#api-consent')).not_to_be_checked()
        if OFFLINE: sent=page.evaluate('window.testSent')
        assert len(sent)==1 and set(sent[0])=={'request_id','prompt','approved'}
        checks.append({'client_adapter':'mocked session, single approved request, safe output, approval reset','result':'pass'})
        browser.close()
    (OUT/'browser-results.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))
finally:
    if server:
        server.terminate()
        try: server.wait(timeout=5)
        except subprocess.TimeoutExpired: server.kill()
