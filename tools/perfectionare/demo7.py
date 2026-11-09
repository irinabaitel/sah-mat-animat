# Drawer examples from Steps Manual Step 1, lessons 7-8 (Mate 1, Mate 2) -> data/nivel1_lectia7_demo.js
import json, sys, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia7_demo.js'

def S(fen, side, text, arrows=(), acts=()):
    return dict(fen=fen, side=side, text=text, arrows=[list(a) for a in arrows], acts=list(acts))
def A(label, move=None, text='', arrows=(), hl=None, mate=None):
    d = dict(label=label, text=text, arrows=[list(a) for a in arrows])
    if move: d['move'] = move
    if hl: d['hl'] = hl
    d['_mate'] = mate  # doar pentru verificare
    return d

G = {}
# ── ACC 0: ce este matul ──
G['mat'] = [
  S('k7/Q7/8/8/8/8/8/8', 'b',
    '<p>Regina albă dă șah regelui negru. Regele nu poate fugi și nicio piesă nu se poate pune în cale.</p>'
    '<p>Dar regele poate <strong>captura</strong> regina: ea nu este apărată.</p>',
    [('a7', 'a8', 'r')],
    [A('Rxa7', 'a8a7', 'Regele capturează regina. Negrul a scăpat de șah.')]),
  S('k7/Q7/1K6/8/8/8/8/8', 'b',
    '<p>Acum regele alb stă pe b6 și o apără pe regină. Regele negru nu mai poate captura regina, nu poate fugi și nicio piesă nu se poate pune în cale.</p>'
    '<p>Regele este în șah și nu poate scăpa de șah. Aceasta este <strong>șah mat</strong> sau, pe scurt, <strong>mat</strong>. Partida s-a terminat: albul a câștigat.</p>',
    [('a7', 'a8', 'r'), ('b6', 'a7', 'g')]),
  S('k7/Q7/1K6/8/8/8/8/8', 'b',
    '<p>„Șah” vine din persană și înseamnă „rege”, iar „mat” înseamnă „mort”.</p>'
    '<p>Regina dă mat pentru că o apără regele. O piesă o <strong>sprijină</strong> pe cealaltă, de aceea îl numim <strong>mat cu sprijin</strong>.</p>'
    '<p>Regele nu se capturează și nu se ia de pe tablă. Cine a primit mat își poate culca regele pe tablă, recunoscând victoria adversarului.</p>'
    '<p>Cine dă mat primește un punct, iar cel care pierde, zero puncte: <strong>1–0</strong> dacă albul câștigă, <strong>0–1</strong> dacă negrul câștigă.</p>',
    [('b6', 'a7', 'g')]),
]
# ── ACC 1: sertare ──
G['sprijin'] = [
  S('8/8/k7/2P5/8/1Q6/8/8', 'w',
    '<p>Mutarea care dă mat se numește <strong>mutare de mat</strong>. Regina albă poate da mat într-o singură mutare. Unde?</p>',
    (), [A('Db6#', 'b3b6', 'Mat! Regina dă șah și îi ia regelui toate pătratele. Pionul de pe c5 o apără, așa că regele nu o poate captura.', [('c5', 'b6', 'g')], mate=True)]),
  S('8/8/8/4b3/8/7K/8/4q3', 'b',
    '<p>Acum negrul dă mat cu regina.</p>',
    (), [A('Dg3#', 'e1g3', 'Mat! Regina stă lângă rege, iar nebunul de pe e5 o apără.', [('e5', 'g3', 'g')], mate=True)]),
  S('8/1QN5/8/k7/8/8/8/8', 'w',
    '<p>Regina trebuie să dea șah și, în același timp, să ia regelui pătratul a4, pe unde ar putea fugi.</p>',
    (), [A('Da6+?', 'b7a6', 'Nu este mat: regina a plecat de pe coloana b, iar regele fuge pe b4.', [('a5', 'b4', 'r')], mate=False),
         A('Db5#', 'b7b5', 'Mat! Regina de pe b5 ține pătratele a4, a6 și b4, iar calul de pe c7 o apără.', [('c7', 'b5', 'g')], mate=True)]),
  S('6r1/8/7p/8/5q2/7K/8/8', 'b',
    '<p>Regele alb nu poate merge nicăieri. Totuși negrul trebuie să aleagă cu grijă șahul.</p>',
    (), [A('Tg3+?', 'g8g3', 'Nu este mat: regele fuge pe h2, pentru că turnul de pe g3 nu ține pătratul acela.', [('h3', 'h2', 'r')], mate=False),
         A('Dg3#', 'f4g3', 'Mat! Regina ține și pătratul h2, iar turnul de pe g8 o apără.', [('g8', 'g3', 'g')], mate=True)]),
]
G['capt'] = [
  S('8/8/8/kpQ5/8/2N5/8/8', 'w',
    '<p>Poți da mat și cu o <strong>captură</strong>.</p>',
    (), [A('Dxb5#', 'c5b5', 'Mat! Regina capturează pionul de pe b5, iar calul de pe c3 o apără.', [('c3', 'b5', 'g')], mate=True)]),
  S('6r1/8/6q1/8/7P/4B3/8/7K', 'b',
    '<p>Dacă adversarul mai are piese pe lângă rege, s-ar putea să se poată apăra. Verifică întotdeauna mutarea înainte s-o faci.</p>',
    (), [A('Dg1+?', 'g6g1', 'Nu este mat: nebunul de pe e3 capturează regina.', [('e3', 'g1', 'r')], mate=False),
         A('Dg2#', 'g6g2', 'Mat! Pe g2 regina nu poate fi capturată decât de rege, iar turnul de pe g8 o apără.', [('g8', 'g2', 'g')], mate=True)]),
]
G['proprii'] = [
  S('k7/pp6/8/8/8/8/2Q5/8', 'w',
    '<p>Pionii negri stau atât de prost încât regina nici nu are nevoie de ajutor.</p>',
    (), [A('Dc8#', 'c2c8', 'Mat! Regele nu poate fugi, pentru că pătratele a7 și b7 sunt ocupate de pionii lui. Acesta este <strong>matul pe ultima linie</strong>.', mate=True)]),
  S('8/5q2/8/6p1/8/6KP/6P1/8', 'b',
    '<p>Aici regina neagră are nevoie de ajutorul pionului ei.</p>',
    (), [A('Df4#', 'f7f4', 'Mat! Pionul de pe g5 apără regina, iar pionii albi de pe g2 și h3 îi încurcă pe propriul rege.', [('g5', 'f4', 'g')], mate=True)]),
  S('8/5q2/8/6p1/8/6KP/6P1/8', 'b',
    '<p>Piesele proprii pot lua regelui multe pătrate. De aceea, la mat, nu trebuie ca adversarul să țină el singur toate pătratele din jurul regelui.</p>'),
]
G['alte'] = [
  S('k7/p1B5/8/1R6/8/8/8/8', 'w',
    '<p>Și celelalte piese pot da mat cu sprijin. Aici dă mat turnul.</p>',
    (), [A('Tb8#', 'b5b8', 'Mat! Turnul stă lângă rege, iar nebunul de pe c7 îl apără.', [('c7', 'b8', 'g')], mate=True)]),
  S('5Bnk/7p/7P/8/8/8/8/8', 'w',
    '<p>Acum dă mat nebunul.</p>',
    (), [A('Ng7#', 'f8g7', 'Mat! Nebunul stă lângă rege, iar pionul de pe h6 îl apără.', [('h6', 'g7', 'g')], mate=True)]),
  S('8/8/8/8/6n1/8/6PP/6NK', 'b',
    '<p>Aici dă mat calul negru.</p>',
    (), [A('Cf2#', 'g4f2', 'Mat! Calul nu poate fi capturat, iar regele alb e închis de propriile piese.', mate=True)]),
  S('8/8/8/8/8/1p6/3r4/KR6', 'b',
    '<p>Și aici dă mat turnul negru.</p>',
    (), [A('Ta2#', 'd2a2', 'Mat! Turnul stă lângă rege, iar pionul de pe b3 îl apără.', [('b3', 'a2', 'g')], mate=True)]),
]
G['adauga'] = [
  S('k7/p7/8/8/8/8/8/8', 'w',
    '<p>Unde ar trebui să stea o <strong>regină albă</strong> ca negrul să primească mat? Gândește-te, apoi apasă butonul.</p>',
    (), [A('Arată pătratul', None, 'Pe c8. De acolo regina dă șah și ține pătratele b7 și b8.', hl=dict(safe=['c8'], unsafe=[]))]),
  S('k1Q5/p7/8/8/8/8/8/8', 'b',
    '<p>Așa: regina de pe c8 dă mat.</p>', [('c8', 'a8', 'r')]),
  S('8/8/8/8/4b3/6P1/7K/8', 'b',
    '<p>Unde ar trebui să stea o <strong>regină neagră</strong> ca albul să primească mat? Există două pătrate bune.</p>',
    (), [A('Arată pătratele', None, 'Pe g2 sau pe h1. Pe ambele pătrate nebunul de pe e4 o apără pe regină.', hl=dict(safe=['g2', 'h1'], unsafe=[]))]),
  S('2Q5/pk6/1p6/8/8/8/8/8', 'b',
    '<p>Regina albă de pe c8 dă șah, dar regele o poate captura. Unde pui un <strong>pion alb</strong> ca să fie mat?</p>',
    [('c8', 'b7', 'r')], [A('Arată pătratul', None, 'Pe d7. Pionul apără regina, iar regele nu o mai poate captura.', hl=dict(safe=['d7'], unsafe=[]))]),
  S('8/8/8/8/8/4b3/8/6rK', 'w',
    '<p>Regele alb este în șah. Pe unde mai poate fugi? Pune acolo un <strong>pion alb</strong> și albul primește mat: propria piesă îi închide drumul.</p>',
    [('g1', 'h1', 'r')], [A('Arată pătratul', None, 'Pe h2. Turnul nu poate fi capturat, pentru că îl apără nebunul de pe e3.', hl=dict(safe=['h2'], unsafe=[]))]),
]
G['paza'] = [
  S('4k3/1R6/8/8/8/8/8/8', 'b',
    '<p>La mat, piesele <strong>lucrează împreună</strong>. Unele <strong>păzesc</strong> pătratele pe unde ar fugi regele, iar alta îl <strong>vânează</strong>: îi dă șah.</p>'
    '<p>Turnul de pe b7 păzește linia 7: regele negru nu poate merge pe d7, e7 și f7. Pe d8 și f8 însă poate.</p>',
    (), [A('Arată pătratele', None, 'Roșu: pătratele păzite de turn. Verde: unde regele mai poate merge.', hl=dict(safe=['d8', 'f8'], unsafe=['d7', 'e7', 'f7']))]),
  S('8/8/8/8/8/8/3q4/5K2', 'w',
    '<p>Regina păzește și mai bine, pentru că ține mai multe pătrate. Aici regele alb mai poate merge doar pe g1.</p>',
    (), [A('Arată pătratele', None, 'Roșu: pătratele păzite de regină. Verde: singurul pătrat liber.', hl=dict(safe=['g1'], unsafe=['e1', 'e2', 'f2', 'g2']))]),
  S('7k/1R6/R7/8/8/8/8/8', 'w',
    '<p>Turnul de pe b7 este <strong>paznicul</strong>. Regele mai poate merge doar pe g8. Turnul de pe a6 este <strong>vânătorul</strong>: el trebuie să dea șah și să ia și pătratul g8.</p>',
    (), [A('Th6+?', 'a6h6', 'Nu este mat: regele fuge pe g8.', [('h8', 'g8', 'r')], mate=False),
         A('Ta8#', 'a6a8', 'Mat! Turnul de pe a8 dă șah și ține și pătratul g8. Turnurile se completează unul pe celălalt.', mate=True)]),
  S('8/8/8/5r2/6r1/8/7K/8', 'b',
    '<p>Un exemplu asemănător, pentru negru.</p>',
    (), [A('Th5#', 'f5h5', 'Mat! Turnul de pe g4 păzește coloana g, iar turnul de pe h5 dă șah pe coloana h. Nici pe h1 regele nu poate fugi: tot pe coloana h ar fi.', mate=True)]),
  S('k7/8/1Q6/8/B7/8/8/8', 'w',
    '<p>Regina păzește, nebunul vânează.</p>',
    (), [A('Nc6#', 'a4c6', 'Mat! Nebunul dă șah pe diagonala c6–a8, iar regina ține pătratele a7, b7 și b8.', mate=True)]),
  S('8/8/8/7q/8/4b3/7P/7K', 'b',
    '<p>Vânătorul trebuie să dea șah și, în același timp, să ia regelui pătratul g2. Nebunul de pe e3 păzește g1.</p>',
    (), [A('Dd1+?', 'h5d1', 'Nu este mat: regele fuge pe g2.', [('h1', 'g2', 'r')], mate=False),
         A('Df3#', 'h5f3', 'Mat! Regina dă șah pe diagonală și ține pătratul g2.', mate=True),
         A('Dd5#', 'h5d5', 'Și așa este mat: regina dă șah de departe, pe diagonala d5–h1.', mate=True)]),
  S('k7/3n4/8/1Q6/8/6B1/8/8', 'w',
    '<p>Unde poate merge regele? Doar pe a7. Nebunul păzește b8, iar regina ține b7 și b8. Regina trebuie să dea șah și să ia pătratul a7, fără să scape din ochi pătratul b7.</p>',
    (), [A('Arată pătratele', None, 'Verde: singurul pătrat liber, a7.', hl=dict(safe=['a7'], unsafe=['b7', 'b8'])),
         A('Da6#', 'b5a6', 'Mat! Regina dă șah și ține a7 și b7, iar nebunul ține b8. Calul de pe d7 nu poate ajuta.', mate=True)]),
]
G['atentie'] = [
  S('3k4/1R4R1/2n5/8/8/8/8/8', 'w',
    '<p>Aici sunt doi paznici pe linia 7. Totuși albul are un singur mat.</p>',
    (), [A('Tb8+?', 'b7b8', 'Nu este mat: calul de pe c6 capturează turnul.', [('c6', 'b8', 'r')], mate=False),
         A('Tg8#', 'g7g8', 'Mat! Pe g8 turnul nu poate fi capturat.', mate=True)]),
  S('8/8/8/8/6B1/8/r6r/4K3', 'b',
    '<p>Acum dă mat negrul.</p>',
    (), [A('Ta1+?', 'a2a1', 'Nu este mat: nebunul se pune în cale, pe d1.', [('g4', 'd1', 'r')], mate=False),
         A('Th1#', 'h2h1', 'Mat! Pe f1 și g1 nicio piesă albă nu se poate pune în cale.', mate=True)]),
  S('6R1/3N3k/7n/8/8/8/8/8', 'w',
    '<p>Pe g8, unde ar putea fugi regele, stă un turn. Regele poate fugi capturându-l.</p>',
    (), [A('Cf8+?', 'd7f8', 'Nu este mat: regele capturează turnul de pe g8.', [('h7', 'g8', 'r')], mate=False),
         A('Cf6#', 'd7f6', 'Mat! Calul face două lucruri: dă șah și apără turnul de pe g8.', [('f6', 'g8', 'g')], mate=True)]),
  S('7k/4R3/8/3BN3/8/8/8/8', 'w',
    '<p>Regele negru nu poate merge nicăieri. Ajunge deci un simplu șah? Nu întotdeauna: vânătorul poate deschide drumul regelui.</p>',
    (), [A('Cf7+?', 'e5f7', 'Nu este mat: calul a închis drumul turnului și al nebunului. Regele poate fugi pe g7, h7 sau g8.', mate=False),
         A('Cg6#', 'e5g6', 'Mat! Calul doar dă șah, iar paznicii, turnul și nebunul, își fac treaba mai departe.', mate=True)]),
]

