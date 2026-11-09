# nivel1_lectia6.html (model cu regi) -> nivel1_lectia7.html (Matul)
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = r'C:/Users/irina/SahMatAnimat/'
s = open(R + 'nivel1_lectia6.html', encoding='utf-8').read()
def sub(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)
def resub(pat, new):
    global s
    s2, n = re.subn(pat, lambda m: new, s, flags=re.S)
    assert n == 1, (n, pat[:80]); s = s2

sub('<title>Atacul asupra regelui</title>', '<title>Matul</title>')
sub('<span class="header-title">Atacul asupra regelui</span>', '<span class="header-title">Matul</span>')

# ── acordeonul 0: ce este matul ──
resub(r'<!-- ── ACC 0: ȘAHUL ── -->.*?<!-- ── ACC 1: IEȘIREA DIN ȘAH ── -->', '''<!-- ── ACC 0: MATUL ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc0" onclick="toggleAcc(0)"><span>👑 Ce este matul?</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body0"><div class="acc-inner">
              <p>Atunci când regele este în șah și nu poate scăpa de șah, adică nu are unde să plece, nicio piesă nu se poate pune în cale și piesa care dă șah nu poate fi capturată, se spune că este <strong>șah mat</strong>. Acesta este scopul jocului: să-i dai mat regelui advers.</p>
              <div id="g-mat-text"></div>
              <div id="g-mat-act"></div>
              <div class="ex-step-nav" id="g-mat-nav"></div>
              <div class="hl-box warn"><strong>Mat = șah + regele nu are scăpare.</strong> Înainte să spui „mat”, verifică cele trei ieșiri din șah: poate regele pleca? Poate fi capturată piesa care dă șah? Se poate pune o piesă în cale?</div>
            </div></div>
          </div>

          <!-- ── ACC 1: CUM DAI MAT ── -->''')
sub('''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🛡️ Ieșirea din șah</span><span class="acc-icon">▶</span></div>''',
    '''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>♛ Cum dai mat</span><span class="acc-icon">▶</span></div>''')
sub('''<p>Din șah ieși în trei feluri: <strong>pleca</strong> cu regele, <strong>capturezi</strong> piesa care dă șah sau <strong>pui o piesă în cale</strong>. Dacă poți alege, alege mutarea cu care nu pierzi nimic.</p>''',
    '''<p>La mat, piesele lucrează împreună. Una dă șah, iar celelalte o apără sau păzesc pătratele pe unde ar putea pleca regele. Uneori chiar piesele regelui îi închid drumul.</p>''')
sub('<p class="src-note">Exercițiile vin din programul Chess Tutor Step 1, din caietul metodei Steps și din lecțiile ChessKid.</p>',
    '<p class="src-note">Exercițiile vin din programul Chess Tutor Step 1, din caietul metodei Steps și din lecțiile ChessKid.</p>')

# ── Exersează ──
resub(r'<p>Alege un joc: îl poți juca împotriva Robotului sau în doi, cu un coleg\.</p>.*?</div></div>\n          </div>\n        </div><!-- /acc-wrapper -->', '''<p>Alege un joc sau intră în arenă.</p>
              <a href="nivel1_joc_vanatoarea_regelui.html" class="practice-btn pb-blue">👑 Vânătoarea regelui<small>Ai toată armata albă, iar regele negru e singur. Îi dai mat înainte să scape?</small></a>
              <a href="pagina5.html" class="practice-btn pb-green">♟ Arena de mat<small>Probleme de mat în 1, 2, 3 și 4 mutări</small></a>
              <a href="nivel1_joc_scapa_de_dame.html" class="practice-btn pb-purple">♛ Scapă de dame<small>Calul pleacă de două regine</small></a>
            </div></div>
          </div>
        </div><!-- /acc-wrapper -->''')

sub('<a href="nivel1_lectia5.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Atacul, captura, apărarea</span></a>',
    '<a href="nivel1_lectia15.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Numărarea atacatorilor</span></a>')
