# Builds data/nivel1_lectia5_ex.js from the Chess Tutor captures + ChessKid worksheets
import json, re, sys, chess
sys.stdout.reconfigure(encoding='utf-8')
S = 'sets/'
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia5_ex.js'

NAME = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
CAP = lambda s: s[0].upper() + s[1:]
RO_LET = {'K': 'R', 'Q': 'D', 'R': 'T', 'B': 'N', 'N': 'C'}
def ro_san(san):
    return ''.join(RO_LET.get(c, c) if i == 0 or san[i-1] in 'x=' and False else RO_LET.get(c, c) if c.isupper() and c in RO_LET else c for i, c in enumerate(san))

INDEF = {chess.KING: 'rege', chess.QUEEN: 'regină', chess.ROOK: 'un turn', chess.BISHOP: 'un nebun', chess.KNIGHT: 'un cal', chess.PAWN: 'un pion'}
def g(b, sq, w):  # agree adjective with piece gender
    return w + 'ă' if b.piece_at(sq).piece_type == chess.QUEEN else w
def load(name): return json.load(open(S + name + '.json', encoding='utf-8'))
def board(fen, side): return chess.Board(fen + ' ' + side + ' - - 0 1')
def nm(b, sq): return NAME[b.piece_at(sq).piece_type]
def side_word(side): return 'Albul' if side == 'w' else 'Negrul'

def attacked_targets(b, sq):
    """enemy pieces attacked by the piece on sq"""
    p = b.piece_at(sq)
    return [t for t in b.attacks(sq) if (q := b.piece_at(t)) and q.color != p.color and q.piece_type != chess.KING]

def defenders(b, sq):
    p = b.piece_at(sq); return list(b.attackers(p.color, sq))

def task_move(t, kind):
    a = t['answer']; side = a['side']; fen = t['before']['fen']
    b = board(fen, side); mv = chess.Move.from_uci(a['uci']); mover = nm(b, mv.from_square)
    cap = b.piece_at(mv.to_square)
    b2 = b.copy(); b2.push(mv)
    alts = []
    for san, v in (t.get('sf') or {}).get('alts', []):
        alts.append(b.parse_san(san).uci())
    if kind in ('attack', 'attackU'):
        tg = attacked_targets(b2, mv.to_square)
        if kind == 'attackU':
            tg = [x for x in tg if not b2.attackers(b2.piece_at(x).color, x)] or tg
        un = kind == 'attackU' and len(tg) == 1
        names = ' și '.join(nm(b2, x) + ((' ' + g(b2, x, 'neapărat')) if un else '') + ' de pe ' + chess.square_name(x) for x in tg)
        expl = f'{CAP(mover)} atacă {names}, iar pe {chess.square_name(mv.to_square)} nu poate fi {g(b2, mv.to_square, "capturat")}.'
    elif kind == 'capture':  # defending by capturing the attacker
        expl = f'{CAP(mover)} capturează atacatorul ({nm(b, mv.to_square)} de pe {chess.square_name(mv.to_square)}). Pericolul a trecut.'
    elif kind == 'away':
        d = [x for x in defenders(b2, mv.to_square)]
        expl = f'{CAP(mover)} fuge pe {chess.square_name(mv.to_square)}, unde nu mai poate fi {g(b2, mv.to_square, "capturat")}.'
        if kind == 'away' and d and t.get('set', '').startswith('L5e'):
            expl = f'{CAP(mover)} fuge pe {chess.square_name(mv.to_square)}. Acolo e {g(b2, mv.to_square, "apărat")} de ' + ' și '.join(INDEF[b2.piece_at(x).piece_type] for x in d) + '.'
    elif kind == 'protect':
        expl = None
    elif kind == 'block':
        expl = None
    elif kind == 'unprot':
        expl = f'{CAP(mover)} capturează {NAME[cap.piece_type]} de pe {chess.square_name(mv.to_square)}, care nu era {g(b, mv.to_square, "apărat")}. {side_word(side)} câștigă o piesă.'
    return dict(type='move', fen=fen + ' ' + side + ' - - 0 1', side=side, answer=a['uci'], san=ro_san(a['san']), alts=alts, check=kind, expl=expl)

