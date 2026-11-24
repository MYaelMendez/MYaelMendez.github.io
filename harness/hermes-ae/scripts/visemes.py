"""Phoneme-driven viseme + caption timeline for Asimov Studio v2.1.

Uses the self-hosted dizione phonemizer (DIZIONE_DATA set explicitly) and
maps IPA-ish symbols to mouth shapes. Falls back to character-level visemes
if the phonemizer is unavailable. Output: /opt/data/asimov-anim/visemes.json
"""
from ae_paths import ANIM, ensure_runtime
ensure_runtime()

import os, json, math, hashlib, re
from pathlib import Path

os.environ.setdefault('DIZIONE_DATA', '/opt/data/tiny-voca-weights/phonemizer')
OUT = ANIM / 'visemes.json'
TEXT = ('I am Asimov. I stand and walk forward. Hermes gives me voice. '
        'Authority remains human root. Greater than underscore ae.')

VOWELS_WIDE = set(list('iɪeɛæ') + ['aɪ', 'eɪ', 'ɔɪ'])
VOWELS_ROUND = set(list('oɔuʊ') + ['ɔː', 'oʊ', 'ɚ', 'ɝ', 'ə'])
VOWELS_OPEN = set(list('aɑæ') + ['ɑː', 'æ'])
CLOSED = {'p','b','m'}
TEETH = {'f','v','θ','ð','s','z','ʃ','ʒ'}

def viseme_for(sym):
    s = sym.strip().lower()
    if s in ('<bos>','<eos>','<sp>') or re.fullmatch(r'[.,!?;:]', s):
        return {'name':'rest','open':0.0,'width':0.15}
    if s in CLOSED: return {'name':'closed','open':0.05,'width':0.20}
    if s in TEETH: return {'name':'teeth','open':0.30,'width':0.65}
    if s in VOWELS_ROUND: return {'name':'round','open':0.45,'width':0.35}
    if s in VOWELS_WIDE: return {'name':'wide','open':0.40,'width':0.90}
    if s in VOWELS_OPEN: return {'name':'open','open':0.85,'width':0.75}
    return {'name':'mid','open':0.45,'width':0.55}

def weight(sym):
    s=sym.strip()
    if s in ('<bos>','<eos>'): return 0.0
    if s=='<sp>': return 0.55
    if re.fullmatch(r'[.,!?;:]',s): return 0.20
    return 1.35 if viseme_for(s)['name'] in ('open','wide','round') else 0.75

def phonemize(text):
    try:
        import dizione
        r=dizione.phonemize(text)
        return list(r.symbols), 'dizione'
    except Exception as e:
        return list(re.sub(r'[^a-z ]','',text.lower()).replace(' ','<sp>')), f'fallback:{type(e).__name__}'

def main():
    syms, source = phonemize(TEXT)
    speech_end = 6.811  # measured tiny-voca M2 duration at speed 1.25
    weights=[weight(s) for s in syms]
    tw=sum(weights) or 1.0
    events=[]; t=0.0
    for s,w in zip(syms,weights):
        dur=(w/tw)*speech_end
        if dur<=0: continue
        v=viseme_for(s)
        events.append({'start':round(t,4),'end':round(t+dur,4),'symbol':s,
                       'viseme':v['name'],'open':v['open'],'width':v['width']})
        t+=dur
    # caption segments from sentences, proportional to length
    sents=[x.strip() for x in re.split(r'(?<=[.!?])\s+',TEXT) if x.strip()]
    total=sum(len(x) for x in sents) or 1
    caps=[]; ct=0.0
    for s in sents:
        d=(len(s)/total)*speech_end
        caps.append({'start':round(ct,4),'end':round(ct+d,4),'text':s})
        ct+=d
    out={'success':True,'text':TEXT,'source':source,'speech_end_s':speech_end,
         'symbols':syms,'phoneme_sha256':hashlib.sha256('|'.join(syms).encode()).hexdigest(),
         'events':events,'captions':caps}
    OUT.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
    print(json.dumps({'success':True,'source':source,'symbols':len(syms),
                      'events':len(events),'captions':len(caps),
                      'sha256':out['phoneme_sha256']}))

if __name__=='__main__':
    main()
