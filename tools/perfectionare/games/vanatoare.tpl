===FILE===
nivel1_joc_vanatoarea_nebunului.html
===TITLE===
Vânătoarea nebunului — Joc
===HEADER===
♝ Vânătoarea nebunului
===PANEL===
        <div class="toggle-row">
          <button class="tgl-btn active" id="modeRobot" onclick="setMode('robot')">🤖 Contra Robotului</button>
          <button class="tgl-btn"        id="modeDuo"   onclick="setMode('duo')">👫 În doi</button>
        </div>
        <div class="animal-grid" id="levelGrid">
          <button class="animal-btn active" data-random="0.9" onclick="setLevel(this)">🐣<span>Pui de găină</span></button>
          <button class="animal-btn" data-random="0.2" onclick="setLevel(this)">🐴<span>Mânz</span></button>
          <button class="animal-btn" data-random="0" onclick="setLevel(this)">🐉<span>Dragon</span></button>
        </div>

        <div class="counter-row">
          <div class="counter-box"><div class="counter-lbl">Repriza</div><div class="counter-val" id="roundVal">1 / 2</div></div>
          <div class="counter-box"><div class="counter-lbl">Mutările albului</div><div class="counter-val" id="movesVal">0 / 10</div></div>
        </div>

        <div id="duoPanels" style="display:none">
          <div class="player-panel" id="pp1"><div class="pp-row"><span class="pp-name">👤 Jucătorul 1</span><span class="pp-strikes" id="pp1-strikes"></span></div><div class="pp-role" id="pp1-role"></div><div class="pp-result" id="pp1-result"></div></div>
          <div class="player-panel" id="pp2"><div class="pp-row"><span class="pp-name">👤 Jucătorul 2</span><span class="pp-strikes" id="pp2-strikes"></span></div><div class="pp-role" id="pp2-role"></div><div class="pp-result" id="pp2-result"></div></div>
        </div>

        <div id="status-box"></div>

        <button id="btn-round2" onclick="startRound(2)">▶ Repriza 2 — schimbați rolurile</button>
        <button class="btn-game" onclick="newMatch()">↺ Joacă din nou</button>

        <details class="howto" open>
          <summary>📖 Cum se joacă</summary>
          <div class="hl-box">
            <h4>Piesele</h4>
            <p>Albul are trei piese: <strong>dama</strong> pe d1, <strong>turnul</strong> pe e1 și <strong>calul</strong> pe g1. Negrul are o singură piesă: <strong>nebunul</strong> pe c8. Pe tablă nu sunt regi.</p>
            <p>Albul mută primul. Apoi mută negrul. Apoi iar albul și tot așa, pe rând. La fiecare mutare muți o singură piesă.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea albul</h4>
            <p>Albul vrea să <strong>captureze nebunul</strong>. Are pentru asta <strong>10 mutări</strong>.</p>
            <p>Albul nu are voie să piardă nicio piesă. Dacă nebunul capturează o piesă albă, albul a pierdut, chiar dacă piesa era apărată.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea negrul</h4>
            <p>Negrul vrea ca nebunul <strong>să nu fie capturat</strong> timp de 10 mutări ale albului.</p>
            <p>Negrul câștigă și dacă nebunul capturează o piesă albă.</p>
          </div>
          <div class="hl-box warn">
            <h4>Ce e greu</h4>
            <p>Înainte de fiecare mutare, albul trebuie să se uite pe diagonalele nebunului. O piesă albă pusă pe o diagonală liberă a nebunului este pierdută.</p>
          </div>
          <div class="hl-box">
            <h4>Reprizele</h4>
            <p>În repriza 1 tu ești albul, iar în repriza 2 ești nebunul. <strong>În doi</strong>, Jucătorul 1 e albul în repriza 1 și nebunul în repriza 2. Câștigă meciul cine, cu albul, a capturat nebunul mai repede.</p>
          </div>
          <p class="pp-role" style="margin-top:8px">Jocul vine din programul Chess Tutor Step 2 (metoda Steps), lecția 12.</p>
        </details>