EN_RO = [
    (r'^The knight is protected by the pawn\.$', 'Calul este apărat de pion.'),
    (r'^The bishop is protected by the pawn\.$', 'Nebunul este apărat de pion.'),
    (r'^The rook is protected by the knight\.$', 'Turnul este apărat de cal.'),
    (r'^The bishop is protected by the knight\.$', 'Nebunul este apărat de cal.'),
    (r'^The pawn on e4 is protected by the f-pawn\.$', 'Pionul de pe e4 este apărat de pionul f.'),
    (r'^The pawn on a7 is protected by the knight\.$', 'Pionul de pe a7 este apărat de cal.'),
    (r'^The knight is protected by the queen\.$', 'Calul este apărat de regină.'),
    (r'^The rook is protected by the queen\.$', 'Turnul este apărat de regină.'),
    (r'^The line of attack is cut off\. (.*)$', None),
]
BLOCK_RO = {
    'The bishop is protecting the pawn on e4.': 'Nebunul apără pionul de pe e4.',
    'The bishop on d4 is well protected.': 'Nebunul de pe d4 e bine apărat.',
    'The knight on d4 is well protected.': 'Calul de pe d4 e bine apărat.',
    'The pawn on a4 is protecting the queen.': 'Pionul de pe a4 apără regina.',
    'The pawn on b5 is protecting the pawn on c6.': 'Pionul de pe b5 apără pionul de pe c6.',
    'The pawn on b6 is protecting the knight.': 'Pionul de pe b6 apără calul.',
    'The pawn on f5 is protecting the pawn on e4.': 'Pionul de pe f5 apără pionul de pe e4.',
    'The pawn on h2 is protecting the pawn on g3.': 'Pionul de pe h2 apără pionul de pe g3.',
    'The pawns on c4 and e4 are protecting the knight.': 'Pionii de pe c4 și e4 apără calul.',
    'The rook on a5 is well protected.': 'Turnul de pe a5 e bine apărat.',
}
def tr(txt):
    for pat, ro in EN_RO:
        m = re.match(pat, txt)
        if m:
            if ro: return ro
            return 'Linia de atac e blocată. ' + BLOCK_RO[m.group(1)]
    raise KeyError(txt)
def prog_text(t):
    return [x for x in t['after']['texts'] if x not in t['before']['texts']][0]

def mk_set(id, title, src, intro, tasks, instr=None):
    return dict(id=id, title=title, src=src, intro=intro, instr=instr, tasks=tasks)

CT3 = 'Chess Tutor Step 1 · lecția 3'; CT5 = 'Chess Tutor Step 1 · lecția 5'
sets_mediu, sets_av, sets_baza = [], [], []

# ---------- MEDIU (Exercises) ----------
d = load('3a'); tasks = [task_move(t, 'attack') for t in d['tasks']]
sets_mediu.append(mk_set('3a', 'Atacă!', CT3, 'Atacă o piesă a adversarului. Ai grijă ca piesa ta să nu poată fi capturată: atacă din siguranță.', tasks, 'Atacă o piesă a adversarului.'))

d = load('L3x_b'); ag = json.load(open('agent_marks.json', encoding='utf-8'))
tasks = []
for t in d['tasks']:
    a = ag['L3x_b'][str(t['i'])]; frm = a['piece_square'][:2]
    b = board(t['before']['fen'], 'w'); side = 'w' if b.piece_at(chess.parse_square(frm)).color else 'b'
    tasks.append(dict(type='route', fen=t['before']['fen'] + f' {side} - - 0 1', side=side, from_=frm, target=a['target'], moves=2, mode='exact', route=a['route'],
                      expl=f'Drumul corect: {frm} → ' + ' → '.join(a['route']) + '.'))
