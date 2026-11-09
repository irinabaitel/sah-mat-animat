import json, chess, sys
sys.stdout.reconfigure(encoding='utf-8')
def safe_after(b, m):
    b2=b.copy(); b2.push(m)
    return not any(mm.to_square==m.to_square for mm in b2.legal_moves)
def checks(fen):
    b=chess.Board(fen); out=[]
    for m in b.legal_moves:
        if b.gives_check(m):
            out.append((b.san(m), m.uci(), safe_after(b,m), b.is_capture(m)))
    return out
if __name__=='__main__':
    d=json.load(open('sets/L6x_a.json',encoding='utf-8'))
    for t in d['tasks']:
        a=t['answer']; fen=t['before']['fen']+' '+a['side']+' - - 0 1'
        print(t['i'], a['san'], [c for c in checks(fen)])
