import os,re,sys
root=sys.argv[1]
pages={};heads={}
for dp,dn,fn in os.walk(root):
    dn[:]=[d for d in dn if not d.startswith('.')]
    for f in fn:
        if f.endswith('.md'):
            p=os.path.join(dp,f); n=f[:-3]; pages[n]=p
            hs=set()
            for l in open(p):
                m=re.match(r'^#{1,6} (.+?)\s*$',l)
                if m: hs.add(m.group(1).strip())
            heads[n]=hs
bad=[]
for n,p in pages.items():
    s=open(p).read()
    for m in re.finditer(r'\[\[([^\]|\\]*?)#([^\]|\\]+)',s):
        tgt=m.group(1).strip() or n; a=m.group(2).strip()
        tgt=tgt.split('/')[-1]
        if tgt not in heads: continue
        if a not in heads[tgt] and not a.startswith('^'): bad.append((n,tgt,a))
for b in bad: print(b)
print('bad anchors:',len(bad))
