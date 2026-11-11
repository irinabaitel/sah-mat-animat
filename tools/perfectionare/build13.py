# Construiește data/nivel1_lectia13_ex.js — lecția „Piese atârnate”
# Surse: Chess Tutor Step 1, lecțiile avansate P2 (P2c „Defending by moving away”, P2e „Defending: choose the correct capture”)
#        și P1 (P1c „Choose the correct capture”). Capturate cu run7.py în sets/P2c.json, P2e.json, P1c.json.
# Mutările la fel de bune sunt luate cu Stockfish (MultiPV); explicațiile sunt generate din poziție și verificate cu python-chess.
import json, os, sys, re, subprocess, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia13_ex.js'
HERE = os.path.dirname(os.path.abspath(__file__))
NAME = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
FEM = {chess.QUEEN}
VAL = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100}
RO_LET = {'K': 'R', 'Q': 'D', 'R': 'T', 'B': 'N', 'N': 'C'}
def ro_san(san): return ''.join(RO_LET.get(c, c) if c.isupper() else c for c in san)
def sqn(s): return chess.square_name(s)
def cap(s): return s[0].upper() + s[1:]
def g(pt, m, f): return f if pt in FEM else m          # acord: atacat / atacată
COL = {True: 'albul', False: 'negrul'}
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
send('uci'); wait('uciok'); send('setoption name MultiPV value 60'); send('isready'); wait('readyok')
def sf_scores(fen, depth=14):
    send('ucinewgame'); send('position fen ' + fen); send(f'go depth {depth}')
    res, pvs = {}, {}
    for l in wait('bestmove'):
        m = re.search(r' depth (\d+) .*multipv \d+ score (cp|mate) (-?\d+).* pv (.+)$', l)
        if m and int(m.group(1)) == depth:
            v = int(m.group(3)); mv = m.group(4).split()
            res[mv[0]] = v if m.group(2) == 'cp' else (100000 - abs(v)) * (1 if v > 0 else -1)
            pvs[mv[0]] = mv
    return res, pvs

def board_of(fen, white):
    b = chess.Board(None); b.set_board_fen(fen); b.turn = white; return b
def full(b): return b.board_fen() + (' w' if b.turn else ' b') + ' - - 0 1'
def diff_move(b, after):
    a = chess.Board(None); a.set_board_fen(after)
    for m in b.legal_moves:
        c = b.copy(); c.push(m)
        if c.board_fen() == a.board_fen(): return m
    return None

def pname(b, s):
    p = b.piece_at(s); return NAME[p.piece_type] + ' de pe ' + sqn(s)
def defenders(b, s, color):
    return [d for d in b.attackers(color, s)]
def hanging(b, s):
    """piesa de pe s e atacată de adversar și neapărată"""
    p = b.piece_at(s); return bool(b.attackers(not p.color, s)) and not b.attackers(p.color, s)

def reply_desc(b, m, pvs):
    """după mutarea greșită m: ce capturează adversarul (din linia Stockfish)"""
    c = b.copy(); c.push(m)
    pv = pvs.get(m.uci())
    if not pv or len(pv) < 2: return None, None
    r = chess.Move.from_uci(pv[1])
    if r not in c.legal_moves: return None, None
    if c.is_capture(r) and c.piece_at(r.to_square):
        t = c.piece_at(r.to_square)
        txt = f'{pname(c, r.from_square)} capturează {NAME[t.piece_type]} de pe {sqn(r.to_square)} ({ro_san(c.san(r))})'
        return txt, r.uci()
    c2 = c.copy(); c2.push(r)
    if c2.is_checkmate(): return f'urmează mat: {ro_san(c.san(r))}', r.uci()
    return None, None

