# Shared helpers for magic item pages.
import re
BAD = {':': ',', '/': '-', '?': '', '"': '', '<': '', '>': '', '|': '-', '*': '', '#': '', '^': '', '[': '(', ']': ')'}
def fname(n): return ''.join(BAD.get(ch, ch) for ch in n).strip().rstrip('.')
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
