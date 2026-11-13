# Stage 2 follow-up: class option pages and sections that are not subclasses go into the class features they extend.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from relink import retire
B = 'Rules/Book of Blades/'; SRC = '%% source: Book of Blades %%'
def body(rel): return split_footer(split_front(read(rel))[1])[0]
def demote(x): return re.sub(r'^(#+) ', lambda m: '#' + m.group(1) + ' ', x, flags=re.M)
def cut_section(text, title):
    m = re.search(r'^## ' + re.escape(title) + r'\n(.*?)(?=^## |\Z)', text, re.S | re.M); assert m, title
    return text[:m.start()] + text[m.end():], m.group(1).strip('\n')
def drop_index_row(text, name):
    row = f'| [[#{name}\\|{name}]] | Any character |\n'; assert row in text, name; return text.replace(row, '')
fm = dict(sections(body(B + 'Fighting Mechanics.md'), 2))
# ---- Fighter
p = 'Rules/Classes/Fighter.md'; s = read(p)
s, exp = cut_section(s, 'Martial Actions Expanded'); s = drop_index_row(s, 'Martial Actions Expanded')
note = re.search(r'> \[!note\] Martial Actions for Paladins and Rangers\n(?:>.*\n?)+', exp).group(0).strip(); exp = exp.replace(note, '')
note = note.replace('This section introduces new martial actions for the fighter. ', '')
new = [(h, "%% source: Player's Guide 2 %%\n\n" + t.strip()) for h, t in sections(strip_src(exp), 3)[1:]]
new += [(h, SRC + '\n\n' + t.strip()) for h, t in sections(fm['Martial Actions'], 3)[1:]]
assert len(new) == 9, len(new)
i = s.index('### Martial Action\n'); j = s.index('\n### ', i + 5); feat = s[i:j]
core = sections(feat, 4)
ents = sorted(core[1:] + new, key=lambda e: key(e[0]))
feat2 = core[0][1].rstrip() + ''.join(f'\n\n#### {h}\n\n{t.strip()}' for h, t in ents) + '\n\n' + note + '\n\nArbalest Skirmish and Springheel are available to any class that has the Martial Action feature.\n'
s = s[:i] + feat2 + s[j:]
write(p, s)
# ---- Mechanist
p = 'Rules/Classes/Mechanist.md'; s = read(p)
s, exp = cut_section(s, 'Augment Effects Expanded'); s = drop_index_row(s, 'Augment Effects Expanded')
new = [(h, "%% source: Player's Guide 2 %%\n\n" + t.strip()) for h, t in sections(strip_src(exp), 4)[1:]]
new += [(h, SRC + '\n\n' + t.strip()) for h, t in sections(fm['Augment Effects'], 3)[1:]]
assert len(new) == 18, len(new)
m = re.search(r'^## Augment Effects\n(.*?)(?=^## )', s, re.S | re.M); core = sections(m.group(1), 3)
assert not ({h for h, _ in core[1:]} & {h for h, _ in new})
ents = sorted(core[1:] + new, key=lambda e: key(e[0]))
s = s[:m.start()] + '## Augment Effects\n\n' + core[0][1].strip() + ''.join(f'\n\n### {h}\n\n{t.strip()}' for h, t in ents) + '\n\n' + s[m.end():]
write(p, s)
# ---- Monk, Ranger: whole pages become sections before the subclasses
def absorb(cls, pages_):
    p = f'Rules/Classes/{cls}.md'; s = read(p); i = s.index(f'## {cls} Subclasses'); add = ''
    for pg in pages_:
        add += f'## {pg}\n\n{SRC}\n\n' + demote(strip_src(body(B + pg + '.md')).strip()) + '\n\n'
    write(p, s[:i] + add + s[i:])
absorb('Monk', ['Technique Forms']); absorb('Ranger', ['Tracking in Combat', 'Booby Traps'])
n = retire('Fighting Mechanics', 'Fighter', 'Martial Action') + retire('Technique Forms', 'Monk', 'Technique Forms') + retire('Tracking in Combat', 'Ranger', 'Tracking in Combat') + retire('Booby Traps', 'Ranger', 'Booby Traps')
for pg in ('Fighting Mechanics', 'Technique Forms', 'Tracking in Combat', 'Booby Traps'): os.remove(os.path.join(V, B + pg + '.md'))
print('links repointed', n)
