# Builds data/nivel1_lectia3_ex.js — lecția „Mutări speciale” (rocada, promovarea, en passant)
# Surse: caietul Steps pasul 1 „Castling: A”; ChessKid L5 (Castling Quiz, Can You Capture En Passant?) și L14 („To Under or Promote?”);
#        Chess Tutor Step 1 lecția 9 (9a, 9b, 9c) și lecția 14 (14a „Mate in one (ep)”).
import json, os, sys, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia3_ex.js'
HERE = os.path.dirname(os.path.abspath(__file__))
RO_LET = {'K': 'R', 'Q': 'D', 'R': 'T', 'B': 'N', 'N': 'C'}
def ro_san(san): return ''.join(RO_LET.get(c, c) if c.isupper() else c for c in san).replace('O-O', '0-0')
def sqn(s): return chess.square_name(s)
NAME = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
NAMEDE = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
COL = {'w': 'albul', 'b': 'negrul'}; COLC = {'w': 'Albul', 'b': 'Negrul'}
ERR = []
def load(n): return json.load(open(os.path.join(HERE, 'sets', n + '.json'), encoding='utf-8'))
def mk_set(id, title, src, intro, tasks, instr=None):
    return dict(id=id, title=title, src=src, intro=intro, instr=instr, tasks=[t for t in tasks if t])

# ── rocada: drepturi deduse din poziție (rege și turn pe pătratele de start) ──
HOME = {('w', 'K'): ('e1', 'h1', 'g1', 'f1', ['f1', 'g1']), ('w', 'Q'): ('e1', 'a1', 'c1', 'd1', ['b1', 'c1', 'd1']),
        ('b', 'K'): ('e8', 'h8', 'g8', 'f8', ['f8', 'g8']), ('b', 'Q'): ('e8', 'a8', 'c8', 'd8', ['b8', 'c8', 'd8'])}
LBL = {('w', 'K'): 'Albul 0-0', ('w', 'Q'): 'Albul 0-0-0', ('b', 'K'): 'Negrul 0-0', ('b', 'Q'): 'Negrul 0-0-0'}
def piece(b, s): return b.piece_at(chess.parse_square(s))
def why_not(b, c, side, moved=None):
    """motivele pentru care culoarea c nu poate face rocada spre side ('K'/'Q'); [] = poate"""
    ks, rs, kto, rto, between = HOME[(c, side)]
    col = chess.WHITE if c == 'w' else chess.BLACK
    k, r = piece(b, ks), piece(b, rs)
    out = []
    if not (k and k.piece_type == chess.KING and k.color == col): out.append(('moved', 'Regele a mutat deja.'))
    elif not (r and r.piece_type == chess.ROOK and r.color == col): out.append(('moved', 'Turnul a mutat deja.'))
    elif moved: out.append(('moved', moved))
    if out: return out
    blk = [s for s in between if piece(b, s)]
    if blk: out.append(('between', f'Între rege și turn stă {NAME[piece(b, blk[0]).piece_type]} de pe {blk[0]}.'))
    att = lambda s: b.is_attacked_by(not col, chess.parse_square(s))
    def who(s):
        a = list(b.attackers(not col, chess.parse_square(s)))
        return f' ({NAME[b.piece_at(a[0]).piece_type]} de pe {sqn(a[0])})' if a else ''
    if att(ks): out.append(('check', 'Regele este în șah' + who(ks) + '.'))
    if att(rto): out.append(('cross', f'Regele ar trece prin {rto}, care este atacat' + who(rto) + '.'))
    if att(kto): out.append(('land', f'Regele ar ajunge în șah pe {kto}' + who(kto) + '.'))
    return out
