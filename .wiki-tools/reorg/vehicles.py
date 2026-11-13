# Stage 2: one cost table and one alphabetical list of vehicle descriptions on Rules/Equipment/Vehicles.md.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Equipment/Vehicles.md'
old = read(P); front, body = split_front(old); body, footer = split_footer(body)
top = sections(body, 2); S = dict(top)
def sub(text): return sections(text, 3)
# --- core rules sections
elements = sub(S['Elements of a Vehicle'])
pg2 = paragraphs(strip_src(S["More Vehicles (Player's Guide 2)"]))
prof, resil = pg2[1], pg2[2]; assert prof.startswith('***Vehicle Proficiency') and resil.startswith('***Vehicle Resilience')
lab = sub(S['More Vehicles (Labyrinth Worldbook)'])
lab_intro = paragraphs(strip_src(lab[0][1]))
using = dict(lab)['Using Vehicles']
airnote = re.search(r'> \[!note\] Introducing Air Vehicles\n(?:>.*\n?)+', using).group(0).strip()
culture = re.search(r'\*\*Common Vehicles by Culture\*\*\n\n((?:\|.*\n?)+)', using).group(1)
labcost = re.search(r'\*\*Vehicle Base Costs\*\*\n\n((?:\|.*\n?)+)\n(\*While[^\n]+)', using)
lab_veh = dict(lab)['Vehicles of the Labyrinth'].strip()
north = sub(S['More Vehicles (Northlands Worldbook)'])
nland = dict(north)['Land Vehicles']
ntab = re.search(r'\*\*Land Vehicles \(Northlands Worldbook\)\*\*\n\n((?:\|.*\n?)+)', nland)
nland_text = nland[:ntab.start()].strip()
# --- descriptions
desc = {}
def take(secs, src=None):
    for h, t in secs:
        if h is None or h in ('Using Vehicles', 'Vehicles of the Labyrinth', 'Land Vehicles'): continue
        t = strip_src(t).strip()
        desc[h] = (src, t)
core_desc = sub(S['Vehicle Descriptions']); take(core_desc)
take(sub(S["Vehicle Descriptions (Player's Guide 2)"]), "Player's Guide 2")
take(sub(S['Vehicle Descriptions (Labyrinth Worldbook)']), 'Labyrinth Worldbook')
take(north, 'Northlands Worldbook')
assert len(desc) == 5 + 4 + 6 + 8, len(desc)
# --- cost table
cost = {'Air': [], 'Land': [], 'Water': []}
def add(tbl):
    cat = None
    for r in table_rows(tbl)[2:]:
        if r[0].endswith(' Vehicles') and not r[1]: cat = r[0].split()[0]; continue
        cost[cat].append(r)
add(re.search(r'\*\*Vehicle Base Cost\*\*\n\n((?:\|.*\n?)+)', core_desc[0][1]).group(1))
add(re.search(r'\*Vehicle\*\n\n((?:\|.*\n?)+)', sub(S["Vehicle Descriptions (Player's Guide 2)"])[0][1]).group(1))
add(labcost.group(1))
cost['Land'] += [['Dog sled', '50 gp, plus 50 gp per dog', '5 mph'], ['Ogre war sled', '1,800 gp', '4 mph']]
for n in ('Drakkar', 'Karvi', 'Knarr', 'Skeid', 'Snekkja'):
    mph = re.search(r'\*\*Speed\*\* [^\n]*?(\d+ mph)', desc[n][1]).group(1)
    cost['Water'].append([f'Longship, {n.lower()}', '—', mph])
name = lambda r: re.sub(r'\[\[[^\]]*\\\|([^\]]*)\]\]', r'\1', r[0])
rows = []
for cat in ('Air', 'Land', 'Water'):
    rows.append(f'| **{cat} vehicles** |  |  |')
    for r in sorted(cost[cat], key=lambda r: key(name(r))):
        n = name(r); target = n.split(', ')[-1].title() if n.startswith('Longship') else n.replace(' (unarmed)', '')
        target = next(h for h in desc if h.lower() == target.lower())
        rows.append(f'| [[#{target}\\|{n}]] | {r[1]} | {r[2]} |')
