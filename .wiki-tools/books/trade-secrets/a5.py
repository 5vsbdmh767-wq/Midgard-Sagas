# Trade Secrets chapter 5 (PDF pages 119-161): disenchanting, recommended items by class,
# new magic items, new fabled items, appendix tables.
# Dry run writes previews to /home/claude/ts; --write changes the vault.
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
from common import *
import stream, recommended
PDF = '/mnt/user-data/uploads/Trade-Secrets.pdf'
WRITE = '--write' in sys.argv
t = stream.render(PDF, 119, 161)
t = re.sub(r'\*\*([^*\n]+?)\*\*\*\*\*\.\*\*\*', r'***\1.***', t)          # **5th Level*****.*** -> ***5th Level.***
t = re.sub(r'\*\* ([,.;:])', r'**\1', t)
t = re.sub(r'^\*\*•\*\* ', '- ', t, flags=re.M)
CR = '\n*Material marked as from Trade Secrets is from Trade Secrets by Kobold Press.*\n'
links = set()

# ---------------- disenchanting (player page)
dz = between(t, '# Optional Rule: Disenchanting Magic Items', '# Recommended Magic Items by Class')
types1 = between(dz, '> [!note]\n> While prima materia', '\n\n#### Overcharging')
types2 = between(dz, '> [!note]\n> such as bones, hands', '\n\n## New Downtime Activity: Disenchanting')
dz = dz.replace(types1, '').replace(types2, '')
box = types1.rstrip() + ' ' + types2.replace('> [!note]\n> ', '').strip()
box = box.replace('> [!note]\n', '> [!note] Types of Prima Materia\n').replace('and**aqua materia.**', 'and **aqua materia**.').replace('It isn’toriously', 'It is notoriously')
dz = rep(dz, '### Types of Prima Materia\n\n', '')
dz = rep(dz, '\n\n## New Downtime Activity: Disenchanting Magic Items', '\n\n' + box + '\n\n## New Downtime Activity: Disenchanting Magic Items')
which = between(dz, '### Which Items Can Be Disenchanted', '\n\nCHA modifier), it might')
dz = dz.replace(which, '')
dz, n_ = re.subn(r'12 \+ the item’s\s+CHA modifier\), it might', '12 + the item’s CHA modifier), it might', dz); assert n_ == 1
dz = rep(dz, '\n\n## New Downtime Activity: Extracting', '\n\n' + which.replace('### Which Items Can Be Disenchanted\n\n> [!note]', '> [!note] Which Items Can Be Disenchanted') + '\n\n## New Downtime Activity: Extracting')
cu = between(dz, '### Constructs and Undead')
dz = dz.replace(cu, cu.replace('### Constructs and Undead\n\n> [!note]', '> [!note] Constructs and Undead'))
# the "Which Creatures Contain Prima Materia?" sidebar printed beside the next section
wc = between(t, '### Which Creatures Contain Prima Materia?', '## Tier 1 Recommended Magic Items')
wtxt = re.sub(r'\s+', ' ', wc.split('> ', 1)[1]).strip()
head_, lst = wtxt.split('Here’s a non-exhaustive list of creatures and creature types that might well contain prima materia: ')
creatures = ['Celestials', 'Constructs (not including robots)', 'Dragons', 'Elementals', 'Fey', 'Fiends', 'Skeletons and zombies', 'Sorcerers']
for c in ['Celestials', 'Constructs', '(not including robots)', 'Dragons', 'Elementals', 'Fey', 'Fiends', 'Skeletons and zombies', 'Sorcerers']: assert c in lst, c
wbox = '> [!note] Which Creatures Contain Prima Materia?\n> ' + head_ + 'Here’s a non-exhaustive list of creatures and creature types that might well contain prima materia:\n>\n' + ''.join(f'> - {c}\n' for c in creatures)
dz = dz.rstrip() + '\n\n' + wbox
dz = dz.replace('# Optional Rule: Disenchanting Magic Items\n\n', '')
dz = re.sub(r'^## New Downtime Activity: (.+)$', r'## \1', dz, flags=re.M)
for a, b in [('She save the rest', 'She saves the rest'), ('you can use 2 ounces of prima materia, roll the recharge die twice', 'you can use 2 ounces of prima materia to roll the recharge die twice'),
             ('note how many charges has above its maximum', 'note how many charges it has above its maximum'), ('PCs can also extra materia', 'PCs can also extract materia'),
             ('**Overcharge Stabilization Dc**', '**Overcharge Stabilization DC**'), ('**Days By Rarity**', '**Days by Rarity**'), ('**Maximum Prima Materia By Rarity**', '**Maximum Prima Materia by Rarity**'),
             ('**Time By Challenge Rating**', '**Time by Challenge Rating**'), ('in conflict, as the rules in the', 'in conflict, as described in the')]:
    if a in dz: dz = dz.replace(a, b)
