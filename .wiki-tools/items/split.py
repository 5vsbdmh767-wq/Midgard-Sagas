# Give every magic item its own page, turn the old item pages into list pages, and repoint links.
# Dry run by default; --write applies. Run from anywhere.
import os, re, sys, glob, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from categories import cat as wcat
MI = 'Rules/Magic/Magic Items/'
W = '--write' in sys.argv
CC = None
OVERRIDE = {'Wings of Flying': 'Cloaks, Robes & Clothing', 'Shield of the World Serpent': 'Tools, Keys & Curiosities', 'Resolute Boots': 'Boots & Footwear',
            'Nine-Escape Knot': 'Tools, Keys & Curiosities', 'Pillow of Somnolence': 'Tools, Keys & Curiosities', 'Hel’s Coin': 'Amulets, Charms & Jewelry',
            'Searing Safe': 'Containers & Vessels', 'Spyhole Rings': 'Tools, Keys & Curiosities', 'Speartag': 'Tools, Keys & Curiosities'}
# page -> (folder for its items, names of sections that are rules, not items)
PAGES = {'Magic Armor': ('Magic Armor', []), 'Magic Weapons': ('Magic Weapons', []), 'Potions': ('Potions', []), 'Rings': ('Rings', []),
         'Rods, Staffs & Wands': ('Rods, Staffs & Wands', []), 'Wondrous Items A–L': (None, []), 'Wondrous Items M–Z': (None, []),
         'Magic Tattoos': ('Magic Tattoos', []), 'Fabled Magic Items': ('Fabled Magic Items', ['Properties and Attunement']),
         'Arcanepunk Items': ('Arcanepunk Items', ['Gem Power Sources', 'Charges, Overcharging, and Repairing']),
         'Weapons of Legacy': ('Weapons of Legacy', ['Mighty Deeds', 'Mighty Deeds In Your Game', 'Example Weapons Of Legacy'])}
BAD = {':': ',', '/': '-', '?': '', '"': '', '<': '', '>': '', '|': '-', '*': '', '#': '', '^': '', '[': '(', ']': ')'}
def fname(n): return ''.join(BAD.get(ch, ch) for ch in n).strip().rstrip('.')
def read(rel): return open(os.path.join(V, rel), encoding='utf-8').read()
def split_page(s):
    m = re.match(r'---\n(.*?)\n---\n', s, re.S); front = m.group(0); rest = s[m.end():]
    fi = rest.rfind('\n---\n<small>'); body, foot = (rest[:fi], rest[fi + 1:].strip()) if fi >= 0 else (rest, '')
    parts = re.split(r'(?m)^(?=## )', body)
    pre = parts[0] if not parts[0].startswith('## ') else ''
    secs = [(re.match(r'## (.+)', x).group(1).strip(), x.split('\n', 1)[1] if '\n' in x else '') for x in parts if x.startswith('## ')]
    return front, pre, secs, foot
RAR = re.compile(r'\b(Very Rare|Uncommon|Common|Rare|Legendary|Artifact|Fabled|Rarity Varies|Rarity by Figurine|Varies)\b', re.I)
def parse_type(t):
    t0 = t.strip('*').strip()
    m = RAR.search(t0); rar = m.group(1).title().replace('By', 'by') if m else '—'
    if rar == 'Varies': rar = 'Rarity Varies'
    att = re.search(r'\((?:[^()]*?)(Requires? Attunement[^()]*)\)', t0, re.I)
    att = att.group(1)[0].upper() + att.group(1)[1:] if att else ''
    att = 'Yes' if att.lower() in ('requires attunement', 'require attunement') else (re.sub(r'(?i)^requires? attunement ', '', att) if att else '—')
    pr = re.search(r'(\d[\d,]*\s*(?:gp)?(?:\s*\+\s*[a-z ]+cost)?|Priceless|Price Varies|Varies)', t0[m.end():] if m else t0)
    kind = re.match(r'([^,(]+(?:\([^)]*\))?)', t0).group(1).strip()
    return kind, rar, att, (pr.group(1).strip() if pr else '—')
def typeline_link(t):
    """Link the rarity and attunement words of a type line."""
    m = re.match(r'^\*(.*)\*(\s*%%.*%%)?$', t.strip())
    if not m: return t
    x = m.group(1)
    x = re.sub(r'\b(Very Rare|Uncommon|Common|Rare|Legendary|Artifact)\b', lambda r: f'[[Using Magic Items#Rarity|{r.group(1)}]]', x, count=1)
    x = re.sub(r'\b(Requires? [Aa]ttunement)', lambda r: f'[[Using Magic Items#Attunement|{r.group(1)}]]', x, count=1)
    x = re.sub(r'^(Weapon)\b', '[[Weapons|Weapon]]', x); x = re.sub(r'^(Armor)\b', '[[Armor|Armor]]', x)
    return f'*{x}*' + (m.group(2) or '')
