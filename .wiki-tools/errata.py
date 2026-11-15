# Apply errata as exact text replacements. Each edit must match exactly once.
# Usage: python3 -I .wiki-tools/errata.py <edits.py>   (the edits file defines EDITS = [(page, old, new), ...])
import sys, os, runpy
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = ' %% errata 2025-05-29 %%'
EDITS = runpy.run_path(sys.argv[1], {'E': E})['EDITS']
idx = {}
for dp, dn, fn in os.walk(V):
    dn[:] = [d for d in dn if not d.startswith('.')]
    for f in fn:
        if f.endswith('.md'): idx.setdefault(f[:-3], []).append(os.path.join(dp, f))
bad = 0; done = []
for page, old, new in EDITS:
    p = idx[page]; assert len(p) == 1, page; p = p[0]
    s = open(p, encoding='utf-8').read(); n = s.count(old)
    if n != 1: print('MISS', page, n, '|', old[:70]); bad += 1; continue
    s = s.replace(old, new); open(p, 'w', encoding='utf-8').write(s); done.append(page)
print('applied', len(done), 'missed', bad)
