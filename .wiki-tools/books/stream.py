# Column-aware PDF-to-markdown extractor for Kobold Press two-column books.
# Usage: python3 -I stream.py BOOK.pdf FIRST LAST            -> debug listing
#        import stream; stream.render(pdf, first, last)       -> markdown
# Fonts are tuned for Trade Secrets (Modesto headings, Segoe tables, Verdigris body).
import pymupdf, re, sys

_docs = {}
def doc(path):
    if path not in _docs: _docs[path] = pymupdf.open(path)
    return _docs[path]

def tag(f):
    if 'BdIt' in f or 'BoldItalic' in f: return 'bi'
    if '-Bd' in f or 'Semibold' in f or 'Black' in f or f.endswith('-Bold'): return 'b'
    if '-It' in f or 'Italic' in f: return 'i'
    return ''
MK = {'bi': '***', 'b': '**', 'i': '*', '': ''}

def md(segs):
    m = []
    for t, x in segs:
        if m and m[-1][0] == t: m[-1][1] += x
        elif not x.strip() and m: m[-1][1] += x
        else: m.append([t, x])
    out = ''
    for t, x in m:
        if not t or not x.strip(): out += x; continue
        lead = x[:len(x) - len(x.lstrip())]; trail = x[len(x.rstrip()):]
        out += lead + MK[t] + x.strip() + MK[t] + trail
    return re.sub(r'[  \t\n]+', ' ', out).replace('‑', '-')

def kind(f, sz):
    if 'PhantomLord' in f: return 'CH'
    if 'Modesto' in f:
        if sz >= 24: return 'H1'
        if 16.5 <= sz < 17.5: return 'H2'
        if sz >= 17.5: return 'RUN'
        if sz >= 14.5: return 'H3'
        return 'H4'
    if 'GillSans' in f: return 'PG'
    if 'Segoe' in f: return 'SEG'
    return 'B'

def elements(pdf, a, b):
    d = doc(pdf); els = []
    for pi in range(a - 1, b):
        pg = d[pi]; W = pg.rect.width
        lines = []
        for blk in pg.get_text('dict')['blocks']:
            if blk['type'] != 0: continue
            for l in blk['lines']:
                sp = [s for s in l['spans'] if s['text'].strip()]
                if not sp: continue
                k = kind(sp[0]['font'], sp[0]['size'])
                if k in ('PG', 'RUN'): continue
                if k == 'SEG' and len(sp) == 1 and 'Semibold' in sp[0]['font'] and sp[0]['size'] >= 9.8: k = 'ITEM'
                x0 = min(s['bbox'][0] for s in sp); y = sp[0]['origin'][1]
                col = 0 if x0 < W / 2 - 8 else 1
                full = x0 < W / 2 - 20 and max(s['bbox'][2] for s in sp) > W / 2 + 20 and k != 'SEG'
                lines.append(dict(pg=pi + 1, col=-1 if full else col, y=y, x=x0, k=k, blk=id(blk),
                                  spans=[(s['font'], s['size'], s['text'], s['bbox'][0], s['bbox'][2]) for s in l['spans']],
                                  title=(k == 'SEG' and len(sp) == 1 and (sp[0]['font'] == 'SegoeUI' or ('Semibold' in sp[0]['font'] and sp[0]['size'] >= 9)))))
        top = min([q['y'] for q in lines if q['col'] != -1], default=0)
        lines.sort(key=lambda L: (L['col'] != -1 or L['y'] > top, L['col'], L['y'], L['x']))
        els.append(('PAGE', pi + 1))
        i = 0
        while i < len(lines):
            L = lines[i]
            if L['k'] in ('H1', 'H2', 'H3', 'H4', 'CH', 'ITEM'):
                txt = re.sub(r'\s+', ' ', ''.join(s[2] for s in L['spans'])).strip()
                while i + 1 < len(lines) and lines[i + 1]['k'] == L['k'] and lines[i + 1]['col'] == L['col'] and lines[i + 1]['y'] - lines[i]['y'] < 30:
                    i += 1; txt += ' ' + re.sub(r'\s+', ' ', ''.join(s[2] for s in lines[i]['spans'])).strip()
                els.append((L['k'], txt, L['pg'], L['col'], L['y'])); i += 1; continue
            if L['k'] == 'SEG':
                grp = [L]; j = i + 1
                while j < len(lines) and lines[j]['k'] == 'SEG' and lines[j]['col'] == L['col'] and lines[j]['y'] - grp[-1]['y'] < 24:
                    grp.append(lines[j]); j += 1
                els.append(('SEG', grp, L['pg'], L['col'], L['y'])); i = j; continue
            grp = [L]; j = i + 1
            while j < len(lines) and lines[j]['blk'] == L['blk'] and lines[j]['k'] == 'B': grp.append(lines[j]); j += 1
            segs = []
            for g in grp:
                for f, sz, t, _, _ in g['spans']: segs.append((tag(f), t))
                segs.append(('', ' '))
            els.append(('B', md(segs).strip(), L['pg'], L['col'], L['y'])); i = j
    return els