sub('<a href="pagina4.html" class="nav-btn nav-btn--forward"><span class="label">Șahul dublu</span>',
    '<a href="aparare_mat.html" class="nav-btn nav-btn--forward"><span class="label">Apărarea împotriva matului</span>')
sub('<script src="data/nivel1_lectia6_demo.js?v=1"></script>\n<script src="data/nivel1_lectia6_ex.js?v=1"></script>',
    '<script src="data/nivel1_lectia7_demo.js?v=1"></script>\n<script src="data/nivel1_lectia7_ex.js?v=1"></script>')
s = s.replace('L6DEMO', 'L7DEMO').replace('L6EX', 'L7EX')
sub("const SAVE_KEY = 'n1l6_ex_v1';", "const SAVE_KEY = 'n1l7_ex_v1';")
resub(r"const TAB_DESC = \{.*?\};", """const TAB_DESC = {
  baza: 'E mat sau nu? Mat într-o mutare și „adaugă piesa”, din caietul metodei Steps.',
  mediu: 'Exercițiile din Chess Tutor: mat într-o mutare, paznicul și vânătorul, adaugă piesa.',
  avansat: 'Exercițiile suplimentare din Chess Tutor, cu poziții din partide adevărate.'
};""")
resub(r"const DEF_GROUPS = \[.*?\];", """const DEF_GROUPS = [
  ['sprijin', '🤝 Matul cu sprijin'],
  ['capt',    '⚔️ Mat cu captură'],
  ['proprii', '🧱 Piesele proprii îl încurcă'],
  ['alte',    '♜ Mat cu turnul, nebunul, calul'],
  ['adauga',  '➕ Unde pui piesa?'],
  ['paza',    '🛡️ Paznicul și vânătorul'],
  ['atentie', '⚠️ Nu orice șah este mat']
];""")
sub("+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Step 1, lecția 6.</p>';",
    "+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Step 1, lecțiile 7 și 8.</p>';")
sub("if (accOpen === 0) renderGroup('sah');", "if (accOpen === 0) renderGroup('mat');")

# ═════════ motorul: mat, promovare, tipurile noi ═════════
sub("function capturers(p, s) {", """function movesOf(p, c) {
  const out = [];
  Object.keys(p).forEach(f => { if (p[f][0] === c) targets(p, f).forEach(t => { if (legalMove(p, f, t)) out.push([f, t]); }); });
  return out;
}
function isMated(p, c) { return inCheck(p, c) && movesOf(p, c).length === 0; }
function kingsApart(p) { const a = kingSq(p, 'w'), b = kingSq(p, 'b'); if (!a || !b) return true; const [x1, y1] = xy(a), [x2, y2] = xy(b); return Math.max(Math.abs(x1 - x2), Math.abs(y1 - y2)) > 1; }
/* de ce nu e mat: prima scăpare găsită */
function whyNotMate(p, c) {
  if (!inCheck(p, c)) return 'Regele nu este în șah, deci nu este mat.';
  const k = kingSq(p, c), mv = movesOf(p, c), ch = attackers(p, k, opp(c));
  const run = mv.find(m => m[0] === k && !p[m[1]]);
  if (run) return 'Nu este mat: regele pleacă pe ' + run[1] + '.';
  const capt = mv.find(m => ch.includes(m[1]));
  if (capt) return 'Nu este mat: ' + (capt[0] === k ? 'regele' : NAME[p[capt[0]][1]] + ' de pe ' + capt[0]) + ' capturează ' + NAME[p[capt[1]][1]] + (p[capt[1]][1] === 'Q' ? 'a' : '') + ' de pe ' + capt[1] + '.';
  const kc = mv.find(m => m[0] === k);
  if (kc) return 'Nu este mat: regele capturează ' + NAME[p[kc[1]][1]] + ' de pe ' + kc[1] + '.';
  const bl = mv[0];
  return 'Nu este mat: ' + NAME[p[bl[0]][1]] + ' de pe ' + bl[0] + ' se pune în cale, pe ' + bl[1] + '.';
}
function capturers(p, s) {""")

