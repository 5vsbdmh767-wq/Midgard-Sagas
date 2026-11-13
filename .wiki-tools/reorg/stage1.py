# Reorg stage 1: remove book labels from player pages, leave hidden source notes,
# unify footers, add a Credits page. Run from the vault root.
import os, re, sys
V = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP = ('.git', '.obsidian', '.wiki-tools', '.claude', '_GM Only', 'z_templates', 'Assets')
CC = re.compile(r'^\*(This page includes material taken from|Player\'s Guide rules material is taken from) the Black Flag Reference Document 1\.2.*\*\s*$')
MAT = re.compile(r'^\*Material marked .*\*\s*$')
CC_LINE = '<small>Includes material from the Black Flag Reference Document 1.2 by Kobold Press, available at koboldpress.com/Black-Flag-Roleplaying, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode). All sources: [[Credits]].</small>'
SRC_LINE = '<small>Sources: [[Credits]].</small>'
stats = dict(labels=0, tags=0, footers=0, files=0)
def process(p):
    s = open(p, encoding='utf-8').read(); o = s
    # 1. standalone label lines -> hidden source note
    def lab(m):
        stats['labels'] += 1
        src = re.sub(r'\[\[([^\]|]+)(\|[^\]]+)?\]\]', r'\1', m.group(1)).strip().rstrip('.')
        src = re.sub(r'^the ', '', src)
        return f'%% source: {src} %%'
    s = re.sub(r'^\*Optional, from ([^*\n]+?)\*[ \t]*$', lab, s, flags=re.M)
    # 2. inline "(optional, X)" tags
    def tag(m): stats['tags'] += 1; return ''
    s = re.sub(r' ?\*?\(optional(?:,| variant)[^)\n]*\)\*?', tag, s)
    s = re.sub(r' ?\(optional\)', tag, s)
    # 3. footers
    lines = s.split('\n'); had_cc = any(CC.match(l) for l in lines); had_mat = any(MAT.match(l) for l in lines)
    if had_cc or had_mat:
        lines = [l for l in lines if not CC.match(l) and not MAT.match(l)]
        s = '\n'.join(lines).rstrip('\n')
        s = re.sub(r'(\n\s*---\s*)+$', '', s).rstrip('\n')      # trailing rule left behind
        s += '\n\n---\n' + (CC_LINE if had_cc else SRC_LINE) + '\n'
        stats['footers'] += 1
    s = re.sub(r'\n{3,}', '\n\n', s)
    if s != o:
        open(p, 'w', encoding='utf-8').write(s); stats['files'] += 1
for dp, dn, fn in os.walk(V):
    dn[:] = [d for d in dn if d not in SKIP]
    for f in fn:
        if f.endswith('.md'): process(os.path.join(dp, f))
print(stats)
