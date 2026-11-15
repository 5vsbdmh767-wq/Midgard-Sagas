# Errata helper: rewrite(page, heading, new_body) replaces everything under a heading (keeping the
# heading and its "*Nth-Level ... Feature*" line), edit(page, old, new) is an exact one-time replacement.
import os, re, glob
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = ' %% errata 2025-05-29 %%'
_idx = {os.path.basename(p)[:-3]: p for p in glob.glob(V + '/**/*.md', recursive=True) if '/.' not in p}
def _rw(pg, f):
    p = _idx[pg]; s = open(p, encoding='utf-8').read(); s2 = f(s); open(p, 'w', encoding='utf-8').write(s2)
def span(s, h, level=None):
    pat = r'^(#{%s}) ' % (level or '2,5') + re.escape(h) + r'\s*$'
    ms = list(re.finditer(pat, s, re.M)); assert len(ms) == 1, (h, len(ms))
    m = ms[0]; lv = len(m.group(1)); e = re.compile(r'^#{1,%d} ' % lv, re.M).search(s, m.end())
    return m.end(), (e.start() if e else len(s))
def rewrite(pg, h, body, level=None, keep_level_line=True, keep_src=True):
    def f(s):
        a, b = span(s, h, level); old = s[a:b]
        keep = []
        for l in old.strip('\n').split('\n\n'):
            if keep_src and l.startswith('%% source'): keep.append(l); continue
            if keep_level_line and re.match(r'^\*[^*].*(Feature|Level)[^*]*\*$', l): keep.append(l); continue
            break
        return s[:a] + '\n\n' + '\n\n'.join(keep + [body.strip() + E]) + '\n\n' + s[b:].lstrip('\n')
    _rw(pg, f)
def edit(pg, old, new, n=1):
    def f(s):
        assert s.count(old) == n, (pg, old[:60], s.count(old)); return s.replace(old, new)
    _rw(pg, f)
