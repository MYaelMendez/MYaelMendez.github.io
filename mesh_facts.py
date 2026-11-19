"""Measured model facts. Never hand-type a count into a spec or a surface.

The '52 meshes' claim was wrong: Windows glob is case-INSENSITIVE, so
glob('*.STL') and glob('*.stl') return the same 26 files twice. Two published
films spoke the false number aloud. This module is the single source.
"""
from pathlib import Path
import os, json

H = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))
MODEL = Path(os.environ.get('HERMES_AE_HOME', H / 'plugins' / 'hermes-ae'))


def mesh_count() -> int:
    d = MODEL / 'model' / 'meshes'
    if not d.exists():
        return 0
    return len({p.stem.lower() for p in d.iterdir() if p.suffix.lower() == '.stl'})


def facts() -> dict:
    xml = MODEL / 'model' / 'xml' / 'asimov_1_25dof_actuated.xml'
    t = xml.read_text(encoding='utf-8') if xml.exists() else ''
    return {'meshes': mesh_count(),
            'actuators': t.count('<position') + t.count('<motor'),
            'source': str(MODEL)}


if __name__ == '__main__':
    print(json.dumps(facts(), indent=2))
