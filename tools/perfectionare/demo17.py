# Exemplele din sertare pentru „Patul” -> data/nivel1_lectia17_demo.js
# Surse: Manualul Steps pasul 1, lecția 12 („Draw”); ChessKid lecțiile 3 și 4.
import json, sys, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia17_demo.js'

def S(fen, side, text, arrows=(), acts=(), st=None):
    """st: starea poziției pentru partea la mutare: 'mate' / 'stale' / 'play' / 'draw' (verificată)"""
    return dict(fen=fen, side=side, text=text, arrows=[list(a) for a in arrows], acts=list(acts), _st=st)
def A(label, move=None, text='', arrows=(), line=None, chk=None):
    """chk: starea după mutare(i) pentru partea care urmează: 'mate' / 'stale' / 'play'"""
    d = dict(label=label, text=text, arrows=[list(a) for a in arrows])
    if move: d['move'] = move
    if line: d['line'] = line
    d['_chk'] = chk
    return d

G = {}
# ── ACC 0: remiza ──
G['remiza'] = [
  S('8/8/4k3/8/8/2K5/8/8', 'w',
    '<p>Pe tablă au rămas doar cei doi regi. Niciunul nu mai poate da mat, așa că partida se termină <strong>remiză</strong>: fiecare jucător primește o jumătate de punct (½–½).</p>',
    st='draw'),
  S('k2R4/2Q5/8/8/8/6K1/8/8', 'b',
    '<p>Să ne amintim matul. Regele negru este în șah (turnul de pe d8) și nu mai are nicio mutare. <strong>Mat</strong>: albul a câștigat.</p><p>Pentru pat sunt importante tocmai aceste două lucruri: dacă regele e în șah și dacă mai are vreo mutare.</p>',
    [('d8', 'a8', 'r')], st='mate'),
]

