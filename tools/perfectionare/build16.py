# Builds data/nivel1_lectia16_ex.js — lecția „Apărarea împotriva matului”
# Surse: Chess Tutor Step 2 lecția 12 (sets/S2_12*), caietul Steps pasul 2 foile „Defending against mate” A și B (wb/defmate_*.json).
import json, os, sys, re, subprocess, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia16_ex.js'
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
NAME_EN = {'king': 'regele', 'queen': 'regina', 'rook': 'turnul', 'bishop': 'nebunul', 'knight': 'calul', 'pawn': 'pionul'}
RO_LET = {'K': 'R', 'Q': 'D', 'R': 'T', 'B': 'N', 'N': 'C'}
CAP = lambda s: s[0].upper() + s[1:]
def ro_san(san): return ''.join(RO_LET.get(c, c) if c.isupper() else c for c in san)
def sqn(s): return chess.square_name(s)
ERR = []

# ── Stockfish: mutările la fel de bune ca răspunsul ──
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
def sf_scores(fen, depth=14):
    send('ucinewgame'); send('position fen ' + fen); send(f'go depth {depth}')
    res = {}
    for l in wait('bestmove'):
        m = re.search(r' depth (\d+) .*multipv \d+ score (cp|mate) (-?\d+).* pv (\S+)', l)
        if m and int(m.group(1)) == depth:
            v = int(m.group(3)); res[m.group(4)] = v if m.group(2) == 'cp' else (100000 - abs(v)) * (1 if v > 0 else -1)
    return res

# ── mat fără să ceară ambii regi ──
def board(fen, side):
    b = chess.Board(None); b.set_board_fen(fen.split(' ')[0]); b.turn = side == 'w'; return b
def safe_after(b, m):
    bb = b.copy(stack=False); bb.push(m); k = bb.king(not bb.turn)
    return k is None or not bb.is_attacked_by(bb.turn, k)
def moves(b): return [m for m in b.pseudo_legal_moves if not b.is_castling(m) and safe_after(b, m)]
def mated(b):
    k = b.king(b.turn)
    return k is not None and b.is_attacked_by(not b.turn, k) and not moves(b)
def mates(b):
    out = []
    for m in moves(b):
        bb = b.copy(stack=False); bb.push(m)
        if mated(bb): out.append(m)
    return out
def mate2(b):  # b.turn = cel care amenință
    for m in moves(b):
        bb = b.copy(stack=False); bb.push(m)
        rs = moves(bb)
        if not rs: continue
        if all(mates((lambda x: (x.push(r), x)[1])(bb.copy(stack=False))) for r in rs): return m
    return None
def threats(fen, side):
    b = board(fen, 'b' if side == 'w' else 'w'); return mates(b)

def ct_line(t):  # textele de după răspuns din Chess Tutor, traduse
    tx = ' '.join(t['after']['texts'])
    out = []
    m = re.search(r'The (king|queen|rook|bishop|knight|pawn) can interpose on ([a-h][1-8])', tx)
    if m: out.append(f'Dacă adversarul dă șah, {NAME_EN[m.group(1)]} se poate pune în cale pe {m.group(2)}.')
    if 'exchanges queens' in tx: out.append('Reginele se schimbă.')
    if 'takes over the attack' in tx: out.append('Acum atacă negrul.')
    if 'can no longer deliver mate' in tx: out.append('Regina nu mai poate da mat.')
    if 'The only move' in tx: out.append('Este singura mutare bună.')
    return ' '.join(out)

PROMO = {chess.QUEEN: 'regină', chess.ROOK: 'turn', chess.BISHOP: 'nebun', chess.KNIGHT: 'cal'}
def gen(pt, w): return w + ('ă' if pt == chess.QUEEN else '')
def why_not(b):  # b.turn = apărătorul, în șah: de ce nu e mat
    k = b.king(b.turn); ch = list(b.attackers(not b.turn, k)) if k is not None else []
    mv = moves(b)
    run = [m for m in mv if m.from_square == k and not b.piece_at(m.to_square)]
    if run: return f'regele ar putea pleca pe {sqn(run[0].to_square)}'
    cap = [m for m in mv if m.to_square in ch]
    if cap:
        m = cap[0]; p = b.piece_at(m.from_square); c = b.piece_at(m.to_square)
        col = ('alb' if c.color else 'negru') if c.piece_type != chess.QUEEN else ('albă' if c.color else 'neagră')
        who = 'regele' if p.piece_type == chess.KING else f'{NAME[p.piece_type]} de pe {sqn(m.from_square)}'
        return f'{who} ar captura {NAME[c.piece_type]} {col}'
    if mv:
        m = mv[0]; p = b.piece_at(m.from_square)
        if p.piece_type == chess.KING: return f'regele ar pleca pe {sqn(m.to_square)}'
        return f'{NAME[p.piece_type]} s-ar pune în cale pe {sqn(m.to_square)}'
    return None