sets_mediu.append(mk_set('3b', 'Drumul cel mai scurt, dar sigur', CT3, 'Mută doar piesa ta. Trebuie să ajungi pe pătratul marcat în <strong>două mutări</strong>. Pe drum nu ai voie pe pătrate nesigure și nu ai voie să capturezi nimic.', tasks, 'Du piesa pe pătratul marcat în două mutări.'))

d = load('L3x_c'); tasks = []
FIX_3c = {}  # c5 is a black bishop (reader saw a pawn)
for t in d['tasks']:
    q = t['before']['texts'][-1]; ans_txt = prog_text(t)
    sqs = list(dict.fromkeys(re.findall(r'\b([a-h][1-8])\b', re.split(r' (?:is|are) ', ans_txt)[0])))
    piece = re.search(r'black (bishop|knight|queen|rook)', q).group(1)
    sym = {'bishop': 'b', 'knight': 'n', 'queen': 'q', 'rook': 'r'}[piece]
    m = re.search(r'on (the [a-h]-file|the \w+ rank|the a1-h8 diagonal)', q); where = m.group(1) if m else 'corner square'
    RO_WHERE = {'the d-file': 'coloana d', 'the 5th rank': 'linia a 5-a', 'the 7th rank': 'linia a 7-a', 'the e-file': 'coloana e', 'the a1-h8 diagonal': 'diagonala a1–h8', 'the a-file': 'coloana a', 'the b-file': 'coloana b', 'the 1st rank': 'linia 1', 'corner square': 'pătratele din colțuri'}[where]
    many = len(sqs) > 1
    ro_piece = {'b': 'un nebun negru', 'n': 'un cal negru', 'q': 'regina neagră', 'r': 'un turn negru'}[sym]
    prompt = (f'Pe care pătrate de pe {RO_WHERE} ar sta în siguranță {ro_piece}? Atinge-le pe toate.' if many else
              (f'Pe care pătrat din colț ar sta în siguranță {ro_piece}?' if where == 'corner square' else f'Pe care pătrat de pe {RO_WHERE} ar sta în siguranță {ro_piece}?'))
    fen3 = t['before']['fen']
    if t['i'] in FIX_3c:
        bb = chess.Board(fen3 + ' w - - 0 1'); bb.set_piece_at(chess.C5, chess.Piece.from_symbol('b')); fen3 = bb.board_fen()
    tasks.append(dict(type='squares', fen=fen3 + ' w - - 0 1', piece=sym, answers=sqs, prompt=prompt,
                      expl=(' și '.join(sqs) + (' sunt pătrate sigure.' if many else ' este pătratul sigur.'))))
sets_mediu.append(mk_set('3c', 'Pătrate sigure', CT3, 'Găsește pătratul pe care o piesă neagră nu poate fi capturată de piesele albe.', tasks))

d = load('L3x_d'); tasks = []
for t in d['tasks']:
    a = ag['L3x_d'][str(t['i'])]; frm = a['piece_square'][:2]
    b = board(t['before']['fen'], 'w'); side = 'w' if b.piece_at(chess.parse_square(frm)).color else 'b'
    tasks.append(dict(type='route', fen=t['before']['fen'] + f' {side} - - 0 1', side=side, from_=frm, target=a['target'], moves=5, mode='min', route=a['route'],
                      expl=f'Un drum posibil în {len(a["route"])} mutări: {frm} → ' + ' → '.join(a['route']) + '.'))
sets_mediu.append(mk_set('3d', 'Drum lung, numai pe pătrate sigure', CT3, 'Du piesa pe pătratul marcat. Reguli: nu ai voie pe pătrate nesigure, nu ai voie să capturezi, nu ai voie de două ori pe același pătrat și trebuie să faci <strong>cel puțin cinci mutări</strong>.', tasks, 'Du piesa pe pătratul marcat în cel puțin cinci mutări.'))

