# Builds data/nivel1_lectia7_ex.js — lecția „Matul”
# Surse: Chess Tutor Step 1 lecțiile 7–8 (sets/L7*, L8*), caietul Steps pasul 1 (wb/mate_*.json), ChessKid lecția 3.
import json, sys, os, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia7_ex.js'
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
ACC = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
PRON = {chess.QUEEN: 'o'}  # „o apără” pentru regină, „îl apără” pentru rest
RO_LET = {'K': 'R', 'Q': 'D', 'R': 'T', 'B': 'N', 'N': 'C'}
LET = {'K': chess.KING, 'Q': chess.QUEEN, 'R': chess.ROOK, 'B': chess.BISHOP, 'N': chess.KNIGHT, 'P': chess.PAWN}
CAP = lambda s: s[0].upper() + s[1:]
def ro_san(san): return ''.join(RO_LET.get(c, c) if c.isupper() else c for c in san)
def sqn(s): return chess.square_name(s)
def load(n): return json.load(open(os.path.join(HERE, 'sets', n + '.json'), encoding='utf-8'))
ERR = []

# ── mat fără să ceară ambii regi pe tablă ──
def board(fen, side):
    b = chess.Board(None); b.set_board_fen(fen.split(' ')[0]); b.turn = side == 'w'; return b
def own_king_safe(b):  # după push: partea care a mutat nu are regele în șah
    k = b.king(not b.turn)
    return k is None or not b.is_attacked_by(b.turn, k)
def moves(b):
    for m in b.pseudo_legal_moves:
        if b.is_castling(m): continue
        t = b.piece_at(m.to_square)
        if t and t.piece_type == chess.KING: continue
        bb = b.copy(stack=False); bb.push(m)
        if own_king_safe(bb): yield m
def mated(b):
    k = b.king(b.turn)
    if k is None or not b.is_attacked_by(not b.turn, k): return False
    return not any(True for _ in moves(b))
def mates(b):
    out = []
    for m in moves(b):
        bb = b.copy(stack=False); bb.push(m)
        if mated(bb): out.append(m)
    return out
def kings_ok(b):
    k1, k2 = b.king(chess.WHITE), b.king(chess.BLACK)
    return k1 is None or k2 is None or chess.square_distance(k1, k2) > 1

def expl_mate(b, m):
    p = b.piece_at(m.from_square); to = m.to_square
    pt = m.promotion or p.piece_type
    bb = b.copy(stack=False); bb.push(m)
    s = CAP(NAME[pt]) + (' nou' if m.promotion else '') + ' dă mat pe ' + sqn(to) + '.'
    if m.promotion: s = f'Pionul se transformă în {dict([(chess.QUEEN, "regină"), (chess.ROOK, "turn"), (chess.BISHOP, "nebun"), (chess.KNIGHT, "cal")])[pt]} și dă mat pe {sqn(to)}.'
    if b.piece_at(to): s = s[:-1] + f' și capturează {NAME[b.piece_at(to).piece_type]}.'
    k = bb.king(bb.turn)
    if k is not None and chess.square_distance(k, to) == 1:
        sup = [q for q in bb.attackers(not bb.turn, to)]
        if sup:
            q = sup[0]; pr = PRON.get(pt, 'îl')
            s += f' {CAP(NAME[bb.piece_at(q).piece_type])} de pe {sqn(q)} {pr} apără.'
    return s

def mate_task(fen, side, answer=None, src=''):
    b = board(fen, side); ms = mates(b)
    if not ms: ERR.append(('nomate', src, fen, side)); return None
    ucis = [m.uci() for m in ms]
    if answer and answer not in ucis:
        ERR.append(('answer-not-mate', src, fen, answer, ucis)); answer = None
    if not answer:
        if len(ms) > 1: ERR.append(('ambiguous', src, fen, ucis))
        answer = ucis[0]
    m = chess.Move.from_uci(answer)
    return dict(type='move', fen=fen.split(' ')[0] + f' {side} - - 0 1', side=side, answer=answer,
                san=ro_san(b.san(m)) + ('' if b.san(m).endswith('#') else '#'), ok=[u for u in ucis if u != answer], check='mate',
                expl=expl_mate(b, m))

