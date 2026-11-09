# nivel1_lectia16.html (Apărarea împotriva matului) -> nivel1_lectia17.html (Patul)
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = r'C:/Users/irina/SahMatAnimat/'
s = open(R + 'nivel1_lectia16.html', encoding='utf-8').read()
def sub(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)
def resub(pat, new):
    global s
    s2, n = re.subn(pat, lambda m: new, s, flags=re.S)
    assert n == 1, (n, pat[:80]); s = s2

sub('<title>Apărarea împotriva matului</title>', '<title>Patul</title>')
sub('<span class="header-title">Apărarea împotriva matului</span>', '<span class="header-title">Patul</span>')

resub(r'<!-- ── ACC 0: MATUL TE PÂNDEȘTE ── -->.*?<!-- ── ACC 1: CUM TE APERI ── -->', '''<!-- ── ACC 0: REMIZA ȘI PATUL ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc0" onclick="toggleAcc(0)"><span>🤝 Remiza și patul</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body0"><div class="acc-inner">
              <p>O partidă de șah nu se termină întotdeauna cu o victorie. Se poate termina și la egalitate: <strong>remiză</strong>. Fiecare jucător primește o jumătate de punct.</p>
              <div id="g-remiza-text"></div>
              <div id="g-remiza-act"></div>
              <div class="ex-step-nav" id="g-remiza-nav"></div>
              <p>O partidă de șah se poate termina și cu <strong>„PAT”</strong>, atunci când un jucător este la mutare și nu este în șah, dar nici nu poate muta nicio piesă.</p>
              <p>Piesele nu pot fi mutate fie pentru că sunt blocate (de exemplu pioni blocați de alte piese), fie pentru că, dacă s-ar muta, ar lăsa regele în șah. Regele nu poate muta dacă este blocat de piesele proprii, de piese adverse apărate, sau dacă pe câmpurile libere ar intra în șah.</p>
              <p>Cu alte cuvinte, când jucătorul la mutare <strong>nu este în șah</strong> și <strong>nu poate muta nicio piesă</strong>, partida se termină <strong>remiză</strong>.</p>
              <div class="hl-box warn"><strong>Atenție când ești în avantaj!</strong> Nu vrei ca în loc de punctul victoriei să obții doar o jumătate de punct. Verifică mereu, înainte să muți, dacă adversarul mai are vreo mutare.</div>
              <div class="hl-box ok"><strong>Folosește patul în apărare!</strong> Când ești în dezavantaj, un scor egal e mai bun decât o înfrângere. Caută posibilitatea de pat.</div>
            </div></div>
          </div>

          <!-- ── ACC 1: CUM RECUNOȘTI PATUL ── -->''')
sub('''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🧩 Cum te aperi de mat</span><span class="acc-icon">▶</span></div>''',
    '''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🧩 Cum recunoști patul</span><span class="acc-icon">▶</span></div>''')
sub('''<p>Fiecare sertar arată o apărare. La sfârșit găsești și <strong>șahul dublu</strong>, la care regele are o singură apărare: să plece.</p>''',
    '''<p>Ca să știi dacă e pat, pune-ți trei întrebări despre jucătorul <strong>la mutare</strong>: Este regele în șah? Poate muta regele? Poate muta altă piesă?</p>''')
sub('<p class="src-note">Exercițiile vin din programul Chess Tutor Step 2 și din caietul metodei Steps, pasul 2.</p>',
    '<p class="src-note">Exercițiile vin din caietul metodei Steps (pasul 1), din lecțiile ChessKid și din programul Chess Tutor Step 1.</p>')

resub(r'<p>Alege un joc sau intră în arenă\.</p>.*?</div></div>\n          </div>\n        </div><!-- /acc-wrapper -->', '''<p>Alege un joc sau intră în arenă.</p>
              <a href="nivel1_joc_vanatoarea_regelui.html" class="practice-btn pb-blue">👑 Vânătoarea regelui<small>Toată armata albă contra regelui negru: dă mat, nu pat</small></a>
              <a href="nivel1_arena_pat.html" class="practice-btn pb-green">⚖️ Arena patului<small>43 de poziții: salvează-te prin pat sau ferește-te să dai pat</small></a>
            </div></div>
          </div>
        </div><!-- /acc-wrapper -->''')

