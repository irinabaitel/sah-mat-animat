===FILE===
nivel1_joc_doi_nebuni.html
===TITLE===
Doi nebuni contra damei — Joc
===HEADER===
♗♗ Doi nebuni contra damei
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
          <div class="counter-box"><div class="counter-lbl">Mutările nebunilor</div><div class="counter-val" id="movesVal">0 / 5</div></div>
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
            <p>Albul are doi <strong>nebuni</strong>, pe c5 și pe e4. Negrul are o <strong>damă</strong>, pe a1. Pe tablă nu sunt regi. Mută întâi albul, apoi negrul, pe rând.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea albul</h4>
            <p>Nebunii trebuie să <strong>reziste 5 mutări</strong> fără să piardă niciun nebun. Dacă nebunii fac 5 mutări și dama nu capturează niciun nebun, albul a câștigat.</p>
            <p>Albul câștigă și dacă un nebun capturează dama.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea negrul</h4>
            <p>Dama încearcă să <strong>captureze un nebun</strong>. Negrul câștigă și dacă vine rândul albului și, orice ar muta, un nebun rămâne atacat de damă.</p>
          </div>
          <div class="hl-box">
            <h4>Ce nu este voie</h4>
            <p>Dama nu are voie să meargă pe un pătrat atacat de un nebun.</p>
            <p>Nebunii pot merge pe orice pătrat de pe diagonală. Dar dacă un nebun ajunge pe un pătrat atacat de damă, dama îl poate captura.</p>
          </div>
          <div class="hl-box warn">
            <h4>Ce e greu</h4>
            <p>Un nebun stă pe pătrate albe, celălalt pe pătrate negre, așa că nu se pot apăra unul pe altul. Dama poate ataca amândoi nebunii dintr-o singură mutare. Înainte să muți, uită-te pe ce pătrate poate ajunge dama.</p>
          </div>
          <div class="hl-box">
            <h4>Reprizele</h4>
            <p>În repriza 1 tu ești albul, cu nebunii, iar în repriza 2 ești negrul, cu dama. <strong>În doi</strong>, Jucătorul 1 are nebunii în repriza 1 și dama în repriza 2. Câștigă meciul cine a rezistat mai multe mutări cu nebunii.</p>
          </div>
          <p class="pp-role" style="margin-top:8px">Jocul vine din programul Chess Tutor Step 2 (metoda Steps), lecția 12.</p>
        </details>
===SCRIPT===
/* =====================================================
   DOI NEBUNI CONTRA DAMEI (Chess Tutor Step 2, lecția 12, joc 12a)
   Nebuni albi c5, e4 contra damei negre a1, fără regi. Nebunii trebuie să reziste 5 mutări (cu joc perfect, mai mult nu se poate).
   Dama nu are voie pe pătrate atacate de nebuni. Robotul Dragon joacă perfect:
   minimax exact, cu memorare, pe (nebun, nebun, damă, mutări rămase, cine mută).
   Cu joc perfect de ambele părți, nebunii rezistă 5 mutări (singura mutare bună la început: Nf2).
   ===================================================== */
/*COMMON*/
const LIMIT = 5, X = 64, ALL = ORT.concat(DIA);
let board, mode = 'robot', randomness = 0.9, round, S, nMoves, turn, roundOver, matchOver, selSq = null, busy = false;
let results = {}, strikes = { 1: 0, 2: 0 };
/* S = { d, l, q }: d = nebunul de pe pătratele negre (pornește de pe c5), l = cel de pe pătratele albe (e4), q = dama */
const pname = p => 'Jucătorul ' + p;
const bishopPlayer = () => round === 1 ? 1 : 2;
const humanSide = () => round === 1 ? 'w' : 'b';
const isHumanTurn = () => mode === 'duo' || turn === humanSide();
const curPlayer = () => turn === 'w' ? bishopPlayer() : 3 - bishopPlayer();