def add_task(fen, side, pieces, solution, cross=None, src='', prompt=None, expl=None):
    """pieces: listă ca ['wQ']; solution: {sq: 'wQ'}; side = culoarea care dă mat"""
    b = board(fen, side)
    for s, p in solution.items():
        assert b.piece_at(chess.parse_square(s)) is None, (src, fen, s)
        b.set_piece_at(chess.parse_square(s), chess.Piece(LET[p[1]], p[0] == 'w'))
    b.turn = side != 'w'
    if not (mated(b) and kings_ok(b)): ERR.append(('add-not-mate', src, fen, solution))
    # toate pătratele bune (pentru o singură piesă)
    good = []
    if len(pieces) == 1 and not cross:
        p = pieces[0]
        for s in chess.SQUARES:
            bb = board(fen, side)
            if bb.piece_at(s): continue
            if LET[p[1]] == chess.PAWN and chess.square_rank(s) in (0, 7): continue
            bb.set_piece_at(s, chess.Piece(LET[p[1]], p[0] == 'w')); bb.turn = side != 'w'
            if mated(bb) and kings_ok(bb): good.append(sqn(s))
        missing = [s for s in solution if s not in good]
        if missing: ERR.append(('add-missing', src, fen, solution, good))
    defender = 'b' if side == 'w' else 'w'
    if expl is None and len(pieces) == 1:
        s0, p0 = next(iter(solution.items())); sq0 = chess.parse_square(s0); pt = LET[p0[1]]
        nm = NAME[pt]; k = b.king(b.turn)
        if p0[0] != side:
            expl = f'{CAP(nm)} de pe {s0} îi închide regelui ultimul pătrat liber. Propria piesă îl încurcă.'
        elif k is not None and b.is_attacked_by(not b.turn, k) and sq0 in b.attackers(not b.turn, k):
            expl = f'{CAP(nm)} de pe {s0} dă mat.'
            if chess.square_distance(k, sq0) == 1:
                sup = list(b.attackers(not b.turn, sq0))
                if sup: expl += f' {CAP(NAME[b.piece_at(sup[0]).piece_type])} de pe {sqn(sup[0])} {PRON.get(pt, "îl")} apără.'
        else:
            expl = f'{CAP(nm)} de pe {s0} păzește pătratele pe unde ar fi putut pleca regele.'
        others = [q for q in good if q != s0]
        if others: expl += ' Merge și pe ' + ', '.join(others) + '.'
    if expl is None:
        s0, p0 = next(iter(solution.items()))
        expl = ('Pe ' + ' sau pe '.join(good) if len(good) > 1 else 'Pe ' + s0) + ': ' + ('albul' if defender == 'w' else 'negrul') + ' primește mat.' if len(pieces) == 1 \
            else 'Piesele stau pe pătratele potrivite: ' + ('albul' if defender == 'w' else 'negrul') + ' primește mat.'
    return dict(type='addmate', fen=fen.split(' ')[0], side=side, defender=defender, pieces=pieces, solution=solution,
                good=good, cross=cross, prompt=prompt, expl=expl)

def mk_set(id, title, src, intro, tasks, instr=None):
    tasks = [t for t in tasks if t]
    return dict(id=id, title=title, src=src, intro=intro, instr=instr, tasks=tasks)
PNAME = {'Q': 'regina', 'R': 'turnul', 'B': 'nebunul', 'N': 'calul', 'P': 'pionul', 'K': 'regele'}
def add_prompt(p):
    c = 'albă' if p[0] == 'w' else 'neagră'
    n = {'Q': 'o regină', 'R': 'un turn', 'B': 'un nebun', 'N': 'un cal', 'P': 'un pion', 'K': 'regele'}[p[1]]
    if p[1] == 'K': return f'Pune regele {"alb" if p[0] == "w" else "negru"} pe tablă, așa încât să fie mat.'
    if p[1] in 'Q': return f'Pune {n} {c} pe tablă, așa încât să fie mat.'
    return f'Pune {n} {"alb" if p[0] == "w" else "negru"} pe tablă, așa încât să fie mat.'

# ═════════ diff de poziții din Chess Tutor ═════════
def fpos(fen):
    b = chess.Board(None); b.set_board_fen(fen); return {sqn(s): p.symbol() for s, p in b.piece_map().items()}
