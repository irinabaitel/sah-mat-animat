# nivel1_lectia7.html (Matul) -> nivel1_lectia16.html (Apărarea împotriva matului)
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = r'C:/Users/irina/SahMatAnimat/'
s = open(R + 'nivel1_lectia7.html', encoding='utf-8').read()
def sub(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)
def resub(pat, new):
    global s
    s2, n = re.subn(pat, lambda m: new, s, flags=re.S)
    assert n == 1, (n, pat[:80]); s = s2

sub('<title>Matul</title>', '<title>Apărarea împotriva matului</title>')
sub('<span class="header-title">Matul</span>', '<span class="header-title">Apărarea împotriva matului</span>')

resub(r'<!-- ── ACC 0: MATUL ── -->.*?<!-- ── ACC 1: CUM DAI MAT ── -->', '''<!-- ── ACC 0: MATUL TE PÂNDEȘTE ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc0" onclick="toggleAcc(0)"><span>🛡️ Ne place să dăm mat, dar...</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body0"><div class="acc-inner">
              <p>...nu ne place să îl luăm! De aceea trebuie să știm să ne apărăm împotriva atacurilor de mat. În primul rând, trebuie să îl <strong>vedem</strong>: la fiecare mutare ne uităm la regele nostru, cine l-ar putea amenința și pe unde ar putea pleca.</p>
              <p>Te aperi de mat la fel ca de orice atac, în patru feluri: <strong>protejezi</strong> pătratul amenințat, <strong>capturezi</strong> o piesă care atacă, <strong>te pui în cale</strong> sau <strong>pleci cu regele</strong>. Alege apărarea cu care nu pierzi material.</p>
              <div id="g-amenint-text"></div>
              <div id="g-amenint-act"></div>
              <div class="ex-step-nav" id="g-amenint-nav"></div>
              <div class="hl-box warn"><strong>Întâi caută amenințarea:</strong> pe ce pătrat ar veni matul și cu ce piese? Abia apoi alege apărarea.</div>
            </div></div>
          </div>

          <!-- ── ACC 1: CUM TE APERI ── -->''')
sub('''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>♛ Cum dai mat</span><span class="acc-icon">▶</span></div>''',
    '''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🧩 Cum te aperi de mat</span><span class="acc-icon">▶</span></div>''')
sub('''<p>La mat, piesele lucrează împreună. Una dă șah, iar celelalte o apără sau păzesc pătratele pe unde ar putea pleca regele. Uneori chiar piesele regelui îi închid drumul.</p>''',
    '''<p>Fiecare sertar arată o apărare. La sfârșit găsești și <strong>șahul dublu</strong>, la care regele are o singură apărare: să plece.</p>''')
sub('<p class="src-note">Exercițiile vin din programul Chess Tutor Step 1, din caietul metodei Steps și din lecțiile ChessKid.</p>',
    '<p class="src-note">Exercițiile vin din programul Chess Tutor Step 2 și din caietul metodei Steps, pasul 2.</p>')

resub(r'<p>Alege un joc sau intră în arenă\.</p>.*?</div></div>\n          </div>\n        </div><!-- /acc-wrapper -->', '''<p>Alege un joc sau intră în arenă.</p>
              <a href="nivel1_joc_doi_nebuni.html" class="practice-btn pb-blue">♗ Doi nebuni contra damei<small>Nebunii rezistă fără să piardă niciunul</small></a>
              <a href="nivel1_joc_vanatoarea_nebunului.html" class="practice-btn pb-purple">♝ Vânătoarea nebunului<small>Dama, turnul și calul prind nebunul fără să piardă nimic</small></a>
              <a href="nivel1_joc_pozitia_initiala.html" class="practice-btn pb-brown">🏠 Înapoi la poziția inițială<small>Piesele albe ajung acasă pe pătrate sigure</small></a>
              <a href="joc_stockfish.html?v=3" class="practice-btn pb-blue">♙ Cine promovează primul?<small>Cursa pionilor: câștigă cu albele</small></a>
              <a href="aparare_mat.html" class="practice-btn pb-green">🛡️ Arena de apărare<small>25 de poziții: oprește matul adversarului</small></a>
            </div></div>
          </div>
        </div><!-- /acc-wrapper -->''')

sub('<a href="nivel1_lectia15.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Numărarea atacatorilor</span></a>',
    '<a href="nivel1_lectia7.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Matul</span></a>')
sub('<a href="nivel1_lectia16.html" class="nav-btn nav-btn--forward"><span class="label">Apărarea împotriva matului</span>',
    '<a href="pagina7.html" class="nav-btn nav-btn--forward"><span class="label">Patul</span>')
sub('<script src="data/nivel1_lectia7_demo.js?v=1"></script>\n<script src="data/nivel1_lectia7_ex.js?v=1"></script>',
    '<script src="data/nivel1_lectia16_demo.js?v=1"></script>\n<script src="data/nivel1_lectia16_ex.js?v=1"></script>')
