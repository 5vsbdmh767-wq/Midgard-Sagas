# Trade Secrets chapter 4 (PDF pages 88-118): gear, structures, tools, weapons, armor.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *
import stream
PDF = '/mnt/user-data/uploads/Trade-Secrets.pdf'
t = stream.render(PDF, 88, 118)
t = re.sub(r'\*\*\*([^*\n]+?)\*\*\*\*\*\.\*\*', r'***\1.***', t)
t = re.sub(r'\*\*\*([^*\n]+?)\*\*\*\.', r'***\1.***', t)
t = re.sub(r'\*\*\*([^*\n]+?)\*\*\*\*\.\*', r'***\1.***', t)
links = set()
CR = '\n*Material marked as from Trade Secrets is from Trade Secrets by Kobold Press.*\n'

def strip_tables(x):
    return re.sub(r'(?:\*\*[^\n]+\*\*\n\n)?(?:\|[^\n]*\|\n)+(?:\n\\\*[^\n]*\n)?', '', x)

# ---------------- gear
gear = between(t, '# New Adventuring Gear', '# Structures')
def merged(sec, n):
    tabs = re.findall(r'((?:\|[^\n]*\|\n)+)', sec)
    items = [r for r in tabs[0].strip().split('\n')[2:]]
    times = [r for r in tabs[1].strip().split('\n')[2:]]
    assert len(items) == n == len(times), (len(items), len(times), n)
    out = '| Item | Cost | Weight | Crafting Time | Crafting DC |\n|---|---|---|---|---|\n'
    for a, b in zip(items, times):
        out += a.rstrip(' |') + ' | ' + b.strip('| ').replace('*', '\\*') + ' |\n'
    return out.replace('200gp', '200 gp')
FOOT = '\\* After the initial preparation time (10% of the total time), this item does not require frequent supervision to craft.\n'
def gsec(h, nxt, n, title):
    s = between(gear, h, nxt)
    intro = s.split('\n\n')[1]
    tab = merged(s, n)
    body = strip_tables(s.replace(h, '', 1).replace(intro, '', 1))
    body = body.replace(FOOT, '')
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    return f'{intro}\n\n**{title}**\n\n{tab}\n{FOOT}\n{body}\n'
prov = gsec('## New Provisions', '## New Alchemical Items', 13, 'New Provisions')
alch = gsec('## New Alchemical Items', '## New Herbal Concoctions', 15, 'New Alchemical Items')
herb = gsec('## New Herbal Concoctions', '## New Mechanical Devices', 12, 'New Herbal Concoctions')
mech_s = between(gear, '## New Mechanical Devices', '## New Equipment Packs')
timer = between(mech_s, '### Timer Duration', 'Setting a timer trigger correctly')
mech_s = mech_s.replace(timer, '')
d12 = between(mech_s, '| d12 | Time Delay |', '\n\n'); mech_s = mech_s.replace(d12, '')
mech = gsec_text = None
intro = mech_s.split('\n\n')[1]
mtab = merged(mech_s, 12)
mbody = strip_tables(mech_s.replace('## New Mechanical Devices', '', 1).replace(intro, '', 1)).replace(FOOT, '')
mbody = re.sub(r'\n{3,}', '\n\n', mbody).strip()
mbody = rep(mbody, 'A timer can be trigger after', 'A timer can be triggered after')
timer_box = ('> [!note] Timer Duration\n> When you set a timer on a trap, choose one of the listed durations for when the trap triggers.\n>\n'
             '> You can use these durations to determine how soon a trap triggers when the character setting the trap fails their WIS (Trapper Tools) check, '
             'rolling a d12 on this chart, and either adding or subtracting that amount from the intended time.\n>\n'
             + ''.join('> ' + l + '\n' for l in d12.strip().split('\n')))
