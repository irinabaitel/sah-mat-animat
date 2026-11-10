===FILE===
nivel1_joc_paznicul_vanatorul.html
===TITLE===
Paznicul și vânătorul — Joc
===HEADER===
♕♖ Paznicul și vânătorul
===CSS===
  .final-note { font-size:0.82em; line-height:1.5; color:var(--c-navy); margin-top:8px; }
  .final-note a { color:var(--c-navy); font-weight:700; }
===PANEL===
        <div class="toggle-row">
          <button class="tgl-btn active" id="varQ" onclick="setVariant('q')">♕♖ Regina și turnul</button>
          <button class="tgl-btn"        id="varR" onclick="setVariant('r')">♖♖ Două turnuri</button>
        </div>
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
          <div class="counter-box"><div class="counter-lbl">Mutările albului</div><div class="counter-val" id="movesVal">0</div></div>
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
            <p id="howPieces">Albul are <strong>regina</strong> pe d1 și <strong>turnul</strong> pe a1. Negrul are doar <strong>regele</strong>, pe e6. Regele alb nu e pe tablă.</p>
            <p>Albul mută primul. Apoi mută regele negru. Apoi iar albul și tot așa, pe rând.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea albul</h4>
            <p>Albul vrea să dea <strong>mat</strong> regelui negru, în cât mai puține mutări.</p>
            <p id="howRoles">Piesele albe lucrează împreună. Una e <strong>paznicul</strong>: ține o linie, ca regele să nu poată trece de ea. Cealaltă e <strong>vânătorul</strong>: dă șah și împinge regele spre margine. Pe drum, regina și turnul își schimbă des rolurile.</p>
          </div>
          <div class="hl-box">
            <h4>Ce vrea negrul</h4>
            <p>Negrul vrea ca regele lui să reziste cât mai mult. Regele nu are voie să intre în șah.</p>
            <p>Dacă o piesă albă stă lângă rege și nu e apărată de cealaltă, regele o capturează. Atunci <strong>albul a pierdut</strong>, pentru că o singură piesă nu poate da mat fără regele ei.</p>
          </div>
          <div class="hl-box warn">
            <h4>Atenție la pat</h4>
            <p>Dacă regele negru nu e în șah și nu mai are nicio mutare, e <strong>pat</strong>. În jocul nostru, la pat albul pierde. Lasă-i regelui măcar un pătrat liber până dai matul.</p>
          </div>
          <div class="hl-box">
            <h4>Reprizele</h4>
            <p>În repriza 1 tu ești albul, iar în repriza 2 ești regele negru și încerci să reziști cât poți. <strong>În doi</strong>, Jucătorul 1 e albul în repriza 1 și regele negru în repriza 2. Câștigă meciul cine, cu albul, a dat mat mai repede.</p>
          </div>
          <p class="final-note">Aici regele alb lipsește, ca să vezi bine cum lucrează împreună cele două piese. Matul adevărat, cu ambii regi pe tablă, îl găsești la Finaluri esențiale: <a href="pagina10.html">Regina și turnul</a> și <a href="pagina12.html">Două turnuri</a>.</p>
          <p class="pp-role" style="margin-top:8px">Jocul vine din programul Chess Tutor (metoda Steps), lecția 8.</p>
        </details>
===SCRIPT===
/* =====================================================
   PAZNICUL ȘI VÂNĂTORUL (Chess Tutor Step 1, lecția 8, jocurile 8a și 8b;
   Manualul Step 1, lecția 8, „Chasing and guarding”)
   Varianta q: Dd1 + Ta1 contra Re6; varianta r: Th1 + Ta1 contra Re6. Fără rege alb.
   Albul dă mat. Regele capturează o piesă neapărată → albul pierde; pat → albul pierde.
   Robotul Dragon joacă după tabelele complete data/mat_dama_turn.bin.gz și
   data/mat_doua_turnuri.bin.gz (tools/perfectionare/games/solve/mat_fara_rege.js):
   DW[(a*64+r)*64+k] = în câte mutări dă albul mat, albul la mutare (255 = nu poate forța).
   ===================================================== */