def allowed(b, c, side): return not why_not(b, c, side)
def can_text(b, c, side):
    w = why_not(b, c, side)
    nm = 'rocada mică' if side == 'K' else 'rocada mare'
    if not w:
        extra = ''
        _, rs, *_ = HOME[(c, side)]
        col = chess.WHITE if c == 'w' else chess.BLACK
        if b.is_attacked_by(not col, chess.parse_square(rs)): extra = ' Nu contează că turnul este atacat.'
        if side == 'Q' and b.is_attacked_by(not col, chess.parse_square('b1' if c == 'w' else 'b8')): extra += ' Nu contează nici că b' + ('1' if c == 'w' else '8') + ' este atacat: pe acolo trece doar turnul.'
        return f'{COLC[c]} poate face {nm}.{extra}'
    return f'{COLC[c]} nu poate face {nm}. ' + ' '.join(x[1] for x in w)
def full(fen, side): return fen + ' ' + side + ' - - 0 1'

# ── 1. Caietul: Castling A (citit de pe foaie, verificat cu răspunsurile din Manual) ──
WB = [  # fen, partea la mutare, culoarea întrebată, latura, răspuns Manual
 ('r4rk1/pp3ppp/5n2/8/8/4BP2/PPP3PP/R2K3R', 'w', 'w', 'K', False),
 ('1r2kB1r/pp3ppp/2n5/8/8/8/PP3PPP/R4RK1', 'b', 'b', 'K', False),
 ('5rk1/1pp2ppp/8/4P3/1bP5/5N2/1P4PP/4K2R', 'w', 'w', 'K', False),
 ('2r1k2r/1R4pp/5n2/8/8/1B6/P5PP/5RK1', 'b', 'b', 'K', False),
 ('5rk1/5ppp/2q1p3/8/8/6P1/1P3P1P/3QK2R', 'w', 'w', 'K', True),
 ('r4rk1/1pp3pp/p7/8/8/2N2bP1/PPP4P/R3K1R1', 'w', 'w', 'Q', False),
 ('4k2r/1p3p1p/6p1/5b2/8/2B4P/1P3PP1/3R2K1', 'b', 'b', 'K', True),
 ('r1b2rk1/pp1nbppp/1qpp1n2/8/2B1PP2/2N2N2/PPP3PP/R1BQK2R', 'w', 'w', 'K', False),
 ('r3k2r/pppq1ppp/2npb3/4p3/2B1Pn1B/2NP1N2/PPP2PPP/R2Q1RK1', 'b', 'b', 'Q', False),
 ('r3r1k1/ppq2ppp/2nb4/2p4R/4p3/1BN1P1P1/PPPBQP2/R3K3', 'w', 'w', 'Q', True),
 ('r3kb1r/pp1q1ppp/1np1bn2/8/3P4/2N2NB1/PP2BPPP/R2Q1RK1', 'b', 'b', 'Q', True),
 ('r4rk1/pppn1ppp/3p1n2/3P4/1bP1q3/1N2BN2/PP2QPPP/R3K2R', 'w', 'w', 'Q', False),
]
def castle_q(fen, side, c, sd, ans, src, prompt=None):
    b = chess.Board(full(fen, side))
    got = allowed(b, c, sd)
    if got != ans: ERR.append(('castle_q', src, fen, got, ans, why_not(b, c, sd))); return None
    nm = 'rocada mică' if sd == 'K' else 'rocada mare'
    hl = HOME[(c, sd)]
    return dict(type='choice', fen=full(fen, side), side=side, src=src, opts=['Da', 'Nu'], answer=['Da' if ans else 'Nu'],
                prompt=prompt or f'Poate {COL[c]} să facă {nm}?', focus=[hl[0], hl[1]],
                expl=can_text(b, c, sd), why={'Da': 'Mai uită-te: ' + (why_not(b, c, sd)[0][1] if not ans else ''), 'Nu': 'Mai uită-te: nu este niciun motiv care să oprească rocada.'})
