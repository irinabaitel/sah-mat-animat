===FILE===
nivel1_joc_cal_neaparate.html
===TITLE===
Calul și piesele neapărate — Joc
===HEADER===
♘ Calul și piesele neapărate
===CSS===
  #btn-show { background:rgba(255,255,255,0.4); }
===PANEL===
        <div class="toggle-row">
          <button class="tgl-btn active" id="modeSolo" onclick="setMode('solo')">👤 Singur</button>
          <button class="tgl-btn"        id="modeDuo"  onclick="setMode('duo')">👫 În doi</button>
        </div>

        <div class="counter-row">
          <div class="counter-box" id="roundBox" style="display:none"><div class="counter-lbl">Repriza</div><div class="counter-val" id="roundVal">1 / 2</div></div>
          <div class="counter-box"><div class="counter-lbl">Mutările calului</div><div class="counter-val" id="movesVal">0 / 40</div></div>
          <div class="counter-box"><div class="counter-lbl">Piese capturate</div><div class="counter-val" id="eatVal">0 / 13</div></div>
        </div>

        <div id="duoPanels" style="display:none">
          <div class="player-panel" id="pp1"><div class="pp-row"><span class="pp-name">👤 Jucătorul 1</span><span class="pp-strikes" id="pp1-strikes"></span></div><div class="pp-result" id="pp1-result"></div></div>
          <div class="player-panel" id="pp2"><div class="pp-row"><span class="pp-name">👤 Jucătorul 2</span><span class="pp-strikes" id="pp2-strikes"></span></div><div class="pp-result" id="pp2-result"></div></div>
        </div>

        <div id="status-box"></div>

        <button id="btn-round2" onclick="startRound(2)">▶ Repriza 2 — e rândul Jucătorului 2</button>
        <button class="btn-game" onclick="newMatch()">↺ Joacă din nou</button>
        <button class="btn-game" id="btn-show" onclick="showSolution()">👁 Arată drumul cel mai scurt</button>

        <details class="howto" open>
          <summary>📖 Cum se joacă</summary>
          <div class="hl-box">
            <h4>Piesele</h4>
            <p>Albul are un singur <strong>cal</strong>, pe b1. Negrul are toate piesele lui, în afară de rege și de cai: două turnuri, doi nebuni, regina și opt pioni. Piesele negre <strong>stau pe loc</strong> tot jocul. Mută numai calul.</p>
          </div>
          <div class="hl-box">
            <h4>Ce trebuie să faci</h4>
            <p>Capturează cu calul <strong>toate cele 13 piese negre</strong>.</p>
            <p>Calul sare în formă de „L”: două pătrate într-o direcție și unul într-o parte. El sare peste piese.</p>
          </div>
          <div class="hl-box warn">
            <h4>Două reguli importante</h4>
            <p><strong>1.</strong> Calul are voie să captureze numai piese <strong>neapărate</strong>. O piesă e apărată dacă altă piesă neagră ar putea captura calul după ce el a luat-o.</p>
            <p><strong>2.</strong> Calul nu are voie să se oprească pe un pătrat unde ar putea fi capturat. Atenție la pioni: pionii negri capturează pe diagonală, în jos.</p>
            <p>Pe măsură ce capturezi, piesele rămase apără tot mai puțin. O piesă apărată la început poate deveni neapărată mai târziu.</p>
          </div>
          <div class="hl-box">
            <h4>Câte mutări ai</h4>
            <p>Ai cel mult <strong>40 de mutări</strong>. Cu drumul cel mai scurt se poate în <strong>26 de mutări</strong>.</p>
            <p id="ruleDuo" style="display:none"><strong>În doi</strong>, fiecare jucător încearcă pe rând, cu aceeași poziție. Câștigă cine capturează toate piesele din mai puține mutări. Dacă niciunul nu reușește, câștigă cel care a capturat mai multe piese.</p>
          </div>
          <div class="hl-box ok">
            <h4>Un sfat</h4>
            <p>Uită-te întâi care piese nu sunt apărate deloc. Fiecare piesă capturată poate lăsa o altă piesă fără apărare. Caută ordinea în care piesele „se eliberează” una pe alta.</p>
          </div>
          <p class="pp-role" style="margin-top:8px">Jocul vine din programul Chess Tutor Step 1 (metoda Steps), lecția 5.</p>
        </details>