/*COMMON*/
const LIMIT = 50;
const VARS = {
    q: { a: 'q', start: { a: 24, r: 0, k: 37 }, file: 'data/mat_dama_turn.bin.gz' },     // d1, a1, e6
    r: { a: 'r', start: { a: 56, r: 0, k: 37 }, file: 'data/mat_doua_turnuri.bin.gz' }    // h1, a1, e6
};
const TABS = {}, PERFECT = { q: 4, r: 5 };
let V = 'q';
var sndCheck = new Audio('Sounds/Check.mp3');
const KM = [];
for (let s = 0; s < 64; s++) {
    const o = [];
    for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) {
        if (!a && !b) continue;
        const c = (s >> 3) + a, r = (s & 7) + b;
        if (c >= 0 && c < 8 && r >= 0 && r < 8) o.push(c * 8 + r);
    }
    KM.push(o);
}
const aDirs = () => VARS[V].a === 'q' ? ORT.concat(DIA) : ORT;
/* pătratul t e atacat de piesele albe (regele negru nu blochează; o piesă scoasă = -1) */
function attacked(a, r, t) {
    const occ = x => x === a || x === r;
    return (a >= 0 && a !== t && slide(a, aDirs(), occ).includes(t)) || (r >= 0 && r !== t && slide(r, ORT, occ).includes(t));
}
function kingMoves(st) {            // mutările permise ale regelui: [la, captură?]
    const out = [];
    KM[st.k].forEach(t => {
        if (t === st.a) { if (!attacked(-1, st.r, t)) out.push([t, 'a']); }
        else if (t === st.r) { if (!attacked(st.a, -1, t)) out.push([t, 'r']); }
        else if (!attacked(st.a, st.r, t)) out.push([t, null]);
    });
    return out;
}
function whiteMoves(st) {           // [piesă, la]
    const occ = x => x === st.a || x === st.r || x === st.k, out = [];
    slide(st.a, aDirs(), occ).forEach(t => { if (t !== st.r && t !== st.k) out.push(['a', t]); });
    slide(st.r, ORT, occ).forEach(t => { if (t !== st.a && t !== st.k) out.push(['r', t]); });
    return out;
}
const inCheck = st => attacked(st.a, st.r, st.k);
function DW(st) {
    const T = TABS[V]; if (!T) return 255;
    return T[(st.a * 64 + st.r) * 64 + st.k];
}
/* după o mutare albă, negrul la mutare: câte mutări albe mai trebuie (0 = mat, 255 = albul pierde/nu poate forța) */
function DB(st) {
    const ms = kingMoves(st);
    if (!ms.length) return inCheck(st) ? 0 : 255;
    if (ms.some(m => m[1])) return 255;
    let w = 0; for (const m of ms) w = Math.max(w, DW(Object.assign({}, st, { k: m[0] })));
    return w;
}
function moved(st, m) { const s = Object.assign({}, st); s[m[0]] = m[1]; return s; }
const hangs = s => kingMoves(s).some(m => m[1]);
const stale = s => !inCheck(s) && !kingMoves(s).length;
function robotPick(st, side, randomness, rnd) {
    if (side === 'w') {
        const ms = whiteMoves(st);
        const mates = ms.filter(m => { const s = moved(st, m); return inCheck(s) && !kingMoves(s).length; });
        if (mates.length && rnd() >= randomness * 0.5) return pickR(mates, rnd);
        const safe = ms.filter(m => { const s = moved(st, m); return !hangs(s) && !stale(s); });
        if (rnd() < randomness) return pickR(rnd() < 0.8 && safe.length ? safe : ms, rnd);
        let bv = 1e9, best = [];
        ms.forEach(m => {
            let v = DB(moved(st, m));
            if (v === 255) v = 1000 + (safe.includes(m) ? 0 : 500);
            if (v < bv) { bv = v; best = [m]; } else if (v === bv) best.push(m);
        });
        return pickR(best, rnd);
    }
    const ms = kingMoves(st), cap = ms.filter(m => m[1]);
    if (cap.length) return ['k', cap[0][0]];
    if (rnd() < randomness) return ['k', pickR(ms, rnd)[0]];
    let bv = -1, best = [];
    ms.forEach(m => {
        const s = Object.assign({}, st, { k: m[0] });
        let v = DW(s); v = (v === 255 ? 300 : v) * 100 + kingMoves(s).length;
        if (v > bv) { bv = v; best = [m]; } else if (v === bv) best.push(m);
    });
    return ['k', pickR(best, rnd)[0]];
}
function pickR(arr, rnd) { return arr[Math.floor(rnd() * arr.length)]; }

