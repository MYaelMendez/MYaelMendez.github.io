import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'

const plugin = await readFile(new URL('../desktop/plugin.js', import.meta.url), 'utf8')
const manifest = JSON.parse(await readFile(new URL('../dashboard/manifest.json', import.meta.url), 'utf8'))
const api = await readFile(new URL('../dashboard/plugin_api.py', import.meta.url), 'utf8')

test('desktop plugin is an opt-in unified package half', () => {
  assert.match(plugin, /const ID = 'tiny-voca-voice'/)
  assert.match(plugin, /id: ID/)
  assert.match(plugin, /defaultEnabled: false/)
  assert.match(plugin, /area: 'panes'/)
  assert.match(plugin, /area: STATUSBAR_AREAS\.right/)
  assert.match(plugin, /area: PALETTE_AREA/)
})

test('desktop plugin only imports allowed modules', () => {
  const specifiers = [...plugin.matchAll(/from\s+'([^']+)'/g)].map(m => m[1])
  assert.deepEqual(specifiers.sort(), ['@hermes/plugin-sdk', 'react', 'react/jsx-runtime'])
})

test('desktop plugin uses only scoped backend routes', () => {
  for (const route of ["/identity", "/status", "/speak"]) {
    assert.ok(plugin.includes(`ctx.rest('${route}'`), `missing ctx.rest(${route})`)
  }
  assert.doesNotMatch(plugin, /fetch\(|XMLHttpRequest|window\.fetch/)
})

test('desktop plugin uses theme variables and no hardcoded UI colors', () => {
  assert.doesNotMatch(plugin, /#[0-9a-fA-F]{3,8}\b|rgb\(|rgba\(/)
  assert.match(plugin, /var\(--ui-text-secondary\)/)
  assert.match(plugin, /var\(--ui-stroke-secondary\)/)
})

test('backend manifest and routes match the unified package', () => {
  assert.deepEqual(manifest, { name: 'tiny-voca-voice', api: 'plugin_api.py' })
  assert.match(api, /router = APIRouter\(\)/)
  for (const route of ['/status', '/identity', '/speak']) {
    assert.ok(api.includes(`@router.${route === '/speak' ? 'post' : 'get'}("${route}")`), `missing ${route}`)
  }
  assert.match(api, /HUMAN:\/\/ROOT/)
})

test('backend keeps heavy TTS imports out of module scope', () => {
  assert.doesNotMatch(api, /^import (numpy|onnxruntime|dizione)/m)
  assert.doesNotMatch(api, /^from (numpy|onnxruntime|dizione)/m)
})