ctable = '**Vehicle Base Cost**\n\n| Vehicle | Cost | Travel Speed (per Hour) |\n|---|---|---|\n' + '\n'.join(rows) + '\n\n\\' + labcost.group(2)
csrc = ("%% sources: Player's Guide 2: canoe, chariot, gnomish balloon, river barge; Labyrinth Worldbook: astral galleon, clockwork cart, dead chariot, infernal barque, sky ship, Styx gondola; "
        "Northlands Worldbook: dog sled, ogre war sled and the five longships (the book gives longships no price) %%")
# --- culture table: drop the book column, link what this page describes
crow = []
gmg = []
for r in table_rows(culture)[2:]:
    if not r[1]: crow.append(f'| **{r[0].lower().capitalize()}** |  |'.replace('vehicles', 'vehicles')); continue
    n = name(r)
    if n in desc: v = f'[[#{n}\\|{n}]]'
    elif n == 'War Wagon' or n == 'Keelboat': v = f'[[#{n}\\|{n}]]'
    else: v = r[0]; gmg.append(n)
    crow.append(f'| {v} | {r[1]} |')
cult = '**Common Vehicles by Culture**\n\n| Vehicle | Used By… |\n|---|---|\n' + '\n'.join(crow)
cult_src = '%% source: Labyrinth Worldbook. Not described on this wiki (Game Master’s Guide): ' + ', '.join(gmg) + ' %%'
lab_veh2 = lab_veh.split(' If a vehicle isn’t included')[0].replace(' (see **Chapter 1**)', '')
# --- assemble
out = []
for h, t in top:
    if h is None: out.append(t); continue
    if h == 'Elements of a Vehicle':
        out.append('## ' + h)
        for h3, t3 in elements:
            if h3 is None: out.append(t3); continue
            out += ['### ' + h3, t3]
            if h3 == 'Type': out += [airnote, '%% source: Labyrinth Worldbook (the note above) %%']
        out += ['### Proficiency and Resilience', "%% source: Player's Guide 2 %%", prof, resil]
    elif h in ('Vehicle Movement', 'Vehicle Repairs'): out += ['## ' + h, t]
    elif h == 'Vehicle Descriptions':
        out += ['## Vehicle Descriptions', 'This section contains a selection of vehicles, including their descriptions and stat blocks.', ctable, csrc]
        for n in sorted(desc, key=key):
            src, t = desc[n]
            out += ['### ' + n] + (['%% source: ' + src + ' %%'] if src else []) + [t]
out += ['## Vehicles by Region', '### The Labyrinth', '%% source: Labyrinth Worldbook %%'] + lab_intro + [lab_veh2, cult, cult_src]
out += ['### The Northlands', '%% source: Northlands Worldbook %%', nland_text, '**Northern Land Vehicles**\n\n' + ntab.group(1).strip(),
        'For the ships of the North, see [[#Longships]].']
new = front + '\n\n'.join(x for x in out if x.strip()) + '\n\n' + footer + '\n'
new = new.replace('The longships presented in this section differ', 'The longships presented here differ').replace('Much like the longships presented later, the', 'Much like the longships, the')
for m in re.finditer(r'^> \[!note\] (.+)$', old, re.M): assert m.group(0) in new, m.group(0)
for m in re.finditer(r'^(?:> )?\*\*\*([^*\n]+?)\.?\*\*\*', old, re.M): assert m.group(0) in new, m.group(0)
print(len(old.split('\n')), '->', len(new.split('\n')), 'descriptions', len(desc), 'not on wiki:', gmg)
if '--write' in sys.argv: write(P, new)
else: open('/home/claude/ts/vehicles_new.md', 'w').write(new)
