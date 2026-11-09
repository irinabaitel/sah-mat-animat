# nivel1_lectia5.html (model) -> nivel1_lectia6.html (Atacul asupra regelui)
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = r'C:/Users/irina/SahMatAnimat/'
s = open(R + 'nivel1_lectia5.html', encoding='utf-8').read()
def sub(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:90])
    s = s.replace(old, new)
def resub(pat, new):
    global s
    s2, n = re.subn(pat, lambda m: new, s, flags=re.S)
    assert n == 1, (n, pat[:80]); s = s2

sub('<title>Atacul, Captura și Apărarea</title>', '<title>Atacul asupra regelui</title>')
sub('<span class="header-title">Atacul, Captura și Apărarea</span>', '<span class="header-title">Atacul asupra regelui</span>')

# ── acordeonul 0: șahul ──
resub(r'<!-- ── ACC 0: ATACUL ȘI CAPTURA ── -->.*?<!-- ── ACC 1: APĂRAREA ── -->', '''<!-- ── ACC 0: ȘAHUL ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc0" onclick="toggleAcc(0)"><span>👑 Ce este șahul?</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body0"><div class="acc-inner">
              <p>Regele este piesa cea mai importantă: el rămâne pe tablă până la sfârșitul partidei. Atacul asupra regelui se numește <strong>șah</strong>.</p>
              <div id="g-sah-text"></div>
              <div id="g-sah-act"></div>
              <div class="ex-step-nav" id="g-sah-nav"></div>
              <div class="hl-box warn"><strong>Regele nu se capturează.</strong> Cine este în șah trebuie să scape de șah chiar la mutarea următoare. O mutare după care regele tău rămâne în șah nu este permisă.</div>
            </div></div>
          </div>

          <!-- ── ACC 1: IEȘIREA DIN ȘAH ── -->''')
sub('''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🛡️ Apărarea</span><span class="acc-icon">▶</span></div>''',
    '''<div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🛡️ Ieșirea din șah</span><span class="acc-icon">▶</span></div>''')
sub('''<p>Când o piesă a ta este atacată, ai patru feluri de a o apăra: <strong>fugi</strong>, <strong>o aperi</strong>, <strong>capturezi atacatorul</strong> sau <strong>blochezi</strong> atacul. Uneori merge un singur fel, alteori poți alege.</p>''',
    '''<p>Din șah ieși în trei feluri: <strong>fugi</strong> cu regele, <strong>capturezi</strong> piesa care dă șah sau <strong>pui o piesă în cale</strong>. Dacă poți alege, alege mutarea cu care nu pierzi nimic.</p>''')
sub('<p class="src-note">Exercițiile vin din programul Chess Tutor Step 1 (metoda Steps) și din lecțiile ChessKid.</p>',
    '<p class="src-note">Exercițiile vin din programul Chess Tutor Step 1, din caietul metodei Steps și din lecțiile ChessKid.</p>')

# ── Exersează ──
resub(r'<p>Atacul, captura și apărarea se învață cel mai bine jucând\..*?</div></div>\n          </div>\n        </div><!-- /acc-wrapper -->', '''<p>Alege un joc: îl poți juca împotriva Robotului sau în doi, cu un coleg.</p>
              <a href="nivel1_joc_regi_nasturi.html" class="practice-btn pb-blue">💎 Regii și diamantele<small>Doi regi adună diamante și nu stau alături</small></a>
              <a href="joc_stockfish.html" class="practice-btn pb-green">♚ Regi și Pioni<small>Regele și opt pioni contra regelui și opt pioni</small></a>
              <a href="nivel1_joc_scapa_de_dame.html?p=2" class="practice-btn pb-purple">♛ Scapă de dame (poziția 2)<small>Calul fuge de două regine</small></a>
              <a href="nivel1_joc_cine_pastreaza.html?v=turn" class="practice-btn pb-brown">🛡️ Cine păstrează ceva? Turn contra cal<small>Cine rămâne cu ceva în plus</small></a>
              <a href="nivel1_joc_rege_pioni.html" class="practice-btn pb-blue">♔ Regele contra pionilor<small>Cât mai mulți pioni ajung pe ultima linie</small></a>
            </div></div>
          </div>
        </div><!-- /acc-wrapper -->''')

sub('<a href="nivel1_lectia4.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Valoarea Pieselor</span></a>',
    '<a href="nivel1_lectia5.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Atacul, captura, apărarea</span></a>')
sub('<a href="nivel1_lectia6.html" class="nav-btn nav-btn--forward"><span class="label">Atacul asupra regelui</span>',
    '<a href="pagina4.html" class="nav-btn nav-btn--forward"><span class="label">Șahul dublu</span>')