def table_md(grp):
    rows = []
    for g in grp:
        for f, sz, t, x0, x1 in g['spans']:
            if not t.strip(): continue
            y = g['y']
            r = next((r for r in rows if abs(r['y'] - y) <= 2.5), None)
            if r is None: r = {'y': y, 'sp': [], 'title': g['title']}; rows.append(r)
            r['sp'].append((x0, x1, tag(f), t, f, sz))
    rows.sort(key=lambda r: r['y'])
    out_title = []
    while rows and rows[0]['title'] and len(rows[0]['sp']) == 1:
        out_title.append(''.join(s[3] for s in sorted(rows[0]['sp'])).strip()); rows.pop(0)
    hdr = []
    while rows and all(s[2] == 'b' for s in rows[0]['sp']): hdr.append(rows.pop(0))
    if not hdr and len(rows) >= 3 and sum(len(''.join(s[3] for s in r['sp'])) for r in rows) / len(rows) > 35:
        # a sidebar set in the table font: return it as one note callout
        txt = md([(s[2], s[3] + ' ') for r in rows for s in sorted(r['sp'])])
        txt = re.sub(r'(\w)- (\w)', r'\1-\2', txt).strip()
        return '> [!note]' + (' ' + ' '.join(out_title) if out_title else '') + '\n> ' + txt + '\n'
    cols = []
    for r in hdr:
        for s in sorted(r['sp']):
            if not any(abs(s[0] - c) < 10 for c in cols): cols.append(s[0])
    if not cols:
        for r in rows[:3]:
            for s in r['sp']:
                if not any(abs(s[0] - c) < 10 for c in cols): cols.append(s[0])
    cols.sort()
    if not cols: return ''
    def ci(x):
        j = 0
        for i, c in enumerate(cols):
            if x >= c - 10: j = i
        return j
    def cells(r):
        cs = [[] for _ in cols]
        for x0, x1, tg, t, f, sz in sorted(r['sp']): cs[ci(x0)].append((tg, t))
        return [md(c).strip() for c in cs]
    H = [''] * len(cols)
    for r in hdr:
        for i, c in enumerate(cells(r)):
            c = c.replace('**', '')
            if c: H[i] = (H[i] + ' ' + c).strip()
    body = []; foot = []; prev_y = None
    for r in rows:
        c = cells(r)
        first = min(s[0] for s in r['sp'])
        if first < cols[0] - 3 or (c[0].startswith('*') and not c[0].startswith('**') and sum(1 for z in c if z) == 1 and len(c[0]) > 15):
            foot.append(' '.join(z for z in c if z)); continue
        if foot: foot[-1] += ' ' + ' '.join(z for z in c if z); continue
        if not c[0] and body and prev_y is not None and r['y'] - prev_y < 16:
            for i, z in enumerate(c):
                if z: body[-1][i] = (body[-1][i] + ' ' + z).strip()
        else: body.append(c)
        prev_y = r['y']
    s = ''
    if out_title: s += '**' + ' '.join(out_title) + '**\n\n'
    s += '| ' + ' | '.join(H) + ' |\n|' + '---|' * len(cols) + '\n'
    for b in body: s += '| ' + ' | '.join(z.replace('|', '\\|') for z in b) + ' |\n'
    for f in foot: s += '\n' + re.sub(r'^\*(?=\s)', '\\*', f) + '\n'
    return s

SMALL = {'a', 'an', 'the', 'and', 'or', 'of', 'in', 'for', 'to', 'as', 'by', 'from', 'with', 'on', 'at'}
def render(pdf, a, b, hmap={'CH': '#', 'H1': '#', 'H2': '##', 'H3': '###', 'H4': '####', 'ITEM': '###'}):
    out = []
    def unfinished(t): return not re.search(r'[.!?:”"\)\*]$', t.strip())
    lastB = None
    for e in elements(pdf, a, b):
        if e[0] == 'PAGE': continue
        if e[0] == 'B':
            t = e[1]
            if lastB is not None and out[lastB].strip() and unfinished(out[lastB]) and (t[:1].islower() or t[:1] in '(,;'):
                out[lastB] = out[lastB].rstrip() + ' ' + t; continue
            out.append(t); lastB = len(out) - 1; continue
        if e[0] == 'SEG': out.append(table_md(e[1])); continue
        txt = e[1]
        if e[0] == 'H2':
            txt = ' '.join(w.lower() if (w.lower() in SMALL and i) else w[:1].upper() + w[1:].lower() for i, w in enumerate(txt.split()))
        out.append(hmap[e[0]] + ' ' + txt)
    return re.sub(r' +\n', '\n', '\n\n'.join(out))

if __name__ == '__main__':
    pdf, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    for e in elements(pdf, a, b):
        if e[0] == 'PAGE': print(f'\n=== PAGE {e[1]}'); continue
        if e[0] == 'SEG': print(f'[SEG col{e[3]} y{round(e[4])}]\n' + table_md(e[1]))
        else: print(f'[{e[0]} col{e[3]} y{round(e[4])}] {e[1][:150]}')
