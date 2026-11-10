# Reface data/nivel1_lectia3_ex.js: exercițiile vechi + cele noi, pe 3 niveluri, cu comentarii mai bogate.
import json, chess, sys, re
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:/Users/irina/SahMatAnimat/'
s = open(ROOT + 'data/nivel1_lectia3_ex.js', encoding='utf-8').read()
J = json.loads(s[s.index('{'):s.rindex('}') + 1])
SETS = {st['id']: st for t in J['tabs'] for st in t['sets']}

NAME = {chess.KING: 'regele', chess.QUEEN: 'regina', chess.ROOK: 'turnul', chess.BISHOP: 'nebunul', chess.KNIGHT: 'calul', chess.PAWN: 'pionul'}
COLN = {True: 'Albul', False: 'Negrul'}
SIDE = {'k': 'mică', 'q': 'mare'}

def sq(n): return chess.parse_square(n)
def nm(b, s_): return NAME[b.piece_at(s_).piece_type] + ' de pe ' + chess.square_name(s_)

def castle_info(fen, white, side):
    """Analiza rocadei pe baza pozițiilor pieselor. Întoarce (motive_care_opresc, note, arată)."""
    b = chess.Board(fen)
    r = '1' if white else '8'
    K, R = 'e' + r, ('h' if side == 'k' else 'a') + r
    pas, dst = ('f' if side == 'k' else 'd') + r, ('g' if side == 'k' else 'c') + r
    btw = (['f', 'g'] if side == 'k' else ['b', 'c', 'd'])
    opp = not white
    def att(x): return list(b.attackers(opp, sq(x)))
    bad, notes, show = [], [], {'red': [], 'arrows': []}
    kp, rp = b.piece_at(sq(K)), b.piece_at(sq(R))
    if not (kp and kp.piece_type == chess.KING and kp.color == white):
        bad.append(('moved', 'Regele a mutat deja: nu mai stă pe ' + K + ', pătratul lui de la începutul partidei. Un rege care a mutat o dată nu mai are voie să facă rocada.'))
        return bad, notes, show
    if not (rp and rp.piece_type == chess.ROOK and rp.color == white):
        bad.append(('moved', 'Turnul a mutat deja: în colțul ' + R + ' nu mai stă turnul de la început. Rocada se face numai cu un turn care nu a mutat.'))
        show['red'].append(R)
    if att(K):
        a = att(K)[0]
        bad.append(('check', 'Regele este în șah: îl atacă ' + nm(b, a) + '. Când regele este în șah, rocada nu este permisă.'))
        show['red'].append(K); show['arrows'].append([chess.square_name(a), K, 'r'])
    blk = [f + r for f in btw if b.piece_at(sq(f + r))]
    if blk and rp and rp.piece_type == chess.ROOK and rp.color == white:
        bad.append(('block', 'Între rege și turn stă ' + nm(b, sq(blk[0])) + '. Pătratele dintre rege și turn trebuie să fie libere.'))
        show['red'].append(blk[0])
    if att(pas):
        a = att(pas)[0]
        bad.append(('pass', 'Regele ar trece prin ' + pas + ', iar acolo atacă ' + nm(b, a) + '. Regele nu are voie să treacă printr-un pătrat atacat.'))
        show['red'].append(pas); show['arrows'].append([chess.square_name(a), pas, 'r'])
    if att(dst):
        a = att(dst)[0]
        bad.append(('dest', 'Regele ar ajunge pe ' + dst + ', unde îl atacă ' + nm(b, a) + '. Ar intra în șah, iar asta nu este permis.'))
        show['red'].append(dst); show['arrows'].append([chess.square_name(a), dst, 'r'])
    if not bad:
        if att(R): notes.append('Turnul este atacat, dar asta nu oprește rocada: regulile privesc regele, nu turnul.')
        if side == 'q' and att('b' + r): notes.append('Pătratul b' + r + ' este atacat, dar pe acolo trece doar turnul, nu regele, așa că nu contează.')
    return bad, notes, show