for w in ['When you set a timer on a trap, choose one of the listed durations for', 'rolling a d12 on this chart, and either adding or subtracting that amount']: assert w in timer, w
for w in ['| 1–4 | 1–10 rounds |', '| 12 | 1 hour |']: assert w in d12, w
mech = f'{intro}\n\n**New Mechanical Devices**\n\n{mtab}\n{FOOT}\n{mbody}\n\n{timer_box}'
packs = between(gear, '## New Equipment Packs').replace('## New Equipment Packs\n\n', '')
packs = re.sub(r'^\*\*([^*]+?) \((\d+ gp)\)\.\*\*', r'***\1 (\2).***', packs, flags=re.M)
packs = rep(packs, '1 days of rations', '1 day of rations')
gear_intro = between(gear, 'For those merchants who cater', '## New Provisions').strip()
fixes = [('This lure can be set in place', 'This lure can be set in place'), ('lures insect to it', 'lures insects to it'),
         ('Since this potion provide no', 'Since this potion provides no'), ('Any WIS (Medicine) checks to treat the injured character has advantage', 'Any WIS (Medicine) checks to treat the injured character have advantage'),
         ('***Marching Meal***.', '***Marching Meal.***'), ('***Puzzling Padlock***.', '***Puzzling Padlock.***'), ('This concentrated alchemist’s fire is quite sludgy goo', 'This concentrated alchemist’s fire is a sludgy goo'),
         ('(instead of one- quarter', '(instead of one-quarter'), ('the tumbler- tickler', 'the tumbler-tickler')]
G = f'''
## More Adventuring Gear (Trade Secrets)

*Optional, from Trade Secrets.*

{gear_intro}

### Provisions

{prov}
### Alchemical Items

{alch}
### Herbal Concoctions

{herb}
### Mechanical Devices

{mech}
### Equipment Packs

{packs.strip()}
'''
for a, b in fixes:
    if a in G: G = G.replace(a, b)
G = linkitalics(tidy(G), links)

# ---------------- tools
tools = between(t, '# Expanded Tool Uses', '# Weapons')
tl_intro = between(tools, 'Nearly every profession', '## Tool Limitations').strip()
lim = between(tools, '## Tool Limitations', '## Big Projects').strip()
big = between(tools, '## Big Projects', '## Creating Tools').strip()
cre = between(tools, '## Creating Tools', '## New Tool Challenges').strip()
ch = between(tools, '## New Tool Challenges')
ch = ch.replace('| Besty bond | 25 gp | — |\n| (1-ounce bottle) |  |  |', '| Besty bond (1-ounce bottle) | 25 gp | — |')
ch = ch.replace('| Disappearing ink | 15 gp | — |\n| (1-ounce bottle) |  |  |', '| Disappearing ink (1-ounce bottle) | 15 gp | — |')
ch = ch.replace('| Drink and dye | 50 gp | ½ lb. |\n| (4-ounce bottle) |  |  |', '| Drink and dye (4-ounce bottle) | 50 gp | ½ lb. |')
ch = rep(ch, '| Identify the ingredients of food and drink by | 10 |\n| taste or smell |  |', '| Identify the ingredients of food and drink by taste or smell | 10 |')
ch = rep(ch, '| Painted vase | 15 gp | l lb. |', '| Painted vase | 15 gp | 1 lb. |')
ch = rep(ch, '### Navigation Tools', '### Navigator Tools')
ch = rep(ch, '**Navigation Tools New Example Tasks**', '**Navigator Tools New Example Tasks**')
ch = rep(ch, '**Iron Goods**\n\n| Metalwork | Cost | Weight |\n|---|---|---|\n| Auto-hammer', '**Tinker Devices**\n\n| Device | Cost | Weight |\n|---|---|---|\n| Auto-hammer')
ch = rep(ch, '**Alchemical Tools New Example Tasks**', '**Alchemist Tools New Example Tasks**')
ch = re.sub(r'^\*([A-Z][^*\n]{1,40}?)\.\*', r'***\1.***', ch, flags=re.M)
ch = re.sub(r'^\*([A-Z][^*\n]{1,40}?)\*\.', r'***\1.***', ch, flags=re.M)
ch = ch.replace('## New Tool Challenges', '### New Tool Challenges').replace('\n### ', '\n#### ').replace('#### New Tool Challenges', '### New Tool Challenges', 1)
for a, b in [('it instantly extinguished the flames', 'it instantly extinguishes the flames'), ('in colder climbs', 'in colder climes'), ('The hook us used', 'The hook is used')]:
    if a in ch: ch = ch.replace(a, b)
