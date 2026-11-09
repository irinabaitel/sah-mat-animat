# Builds data/nivel1_lectia6_ex.js (Chess Tutor Step 1 L6 + ChessKid L3 + Steps workbook)
import json, re, sys, os, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia6_ex.js'
NAME = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
RO_LET = {'K': 'R', 'Q': 'D', 'R': 'T', 'B': 'N', 'N': 'C'}
def ro_san(san): return ''.join(RO_LET.get(c, c) if c.isupper() else c for c in san)
CAP = lambda s: s[0].upper() + s[1:]
def g(pt, w): return w + 'ă' if pt == chess.QUEEN else w
def load(n): return json.load(open('sets/' + n + '.json', encoding='utf-8'))
def sqn(s): return chess.square_name(s)
def legal_capturers(b, sq): return [m.from_square for m in b.legal_moves if m.to_square == sq]
ERR = []

def expl_move(b, m, kind):
    p = b.piece_at(m.from_square); cap = b.piece_at(m.to_square); to = sqn(m.to_square); nm = NAME[p.piece_type]
    if kind == 'give':
        s = f'{CAP(nm)} dă șah de pe {to}'
        if cap: s += f' și capturează {NAME[cap.piece_type]}'
        return s + f'. Acolo nu poate fi {g(p.piece_type, "capturat")}.'
    if kind == 'out':
        chk = list(b.checkers())
        if p.piece_type == chess.KING and not cap:
            return f'Regele fuge pe {to}, unde nu mai este atacat.'
        if cap and m.to_square in chk:
            return f'{CAP(nm)} capturează {NAME[cap.piece_type]} care dădea șah.'
        if cap:
            return f'{CAP(nm)} capturează {NAME[cap.piece_type]}.'
        return f'{CAP(nm)} se pune în calea șahului, pe {to}.'
    return None

def move_task(fen, uci, kind, ok=(), expl=None, okmsg=None):
    b = chess.Board(fen); m = chess.Move.from_uci(uci)
    assert m in b.legal_moves, (fen, uci)
    if kind == 'give': assert b.gives_check(m), (fen, uci)
    if kind == 'out': assert b.is_check(), (fen, uci)
    for u in ok: assert chess.Move.from_uci(u) in b.legal_moves, (fen, u)
    d = dict(type='move', fen=fen, side='w' if b.turn else 'b', answer=uci, san=ro_san(b.san(m)), ok=list(ok), check=kind,
             expl=expl or expl_move(b, m, kind))
    if okmsg: d['okmsg'] = okmsg
    return d

def checksq_task(fen, frm, answers, prompt, safe=True):
    b = chess.Board(fen); s0 = chess.parse_square(frm); comp = []
    for m in b.legal_moves:
        if m.from_square != s0 or not b.gives_check(m) or b.is_capture(m): continue
        b2 = b.copy(); b2.push(m)
        if safe and legal_capturers(b2, m.to_square): continue
        comp.append(sqn(m.to_square))
    if sorted(comp) != sorted(answers): ERR.append(('checksq', fen, sorted(comp), sorted(answers)))
    p = b.piece_at(s0)
    return dict(type='checksq', fen=fen, side='w' if p.color else 'b', from_=frm, answers=answers, safe=safe, prompt=prompt,
                expl=CAP(NAME[p.piece_type]) + ' dă șah' + (' din siguranță' if safe else '') + ' de pe ' + ', '.join(answers[:-1]) + (' și ' if len(answers) > 1 else '') + answers[-1] + '.')