def expl_def(fen, side, uci, thr):
    b = board(fen, side); m = chess.Move.from_uci(uci); p = b.piece_at(m.from_square); to = m.to_square
    who = CAP(NAME[p.piece_type]); cap = b.piece_at(to)
    bb = b.copy(stack=False); bb.push(m)
    chk = bb.is_check()
    tsq = sorted({t.to_square for t in thr})
    if m.promotion:
        s = f'Pionul se transformă în {PROMO[m.promotion]}' + (' și dă șah.' if chk else '.')
    elif cap:
        s = f'{who} capturează {NAME[cap.piece_type]} de pe {sqn(to)}' + (' și dă șah.' if chk else '.')
    elif p.piece_type == chess.KING:
        s = f'Regele pleacă pe {sqn(to)}.'
    elif chk:
        s = f'{who} dă șah de pe {sqn(to)}.'
    elif any(q in bb.attacks(to) for q in tsq):
        q = next(q for q in tsq if q in bb.attacks(to))
        s = f'{who} apără acum pătratul {sqn(q)}.'
    elif any(to in chess.SquareSet(chess.between(t.from_square, t.to_square)) for t in thr):
        s = f'{who} se pune în cale pe {sqn(to)}.'
    elif p.piece_type == chess.PAWN:
        s = f'Pionul înaintează pe {sqn(to)}.'
    else:
        s = f'{who} se mută pe {sqn(to)}.'
    pre = ''
    if not thr and not b.is_check() and mate2(board(fen, 'b' if side == 'w' else 'w')):
        pre = 'Adversarul amenința mat în două mutări. '
    if thr:
        tb = board(fen, 'b' if side == 'w' else 'w'); t0 = thr[0]
        pre = f'Adversarul amenința {ro_san(tb.san(t0)).rstrip("#")} mat. '
        # de ce nu mai merge amenințarea după mutarea ta
        if not chk and t0 in bb.pseudo_legal_moves and safe_after(bb, t0):
            b3 = bb.copy(stack=False); b3.push(t0)
            if b3.is_check():
                w = why_not(b3)
                if w: s += f' Acum, după {ro_san(bb.san(t0)).rstrip("#")}, {w}.'
    return pre + s

EXPL_FIX = {  # amenințări de mat în două mutări, explicate de mână
    'A4': 'Albul amenința să captureze turnul de pe a8 și apoi să atace regele pe ultima linie. De pe d8, regina apără ultima linie și se oferă la schimb.',
    'A7': 'Negrul amenința Dd1+ și apoi mat pe prima linie. Turnul vine pe e1 și apără prima linie.',
    'S2_12a#3': 'Albul amenința Tf8+ Dxf8 Txf8 mat. De pe g8, regele apără pătratul f8.',
}
def def_task(fen, side, answer, src, extra='', prompt=None, badmsg=None, need_threat=True):
    b = board(fen, side)
    if b.king(chess.WHITE) is None or b.king(chess.BLACK) is None: ERR.append(('kings', src)); return None
    thr = threats(fen, side)
    if not thr and not b.is_check():
        m2 = mate2(board(fen, 'b' if side == 'w' else 'w'))
        if m2 is None: ERR.append(('no-threat', src, fen, side))
        badmsg = badmsg or 'Nu este apărarea cea bună. Adversarul nu dă mat imediat, dar îți poate da mat în două mutări. Uită-te cum.'
    m = chess.Move.from_uci(answer)
    if m not in moves(b): ERR.append(('illegal', src, fen, answer)); return None
    bb = b.copy(stack=False); bb.push(m)
    if mates(bb): ERR.append(('answer-allows-mate', src, fen, answer, [x.uci() for x in mates(bb)]))
    full = fen.split(' ')[0] + f' {side} - - 0 1'
    sc = sf_scores(full)
    ans = sc.get(answer)
    best = max(sc.values()) if sc else None
    ok = []
    for u, v in sc.items():
        if u == answer: continue
        mm = chess.Move.from_uci(u); b2 = b.copy(stack=False); b2.push(mm)
        if mates(b2): continue
        if v >= (ans if ans is not None else best) - 50 and v >= best - 80: ok.append(u)
    if ans is not None and best is not None and ans < best - 150: ERR.append(('sf-prefers', src, fen, answer, ans, max(sc, key=sc.get), best))
    e = EXPL_FIX.get(src) or expl_def(fen, side, answer, thr)
    if extra:
        mm = re.search(r'în cale pe ([a-h][1-8])', extra)
        if not (mm and f's-ar pune în cale pe {mm.group(1)}' in e): e += ' ' + extra
    t = dict(type='move', check='defmate', fen=full, side=side, answer=answer, san=ro_san(b.san(m)), ok=ok, expl=e)
    if prompt: t['prompt'] = prompt
    if badmsg: t['badmsg'] = badmsg
    return t

