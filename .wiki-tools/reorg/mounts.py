# Stage 2: one Mounts table and one Mounts section on Rules/Equipment/Mounts & Services.md.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Equipment/Mounts & Services.md'
old = read(P); front, body = split_front(old); body, footer = split_footer(body)
S = dict((h, t) for h, t in sections(body, 2))
mounts, services, pg2, combat, north = S['Mounts'], S['Services'], S["Mounts & Combat Animals (Player's Guide 2)"], S['Combat Animals'], S['More Mounts (Northlands Worldbook)']
def grab(text, title):
    m = re.search(re.escape(title) + r'\n\n((?:\|.*\n?)+)', text); assert m, title
    return m.group(0), [r for r in table_rows(m.group(1))[2:]]
blk, core_rows = grab(services, '**Mounts**'); services = services.replace(blk, '')
blk, uniq_rows = grab(combat, '*Unique Mounts*'); combat = combat.replace(blk, '')
blk, north_rows = grab(north, '**Mounts (Northlands Worldbook)**')
mv2 = [r[0] for r in uniq_rows if r[4] == 'MV2']
rows = ['| **Common mounts** |  |  |  |'] + [f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} |' for r in core_rows]
rows += ['| **Unusual mounts** |  |  |  |'] + [f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} |' for r in uniq_rows]
rows += ['| **Northern mounts** |  |  |  |'] + [f'| {r[0]} | {r[2]} | — | {r[1]} |' for r in north_rows]
table = '**Mounts**\n\n| Mount | Cost | Speed (per Round) | Carrying Capacity |\n|---|---|---|---|\n' + '\n'.join(rows)
srcs = ("%% sources: Player's Guide 2: unusual mounts and the three notes on climbing, flying and swimming mounts (stat blocks are in Monster Vault, except "
        + ' and '.join(mv2) + " in Monster Vault 2); Northlands Worldbook: northern mounts and the paragraph on travel in the Northlands %%")
m_pre, m_gear = mounts.split('#### Mount Gear and Expenses')
pg2p = paragraphs(strip_src(pg2))
assert pg2p[1].startswith('The mounts listed in this section')
unusual = [pg2p[1].replace('The mounts listed in this section', 'The unusual mounts on the table', 1)] + pg2p[2:]
note = open('/home/claude/ts/mounts_note.md').read().strip()
np_ = paragraphs(strip_src(north))[0]
cut = ' The **Mounts** table shows each animal’s carrying capacity. For land vehicles, see [[Vehicles#More Vehicles (Northlands Worldbook)|Vehicles]].'
assert cut in np_; np_ = np_.replace(cut, ' For land vehicles, see [[Vehicles]].')
a = 'obeys the new handler instead. At\n'; b = '\nGM’s discretion, a Beast'
assert a in combat and b in combat
tail = re.search(r'\nGM’s discretion, a Beast[^\n]*', combat).group(0)
combat = combat.replace(tail, '').replace('obeys the new handler instead. At', 'obeys the new handler instead. At the ' + tail.strip())
out = ['## Mounts', m_pre.strip()] + unusual + [np_, note, table, srcs, '#### Mount Gear and Expenses', m_gear.strip(),
       '## Combat Animals', "%% source: Player's Guide 2 %%", combat.strip(), '## Services', services.strip()]
new = front + '\n\n'.join(out) + '\n\n' + footer + '\n'
for m in re.finditer(r'^(?:> )?\*\*\*([^*\n]+?)\.?\*\*\*', old, re.M): assert m.group(0) in new, m.group(0)
for h in re.findall(r'^#{3,4} .*$', old, re.M): assert h in new, h
for r in core_rows + uniq_rows + north_rows: assert r[0] in table
print(len(old.split('\n')), '->', len(new.split('\n')), 'mounts', len(core_rows), len(uniq_rows), len(north_rows))
if '--write' in sys.argv: write(P, new)
else: open('/home/claude/ts/mounts_new.md', 'w').write(new)