===SCRIPT===
/* =====================================================
   CALUL ȘI PIESELE NEAPĂRATE (Chess Tutor Step 1, lecția 5, joc 5b)
   Calul alb capturează toate piesele negre, dar numai pe cele neapărate,
   și nu se oprește niciodată pe un pătrat atacat. 40 de mutări; se poate în 26.
   ===================================================== */
/*COMMON*/
const MAX_MOVES = 40, BEST = 26, TOTAL = 13;
function startPieces() {
    const P = {};
    ['R', null, 'B', 'Q', null, 'B', null, 'R'].forEach((t, c) => { if (t) P[c * 8 + 7] = t; P[c * 8 + 6] = 'P'; });
    return P;
}
/* piesa neagră care ar putea captura calul pe pătratul t (după ce a luat ce era pe t); -1 = niciuna */
function attackerOf(P, t) {
    const occ = s => s in P;
    for (const k in P) {
        const s = +k; if (s === t) continue;
        const tp = P[k]; let hit = false;
        if (tp === 'P') hit = ((s >> 3) === (t >> 3) + 1 || (s >> 3) === (t >> 3) - 1) && (s & 7) === (t & 7) + 1;
        else if (tp === 'R') hit = slide(s, ORT, occ).includes(t);
        else if (tp === 'B') hit = slide(s, DIA, occ).includes(t);
        else if (tp === 'Q') hit = slide(s, ORT.concat(DIA), occ).includes(t);
        if (hit) return s;
    }
    return -1;
}
function after(P, t) { const Q = Object.assign({}, P); delete Q[t]; return Q; }
const PN = { P: 'pionul', R: 'turnul', B: 'nebunul', Q: 'regina' };

/* ---------- stare ---------- */
let board, mode = 'solo', round, P, K, moves, roundOver, matchOver, selSq = null, demo = null;
let results = {}, strikes = { 1: 0, 2: 0 };
const eaten = () => TOTAL - Object.keys(P).length;
const pname = p => 'Jucătorul ' + p;

function legalTargets(sq) { return idx(sq) === K ? KN[K].map(name) : []; }
function whyBad(t) {                       // null = mutare permisă
    const P2 = after(P, t), a = attackerOf(P2, t);
    if (a < 0) return null;
    if (P[t]) return cap(PN[P[t]]) + ' de pe ' + name(t) + ' este apărat' + (P[t] === 'Q' ? 'ă' : '') + ' de ' + PN[P2[a]] + ' de pe ' + name(a) + '.';
    return 'Pe ' + name(t) + ' calul ar putea fi capturat de ' + PN[P2[a]] + ' de pe ' + name(a) + '.';
}
function cap(s) { return s[0].toUpperCase() + s.slice(1); }
function safeMoves() { return KN[K].filter(t => whyBad(t) === null); }

function buildPos() { const pos = {}; for (const k in P) pos[name(+k)] = 'b' + P[k]; if (K !== null) pos[name(K)] = 'wN'; return pos; }
function showSelection(sq) {
    clearHL(true); $('.square-' + sq).addClass('highlight-selected');
    legalTargets(sq).forEach(t => $('.square-' + t).addClass(P[idx(t)] ? 'highlight-capture' : 'highlight-legal'));
}
function updateUI() {
    document.getElementById('roundVal').textContent = round + ' / 2';
    document.getElementById('movesVal').textContent = moves + ' / ' + MAX_MOVES;
    document.getElementById('eatVal').textContent = eaten() + ' / ' + TOTAL;
    [1, 2].forEach(p => {
        document.getElementById('pp' + p + '-strikes').textContent = '❌'.repeat(strikes[p]) + '▫️'.repeat(MAX_STRIKES - strikes[p]);
        document.getElementById('pp' + p).className = 'player-panel' + (!roundOver && !matchOver && round === p ? ' active' : '');
        const r = results[p];
        document.getElementById('pp' + p + '-result').textContent = !r ? '' : r.done ? 'a capturat tot în ' + r.moves + ' de mutări' : 'a capturat ' + r.eaten + ' piese';
    });
}

