"""hermes-ae 3.18.0 — one self-contained, receipted MoH orchestrator.

`ae` dispatches to the registered tools of all local plugins by loading their
modules with a lightweight FakeCtx, then writes a single HUMAN://ROOT
hash-chained receipt for every action. No heavy imports at registration.
"""
import json, hashlib, importlib.util, subprocess, os, shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / 'scripts'
HARNESSES = ROOT / 'harnesses.json'
HERMES_HOME = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
PY = os.environ.get('HERMES_AE_PYTHON', '/usr/local/bin/python3')
PLUGINS = Path(os.environ.get('HERMES_AE_PLUGINS', HERMES_HOME / 'plugins'))
LEDGER = Path(os.environ.get('HERMES_AE_LEDGER', HERMES_HOME / 'ae-receipts.jsonl'))
ANIM = Path(os.environ.get('HERMES_AE_ANIM', HERMES_HOME / 'ae' / 'asimov-anim'))
GALLERY = Path(os.environ.get('HERMES_AE_GALLERY', HERMES_HOME / 'ae' / 'gallery'))

# op -> (plugin, tool). Use op="call" with plugin/tool for anything else.
SHORTCUTS = {
    'speak':        ('tiny-voca-voice', 'tts_speak'),
    'voices':       ('tiny-voca-voice', 'tts_voices'),
    'render':       ('ffmpeg-agentic', 'ffmpeg_render'),
    'probe':        ('ffmpeg-agentic', 'ffmpeg_probe'),
    'gallery':      ('ffmpeg-agentic', 'video_gallery'),
    'witness':      ('ffmpeg-agentic', 'ffmpeg_witness'),
    'vlc':          ('vlc-mesh', 'vlc_media'),
    'nodes':        ('vlc-mesh', 'vlc_nodes'),
    'vlc_receipts': ('vlc-mesh', 'vlc_receipts'),
    'robot_say':    ('hermes-asimov', 'asimov_say'),
    'robot_status': ('hermes-asimov', 'asimov_status'),
    'robot_video':  ('hermes-asimov', 'asimov_voice_video'),
    'studio_video': ('hermes-asimov', 'asimov_studio_video'),
    'studio':       ('mujoco-studio', 'studio_shoot'),
    'physics':      ('mujoco-studio', 'studio_physics'),
    'studio_status':('mujoco-studio', 'studio_status'),
    'studio_sync':  ('mujoco-studio', 'studio_sync'),
    'studio_publish':('mujoco-studio', 'studio_publish'),
    'robot_voice':  ('robotVOICE', 'robot_speak'),
    'face_states':  ('robotVOICE', 'robot_face_states'),
    'chimera_speak':('chimera-voice', 'chimera_speak'),
    'chimera_sing': ('chimera-voice', 'chimera_sing'),
    'ae_command':   ('ae-c2', 'ae_command'),
    'ae_status':    ('ae-c2', 'ae_status'),
}

_cache = {}

# Bundled orchestrators — run in-process scripts, not legacy plugins.
LOCAL_OPS = {
    'studio_video': ('studio_video.py', 1500),
    'free_walk': ('free_walk_video.py', 1500),
    'masterpiece': ('masterpiece_video.py', 1800),
    'asimov_agent': ('asimov_agent_video.py', 1500),
    'ffmpeg_demo': ('ffmpeg_harness_demo.py', 1500),
    'policy_locomotion': ('policy_locomotion.py', 1500),
    'policy_walk': ('policy_walk_video.py', 1500),
    'viewport_dom': ('viewport_dom.py', 120),
    'projection_render': ('sovereign_projection.py', 1500),
    'tv_episode': ('tv_episode.py', 1500),
}


def _run_local(script, args, timeout):
    path = SCRIPTS / script
    if not path.exists():
        return {'success': False, 'error': f'bundled script missing: {path}'}
    try:
        p = subprocess.run([PY, str(path), json.dumps(args)], capture_output=True,
                           text=True, timeout=timeout)
        if p.returncode != 0:
            return {'success': False, 'error': (p.stderr or p.stdout)[-1000:]}
        return json.loads(p.stdout.strip().splitlines()[-1])
    except Exception as e:
        return {'success': False, 'error': f'{type(e).__name__}: {e}'}