# ── ACC 1: sertare ──
G['cepat'] = [
  S('k7/8/1Q6/8/8/6K1/2R5/8', 'b',
    '<p>Negrul e la mutare. Regele lui nu are niciun pătrat liber: a7, b7 și b8 sunt atacate de regina albă. Dar regele <strong>nu este în șah</strong>.</p><p>Asta este <strong>patul</strong>: jucătorul la mutare nu e în șah și nu poate face nicio mutare. Partida se termină remiză.</p><p>Albul are în plus o regină și un turn, dar a ratat victoria.</p>',
    [('b6', 'a7', 'r'), ('b6', 'b7', 'r'), ('b6', 'b8', 'r')], st='stale'),
  S('8/8/8/8/8/2KQ4/8/2k5', 'b',
    '<p>Și aici negrul e la mutare și nu e în șah. Regele alb păzește b2, iar regina toate celelalte pătrate. Este pat.</p><p>Cu regina pe c2 ar fi fost mat. O mutare greșită a reginei face diferența dintre victorie și remiză.</p>',
    [('c3', 'b2', 'r'), ('d3', 'd2', 'r'), ('d3', 'd1', 'r'), ('d3', 'b1', 'r')], st='stale'),
  S('1k4r1/1pp5/p7/1n6/8/8/5q2/7K', 'w',
    '<p>Negrul a capturat toate piesele albe și a închis regele în colț. Dar regele alb <strong>nu este atacat</strong> și nu are niciun pătrat sigur. Albul e la mutare: pat.</p><p>Cu atâtea piese în plus, negrul trebuia să găsească matul.</p>',
    [('f2', 'g1', 'r'), ('f2', 'g2', 'r'), ('f2', 'h2', 'r')], st='stale'),
]
G['toate'] = [
  S('7k/4Q2P/p7/Pp6/1P6/8/K7/8', 'b',
    '<p>Regele negru nu se poate mișca, iar pionii negri sunt blocați: a6 de pionul de pe a5, b5 de pionul de pe b4. Negrul nu e în șah și nu poate muta nicio piesă. Este pat.</p><p>La pat nu ne uităm doar la rege. <strong>Nicio piesă</strong> a jucătorului la mutare nu trebuie să mai poată muta.</p>',
    [('e7', 'g7', 'r'), ('h7', 'g8', 'r')], st='stale'),
  S('k7/b1K5/7p/7P/R7/8/8/8', 'b',
    '<p>Regele de pe a8 nu poate muta, iar pionul de pe h6 e blocat. Ce surprinde e că nici nebunul de pe a7 nu poate muta: dacă pleacă, turnul de pe a4 dă șah regelui. Ar fi o mutare interzisă.</p><p>Negrul e în pat.</p>',
    [('a4', 'a8', 'r')], st='stale'),
  S('3k4/1pp2pp1/1b4r1/pP2p3/P3P3/6Nb/5P1P/3qB1KR', 'w',
    '<p>Un pat celebru, din partida Troițki – Vogt, 1896. Negrul tocmai a capturat pe d1 regina albă, dată de sacrificiu. Albul e la mutare și are multe piese, dar niciuna nu poate muta:</p><p>turnul de pe h1 e închis, regele ar intra în șahul nebunului de pe h3, calul de pe g3, nebunul de pe e1 și pionul de pe f2 sunt legați de rege, iar ceilalți pioni sunt blocați. Este pat.</p>',
    [('h3', 'g2', 'r'), ('g6', 'g1', 'r'), ('d1', 'g1', 'r'), ('b6', 'g1', 'r')], st='stale'),
  S('8/2R5/5R2/3k4/8/B1K2N2/4Q3/8', 'b',
    '<p>Un exemplu greu de întâlnit în partide: albul atacă toate pătratele din jurul regelui negru, dar regele nu este în șah. Negrul e la mutare: pat.</p><p>Dacă ar fi fost albul la mutare, ar fi avut mai multe maturi într-o mutare. Nu trebuie să capturezi toate piesele și nici să aduci multe piese: ajunge un mat simplu.</p>',
    st='stale'),
]
G['nupat'] = [
  S('7k/8/p4N1B/8/K7/8/8/8', 'b',
    '<p>Regele negru nu poate muta, dar pionul de pe a6 poate. Deci <strong>nu este pat</strong>: negrul joacă a5.</p><p>După a5, albul trebuie să fie atent. Încearcă mutările de mai jos.</p>',
    [('a6', 'a5', 'g')],
    [A('a5 Rxa5?', line=['a6a5', 'a4a5'], text='Greșit. Regele alb capturează pionul și negrul nu mai are nicio mutare: pat.', chk='stale'),
     A('a5 Nc1!', line=['a6a5', 'h6c1'], text='Bine. Nebunul pleacă de pe h6 și eliberează pătratul g7 pentru regele negru. Patul nu mai e posibil, iar pionul de pe a5 va fi capturat la mutarea următoare.', arrows=[('h8', 'g7', 'g')], chk='play')],
    st='play'),
  S('7k/1n3Q2/6K1/p7/8/8/8/8', 'b',
    '<p>Regele negru nu are nicio mutare. Mulți ar spune că e pat, dar <strong>nu este</strong>: negrul mai are calul de pe b7 și pionul de pe a5, care pot muta.</p><p>Negrul mută, iar albul dă apoi mat pe g7, f8 sau e8.</p>',
    [('b7', 'd6', 'g'), ('a5', 'a4', 'g')], st='play'),
]
G['randul'] = [
  S('k7/p7/P7/8/3K4/8/1R6/8', 'w',
    '<p>Negrul nu ar avea nicio mutare. Dar e rândul <strong>albului</strong>, așa că jocul continuă. Pat este doar când jucătorul <strong>la mutare</strong> nu poate muta.</p><p>Albul trebuie să fie atent: dacă turnul rămâne pe coloana b, după mutarea lui negrul e în pat.</p>',
    [('b2', 'b8', 'r'), ('b2', 'b7', 'r')],
    [A('Rc5?', 'd4c5', 'Greșit. Turnul a rămas pe coloana b, iar negrul nu mai are nicio mutare: pat.', chk='stale'),
     A('Th2', 'b2h2', 'Bine. Turnul pleacă de pe coloana b. Regele negru poate merge pe b8 și jocul continuă.', [('a8', 'b8', 'g')], chk='play')],
    st='play'),
]
G['arma'] = [
  S('3K3k/8/6Q1/8/8/4r3/8/8', 'b',
    '<p>Negrul are doar un turn contra reginei. Regele negru nu poate muta, dar turnul încă poate. Dacă negrul scapă de turn, rămâne fără nicio mutare: pat.</p><p>Jucătorii atenți folosesc patul ca <strong>armă</strong>, când sunt în dezavantaj. Încearcă:</p>',
    (),
    [A('Td3+ Dxd3', line=['e3d3', 'g6d3'], text='Șahul de pe d3 nu ajută: regina capturează turnul și regele negru poate muta din nou. Nu e pat.', chk='play'),
     A('Te8+ Rxe8?', line=['e3e8', 'd8e8'], text='Dacă regele alb capturează turnul, negrul nu mai are nicio mutare și nu e în șah: pat. Albul a ratat victoria.', chk='stale'),
     A('Te8+ Dxe8', line=['e3e8', 'g6e8'], text='Albul trebuie să captureze cu regina. Așa regele negru primește pătratele g7 și h7, iar patul nu se mai face.', arrows=[('h8', 'g7', 'g')], chk='play')],
    st='play'),
]
G['evita'] = [
  S('8/k1P5/8/K7/8/8/8/8', 'w',
    '<p>Albul vrea să promoveze pionul. Dar atenție: dacă face regină, regele negru nu mai are nicio mutare.</p>',
    (),
    [A('c8=D?', 'c7c8q', 'Greșit. Regina de pe c8 și regele alb păzesc toate pătratele regelui negru: pat.', chk='stale'),
     A('c8=T!', 'c7c8r', 'Bine. Turnul păzește linia a 8-a, dar regele negru poate merge pe b7. Albul câștigă cu regele și turnul.', [('a7', 'b7', 'g')], chk='play')],
    st='play'),
  S('8/5P1k/5K2/8/8/8/8/8', 'w',
    '<p>Aceeași capcană, în alt colț. Promovarea în regină dă pat. Albul are mai multe mutări câștigătoare, dar cea mai frumoasă este promovarea în turn.</p>',
    (),
    [A('f8=D?', 'f7f8q', 'Greșit. Regele negru nu mai are niciun pătrat liber: pat.', chk='stale'),
     A('f8=T!', 'f7f8r', 'Bine. Regele negru poate merge pe h6, iar albul dă mat în curând.', [('h7', 'h6', 'g')], chk='play')],
    st='play'),
  S('7k/8/8/6Q1/8/8/8/4K3', 'w',
    '<p>Regina a împins regele negru în colț. Acum e momentul să vină regele alb în ajutor. O mutare grăbită a reginei strică totul.</p>',
    (),
    [A('Dg6?', 'g5g6', 'Greșit. Regele negru nu mai are nicio mutare și nu e în șah: pat.', chk='stale'),
     A('Rf2', 'e1f2', 'Bine. Regele alb se apropie. Regele negru are încă pătratele h7 și g8, deci nu e pat.', [('h8', 'h7', 'g')], chk='play')],
    st='play'),
]

