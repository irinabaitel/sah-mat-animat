# Drawer examples from Steps Manual Step 1, lessons 3 and 5 -> data/nivel1_lectia5_demo.js
import json, sys, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia5_demo.js'

def S(fen, side, text, arrows=(), acts=()):
    return dict(fen=fen, side=side, text=text, arrows=[list(a) for a in arrows], acts=list(acts))
def A(label, move=None, text='', arrows=(), hl=None):
    d = dict(label=label, text=text, arrows=[list(a) for a in arrows])
    if move: d['move'] = move
    if hl: d['hl'] = hl
    return d

G = {}
G['atac'] = [
  S('8/1b6/4b3/8/8/1R5N/8/8', 'w',
    '<p>Turnul de pe b3 „privește” pe coloana b până la nebunul de pe b7. Spunem că turnul <strong>atacă</strong> nebunul.</p>'
    '<p>Dacă albul e la mutare, poate <strong>captura</strong> nebunul: turnul ia locul lui pe b7, iar nebunul iese din joc.</p>'
    '<p>În dreapta, nebunul negru de pe e6 atacă calul de pe h3.</p>',
    [('b3', 'b7', 'r'), ('e6', 'h3', 'b')],
    [A('Albul: Txb7', 'b3b7', 'Turnul a capturat nebunul.'), A('Negrul: Nxh3', 'e6h3', 'Nebunul a capturat calul.')]),
  S('8/7B/Q7/5b2/2r5/8/6nK/8', 'w',
    '<p>Regina de pe a6 atacă turnul de pe c4. Atenție: piesele atacă și înapoi, nu doar înainte.</p>'
    '<p>Nebunii de pe h7 și f5 se atacă unul pe altul. Care pe care îl capturează? Depinde cine e la mutare.</p>'
    '<p>Și regele poate captura: regele de pe h2 atacă calul de pe g2.</p>',
    [('a6', 'c4', 'r'), ('h7', 'f5', 'r'), ('f5', 'h7', 'b'), ('h2', 'g2', 'r')],
    [A('Dxc4', 'a6c4', 'Regina a capturat turnul.'), A('Rxg2', 'h2g2', 'Regele a capturat calul.')]),
  S('8/1b3b2/1n3N2/8/8/1Q3Q2/8/8', 'w',
    '<p>Regina de pe b3 atacă calul de pe b6, dar <strong>nu</strong> și nebunul de pe b7: calul stă în drum. Regina, turnul și nebunul nu pot sări peste piese.</p>'
    '<p>În dreapta, pe f6 stă un cal alb. Nici peste piesele proprii nu se poate sări: regina de pe f3 nu atacă nebunul de pe f7.</p>',
    [('b3', 'b6', 'r')],
    [A('Dxb6', 'b3b6', 'Regina a capturat calul. Abia acum atacă și nebunul.', [('b6', 'b7', 'r')])]),
  S('8/8/n7/4r3/1R2nQ1b/5N2/6B1/8', 'w',
    '<p>Calul capturează la fel ca celelalte piese: calul negru de pe a6 poate captura turnul de pe b4.</p>'
    '<p>Dar calul <strong>sare</strong>. Calul de pe f3 poate captura turnul de pe e5 sau nebunul de pe h4, chiar dacă pe e4 și f4 stau piese în drum. Calul sare peste orice piesă, a lui sau a adversarului.</p>',
    [('a6', 'b4', 'b'), ('f3', 'e5', 'r'), ('f3', 'h4', 'r')],
    [A('Cxe5', 'f3e5', 'Calul a sărit peste piese și a capturat turnul.'), A('Cxh4', 'f3h4', 'Calul a sărit peste piese și a capturat nebunul.')]),
  S('r7/5r2/8/8/7B/1Q6/6R1/8', 'w',
    '<p>Când ataci o piesă, ai grijă ca piesa ta să nu poată fi capturată.</p>'
    '<p>Regina vrea să atace turnul de pe a8. Pe linie sau pe coloană, turnul ar captura-o. Pe diagonală însă turnul nu atacă, deci regina atacă sigur de pe diagonală, de exemplu <strong>Dd5</strong>.</p>'
    '<p>În dreapta, negrul nu atacă turnul alb cu Tg7: turnul alb l-ar captura. Nebunul alb însă poate fi atacat sigur: <strong>Th7</strong> (sau Tf4).</p>',
    [],
    [A('Albul: Dd5', 'b3d5', 'Regina atacă turnul și turnul nu o poate captura.', [('d5', 'a8', 'r')]),
     A('Negrul: Tg7?', 'f7g7', 'Greșit: turnul alb capturează turnul negru.', [('g2', 'g7', 'r')]),
     A('Negrul: Th7', 'f7h7', 'Turnul atacă nebunul și nebunul nu îl poate captura.', [('h7', 'h4', 'b')])]),
  S('8/3r4/8/8/1n6/5B2/8/8', 'w',
    '<p>Cu mai multe piese pe tablă devine mai greu. Nebunul de pe f3 poate ataca turnul de pe d7 din două locuri: c6 și g4.</p>'
    '<p>Pe c6 calul de pe b4 l-ar captura. Mutarea bună este <strong>Ng4</strong>.</p>',
    [],
    [A('Nc6?', 'f3c6', 'Greșit: calul capturează nebunul.', [('b4', 'c6', 'b')]),
     A('Ng4', 'f3g4', 'Nebunul atacă turnul și nu poate fi capturat.', [('g4', 'd7', 'r')])]),
]
G['fugi'] = [
  S('8/8/8/2n5/8/4Q3/8/8', 'b',
    '<p>Calul de pe c5 este atacat de regină. Cea mai simplă apărare: calul <strong>fuge</strong> pe un pătrat sigur.</p><p>Unde poate fugi? Gândește-te, apoi apasă butonul.</p>',
    [('e3', 'c5', 'r')],
    [A('Arată pătratele', None, 'Pătratele sigure (verzi) sunt d7, b7, a6 și a4. Pe b3, d3, e4 și e6 (roșii) regina ar captura calul.',
       hl=dict(safe=['d7', 'b7', 'a6', 'a4'], unsafe=['b3', 'd3', 'e4', 'e6']))]),
]
G['apara'] = [
  S('6r1/8/8/2n5/8/4Q3/8/8', 'b',
    '<p>Acum negrul mai are un turn pe g8. Pe lângă fugă, poate <strong>apăra</strong> calul cu turnul.</p><p>Regina valorează mai mult decât calul, deci albul nu va captura un cal apărat.</p>',
    [('e3', 'c5', 'r')],
    [A('Tc8', 'g8c8', 'Turnul apără calul. Dacă regina capturează calul, turnul o capturează pe ea.', [('c8', 'c5', 'g')]),
     A('Tg5?', 'g8g5', 'Greșit: turnul apără calul, dar el însuși nu e apărat. Regina capturează turnul.', [('e3', 'g5', 'r')])]),
  S('8/8/8/1b1R4/8/8/2n5/8', 'b',
    '<p>Nebunul negru de pe b5 e atacat de turn. Negrul îl poate apăra cu calul. Sau nebunul poate fugi, de exemplu pe a4.</p><p>Când aperi, uită-te și la mutările adversarului.</p>',
    [('d5', 'b5', 'r')],
    [A('Ca3', 'c2a3', 'Calul apără nebunul și stă în siguranță.', [('a3', 'b5', 'g')]),
     A('Cd4?', 'c2d4', 'Greșit: calul apără nebunul, dar acum turnul poate captura calul.', [('d5', 'd4', 'r')])]),
  S('8/8/8/4q2N/8/6P1/8/8', 'w',
    '<p>Regina neagră atacă calul de pe h5. Albul are două apărări bune. Le găsești?</p>',
    [('e5', 'h5', 'b')],
    [A('g4', 'g3g4', 'Pionul apără calul.', [('g4', 'h5', 'g')]),
     A('Cf4', 'h5f4', 'Calul fuge pe f4, unde e apărat de pion.', [('g3', 'f4', 'g')])]),
]
G['capt'] = [
  S('8/1p6/8/2n5/8/1N6/P7/8', 'b',
    '<p>Caii se atacă unul pe altul. Calul alb e apărat de pionul de pe a2. Calul negru nu e apărat.</p>'
    '<p>Negrul poate fugi cu calul, îl poate apăra cu b6 sau poate <strong>captura atacatorul</strong>.</p>',
    [('b3', 'c5', 'r'), ('c5', 'b3', 'b')],
    [A('Cxb3', 'c5b3', 'Calul negru capturează atacatorul. Pionul recapturează, dar schimbul e egal: cal pentru cal.', [('a2', 'b3', 'r')]),
     A('b6', 'b7b6', 'Pionul apără calul.', [('b6', 'c5', 'g')])]),
  S('8/6p1/5n2/8/4R2B/8/8/8', 'w',
    '<p>Turnul de pe e4 e atacat de cal. Albul poate muta turnul sau poate captura atacatorul cu nebunul. Ambele apărări sunt corecte.</p>',
    [('f6', 'e4', 'b')],
    [A('Nxf6', 'h4f6', 'Nebunul capturează calul. Pionul recapturează nebunul, dar turnul e salvat și schimbul e egal.')]),
]
G['bloc'] = [
  S('8/8/2p5/3b4/8/4P3/6Q1/8', 'w',
    '<p>Nebunul de pe d5 atacă regina. Regina poate fugi, de exemplu pe f2. Să captureze nebunul ar fi o greșeală: pionul de pe c6 recapturează, iar regina valorează mult mai mult.</p>'
    '<p>A patra apărare: o piesă se pune <strong>în calea atacului</strong>. Pionul blochează diagonala: e4.</p>',
    [('d5', 'g2', 'b')],
    [A('e4', 'e3e4', 'Pionul stă între nebun și regină. Blocarea o vei folosi mai ales când regele e în șah.'),
     A('Dxd5?', 'g2d5', 'Greșit: pionul recapturează regina.', [('c6', 'd5', 'r')])]),
]
G['recap'] = [
  S('8/8/1p6/q7/8/NPQ5/3P4/8', 'w',
    '<p>Calul de pe a3 e atacat. Câte apărări găsești? Încearcă fiecare buton.</p>',
    [('a5', 'a3', 'b')],
    [A('Fugi: Cc4', 'a3c4', 'Calul fuge pe un pătrat sigur.'),
     A('Capturează: Dxa5', 'c3a5', 'Regina capturează atacatorul. Pionul de pe b6 recapturează, dar schimbul e egal: regină pentru regină.'),
     A('Apără: Db2', 'c3b2', 'Regina apără calul.', [('b2', 'a3', 'g')]),
     A('Face loc: b4', 'b3b4', 'Pionul nu apără el calul, dar face loc reginei: acum regina apără calul.', [('c3', 'a3', 'g')])]),
  S('8/8/4q2N/8/4pP2/4B3/8/8', 'w',
    '<p>Calul de pe h6 e în pericol și nu are niciun pătrat sigur: regina le acoperă pe toate. Ce poate face albul?</p>',
    [('e6', 'h6', 'b')],
    [A('f5', 'f4f5', 'Pionul atacă regina și e apărat de cal. În plus, a făcut loc nebunului: acum nebunul apără calul.', [('f5', 'e6', 'r'), ('e3', 'h6', 'g')])]),
  S('6k1/5r2/6p1/2B3P1/3P4/6P1/3K1R2/8', 'w',
    '<p>Turnul de pe f2 e atacat. Câte mutări bune are albul? Numără-le, apoi verifică.</p>',
    [('f7', 'f2', 'b')],
    [A('Arată toate', None,
       '<ul style="margin:4px 0 4px 18px"><li>fuge: Te2, Tg2, Th2</li><li>capturează: Txf7</li><li>apără: Re3, Re2, Re1</li>'
       '<li>face loc nebunului: d5</li><li>turnul trece pe un pătrat apărat: Tf4, Tf6</li></ul>În total zece mutări bune.')]),
]

