# Helpers for building wiki pages from extracted book text.
import re, os, glob
V = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # vault root

def between(t, a, b=None):
    assert t.count(a) == 1, (a, t.count(a))
    i = t.index(a)
    if b is None: return t[i:]
    j = t.index(b, i + len(a)); return t[i:j]

def rep(t, a, b, n=1):
    assert t.count(a) == n, (a, t.count(a)); return t.replace(a, b)

def demote(x): return re.sub(r'^(#+) ', lambda m: '#' + m.group(1) + ' ', x, flags=re.M)

_idx = None
def idx():
    """lowercase heading -> (page, heading) for spells, rituals and magic items."""
    global _idx
    if _idx is None:
        _idx = {}
        for p in glob.glob(V + '/Rules/Magic/Spells/*.md') + glob.glob(V + '/Rules/Magic/Rituals/*.md') + glob.glob(V + '/Rules/Magic/Magic Items/*.md'):
            n = os.path.basename(p)[:-3]
            for l in open(p, encoding='utf-8'):
                m = re.match(r'^#{2,5} (.+?)\s*$', l)
                if m: _idx.setdefault(m.group(1).strip().lower(), (n, m.group(1).strip()))
    return _idx

def linkitalics(t, report=None):
    """Link *italic* spell/item names to their wiki entries (first form or singular)."""
    def f(m):
        term = m.group(1); k = term.lower().strip()
        for c in (k, k.rstrip('s')):
            if c in idx():
                pg, h = idx()[c]
                if report is not None: report.add(term)
                return f'*[[{pg}#{h}|{term}]]*'
        return m.group(0)
    out = []
    for line in t.split('\n'):
        if line.startswith('|'):
            line = re.sub(r'(?<![*\w])\*([^*\n|]{3,40})\*(?![*\w])', lambda m: f(m).replace('|', '\\|'), line)
        else:
            line = re.sub(r'(?<![*\w])\*([^*\n]{3,40})\*(?![*\w])', f, line)
        out.append(line)
    return '\n'.join(out)

def tidy(t): return re.sub(r'\n{3,}', '\n\n', re.sub(r' +\n', '\n', t))

CREDIT = '\n\n---\n*Material marked as from Trade Secrets is from Trade Secrets by Kobold Press.*\n'
OPT = '*Optional, from Trade Secrets.*\n\n'
