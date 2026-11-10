# nivel1_lectia17.html (Patul, motorul cel mai nou) -> nivel1_lectia3.html (Mutări speciale)
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = r'C:/Users/irina/SahMatAnimat/'
s = open(R + 'nivel1_lectia17.html', encoding='utf-8').read()
def sub(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)
def resub(pat, new):
    global s
    s2, n = re.subn(pat, lambda m: new, s, flags=re.S)
    assert n == 1, (n, pat[:80]); s = s2

sub('<title>Patul</title>', '<title>Mutări speciale</title>')
sub('<span class="header-title">Patul</span>', '<span class="header-title">Mutări speciale</span>')

# ── ACC 0: textele Irinei din pagina veche ──
resub(r'<!-- ── ACC 0: REMIZA ȘI PATUL ── -->.*?<!-- ── ACC 1: CUM RECUNOȘTI PATUL ── -->', '''<!-- ── ACC 0: MUTĂRI SPECIALE ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc0" onclick="toggleAcc(0)"><span>✨ Mutări speciale</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body0"><div class="acc-inner">
              <p>Mutările speciale par că încalcă regulile pe care le-am învățat până acum. Cu toate acestea, ele sunt permise de regulament — toți jucătorii de șah trebuie să le cunoască!</p>
              <div id="g-intro-text"></div>
              <div id="g-intro-act"></div>
              <div class="ex-step-nav" id="g-intro-nav"></div>
              <h4 class="sm-title">♚♜ Rocada</h4>
              <p>Rocada este o mutare de rege — singura mutare în care ai voie să miști două piese. Regele se deplasează două pătrate, iar turnul se așază de partea cealaltă.</p>
              <p><strong>6 condiții pentru rocadă:</strong></p>
              <ul class="sm-list">
                <li>Regele nu s-a mișcat niciodată în această partidă</li>
                <li>Turnul ales nu s-a mișcat niciodată în această partidă</li>
                <li>Nicio piesă nu se află între rege și turn</li>
                <li>Regele nu este în șah în momentul în care se face rocada</li>
                <li>Regele nu trece printr-un câmp atacat de adversar</li>
                <li>Regele nu ajunge pe un câmp atacat (nu intră în șah)</li>
              </ul>
              <div class="hl-box"><strong>🏆 Regulă de turneu:</strong> Trebuie să miști mai întâi regele, apoi, cu aceeași mână, turnul. Dacă atingi turnul primul, ești obligat să-l muți — și nu mai poți face rocada! Dacă faci rocada cu două mâini, se consideră mutare ilegală.</div>
              <h4 class="sm-title">♟→♛ Promovarea</h4>
              <p>Când un pion ajunge la ultima linie a adversarului (linia 8 pentru alb, linia 1 pentru negru), se transformă imediat în altă piesă. Aproape mereu: Regina!</p>
              <div class="hl-box warn"><strong>🤔 De ce nu mereu Regina?</strong> Uneori promovând în Regină faci pat (egalitate)! În acele situații rare se alege Turn sau Cal. Dar 99% din timp: Regina!</div>
              <div class="hl-box"><strong>🏆 Reguli de turneu:</strong>
                <ul class="sm-list">
                  <li>Dacă pionul ajunge pe ultima linie și jucătorul apasă pe ceas fără să-l schimbe cu o altă piesă → mutare ilegală; adversarul primește 1 minut extra, iar pionul trebuie înlocuit.</li>
                  <li>Dacă nu are o regină la dispoziție, jucătorul care promovează trebuie să oprească ceasul și să îi solicite arbitrului o regină.</li>
                  <li>Un turn așezat invers pe tablă va fi considerat turn și jucătorul îl va folosi ca atare.</li>
                </ul>
              </div>
              <h4 class="sm-title">↗ En passant</h4>
              <p>Cea mai surprinzătoare mutare! Dacă un pion adversar avansează 2 pătrate de pe linia de start și ajunge lângă pionul tău, poți să-l capturezi ca și cum ar fi avansat doar 1 pătrat.</p>
              <div class="hl-box warn"><strong>⚠️ ACUM ORI NICIODATĂ!</strong> Dacă nu capturezi imediat, la mutarea aceea, pierzi dreptul pentru totdeauna. Fii atent!</div>
            </div></div>
          </div>

          <!-- ── ACC 1: CUM SE FAC ── -->''')