def mk_task(fen, white, ans, kind, ct_text=''):
    b = board_of(fen, white)
    if ans not in b.legal_moves: ERR.append(('ans', fen, ans)); return None
    sc, pvs = sf_scores(full(b))
    best = max(sc.values())
    a = ans.uci()
    if a not in sc: ERR.append(('sf-missing', fen, a)); return None
    if sc[a] < best - 60: ERR.append(('ans-not-best', fen, ro_san(b.san(ans)), sc[a], best))
    okl = [u for u, v in sc.items() if u != a and v >= min(best, sc[a]) - 40]
    p = b.piece_at(ans.from_square); san = ro_san(b.san(ans))
    after = b.copy(); after.push(ans)
    t = dict(type='move', fen=full(b), side='w' if white else 'b', answer=a, san=san, ok=okl, check='best')
    bad = {}
    if kind == 'safe':                         # P2c: piesa atacată pleacă pe un pătrat sigur
        prot = [pname(after, d) for d in after.attackers(p.color, ans.to_square)]
        att = [d for d in b.attackers(not p.color, ans.from_square)]
        t['expl'] = (f'{cap(NAME[p.piece_type])} de pe {sqn(ans.from_square)} era {g(p.piece_type, "atacat", "atacată")} de {pname(b, att[0])} și nu {g(p.piece_type, "îl", "o")} apăra nimeni. '
                     f'Pe {sqn(ans.to_square)} e în siguranță: {g(p.piece_type, "îl", "o")} apără {" și ".join(prot)}.') if att and prot else None
        if not t['expl']: ERR.append(('safe-expl', fen, san)); t['expl'] = f'Corect! {san}: piesa e acum în siguranță.'
        for m in b.legal_moves:
            u = m.uci()
            if u == a or u in okl: continue
            c = b.copy(); c.push(m)
            if m.from_square == ans.from_square:
                at = list(c.attackers(not p.color, m.to_square))
                if at and not c.attackers(p.color, m.to_square):
                    bad[u] = [f'Pe {sqn(m.to_square)} {NAME[p.piece_type]} ar fi tot {g(p.piece_type, "atârnat", "atârnată")}: {g(p.piece_type, "îl", "o")} capturează {pname(c, at[0])}. Caută un pătrat unde e {g(p.piece_type, "apărat", "apărată")}.', sqn(at[0]) + sqn(m.to_square)]
                    continue
            rd, ru = reply_desc(b, m, pvs)
            if rd: bad[u] = [f'După {ro_san(b.san(m))}, {rd}. Mai încearcă!', ru]
        t['failmsg'] = f'{cap(NAME[p.piece_type])} de pe {sqn(ans.from_square)} e {g(p.piece_type, "atacat", "atacată")} și nu {g(p.piece_type, "îl", "o")} apără nimeni. Mută {g(p.piece_type, "-l", "-o")} pe un pătrat sigur.'.replace('Mută -l', 'Mută-l').replace('Mută -o', 'Mută-o')
    else:                                      # capturi: câștigă material (P1c) / apără-te (P2e)
        tp = b.piece_at(ans.to_square)
        if kind == 'win' and ct_text:
            t['expl'] = ct_text
        elif kind == 'win':
            if tp and hanging(b, ans.to_square):
                t['expl'] = f'{cap(NAME[tp.piece_type])} de pe {sqn(ans.to_square)} era {g(tp.piece_type, "atârnat", "atârnată")}: nu {g(tp.piece_type, "îl", "o")} apăra nimeni. {san} câștigă material.'
            elif tp and VAL[tp.piece_type] > VAL[p.piece_type]:
                t['expl'] = f'{cap(NAME[tp.piece_type])} valorează mai mult decât {NAME[p.piece_type]}. Chiar dacă adversarul recapturează, {san} câștigă material.'
            else:
                t['expl'] = f'{san} câștigă material.'
        else:
            t['expl'] = ct_text or f'{san}: nu pierzi nimic.'
        for m in b.legal_moves:
            u = m.uci()
            if u == a or u in okl or not b.is_capture(m): continue
            c = b.copy(); c.push(m)
            rd, ru = reply_desc(b, m, pvs)
            if rd: bad[u] = [f'După {ro_san(b.san(m))}, {rd}. Pierzi material. Mai încearcă!', ru]
            else: bad[u] = [f'{ro_san(b.san(m))} nu câștigă material. Caută altă captură.', None]
        t['failmsg'] = 'Nu este captura cea mai bună. Uită-te ce poate captura adversarul după mutarea ta.' if kind == 'def' else 'Caută o captură care câștigă material: o piesă neapărată sau una care valorează mai mult.'
    if bad: t['bad'] = bad
    return t

