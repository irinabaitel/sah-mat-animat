===FILE===
nivel1_joc_scapa_de_dame.html
===TITLE===
Scapă de dame — Joc
===HEADER===
♘ Scapă de dame
===PANEL===
        <div class="toggle-row">
          <button class="tgl-btn active" id="modeRobot" onclick="setMode('robot')">🤖 Contra Robotului</button>
          <button class="tgl-btn"        id="modeDuo"   onclick="setMode('duo')">👫 În doi</button>
        </div>
        <div class="toggle-row">
          <button class="tgl-btn active" id="pos1" onclick="setPos(1)">Poziția 1</button>
          <button class="tgl-btn"        id="pos2" onclick="setPos(2)">Poziția 2</button>
        </div>
        <div class="animal-grid" id="levelGrid">
          <button class="animal-btn active" data-random="0.9" onclick="setLevel(this)">🐣<span>Pui de găină</span></button>
          <button class="animal-btn" data-random="0.2" onclick="setLevel(this)">🐴<span>Mânz</span></button>
          <button class="animal-btn" data-random="0" onclick="setLevel(this)">🐉<span>Dragon</span></button>
        </div>

        <div class="counter-row">
          <div class="counter-box"><div class="counter-lbl">Repriza</div><div class="counter-val" id="roundVal">1 / 2</div></div>
          <div class="counter-box"><div class="counter-lbl">Mutările calului</div><div class="counter-val" id="movesVal">0 / 10</div></div>
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
            <p id="posTxt">Albul are un <strong>cal</strong>, pe f6. Negrul are două <strong>regine</strong>, pe c4 și pe g6.</p><p>Mută întâi calul, apoi reginele, pe rând: o mutare calul, o mutare una dintre regine.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea calul</h4>
            <p>Calul fuge mereu pe un pătrat unde reginele nu-l pot captura. Dacă o regină ajunge pe un pătrat atacat de cal și nu e apărată de cealaltă regină, calul o <strong>capturează</strong> și câștigă.</p>
            <p>Calul câștigă și dacă rezistă <strong>10 mutări</strong> fără să fie capturat.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vor reginele</h4>
            <p>Reginele încearcă să <strong>captureze calul</strong>. Ele trebuie să-l prindă, dar fără să se pună singure în calea calului.</p>
          </div>
          <div class="hl-box warn">
            <h4>Ce e greu</h4>
            <p>Reginele sunt foarte puternice. Cu mutări foarte bune, ele prind calul repede. Calul trebuie să caute pătratele unde nu poate fi atacat și să pândească greșeala unei regine.</p>
          </div>
          <div class="hl-box">
            <h4>Reprizele</h4>
            <p>În repriza 1 tu ești calul, iar în repriza 2 ești reginele. <strong>În doi</strong>, Jucătorul 1 e calul în repriza 1 și reginele în repriza 2.</p>
          </div>
          <p class="pp-role" style="margin-top:8px">Jocul vine din programul Chess Tutor Step 1 (metoda Steps): poziția 1 din lecția 5, poziția 2 din lecția 6.</p>
        </details>
===SCRIPT===
/* =====================================================
   SCAPĂ DE DAME (Chess Tutor Step 1, lecția 5, joc 5c)
   Cal alb contra două regine negre. Calul câștigă dacă capturează o regină
   sau rezistă 10 mutări; reginele câștigă dacă îl capturează.
   Robotul joacă din tabela calculată retrograd (fără limită de mutări).
   ===================================================== */
/*COMMON*/
const LIMIT = 10;
const QD = ORT.concat(DIA);
/* ---------- tabela retrogradă: stare = (n, a, b), a<b; VQ = reginele la mutare, VN = calul la mutare
   valoare = număr de semimutări până la capturarea calului (cu joc perfect); Infinity = calul scapă ---------- */