baza = []
baza.append(mk_set('wbR', 'Caietul: rocada', 'Caietul metodei Steps, pasul 1, foaia „Rocada: A”',
    'Poate jucătorul să facă rocada? Verifică pe rând: regele și turnul n-au mutat? E liber între ele? Regele nu e în șah, nu trece și nu ajunge pe un pătrat atacat?',
    [castle_q(f, s, c, sd, a, f'wbCastA#{i + 1}') for i, (f, s, c, sd, a) in enumerate(WB)]))

# ── 2. ChessKid L5: Castling Quiz (poate albul să facă rocada, oricare parte) ──
CK = [('rn3rk1/2q1ppbp/p1p2np1/1p6/3P4/P1N3P1/1PQ1PPBP/3RK1NR', False),
      ('r3r1k1/ppqnbppp/2p3b1/3pN3/3P1PP1/2P1NB1P/PP2K1Q1/R6R', False),
      ('r3r1k1/pb2qppp/3ppn2/2b3B1/Pp2P3/1B3N1P/1PP1QPP1/R3K2R', True),
      ('rnbq1rk1/pp3ppp/2p1pn2/3p2B1/1b1PP3/2N2P2/PPPQ2PP/R3KBNR', True),
      ('r4rk1/2qnppbp/b2p1np1/2pP4/4P3/P1N2NP1/1PQ2PBP/R1B1K2R', False),
      ('rn2k2r/ppq1bppp/2p1p1b1/4N3/3P1P2/2n1B3/PPPQB1PP/R3K2R', True),
      ('r1b1k2r/2q1bppp/p1n1p3/3pP3/1p1N1P2/3nBN2/PPP1Q1PP/R3K2R', False),
      ('r3r1k1/1p3p1p/2n3p1/p5B1/5P2/2P5/P1P3PP/R3K2R', False)]
cks = []
for i, (fen, ans) in enumerate(CK):
    b = chess.Board(full(fen, 'w'))
    k, q = allowed(b, 'w', 'K'), allowed(b, 'w', 'Q')
    if (k or q) != ans: ERR.append(('ck-castle', i + 1, k, q, ans)); continue
    parts = [can_text(b, 'w', 'K'), can_text(b, 'w', 'Q')]
    cks.append(dict(type='choice', fen=full(fen, 'w'), side='w', src=f'CK5-castle#{i + 1}', opts=['Da', 'Nu'], answer=['Da' if ans else 'Nu'],
        prompt='Poate albul să facă rocada la mutarea aceasta (mică sau mare)?', focus=['e1'],
        expl=' '.join(parts), why={'Da': 'Mai uită-te la fiecare rocadă: ' + ' '.join(x[1] for x in why_not(b, 'w', 'K')[:1] + why_not(b, 'w', 'Q')[:1]), 'Nu': 'Mai uită-te: una dintre rocade este permisă.'}))
baza.append(mk_set('ckR', 'ChessKid: poate albul să facă rocada?', 'ChessKid, lecția 5, „Castling Quiz” 1 și 2',
    'Albul este la mutare. Poate face rocada, măcar de o parte?', cks))

# ── 3. ChessKid L5: Can You Capture En Passant? ──
EPQ = [('2r2rk1/1pp1n1bp/3qnpp1/pP2p3/8/1N1P1N1P/PBP2PP1/R2QR1K1', 'w', 'a6', True, 'Negrul tocmai a jucat a7-a5.', 'b5a6',
        'Da: pionul negru a sărit două pătrate și a ajuns lângă pionul de pe b5. Albul îl poate captura en passant: bxa6.'),
       ('2r2rk1/1p1nqpb1/p1p1n1p1/7p/2Pp4/1Q4P1/PP2NPBP/3R1RK1', 'b', 'c3', True, 'Albul tocmai a jucat c2-c4.', 'd4c3',
        'Da: pionul alb a sărit două pătrate și a trecut pe lângă pionul de pe d4. Negrul îl poate captura en passant: dxc3.'),
       ('r2q1rk1/p2p1ppp/1pP2n2/4p3/P7/1P1QP1N1/5PPP/1R1R2K1', 'b', None, False, 'Negrul joacă d7-d5.', None,
        'Nu: după d7-d5 nu stă niciun pion alb lângă d5, pe linia 5. Pionul de pe c6 nu poate captura en passant.'),
       ('r1q2rk1/1p1b1p2/p1p1nPp1/3p3p/3P2PQ/2PB3R/PP2N2P/5RK1', 'w', None, False, 'Negrul tocmai a jucat h7-h5.', None,
        'Nu: pionul alb de pe g4 nu stă pe linia 5, deci nu poate captura en passant. (Pionul alb poate captura normal pe h5, dar asta nu este en passant.)')]
