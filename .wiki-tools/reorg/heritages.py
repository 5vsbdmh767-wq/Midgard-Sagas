# Stage 2: one language section, one recommended-heritage table and one alphabetical list of heritages.
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
P = 'Rules/Lineages & Heritages/Heritages.md'
old = read(P); front, body = split_front(old); body, footer = split_footer(body)
top = sections(body, 2); S = dict(top)
TAB = re.compile(r'\n*(?:\*\*|\*)Common Heritages by Lineage(?: \([^)]*\))?(?:\*\*|\*)\n\n((?:\|.*\n?)+)')
rec = {}; order = []
def harvest(text):
    def f(m):
        for r in table_rows(m.group(1))[2:]:
            if r[0].startswith('(*)') or r[0].startswith('Player’s Guide'): continue
            plain = re.sub(r'\[\[[^\]]*\\\|([^\]]*)\]\]', r'\1', r[0]); plain = re.sub(r'\[\[([^\]]*)\]\]', r'\1', plain)
            if plain not in rec: rec[plain] = [r[0], []]; order.append(plain)
            elif '[[' in r[0] and '[[' not in rec[plain][0]: rec[plain][0] = r[0]
            for h in r[1].split(','):
                h = re.sub(r'\[\[([^\]]*)\]\]', r'\1', h.strip().rstrip('*').strip())
                if h and h not in rec[plain][1]: rec[plain][1].append(h)
        return '\n\n'
    return TAB.sub(f, text + '\n').rstrip('\n')
her = {}
def take(text, dup_suffix=None):
    for h, t in sections(text, 3):
        if h is None or not h.endswith('Heritage') and '(Lineages & Heritages)' not in h: continue
        her.setdefault(h, harvest(t).strip())
core_opts = sections(S['Heritage Options'], 3)
for k in S:
    if k and (k.startswith('Heritage Options') or k.startswith('More Heritages')): take(S[k])
harvest(S["Heritage Options (Player's Guide 2)"]); harvest(S['More Heritages (Tales of the Old Margreve)'])
lin = read('Rules/Lineages & Heritages/Lineages.md'); m = TAB.search(lin); harvest(lin[m.start():m.end()])
# duplicates with identical traits: keep one entry, second description in a place-named note
def traits(t): return [p for p in paragraphs(strip_src(t)) if p.startswith('***')]
def descr(t): return [p for p in paragraphs(strip_src(t)) if not p.startswith('***')]
for n, place in (('Hiveheim Heritage', 'In Björnrike'), ('Moonlit Heritage', 'In the Moonlit Glades')):
    b = her.pop(n + ' (Lineages & Heritages)'); a = her[n]
    assert traits(a) == traits(b), n
    note = '> [!note] ' + place + '\n' + '\n>\n'.join('> ' + p for p in descr(b)) + '\n>'
    ps = paragraphs(a); i = next(i for i, p in enumerate(ps) if p.startswith('***'))
    her[n] = '\n\n'.join(ps[:i] + [note, '%% source of the note above: Lineages & Heritages (its traits are identical) %%'] + ps[i:])
for n in ('Changeling Heritage', 'Umbral Heritage'): her[n] = her[n].replace('%% source: Book of Ebon Tides %%', '%% source: Book of Ebon Tides (a 5th Edition book with no heritages; built for this wiki from the learned traits of its peoples, following Converting 5e Material) %%'); assert 'built for this wiki' in her[n]
assert len(her) == 14 + 11 + 5 + 9 + 15 + 3 + 2 + 5, len(her)
def suits(n):
    return {None: 'Any character', "Player's Guide 2": 'Any character', 'Tales of the Old Margreve': 'The [[The Margreve\\|Margreve]] forest',
            'Labyrinth Worldbook': 'The [[The Labyrinth\\|Labyrinth]]', 'Lineages & Heritages': 'Midgard', 'Book of Blades': 'Martial characters',
            'Book of Ebon Tides': 'The [[The Shadow Realm\\|Shadow Realm]]', 'Night Hunters': 'Horror campaigns'}[(src_of(her[n]) or '').split(' (')[0] or None]