/* ---------- desfășurarea ---------- */
function newMatch() { stopDemo(); results = {}; strikes = { 1: 0, 2: 0 }; matchOver = false; startRound(1); }
function startRound(r) {
    stopDemo();
    round = r; P = startPieces(); K = idx('b1'); moves = 0; roundOver = false; selSq = null;
    board.position(buildPos(), false); clearHL();
    document.getElementById('btn-round2').style.display = 'none';
    setStatus(mode === 'duo' ? pname(r) + ' mută calul.' : 'Mută calul. Capturează toate piesele negre, dar numai pe cele neapărate.');
    updateUI();
}
function doMove(fromSq, toSq) {
    selSq = null; clearHL();
    const t = idx(toSq), captured = P[t] || null;
    if (captured) delete P[t];
    K = t; moves++;
    board.position(buildPos(), false); markLast(fromSq, toSq);
    play(captured ? sndCapture : sndMove);
    updateUI();
    if (!Object.keys(P).length) return endRound(true);
    if (moves >= MAX_MOVES) return endRound(false, 'Ai folosit toate cele 40 de mutări.');
    if (!safeMoves().length) return endRound(false, 'Calul nu mai are niciun pătrat sigur.');
    const who = mode === 'duo' ? pname(round) + ' mută calul.' : 'Mută calul.';
    setStatus(captured ? 'Ai capturat ' + PN[captured] + ' de pe ' + toSq + '. ' + who : who);
}
function endRound(done, why) {
    roundOver = true;
    setTimeout(() => play(sndMate), 250);
    results[round] = { done, moves, eaten: eaten() };
    let msg = done ? '🏆 Toate cele 13 piese au fost capturate în <strong>' + moves + ' de mutări</strong>. '
                   : '⛔ ' + why + ' Ai capturat ' + eaten() + ' din 13 piese. ';
    if (done) msg += moves <= BEST ? 'Exact drumul cel mai scurt!' : 'Drumul cel mai scurt are ' + BEST + ' de mutări.';
    if (mode === 'solo' && done) { if (typeof spawnConfetti === 'function') spawnConfetti(2);msg += '<br>' + (moves <= 30 ? '⭐⭐⭐' : moves <= 35 ? '⭐⭐☆' : '⭐☆☆'); }
    if (mode === 'duo') {
        if (round === 1) document.getElementById('btn-round2').style.display = 'block';
        else { matchOver = true; msg += '<br><br>' + matchSummary(); }
    }
    setStatus(msg, done ? 'ok' : 'warn');
    updateUI();
}
function matchSummary() {
    const a = results[1], b = results[2]; let w = 0;
    if (a.done && b.done) w = a.moves < b.moves ? 1 : b.moves < a.moves ? 2 : 0;
    else if (a.done || b.done) w = a.done ? 1 : 2;
    else w = a.eaten > b.eaten ? 1 : b.eaten > a.eaten ? 2 : 0;
    if (!w) return '🤝 <strong>Egalitate.</strong>';
    document.getElementById('pp' + w).className = 'player-panel winner';
    return '🏆 <strong>' + pname(w) + ' câștigă meciul.</strong>';
}
function illegal(sq, reason) {
    if (sq) flashWrong(sq);
    selSq = null; clearHL(true);
    if (mode !== 'duo') { setStatus('⚠️ ' + reason, 'warn'); return; }
    const p = round; strikes[p]++; updateUI();
    if (strikes[p] >= MAX_STRIKES) {
        roundOver = true; matchOver = true;
        const o = p === 1 ? 2 : 1;
        document.getElementById('btn-round2').style.display = 'none';
        document.getElementById('pp' + o).className = 'player-panel winner';
        setStatus('❌ ' + reason + '<br>' + pname(p) + ' a încercat 3 mutări nepermise.<br>🏆 <strong>' + pname(o) + ' câștigă meciul.</strong>', 'warn');
        return;
    }
    setStatus('❌ ' + reason + ' Încercări nepermise pentru ' + pname(p) + ': ' + strikes[p] + ' din ' + MAX_STRIKES + '.', 'warn');
}
function tryMove(from, to) {
    if (!legalTargets(from).includes(to)) return illegal(to, 'Calul sare numai în formă de „L”.');
    const why = whyBad(idx(to));
    if (why) return illegal(to, why);
    doMove(from, to);
}

