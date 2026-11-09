# Construieste nivel1_arena_pat.html din pagina90a.html (arena model)
import re, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
s = open('pagina90a.html', encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b, 1)

rep('<title>Arenă Subpromovarea — Nivelul IV</title>', '<title>Arena patului — Nivelul I</title>')
rep('<span class="header-title">Arenă Subpromovarea</span>', '<span class="header-title">Arena patului</span>')
rep('<span class="lesson-badge">40 puzzle-uri</span>', '<span class="lesson-badge">43 de poziții</span>')
rep('<div class="panel-heading">Subpromovarea</div>', '<div class="panel-heading">Patul: salvează-te sau ferește-te</div>')
rep('<span class="level-badge" id="levelBadge">UȘOR</span>', '<span class="level-badge" id="levelBadge">SALVEAZĂ PRIN PAT</span>')
rep('''                onclick="resetAll()">🎉 Totul rezolvat! Joacă din nou →</button>''',
'''                onclick="resetAllProgress()">🎉 Totul rezolvat! Joacă din nou →</button>
        <button class="btn-arena" id="resetAllBtn" onclick="resetAllProgress()"
                style="display:none; margin-top:8px; background:rgba(192,57,43,0.82);">
          ↺ Joacă din nou (resetează tot)
        </button>
        <p class="src-note">Pozițiile vin din programul Chess Tutor Step 2 (metoda Steps), lecția despre pat.</p>''')
rep('''<button class="arena-back-btn" onclick="window.location='pagina90.html'">← Subpromovarea</button>''',
    '''<button class="arena-back-btn" onclick="window.location='nivel1_lectia17.html'">← Lecția Patul</button>''')
rep('''    <a href="pagina90.html" class="nav-btn nav-btn--back">
      <span class="icon">←</span><span class="label">Lecție Subpromovarea</span>''', '''    <a href="nivel1_lectia17.html" class="nav-btn nav-btn--back">
      <span class="icon">←</span><span class="label">Lecția Patul</span>''')
rep('''    <a href="pagina91.html" class="nav-btn nav-btn--forward">
      <span class="icon">→</span><span class="label">Desperado</span>''', '''    <a href="nivel1_lectia12.html" class="nav-btn nav-btn--forward">
      <span class="icon">→</span><span class="label">Câștig, egal și pierdere</span>''')
rep('    .last-move-to   { background: rgba(80,180,80,0.55) !important; }', '''    .last-move-to   { background: rgba(80,180,80,0.55) !important; }
    .sq-pat { box-shadow: inset 0 0 0 4px #e6b800, inset 0 0 18px rgba(230,184,0,0.75) !important; }
    .src-note { font-size:0.8rem; color:rgba(26,26,46,.55); margin-top:10px; }
    .board-wrapper { position: relative; }''')
rep("const SAVE_KEY = 'underpromotion_arena_progress';", "const SAVE_KEY = 'stalemate_arena_ct2_progress';")
rep("const LEVEL_LABELS  = ['UȘOR', 'MEDIU', 'GREU'];", "const KIND_LABELS = { defend: 'SALVEAZĂ PRIN PAT', avoid: 'NU DA PAT' };")
rep("const LEVEL_CLASSES = ['', 'med', 'hard'];",
    "let hintStage = 0;\nvar sndMove = new Audio('Sounds/Move.mp3'), sndCapture = new Audio('Sounds/Capture.mp3'), sndMate = new Audio('Sounds/Mate.mp3');\nfunction playSnd(a) { try { a.currentTime = 0; a.play().catch(function () {}); } catch (e) {} }")
rep("document.querySelectorAll('.square-selected,.highlight-check,.last-move-from,.last-move-to')\n    .forEach(el => el.classList.remove('square-selected','highlight-check','last-move-from','last-move-to'));",
    "document.querySelectorAll('.square-selected,.highlight-check,.last-move-from,.last-move-to,.sq-pat')\n    .forEach(el => el.classList.remove('square-selected','highlight-check','last-move-from','last-move-to','sq-pat'));")

