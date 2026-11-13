# Stage 2: fold the Trade Secrets tool material into each core tool section of Rules/Equipment/Tools.md.
# Dry run writes /home/claude/ts/tools_new.md; --write replaces the page.
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Equipment/Tools.md'
front, body = split_front(read(P)); body, footer = split_footer(body)
top = sections(body, 2)
intro = top[0][1]
desc = next(t for h, t in top if h == 'Tool Descriptions')
more = next(t for h, t in top if h and h.startswith('More Tool Uses'))
core = sections(desc, 3); ts3 = sections(more, 3)
ts_intro = strip_src(ts3[0][1]).strip()
big = next(t for h, t in ts3 if h == 'Big Projects')
ts = dict((h, t) for h, t in sections(next(t for h, t in ts3 if h == 'New Tool Challenges'), 4) if h)
assert [h for h, _ in core[1:]] == list(ts), (set(ts) ^ set(h for h, _ in core[1:]))

TBL = re.compile(r'(?:\*\*([^*\n]*Example Tasks[^*\n]*)\*\*\n\n)?((?:\|.*\n?)+)')
def rows_of(tbl):
    out = []
    for c in table_rows(tbl)[2:]:
        if len(c) > 1 and c[1] == '' and out: out[-1][0] += ' ' + c[0]   # rejoin a wrapped task
        else: out.append([c[0], c[1]])
    return out
FIX = {  # tables the first conversion scrambled; checked against the Player's Guide
 'Clothier Tools': [['Determine a garment’s age and origin', '10'], ['Sew an injury closed', '15'], ['Patch a torn sail during a raging storm', '20']],
 'Construction Tools': [['Drive a spike into a stone (or similarly hard) surface', '10'], ['Break down and repurpose materials from a woodshed', '15'], ['Construct a temporary brace to keep a roof from collapsing', '20']],
 'Herbalist Tools': [['Safely harvest and preserve a plant for later use', '10'], ['Identify a poison with a sample of affected flesh', '15'], ['Mix a hasty concoction to temporarily halt the effects of a deadly disease', '20']],
}
def split_core(name, text):
    """-> (text before the task table, rows, text after)"""
    paras = paragraphs(text); pre = []; post = []; rows = None; i = 0
    while i < len(paras):
        p = paras[i]
        if re.match(r'^\*\*[^*]*Example Tasks[^*]*\*\*$', p): i += 1; continue
        if p.startswith('| Task | DC'):
            if rows is None: rows = rows_of(p)
            i += 1; continue
        if p.startswith('**Tools**'): i += 2; continue
        if p.startswith('> [!note] Magical Mounts'): i += 1; continue
        (pre if rows is None else post).append(p); i += 1
    if name in FIX: rows = FIX[name]
    return pre, rows, post
def split_ts(name, text):
    m = re.search(r'\*\*' + re.escape(name) + r' New Example Tasks\*\*\n\n((?:\|.*\n)+)', text + '\n')
    assert m, name
    return text[:m.start()].strip('\n'), rows_of(m.group(1)), (text + '\n')[m.end():].strip('\n')
def dc(r):
    return int(r[1]) if r[1].isdigit() else 99

cost = re.search(r'\*\*Tools\*\*\n\n((?:\|.*\n)+)', desc).group(0).strip()
mounts_note = re.search(r'> \[!note\] Magical Mounts\n(?:>.*\n?)+', desc).group(0).strip()
out = [intro, '%% source: Trade Secrets %%\n' + ts_intro, cost, '## Tool Descriptions', core[0][1]]
n_core = n_ts = 0
for name, text in core[1:]:
    pre, rows, post = split_core(name, text)
    assert rows and len(rows) == 3, (name, rows)
    tpre, trows, tpost = split_ts(name, ts[name])
    n_core += len(rows); n_ts += len(trows)
    allrows = sorted(rows + trows, key=dc)
    tbl = f'**{name} Example Tasks**\n\n| Task | DC |\n|---|---|\n' + '\n'.join(f'| {a} | {b} |' for a, b in allrows)
    note = '%% source: Trade Secrets (everything below in this section, and these example tasks: ' + '; '.join(r[0] for r in trows) + ') %%'
    out += ['### ' + name] + pre + [tbl] + post + [note, tpre, tpost]
out += ['## Big Projects', '%% source: Trade Secrets %%', big]
new = front + '\n\n'.join(x for x in out if x.strip()) + '\n\n' + footer + '\n'
old = read(P)
# nothing lost: every lead-in entry and every non-task table row of the old page is still present
for m in re.finditer(r'^\*\*\*([^*\n]+?)\.?\*\*\*', old, re.M):
    assert m.group(0) in new or m.group(0) in mounts_note, m.group(0)
lost = [l for l in old.split('\n') if l.startswith('|') and l not in new and not re.search(r'\|\s*(\d+|\*)?\s*\|$', l) ]
assert not [l for l in lost if l.count('|') < 5], lost
print('core tasks', n_core, 'added tasks', n_ts, 'lines', len(old.split('\n')), '->', len(new.split('\n')))
if '--write' in sys.argv:
    write(P, new); open('/home/claude/ts/mounts_note.md', 'w').write(mounts_note + '\n')
else:
    os.makedirs('/home/claude/ts', exist_ok=True); open('/home/claude/ts/tools_new.md', 'w').write(new)
