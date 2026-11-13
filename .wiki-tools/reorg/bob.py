# Stage 2, part 2: fold the Book of Blades equipment pages into the unified lists, then retire those pages.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
W = '--write' in sys.argv
SRC = '%% source: Book of Blades %%'
B = 'Rules/Book of Blades/'
pages = {}
def get(rel):
    if rel not in pages: pages[rel] = read(rel)
    return pages[rel]
def put(rel, s): pages[rel] = s
plain = lambda c: re.sub(r'\*', '', re.sub(r'\[\[[^\]]*?\\?\|([^\]]*)\]\]', r'\1', c))
def add_row(text, cat, row):
    """insert a table row under the bold category row `cat`, alphabetically."""
    L = text.split('\n'); i = next(k for k, l in enumerate(L) if l.startswith(f'| **{cat}** |')); j = i + 1
    name = key(plain(row.split('|')[1]))
    while j < len(L) and L[j].startswith('|') and not L[j].startswith('| **'):
        if key(plain(L[j].split('|')[1])) > name: break
        j += 1
    L.insert(j, row); return '\n'.join(L)
def add_entry(text, head, block, name, level=None):
    """insert a lead-in entry (or ### section if level) into the section starting at heading line `head`, alphabetically."""
    i = text.index(head); nxt = re.compile(r'^#{1,%d} ' % (head.count('#')), re.M).search(text, i + len(head)); end = nxt.start() if nxt else len(text)
    sec = text[i:end]
    pat = re.compile(r'^#{%d} (.+)$' % level, re.M) if level else re.compile(r'^\*\*\*([^*\n]+?)\.?\*\*\*', re.M)
    pos = None
    for m in pat.finditer(sec):
        if key(re.sub(r' \(.*', '', m.group(1))) > key(name): pos = m.start(); break
    if pos is None:
        m2 = re.search(r'\n(?=\*\*[A-Z][^*\n]*\*\*\n\n\||%% sources)', sec) if not level else None
        pos = len(sec.rstrip('\n')) + 1 if not m2 else m2.start() + 1
        sec = sec[:pos].rstrip('\n') + '\n\n' + block + '\n\n' + sec[pos:].lstrip('\n')
    else: sec = sec[:pos] + block + '\n\n' + sec[pos:]
    return text[:i] + sec + text[end:]
def add_src(text, marker, extra):
    i = text.index(marker); j = text.index(' %%', i); return text[:j] + '; Book of Blades: ' + extra + text[j:]
def ents_of(text):
    return {n: '\n\n'.join(ps) for n, ps in entries(text)[1]}

# ---------- sources
arms = read(B + 'Martial Arms.md'); opts = read(B + 'More Weapon Options.md'); gear = read(B + 'Martial Gear.md'); mmi = read(B + 'Martial Magic Items.md')
A = dict(sections(split_footer(split_front(arms)[1])[0], 2))
# repair two paragraphs the conversion broke
A['New Weapons'] = A['New Weapons'].replace(' The butterfly **Martial Arts Weapons**\n\nsword is often', ' The butterfly sword is often')
A['New Weapons'] = re.sub(r'opponent’s weapons, and the\n\n\| 5 sp \|.*?\n\nlong central prong', 'opponent’s weapons, and the long central prong', A['New Weapons'], flags=re.S)
assert '| 5 sp |' not in A['New Weapons'] and 'butterfly sword is often' in A['New Weapons']

# ---------- Weapons
wp = 'Rules/Equipment/Weapons.md'; w = get(wp)
rows = {'Simple Melee Weapons': ['| Boomerang, rebounding | 5 sp | 1d4 bludgeoning | 1 lb. | — | Thrown (range 20/60 ft.) |', '| Umbrella | 5 sp | 1d4 piercing | 2 lb. | — | — |',
          '| Nunchaku | 2 sp | 1d6 bludgeoning | 2 lb. | Whirling Distraction | Finesse |', '| Sai | 2 gp | 1d4 piercing | 2 lb. | Disarming Parry, Disarming Twist, Hook and Pivot, Weapon Trap | Finesse, Hooked, Light |',
          '| Tonfa | 2 sp | 1d4 bludgeoning | 3 lb. | Disarming Parry, Disarming Twist, Forearm Block, Hook and Pivot, Weapon Trap | Finesse, Hooked, Light, Shielding, Special |'],
        'Martial Melee Weapons': ['| Lasso | 5 sp | 1d4 bludgeoning | 10 lb. | — | Thrown (range 20/60 ft.) |', '| Scythe, war | 1 sp | 1d12 slashing | 6 lb. | — | Reach, Two-handed |',
          '| Butterfly sword | 10 gp | 1d6 slashing | 2 lb. | Disarming Parry, Disarming Twist, Hook and Pivot, Weapon Trap | Finesse, Hooked, Light |',
          '| Ji | 15 gp | 1d10 piercing | 6 lb. | Disarming Parry, Disarming Twist, Hook and Pivot, Weapon Trap | Heavy, Hooked, Reach, Two-handed |',
          '| Hook sword | 15 gp | 1d6 slashing | 3 lb. | Disarming Parry, Disarming Twist, Hook and Pivot, Weapon Trap | Hooked, Light, Special, Versatile (1d8) |',
          '| Rope dart | 5 sp | 1d6 bludgeoning | 3 lb. | Ensnare, Twine, Whirling Distraction | Finesse, Reach, Two-handed |'],
        'Simple Ranged Weapons': ['| Shuriken | 5 cp | 1d4 piercing | 1/8 lb. | Misdirect | Finesse, Thrown (range 30/60 ft.) |']}