# --- logica mutarilor
a = s.index('function finishUserMove'); b = s.index('/* ── Move history')
s = s[:a] + r'''function promptText() {
  const p = PUZZLES[curIdx];
  const who = '<b>' + (solverColor === 'w' ? 'Albul' : 'Negrul') + ' la mutare.</b> ';
  return who + (p.kind === 'defend'
    ? 'Poziția e pierdută. Salvează partida prin pat.'
    : 'Ești în câștig. Joacă cea mai bună mutare, fără să dai pat.');
}
function kingSq(color) {
  const B = chess.board();
  for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) {
    const q = B[r][c];
    if (q && q.type === 'k' && q.color === color) return 'abcdefgh'[c] + (8 - r);
  }
  return null;
}
function markState() {
  if (!chess) return;
  document.querySelectorAll('.highlight-check,.sq-pat').forEach(el => el.classList.remove('highlight-check','sq-pat'));
  if (chess.in_check()) applyHL(kingSq(chess.turn()), 'highlight-check');
  else if (chess.in_stalemate()) applyHL(kingSq(chess.turn()), 'sq-pat');
}
function afterMoveFx(move) {
  if (chess.in_checkmate()) playSnd(sndMate);
  else playSnd(move.captured ? sndCapture : sndMove);
  markState();
}

function finishUserMove(from, to, promotion) {
  const move = chess.move({ from, to, promotion: promotion || 'q' });
  if (!move) { board.position(chess.fen(), false); return; }
  board.position(chess.fen(), true);
  recordMove(from, to, promotion);
  setLastMoveHL(from, to);
  afterMoveFx(move);
  clearPracHint(); hintStage = 0;
  curMoveIdx++;
  if (curMoveIdx >= PUZZLES[curIdx].moves.length) {
    onSolved();
  } else {
    setMsg('idle', '✓ Bună mutare! Răspunde adversarul…');
    setTimeout(opponentReply, 600);
  }
}

function wrongMove(from, to, prom) {
  const p = PUZZLES[curIdx];
  const t = new Chess(chess.fen());
  const m = t.move({ from, to, promotion: prom || 'q' });
  let txt = '❌ Nu e cea mai bună mutare. Mai încearcă!';
  if (m && t.in_stalemate() && p.kind === 'avoid') txt = '❌ Ai da pat și partida s-ar termina la egalitate. Caută altă mutare!';
  else if (m && p.kind === 'defend') txt = '❌ Așa nu se salvează partida. Mai încearcă!';
  shakeBoard();
  setMsg('err', txt);
  setTimeout(() => { if (solving && !solved) setMsg('idle', promptText()); }, 1800);
}

function tryMove(from, to) {
  if (!solving || solved) return 'snapback';
  if (!chess.moves({ square: from, verbose: true }).some(m => m.to === to)) return 'snapback';
  const expected = PUZZLES[curIdx].moves[curMoveIdx];
  const piece   = chess.get(from);
  const isProm  = piece && piece.type === 'p' && (to[1] === '8' || to[1] === '1');
  const expProm = expected.length > 4 ? expected.slice(4) : null;

  if (isProm) {
    pendingPromo = true;
    const visual = board.position();
    if (visual[from]) {
      visual[to] = visual[from];
      delete visual[from];
      board.position(visual, false);
    }
    showPromoPicker(from, to, piece.color, function (chosen) {
      pendingPromo = false;
      if (chosen === null) {
        board.position(chess.fen(), false);
        return;
      }
      if (from !== expected.slice(0,2) || to !== expected.slice(2,4) || chosen !== expProm) {
        board.position(chess.fen(), false);
        wrongMove(from, to, chosen);
        return;
      }
      finishUserMove(from, to, chosen);
    });
    return undefined;
  }

  if (from !== expected.slice(0,2) || to !== expected.slice(2,4)) {
    wrongMove(from, to, 'q');
    return 'snapback';
  }
  finishUserMove(from, to, 'q');
  return undefined;
}

function opponentReply() {
  if (curMoveIdx >= PUZZLES[curIdx].moves.length) return;
  const mv = PUZZLES[curIdx].moves[curMoveIdx];
  const prom = mv.length > 4 ? mv.slice(4) : 'q';
  const moveObj = chess.move({ from: mv.slice(0,2), to: mv.slice(2,4), promotion: prom });
  if (moveObj) {
    board.position(chess.fen(), true);
    recordMove(mv.slice(0,2), mv.slice(2,4), prom);
    setLastMoveHL(mv.slice(0,2), mv.slice(2,4));
    afterMoveFx(moveObj);
    curMoveIdx++;
    if (curMoveIdx >= PUZZLES[curIdx].moves.length) onSolved();
    else setMsg('idle', 'E rândul tău.');
  }
}

function onSolved() {
  solved = true; solving = false;
  completed[curIdx] = true;
  saveState(); updateProgress(); celebrate();
  setMsg('ok', '✅ ' + PUZZLES[curIdx].expl);
  document.getElementById('nextBtn').disabled = (curIdx >= PUZZLES.length - 1);
  document.getElementById('btnHint').disabled = true;
  document.getElementById('btnSol').disabled  = true;
  if (Object.keys(completed).length >= PUZZLES.length) {
    document.getElementById('playAgainBtn').style.display = 'flex';
  }
}

''' + s[b:]