sub('''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🧩 Cum recunoști patul</span><span class="acc-icon">▶</span></div>''',
    '''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🧩 Mutările speciale pe tablă</span><span class="acc-icon">▶</span></div>''')
sub('''<p>Ca să știi dacă e pat, pune-ți trei întrebări despre jucătorul <strong>la mutare</strong>: Este regele în șah? Poate muta regele? Poate muta altă piesă?</p>''',
    '''<p>Fiecare sertar arată o mutare specială. Apasă butoanele ca să vezi mutarea pe tablă.</p>''')
sub('<p class="src-note">Exercițiile vin din caietul metodei Steps (pasul 1), din lecțiile ChessKid și din programul Chess Tutor Step 1.</p>',
    '<p class="src-note">Exercițiile vin din caietul metodei Steps (pasul 1), din lecțiile ChessKid 5 și 14 și din programul Chess Tutor Step 1 (lecțiile 9 și 14).</p>')

resub(r'<p>Alege un joc sau intră în arenă\.</p>.*?</div></div>\n          </div>\n        </div><!-- /acc-wrapper -->', '''<p>Promovarea și en passant se văd cel mai bine într-o partidă adevărată. Joacă o partidă cu regi și pioni, contra Robotului sau în doi.</p>
              <a href="joc_stockfish.html?v=2" class="practice-btn pb-blue">♚ Regi și Pioni 2 — partida completă<small>Promovare, en passant și mat</small></a>
              <a href="joc_pioni.html" class="practice-btn pb-green">♙ Jocul Pionilor<small>Câștigă cine promovează primul</small></a>
            </div></div>
          </div>
        </div><!-- /acc-wrapper -->''')

sub('<a href="nivel1_lectia16.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Apărarea împotriva matului</span></a>',
    '<a href="nivel1_lectia6.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Atacul asupra regelui</span></a>')
sub('<a href="nivel1_lectia12.html" class="nav-btn nav-btn--forward"><span class="label">Câștig, egal și pierdere</span>',
    '<a href="nivel1_lectia13.html" class="nav-btn nav-btn--forward"><span class="label">Piese atârnate</span>')
sub('<script src="data/nivel1_lectia17_demo.js?v=1"></script>\n<script src="data/nivel1_lectia17_ex.js?v=1"></script>',
    '<script src="data/nivel1_lectia3_demo.js?v=1"></script>\n<script src="data/nivel1_lectia3_ex.js?v=1"></script>')
s = s.replace('L17DEMO', 'L3DEMO').replace('L17EX', 'L3EX')
sub("const SAVE_KEY = 'n1l17_ex_v1';", "const SAVE_KEY = 'n1l3_ex_v2';")
resub(r"const TAB_DESC = \{.*?\};", """const TAB_DESC = {
  baza: 'Rocada și en passant: da sau nu? Din caietul metodei Steps și din lecțiile ChessKid.',
  mediu: 'Exercițiile din Chess Tutor: care rocade sunt permise?',
  avansat: 'De ce nu e permisă rocada, mat cu en passant și promovarea în piesa potrivită.'
};""")
resub(r"const DEF_GROUPS = \[.*?\];", """const DEF_GROUPS = [
  ['rocada',   '🏰 Rocada mică și rocada mare'],
  ['rocnu1',   '🚫 Fără rocadă: au mutat sau e ceva în cale'],
  ['rocnu2',   '⚠️ Fără rocadă: șahul'],
  ['promo',    '♛ Promovarea'],
  ['subpromo', '🤔 De ce nu mereu regina?'],
  ['ep',       '↗ En passant'],
  ['epacum',   '⏱️ Acum ori niciodată']
];""")
sub("+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Manualul pasului 1, lecția 12; ChessKid, lecțiile 3 și 4.</p>';",
    "+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Manualul pasului 1, lecțiile 4, 9 și 14; ChessKid, lecțiile 5 și 14.</p>';")
sub("if (accOpen === 0) renderGroup('remiza');", "if (accOpen === 0) renderGroup('intro');")
sub("    .src-note {", """    .sm-title { font-family: var(--font-display); color: var(--c-navy); margin: 14px 0 4px; font-size: 1.05em; }
    .sm-list { margin: 4px 0 8px 18px; line-height: 1.6; }
    .src-note {""")

