# Repoint links after headings change.  usage in scripts: relink({("Weapons","Old Heading"): "New Heading" or None})
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import V
SKIP = ('.git', '.obsidian', '.wiki-tools', '.claude')
def relink(mapping, pages=None):
    """mapping: {(page, old_anchor): new_anchor|None|(new_page, new_anchor|None)}; pages: {old_page: new_page} renames."""
    n = 0
    pat = re.compile(r'\[\[([^\]\[|#]*)(#[^\]\[|]*)?((?:\\?\|)[^\]\[]*)?\]\]')
    for dp, dn, fn in os.walk(V):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if not f.endswith('.md'): continue
            p = os.path.join(dp, f); s = open(p, encoding='utf-8').read(); self_name = f[:-3]
            def sub(m):
                nonlocal n
                page, anc, alias = m.group(1), (m.group(2) or '')[1:], m.group(3) or ''
                tp = page or self_name
                k = (tp, anc)
                if anc and k in mapping:
                    new = mapping[k]; n += 1
                    npage, nanc = (new if isinstance(new, tuple) else (tp, new))
                    shown = '' if (not page and npage == self_name) else npage
                    if not alias and not nanc and not shown: shown = npage
                    if not alias: alias = '|' + anc      # keep the visible text the same
                    return f'[[{shown}{"#" + nanc if nanc else ""}{alias}]]'
                if pages and page in pages:
                    n += 1
                    if not alias and not anc: alias = '|' + page
                    return f'[[{pages[page]}{"#" + anc if anc else ""}{alias}]]'
                return m.group(0)
            t = pat.sub(sub, s)
            if t != s: open(p, 'w', encoding='utf-8').write(t)
    return n

def retire(page, newpage, newanchor=None, aliases=()):
    """Point every link to a removed page (or its aliases) at newpage#newanchor. Sub-anchors are kept on the new page."""
    n = 0; names = (page,) + tuple(aliases)
    pat = re.compile(r'\[\[(' + '|'.join(re.escape(x) for x in names) + r')(#[^\]\[|\\]*)?((?:\\?\|)[^\]\[]*)?\]\]')
    for dp, dn, fn in os.walk(V):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if not f.endswith('.md'): continue
            p = os.path.join(dp, f); s = open(p, encoding='utf-8').read()
            def sub(m):
                nonlocal n; n += 1
                anc = m.group(2) or ('#' + newanchor if newanchor else ''); alias = m.group(3)
                if not alias:
                    line_start = s.rfind('\n', 0, m.start()) + 1
                    bar = '\\|' if s[line_start:line_start + 1] == '|' else '|'
                    alias = bar + m.group(1)
                tgt = '' if f[:-3] == newpage and anc else newpage
                return f'[[{tgt}{anc}{alias}]]'
            new = pat.sub(sub, s)
            if new != s: open(p, 'w', encoding='utf-8').write(new)
    return n