CONDS = ['Blinded', 'Charmed', 'Deafened', 'Frightened', 'Grappled', 'Incapacitated', 'Invisible', 'Paralyzed', 'Petrified', 'Poisoned', 'Prone', 'Restrained', 'Stunned', 'Unconscious']
PROTECT = re.compile(r'!?\[\[[^\]]*\]\]|\[[^\]]*\]\([^)]*\)|%%.*?%%|`[^`]*`|\*\*\*[^*\n]+\*\*\*', re.S)
def link_conditions(body):
    done = set(); out = []
    for line in body.split('\n'):
        if line.startswith(('#', '|', '*Weapon', '*Armor', '*Wondrous', '*Potion', '*Ring', '*Rod', '*Staff', '*Wand')): out.append(line); continue
        segs = []; last = 0
        for m in PROTECT.finditer(line): segs.append((line[last:m.start()], True)); segs.append((m.group(0), False)); last = m.end()
        segs.append((line[last:], True)); new = ''
        for txt, ok in segs:
            if ok:
                for c in CONDS:
                    if c in done: continue
                    mm = re.search(r'(?<![\w\[|])(' + c.lower() + r')(?![\w\]])', txt)
                    if mm and not (c == 'Prone' and 'knocked prone' not in txt and 'fall prone' not in txt and 'falls prone' not in txt and 'is prone' not in txt):
                        txt = txt[:mm.start()] + f'[[Conditions#{c}|{mm.group(1)}]]' + txt[mm.end():]; done.add(c)
            new += txt
        out.append(new)
    return '\n'.join(out)
items = {}; lists = collections.defaultdict(list); oldmap = {}   # oldmap[(page, heading)] -> (newpage, anchor or None)
pages_out = {}
for page, (folder, rules) in PAGES.items():
    rel = MI + page + '.md'; s = read(rel); front, pre, secs, foot = split_page(s)
    if CC is None and 'CC BY' in foot: CC = foot
    keep = []
    # merge same-name sections (weapons of legacy: lore + rules; figurines: two lists)
    merged = collections.OrderedDict()
    for h, b in secs:
        if h in rules: keep.append((h, b)); continue
        if h in merged:
            prev = merged[h]
            if h == 'Figurine of Wondrous Power':
                extra = [p for p in b.split('\n\n') if p.startswith('***')]
                src = re.search(r'%% source: [^%]*%%', b).group(0)
                prev = prev.rstrip('\n') + '\n\n## More Figurines\n' + src + '\n\n' + '\n\n'.join(extra) + '\n'
            else: prev = b.rstrip('\n') + '\n\n' + prev.lstrip('\n')   # stats first, then the story and suggested deeds
            merged[h] = prev
        else: merged[h] = b
    for h, b in merged.items():
        f = folder or OVERRIDE.get(h) or wcat(h)
        if folder is None: f = 'Wondrous Items/' + f
        name = fname(h)
        assert name not in items, (name, page)
        items[name] = dict(title=h, folder=f, body=b, page=page, foot=foot, list=(folder or f.split('/')[-1]))
        oldmap[(page, h)] = (name, None)
        for sub in re.findall(r'^#{3,5} (.+)$', b, re.M): oldmap[(page, sub.strip())] = (name, sub.strip())
        lists[items[name]['list']].append(name)
    pages_out[page] = (front, pre, keep, foot)
print('items', len(items)); print({k: len(v) for k, v in lists.items()})
# ---------- item pages
def fix_self_links(b, page):
    def sub(m):
        anc, alias = m.group(1), m.group(2)
        tgt = oldmap.get((page, anc))
        if not tgt: return m.group(0)
        n, a = tgt; return f'[[{n}{"#" + a if a else ""}{alias or "|" + anc}]]'
    return re.sub(r'\[\[#([^\]|\\]+)((?:\\?\|)[^\]]*)?\]\]', sub, b)