# ---- verification ----
def board(fen, side): return chess.Board(fen + ' ' + side + ' - - 0 1')
for k, steps in G.items():
    for i, s in enumerate(steps):
        b = board(s['fen'], s['side'])
        for a in s['acts']:
            if 'move' in a:
                mv = chess.Move.from_uci(a['move'])
                bb = b.copy(); bb.turn = bb.piece_at(mv.from_square).color
                assert mv in bb.pseudo_legal_moves, (k, i, a['label'])
                san = bb.san(mv) if bb.king(bb.turn) is not None or True else ''
for sqs in (['d7', 'b7', 'a6', 'a4'], ['b3', 'd3', 'e4', 'e6']):
    for q in sqs:
        b = board('8/8/8/8/8/4Q3/8/8', 'w'); b.set_piece_at(chess.parse_square(q), chess.Piece.from_symbol('n'))
        print(q, 'attacked' if b.attackers(chess.WHITE, chess.parse_square(q)) else 'safe')
# count position: all ten moves must leave f2-rook (or its new square) not losing material by 1-ply check
b = board('6k1/5r2/6p1/2B3P1/3P4/6P1/3K1R2/8', 'w')
for u in ['f2e2', 'f2g2', 'f2h2', 'f2f7', 'd2e3', 'd2e2', 'd2e1', 'd4d5', 'f2f4', 'f2f6']:
    bb = b.copy(); mv = chess.Move.from_uci(u); assert mv in bb.legal_moves, u; bb.push(mv)
    rsq = [s for s in bb.pieces(chess.ROOK, chess.WHITE)]
    st = [(chess.square_name(s), len(bb.attackers(chess.BLACK, s)), len(bb.attackers(chess.WHITE, s))) for s in rsq]
    print(u, st)
open(OUT, 'w', encoding='utf-8').write('/* Exemplele din sertarele lecției „Atacul, captura, apărarea”.\n   Sursa: metoda Steps (Brunia & van Wijgerden), Manual Step 1, lecțiile 3 și 5. */\nwindow.L5DEMO = ' + json.dumps(G, ensure_ascii=False) + ';\n')
print('ok', {k: len(v) for k, v in G.items()})