===SCRIPT===
/* =====================================================
   VÂNĂTOAREA NEBUNULUI (Chess Tutor Step 2, lecția 12, joc 12b)
   Dd1, Te1, Cg1 contra Nc8, fără regi. Albul trebuie să captureze nebunul
   în cel mult 10 mutări, fără să piardă nicio piesă.
   Robotul Dragon joacă după o tabelă completă (data/vanatoare_nebun.bin.gz):
   pentru fiecare poziție cu albul la mutare, în câte mutări capturează albul nebunul.
   ===================================================== */
/*COMMON*/
/*CORE-START*/
const LIMIT = 10, START = { q: 24, r: 32, n: 48, b: 23 };   // d1, e1, g1, c8
let TAB = null, PERFECT = 3;
const TRI = [0, 8, 9, 16, 17, 18, 24, 25, 26, 27], TRIX = new Int8Array(64).fill(-1);
TRI.forEach((s, i) => TRIX[s] = i);
const SYM = [(f, r) => [f, r], (f, r) => [7 - f, r], (f, r) => [f, 7 - r], (f, r) => [7 - f, 7 - r],
             (f, r) => [r, f], (f, r) => [7 - r, f], (f, r) => [r, 7 - f], (f, r) => [7 - r, 7 - f]];
const symSq = (t, s) => { const [f, r] = SYM[t](s >> 3, s & 7); return f * 8 + r; };
const W3 = ['q', 'r', 'n'];
function hits(p, s, t, occ) {                  // piesa p de pe s atacă t?
    if (p === 'n') return KN[s].includes(t);
    return slide(s, p === 'q' ? ORT.concat(DIA) : p === 'r' ? ORT : DIA, occ).includes(t);
}
const occOf = st => (x => x === st.q || x === st.r || x === st.n || x === st.b);
function whiteHits(st) { const o = occOf(st); return W3.filter(p => hits(p, st[p], st.b, o)); }
function bishopHits(st) { const o = occOf(st); return W3.filter(p => hits('b', st.b, st[p], o)); }
/* V = în câte mutări capturează albul nebunul, albul la mutare; 0 = nu poate forța captura */
function V(st) {
    if (whiteHits(st).length) return 1;
    if (!TAB) return 0;
    let t = 0; while (TRIX[symSq(t, st.q)] < 0) t++;
    const i = ((TRIX[symSq(t, st.q)] * 64 + symSq(t, st.b)) * 64 + symSq(t, st.n)) * 64 + symSq(t, st.r);
    const v = TAB[i >> 1]; return (i & 1) ? v >> 4 : v & 15;
}
function whiteMoves(st) {                      // [piesă, de la, la]
    const o = occOf(st), out = [];
    W3.forEach(p => {
        const ts = p === 'n' ? KN[st[p]] : slide(st[p], p === 'q' ? ORT.concat(DIA) : ORT, o);
        ts.forEach(t => { if (t !== st.q && t !== st.r && t !== st.n) out.push([p, st[p], t]); });
    });
    return out;
}
function bishopMoves(st) { return slide(st.b, DIA, occOf(st)).map(t => ['b', st.b, t]); }
function moved(st, m) { const s = Object.assign({}, st); s[m[0]] = m[2]; return s; }
const INF = 99, val = v => v === 0 ? INF : v;
/* valoarea unei mutări albe: câte mutări mai trebuie după ea (INF = nebunul scapă sau capturează) */
function whiteMoveValue(st, m) {
    const s = moved(st, m);
    if (m[2] === st.b) return 0;
    if (bishopHits(s).length) return INF + 1;
    let worst = 0;
    for (const bm of bishopMoves(s)) worst = Math.max(worst, val(V(moved(s, bm))));
    return worst;
}
/* robotul: alege mutarea pentru partea la mutare; rnd = Math.random */
function robotPick(st, side, randomness, rnd) {
    if (side === 'w') {
        const ms = whiteMoves(st), cap = ms.filter(m => m[2] === st.b);
        if (cap.length && rnd() >= randomness * 0.5) return cap[0];
        if (rnd() < randomness) {
            const safe = ms.filter(m => m[2] !== st.b && !bishopHits(moved(st, m)).length);
            return pickR(rnd() < 0.7 && safe.length ? safe : ms.filter(m => m[2] !== st.b), rnd);
        }
        let bv = 1e9, best = [];
        ms.forEach(m => {
            let v = whiteMoveValue(st, m);
            if (v >= INF) v = INF * 10 + (v > INF ? 1000 : 0) + bishopMoves(moved(st, m)).length;
            if (v < bv) { bv = v; best = [m]; } else if (v === bv) best.push(m);
        });
        return pickR(best, rnd);
    }
    const ms = bishopMoves(st), cap = ms.filter(m => W3.some(p => st[p] === m[2]));
    if (cap.length && rnd() >= randomness * 0.5) return cap[0];
    const quiet = ms.filter(m => !cap.includes(m));
    if (!quiet.length) return cap[0];
    if (rnd() < randomness) return pickR(quiet, rnd);
    let bv = -1, best = [];
    quiet.forEach(m => {
        const s = moved(st, m), v = val(V(s)) * 100 + bishopMoves(s).length;
        if (v > bv) { bv = v; best = [m]; } else if (v === bv) best.push(m);
    });
    return pickR(best, rnd);
}
function pickR(arr, rnd) { return arr[Math.floor(rnd() * arr.length)]; }
/*CORE-END*/

