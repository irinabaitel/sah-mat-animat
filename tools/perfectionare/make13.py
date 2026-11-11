# nivel1_lectia3.html (Mutări speciale, scheletul aprobat) -> nivel1_lectia13.html (Piese atârnate)
# Păstrează textele și pozițiile lecției vechi (vechea pagină e citită din git: e1c0243.. ultima versiune înainte de refacere),
# sertarele: Ce faci când ai o piesă atârnată / Piese atârnate în partide, apoi Exerciții (3 niveluri) și Exersează.
# Cele 5 poziții „Capturează piesa atârnată!” devin primul set din Exerciții (le faci tu pe tablă).
import re, sys, json, subprocess, chess
sys.stdout.reconfigure(encoding='utf-8')
R = r'C:/Users/irina/SahMatAnimat/'
s = open(R + 'nivel1_lectia3.html', encoding='utf-8').read()
old = subprocess.run(['git', '-C', R, 'show', 'bc25c64:nivel1_lectia13.html'], capture_output=True, text=True, encoding='utf-8').stdout
assert 'const chapters' in old

def sub(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90]); s = s.replace(a, b)
def resub(pat, new):
    global s
    s2, n = re.subn(pat, lambda m: new, s, flags=re.S); assert n == 1, (n, pat[:80]); s = s2

# ── capitolele vechi, citite din pagina veche ──
chs = re.search(r'const chapters = \[(.*?)\n\];', old, re.S).group(1)
items = re.split(r'\n  /\* \d+ — [^*]*\*/\n', chs)[1:]
def jsval(txt, key, kind='str'):
    if kind == 'str':
        m = re.search(key + r":\s*'((?:[^'\\]|\\.)*)'", txt); return m.group(1) if m else None
    m = re.search(key + r':\s*(\[[^\]]*\])', txt); return json.loads(m.group(1).replace("'", '"')) if m else None
CH = []
for it in items:
    ann = dict((int(k), v) for k, v in re.findall(r"\n\s*(\d+): '((?:[^'\\]|\\.)*)'", it))
    CH.append(dict(fen=jsval(it, 'fen'), orient=jsval(it, 'orient'), san=jsval(it, 'san', 'arr'), safe=jsval(it, 'safeSquares', 'arr'), ann=ann))
assert len(CH) == 12, len(CH)
acc = re.search(r'const accData = \[(.*?)\n\];', old, re.S).group(1)
AD = [dict(ch=(None if m[0] == 'null' else int(m[0])), title=m[1], desc=m[2]) for m in
      re.findall(r"\{ chIdx: (\w+), kind: '\w+', num: '[^']*', title: '((?:[^'\\]|\\.)*)'.*?desc: '((?:[^'\\]|\\.)*)' \}", acc, re.S)]
assert len(AD) == 13, len(AD)

RO = {'R': 'K', 'D': 'Q', 'T': 'R', 'N': 'B', 'C': 'N'}
def steps_of(c):
    b = chess.Board(c['fen']); out = [dict(fen=b.board_fen(), text=c['ann'].get(0, ''), arrow=None, hl=[])]
    if c['safe']:
        out.append(dict(fen=b.board_fen(), text=c['ann'].get(1, ''), arrow=None, hl=[[q, 'sq-h3'] for q in c['safe']]))
        return out
    for k, san in enumerate(c['san'], 1):
        m = b.parse_san(san); b.push(m)
        out.append(dict(fen=b.board_fen(), text=c['ann'].get(k, ''), arrow=[chess.square_name(m.from_square), chess.square_name(m.to_square)], hl=[]))
    return out
def demo(ad):
    d = dict(title=ad['title'], desc=ad['desc'])
    if ad['ch'] is not None:
        c = CH[ad['ch']]; d['orient'] = c['orient']; d['steps'] = steps_of(c)
    return d
DEMOS = dict(def_=[demo(a) for a in AD[0:5]], game=[demo(a) for a in AD[5:8]])
DEMOS['def'] = DEMOS.pop('def_')
CAPT = [CH[a['ch']] for a in AD[8:13]]      # cele 5 „Capturează piesa atârnată!” → exerciții