sub('<a href="nivel1_lectia7.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Matul</span></a>',
    '<a href="nivel1_lectia16.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Apărarea împotriva matului</span></a>')
sub('<a href="nivel1_lectia17.html" class="nav-btn nav-btn--forward"><span class="label">Patul</span>',
    '<a href="nivel1_lectia12.html" class="nav-btn nav-btn--forward"><span class="label">Câștig, egal și pierdere</span>')
sub('<script src="data/nivel1_lectia16_demo.js?v=1"></script>\n<script src="data/nivel1_lectia16_ex.js?v=1"></script>',
    '<script src="data/nivel1_lectia17_demo.js?v=1"></script>\n<script src="data/nivel1_lectia17_ex.js?v=1"></script>')
s = s.replace('L16DEMO', 'L17DEMO').replace('L16EX', 'L17EX')
sub("const SAVE_KEY = 'n1l16_ex_v1';", "const SAVE_KEY = 'n1l17_ex_v1';")
resub(r"const TAB_DESC = \{.*?\};", """const TAB_DESC = {
  baza: 'Mat, pat sau se joacă? Din caietul metodei Steps și din lecțiile ChessKid.',
  mediu: 'Exercițiile din Chess Tutor: mat, pat sau se joacă?',
  avansat: 'Exercițiile din lecția avansată Chess Tutor: unde e regele în pat, evită patul, lasă-i adversarului o mutare.'
};""")
resub(r"const DEF_GROUPS = \[.*?\];", """const DEF_GROUPS = [
  ['cepat',  '🤝 Ce este patul'],
  ['toate',  '♟️ Toate piesele, nu doar regele'],
  ['nupat',  '❓ Nu e pat'],
  ['randul', '⏱️ Pat e doar când ești la mutare'],
  ['arma',   '🛡️ Patul ca armă'],
  ['evita',  '⚠️ Cum eviți patul']
];""")
sub("+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Manualul și caietul pasului 2, lecția 12. Șahul dublu: ChessKid, lecția 11.</p>';",
    "+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Manualul pasului 1, lecția 12; ChessKid, lecțiile 3 și 4.</p>';")
sub("if (accOpen === 0) renderGroup('amenint');", "if (accOpen === 0) renderGroup('remiza');")

# ═════════ patul pe tablă ═════════
sub("function isMated(p, c) { return inCheck(p, c) && movesOf(p, c).length === 0; }",
    """function isMated(p, c) { return inCheck(p, c) && movesOf(p, c).length === 0; }
function isStale(p, c) { return !!kingSq(p, c) && !inCheck(p, c) && movesOf(p, c).length === 0; }
function markStale(p, c) { if (isStale(p, c)) mark(kingSq(p, c), 'sq-pat'); }""")
sub("    .src-note {", "    .sq-pat { box-shadow: inset 0 0 0 4px #e6b800, inset 0 0 18px rgba(230,184,0,0.75) !important; }\n    .src-note {")
sub("  setTimeout(() => { drawArrows(s.arrows); markChecks(fenToPos(s.fen)); }, 60);",
    "  setTimeout(() => { drawArrows(s.arrows); markChecks(fenToPos(s.fen)); markStale(fenToPos(s.fen), s.side); }, 60);")
# acțiunile din sertare: promovare (al 5-lea caracter) și marcarea patului
sub("""      const u = a.line[k], f = u.slice(0, 2), t = u.slice(2, 4), capt = !!pos[t];
      pos = applyMove(pos, f, t); board.position(pos, true);
      clearMarks(); markChecks(pos); clearArrows(); drawArrows([[f, t, 'g']]);""",
    """      const u = a.line[k], f = u.slice(0, 2), t = u.slice(2, 4), capt = !!pos[t], mover = pos[f][0];
      pos = applyMove(pos, f, t); if (u[4]) pos[t] = mover + u[4].toUpperCase(); board.position(pos, true);
      clearMarks(); markChecks(pos); markStale(pos, opp(mover)); clearArrows(); drawArrows([[f, t, 'g']]);""")