/* ---------- drumul cel mai scurt (căutare în lățime pe toate pozițiile) ---------- */
function solve() {
    const P0 = startPieces(), keys = Object.keys(P0).map(Number), bit = {};
    keys.forEach((s, i) => bit[s] = i);
    const full = (1 << keys.length) - 1, start = idx('b1') * 4194304 + full;
    const prev = new Map([[start, -1]]), q = [start];
    for (let h = 0; h < q.length; h++) {
        const st = q[h], k = Math.floor(st / 4194304), m = st % 4194304;
        if (m === 0) { const path = []; let x = st; while (x !== start) { path.push(Math.floor(x / 4194304)); x = prev.get(x); } return path.reverse(); }
        const Pm = {}; keys.forEach(s => { if (m >> bit[s] & 1) Pm[s] = P0[s]; });
        for (const t of KN[k]) {
            const nm = (t in bit && (m >> bit[t] & 1)) ? m & ~(1 << bit[t]) : m;
            if (attackerOf(after(Pm, t), t) >= 0) continue;
            const ns = t * 4194304 + nm;
            if (!prev.has(ns)) { prev.set(ns, st); q.push(ns); }
        }
    }
    return null;
}
function stopDemo() { if (demo) { clearTimeout(demo); demo = null; } }
function showSolution() {
    startRound(round || 1); roundOver = true;
    const path = solve(); if (!path) return;
    setStatus('👁 Drumul cel mai scurt: ' + path.length + ' de mutări. Urmărește calul.');
    let i = 0;
    const stepf = () => {
        if (i >= path.length) { demo = null; setStatus('👁 Gata: toate piesele în ' + path.length + ' de mutări. Apasă „Joacă din nou” ca să încerci tu.', 'ok'); return; }
        const from = name(K), t = path[i++], c = t in P; if (c) delete P[t]; K = t; moves++;
        board.position(buildPos(), false); clearHL(); markLast(from, name(t)); play(c ? sndCapture : sndMove); updateUI();
        demo = setTimeout(stepf, 900);
    };
    demo = setTimeout(stepf, 600);
}

/* ---------- setări ---------- */
function setMode(m) {
    mode = m;
    document.getElementById('modeSolo').className = 'tgl-btn' + (m === 'solo' ? ' active' : '');
    document.getElementById('modeDuo').className  = 'tgl-btn' + (m === 'duo' ? ' active' : '');
    ['roundBox', 'duoPanels', 'ruleDuo'].forEach(id => document.getElementById(id).style.display = m === 'duo' ? '' : 'none');
    newMatch();
}

/* ---------- input: click și drag ---------- */
function canAct() { return !roundOver && !matchOver && !demo; }
board = Chessboard('board', {
    position: 'empty', pieceTheme: 'https://lichess1.org/assets/piece/caliente/{piece}.svg',
    draggable: true, showNotation: true,
    onDragStart: function (source) {
        if (!canAct()) return false;
        if (selSq && source !== selSq) { const from = selSq; setTimeout(() => tryMove(from, source), 0); return false; }
        if (idx(source) !== K) { illegal(source, 'Piesele negre stau pe loc. Mută calul alb.'); return false; }
        selSq = source; showSelection(source);
    },
    onDrop: function (source, target) {
        if (target === 'offboard' || target === source) return 'snapback';
        selSq = null;
        if (!legalTargets(source).includes(target)) { illegal(target, 'Calul sare numai în formă de „L”.'); return 'snapback'; }
        const why = whyBad(idx(target));
        if (why) { illegal(target, why); return 'snapback'; }
        doMove(source, target);
    },
    onSnapEnd: function () { board.position(buildPos(), false); }
});
$(document).on('click', '#board [class*="square-"]', function () {
    if (!canAct() || !selSq) return;
    const m = (this.className || '').match(/square-([a-h][1-8])/); if (!m) return;
    const sq = m[1];
    if (sq === selSq || P[idx(sq)]) return;
    tryMove(selSq, sq);
});
$(window).resize(() => board.resize());
newMatch();