sub('<script src="data/nivel1_lectia5_demo.js?v=1"></script>\n<script src="data/nivel1_lectia5_ex.js?v=1"></script>',
    '<script src="data/nivel1_lectia6_demo.js?v=1"></script>\n<script src="data/nivel1_lectia6_ex.js?v=1"></script>')
s = s.replace('L5DEMO', 'L6DEMO').replace('L5EX', 'L6EX')
sub("const SAVE_KEY = 'n1l5_ex_v1';", "const SAVE_KEY = 'n1l6_ex_v1';")
resub(r"const TAB_DESC = \{.*?\};", """const TAB_DESC = {
  baza: 'Primii pași: dă șah, capturează piesa care dă șah, pune o piesă în cale, fugi cu regele.',
  mediu: 'Exercițiile din Chess Tutor: șah din siguranță, ieșirea din șah, șah din două mutări.',
  avansat: 'Exercițiile suplimentare din Chess Tutor, pentru cei care vor mai mult.'
};""")
resub(r"const DEF_GROUPS = \[.*?\];", """const DEF_GROUPS = [
  ['fugi',  '🏃 Fugi cu regele'],
  ['capt',  '⚔️ Capturează piesa care dă șah'],
  ['bloc',  '🚧 Pune o piesă în cale'],
  ['toate', '🔁 Toate trei'],
  ['best',  '⭐ Care este cea mai bună?'],
  ['regi',  '👑 Regii nu stau alături']
];""")
sub("+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Step 1, lecțiile 3 și 5.</p>';",
    "+ '<p class=\"src-note\">Exemplele din sertare: metoda Steps (Brunia &amp; van Wijgerden), Step 1, lecția 6.</p>';")
sub("if (accOpen === 0) renderGroup('atac');", "if (accOpen === 0) renderGroup('sah');")
sub("document.getElementById('g-' + key + '-text').innerHTML = (key === 'atac' ? '' : turn) + s.text;",
    "document.getElementById('g-' + key + '-text').innerHTML = (s.acts.length ? turn : '') + s.text;")

# ── marcaj de șah pe rege ──
sub("el.classList.remove('hint-square','sq-safe',", "el.classList.remove('highlight-check','hint-square','sq-safe',")
sub("  setTimeout(() => drawArrows(s.arrows), 60);", "  setTimeout(() => { drawArrows(s.arrows); markChecks(fenToPos(s.fen)); }, 60);")

# ── utilitare cu regi ──
sub("function pname(pos, s) { return NAME[pos[s][1]]; }", """function pname(pos, s) { return NAME[pos[s][1]]; }
function kingSq(p, c) { return Object.keys(p).find(q => p[q] === c + 'K'); }
function inCheck(p, c) { const k = kingSq(p, c); return !!k && attackers(p, k, opp(c)).length > 0; }
function legalMove(p, f, t) {
  if (!targets(p, f).includes(t) || (p[t] && p[t][1] === 'K')) return false;
  return !inCheck(applyMove(p, f, t), p[f][0]);
}
function capturers(p, s) { const c = p[s][0]; return attackers(p, s, opp(c)).filter(a => legalMove(p, a, s)); }
function markChecks(p) { ['w', 'b'].forEach(c => { if (inCheck(p, c)) mark(kingSq(p, c), 'highlight-check'); }); }""")
# în exemple: după mutare, marcajul de șah se actualizează
sub("    setTimeout(() => { board.position(pos, true); playSnd(capt ? sndCapture : sndMove); }, 120);",
    "    setTimeout(() => { board.position(pos, true); playSnd(capt ? sndCapture : sndMove); clearMarks(); markChecks(pos); if (a.hl) { a.hl.unsafe.forEach(q => mark(q, 'sq-unsafe')); } }, 120);")
sub("  if (a.hl) { a.hl.safe.forEach(q => mark(q, 'sq-safe')); a.hl.unsafe.forEach(q => mark(q, 'sq-unsafe')); }",
    "  if (!a.move) markChecks(pos);\n  if (a.hl) { a.hl.safe.forEach(q => mark(q, 'sq-safe')); a.hl.unsafe.forEach(q => mark(q, 'sq-unsafe')); }")

# ── tipuri de sarcini ──
sub("if (['move', 'route', 'squares', 'marks', 'place'].includes(T.type)) tools.push", "if (['move', 'route', 'squares', 'marks', 'place', 'checksq'].includes(T.type)) tools.push")
sub("if (['route', 'marks', 'place', 'squares'].includes(T.type)) tools.push", "if (['route', 'marks', 'place', 'squares', 'checksq'].includes(T.type)) tools.push")
sub("  if (T.type === 'route') { st.cur = T.from; st.steps = []; st.seen = [T.from]; mark(T.target, 'sq-target'); }",
    "  if (T.type === 'move') markChecks(pos);\n  if (T.type === 'route') { st.cur = T.from; st.steps = []; st.seen = [T.from]; if (T.target) mark(T.target, 'sq-target'); }\n  else if (T.type === 'checksq') { st.found = []; mark(T.from, 'sq-focus'); }")
