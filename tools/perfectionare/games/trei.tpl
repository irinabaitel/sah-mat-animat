===FILE===
nivel1_joc_cal_trei_piese.html
===TITLE===
Calul contra trei piese — Joc
===HEADER===
♘ Calul contra trei piese
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
          <div class="counter-box"><div class="counter-lbl">Mutările calului</div><div class="counter-val" id="movesVal">0 / 8</div></div>
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
            <p>Albul are un <strong>cal</strong>, pe b1. Negrul are trei piese: un <strong>turn</strong> pe a8, un <strong>cal</strong> pe b8 și un <strong>nebun</strong> pe c8. Mută întâi calul alb, apoi negrul, pe rând.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea calul alb</h4>
            <p>Calul alb trebuie să <strong>reziste 8 mutări</strong> fără să fie capturat. După a opta lui mutare, a câștigat.</p>
            <p>Calul alb nu are voie să sară pe un pătrat unde ar putea fi capturat. Dacă o piesă neagră rămâne neapărată în calea lui, o poate captura.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea negrul</h4>
            <p>Negrul încearcă să <strong>captureze calul alb</strong> înainte de a opta lui mutare. Negrul câștigă și dacă calul alb nu mai are niciun pătrat sigur.</p>
          </div>
          <div class="hl-box warn">
            <h4>Ce e greu</h4>
            <p>Trei piese care lucrează împreună închid repede calea calului. Calul trebuie să se uite la fiecare mutare care pătrate sunt atacate și să nu intre într-un colț.</p>
          </div>
          <div class="hl-box">
            <h4>Reprizele</h4>
            <p>În repriza 1 tu ești calul alb, iar în repriza 2 ești negrul. <strong>În doi</strong>, Jucătorul 1 e calul în repriza 1 și negrul în repriza 2. Câștigă meciul cine, cu negrul, a prins calul mai repede.</p>
          </div>
          <p class="pp-role" style="margin-top:8px">Jocul vine din programul Chess Tutor Step 1 (metoda Steps), lecția 5.</p>
        </details>
===SCRIPT===
/* =====================================================
   CALUL CONTRA TREI PIESE (Chess Tutor Step 1, lecția 5, joc 5d)
   Cal alb b1 contra Ta8, Cb8, Nc8. Calul trebuie să reziste 8 mutări.
   Robotul caută înainte (cu memorare) cel mult 6 mutări ale calului.
   ===================================================== */
/*COMMON*/
const LIMIT = 8, HOR = 6, X = 64;            // X = piesă capturată
let board, mode = 'robot', randomness = 0.9, round, S, nMoves, turn, roundOver, matchOver, selSq = null, busy = false;
let results = {}, strikes = { 1: 0, 2: 0 };
/* S = { k, r, n, b } (pătrate 0..63, 64 = capturată) */
const pname = p => 'Jucătorul ' + p;
const knightPlayer = () => round === 1 ? 1 : 2;
const humanSide = () => round === 1 ? 'w' : 'b';
const isHumanTurn = () => mode === 'duo' || turn === humanSide();
const curPlayer = () => turn === 'w' ? knightPlayer() : 3 - knightPlayer();
const PN = { r: 'turnul', n: 'calul negru', b: 'nebunul' };

/* ---------- geometrie ---------- */
function attackers(k, r, n, b, t) {         // ce piesă neagră atacă t (calul alb pe t, pe k nu mai e nimic)
    const occ = s => s === r || s === n || s === b || s === t;
    if (r !== X && slide(r, ORT, occ).includes(t)) return 'r';
    if (n !== X && KN[n].includes(t)) return 'n';
    if (b !== X && slide(b, DIA, occ).includes(t)) return 'b';
    return null;
}
function knightOpts(k, r, n, b) {           // mutările sigure ale calului alb: [t, r2, n2, b2]
    const out = [];
    for (const t of KN[k]) {
        const r2 = r === t ? X : r, n2 = n === t ? X : n, b2 = b === t ? X : b;
        if (!attackers(t, r2, n2, b2, t)) out.push([t, r2, n2, b2]);
    }
    return out;
}
function blackMoves(k, r, n, b) {            // [piesă, de la, la]
    const occ = s => s === r || s === n || s === b || s === k;
    const mine = s => s === r || s === n || s === b;
    const out = [];
    if (r !== X) slide(r, ORT, occ).forEach(t => { if (!mine(t)) out.push(['r', r, t]); });
    if (n !== X) KN[n].forEach(t => { if (!mine(t)) out.push(['n', n, t]); });
    if (b !== X) slide(b, DIA, occ).forEach(t => { if (!mine(t)) out.push(['b', b, t]); });
    return out;
}
function moved(st, m) { const s = Object.assign({}, st); s[m[0]] = m[2]; return s; }

