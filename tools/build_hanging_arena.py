"""build_hanging_arena.py — alege 40 de puzzle-uri din tools/hanging_raw.json (vezi fetch_hanging.py)
-> data/hanging_arena.json pentru nivel1_arena_atarnate.html. 10 ușoare (o mutare), 20 medii, 10 avansate."""
import json, sys, os, chess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fetch_hanging as F
RO = {'N': 'C', 'B': 'N', 'R': 'T', 'Q': 'D', 'K': 'R'}
NAME = {chess.KNIGHT: ('calul', 'atârnat'), chess.BISHOP: ('nebunul', 'atârnat'), chess.ROOK: ('turnul', 'atârnat'), chess.QUEEN: ('dama', 'atârnată')}
def ro_san(s): return ''.join(RO.get(c, c) for c in s)

items = []
for p in F.raw.values():
    a = F.analyse(p)
    if not a: continue
    b = chess.Board(a['fen']); b.push_uci(a['moves'][0])
    fen = b.fen(); sol = a['moves'][1:]; t = b.copy(); san = []
    cap = t.piece_at(chess.Move.from_uci(sol[0]).to_square)
    for u in sol:
        m = chess.Move.from_uci(u); san.append(ro_san(t.san(m))); t.push(m)
    nm, adj = NAME[cap.piece_type]
    if len(sol) == 1 and t.is_checkmate():
        expl = f'Corect. {nm.capitalize()} era {adj}: l-ai capturat și ai dat mat.' if cap.piece_type != chess.QUEEN else 'Corect. Dama era atârnată: ai capturat-o și ai dat mat.'
    elif len(sol) == 1:
        expl = f'Corect. {nm.capitalize()} era {adj} și l-ai capturat.' if cap.piece_type != chess.QUEEN else 'Corect. Dama era atârnată și ai capturat-o.'
    else:
        expl = (f'Corect. Ai capturat {nm} {adj}' if cap.piece_type != chess.QUEEN else 'Corect. Ai capturat dama atârnată') + \
               (' și ai dat mat.' if t.is_checkmate() else ' și ai jucat mai departe cele mai bune mutări.')
    items.append(dict(id=a['id'], fen=fen, last=a['moves'][0], moves=sol, san=san, rating=a['rating'], plays=a['plays'],
                      expl=expl, mate=t.is_checkmate()))

used = set()
def pick(cond, n, key):
    c = sorted([x for x in items if cond(x) and x['id'] not in used], key=key)[:n]
    for x in c: used.add(x['id'])
    return c
easy = pick(lambda x: len(x['moves']) == 1 and x['plays'] >= 500, 10, lambda x: x['rating'])
med  = pick(lambda x: len(x['moves']) <= 3 and 850 <= x['rating'] < 1300 and x['plays'] >= 500, 20, lambda x: -x['plays'])
adv  = pick(lambda x: len(x['moves']) == 3 and 1300 <= x['rating'] < 1700 and x['plays'] >= 500, 10, lambda x: -x['plays'])
med.sort(key=lambda x: x['rating']); adv.sort(key=lambda x: x['rating'])
out = []
for lvl, grp in ((0, easy), (1, med), (2, adv)):
    for x in grp:
        out.append(dict(id=x['id'], fen=x['fen'], last=x['last'], moves=x['moves'], san=x['san'], level=lvl, expl=x['expl']))
    print(lvl, len(grp), [x['rating'] for x in grp])
json.dump(out, open(os.path.join(HERE, '..', 'data', 'hanging_arena.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('total', len(out))