/* ---------- geometrie ---------- */
function queenAttacks(q, d, l) {              // ce nebuni atacă dama (lista de pătrate)
    const occ = t => t === d || t === l;
    const s = slide(q, ALL, occ);
    return [d, l].filter(b => b !== X && s.includes(b));
}
function bishopOn(t, d, l) {                  // nebunul care atacă pătratul t (cu dama pe t), sau X
    const occ = s => s === d || s === l || s === t;
    if (d !== X && slide(d, DIA, occ).includes(t)) return d;
    if (l !== X && slide(l, DIA, occ).includes(t)) return l;
    return X;
}
function whiteMoves(d, l, q) {                // [d2, l2, capturează dama?, de la, la]
    const occ = t => t === d || t === l || t === q, out = [];
    slide(d, DIA, occ).forEach(t => { if (t !== l) out.push([t, l, t === q, d, t]); });
    slide(l, DIA, occ).forEach(t => { if (t !== d) out.push([d, t, t === q, l, t]); });
    return out;
}
function queenMoves(d, l, q) {                // mutările permise ale damei: [la, capturează?]
    const occ = t => t === d || t === l, out = [];
    slide(q, ALL, occ).forEach(t => {
        if (t === d || t === l) out.push([t, true]);
        else if (bishopOn(t, d, l) === X) out.push([t, false]);
    });
    return out;
}
const hangs = m => !m[2] && queenAttacks(S.q, m[0], m[1]).length > 0;

/* ---------- căutare exactă: câte mutări sigure mai fac nebunii ---------- */
const memo = new Map();
function valW(d, l, q, left) {                // albul la mutare, nebunii în siguranță
    if (left <= 0) return 0;
    const K = (((d * 64 + l) * 64 + q) * 8 + left) * 2;
    let v = memo.get(K); if (v !== undefined) return v;
    v = 0;
    for (const m of whiteMoves(d, l, q)) {
        const x = m[2] ? left : queenAttacks(q, m[0], m[1]).length ? 0 : 1 + valB(m[0], m[1], q, left - 1);
        if (x > v) v = x;
        if (v === left) break;
    }
    memo.set(K, v); return v;
}
function valB(d, l, q, left) {                // negrul la mutare, niciun nebun atacat
    if (left <= 0) return 0;
    const K = (((d * 64 + l) * 64 + q) * 8 + left) * 2 + 1;
    let v = memo.get(K); if (v !== undefined) return v;
    v = left;
    for (const [t] of queenMoves(d, l, q)) {
        const x = valW(d, l, t, left);
        if (x < v) v = x;
        if (v === 0) break;
    }
    memo.set(K, v); return v;
}
function whiteMoveValue(m, left) { return m[2] ? left : queenAttacks(S.q, m[0], m[1]).length ? 0 : 1 + valB(m[0], m[1], S.q, left - 1); }