out_files = {}
for name, it in items.items():
    b = fix_self_links(it['body'], it['page']).strip('\n')
    b = re.sub(r'^###? ', lambda m: '## ' if m.group(0) == '### ' else m.group(0), b, flags=re.M)   # promote subheadings by one
    b = re.sub(r'^####', '###', b, flags=re.M)
    lines = b.split('\n')
    for i, l in enumerate(lines):
        if re.match(r'^\*[A-Z][^*]*\*(\s*%%.*%%)?$', l.strip()) and RAR.search(l): lines[i] = typeline_link(l); break
    b = link_conditions('\n'.join(lines))
    b = re.sub(r'\[\[' + re.escape(name) + r'(?:\\?\|([^\]]*))?\]\]', lambda m: m.group(1) or name, b)
    aliases = [it['title']] if fname(it['title']) != it['title'] else []
    fm = '---\n' + (f'aliases: [{", ".join(json.dumps(a, ensure_ascii=False) for a in aliases)}]\n' if aliases else '') + 'publish: true\n---\n'
    lst = it['list']
    nav = f'Part of [[{lst}]]' + (' in [[Wondrous Items]]' if it['folder'].startswith('Wondrous') else '') + '. See also [[Magic Items A–Z]] and [[Magic Items by Rarity]].'
    foot = it['foot'] if '%% source' not in b[:200] or 'CC BY' not in it['foot'] else '---\n<small>Sources: [[Credits]].</small>'
    if '%% source' in b[:200]: foot = '---\n<small>Sources: [[Credits]].</small>'
    out_files[f'{MI}{it["folder"]}/{name}.md'] = fm + b + '\n\n' + nav + '\n\n' + (foot or '---\n<small>Sources: [[Credits]].</small>') + '\n'
# ---------- list pages
def row(name):
    it = items[name]; t = next((l for l in it['body'].split('\n') if re.match(r'^\*[A-Z]', l.strip()) and RAR.search(l)), '')
    kind, rar, att, pr = parse_type(t) if t else ('—', '—', '—', '—')
    if att == '—':
        bl = [l for l in it['body'].split('\n') if l.strip()]
        if t in bl and bl.index(t) + 1 < len(bl) and re.match(r'^\*\(Requires? Attunement', bl[bl.index(t) + 1]):
            x = re.match(r'^\*\(Requires? Attunement\s*([^)]*)\)', bl[bl.index(t) + 1]).group(1); att = x or 'Yes'
    if name == 'Jarlpact Rings': kind, rar, att, pr = 'Ring (set of four)', 'Rarity Varies', 'Yes', 'Price Varies'
    if '%% price pending' in t: pr = 'pending'
    return name, kind, rar, att, pr
ROWS = {n: row(n) for n in items}
RORDER = ['Common', 'Uncommon', 'Rare', 'Very Rare', 'Legendary', 'Artifact', 'Fabled', 'Rarity Varies', 'Rarity by Figurine', '—']
def table(names, cat_col=False):
    h = '| Item | Type | Rarity | Attunement | Price |' + (' Category |' if cat_col else '')
    out = [h, '|' + '---|' * (6 if cat_col else 5)]
    for n in sorted(names, key=lambda x: x.lower()):
        _, k, r, a, p = ROWS[n]; c = items[n]['list']
        out.append(f'| [[{n}]] | {k} | {r} | {a} | {p} |' + (f' [[{c}]] |' if cat_col else ''))
    return '\n'.join(out)
WDESC = {}
for page, (front, pre, keep, foot) in pages_out.items():
    if page.startswith('Wondrous Items'): continue
    body = pre.rstrip('\n') + ('\n\n' if pre.strip() else '') + ''.join(f'## {h}\n{b.rstrip()}\n\n' for h, b in keep)
    body += '## Items\n\n' + table(lists[PAGES[page][0]]) + '\n'
    out_files[MI + page + '.md'] = front + body.lstrip('\n') + '\n' + (foot or '---\n<small>Sources: [[Credits]].</small>') + '\n'
wcats = sorted(k for k in lists if k not in [v[0] for v in PAGES.values()])
for c in wcats:
    out_files[f'{MI}Wondrous Items/{c}.md'] = '---\npublish: true\n---\nWondrous items of this kind. All wondrous items are listed on [[Wondrous Items]].\n\n## Items\n\n' + table(lists[c]) + '\n\n---\n<small>Sources: [[Credits]].</small>\n'