def mk_set(id, title, src, intro, tasks, instr=None):
    return dict(id=id, title=title, src=src, intro=intro, instr=instr, tasks=[t for t in tasks if t])
def load(n): return json.load(open(os.path.join(HERE, 'sets', n + '.json'), encoding='utf-8'))
def fpos(fen):
    b = chess.Board(None); b.set_board_fen(fen); return {sqn(s): p.symbol() for s, p in b.piece_map().items()}
def ct_move(t):
    """mutarea din Chess Tutor: caută mutarea legală care duce cel mai aproape de captura „după”."""
    a, z = fpos(t['before']['fen']), fpos(t['after']['fen'])
    best = None
    for side in 'wb':
        b = board(t['before']['fen'], side)
        for m in moves(b):
            bb = b.copy(stack=False); bb.push(m)
            r = {sqn(q): p.symbol() for q, p in bb.piece_map().items()}
            d = sum(1 for q in set(r) | set(z) if r.get(q) != z.get(q))
            if best is None or d < best[0]: best = (d, side, m.uci())
    # rocada nu e în motorul paginii: o căutăm separat
    for side, k, r, kt, rt in (('w', 'e1', 'h1', 'g1', 'f1'), ('w', 'e1', 'a1', 'c1', 'd1'), ('b', 'e8', 'h8', 'g8', 'f8'), ('b', 'e8', 'a8', 'c8', 'd8')):
        K = 'K' if side == 'w' else 'k'
        if a.get(k) == K and z.get(kt) == K and k not in z:
            ERR.append(('castling', t['i'])); return None, None
    if best and best[0] <= 1: return best[1], best[2]
    ERR.append(('ct-diff', t['i'], best)); return None, None
CT_FIX = {  # Chess Tutor joacă aici o serie: șah, răspuns, captură. Exercițiul cere prima mutare.
    ('S2_12c', 2): ('w', 'a7a8', 'După Rh7, regina capturează pionul de pe f3 (Dxf3) și matul dispare.'),
    ('S2_12c', 8): ('w', 'f2h1', 'Calul pleacă și deschide coloana f: turnul de pe f1 dă șah. După mutarea regelui, calul capturează regina de pe g3.'),
}
def ct_set(sid, id, title, src, intro, instr):
    tasks = []
    for t in load(sid)['tasks']:
        if (sid, t['i']) in CT_FIX:
            side, u, ex = CT_FIX[(sid, t['i'])]
            tasks.append(def_task(t['before']['fen'], side, u, f'{sid}#{t["i"]}', ex)); continue
        side, u = ct_move(t)
        if side: tasks.append(def_task(t['before']['fen'], side, u, f'{sid}#{t["i"]}', ct_line(t)))
    return mk_set(id, title, src, intro, tasks, instr)

CT = 'Chess Tutor Step 2 · lecția 12'
I_DEF = 'Adversarul amenință mat. Apără-te fără să pierzi material.'
baza, mediu, av = [], [], []

# ═════════ MEDIU: Chess Tutor ═════════
mediu.append(ct_set('S2_12a', '12a', 'Protejezi pătratul', CT, 'Adversarul amenință mat. Caută pătratul unde ar veni matul. Îl poți apăra fără să pierzi material?', I_DEF))
mediu.append(ct_set('S2_12b', '12b', 'Regele pleacă', CT, 'Adversarul amenință mat. Poate regele să plece din timp? Sau îi poți face loc, ca să aibă unde pleca?', I_DEF))
mediu.append(ct_set('S2_12c', '12c', 'Capturezi un atacator', CT, 'Adversarul amenință mat. Poți captura una dintre piesele care lucrează la mat: pe cea care ar da șah, pe cea care o apără sau pe cea care păzește pătratele regelui.', I_DEF))
mediu.append(ct_set('S2_12d', '12d', 'Te pui în cale', CT, 'Adversarul amenință mat. Aici te salvează o piesă pusă în cale.', I_DEF))