T = f'''
## More Tool Uses (Trade Secrets)

*Optional, from Trade Secrets.*

{tl_intro}

{demote(big)}

{ch.strip()}
'''
T = linkitalics(tidy(T), links)

# ---------------- weapons
wp = between(t, '# Weapons', '**Armor**\n')
wt_intro = between(wp, 'The listed additional weapons', '## Weapon Types').strip()
descs = re.findall(r'^\*([^*]+?) \(((?:Simple|Martial|Marital)[^)]*?)\)\.?\*\.? ?(.+)$', wp, re.M)
descs += [(a, b, c) for a, b, c in re.findall(r'^\*([^*]+?) \(((?:Simple|Martial)[^)*]*?)\*\)\. (.+)$', wp, re.M)]
D = {}
for n, k, txt in descs: D[n.strip()] = (k.replace('Marital', 'Martial'), txt.strip())
SKIP = {'Garrote', 'Hook Swords', 'Net', 'Rope Dart'}
order = sorted(D)
assert len(D) == 24, sorted(D)  # the book gives no description for the sabre
wdesc = '\n\n'.join(f'***{n} ({D[n][0]}).*** {D[n][1]}' for n in order if n not in SKIP)
W = [('Simple Melee Weapons', [('Bayonet', '3 gp', '1d6 piercing', '1 lb.', 'Hamstring', 'Two-handed'), ('Cat o’ nine tails', '10 gp', '1d4 bludgeoning', '4 lb.', 'Disarm, Trip', '—'),
      ('Gaff', '4 sp', '1d6 piercing', '3 lb.', 'Trip', 'Reach, Two-handed'), ('Hairpin', '1 sp', '1 piercing', '0 lb.', '—', 'Disguised, Finesse, Light'), ('Hot iron', '1 gp', '1d4 bludgeoning', '2 lb.', 'Bash, Brand', 'Hot'),
      ('Jitte', '2 gp', '1d4 bludgeoning', '1 lb.', 'Bash, Disarm, Grappling', 'Defensive, Finesse, Light'), ('Monkey’s fist', '1 sp', '1d4 bludgeoning', '1 lb.', 'Bash, Grappling', 'Finesse, Light'),
      ('Pitchfork', '1 sp', '1d4 piercing', '3 lb.', 'Pinning Shot, Trip', 'Reach, Two-handed'), ('Tiger claws', '5 gp', '1d4 slashing', '1 lb.', '—', 'Finesse, Light, Secure'),
      ('Throwing stick', '1 sp', '1d4 bludgeoning', '1 lb.', 'Bash', 'Light, Thrown (range 60/180 ft.)'), ('War fan', '4 gp', '1d4 bludgeoning', '2 lb.', 'Bash, Disarm', 'Defensive, Disguised, Finesse, Light')]),
     ('Simple Ranged Weapons', [('Bolo', '2 sp', '1d4 bludgeoning', '1 lb.', 'Trip', 'Thrown (range 20/60 ft.)')]),
     ('Martial Melee Weapons', [('Aruval', '13 gp', '1d8 slashing', '3 lb.', 'Hamstring, Trip', '—'), ('Broadsword', '15 gp', '1d8 slashing', '3 lb.', 'Bash, Disarm, Hamstring', '—'),
      ('Fire lance', '25 gp', '1d8 piercing', '4 lb.', 'Distract, Trip', 'Reach, Thrown (30/90 ft.), Two-handed'), ('Guisarme', '20 gp', '1d10 piercing', '6 lb.', 'Pull, Hamstring, Trip', 'Heavy, Reach, Two-handed'),
      ('Katar', '5 gp', '1d6 piercing', '1 lb.', '—', 'Finesse, Light, Secure'), ('Lucerne hammer', '25 gp', '1d10 piercing', '6 lb.', 'Bash, Trip', 'Heavy, Reach, Two-handed'),
      ('Pistol sword, pistol\\*', '150 gp', '1d6 piercing', '4 lb.', '', 'Ammunition (range 20/80 ft.), Gunpowder, Loading'), ('Poleaxe', '20 gp', '1d10 slashing', '4 lb.', 'Bash, Disarm, Hamstring, Trip', 'Heavy, Two-handed'),
      ('Sabre', '20 gp', '1d8 slashing', '2.5 lb.', 'Bash, Disarm, Hamstring', 'Finesse, Secure')]),
     ('Martial Ranged Weapons', [('Pistol sword, sword\\*', '150 gp', '1d8 slashing', '4 lb.', '', '—')])]