sub("  if (T.type === 'squares') return clickSquares(s);", "  if (T.type === 'squares') return clickSquares(s);\n  if (T.type === 'checksq') return clickCheckSq(s);")

resub(r"/\* ── tipul „move” ── \*/.*?/\* ── tipul „squares” \(pătrate sigure\) ── \*/", r"""/* ── tipul „move” (cu regi: șah, ieșirea din șah) ── */
function moveTask(f, t) {
  const uci = f + t, side = T.side, np = applyMove(pos, f, t), capt = !!pos[t];
  if (inCheck(np, side)) {
    fail(inCheck(pos, side) ? '❌ După mutarea aceasta regele tău este tot în șah. Mutarea nu este permisă.' : '❌ Mutarea nu este permisă: regele tău ar ajunge în șah.');
    return false;
  }
  let ok = uci === T.answer || (T.ok || []).includes(uci), msg = null;
  if (!ok && T.check === 'give') {
    if (!inCheck(np, opp(side))) { fail('❌ Mutarea aceasta nu dă șah. Mai încearcă!'); return false; }
    const c = capturers(np, t);
    if (c.length) { fail('❌ Dai șah, dar pe ' + t + ' ' + pname(np, t) + ' poate fi ' + gen(np, t, 'capturat') + ' de ' + pname(np, c[0]) + ' de pe ' + c[0] + '. Caută un șah sigur.'); return false; }
    ok = true; msg = 'Corect! Ai dat șah din siguranță.';
  }
  if (ok) {
    clearHint(); clearMarks(); pos = np; playSnd(capt ? sndCapture : sndMove);
    setTimeout(() => markChecks(pos), 60);
    success(uci === T.answer ? (T.expl || 'Corect!') : (msg || T.okmsg || 'Corect! Și aceasta este o mutare bună.'));
    return true;
  }
  if (T.check === 'give') {
    if (!inCheck(np, opp(side))) fail('❌ Mutarea aceasta nu dă șah. Mai încearcă!');
    else fail('❌ Nu este șahul căutat. Mai încearcă!');
  } else if (inCheck(pos, side)) fail('❌ Ai ieșit din șah, dar nu este cea mai bună mutare. Uită-te ce poate captura adversarul după mutarea ta.');
  else fail('❌ Nu este cea mai bună mutare. Uită-te ce poate captura adversarul după mutarea ta.');
  return false;
}

/* ── tipul „route” ── */
function routeMove(f, t, pr) {
  const p = pos[f];
  if (pos[t]) { fail('❌ Nu ai voie să capturezi.'); return false; }
  if (p[1] === 'P' && /[18]/.test(t[1]) && !pr) {
    st.pend = [f, t];
    document.getElementById('ex-opts').innerHTML = '<p class="set-intro">Pionul ajunge pe ultima linie. În ce piesă se transformă?</p><div class="opt-row">'
      + [['Q', 'Regină'], ['R', 'Turn'], ['B', 'Nebun'], ['N', 'Cal']].map(x => '<button class="opt-btn" onclick="pickPromo(\'' + x[0] + '\')">' + x[1] + '</button>').join('') + '</div>';
    warn('Alege piesa în care se transformă pionul.');
    return false;
  }
  const np = applyMove(pos, f, t); if (pr) np[t] = p[0] + pr;
  const cs = capturers(np, t);
  if (cs.length) { fail('❌ Pe ' + t + ' ' + NAME[np[t][1]] + ' poate fi ' + (np[t][1] === 'Q' ? 'capturată' : 'capturat') + ' de ' + pname(np, cs[0]) + ' de pe ' + cs[0] + '. Alege alt pătrat.'); return false; }
  if (T.mode === 'min' && st.seen.includes(t)) { fail('❌ Ai mai fost pe ' + t + '. Nu ai voie de două ori pe același pătrat.'); return false; }
  clearHint(); clearFeedback(); document.getElementById('ex-opts').innerHTML = '';
  pos = np; st.cur = t; st.steps.push(t); st.seen.push(t); playSnd(sndMove);
  mark(t, 'sq-step', st.steps.length);
  const n = st.steps.length;
  if (T.mode === 'check') {
    const ek = kingSq(pos, opp(p[0])), chk = !!ek && attackers(pos, ek, p[0]).includes(t);
    if (chk) setTimeout(() => mark(ek, 'highlight-check'), 60);
    if (n === 2 && chk) success('Șah! ' + T.expl);
    else if (n === 2) { fail('După două mutări nu ai dat șah. Încearcă din nou (↺).'); solved = true; }
    else if (chk) { fail('Ai dat șah deja la prima mutare, dar exercițiul cere șahul la a doua mutare. Încearcă din nou (↺).'); solved = true; }
    return true;
  }
  if (t === T.target) {
    if (T.mode === 'exact' && n > T.moves) { fail('Ai ajuns, dar în ' + n + ' mutări. Se poate în ' + T.moves + '. Încearcă din nou (↺).'); solved = true; return true; }
    if (T.mode === 'min' && n < T.moves) { fail('Ai ajuns prea repede: trebuie cel puțin ' + T.moves + ' mutări. Încearcă din nou (↺).'); solved = true; return true; }
    success('Ai ajuns în ' + n + ' mutări. ' + T.expl);
  } else if (T.mode === 'exact' && n >= T.moves) {
    fail('Nu ai ajuns în ' + T.moves + ' mutări. Încearcă din nou (↺).'); solved = true;
  }
  return true;
}
function pickPromo(x) {
  if (!st.pend) return;
  const [f, t] = st.pend; st.pend = null;
  routeMove(f, t, x); board.position(pos, false);
}

/* ── tipul „checksq” (de unde dă piesa șah) ── */
function clickCheckSq(s) {
  const f = T.from, pc = pos[f];
  if (s === f || st.found.includes(s)) return;
  if (pos[s]) { warn('Caută pătrate goale: aici nu capturăm.'); return; }
  if (!targets(pos, f).includes(s)) { warn(cap(pname(pos, f)) + ' nu poate ajunge pe ' + s + ' dintr-o mutare.'); return; }
  const np = applyMove(pos, f, s), ek = kingSq(np, opp(pc[0]));
  if (T.answers.includes(s)) {
    st.found.push(s); mark(s, 'sq-safe');
    if (st.found.length === T.answers.length) success(T.expl);
    else showFeedback('Bine! Mai ' + (T.answers.length - st.found.length === 1 ? 'este un pătrat' : 'sunt ' + (T.answers.length - st.found.length) + ' pătrate') + '.', 'success');
    return;
  }
  mark(s, 'sq-unsafe'); setTimeout(() => unmark(s, 'sq-unsafe'), 900);
  if (!ek || !attackers(np, ek, pc[0]).includes(s)) fail('❌ De pe ' + s + ' ' + pname(pos, f) + ' nu dă șah.');
  else { const cs = capturers(np, s); fail('❌ De pe ' + s + ' dă șah, dar ' + pname(pos, f) + ' ar fi ' + gen(pos, f, 'capturat') + ' de ' + pname(np, cs[0]) + ' de pe ' + cs[0] + '.'); }
}

/* ── tipul „squares” (pătrate sigure) ── */""")

