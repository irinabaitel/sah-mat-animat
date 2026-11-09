# Verificare independentă (Python, minimax naiv cu adâncime limitată) a tabelei din cursa_solver.js
import json, random, subprocess, sys
from functools import lru_cache
T = {0: (2, 7), 1: (5, 7), 2: (5, 0), 3: (2, 0)}   # c8 f8 f1 c1 ca (col, rând)
def light(c, r): return (c + r) % 2 == 1
def rays(p, k):
    c0, r0 = p[k]; out = []
    for a, b in ((1,1),(1,-1),(-1,1),(-1,-1)):
        c, r = c0 + a, r0 + b
        while 0 <= c < 8 and 0 <= r < 8:
            out.append((c, r))
            if (c, r) in p: break
            c += a; r += b
    return out
def mv(side, p):
    ks = (0, 1) if side == 0 else (2, 3)
    for k in ks:
        for t in rays(p, k):
            if t in p:
                if p.index(t) == k ^ 2: yield None, True
                continue
            q = list(p); q[k] = t; q = tuple(q)
            yield q, all(q[j] == T[j] for j in ks)
@lru_cache(None)
def win(side, p, d):   # cel la mutare câștigă în cel mult d semimutări
    if d <= 0: return False
    for q, w in mv(side, p):
        if w: return True
        if d >= 3 and lose(1 - side, q, d - 1): return True
    return False
@lru_cache(None)
def lose(side, p, d):  # cel la mutare pierde în cel mult d semimutări
    if d <= 1: return False
    for q, w in mv(side, p):
        if w or not win(1 - side, q, d - 1): return False
    return True
random.seed(1); cases = []
while len(cases) < 600:
    p = [None] * 4
    for k in range(4):
        while True:
            s = (random.randrange(8), random.randrange(8))
            if light(*s) == (k % 2 == 0) and s not in p: break
        p[k] = s
    p = tuple(p)
    if all(p[j] == T[j] for j in (0, 1)) or all(p[j] == T[j] for j in (2, 3)): continue
    cases.append((random.randrange(2), p))
js = "const S=require('./cursa_solver.js')();const c=" + json.dumps([[s, [a*8+b for a, b in p]] for s, p in cases]) + ";console.log(JSON.stringify(c.map(([s,p])=>S.V[S.enc(s,p)])))"
open('_cc.js', 'w').write(js)
V = json.loads(subprocess.check_output(['node', '_cc.js']))
bad = 0; D = 9
for (s, p), v in zip(cases, V):
    for d in range(1, D + 1):
        a = win(s, p, d); b = 0 < v <= d
        c = lose(s, p, d); e = v < 0 and -v <= d
        if a != b or c != e: bad += 1; print('BAD', s, p, v, d, a, c); break
print('checked', len(cases), 'bad', bad, 'values', sorted(set(V)))
