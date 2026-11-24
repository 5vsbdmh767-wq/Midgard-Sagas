# Writes the "Made with" line on magic item pages from ingredients.json.
# Run from the repo root: python3 -I .wiki-tools/items/ingredients.py
# Safe to re-run: an existing Made with line is replaced, not duplicated.
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, 'ingredients.json'), encoding='utf-8'))
LINK = '[[Crafting Magic Items|Made with]]: '
OLD = re.compile(r'^\[\[Crafting Magic Items\|Made with\]\]: .*\n\n', re.M)

def line(e):
    w = e['made_with']
    if w == 'NOCRAFT':
        return LINK + "can't be crafted."
    if w == 'NONE':
        r = re.sub(r',? per its own text$', '', e['flag'])
        return LINK + 'no monster parts; ' + r + '.'
    if w.startswith('VARIES: '):
        return LINK + w[8:] + ". Use as many as the version's rarity calls for."
    return LINK + w

changed = 0
for path, e in DATA.items():
    t = open(path, encoding='utf-8').read()
    new = OLD.sub('', t)
    i = new.find('\nPart of [[')
    if i < 0:
        print('no footer:', path); continue
    new = new[:i + 1] + line(e) + '\n\n' + new[i + 1:]
    if new != t:
        open(path, 'w', encoding='utf-8').write(new); changed += 1
print('pages changed:', changed)
