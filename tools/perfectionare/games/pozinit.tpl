===FILE===
nivel1_joc_pozitia_initiala.html
===TITLE===
Înapoi la poziția inițială — Joc
===HEADER===
♔ Înapoi la poziția inițială
===CSS===
  .goal-row { display:flex; gap:3px; justify-content:center; margin-bottom:8px; flex-wrap:wrap; }
  .goal-cell { width:30px; text-align:center; font-size:0.72em; color:rgba(26,58,107,0.7); line-height:1.1; }
  .goal-cell img { width:28px; height:28px; display:block; margin:0 auto; opacity:0.35; }
  .goal-cell.done img { opacity:1; }
  .stars { font-size:1.3em; letter-spacing:2px; }
===PANEL===
        <div class="counter-row">
          <div class="counter-box"><div class="counter-lbl">Mutările tale</div><div class="counter-val" id="movesVal">0</div></div>
          <div class="counter-box"><div class="counter-lbl">Cel mai scurt drum</div><div class="counter-val" id="bestVal">29</div></div>
        </div>

        <div class="sec-title">Unde trebuie să ajungă piesele</div>
        <div class="goal-row" id="goalRow"></div>

        <div class="toggle-row">
          <button class="tgl-btn" id="btnThreat" onclick="toggleThreat()">Arată pătratele atacate</button>
        </div>

        <div id="status-box"></div>

        <button class="btn-game" onclick="undo()">↶ Mută înapoi</button>
        <button class="btn-game" onclick="restart()">↺ Încearcă din nou</button>

        <details class="howto" open>
          <summary>📖 Cum se joacă</summary>
          <div class="hl-box">
            <h4>Piesele</h4>
            <p>Piesele albe au ajuns pe rândul 8, în ordinea turn, cal, nebun, <strong>rege</strong>, <strong>damă</strong>, nebun, cal, turn. Atenție: regele stă pe d8, iar dama pe e8.</p>
            <p>Pe tablă mai sunt <strong>șase pioni negri și un cal negru</strong>. Ei nu se mută niciodată. Sunt obstacolele.</p>
          </div>
          <div class="hl-box">
            <h4>Ce ai de făcut</h4>
            <p>Du piesele albe în <strong>poziția inițială</strong>: turnurile pe a1 și h1, caii pe b1 și g1, nebunii pe c1 și f1, dama pe d1, regele pe e1.</p>
            <p>Muți numai cu albul, câte o piesă la fiecare mutare. Piesele merg ca în șah.</p>
          </div>
          <div class="hl-box warn">
            <h4>Ce nu ai voie</h4>
            <p>Nu ai voie să capturezi nimic.</p>
            <p>Nu ai voie să oprești o piesă pe un <strong>pătrat atacat</strong> de un pion negru sau de calul negru. Pionul negru atacă cele două pătrate de pe diagonală, din fața lui (în jos, spre rândul 1). O piesă poate totuși să treacă peste un pătrat atacat, fără să se oprească acolo.</p>
          </div>
          <div class="hl-box">
            <h4>Stelele</h4>
            <p>Se poate în <strong>29 de mutări</strong>. Dacă reușești în 29 primești ⭐⭐⭐, în cel mult 33 primești ⭐⭐, iar altfel ⭐.</p>
            <p>Gândește-te și la ordine: unele piese trebuie să plece primele, ca să le facă loc celorlalte.</p>
          </div>
        </details>
===SCRIPT===
/* =====================================================
   ÎNAPOI LA POZIȚIA INIȚIALĂ (Chess Tutor Step 2, lecția 12, joc 12c)
   Piesele albe pornesc de pe rândul 8 (Ra8 Cb8 Nc8 Rd8 De8 Nf8 Cg8 Th8)
   și trebuie duse pe pătratele de start, fără capturi și fără să se oprească
   pe pătrate atacate de pionii negri (a6 b4 c5 d6 f3 h5) sau de calul d5.
   Cel mai scurt drum: 29 de mutări (verificat cu IDA*).
   ===================================================== */
