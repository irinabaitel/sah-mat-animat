import sys
exec(open('base.py').read())
sys.setrecursionlimit(10000)
start=tuple(sq(f+'8') for f in 'abcdefgh')
def enc(st):
    st=list(st)
    for t in 'RN':
        i,j=[k for k in range(8) if types[k]==t]
        if st[i]>st[j]: st[i],st[j]=st[j],st[i]
    v=0
    for s in st: v=v*64+s
    return v
def search(bound):
    TT={}; path=[]; cnt=[0]
    def dfs(st,g):
        hh=h(st)
        if g+hh>bound: return False
        if hh==0: return True
        k=enc(st)
        if TT.get(k,999)<=g: return False
        TT[k]=g; cnt[0]+=1
        occ=set(st); ch=[]
        for i in range(8):
            for x in moves(types[i],st[i],occ):
                ns=st[:i]+(x,)+st[i+1:]; ch.append((h(ns),i,x,ns))
        ch.sort()
        for hv,i,x,ns in ch:
            path.append(nm(st[i])+nm(x))
            if dfs(ns,g+1): return True
            path.pop()
        return False
    ok=dfs(start,0); print('bound',bound,ok,'nodes',cnt[0],flush=True); return ok,path
for b in range(29,40):
    ok,p=search(b)
    if ok: print(len(p),' '.join(p)); break