n_w = 0
for cat, rr in rows.items():
    for r in rr: w = add_row(w, cat, r); n_w += 1
w = add_src(w, '%% sources: Player', 'Boomerang, rebounding, Butterfly sword, Hook sword, Ji, Lasso, Nunchaku, Rope dart, Sai, Scythe, war, Shuriken, Tonfa, Umbrella')
CAT = {'Butterfly Sword': 'Martial Melee', 'Hook Sword': 'Martial Melee', 'Ji': 'Martial Melee', 'Nunchaku': 'Simple Melee', 'Rope Dart': 'Martial Melee', 'Sai': 'Simple Melee',
       'Shuriken': 'Simple Ranged', 'Tonfa': 'Simple Melee', 'Boomerang': 'Simple Melee', 'Lasso': 'Martial Melee', 'Scythe': 'Martial Melee', 'Umbrella': 'Simple Melee'}
RENAME = {'Boomerang': 'Boomerang, Rebounding', 'Scythe': 'Scythe, War'}
nw_a, nw_b = A['New Weapons'].split('### Weapon Properties'); we = ents_of(nw_a); we.update(ents_of(nw_b)); assert set(CAT) - {'Special'} <= set(we), set(CAT) - set(we)
for n in CAT:
    ps = we[n].split('\n\n'); nn = RENAME.get(n, n)
    ps[0] = re.sub(r'^\*\*\*[^*]+\*\*\*', f'***{nn} ({CAT[n]}).***', ps[0]) + ' ' + SRC
    w = add_entry(w, '## Weapon Descriptions', '\n\n'.join(ps), nn)
for n in ('Hooked', 'Shielding'):
    w = add_entry(w, '## Weapon Properties', we[n] + ' ' + SRC, n)
O = sections(split_footer(split_front(opts)[1])[0], 2); Od = dict(O)
n_o = 0
for sec in ('Weapon Options for Martial Arts Weapons', 'New Weapon Options for Existing Weapons'):
    for h, t in sections(Od[sec], 3)[1:]:
        w = add_entry(w, '## Weapon Options', f'### {h}\n\n{SRC}\n\n{t.strip()}', h, level=3); n_o += 1
w = w.replace(' (see **New Weapons** in this chapter)', '')
pre = paragraphs(strip_src(O[0][1]))
monk = next(p for p in pre if p.startswith('> [!note] Optional Class Feature')); mentor = next(p for p in pre if p.startswith('Not every weapon option'))
unarmed = paragraphs(Od['New Weapon Options'])[1]; assert unarmed.startswith('Remember that unarmed strikes')
monk = monk.replace('> [!note] Optional Class Feature: Additional Monk Weapon Proficiencies', '> [!note] Additional Monk Weapon Proficiencies')
mentor = mentor.replace(' (see **Martial Mentors** in **Chapter 2**)', '')
i = w.index('\n### ', w.index('## Weapon Options'))
w = w[:i].rstrip('\n') + '\n\n' + SRC.replace(' %%', ' (the next two paragraphs and the note) %%') + '\n\n' + unarmed + '\n\n' + mentor + '\n\n' + monk + '\n' + w[i:]
mag = Od['Magic Item Weapon Options'].strip()
i = w.index('## Weapon Materials')
w = w[:i] + '## Magic Weapon Options\n\n' + SRC + '\n\n' + mag + '\n\n' + w[i:]
put(wp, w)

