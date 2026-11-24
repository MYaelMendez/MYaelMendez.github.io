// tinyVOCA desktop dock — unified package half for Hermes Desktop.
// Loaded from $HERMES_HOME/plugins/tiny-voca-voice/desktop/plugin.js.
import {
  Button, Input, PALETTE_AREA, STATUSBAR_AREAS, StatusDot,
  host, useMutation, useQuery, useQueryClient
} from '@hermes/plugin-sdk'
import { useState } from 'react'
import { jsx, jsxs } from 'react/jsx-runtime'

const ID = 'tiny-voca-voice'
const VERSION = '1.3.1'
const VOICE_COLORS = { F2: 'var(--ui-accent)', M2: 'var(--ui-text-secondary)', ROBOT: 'var(--ui-text-tertiary)', 'SOVÆREIGN': 'var(--ui-accent)' }

function useIdentity(ctx) {
  return useQuery({
    queryKey: [ctx.source, 'identity'],
    queryFn: () => ctx.rest('/identity'),
    staleTime: 60000,
    refetchOnWindowFocus: false
  })
}

function useStatus(ctx) {
  return useQuery({
    queryKey: [ctx.source, 'status'],
    queryFn: () => ctx.rest('/status'),
    refetchInterval: 15000
  })
}

function IdentityRow({ id, binding }) {
  const color = VOICE_COLORS[id] || 'var(--ui-text-secondary)'
  return jsxs('div', {
    style: { borderBottom: '1px solid var(--ui-stroke-secondary)', padding: '8px 0' },
    children: [
      jsxs('div', { style: { display: 'flex', alignItems: 'center', gap: 8 }, children: [
        jsx(StatusDot, { tone: 'ok', size: 8 }),
        jsx('strong', { style: { color, fontSize: 12 }, children: id }),
        jsx('span', { style: { fontSize: 12, color: 'var(--ui-text-secondary)' }, children: binding.name })
      ] }),
      jsx('div', { style: { fontSize: 11, color: 'var(--ui-text-tertiary)' }, children: binding.compute_layer }),
      jsx('div', { style: { fontSize: 10, color: 'var(--ui-text-quaternary)' }, children: binding.runtime })
    ]
  })
}

