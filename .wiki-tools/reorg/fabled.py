# Stage 2: one alphabetical list on Rules/Magic Items/Fabled Magic Items.md.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Magic Items/Fabled Magic Items.md'
old = read(P); front, body = split_front(old); body, foot = split_footer(body)
top = sections(body, 2); items = {}; cur = None; props = None
for h, t in top[1:]:
    if h.startswith('More Fabled Items'): cur = src_of(t); continue
    if h == 'Properties and Attunement': props = t; continue
    if h.startswith('Bright Fey Weapons'): h = 'Bright Fey Weapons'; t = t.replace('\n\nSee the start of this page for how fabled items work.', '')
    if cur and not src_of(t) : t = f'%% source: {cur} %%\n\n' + t
    assert h not in items; items[h] = t
out = [top[0][1], '## Properties and Attunement', "%% source: Player's Guide 2 %%", props]
out += [f'## {n}\n\n{items[n]}' for n in sorted(items, key=key)]
new = front + '\n\n'.join(x.strip('\n') for x in out) + '\n\n' + foot + '\n'
for h in re.findall(r'^### .*$', old, re.M): assert h in new
print(len(items), 'items', [ (n, src_of(items[n])) for n in sorted(items, key=key)][:40])
if '--write' in sys.argv: write(P, new)
