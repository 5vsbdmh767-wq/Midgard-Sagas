# Parse Trade Secrets' "Recommended Magic Items by Class" tables (PDF pages 124-130)
# into rows: (tier, class, item, source_number, price, application).
import pymupdf, re
PDF = '/mnt/user-data/uploads/Trade-Secrets.pdf'

def spans(pg):
    out = []
    for b in pg.get_text('dict')['blocks']:
        if b['type']: continue
        for l in b['lines']:
            for s in l['spans']:
                if s['text'].strip() and 'Segoe' in s['font']:
                    out.append(dict(y=s['origin'][1], x=s['bbox'][0], x1=s['bbox'][2], f=s['font'], sz=s['size'], t=s['text']))
    return out

def parse():
    d = pymupdf.open(PDF)
    rows = []; tier = None; cls = None
    for pi in range(123, 130):
        pg = d[pi]; S = spans(pg)
        heads = sorted([s for s in S if s['t'].strip() == 'Magic Items' and 'Black' in s['f']], key=lambda s: s['y'])
        titles = sorted([s for s in S if 'Recommended Magic Items by Class' in s['t']], key=lambda s: s['y'])
        for hi, h in enumerate(heads):
            title = max([t for t in titles if t['y'] < h['y']], key=lambda t: t['y'])
            m = re.match(r'Tier (\d)', title['t']); tier = int(m.group(1))
            same = [s for s in S if abs(s['y'] - h['y']) < 2 and 'Black' in s['f']]
            xc = min(s['x'] for s in same); xi = h['x']
            xp = [s['x'] for s in same if s['t'].strip() == 'Price'][0]
            xa = [s['x'] for s in same if s['t'].strip() == 'Application'][0]
            ybot = min([t['y'] for t in titles if t['y'] > h['y']] + [s['y'] for s in S if s['y'] > h['y'] and re.match(r'^\s*1\s*$', s['t']) and s['x'] < xi and s['sz'] > 6] + [9999])
            body = [s for s in S if h['y'] + 3 < s['y'] < ybot - 1 and s['x'] >= xc - 2 and s['x'] < (xa + 300)]
            # stop at the footnote row (Player's Guide markers)
            foot = [s for s in body if 'Player’s Guide' in s['t'] or 'Labyrinth Worldbook' in s['t']]
            if foot: body = [s for s in body if s['y'] < min(f['y'] for f in foot) - 2]
            col = lambda s: 0 if s['x'] < xi - 2 else 1 if s['x'] < xp - 2 else 2 if s['x'] < xa - 2 else 3
            # items: italic lines in column 1, ended by a small source marker
            c1 = sorted([s for s in body if col(s) == 1], key=lambda s: (round(s['y'] + (2.8 if s['sz'] < 6 else 0)), s['x']))
            items = []; cur = None
            for s in c1:
                if s['sz'] < 6:
                    if cur is None: continue
                    cur['src'] = s['t'].strip(); items.append(cur); cur = None; continue
                txt = s['t']
                msup = re.match(r'^(.*?)(\d|²)$', txt.strip()) if s['sz'] > 6 and re.search(r'[a-z\)]\d$|²$', txt.strip()) else None
                if cur is None: cur = dict(y=s['y'], name='', src=None)
                if msup:
                    cur['name'] += msup.group(1); cur['src'] = msup.group(2).replace('²', '2'); items.append(cur); cur = None
                else:
                    cur['name'] += txt
            if cur: items.append(cur)
            for it in items: it['name'] = re.sub(r'\s+', ' ', it['name']).strip()
            starts = [it['y'] for it in items]
            def bucket(s):
                k = 0
                for i, y in enumerate(starts):
                    if s['y'] >= y - 2.5: k = i
                return k
            prices = [''] * len(items); apps = [[] for _ in items]
            for s in sorted([s for s in body if col(s) == 2], key=lambda s: (round(s['y']), s['x'])):
                if s['sz'] < 6: continue
                prices[bucket(s)] += s['t']
            for s in sorted([s for s in body if col(s) == 3], key=lambda s: (round(s['y']), s['x'])):
                t = s['t']
                if 'Italic' in s['f'] and t.strip(): t = re.sub(r'^(\s*)(.*?)(\s*)$', r'\1*\2*\3', t)
                apps[bucket(s)].append(t)
            classes = sorted([s for s in body if col(s) == 0 and 'Semibold' in s['f']], key=lambda s: s['y'])
            for i, it in enumerate(items):
                cs = [c for c in classes if c['y'] <= it['y'] + 2.5]
                if cs: cls = cs[-1]['t'].strip()
                app = re.sub(r'\s+', ' ', ''.join(apps[i])).strip()
                app = re.sub(r'\*\s*\*', '', app)
                rows.append((tier, cls, it['name'], it['src'], re.sub(r'\s+', ' ', prices[i]).strip(), app))
    return rows

if __name__ == '__main__':
    for r in parse(): print(r[0], '|', r[1], '|', r[2], '|', r[3], '|', r[4], '|', r[5][:90])