# ── verificare: fiecare mutare e posibilă, iar „mate” corespunde ──
def board(fen, side):
    b = chess.Board(None); b.set_board_fen(fen); b.turn = side == 'w'; return b
def is_mate_after(b, mv):
    b = b.copy(); b.push(mv)
    them = b.turn
    if b.king(them) is None: return None
    if not b.is_check(): return False
    # mutări legale ale apărătorului: pseudo-legal + regele nu rămâne în șah
    for m in b.pseudo_legal_moves:
        bb = b.copy(); bb.push(m)
        if not bb.is_attacked_by(not them, bb.king(them)): return False
    return True
bad = 0
for k, steps in G.items():
    for s in steps:
        b = board(s['fen'], s['side'])
        for a in s['acts']:
            mt = a.pop('_mate')
            if 'move' in a:
                m = chess.Move.from_uci(a['move'])
                assert m in b.pseudo_legal_moves, (k, s['fen'], a['move'])
                if mt is not None:
                    got = is_mate_after(b, m)
                    if got != mt: print('NEPOTRIVIRE', k, s['fen'], a['move'], 'aștept', mt, 'am', got); bad += 1
assert not bad
open(OUT, 'w', encoding='utf-8').write('/* Exemplele din sertarele lecției „Matul”.\n   Sursa: metoda Steps (Brunia & van Wijgerden), Manualul pasului 1, lecțiile 7 și 8.\n   Generat automat. */\nwindow.L7DEMO = ' + json.dumps(G, ensure_ascii=False) + ';\n')
print('ok', {k: len(v) for k, v in G.items()})
