===FILE===
nivel1_joc_schimba_nebunii.html
===TITLE===
Schimbă nebunii — Joc
===HEADER===
♗ Schimbă nebunii
===PANEL===
        <div class="toggle-row">
          <button class="tgl-btn active" id="modeSolo" onclick="setMode('solo')">👤 Singur</button>
          <button class="tgl-btn"        id="modeDuo"  onclick="setMode('duo')">👫 În doi</button>
        </div>

        <div class="counter-row">
          <div class="counter-box"><div class="counter-lbl">Mutări</div><div class="counter-val" id="movesVal">0</div></div>
          <div class="counter-box"><div class="counter-lbl">La mutare</div><div class="counter-val" id="turnVal">Albul</div></div>
        </div>

        <div id="duoPanels" style="display:none">
          <div class="player-panel" id="pp1"><div class="pp-row"><span class="pp-name">👤 Jucătorul 1</span><span class="pp-strikes" id="pp1-strikes"></span></div><div class="pp-role">♗ nebunii albi</div></div>
          <div class="player-panel" id="pp2"><div class="pp-row"><span class="pp-name">👤 Jucătorul 2</span><span class="pp-strikes" id="pp2-strikes"></span></div><div class="pp-role">♝ nebunii negri</div></div>
        </div>

        <div id="status-box"></div>

        <button class="btn-game" id="btn-undo" onclick="undo()">⟲ Ia înapoi ultima mutare</button>
        <button class="btn-game" onclick="newGame()">↺ Joacă din nou</button>
        <button class="btn-game" id="btn-show" onclick="showSolution()" style="background:rgba(255,255,255,0.4)">👁 Arată o soluție</button>

        <details class="howto" open>
          <summary>📖 Cum se joacă</summary>
          <div class="hl-box">
            <h4>Piesele</h4>
            <p>Albul are doi <strong>nebuni</strong>, pe c1 și pe f1. Negrul are doi nebuni, pe c8 și pe f8.</p>
          </div>
          <div class="hl-box">
            <h4>Ce trebuie să faci</h4>
            <p><strong>Schimbă locurile nebunilor</strong>: nebunii albi ajung pe c8 și pe f8, iar nebunii negri pe c1 și pe f1.</p>
            <p>Muți pe rând cu albul și cu negrul: o mutare albul, o mutare negrul. Începe albul.</p>
          </div>
          <div class="hl-box warn">
            <h4>Regula importantă</h4>
            <p>Pe drum, nebunii albi și nebunii negri <strong>nu au voie să se atace</strong> niciodată. Nicio mutare nu are voie să pună un nebun pe aceeași diagonală liberă cu un nebun al adversarului.</p>
            <p>Nebunul de pe pătrate albe nu-l poate ataca niciodată pe cel de pe pătrate negre. Fii atent la nebunii care merg pe aceeași culoare.</p>
          </div>
          <div class="hl-box">
            <h4>Câte mutări</h4>
            <p>Se poate în <strong>12 mutări</strong> (6 ale albului și 6 ale negrului). Dacă te-ai încurcat, poți lua înapoi ultima mutare.</p>
            <p id="ruleDuo" style="display:none"><strong>În doi</strong>, jucați împreună: Jucătorul 1 mută nebunii albi, Jucătorul 2 pe cei negri. Câștigați amândoi dacă schimbați locurile.</p>
          </div>
          <p class="pp-role" style="margin-top:8px">Jocul vine din programul Chess Tutor Step 1 (metoda Steps), lecția 3.</p>
        </details>
===SCRIPT===
/* =====================================================
   SCHIMBĂ NEBUNII (Chess Tutor Step 1, lecția 3, joc 3d)
   Nebunii albi c1,f1 și negri c8,f8 își schimbă locurile, mutând pe rând,
   fără să se atace vreodată. Minimum 12 mutări.
   ===================================================== */