s = s.replace('L7DEMO', 'L16DEMO').replace('L7EX', 'L16EX')
sub("const SAVE_KEY = 'n1l7_ex_v1';", "const SAVE_KEY = 'n1l16_ex_v1';")
resub(r"const TAB_DESC = \{.*?\};", """const TAB_DESC = {
  baza: 'Apără-te de mat și „Există apărare?”, din caietul metodei Steps.',
  mediu: 'Exercițiile din Chess Tutor: protejezi, pleci cu regele, capturezi, te pui în cale.',
  avansat: 'Exercițiile suplimentare din Chess Tutor: toate apărările amestecate și ieșirea din șah fără să primești mat.'
};""")
resub(r"const DEF_GROUPS = \[.*?\];", """const DEF_GROUPS = [
  ['protejezi', '🛡️ Protejezi pătratul'],
  ['razex',     '🔭 Apărarea prin raze X'],
  ['tempo',     '⏱️ Câștigi timp cu un șah'],
  ['capturezi', '⚔️ Capturezi un atacator'],
  ['pleci',     '👣 Regele pleacă sau îi faci loc'],
  ['incale',    '🧱 Te pui în cale'],
  ['cauta',     '🔎 Cum cauți apărarea'],
  ['dublu',     '⚡ Șahul dublu: regele pleacă']
];""")
sub("+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Step 1, lecțiile 7 și 8.</p>';",
    "+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Manualul și caietul pasului 2, lecția 12. Șahul dublu: ChessKid, lecția 11.</p>';")
sub("if (accOpen === 0) renderGroup('mat');", "if (accOpen === 0) renderGroup('amenint');")

# ═════════ sertare: acțiuni cu mai multe mutări (line) ═════════
sub("""  if (a.move) {
    const f = a.move.slice(0, 2), t = a.move.slice(2, 4), capt = !!pos[t];""", """  if (a.line) {
    let k = 0;
    const step = () => {
      const u = a.line[k], f = u.slice(0, 2), t = u.slice(2, 4), capt = !!pos[t];
      pos = applyMove(pos, f, t); board.position(pos, true);
      clearMarks(); markChecks(pos); clearArrows(); drawArrows([[f, t, 'g']]);
      playSnd(['w', 'b'].some(c => isMated(pos, c)) ? sndMate : capt ? sndCapture : sndMove);
      if (++k < a.line.length) setTimeout(step, 950);
    };
    setTimeout(step, 150);
  }
  if (a.move) {
    const f = a.move.slice(0, 2), t = a.move.slice(2, 4), capt = !!pos[t];""")

# ═════════ exerciții: apărarea de mat (check: 'defmate') ═════════
sub("""  let ok = uci === T.answer || (T.ok || []).includes(uci), msg = null;""", """  if (T.check === 'defmate' && uci !== T.answer && !(T.ok || []).includes(uci)) {
    const mm = movesOf(np, opp(side)).find(m => isMated(applyMove(np, m[0], m[1]), side));
    clearArrows();
    if (mm) { drawArrows([[mm[0], mm[1], 'r']]); fail('❌ Nu ajută: ' + NAME[np[mm[0]][1]] + ' de pe ' + mm[0] + ' dă mat pe ' + mm[1] + '. Mai încearcă!'); }
    else fail('❌ ' + (T.badmsg || 'Matul nu vine imediat, dar mutarea aceasta nu este cea mai bună: pierzi material sau adversarul ajunge tot la mat. Caută altă apărare.'));
    return false;
  }
  let ok = uci === T.answer || (T.ok || []).includes(uci), msg = null;""")

# tipul „defq”: Există apărare? Da/Nu, apoi mutarea
sub("""  else if (T.type === 'mateq') {
    markChecks(pos);
    o.innerHTML = optButtons(['Da', 'Nu']);
  }""", """  else if (T.type === 'mateq') {
    markChecks(pos);
    o.innerHTML = optButtons(['Da', 'Nu']);
  }
  else if (T.type === 'defq') {
    markChecks(pos);
    o.innerHTML = optButtons(['Da', 'Nu']);
  }""")
sub("""  else if (T.type === 'mateq') {
    ok = (v === 'Da') === T.answer; okMsg = T.expl;""", """  else if (T.type === 'defq') {
    ok = (v === 'Da') === T.answer;
    btn.classList.add(ok ? 'ok' : 'bad');
    if (!ok) { fail('❌ ' + (T.answer ? 'Mai uită-te: există o apărare.' : 'Mai uită-te: caută întâi amenințarea, apoi încearcă toate apărările. Niciuna nu ajunge.')); return; }
    if (!T.answer) { drawArrows(T.threat.map(u => [u.slice(0, 2), u.slice(2, 4), 'r'])); success(T.expl); return; }
    T = Object.assign({}, T, { type: 'move', check: 'defmate', answer: T.move });
    document.getElementById('ex-opts').innerHTML = '';
    document.getElementById('ex-tools').innerHTML = '<button class="tool-btn" onclick="giveHint()">💡 Indiciu</button><button class="tool-btn" onclick="showAnswer()">👁 Arată răspunsul</button>';
    warn('Da, există o apărare. Acum joac-o pe tablă.');
    return;
  }
  else if (T.type === 'mateq') {
    ok = (v === 'Da') === T.answer; okMsg = T.expl;""")
sub("""function showAnswer() {
  if (solved && T.type !== 'route') return;
  clearHint(); solved = true;""", """function showAnswer() {
  if (solved && T.type !== 'route') return;
  if (T.type === 'defq') {
    if (!T.answer) { clearHint(); solved = true; drawArrows(T.threat.map(u => [u.slice(0, 2), u.slice(2, 4), 'r'])); warn('👁 ' + T.expl); return; }
    T = Object.assign({}, T, { type: 'move', check: 'defmate', answer: T.move }); document.getElementById('ex-opts').innerHTML = '';
  }
  clearHint(); solved = true;""")

open(R + 'nivel1_lectia16.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
