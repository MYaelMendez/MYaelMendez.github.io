"""ffmpeg harness demo driven by the hermes-agent build body.

Reuses the Asimov identity renderer with ffmpeg-specific narration, title,
stage ribbon, receipt action, and output. One JSON line on completion.
"""
import importlib.util, json, sys
from pathlib import Path
from ae_paths import ANIM, SCRIPTS

sys.path.insert(0, str(SCRIPTS))
_spec = importlib.util.spec_from_file_location('asimov_agent_video', SCRIPTS / 'asimov_agent_video.py')
if _spec is None or _spec.loader is None:
    raise RuntimeError('cannot load asimov_agent_video renderer')
_agent = importlib.util.module_from_spec(_spec)
sys.modules['asimov_agent_video'] = _agent
_spec.loader.exec_module(_agent)

setattr(_agent, 'TEXT', (
    'I am hermes-agent, driving the ffmpeg harness. '
    'Deterministic frames become H.264 and A A C. '
    'ffprobe checks duration, codec, and audio. '
    'A receipt seals every render. '
    'Human root stays. Execution is visible.'
))
setattr(_agent, 'TITLE', '>_æ: FFMPEG // HARNESS')
setattr(_agent, 'SUBTITLE', 'BODY: ASIMOV-1 · HUMAN://ROOT → VIDEO://RENDER')
setattr(_agent, 'STAGE_LINE', 'FRAMES → ENCODE → PROBE → WITNESS → RECEIPT')
setattr(_agent, 'ACTION', 'VIDEO://FFMPEG_HARNESS_DEMO')
setattr(_agent, 'BASE', ANIM / 'ffmpeg_harness_demo')
setattr(_agent, 'FRAMES', _agent.BASE / 'frames')

args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
args.setdefault('publish', True)
args.setdefault('output', str(ANIM / 'ffmpeg-harness-demo-916.mp4'))
sys.argv = [sys.argv[0], json.dumps(args)]
_agent.main()
