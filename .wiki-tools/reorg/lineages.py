# Stage 4: one page per lineage under Rules/Characters/Lineages/, with versions, variants and extra adaptations on that page.
import sys, os, re, difflib, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Characters/Lineages.md'; OUT = 'Rules/Characters/Lineages/'
old = read(P); front, body = split_front(old); body, foot = split_footer(body)
top = sections(body, 2); S = dict(top)
PLACE = {'Labyrinth': 'Labyrinth', 'Lineages & Heritages': 'Midgard', 'Northlands': 'Northlands'}
SUITS = {None: 'Any character', "Player's Guide 2": 'Any character', 'Tales of the Old Margreve': 'The [[The Margreve\\|Margreve]] forest', 'Labyrinth Worldbook': 'The [[The Labyrinth\\|Labyrinth]]',
         'Lineages & Heritages': 'Midgard', 'Northlands Worldbook': 'The [[Northlands]]', 'Book of Ebon Tides': 'The [[The Shadow Realm\\|Shadow Realm]]', 'Night Hunters': 'Horror campaigns'}
PEOPLE = {'Dwarf': 'Dwarves', 'Elf': 'Elves', 'Human': 'Humans', 'Kobold': 'Kobolds', 'Orc': 'Orcs', 'Syderean': 'Sydereans', 'Elemental Scion': 'Elemental Scions', 'Goblin': 'Goblins',
          'Rachisan': 'Rachisans', 'Shade': 'Shades', 'Minotaur': 'Minotaurs', 'Satyr': 'Satyrs', 'Centaur': 'Centaurs', 'Dryad': 'Dryads', 'Eonic': 'Eonics', 'Gnoll': 'Gnolls'}
for n in ('Beastkin', 'Dhampir', 'Dragonborn', 'Gearforged', 'Sapopova', 'Tosculi', 'Alseid', 'Bearfolk', 'Erina', 'Piney', 'Derro', 'Lizardfolk', 'Ratfolk', 'Ravenfolk', 'Shadow Fey', 'Trollkin', 'Giantkin', 'Werekin'): PEOPLE[n] = n
L = {}    # lineage -> dict(base=(src,text), versions=[(tag,src,text,oldh)], variants=[(name,src,text,oldh)], extras=[(title,src,text,oldh)])
order = []; north_intro = None
def slot(n):
    if n not in L: L[n] = dict(base=None, versions=[], variants=[], extras=[]); order.append(n)
    return L[n]
for h2, t2 in top[1:]:
    gsrc = src_of(sections(t2, 3)[0][1])
    for h, t in sections(t2, 3)[1:]:
        if h2 == 'Elements of a Lineage': continue
        src = src_of(t) or gsrc; t = strip_src(t).strip()
        if h == 'Northlands Lineage Variants': north_intro = paragraphs(t)[1]; continue
        m = re.match(r'^(.+?) Lineage Variant: (.+)$', h)
        if m: slot(m.group(1))['variants'].append((m.group(2), src, t, h)); continue
        m = re.match(r'^(.+?) Lineage Expansion$', h)
        if m: slot(m.group(1))['extras'].append(('More Natural Adaptations', src, t, h)); continue
        m = re.match(r'^(.+?) (?:Lineage Expanded|Natural Adaptation): (.+)$', h)
        if m: slot(m.group(1))['extras'].append(('Natural Adaptation: ' + m.group(2), src, t, h)); continue
        m = re.match(r'^(.+?) \((Labyrinth|Lineages & Heritages|Northlands)\)$', h)
        if m: slot(m.group(1))['versions'].append((PLACE[m.group(2)], src, t, h)); continue
        d = slot(h)
        if d['base'] is None: d['base'] = (src, t, h)
        else: d['versions'].append(('?', src, t, h))
assert all(d['base'] for d in L.values()), [n for n, d in L.items() if not d['base']]
def traits(t):
    d = {}
    for p in paragraphs(t):
        m = re.match(r'\*\*\*([^*]+?)\.?\*\*\*\.? ?(.*)', p, re.S)
        if m: d[m.group(1).strip()] = m.group(2)
    return d
