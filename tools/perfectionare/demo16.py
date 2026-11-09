# Exemplele din sertare pentru „Apărarea împotriva matului” -> data/nivel1_lectia16_demo.js
# Surse: Manualul Steps pasul 2, lecția 12; caietul Steps pasul 2, p. 49; ChessKid lecția 11 (șahul dublu).
import json, sys, chess
sys.stdout.reconfigure(encoding='utf-8')
OUT = r'C:/Users/irina/SahMatAnimat/data/nivel1_lectia16_demo.js'

def S(fen, side, text, arrows=(), acts=()):
    return dict(fen=fen, side=side, text=text, arrows=[list(a) for a in arrows], acts=list(acts))
def A(label, move=None, text='', arrows=(), line=None, chk=None):
    """chk: 'def' = după mutare adversarul nu mai are mat într-o mutare; 'fail' = adversarul are mat; 'mate' = mutarea dă mat"""
    d = dict(label=label, text=text, arrows=[list(a) for a in arrows])
    if move: d['move'] = move
    if line: d['line'] = line
    d['_chk'] = chk
    return d

G = {}
# ── ACC 0: matul te pândește ──
G['amenint'] = [
  S('3b1k2/6p1/3q1pQ1/3B4/2P4p/7P/6K1/8', 'b',
    '<p>Albul amenință <strong>Df7 mat</strong>: regina ar da șah pe f7, apărată de nebunul de pe d5.</p>'
    '<p>Negrul e la mutare. Încearcă pe rând apărările de mai jos. Unele sunt bune, altele greșite.</p>',
    [('g6', 'f7', 'r'), ('d5', 'f7', 'r')],
    [A('De7', 'd6e7', '<strong>Protejezi.</strong> Regina apără pătratul f7. Merg la fel de bine Dd7 sau Dc7.', [('e7', 'f7', 'g')], chk='def'),
     A('Dg3+', 'd6g3', '<strong>Capturezi.</strong> Regina neagră se schimbă cu regina albă: după Dxg3 hxg3, Rxg3 piesa care amenința matul a dispărut. Negrul pierde doar un pion.', chk='def'),
     A('Dxd5?', 'd6d5', 'Greșit. Regina capturează nebunul, dar pionul de pe c4 o recapturează (cxd5). Regina e pierdută.', [('c4', 'd5', 'r')]),
     A('De6?', 'd6e6', 'Greșit. Regina se pune între nebun și f7, dar nebunul o capturează (Nxe6).', [('d5', 'e6', 'r')]),
     A('Re7?', 'f8e7', 'Greșit. Regele pleacă, dar Df7 este tot mat. La mat, pătratul amenințat rămâne pe loc, iar regele nu scapă plecând.', [('g6', 'f7', 'r')], chk='fail')]),
]

