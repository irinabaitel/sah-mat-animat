# Builds data/nivel1_lectia17_ex.js — lecția „Patul”
# Surse: caietul Steps pasul 1 „Mate, stalemate or play: A” (wb/stalemate_A.json), ChessKid L4 „Checkmate or Stalemate?”,
#        Chess Tutor Step 1 lecția 12 (12a, 12b) și lecția avansată P6 (P6a–d).
import json, os, sys, re, subprocess, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia17_ex.js'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
NAME = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
RO_LET = {'K': 'R', 'Q': 'D', 'R': 'T', 'B': 'N', 'N': 'C'}
def ro_san(san): return ''.join(RO_LET.get(c, c) if c.isupper() else c for c in san)
def sqn(s): return chess.square_name(s)
COL = {'w': 'albul', 'b': 'negrul'}
COLA = {'w': 'alb', 'b': 'negru'}
ERR = []

SF = subprocess.Popen(['node', os.path.join(HERE, 'node_modules/stockfish/bin/stockfish-19-lite-single.js')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
def send(c): SF.stdin.write(c + '\n'); SF.stdin.flush()
def wait(tok):
    out = []
    while True:
        l = SF.stdout.readline()
        if not l: return out
        out.append(l.strip())
        if l.startswith(tok): return out
send('uci'); wait('uciok'); send('setoption name MultiPV value 40'); send('isready'); wait('readyok')
def sf_scores(fen, depth=16):
    send('ucinewgame'); send('position fen ' + fen); send(f'go depth {depth}')
    res = {}
    for l in wait('bestmove'):
        m = re.search(r' depth (\d+) .*multipv \d+ score (cp|mate) (-?\d+).* pv (\S+)', l)
        if m and int(m.group(1)) == depth:
            v = int(m.group(3)); res[m.group(4)] = v if m.group(2) == 'cp' else (100000 - abs(v)) * (1 if v > 0 else -1)
    return res

def board(fen, side):
    b = chess.Board(None); b.set_board_fen(fen.split(' ')[0]); b.turn = side == 'w'; return b
def full(b): return b.board_fen() + (' w' if b.turn else ' b') + ' - - 0 1'
def state(b):
    if b.is_checkmate(): return 'mate'
    if b.is_stalemate(): return 'stale'
    return 'play'
def opp(s): return 'b' if s == 'w' else 'w'

# ── explicații generate din poziție ──
def expl_state(b, st, mv=None):
    s = 'w' if b.turn else 'b'
    if st == 'mate':
        return f'Regele {COLA[s]} este în șah și nu are nicio mutare: <strong>mat</strong>. Câștigă {COL[opp(s)]}.'
    if st == 'stale':
        pieces = [p for p in b.piece_map().values() if p.color == b.turn and p.piece_type != chess.KING]
        extra = ' Nici celelalte piese ale lui nu pot muta.' if pieces else ''
        return f'Regele {COLA[s]} nu este în șah, dar nu are nicio mutare.{extra} Este <strong>pat</strong>: partida se termină remiză.'
    m = mv or describe_pick(b)
    p = b.piece_at(m.from_square)
    what = f'{NAME[p.piece_type]} de pe {sqn(m.from_square)} poate muta: {ro_san(b.san(m))}'
    chk = ' Regele e în șah, dar poate scăpa.' if b.is_check() else ''
    return f'Nu e nici mat, nici pat: {COL[s]} mai poate muta.{chk} De exemplu, {what}.'
def describe_pick(b):
    ms = list(b.legal_moves)
    caps = [m for m in ms if b.is_capture(m)]
    return (caps or ms)[0]

def mk_set(id, title, src, intro, tasks, instr=None):
    return dict(id=id, title=title, src=src, intro=intro, instr=instr, tasks=[t for t in tasks if t])
def load(n): return json.load(open(os.path.join(HERE, 'sets', n + '.json'), encoding='utf-8'))
def fpos(fen):
    b = chess.Board(None); b.set_board_fen(fen); return {sqn(s): p.symbol() for s, p in b.piece_map().items()}

OPTS3 = ['Mat', 'Pat', 'Se joacă']
KEY = {'mate': 'Mat', 'stale': 'Pat', 'play': 'Se joacă'}
def msp(fen, side, src, st_expect=None, move=None, opts=OPTS3, prompt=None, extra=''):
    b = board(fen, side); st = state(b)
    if st_expect and st != st_expect: ERR.append(('msp-state', src, st, st_expect)); return None
    t = dict(type='msp', fen=full(b), side=side, opts=opts, answer=KEY[st], src=src)
    if prompt: t['prompt'] = prompt
    if st == 'play' and move:
        m = chess.Move.from_uci(move)
        if m not in b.legal_moves: ERR.append(('msp-move', src, move)); return None
        t['move'] = move; t['san'] = ro_san(b.san(m))
        t['ok'] = [x.uci() for x in b.legal_moves if x != m and good_alt(b, m, x)]
        t['expl'] = expl_state(b, st, m) + (' ' + extra if extra else '')
        t['mexpl'] = 'Corect: ' + t['san'] + '.' + (' ' + extra if extra else '')
    else:
        t['expl'] = expl_state(b, st) + (' ' + extra if extra else '')
    if st == 'mate':
        t['hl'] = [sqn(q) for q in b.checkers()]
    return t
def good_alt(b, m, x):
    sc = sf_scores(full(b))
    a, y = sc.get(m.uci()), sc.get(x.uci())
    return a is not None and y is not None and y >= a - 50

# ═════════ DE BAZĂ ═════════
WB = 'Steps · caietul pasului 1'
baza = []
ta = []
for e in json.load(open(os.path.join(HERE, 'wb', 'stalemate_A.json'), encoding='utf-8')):
    if not e['fen']: continue
    fen, side = e['fen'].split(' ')[0], e['fen'].split(' ')[1]
    st = {'mate': 'mate', 'stalemate': 'stale', 'play': 'play'}[e['kind']]
    ta.append(msp(fen, side, f"A{e['n']}", st, e.get('answer')))
baza.append(mk_set('wbA', 'Mat, pat sau se joacă?', WB,
    'Uită-te la partea care e la mutare. Este în șah? Poate muta regele? Poate muta altă piesă? Alege răspunsul. Dacă partida continuă, joacă apoi mutarea.', ta,
    'Mat, pat sau se joacă?'))

CK4 = [  # ChessKid lecția 4, „Checkmate or Stalemate?” (răspunsurile din Answer Key)
    ('1k6/1Q6/2K5/8/8/8/8/8', 'b', 'mate'), ('1r1q1r1k/2bbN1p1/2p2p2/pp1p4/3P1PP1/2P5/PP1B4/2K1R2R', 'b', 'mate'),
    ('k7/2Q5/K7/8/8/8/8/8', 'b', 'stale'), ('2K5/8/8/8/8/8/1R4R1/k7', 'b', 'stale'),
    ('3K4/8/8/5bk1/4r3/6b1/8/8', 'w', 'stale'), ('7k/8/6KN/4B3/8/8/8/8', 'b', 'mate'),
    ('8/8/8/8/8/6K1/8/1R4k1', 'b', 'mate'), ('8/8/3p4/3P3p/7P/NK6/3N4/k7', 'b', 'stale'),
]
tc = [msp(f, s, f'CK4-{i}', st, opts=['Mat', 'Pat']) for i, (f, s, st) in enumerate(CK4, 1)]
baza.append(mk_set('ck4', 'Mat sau pat?', 'ChessKid · lecția 4',
    'Regele nu mai are nicio mutare. Este în șah? Atunci e mat. Nu e în șah și nicio altă piesă nu poate muta? Atunci e pat.', tc, 'Mat sau pat?'))

# ═════════ MEDIU: Chess Tutor L12 ═════════
CT1 = 'Chess Tutor Step 1 · lecția 12'
def side_from(txt):
    t = ' '.join(txt)
    m = re.search(r'\b(White|Black) (is|can)', t)
    return ('w' if m.group(1) == 'White' else 'b') if m else None
def ct_msp(sid, id, title):
    tasks = []
    for t in load(sid)['tasks']:
        side = side_from(t['after']['texts'])
        if not side: ERR.append(('side?', sid, t['i'])); continue
        fen = t['before']['fen']; b = board(fen, side); st = state(b)
        txt = ' '.join(t['after']['texts'])
        want = 'stale' if 'stalemated' in txt else 'mate' if 'mated' in txt else 'play'
        if st != want: ERR.append(('ct-state', sid, t['i'], st, want)); continue
        mv = None
        if st == 'play' and t['after']['fen'] != fen:   # Chess Tutor arată o mutare: o folosim în explicație
            z = fpos(t['after']['fen'])
            for m in b.legal_moves:
                bb = b.copy(); bb.push(m)
                if {sqn(q): p.symbol() for q, p in bb.piece_map().items()} == z: mv = m
        tk = msp(fen, side, f'{sid}#{t["i"]}', st)
        if tk and mv: tk['expl'] = expl_state(b, st, mv)
        tasks.append(tk)
    return mk_set(id, title, CT1, 'Uită-te la partea care e la mutare. Este în șah? Poate muta regele? Poate muta altă piesă? Abia apoi alege.', tasks, 'Mat, pat sau se joacă?')
mediu = [ct_msp('L12e_a', '12a', 'Mat, pat sau se joacă? (1)'), ct_msp('L12e_b', '12b', 'Mat, pat sau se joacă? (2)')]

# ═════════ AVANSAT: Chess Tutor P6 ═════════
CTP = 'Chess Tutor Step 1 · lecția P6'
def kplace(sid, id, title, intro):
    tasks = []
    for t in load(sid)['tasks']:
        txt = ' '.join(t['after']['texts'])
        kc = 'w' if 'white king' in txt else 'b'
        fen = t['before']['fen']; K = 'K' if kc == 'w' else 'k'
        if K in fen: ERR.append(('kplace-has-king', sid, t['i'])); continue
        ans = []
        for q in chess.SQUARES:
            b = board(fen, kc)
            if b.piece_at(q): continue
            b.set_piece_at(q, chess.Piece(chess.KING, kc == 'w'))
            if b.is_stalemate(): ans.append(sqn(q))
        zk = [q for q, p in fpos(t['after']['fen']).items() if p == K]
        if not ans or (zk and zk[0] not in ans): ERR.append(('kplace', sid, t['i'], ans, zk)); continue
        tasks.append(dict(type='kplace', fen=fen + ' ' + kc + ' - - 0 1', side=kc, kc=kc, answers=ans, src=f'{sid}#{t["i"]}',
            prompt='Pune regele ' + COLA[kc] + ' pe tablă așa încât ' + COL[kc] + ', la mutare, să fie în pat.',
            expl=('Pe ' + ans[0] + ' regele nu e în șah și nu are nicio mutare' + (', iar nici celelalte piese ale lui nu pot muta' if len([c for c in fen if (c.isupper() if kc == 'w' else c.islower()) and c.isalpha()]) else '') + ': pat.'
                  + (' Merge și pe ' + ', '.join(ans[1:]) + '.' if len(ans) > 1 else ''))))
    return mk_set(id, title, CTP, intro, tasks)

NS_FIX = {('P6_b', 7): ('w', 'g5g6'),   # Chess Tutor arată trei mutări deodată (g6 Rg7 Re7)
          ('P6_c', 10): ('w', 'g2g6')}  # Chess Tutor nu arată mutarea; Tg6 (turnul se dă, pionul f merge la damă)
def nostale(sid, id, title, intro, instr):
    tasks = []
    for t in load(sid)['tasks']:
        a, z = t['before']['fen'], t['after']['fen']
        best = None
        for side in 'wb':
            b = board(a, side)
            for m in b.legal_moves:
                bb = b.copy(); bb.push(m)
                r = {sqn(q): p.symbol() for q, p in bb.piece_map().items()}; zz = fpos(z)
                d = sum(1 for q in set(r) | set(zz) if r.get(q) != zz.get(q))
                if best is None or d < best[0]: best = (d, side, m)
        if best and best[0] > 2:   # Chess Tutor a jucat și răspunsul adversarului
            zz = fpos(z)
            for side in 'wb':
                b = board(a, side)
                for m in b.legal_moves:
                    bb = b.copy(); bb.push(m)
                    for r in bb.legal_moves:
                        b3 = bb.copy(); b3.push(r)
                        if {sqn(q): p.symbol() for q, p in b3.piece_map().items()} == zz: best = (0, side, m)
        if (sid, t['i']) in NS_FIX: side, u = NS_FIX[(sid, t['i'])]; best = (0, side, chess.Move.from_uci(u))
        if not best or best[0] > 2: ERR.append(('nostale-diff', sid, t['i'], best and best[0])); continue
        _, side, m = best
        b = board(a, side)
        sc = sf_scores(full(b))
        av = sc.get(m.uci())
        if av is None: ERR.append(('sf-miss', sid, t['i'])); continue
        ok = []
        for x in b.legal_moves:
            if x == m: continue
            bb = b.copy(); bb.push(x)
            if bb.is_stalemate(): continue
            v = sc.get(x.uci())
            if v is not None and v >= av - 50 and v >= max(sc.values()) - 80: ok.append(x.uci())
        stale = []
        for x in b.legal_moves:
            bb = b.copy(); bb.push(x)
            if bb.is_stalemate(): stale.append(x.uci())
        ctx = ' '.join(t['after']['texts']).split('/')
        tasks.append(dict(type='move', check='nostale', fen=full(b), side=side, answer=m.uci(), san=ro_san(b.san(m)), ok=ok, stale=stale,
                          src=f'{sid}#{t["i"]}', expl=expl_nostale(b, m)))
    return mk_set(id, title, CTP, intro, tasks, instr)
def expl_nostale(b, m):
    bb = b.copy(); bb.push(m)
    san = ro_san(b.san(m))
    if bb.is_stalemate(): ERR.append(('answer-stalemates', full(b), m.uci()))
    st = []
    for x in b.legal_moves:
        b2 = b.copy(); b2.push(x)
        if b2.is_stalemate(): st.append(ro_san(b.san(x)))
    warn = (' Atenție: ' + ', '.join(st[:3]) + (' ar fi dat' if len(st) > 1 else ' ar fi dat') + ' pat.') if st else ''
    if bb.is_checkmate(): return f'{san}: mat.{warn}'
    pieces = '' if bb.is_check() else ''
    if bb.is_attacked_by(bb.turn, m.to_square) and not bb.is_attacked_by(not bb.turn, m.to_square) and b.piece_at(m.from_square).piece_type not in (chess.PAWN, chess.KING):
        give = ' Piesa se poate pierde, dar partida rămâne câștigată.'
    else: give = ''
    return f'{san}. Adversarul mai are o mutare, deci nu e pat.{give}{warn}'

av = []
av.append(kplace('P6_a', 'P6a', 'Unde e regele în pat?', 'Pe tablă lipsește un rege. Pune-l pe un pătrat unde, la mutare, nu e în șah și nu poate muta nimic.'))
av.append(nostale('P6_b', 'P6b', 'Evită patul', 'Adversarul mai are puține mutări. Ai grijă să nu-l lași fără nicio mutare când nu e în șah. Caută mutarea cea mai bună.', 'Joacă mutarea cea mai bună. Nu da pat!'))
if os.path.exists(os.path.join(HERE, 'sets', 'P6_c.json')):
    av.append(nostale('P6_c', 'P6c', 'Lasă-i o mutare', 'Adversarul nu are nicio mutare, dar e rândul tău, deci încă nu e pat. Mută așa încât să-i lași o mutare. Chiar dacă dai material, e bine cât timp poziția rămâne câștigată.', 'Joacă mutarea cea mai bună. Nu da pat!'))
if os.path.exists(os.path.join(HERE, 'sets', 'P6_d.json')):
    av.append(kplace('P6_d', 'P6d', 'Unde e regele în pat? (2)', 'Pe tablă lipsește un rege. Pune-l pe un pătrat unde, la mutare, nu e în șah și nu poate muta nimic.'))

SF.stdin.close()
DATA = dict(tabs=[dict(id='baza', title='De bază', sets=baza), dict(id='mediu', title='Mediu', sets=mediu), dict(id='avansat', title='Avansat', sets=av)])
open(OUT, 'w', encoding='utf-8').write('/* Exercițiile lecției „Patul”.\n   Surse: caietul Steps pasul 1, ChessKid lecția 4, Chess Tutor Step 1 (lecțiile 12 și P6).\n   Generat automat — nu edita de mână. */\nwindow.L17EX = ' + json.dumps(DATA, ensure_ascii=False) + ';\n')
tot = 0
for t in DATA['tabs']:
    print(t['title'], [(s['id'], len(s['tasks'])) for s in t['sets']]); tot += sum(len(s['tasks']) for s in t['sets'])
print('total', tot)
for e in ERR: print('ERR', e)