d = load('L3x_e'); tasks = []
for t in d['tasks']:
    a = ag['L3x_e'][str(t['i'])]
    sol = {}
    for m in a['solution'].split(','):
        m = m.strip(); sol[m[1:3]] = m[0]
    tasks.append(dict(type='place', numbers=a['numbers'], boxes=a['boxes'], solution=sol,
                      expl='Piesele stau corect: ' + ', '.join({'R': 'turnul', 'B': 'nebunul', 'N': 'calul'}[p] + ' pe ' + s for s, p in sol.items()) + '.'))
sets_mediu.append(mk_set('3e', 'Unde stau piesele?', CT3, 'Pune turnul, nebunul și calul pe pătratele marcate. Cifra de pe un pătrat îți spune <strong>de câte ori este atacat</strong> acel pătrat. Cu ajutorul ei afli care piesă unde stă.', tasks, 'Așază piesele pe pătratele marcate.'))

d = load('L5x_a'); tasks = [task_move(t, 'attackU') for t in d['tasks']]
sets_mediu.append(mk_set('5a', 'Atacă piesa potrivită', CT5, 'Pe tablă e o singură piesă care poate ataca. Atacă cu ea o piesă a adversarului care <strong>nu este apărată</strong>. Atacul trebuie să fie sigur: piesa ta trebuie să stea pe un pătrat unde nu poate fi capturată.', tasks, 'Atacă din siguranță o piesă neapărată.'))
d = load('L5x_b'); tasks = []
for t in d['tasks']:
    x = task_move(t, 'capture'); tasks.append(x)
sets_mediu.append(mk_set('5b', 'Apără-te capturând', CT5, 'O piesă e în pericol. Apărarea corectă: <strong>capturezi atacatorul</strong>, fie cu piesa atacată, fie cu altă piesă.', tasks, 'Joacă cea mai bună mutare.'))
d = load('L5x_c'); tasks = [task_move(t, 'away') for t in d['tasks']]
sets_mediu.append(mk_set('5c', 'Apără-te fugind', CT5, 'O piesă e atacată. <strong>Mut-o pe un pătrat sigur.</strong>', tasks, 'Joacă cea mai bună mutare.'))
d = load('L5x_d'); tasks = []
for t in d['tasks']:
    x = task_move(t, 'protect'); x['expl'] = tr(prog_text(t)); tasks.append(x)
sets_mediu.append(mk_set('5d', 'Apără-te protejând', CT5, 'O piesă e atacată. Altă piesă vine în ajutor și <strong>o apără</strong>.', tasks, 'Joacă cea mai bună mutare.'))
d = load('L5x_e'); tasks = [task_move(t, 'unprot') for t in d['tasks']]
sets_mediu.append(mk_set('5e', 'Capturează piesa neapărată', CT5, 'Uită-te la toate capturile posibile. Verifică dacă piesa pe care o poți captura este apărată sau nu. <strong>Capturează piesa neapărată.</strong>', tasks, 'Joacă cea mai bună mutare.'))

# ---------- AVANSAT (Extra exercises) ----------
for sid, title, intro in (('L3e_a', 'Mutări sigure și nesigure', 'Pentru piesa indicată, găsește <strong>toate mutările sigure</strong> (pe pătrate unde nu poate fi capturată).'),
                          ('L3e_b', 'Mutări sigure și nesigure, cu capturi', 'La fel ca înainte, dar acum socotești și capturile: o captură e bună doar dacă piesa ta nu poate fi capturată înapoi.')):
    d = load(sid); tasks = []
    for t in d['tasks']:
        b = board(t['before']['fen'], 'w'); sq = chess.parse_square(t['piece'])
        p = b.piece_at(sq); col = 'albă' if p.color else 'neagră'
        pn = NAME[p.piece_type]
        tasks.append(dict(type='marks', fen=t['before']['fen'] + (' w' if p.color else ' b') + ' - - 0 1', piece=t['piece'], safe=t['safe'], unsafe=t['unsafe'],
                          prompt=f'Unde poate muta în siguranță {pn} de pe {t["piece"]}? Atinge toate pătratele sigure.',
                          expl='Mutări sigure: ' + ', '.join(t['safe']) + '. Nesigure: ' + ', '.join(t['unsafe']) + '.'))
    sets_av.append(mk_set(sid[-1] if False else sid, title, 'Chess Tutor Step 1 · lecția 3 (extra)', intro, tasks))