export function TinyVocaPane({ ctx }) {
  const [text, setText] = useState('Human root to æ to receipt.')
  const [voice, setVoice] = useState('M2')
  const [speed, setSpeed] = useState(1.25)
  const qc = useQueryClient()
  const identity = useIdentity(ctx)
  const status = useStatus(ctx)
  const speak = useMutation({
    mutationFn: body => ctx.rest('/speak', { method: 'POST', body }),
    onSuccess: result => {
      host.notify({ kind: 'success', message: result?.receipt ? `tinyVOCA receipt ${result.receipt.slice(0, 12)}` : 'tinyVOCA spoke.' })
      qc.invalidateQueries({ queryKey: [ctx.source, 'status'] })
    },
    onError: err => host.notify({ kind: 'error', message: String(err?.message || err) })
  })
  const bindings = identity.data?.identity?.bindings || {}
  const layers = status.data?.compute_layers || identity.data?.identity?.compute_layers || {}

  return jsxs('div', {
    style: { display: 'flex', flexDirection: 'column', gap: 12, padding: 14, fontSize: 12, height: '100%', overflowY: 'auto' },
    children: [
      jsxs('div', { style: { display: 'flex', alignItems: 'center', justifyContent: 'space-between' }, children: [
        jsx('strong', { style: { fontSize: 14 }, children: '>_æ: tinyVOCA' }),
        jsx('span', { style: { color: 'var(--ui-text-quaternary)' }, children: VERSION })
      ] }),
      jsx('div', { style: { color: 'var(--ui-text-tertiary)' }, children: 'Local English TTS · CPU · 24 kHz · hash-chained receipts' }),
      jsx('div', { style: { color: status.data?.model_present ? 'var(--ui-accent)' : 'var(--ui-text-tertiary)' }, children: status.data?.model_present ? 'Weights present' : 'Weights not provisioned' }),
      jsx('div', { style: { display: 'flex', gap: 6, alignItems: 'center' }, children: [
        jsx(Input, { value: text, onChange: e => setText(e.target.value), placeholder: 'Text for tinyVOCA', style: { flex: 1 } }),
        jsx(Button, { type: 'button', size: 'sm', variant: 'ghost', onClick: () => { qc.invalidateQueries({ queryKey: [ctx.source, 'identity'] }); qc.invalidateQueries({ queryKey: [ctx.source, 'status'] }) }, children: 'Refresh' })
      ] }),
      jsxs('div', { style: { display: 'flex', gap: 6 }, children: [
        jsxs('select', {
          value: voice, onChange: e => setVoice(e.target.value),
          style: { background: 'transparent', color: 'var(--ui-text-secondary)', border: '1px solid var(--ui-stroke-secondary)', borderRadius: 4, padding: '4px 6px' },
          children: ['M2', 'F2', 'ROBOT', 'SOVÆREIGN'].map(v => jsx('option', { value: v, children: v }, v))
        }),
        jsxs('select', {
          value: String(speed), onChange: e => setSpeed(Number(e.target.value)),
          style: { background: 'transparent', color: 'var(--ui-text-secondary)', border: '1px solid var(--ui-stroke-secondary)', borderRadius: 4, padding: '4px 6px' },
          children: [1, 1.25, 1.5, 1.8].map(v => jsx('option', { value: String(v), children: `${v}×` }, v))
        }),
        jsx(Button, {
          type: 'button', size: 'sm', disabled: speak.isPending,
          onClick: () => speak.mutate({ text, voice, speed }),
          children: speak.isPending ? 'Speaking…' : 'Speak'
        })
      ] }),
      speak.data?.success && jsx('div', { style: { color: 'var(--ui-accent)', fontSize: 11 }, children: `receipt ${String(speak.data.receipt || '').slice(0, 16)} · ${speak.data.output}` }),
      speak.error && jsx('div', { style: { color: 'var(--ui-text-secondary)', fontSize: 11 }, children: String(speak.error?.message || speak.error) }),
      jsx('div', { style: { fontWeight: 600, marginTop: 4 }, children: 'Voice → compute layer' }),
      jsxs('div', { children: Object.entries(bindings).map(([id, binding]) => jsx(IdentityRow, { id, binding }, id)) }),
      jsx('div', { style: { color: 'var(--ui-text-tertiary)', fontSize: 11, marginTop: 8 }, children: 'HUMAN://ROOT → æ → RECEIPT · authority not transferable' })
    ]
  })
}

export function TinyVocaStatus({ ctx }) {
  const status = useStatus(ctx)
  return jsx(Button, {
    type: 'button', variant: 'ghost', size: 'sm',
    title: 'tinyVOCA local voice',
    onClick: () => host.notify({ kind: 'info', message: `tinyVOCA ${VERSION} · ${status.data?.model_present ? 'weights present' : 'weights missing'}` }),
    children: jsxs('span', { style: { display: 'flex', alignItems: 'center', gap: 5 }, children: [
      jsx(StatusDot, { tone: status.data?.model_present ? 'ok' : 'warning', size: 7 }),
      'tinyVOCA'
    ] })
  })
}

export default {
  id: ID,
  name: 'tinyVOCA Voice Dock',
  description: 'Local tiny-voca voices docked beside the conversation with a scoped speech backend.',
  defaultEnabled: false,
  register(ctx) {
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: 'tinyVOCA',
      data: { placement: 'right', dock: { pane: 'workspace', pos: 'right' }, width: '300px' },
      render: () => jsx(TinyVocaPane, { ctx })
    })
    ctx.register({
      id: 'status',
      area: STATUSBAR_AREAS.right,
      order: 140,
      render: () => jsx(TinyVocaStatus, { ctx })
    })
    ctx.register({
      id: 'palette',
      area: PALETTE_AREA,
      data: {
        id: 'tiny-voca.status',
        label: 'tinyVOCA: local voice status',
        keywords: ['tinyvoca', 'tiny voca', 'tts', 'voice', 'nous girl', 'hermes agent'],
        run: () => host.notify({ kind: 'info', message: `tinyVOCA ${VERSION} docked. Open the tinyVOCA pane for voices and receipts.` })
      }
    })
  }
}