dz = re.sub(r'\| Creature CR \| Time Required \| Creature CR \| Time Required \|\n\|---\|---\|---\|---\|\n((?:\|[^\n]*\|\n)+)',
            lambda m: '| Creature CR | Time Required |\n|---|---|\n' + ''.join(f'| {a} | {b} |\n' for a, b in
                [tuple(x.strip() for x in r.strip('|').split('|')[:2]) for r in m.group(1).strip().split('\n')] +
                [tuple(x.strip() for x in r.strip('|').split('|')[2:4]) for r in m.group(1).strip().split('\n')] if a), dz)
DIS = f'''---
aliases: [Prima Materia, Disenchanting Magic Items, Extracting Prima Materia]
publish: true
---
{OPT}{tidy(dz).strip()}
'''
DIS = linkitalics(DIS, links).rstrip() + CREDIT

# ---------------- recommended items by class
SRC = {'1': 'Player’s Guide', '2': 'Player’s Guide 2', '3': 'Labyrinth Worldbook', '4': 'Trade Secrets'}
rows = recommended.parse()
fixed = []
for tier, cls, item, src, price, app in rows:
    if tier == 2 and item in ('shield of righteousness', 'wrathful weapon', 'tattoo of the dawn'): cls = 'Paladin'   # the book's row lost its class label
    app = re.sub(r'\s*1?\s*spellscroll \(3rd circle\)1\s*', ' ', app).replace('not 1actively', 'not actively')
    app = re.sub(r'(\.)\d$', r'\1', app).replace('*+3sword*', '*+3 sword*').replace('*bagof holding*', '*bag of holding*')
    app = app.replace('Not an obvious, but', 'Not an obvious choice, but')
    item = {'rover\'s boots': 'rover’s boots', 'countercharm charm': 'countercharm charm', 'weapon of the Wyrd': 'weapon of the Wyrd'}.get(item, item)
    price = price.replace('1000 gp', '1,000 gp').replace('10,000 + base', '10,000 gp + base')
    fixed.append((tier, cls, item, src, price, app.strip()))
def itemlink(name):
    k = name.lower()
    cands = [k, re.sub(r' \(.*\)$', '', k), k.replace('scroll: ', ''), {'belt of storm giant strength': 'belt of giant strength', 'starry half-plate': 'starry half plate'}.get(k, k)]
    for c in cands:
        if c in idx():
            pg, h = idx()[c]; links.add(name)
            return f'*[[{pg}#{h}\\|{name}]]*'
    return f'*{name}*'
REC_INTRO = between(t, '# Recommended Magic Items by Class', '### Which Creatures Contain Prima Materia?').replace('# Recommended Magic Items by Class\n\n', '').strip()
REC_INTRO = REC_INTRO.replace('The **Recommended Magic Items** tables', 'The tables below')
tier_intro = {}
for n in (1, 2, 3, 4):
    a = f'## Tier {n} Recommended Magic Items'
    b = f'**Tier {n} Recommended Magic Items by Class**'
    tier_intro[n] = between(t, a, b).replace(a, '').strip()
# tier 2 general advice printed between the continued tables
adv = [between(t, 'Every hero wants items that boost', '**Tier 2 Recommended Magic Items by Class (Cont.)**').strip(),
       between(t, 'As always, potions that cure you', '**Tier 2 Recommended Magic Items by Class (Cont.)**').strip()]
tier_intro[2] += '\n\n' + '\n\n'.join(adv)
for n in (3, 4):
    extra = re.findall(r'\n\n([A-Z][^\n|#*>]{40,})(?=\n\n\*\*Tier ' + str(n) + r' Recommended Magic Items by Class \(Cont\.\)\*\*)', t)
    if extra: tier_intro[n] += '\n\n' + '\n\n'.join(e.strip() for e in extra)
