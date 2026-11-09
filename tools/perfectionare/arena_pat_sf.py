import json, chess, sys, subprocess, re
sys.stdout.reconfigure(encoding='utf-8')
p = subprocess.Popen(['node','node_modules/stockfish/bin/stockfish-19-lite-single.js'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
def send(c): p.stdin.write(c+'\n'); p.stdin.flush()
def wait(tok):
    L=[]
    while True:
        l=p.stdout.readline()
        if not l: break
        L.append(l.strip())
        if l.startswith(tok): return L
send('uci'); wait('uciok'); send('setoption name MultiPV value 8'); send('isready'); wait('readyok')
def analyse(fen, depth=18):
    send('ucinewgame'); send('position fen '+fen); send(f'go depth {depth}')
    res={}
    for l in wait('bestmove'):
        m=re.search(r' depth (\d+) .*multipv (\d+) score (cp|mate) (-?\d+).* pv (\S+)', l)
        if m and int(m.group(1))==depth:
            sc=int(m.group(4)); sc= sc if m.group(3)=='cp' else ((100000-sc) if sc>0 else (-100000-sc))
            res[m.group(5)]=sc
    return res
lines=json.load(open('sets/S2P6_lines.json'))
keep=['c%d'%i for i in range(1,11)]+['d%d'%i for i in range(1,11)]+['b%d'%i for i in range(1,11)]+['e%d'%i for i in range(1,11)]+['f2','f6','f8','f9']
out={}
for k in keep:
    n=k[0]; i=int(k[1:])
    t=json.load(open(f'sets/S2P6_{n}.json',encoding='utf-8'))['tasks'][i-1]
    side,line=lines[k][0]
    fen=t['before']['fen']+' '+side+' - - 0 1'
    b=chess.Board(fen); sans=[]
    for u in line: m=chess.Move.from_uci(u); sans.append(b.san(m)); b.push(m)
    final='stalemate' if b.is_stalemate() else ('mate' if b.is_checkmate() else ('insuf' if b.is_insufficient_material() else 'open'))
    # alternatives at each user ply
    alts=[]; bb=chess.Board(fen)
    for j,u in enumerate(line):
        if j%2==0:
            r=analyse(bb.fen()); exp=r.get(u); best=max(r.values())
            ok=[x for x,v in r.items() if x!=u and exp is not None and v>=exp-80 and (exp<50 and abs(v)<=30 or exp>=50 and v>=200)]
            # for avoid sets with mate scores, accept other wins
            alts.append({'ply':j,'exp':exp,'best':best,'ok':ok,'all':r})
        bb.push(chess.Move.from_uci(u))
    out[k]={'side':side,'fen':fen,'line':line,'san':sans,'final':final,'alts':alts,'txt':t['after']['texts'][1] if len(t['after']['texts'])>2 else ''}
    print(k,side,sans,final,[(a['exp'],a['best'],[chess.Board(fen).san(chess.Move.from_uci(x)) if a['ply']==0 else x for x in a['ok']]) for a in alts],flush=True)
json.dump(out,open('sets/S2P6_arena.json','w'),ensure_ascii=False,indent=0)
send('quit')
