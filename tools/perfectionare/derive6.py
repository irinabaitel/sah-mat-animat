import json, chess, sys, re
sys.stdout.reconfigure(encoding='utf-8')
exec(open('sfmulti.py').read().split('out={}')[0])
for s in ['L6x_a','L6x_b','L6e_a','L6e_b']:
    d=json.load(open(f'sets/{s}.json',encoding='utf-8'))
    for t in d['tasks']:
        found=None
        for side in 'wb':
            b=chess.Board(t['before']['fen']+f' {side} - - 0 1')
            for m in b.legal_moves:
                b.push(m)
                if b.board_fen()==t['after']['fen']: found=(side,m)
                b.pop()
            if found: break
        if not found: print('PROBLEM',s,t['i']); continue
        side,m=found; fen=t['before']['fen']+f' {side} - - 0 1'; b=chess.Board(fen)
        r=analyse(fen); ans=r.get(m.uci()); best=max(r.values())
        alts=[u for u,v in r.items() if u!=m.uci() and ans is not None and v>=ans-30]
        t['answer']=dict(uci=m.uci(),side=side,san=b.san(m),check=b.is_check(),gives=b.gives_check(m))
        t['sf']=dict(ans=ans,best=best,alts=alts)
        print(s,t['i'],side,b.san(m),'incheck',b.is_check(),'ans',ans,'best',best,'alts',[b.san(chess.Move.from_uci(u)) for u in alts],flush=True)
    json.dump(d,open(f'sets/{s}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
send('quit')