CORE3 = {'Age', 'Size', 'Speed'}
def rules(t):
    i = t.find('Lineage Traits'); return traits(t[i:] if i >= 0 else t)
def same_rules(a, b):
    ta, tb = rules(a), rules(b); ka = set(ta) - CORE3; kb = set(tb) - CORE3
    if ka != kb: return False
    return all(difflib.SequenceMatcher(None, ta[k], tb[k]).ratio() > 0.8 or not tb[k] or not ta[k] or min(len(ta[k]), len(tb[k])) < 5 for k in ka)
def shift(t, n):   # promote headings by n levels
    return re.sub(r'^(#+) ', lambda m: '#' * max(2, len(m.group(1)) - n) + ' ', t, flags=re.M)
rec = {}
her = read('Rules/Characters/Heritages.md')
tb = re.search(r'\*\*Common Heritages by Lineage\*\*\n\n((?:\|.*\n?)+)', her).group(1)
for r in table_rows(tb)[2:]:
    nm = re.sub(r'\[\[[^\]]*\\\|([^\]]*)\]\]', r'\1', r[0]); nm = re.sub(r'\[\[([^\]]*)\]\]', r'\1', nm)
    rec[nm] = r[1].replace('[[#', '[[Heritages#').replace('\\|', '|')
VREC = {'Duergar': 'Duergar (Dwarf Variant)', 'Drow': 'Drow (Elf Variant)', 'Sea Elf': 'Sea Elf (Elf)', 'Midnight Dwarf': 'Midnight Dwarf', 'Star Elf': 'Star Elf'}
anchors = {}; pages = {}; rows = []; flags = []
for n in sorted(order, key=key):
    d = L[n]; pg = n + ' Lineage'; src, base, oldh = d['base']; anchors[oldh] = (pg, None)
    bp = paragraphs(base); i = next((k for k, p in enumerate(bp) if p.startswith('####')), len(bp))
    lead = []
    if n in PEOPLE: lead.append(f'For who they are in Midgard, see [[{PEOPLE[n]}]].')
    if n in rec: lead.append(f'Common heritages: {rec[n]}.')
    out = bp[:i] + ([' '.join(lead)] if lead else []) + ([f'%% source: {src} %%'] if src else []) + [shift('\n\n'.join(bp[i:]), 2)]
    vnames = []
    for tag, vsrc, vt, vh in d['versions']:
        if same_rules(base, vt):
            ta = traits(base); extra = [p for p in paragraphs(vt[:vt.find('Lineage Traits')].rsplit('####', 1)[0]) if not p.startswith('#') and not re.match(r'\*\*\*', p) and not p.startswith('|') and not re.match(r'\*\*[^*]+\*\*$', p)]
            lore = [p for p in paragraphs(vt[:vt.find('Lineage Traits')]) if re.match(r'\*\*\*', p) and ('***' + LEAD.match(p).group(1).strip()) not in base]
            title = {'Midgard': 'In Midgard', 'Labyrinth': 'In the Labyrinth', 'Northlands': 'In the Northlands'}[tag]
            out += ['> [!note] ' + title + '\n' + '\n>\n'.join('> ' + p.replace('\n', '\n> ') for p in extra + lore) + '\n>', f'%% source of the note above: {vsrc} (its rules match the entry above) %%']
            anchors[vh] = (pg, None); flags.append(f'{n}: the {vsrc} version has the same rules; its description is kept in a note')
        else:
            title = f'{tag} {n}'; out += [f'## {title}', f'%% source: {vsrc} %%', shift(vt, 1).replace('## ', '### ') if False else shift(vt, 1)]
            anchors[vh] = (pg, title); vnames.append(title)
    for vn, vsrc, vt, vh in sorted(d['variants'], key=lambda v: key(v[0])):
        note = f' Common heritages: {rec[VREC[vn]]}.' if vn in VREC and VREC[vn] in rec else ''
        xs = '%% source: ' + vsrc + (' (a 5th Edition book; converted for this wiki following Converting 5e Material)' if vsrc == 'Book of Ebon Tides' else '') + ' %%'
        blk = shift(vt, 1)
        if n == 'Dwarf' and vn == 'Baugsmidr Dwarf': blk = north_intro + '\n\n' + blk
        out += [f'## {vn}', xs, blk + (('\n\n' + note.strip()) if note else '')]; anchors[vh] = (pg, vn); vnames.append(vn)
    for tt, vsrc, vt, vh in d['extras']:
        if tt == 'Natural Adaptation: Spellborn': tt = 'Natural Adaptation: Spellborn (Labyrinth)'
        out += [f'## {tt}', f'%% source: {vsrc} %%', shift(vt, 1)]; anchors[vh] = (pg, tt)
    core = src is None
    footer = foot if core else '---\n<small>Sources: [[Credits]].</small>'
    text = '---\npublish: true\n---\n' + '\n\n'.join(x.strip('\n') for x in out if x.strip()) + '\n\n' + footer + '\n'
    text = text.replace('[[#Natural Adaptation|', '[[Lineages#Natural Adaptation|').replace('[[#Bearfolk (Northlands)|', '[[#Northlands Bearfolk|')
    if src == 'Book of Ebon Tides': text = text.replace(f'%% source: {src} %%', f'%% source: {src} (a 5th Edition book; converted for this wiki following Converting 5e Material) %%', 1)
    pages[pg] = text
    bar = '\\|'
    rows.append(f'| [[{pg}{bar}{n}]] | ' + (', '.join(f'[[{pg}#{v}{bar}{v}]]' for v in vnames) or '—') + f' | {SUITS[src]} |')
