/* ---------- comun (sunete, geometrie, afișare) ---------- */
const COLS = 'abcdefgh';
const MAX_STRIKES = 3;
var sndMove = new Audio('Sounds/Move.mp3'), sndCapture = new Audio('Sounds/Capture.mp3'), sndMate = new Audio('Sounds/Mate.mp3');
function play(s) { try { s.currentTime = 0; s.play().catch(function () {}); } catch (e) {} }
const idx  = s => COLS.indexOf(s[0]) * 8 + (parseInt(s[1]) - 1);
const name = i => COLS[i >> 3] + ((i & 7) + 1);
const KN = [];
for (let s = 0; s < 64; s++) {
    const out = [];
    for (const [a, b] of [[1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,-1],[-2,1],[-1,2]]) {
        const c = (s >> 3) + a, r = (s & 7) + b;
        if (c >= 0 && c < 8 && r >= 0 && r < 8) out.push(c * 8 + r);
    }
    KN.push(out);
}
const ORT = [[1,0],[-1,0],[0,1],[0,-1]], DIA = [[1,1],[1,-1],[-1,1],[-1,-1]];
function slide(s, dirs, isOcc) {          // pătratele atinse pe linii; se oprește la prima piesă (inclusiv)
    const out = [];
    for (const [a, b] of dirs) {
        let c = (s >> 3) + a, r = (s & 7) + b;
        while (c >= 0 && c < 8 && r >= 0 && r < 8) { const t = c * 8 + r; out.push(t); if (isOcc(t)) break; c += a; r += b; }
    }
    return out;
}
function pickRandom(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function clearHL(keepLast) {
    const cls = 'highlight-selected highlight-legal highlight-capture sq-wrong' + (keepLast ? '' : ' highlight-last');
    $('#board [class*="square-"]').removeClass(cls);
}
function flashWrong(sq) { const el = $('.square-' + sq); el.addClass('sq-wrong'); setTimeout(() => el.removeClass('sq-wrong'), 600); }
function setStatus(msg, cls) { const el = document.getElementById('status-box'); el.innerHTML = msg; el.className = cls || ''; }
function markLast(from, to) { $('.square-' + from).addClass('highlight-last'); $('.square-' + to).addClass('highlight-last'); }