# verify the hand table against the extracted text
for grp, rows in W:
    for r in rows:
        nm = r[0].replace('\\*', '*').replace('’ ', ' ').replace('Lucerne hammer', 'Lucerne Hammer').replace('Cat o nine', 'Cat o nine')
        line = [l for l in t.split('\n') if l.startswith('| ' + nm.replace('Cat o’ nine', 'Cat o nine') + ' |')]
        assert line, nm
        c = [x.strip() for x in line[0].strip('|').split('|')]
        assert c[1].rstrip('.') == r[1] and c[2].replace('piecing', 'piercing') == r[2] and c[3] == r[3], (nm, c, r)
wtab = '**Weapons (Trade Secrets)**\n\n| Weapon | Cost | Damage | Weight | Weapon Options | Properties |\n|---|---|---|---|---|---|\n'
for grp, rows in W:
    wtab += f'| **{grp}** |  |  |  |  |  |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in rows)
wtab += '\n\\* The listings for “Pistol sword, pistol” and “Pistol sword, sword” are the same item showing different attack modes.\n'
opts = between(wp, '## Weapon Options', '## Weapon Materials')
mats = between(wp, '## Weapon Materials', '## Weapon Properties')
props = between(wp, '## Weapon Properties')
props_tail = between(t, '*Linked.* This set of two weapons', '# Armor')
def lab(x): return re.sub(r'^\*([A-Z][^*\n]{1,30}?)\.\*', r'***\1.***', x, flags=re.M)
props_all = lab(props.strip() + '\n\n' + props_tail.strip())
props_all = re.sub(r'\*\*\*Linked\.\*\*\*[^\n]*\n\n', '', props_all)
props_all = re.sub(r'\n?\*\*\*Strangling\.\*\*\*[^\n]*', '', props_all)
props_all = props_all.replace('## Weapon Properties', '### Weapon Properties (Trade Secrets)')
WEAP = f'''
## More Weapons (Trade Secrets)

*Optional, from Trade Secrets.*

{wt_intro}

### Weapon Types (Trade Secrets)

Each weapon is categorized into a type associated with a proficiency, either simple or martial.

{wdesc}

{wtab}
{lab(opts).replace('## Weapon Options', '### Weapon Options (Trade Secrets)').strip()}

{lab(mats).replace('## Weapon Materials', '### Weapon Materials (Trade Secrets)').strip()}

{props_all.strip()}
'''
WEAP = rep(WEAP, '***Brand.***', '***Brand.***')
WEAP = linkitalics(tidy(WEAP), links)

