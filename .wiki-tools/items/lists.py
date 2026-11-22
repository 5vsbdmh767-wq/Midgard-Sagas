# Rebuild every magic item table (list pages, Wondrous Items, Magic Items A-Z, Magic Items by Rarity) from the item pages.
# Run after adding or changing item pages. --write applies; otherwise prints what would change.
import os, re, sys, glob, collections
V = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); MI = os.path.join(V, 'Rules/Magic/Magic Items')
W = '--write' in sys.argv
RAR = re.compile(r'\b(Very Rare|Uncommon|Common|Rare|Legendary|Artifact|Fabled|Rarity Varies|Rarity by Figurine|Varies)\b', re.I)
RORDER = ['Common', 'Uncommon', 'Rare', 'Very Rare', 'Legendary', 'Artifact', 'Fabled', 'Rarity Varies', 'Rarity by Figurine', '—']
def plain(s): return re.sub(r'\[\[(?:[^\]|]*\\?\|)?([^\]]*)\]\]', r'\1', s).replace('* *', ' ')
def parse_type(t, nxt):
    pend = '%% price pending' in t
    t0 = plain(re.sub(r'%%.*?%%', '', t)).strip().strip('*').strip()
    rs = [r.title() for r in RAR.findall(t0)]
    rs = rs[:1] + [r for r in rs[1:] if r != 'Varies']
    rar = rs[0].replace('By', 'by') if rs else '—'
    if rar == 'Varies' or (len(set(rs)) > 1 and not rar.startswith('Rarity')): rar = 'Rarity Varies'
    att = re.search(r'\((?:[^()]*?)(Requires? Attunement[^()]*)\)', t0, re.I)
    if not att and nxt: att = re.match(r'^\*\((Requires? Attunement[^)]*)\)', plain(nxt))
    att = re.sub(r'(?i)^requires? attunement\s*', '', att.group(1)).strip() or 'Yes' if att else '—'
    m = RAR.search(t0); after = t0[m.end():] if m else t0
    pr = re.search(r'(\d[\d,]*\s*(?:gp)?(?:\s*\+\s*[a-z ]+cost)?|Priceless|Price Varies|Varies)', after)
    kind = re.match(r'([^,(]+(?:\([^)]*\))?)', t0).group(1).strip()
    return kind, rar, att, ('pending' if pend else pr.group(1).strip() if pr else '—')
items = {}
for p in glob.glob(MI + '/**/*.md', recursive=True):
    rel = os.path.relpath(p, MI); parts = rel.split(os.sep)
    if len(parts) < 2 or (parts[0] == 'Wondrous Items' and len(parts) < 3): continue
    s = open(p, encoding='utf-8').read(); name = parts[-1][:-3]
    lines = [l for l in s.split('\n') if l.strip()]
    i = next((i for i, l in enumerate(lines) if l.startswith('*') and not l.startswith('**') and RAR.search(plain(l))), None)
    row = parse_type(lines[i], lines[i + 1] if i is not None and i + 1 < len(lines) else '') if i is not None else ('—',) * 4
    if name == 'Jarlpact Rings': row = ('Ring (set of four)', 'Rarity Varies', 'Yes', 'Price Varies')
    items[name] = (parts[-2],) + row
CLASSES = 'Barbarian Bard Cleric Druid Fighter Mechanist Monk Paladin Ranger Rogue Sorcerer Warlock Wizard Theurge Vanguard Witch'.split()
def linkcls(a): return re.sub(r'\b(' + '|'.join(CLASSES) + r')\b', r'[[\1]]', a)
def table(names, cat_col=False):
    out = ['| Item | Type | Rarity | Attunement | Price |' + (' Category |' if cat_col else ''), '|' + '---|' * (6 if cat_col else 5)]
    for n in sorted(names, key=str.lower):
        c, k, r, a, p = items[n]; out.append(f'| [[{n}]] | {k} | {r} | {linkcls(a)} | {p} |' + (f' [[{c}]] |' if cat_col else ''))
    return '\n'.join(out)
bycat = collections.defaultdict(list)
for n, v in items.items(): bycat[v[0]].append(n)
wcats = sorted(os.path.basename(d.rstrip('/')) for d in glob.glob(MI + '/Wondrous Items/*/'))
writes = {}
def put_items(path, names, cat_col=False, head='## Items\n\n'):
    s = writes.get(path) or open(path, encoding='utf-8').read()
    i = s.index(head) + len(head); j = s.index('\n\n', s.index('|---', i)) if '\n\n' in s[s.index('|---', i):] else len(s)
    writes[path] = s[:i] + table(names, cat_col) + s[j:]
for c, names in bycat.items():
    if c in wcats: put_items(f'{MI}/Wondrous Items/{c}.md', names)
    elif c != 'Wondrous Items': put_items(f'{MI}/{c}.md', names)
wi = f'{MI}/Wondrous Items/Wondrous Items.md'; s = open(wi, encoding='utf-8').read()
cnt = '| Category | Items |\n|---|---|\n' + '\n'.join(f'| [[{c}]] | {len(bycat[c])} |' for c in wcats)
s = re.sub(r'\| Category \| Items \|\n\|---\|---\|\n(?:\|.*\n?)*', cnt + '\n', s, count=1); writes[wi] = s
put_items(wi, [n for c in wcats for n in bycat[c]], True, '## All Wondrous Items\n\n')
az = f'{MI}/Magic Items A–Z.md'; s = open(az, encoding='utf-8').read(); i = s.index('| Item |'); j = s.index('\n\n', i)
writes[az] = s[:i] + table(list(items), True) + s[j:]
br = f'{MI}/Magic Items by Rarity.md'; s = open(br, encoding='utf-8').read(); i = s.index('## '); j = s.index('\n\n---\n<small>')
byr = collections.defaultdict(list)
for n, v in items.items(): byr[v[2]].append(n)
writes[br] = s[:i] + '\n\n'.join(f'## {r}\n\n' + table(byr[r], True) for r in RORDER if byr.get(r)) + s[j:]
ch = 0
for p, s in writes.items():
    if open(p, encoding='utf-8').read() != s:
        ch += 1; print('changes', os.path.relpath(p, V))
        if W: open(p, 'w', encoding='utf-8').write(s)
print(len(items), 'items;', ch, 'pages', 'written' if W else 'would change')