d = load('L3e_c'); tasks = []
FIX_C = {8: 'd5', 9: 'f2'}
for t in d['tasks']:
    a = ag['L3e_c'][str(t['i'])]; ans = FIX_C.get(t['i'], a['answer_square_shown'])
    tasks.append(dict(type='nocircle', circles=a['circles'], answer=ans, options=sorted(a['circles'] + [ans]), expl=f'Pe {ans} nu este niciun cerc.'))
sets_av.append(mk_set('L3e_c', 'Unde nu e cerc?', 'Chess Tutor Step 1 · lecția 3 (extra)', 'Pe tablă sunt trei cercuri, fără litere și cifre pe margine. Care dintre cele patru pătrate <strong>nu</strong> are cerc?', tasks))
d = load('L3e_d'); tasks = []
for t in d['tasks']:
    sq = re.search(r'square ([a-h][1-8])', t['before']['texts'][-1]).group(1)
    tasks.append(dict(type='clicksq', answer=sq, prompt=f'Atinge pătratul {sq}.', expl=f'Acesta este pătratul {sq}.'))
sets_av.append(mk_set('L3e_d', 'Găsește pătratul', 'Chess Tutor Step 1 · lecția 3 (extra)', 'Tabla nu are litere și cifre pe margine. Atinge pătratul cerut.', tasks))

d = load('L5e_a'); tasks = []
for t in d['tasks']:
    t['set'] = 'L5e_a'; x = task_move(t, 'away'); tasks.append(x)
sets_av.append(mk_set('L5e_a', 'Fugi pe un pătrat apărat', 'Chess Tutor Step 1 · lecția 5 (extra)', 'O piesă e atacată. Mut-o pe un pătrat sigur: pătratul e sigur pentru că acolo piesa ta <strong>este apărată</strong>.', tasks, 'Joacă cea mai bună mutare.'))
d = load('L5e_b'); tasks = []
for t in d['tasks']:
    x = task_move(t, 'block'); x['expl'] = tr(prog_text(t)); tasks.append(x)
sets_av.append(mk_set('L5e_b', 'Apără-te blocând', 'Chess Tutor Step 1 · lecția 5 (extra)', 'O piesă e atacată. Altă piesă îi vine în ajutor <strong>punându-se în calea atacului</strong>. Dar piesa care blochează trebuie să fie apărată.', tasks, 'Joacă cea mai bună mutare.'))
d = load('L5e_c'); tasks = [task_move(t, 'unprot') for t in d['tasks']]
sets_av.append(mk_set('L5e_c', 'Capturează piesa neapărată (2)', 'Chess Tutor Step 1 · lecția 5 (extra)', 'Uită-te la toate capturile posibile. <strong>Capturează piesa neapărată.</strong>', tasks, 'Joacă cea mai bună mutare.'))
tasks = []
for i in range(1, 11):
    a = ag['L5e_d'][str(i)]
    tasks.append(dict(type='namesq', cross=a['cross'], options=a['options'], expl=f'Pătratul cu cruce este {a["cross"]}.'))
sets_av.append(mk_set('L5e_d', 'Cum se numește pătratul? (tabla întoarsă)', 'Chess Tutor Step 1 · lecția 5 (extra)', 'Tabla este întoarsă: o vezi din partea negrului și nu are litere și cifre pe margine. Cum se numește pătratul cu cruce?', tasks))