# ---------------- armor
ar = between(t, '# Armor\n')
a_intro = between(ar, 'The listed additional types of armor', '## Armor Types').strip()
ad = re.findall(r'\*([A-Z][^*(]+?) \(((?:Light|Medium|Heavy) Armor|Shield)\)\.\* ?([^\n*]+(?:\n(?!\n)[^\n]+)*)', ar)
AD = {n.strip(): (k, x.strip()) for n, k, x in ad}
assert len(AD) == 9, sorted(AD)  # the book gives no description for the scutum
A = [('Light Armor', [('Fashionable armor', '20 gp', '11 + DEX modifier', '6 lb.', '—')]),
     ('Medium Armor', [('Bone', '15 gp', '13 + DEX modifier (max 2)', '20 lb.', 'Cumbersome (STR 13), Natural Materials'), ('Lamellar', '40 gp', '14 + DEX modifier (max 2)', '40 lb.', 'Cumbersome (STR 13), Noisy')]),
     ('Heavy Armor', [('Wooden plate', '5 gp', '14', '45 lb.', 'Buoyant, Cumbersome (STR 16), Natural Materials')]),
     ('Shields', [('Buckler', '5 gp', '+1', '3 lb.', 'Offensive'), ('Leather shield', '1 gp', '+1', '1 lb.', 'Natural Materials'), ('Musket shield', '70 gp', '+2', '15 lb.', 'Two-handed'),
                  ('Pavise', '20 gp', '+3', '15 lb.', 'Cover, Two-handed'), ('Scutum', '15 gp', '+2', '8 lb.', 'Interlocking'), ('Spike shield', '10 gp', '+1', '4 lb.', 'Spiked')])]
atab = '**Armor (Trade Secrets)**\n\n| Armor | Cost | Armor Class (AC) | Weight | Properties |\n|---|---|---|---|---|\n'
for g, rows in A: atab += f'| **{g}** |  |  |  |  |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in rows)
amat = lab(between(ar, '## Armor Materials', '## Armor Properties')).replace('## Armor Materials', '### Armor Materials (Trade Secrets)')
aprop = lab(between(ar, '## Armor Properties')).replace('## Armor Properties', '### Armor Properties (Trade Secrets)')
ARM = f'''
## More Armor (Trade Secrets)

*Optional, from Trade Secrets.*

{a_intro}

### Armor Types (Trade Secrets)

Armor is categorized into four types: light, medium, heavy, and shield. You need proficiency in the relevant armor type to use it well (as described in the *Player’s Guide*).

{chr(10).join(f"***{n} ({AD[n][0]}).*** {AD[n][1]}" + chr(10) for n in sorted(AD))}
{atab}
{amat.strip()}

{aprop.strip()}
'''
ARM = tidy(ARM)

# ---------------- structures (player page)
st = between(t, '# Structures', '# Expanded Tool Uses')
st = st.replace('# Structures\n\n', '')
st = between(st, '## Setting Up Shop\n\n').replace('## Setting Up Shop\n\n', '')
# effects for the two shop component tables
comp = between(st, '### Components', '### Location')
eff = re.findall(r'(\| Effect \|\n\|---\|\n(?:\|[^\n]*\|\n)+)', st)
assert len(eff) == 2, len(eff)
e1 = [r.strip('| ') for r in eff[0].strip().split('\n')[2:]]
e2 = [r.strip('| ') for r in eff[1].strip().split('\n')[2:]]
loc_eff = re.findall(r'(\| Effect \|\n\|---\|\n(?:\|[^\n]*\|\n)+)', st)
t1 = between(comp, '**Shop Components**\n', '\n\n')
t2 = between(comp, '**Shop Components (Cont.)**\n', '\n\n')
r1 = [l for l in t1.strip().split('\n') if l.startswith('| ') and not l.startswith('| Item |')]
r2 = [l for l in t2.strip().split('\n') if l.startswith('| ') and not l.startswith('| Item |')]
assert len(r1) == 24 == len(e1), (len(r1), len(e1))
assert len(r2) == 24 == len(e2), (len(r2), len(e2))
# the second "Effect" list printed under Location belongs to the continued table (checked against the page image)
assert e2[1] == '+2% to maximum Stake' and e2[14] == 'Advantage on Commerce Resolution'
ct = '**Shop Components**\n\n| Item | Cost | Effect |\n|---|---|---|\n' + ''.join(a.rstrip(' |') + ' | ' + b + ' |\n' for a, b in zip(r1 + r2, e1 + e2))
for e in eff: st = st.replace(e, '')
st = st.replace(t1, '').replace(t2, '').replace('**Shop Components**\n\n\n', '').replace('**Shop Components (Cont.)**\n\n\n', '')
st = st.replace('**Shop Components**\n\n', '', 1) if st.count('**Shop Components**') > 1 else st
for lab_ in ['Signage', 'Awning', 'Heating', 'Lighting', 'Display Cases', 'Decorations', 'Merchant’s Cage', 'Alarms', 'Lockboxes', 'Reputation']:
    st = re.sub(r'(^|\n)' + re.escape(lab_) + r'\. ', r'\1***' + lab_ + '.*** ', st)
