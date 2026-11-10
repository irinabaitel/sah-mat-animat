# Exemplele din sertare pentru „Mutări speciale” -> data/nivel1_lectia3_demo.js
# Surse: Manualul Steps pasul 1, lecțiile 9 (Castling), 4 (The pawn) și 14 (Capturing en passant); ChessKid lecțiile 5 și 14.
import json, sys, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia3_demo.js'

def S(fen, side, text, arrows=(), acts=(), cr='-', ep='-'):
    return dict(fen=fen, side=side, text=text, arrows=[list(a) for a in arrows], acts=list(acts), _cr=cr, _ep=ep)
def A(label, move=None, text='', arrows=(), line=None, bad=None):
    """bad: indexul mutării din linie care NU e permisă (se arată doar explicația)"""
    d = dict(label=label, text=text, arrows=[list(a) for a in arrows])
    if move: d['move'] = move
    if line: d['line'] = line
    d['_bad'] = bad
    return d

G = {}
# ── ACC 0 ──
G['intro'] = [
  S('r1bqkb1r/2p2ppp/p1np1n2/1p2p3/4P3/1BP2N2/PP1P1PPP/RNBQK2R', 'w',
    '<p>Albul vrea să-și pună regele la adăpost. Regele a rămas pe e1, iar între el și turnul de pe h1 drumul e liber. Este momentul pentru o mutare specială: <strong>rocada</strong>.</p>',
    [('e1', 'g1', 'g')], [A('0-0', 'e1g1', 'Regele a mers două pătrate spre turn, iar turnul a sărit peste el, pe f1. Regele stă acum ascuns după pioni.')], cr='KQkq'),
]