# ── ACC 1: sertare ──
G['protejezi'] = [
  S('q5k1/5p1p/5QpP/8/8/8/8/8', 'b',
    '<p>Albul amenință mat pe g7: regina ar captura acolo, apărată de pionul de pe h6.</p><p>Cea mai des folosită apărare este să <strong>protejezi</strong> pătratul amenințat.</p>',
    [('f6', 'g7', 'r'), ('h6', 'g7', 'r')],
    [A('Df8', 'a8f8', 'Regina neagră apără acum pătratul g7. Matul nu mai vine.', [('f8', 'g7', 'g')], chk='def')]),
  S('8/8/8/8/8/5bPq/2Q2B1P/6K1', 'w',
    '<p>Negrul amenință <strong>Dg2 mat</strong>, cu regina apărată de nebunul de pe f3.</p><p>Regina albă ar putea apăra g2 de-a lungul liniei a doua, dar îi stă în cale nebunul de pe f2. Albul mută nebunul.</p>',
    [('h3', 'g2', 'r'), ('f3', 'g2', 'r')],
    [A('Ne3', 'f2e3', 'Nebunul a plecat de pe f2, iar regina de pe c2 apără acum g2. Merge orice mutare a nebunului de pe f2.', [('c2', 'g2', 'g')], chk='def')]),
  S('6k1/3q1b1p/6pQ/4B3/8/8/8/8', 'b',
    '<p>Albul amenință <strong>Dg7 mat</strong>, cu regina apărată de nebunul de pe e5.</p><p>Regina neagră ar apăra g7 pe linia a 7-a, dar nebunul ei de pe f7 îi stă în cale. Nu trebuie să muți regina: îi faci loc.</p>',
    [('h6', 'g7', 'r'), ('e5', 'g7', 'r')],
    [A('Ne6', 'f7e6', 'Nebunul pleacă de pe f7, iar regina de pe d7 apără g7. Linia a 7-a s-a eliberat.', [('d7', 'g7', 'g')], chk='def')]),
]
G['razex'] = [
  S('1q4k1/1p3p1p/2n2QpB/8/8/8/8/8', 'b',
    '<p>Albul amenință <strong>Dg7 mat</strong>. Negrul poate apăra g7 în două feluri. Unul e bun, celălalt nu.</p>',
    [('f6', 'g7', 'r'), ('h6', 'g7', 'r')],
    [A('Df8?', 'b8f8', 'Regina apără g7, dar nebunul de pe h6 o capturează (Nxf8). Negrul pierde regina.', [('h6', 'f8', 'r')], chk='def'),
     A('De5!', 'b8e5', 'Mutarea surpriză. Regina de pe e5 se uită spre g7 <strong>prin</strong> regina albă. Dacă regina albă capturează pe g7, regina neagră o recapturează. Spunem că apără „prin raze X”.', [('e5', 'g7', 'g')], chk='def')]),
  S('8/8/8/8/4r3/5Q2/6PP/R3q2K', 'w',
    '<p>Regina neagră de pe e1 dă șah. Albul se pune în cale cu regina.</p>',
    [('e1', 'h1', 'r')],
    [A('Df1', 'f3f1', 'Regina albă se pune în cale. Dacă regina neagră o capturează, turnul de pe a1 recapturează: îl apără prin regina neagră, prin raze X.', [('a1', 'f1', 'g')], chk='def')]),
  S('8/8/8/8/8/2N2qPb/1P3P1P/4Q1K1', 'w',
    '<p>Negrul amenință <strong>Dg2 mat</strong>, cu regina apărată de nebunul de pe h3.</p>',
    [('f3', 'g2', 'r'), ('h3', 'g2', 'r')],
    [A('Df1?', 'e1f1', 'Regina apără g2, dar nebunul o capturează (Nxf1). Albul pierde regina pentru un nebun.', [('h3', 'f1', 'r')], chk='def'),
     A('De4!', 'e1e4', 'Regina albă apără g2 prin regina neagră. Dacă negrul dă Dg2+, regina albă o capturează. Iar dacă negrul capturează pe e4, calul recapturează.', [('e4', 'g2', 'g')], chk='def')]),
  S('8/1Q1R1ppk/8/3P4/4q2n/8/1P4PP/6BK', 'w',
    '<p>Negrul amenință <strong>Dg2 mat</strong>, cu regina apărată de calul de pe h4. Nu e ușor de apărat g2.</p>',
    [('e4', 'g2', 'r'), ('h4', 'g2', 'r')],
    [A('d6', 'd5d6', 'Pionul înaintează și deschide diagonala. Regina de pe b7 apără acum g2 prin regina neagră.', [('b7', 'g2', 'g')], chk='def')]),
]
G['tempo'] = [
  S('6k1/1p5p/2p2p2/2B5/1P6/P4bPq/2Q2P1P/6K1', 'w',
    '<p>Negrul amenință <strong>Dg2 mat</strong>. Albul ar vrea să-și aducă regina pe f1, dar de pe c2 nu ajunge acolo într-o singură mutare.</p>',
    [('h3', 'g2', 'r'), ('f3', 'g2', 'r')],
    [A('Dc4+ și Df1', line=['c2c4', 'g8g7', 'c4f1'], text='Albul dă întâi șah. Negrul trebuie să răspundă la șah, iar albul câștigă o mutare: regina ajunge pe f1 și apără g2.', chk='def'),
     A('Db3+?', line=['c2b3', 'f3d5'], text='Șah, dar nebunul se pune în cale pe d5, iar regina albă nu mai ajunge pe f1. Matul pe g2 rămâne.')]),
]
G['capturezi'] = [
  S('1k6/p1p5/QnP5/8/3q4/8/1P6/KN6', 'b',
    '<p>Albul amenință <strong>Db7 mat</strong>, cu regina apărată de pionul de pe c6.</p><p>O apărare isteață este să <strong>capturezi</strong> unul dintre atacatori.</p>',
    [('a6', 'b7', 'r'), ('c6', 'b7', 'r')],
    [A('Da4+', 'd4a4', 'Regina neagră dă șah și se oferă la schimb. După Dxa4 Cxa4 regina albă a dispărut, deci și matul.', chk='def')]),
  S('8/5Q2/8/8/5Rn1/7q/5P1P/7K', 'w',
    '<p>Negrul amenință mat pe h2 și pe f1. Calul de pe g4 apără h2.</p>',
    [('h3', 'h2', 'r'), ('h3', 'f1', 'r')],
    [A('Txg4', 'f4g4', 'Turnul capturează calul. Albul dă un turn pe un cal, deci pierde puțin material, dar asta e mai bine decât să primească mat.', chk='def')]),
  S('6k1/RR6/2p5/1r1n4/8/8/8/8', 'b',
    '<p>Albul amenință <strong>Ta8 mat</strong>. Negrul nu poate împiedica mutarea Ta8, dar poate captura <strong>paznicul</strong>: turnul de pe b7 ține linia a 7-a.</p>',
    [('a7', 'a8', 'r'), ('b7', 'g7', 'r')],
    [A('Txb7', 'b5b7', 'Turnul negru se schimbă cu paznicul. Acum regele are din nou pătrate libere pe linia a 7-a.', chk='def')]),
  S('8/8/8/8/6p1/5n2/4r2P/R4R1K', 'w',
    '<p>Negrul amenință <strong>Txh2 mat</strong>, cu turnul apărat de calul de pe f3.</p>',
    [('e2', 'h2', 'r'), ('f3', 'h2', 'r')],
    [A('Txf3', 'f1f3', 'Turnul capturează calul care îl ajută pe turnul negru. Pionul recapturează, deci albul pierde material, dar scapă de mat.', chk='def')]),
]
G['pleci'] = [
  S('8/8/8/8/3b4/1Pq5/P1P5/1K1Q4', 'w',
    '<p>Negrul amenință mat pe b2 și pe a1. Pare că albul trebuie să cedeze.</p>',
    [('c3', 'b2', 'r'), ('c3', 'a1', 'r')],
    [A('Dc1?', 'd1c1', 'Regina apără b2, dar nu și a1: Da1 este mat.', [('c3', 'a1', 'r')], chk='fail'),
     A('Dxd4?', 'd1d4', 'Matul nu mai vine, dar regina neagră o capturează pe cea albă (Dxd4).', chk='def'),
     A('Rc1', 'b1c1', 'Regele se salvează singur: <strong>pleacă</strong>. Negrul nu mai poate da mat.', chk='def')]),
  S('7k/6pp/8/6N1/8/8/4R3/8', 'b',
    '<p>Albul amenință <strong>Te8 mat</strong> pe ultima linie, iar calul de pe g5 îi ia regelui pătratul h7.</p>',
    [('e2', 'e8', 'r')],
    [A('Rg8?', 'h8g8', 'Plecarea regelui nu ajută: Te8 este tot mat.', [('e2', 'e8', 'r')], chk='fail'),
     A('g6', 'g7g6', 'Negrul îi face regelui loc: după g6, regele poate pleca pe g7.', [('h8', 'g7', 'g')], chk='def')]),
  S('7k/4q1p1/6Qn/6N1/8/8/8/8', 'b',
    '<p>Albul amenință <strong>Dh7 mat</strong>, cu regina apărată de calul de pe g5.</p>',
    [('g6', 'h7', 'r'), ('g5', 'h7', 'r')],
    [A('Rg8 …', line=['h8g8', 'g6h7', 'g8f8', 'h7h8', 'h6g8'], text='Regele pleacă pe g8 ca să se apere. După Dh7+ Rf8 și Dh8+, negrul se salvează punând calul în cale pe g8.', chk='def')]),
  S('8/8/8/8/3q4/8/PP6/K7', 'w',
    '<p>Negrul amenință <strong>Dd1 mat</strong> pe prima linie.</p>',
    [('d4', 'd1', 'r')],
    [A('Rb1?', 'a1b1', 'Regele pleacă, dar tot pe prima linie: Dd1 este mat.', [('d4', 'd1', 'r')], chk='fail'),
     A('a3', 'a2a3', 'Albul îi face regelui loc pe a2. Acum nu mai e mat.', [('a1', 'a2', 'g')], chk='def')]),
]
G['incale'] = [
  S('1k6/p1p5/Qp1q4/3B4/2P5/8/8/8', 'b',
    '<p>Albul amenință <strong>Db7 mat</strong>, cu regina apărată de nebunul de pe d5. Nebunul nu poate fi capturat: îl apără pionul de pe c4.</p>',
    [('a6', 'b7', 'r'), ('d5', 'b7', 'r')],
    [A('c6', 'c7c6', 'Pionul <strong>se pune în cale</strong> între nebun și b7. Regina albă nu mai e apărată pe b7.', chk='def')]),
  S('5r2/6R1/8/8/8/7b/7P/6K1', 'w',
    '<p>Negrul amenință <strong>Tf1 mat</strong>, cu turnul apărat de nebunul de pe h3.</p>',
    [('f8', 'f1', 'r'), ('h3', 'f1', 'r')],
    [A('Tg2?', 'g7g2', 'Turnul apără, dar nebunul îl capturează (Nxg2). Albul pierde turnul.', [('h3', 'g2', 'r')], chk='def'),
     A('Rh1 …', line=['g1h1', 'f8f1', 'g7g1'], text='Regele face loc turnului. După Tf1+, turnul alb se pune în cale pe g1 și matul nu mai vine.', chk='def')]),
  S('8/1R1P4/5Bp1/2p3P1/p7/P3kn1p/r6P/5K2', 'w',
    '<p>Negrul amenință <strong>Tf2 mat</strong>.</p>',
    [('a2', 'f2', 'r')],
    [A('Tb2?', 'b7b2', 'Turnul atacă turnul negru, dar acum nebunul nu mai apără a1: urmează Ta1+.', [('a2', 'a1', 'r')]),
     A('Nb2', 'f6b2', 'Nebunul <strong>se pune în cale</strong> pe b2. Turnul negru e închis și nu mai poate da mat.', chk='def')]),
]
G['cauta'] = [
  S('4rr1k/1bb3pp/p2q4/1p6/8/1BP4P/PPQNRPP1/4R2K', 'w',
    '<p>Caută întâi <strong>pătratul</strong> unde vine matul. Aici negrul vrea <strong>Dh2 mat</strong>, cu regina apărată de nebunul de pe c7.</p>'
    '<p>Apoi treci prin toate apărările: protejezi? capturezi? te pui în cale? pleci cu regele?</p>',
    [('d6', 'h2', 'r'), ('c7', 'h2', 'r')],
    [A('Rg1?', line=['h1g1', 'd6h2', 'g1f1', 'h2h1'], text='Regele pleacă, dar matul îl ajunge din urmă: Dh2+ Rf1 Dh1 mat.', chk=None),
     A('Cf1', 'd2f1', 'Calul apără h2. Mutarea simplă e cea bună.', [('f1', 'h2', 'g')], chk='def')]),
]
G['dublu'] = [
  S('q3r2k/6pp/8/3Q2N1/8/8/6PP/7K', 'w',
    '<p>Aici e invers: albul atacă. Negrul amenință Te1 mat, așa că albul trebuie să dea șah după șah.</p>',
    [('e8', 'e1', 'r')],
    [A('Cf7+ Rg8 Ch6++', line=['g5f7', 'h8g8', 'f7h6'], text='Calul pleacă de pe f7 și dă șah, iar în același timp deschide drumul reginei, care dă și ea șah. Sunt <strong>două șahuri deodată</strong>: un <strong>șah dublu</strong>.')]),
  S('q3r1k1/6pp/7N/3Q4/8/8/6PP/7K', 'b',
    '<p>Regele negru primește șah de la cal și de la regină în același timp.</p>'
    '<p>Negrul nu poate captura ambele piese dintr-o mutare și nici nu se poate pune în cale pe două linii. La șah dublu, <strong>doar regele se poate muta</strong>.</p>',
    [('h6', 'g8', 'r'), ('d5', 'g8', 'r')],
    [A('Rh8', 'g8h8', 'Regele pleacă. Capturarea calului (gxh6) nu era permisă: regina tot ar fi dat șah.'),
     A('Rh8 Dg8+ Txg8 Cf7#', line=['g8h8', 'd5g8', 'e8g8', 'h6f7'], text='Albul jertfește regina, iar calul dă mat. Regele e închis de piesele lui, ca într-o cutie.', chk='mate')]),
  S('r1b1k2r/ppp1qppp/3p1B2/2b1n3/8/2NP4/PPP2PPP/R2QKBNR', 'b',
    '<p>Ambele piese negre care vor da șah pot fi capturate. Contează?</p>',
    (),
    [A('Cf3++', 'e5f3', 'Calul dă șah, iar regina de pe e7 dă și ea șah pe coloana e. E mat, deși albul ar putea captura calul sau regina: la șah dublu, capturarea unei singure piese nu ajută.', chk='mate')]),
]