st = rep(st, ' ***Shelving.***', '\n\n***Shelving.***')
st = rep(st, '3 pounds. Safes. A safe or keeps', '3 pounds.\n\n***Safes.*** A safe keeps')
st = re.sub(r'^\*\*•\*\* ', '- ', st, flags=re.M)
st = re.sub(r'^\*\*•\*\* ?', '- ', st, flags=re.M)
st = rep(st, '\n\n### Location', '\n\n' + ct + '\n### Location')
sb = between(st, '### Stake Limit by Shop Size', '***Pavilion.***')
st = st.replace(sb, '')
st = rep(st, '### Mobile Shops', '> [!note] Stake Limit by Shop Size\n> Although a pound of diamonds is obviously worth more than a pound of flour, the Stake Limits listed in this section assume goods that sell for about 1 gp per pound. If a PC wishes to deal in goods that are worth more or less than that rough equivalent, multiply or divide the Stake Limit by up to 100.\n\n### Mobile Shops')
assert 'multiply or' in sb and 'divide the Stake Limit by up to 100' in sb
st = rep(st, '**Shop Components**\n\n| Item | Cost | Stake Limit | Hireling Limit |', '**Mobile Shops**\n\n| Item | Cost | Stake Limit | Hireling Limit |')
st = rep(st, '**Workshops, Factories, And Farms**', '**Workshops, Factories, and Farms**')
st = rep(st, 'This mechanic is described in more detail under **Running a Business**.', 'This mechanic is described in more detail under [[Running a Business]].')
st = rep(st, 'per the rules in **Chapter 1**.', 'per the rules in [[Running a Business]].')
st = st.replace('(See **Running a Business**.)', '(See [[Running a Business]].)')
st = st.replace('for **Running a Business**.', 'for [[Running a Business]].')
for a, b in [('(and your customers) needs', '(and your customers) need'), ('boats of this size are have', 'boats of this size have'), ('100-square- foot', '100-square-foot'), ('2,500-square- foot', '2,500-square-foot'), ('— from unauthorized', '—from unauthorized')]:
    if a in st: st = st.replace(a, b)
st = re.sub(r'^#(#+) ', r'\1 ', st, flags=re.M)
SHOP = f'''---
aliases: [Structures, Shop Components, Renting a Shop]
publish: true
---
{OPT}Before a business can operate, it needs someplace to conduct its business. This page covers financing a business, building it from components, choosing a location, and buying or renting a shop, workshop, factory, or farm. For the daily rules of making money, see [[Running a Business]].

{st.strip()}
'''
SHOP = rep(SHOP, 'Before a business can operate, it needs someplace to conduct its business. From modest', 'From modest') if SHOP.count('Before a business can operate') == 2 else SHOP
def unfold(m):
    hdr = m.group(1); rows = m.group(2).strip().split('\n')
    L = []; R = []
    for row in rows:
        c = [x.strip() for x in row.strip('|').split('|')]
        L.append(c[:2])
        if c[2]: R.append(c[2:])
    return f'| {hdr} | DC |\n|---|---|\n' + ''.join(f'| {a} | {b} |\n' for a, b in L + R)
SHOP = re.sub(r'\| ([^|]+?) \| DC \| \1 \| DC \|\n\|---\|---\|---\|---\|\n((?:\|[^\n]*\|\n)+)', unfold, SHOP)
SHOP = rep(SHOP, '- Eviction Notice: ', '- ***Eviction Notice:*** ')
SHOP = linkitalics(tidy(SHOP), links).rstrip() + CREDIT