def castle_text(fen, white, side, short=False):
    bad, notes, show = castle_info(fen, white, side)
    head = COLN[white] + (' nu poate' if bad else ' poate') + ' face rocada ' + SIDE[side] + '.'
    if bad:
        return head + ' ' + bad[0][1], bad, show
    tail = ' ' + ' '.join(notes) if notes else (' Toate condițiile sunt îndeplinite.' if not short else '')
    return head + tail, bad, show

def chk_answer(ok, want, label):
    if ok != want: print('!! NEPOTRIVIRE', label)

# ── 1. Caietul: rocada (choice Da/Nu) ──
for i, t in enumerate(SETS['wbR']['tasks']):
    side = 'k' if 'mică' in t['prompt'] else 'q'
    white = t['side'] == 'w'
    txt, bad, show = castle_text(t['fen'], white, side)
    chk_answer(not bad, t['answer'] == ['Da'], 'wbR %d' % i)
    t['expl'] = txt
    t['why'] = {'Da': 'Mai uită-te. ' + (bad[0][1] if bad else ''), 'Nu': 'Mai uită-te: regele și turnul n-au mutat, între ele e liber, iar regele nu este în șah și nu trece și nu ajunge pe un pătrat atacat. Rocada este permisă.'}
    t['show'] = show

# ── 2. ChessKid: poate albul să facă rocada (oricare parte) ──
for i, t in enumerate(SETS['ckR']['tasks']):
    parts, okany, shows = [], False, {'red': [], 'arrows': []}
    for side in 'kq':
        txt, bad, show = castle_text(t['fen'], True, side, short=True)
        parts.append(txt); okany = okany or not bad
        shows['red'] += show['red']; shows['arrows'] += show['arrows']
    chk_answer(okany, t['answer'] == ['Da'], 'ckR %d' % i)
    t['expl'] = ' '.join(parts)
    t['why'] = {'Da': 'Mai uită-te la fiecare rocadă, pe rând. ' + ' '.join(p for p in parts if 'nu poate' in p),
                'Nu': 'Mai uită-te: una dintre rocade este permisă.'}
    t['show'] = shows

# ── 3. Chess Tutor: toate rocadele permise (castles) ──
for sid in ['9a', '9b']:
    for i, t in enumerate(SETS[sid]['tasks']):
        rs = {}
        for white in (True, False):
            for side in 'kq':
                txt, bad, show = castle_text(t['fen'], white, side, short=True)
                rs[COLN[white] + ' 0-0' + ('-0' if side == 'q' else '')] = txt
                chk_answer(not bad, (COLN[white] + ' 0-0' + ('-0' if side == 'q' else '')) in t['answer'], sid + ' %d' % i)
        t['reasons'] = rs

# ── 4. De ce nu e permisă rocada (choice cu motive) ──
OPT = {'moved': 'Regele sau turnul au mutat deja', 'block': 'O piesă stă între rege și turn', 'check': 'Regele este în șah',
       'pass': 'Regele ar trece printr-un pătrat atacat', 'dest': 'Regele ar ajunge în șah'}
for i, t in enumerate(SETS['9c']['tasks']):
    side = 'k' if 'mică' in t['prompt'] else 'q'
    r = '1'
    bad, notes, show = castle_info(t['fen'], True, side)
    kinds = [k for k, _ in bad]
    if [OPT[k] for k in kinds] != t['answer']:
        print('!! 9c', i, kinds, t['answer'])
    pas, dst = ('f' if side == 'k' else 'd') + r, ('g' if side == 'k' else 'c') + r
    WHYNOT = {'moved': 'Regele și turnul stau încă pe pătratele lor de la început.',
              'block': 'Între rege și turn nu stă nicio piesă.',
              'check': 'Regele nu este în șah acum: nicio piesă nu îl atacă.',
              'pass': 'Pătratul ' + pas + ', prin care trece regele, nu este atacat.',
              'dest': 'Pătratul ' + dst + ', unde ajunge regele, nu este atacat.'}
    t['why'] = {OPT[k]: 'Nu acesta e motivul. ' + WHYNOT[k] for k in OPT if k not in kinds}
    t['expl'] = bad[0][1]
    t['show'] = show