# ═════════ AVANSAT: Chess Tutor extra ═════════
av.append(ct_set('S2_12xa', '12xa', 'Toate apărările', CT, 'Adversarul amenință mat. Te poți apăra protejând, capturând, punând o piesă în cale sau plecând cu regele.', I_DEF))
av.append(ct_set('S2_12xb', '12xb', 'Ieși din șah fără să primești mat', CT, 'Regele tău e în șah. Cum iese din șah? Ai grijă: după mutarea ta, adversarul nu trebuie să poată da mat. Gândește-te la toate variantele și abia apoi mută.', 'Ieși din șah așa încât adversarul să nu-ți poată da mat.'))

# ═════════ DE BAZĂ: caietul Steps pasul 2 ═════════
WB = 'Steps · caietul pasului 2'
A = json.load(open(os.path.join(HERE, 'wb', 'defmate_A.json'), encoding='utf-8'))
ta = []
for e in A:
    if not e['src'].startswith('A') or not e['fen']: continue
    bad = None
    if e['src'] in ('A4', 'A7'): bad = 'Nu este apărarea cea bună. Adversarul nu dă mat imediat, dar îți poate da mat în două mutări. Uită-te cum.'
    ta.append(def_task(e['fen'], e['side'], e['key'], e['src'], badmsg=bad, need_threat=e['src'] not in ('A4', 'A7')))
baza.append(mk_set('wbA', 'Apără-te de mat', WB, 'Adversarul amenință mat. Cu mutarea potrivită oprești matul. Nu pierde material fără rost.', ta, I_DEF))

B = json.load(open(os.path.join(HERE, 'wb', 'defmate_B.json'), encoding='utf-8'))
NO_EXPL = {
  'B1': 'Nu. Albul amenință Th7 mat. Doar Ta7 îl oprește, dar după Txa7 matul vine la mutarea următoare.',
  'B4': 'Nu. Albul amenință Da7 mat. Mutările care îl opresc dau regina, iar albul dă mat oricum, puțin mai târziu.',
  'B5': 'Nu. Negrul amenință De1 mat. Nicio mutare nu oprește matul de tot: cel mult îl amână cu o mutare.',
  'B8': 'Nu. Albul amenință mat cu Cf7 și cu Cg6. Orice ar muta negrul, unul dintre ele rămâne.',
  'B11': 'Nu. Negrul amenință Tc2 mat și nicio mutare nu îl oprește.',
  'B12': 'Nu. Negrul amenință Db2 mat și nicio mutare nu îl oprește.',
}
YES_EXTRA = {}
tb = []
for e in B:
    full = e['fen'] + f" {e['side']} - - 0 1"
    thr = threats(e['fen'], e['side'])
    if not thr: ERR.append(('B-no-threat', e['src']))
    q = dict(type='defq', fen=full, side=e['side'], prompt='Adversarul amenință mat. Te poți apăra fără să pierzi material?', threat=[thr[0].uci()] if thr else [])
    if e['answer'] == 'no':
        q.update(answer=False, expl=NO_EXPL[e['src']])
    else:
        t = def_task(e['fen'], e['side'], e['answer'], e['src'], YES_EXTRA.get(e['src'], ''))
        if not t: continue
        q.update(answer=True, move=t['answer'], san=t['san'], ok=t['ok'], expl=t['expl'])
    tb.append(q)
baza.append(mk_set('wbB', 'Există apărare?', WB, 'Adversarul amenință mat. Uneori există o apărare, alteori nu. Răspunde întâi cu Da sau Nu. Dacă alegi „Da”, joacă apoi mutarea.', tb))

SF.stdin.close()
DATA = dict(tabs=[dict(id='baza', title='De bază', sets=baza), dict(id='mediu', title='Mediu', sets=mediu), dict(id='avansat', title='Avansat', sets=av)])
open(OUT, 'w', encoding='utf-8').write('/* Exercițiile lecției „Apărarea împotriva matului”.\n   Surse: Chess Tutor Step 2 (metoda Steps, lecția 12), caietul Steps pasul 2.\n   Generat automat — nu edita de mână. */\nwindow.L16EX = ' + json.dumps(DATA, ensure_ascii=False) + ';\n')
tot = 0
for t in DATA['tabs']:
    print(t['title'], [(s['id'], len(s['tasks'])) for s in t['sets']]); tot += sum(len(s['tasks']) for s in t['sets'])
print('total', tot)
for e in ERR: print('ERR', e)
