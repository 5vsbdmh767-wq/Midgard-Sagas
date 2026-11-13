# Reorg stage 2: one Adventuring Gear page.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Equipment/Adventuring Gear.md'
old = read(P)
front, rest = split_front(old); body, footer = split_footer(rest)
S = sections(body, 2); T = dict(S); assert len(T) == len(S)
def sent(n):  # sentence-case a gear name, like the core table
    w = n.split(' ')
    return ' '.join([w[0]] + [x if re.match(r'^\(?[A-Z]{2,}', x) else (x[0] + x[1:].lower() if x.startswith('(') else x.lower()) for x in w[1:]])
CATS = ['General Gear', 'Alchemical Concoctions', 'Ammunition', 'Containers', 'Herbal Concoctions', 'Mechanical Devices', 'Provisions', 'Spellcasting Foci']
rows = {c: [] for c in CATS}; srcs = {}; craft = []
def add(cat, name, cost, wt, src=None):
    rows[cat].append([name, cost, wt])
    if src: srcs.setdefault(src, []).append(name)
# core two-up table: read down the left pair, then down the right pair
core = [c for c in table_rows(T['Special Gear']) if len(c) == 6 and c[0] != 'Gear' and not set(c[0]) <= set('-: ')]
SUB = {'Alchemical Concoctions': 3, 'Ammunition': 4, 'Containers': 12, 'Herbal Concoctions': 6, 'Spellcasting Foci': 4}
seq = [c[:3] for c in core] + [c[3:] for c in core]
i = 0
while i < len(seq):
    n, cost, wt = seq[i]
    if n in SUB:
        assert not cost, n
        for j in range(1, SUB[n] + 1): add(n, *seq[i + j])
        i += SUB[n] + 1
    else: add('General Gear', n, cost, wt); i += 1
assert [r[0] for r in rows['Herbal Concoctions']] == ['Antitoxin (vial)', 'Perfume (vial)', 'Poison, basic (vial)', 'Poison, essence of ether (vial)', 'Poison, last gasp (vial)', 'Poison, midnight tears (vial)'], rows['Herbal Concoctions']
assert rows['Spellcasting Foci'][-1][0] == 'Wyrd focus' and rows['Containers'][0][0] == 'Backpack' and rows['Containers'][-1][0] == 'Waterskin'
# Player's Guide 2 table
cat = 'General Gear'
for c in table_rows(T["More Adventuring Gear (Player's Guide 2)"]):
    if len(c) != 3 or c[0] == 'Gear' or set(c[0]) <= set('-: '): continue
    if c[0] in ('Alchemical Concoctions', 'Ammunition'): cat = c[0]; continue
    if c[0] == 'Crossbow (Empty)': cat = 'General Gear'; continue
    n = 'Magazine, repeating crossbow (empty)' if c[0] == 'Magazine, Repeating' else sent(c[0])
    add(cat, n, c[1], c[2], "Player's Guide 2")
# Northlands table (Item | Weight | Cost)
for c in table_rows(T['More Adventuring Gear (Northlands Worldbook)']):
    if len(c) != 3 or c[0] == 'Item' or set(c[0]) <= set('-: '): continue
    add('General Gear', sent(c[0]), c[2], c[1], 'Northlands Worldbook')
# Trade Secrets tables
ts = dict(sections(T['More Adventuring Gear (Trade Secrets)'], 3))
TSCAT = {'Provisions': 'Provisions', 'Alchemical Items': 'Alchemical Concoctions', 'Herbal Concoctions': 'Herbal Concoctions', 'Mechanical Devices': 'Mechanical Devices'}
for sec, cat in TSCAT.items():
    for c in table_rows(ts[sec]):
        if len(c) != 5 or c[0] == 'Item' or set(c[0]) <= set('-: '): continue
        add(cat, sent(c[0]), c[1], c[2], 'Trade Secrets'); craft.append([sent(c[0]), c[3], c[4]])
allnames = [r[0] for c in CATS for r in rows[c]]
d = sorted({n for n in allnames if allnames.count(n) > 1}); assert not d, d
table = '**Adventuring Gear**\n\n| Gear | Cost | Weight |\n|---|---|---|\n'
for c in CATS: table += f'| **{c}** |  |  |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in sorted(rows[c], key=lambda r: key(r[0])))
table += '\n%% sources: ' + '; '.join(f'{k}: {", ".join(sorted(v))}' for k, v in srcs.items()) + ' %%\n'
ctab = '**Crafting Times**\n\n| Gear | Crafting Time | Crafting DC |\n|---|---|---|\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in sorted(craft, key=lambda r: key(r[0])))
ctab += '\n\\* After the initial preparation time (10% of the total time), this item does not require frequent supervision to craft.\n'
# ---- descriptions
def clean(x): return '\n'.join(l for l in strip_src(x).split('\n') if not l.startswith('|') and not re.match(r'^\*{1,2}(Adventuring Gear|New [A-Z][a-z]+( [A-Z][a-z]+)?|Adventuring Gear \(Northlands Worldbook\)|Container Capacity)\*{1,2}$', l.strip()))
def notes(x):
    found = re.findall(r'(?:^> .*\n?|^>\n?)+', x, re.M)
    for f in found: x = x.replace(f, '')
    return x, [f.strip('\n') for f in found]