# ── 5. ChessKid: se poate captura en passant (texte + ultima mutare) ──
CKE = [
    ('a7a5', 'Da. Pionul negru a sărit două pătrate, de pe a7 pe a5 și a ajuns chiar lângă pionul alb de pe b5. Pionul alb îl poate captura en passant: merge pe a6, pătratul peste care a sărit pionul negru, iar pionul de pe a5 dispare de pe tablă.'),
    ('c2c4', 'Da. Pionul alb a sărit două pătrate, de pe c2 pe c4 și a trecut pe lângă pionul negru de pe d4. Negrul îl poate captura en passant: pionul de pe d4 merge pe c3, iar pionul alb de pe c4 dispare de pe tablă.'),
    ('d7d5', 'Nu. După d7-d5, lângă pionul negru, pe linia a 5-a, nu stă niciun pion alb. Pionul alb de pe c6 se află mai sus, pe linia a 6-a, deci nu poate captura en passant.'),
    ('h7h5', 'Nu. Pentru en passant, pionul alb ar trebui să stea pe linia a 5-a, chiar lângă pionul care a sărit. Pionul alb de pe g4 este pe linia a 4-a. El poate captura pe h5 în mod obișnuit, dar aceea nu este o captură en passant.'),
]
for t, (last, ex) in zip(SETS['ckE']['tasks'], CKE):
    t['last'] = last; t['expl'] = ex
    t['why'] = {'Da': 'Mai uită-te: en passant se poate numai imediat după ce un pion sare două pătrate și ajunge chiar lângă pionul tău, pe aceeași linie.',
                'Nu': 'Mai uită-te: pionul a sărit două pătrate și a ajuns chiar lângă un pion advers.'}

# ── 6. Mat într-o mutare cu en passant (Chess Tutor 14) ──
M14 = [
    ('Calul merge pe f4 și dă șah. Regele negru nu are unde să plece: pătratele g4, g5 și g6 sunt păzite de regele alb, iar pe h4 stă propriul pion.',
     {'g2g4': 'Pionul dă șah, dar nu este mat: pionul negru de pe h4 îl capturează en passant (hxg3) și regele scapă de șah. Mai încearcă!'}),
    ('Pionul sare pe g4 și dă șah. Pionul negru de pe h3 nu îl poate captura en passant, pentru că nu stă lângă el, pe linia a 4-a. Regele nu are scăpare: calul păzește h4, iar regele alb păzește g4, g5 și g6.', {}),
    ('Pionul sare pe h4 și dă șah. Lângă h4 nu stă niciun pion negru, deci nu există en passant, iar regele negru nu are unde să plece.',
     {'f2f4': 'Pionul dă șah, dar nu este mat: pionul negru de pe e4 îl capturează en passant (exf3) și regele scapă de șah. Mai încearcă!'}),
    ('Pionul merge pe d4 și dă șah. A mers un singur pătrat, de pe d3, așa că nu poate fi capturat en passant. Regele negru nu are scăpare.',
     {'f2f4': 'Pionul dă șah, dar nu este mat: a sărit două pătrate, iar pionul negru de pe e4 îl capturează en passant (exf3). Mai încearcă!'}),
    ('Nebunul merge pe d7 și dă șah. Regina de pe d6 păzește toate pătratele din jurul regelui negru, iar regele alb păzește g4. Este mat.',
     {'g2g4': 'Pionul dă șah, dar nu este mat: pionul negru de pe h4 îl capturează en passant (hxg3). Mai încearcă!'}),
    ('Nebunul negru merge pe d5 și dă șah. Regele alb nu are unde să plece și nimeni nu poate captura nebunul. Este mat.',
     {'f7f5': 'Pionul dă șah, dar nu este mat: pionul alb de pe e5 îl capturează en passant (exf6). Mai încearcă!'}),
    ('Pionul sare pe g4 și dă șah. Pionul negru de pe f4 ar putea captura en passant pe g3, dar nu are voie: dacă pleacă de pe f4, turnul de pe f3 ar da șah regelui pe coloana f. Este mat.', {}),
    ('Pionul sare pe a4 și dă șah. Pionul negru de pe b4 ar putea captura en passant pe a3, dar nu are voie: dacă pleacă de pe b4, regina de pe b3 ar da șah regelui pe coloana b. Este mat.', {}),
    ('Pionul merge pe a4 și dă șah. A mers un singur pătrat, de pe a3, așa că nu poate fi capturat en passant. Este mat.',
     {'c2c4': 'Pionul dă șah, dar nu este mat: a sărit două pătrate, iar pionul negru de pe b4 îl capturează en passant (bxc3). Mai încearcă!'}),
    ('Turnul negru merge pe b3 și dă șah. Regele alb nu are scăpare. Este mat.',
     {'c7c5': 'Pionul dă șah, dar nu este mat: pionul alb de pe b5 îl capturează en passant (bxc6). Mai încearcă!',
      'a7a5': 'Pionul dă șah, dar nu este mat: pionul alb de pe b5 îl capturează en passant (bxa6). Mai încearcă!'}),
]
for t, (ex, nm_) in zip(SETS['14a']['tasks'], M14):
    t['expl'] = ex
    for k in nm_: t['notmate'][k] = nm_[k]
    if set(t['notmate']) != set(nm_): print('!! 14a notmate', t['fen'], t['notmate'].keys(), nm_.keys())
    t['notmate'] = nm_

