# Replace "(see Player's Guide)" style notes with links to the wiki's own pages.
# Dry run prints every change and every note it could not resolve; --write applies.
import sys, os, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
SKIPF = {"Player's Guide 2.md", 'Recommended Magic Items by Class.md', 'Credits.md'}
files = [p for p in glob.glob(V + '/Rules/**/*.md', recursive=True) if os.path.basename(p) not in SKIPF]
H = {}   # lowercase heading -> [(page, heading)]
for p in files:
    pg = os.path.basename(p)[:-3]
    for m in re.finditer(r'^#{2,5} (.+?)\s*$', open(p, encoding='utf-8').read(), re.M):
        H.setdefault(m.group(1).lower().replace('’', "'"), []).append((pg, m.group(1)))
CLASSES = {os.path.basename(p)[:-3] for p in glob.glob(V + '/Rules/Classes/*.md')} - {'Classes'}
SPELLP = re.compile(r'^(Cantrips|\d\w\w-Circle Spells|Rituals .*)$')
def find(name, page, prefer=None):
    c = H.get(name.lower().replace('’', "'"), [])
    if not c: return None
    for pg, h in c:
        if pg == page: return (pg, h)
    if prefer:
        pc = [x for x in c if prefer(x[0])]
        if len({x[0] for x in pc}) == 1: return pc[0]
    if len({x[0] for x in c}) == 1: return c[0]
    return None
def link(t, page, shown, intable):
    pg, h = t; bar = '\\|' if intable else '|'
    return f'[[#{h}{bar}{shown}]]' if pg == page else f'[[{pg}#{h}{bar}{shown}]]'
PG = r"(?:the )?\*{0,2}Player[’']s\*{0,2} ?\*{0,2}Guide\*{0,2}(?: and \*Player[’']s Guide 2\*)?"
NOTE = re.compile(r" ?\((?:see|See) (?:(?P<what>[^()]*?) (?:in|of) )?" + PG + r"(?P<tail> for [^()]*?)?\.?\)")
MANUAL = {'downtime crafting activity': ('Between Adventures', 'Crafting'), 'sorcery points': ('Sorcerer', 'Sorcery Points'), 'sorcery point': ('Sorcerer', 'Sorcery Points'),
          'technique points': ('Monk', 'Techniques'), 'technique point': ('Monk', 'Techniques')}