def build_rec():
    REC = f'''---
    aliases: [Recommended Magic Items, Magic Items by Class]
    publish: true
    ---
    {OPT}{REC_INTRO}
    
    Each item notes the book it comes from. Items from the *Player’s Guide*, *Player’s Guide 2*, the *Labyrinth Worldbook*, and *Trade Secrets* are linked where the wiki has them.
    '''
    TIER = {1: 'Tier 1 (Levels 1–4)', 2: 'Tier 2 (Levels 5–10)', 3: 'Tier 3 (Levels 11–16)', 4: 'Tier 4 (Levels 17–20)'}
    for n in (1, 2, 3, 4):
        REC += f'\n## Tier {n} Recommended Magic Items\n\n{tier_intro[n]}\n\n| Class | Magic Item | Source | Price | Why It Helps |\n|---|---|---|---|---|\n'
        last = None
        for tier, cls, item, src, price, app in fixed:
            if tier != n: continue
            REC += f'| {"**" + cls + "**" if cls != last else ""} | {itemlink(item)} | {SRC.get(src, "")} | {price} | {app.replace("|", "\\|")} |\n'
            last = cls
    REC = tidy(REC).rstrip() + CREDIT
    return re.sub(r'^    ', '', REC, flags=re.M)
REC = build_rec()

# ---------------- new magic items
mi = between(t, '# New Magic Items', '# New Fabled Items')
mi = rep(mi, '**Pauper’s Grove**\n\n*Wondrous Item, Rare 4,000 gp*', '### Pauper’s Grove\n\n*Wondrous Item, Rare 4,000 gp*')
mi = mi.replace('for up to q hour', 'for up to 1 hour').replace('12,000gp', '12,000 gp')
# move stray tables into their items
lev = between(mi, '**Levers of the Apparatus**\n\n|', '\n\n\n')
fb = between(mi, '| Forward | Back |', '\n\n\n')
mi = mi.replace(lev, '').replace(fb, '')
lrows = [r for r in lev.strip().split('\n')[4:]]; frows = [r for r in fb.strip().split('\n')[2:]]
assert len(lrows) == len(frows) == 2, (lrows, frows)
levers = '**Levers of the Apparatus**\n\n| Lever | Left | Right | Forward | Back |\n|---|---|---|---|---|\n' + ''.join(a.rstrip(' |') + ' | ' + b.strip('| ') + ' |\n' for a, b in zip(lrows, frows))
sk = between(mi, '**Skintaker Cloaks**\n\n|', '\n\n\n'); mi = mi.replace(sk, '')
sk = sk.replace('| Animal Uncommon | Price | AC Bonus | Effects |\n|---|---|---|---|\n', '| Animal | Price | AC Bonus | Effects |\n|---|---|---|---|\n| **Uncommon** |  |  |  |\n')
se = between(mi, '| Spirit Effigy Creature Types Creature Type | Price | Creature Type | Price |', '\n\n\n'); mi = mi.replace(se, '')
srows = [[x.strip() for x in r.strip('|').split('|')] for r in se.strip().split('\n')[2:]]
sflat = [r[:2] for r in srows] + [r[2:] for r in srows if r[2]]
seff = '**Spirit Effigy Creature Types**\n\n| Creature Type | Price |\n|---|---|\n' + ''.join(f'| {a} | {b} |\n' for a, b in sflat)
assert len(sflat) == 23
items = re.split(r'\n### ', '\n' + between(mi, '### Apparatus of the Avian'))[1:]
NEW = {}
for it in items:
    name, body = it.split('\n', 1)
    body = body.strip()
    m = re.match(r'^(\*[^*\n]+\*)\s*(.*)$', body, re.S)
    typ, rest = m.group(1), m.group(2).strip()
    rest = re.sub(r'^\*(\w+)\* ', r'\1 ', rest)
    rest = re.sub(r'^\*([^*]+)\* ', r'\1 ', rest)
    if name == 'Apparatus of the Avian': rest = rest.rstrip() + '\n\n' + levers
    if name == 'Skintaker Cloak': rest = rest.rstrip() + '\n\n' + sk.strip()
    if name == 'Spirit Effigy':
        rest = rep(rest, 'See the **Spirit Effigy Creature Types** table for prices.', 'See the **Spirit Effigy Creature Types** table for prices.\n\n' + seff)
    for a, b in [('lures', 'lures'), ('A second command word revert the tent’s iron to canvas, so it can folded up', 'A second command word reverts the tent’s iron to canvas, so it can be folded up')]:
        rest = rest.replace(a, b)
    NEW[name] = (typ, tidy(rest).strip())