# ── exercițiile: adaugă setul cu cele 5 poziții la începutul tabului „De bază” ──
exs = open(R + 'data/nivel1_lectia13_ex.js', encoding='utf-8').read()
EX = json.loads(exs[exs.index('{'):exs.rindex(';')])
if EX['tabs'][0]['sets'][0]['id'] != 'capt':
    tasks = []
    for c in CAPT:
        b = chess.Board(c['fen']); m = b.parse_san(c['san'][0])
        expl = re.sub(r'^<strong>[^<]*</strong>\s*—\s*', '', c['ann'][1])
        tasks.append(dict(type='move', fen=c['fen'], side='w' if b.turn else 'b', answer=m.uci(), san=c['san'][0], ok=[], check='best',
                          expl='Corect! ' + expl[0].upper() + expl[1:],
                          failmsg='Nu este piesa atârnată. Caută o piesă a adversarului care e atacată și pe care nu o apără nimeni.'))
    EX['tabs'][0]['sets'].insert(0, dict(id='capt', title='🎯 Capturează piesa atârnată', src='lecția veche (Steps)',
        intro='Adversarul are o piesă <strong>atârnată</strong>: e atacată și nu o apără nimeni. Găsește-o și captureaz-o.',
        instr='Capturează piesa atârnată.', tasks=tasks))
    open(R + 'data/nivel1_lectia13_ex.js', 'w', encoding='utf-8').write(exs[:exs.index('{')] + json.dumps(EX, ensure_ascii=False) + ';\n')

# ═════════ pagina ═════════
sub('<title>Mutări speciale</title>', '<title>Piese atârnate</title>')
sub('<span class="header-title">Mutări speciale</span>', '<span class="header-title">Piese atârnate</span>')

def demo_block(key, label_btn):
    return f'''<div class="demo-pick" id="{key}-pick"></div>
              <div class="demo-title" id="{key}-title"></div>
              <div class="demo-desc" id="{key}-desc"></div>
              <span class="demo-badge" id="{key}-badge"></span>
              <div class="demo-text" id="{key}-text"></div>
              <div class="step-btns" id="{key}-steps">
                <button class="step-btn" id="{key}-prev" onclick="demoStep('{key}', -1)">◀ Înapoi</button>
                <button class="step-btn" id="{key}-next" onclick="demoStep('{key}', 1)">Înainte ▶</button>
              </div>'''

resub(r'<div id="acc-wrapper">.*?</div><!-- /acc-wrapper -->', f'''<div id="acc-wrapper">
          <div class="hl-box">
            <p><strong>Piesa atârnată</strong> este o piesă atacată, care poate fi capturată gratis pentru că nimeni nu o apără.</p>
            <p>Uneori le găsim pe tablă datorită neatenției adversarului (asta se întâmplă la începători, jucătorii avansați nu fac astfel de greșeli), dar, pe măsură ce devenim mai buni la șah, învățăm să folosim diverse tactici pentru a-l face pe adversar să rămână cu o piesă atârnată.</p>
            <p><strong>Ce sunt tacticile?</strong> Mutări și idei pe termen scurt prin care se obține un avantaj imediat.</p>
          </div>

          <!-- ── ACC 0: CE FACI CÂND AI O PIESĂ ATÂRNATĂ ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc0" onclick="toggleAcc(0)"><span>🛡️ Ce faci când ai o piesă atârnată?</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body0"><div class="acc-inner">
              <p>E rândul tău la mutare și ai o piesă atârnată. Ai cinci răspunsuri. Alege unul ca să-l vezi pe tablă:</p>
              {demo_block('def', '')}
              <button class="step-btn" onclick="goExercises()">🧩 Exerciții →</button>
            </div></div>
          </div>

          <!-- ── ACC 1: PIESE ATÂRNATE ÎN PARTIDE ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc1" onclick="toggleAcc(1)"><span>🎯 Piese atârnate în partide</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body1"><div class="acc-inner">
              {demo_block('game', '')}
              <div class="hl-box ok"><strong>Reține asta din lecție</strong><br><strong>Când muți, ai grijă ca piesa ta să fie în siguranță.</strong> Întreabă-te întotdeauna dacă pătrățelul pe care muți piesa este sigur.</div>
              <button class="step-btn" onclick="goExercises()">🧩 Exerciții →</button>
            </div></div>
          </div>

          <!-- ── ACC 2: EXERCIȚII ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc2" onclick="toggleAcc(2)"><span>🧩 Exerciții</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body2"><div class="acc-inner">
              <div class="tabs" id="tabs"></div>
              <div class="tab-desc" id="tab-desc"></div>
              <div id="set-list" style="display:flex;flex-direction:column;gap:8px;"></div>
              <p class="src-note">Exercițiile sunt preluate din caietul metodei Steps, din lecțiile ChessKid și din programul Chess Tutor.</p>
            </div></div>
          </div>

          <!-- ── ACC 3: EXERSEAZĂ ── -->
          <div class="acc-item">
            <div class="acc-head" id="mAcc3" onclick="toggleAcc(3)"><span>🎮 Exersează!</span><span class="acc-icon">▶</span></div>
            <div class="acc-body" id="body3"><div class="acc-inner">
              <p>Alege un joc sau intră în arenă.</p>
              <a href="nivel1_joc_cal_neaparate.html" class="practice-btn pb-blue">♘ Calul și piesele neapărate<small>Calul capturează piesele pe care nu le apără nimeni</small></a>
              <a href="nivel1_arena_atarnate.html" class="practice-btn pb-green">🎯 Arena pieselor atârnate<small>40 de poziții din partide reale: capturează piesa neapărată</small></a>
            </div></div>
          </div>
        </div><!-- /acc-wrapper -->''')