def ct_move(t):
    a, z = fpos(t['before']['fen']), fpos(t['after']['fen'])
    gone = [s for s in a if s not in z or z[s] != a[s]]
    new = [s for s in z if a.get(s) != z[s]]
    if len(gone) == 1 and len(new) == 1:
        f, to = gone[0], new[0]; side = 'w' if a[f].isupper() else 'b'
        promo = z[to].lower() if a[f].lower() == 'p' and z[to].lower() != 'p' else ''
        return side, f + to + promo
    return None, None
def ct_added(t):
    a, z = fpos(t['before']['fen']), fpos(t['after']['fen'])
    assert all(z.get(s) == p for s, p in a.items()), t['i']
    return {s: ('w' if p.isupper() else 'b') + p.upper() for s, p in z.items() if s not in a}

def ct_mate_set(sid, id, title, src, intro):
    d = load(sid); tasks = []
    for t in d['tasks']:
        side, u = ct_move(t)
        txt = ' '.join(t['after']['texts'])
        if not side:
            side = 'b' if 'White is checkmated' in txt else 'w'
            if 'checkmated' not in txt and 'mated' not in txt:
                bw, bb_ = mates(board(t['before']['fen'], 'w')), mates(board(t['before']['fen'], 'b'))
                side = 'w' if bw and not bb_ else 'b' if bb_ and not bw else side
        tasks.append(mate_task(t['before']['fen'], side, u, f'{sid}#{t["i"]}'))
    return mk_set(id, title, src, intro, tasks, 'Dă mat într-o mutare.')

def ct_add_set(sid, id, title, src, intro):
    d = load(sid); tasks = []
    for t in d['tasks']:
        add = ct_added(t); fen = t['before']['fen']
        if len(add) == 2 and any(p[1] == 'K' for p in add.values()):  # programul arată și regele la răspuns
            ks = [s for s, p in add.items() if p[1] == 'K'][0]
            b0 = chess.Board(None); b0.set_board_fen(fen); b0.set_piece_at(chess.parse_square(ks), chess.Piece(chess.KING, add[ks][0] == 'w'))
            fen = b0.board_fen(); del add[ks]
        if len(add) != 1: ERR.append(('add-count', sid, t['i'], add)); continue
        (s, p), = add.items()
        txt = ' '.join(t['after']['texts'])
        mating = 'b' if 'White is' in txt else 'w' if 'Black is' in txt else p[0]
        pr = add_prompt(p) if p[0] == mating else add_prompt(p).replace('așa încât să fie mat', 'așa încât să-i închidă regelui ultimul pătrat liber și să fie mat')
        tasks.append(add_task(fen, mating, [p], add, src=f'{sid}#{t["i"]}', prompt=pr))
    return mk_set(id, title, src, intro, tasks)

def ct_cross_set(sid, id, title, src, intro):
    d = load(sid); tasks = []
    ORDER = 'KQRBNP'
    for t in d['tasks']:
        z = fpos(t['after']['fen'])
        sol = {s: ('w' if p.isupper() else 'b') + p.upper() for s, p in z.items()}
        pcs = sorted(sol.values(), key=lambda p: (p[0] == 'b', ORDER.index(p[1])))
        tasks.append(add_task('8/8/8/8/8/8/8/8', 'w', pcs, sol, cross=sorted(sol), src=f'{sid}#{t["i"]}',
                              prompt='Pune piesele pe pătratele marcate, așa încât negrul să primească mat.'))
    return mk_set(id, title, src, intro, tasks)

CT7 = 'Chess Tutor Step 1 · lecția 7'; CT8 = 'Chess Tutor Step 1 · lecția 8'
CT7X = 'Chess Tutor Step 1 · lecția 7 (extra)'; CT8X = 'Chess Tutor Step 1 · lecția 8 (extra)'
I_MATE = 'Dă mat într-o singură mutare. Înainte să muți, uită-te pe unde ar mai putea pleca regele.'
I_ADD = 'Pune piesa pe tablă, pe pătratul potrivit, așa încât să fie mat.'
baza, mediu, av = [], [], []