/* ---------- căutare ---------- */
const memo = new Map();
const key = (k, r, n, b, left, side) => ((((k * 65 + r) * 65 + n) * 65 + b) * 9 + left) * 2 + side;
function blackWins(k, r, n, b, left) {       // negrul la mutare; calul mai are de făcut `left` mutări
    if (left <= 0) return false;
    if (attackers(k, r, n, b, k)) return true;
    const K = key(k, r, n, b, left, 1); if (memo.has(K)) return memo.get(K);
    let res = false;
    for (const m of blackMoves(k, r, n, b)) {
        const s = { r, n, b }; s[m[0]] = m[2];
        if (knightLoses(k, s.r, s.n, s.b, left)) { res = true; break; }
    }
    memo.set(K, res); return res;
}
function knightLoses(k, r, n, b, left) {     // calul la mutare
    if (left <= 0) return false;
    const K = key(k, r, n, b, left, 0); if (memo.has(K)) return memo.get(K);
    const opts = knightOpts(k, r, n, b);
    let res = true;
    for (const [t, r2, n2, b2] of opts) {
        if (left === 1 || !blackWins(t, r2, n2, b2, left - 1)) { res = false; break; }
    }
    memo.set(K, res); return res;
}

/* ---------- afișare ---------- */
function buildPos() {
    const p = {}; if (S.k !== X) p[name(S.k)] = 'wN';
    if (S.r !== X) p[name(S.r)] = 'bR'; if (S.n !== X) p[name(S.n)] = 'bN'; if (S.b !== X) p[name(S.b)] = 'bB';
    return p;
}
const blackAt = s => s === S.r ? 'r' : s === S.n ? 'n' : s === S.b ? 'b' : null;
function targetsOf(s) {
    if (turn === 'w') return s === S.k ? KN[s].slice() : [];
    const p = blackAt(s); if (!p) return [];
    return blackMoves(S.k, S.r, S.n, S.b).filter(m => m[0] === p).map(m => m[2]);
}
function showSelection(sq) {
    clearHL(true); $('.square-' + sq).addClass('highlight-selected');
    targetsOf(idx(sq)).forEach(t => $('.square-' + name(t)).addClass((t === S.k || blackAt(t)) ? 'highlight-capture' : 'highlight-legal'));
}
function updateUI() {
    document.getElementById('roundVal').textContent = round + ' / 2';
    document.getElementById('movesVal').textContent = nMoves + ' / ' + LIMIT;
    [1, 2].forEach(p => {
        document.getElementById('pp' + p + '-strikes').textContent = '❌'.repeat(strikes[p]) + '▫️'.repeat(MAX_STRIKES - strikes[p]);
        document.getElementById('pp' + p + '-role').textContent = p === knightPlayer() ? '♘ calul alb' : '♜♞♝ negrul';
        document.getElementById('pp' + p).className = 'player-panel' + (!roundOver && !matchOver && curPlayer() === p ? ' active' : '');
        const r = results[p];
        document.getElementById('pp' + p + '-result').textContent = r === undefined ? '' : r === null ? 'cu negrul: nu a prins calul' : 'cu negrul: a prins calul după ' + r + ' mutări ale lui';
    });
}
function turnMsg() {
    if (mode === 'duo') return pname(curPlayer()) + (turn === 'w' ? ' mută calul alb.' : ' mută o piesă neagră.');
    return turn === 'w' ? 'Mută calul alb pe un pătrat sigur.' : 'Mută o piesă neagră. Încearcă să prinzi calul.';
}