const KEY = (n, a, b) => a < b ? n * 4096 + a * 64 + b : n * 4096 + b * 64 + a;
const INF = 1e9;
let VN, VQ;
function qAtt(q, other, t) {            // regina de pe q atacă t? (cealaltă regină poate bloca; calul nu blochează atacul spre el)
    return slide(q, QD, s => s === other).includes(t);
}
function queenMoves(q, other) { return slide(q, QD, s => s === other).filter(s => s !== other); }
function buildTable() {
    VN = new Float64Array(262144).fill(INF); VQ = new Float64Array(262144).fill(INF);
    for (let n = 0; n < 64; n++) for (let a = 0; a < 64; a++) for (let b = a + 1; b < 64; b++) {
        if (a === n || b === n) continue;
        if (qAtt(a, b, n) || qAtt(b, a, n)) VQ[KEY(n, a, b)] = 1;    // reginele capturează imediat
    }
    let changed = true;
    while (changed) {
        changed = false;
        for (let n = 0; n < 64; n++) for (let a = 0; a < 64; a++) for (let b = a + 1; b < 64; b++) {
            if (a === n || b === n) continue;
            const k = KEY(n, a, b);
            if (VN[k] >= INF) {               // calul la mutare: maximizează; dacă poate captura o regină neapărată = calul câștigă (INF)
                let worst = 0, escape = false;
                for (const t of KN[n]) {
                    if (t === a || t === b) {
                        const other = t === a ? b : a;
                        if (!qAtt(other, -1, t)) { escape = true; break; }
                        continue;               // regina apărată: capturarea pierde calul (nepermis în joc)
                    }
                    const v = VQ[KEY(t, a, b)];
                    if (v >= INF) { escape = true; break; }
                    if (v > worst) worst = v;
                }
                if (!escape && worst > 0) { VN[k] = worst + 1; changed = true; }
            }
            if (VQ[k] >= INF) {               // reginele la mutare: minimizează
                let best = INF;
                for (const [q, o] of [[a, b], [b, a]]) for (const t of queenMoves(q, o)) {
                    if (t === n) continue;
                    const v = VN[KEY(n, t, o)];
                    if (v < best) best = v;
                }
                if (best < INF) { VQ[k] = best + 1; changed = true; }
            }
        }
    }
}

/* ---------- stare ---------- */
const POS = { 1: ['f6', 'c4', 'g6'], 2: ['e4', 'c2', 'd8'] };
let posN = new URLSearchParams(location.search).get('p') === '2' ? 2 : 1;
let board, mode = 'robot', randomness = 0.9, round, N, QA, QB, nMoves, turn, roundOver, matchOver, selSq = null, busy = false;
let results = {}, strikes = { 1: 0, 2: 0 };
const pname = p => 'Jucătorul ' + p;
const knightPlayer = () => round === 1 ? 1 : 2;          // în doi: J1 = cal în repriza 1
const humanSide = () => round === 1 ? 'n' : 'q';         // contra Robotului: tu = calul în repriza 1
const isHumanTurn = () => mode === 'duo' || turn === humanSide();
const curPlayer = () => turn === 'n' ? knightPlayer() : 3 - knightPlayer();

function buildPos() { const p = {}; if (N >= 0) p[name(N)] = 'wN'; if (QA >= 0) p[name(QA)] = 'bQ'; if (QB >= 0) p[name(QB)] = 'bQ'; return p; }
function targetsOf(s) {
    if (turn === 'n') return s === N ? KN[N].slice() : [];
    if (s === QA) return slide(QA, QD, t => t === QB || t === N).filter(t => t !== QB);
    if (s === QB) return slide(QB, QD, t => t === QA || t === N).filter(t => t !== QA);
    return [];
}
function knightProblem(t) {                 // null = mutare permisă pentru cal
    if (t === QA || t === QB) {
        const other = t === QA ? QB : QA;
        return qAtt(other, -1, t) ? 'Regina de pe ' + name(t) + ' e apărată de cealaltă regină. Calul ar fi capturat.' : null;
    }
    for (const q of [QA, QB]) { const o = q === QA ? QB : QA; if (qAtt(q, o, t)) return 'Pe ' + name(t) + ' calul ar fi capturat de regina de pe ' + name(q) + '.'; }
    return null;
}
function knightSafe() { return KN[N].filter(t => knightProblem(t) === null); }