LOCAL_FUNCS = {
    'speak': 'Generate speech with the bundled tiny-voca CLI.',
    'tts_speak': 'Alias of speak — tiny-voca as a Hermes TTS primitive.',
    'voices': 'List bundled TTS voices.',
    'tts_voices': 'Alias of voices — list tiny-voca voices.',
    'tts_receipts': 'List tiny-voca speech receipts from the unified ledger.',
    'probe': 'Probe a media file with ffprobe.',
    'witness': 'List video/sha256 receipts from the unified ledger.',
    'gallery': 'Regenerate the video gallery from files on disk.',
    'physics': 'Step the synced MuJoCo model (supports legacy=true).',
    'studio_sync': 'Verify bundled model, runtime, and receipt hashes.',
    'harnesses': 'List the Mixture of Harnesses registry.',
    'harness': 'Inspect one named harness.',
    'run_harness': 'Run a light harness chain (no video pipelines).',
    'agent_body': 'Show the Asimov = hermes-agent build identity binding.',
    'agent': 'Show the unified Asimov Agent identity and runtime state.',
    'projection': 'Inspect the sovereign projection package.',
    'head': 'Native Asimov head viewport: mask state, tiny-voca fallback, Pi500 teleop.',
    'face': 'Legacy alias of head — native Asimov head viewport.',
    'head_dom': 'Read-only DOM projection for the native Asimov head viewport.',
    'twin': 'Asimov USD digital twin: build/verify/info from official URDF + qpos.',
    'policy': 'æ Policy: show/verify/evaluate the machine-readable authority policy.',
    'daobrain': 'DAO Brain: policy-gated proposals driving the native Asimov head viewport.',
    'verbs': 'æ Robot Verbs: list/plan/execute governed wrappers over official Menlo SDK verbs.',
    'ffmpeg': 'Probe the ffmpeg media harness runtime.',
}


def _cmd(cmd, timeout=300):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        return {'success': False, 'error': (p.stderr or p.stdout or 'command failed')[-1000:]}
    try:
        return json.loads(p.stdout.strip())
    except Exception:
        try:
            return json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:
            return {'success': False, 'error': 'non-JSON output', 'raw': p.stdout[-400:]}


def _sha_file(path):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except Exception:
        return None


def _ffmpeg_harness(args):
    """Governed ffmpeg harness probe: version, encoders, and runtime readiness."""
    try:
        v = subprocess.run(['ffmpeg','-hide_banner','-version'],capture_output=True,text=True,timeout=20)
        p = subprocess.run(['ffprobe','-hide_banner','-version'],capture_output=True,text=True,timeout=20)
        e = subprocess.run(['ffmpeg','-hide_banner','-encoders'],capture_output=True,text=True,timeout=20)
    except Exception as exc:
        return {'success': False, 'error': str(exc), 'authority': 'HUMAN://ROOT'}
    enc = (e.stdout or e.stderr)
    encoders = {'libx264': 'libx264' in enc, 'aac': ' aac ' in enc or 'aac ' in enc}
    ok = v.returncode == 0 and p.returncode == 0 and all(encoders.values())
    return {'success': ok, 'authority': 'HUMAN://ROOT',
            'ffmpeg_version': (v.stdout or '').splitlines()[0] if v.stdout else None,
            'ffprobe_version': (p.stdout or '').splitlines()[0] if p.stdout else None,
            'encoders': encoders,
            'receipt_action': 'VIDEO://RENDER'}

