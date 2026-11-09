# Retrograde: Q,R,N albe contra nebun negru, fără regi. Albul la mutare.
# V[q,r,n,b] = în câte mutări albe capturează albul nebunul (0 = niciodată / stare invalidă).
# Negrul câștigă imediat dacă nebunul atacă o piesă albă (o capturează).
import numpy as np, time, gzip, sys
S = 64
sq = lambda f, r: f * 8 + r
ORT = [(1,0),(-1,0),(0,1),(0,-1)]; DIA = [(1,1),(1,-1),(-1,1),(-1,-1)]
def rays(s, dirs):
    out = []
    for a, b in dirs:
        f, r = s // 8 + a, s % 8 + b; ray = []
        while 0 <= f < 8 and 0 <= r < 8: ray.append(f * 8 + r); f += a; r += b
        out.append(ray)
    return out
KN = [[(s//8+a)*8+(s%8+b) for a,b in [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)] if 0<=s//8+a<8 and 0<=s%8+b<8] for s in range(64)]
I = np.arange(64)
# grilă 3D pentru „celelalte trei piese” (x,y,z)
X = I[:,None,None]; Y = I[None,:,None]; Z = I[None,None,:]
occ3 = [((X==s)|(Y==s)|(Z==s)) for s in range(64)]   # ocupat de una din cele trei
q4 = I[:,None,None,None]; r4 = I[None,:,None,None]; n4 = I[None,None,:,None]; b4 = I[None,None,None,:]
valid = (q4!=r4)&(q4!=n4)&(q4!=b4)&(r4!=n4)&(r4!=b4)&(n4!=b4)
t0 = time.time()
# atacul nebunului asupra unei piese albe: A[q,r,n,b]
A = np.zeros((S,S,S,S), bool)
for b in range(64):
    for ray in rays(b, DIA):
        clear = np.ones((S,S,S), bool)
        for s in ray:
            A[:,:,:,b] |= clear & occ3[s]
            clear &= ~occ3[s]
A &= valid
# W1: albul atacă nebunul
W = np.zeros((S,S,S,S), bool)
for b in range(64):
    # dama (axa 0), blocată de r,n ; turnul (axa1) blocat de q,n ; calul
    for ray in rays(b, ORT + DIA):
        clear = np.ones((S,S), bool)   # peste (r,n)
        for s in ray:
            W[s,:,:,b] |= clear
            clear &= ~((I[:,None]==s)|(I[None,:]==s))
    for ray in rays(b, ORT):
        clear = np.ones((S,S), bool)   # peste (q,n)
        for s in ray:
            W[:,s,:,b] |= clear
            clear &= ~((I[:,None]==s)|(I[None,:]==s))
    for s in KN[b]: W[:,:,s,b] = True
W &= valid
V = np.zeros((S,S,S,S), np.uint8); V[W] = 1
print('W1', W.sum(), time.time()-t0, flush=True)
k = 1
while True:
    # Lost (negrul la mutare, pierde în <=k): fără captură și toate mutările nebunului duc în W
    allW = np.ones((S,S,S,S), bool)
    for b in range(64):
        for ray in rays(b, DIA):
            clear = np.ones((S,S,S), bool)
            for s in ray:
                clear &= ~occ3[s]
                allW[:,:,:,b] &= ~clear | W[:,:,:,s]
    Lost = allW & ~A & valid
    # Nou: albul mută într-o stare Lost
    N = np.zeros((S,S,S,S), bool)
    for q in range(64):
        for ray in rays(q, ORT + DIA):
            clear = np.ones((S,S,S), bool)
            for s in ray:
                clear &= ~occ3[s]          # (r,n,b) ocupă s
                N[q] |= clear & Lost[s]
    for r in range(64):
        for ray in rays(r, ORT):
            clear = np.ones((S,S,S), bool)
            for s in ray:
                clear &= ~occ3[s]          # (q,n,b)
                N[:,r] |= clear & Lost[:,s]
    for n in range(64):
        for s in KN[n]:
            N[:,:,n] |= Lost[:,:,s]      # Lost e fals unde s e ocupat
    N &= valid & ~W
    c = N.sum(); print('k', k+1, c, time.time()-t0, flush=True)
    if c == 0: break
    k += 1; V[N] = k; W |= N
start = (sq(3,0), sq(4,0), sq(6,0), sq(2,7))
print('start', V[start])
np.save(r'C:/Users/irina/AppData/Local/Temp/claude/5f5cca6ec2cb1060/57a79c16-0421-4278-82d3-fb32d3123bed/scratchpad/V.npy', V)
print('hist', np.bincount(V[valid]))