sub("""    const f = a.move.slice(0, 2), t = a.move.slice(2, 4), capt = !!pos[t];
    pos = applyMove(pos, f, t);
    setTimeout(() => { board.position(pos, true); playSnd(['w', 'b'].some(c => isMated(pos, c)) ? sndMate : capt ? sndCapture : sndMove); clearMarks(); markChecks(pos); if (a.hl) { a.hl.unsafe.forEach(q => mark(q, 'sq-unsafe')); } }, 120);""",
    """    const f = a.move.slice(0, 2), t = a.move.slice(2, 4), capt = !!pos[t], mover = pos[f][0];
    pos = applyMove(pos, f, t); if (a.move[4]) pos[t] = mover + a.move[4].toUpperCase();
    setTimeout(() => { board.position(pos, true); playSnd(['w', 'b'].some(c => isMated(pos, c)) ? sndMate : capt ? sndCapture : sndMove); clearMarks(); markChecks(pos); markStale(pos, opp(mover)); if (a.hl) { a.hl.unsafe.forEach(q => mark(q, 'sq-unsafe')); } }, 120);""")

# ═════════ exerciții: tipurile noi ═════════
sub("""  if (['move', 'route', 'squares', 'marks', 'place', 'checksq', 'addmate'].includes(T.type)) tools.push""",
    """  if (['move', 'route', 'squares', 'marks', 'place', 'checksq', 'addmate', 'kplace'].includes(T.type)) tools.push""")
sub("""  if (['route', 'marks', 'place', 'squares', 'checksq', 'addmate'].includes(T.type)) tools.push""",
    """  if (['route', 'marks', 'place', 'squares', 'checksq', 'addmate', 'kplace'].includes(T.type)) tools.push""")
sub("""  else if (T.type === 'defq') {
    markChecks(pos);
    o.innerHTML = optButtons(['Da', 'Nu']);
  }""", """  else if (T.type === 'defq') {
    markChecks(pos);
    o.innerHTML = optButtons(['Da', 'Nu']);
  }
  else if (T.type === 'msp') {
    markChecks(pos);
    o.innerHTML = optButtons(T.opts);
  }
  else if (T.type === 'kplace') {
    o.innerHTML = '<p class="set-intro">Atinge pătratul unde pui regele ' + (T.kc === 'w' ? 'alb' : 'negru') + '.</p>';
  }""")
sub("  if (T.type === 'place') return clickPlace(s);", "  if (T.type === 'place') return clickPlace(s);\n  if (T.type === 'kplace') return clickKPlace(s);")
sub("""  else if (T.type === 'mateq') {
    ok = (v === 'Da') === T.answer; okMsg = T.expl;""", """  else if (T.type === 'msp') {
    ok = v === T.answer;
    btn.classList.add(ok ? 'ok' : 'bad');
    if (!ok) {
      const chk = inCheck(pos, T.side), M = {
        'Mat': chk ? 'Regele e în șah, dar mai uită-te: poate scăpa? Poate captura, se poate pune ceva în cale, poate pleca?' : 'Regele nu este în șah. Fără șah nu poate fi mat.',
        'Pat': chk ? 'Regele este în șah, deci nu poate fi pat.' : 'Mai uită-te: poate muta regele sau altă piesă? Ai grijă la pionii blocați și la piesele legate.',
        'Se joacă': chk ? 'Regele e în șah. Are vreo scăpare? Uită-te la toate piesele.' : 'Mai uită-te: are vreo piesă a jucătorului la mutare o mutare permisă?' };
      fail('❌ ' + M[v]); return;
    }
    if (T.answer === 'Mat') { (T.hl || []).forEach(q => drawArrows([[q, kingSq(pos, T.side), 'r']])); }
    if (T.answer === 'Pat') markStale(pos, T.side);
    if (T.move) {
      T = Object.assign({}, T, { type: 'move', check: 'best', answer: T.move, expl: T.mexpl || T.expl });
      document.getElementById('ex-opts').innerHTML = '';
      document.getElementById('ex-tools').innerHTML = '<button class="tool-btn" onclick="giveHint()">💡 Indiciu</button><button class="tool-btn" onclick="showAnswer()">👁 Arată răspunsul</button>';
      warn('Corect, partida continuă. Acum joacă mutarea pe tablă.');
      return;
    }
    success(T.expl); return;
  }
  else if (T.type === 'mateq') {
    ok = (v === 'Da') === T.answer; okMsg = T.expl;""")