let board, mode = 'robot', randomness = 0.9, round, S, nMoves, turn, roundOver, matchOver, selSq = null, busy = false;
let results = {}, strikes = { 1: 0, 2: 0 }, tabFailed = {};
const pname = p => 'Jucătorul ' + p;
const whitePlayer = () => round === 1 ? 1 : 2;
const humanSide = () => round === 1 ? 'w' : 'b';
const isHumanTurn = () => mode === 'duo' || turn === humanSide();
const curPlayer = () => turn === 'w' ? whitePlayer() : 3 - whitePlayer();
const PN = () => ({ a: VARS[V].a === 'q' ? 'regina' : 'turnul de pe ' + name(S.a), r: VARS[V].a === 'q' ? 'turnul' : 'turnul de pe ' + name(S.r), k: 'regele' });
const FEN = () => ({ a: VARS[V].a === 'q' ? 'wQ' : 'wR', r: 'wR', k: 'bK' });

/* ---------- tabelele ---------- */
async function loadTab(v) {
    if (TABS[v] || tabFailed[v]) return;
    try {
        const res = await fetch(VARS[v].file);
        if (!res.ok) throw 0;
        const ds = res.body.pipeThrough(new DecompressionStream('gzip'));
        TABS[v] = new Uint8Array(await new Response(ds).arrayBuffer());
    } catch (e) { tabFailed[v] = true; }
}

/* ---------- afișare ---------- */
function buildPos() { const p = {}, F = FEN(); ['a', 'r', 'k'].forEach(x => { if (S[x] !== null) p[name(S[x])] = F[x]; }); return p; }
const pieceAt = s => ['a', 'r', 'k'].find(x => S[x] === s) || null;
function targetsOf(s) {
    const p = pieceAt(s); if (!p) return [];
    if (turn === 'w' && p === 'k' || turn === 'b' && p !== 'k') return [];
    return turn === 'w' ? whiteMoves(S).filter(m => m[0] === p).map(m => m[1]) : kingMoves(S).map(m => m[0]);
}
function showSelection(sq) {
    clearHL(true); $('.square-' + sq).addClass('highlight-selected');
    targetsOf(idx(sq)).forEach(t => $('.square-' + name(t)).addClass(pieceAt(t) ? 'highlight-capture' : 'highlight-legal'));
}
function markCheck() {
    $('#board [class*="square-"]').removeClass('highlight-check');
    if (S.a !== null && S.r !== null && inCheck(S)) $('.square-' + name(S.k)).addClass('highlight-check');
}
function updateUI() {
    document.getElementById('roundVal').textContent = round + ' / 2';
    document.getElementById('movesVal').textContent = nMoves;
    [1, 2].forEach(p => {
        document.getElementById('pp' + p + '-strikes').textContent = '❌'.repeat(strikes[p]) + '▫️'.repeat(MAX_STRIKES - strikes[p]);
        document.getElementById('pp' + p + '-role').textContent = p === whitePlayer() ? (V === 'q' ? '♕♖ albul' : '♖♖ albul') : '♚ regele negru';
        document.getElementById('pp' + p).className = 'player-panel' + (!roundOver && !matchOver && curPlayer() === p ? ' active' : '');
        const r = results[p];
        document.getElementById('pp' + p + '-result').textContent = r === undefined ? '' : r === null ? 'cu albul: nu a dat mat' : 'cu albul: a dat mat în ' + r + (r === 1 ? ' mutare' : ' mutări');
    });
}
function turnMsg() {
    if (mode === 'duo') return pname(curPlayer()) + (turn === 'w' ? ' mută o piesă albă.' : ' mută regele negru.');
    if (turn === 'b') return 'Mută regele negru. Ține-l cât mai departe de margine.';
    return 'Mută o piesă albă. Ai grijă ca regele să nu o poată captura.';
}

