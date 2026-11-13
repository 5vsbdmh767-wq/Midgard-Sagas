# Reorg stage 2: one Weapons page (one table, one list each of descriptions, options, materials, properties).
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Equipment/Weapons.md'
front, rest = split_front(read(P)); body, footer = split_footer(rest)
S = sections(body, 2)
T = {t: x for t, x in S}
assert len(T) == len(S), [t for t, _ in S]
SRC = {"More Weapons (Player's Guide 2)": "Player's Guide 2", 'Weapon Types': "Player's Guide 2", "Weapon Materials (Player's Guide 2)": "Player's Guide 2",
       "Weapon Properties (Player's Guide 2)": "Player's Guide 2", 'More Weapons (Northlands Worldbook)': 'Northlands Worldbook', 'More Weapons (Trade Secrets)': 'Trade Secrets'}
# ---- table
CATS = ['Simple Melee Weapons', 'Simple Ranged Weapons', 'Martial Melee Weapons', 'Martial Ranged Weapons']
rows = {c: [] for c in CATS}; bysrc = {}
def norm(c):
    name, cost, dmg, wt, opt, prop = c
    dmg = re.sub(r'\b(Bludgeoning|Piercing|Slashing)\b', lambda m: m.group(1).lower(), dmg)
    prop = prop.replace('Two-Handed', 'Two-handed')
    prop = re.sub(r'\((\d+/\d+)( ft\.)?\)', r'(range \1 ft.)', prop)
    prop = re.sub(r'\(range (\d+/\d+)\)', r'(range \1 ft.)', prop)
    prop = re.sub(r'\((1d\d+), range (\d+/\d+)\)', r'(\1, range \2 ft.)', prop)
    return [name, cost.rstrip('.'), dmg, wt, opt or '—', prop]
for title, text in S:
    cat = None
    for c in table_rows(text):
        if len(c) != 6 or c[0] == 'Weapon' or set(c[0]) <= set('-: '): continue
        n = c[0].replace('**', '')
        if n in CATS: cat = n; continue
        assert cat, c
        rows[cat].append(norm(c)); bysrc.setdefault(SRC.get(title, 'Player\'s Guide'), []).append(c[0].replace('\\*', ''))
names = [r[0] for c in CATS for r in rows[c]]
dups = sorted({n for n in names if names.count(n) > 1}); assert not dups, dups
table = '**Weapons**\n\n| Weapon | Cost | Damage | Weight | Weapon Options | Properties |\n|---|---|---|---|---|---|\n'
for c in CATS:
    table += f'| **{c}** |  |  |  |  |  |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in sorted(rows[c], key=lambda r: key(r[0])))
table += '\n\\* The listings for “Pistol sword, pistol” and “Pistol sword, sword” are the same item showing different attack modes.\n'
table += '\n%% sources: ' + '; '.join(f'{k}: {", ".join(sorted(v))}' for k, v in bysrc.items() if k != "Player's Guide") + ' %%\n'
# ---- text pieces
def untable(x): return '\n'.join(l for l in x.split('\n') if not l.startswith('|') and l.strip() not in ('**Weapons**', '*Weapons*', '**Weapons (Northlands Worldbook)**', '**Weapons (Trade Secrets)**'))
def ents(title, sub=None):
    x = strip_src(untable(T[title]))
    if sub:
        ss = dict(sections(x, 3)); x = ss[sub]
    else:
        x = sections(x, 3)[0][1]
    return entries(x)
def tagged(es, src): return [(n, ps[:1] + ps[1:] , src) for n, ps in es]
desc = []; mats = []; props = []
l, e = ents('Weapon Types'); desc += tagged(e, "Player's Guide 2")
l, e = ents('More Weapons (Northlands Worldbook)'); desc += tagged(e, 'Northlands Worldbook')
l, e = ents('More Weapons (Trade Secrets)', 'Weapon Types (Trade Secrets)'); desc += tagged(e, 'Trade Secrets')
core_mat_loose, e = ents('Weapon Materials'); mats += tagged(e, None)
l, e = ents("Weapon Materials (Player's Guide 2)"); mats += tagged(e, "Player's Guide 2")
l, e = ents('More Weapons (Trade Secrets)', 'Weapon Materials (Trade Secrets)'); mats += tagged(e, 'Trade Secrets')
core_prop_text = T['Weapon Properties']
note = re.search(r'> \[!note\] Equipment Packs\n(?:>.*\n?)+', core_prop_text).group(0)
core_prop_loose, e = entries(core_prop_text.replace(note, '')); props += tagged(e, None)
l, e = ents("Weapon Properties (Player's Guide 2)"); props += tagged(e, "Player's Guide 2")
l, e = ents('More Weapons (Trade Secrets)', 'Weapon Properties (Trade Secrets)'); props += tagged(e, 'Trade Secrets')
def render(es):
    out = []
    names = [key(n) for n, _, _ in es]; d = {n for n in names if names.count(n) > 1}; assert not d, d
    for n, ps, src in sorted(es, key=lambda z: key(z[0])):
        ps = [p for p in ps if 'Northlands Worldbook also describes masterwork' not in p]
        out.append('\n\n'.join(ps) + (f' %% source: {src} %%' if src else ''))
    return '\n\n'.join(out)
# descriptions: drop the "(Martial Melee)" style tags? keep them, they are useful
# ---- options
opt_sec = sections(T['Weapon Options'], 3)
opt_intro = opt_sec[0][1]
opts = [(t, x, None) for t, x in opt_sec[1:]]
nl = dict(sections(T['More Weapons (Northlands Worldbook)'], 3)); opts.append(('Puncture', nl['Puncture'], 'Northlands Worldbook'))
tl, te = ents('More Weapons (Trade Secrets)', 'Weapon Options (Trade Secrets)')
for n, ps in te: opts.append((n, LEAD.sub('', ps[0]) + ('\n\n' + '\n\n'.join(ps[1:]) if ps[1:] else ''), 'Trade Secrets'))
opt_md = '\n\n'.join(f'### {n}\n\n' + (f'%% source: {s} %%\n\n' if s else '') + x.strip() for n, x, s in sorted(opts, key=lambda z: key(z[0])))
# ---- improvised weapons: text before and after the old table
imp = [p for p in paragraphs(untable(T['Improvised Weapons']))]
pre = S[0][1]
new = f'''{front}{pre}

## Weapon Types & Proficiencies

{T['Weapon Types & Proficiencies']}

{table}
## Weapon Descriptions

{render(desc)}

## Weapon Properties

{chr(10).join(core_prop_loose)}

{render(props)}

## Weapon Options

{opt_intro}

{opt_md}

## Weapon Materials

{(chr(10)+chr(10)).join(core_mat_loose)}

{render(mats)}

## Improvised Weapons

{(chr(10)+chr(10)).join(imp)}

{footer}
'''
old = read(P)
# nothing lost: every lead-in name, option heading and table row name must survive
for n in set(re.findall(r'^\*\*\*([^*\n]+?)\.?\*\*\*', old, re.M)) | set(names):
    assert n in new, n
if '--write' in sys.argv:
    write(P, new)
    open(os.path.join(V, '.wiki-tools/reorg/_moved_equipment_packs_note.md'), 'w').write(note)
else:
    open('/home/claude/ts/weapons_new.md', 'w').write(new)
print(len(names), 'weapons;', len(desc), 'descriptions;', len(props), 'properties;', len(opts), 'options;', len(mats), 'materials')