/* ---------- afișare ---------- */
function buildPos() {
    const p = {};
    if (S.d !== X) p[name(S.d)] = 'wB'; if (S.l !== X) p[name(S.l)] = 'wB'; if (S.q !== X) p[name(S.q)] = 'bQ';
    return p;
}
const isBishop = s => s !== X && (s === S.d || s === S.l);
function targetsOf(s) {
    if (turn === 'w') return isBishop(s) ? whiteMoves(S.d, S.l, S.q).filter(m => m[3] === s).map(m => m[4]) : [];
    return s === S.q ? queenMoves(S.d, S.l, S.q).map(m => m[0]) : [];
}
function showSelection(sq) {
    clearHL(true); $('.square-' + sq).addClass('highlight-selected');
    targetsOf(idx(sq)).forEach(t => $('.square-' + name(t)).addClass((t === S.q || isBishop(t)) ? 'highlight-capture' : 'highlight-legal'));
}
function updateUI() {
    document.getElementById('roundVal').textContent = round + ' / 2';
    document.getElementById('movesVal').textContent = nMoves + ' / ' + LIMIT;
    [1, 2].forEach(p => {
        document.getElementById('pp' + p + '-strikes').textContent = '❌'.repeat(strikes[p]) + '▫️'.repeat(MAX_STRIKES - strikes[p]);
        document.getElementById('pp' + p + '-role').textContent = p === bishopPlayer() ? '♗♗ nebunii albi' : '♛ dama neagră';
        document.getElementById('pp' + p).className = 'player-panel' + (!roundOver && !matchOver && curPlayer() === p ? ' active' : '');
        const r = results[p];
        document.getElementById('pp' + p + '-result').textContent = r === undefined ? '' : r >= LIMIT ? 'cu nebunii: a rezistat toate cele ' + LIMIT + ' mutări' : 'cu nebunii: a rezistat ' + r + (r === 1 ? ' mutare' : ' mutări');
    });
}
function turnMsg() {
    if (mode === 'duo') return pname(curPlayer()) + (turn === 'w' ? ' mută un nebun.' : ' mută dama.');
    return turn === 'w' ? 'Mută un nebun. Nu-l lăsa pe un pătrat unde îl poate captura dama.' : 'Mută dama. Încearcă să atingi un nebun neapărat.';
}