/*COMMON*/
const SOLUTION = ['c1-b2', 'c8-g4', 'f1-g2', 'g4-e2', 'g2-h3', 'f8-b4', 'b2-g7', 'b4-d2', 'h3-c8', 'd2-c1', 'g7-f8', 'e2-f1'];
let board, mode = 'solo', W, B, turn, hist, over, selSq = null, demo = null, strikes = { 1: 0, 2: 0 };
const occ = s => W.includes(s) || B.includes(s);
const pname = p => 'Jucătorul ' + p;
const curPlayer = () => turn === 'w' ? 1 : 2;
function attackPair(Wx, Bx) {                     // [alb, negru] care se atacă, sau null
    const o = s => Wx.includes(s) || Bx.includes(s);
    for (const w of Wx) for (const t of slide(w, DIA, o)) if (Bx.includes(t)) return [w, t];
    return null;
}
function buildPos() { const p = {}; W.forEach(s => p[name(s)] = 'wB'); B.forEach(s => p[name(s)] = 'bB'); return p; }
function own(s) { return (turn === 'w' ? W : B).includes(s); }
function targetsOf(s) { return own(s) ? slide(s, DIA, occ).filter(t => !occ(t)) : []; }
function problem(f, t) {
    if (!targetsOf(f).includes(t)) return occ(t) ? 'Aici nu se capturează: nebunii doar își schimbă locurile.' : 'Nebunul merge numai pe diagonală și nu sare peste piese.';
    const W2 = W.map(s => s === f ? t : s), B2 = B.map(s => s === f ? t : s);
    const a = attackPair(W2, B2);
    if (a) return 'Nu se poate: nebunul alb de pe ' + name(a[0]) + ' și nebunul negru de pe ' + name(a[1]) + ' s-ar ataca.';
    return null;
}
function anyLegal() {
    for (const f of (turn === 'w' ? W : B)) for (const t of targetsOf(f)) if (!problem(f, t)) return true;
    return false;
}
const done = () => W.includes(idx('c8')) && W.includes(idx('f8')) && B.includes(idx('c1')) && B.includes(idx('f1'));

function showSelection(sq) {
    clearHL(true); $('.square-' + sq).addClass('highlight-selected');
    targetsOf(idx(sq)).forEach(t => $('.square-' + name(t)).addClass('highlight-legal'));
}
function updateUI() {
    document.getElementById('movesVal').textContent = hist.length;
    document.getElementById('turnVal').textContent = turn === 'w' ? 'Albul' : 'Negrul';
    [1, 2].forEach(p => {
        document.getElementById('pp' + p + '-strikes').textContent = '❌'.repeat(strikes[p]) + '▫️'.repeat(MAX_STRIKES - strikes[p]);
        document.getElementById('pp' + p).className = 'player-panel' + (!over && curPlayer() === p ? ' active' : '');
    });
    document.getElementById('btn-undo').disabled = !hist.length || over || !!demo;
}
function turnMsg() {
    const who = turn === 'w' ? 'un nebun alb' : 'un nebun negru';
    return mode === 'duo' ? pname(curPlayer()) + ' mută ' + who + '.' : 'Mută ' + who + '.';
}