# mutarea cu promovare la alegere (tipul move)
sub("""function attempt(f, t) {
  if (!targets(pos, f).includes(t)) { warn('Piesa nu se poate muta pe ' + t + '.'); return false; }""",
    """function attempt(f, t) {
  if (!targets(pos, f).includes(t)) { warn('Piesa nu se poate muta pe ' + t + '.'); return false; }
  if (T.type === 'move' && pos[f][1] === 'P' && /[18]/.test(t[1])) {
    if (inCheck(applyMove(pos, f, t), T.side)) { fail('❌ Mutarea nu este permisă: regele tău ar rămâne în șah.'); return false; }
    st.pend = [f, t];
    document.getElementById('ex-opts').innerHTML = '<p class="set-intro">Pionul ajunge pe ultima linie. În ce piesă se transformă?</p><div class="opt-row">'
      + [['Q', 'Regină'], ['R', 'Turn'], ['B', 'Nebun'], ['N', 'Cal']].map(x => '<button class="opt-btn" onclick="pickPromo(\\'' + x[0] + '\\')">' + x[1] + '</button>').join('') + '</div>';
    warn('Alege piesa în care se transformă pionul.');
    return false;
  }""")
sub("""  const [f, t] = st.pend; st.pend = null;
  routeMove(f, t, x); board.position(pos, false);""",
    """  const [f, t] = st.pend; st.pend = null;
  if (T.type === 'move') { document.getElementById('ex-opts').innerHTML = ''; moveTask(f, t, x); board.position(pos, false); return; }
  routeMove(f, t, x); board.position(pos, false);""")

sub("""function moveTask(f, t) {
  const uci = f + t, side = T.side, np = applyMove(pos, f, t), capt = !!pos[t];""",
    """function moveTask(f, t, pr) {
  const uci = f + t + (pr ? pr.toLowerCase() : ''), side = T.side, np = applyMove(pos, f, t), capt = !!pos[t];
  if (pr) np[t] = side + pr;
  if (T.check === 'mate') {
    if (inCheck(np, side)) { fail(inCheck(pos, side) ? '❌ După mutarea aceasta regele tău este tot în șah.' : '❌ Mutarea nu este permisă: regele tău ar ajunge în șah.'); return false; }
    if (isMated(np, opp(side))) {
      clearHint(); clearMarks(); pos = np; playSnd(sndCapture);
      setTimeout(() => markChecks(pos), 60);
      success(uci === T.answer ? 'Mat! ' + (T.expl || '') : 'Mat! Și aceasta este o mutare bună.');
      return true;
    }
    fail('❌ ' + whyNotMate(np, opp(side)) + ' Mai încearcă!');
    return false;
  }""")

# ── tipurile noi: addmate (pune piesa / piesele) și mateq (este mat?) ──
sub("""  else if (T.type === 'nocircle') {
    T.circles.forEach(s => mark(s, 'sq-circle'));""",
    """  else if (T.type === 'addmate') {
    st.placed = {}; st.sel = 0;
    (T.cross || []).forEach(q => mark(q, 'sq-box'));
    renderAddPieces();
  }
  else if (T.type === 'mateq') {
    markChecks(pos);
    o.innerHTML = optButtons(['Da', 'Nu']);
  }
  else if (T.type === 'nocircle') {
    T.circles.forEach(s => mark(s, 'sq-circle'));""")