changes = []; unresolved = []
def fix_line(line, page):
    intable = line.startswith('|')
    def sub(m):
        pre = line[:m.start()]; what = m.group('what'); tail = m.group('tail')
        def done(newpre_suffix=None, repl=''):
            return repl
        if what:
            w = re.sub(r'\*\*|\*', '', what).strip(); w2 = re.sub(r'^(?:the )?(.*?)(?: (?:class )?feature| downtime activity| rules| sidebar| section)?$', r'\1', w)
            w2 = re.sub(r' in \*\*Chapter \d+\*\*$| in Chapter \d+$', '', w2)
            cands = [w2, w2.title()] + ([w2 + ' Class Features'] if w2.lower() in {c.lower() for c in CLASSES} else [])
            if re.match(r'^(the )?(\w+)( class| or \w+)?$', w, re.I) and w2.split()[0].title() in CLASSES:
                c = w2.split()[0].title(); return f' (see [[{c}{chr(92) if intable else ""}|{w2}]])' if c != page else ''
            NAMED = {'weapons': ('Weapons', None), 'weapon options': ('Weapons', 'Weapon Options'), 'talents': ('Talents', None), 'luck': ('Rolling the Dice', 'Luck'),
                     'vehicle repair': ('Vehicles', 'Vehicle Repairs'), 'class progression tables': ('Classes', None), 'squeezing into a smaller space': ('Encounter Gameplay', None)}
            if w2.lower() in NAMED:
                pg_, h_ = NAMED[w2.lower()]; bar = '\\|' if intable else '|'
                return f' (see [[{pg_}{"#" + h_ if h_ else ""}{bar}{w2}]])'
            for cnd in cands:
                t = find(cnd, page, lambda p: p in CLASSES)
                if t: return f' (see {link(t, page, w2, intable)})'
            unresolved.append((page, 'named: ' + m.group(0).strip())); return m.group(0)
        if tail: # "for spells", "for both": the things are named just before
            if '[[' in pre[-400:]: return ''
            i0 = max(pre.rfind('. ', 0, len(pre) - 2), 0); seg = pre[i0:]; hit = [0]
            def li(mi):
                outp = []
                for part in re.split(r'(, (?:and |or )?| and | or )', mi.group(1)):
                    t = find(part.strip().rstrip('.'), page, lambda p: bool(SPELLP.match(p)))
                    if t and part.strip(): outp.append(link(t, page, part, intable)); hit[0] += 1
                    else: outp.append(part)
                return '*' + ''.join(outp) + '*'
            seg2 = re.sub(r'(?<![*\w])\*([^*\n]{3,200}?)\*(?![*\w])', li, seg)
            if hit[0]: return ('LINK', i0, len(pre), seg2)
            unresolved.append((page, 'tail: ' + pre[-60:] + m.group(0))); return m.group(0)
        if re.search(r'\]\]\*?(?: spells?| cantrips?| ritual)?$', pre): return ''
        mm = re.search(r'(?:[Yy]our |[Tt]he |an? )?((?:[A-Z][\w’\'-]*(?: of| the| to| on| in| and| a)? ?)+)(?:class )?(feature|boon|trait|augment)s?$', pre)
        if mm:
            nm = mm.group(1).strip(); t = find(nm, page, lambda p: p in CLASSES)
            if t: return ('LINK', mm.start(1), mm.start(1) + len(mm.group(1).rstrip()), link(t, page, nm, intable))
        mm = re.search(r'((?:[A-Z][\w’\'-]*(?: of| the| to| on)? ?)+)$', pre)
        if mm and mm.group(1).strip():
            nm = mm.group(1).strip(); t = find(nm, page, lambda p: p == page)
            if t and t[0] == page: return ('LINK', mm.start(1), mm.start(1) + len(nm), link(t, page, nm, intable))
        mm = re.search(r'downtime (researching|carousing|crafting|training|working)$', pre)
        if mm: return ('LINK', mm.start(1), mm.end(1), link(('Between Adventures', mm.group(1).title()), page, mm.group(1), intable))
        mm = re.search(r'(\w+) Progression table$', pre)
        if mm and mm.group(1) == page: return ''
        mm = re.search(r'(\w+) (?:downtime )?activity(?: description)?$', pre)
        if mm and find(mm.group(1), 'Between Adventures'):
            t = ('Between Adventures', mm.group(1).title()); return ('LINK', mm.start(1), mm.end(1), link(t, page, mm.group(1), intable))
        for k, t in MANUAL.items():
            if pre.lower().endswith(k):
                i = len(pre) - len(k); return ('LINK', i, len(pre), link(t, page, pre[i:], intable))
        mm = re.search(r'\*\*(\w+) Progression\*\* table$', pre)
        if mm: return '' if mm.group(1) == page else ('LINK', mm.start(), len(pre), f'{link((mm.group(1), "Class Features"), page, mm.group(1) + " Progression", intable)} table')
        mm = re.search(r'\*?([a-z][a-z’\' ]{3,30}?)\*? (spell|cantrip)$', pre)
        if mm:
            words = mm.group(1).split()
            for k in range(min(4, len(words)), 0, -1):
                nm = ' '.join(words[-k:]); t = find(nm, page, lambda p: bool(SPELLP.match(p)))
                if t and SPELLP.match(t[0]):
                    i = pre.rfind(nm); return ('LINK', i, i + len(nm), '*' + link(t, page, nm, intable) + '*' if pre[i-1:i] != '*' else link(t, page, nm, intable))
        unresolved.append((page, 'bare: ' + pre[-70:] + m.group(0))); return m.group(0)
    line = re.sub(r'(?<=\w)\* \*(?=\w)', ' ', line); line = re.sub(r'\*([a-z’ ]+) spell\*', r'*\1* spell', line); out = line
    for _ in range(12):
        m = NOTE.search(out)
        if not m: break
        line_ = out
        def run():
            nonlocal line
            line = line_
            return sub(m)
        r = run()
        if isinstance(r, tuple):
            _, a, b, lk = r; new = out[:a] + lk + out[b:m.start()] + out[m.end():]
        elif r == m.group(0):
            out = out[:m.start()] + '\x00' + out[m.start():]   # guard so the loop moves on
            out = out[:m.start()+1] + out[m.start()+1:].replace('(', '\x01', 1); continue
        else: new = out[:m.start()] + r + out[m.end():]
        changes.append((page, out[max(0, m.start()-60):m.end()], new[max(0, m.start()-60):m.start()+len(new)-len(out)+len(m.group(0))+25])); out = new
    return out.replace('\x00', '').replace('\x01', '(')
for p in sorted(files):
    page = os.path.basename(p)[:-3]; s = open(p, encoding='utf-8').read()
    new = '\n'.join(fix_line(l, page) if 'Guide' in l and '%%' not in l[:3] else l for l in s.split('\n'))
    if new != s and '--write' in sys.argv: open(p, 'w', encoding='utf-8').write(new)
print('changed', len(changes), 'unresolved', len(unresolved))
if '--write' not in sys.argv:
    with open('/home/claude/ts/see_changes.txt', 'w') as f:
        for c in changes: f.write(f'{c[0]}\n   - {c[1]}\n   + {c[2]}\n')
    for u in unresolved: print(u[0], '|', u[1][:170])
