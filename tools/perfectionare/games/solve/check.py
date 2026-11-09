import numpy as np, random
V=np.load(r'C:/Users/irina/AppData/Local/Temp/claude/5f5cca6ec2cb1060/57a79c16-0421-4278-82d3-fb32d3123bed/scratchpad/V.npy')
D={'Q':[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)],'R':[(1,0),(-1,0),(0,1),(0,-1)],'B':[(1,1),(1,-1),(-1,1),(-1,-1)]}
KN=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
def targets(t,s,occ):
    f,r=divmod(s,8);out=[]
    if t=='N':
        return [(f+a)*8+r+b for a,b in KN if 0<=f+a<8 and 0<=r+b<8]
    for a,b in D[t]:
        x,y=f+a,r+b
        while 0<=x<8 and 0<=y<8:
            out.append(x*8+y)
            if x*8+y in occ: break
            x+=a;y+=b
    return out
from functools import lru_cache
@lru_cache(None)
def wwin(q,r,n,b,d):  # white to move wins within d
    if d<=0: return False
    P={'Q':q,'R':r,'N':n};occ={q,r,n,b}
    for t,s in P.items():
        if b in targets(t,s,occ): return True
    if d==1: return False
    for t,s in P.items():
        for u in targets(t,s,occ):
            if u in occ: continue
            P2=dict(P);P2[t]=u
            if blost(P2['Q'],P2['R'],P2['N'],b,d-1): return True
    return False
@lru_cache(None)
def blost(q,r,n,b,d):
    occ={q,r,n,b}
    ts=targets('B',b,occ)
    if any(u in (q,r,n) for u in ts): return False
    return all(wwin(q,r,n,u,d) for u in ts)
st=(24,32,48,23)
print([wwin(*st,d) for d in (1,2,3)], V[st])
random.seed(1);bad=0
for i in range(300):
    s=random.sample(range(64),4); v=int(V[tuple(s)])
    for d in range(1,5):
        if wwin(*s,d)!=(v!=0 and v<=d): bad+=1;print('bad',s,v,d)
print('bad',bad)