# ── 7. ChessKid: regina sau altă piesă ──
CK14 = [
    ({'f7f8q': 'Pat! Regina de pe f8 păzește g7 și h7... iar regele negru nu mai are nicio mutare, deși nu este în șah. Partida s-ar termina remiză. Încearcă altă piesă.',
      'f7f8r': 'Pat! Turnul de pe f8 îi ia regelui negru ultimele mutări, deși nu este în șah. Partida s-ar termina remiză. Încearcă altă piesă.',
      'f7f8n': 'Calul nu dă pat, dar nici nu duce la mat în trei mutări. Încearcă altă piesă.'},
     'Subpromovare în nebun: 1.f8=N! Negrul nu e în pat, pentru că nebunul lui de pe g8 poate muta. După ce pleacă nebunul negru, urmează 2.Ce7 și 3.Ng7 mat. Cu regină sau turn ar fi fost pat imediat.'),
    ({'f7f8q': 'Pat! Regina de pe f8 păzește g7 și g8, iar regele negru de pe h7 nu mai are nicio mutare, deși nu este în șah. Partida s-ar termina remiză. Încearcă altă piesă.'},
     'Subpromovare în turn: 1.f8=T! Regele negru mai are pătratul g7 și nu este pat. Merg și calul sau nebunul. Cu regină ar fi fost pat.'),
    ({'h7h8q': 'Regina nu dă șah aici, iar negrul scapă. Caută piesa care dă mat chiar acum.',
      'h7h8r': 'Turnul nu dă șah aici. Caută piesa care dă mat chiar acum.',
      'h7h8b': 'Nebunul nu dă șah aici. Caută piesa care dă mat chiar acum.'},
     'Subpromovare în cal: 1.h8=C este mat imediat. Calul dă șah, iar toate pătratele din jurul regelui negru sunt păzite de turnuri și de nebun.'),
    ({'h7h8r': 'Turnul nu dă pat, dar nu duce la mat atât de repede. Aici nu există pericol de pat: alege piesa cea mai puternică.',
      'h7h8b': 'Nebunul nu duce la mat atât de repede. Aici nu există pericol de pat: alege piesa cea mai puternică.',
      'h7h8n': 'Calul nu duce la mat atât de repede. Aici nu există pericol de pat: alege piesa cea mai puternică.'},
     'Aici regina este cea mai bună: 1.h8=D! Regele negru mai are pătratul g6, deci nu este pat. După 1...Rg6 urmează 2.Dg7 mat.'),
]
for t, (bp, ex) in zip(SETS['ck14']['tasks'], CK14):
    assert set(bp) == set(t['badpromo']), (t['fen'], bp.keys(), t['badpromo'].keys())
    t['badpromo'] = bp; t['expl'] = ex