# ═════════ motorul: rocada și en passant pe tablă ═════════
sub("""function applyMove(pos, from, to) {
  const np = Object.assign({}, pos); np[to] = np[from]; delete np[from];""",
    """function applyMove(pos, from, to) {
  const np = Object.assign({}, pos), pc = np[from];
  if (pc && pc[1] === 'K' && from[0] === 'e' && Math.abs(to.charCodeAt(0) - from.charCodeAt(0)) === 2) {   // rocada
    const r = from[1], rf = (to[0] === 'g' ? 'h' : 'a') + r, rt = (to[0] === 'g' ? 'f' : 'd') + r;
    if (np[rf]) { np[rt] = np[rf]; delete np[rf]; }
  }
  if (pc && pc[1] === 'P' && from[0] !== to[0] && !np[to]) delete np[to[0] + from[1]];   // en passant
  np[to] = np[from]; delete np[from];""")

# ═════════ exerciții: tipurile noi ═════════
sub("""  else if (T.type === 'kplace') {
    o.innerHTML = '<p class="set-intro">Atinge pătratul unde pui regele ' + (T.kc === 'w' ? 'alb' : 'negru') + '.</p>';
  }""", """  else if (T.type === 'kplace') {
    o.innerHTML = '<p class="set-intro">Atinge pătratul unde pui regele ' + (T.kc === 'w' ? 'alb' : 'negru') + '.</p>';
  }
  else if (T.type === 'choice') {
    markChecks(pos); (T.focus || []).forEach(q => mark(q, 'sq-focus'));
    o.innerHTML = '<div class="opt-row' + (T.opts.length > 2 ? ' opt-col' : '') + '">' + T.opts.map((v, i) => '<button class="opt-btn" onclick="pickOpt(this,' + i + ')">' + v + '</button>').join('') + '</div>';
  }
  else if (T.type === 'castles') {
    st.on = {};
    markChecks(pos);
    o.innerHTML = '<div class="opt-row">' + CASTLES.map((v, i) => '<button class="opt-btn" id="cs-' + i + '" onclick="castTog(' + i + ')">' + v + '</button>').join('') + '</div>'
      + '<div class="opt-row" style="margin-top:6px"><button class="pill" onclick="castCheck()">✔ Verifică</button></div>';
  }""")
sub("""function clickNamed(s) {""", """const CASTLES = ['Albul 0-0', 'Albul 0-0-0', 'Negrul 0-0', 'Negrul 0-0-0'];
function castTog(i) {
  if (solved) return;
  st.on[i] = !st.on[i]; document.getElementById('cs-' + i).classList.toggle('sel', !!st.on[i]); clearFeedback();
}
function castCheck() {
  if (solved) return;
  const picked = CASTLES.filter((v, i) => st.on[i]);
  const extra = picked.find(v => !T.answer.includes(v)), miss = T.answer.find(v => !picked.includes(v));
  if (extra) { fail('❌ ' + extra + ': nu se poate. ' + T.reasons[extra].replace(/^[^.]*\\. /, '')); return; }
  if (miss) { fail('❌ Mai este ' + (T.answer.length - picked.length > 1 ? 'câte o rocadă permisă' : 'o rocadă permisă') + '. Verifică din nou fiecare rege.'); return; }
  CASTLES.forEach((v, i) => document.getElementById('cs-' + i).classList.add(T.answer.includes(v) ? 'ok' : 'bad'));
  success((T.answer.length ? 'Corect! ' : 'Corect: nicio rocadă nu este permisă. ') + CASTLES.map(v => T.reasons[v]).join(' '));
}
function clickNamed(s) {""")
sub("""function pickOpt(btn, v) {
  if (solved) return;
  let ok, okMsg, badMsg;""", """function pickOpt(btn, v) {
  if (solved) return;
  if (T.type === 'choice') {
    const val = T.opts[v], ok = T.answer.includes(val);
    btn.classList.add(ok ? 'ok' : 'bad');
    if (!ok) { fail('❌ ' + ((T.why || {})[val] || 'Mai uită-te.')); return; }
    if (T.epmove) { clearArrows(); drawArrows([[T.epmove.slice(0, 2), T.epmove.slice(2, 4), 'g']]); }
    success(T.expl); return;
  }
  let ok, okMsg, badMsg;""")