sub('''.sq-h4 { background-image: linear-gradient(rgba(220,60,60,0.45), rgba(220,60,60,0.45)) !important; }''',
    '''.sq-h4 { background-image: linear-gradient(rgba(220,60,60,0.45), rgba(220,60,60,0.45)) !important; }
    .demo-pick { display:flex; flex-direction:column; gap:6px; margin:6px 0 10px; }
    .demo-pick .mode-btn { text-align:left; white-space:normal; line-height:1.35; }
    .demo-desc { font-size:0.92rem; margin:4px 0 8px; }
    .demo-desc:empty { display:none; }''')

DJS = 'var DEMOS = ' + json.dumps(DEMOS, ensure_ascii=False) + ';\n' + r'''
var DSTATE = { def: { k: 0, i: 0 }, game: { k: 0, i: 0 } }, accOpen = -1;
function demoSound(a, b) {
  const ka = Object.keys(a), kb = Object.keys(b);
  if (['w', 'b'].some(c => isMated(b, c))) playSnd(sndMate);
  else playSnd(kb.length < ka.length ? sndCapture : sndMove, b);
}
function demoPick(key) {
  document.getElementById(key + '-pick').innerHTML = DEMOS[key].map((d, k) =>
    '<button class="mode-btn' + (k === DSTATE[key].k ? ' active' : '') + '" onclick="demoChoose(\'' + key + '\',' + k + ')">' + (key === 'def' ? (k + 1) + '. ' : '') + d.title + '</button>').join('');
}
function demoChoose(key, k) { DSTATE[key] = { k: k, i: 0 }; demoRender(key); }
function demoRender(key, prev) {
  mode = 'lesson';
  const st = DSTATE[key], d = DEMOS[key][st.k];
  demoPick(key);
  document.getElementById(key + '-title').innerHTML = key === 'def' ? '' : d.title;
  document.getElementById(key + '-desc').innerHTML = d.desc;
  clearMarks(); clearArrows(); clearFeedback();
  const stepsEl = document.getElementById(key + '-steps');
  if (!d.steps) {
    stepsEl.style.display = 'none';
    document.getElementById(key + '-badge').textContent = ''; document.getElementById(key + '-text').innerHTML = '';
    return;
  }
  stepsEl.style.display = '';
  makeBoard(true, d.orient || 'white');
  const s = d.steps[st.i], p = fenToPos(s.fen + ' w - - 0 1');
  if (prev !== undefined && st.i === prev + 1) demoSound(fenToPos(d.steps[prev].fen + ' w - - 0 1'), p);
  board.position(p, prev !== undefined);
  setTimeout(() => { clearMarks(); s.hl.forEach(h => mark(h[0], h[1])); markChecks(p); if (s.arrow) drawArrows([[s.arrow[0], s.arrow[1], 'g']]); }, 220);
  document.getElementById(key + '-badge').textContent = d.steps.length > 1 ? 'Pasul ' + (st.i + 1) + ' din ' + d.steps.length : '';
  document.getElementById(key + '-text').innerHTML = s.text;
  document.getElementById(key + '-prev').disabled = st.i === 0;
  document.getElementById(key + '-next').disabled = st.i === d.steps.length - 1;
}
function demoStep(key, delta) {
  const st = DSTATE[key], n = DEMOS[key][st.k].steps.length, prev = st.i;
  st.i = Math.max(0, Math.min(n - 1, st.i + delta));
  if (st.i !== prev) demoRender(key, prev);
}

function toggleAcc(idx) {
  const was = accOpen === idx;
  [0, 1, 2, 3].forEach(i => { document.getElementById('body' + i).classList.remove('open'); document.getElementById('mAcc' + i).classList.remove('open'); });
  accOpen = was ? -1 : idx;
  if (!was) { document.getElementById('body' + idx).classList.add('open'); document.getElementById('mAcc' + idx).classList.add('open'); }
  setTimeout(() => {
    if (mode === 'task') return;
    const key = ['def', 'game'][accOpen];
    if (key) { DSTATE[key].i = 0; demoRender(key); }
    else { mode = 'lesson'; makeBoard(true, 'white'); clearMarks(); clearArrows(); clearFeedback(); board.position('start', false); }
  }, 30);
}
'''
resub(r'/\* ═════════ Demonstrațiile din sertare.*?(?=/\* derulează doar panoul)', '/* ═════════ Exemplele din sertare (pozițiile lecției, pas cu pas) ═════════ */\n' + DJS)
sub("""  if (accOpen !== 3) toggleAcc(3);
  scrollPanelTo(document.getElementById('mAcc3'));""", """  if (accOpen !== 2) toggleAcc(2);
  scrollPanelTo(document.getElementById('mAcc2'));""", 2)