# ---- index page
el = S['Elements of a Lineage']; var_intro = paragraphs(sections(S['Variant Lineages'], 3)[0][1])
index = [top[0][1].replace(' Lineage options include beastkin, dwarf, elf, human, kobold, orc, syderean, and smallfolk.', ''), '## Elements of a Lineage', el,
         '### Variant Lineages', "%% source: Player's Guide 2 %%"] + var_intro + ['## Lineage List',
         'Each lineage has its own page. Variants and regional versions of a lineage are on that lineage’s page.',
         '| Lineage | Variants and Versions | Suits |\n|---|---|---|\n' + '\n'.join(rows)]
newidx = front + '\n\n'.join(x.strip('\n') for x in index) + '\n\n' + foot + '\n'
# nothing lost: every trait lead-in of the old page is on some new page
alltxt = newidx + ''.join(pages.values())
miss = [m.group(0) for m in re.finditer(r'^(?:- )?\*\*\*([^*\n]+?)\.?\*\*\*', old, re.M) if m.group(0) not in alltxt]
dropped_dupes = set()
for n, d in L.items():
    for tag, vsrc, vt, vh in d['versions']:
        if same_rules(d['base'][1], vt): dropped_dupes |= {m.group(0) for m in re.finditer(r'^\*\*\*([^*\n]+?)\.?\*\*\*', vt, re.M)}
real = [m for m in miss if m not in dropped_dupes and m.replace('- ***', '- **').replace('.***', '.**') not in alltxt]
print(len(pages), 'pages;', 'missing lead-ins not explained by merged duplicates:', real)
for f_ in flags: print('  merged:', f_)
print('named versions/variants:', sum(r.count('#') for r in rows))
if '--write' in sys.argv:
    for pg, t in pages.items(): write(OUT + pg + '.md', t)
    write(P, newidx); json.dump({k: list(v) for k, v in anchors.items()}, open('/home/claude/ts/lineage_anchors.json', 'w'))
else:
    os.makedirs('/home/claude/ts/lin', exist_ok=True)
    for pg, t in pages.items(): open('/home/claude/ts/lin/' + pg + '.md', 'w').write(t)
    open('/home/claude/ts/lin/_Lineages.md', 'w').write(newidx)
