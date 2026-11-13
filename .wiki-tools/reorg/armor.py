# Reorg stage 2: one Armor page.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Equipment/Armor.md'
old = read(P)
front, rest = split_front(old); body, footer = split_footer(rest)
S = sections(body, 2); T = dict(S); assert len(T) == len(S)
CATS = ['Light Armor', 'Medium Armor', 'Heavy Armor', 'Shields']
def cap(n): return n[0].upper() + n[1:].lower() if not n.isupper() else n
rows = {c: [] for c in CATS}; srcs = {}
def catname(x):
    x = x.replace('**', '')
    for c in CATS:
        if x.startswith(c.rstrip('s')): return c
    return None
def take(title, src, conv=None):
    cat = None
    for c in table_rows(T[title]):
        if len(c) not in (5, 6) or c[0] in ('Armor', 'Category', 'Dragon Type') or set(c[0]) <= set('-: ') or c[0].startswith('At the GM'): continue
        if c[0] in ('Light', 'Medium', 'Heavy', 'Shield') and len(c) == 3: continue
        k = catname(c[0])
        if k and not any(c[1:]): cat = k; continue
        if k and c[0].replace('**', '') in ('Shield',) and not c[1]: cat = k; continue
        r = conv(c) if conv else c
        r = [cap(r[0])] + r[1:]
        rows[cat].append(r)
        if src: srcs.setdefault(src, []).append(r[0])
take('Armor Types & Proficiencies', None)
for r in rows['Light Armor']:
    if r[0] == 'Padded': r[4] = 'Noisy\\*'
for r in rows['Shields']:
    if r[0] == 'Shield': r[4] = '—\\*'
take('Armor Types', "Player's Guide 2")
def nl(c):  # Armor | AC | Strength | Stealth | Weight | Cost  ->  core columns
    props = []
    if c[2] not in ('—', ''): props.append(f'Cumbersome ({c[2]})')
    if c[3].lower().startswith('disadv'): props.append('Noisy')
    return [c[0], c[5], c[1], c[4], ', '.join(props) or '—']
take('More Armor (Northlands Worldbook)', 'Northlands Worldbook', nl)
take('More Armor (Trade Secrets)', 'Trade Secrets')
names = [r[0] for c in CATS for r in rows[c]]
assert len(names) == 14 + 4 + 4 + 10, len(names)
assert not {n for n in names if names.count(n) > 1}
table = '**Armor**\n\n| Armor | Cost | Armor Class (AC) | Weight | Properties |\n|---|---|---|---|---|\n'
for c in CATS: table += f'| **{c}** |  |  |  |  |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in sorted(rows[c], key=lambda r: key(r[0])))
table += '\n\\* At the GM’s discretion, this armor can have the Natural Materials property. Make this decision when you acquire it and note it on your character sheet.\n'
table += '\n%% sources: ' + '; '.join(f'{k}: {", ".join(sorted(v))}' for k, v in srcs.items()) + ' %%\n'
def clean(x): return '\n'.join(l for l in strip_src(x).split('\n') if not l.startswith('|') and l.strip() not in ('*Armor*', '**Armor (Northlands Worldbook)**', '**Armor (Trade Secrets)**'))
# ---- descriptions by type
core = sections(T['Armor Types & Proficiencies'], 3)
type_intro = core[0][1]
D = {c: [] for c in CATS}; intro = {}; note = None
for t, x in core[1:]:
    m = re.search(r'> \[!note\] What About Equipment Size\?\n(?:>.*\n?)+', x)
    if m: note = m.group(0).strip('\n'); x = x.replace(m.group(0), '')
    loose, es = entries(clean(x)); intro[t] = loose
    for n, ps in es: D[t].append((n, ps, None))
def tagged(text, src):
    loose, es = entries(clean(text))
    for n, ps in es:
        m = re.match(r'^(.*?) \((Light Armor|Medium Armor|Heavy Armor|Shield)\)$', n); assert m, n
        ps = [ps[0].replace(f'***{n}.***', f'***{m.group(1)}.***', 1)] + ps[1:]
        assert ps[0].startswith(f'***{m.group(1)}.***'), ps[0][:60]
        D['Shields' if m.group(2) == 'Shield' else m.group(2)].append((m.group(1), ps, src))
tagged(T['Armor Types'], "Player's Guide 2")
tagged(T['More Armor (Northlands Worldbook)'], 'Northlands Worldbook')
ts = dict(sections(T['More Armor (Trade Secrets)'], 3))
tagged(ts['Armor Types (Trade Secrets)'], 'Trade Secrets')
def render(es):
    names = [key(n) for n, _, _ in es]; assert not {n for n in names if names.count(n) > 1}, names
    return '\n\n'.join('\n\n'.join(ps) + (f' %% source: {s} %%' if s else '') for n, ps, s in sorted(es, key=lambda z: key(z[0])))
types = '\n\n'.join(f'### {c}\n\n' + '\n\n'.join(intro[c]) + '\n\n' + render(D[c]) for c in CATS)
# ---- materials and properties
def gather(pairs):
    out = []; loose0 = None
    for text, src in pairs:
        loose, es = entries(clean(text))
        if loose0 is None: loose0 = loose
        out += [(n, ps, src) for n, ps in es]
    return loose0, out
dragon = '*Dragonhide Damage*\n\n| Dragon Type | Damage Type |\n|---|---|\n' + ''.join('| ' + ' | '.join(c) + ' |\n' for c in table_rows(T["Armor Materials (Player's Guide 2)"])[2:])
mloose, mats = gather([(T['Armor Materials'], None), (T["Armor Materials (Player's Guide 2)"].replace('*Dragonhide Damage*', ''), "Player's Guide 2"), (ts['Armor Materials (Trade Secrets)'], 'Trade Secrets')])
mats = [(n, ps + ([dragon.replace('*Dragonhide Damage*', '**Dragonhide Damage**')] if n == 'Dragonhide' else []), s) for n, ps, s in mats]
mats = [(n, [re.sub(r'^\*\*\*(Carapace|Dragonhide)\*\*\*\.', r'***\1.***', ps[0])] + ps[1:], s) for n, ps, s in mats]
ploose, props = gather([(T['Armor Properties'], None), (ts['Armor Properties (Trade Secrets)'], 'Trade Secrets')])
def render2(es):
    out = []
    for n, ps, s in sorted(es, key=lambda z: key(z[0])):
        ps = list(ps)
        ps[0] = ps[0] + (f' %% source: {s} %%' if s else '')
        out.append('\n\n'.join(ps))
    return '\n\n'.join(out)
new = f'''{front}{S[0][1]}

## Calculating Armor Class (AC)

{T['Calculating Armor Class (AC)']}

## Armor Types & Proficiencies

{type_intro}

{table}
{note}

{types}

## Armor Properties

{(chr(10)+chr(10)).join(ploose)}

{render2(props)}

## Armor Materials

{(chr(10)+chr(10)).join(mloose)}

{render2(mats)}

## Getting into and Out of Armor

{T['Getting into and Out of Armor']}

{footer}
'''
for n in set(re.findall(r'^\*\*\*([^*\n]+?)\.?\*\*\*', old, re.M)):
    n2 = re.sub(r' \((Light Armor|Medium Armor|Heavy Armor|Shield)\)$', '', n)
    assert n2 in new, n
if '--write' in sys.argv: write(P, new)
else: open('/home/claude/ts/armor_new.md', 'w').write(new)
print({c: len(rows[c]) for c in CATS}, {c: len(D[c]) for c in CATS}, len(mats), 'materials', len(props), 'properties')
