# Stage 2: one alphabetical list of backgrounds with an index table on Rules/Backgrounds & Talents/Backgrounds.md.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Backgrounds & Talents/Backgrounds.md'
old = read(P); front, body = split_front(old); body, footer = split_footer(body)
top = sections(body, 2)
intro = top[0][1]; elements = dict(top)['Elements of a Background']
fac = dict(top)['Faction Backgrounds']
wtab = re.search(r'\*\*Wanderer Adventuring Motivation\*\*\n\n(\| d8 \|(?:.*\n?)+)', fac + '\n').group(0).strip()
fpar = paragraphs(fac)[:2]
bg = {}
for h, t in top:
    if h is None or h == 'Elements of a Background' or h == 'Faction Backgrounds' or h.startswith('More Backgrounds'): continue
    bg[h] = t
assert len(bg) == 52, len(bg)
assert bg['Wanderer'].rstrip().count('\n| ') == 0
bg['Wanderer'] = bg['Wanderer'].rstrip() + '\n\n' + wtab
FACTION = {'Concordan Guard', 'Grove Warden', 'Portal Wright', 'Visionary'}
def suits(n, src):
    if n in FACTION: return 'The [[The Labyrinth\\|Labyrinth]] (faction background)'
    if n == 'Vampire Hunter': return 'Any character; pairs well with a dhampir'
    if n in ('Argent Rats Mercenary', 'Envoy of Winter'): return '[[Zobeck]]'
    return {None: 'Any character', "Player's Guide 2": 'Any character', 'Tales of the Old Margreve': 'The Margreve forest',
            'Labyrinth Worldbook': 'The [[The Labyrinth\\|Labyrinth]]', 'Lineages & Heritages': 'Midgard',
            'Book of Blades': 'Martial characters', 'Northlands Worldbook': 'The [[Northlands]]', 'Night Hunters': 'Horror campaigns'}[src]
rows = []
for n in sorted(bg, key=key):
    m = re.search(r'\*\*Skill Proficiencies:?\*\*:? *(.+)', bg[n]); assert m, n
    sk = re.sub(r'^(Choose two from|You are proficient in your choice of two of the following:) ', 'Two of ', m.group(1).strip()).rstrip('.').replace('|', '\\|')
    rows.append(f'| [[#{n}\\|{n}]] | {sk} | {suits(n, src_of(bg[n]))} |')
index = '| Background | Skill Proficiencies | Suits |\n|---|---|---|\n' + '\n'.join(rows)
f0 = 'This section contains new backgrounds tied to the four major heroic factions. These backgrounds are aimed at characters who grew up in the Labyrinth.'
assert fpar[0] == f0, fpar[0]
f0 = 'The Concordan guard, grove warden, portal wright, and visionary are tied to the four major heroic factions of the [[The Labyrinth|Labyrinth]]. These backgrounds are aimed at characters who grew up there.'
out = [intro, '## Elements of a Background', elements, '## Background List',
       'Every background, in alphabetical order. The last column says where a background fits best; any background can be used anywhere.',
       index, 'For an ongoing goal your character can take up during play, see [[Character Threads]].',
       '### Faction Backgrounds', '%% source: Labyrinth Worldbook %%', f0, fpar[1]]
for n in sorted(bg, key=key): out += ['## ' + n, bg[n]]
new = front + '\n\n'.join(x.strip('\n') for x in out) + '\n\n' + footer + '\n'
for h in re.findall(r'^###+ .*$', old, re.M): assert new.count(h) >= old.count(h), h
ol = [l for l in old.split('\n') if l.startswith('| ')]; missing = [l for l in set(ol) if l not in new]
assert all(l.startswith('| d8 | Adventuring Motivation') or re.match(r'\| \d \| (I|Adv|Hope)', l) or l == '|   |   |' for l in missing), missing
print(len(old.split('\n')), '->', len(new.split('\n')))
if '--write' in sys.argv: write(P, new)
else: open('/home/claude/ts/backgrounds_new.md', 'w').write(new)