let board, mode = 'robot', randomness = 0.9, round, S, nMoves, turn, roundOver, matchOver, selSq = null, busy = false;
let results = {}, strikes = { 1: 0, 2: 0 }, tabFailed = false;
const pname = p => 'Jucătorul ' + p;
const whitePlayer = () => round === 1 ? 1 : 2;
const humanSide = () => round === 1 ? 'w' : 'b';
const isHumanTurn = () => mode === 'duo' || turn === humanSide();
const curPlayer = () => turn === 'w' ? whitePlayer() : 3 - whitePlayer();
const PN = { q: 'dama', r: 'turnul', n: 'calul', b: 'nebunul' };
const FEN = { q: 'wQ', r: 'wR', n: 'wN', b: 'bB' };

/* ---------- tabela ---------- */
(async function loadTab() {
    try {
        const res = await fetch('data/vanatoare_nebun.bin.gz');
        if (!res.ok) throw 0;
        const ds = res.body.pipeThrough(new DecompressionStream('gzip'));
        TAB = new Uint8Array(await new Response(ds).arrayBuffer());
        PERFECT = V(START) || PERFECT;
    } catch (e) { tabFailed = true; }
})();

/* ---------- afișare ---------- */
function buildPos() { const p = {}; ['q', 'r', 'n', 'b'].forEach(k => { if (S[k] !== null) p[name(S[k])] = FEN[k]; }); return p; }
const pieceAt = s => ['q', 'r', 'n', 'b'].find(k => S[k] === s) || null;
function targetsOf(s) {
    const p = pieceAt(s); if (!p) return [];
    if (turn === 'w' && p === 'b' || turn === 'b' && p !== 'b') return [];
    return (turn === 'w' ? whiteMoves(S) : bishopMoves(S)).filter(m => m[0] === p).map(m => m[2]);
}
function showSelection(sq) {
    clearHL(true); $('.square-' + sq).addClass('highlight-selected');
    targetsOf(idx(sq)).forEach(t => $('.square-' + name(t)).addClass(pieceAt(t) ? 'highlight-capture' : 'highlight-legal'));
}
function updateUI() {
    document.getElementById('roundVal').textContent = round + ' / 2';
    document.getElementById('movesVal').textContent = nMoves + ' / ' + LIMIT;
    [1, 2].forEach(p => {
        document.getElementById('pp' + p + '-strikes').textContent = '❌'.repeat(strikes[p]) + '▫️'.repeat(MAX_STRIKES - strikes[p]);
        document.getElementById('pp' + p + '-role').textContent = p === whitePlayer() ? '♕♖♘ albul' : '♝ nebunul';
        document.getElementById('pp' + p).className = 'player-panel' + (!roundOver && !matchOver && curPlayer() === p ? ' active' : '');
        const r = results[p];
        document.getElementById('pp' + p + '-result').textContent = r === undefined ? '' : r === null ? 'cu albul: nu a capturat nebunul' : 'cu albul: a capturat nebunul în ' + r + (r === 1 ? ' mutare' : ' mutări');
    });
}
function turnMsg() {
    if (mode === 'duo') return pname(curPlayer()) + (turn === 'w' ? ' mută o piesă albă.' : ' mută nebunul.');
    return turn === 'w' ? 'Mută o piesă albă. Nu o pune pe o diagonală a nebunului.' : 'Mută nebunul pe un pătrat unde nu poate fi capturat.';
}