/*COMMON*/
const BEST = 29;
const BLACK = { a6: 'bP', b4: 'bP', c5: 'bP', d6: 'bP', f3: 'bP', h5: 'bP', d5: 'bN' };
const START = { a8: 'wR', b8: 'wN', c8: 'wB', d8: 'wK', e8: 'wQ', f8: 'wB', g8: 'wN', h8: 'wR' };
const GOAL = { a1: 'wR', b1: 'wN', c1: 'wB', d1: 'wQ', e1: 'wK', f1: 'wB', g1: 'wN', h1: 'wR' };
const PN = { R: 'Turnul', N: 'Calul', B: 'Nebunul', Q: 'Dama', K: 'Regele' };
let board, W, hist, selSq = null, done = false, showThreat = false;

/* pătratele atacate: pionii negri în jos pe diagonală, calul d5 în L */
const ATT = {};
(function () {
    for (const s in BLACK) {
        const c = COLS.indexOf(s[0]), r = parseInt(s[1]) - 1;
        if (BLACK[s] === 'bP') { for (const dc of [-1, 1]) if (c + dc >= 0 && c + dc < 8 && r > 0) { const t = COLS[c + dc] + r; if (!BLACK[t]) ATT[t] = s; } }
        else KN[idx(s)].forEach(t => { const n = name(t); if (!BLACK[n]) ATT[n] = s; });
    }
})();

const occAt = s => W[s] || BLACK[s] || null;
function reach(sq) {                      // pătratele unde poate merge piesa (fără reguli de siguranță): [pătrat, blocat de]
    const p = W[sq][1], s = idx(sq), out = [];
    const occ = t => !!occAt(name(t));
    if (p === 'N') KN[s].forEach(t => out.push(t));
    else if (p === 'K') { for (const [a, b] of ORT.concat(DIA)) { const c = (s >> 3) + a, r = (s & 7) + b; if (c >= 0 && c < 8 && r >= 0 && r < 8) out.push(c * 8 + r); } }
    else out.push(...slide(s, p === 'R' ? ORT : p === 'B' ? DIA : ORT.concat(DIA), occ));
    return out.map(name);
}
function whyNot(from, to) {               // null = mutare permisă
    const p = W[from][1];
    if (!reach(from).includes(to)) {
        if (p === 'N') return 'Calul sare numai în formă de „L”.';
        if (p === 'K') return 'Regele merge numai câte un pătrat.';
        const geo = idx(to), f = idx(from), dc = (geo >> 3) - (f >> 3), dr = (geo & 7) - (f & 7);
        const line = dc === 0 || dr === 0, diag = Math.abs(dc) === Math.abs(dr);
        if (p === 'R' && !line) return 'Turnul merge numai în linie dreaptă.';
        if (p === 'B' && !diag) return 'Nebunul merge numai pe diagonală.';
        if (p === 'Q' && !line && !diag) return 'Dama merge în linie dreaptă sau pe diagonală.';
        return PN[p] + ' nu sare peste piese.';
    }
    if (W[to]) return 'Pe ' + to + ' stă deja o piesă albă.';
    if (BLACK[to]) return 'Nu ai voie să capturezi.';
    if (ATT[to]) return 'Pe ' + to + ' piesa ar fi atacată de ' + (BLACK[ATT[to]] === 'bN' ? 'calul negru' : 'pionul negru') + ' de pe ' + ATT[to] + '.';
    return null;
}
const legalTargets = sq => reach(sq).filter(t => !whyNot(sq, t));
function solved() { return Object.keys(GOAL).every(s => W[s] === GOAL[s]); }