eps = []
for i, (fen, side, ep, ans, cap, mv, expl) in enumerate(EPQ):
    if i == 2:  # poziția e dinaintea mutării d7-d5; o arătăm după mutare
        b = chess.Board(full(fen, 'b')); b.push_uci('d7d5'); fen2 = b.fen()
    else:
        fen2 = fen + ' ' + side + ' - ' + (ep or '-') + ' 0 1'
    b = chess.Board(fen2)
    has = any(b.is_en_passant(m) for m in b.legal_moves)
    if has != ans: ERR.append(('ep-q', i + 1, has, ans)); continue
    eps.append(dict(type='choice', fen=b.board_fen() + (' w' if b.turn else ' b') + ' - - 0 1', side='w' if b.turn else 'b', src=f'CK5-ep#{i + 1}',
        opts=['Da', 'Nu'], answer=['Da' if ans else 'Nu'], prompt=cap + ' Se poate captura en passant?', expl=expl, epmove=mv,
        why={'Da': 'Mai uită-te: en passant se poate doar imediat după ce un pion sare două pătrate și ajunge chiar lângă pionul tău, pe aceeași linie.', 'Nu': 'Mai uită-te: pionul a sărit două pătrate și a ajuns lângă un pion advers.'}))
baza.append(mk_set('ckE', 'ChessKid: se poate captura en passant?', 'ChessKid, lecția 5, „Can You Capture En Passant?”',
    'Citește ce mutare s-a jucat chiar acum. Se poate captura en passant?', eps))

# ── 4. Chess Tutor 9a, 9b: care rocade sunt permise? ──
def castles(sid, id, title):
    tasks = []
    for t in load(sid)['tasks']:
        fen = t['before']['fen']
        b = chess.Board(full(fen, 'w'))
        allow = [LBL[(c, s)] for c in 'wb' for s in 'KQ' if allowed(b, c, s)]
        reasons = {LBL[(c, s)]: can_text(b, c, s) for c in 'wb' for s in 'KQ'}
        ct = ' '.join(t['after']['texts'][1:-1]).replace('\r\n', ' ')
        print(f'{sid}#{t["i"]}', allow, '| CT:', ct[:150])
        tasks.append(dict(type='castles', fen=full(fen, 'w'), side='', src=f'{sid}#{t["i"]}', answer=allow, reasons=reasons,
            prompt='Bifează toate rocadele permise (pentru alb și pentru negru), apoi apasă „Verifică”.'))
    return mk_set(id, title, 'Chess Tutor Step 1, lecția 9', 'Nu contează cine e la mutare. Pentru fiecare jucător și pentru fiecare parte, întreabă-te dacă rocada este permisă.', tasks)
mediu = [castles('L9e_a', '9a', 'Rocada: da sau nu? (1)'), castles('L9e_b', '9b', 'Rocada: da sau nu? (2)')]

# ── 5. Chess Tutor 9c: de ce nu e permisă rocada? ──
WHY_OPTS = {'moved': 'Regele sau turnul au mutat deja', 'between': 'O piesă stă între rege și turn', 'check': 'Regele este în șah',
            'cross': 'Regele ar trece printr-un pătrat atacat', 'land': 'Regele ar ajunge în șah'}