def load(n): return json.load(open(os.path.join(HERE, 'sets', n + '.json'), encoding='utf-8'))
def tasks_of(n, kind, texts=None):
    out = []
    for i, tk in enumerate(load(n)['tasks']):
        fb, fa = tk['before']['fen'], tk['after']['fen']
        # cine mută: încercăm ambele culori
        m = None
        for white in (True, False):
            b = board_of(fb, white)
            if b.is_valid() or True:
                mm = diff_move(b, fa)
                if mm: m = mm; side = white; break
        if not m: ERR.append(('nomove', n, i + 1)); continue
        t = mk_task(fb, side, m, kind, (texts or {}).get(i + 1, ''))
        if t: t['src'] = f'{n} #{i + 1}'; out.append(t)
    return out

# P2e: textele Chess Tutor, traduse
P2E_TXT = {
    1: 'Corect! Regina recapturează pe e3 și albul nu pierde nimic.',
    2: 'Corect! Calul capturează nebunul pe f5 și albul nu pierde nimic.',
    3: 'Corect! Regina capturează calul de pe f2. Albul nu pierde nimic.',
    4: 'Corect! Regina capturează pionul de pe h3 și după aceea negrul primește mat.',
    5: 'Corect! Calul capturează calul de pe c4 și albul nu pierde nimic.',
    6: 'Corect! Pionul capturează calul de pe g4: albul nu pierde material și nu primește mat.',
    7: 'Corect! Regina capturează turnul de pe d5 și negrul nu pierde nimic.',
    8: 'Corect! Regele capturează nebunul de pe f3 și albul nu pierde nimic.',
    9: 'Corect! Regina capturează calul de pe e5 și albul nu pierde nimic.',
    10: 'Corect! Regina capturează turnul de pe e5. Negrul nu pierde nimic și păzește în continuare pătratul a8.',
}

P1C_TXT = {
    3: 'Turnul de pe f6 e atacat de două piese albe (turnul de pe f1 și regina) și apărat de una singură (nebunul de pe e7). După Txf6 Nxf6 Dxf6, albul a câștigat un nebun.',
    6: 'Negrul capturează turnul de pe c3. Dacă regina albă recapturează (Dxc3), regina neagră capturează turnul de pe d1, care a rămas atârnat. Negrul câștigă un turn.',
    8: 'Calul capturează calul de pe e2, cu șah. Albul trebuie să recaptureze (Dxe2), iar apoi pionul de pe h6 capturează calul de pe g5. Negrul câștigă un cal.',
    9: 'Nebunul capturează calul de pe c6, cu șah. După bxc6, pionul de pe e5 capturează calul de pe f6 (exf6). Albul câștigă un cal.',
}

SETS = [
  ('baza', 'De bază', [dict(id='p2c', title='🏃 Mută piesa la loc sigur', src='Chess Tutor P2c',
      intro='O piesă a ta e <strong>atârnată</strong>: e atacată și nu o apără nimeni. Găsește-o și mut-o pe un pătrat unde e apărată.',
      instr='Mută piesa atârnată pe un pătrat sigur.', tasks=tasks_of('P2c', 'safe'))]),
  ('mediu', 'Mediu', [dict(id='p1c', title='🎯 Captura care câștigă material', src='Chess Tutor P1c',
      intro='Poți captura în mai multe feluri. Alege captura care <strong>câștigă material</strong>: o piesă atârnată sau o piesă care valorează mai mult decât cea cu care capturezi.',
      instr='Joacă captura care câștigă material.', tasks=tasks_of('P1c', 'win', P1C_TXT))]),
  ('avansat', 'Avansat', [dict(id='p2e', title='🛡️ Captura corectă când te aperi', src='Chess Tutor P2e',
      intro='Trebuie să capturezi o piesă a adversarului, dar se poate în mai multe feluri. Alege captura după care <strong>nu pierzi nimic</strong>.',
      instr='Alege captura după care nu pierzi material.', tasks=tasks_of('P2e', 'def', P2E_TXT))]),
]
data = dict(tabs=[dict(id=i, title=t, sets=s) for i, t, s in SETS])
open(OUT, 'w', encoding='utf-8').write('/* Exercițiile lecției „Piese atârnate”. Surse: Chess Tutor Step 1 (metoda Steps), lecțiile avansate P1 și P2.\n   Generat de tools/perfectionare/build13.py — nu edita de mână. */\nwindow.L13EX = ' + json.dumps(data, ensure_ascii=False) + ';\n')
print('scris', OUT, sum(len(s['tasks']) for _, _, ss in SETS for s in ss), 'sarcini')
for e in ERR: print('ERR', e)
SF.kill()