def _asimov_agent(args):
    """Unified Asimov Agent identity and runtime state."""
    ident_path = ROOT / 'identity.json'
    if not ident_path.exists():
        return {'success': False, 'error': 'identity.json missing'}
    ident = json.loads(ident_path.read_text())
    agent = dict(ident.get('agent', {}))
    chain = _verify_chain()
    registry = json.loads(HARNESSES.read_text()) if HARNESSES.exists() else {'harnesses': []}
    package = ROOT / 'packages' / 'ae-locomotion' / '1.0.0' / 'manifest.json'
    pkg = json.loads(package.read_text()) if package.exists() else {}
    phys = ROOT / 'model' / 'xml' / 'asimov_1_25dof_physics.xml'
    policy = ROOT / 'model' / 'xml' / 'asimov_1_policy_physics.xml'
    urdf = ROOT / 'model' / 'urdf' / 'asimov_1_25dof.urdf'
    capabilities = {
        'tts': (SCRIPTS / 'tiny_voca_voice.py').exists(),
        'video': any((SCRIPTS / s).exists() for s in ('masterpiece_video.py', 'ffmpeg_harness_demo.py')),
        'physics': (SCRIPTS / 'physics.py').exists(),
        'onnx_locomotion': (SCRIPTS / 'policy_locomotion.py').exists() and bool(pkg),
        'qpos_viewport': (ROOT / 'webgl' / 'qpos_viewer.html').exists(),
        'viewport_dom': (SCRIPTS / 'viewport_dom.py').exists(),
        'head_viewport': (SCRIPTS / 'head_viewport.py').exists(),
        'head_dom': (SCRIPTS / 'viewport_dom.py').exists(),
        'publish': (SCRIPTS / 'publish_docs.py').exists(),
        'receipts': chain.get('success', False),
    }
    return {'success': True, 'authority': 'HUMAN://ROOT', 'agent': agent,
            'voice': ident.get('bindings', {}).get('M2'),
            'body': ident.get('actor'),
            'harnesses': [h['name'] for h in registry.get('harnesses', [])],
            'policy': {'name': pkg.get('policy', {}).get('name'), 'sha256': pkg.get('policy', {}).get('sha256'),
                       'verified': pkg.get('verified')},
            'model_sha256': {'physics': _sha_file(phys), 'policy_physics': _sha_file(policy), 'urdf': _sha_file(urdf)},
            'capabilities': capabilities,
            'ledger': {'success': chain.get('success', False), 'count': chain.get('count'), 'head': chain.get('head')},
            'receipt_action': 'AGENT://ASIMOV'}

def _projection(args):
    """Inspect the sovereign projection package and its first principles."""
    pkg = ROOT / 'packages' / 'sovereign-projection' / '1.0.0'
    if not pkg.exists():
        return {'success': False, 'error': 'projection package missing'}
    manifest = json.loads((pkg / 'manifest.json').read_text())
    assets = pkg / 'assets'
    return {'success': True, 'authority': 'HUMAN://ROOT', 'manifest': manifest,
            'assets': sorted(p.name for p in assets.iterdir()) if assets.exists() else [],
            'receipt_action': 'PROJECTION://'}