sub("""function clickNamed(s) {""", """function clickKPlace(s) {
  const base = fenToPos(T.fen);
  if (base[s]) { warn('Pe ' + s + ' stă deja o piesă. Alege un pătrat liber.'); return; }
  const np = Object.assign({}, base); np[s] = T.kc + 'K';
  pos = np; board.position(pos, false); playSnd(sndMove); clearHint(); clearMarks();
  if (T.answers.includes(s)) { setTimeout(() => markStale(pos, T.kc), 30); success('Pat! ' + T.expl); return; }
  const back = () => { pos = fenToPos(T.fen); board.position(pos, false); clearMarks(); };
  if (inCheck(np, T.kc)) {
    const a = attackers(np, s, opp(T.kc))[0];
    setTimeout(() => { mark(s, 'highlight-check'); if (a) drawArrows([[a, s, 'r']]); }, 30);
    fail('❌ Pe ' + s + ' regele ar fi în șah' + (a ? ' (' + NAME[np[a][1]] + ' de pe ' + a + ')' : '') + '. Pat înseamnă fără șah.');
  } else {
    const m = movesOf(np, T.kc)[0];
    setTimeout(() => { if (m) drawArrows([[m[0], m[1], 'g']]); }, 30);
    fail('❌ Pe ' + s + ' nu e pat: ' + (m ? (m[0] === s ? 'regele poate merge pe ' + m[1] : NAME[np[m[0]][1]] + ' de pe ' + m[0] + ' poate muta pe ' + m[1]) : '') + '.');
  }
  setTimeout(back, 1600);
}
function clickNamed(s) {""")
# mutările care dau pat
sub("""  let ok = uci === T.answer || (T.ok || []).includes(uci), msg = null;""",
    """  if (T.check === 'nostale' && uci !== T.answer && !(T.ok || []).includes(uci)) {
    if (isStale(np, opp(side))) {
      pos = np; board.position(pos, false); setTimeout(() => markStale(pos, opp(side)), 30);
      fail('❌ Pat! Adversarul nu e în șah și nu mai are nicio mutare: partida s-ar termina remiză. Mai încearcă!');
      setTimeout(() => { pos = fenToPos(T.fen); board.position(pos, false); clearMarks(); markChecks(pos); }, 1600);
    } else fail('❌ Nu e pat, dar nu este cea mai bună mutare. Mai caută.');
    return false;
  }
  let ok = uci === T.answer || (T.ok || []).includes(uci), msg = null;""")
# răspunsul arătat
sub("""  clearHint(); solved = true;
  const msg = '👁 ';""", """  if (T.type === 'msp') {
    if (!T.move) { clearHint(); solved = true; if (T.answer === 'Pat') markStale(pos, T.side); warn('👁 ' + T.answer + '. ' + T.expl); return; }
    T = Object.assign({}, T, { type: 'move', check: 'best', answer: T.move }); document.getElementById('ex-opts').innerHTML = '';
  }
  if (T.type === 'kplace') {
    clearHint(); solved = true; pos = fenToPos(T.fen); pos[T.answers[0]] = T.kc + 'K'; board.position(pos, false);
    setTimeout(() => markStale(pos, T.kc), 30); warn('👁 ' + T.expl); return;
  }
  clearHint(); solved = true;
  const msg = '👁 ';""")
sub("""  if (T.type === 'squares' || T.type === 'checksq') {""",
    """  if (T.type === 'kplace') { clearHint(); mark(T.answers[0], 'hint-square'); warn('💡 Încearcă pătratul verde.'); return; }
  if (T.type === 'squares' || T.type === 'checksq') {""")

open(R + 'nivel1_lectia17.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