SETS['ck14']['tasks'][0]['badpromo']['f7f8q'] = 'Pat! Regina de pe f8 îi ia regelui negru ultima mutare, deși nu este în șah. Partida s-ar termina remiză. Încearcă altă piesă.'

# ── 8. Exercițiile vechi de promovare, acum cu mutare pe tablă ──
def fen_of(d, side):
    b = chess.Board(None)
    for k, v in d.items():
        b.set_piece_at(sq(k), chess.Piece(chess.PIECE_SYMBOLS.index(v[1].lower()), v[0] == 'w'))
    b.turn = side == 'w'; return b.fen()
PAT = 'Pat! Regele advers nu este în șah, dar nu mai are nicio mutare. Partida s-ar termina remiză. Încearcă altă piesă.'
OLDP = [
    dict(type='move', check='best', fen=fen_of({'f7': 'wP', 'h7': 'bK', 'h5': 'wK'}, 'w'), side='w', answer='f7f8r', san='f8=T', ok=[],
         prompt='Promovează pionul. Atenție la pat!',
         badpromo={'f7f8q': 'Pat! Regina de pe f8 păzește g7 și g8, iar regele alb păzește g6 și h6. Regele negru nu este în șah, dar nu mai are nicio mutare: remiză. Încearcă altă piesă.',
                   'f7f8b': 'Nu e pat, dar cu un rege și un nebun nu se poate da mat. Partida s-ar termina remiză. Încearcă altă piesă.',
                   'f7f8n': 'Nu e pat, dar cu un rege și un cal nu se poate da mat. Partida s-ar termina remiză. Încearcă altă piesă.'},
         post=['h7g7'],
         expl='Subpromovare în turn: f8=T! Turnul nu atacă pătratul g7, așa că regele negru mai are o mutare și nu e pat. Cu rege și turn, albul câștigă: va împinge regele negru spre margine și îi va da mat.'),
    dict(type='move', check='best', fen=fen_of({'b6': 'wQ', 'e3': 'wN', 'a3': 'wP', 'g2': 'wP', 'h3': 'wP', 'h2': 'wK', 'e4': 'bQ', 'a4': 'bP', 'b5': 'bP', 'f2': 'bP', 'g7': 'bP', 'h6': 'bP', 'h7': 'bK'}, 'b'),
         side='b', pre=['e4e3', 'b6e3'], answer='f2f1n', san='f1=C+', ok=[],
         prompt='Negrul a capturat calul (1...Dxe3), iar albul a recapturat cu regina (2.Dxe3). Acum promovează pionul de pe f2 în piesa care câștigă regina albă.',
         badpromo={'f2f1q': 'Noua regină nu dă șah, iar albul își păstrează regina. Partida rămâne egală. Caută piesa care atacă în același timp regele alb de pe h2 și regina de pe e3.',
                   'f2f1r': 'Turnul nu atacă nici regele, nici regina albă, iar regina albă poate captura pionii negri. Caută piesa care atacă în același timp regele de pe h2 și regina de pe e3.',
                   'f2f1b': 'Nebunul nu atacă nici regele, nici regina albă. Caută piesa care atacă în același timp regele de pe h2 și regina de pe e3.'},
         post=['h2g1', 'f1e3'],
         expl='Subpromovare în cal: f1=C+! Calul nou dă șah regelui de pe h2 și atacă în același timp regina de pe e3: este un atac dublu. Regele trebuie să iasă din șah (Rg1), iar calul capturează regina (Cxe3). Negrul rămâne cu un cal în plus.'),
    dict(type='move', check='best', fen=fen_of({'b8': 'wQ', 'd7': 'wP', 'c6': 'bK', 'e6': 'wB', 'g6': 'bP', 'g5': 'wP', 'h5': 'bP', 'b4': 'wK', 'h4': 'wP'}, 'w'),
         side='w', answer='d7d8n', san='d8=C#', ok=[],
         prompt='Promovează pionul în piesa care dă mat imediat. Atenție la pat!',
         badpromo={'d7d8q': PAT, 'd7d8r': PAT, 'd7d8b': PAT},
         expl='Subpromovare în cal: d8=C este mat! Calul de pe d8 dă șah regelui de pe c6, iar toate pătratele din jurul regelui sunt păzite: b5, b6, b7, c7 și d6 de regina albă, c5 de regele alb, d5 și d7 de nebun. Regina, turnul sau nebunul nu dau șah de pe d8, iar regele negru nu ar mai avea nicio mutare: ar fi pat.'),
    dict(type='move', check='best', fen=fen_of({'c7': 'wP', 'd4': 'bR', 'c2': 'wK', 'a1': 'bK'}, 'w'),
         side='w', answer='c7c8r', san='c8=T', ok=[],
         prompt='Promovează pionul. Gândește-te ce poate face turnul negru după promovare.',
         badpromo={'c7c8q': 'Negrul răspunde Tc4+! Dacă regina capturează turnul (Dxc4), regele negru de pe a1 nu mai are nicio mutare și nu este în șah: pat. Dacă regina nu capturează, turnul o capturează pe ea. Încearcă altă piesă.',
                   'c7c8b': 'Negrul răspunde Tc4+ și apoi capturează nebunul de pe c8. Albul rămâne fără nimic. Încearcă altă piesă.',
                   'c7c8n': 'Negrul răspunde Tc4+ și apoi capturează calul de pe c8. Albul rămâne fără nimic. Încearcă altă piesă.'},
         post=['d4a4', 'c2b3'],
         expl='Subpromovare în turn: c8=T! Acum albul amenință Ta8+, așa că negrul își pune turnul pe a4 (Ta4). Urmează Rb3! Regele alb atacă turnul de pe a4 și amenință în același timp mat cu Tc1. Negrul nu se poate apăra de amândouă. (Dacă albul ar fi promovat regină, negrul ar fi scăpat prin pat după Tc4+.)'),
    dict(type='move', check='best', fen=fen_of({'h8': 'wR', 'a5': 'bK', 'b4': 'bP', 'b3': 'wK', 'a2': 'bP', 'c2': 'bR'}, 'b'),
         side='b', answer='a2a1n', san='a1=C#', ok=[],
         prompt='Promovează pionul negru în piesa care dă mat imediat.',
         badpromo={'a2a1q': 'Regina de pe a1 nu dă șah. Albul răspunde Ta8+: regele negru trebuie să plece de pe coloana a, iar turnul alb capturează apoi regina de pe a1. Încearcă altă piesă.',
                   'a2a1r': 'Turnul de pe a1 nu dă șah. Albul răspunde Ta8+: regele negru pleacă de pe coloana a, iar turnul alb capturează turnul de pe a1. Încearcă altă piesă.',
                   'a2a1b': 'Nebunul de pe a1 nu dă șah. Albul răspunde Ta8+: regele negru pleacă de pe coloana a, iar turnul alb capturează nebunul de pe a1. Încearcă altă piesă.'},
         expl='Subpromovare în cal: a1=C este mat! Calul dă șah regelui alb de pe b3 și apără turnul de pe c2. Regele alb nu are unde să plece: a3 și c3 sunt atacate de pionul de pe b4, a2, b2 și c4 de turn, a4 de regele negru, iar pionul de pe b4 este apărat de regele negru.'),
]
# verificare
for t in OLDP:
    b = chess.Board(t['fen'])
    for u in t.get('pre', []): b.push_uci(u)
    m = chess.Move.from_uci(t['answer']); assert m in b.legal_moves
    b2 = b.copy(); b2.push(m)
    print('promo', t['san'], 'MAT' if b2.is_checkmate() else '', end=' | ')
    for u in t['badpromo']:
        b3 = b.copy(); b3.push_uci(u); print(u[-1], 'PAT' if b3.is_stalemate() else 'mat' if b3.is_checkmate() else '-', end=' ')
    for u in t.get('post', []): b2.push_uci(u)
    print()