def _local_func(op, args):
    try:
        if op in ('speak', 'tts_speak'):
            text = args.get('text', '')
            if not text:
                return {'success': False, 'error': 'text is required'}
            out = args.get('output', str(ANIM / 'ae-speech.wav'))
            ANIM.mkdir(parents=True, exist_ok=True)
            r = _cmd([PY, str(SCRIPTS / 'tiny_voca_voice.py'), '--text', text,
                      '--voice', args.get('voice', 'M2'), '--output', out], timeout=300)
            return r if r.get('success') else {'success': False, 'error': r.get('error'), 'raw': r}
        if op in ('voices', 'tts_voices'):
            return {'success': True, 'voices': [
                {'id': 'F2', 'name': 'nous girl', 'aliases': ['nous-girl', 'nous girl', 'nous_girl'],
                 'language': 'en-US', 'sample_rate': 24000},
                {'id': 'M2', 'name': 'hermes-agent', 'aliases': ['hermes-agent', 'hermes agent', 'hermes_agent'],
                 'language': 'en-US', 'sample_rate': 24000}]}
        if op == 'probe':
            path = args.get('output') or args.get('path')
            if not path or not Path(path).exists():
                return {'success': False, 'error': 'existing output/path is required'}
            return _cmd(['ffprobe', '-v', 'error', '-show_entries',
                         'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames',
                         '-show_entries', 'format=duration,size', '-of', 'json', str(path)])
        if op in ('witness', 'tts_receipts'):
            lines = [json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()] if LEDGER.exists() else []
            needle = 'TTS' if op == 'tts_receipts' else 'VIDEO'
            hits = [e for e in lines if needle in str(e.get('action', '')).upper()]
            return {'success': True, 'count': len(hits),
                    'receipts': hits[-int(args.get('limit') or 10):]}
        if op == 'gallery':
            if not GALLERY.exists():
                return {'success': False, 'error': f'gallery repo missing: {GALLERY}'}
            env = dict(os.environ, HERMES_AE_GALLERY=str(GALLERY))
            p = subprocess.run([PY, str(SCRIPTS / 'generate_gallery.py')], capture_output=True,
                               text=True, timeout=180, env=env)
            if p.returncode != 0:
                return {'success': False, 'error': (p.stderr or p.stdout)[-1000:]}
            return json.loads(p.stdout.strip().splitlines()[-1])
        if op == 'physics':
            cmd = [PY, str(SCRIPTS / 'physics.py'), str(args.get('steps') or 500)]
            if args.get('legacy'):
                cmd.append('--legacy')
            return _cmd(cmd, timeout=180)
        if op == 'studio_sync':
            model = ROOT / 'model'
            paths = {
                'original': model / 'xml' / 'asimov_1_25dof.xml',
                'actuated': model / 'xml' / 'asimov_1_25dof_actuated.xml',
                'physics': model / 'xml' / 'asimov_1_25dof_physics.xml',
                'mocap': model / 'xml' / 'asimov_mocap_physics.xml',
                'urdf': model / 'urdf' / 'asimov_1_25dof.urdf',
            }
            hashes = {k: _sha_file(v) for k, v in paths.items()}
            vids = {}
            for name in ('asimov-studio-v2-916.mp4', 'asimov-free-walk-916.mp4'):
                f = ANIM / name
                vids[name] = {'sha256': _sha_file(f), 'bytes': f.stat().st_size if f.exists() else 0}
            chain = _verify_chain()
            ok = all(hashes.values()) and chain['success']
            return {'success': ok, 'authority': 'HUMAN://ROOT', 'version': '3.18.0',
                    'model_sha256': hashes, 'videos': vids, 'receipts': chain}
        if op == 'verify':
            return _verify_chain()
        if op == 'agent':
            return _asimov_agent(args)
        if op == 'projection':
            return _projection(args)
        if op == 'ffmpeg':
            return _ffmpeg_harness(args)
        if op == 'twin':
            return _run_local('asimov_twin.py', args, 300)
        if op == 'policy':
            return _run_local('ae_policy.py', args, 300)
        if op == 'daobrain':
            return _run_local('daobrain.py', args, 300)
        if op == 'verbs':
            return _run_local('ae_verbs.py', args, 300)
        if op in ('head', 'face'):
            return _run_local('head_viewport.py', args, 300)
        if op == 'head_dom':
            return _run_local('viewport_dom.py', args, 120)
        if op == 'agent_body':
            path = ROOT / 'identity.json'
            if not path.exists():
                return {'success': False, 'error': 'identity.json missing'}
            ident = json.loads(path.read_text())
            m = ROOT / 'model' / 'xml' / 'asimov_1_25dof_physics.xml'
            ident['model_sha256'] = _sha_file(m)
            ident['success'] = bool(ident.get('bindings', {}).get('M2', {}).get('body') == 'asimov-1')
            return ident
        if op in ('harnesses', 'harness', 'run_harness'):
            aliases = {'media': 'ffmpeg'}
            if not HARNESSES.exists():
                return {'success': False, 'error': f'registry missing: {HARNESSES}'}
            registry = json.loads(HARNESSES.read_text())
            items = registry['harnesses'] if isinstance(registry, dict) else registry
            by_name = {h['name']: h for h in items}
            if op == 'harnesses':
                return {'success': True, 'count': len(items), 'harnesses': items,
                        'authority': 'HUMAN://ROOT'}
            name = args.get('name'); name = aliases.get(name, name)
            if op == 'harness':
                if not name or name not in by_name:
                    return {'success': False, 'error': f'unknown harness {name!r}',
                            'available': sorted(by_name)}
                entry = dict(by_name[name])
                probe = {'voice': 'voices', 'physics': 'physics', 'ledger': 'verify', 'ffmpeg': 'ffmpeg'}.get(name)
                if probe:
                    entry['probe'] = _local_func(probe, {'steps': 10})
                return {'success': True, 'harness': entry, 'authority': 'HUMAN://ROOT'}
            chain = args.get('chain') or ([name] if name else [])
            if not chain:
                return {'success': False, 'error': 'chain or name is required',
                        'available': sorted(by_name)}
            results = []
            probe_map = {'voice': 'voices', 'physics': 'physics', 'ledger': 'verify', 'ffmpeg': 'ffmpeg'}
            for hname in chain:
                hname = aliases.get(hname, hname)
                if hname not in by_name:
                    results.append({'harness': hname, 'success': False, 'error': 'unknown'})
                    continue
                pop = probe_map.get(hname)
                results.append({'harness': hname,
                                'result': _local_func(pop, {'steps': 10}) if pop else
                                {'success': True, 'manifest': by_name[hname]}})
            return {'success': all(r.get('success', r.get('result', {}).get('success', False)) for r in results),
                    'chain': results, 'authority': 'HUMAN://ROOT'}
        return {'success': False, 'error': f'unknown local op {op}'}
    except Exception as e:
        return {'success': False, 'error': f'{type(e).__name__}: {e}'}