# ═════════ verificare ═════════
def board(fen, side):
    b = chess.Board(None); b.set_board_fen(fen); b.turn = side == 'w'; return b
def safe_after(b, m):
    bb = b.copy(stack=False); bb.push(m); k = bb.king(not bb.turn)
    return k is None or not bb.is_attacked_by(bb.turn, k)
def mated(b):
    k = b.king(b.turn)
    if k is None or not b.is_attacked_by(not b.turn, k): return False
    return not any(safe_after(b, m) for m in b.pseudo_legal_moves)
def mates(b):
    out = []
    for m in b.pseudo_legal_moves:
        if not safe_after(b, m): continue
        bb = b.copy(stack=False); bb.push(m)
        if mated(bb): out.append(m.uci())
    return out
bad = 0
for k, steps in G.items():
    for s in steps:
        for a in s['acts']:
            chk = a.pop('_chk')
            b = board(s['fen'], s['side'])
            seq = a.get('line') or [a['move']]
            for u in seq:
                m = chess.Move.from_uci(u)
                if m not in b.pseudo_legal_moves or not safe_after(b, m):
                    print('ILEGAL', k, a['label'], u); bad += 1; break
                b.push(m)
            if chk == 'mate' and not mated(b): print('NU E MAT', k, a['label']); bad += 1
            if chk == 'def' and mates(b): print('MAT POSIBIL', k, a['label'], mates(b)); bad += 1
            if chk == 'fail' and not mates(b): print('NU E MAT DUPĂ GREȘEALĂ', k, a['label']); bad += 1
        # amenințarea de la începutul exemplului (pentru exemplele cu apărare)
        if k not in ('dublu',):
            b = board(s['fen'], 'b' if s['side'] == 'w' else 'w')
            if not mates(b) and not b.is_check(): print('fără amenințare de mat într-o mutare:', k, s['fen'])
assert not bad, bad
open(OUT, 'w', encoding='utf-8').write('/* Exemplele din sertarele lecției „Apărarea împotriva matului”.\n   Surse: metoda Steps (Brunia & van Wijgerden), Manualul și caietul pasului 2, lecția 12; ChessKid, lecția 11.\n   Generat automat. */\nwindow.L16DEMO = ' + json.dumps(G, ensure_ascii=False) + ';\n')
print('ok', {k: len(v) for k, v in G.items()})