/* ---------- afișare ---------- */
function buildPos() { return Object.assign({}, BLACK, W); }
function paintThreat() {
    $('#board [class*="square-"]').removeClass('highlight-threat');
    if (showThreat) Object.keys(ATT).forEach(s => $('.square-' + s).addClass('highlight-threat'));
}
function redraw(last) {
    board.position(buildPos(), false); clearHL(); paintThreat();
    if (last) markLast(last[0], last[1]);
    updateUI();
}
function updateUI() {
    document.getElementById('movesVal').textContent = hist.length;
    let h = '';
    for (const s of Object.keys(GOAL)) {
        h += '<div class="goal-cell' + (W[s] === GOAL[s] ? ' done' : '') + '"><img src="https://lichess1.org/assets/piece/caliente/' + GOAL[s] + '.svg" alt="">' + s + '</div>';
    }
    document.getElementById('goalRow').innerHTML = h;
}
function showSelection(sq) {
    clearHL(true); $('.square-' + sq).addClass('highlight-selected');
    legalTargets(sq).forEach(t => $('.square-' + t).addClass('highlight-legal'));
}
function toggleThreat() {
    showThreat = !showThreat;
    const b = document.getElementById('btnThreat');
    b.className = 'tgl-btn' + (showThreat ? ' active' : '');
    b.textContent = showThreat ? 'Ascunde pătratele atacate' : 'Arată pătratele atacate';
    paintThreat();
}

/* ---------- desfășurarea ---------- */
function restart() {
    W = Object.assign({}, START); hist = []; selSq = null; done = false;
    redraw(null);
    setStatus('Alege o piesă albă și du-o spre pătratul ei de start.');
}
function undo() {
    if (!hist.length) return;
    const m = hist.pop(); W[m[0]] = W[m[1]]; delete W[m[1]];
    done = false; selSq = null;
    redraw(hist.length ? hist[hist.length - 1] : null);
    setStatus('Ai luat înapoi mutarea ' + m[0] + '–' + m[1] + '.');
}
function apply(from, to) {
    W[to] = W[from]; delete W[from]; hist.push([from, to]); selSq = null;
    redraw([from, to]); play(sndMove);
    if (solved()) {
        done = true; setTimeout(() => play(sndMate), 250);
        const n = hist.length, st = n <= BEST ? 3 : n <= BEST + 4 ? 2 : 1;
        let msg = '🏁 Toate piesele sunt la locul lor, în <strong>' + n + '</strong> ' + (n % 100 >= 20 || n % 100 === 0 ? 'de ' : '') + 'mutări. <span class="stars">' + '⭐'.repeat(st) + '</span>';
        msg += st === 3 ? '<br>Ai găsit cel mai scurt drum.' : '<br>Se poate și în ' + BEST + ' de mutări. Mai încearcă!';
        setStatus(msg, 'ok');
        return;
    }
    const p = W[to];
    setStatus(GOAL[to] === p ? PN[p[1]] + ' a ajuns la locul lui pe ' + to + '.' : 'Mutarea ' + hist.length + ': ' + from + '–' + to + '.');
}
function illegal(sq, reason) { if (sq) flashWrong(sq); selSq = null; clearHL(true); setStatus('⚠️ ' + reason, 'warn'); }
function tryMove(from, to) { const why = whyNot(from, to); if (why) return illegal(to, why); apply(from, to); }

/* ---------- input: click și drag ---------- */
board = Chessboard('board', {
    position: 'empty', pieceTheme: 'https://lichess1.org/assets/piece/caliente/{piece}.svg',
    draggable: true, showNotation: true,
    onDragStart: function (source) {
        if (done) return false;
        if (selSq && source !== selSq && !W[source]) { const from = selSq; setTimeout(() => tryMove(from, source), 0); return false; }
        if (!W[source]) { illegal(source, 'Piesele negre nu se mută. Mută o piesă albă.'); return false; }
        selSq = source; showSelection(source);
    },
    onDrop: function (source, target) {
        if (target === 'offboard' || target === source) return 'snapback';
        selSq = null;
        const why = whyNot(source, target);
        if (why) { illegal(target, why); return 'snapback'; }
        apply(source, target);
    },
    onSnapEnd: function () { board.position(buildPos(), false); paintThreat(); }
});
$(document).on('click', '#board [class*="square-"]', function () {
    if (done || !selSq) return;
    const m = (this.className || '').match(/square-([a-h][1-8])/); if (!m) return;
    const sq = m[1];
    if (sq === selSq || W[sq]) return;
    tryMove(selSq, sq);
});
$(window).resize(() => { board.resize(); redraw(hist.length ? hist[hist.length - 1] : null); });
restart();
