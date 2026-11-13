# Shared helpers for the reorganization scripts.
import re, os
V = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def read(rel): return open(os.path.join(V, rel), encoding='utf-8').read()
def write(rel, s):
    p = os.path.join(V, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(re.sub(r'\n{3,}', '\n\n', s).rstrip('\n') + '\n')
def split_front(s):
    m = re.match(r'^---\n.*?\n---\n', s, re.S)
    return (m.group(0), s[m.end():]) if m else ('', s)
def split_footer(s):
    m = re.search(r'\n---\n<small>.*</small>\s*$', s, re.S)
    return (s[:m.start()], s[m.start():].strip('\n')) if m else (s, '')
def sections(body, level=2):
    """Split on headings of exactly `level`. Returns [(title or None, text)]; first item is the preamble."""
    pat = re.compile(r'^' + '#' * level + r' (.+?)\s*$', re.M)
    out = []; pos = 0; title = None
    for m in pat.finditer(body):
        out.append((title, body[pos:m.start()].strip('\n'))); title = m.group(1); pos = m.end()
    out.append((title, body[pos:].strip('\n')))
    return out
LEAD = re.compile(r'^\*\*\*([^*\n]+?)\.?\*\*\*\.? ?')
def paragraphs(text): return [p for p in re.split(r'\n\s*\n', text.strip('\n')) if p.strip()]
def entries(text):
    """Group paragraphs into lead-in entries. Returns (loose_paragraphs_before_first_entry, [(name, [paras])])."""
    loose = []; ents = []
    for p in paragraphs(text):
        m = LEAD.match(p)
        if m and not p.startswith('|'): ents.append((m.group(1).strip(), [p]))
        elif ents: ents[-1][1].append(p)
        else: loose.append(p)
    return loose, ents
def src_of(text):
    m = re.search(r'%% source: ([^%]+?) %%', text); return m.group(1) if m else None
def strip_src(text): return re.sub(r'%% source: [^%]+? %%\n*', '', text)
def key(name): return re.sub(r'^(the|a|an) ', '', re.sub(r'[^a-z0-9 ]', '', name.lower()))
def table_rows(text):
    """All markdown table rows as lists of cells (header and separator rows included)."""
    return [[c.strip() for c in re.split(r'(?<!\\)\|', l.strip().strip('|'))] for l in text.split('\n') if l.startswith('|')]