# ── ACC 1: sertare ──
G['rocada'] = [
  S('8/8/8/8/8/8/8/4K2R', 'w',
    '<p>Regele și turnul sunt pe pătratele de la început. <strong>Rocada mică</strong> (0-0) se face așa:</p><ul><li>apuci <strong>doar regele</strong> și îl muți două pătrate spre turn (pe g1);</li><li>lași regele din mână;</li><li>cu <strong>aceeași mână</strong> apuci turnul și îl pui de cealaltă parte a regelui (pe f1).</li></ul>',
    [('e1', 'g1', 'g'), ('h1', 'f1', 'g')], [A('0-0', 'e1g1', 'Rocada mică: regele pe g1, turnul pe f1. În colț a rămas un singur pătrat liber.')], cr='K'),
  S('8/8/8/8/8/8/8/R3K3', 'w',
    '<p><strong>Rocada mare</strong> (0-0-0) se face la fel, spre turnul de pe a1: regele merge două pătrate (pe c1), iar turnul trece de cealaltă parte (pe d1).</p>',
    [('e1', 'c1', 'g'), ('a1', 'd1', 'g')], [A('0-0-0', 'e1c1', 'Rocada mare: regele pe c1, turnul pe d1. De data aceasta în colț au rămas două pătrate: a1 și b1.')], cr='Q'),
  S('r3k3/ppp5/8/8/8/8/5PPP/4K2R', 'w',
    '<p>Rocada pe tabla goală nu arată la ce folosește. Aici regii au pionii în față. După rocadă, regele alb stă în siguranță în spatele pionilor, iar turnul intră în joc.</p>',
    (), [A('0-0 și 0-0-0', line=['e1g1', 'e8c8'], text='Albul face rocada mică, negrul rocada mare. Regele alb e complet la adăpost; pe cel negru l-ar putea ataca un nebun pe diagonala h3–c8.')], cr='Kq'),
  S('r3k2r/2p2ppp/p1np1n2/1p2p3/4P3/1BPP1N2/PP3PPP/R3K2R', 'w',
    '<p>Albul poate face rocada de ambele părți: drumul e liber spre ambele turnuri.</p>',
    (), [A('0-0', 'e1g1', 'Rocada mică: regele pe g1, turnul pe f1.'), A('0-0-0', 'e1c1', 'Rocada mare: regele pe c1, turnul pe d1.')], cr='KQkq'),
]
G['rocnu1'] = [
  S('r2k3r/ppp2pp1/7p/8/8/6P1/PPP2P1P/1R2K1R1', 'w',
    '<p>Nu ai voie să faci rocada <strong>dacă regele a mutat deja</strong> în partida aceasta, chiar dacă s-a întors pe e8. Regele negru a mutat pe d8, deci negrul nu mai poate face rocada.</p><p>Nici <strong>cu un turn care a mutat</strong> nu ai voie, chiar dacă s-a întors pe a1 sau h1. Turnurile albe au plecat pe b1 și g1, deci albul nu poate face rocada.</p>'),
  S('rn2kB1r/ppp2p1p/6p1/8/1b6/6P1/PPP2PP1/R3K2R', 'b',
    '<p>Nu ai voie să faci rocada <strong>dacă între rege și turn stă o piesă</strong>. Negrul nu poate face rocada mare (calul de pe b8 e în cale) și nici rocada mică (nebunul alb de pe f8 e în cale).</p>',
    (), cr='KQkq'),
]
G['rocnu2'] = [
  S('rn2kB1r/ppp2p1p/6p1/8/1b6/6P1/PPP2PP1/R3K2R', 'w',
    '<p>Nu ai voie să faci rocada <strong>dacă ești în șah</strong>. Nebunul de pe b4 dă șah regelui alb, deci albul nu poate face rocada în nicio parte.</p>',
    [('b4', 'e1', 'r')], cr='KQkq'),
  S('r3k2r/1p4pp/p1p1B3/8/3b4/1P4Pb/P1P2P1P/R3K2R', 'b',
    '<p>Nu ai voie să faci rocada <strong>dacă după ea regele ar ajunge în șah</strong>. Nebunul alb de pe e6 atacă g8 și c8: negrul nu poate face nicio rocadă.</p>',
    [('e6', 'g8', 'r'), ('e6', 'c8', 'r')], cr='KQkq'),
  S('r3k2r/1p4pp/p1p1B3/8/3b4/1P4Pb/P1P2P1P/R3K2R', 'w',
    '<p>Nu ai voie să faci rocada <strong>dacă regele trece printr-un pătrat atacat</strong>. Nebunul de pe h3 atacă f1, deci albul nu poate face rocada mică.</p><p>Rocada mare este permisă, deși nebunul de pe d4 atacă turnul de pe a1. Contează doar pătratele <strong>regelui</strong>: e1, d1 și c1.</p>',
    [('h3', 'f1', 'r'), ('d4', 'a1', 'y')], [A('0-0-0', 'e1c1', 'Rocada mare e permisă: regele nu e în șah, nu trece printr-un pătrat atacat și nu ajunge în șah.')], cr='KQkq'),
]
G['promo'] = [
  S('8/3P4/8/8/8/8/8/8', 'w',
    '<p>Pionul care ajunge pe ultima linie se transformă într-o <strong>regină, un turn, un nebun sau un cal</strong> de aceeași culoare. Nu poate rămâne pion și nu poate deveni rege. Asta se numește <strong>promovare</strong>.</p><p>Alege piesa:</p>',
    [('d7', 'd8', 'g')], [A('d8=D', 'd7d8q'), A('d8=T', 'd7d8r'), A('d8=N', 'd7d8b'), A('d8=C', 'd7d8n')]),
  S('8/1p4p1/6Pp/2N1p3/3Q1R2/8/1p6/2R5', 'b',
    '<p>Pionii negri merg în jos. Pionul de pe b2 poate promova pe b1 sau capturând turnul de pe c1. Pionul de pe e5 poate captura regina sau turnul ori poate merge un pas înainte.</p>',
    (), [A('b1=D', 'b2b1q', 'Pionul a ajuns pe b1 și a devenit regină.'), A('bxc1=D', 'b2c1q', 'Pionul a capturat turnul și s-a transformat în regină.'), A('exd4', 'e5d4', 'Pionul de pe e5 capturează regina.')]),
]
G['subpromo'] = [
  S('8/k1P5/2K5/8/8/8/8/8', 'w',
    '<p>Aproape mereu pionul devine regină. Dar uneori regina face <strong>pat</strong>. Aici albul trebuie să promoveze pionul de pe c7. Încearcă:</p>',
    (), [A('c8=D?', 'c7c8q', 'Pat! Regele negru nu e în șah, dar nu mai are nicio mutare. Remiză.', bad=None),
         A('c8=T!', line=['c7c8r', 'a7a6', 'c8a8'], text='Cu turnul nu e pat: regele negru poate merge pe a6, iar turnul dă mat pe a8.')]),
]
G['ep'] = [
  S('8/6p1/1p6/5P2/P7/8/8/8', 'b',
    '<p>Pionii pot sări două pătrate de pe linia de start. Pionii de pe a4 și b6 se blochează unul pe altul. Dar pionul de pe g7 ar putea trece pe lângă pionul alb de pe f5, sărind direct pe g5.</p><p>Ca să nu se întâmple asta, albul poate face ca și cum pionul ar fi mers <strong>un singur pătrat</strong> și îl capturează: <strong>en passant</strong> (în franceză, „în trecere”).</p>',
    [('g7', 'g5', 'g')], [A('g5 fxg6', line=['g7g5', 'f5g6'], text='Negrul a jucat g7-g5, iar albul a capturat en passant: pionul alb a ajuns pe g6, iar pionul negru a dispărut de pe g5.')]),
  S('8/8/8/8/3p4/8/2P5/8', 'w',
    '<p>Albul joacă c2-c4. Pionul negru de pe d4 îl poate captura ca și cum ar fi mers doar până pe c3.</p>',
    [('c2', 'c4', 'g')], [A('c4 dxc3', line=['c2c4', 'd4c3'], text='Pionul negru a ajuns pe c3, un pătrat <strong>gol</strong>, iar pionul alb de pe c4 a fost capturat. Este singura captură în care piesa nu ajunge pe pătratul piesei capturate.')]),
  S('8/8/7p/6P1/1p6/8/P7/8', 'w',
    '<p>Pionul alb de pe a2 vrea să treacă pe lângă pionul negru de pe b4.</p>',
    [('a2', 'a4', 'g')], [A('a4 bxa3', line=['a2a4', 'b4a3'], text='Albul a sărit două pătrate, iar negrul a capturat imediat en passant: bxa3.')]),
]
G['epacum'] = [
  S('8/8/7p/6P1/1p6/8/P7/8', 'w',
    '<p>En passant se poate face <strong>numai imediat</strong>, la mutarea următoare. Dacă joci altceva, pierzi dreptul pentru totdeauna. Și nu ești obligat: dacă nu vrei, nu capturezi.</p>',
    (), [A('a4 h5 g6', line=['a2a4', 'h6h5', 'g5g6'], text='Albul a jucat a2-a4, dar negrul a mutat pionul de pe h6. Acum e prea târziu: pionul de pe b4 nu mai poate captura en passant pe a3.')]),
]

