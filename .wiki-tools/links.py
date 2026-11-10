import os,re,sys,collections
root=sys.argv[1]; names={}; aliases={}; pub={}
for dp,dns,fns in os.walk(root):
    dns[:]=[d for d in dns if not d.startswith('.')]
    for f in fns:
        p=os.path.join(dp,f); r=os.path.relpath(p,root)
        if f.endswith('.md'):
            t=open(p,encoding='utf-8').read()
            fm=re.match(r'^---\n(.*?)\n---',t,re.S); fmt=fm.group(1) if fm else ''
            ispub=not re.search(r'^publish: false',fmt,re.M) and not r.startswith(('_GM Only','z_templates','Calculators','Assets'+os.sep+'Excalidraw'))
            names[f[:-3].lower()]=ispub; pub[r]=(ispub,t)
            m=re.search(r'^aliases:\s*\[(.*?)\]',fmt,re.M)
            if m:
                for a in m.group(1).split(','):
                    a=a.strip().strip('"\'')
                    if a: names.setdefault(a.lower(),ispub)
        else: names[f.lower()]=True
dead=collections.Counter(); tohidden=collections.Counter(); where=collections.defaultdict(set)
new=set(sys.argv[2:])
for r,(ispub,t) in pub.items():
    if not ispub: continue
    for m in re.finditer(r'!?\[\[([^\]|#\\]+)',t):
        tgt=m.group(1).strip(); k=os.path.basename(tgt).lower()
        if k.endswith('.md'): k=k[:-3]
        if k not in names: dead[tgt]+=1; where[tgt].add(r)
        elif not names[k]: tohidden[tgt]+=1; where[tgt].add(r)
print("published notes:",sum(1 for v in pub.values() if v[0]),"hidden:",sum(1 for v in pub.values() if not v[0]))
print("links to pages that don't exist:",sum(dead.values()),"(",len(dead),"targets)")
print("links to hidden pages:",sum(tohidden.values()))
print("--- broken links inside pages I wrote:")
for tgt in list(dead)+list(tohidden):
    for r in where[tgt]:
        if any(r.endswith(n) for n in new): print(" ",tgt,"<-",r)
print("--- broken links in campaign primer:")
for tgt in list(dead)+list(tohidden):
    for r in where[tgt]:
        if 'Between Iron & Oak.md' in r: print(" ",tgt)
print("--- top missing targets:",dead.most_common(15))