sub("""function optButtons(list) {""", """function pieceImg(p) { return '<img src="' + PIECE_THEME.replace('{piece}', p) + '" alt="" style="width:40px;height:40px;display:block">'; }
function renderAddPieces() {
  const used = Object.values(st.placed);
  document.getElementById('ex-opts').innerHTML = '<div class="opt-row">' + T.pieces.map((p, i) => {
    const on = Object.keys(st.placed).find(q => st.placed[q] === i) ;
    return '<button class="opt-btn' + (i === st.sel ? ' sel' : '') + '" style="padding:4px 8px' + (on ? ';opacity:.45' : '') + '" onclick="selAdd(' + i + ')" title="' + NAME[p[1]] + '">' + pieceImg(p) + '</button>';
  }).join('') + '</div><p class="set-intro" style="margin-top:6px">' + (T.pieces.length > 1 ? 'Alege o piesă, apoi atinge un pătrat albastru. Poți muta o piesă pusă greșit.' : 'Atinge pătratul unde pui piesa. O poți muta oricând pe alt pătrat.') + '</p>';
}
function selAdd(i) { st.sel = i; renderAddPieces(); }
function addPos() { const p = fenToPos(T.fen); Object.keys(st.placed).forEach(q => p[q] = T.pieces[st.placed[q]]); return p; }
function clickAdd(s) {
  if (T.cross && !T.cross.includes(s)) { warn('Pune piesele numai pe pătratele albastre.'); return; }
  const base = fenToPos(T.fen);
  if (base[s]) { warn('Pe ' + s + ' stă deja o piesă. Alege un pătrat liber.'); return; }
  const p = T.pieces[st.sel];
  if (p[1] === 'P' && /[18]/.test(s[1])) { warn('Un pion nu poate sta pe prima sau pe ultima linie.'); return; }
  Object.keys(st.placed).forEach(q => { if (st.placed[q] === st.sel || q === s) delete st.placed[q]; });
  st.placed[s] = st.sel;
  pos = addPos(); board.position(pos, false); playSnd(sndMove); clearHint();
  clearMarks(); (T.cross || []).forEach(q => mark(q, 'sq-box'));
  const free = T.pieces.findIndex((x, i) => !Object.values(st.placed).includes(i));
  if (free >= 0) { st.sel = free; renderAddPieces(); clearFeedback(); return; }
  renderAddPieces();
  setTimeout(() => markChecks(pos), 30);
  if (!kingsApart(pos)) { fail('❌ Regii nu au voie să stea unul lângă altul.'); return; }
  if (inCheck(pos, T.side)) { fail('❌ Acum regele care dă mat ar fi el însuși în șah. Mută piesele.'); return; }
  if (isMated(pos, T.defender)) { success('Mat! ' + T.expl); return; }
  fail('❌ ' + whyNotMate(pos, T.defender) + (T.pieces.length > 1 ? ' Schimbă piesele între ele.' : ' Mută piesa pe alt pătrat.'));
}
function optButtons(list) {""")
sub("  if (T.type === 'place') return clickPlace(s);\n  if (T.type === 'clicksq') return clickNamed(s);",
    "  if (T.type === 'place') return clickPlace(s);\n  if (T.type === 'addmate') return clickAdd(s);\n  if (T.type === 'clicksq') return clickNamed(s);")
sub("if (['move', 'route', 'squares', 'marks', 'place', 'checksq'].includes(T.type)) tools.push('<button class=\"tool-btn\" onclick=\"giveHint()\">💡 Indiciu</button>');",
    "if (['move', 'route', 'squares', 'marks', 'place', 'checksq', 'addmate'].includes(T.type)) tools.push('<button class=\"tool-btn\" onclick=\"giveHint()\">💡 Indiciu</button>');")
sub("if (['route', 'marks', 'place', 'squares', 'checksq'].includes(T.type)) tools.push('<button class=\"tool-btn\" onclick=\"loadTask()\">↺ Din nou</button>');",
    "if (['route', 'marks', 'place', 'squares', 'checksq', 'addmate'].includes(T.type)) tools.push('<button class=\"tool-btn\" onclick=\"loadTask()\">↺ Din nou</button>');")
sub("""  else if (T.type === 'yesno') {
    ok = (v === 'Da') === T.answer;""", """  else if (T.type === 'mateq') {
    ok = (v === 'Da') === T.answer; okMsg = T.expl;
    badMsg = T.answer ? 'Mai uită-te: are regele vreo scăpare? Încearcă toate cele trei ieșiri din șah.' : 'Mai uită-te: regele are o scăpare. Caut-o.';
  }
  else if (T.type === 'yesno') {
    ok = (v === 'Da') === T.answer;""")