# clasele de evidențiere din exemple se șterg și ele
sub("el.classList.remove('highlight-check','hint-square',", "el.classList.remove('sq-h2','sq-h3','sq-h4','highlight-check','hint-square',")

resub(r"const SAVE_KEY = '[^']*';", "const SAVE_KEY = 'n1l13_ex_v1';")
resub(r"const TAB_DESC = \{.*?\};", """const TAB_DESC = {
  baza: 'Capturează piesa atârnată a adversarului și pune-ți la adăpost piesa atârnată.',
  mediu: 'Dintre mai multe capturi, alege-o pe cea care câștigă material.',
  avansat: 'Când trebuie să capturezi ca să te aperi, alege captura după care nu pierzi nimic.'
};""")
s = s.replace('L3EX', 'L13EX')
sub('<script src="data/nivel1_lectia3_ex.js?v=2"></script>', '<script src="data/nivel1_lectia13_ex.js?v=1"></script>')
sub('<a href="nivel1_lectia6.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Atacul asupra regelui</span></a>',
    '<a href="nivel1_lectia3.html" class="nav-btn nav-btn--back"><span class="icon" aria-hidden="true">&#8592;</span><span class="label">Mutări speciale</span></a>')
sub('<a href="nivel1_lectia13.html" class="nav-btn nav-btn--forward"><span class="label">Piese atârnate</span><span class="icon" aria-hidden="true">&#8594;</span></a>',
    '<a href="nivel1_lectia15.html" class="nav-btn nav-btn--forward"><span class="label">Numărarea atacatorilor și apărătorilor</span><span class="icon" aria-hidden="true">&#8594;</span></a>')
open(R + 'nivel1_lectia13.html', 'w', encoding='utf-8').write(s)
print('ok', len(s), 'demos', len(DEMOS['def']), len(DEMOS['game']))