av = []
tasks = []
for t in load('L9e_c')['tasks']:
    fen = t['after']['fen'] if t['i'] == 6 else t['before']['fen']   # la 6 Chess Tutor arată cum turnul s-a întors pe h1
    q = ' '.join(t['after']['texts'])
    sd = 'Q' if 'castle long' in q else 'K'
    b = chess.Board(full(fen, 'w'))
    moved = 'Turnul de pe h1 a mai mutat (a fost pe h3 și s-a întors), deci rocada mică nu mai e permisă.' if t['i'] == 6 and sd == 'K' else None
    w = why_not(b, 'w', sd, moved)
    if t['i'] == 7 and not w: w = [('moved', 'Regele a mutat deja.')]
    print('L9e_c#%d' % t['i'], sd, [x[0] for x in w], '| CT:', ' '.join(t['after']['texts'][1:-1])[:120].replace('\r\n', ' '))
    if not w: ERR.append(('9c-allowed', t['i'])); continue
    nm = 'rocada mică' if sd == 'K' else 'rocada mare'
    tasks.append(dict(type='choice', fen=full(fen, 'w'), side='w', src=f'L9e_c#{t["i"]}', opts=list(WHY_OPTS.values()),
        answer=[WHY_OPTS[x[0]] for x in w], prompt=f'De ce nu poate albul să facă {nm}?', focus=[HOME[('w', sd)][0], HOME[('w', sd)][1]],
        expl=' '.join(x[1] for x in w), why={v: 'Nu acesta e motivul aici. Mai uită-te.' for v in WHY_OPTS.values()}))
av.append(mk_set('9c', 'De ce nu e permisă rocada?', 'Chess Tutor Step 1, lecția 9', 'Albul nu poate face rocada. Alege motivul.', tasks))

# ── 6. Chess Tutor 14a: mat într-o mutare (cu en passant) ──
def mate_ep(sid, id, title):
    tasks = []
    for t in load(sid)['tasks']:
        bf, af = t['before']['fen'], t['after']['fen']
        found = None
        for side in 'wb':
            b = chess.Board(full(bf, side))
            for m in b.legal_moves:
                b2 = b.copy(); b2.push(m)
                if b2.board_fen() == af and b2.is_checkmate(): found = (side, m)
        if not found: ERR.append(('14a-nomate', t['i'])); continue
        side, m = found
        b = chess.Board(full(bf, side))
        mates = [x.uci() for x in b.legal_moves if (lambda bb: (bb.push(x), bb.is_checkmate())[1])(b.copy())]
        # mutările care ar fi mat fără en passant (pagina nu știe singură de en passant)
        notmate = {}
        for x in b.legal_moves:
            b2 = b.copy(); b2.push(x)
            if b2.is_check() and not b2.is_checkmate():
                esc = [y for y in b2.legal_moves if b2.is_en_passant(y)]
                others = [y for y in b2.legal_moves if not b2.is_en_passant(y)]
                if esc and not others:
                    notmate[x.uci()] = f'Nu e mat: pionul de pe {sqn(esc[0].from_square)} capturează en passant ({ro_san(b2.san(esc[0]))}) și scapă regele din șah.'
        san = ro_san(b.san(m))
        txt = ' '.join(t['after']['texts'][1:-1])
        expl = f'{san} și mat.'
        if 'may not capture en passant' in txt:
            b2 = b.copy(); b2.push(m)
            expl += f' Pionul de pe {sqn(b2.ep_square + (8 if side == "w" else -8)) if b2.ep_square is not None else ""} nu poate captura en passant: regele lui ar rămâne în șah.'
        elif b.piece_at(m.from_square).piece_type == chess.PAWN and abs(m.to_square - m.from_square) == 16:
            b2 = b.copy(); b2.push(m)
            if b2.ep_square is not None:
                expl += ' Pionul a sărit două pătrate. En passant nu salvează: nu există sau ar lăsa regele în șah.'
        tasks.append(dict(type='move', check='mate', fen=full(bf, side), side=side, answer=m.uci(), san=san, ok=[x for x in mates if x != m.uci()],
                          notmate=notmate, src=f'{sid}#{t["i"]}', expl=expl))
        print(f'{sid}#{t["i"]}', side, san, 'mates', mates, 'notmate', list(notmate))
    return mk_set(id, title, 'Chess Tutor Step 1, lecția 14', 'Dă mat într-o mutare. Ai grijă la en passant: uneori o mutare de pion care pare mat poate fi capturată en passant.', tasks,
                  'Dă mat într-o mutare.')