def _out(d):
    return json.dumps(d, ensure_ascii=False)


def _last_hash():
    if not LEDGER.exists():
        return 'GENESIS'
    lines = [x for x in LEDGER.read_text(encoding='utf-8').splitlines() if x.strip()]
    if not lines:
        return 'GENESIS'
    try:
        return json.loads(lines[-1])['hash']
    except Exception:
        return 'GENESIS'


def _receipt(action, detail):
    e = {'ts': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
         'action': action, 'authority': 'HUMAN://ROOT', 'prev': _last_hash(),
         'detail': detail}
    payload = json.dumps(e, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    e['hash'] = hashlib.sha256(payload.encode()).hexdigest()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open('a', encoding='utf-8') as f:
        f.write(json.dumps(e, ensure_ascii=False) + '\n')
    return e


def _verify_chain():
    if not LEDGER.exists():
        return {'success': True, 'count': 0, 'head': 'GENESIS'}
    lines = [x for x in LEDGER.read_text(encoding='utf-8').splitlines() if x.strip()]
    prev, ok, broken = 'GENESIS', True, None
    for i, line in enumerate(lines):
        e = json.loads(line)
        h = e.pop('hash', None)
        if e.get('prev') != prev:
            ok, broken = False, i; break
        payload = json.dumps(e, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        calc = hashlib.sha256(payload.encode()).hexdigest()
        if calc != h:
            ok, broken = False, i; break
        prev = h
    return {'success': ok, 'count': len(lines), 'head': prev, 'broken_at': broken}


class FakeCtx:
    def __init__(self):
        self.tools = {}
        self.commands = {}
        self.hooks = {}

    def register_tool(self, name, toolset, handler, schema):
        self.tools[name] = (handler, toolset)

    def register_command(self, name, handler, description, args_hint):
        self.commands[name] = (handler, description, args_hint)

    def register_skill(self, name, path):
        pass

    def register_hook(self, name, handler):
        self.hooks[name] = handler


def _tools(plugin):
    if plugin in _cache:
        return _cache[plugin]
    path = PLUGINS / plugin / '__init__.py'
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location(f'ae_{plugin}', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    ctx = FakeCtx()
    if hasattr(m, 'register'):
        m.register(ctx)
    _cache[plugin] = ctx.tools
    return ctx.tools


def _call(plugin, tool, args):
    tools = _tools(plugin)
    if tool not in tools:
        return {'success': False, 'error': f'tool {tool!r} not in plugin {plugin!r}',
                'available': sorted(tools)}
    handler = tools[tool][0]
    try:
        r = handler(args)
        if isinstance(r, str):
            try:
                r = json.loads(r)
            except Exception:
                pass
        return r
    except Exception as e:
        return {'success': False, 'error': f'{type(e).__name__}: {e}'}


def register(ctx):
    def ae(args: dict) -> str:
        op = args.get('op', 'status')
        arg = dict(args)
        arg.pop('op', None)

        if op == 'status':
            dirs = sorted(p.name for p in PLUGINS.iterdir() if p.is_dir()) if PLUGINS.exists() else []
            chain = _verify_chain()
            result = {'success': True, 'actor': 'hermes-ae', 'authority': 'HUMAN://ROOT',
                      'version': '3.18.0', 'plugins_on_disk': len(dirs),
                      'shortcuts': sorted(SHORTCUTS), 'receipts': chain}
        elif op == 'receipts':
            limit = int(arg.get('limit') or 10)
            lines = LEDGER.read_text(encoding='utf-8').splitlines() if LEDGER.exists() else []
            result = {'success': True, 'count': len(lines),
                      'receipts': [json.loads(x) for x in lines[-limit:]]}
        elif op == 'verify':
            result = _verify_chain()
        elif op == 'ops':
            result = {'success': True, 'shortcuts': sorted(SHORTCUTS), 'local_ops': sorted(LOCAL_OPS),
                      'local_funcs': sorted(LOCAL_FUNCS),
                      'note': 'use op=free_walk or studio_video for bundled pipelines; op=call reaches local legacy plugins'}
        elif op == 'call':
            plugin, tool = arg.pop('plugin', None), arg.pop('tool', None)
            if not plugin or not tool:
                result = {'success': False, 'error': 'plugin and tool are required for op=call'}
            else:
                result = _call(plugin, tool, arg)
        elif op in LOCAL_FUNCS:
            result = _local_func(op, arg)
        elif op in LOCAL_OPS:
            script, timeout = LOCAL_OPS[op]
            result = _run_local(script, arg, timeout)
        elif op in SHORTCUTS:
            plugin, tool = SHORTCUTS[op]
            result = _call(plugin, tool, arg)
        else:
            result = {'success': False, 'error': f'unknown op {op!r}',
                      'available': ['status', 'receipts', 'verify', 'ops', 'call'] + sorted(LOCAL_FUNCS) + sorted(LOCAL_OPS) + sorted(SHORTCUTS)}

        try:
            ok = bool(result.get('success', True))
        except Exception:
            ok = False
        rec = _receipt(f'AE://{op.upper()}', {'ok': ok})
        out = {'success': ok, 'op': op, 'result': result, 'receipt': rec}
        return _out(out)

    ctx.register_tool(
        name='ae', toolset='hermes-ae', handler=ae,
        schema={'type': 'object', 'properties': {
            'op': {'type': 'string', 'description': 'Operation: status, receipts, verify, ops, call, or any shortcut.'},
            'plugin': {'type': 'string', 'description': 'Plugin name for op=call.'},
            'tool': {'type': 'string', 'description': 'Tool name for op=call.'},
            'text': {'type': 'string'}, 'voice': {'type': 'string'},
            'output': {'type': 'string'}, 'script': {'type': 'string'},
            'preset': {'type': 'string'}, 'camera': {'type': 'string'},
            'scene': {'type': 'string'}, 'steps': {'type': 'integer'},
            'limit': {'type': 'integer'}, 'arg': {'type': 'string'},
            'node': {'type': 'string'}, 'action': {'type': 'string'},
            'seconds': {'type': 'integer'}, 'captions': {'type': 'boolean'},
            'physics': {'type': 'boolean'}, 'publish': {'type': 'boolean'},
            'path': {'type': 'string'}, 'legacy': {'type': 'boolean'},
            'name': {'type': 'string'}, 'chain': {'type': 'array'},
        }, 'required': []},
    )