sub("""  if (T.type === 'place') {
    const s = Object.keys(T.solution).find(q => st.placed[q] !== T.solution[q]);""", """  if (T.type === 'addmate') {
    const s = Object.keys(T.solution).find(q => st.placed[q] === undefined || T.pieces[st.placed[q]] !== T.solution[q]);
    if (!s) return;
    hintStage++; clearHint(); mark(s, 'hint-square');
    const pn = NAME[T.solution[s][1]];
    if (T.pieces.length === 1) warn(hintStage === 1 ? '💡 Pune piesa pe pătratul <strong>verde</strong>.' : '💡 ' + cap(pn) + ' merge pe <strong>' + s + '</strong>.');
    else warn('💡 Pe pătratul verde stă ' + pn + (T.solution[s][0] === 'w' ? ' alb' : ' negru').replace(/^ (alb|negru)$/, ' $1') + '.');
    return;
  }
  if (T.type === 'place') {
    const s = Object.keys(T.solution).find(q => st.placed[q] !== T.solution[q]);""")
sub("""  else if (T.type === 'namesq') { warn(msg + T.expl); }
  else if (T.type === 'yesno') {""", """  else if (T.type === 'namesq') { warn(msg + T.expl); }
  else if (T.type === 'addmate') {
    pos = fenToPos(T.fen); Object.keys(T.solution).forEach(q => pos[q] = T.solution[q]); board.position(pos, false);
    clearMarks(); setTimeout(() => markChecks(pos), 30); document.getElementById('ex-opts').innerHTML = ''; warn(msg + T.expl);
  }
  else if (T.type === 'mateq') { warn(msg + T.expl); }
  else if (T.type === 'yesno') {""")
# Arată răspunsul la move: promovarea corectă (și subpromovarea)
sub("""    const f = T.answer.slice(0, 2), t = T.answer.slice(2, 4), capt = !!pos[t];
    pos = applyMove(pos, f, t); board.position(pos, true); playSnd(capt ? sndCapture : sndMove);""",
    """    const f = T.answer.slice(0, 2), t = T.answer.slice(2, 4), capt = !!pos[t];
    pos = applyMove(pos, f, t); if (T.answer[4]) pos[t] = T.side + T.answer[4].toUpperCase();
    board.position(pos, true); playSnd(capt ? sndCapture : sndMove);""")
# culoarea piesei de pus contează la mesajul pentru indiciu: simplificare
s = s.replace("""(T.solution[s][0] === 'w' ? ' alb' : ' negru').replace(/^ (alb|negru)$/, ' $1')""", """(T.solution[s][0] === 'w' ? ' (alb)' : ' (negru)')""")

sub("var sndMove = new Audio('Sounds/Move.mp3'), sndCapture = new Audio('Sounds/Capture.mp3');",
    "var sndMove = new Audio('Sounds/Move.mp3'), sndCapture = new Audio('Sounds/Capture.mp3'), sndMate = new Audio('Sounds/Mate.mp3');")
sub("const side = T.side || (T.type === 'yesno' ? null : null);", "const side = T.type === 'addmate' ? null : T.side;")
sub("clearHint(); clearMarks(); pos = np; playSnd(sndCapture);\n      setTimeout(() => markChecks(pos), 60);\n      success(uci === T.answer ? 'Mat! '", "clearHint(); clearMarks(); pos = np; playSnd(sndMate);\n      setTimeout(() => markChecks(pos), 60);\n      success(uci === T.answer ? 'Mat! '")
s = s.replace("if (isMated(pos, T.defender)) { success('Mat! ' + T.expl); return; }", "if (isMated(pos, T.defender)) { playSnd(sndMate); success('Mat! ' + T.expl); return; }")
# în sertare: sunet de mat când mutarea dă mat
sub("setTimeout(() => { board.position(pos, true); playSnd(capt ? sndCapture : sndMove);", "setTimeout(() => { board.position(pos, true); playSnd(['w', 'b'].some(c => isMated(pos, c)) ? sndMate : capt ? sndCapture : sndMove);")
open(R + 'nivel1_lectia7.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