# ═════════ verificare ═════════
def board(fen, side):
    b = chess.Board(None); b.set_board_fen(fen); b.turn = side == 'w'; return b
def state(b):
    if not b.king(chess.WHITE) or not b.king(chess.BLACK): return '?'
    if b.is_checkmate(): return 'mate'
    if b.is_stalemate(): return 'stale'
    return 'play'
bad = 0
for k, steps in G.items():
    for s in steps:
        b = board(s['fen'], s['side']); st = s.pop('_st')
        got = 'draw' if len(b.piece_map()) == 2 else state(b)
        if st and st != got: print('STARE', k, s['fen'], st, got); bad += 1
        for a in s['acts']:
            chk = a.pop('_chk')
            b = board(s['fen'], s['side'])
            for u in (a.get('line') or [a['move']]):
                m = chess.Move.from_uci(u)
                if m not in b.legal_moves: print('ILEGAL', k, a['label'], u); bad += 1; break
                b.push(m)
            if chk and state(b) != chk: print('DUPĂ', k, a['label'], chk, state(b)); bad += 1
assert not bad, bad
open(OUT, 'w', encoding='utf-8').write('/* Exemplele din sertarele lecției „Patul”.\n   Surse: metoda Steps (Brunia & van Wijgerden), Manualul pasului 1, lecția 12; ChessKid, lecțiile 3 și 4.\n   Generat automat. */\nwindow.L17DEMO = ' + json.dumps(G, ensure_ascii=False) + ';\n')
print('ok', {k: len(v) for k, v in G.items()})