# mutările care ar părea mat, dar en passant salvează; promovările greșite
sub("""    if (isMated(np, opp(side))) {
      clearHint(); clearMarks(); pos = np; playSnd(sndMate);""", """    if (T.notmate && T.notmate[uci]) {
      const m = T.notmate[uci].match(/pionul de pe ([a-h][1-8])/); clearArrows();
      if (m) drawArrows([[m[1], t[0] + m[1][1], 'r']]);
      fail('❌ ' + T.notmate[uci] + ' Mai încearcă!'); return false;
    }
    if (isMated(np, opp(side))) {
      clearHint(); clearMarks(); pos = np; playSnd(sndMate);""")
sub("""  if (T.check === 'nostale' && uci !== T.answer && !(T.ok || []).includes(uci)) {""",
    """  if (T.badpromo && T.badpromo[uci]) {
    if (isStale(np, opp(side))) { pos = np; board.position(pos, false); setTimeout(() => markStale(pos, opp(side)), 30);
      setTimeout(() => { pos = fenToPos(T.fen); board.position(pos, false); clearMarks(); markChecks(pos); }, 1600); }
    fail('❌ ' + T.badpromo[uci]); return false;
  }
  if (T.check === 'nostale' && uci !== T.answer && !(T.ok || []).includes(uci)) {""")
# instrumente: indiciu pentru tipurile noi
sub("""  if (['move', 'route', 'squares', 'marks', 'place', 'checksq', 'addmate', 'kplace'].includes(T.type)) tools.push""",
    """  if (['move', 'route', 'squares', 'marks', 'place', 'checksq', 'addmate', 'kplace', 'choice', 'castles'].includes(T.type)) tools.push""")
sub("""  if (T.type === 'kplace') { clearHint(); mark(T.answers[0], 'hint-square'); warn('💡 Încearcă pătratul verde.'); return; }""",
    """  if (T.type === 'kplace') { clearHint(); mark(T.answers[0], 'hint-square'); warn('💡 Încearcă pătratul verde.'); return; }
  if (T.type === 'choice') { warn('💡 ' + (T.hint || 'Verifică pe rând: au mutat regele sau turnul? E ceva între ele? Regele e în șah? Trece sau ajunge pe un pătrat atacat?')); return; }
  if (T.type === 'castles') {
    const v = CASTLES.find((x, i) => !!st.on[i] !== T.answer.includes(x));
    warn(v ? '💡 Mai uită-te la <strong>' + v + '</strong>.' : '💡 Totul pare bine. Apasă „Verifică”.'); return;
  }""")
sub("""  if (T.type === 'kplace') {
    clearHint(); solved = true; pos = fenToPos(T.fen); pos[T.answers[0]] = T.kc + 'K'; board.position(pos, false);""",
    """  if (T.type === 'choice') { clearHint(); solved = true; if (T.epmove) drawArrows([[T.epmove.slice(0, 2), T.epmove.slice(2, 4), 'g']]); warn('👁 ' + T.answer.join(' / ') + '. ' + T.expl); return; }
  if (T.type === 'castles') {
    clearHint(); solved = true;
    CASTLES.forEach((v, i) => { const b = document.getElementById('cs-' + i); b.classList.remove('sel'); b.classList.add(T.answer.includes(v) ? 'ok' : 'bad'); });
    warn('👁 ' + (T.answer.length ? 'Permise: ' + T.answer.join(', ') + '. ' : 'Nicio rocadă nu e permisă. ') + CASTLES.map(v => T.reasons[v]).join(' ')); return;
  }
  if (T.type === 'kplace') {
    clearHint(); solved = true; pos = fenToPos(T.fen); pos[T.answers[0]] = T.kc + 'K'; board.position(pos, false);""")
sub("    .sq-pat {", "    .opt-col { flex-direction: column; align-items: stretch; }\n    .opt-btn.sel { outline: 3px solid var(--c-navy); }\n    .sq-pat {")

assert 'L17' not in s and 'lectia17' not in s.replace('nivel1_lectia17.html', ''), [m.start() for m in re.finditer('L17|lectia17', s)][:5]
open(R + 'nivel1_lectia3.html', 'w', encoding='utf-8').write(s)
print('ok', len(s))