rep("""    applyHL(moveHistory[idx - 1].to,   'last-move-to');
  }
}""", """    applyHL(moveHistory[idx - 1].to,   'last-move-to');
  }
  const keep = chess; chess = temp; markState(); chess = keep;
}""")

# loadPuzzle: fara mutare de setup
a = s.index('  const setup = p.moves[0];'); b = s.index('  solverColor = chess.turn();')
s = s[:a] + '  curMoveIdx = 0;\n  clearPracHint(); hintStage = 0;\n\n' + s[b:]
rep("    setMsg('idle', '<b>' + (solverColor === 'w' ? 'Albul' : 'Negrul') + ' la mutare.</b> Promovează — dar fii atent ce piesă alegi!');",
    "    setMsg('idle', promptText());")
rep("""  clearHL();
  setLastMoveHL(setup.slice(0,2), setup.slice(2,4));
}""", """  clearHL();
  markState();
}""")
rep("""  const lvl = Math.max(0, Math.min((p.level || 1) - 1, 2));
  const lb  = document.getElementById('levelBadge');
  lb.textContent = LEVEL_LABELS[lvl];
  lb.className   = 'level-badge' + (LEVEL_CLASSES[lvl] ? ' ' + LEVEL_CLASSES[lvl] : '');""",
"""  const lb  = document.getElementById('levelBadge');
  lb.textContent = KIND_LABELS[p.kind];
  lb.className   = 'level-badge' + (p.kind === 'avoid' ? ' med' : '');""")
rep("""  document.getElementById('progressOuter').setAttribute('data-tip', done + ' / ' + PUZZLES.length + ' rezolvate');""",
"""  document.getElementById('progressOuter').setAttribute('data-tip', done + ' / ' + PUZZLES.length + ' rezolvate');
  const rb = document.getElementById('resetAllBtn');
  if (rb) rb.style.display = (done > 0 && done < PUZZLES.length) ? 'flex' : 'none';""")

