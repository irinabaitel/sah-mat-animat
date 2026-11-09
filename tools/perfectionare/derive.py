import json, chess, sys
sys.stdout.reconfigure(encoding='utf-8')
def grid(f):
    g={}
    for ri,row in enumerate(f.split('/')):
        fi=0
        for c in row:
            if c.isdigit(): fi+=int(c)
            else: g[chess.square(fi,7-ri)]=c; fi+=1
    return g
for s in ['3a','L5x_a','L5x_b','L5x_c','L5x_d','L5x_e','L5e_a','L5e_b','L5e_c']:
    d=json.load(open(f'sets/{s}.json'))
    for t in d['tasks']:
        a,b=grid(t['before']['fen']),grid(t['after']['fen'])
        frm=[q for q in a if b.get(q)!=a[q] and b.get(q) is None or (q in b and b[q]!=a[q] and False)]
        frm=[q for q in a if q not in b]
        to=[q for q in b if a.get(q)!=b[q]]
        t.pop('answer',None)
        if len(frm)==1 and len(to)==1:
            p=a[frm[0]]; side='w' if p.isupper() else 'b'
            bd=chess.Board(None)
            for q,c in a.items(): bd.set_piece_at(q,chess.Piece.from_symbol(c))
            bd.turn = side=='w'
            mv=chess.Move(frm[0],to[0])
            if mv in bd.pseudo_legal_moves:
                t['answer']=dict(uci=mv.uci(), side=side, san=bd.san(mv)); continue
        print('PROBLEM', s, t['i'], [chess.square_name(q) for q in frm], [chess.square_name(q) for q in to])
    json.dump(d,open(f'sets/{s}.json','w'),ensure_ascii=False,indent=1)
print('ok')