function showSelection(sq) {
    clearHL(true); $('.square-' + sq).addClass('highlight-selected');
    targetsOf(idx(sq)).forEach(t => $('.square-' + name(t)).addClass((t === N || t === QA || t === QB) ? 'highlight-capture' : 'highlight-legal'));
}
function updateUI() {
    document.getElementById('roundVal').textContent = round + ' / 2';
    document.getElementById('movesVal').textContent = nMoves + ' / ' + LIMIT;
    [1, 2].forEach(p => {
        document.getElementById('pp' + p + '-strikes').textContent = '❌'.repeat(strikes[p]) + '▫️'.repeat(MAX_STRIKES - strikes[p]);
        document.getElementById('pp' + p + '-role').textContent = (p === knightPlayer() ? '♘ calul' : '♛ reginele');
        document.getElementById('pp' + p).className = 'player-panel' + (!roundOver && !matchOver && curPlayer() === p ? ' active' : '');
        const r = results[p];
        document.getElementById('pp' + p + '-result').textContent = r === undefined ? '' : r === null ? 'ca regine: nu a prins calul' : 'ca regine: a prins calul în ' + r + ' mutări ale calului';
    });
}
function turnMsg() {
    if (mode === 'duo') return pname(curPlayer()) + (turn === 'n' ? ' mută calul.' : ' mută o regină.');
    return turn === 'n' ? 'Mută calul pe un pătrat sigur.' : 'Mută o regină. Încearcă să prinzi calul.';
}