def route_task(fen, frm, route, promo=None):
    b = chess.Board(fen); s0 = chess.parse_square(frm); p = b.piece_at(s0)
    b.turn = p.color; cur = s0
    for k, t in enumerate(route):
        mv = chess.Move(cur, chess.parse_square(t), promotion=(chess.Piece.from_symbol(promo).piece_type if promo and k == len(route) - 1 else None))
        assert mv in b.legal_moves and not b.is_capture(mv), (fen, frm, route)
        if k == len(route) - 1: assert b.gives_check(mv), (fen, route)
        b.push(mv)
        assert not legal_capturers(b, mv.to_square), ('unsafe', fen, route, t)
        b.turn = p.color; cur = mv.to_square
    side = 'w' if p.color else 'b'
    e = f'Drumul: {frm} → ' + ' → '.join(route) + (f' (pionul devine {NAME[chess.Piece.from_symbol(promo).piece_type]})' if promo else '') + '. A doua mutare dă șah, iar piesa stă în siguranță.'
    return dict(type='route', fen=fen.split(' ')[0] + f' {side} - - 0 1', side=side, from_=frm, target=None, moves=2, mode='check', route=route, promo=promo, expl=e)

def mk_set(id, title, src, intro, tasks, instr=None): return dict(id=id, title=title, src=src, intro=intro, instr=instr, tasks=tasks)
CT = 'Chess Tutor Step 1 · lecția 6'; CTX = 'Chess Tutor Step 1 · lecția 6 (extra)'
baza, mediu, av = [], [], []

# ---------- MEDIU ----------
d = load('L6x_a'); tasks = []
for t in d['tasks']:
    a = t['answer']; tasks.append(move_task(t['before']['fen'] + f" {a['side']} - - 0 1", a['uci'], 'give'))
mediu.append(mk_set('6a', 'Dă șah', CT, 'Dă șah regelui adversarului. Ai grijă: piesa care dă șah nu are voie să poată fi capturată. Uită-te la toate șahurile posibile și alege-l pe cel sigur.', tasks, 'Dă șah din siguranță.'))

def out_set(sid, id, title, src, intro, extra=None):
    d = load(sid); tasks = []
    for t in d['tasks']:
        a = t['answer']; fen = t['before']['fen'] + f" {a['side']} - - 0 1"
        kind = 'out' if a['check'] else 'best'
        e = extra(t) if extra else None
        tasks.append(move_task(fen, a['uci'], kind, ok=t['sf']['alts'] if kind == 'out' else (), expl=e))
    return mk_set(id, title, src, intro, tasks, 'Joacă cea mai bună mutare.')
mediu.append(out_set('L6x_b', '6b', 'Ieși din șah', CT, 'Regele tău este în șah. Ai trei feluri de a ieși din șah: <strong>fugi</strong> cu regele, <strong>capturezi</strong> piesa care dă șah sau <strong>pui o piesă în cale</strong>. Alege-l pe cel mai bun: să nu pierzi nimic.'))

d = load('L6x_c'); tasks = []
for t in d['tasks']:
    txt = t['after']['texts'][0]; sqs = re.findall(r'\b([a-h][1-8])\b', txt.split(':', 1)[1])
    fen = t['before']['fen'] + ' w - - 0 1'; b = chess.Board(fen)
    q = [sqn(s) for s in b.pieces(chess.QUEEN, chess.WHITE)][0]
    tasks.append(checksq_task(fen, q, sqs, 'De pe ce pătrate poate da regina șah din siguranță? Atinge-le pe toate.'))
mediu.append(mk_set('6c', 'De unde dă regina șah?', CT, 'Regina albă poate da șah dintr-o singură mutare. Găsește <strong>toate</strong> pătratele de unde dă șah și unde nu poate fi capturată.', tasks))

def route_set(sid, id, title, src, intro):
    d = load(sid); tasks = []
    for t in d['tasks']:
        txt = t['after']['texts'][0].replace('−', '-')
        sq = re.findall(r'\b([a-h][1-8])\b', txt)
        m = re.search(r'(knight|bishop|rook|queen) check', txt)
        promo = {'knight': 'N', 'bishop': 'B', 'rook': 'R', 'queen': 'Q'}[m.group(1)] if m else None
        tasks.append(route_task(t['before']['fen'] + ' w - - 0 1', sq[0], sq[1:3], promo))
    return mk_set(id, title, src, intro, tasks, 'Dă șah din siguranță la a doua mutare.')