function newGame() {
    stopDemo();
    W = [idx('c1'), idx('f1')]; B = [idx('c8'), idx('f8')]; turn = 'w'; hist = []; over = false; selSq = null; strikes = { 1: 0, 2: 0 };
    board.position(buildPos(), false); clearHL();
    setStatus(turnMsg()); updateUI();
}
function apply(f, t, quiet) {
    hist.push([f, t]);
    const L = turn === 'w' ? W : B; L[L.indexOf(f)] = t;
    turn = turn === 'w' ? 'b' : 'w'; selSq = null;
    board.position(buildPos(), false); clearHL(); markLast(name(f), name(t)); play(sndMove);
    if (done()) return finish();
    if (quiet) { updateUI(); return; }
    if (!anyLegal()) setStatus('🚧 ' + (turn === 'w' ? 'Albul' : 'Negrul') + ' nu mai are nicio mutare permisă. Ia înapoi o mutare sau două și încearcă alt drum.', 'warn');
    else setStatus(turnMsg());
    updateUI();
}
function finish() {
    over = true; setTimeout(() => play(sndMate), 250);
    let msg = '🏆 Nebunii și-au schimbat locurile în <strong>' + hist.length + (hist.length >= 20 ? ' de' : '') + ' mutări</strong>. ';
    if (demo) msg = '👁 Gata: o soluție în 12 mutări. Apasă „Joacă din nou” ca să încerci tu.';
    else {
        msg += hist.length <= 12 ? 'Cel mai scurt drum!' : 'Se poate și în 12 mutări.';
        msg += '<br>' + (hist.length <= 12 ? '⭐⭐⭐' : hist.length <= 16 ? '⭐⭐☆' : '⭐☆☆');
        if (mode === 'duo') msg += '<br>Ați reușit împreună.';
        if (typeof spawnConfetti === 'function') spawnConfetti(2);
    }
    setStatus(msg, 'ok'); updateUI();
}
function undo() {
    if (!hist.length || over || demo) return;
    const [f, t] = hist.pop();
    turn = turn === 'w' ? 'b' : 'w';
    const L = turn === 'w' ? W : B; L[L.indexOf(t)] = f;
    selSq = null; board.position(buildPos(), false); clearHL();
    setStatus('⟲ Am luat înapoi ' + name(f) + '–' + name(t) + '. ' + turnMsg()); updateUI();
}
function illegal(sq, reason) {
    if (sq) flashWrong(sq);
    selSq = null; clearHL(true);
    if (mode !== 'duo') { setStatus('⚠️ ' + reason, 'warn'); return; }
    const p = curPlayer(); strikes[p]++; updateUI();
    if (strikes[p] >= MAX_STRIKES) {
        over = true; updateUI();
        setStatus('❌ ' + reason + '<br>' + pname(p) + ' a încercat 3 mutări nepermise. Jocul se termină. Apăsați „Joacă din nou”.', 'warn');
        return;
    }
    setStatus('❌ ' + reason + ' Încercări nepermise pentru ' + pname(p) + ': ' + strikes[p] + ' din ' + MAX_STRIKES + '.', 'warn');
}
function tryMove(from, to) {
    const why = problem(idx(from), idx(to));
    if (why) return illegal(to, why);
    apply(idx(from), idx(to));
}
function stopDemo() { if (demo) { clearTimeout(demo); demo = null; } }
function showSolution() {
    newGame(); let i = 0;
    setStatus('👁 Urmărește o soluție în 12 mutări.');
    const stepf = () => {
        if (i >= SOLUTION.length) { demo = null; return; }
        const [a, b] = SOLUTION[i++].split('-');
        apply(idx(a), idx(b), true);
        if (over) { demo = null; updateUI(); return; }
        demo = setTimeout(stepf, 1000);
    };
    demo = setTimeout(stepf, 600); updateUI();
}
function setMode(m) {
    mode = m;
    document.getElementById('modeSolo').className = 'tgl-btn' + (m === 'solo' ? ' active' : '');
    document.getElementById('modeDuo').className  = 'tgl-btn' + (m === 'duo' ? ' active' : '');
    ['duoPanels', 'ruleDuo'].forEach(id => document.getElementById(id).style.display = m === 'duo' ? '' : 'none');
    newGame();
}

/* ---------- input: click și drag ---------- */
function canAct() { return !over && !demo; }
board = Chessboard('board', {
    position: 'empty', pieceTheme: 'https://lichess1.org/assets/piece/caliente/{piece}.svg',
    draggable: true, showNotation: true,
    onDragStart: function (source) {
        if (!canAct()) return false;
        const s = idx(source);
        if (selSq && source !== selSq && !own(s)) { const from = selSq; setTimeout(() => tryMove(from, source), 0); return false; }
        if (!own(s)) { illegal(source, turn === 'w' ? 'Acum mută albul.' : 'Acum mută negrul.'); return false; }
        selSq = source; showSelection(source);
    },
    onDrop: function (source, target) {
        if (target === 'offboard' || target === source) return 'snapback';
        selSq = null;
        const why = problem(idx(source), idx(target));
        if (why) { illegal(target, why); return 'snapback'; }
        apply(idx(source), idx(target));
    },
    onSnapEnd: function () { board.position(buildPos(), false); }
});
$(document).on('click', '#board [class*="square-"]', function () {
    if (!canAct() || !selSq) return;
    const m = (this.className || '').match(/square-([a-h][1-8])/); if (!m) return;
    const sq = m[1];
    if (sq === selSq || occ(idx(sq))) return;
    tryMove(selSq, sq);
});
$(window).resize(() => board.resize());
newGame();