# ── 9. Exercițiile vechi de en passant ──
OLDE = [
    dict(type='move', check='best', fen='4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1', side='w', last='d7d5', ep='d6', answer='e5d6', san='exd6 e.p.', ok=[],
         prompt='Negrul tocmai a mutat pionul de pe d7 pe d5, două pătrate dintr-odată. Capturează-l en passant!',
         bad={},
         expl='Pionul alb de pe e5 merge pe d6, pătratul peste care a sărit pionul negru, iar pionul de pe d5 dispare de pe tablă. Se notează exd6 e.p. Dacă albul ar fi jucat altceva, nu mai putea captura en passant la mutarea următoare.'),
    dict(type='choice', fen='4k3/8/8/3pP3/8/8/8/4K3 w - - 0 1', side='w', last='d6d5', opts=['Da', 'Nu'], answer=['Nu'],
         prompt='Pionul negru tocmai a ajuns pe d5, dar a venit de pe d6, adică a mers un singur pătrat. Poate albul să-l captureze en passant?',
         why={'Da': 'Mai uită-te: pionul negru a mers un singur pătrat, de pe d6 pe d5. En passant se poate numai după un salt de două pătrate de pe linia de start.'},
         expl='Nu. Poziția arată la fel ca în exercițiul de dinainte, dar pionul negru a venit de pe d6, nu de pe d7. En passant se poate numai când pionul sare două pătrate de pe linia lui de start. Aici contează de unde a venit pionul, nu doar unde a ajuns.'),
    dict(type='choice', fen='r5k1/pp6/8/2Pp3Q/3P4/8/8/K7 w - - 0 1', side='w', last='d6d5', opts=['Da', 'Nu'], answer=['Nu'],
         prompt='Negrul tocmai a mutat pionul de pe d6 pe d5. Poate pionul alb de pe c5 să-l captureze en passant?',
         why={'Da': 'Mai uită-te: pionul negru a mers un singur pătrat, de pe d6 pe d5. En passant se poate numai după un salt de două pătrate de pe linia de start.'},
         show={'red': [], 'arrows': [['h5', 'd5', 'g']]},
         expl='Nu. Pionul negru a mers un singur pătrat, deci en passant nu este permis. Albul poate însă captura pionul de pe d5 în mod obișnuit, cu regina: Dxd5 (săgeata verde).'),
    dict(type='move', check='best', fen='8/8/8/8/2p5/6k1/P2P4/6K1 w - - 0 1', side='w', answer='a2a4', san='a4', ok=[],
         prompt='Albul vrea să avanseze un pion două pătrate dintr-odată. Alege pionul pe care pionul negru de pe c4 nu îl poate captura en passant.',
         bad={'d2d4': ['Pionul de pe d4 ar trece pe lângă pionul negru de pe c4, iar acesta îl capturează en passant: cxd3 (săgeata roșie). Încearcă alt pion.', 'c4d3'],
              'd2d3': ['Pe d3, pionul alb este capturat direct de pionul de pe c4 (săgeata roșie). Avansează un pion două pătrate.', 'c4d3'],
              'a2a3': ['Mutarea este bună, dar exercițiul cere un pas dublu: avansează un pion două pătrate.', None]},
         expl='a2-a4! Pionul de pe a4 nu ajunge lângă pionul negru de pe c4, așa că nu poate fi capturat en passant. Dacă albul ar fi jucat d2-d4, pionul negru l-ar fi capturat: cxd3 e.p.'),
    dict(type='move', check='best', fen='6q1/4k3/4p3/4PpP1/4K1R1/8/8/8 w - f6 0 1', side='w', last='f7f5', ep='f6', answer='g5f6', san='gxf6+ e.p.', ok=[],
         prompt='Negrul tocmai a mutat f7-f5 și dă șah regelui alb. Pionul negru poate fi capturat en passant de doi pioni albi. Alege captura cea mai bună!',
         bad={'e5f6': ['Și exf6 e.p. scapă regele de șah, dar nu câștigă nimic. Caută captura care, pe lângă șah, deschide drumul turnului de pe g4 spre regina neagră de pe g8.', None]},
         post=['e7f7', 'g4g8'],
         expl='gxf6+ e.p.! Pionul de pe g5 capturează en passant și ajunge pe f6, de unde dă șah regelui negru. În același timp, coloana g s-a eliberat: turnul de pe g4 atacă acum regina de pe g8. Regele negru trebuie să iasă din șah, iar turnul capturează regina.'),
]
for t in OLDE:
    b = chess.Board(t['fen']); assert b.is_valid(), t['fen']
    if t['type'] == 'move':
        m = chess.Move.from_uci(t['answer']); assert m in b.legal_moves, t['answer']
        for u in t.get('bad', {}): assert chess.Move.from_uci(u) in b.legal_moves, u
        b.push(m)
        for u in t.get('post', []): b.push_uci(u)