/* ---------- desfășurarea ---------- */
function newMatch() { results = {}; strikes = { 1: 0, 2: 0 }; matchOver = false; startRound(1); }
function startRound(r) {
    round = r; S = Object.assign({}, VARS[V].start);
    nMoves = 0; turn = 'w'; roundOver = false; selSq = null; busy = false;
    board.position(buildPos(), false); clearHL(); markCheck();
    document.getElementById('btn-round2').style.display = 'none';
    setStatus(turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function apply(from, to) {
    const f = idx(from), t = idx(to), p = pieceAt(f), cap = pieceAt(t), names = PN();
    if (cap) S[cap] = null;
    S[p] = t; if (turn === 'w') nMoves++;
    selSq = null; clearHL();
    board.position(buildPos(), false); markLast(from, to); markCheck();
    if (cap) { play(sndCapture); return endRound('b', 'Regele a capturat ' + names[cap] + ' pe ' + to + '. Fără ea, albul nu mai poate da mat.'); }
    if (turn === 'w') {
        const moves = kingMoves(S), chk = inCheck(S);
        if (!moves.length && chk) { play(sndMate); return endRound('w', 'Mat la mutarea ' + nMoves + '!'); }
        if (!moves.length) { play(sndMove); return endRound('b', 'Pat! Regele negru nu e în șah, dar nu mai are nicio mutare. La pat, albul pierde.'); }
        play(chk ? sndCheck : sndMove);
        if (nMoves >= LIMIT) return endRound('b', 'Regele negru a rezistat ' + LIMIT + ' de mutări ale albului.');
    } else play(sndMove);
    turn = turn === 'w' ? 'b' : 'w';
    setStatus(turnMsg()); updateUI();
    if (!isHumanTurn()) robotMove();
}
function endRound(winner, why) {
    roundOver = true;
    results[whitePlayer()] = winner === 'w' ? nMoves : null;
    let msg;
    const best = PERFECT[V];
    if (mode === 'robot') {
        const youWin = winner === humanSide();
        if (round === 1) {
            msg = (youWin ? '🏆 Ai câștigat! ' : '🤖 Robotul a câștigat. ') + why;
            if (youWin && nMoves > best) msg += '<br>Se poate și mai repede: oricum ar juca negrul, albul poate da mat în ' + best + ' mutări.';
            if (!youWin) msg += '<br>Încearcă din nou: înainte de fiecare mutare uită-te la pătratele din jurul regelui. O piesă albă de lângă rege trebuie să fie apărată de cealaltă.';
        } else {
            msg = (youWin ? '🏆 Ai câștigat! ' : '🤖 Robotul a dat mat. ') + why;
            if (!youWin) msg += '<br>Regele tău a rezistat ' + nMoves + (nMoves === 1 ? ' mutare' : ' mutări') + ' ale albului.';
        }
    } else {
        msg = '🏁 ' + why + ' ' + (winner === 'w' ? 'Câștigă albul (' + pname(whitePlayer()) + ').' : 'Câștigă regele negru (' + pname(3 - whitePlayer()) + ').');
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
    return '🏆 <strong>' + pname(w) + ' câștigă meciul</strong>: a dat mat mai repede.';
}

/* ---------- Robotul ---------- */
function robotMove() {
    busy = true;
    if (!TABS[V] && !tabFailed[V] && randomness < 0.5) { setStatus('🤖 Robotul se pregătește...'); loadTab(V); setTimeout(robotMove, 300); return; }
    setTimeout(() => {
        busy = false; if (roundOver) return;
        const m = robotPick(S, turn, randomness, Math.random);
        const from = turn === 'w' ? S[m[0]] : S.k;
        apply(name(from), name(m[1]));
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
    const other = pieceAt(t);
    if (p === 'k') {
        if (Math.abs((f >> 3) - (t >> 3)) > 1 || Math.abs((f & 7) - (t & 7)) > 1) return 'Regele merge numai câte un pătrat, în orice direcție.';
        if (other) return 'Piesa de pe ' + to + ' e apărată de cealaltă piesă albă. Regele nu are voie să o captureze.';
        return 'Pătratul ' + to + ' e atacat de o piesă albă. Regele nu are voie să intre în șah.';
    }
    if (other === 'k') return 'Regele nu se capturează. Albul trebuie să-i dea mat.';
    if (other) return 'Nu poți captura o piesă de aceeași culoare.';
    return p === 'a' && VARS[V].a === 'q' ? 'Regina merge pe linii, pe coloane și pe diagonale și nu sare peste piese.'
         : 'Turnul merge numai în linie dreaptă și nu sare peste piese.';
}
function tryMove(from, to) { const why = checkMove(from, to); if (why) return illegal(to, why); apply(from, to); }
function ownPiece(s) { const p = pieceAt(s); return !!p && (turn === 'w' ? p !== 'k' : p === 'k'); }

/* ---------- setări ---------- */
function setVariant(v) {
    V = v; loadTab(v);
    document.getElementById('varQ').className = 'tgl-btn' + (v === 'q' ? ' active' : '');
    document.getElementById('varR').className = 'tgl-btn' + (v === 'r' ? ' active' : '');
    document.getElementById('howPieces').innerHTML = v === 'q'
        ? 'Albul are <strong>regina</strong> pe d1 și <strong>turnul</strong> pe a1. Negrul are doar <strong>regele</strong>, pe e6. Regele alb nu e pe tablă.'
        : 'Albul are <strong>două turnuri</strong>, pe a1 și pe h1. Negrul are doar <strong>regele</strong>, pe e6. Regele alb nu e pe tablă.';
    document.getElementById('howRoles').innerHTML = v === 'q'
        ? 'Piesele albe lucrează împreună. Una e <strong>paznicul</strong>: ține o linie, ca regele să nu poată trece de ea. Cealaltă e <strong>vânătorul</strong>: dă șah și împinge regele spre margine. Pe drum, regina și turnul își schimbă des rolurile.'
        : 'Turnurile lucrează împreună. Unul e <strong>paznicul</strong>: ține o linie, ca regele să nu poată trece de ea. Celălalt e <strong>vânătorul</strong>: dă șah și împinge regele spre margine. Apoi își schimbă rolurile, ca o scară care urcă. E puțin mai greu decât cu regina, pentru că regele se poate apropia de turnuri.';
    newMatch();
}
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
        if (!ownPiece(s)) { illegal(source, turn === 'w' ? 'Acum mută albul.' : 'Acum mută regele negru.'); return false; }
        selSq = source; showSelection(source);
    },
    onDrop: function (source, target) {
        if (target === 'offboard' || target === source) return 'snapback';
        selSq = null;
        const why = checkMove(source, target);
        if (why) { illegal(target, why); return 'snapback'; }
        apply(source, target);
    },
    onSnapEnd: function () { board.position(buildPos(), false); markCheck(); }
});
$(document).on('click', '#board [class*="square-"]', function () {
    if (!canAct() || !selSq) return;
    const m = (this.className || '').match(/square-([a-h][1-8])/); if (!m) return;
    const sq = m[1];
    if (sq === selSq || ownPiece(idx(sq))) return;
    tryMove(selSq, sq);
});
$(window).resize(() => board.resize());
loadTab('q');
setVariant(new URLSearchParams(location.search).get('v') === '2' ? 'r' : 'q');
