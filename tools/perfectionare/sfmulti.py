import subprocess, json, chess, sys, re
sys.stdout.reconfigure(encoding='utf-8')
p = subprocess.Popen(['node','node_modules/stockfish/bin/stockfish-19-lite-single.js'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
def send(c): p.stdin.write(c+'\n'); p.stdin.flush()
def wait(tok):
    lines=[]
    while True:
        l=p.stdout.readline()
        if not l: break
        lines.append(l.strip())
        if l.startswith(tok): return lines
send('uci'); wait('uciok'); send('setoption name MultiPV value 6'); send('isready'); wait('readyok')
def analyse(fen, depth=16):
    send('position fen '+fen); send(f'go depth {depth}')
    lines=wait('bestmove'); res={}
    for l in lines:
        m=re.search(r' depth (\d+) .*multipv (\d+) score (cp|mate) (-?\d+).* pv (\S+)', l)
        if m and int(m.group(1))==depth:
            sc=int(m.group(4)); sc= sc if m.group(3)=='cp' else (100000 if sc>0 else -100000)
            res[m.group(5)]=sc
    return res
out={}
for s in ['L5x_b','L5x_c','L5x_d','L5x_e','L5e_a','L5e_b','L5e_c']:
    d=json.load(open(f'sets/{s}.json'))
    for t in d['tasks']:
        a=t['answer']; fen=t['before']['fen']+' '+a['side']+' - - 0 1'
        r=analyse(fen); best=max(r.values()); ans=r.get(a['uci'])
        b=chess.Board(fen)
        alts=[(b.san(chess.Move.from_uci(u)),v) for u,v in sorted(r.items(),key=lambda x:-x[1]) if u!=a['uci'] and v>=best-60 and v>=(ans if ans is not None else best)-60]
        t['sf']=dict(best=best, answer=ans, alts=alts)
        print(s,t['i'],a['san'],'ans',ans,'best',best,'alts',alts, flush=True)
    json.dump(d,open(f'sets/{s}.json','w'),ensure_ascii=False,indent=1)
send('quit')
