import json, chess, sys
sys.stdout.reconfigure(encoding='utf-8')
def search(bfen, afen, maxd=4):
    res=[]
    for side in (chess.WHITE, chess.BLACK):
        b=chess.Board(bfen+(' w' if side else ' b')+' - - 0 1')
        if not b.is_valid(): continue
        def rec(b,line,d):
            if b.board_fen()==afen and line: res.append((side,list(line))); return
            if d==0: return
            for m in b.legal_moves:
                b.push(m); line.append(m.uci()); rec(b,line,d-1); line.pop(); b.pop()
        rec(b,[],maxd)
        if res: break
    return res
out={}
for n in 'bcdef':
    d=json.load(open(f'sets/S2P6_{n}.json',encoding='utf-8'))
    for t in d['tasks']:
        bf=t['before']['fen']; af=t['after']['fen']
        r=search(bf,af,2) or search(bf,af,3) or search(bf,af,4)
        r=sorted(r,key=lambda x:len(x[1]))
        short=[x for x in r if len(x[1])==len(r[0][1])] if r else []
        print(n,t['i'],[( 'w' if s else 'b', l) for s,l in short][:4])
        out[f'{n}{t["i"]}']=[('w' if s else 'b', l) for s,l in short]
json.dump(out,open('sets/S2P6_lines.json','w'),indent=0)