print('ep ok')

for t in OLDP: t['failmsg'] = 'Mută pionul pe ultima linie și alege piesa în care se transformă.'
OLDE[0]['failmsg'] = 'Caută captura en passant: pionul alb care stă chiar lângă pionul care a sărit două pătrate.'
OLDE[3]['failmsg'] = 'Avansează un pion două pătrate dintr-odată.'
OLDE[4]['failmsg'] = 'Regele alb este în șah de la pionul de pe f5. Caută o captură en passant care scapă regele de șah.'
for st in SETS.values(): st.pop('src', None)
SETS['wbR']['title'] = '♚ Rocada: da sau nu?'
SETS['ckR']['title'] = '♚ Poate albul să facă rocada?'
SETS['ckE']['title'] = '↗ Se poate captura en passant?'
SETS['9a']['title'] = '♚ Care rocade sunt permise? (1)'
SETS['9b']['title'] = '♚ Care rocade sunt permise? (2)'
SETS['9c']['title'] = '♚ De ce nu e permisă rocada?'
SETS['14a']['title'] = '↗ Mat într-o mutare: atenție la en passant'
SETS['ck14']['title'] = '♟ Regina sau altă piesă?'
SETS['9a']['intro'] = SETS['9b']['intro'] = 'Aici nu contează cine e la mutare. Verifică, pe rând, ambele rocade ale albului și ambele rocade ale negrului.'
SETS['14a']['intro'] = 'Dă mat într-o mutare. Ai grijă: un pion care sare două pătrate și dă șah poate fi capturat en passant.'
SETS['ck14']['intro'] = 'Albul are mat în cel mult trei mutări. Promovează pionul în piesa potrivită: uneori regina dă pat!'
NEW = {
    'oP': dict(id='oP', title='♟ Ce piesă alegi la promovare?', intro='Mută pionul pe ultima linie și alege piesa. De cele mai multe ori alegi regina, dar aici trebuie să te gândești mai bine.', instr=None, tasks=OLDP),
    'oE': dict(id='oE', title='↗ En passant: da sau nu?', intro='Uită-te la săgeata albastră: ea arată mutarea pe care a făcut-o adversarul chiar acum.', instr=None, tasks=OLDE),
}
ALL = dict(SETS, **NEW)
OUT = {'tabs': [
    {'id': 'baza', 'title': 'De bază', 'sets': [ALL[k] for k in ['wbR', 'ckR', 'oE', 'ckE']]},
    {'id': 'mediu', 'title': 'Mediu', 'sets': [ALL[k] for k in ['9a', '9b', 'oP']]},
    {'id': 'avansat', 'title': 'Avansat', 'sets': [ALL[k] for k in ['9c', 'ck14', '14a']]},
]}
n = sum(len(st['tasks']) for t in OUT['tabs'] for st in t['sets'])
print('total exercitii', n)
js = '/* Exercițiile lecției „Mutări speciale”: rocada, promovarea, en passant. Generat de tools/perfectionare/build3b.py. */\nwindow.L3EX = ' + json.dumps(OUT, ensure_ascii=False) + ';\n'
open(ROOT + 'data/nivel1_lectia3_ex.js', 'w', encoding='utf-8').write(js)
txt = json.dumps(OUT, ensure_ascii=False)
print('virgula-si:', txt.count(', și '), ' mananca:', len(re.findall('mănânc|mânc', txt)))