# ═════════ verificare ═════════
bad = 0
def mk(s):
    b = chess.Board(None); b.set_board_fen(s['fen']); b.turn = s['side'] == 'w'
    b.castling_rights = 0
    if s['_cr'] != '-': b.set_castling_fen(s['_cr'])
    return b
def legal(b):
    return list(b.legal_moves) if b.king(chess.WHITE) is not None and b.king(chess.BLACK) is not None else list(b.pseudo_legal_moves)
for k, steps in G.items():
    for s in steps:
        for a in s['acts']:
            a.pop('_bad')
            b = mk(s)
            for u in (a.get('line') or [a['move']]):
                m = chess.Move.from_uci(u)
                if b.king(chess.WHITE) is None and len(u) == 4 and b.piece_at(m.from_square) and b.piece_at(m.from_square).piece_type == chess.PAWN and u[3] in '18': pass
                if m not in legal(b): print('ILEGAL', k, a['label'], u, b.fen()); bad += 1; break
                b.push(m)
        s.pop('_cr'); s.pop('_ep')
# verificări de conținut
b = chess.Board('8/k1P5/2K5/8/8/8/8/8 w - - 0 1'); b.push_uci('c7c8q'); assert b.is_stalemate()
b = chess.Board('8/k1P5/2K5/8/8/8/8/8 w - - 0 1');
for u in ['c7c8r', 'a7a6', 'c8a8']: b.push_uci(u)
assert b.is_checkmate()
assert not bad, bad
open(OUT, 'w', encoding='utf-8').write('/* Exemplele din sertarele lecției „Mutări speciale”.\n   Surse: metoda Steps (Brunia & van Wijgerden), Manualul pasului 1, lecțiile 4, 9 și 14; ChessKid, lecțiile 5 și 14.\n   Generat automat. */\nwindow.L3DEMO = ' + json.dumps(G, ensure_ascii=False) + ';\n')
print('ok', {k: len(v) for k, v in G.items()})
