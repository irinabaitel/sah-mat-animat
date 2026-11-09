# Drawer examples from Steps Manual Step 1, lesson 6 (Check) -> data/nivel1_lectia6_demo.js
import json, sys, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia6_demo.js'

def S(fen, side, text, arrows=(), acts=()):
    return dict(fen=fen, side=side, text=text, arrows=[list(a) for a in arrows], acts=list(acts))
def A(label, move=None, text='', arrows=(), hl=None):
    d = dict(label=label, text=text, arrows=[list(a) for a in arrows])
    if move: d['move'] = move
    if hl: d['hl'] = hl
    return d

G = {}
G['sah'] = [
  S('5k2/8/8/5R2/8/8/8/8', 'b',
    '<p>Turnul alb de pe f5 „privește” pe coloana f până la regele negru de pe f8: regele este atacat.</p>'
    '<p>Atacul asupra regelui are un nume special: <strong>șah</strong>. Regele nu poate fi capturat. De aceea cel care este în șah <strong>trebuie</strong> să scape de șah chiar la mutarea următoare.</p>',
    [('f5', 'f8', 'r')]),
  S('8/8/8/8/8/2b5/8/4K3', 'w',
    '<p>Aici nebunul negru de pe c3 dă șah regelui alb de pe e1, pe diagonala a5–e1.</p>'
    '<p>Când dai șah, se obișnuiește să spui „șah”. Nu e obligatoriu, dar e politicos.</p>',
    [('c3', 'e1', 'r')]),
]
G['fugi'] = [
  S('5k2/8/8/5R2/8/8/8/8', 'b',
    '<p>Regele negru e în șah. Cel mai simplu este să <strong>fugă</strong> pe un pătrat unde turnul nu-l mai atacă.</p><p>Încearcă mutările de mai jos. Una dintre ele este greșită.</p>',
    [('f5', 'f8', 'r')],
    [A('Rg8', 'f8g8', 'Regele a ieșit de pe coloana f. Nu mai este în șah.'),
     A('Re7', 'f8e7', 'Și așa regele iese din șah.'),
     A('Rf7?', 'f8f7', 'Greșit: regele a rămas pe coloana f, deci este tot în șah. Mutarea aceasta nu este permisă.', [('f5', 'f7', 'r')])]),
  S('8/8/8/8/8/2b5/8/4K3', 'w',
    '<p>Regele alb e în șah de la nebun. Unde poate fugi?</p>',
    [('c3', 'e1', 'r')],
    [A('Rf2', 'e1f2', 'Regele a ieșit de pe diagonala nebunului.'),
     A('Rd1', 'e1d1', 'Și așa regele iese din șah.'),
     A('Rd2?', 'e1d2', 'Greșit: d2 este tot pe diagonala nebunului. Regele ar rămâne în șah.', [('c3', 'd2', 'r')])]),
]
G['capt'] = [
  S('R2k4/8/2b5/8/8/8/8/8', 'b',
    '<p>Turnul de pe a8 dă șah. Negrul poate fugi cu regele, dar poate și să <strong>captureze</strong> turnul cu nebunul.</p>',
    [('a8', 'd8', 'r')],
    [A('Nxa8', 'c6a8', 'Nebunul capturează turnul care dădea șah. Este cea mai bună mutare: negrul a câștigat un turn.'),
     A('Re7', 'd8e7', 'Și așa negrul iese din șah, dar capturarea turnului este mai bună.')]),
  S('8/8/8/8/6q1/7P/8/6K1', 'w',
    '<p>Regina neagră de pe g4 dă șah pe coloana g. Ce face albul?</p>',
    [('g4', 'g1', 'r')],
    [A('hxg4', 'h3g4', 'Pionul capturează regina care dădea șah.'),
     A('Rf2', 'g1f2', 'Și așa albul iese din șah, dar pierde ocazia să captureze regina.')]),
  S('8/2Q5/pk6/1p6/8/8/8/8', 'b',
    '<p>Și <strong>regele</strong> poate captura piesa care dă șah, dacă ea nu este apărată.</p><p>Regina albă de pe c7 dă șah regelui negru. Negrul are o singură mutare.</p>',
    [('c7', 'b6', 'r')],
    [A('Rxc7', 'b6c7', 'Regele capturează regina. Regina nu era apărată, deci regele are voie.'),
     A('Ra5?', 'b6a5', 'Greșit: pe a5 regele e tot în șah. După ce regele pleacă de pe b6, regina atacă pe diagonală până la a5.', [('c7', 'a5', 'r')])]),
  S('8/8/5Q2/8/6p1/5b2/7P/6BK', 'w',
    '<p>Nebunul negru de pe f3 dă șah regelui alb de pe h1. Regele nu are unde fugi, iar nicio piesă nu se poate pune în cale.</p>',
    [('f3', 'h1', 'r')],
    [A('Dxf3', 'f6f3', 'Singura mutare: regina capturează nebunul. Păcat, pionul de pe g4 o va captura pe regină. Dar altă mutare nu există.', [('g4', 'f3', 'b')])]),
]
G['bloc'] = [
  S('kb6/1p6/8/8/Q7/8/8/8', 'b',
    '<p>A treia apărare: <strong>pui o piesă în cale</strong>, între rege și piesa care dă șah.</p><p>Regina albă dă șah pe coloana a. Regele negru nu are unde fugi.</p>',
    [('a4', 'a8', 'r')],
    [A('Na7', 'b8a7', 'Nebunul se pune în calea reginei, pe a7. Este singura mutare.')]),
  S('8/8/8/8/8/7N/6PP/4r2K', 'w',
    '<p>Turnul negru dă șah pe linia 1.</p>',
    [('e1', 'h1', 'r')],
    [A('Cg1', 'h3g1', 'Calul se pune în cale, pe g1. Este singura mutare.')]),
  S('8/8/8/8/8/8/8/8', 'w',
    '<p>Ai observat? La o piesă atacată aveam patru apărări. La șah sunt doar <strong>trei</strong>: fugi, capturezi sau pui o piesă în cale.</p>'
    '<p>Apărarea regelui cu altă piesă nu ajută: regele ar rămâne tot în șah.</p>'),
]
G['toate'] = [
  S('4q1k1/8/4Q3/5P2/8/8/8/8', 'b',
    '<p>Aici negrul poate ieși din șah în toate cele trei feluri. Încearcă-le.</p>',
    [('e6', 'g8', 'r')],
    [A('Dxe6', 'e8e6', 'Capturează: regina neagră capturează regina albă. Pionul de pe f5 o recapturează, deci se schimbă reginele.'),
     A('Df7', 'e8f7', 'Pune o piesă în cale: regina se pune pe f7, unde e apărată de rege.'),
     A('Rf8', 'g8f8', 'Fuge: regele merge pe f8. De acolo apără și regina de pe e8.'),
     A('Rh8?', 'g8h8', 'Regele iese din șah, dar regina albă capturează acum regina de pe e8.', [('e6', 'e8', 'r')])]),
  S('8/8/8/8/1p6/r4K2/2N5/8', 'w',
    '<p>Și albul poate ieși din șah în trei feluri.</p>',
    [('a3', 'f3', 'r')],
    [A('Cxa3', 'c2a3', 'Capturează: calul capturează turnul care dădea șah.'),
     A('Ce3', 'c2e3', 'Pune o piesă în cale: calul se pune pe e3.'),
     A('Re2', 'f3e2', 'Fuge: regele merge pe e2.')]),
]
G['best'] = [
  S('8/8/8/8/1B6/2b5/8/K7', 'w',
    '<p>Când poți ieși din șah în mai multe feluri, alege-l pe cel cu care <strong>nu pierzi nimic</strong>.</p><p>Nebunul negru dă șah. Regele poate fugi pe a2 sau b1. Dar e cea mai bună mutare?</p>',
    [('c3', 'a1', 'r')],
    [A('Nxc3', 'b4c3', 'Corect: nebunul alb capturează nebunul care dădea șah.'),
     A('Ra2?', 'a1a2', 'Regele a ieșit din șah, dar nebunul negru capturează acum nebunul de pe b4.', [('c3', 'b4', 'r')])]),
  S('8/7k/8/8/6nR/8/8/8', 'b',
    '<p>Turnul alb dă șah pe coloana h.</p>',
    [('h4', 'h7', 'r')],
    [A('Ch6', 'g4h6', 'Corect: calul se pune în cale, pe h6, unde e apărat de rege.'),
     A('Rg8?', 'h7g8', 'Regele a ieșit din șah, dar turnul capturează acum calul de pe g4.', [('h4', 'g4', 'r')])]),
]
G['regi'] = [
  S('8/8/8/8/1k6/8/1K6/8', 'w',
    '<p>Doi regi nu au voie să stea niciodată unul lângă altul: s-ar ataca unul pe celălalt.</p>'
    '<p>Regele alb nu are voie pe a3, b3 și c3. Nici regele negru nu are voie acolo.</p>',
    (), [A('Arată pătratele interzise', None, 'Pe pătratele roșii nu are voie niciun rege.', hl=dict(safe=[], unsafe=['a3', 'b3', 'c3']))]),
  S('8/8/8/6k1/6bN/6K1/8/8', 'w',
    '<p>Pătratul dintre regi nu trebuie să fie gol. Aici pe g4 stă un nebun, iar regii sunt la distanță de un pătrat. Totul este în regulă.</p>'),
]
# verificare: fiecare mutare din exemple trebuie să fie legală (fără regi, verificăm doar geometria cu python-chess pseudo-legal)
for k, steps in G.items():
    for s in steps:
        b = chess.Board(None); b.set_board_fen(s['fen']); b.turn = s['side'] == 'w'
        for a in s['acts']:
            if 'move' in a:
                m = chess.Move.from_uci(a['move'])
                assert m in b.pseudo_legal_moves, (k, s['fen'], a['move'])
open(OUT, 'w', encoding='utf-8').write('/* Exemplele din sertarele lecției „Atacul asupra regelui”.\n   Sursa: metoda Steps (Brunia & van Wijgerden), Manualul pasului 1, lecția 6.\n   Generat automat. */\nwindow.L6DEMO = ' + json.dumps(G, ensure_ascii=False) + ';\n')
print('ok', {k: len(v) for k, v in G.items()})