# ---------------- write
def append(path, block, credit_after):
    p = V + path; s = open(p, encoding='utf-8').read()
    assert 'Trade Secrets)' not in s, path
    i = s.rindex('\n---\n*This page includes material')
    s = s[:i].rstrip('\n') + '\n' + block.rstrip('\n') + '\n' + s[i:]
    s = s.rstrip('\n') + '\n' + CR
    open(p, 'w', encoding='utf-8').write(s)
if '--write' in sys.argv:
    append('/Rules/Equipment/Adventuring Gear.md', G, True)
    append('/Rules/Equipment/Tools.md', T, True)
    append('/Rules/Equipment/Weapons.md', WEAP, True)
    append('/Rules/Equipment/Armor.md', ARM, True)
    open(V + '/Rules/Trade Secrets/Setting Up Shop.md', 'w', encoding='utf-8').write(SHOP)
    gm = f'''---
publish: false
---
*From Trade Secrets, chapter 4. GM advice on tools. The player-facing rules from this chapter are on [[Adventuring Gear#More Adventuring Gear (Trade Secrets)|Adventuring Gear]], [[Tools#More Tool Uses (Trade Secrets)|Tools]], [[Weapons#More Weapons (Trade Secrets)|Weapons]], [[Armor#More Armor (Trade Secrets)|Armor]], and [[Setting Up Shop]].*

{demote(lim)}

{demote(cre)}
'''
    open(V + '/_GM Only/Trade Secrets/Equipment Expanded (GM).md', 'w', encoding='utf-8').write(tidy(gm))
else:
    for name, x in [('G', G), ('T', T), ('WEAP', WEAP), ('ARM', ARM), ('SHOP', SHOP)]:
        open(f'/home/claude/ts/out_{name}.md', 'w').write(x)
    print('linked', sorted(links))

if '--write' in sys.argv:
    s = open(V + '/Rules/Trade Secrets/Setting Up Shop.md', encoding='utf-8').read()
    s = rep(s, '| 101−200 gp |', '| 100−200 gp |', 3)
    open(V + '/Rules/Trade Secrets/Setting Up Shop.md', 'w', encoding='utf-8').write(s)
    p = V + '/Rules/Trade Secrets/Running a Business.md'; s = open(p, encoding='utf-8').read()
    s = rep(s, '**Structures** in **Chapter 4** has more information', '[[Setting Up Shop]] has more information')
    s = rep(s, '**Structures** in **Chapter 4** for more information.', '[[Setting Up Shop]] for more information.')
    s = rep(s, '(see **Structures**)', '(see [[Setting Up Shop]])')
    s = rep(s, '**Structures** rules in **Chapter 4**', '[[Setting Up Shop]] rules')
    open(p, 'w', encoding='utf-8').write(s)
    p = V + '/Rules/Trade Secrets/Trade Secrets.md'; s = open(p, encoding='utf-8').read()
    s = rep(s, '- [[Running a Business]]: investing, securing supply, hiring staff, and the Running a Business downtime activity\n',
            '- [[Running a Business]]: investing, securing supply, hiring staff, and the Running a Business downtime activity\n- [[Setting Up Shop]]: financing, shop components, location, mobile and permanent shops, workshops, factories, farms, and renting\n')
    s = rep(s, '- [[Batch Crafting]]: fourteen downtime activities for brewing, farming, mining, smithing, and other trades\n',
            '- [[Batch Crafting]]: fourteen downtime activities for brewing, farming, mining, smithing, and other trades\n\n## Gear\n'
            '- [[Adventuring Gear#More Adventuring Gear (Trade Secrets)|New adventuring gear]]: provisions, alchemical items, herbal concoctions, mechanical devices, and equipment packs\n'
            '- [[Tools#More Tool Uses (Trade Secrets)|New tool uses]]: big projects, and new goods and tasks for every tool set\n'
            '- [[Weapons#More Weapons (Trade Secrets)|New weapons]] and [[Armor#More Armor (Trade Secrets)|new armor]]\n')
    open(p, 'w', encoding='utf-8').write(s)
