"""Offline Chromium smoke tests of the changed root page.

Uses small, labeled fixtures for unchanged atlas/manifest/peer-contract responses.
Does not test external destinations, OAuth, live WebMCP, publishing, or providers.
Run: python tests/origin-browser.py --chromium /usr/bin/chromium
Requires the Playwright Python package and an installed Chromium executable.
"""
from __future__ import annotations
import argparse
import functools
import http.server
import json
import threading
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT.parent / 'evidence'
EVIDENCE.mkdir(exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        redirects = {
            '/ae-atlas.js': '/tests/fixtures/atlas.js',
            '/ae-destinations.json': '/tests/fixtures/destinations.json',
            '/capability-manifest.json': '/tests/fixtures/manifest.json',
        }
        self.path = redirects.get(self.path, self.path)
        super().do_GET()
    def log_message(self, *_):
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    args = parser.parse_args()
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    records = []
    def record(label, condition):
        if not condition:
            raise AssertionError(label)
        records.append({'test': label, 'result': 'pass'})
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=args.chromium, headless=True, args=['--no-sandbox'])
            for width, height in [(360, 640), (390, 844), (1440, 900)]:
                context = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion='reduce', accept_downloads=True)
                # No external provider traffic, not even Google Fonts, in this suite.
                context.route('**/*', lambda route: route.continue_() if urlparse(route.request.url).hostname == '127.0.0.1' else route.abort())
                page = context.new_page()
                errors, requests = [], []
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.on('request', lambda r: requests.append(r.url))
                page.goto(base)
                page.wait_for_function("document.getElementById('destination-state').textContent.includes('contract checked')")
                record(f'{width}: boots without JavaScript errors', not errors)
                record(f'{width}: preserves living face and atlas', page.locator('#glyph svg').count() == 1 and page.locator('.mesh .door').count() == 3)
                record(f'{width}: no horizontal document overflow', page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
                record(f'{width}: reduced motion honored', page.locator('html').get_attribute('data-motion') == 'paused')
                record(f'{width}: principal intention default; runtime unverified', page.locator('#executor-choice').input_value() == 'ae' and 'not verified' in page.locator('#destination-state').inner_text())
                def command(value):
                    page.locator('#cmd').fill(value)
                    page.locator('#cmd').press('Enter')
                command('$MCP')
                record(f'{width}: MCP stays on origin without redirect', page.url == base and page.locator('#origin-tab').get_attribute('aria-pressed') == 'true')
                command('$\u2764\ufe0f')
                record(f'{width}: heart focuses human intention', page.locator('#human-intent').evaluate('(e)=>e===document.activeElement'))
                command('<img src=x onerror="window.__injected=1">')
                record(f'{width}: command injection rendered only as text', page.locator('#log img').count() == 0 and page.evaluate('window.__injected === undefined'))
                command('scan')
                record(f'{width}: no fabricated chain verification', '0 external checks' in page.locator('#log').inner_text())
                page.locator('#human-intent').fill('PRIVATE-INTENT-CANARY: never publish this')
                page.locator('#executor-choice').select_option('codex')
                command('x0:y0:z:0:\u00e6:\u00e6:\u00e6')
                record(f'{width}: exact public address opens review, not publication', page.locator('#public-pane').is_visible() and page.locator('#public-export').is_disabled())
                page.locator('#public-label').fill('Public demo agency')
                page.locator('#public-preview').click()
                proposal = json.loads(page.locator('#public-record').inner_text())
                record(f'{width}: public projection excludes private intent and authority', 'CANARY' not in json.dumps(proposal) and proposal['authority']['grant'] is None and proposal['publication']['deployment_authorized'] is False)
                record(f'{width}: review mandatory before export', page.locator('#public-export').is_disabled())
                page.locator('#public-reviewed').check()
                page.locator('#public-label').fill('Edited public agency')
                record(f'{width}: changing reviewed data invalidates approval', page.locator('#public-export').is_disabled() and not page.locator('#public-reviewed').is_checked())
                page.locator('#public-preview').click()
                page.locator('#public-reviewed').check()
                with page.expect_download() as info:
                    page.locator('#public-export').click()
                download = info.value
                target = EVIDENCE / f'public-draft-{width}.json'
                download.save_as(target)
                exported = json.loads(target.read_text())
                record(f'{width}: export is draft, not external witness', not exported['witness']['external_success'] and exported['execution']['preference'] == 'codex')
                record(f'{width}: private intention absent from storage and request URLs', 'CANARY' not in page.evaluate('JSON.stringify(localStorage)') and not any('CANARY' in u for u in requests))
                page.locator('#theme-toggle').click()
                record(f'{width}: existing theme control works', page.locator('html').get_attribute('data-theme') == 'day')
                page.locator('#theme-toggle').click()
                page.locator('#glyph').press('Enter')
                record(f'{width}: announcements keyboard control works', page.locator('#glyph').get_attribute('aria-expanded') == 'true')
                page.locator('#glyph').press('Enter')
                page.locator('#origin-tab').click()
                page.screenshot(path=str(EVIDENCE / f'origin-{width}.png'), full_page=True)
                record(f'{width}: no runtime errors after full journey', not errors)
                page.reload()
                page.wait_for_function("document.getElementById('destination-state').textContent.includes('contract checked')")
                record(f'{width}: only preference survives reload; private intention does not', page.locator('#executor-choice').input_value() == 'codex' and page.locator('#human-intent').input_value() == '')
                page.goto(base + '#x0%3Ay0%3Az%3A0%3A%C3%A6%3A%C3%A6%3A%C3%A6')
                page.wait_for_selector('#public-pane', state='visible')
                record(f'{width}: shared public address remains a review state', page.locator('#public-export').is_disabled())
                context.close()
            for scenario in ('invalid', 'missing'):
                context = browser.new_context(viewport={'width':390,'height':844})
                context.route('**/*', lambda route: route.continue_() if urlparse(route.request.url).hostname == '127.0.0.1' else route.abort())
                if scenario == 'invalid':
                    data = json.loads((ROOT/'tests/fixtures/destinations.json').read_text())
                    data['authority']['inherit'] = True
                    context.route('**/ae-destinations.json', lambda r: r.fulfill(json=data))
                else:
                    context.route('**/ae-destinations.json', lambda r: r.fulfill(status=503, body='unavailable'))
                page = context.new_page()
                page.goto(base)
                page.wait_for_function("document.getElementById('destination-state').textContent.includes('unavailable or invalid')")
                record(f'{scenario} contract: fails closed without changing destinations', page.locator('#public-preview').is_disabled() and page.locator('#origin-site').is_hidden())
                context.close()
            browser.close()
    finally:
        server.shutdown()
        report = {'suite':'local Chromium with fixtures','tests':records,'count':len(records),'limits':['No production deployment','No external destination validation','No physical iPhone or Safari test','No live WebMCP host, authentication, or provider test']}
        (EVIDENCE/'browser-tests.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({'passed':len(records),'fixtures':True,'viewports':['360x640','390x844','1440x900']}))

if __name__ == '__main__':
    main()