# ═════════ MEDIU: Chess Tutor ═════════
mediu.append(ct_add_set('L7e_a', '7a', 'Adaugă piesa (1)', CT7, I_ADD + ' Piesa care dă mat este apărată de altă piesă.'))
mediu.append(ct_mate_set('L7e_b', '7b', 'Mat într-o mutare (1)', CT7, I_MATE))
mediu.append(ct_mate_set('L7e_c', '7c', 'Mat într-o mutare (2)', CT7, I_MATE + ' Aici și piesele adversarului se pot apăra.'))
mediu.append(ct_add_set('L7e_d', '7d', 'Adaugă piesa (2)', CT7, I_ADD))
mediu.append(ct_mate_set('L8e_a', '8a', 'Paznicul și vânătorul', CT8, 'Piesele lucrează împreună: una păzește pătratele pe unde ar pleca regele, alta îi dă șah. Dă mat într-o mutare.'))
mediu.append(ct_add_set('L8e_b', '8b', 'Adaugă piesa (3)', CT8, I_ADD + ' Aici piesa adăugată poate fi paznic sau vânător.'))
mediu.append(ct_mate_set('L8e_c', '8c', 'Mat într-o mutare (3)', CT8, I_MATE))
mediu.append(ct_cross_set('L8e_d', '8d', 'Pune piesele pe cruci', CT8, 'Ai câteva piese, iar pe tablă sunt marcate pătratele lor. Pune piesele pe pătratele marcate, așa încât negrul să primească mat. Fiecare piesă merge pe un singur pătrat.'))

# ═════════ AVANSAT: Chess Tutor extra ═════════
av.append(ct_mate_set('L7x_a', 'L7x_a', 'Mat într-o mutare (extra 1)', CT7X, I_MATE))
av.append(ct_mate_set('L7x_b', 'L7x_b', 'Mat în partide adevărate', CT7X, 'Pozițiile acestea sunt din partide. Pe tablă sunt multe piese: caută cu răbdare mutarea care dă mat.'))
av.append(ct_mate_set('L8x_a', 'L8x_a', 'Mat într-o mutare (extra 2)', CT8X, I_MATE))
av.append(ct_add_set('L8x_b', 'L8x_b', 'Adaugă piesa (extra)', CT8X, 'Aici regele nu mai are niciun pătrat liber după ce pui piesa. Uneori piesa adăugată e a celui care primește mat: ea îi închide regelui drumul.'))

# ═════════ DE BAZĂ: ChessKid + caietul Steps ═════════
CK = 'ChessKid · lecția 3'
CKQ = [  # (fen, mat?, explicație)
  ('5k2/4PP2/5K2/8/8/8/1p6/8', True, 'Da, este mat. Pionul de pe e7 dă șah. Regele nu poate captura pionii, pentru că îi apără regele alb, iar pe g8 și e8 îl atacă pionul de pe f7.'),
  ('1r3r1k/2bbN1p1/2p2p2/pp1p3Q/q2P1PP1/2P3K1/PP1B4/8', True, 'Da, este mat. Regina dă șah pe coloana h, iar calul de pe e7 ține pătratul g8. Nicio piesă nu se poate pune în cale.'),
  ('r1bqk2r/pppp1Qpp/2n4n/2b1p3/2B1P3/5N2/PPPP1PPP/RNB1K2R', False, 'Nu este mat: calul de pe h6 capturează regina de pe f7.'),
  ('R4k2/8/4K3/8/8/8/8/8', False, 'Nu este mat: regele pleacă pe g7.'),
  ('rq1b2rk/2p2Npp/3p1n2/4p3/pp1PP3/2P4P/PP3PP1/2BRR1K1', True, 'Da, este mat. Calul dă șah, iar regele e închis de propriile piese. Acesta se numește „mat sufocat”.'),
  ('3q1r1k/r6Q/bpnbpp2/p1pp4/3P1P2/2P1PR2/PPBB2PP/R5K1', False, 'Nu este mat: turnul de pe a7 capturează regina de pe h7.'),
  ('r1bqk1nr/pppp1ppp/2n5/b7/2B5/B1p2N2/P4PPP/RN1QR1K1', False, 'Nu este mat: negrul poate pune o piesă în cale, pe e7.'),
  ('7k/5Q2/8/8/2K5/8/1N6/8', False, 'Nu este mat, pentru că regele negru nu este nici măcar în șah. Totuși nu are nicio mutare: aceasta se numește <strong>pat</strong>. Despre pat vei învăța într-o lecție viitoare.'),
]
tasks = []
for f, ans, e in CKQ:
    b = board(f, 'b'); assert mated(b) == ans, f
    tasks.append(dict(type='mateq', fen=f + ' b - - 0 1', answer=ans, expl=e, prompt='Regele negru este mat?'))