# ---------- DE BAZĂ (ChessKid) ----------
H = [('r5k1/2q1ppbp/p2r2p1/1p2n3/8/1QN3P1/PP2PPBP/R4RK1', 'g2a8', 'Turnul de pe a8 nu e apărat: nebunul de pe g2 îl capturează.'),
     ('r5k1/6n1/2pr3p/pp2p1p1/4P3/3PKNP1/1P4P1/R1R5', 'f3e5', 'Pionul de pe e5 nu e apărat: calul de pe f3 îl capturează.'),
     ('r1bqr1k1/pp3ppp/2p2nn1/2bpp3/4P3/1B1PBNNP/PPP2PP1/R2QR1K1', 'e3c5', 'Nebunul de pe c5 nu e apărat: nebunul de pe e3 îl capturează.'),
     ('q1b2rk1/4bppp/2npp3/1p6/3NP1n1/1PN1B3/1PP1BPPP/R2Q2K1', 'a1a8', 'Regina de pe a8 nu e apărată: turnul de pe a1 o capturează.')]
tasks = []
for f, u, e in H:
    b = board(f, 'w'); mv = chess.Move.from_uci(u)
    tasks.append(dict(type='move', fen=f + ' w - - 0 1', side='w', answer=u, san=ro_san(b.san(mv)), alts=[], check='hanging', expl=e))
sets_baza.append(mk_set('ck_hang', 'Cine e neapărat?', 'ChessKid · lecția 5', 'Negrul are o piesă <strong>neapărată</strong>: dacă o capturezi, nimeni nu o poate recaptura. Găsește-o și captureaz-o.', tasks, 'Capturează piesa neagră neapărată.'))
D = [('1r4k1/2q1ppbp/3r2p1/1ppPn3/8/P1N5/1PQ2PPP/R3RBK1', 'e5', True, 'g7', 'Da. Calul de pe e5 este apărat de nebunul de pe g7.'),
     ('6k1/2b3np/8/pp2p3/4P3/3P1N2/5K2/6R1', 'g7', True, 'g8', 'Da. Calul de pe g7 este apărat de regele de pe g8.'),
     ('r6k/r6p/7n/2b1p3/1p2P3/1B3N1P/PPP2PP1/2BR2K1', 'h6', False, None, 'Nu. Calul de pe h6 nu este apărat de nicio piesă neagră.'),
     ('r1bq1rk1/pppp1ppp/2n5/2b1p1Nn/2B1P3/2PP4/PP3PPP/RNBQK2R', 'h5', False, None, 'Nu. Calul de pe h5 nu este apărat de nicio piesă neagră.')]
tasks = [dict(type='yesno', fen=f + ' w - - 0 1', sq=sq, answer=ans, defender=dfn, prompt=f'Calul negru de pe {sq} este atacat. Este și apărat?', expl=e) for f, sq, ans, dfn, e in D]
sets_baza.append(mk_set('ck_def', 'E apărat calul?', 'ChessKid · lecția 5', 'Calul negru este atacat. Uită-te bine: îl apără vreo piesă neagră?', tasks))

DATA = dict(tabs=[dict(id='baza', title='De bază', sets=sets_baza), dict(id='mediu', title='Mediu', sets=sets_mediu), dict(id='avansat', title='Avansat', sets=sets_av)])
# rename from_ -> from
js = json.dumps(DATA, ensure_ascii=False).replace('"from_"', '"from"')
open(OUT, 'w', encoding='utf-8').write('/* Exercițiile lecției „Atacul, captura, apărarea”.\n   Surse: Chess Tutor Step 1 (metoda Steps, lecțiile 3 și 5) și ChessKid (lecția 5).\n   Generat automat — nu edita de mână. */\nwindow.L5EX = ' + js + ';\n')
n = sum(len(s['tasks']) for tb in DATA['tabs'] for s in tb['sets'])
print('tasks', n, [(tb['id'], len(tb['sets'])) for tb in DATA['tabs']])
for tb in DATA['tabs']:
    for s in tb['sets']:
        for t in s['tasks'][:2]:
            print(s['id'], t.get('san', ''), '|', t.get('expl'))