names = sorted(her, key=key)
short = lambda n: n[:-len(' Heritage')]
typical = {}
for l in order:
    for h in rec[l][1]:
        hh = next((n for n in names if short(n).lower() == h.lower()), None); assert hh, h
        typical.setdefault(hh, []).append(l)
index = '| Heritage | Suits | Often chosen by |\n|---|---|---|\n' + '\n'.join(
    f'| [[#{n}\\|{short(n)}]] | {suits(n)} | {", ".join(sorted(typical.get(n, []))) or "—"} |' for n in names)
def hl(h):
    n = next(n for n in names if short(n).lower() == h.lower()); return f'[[#{n}\\|{short(n)}]]'
rtab = '**Common Heritages by Lineage**\n\n| Lineage | Recommended Heritages |\n|---|---|\n' + '\n'.join(
    f'| {rec[l][0]} | {", ".join(hl(h) for h in sorted(rec[l][1]))} |' for l in sorted(order, key=key))
# --- languages
el = sections(S['Elements of a Heritage'], 3); lang = dict(el)['Languages']
lp = paragraphs(lang); core_txt = [p for p in lp if not p.startswith('|') and not p.startswith('**')]
pl = S["Languages (Player's Guide 2)"]
def tbl(text, title): return re.search(re.escape(title) + r'\n\n((?:\|.*\n?)+)', text).group(1).strip()
std = tbl(pl, '*Standard Languages*'); eso = tbl(pl, '*Esoteric Languages*')
for a, b in (('| Dwarves |', '| [[Dwarves]] |'), ('Humans,', '[[Humans]],'), ('| Elves,', '| [[Elves]],'), ('| Gnomes |', '| [[Gnomes]] |'), ('| Halflings |', '| [[Halflings]] |'), ('| Orcs |', '| [[Orcs]] |')):
    assert a in std, a; std = std.replace(a, b)
ents = [p for p in paragraphs(strip_src(pl)) if p.startswith('***')]
ml = dict(sections(S['More Heritages (Tales of the Old Margreve)'], 3))['Languages']
ents += [p for p in paragraphs(ml) if p.startswith('***')]
ents.sort(key=lambda p: key(LEAD.match(p).group(1)))
mint = paragraphs(ml)[0]; assert mint.startswith('The heritages in this section introduce two new languages')
mint = mint.replace('The heritages in this section introduce two new languages: [[Erina]] and [[Piney]].', 'The [[The Margreve|Margreve]] has two languages of its own: [[Erina]] and [[Piney]].')
langs = core_txt + ['**Standard Languages**\n\n' + std, '**Esoteric Languages**\n\n' + eso, mint] + ents + [
    "%% sources: Player's Guide 2: the typical speakers lists, Deep Speech and Umbral; Tales of the Old Margreve: Erina and Piney %%"]
opt_intro = [p for p in paragraphs(core_opts[0][1])]
out = [top[0][1], '## Elements of a Heritage', el[0][1], '### Languages'] + langs + ['## Heritage Options'] + opt_intro + [
    rtab, "%% sources: every book that offers lineages; see each heritage and lineage for its own source %%",
    'The table below lists every heritage in alphabetical order.', index]
for n in names: out += ['### ' + n, her[n]]
new = front + '\n\n'.join(x.strip('\n') for x in out) + '\n\n' + footer + '\n'
for m_ in re.finditer(r'^\*\*\*([^*\n]+?)\.?\*\*\*', old, re.M): assert m_.group(0) in new, m_.group(0)
print(len(old.split('\n')), '->', len(new.split('\n')), 'heritages', len(her), 'lineages', len(rec))
if '--write' in sys.argv: write(P, new)
else: open('/home/claude/ts/heritages_new.md', 'w').write(new)