baza.append(mk_set('ck_mateq', 'Este mat?', CK, 'Uită-te bine: regele negru poate pleca, poate captura piesa care dă șah sau se poate pune o piesă în cale? Dacă nu poate nimic din acestea, este mat.', tasks))

WB = os.path.join(HERE, 'wb', 'mate_sheets.json')
w = json.load(open(WB, encoding='utf-8'))
WBSRC = 'Steps · caietul pasului 1'
SHEETS = [  # cheie, id, titlu, intro
  ('w26', 'wb_m1A', 'Mat într-o mutare A', 'Dă mat într-o mutare. Piesa care dă mat trebuie să fie apărată.'),
  ('w27', 'wb_addA', 'Adaugă piesa A', 'Pune piesa pe tablă, așa încât să fie mat.'),
  ('w28', 'wb_addB', 'Adaugă piesa B', 'Pune piesa pe tablă, așa încât să fie mat. Piesa poate da șah și, în același timp, păzi pătratele pe unde ar pleca regele.'),
  ('w29', 'wb_m1B', 'Mat într-o mutare B', 'Dă mat într-o mutare. Paznicul și vânătorul lucrează împreună.'),
  ('w30', 'wb_m1C', 'Mat într-o mutare C', 'Dă mat într-o mutare. Uneori propriile piese îi închid regelui drumul.'),
  ('w31', 'wb_addC', 'Adaugă piesa C', 'Pune piesa pe tablă, așa încât să fie mat.'),
  ('w32', 'wb_addD', 'Adaugă paznicul D', 'Regele este deja în șah. Pune piesa pe un pătrat de unde păzește pătratele pe unde ar pleca regele.'),
  ('w33', 'wb_m1D', 'Mat într-o mutare D', 'Dă mat într-o mutare.'),
  ('w34', 'wb_m1E', 'Mat într-o mutare E', 'Dă mat într-o mutare. Pe tablă sunt mai multe piese.'),
  ('w35', 'wb_m1F', 'Mat într-o mutare F', 'Dă mat într-o mutare.'),
  ('w36', 'wb_m1G', 'Mat într-o mutare G', 'Dă mat într-o mutare. Atenție la capcane: nu orice șah este mat.'),
  ('w37', 'wb_m1H', 'Mat într-o mutare H', 'Dă mat într-o mutare. Atenție la capcane: nu orice șah este mat.'),
]
for key, id, title, intro in SHEETS:
    tasks = []
    for x in w[key]:
        src = f'{key}#{x["n"]}'
        if x['kind'] == 'move':
            t = mate_task(x['fen'], x['side'], x['answers'][0], src)
            if t:
                extra = [u for u in x['answers'][1:] if u not in t['ok'] and u != t['answer']]
                assert not extra, (src, extra)
            tasks.append(t)
        else:
            a0 = x['answers'][0]; pl = a0[0] if a0[0] in 'KQRBN' else 'P'; sq = a0[-2:]
            p = x['side'] + pl
            t = add_task(x['fen'], x['side'], [p], {sq: p}, src=src, prompt=add_prompt(p))
            want = sorted(a[-2:] for a in x['answers'])
            if len(want) > 1 and sorted(t['good']) != want and not set(want) <= set(t['good']): ERR.append(('wb-add-answers', src, want, t['good']))
            tasks.append(t)
    baza.append(mk_set(id, title, WBSRC, intro, tasks, 'Dă mat într-o mutare.' if w[key][0]['kind'] == 'move' else None))

DATA = dict(tabs=[dict(id='baza', title='De bază', sets=baza), dict(id='mediu', title='Mediu', sets=mediu), dict(id='avansat', title='Avansat', sets=av)])
js = json.dumps(DATA, ensure_ascii=False)
open(OUT, 'w', encoding='utf-8').write('/* Exercițiile lecției „Matul”.\n   Surse: Chess Tutor Step 1 (metoda Steps, lecțiile 7–8), caietul Steps pasul 1, ChessKid (lecția 3).\n   Generat automat — nu edita de mână. */\nwindow.L7EX = ' + js + ';\n')
tot = 0
for t in DATA['tabs']:
    print(t['title'], [(s['id'], len(s['tasks'])) for s in t['sets']]); tot += sum(len(s['tasks']) for s in t['sets'])
print('total', tot)
for e in ERR: print('ERR', e)