out_files[f'{MI}Wondrous Items/Wondrous Items.md'] = '---\naliases: [Wondrous Item]\npublish: true\n---\nWondrous items are worn items such as boots, belts, cloaks and amulets, and other objects such as bags, instruments and figurines. They are grouped by kind.\n\n| Category | Items |\n|---|---|\n' + '\n'.join(f'| [[{c}]] | {len(lists[c])} |' for c in wcats) + '\n\n## All Wondrous Items\n\n' + table([n for c in wcats for n in lists[c]], True) + '\n\n---\n<small>Sources: [[Credits]].</small>\n'
allnames = list(items)
out_files[MI + 'Magic Items A–Z.md'] = '---\naliases: [All Magic Items, Magic Item List]\npublish: true\n---\nEvery magic item on this wiki, in alphabetical order. Each name links to the item’s own page.\n\n' + table(allnames, True) + '\n\n---\n<small>Sources: [[Credits]].</small>\n'
byr = collections.defaultdict(list)
for n in allnames: byr[ROWS[n][2]].append(n)
out_files[MI + 'Magic Items by Rarity.md'] = '---\naliases: [Magic Items by Rarity]\npublish: true\n---\nEvery magic item, grouped by rarity, for handing out treasure. See [[Using Magic Items#Rarity|Rarity]] for what each rarity means.\n\n' + '\n\n'.join(f'## {r}\n\n' + table(byr[r], True) for r in RORDER if byr.get(r)) + '\n\n---\n<small>Sources: [[Credits]].</small>\n'
hub = read(MI + 'Magic Items.md').replace('- [[Wondrous Items A–L]]\n- [[Wondrous Items M–Z]]\n', '- [[Wondrous Items]]\n')
assert '- [[Wondrous Items]]\n- [[Magic Tattoos]]' in hub, 'hub'
hub = hub.replace('## Magic Items by Type\n', '## All Magic Items\n- [[Magic Items A–Z]]\n- [[Magic Items by Rarity]]\n\n## Magic Items by Type\n')
out_files[MI + 'Magic Items.md'] = hub
# ---------- relink the wiki
def relink_text(s, selfname=None):
    if '\n' in s: return '\n'.join(relink_text(l) for l in s.split('\n'))
    T = [s.lstrip().startswith('|')]
    def sub(m):
        pg, anc, alias = m.group(1), m.group(2), m.group(3)
        t = oldmap.get((pg, anc)) if anc else None
        if not t: return m.group(0)
        n, a = t
        sep = (alias[:2] if alias.startswith('\\|') else '|') if alias else ('\\|' if T[0] else '|')
        txt = alias[len(sep):] if alias else (a or anc)
        tgt = n + ('#' + a if a else '')
        if txt == n and not a: return f'[[{n}]]'
        return f'[[{tgt}{sep}{txt}]]'
    return re.sub(r'\[\[([^\]#|\\]+)#([^\]|\\]+)?((?:\\?\|)[^\]]*)?\]\]|\[\[(Wondrous Items [AM]–[LZ])((?:\\?\|)[^\]]*)?\]\]',
                  lambda m: sub(m) if m.group(1) else (f'[[Wondrous Items{m.group(5)}]]' if m.group(5) and m.group(5).lstrip('\\|') != 'Wondrous Items' else '[[Wondrous Items]]'), s)
changed = 0; nlinks = 0
for dp, dn, fn in os.walk(V):
    dn[:] = [d for d in dn if not d.startswith('.')]
    for f in fn:
        if not f.endswith('.md'): continue
        p = os.path.join(dp, f); rel = os.path.relpath(p, V)
        if rel in out_files: continue
        s = open(p, encoding='utf-8').read(); n = relink_text(s)
        if n != s:
            changed += 1; nlinks += sum(1 for a, b in zip(re.findall(r'\[\[[^\]]*\]\]', s), re.findall(r'\[\[[^\]]*\]\]', n)) if a != b)
            if W: open(p, 'w', encoding='utf-8').write(n)
for rel in list(out_files): out_files[rel] = relink_text(out_files[rel])
print('pages relinked', changed, 'links', nlinks, 'files to write', len(out_files))
if W:
    for rel, s in out_files.items():
        os.makedirs(os.path.dirname(os.path.join(V, rel)), exist_ok=True); open(os.path.join(V, rel), 'w', encoding='utf-8').write(s)
    for pg in ('Wondrous Items A–L', 'Wondrous Items M–Z'): os.remove(os.path.join(V, MI + pg + '.md'))
else:
    os.makedirs('/home/claude/ts/split', exist_ok=True)
    for rel, s in out_files.items():
        q = '/home/claude/ts/split/' + rel; os.makedirs(os.path.dirname(q), exist_ok=True); open(q, 'w', encoding='utf-8').write(s)