# indicii și răspuns
sub("  if (T.type === 'squares') { const s = T.answers.find(q => !st.found.includes(q)); clearHint(); mark(s, 'hint-square'); warn('💡 Uită-te la pătratul verde.'); return; }",
    "  if (T.type === 'squares' || T.type === 'checksq') { const s = T.answers.find(q => !st.found.includes(q)); clearHint(); mark(s, 'hint-square'); warn('💡 Uită-te la pătratul verde.'); return; }")
sub("""    pos = T.fen ? fenToPos(T.fen) : {}; clearMarks(); mark(T.target, 'sq-target');
    const p = pos[T.from]; delete pos[T.from]; pos[T.route[T.route.length - 1]] = p;
    board.position(pos, true);
    T.route.forEach((s, i) => mark(s, 'sq-step', i + 1));""",
    """    pos = T.fen ? fenToPos(T.fen) : {}; clearMarks(); if (T.target) mark(T.target, 'sq-target');
    const p = pos[T.from]; delete pos[T.from]; pos[T.route[T.route.length - 1]] = T.promo ? p[0] + T.promo : p;
    board.position(pos, true);
    T.route.forEach((s, i) => mark(s, 'sq-step', i + 1)); setTimeout(() => markChecks(pos), 300);
    document.getElementById('ex-opts').innerHTML = '';""")
sub("  } else if (T.type === 'marks') { revealMarks(); warn(msg + T.expl); }",
    "  } else if (T.type === 'checksq') { T.answers.forEach(s => mark(s, 'sq-safe')); warn(msg + T.expl); }\n  else if (T.type === 'marks') { revealMarks(); warn(msg + T.expl); }")
sub("    setTimeout(() => drawArrows([[f, t, 'g']]), 300);", "    setTimeout(() => { drawArrows([[f, t, 'g']]); clearMarks(); markChecks(pos); }, 300);")

assert 'L5' not in s.replace('nivel1_lectia5', ''), [m.start() for m in re.finditer('L5', s)][:5]
open(R + 'nivel1_lectia6.html', 'w', encoding='utf-8', newline='').write(s)
print('ok', len(s))
