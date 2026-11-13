# Stage 2: on every class page, fold added boons, metamagic and invocations into the core lists and
# put all subclasses in one alphabetical run with an index table.
import sys, os, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
SUITS = {None: 'Any character', "Player's Guide 2": 'Any character', 'Book of Blades': 'Any character',
         'Tales of the Old Margreve': 'The [[The Margreve\\|Margreve]] forest', 'Labyrinth Worldbook': 'The [[The Labyrinth\\|Labyrinth]]',
         'Northlands Worldbook': 'The [[Northlands]]', 'Night Hunters': 'Horror campaigns'}
def bullets(text):
    """-> (text before first bullet, [bullet blocks], text after last bullet)"""
    ps = paragraphs(text); i = [k for k, p in enumerate(ps) if p.startswith('- **')]
    if not i: return ps, [], []
    assert i == list(range(i[0], i[-1] + 1)), text[:200]
    return ps[:i[0]], ps[i[0]:i[-1] + 1], ps[i[-1] + 1:]
bname = lambda b: re.match(r'- \*\*(.+?)\.?\*\*', b).group(1)
def merge_boons(cf, boons, log):
    """cf: Class Features text; boons: the added Boons section text."""
    c3 = sections(cf, 3)
    for kind in ('Heroic', 'Epic'):
        add = dict(sections(boons, 3))[kind + ' Boons']
        _, nb, _ = bullets(add); assert nb, kind
        k = next(k for k, (h, _) in enumerate(c3) if h == kind + ' Boon')
        pre, cb, post = bullets(c3[k][1])
        if not cb:   # the core feature is a single boon written as a paragraph or sub-feature: keep it, add the others after
            pre = pre + ['Instead of the boon above, you can choose one of the following ' + kind.lower() + ' boons:']
        pre = [p.replace('You gain the following epic boon:', 'You gain one of the following epic boons:') for p in pre]
        allb = sorted(cb + nb, key=lambda b: key(bname(b)))
        src = "%% source: Player's Guide 2: " + ', '.join(bname(b) for b in nb) + ' %%'
        c3[k] = (c3[k][0], '\n\n'.join(pre + allb + [src] + post))
        log.append(f'{kind} boons +{len(nb)} (core {len(cb)})')
    return c3[0][1] + ''.join(f'\n\n### {h}\n\n{t}' for h, t in c3[1:])
def merge_h4(cf, feature, extra, src, log):
    """add #### entries from `extra` into the ### feature of cf, alphabetically."""
    c3 = sections(cf, 3); k = next(k for k, (h, _) in enumerate(c3) if h == feature)
    core = sections(c3[k][1], 4); new = [(h, f'%% source: {src} %%\n\n' + t) for h, t in sections(strip_src(extra), 4)[1:]]
    ents = sorted(core[1:] + new, key=lambda e: key(e[0]))
    c3[k] = (feature, core[0][1] + ''.join(f'\n\n#### {h}\n\n{t}' for h, t in ents)); log.append(f'{feature} +{len(new)}')
    return c3[0][1] + ''.join(f'\n\n### {h}\n\n{t}' for h, t in c3[1:])
report = []
for p in sorted(glob.glob(V + '/Rules/Classes/*.md')):
    c = os.path.basename(p)[:-3]
    if c == 'Classes': continue
    rel = 'Rules/Classes/' + c + '.md'; old = read(rel); front, body = split_front(old); body, foot = split_footer(body)
    top = sections(body, 2); names = [h for h, _ in top]; i = names.index(c + ' Subclasses'); log = []
    pre = list(top[:i]); core_intro = top[i][1]; subs = {}; dropped = []
    for h, t in top[i + 1:]:
        if h.endswith('Subclasses'): dropped.append(h); continue
        if h == c + ' Boons':
            k = next(k for k, (hh, _) in enumerate(pre) if hh == 'Class Features'); pre[k] = (pre[k][0], merge_boons(pre[k][1], t, log)); continue
        if h == 'Metamagic Options':
            k = next(k for k, (hh, _) in enumerate(pre) if hh == 'Class Features'); pre[k] = (pre[k][0], merge_h4(pre[k][1], 'Metamagic', t, src_of(t), log)); continue
        if h.startswith('Eldritch Invocations ('):
            k = next(k for k, (hh, _) in enumerate(pre) if hh == 'Eldritch Invocations'); src = src_of(t)
            core = sections(pre[k][1], 3); lvl = 4 if '\n#### ' in t else 3
            new = [(hh, f'%% source: {src} %%\n\n' + strip_src(tt).strip()) for hh, tt in sections(t, lvl)[1:]]
            ents = sorted(core[1:] + new, key=lambda e: key(e[0]))
            pre[k] = (pre[k][0], core[0][1] + ''.join(f'\n\n### {hh}\n\n{tt}' for hh, tt in ents)); log.append(f'invocations +{len(new)}'); continue
        assert h not in subs, h; subs[h] = t
    order = sorted(subs, key=key)
    idx = '| Subclass | Suits |\n|---|---|\n' + '\n'.join(f'| [[#{n}\\|{n}]] | {SUITS[src_of(subs[n])]} |' for n in order)
    out = [pre[0][1]] + [f'## {h}\n\n{t}' for h, t in pre[1:]] + [f'## {c} Subclasses', core_intro, idx] + [f'## {n}\n\n{subs[n]}' for n in order]
    new = front + '\n\n'.join(x.strip('\n') for x in out if x.strip()) + '\n\n' + foot + '\n'
    for h in set(re.findall(r'^#{2,4} (.*)$', old, re.M)):
        if h.endswith('Subclasses') or h in (c + ' Boons', 'Heroic Boons', 'Epic Boons', 'Metamagic Options') or h.startswith('Eldritch Invocations (') or h in ('Heroic Boon', 'Epic Boon'): continue
        assert re.search(r'^#{2,4} ' + re.escape(h) + '$', new, re.M), (c, h)
    for b in re.findall(r'^- \*\*.+?\*\*', old, re.M): assert b in new, (c, b)
    report.append(f'{c}: {len(subs)} subclasses; ' + '; '.join(log) + f'; dropped headers: {len(dropped)}; lines {len(old.splitlines())}->{len(new.splitlines())}')
    if '--write' in sys.argv: write(rel, new)
    else: os.makedirs('/home/claude/ts/classes', exist_ok=True); open(f'/home/claude/ts/classes/{c}.md', 'w').write(new)
print('\n'.join(report))