core_text, core_notes = notes(T['Special Gear'])
cap_table = '**Container Capacity**\n\n' + '\n'.join(l for l in T['Special Gear'].split('\n') if l.startswith('| ') and len(table_rows(l)[0]) == 3 or l.startswith('|---|---|---|') and False)
cap_rows = [c for c in table_rows(T['Special Gear']) if len(c) == 3]
cap_table = '**Container Capacity**\n\n| ' + ' | '.join(cap_rows[0]) + ' |\n|---|---|---|\n' + ''.join('| ' + ' | '.join(c) + ' |\n' for c in cap_rows[2:])
loose_core, e_core = entries(clean(core_text))
_, e_pg2 = entries(clean(T["Special Gear (Player's Guide 2)"]))
_, e_nl = entries(clean(T['More Adventuring Gear (Northlands Worldbook)']))
E = {c: [] for c in CATS}
lookup = {}
for c in CATS:
    for r in rows[c]: lookup[key(re.sub(r' \(.*\)$', '', r[0]))] = c
def cat_of(name, default='General Gear'):
    k = key(re.sub(r' \(.*\)$', '', name))
    if k in lookup: return lookup[k]
    for lk, c in lookup.items():
        if lk.startswith(k) or k.startswith(lk): return c
    return default
for n, ps in e_core: E[cat_of(n)].append((n, ps, None))
for n, ps in e_pg2: E[cat_of(n)].append((n, ps, "Player's Guide 2"))
for n, ps in e_nl: E[cat_of(n)].append((n, ps, 'Northlands Worldbook'))
intro = {}
timer = None
for sec, cat in TSCAT.items():
    x, nn = notes(ts[sec])
    if nn: timer = nn[0]
    x = clean(x).replace('\\* After the initial preparation time (10% of the total time), this item does not require frequent supervision to craft.', '')
    loose, es = entries(x)
    intro[cat] = loose
    for n, ps in es: E[cat].append((n, ps, 'Trade Secrets'))
assert timer and 'Timer Duration' in timer
def render(es):
    names = [key(n) for n, _, _ in es]; dd = {n for n in names if names.count(n) > 1}; assert not dd, dd
    return '\n\n'.join('\n\n'.join(ps) + (f' %% source: {s} %%' if s else '') for n, ps, s in sorted(es, key=lambda z: key(z[0])))
NOTE = {n.split('\n')[0]: n for n in core_notes}
desc = ''
for c in CATS:
    if not E[c] and not intro.get(c): continue
    desc += f'\n### {c}\n\n' + ('\n\n'.join(intro.get(c, [])) + '\n\n' if intro.get(c) else '') + render(E[c]) + '\n'
    if c == 'Containers': desc += '\n' + NOTE['> [!note] Container Capacity'] + '\n\n' + cap_table
    if c == 'Herbal Concoctions': desc += '\n' + NOTE['> [!note] Using Poison'] + '\n'
    if c == 'Mechanical Devices': desc += '\n' + timer + '\n'
# ---- packs
pk = open(os.path.join(V, '.wiki-tools/reorg/_moved_equipment_packs_note.md')).read()
pk = re.sub(r'^> ?', '', pk, flags=re.M).replace('[!note] Equipment Packs\n', '').strip()
head, *parts = re.split(r' ?\*\*([^*]+ Pack \(\d+ gp\))\.\*\* ', pk)
packs = [(parts[i], parts[i + 1].strip(), None) for i in range(0, len(parts), 2)]
tl, te = entries(clean(ts['Equipment Packs']))
for n, ps in te: packs.append((n, LEAD.sub('', ps[0]), 'Trade Secrets'))
pmd = '\n\n'.join(f'***{n}.*** {x}' + (f' %% source: {s} %%' if s else '') for n, x, s in sorted(packs, key=lambda z: key(z[0])))
# ---- trinkets
tr = strip_src(T["Trinkets (Player's Guide 2)"]).strip().replace('*Trinkets*', '**Trinkets**')
ts_intro = paragraphs(strip_src(sections(T['More Adventuring Gear (Trade Secrets)'], 3)[0][1]))
new = f'''{front}{S[0][1]}

{table}
{ctab}
## Gear Descriptions

This section describes items that have special rules or require further explanation.
{desc}
## Equipment Packs

{head.strip()} {tl[0] if tl else ''}

{pmd}

## Trinkets

%% source: Player's Guide 2 %%

{tr}

{footer}
'''
for n in set(re.findall(r'^\*\*\*([^*\n]+?)\.?\*\*\*', old, re.M)):
    assert n in new, n
for c in table_rows(old):
    for cell in c[:1] + (c[3:4] if len(c) == 6 else []):
        if cell and not set(cell) <= set('-: ') and cell not in ('Gear', 'Item', 'Container', 'd100', 'd12') and not cell.isdigit() and '–' not in cell[:4]:
            assert sent(cell).lower() in new.lower() or cell.lower() in new.lower() or cell in ('Magazine, Repeating', 'Crossbow (Empty)'), cell
if '--write' in sys.argv: write(P, new)
else: open('/home/claude/ts/gear_new.md', 'w').write(new)
print({c: len(rows[c]) for c in CATS}, {c: len(E[c]) for c in CATS}, len(packs), 'packs', 'dropped intro:', [p[:60] for p in ts_intro], [p[:50] for p in loose_core])