/* ---------- desfășurarea ---------- */
function newMatch() { results = {}; strikes = { 1: 0, 2: 0 }; matchOver = false; startRound(1); }
function startRound(r) {
    round = r; S = Object.assign({}, START);
    nMoves = 0; turn = 'w'; roundOver = false; selSq = null; busy = false;
    board.position(buildPos(), false); clearHL();
    document.getElementById('btn-round2').style.display = 'none';
    setStatus(turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function apply(from, to) {
    const f = idx(from), t = idx(to), p = pieceAt(f), cap = pieceAt(t);
    if (cap) S[cap] = null;
    S[p] = t; if (turn === 'w') nMoves++;
    selSq = null; clearHL();
    board.position(buildPos(), false); markLast(from, to);
    play(cap ? sndCapture : sndMove);
    if (cap === 'b') return endRound('w', cap1(PN[p]) + ' a capturat nebunul pe ' + to + (nMoves === 1 ? ', din prima mutare.' : ', la mutarea ' + nMoves + '.'));
    if (cap) return endRound('b', 'Nebunul a capturat ' + PN[cap] + ' pe ' + to + '.');
    if (turn === 'w' && nMoves >= LIMIT) return endRound('b', 'Nebunul a rezistat ' + LIMIT + ' mutări ale albului.');
    turn = turn === 'w' ? 'b' : 'w';
    setStatus(turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function endRound(winner, why) {
    roundOver = true; setTimeout(() => play(sndMate), 250);
    results[whitePlayer()] = winner === 'w' ? nMoves : null;
    let msg;
    if (mode === 'robot') {
        const youWin = winner === humanSide();
        msg = (youWin ? '🏆 Ai câștigat! ' : '🤖 Robotul a câștigat. ') + why;
        if (round === 1 && youWin && nMoves > PERFECT) msg += '<br>Se poate și mai repede: oricum ar juca negrul, albul poate captura nebunul în cel mult ' + PERFECT + ' mutări.';
        if (round === 1 && !youWin) msg += '<br>Încearcă din nou: înainte de fiecare mutare uită-te pe diagonalele nebunului. Nicio piesă albă nu are voie să stea pe ele.';
    } else {
        msg = '🏁 ' + why + ' ' + (winner === 'w' ? 'Câștigă albul (' + pname(whitePlayer()) + ').' : 'Câștigă nebunul (' + pname(3 - whitePlayer()) + ').');
    }
    if (round === 1) document.getElementById('btn-round2').style.display = 'block';
    else { matchOver = true; if (mode === 'duo') msg += '<br><br>' + matchSummary(); }
    setStatus(msg, (mode === 'robot' ? winner === humanSide() : true) ? 'ok' : 'warn');
    updateUI();
}
function matchSummary() {
    const a = results[1], b = results[2];
    let w = 0;
    if (a !== null && b !== null) w = a < b ? 1 : b < a ? 2 : 0;
    else if (a !== null || b !== null) w = a !== null ? 1 : 2;
    if (!w) return '🤝 <strong>Egalitate.</strong>';
    document.getElementById('pp' + w).className = 'player-panel winner';
    return '🏆 <strong>' + pname(w) + ' câștigă meciul</strong>: a capturat nebunul mai repede.';
}

/* ---------- Robotul ---------- */
function robotMove() {
    busy = true;
    if (!TAB && !tabFailed && randomness < 0.5) { setStatus('🤖 Robotul se pregătește...'); setTimeout(robotMove, 300); return; }
    setTimeout(() => {
        busy = false; if (roundOver) return;
        const m = robotPick(S, turn, randomness, Math.random);
        apply(name(m[1]), name(m[2]));
    }, 600);
}

/* ---------- om ---------- */
function illegal(sq, reason) {
    if (sq) flashWrong(sq);
    selSq = null; clearHL(true);
    if (mode !== 'duo') { setStatus('⚠️ ' + reason, 'warn'); return; }
    const p = curPlayer(); strikes[p]++; updateUI();
    if (strikes[p] >= MAX_STRIKES) {
        roundOver = true; matchOver = true;
        const o = 3 - p;
        document.getElementById('btn-round2').style.display = 'none';
        document.getElementById('pp' + o).className = 'player-panel winner';
        setStatus('❌ ' + reason + '<br>' + pname(p) + ' a încercat 3 mutări nepermise.<br>🏆 <strong>' + pname(o) + ' câștigă meciul.</strong>', 'warn');
        return;
    }
    setStatus('❌ ' + reason + ' Încercări nepermise pentru ' + pname(p) + ': ' + strikes[p] + ' din ' + MAX_STRIKES + '.', 'warn');
}
function checkMove(from, to) {
    const f = idx(from), t = idx(to), p = pieceAt(f);
    if (targetsOf(f).includes(t)) return null;
    const own = pieceAt(t);
    if (own && (own === 'b') === (p === 'b')) return 'Nu poți captura o piesă de aceeași culoare.';
    return p === 'q' ? 'Dama merge pe linii, pe coloane și pe diagonale și nu sare peste piese.'
         : p === 'r' ? 'Turnul merge numai în linie dreaptă și nu sare peste piese.'
         : p === 'n' ? 'Calul sare numai în formă de „L”.'
         : 'Nebunul merge numai pe diagonală și nu sare peste piese.';
}
function cap1(s) { return s[0].toUpperCase() + s.slice(1); }
function tryMove(from, to) { const why = checkMove(from, to); if (why) return illegal(to, why); apply(from, to); }
function ownPiece(s) { const p = pieceAt(s); return !!p && (turn === 'w' ? p !== 'b' : p === 'b'); }

/* ---------- setări ---------- */
function setMode(m) {
    mode = m;
    document.getElementById('modeRobot').className = 'tgl-btn' + (m === 'robot' ? ' active' : '');
    document.getElementById('modeDuo').className   = 'tgl-btn' + (m === 'duo' ? ' active' : '');
    document.getElementById('levelGrid').style.display = m === 'robot' ? '' : 'none';
    document.getElementById('duoPanels').style.display = m === 'duo' ? '' : 'none';
    newMatch();
}
function setLevel(btn) {
    document.querySelectorAll('.animal-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active'); randomness = parseFloat(btn.dataset.random);
    if (typeof minigameHideHints === 'function') minigameHideHints(randomness === 0);
    newMatch();
}

/* ---------- input: click și drag ---------- */
function canAct() { return !roundOver && !matchOver && !busy && isHumanTurn(); }
board = Chessboard('board', {
    position: 'empty', pieceTheme: 'https://lichess1.org/assets/piece/caliente/{piece}.svg',
    draggable: true, showNotation: true,
    onDragStart: function (source) {
        if (!canAct()) return false;
        const s = idx(source);
        if (selSq && source !== selSq && !ownPiece(s)) { const from = selSq; setTimeout(() => tryMove(from, source), 0); return false; }
        if (!ownPiece(s)) { illegal(source, turn === 'w' ? 'Acum mută albul.' : 'Acum mută nebunul.'); return false; }
        selSq = source; showSelection(source);
    },
    onDrop: function (source, target) {
        if (target === 'offboard' || target === source) return 'snapback';
        selSq = null;
        const why = checkMove(source, target);
        if (why) { illegal(target, why); return 'snapback'; }
        apply(source, target);
    },
    onSnapEnd: function () { board.position(buildPos(), false); }
});
$(document).on('click', '#board [class*="square-"]', function () {
    if (!canAct() || !selSq) return;
    const m = (this.className || '').match(/square-([a-h][1-8])/); if (!m) return;
    const sq = m[1];
    if (sq === selSq || ownPiece(idx(sq))) return;
    tryMove(selSq, sq);
});
$(window).resize(() => board.resize());
newMatch();