# indiciu in trepte
a = s.index('function showHint()'); b = s.index('function showSolution()')
s = s[:a] + r'''function clearPracHint() {
  document.querySelectorAll('.hint-square').forEach(el => el.classList.remove('hint-square'));
  const sv = document.getElementById('prac-hint-svg'); if (sv) sv.remove();
}
function drawPracHintArrow(from, to) {
  const old = document.getElementById('prac-hint-svg'); if (old) old.remove();
  const NS = 'http://www.w3.org/2000/svg';
  const bw = document.getElementById('boardWrapper'); if (!bw) return;
  const ori = board.orientation();
  const tlSq = bw.querySelector('[data-square="' + (ori === 'white' ? 'a8' : 'h1') + '"]');
  let sqSz, svgX = 0, svgY = 0;
  if (tlSq) {
    sqSz = tlSq.offsetWidth;
    const bwRect = bw.getBoundingClientRect(), tlRect = tlSq.getBoundingClientRect();
    svgX = Math.round(tlRect.left - bwRect.left); svgY = Math.round(tlRect.top - bwRect.top);
  } else { sqSz = bw.offsetWidth / 8; }
  const sz = sqSz * 8;
  const svg = document.createElementNS(NS, 'svg');
  svg.id = 'prac-hint-svg';
  svg.style.cssText = 'position:absolute;pointer-events:none;z-index:20;';
  svg.style.left = svgX + 'px'; svg.style.top = svgY + 'px';
  svg.style.width = sz + 'px'; svg.style.height = sz + 'px';
  const defs = document.createElementNS(NS, 'defs'); svg.appendChild(defs);
  const col = 'rgba(60,190,80,0.92)';
  const mk = document.createElementNS(NS, 'marker');
  mk.setAttribute('id', 'phintarr'); mk.setAttribute('markerWidth', '4'); mk.setAttribute('markerHeight', '4');
  mk.setAttribute('refX', '3.5'); mk.setAttribute('refY', '2'); mk.setAttribute('orient', 'auto');
  const mp = document.createElementNS(NS, 'path'); mp.setAttribute('d', 'M0,0 L4,2 L0,4 L1,2 Z'); mp.setAttribute('fill', col);
  mk.appendChild(mp); defs.appendChild(mk);
  function sqCenter(sq) { let c = sq.charCodeAt(0) - 97, r = parseInt(sq[1]) - 1; if (ori === 'black') { c = 7 - c; r = 7 - r; } const q = sz / 8; return { x: c * q + q / 2, y: (7 - r) * q + q / 2 }; }
  const f = sqCenter(from), t = sqCenter(to), dx = t.x - f.x, dy = t.y - f.y, len = Math.sqrt(dx * dx + dy * dy);
  if (len < 1) return;
  const ux = dx / len, uy = dy / len, SW = Math.max(3, sqSz * 0.09);
  const ln = document.createElementNS(NS, 'line');
  ln.setAttribute('x1', f.x); ln.setAttribute('y1', f.y); ln.setAttribute('x2', t.x - ux * SW); ln.setAttribute('y2', t.y - uy * SW);
  ln.setAttribute('stroke', col); ln.setAttribute('stroke-width', String(SW)); ln.setAttribute('stroke-linecap', 'round');
  ln.setAttribute('marker-end', 'url(#phintarr)');
  svg.appendChild(ln);
  bw.appendChild(svg);
}
/* Indiciu în trepte: 1) pătratul piesei → 2) + săgeata → 3) mutarea scrisă */
function showHint() {
  if (!solving || solved || viewIdx < moveHistory.length) return;
  const p = PUZZLES[curIdx];
  const mv = p.moves[curMoveIdx];
  const from = mv.slice(0, 2), to = mv.slice(2, 4);
  hintStage = Math.min(hintStage + 1, 3);
  clearPracHint();
  applyHL(from, 'hint-square');
  if (hintStage === 1) setMsg('idle', '💡 Mută piesa marcată cu verde.');
  else drawPracHintArrow(from, to);
  if (hintStage === 2) setMsg('idle', '💡 Urmează săgeata.');
  if (hintStage === 3) setMsg('idle', '💡 Mutarea: <b>' + p.san[curMoveIdx] + '</b>');
}

''' + s[b:]
rep("""  removePromoPicker();
  solving = false;
  const p = PUZZLES[curIdx];""", """  removePromoPicker();
  clearPracHint(); hintStage = 0;
  solving = false;
  const p = PUZZLES[curIdx];""")
rep("""    chess.move({ from: m.from, to: m.to, promotion: m.prom });
    board.position(chess.fen(), true);
    moveHistory.push(m);
    viewIdx++;
    setLastMoveHL(m.from, m.to);""", """    const mo = chess.move({ from: m.from, to: m.to, promotion: m.prom });
    board.position(chess.fen(), true);
    moveHistory.push(m);
    viewIdx++;
    setLastMoveHL(m.from, m.to);
    if (mo) afterMoveFx(mo);""")
rep("""      setMsg('idle', '🔑 Soluție completă. Apasă „↺ Resetează" ca s-o încerci tu.');""",
    """      setMsg('idle', '🔑 ' + p.expl + '<br>Apasă „↺ Resetează" ca s-o încerci tu.');""")
rep("""function resetAll() {""", """function resetAllProgress() {""")
rep("fetch('data/underpromotion_top40.json')", "fetch('data/stalemate_arena.json?v=20261110')")
rep("data/underpromotion_top40.json');", "data/stalemate_arena.json');")
rep("window.addEventListener('resize', debounce(() => { removePromoPicker(); board.resize(); }, 150));",
    "window.addEventListener('resize', debounce(() => { removePromoPicker(); board.resize(); clearPracHint(); hintStage = 0; markState(); }, 150));")
left = [m.start() for m in re.finditer('ubpromov|underprom|resetAll\\(', s)]
assert not left, [s[i-40:i+40] for i in left]
open('nivel1_arena_pat.html', 'w', encoding='utf-8').write(s)
print('ok')