/* ---------- desfășurarea ---------- */
function newMatch() { results = {}; strikes = { 1: 0, 2: 0 }; matchOver = false; startRound(1); }
function startRound(r) {
    memo.clear(); round = r; S = { k: idx('b1'), r: idx('a8'), n: idx('b8'), b: idx('c8') };
    nMoves = 0; turn = 'w'; roundOver = false; selSq = null; busy = false;
    board.position(buildPos(), false); clearHL();
    document.getElementById('btn-round2').style.display = 'none';
    setStatus(turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function apply(from, to) {
    const f = idx(from), t = idx(to);
    let cap = null;
    if (turn === 'w') {
        cap = blackAt(t); if (cap) S[cap] = X;
        S.k = t; nMoves++;
    } else {
        if (t === S.k) { cap = 'k'; S.k = X; }
        S[blackAt(f)] = t;
    }
    selSq = null; clearHL();
    board.position(buildPos(), false); markLast(from, to);
    play(cap ? sndCapture : sndMove);
    if (cap === 'k') return endRound('b', 'Negrul a capturat calul pe ' + to + '.');
    if (turn === 'w' && nMoves >= LIMIT) return endRound('w', 'Calul a rezistat ' + LIMIT + ' mutări.');
    turn = turn === 'w' ? 'b' : 'w';
    if (turn === 'w' && !knightOpts(S.k, S.r, S.n, S.b).length) { updateUI(); return endRound('b', 'Calul alb nu mai are niciun pătrat sigur.'); }
    setStatus((cap ? 'Calul alb a capturat ' + PN[cap] + '. ' : '') + turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function endRound(winner, why) {
    roundOver = true; setTimeout(() => play(sndMate), 250);
    const bPlayer = 3 - knightPlayer();
    results[bPlayer] = winner === 'b' ? nMoves : null;
    let msg;
    if (mode === 'robot') {
        const youWin = winner === humanSide();
        msg = (youWin ? '🏆 Ai câștigat! ' : '🤖 Robotul a câștigat. ') + why;
        if (round === 1 && !youWin) msg += '<br>Încearcă din nou: caută pătratele de unde calul are mai multe ieșiri și ferește-te de colțuri.';
    } else {
        msg = '🏁 ' + why + ' ' + (winner === 'w' ? 'Câștigă calul (' + pname(knightPlayer()) + ').' : 'Câștigă negrul (' + pname(bPlayer) + ').');
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
        const { k, r, n, b } = S, left = LIMIT - nMoves;
        let from, to;
        if (turn === 'w') {
            const opts = knightOpts(k, r, n, b);
            let pick;
            if (Math.random() < randomness) pick = pickRandom(opts);
            else if (nMoves === 0) pick = opts.find(o => o[0] === idx(pickRandom(['c3', 'd2'])));
            else {
                const good = opts.filter(o => left === 1 || !blackWins(o[0], o[1], o[2], o[3], Math.min(left - 1, HOR)));
                const pool = good.length ? good : opts;
                pool.sort((x, y) => knightOpts(y[0], y[1], y[2], y[3]).length - knightOpts(x[0], x[1], x[2], x[3]).length);
                pick = pool[0];
            }
            from = k; to = pick[0];
        } else {
            const ms = blackMoves(k, r, n, b);
            const capK = ms.find(m => m[2] === k);
            let pick;
            if (capK && Math.random() >= randomness * 0.5) pick = capK;
            else if (Math.random() < randomness) pick = pickRandom(ms.filter(m => m[2] !== k));
            else {
                const h = Math.min(left, HOR);
                const win = ms.filter(m => m[2] !== k && (() => { const s = moved(S, m); return knightLoses(s.k, s.r, s.n, s.b, h); })());
                if (win.length) pick = pickRandom(win);
                else {                      // fără câștig sigur: lasă calului cât mai puține pătrate sigure, fără să lase piese neapărate
                    let bv = 1e9, best = [];
                    ms.filter(m => m[2] !== k).forEach(m => {
                        const s = moved(S, m), o = knightOpts(s.k, s.r, s.n, s.b);
                        const v = o.length * 10 + o.filter(x => x[1] !== s.r || x[2] !== s.n || x[3] !== s.b).length * 30;
                        if (v < bv) { bv = v; best = [m]; } else if (v === bv) best.push(m);
                    });
                    pick = pickRandom(best);
                }
            }
            from = pick[1]; to = pick[2];
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
function checkMove(from, to) {
    const f = idx(from), t = idx(to);
    if (!targetsOf(f).includes(t)) {
        if (turn === 'w') return 'Calul sare numai în formă de „L”.';
        const p = blackAt(f);
        return p === 'r' ? 'Turnul merge numai în linie dreaptă și nu sare peste piese.' : p === 'b' ? 'Nebunul merge numai pe diagonală și nu sare peste piese.' : 'Calul sare numai în formă de „L” și nu capturează piesele lui.';
    }
    if (turn === 'w') {
        const c = blackAt(t), r2 = c === 'r' ? X : S.r, n2 = c === 'n' ? X : S.n, b2 = c === 'b' ? X : S.b;
        const a = attackers(t, r2, n2, b2, t);
        if (a) {
            const where = { r: r2, n: n2, b: b2 }[a];
            return c ? cap1(PN[c]) + ' de pe ' + to + ' e apărat de ' + PN[a] + ' de pe ' + name(where) + '.'
                     : 'Pe ' + to + ' calul ar fi capturat de ' + PN[a] + ' de pe ' + name(where) + '.';
        }
    }
    return null;
}
function cap1(s) { return s[0].toUpperCase() + s.slice(1); }
function tryMove(from, to) { const why = checkMove(from, to); if (why) return illegal(to, why); apply(from, to); }
function ownPiece(s) { return turn === 'w' ? s === S.k : !!blackAt(s); }

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
        if (!ownPiece(s)) { illegal(source, turn === 'w' ? 'Acum mută calul alb.' : 'Acum mută o piesă neagră.'); return false; }
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
    if (sq === selSq || S.k === idx(sq) || blackAt(idx(sq))) return;
    tryMove(selSq, sq);
});
$(window).resize(() => board.resize());
newMatch();