INTRO_R = 'Mută numai piesa albă care nu e rege. Ai <strong>două mutări</strong>, iar adversarul nu mută între ele. La a doua mutare trebuie să dai <strong>șah</strong>. Pe drum nu ai voie să capturezi și nici să te oprești pe un pătrat unde piesa poate fi capturată.'
mediu.append(route_set('L6x_d', '6d', 'Șah din două mutări', CT, INTRO_R))

# ---------- AVANSAT ----------
av.append(out_set('L6e_a', 'L6e_a', 'Ieși din șah (2)', CTX, 'Regele tău este în șah. Fugi, capturează sau pune o piesă în cale. Alege mutarea cu care nu pierzi nimic.'))
TR = {'The attacker has been captured.': 'Atacatorul a fost capturat.',
      'The piece which was being threatened is safe.': 'Piesa atacată a fugit pe un pătrat sigur.',
      'The piece which was being threatened is protected.': 'Piesa atacată este acum apărată.',
      'The correct defence: interposing.': 'Apărarea corectă: o piesă se pune în calea atacului.',
      'The correct form of defence is interposing.': 'Apărarea corectă: o piesă se pune în calea atacului.'}
av.append(out_set('L6e_b', 'L6e_b', 'Apărare: toate felurile', CTX, 'O piesă e atacată. Alege apărarea cea bună: fugi, o aperi, capturezi atacatorul sau pui o piesă în cale.', extra=lambda t: TR[t['after']['texts'][0]]))
d = load('L6e_c'); tasks = []
for t in d['tasks']:
    sq = re.search(r'square ([a-h][1-8])', t['before']['texts'][-1]).group(1)
    tasks.append(dict(type='clicksq', answer=sq, prompt=f'Atinge pătratul {sq}.', expl=f'Acesta este pătratul {sq}.'))
av.append(mk_set('L6e_c', 'Găsește pătratul', CTX, 'Tabla nu are litere și cifre pe margine. Atinge pătratul cerut.', tasks))
av.append(route_set('L6e_d', 'L6e_d', 'Șah din două mutări (2)', CTX, INTRO_R))

# ---------- DE BAZĂ: ChessKid lecția 3 ----------
CK = 'ChessKid · lecția 3'
K1 = [('8/3k4/8/8/8/8/6R1/1K6 w - - 0 1', 'g2', ['d2', 'g7']), ('8/8/3k4/8/8/8/8/1K2B3 w - - 0 1', 'e1', ['b4', 'g3']),
      ('8/8/4k3/8/8/5N2/8/6K1 w - - 0 1', 'f3', ['d4', 'g5']), ('6k1/8/8/8/8/8/4Q3/6K1 w - - 0 1', 'e2', ['a2', 'c4', 'e6', 'e8', 'g2', 'g4'])]
tasks = []
for f, frm, ans in K1:
    b = chess.Board(f); pn = NAME[b.piece_at(chess.parse_square(frm)).piece_type]
    tasks.append(checksq_task(f, frm, ans, f'De pe ce pătrate poate da {pn} șah? Atinge-le pe toate ({len(ans)}).', safe=False))
baza.append(mk_set('ck_give', 'Dă șah regelui', CK, 'Piesa albă poate da șah dintr-o mutare. Găsește toate pătratele de unde dă șah regelui negru.', tasks))
K2 = [('2k5/8/8/8/8/8/2r5/1RKR4 w - - 0 1', 'c1c2'), ('1b4k1/8/8/4q3/2NK4/8/8/8 w - - 0 1', 'c4e5'),
      ('1r5B/8/2N5/K7/4k3/8/8/r7 w - - 0 1', 'h8a1'), ('8/7k/6n1/6rK/7n/6b1/8/8 w - - 0 1', 'h5g5')]