# ---------- Armor
ap = 'Rules/Equipment/Armor.md'; a = get(ap)
ae = ents_of(A['Armor'].split('> [!tip]')[0])
tip = re.search(r'> \[!tip\] Challenges for the Well-Equipped Adventurer\n(?:>.*\n?)+', A['Armor']).group(0)
a = add_row(a, 'Shields', '| Lantern shield | 30 gp | +2 | 8 lb. | — |'); a = add_row(a, 'Shields', '| Spiked shield, large | 100 gp | +2 | 8 lb. | Light |')
L = a.split('\n'); k = next(k for k, l in enumerate(L) if l.startswith('| **Shields** |'))
L[k:k] = ['| **Special Armor** |  |  |  |  |', '| Dragonscale armor | +5,000 gp | Matches type | +10 lb. | Natural Materials (as armor) |', '| Winged armor | +200 gp | Matches type | +10 lb. | — |']
a = '\n'.join(L)
a = add_src(a, '%% sources: Player', 'Dragonscale armor, Lantern shield, Spiked shield, large, Winged armor')
a = add_entry(a, '### Shields', ae['Lantern Shield'].replace('***Lantern Shield.***', '***Lantern Shield.***', 1) + ' ' + SRC if '\n\n' not in ae['Lantern Shield'] else ae['Lantern Shield'].replace('\n\n', ' ' + SRC + '\n\n', 1), 'Lantern Shield')
a = add_entry(a, '### Shields', ae['Spiked Shield'].replace('***Spiked Shield.*** Note that this shield', '***Spiked Shield, Large.*** This shield') + ' ' + SRC, 'Spiked Shield, Large')
special = '### Special Armor\n\n' + SRC + '\n\nThese are made as light, medium, or heavy armor; the cost and weight are added to the base armor.\n\n' + ae['Dragonscale Armor'] + '\n\n' + ae['Winged Armor']
i = a.index('### Shields'); a = a[:i] + special + '\n\n' + a[i:]
put(ap, a)

# ---------- Adventuring Gear, Mounts
G = dict(sections(split_footer(split_front(gear)[1])[0], 2))
gp = 'Rules/Equipment/Adventuring Gear.md'; g = get(gp); ge = ents_of(G['Rogue Gear'])
g = add_row(g, 'Alchemical Concoctions', '| Ether (vial) | 25 gp | 1/4 lb. |'); g = add_row(g, 'Alchemical Concoctions', '| Smokeball | 10 gp | 1 lb. |'); g = add_row(g, 'General Gear', '| Garrote | 5 sp | 1/2 lb. |')
g = add_src(g, '%% sources: Player', 'Ether (vial), Garrote, Smokeball')
first = lambda blk: blk.replace('\n\n', ' ' + SRC + '\n\n', 1) if '\n\n' in blk else blk + ' ' + SRC
g = add_entry(g, '### Alchemical Concoctions', first(ge['Ether']), 'Ether'); g = add_entry(g, '### Alchemical Concoctions', first(ge['Smokeball']).replace('10-footradius', '10-foot-radius'), 'Smokeball')
g = add_entry(g, '### General Gear', first(ge['Garrote']), 'Garrote')
put(gp, g)
mp = 'Rules/Equipment/Mounts & Services.md'; m = get(mp); me = ents_of(G['Mount Gear'])
mrows = [r for r in table_rows(G['Mount Gear'])[2:]]; assert len(mrows) == 14 and len(me) == 13, (len(mrows), len(me))
i = m.index('**Mount Gear and Expenses**\n\n|'); j = m.index('\n\n', m.index('|---', i)); old_tbl = m[i:j]
cur = [l for l in old_tbl.split('\n') if l.startswith('| ')][1:]
groups = []      # keep the drawn-object rows under their heading
for l in cur:
    if l.startswith('| Carriage') or l.startswith('| Cart') or l.startswith('| Chariot') or l.startswith('| Sled') or l.startswith('| Wagon'): groups[-1][1].append(l)
    else: groups.append([l, []])
for r in mrows: groups.append([f'| {r[0]} | {r[1]} | {r[2]} |', []])
groups.sort(key=lambda x: key(x[0].split('|')[1]))
new_tbl = '**Mount Gear and Expenses**\n\n| Item | Cost | Weight |\n|---|---|---|\n' + '\n'.join(x for gq in groups for x in [gq[0]] + gq[1])
m = m.replace(old_tbl, new_tbl + '\n\n%% sources: Book of Blades: ' + ', '.join(r[0] for r in mrows) + ' %%')
for n in sorted(me, key=key, reverse=True): m = add_entry(m, '#### Mount Gear and Expenses', me[n] + ' ' + SRC, n)
put(mp, m)

