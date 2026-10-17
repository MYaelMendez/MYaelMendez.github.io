#!/usr/bin/env python3
"""Normalize Unbound Bible RV1909 (raw/) -> src/rv1909/rv1909.jsonl  (id 'rv1909:GEN.1.1', text)."""
import json, re, unicodedata, hashlib, collections, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT/'src/rv1909/raw/spanish_reina_valera_1909_utf8.txt'
CW = json.load(open(ROOT/'align/crosswalk.json'))
unb2code = {b['unbound']: b['code'] for b in CW['books'] if b.get('unbound')}
out, counts, issues = [], collections.OrderedDict(), []
for line in open(RAW, encoding='utf-8'):
    if line.startswith('#') or not line.strip(): continue
    p = line.rstrip('\n').split('\t')
    bk, ch, vs, sub, order, text = p[0], int(p[1]), int(p[2]), p[3], int(p[4]), p[5]
    if sub: issues.append(f'subverse {bk} {ch}:{vs}{sub}')
    t = unicodedata.normalize('NFC', re.sub(r'<[^>]+>', '', text))
    t = re.sub(r'\s+', ' ', t).strip()
    if not t: issues.append(f'empty {bk} {ch}:{vs}')
    code = unb2code[bk]
    out.append({'id': f'rv1909:{code}.{ch}.{vs}', 'text': t})
    counts[code] = counts.get(code, 0) + 1
ids = [o['id'] for o in out]; assert len(ids) == len(set(ids)), 'duplicate ids'
dst = ROOT/'src/rv1909/rv1909.jsonl'
with open(dst, 'w', encoding='utf-8') as f:
    for o in out: f.write(json.dumps(o, ensure_ascii=False) + '\n')
sha = hashlib.sha256(dst.read_bytes()).hexdigest()
json.dump({'edition': 'rv1909', 'verses': len(out), 'books': len(counts), 'per_book': counts,
           'sha256_jsonl': sha, 'issues': issues}, open(ROOT/'src/rv1909/stats.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), len(counts), sha, issues[:10])