/* ---------- desfășurarea ---------- */
function newMatch() { results = {}; strikes = { 1: 0, 2: 0 }; matchOver = false; startRound(1); }
function startRound(r) {
    round = r; S = { d: idx('c5'), l: idx('e4'), q: idx('a1') };
    nMoves = 0; turn = 'w'; roundOver = false; selSq = null; busy = false;
    board.position(buildPos(), false); clearHL();
    document.getElementById('btn-round2').style.display = 'none';
    setStatus(turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function apply(from, to) {
    const f = idx(from), t = idx(to);
    selSq = null; clearHL();
    if (turn === 'w') {
        const capQ = t === S.q;
        if (capQ) S.q = X;
        if (S.d === f) S.d = t; else S.l = t;
        nMoves++;
        board.position(buildPos(), false); markLast(from, to); play(capQ ? sndCapture : sndMove);
        if (capQ) return endRound('w', 'Nebunul a capturat dama pe ' + to + '.');
        const att = queenAttacks(S.q, S.d, S.l);
        if (!att.length && nMoves >= LIMIT) return endRound('w', 'Nebunii au rezistat ' + LIMIT + ' mutări.');
        turn = 'b';
        if (!att.length && !queenMoves(S.d, S.l, S.q).length) { updateUI(); return endRound('w', 'Dama nu mai are nicio mutare.'); }
        setStatus(turnMsg()); updateUI();
    } else {
        const cap = isBishop(t);
        if (cap) { if (S.d === t) S.d = X; else S.l = X; }
        S.q = t;
        board.position(buildPos(), false); markLast(from, to); play(cap ? sndCapture : sndMove);
        if (cap) return endRound('b', 'Dama a capturat nebunul de pe ' + to + '.');
        if (nMoves >= LIMIT) return endRound('w', 'Nebunii au rezistat ' + LIMIT + ' mutări.');
        turn = 'w';
        const ms = whiteMoves(S.d, S.l, S.q);
        if (!ms.some(m => m[2] || !queenAttacks(S.q, m[0], m[1]).length)) {
            updateUI();
            return endRound('b', 'Orice ar muta albul, un nebun rămâne atacat de damă.');
        }
        setStatus(turnMsg()); updateUI();
    }
    if (!isHumanTurn()) robotMove();
}
function endRound(winner, why) {
    roundOver = true; setTimeout(() => play(sndMate), 250);
    // câte mutări au rezistat nebunii: mutarea după care dama a capturat nu se numără
    results[bishopPlayer()] = winner === 'w' ? LIMIT : turn === 'w' ? nMoves : Math.max(0, nMoves - 1);
    let msg;
    if (mode === 'robot') {
        const youWin = winner === humanSide();
        msg = (youWin ? '🏆 Ai câștigat! ' : '🤖 Robotul a câștigat. ') + why;
        if (round === 1 && !youWin) msg += '<br>Încearcă din nou: înainte de fiecare mutare, caută pătratele de unde dama ar putea ataca amândoi nebunii.';
    } else {
        msg = '🏁 ' + why + ' ' + (winner === 'w' ? 'Câștigă nebunii (' + pname(bishopPlayer()) + ').' : 'Câștigă dama (' + pname(3 - bishopPlayer()) + ').');
    }
    if (round === 1) document.getElementById('btn-round2').style.display = 'block';
    else { matchOver = true; if (mode === 'duo') msg += '<br><br>' + matchSummary(); }
    setStatus(msg, (mode === 'robot' ? winner === humanSide() : true) ? 'ok' : 'warn');
    updateUI();
}
function matchSummary() {
    const a = results[1], b = results[2];
    const w = a > b ? 1 : b > a ? 2 : 0;
    if (!w) return '🤝 <strong>Egalitate.</strong>';
    document.getElementById('pp' + w).className = 'player-panel winner';
    return '🏆 <strong>' + pname(w) + ' câștigă meciul</strong>: a rezistat mai multe mutări cu nebunii.';
}

/* ---------- Robotul ---------- */
function robotMove() {
    busy = true;
    setTimeout(() => {
        busy = false; if (roundOver) return;
        const left = LIMIT - nMoves;
        let from, to;
        if (turn === 'w') {
            const ms = whiteMoves(S.d, S.l, S.q);
            const safe = ms.filter(m => !hangs(m));
            let pick;
            if (Math.random() < randomness) pick = pickRandom(safe.length ? safe : ms);
            else {
                let bv = -1, best = [];
                ms.forEach(m => { const v = whiteMoveValue(m, left); if (v > bv) { bv = v; best = [m]; } else if (v === bv) best.push(m); });
                pick = pickRandom(best);
            }
            from = pick[3]; to = pick[4];
        } else {
            const ms = queenMoves(S.d, S.l, S.q);
            const caps = ms.filter(m => m[1]), quiet = ms.filter(m => !m[1]);
            let pick;
            if (caps.length && Math.random() >= randomness * 0.5) pick = pickRandom(caps);
            else if (quiet.length && Math.random() < randomness) pick = pickRandom(quiet);
            else if (caps.length) pick = pickRandom(caps);
            else {
                let bv = 1e9, best = [];
                quiet.forEach(m => { const v = valW(S.d, S.l, m[0], left); if (v < bv) { bv = v; best = [m]; } else if (v === bv) best.push(m); });
                pick = pickRandom(best);
            }
            from = S.q; to = pick[0];
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
    if (!ownPiece(f)) return turn === 'w' ? 'Acum mută un nebun alb.' : 'Acum mută dama neagră.';
    if (targetsOf(f).includes(t)) return null;
    if (turn === 'w') return 'Nebunul merge numai pe diagonală și nu sare peste piese.';
    const occ = s => s === S.d || s === S.l;
    if (slide(S.q, ALL, occ).includes(t)) {
        const b = bishopOn(t, S.d, S.l);
        return 'Dama nu are voie pe ' + to + ': acolo ar fi capturată de nebunul de pe ' + name(b) + '.';
    }
    return 'Dama merge pe linii, pe coloane și pe diagonale și nu sare peste piese.';
}
function tryMove(from, to) { const why = checkMove(from, to); if (why) return illegal(to, why); apply(from, to); }
function ownPiece(s) { return turn === 'w' ? isBishop(s) : s === S.q; }

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
        if (!ownPiece(s)) { illegal(source, turn === 'w' ? 'Acum mută un nebun alb.' : 'Acum mută dama neagră.'); return false; }
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
setTimeout(() => valW(idx('c5'), idx('e4'), idx('a1'), LIMIT), 50);   // calculul Dragonului, pregătit din timp