av.append(mate_ep('L14e_a', '14a', 'Mat într-o mutare (en passant)'))

# ── 7. ChessKid L14: promovare sau subpromovare ──
PR = [('6bk/5P2/7K/5N2/8/8/8/8', 'f7f8b', [], 'Subpromovare în nebun: 1.f8=N! Nebunul negru pleacă, 2.Ce7 și 3.Ng7 mat. Cu regină sau turn ar fi pat imediat.'),
      ('8/4KP1k/6p1/6P1/8/8/8/8', 'f7f8r', ['f7f8n', 'f7f8b'], 'Subpromovare: 1.f8=T! (merg și calul sau nebunul). Cu regină ar fi pat: regele negru nu mai are nicio mutare.'),
      ('R7/5k1P/8/3K4/4R3/2B5/8/8', 'h7h8n', [], 'Subpromovare în cal: 1.h8=C este mat imediat! Calul dă șah, iar regele negru nu are unde să plece.'),
      ('8/5k1P/7P/4R3/6K1/8/8/8', 'h7h8q', [], 'Aici regina este cea mai bună: 1.h8=D! Rg6 2.Dg7 mat.')]
prs = []
for i, (fen, ans, ok, expl) in enumerate(PR):
    b = chess.Board(full(fen, 'w'))
    if chess.Move.from_uci(ans) not in b.legal_moves: ERR.append(('promo', i + 1)); continue
    bad = {}
    for p in 'qrbn':
        u = ans[:4] + p
        if u == ans or u in ok: continue
        b2 = b.copy(); b2.push_uci(u)
        bad[u] = 'Pat! Negrul nu e în șah și nu mai are nicio mutare: remiză.' if b2.is_stalemate() else 'Nu este cea mai bună piesă aici. Încearcă alta.'
    prs.append(dict(type='move', check='best', fen=full(fen, 'w'), side='w', answer=ans, san=ro_san(b.san(chess.Move.from_uci(ans))), ok=ok, badpromo=bad, src=f'CK14-promo#{i + 1}', expl=expl))
av.append(mk_set('ck14', 'Regina sau altă piesă?', 'ChessKid, lecția 14, „To Under or Promote?”',
    'Albul are mat în trei mutări. Promovează pionul în piesa potrivită: uneori regina dă pat!', prs, 'Promovează pionul în piesa potrivită.'))

if ERR:
    for e in ERR: print('EROARE', e)
    sys.exit(1)
DATA = dict(tabs=[dict(id='baza', title='De bază', sets=baza), dict(id='mediu', title='Mediu', sets=mediu), dict(id='avansat', title='Avansat', sets=av)])
open(OUT, 'w', encoding='utf-8').write('/* Exercițiile lecției „Mutări speciale”.\n   Surse: caietul Steps pasul 1, ChessKid lecțiile 5 și 14, Chess Tutor Step 1 (lecțiile 9 și 14).\n   Generat automat — nu edita de mână. */\nwindow.L3EX = ' + json.dumps(DATA, ensure_ascii=False) + ';\n')
tot = 0
for t in DATA['tabs']:
    for st in t['sets']: print(t['id'], st['id'], len(st['tasks'])); tot += len(st['tasks'])
print('total', tot)