baza.append(mk_set('ck_cap', 'Capturează piesa care dă șah', CK, 'Regele alb e în șah. Ieși din șah capturând piesa care dă șah.', [move_task(f, u, 'out') for f, u in K2], 'Capturează piesa care dă șah.'))
K3 = [('5krr/2B2p2/8/8/8/8/5P2/5RK1 w - - 0 1', 'c7g3', ()), ('r4rk1/pbp3pp/1p1p4/4p3/3PK3/2PNP3/PP4PP/3RR3 w - - 0 1', 'd4d5', ()),
      ('rnb1kbnr/pp1p1ppp/4p3/2p5/4P2q/2N2P2/PPPP2PP/R1BQKBNR w - - 0 1', 'g2g3', ()),
      ('rnbqr1k1/ppp2ppp/3p1n2/8/8/B1PP1N2/P1P2PPP/R2QKB1R w - - 0 1', 'f1e2', ('d1e2', 'f3e5'))]
tasks = [move_task(f, u, 'out', ok=ok, okmsg='Corect, ai blocat șahul. Cea mai bună este însă Ne2: nebunul valorează mai puțin decât regina.' if ok else None) for f, u, ok in K3]
baza.append(mk_set('ck_block', 'Pune o piesă în cale', CK, 'Regele alb e în șah. Ieși din șah punând o piesă între rege și piesa care dă șah.', tasks, 'Blochează șahul.'))
K4 = [('4k3/8/7R/8/3n4/8/8/r2K4 w - - 0 1', 'd1d2', ()), ('8/2k5/8/4K3/8/1b4n1/1b6/8 w - - 0 1', 'e5f4', ()),
      ('8/8/8/8/4k3/4q3/8/4K3 w - - 0 1', 'e1d1', ('e1f1',)), ('8/6b1/4p3/5pp1/2p1K3/8/4n1k1/8 w - - 0 1', 'e4e3', ())]
baza.append(mk_set('ck_run', 'Fugi cu regele', CK, 'Regele alb e în șah. Mută-l pe un pătrat unde nu mai e atacat.', [move_task(f, u, 'out', ok=ok) for f, u, ok in K4], 'Fugi cu regele pe un pătrat sigur.'))

# ---------- DE BAZĂ: caietul Steps ----------
WB = 'wb/workbook_check.json'
if os.environ.get('WB') and os.path.exists(WB):
    w = json.load(open(WB, encoding='utf-8'))
    for key, id, title, intro, kind, instr in (
        ('give_A', 'wb_give', 'Dă șah (caiet)', 'Dă șah din siguranță. Nu ai voie să pierzi material.', 'give', 'Dă șah din siguranță.'),
        ('out_A', 'wb_outA', 'Ieși din șah (caiet A)', 'Regele e în șah. Fugi, capturează sau pune o piesă în cale. Alege mutarea cea mai bună.', 'out', 'Joacă cea mai bună mutare.'),
        ('out_B', 'wb_outB', 'Ieși din șah (caiet B)', 'Regele e în șah. Alege cea mai bună apărare: să nu pierzi nimic.', 'out', 'Joacă cea mai bună mutare.')):
        tasks = []
        for x in w[key]:
            u = x['answer_uci']; tasks.append(move_task(x['fen'], u[0], kind, ok=u[1:]))
        baza.append(mk_set(id, title, 'Steps · caietul pasului 1', intro, tasks, instr))
else:
    print('NO WORKBOOK YET')

DATA = dict(tabs=[dict(id='baza', title='De bază', sets=baza), dict(id='mediu', title='Mediu', sets=mediu), dict(id='avansat', title='Avansat', sets=av)])
js = json.dumps(DATA, ensure_ascii=False).replace('"from_"', '"from"')
open(OUT, 'w', encoding='utf-8').write('/* Exercițiile lecției „Atacul asupra regelui” (șahul).\n   Surse: Chess Tutor Step 1 (metoda Steps, lecția 6), ChessKid (lecția 3), caietul Steps pasul 1.\n   Generat automat — nu edita de mână. */\nwindow.L6EX = ' + js + ';\n')
for t in DATA['tabs']: print(t['title'], [(s['id'], len(s['tasks'])) for s in t['sets']])
print('ERR', ERR)