assert len(NEW) == 38, len(NEW)
def page_for(name, typ):
    tl = typ.lower()
    if tl.startswith('*potion'): return 'Potions'
    if tl.startswith('*armor') or tl.startswith('*shield'): return 'Magic Armor'
    if tl.startswith('*weapon'): return 'Magic Weapons'
    return 'Wondrous Items A–L' if name[0].upper() <= 'L' else 'Wondrous Items M–Z'
PLAN = {}
for n, (typ, body) in NEW.items():
    PLAN.setdefault(page_for(n, typ), []).append((n, f'## {n}\n\n*Optional, from Trade Secrets.*\n\n{typ}\n\n{body}\n'))

def insert_items(page, entries):
    p = V + f'/Rules/Magic Items/{page}.md'; s = open(p, encoding='utf-8').read()
    cut = s.rindex('\n---\n*This page includes')
    body, tail = s[:cut], s[cut:]
    for n, block in sorted(entries):
        assert f'\n## {n}\n' not in body, n
        heads = [(m.start(), m.group(1)) for m in re.finditer(r'\n## (.+)\n', body)]
        key = lambda x: re.sub(r'^the ', '', x.lower())
        pos = next((i for i, h in heads if key(h) > key(n) and not h.startswith('More ')), None)
        if pos is None: body = body.rstrip('\n') + '\n\n' + block
        else: body = body[:pos] + '\n' + block + body[pos:]
    tail = tail.rstrip('\n') + '\n' + CR
    open(p, 'w', encoding='utf-8').write(re.sub(r'\n{3,}', '\n\n', body) + tail)

# ---------------- fabled items
fa = between(t, '# New Fabled Items', '# Appendix: Mercantile Tables')
fa_intro = fa.split('\n\n')[1].strip()
fa_items = re.split(r'\n### ', '\n' + between(fa, '### Ancestral Armor'))[1:]
FAB = f'\n## More Fabled Items (Trade Secrets)\n\n*Optional, from Trade Secrets.*\n\n{fa_intro}\n'
for it in fa_items:
    name, body = it.split('\n', 1)
    body = body.strip()
    m = re.match(r'^(\*[^*\n]+\*)\s*(.*)$', body, re.S)
    body = m.group(1) + '\n\n' + m.group(2).strip()
    FAB += f'\n## {name}\n\n{tidy(body).strip()}\n'
FAB = FAB.replace('can be summoned for 8 before disappearing', 'can be summoned for 8 hours before disappearing') if 'for 8 before' in FAB else FAB
FAB = linkitalics(FAB, links)

# ---------------- appendix (GM)
ap = between(t, '# Appendix: Mercantile Tables', '# MORE PATHS.')
GM = '---\npublish: false\n---\n*From Trade Secrets, appendix. Quick d20 tables for markets, merchants, and trade.*\n\n' + tidy(ap.replace('# Appendix: Mercantile Tables', '').strip()) + '\n'

if not WRITE:
    for k, v in [('DIS', DIS), ('REC', REC), ('FAB', FAB), ('GM', GM)]: open(f'/home/claude/ts/out5_{k}.md', 'w').write(v)
    with open('/home/claude/ts/out5_ITEMS.md', 'w') as f:
        for pg, es in PLAN.items():
            f.write(f'\n\n######## {pg}\n'); [f.write(b + '\n') for _, b in es]
    print('linked', sorted(links)); print({k: [n for n, _ in v] for k, v in PLAN.items()})
else:
    open(V + '/Rules/Trade Secrets/Disenchanting.md', 'w', encoding='utf-8').write(DIS)
    open(V + '/_GM Only/Trade Secrets/Mercantile Tables (GM).md', 'w', encoding='utf-8').write(GM)
    for pg, es in PLAN.items(): insert_items(pg, es)
    p = V + '/Rules/Magic Items/Fabled Magic Items.md'; s = open(p, encoding='utf-8').read()
    assert 'Trade Secrets)' not in s
    i = s.rindex('\n---\n*This page includes')
    s = s[:i].rstrip('\n') + '\n' + FAB.rstrip('\n') + '\n' + s[i:].rstrip('\n') + '\n' + CR
    open(p, 'w', encoding='utf-8').write(s)
    import common; common._idx = None
    REC = build_rec()
    open(V + '/Rules/Magic Items/Recommended Magic Items by Class.md', 'w', encoding='utf-8').write(REC)