/* ---------- desfășurarea ---------- */
function newMatch() { results = {}; strikes = { 1: 0, 2: 0 }; matchOver = false; startRound(1); }
function startRound(r) {
    round = r; N = idx(POS[posN][0]); QA = idx(POS[posN][1]); QB = idx(POS[posN][2]); nMoves = 0; turn = 'n'; roundOver = false; selSq = null; busy = false;
    board.position(buildPos(), false); clearHL();
    document.getElementById('btn-round2').style.display = 'none';
    setStatus(turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function apply(from, to) {
    const f = idx(from), t = idx(to);
    let cap = false;
    if (turn === 'n') {
        if (t === QA) { QA = -1; cap = true; } else if (t === QB) { QB = -1; cap = true; }
        N = t; nMoves++;
    } else {
        if (t === N) { N = -1; cap = true; }
        if (f === QA) QA = t; else QB = t;
    }
    selSq = null; clearHL();
    board.position(buildPos(), false); markLast(from, to);
    play(cap ? sndCapture : sndMove);
    if (turn === 'n' && cap) return endRound('n', 'Calul a capturat regina de pe ' + to + '.');
    if (turn === 'q' && cap) return endRound('q', 'Regina a capturat calul pe ' + to + '.');
    if (turn === 'n' && nMoves >= LIMIT) return endRound('n', 'Calul a rezistat ' + LIMIT + ' mutări.');
    turn = turn === 'n' ? 'q' : 'n';
    if (turn === 'n' && !knightSafe().length) {
        updateUI();
        return endRound('q', 'Calul nu mai are niciun pătrat sigur.', true);
    }
    setStatus(turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function endRound(winner, why, trapped) {
    roundOver = true; setTimeout(() => play(sndMate), 250);
    if (winner === 'q' && trapped) { /* calul prins fără ieșire */ }
    const qPlayer = 3 - knightPlayer();
    results[qPlayer] = winner === 'q' ? nMoves : null;
    let msg;
    if (mode === 'robot') {
        const youWin = winner === humanSide();
        msg = (youWin ? '🏆 Ai câștigat! ' : '🤖 Robotul a câștigat. ') + why;
        if (round === 1 && !youWin && winner === 'q') msg += '<br>Reginele sunt foarte puternice: cu mutări bune, ele închid calul repede. Încearcă din nou și pândește o regină neapărată.';
    } else {
        msg = '🏁 ' + why + ' ' + (winner === 'n' ? 'Câștigă calul (' + pname(knightPlayer()) + ').' : 'Câștigă reginele (' + pname(qPlayer) + ').');
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
    return '🏆 <strong>' + pname(w) + ' câștigă meciul</strong>: a prins calul mai repede.';
}

/* ---------- Robotul ---------- */
function robotMove() {
    busy = true;
    setTimeout(() => {
        busy = false; if (roundOver) return;
        let from, to;
        if (turn === 'n') {
            const ok = knightSafe();
            const caps = ok.filter(t => t === QA || t === QB);
            let t;
            if (caps.length && Math.random() >= randomness * 0.5) t = caps[0];
            else if (Math.random() < randomness) t = pickRandom(ok);
            else { let bv = -1; ok.forEach(m => { const v = (m === QA || m === QB) ? INF * 2 : VQ[KEY(m, QA, QB)]; if (v > bv) { bv = v; t = m; } }); }
            from = N; to = t;
        } else {
            const opts = [];
            for (const [q, o] of [[QA, QB], [QB, QA]]) for (const t of slide(q, QD, s => s === o || s === N).filter(s => s !== o)) {
                if (t === N) { opts.push([q, t, -1]); continue; }
                const hang = KN[N].includes(t) && !qAtt(o, -1, t);
                opts.push([q, t, hang ? INF * 2 : VN[KEY(N, t, o)]]);
            }
            const win = opts.find(o => o[2] === -1);
            let pick;
            if (win && Math.random() >= randomness * 0.5) pick = win;
            else if (Math.random() < randomness) pick = pickRandom(opts);
            else { opts.sort((x, y) => x[2] - y[2]); const bv = opts[0][2]; pick = pickRandom(opts.filter(o => o[2] === bv)); }
            from = pick[0]; to = pick[1];
        }
        apply(name(from), name(to));
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
function checkMove(from, to) {               // null = bine
    const f = idx(from), t = idx(to);
    if (!targetsOf(f).includes(t)) return turn === 'n' ? 'Calul sare numai în formă de „L”.' : 'Regina merge în linie dreaptă sau pe diagonală și nu sare peste piese.';
    if (turn === 'n') return knightProblem(t);
    return null;
}
function tryMove(from, to) { const why = checkMove(from, to); if (why) return illegal(to, why); apply(from, to); }
function ownPiece(s) { return turn === 'n' ? s === N : (s === QA || s === QB); }

/* ---------- setări ---------- */
function setMode(m) {
    mode = m;
    document.getElementById('modeRobot').className = 'tgl-btn' + (m === 'robot' ? ' active' : '');
    document.getElementById('modeDuo').className   = 'tgl-btn' + (m === 'duo' ? ' active' : '');
    document.getElementById('levelGrid').style.display = m === 'robot' ? '' : 'none';
    document.getElementById('duoPanels').style.display = m === 'duo' ? '' : 'none';
    newMatch();
}
function setPos(n) {
    posN = n;
    [1, 2].forEach(k => document.getElementById('pos' + k).className = 'tgl-btn' + (k === n ? ' active' : ''));
    const p = POS[n];
    document.getElementById('posTxt').innerHTML = 'Albul are un <strong>cal</strong>, pe ' + p[0] + '. Negrul are două <strong>regine</strong>, pe ' + p[1] + ' și pe ' + p[2] + '.';
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
        if (!ownPiece(s)) { illegal(source, turn === 'n' ? 'Acum mută calul alb.' : 'Acum mută una dintre reginele negre.'); return false; }
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
    if (sq === selSq || [N, QA, QB].includes(idx(sq))) return;
    tryMove(selSq, sq);
});
$(window).resize(() => board.resize());
setStatus('Se pregătește Robotul…');
setTimeout(() => { buildTable(); setPos(posN); }, 30);