# ---------- magic items
def item_page(typeline, name):
    t = typeline.lower()
    if t.startswith('*armor'): return 'Rules/Magic Items/Magic Armor.md'
    if t.startswith('*weapon'): return 'Rules/Magic Items/Magic Weapons.md'
    assert t.startswith('*wondrous'), typeline
    return 'Rules/Magic Items/Wondrous Items A–L.md' if key(name)[0] <= 'l' else 'Rules/Magic Items/Wondrous Items M–Z.md'
def add_item(rel, name, body):
    s = get(rel); fr, bd = split_front(s); bd, ft = split_footer(bd); secs = sections(bd, 2)
    assert name not in [h for h, _ in secs], name
    k = next((k for k, (h, _) in enumerate(secs) if h and key(h) > key(name)), len(secs))
    secs.insert(k, (name, body)); put(rel, fr + (secs[0][1] + '\n\n' if secs[0][1].strip() else '') + '\n\n'.join(f'## {h}\n\n{t.strip()}' for h, t in secs[1:]) + '\n\n' + ft + '\n')
moved = {}
mount_items = []
for h, t in sections(split_footer(split_front(gear)[1])[0], 2):
    if h in (None, 'Rogue Gear', 'Mount Gear', 'Magic Items For Mounts'): continue
    t = t.replace('\n\n**Armor And Barding Types**', '').strip(); tl = paragraphs(t)[0]
    rel = item_page(tl, h); add_item(rel, h, SRC + '\n\n' + t); moved[h] = rel; mount_items.append(h)
M = sections(split_footer(split_front(mmi)[1])[0], 2); Md = dict(M)
for h, t in sections(Md['Magic Items for Martial Wielders'], 3)[1:]:
    rel = item_page(paragraphs(t)[0], h); add_item(rel, h, SRC + '\n\n' + t.strip()); moved[h] = rel
fsecs = sections(Md['Fabled Magic Items'], 3)[1:]; assert len(fsecs) == 22
fp = 'Rules/Magic Items/Fabled Magic Items.md'
for (h1, lore), (h2, stat) in zip(fsecs[0::2], fsecs[1::2]):
    assert h1.lower() == h2.lower(), (h1, h2)
    lp = paragraphs(lore); sp = paragraphs(stat)
    mm = re.search(r' (\w+)\*$', lp[0])
    if len(lp) > 1 and lp[1].startswith('and *'): lp[0] = lp[0][:mm.start()] + '*'; lp[1] = f'*{mm.group(1)}* ' + lp[1]
    if sp[0].endswith('Fabled*') and sp[1].startswith('*Priceless'):
        x = re.match(r'\*Priceless\n? ?(\([^)]*\))\* ?(.*)', sp[1], re.S); sp[0] = sp[0][:-1] + ' Priceless ' + x.group(1) + '*'; sp[1] = x.group(2)
    add_item(fp, h2, SRC + '\n\n' + '\n\n'.join([sp[0]] + lp + sp[1:])); moved[h2] = fp
# pointer on the mounts page
m = get(mp); i = m.index('**Mount Gear and Expenses**\n\n|')
bar = lambda n: f'*[[{os.path.basename(moved[n])[:-3]}#{n}|{n.lower()}]]*'
m = m[:i] + '***Magic Items for Mounts.*** Some magic items are made for mounts or their riders: ' + ', '.join(bar(n) for n in sorted(mount_items, key=key)) + '. Items that require attunement must be attuned to by the mount’s rider, not the mount itself. ' + SRC + '\n\n' + m[i:]
put(mp, m)

# ---------- Rogue tricks
rp = 'Rules/Classes/Rogue.md'; r = get(rp); i = r.index('## Rogue Subclasses')
put(rp, r[:i] + '## Rogue Tricks\n\n' + SRC + '\n\n' + Od['Rogue Tricks'].strip() + '\n\n' + r[i:])

# ---------- GM note, link fix on Equipment
gm = '---\npublish: false\n---\nGM advice moved off the player pages during the reorganization.\n\n%% source: Book of Blades %%\n\n' + tip
print('weapons +%d rows, +%d options; items moved: %d' % (n_w, n_o, len(moved)))
for k_, v in sorted(moved.items()): print('  ', k_, '->', os.path.basename(v))
if W:
    for rel, s in pages.items(): write(rel, s)
    write('_GM Only/Book of Blades GM Notes.md', gm)
    import json; json.dump(moved, open('/home/claude/ts/bob_moved.json', 'w'))
else:
    os.makedirs('/home/claude/ts/bob', exist_ok=True)
    for rel, s in pages.items(): open('/home/claude/ts/bob/' + os.path.basename(rel), 'w').write(s)
