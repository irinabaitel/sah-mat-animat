const { Chess } = require('chess.js');
const fs = require('fs');

/* 2 puzzle-uri din utilizator (p3, p5) — p1, p2, p4 merg pe lecție */
const USER_PUZZLES = [
  { id: 'user-p3', level: 2, fen: '6r1/1p1np2k/p4b1p/q1pP4/2P1N3/4B3/PPQ4P/5RK1 w - - 0 1',
    san: 'Ng5+ Kg7 Qh7+ Kf8 Qf7#' },
  { id: 'user-p5', level: 3, fen: '2b5/5Npp/p1P5/P1R4k/1p4r1/3r1pPK/4BP1P/7R b - - 1 31',
    san: 'Rg5+ g4+ Bxg4+ Kg3 fxe2+ f3 Rxf3+ Kg2 Rxc5' }
];

const out = [];

for (const p of USER_PUZZLES) {
  const c = new Chess(p.fen);
  const sans = p.san.trim().split(/\s+/);
  const uci = [];
  for (const s of sans) {
    const r = c.move(s);
    if (!r) { console.error('FAIL', p.id, 'at', s); break; }
    let u = r.from + r.to;
    if (r.promotion) u += r.promotion;
    uci.push(u);
  }
  out.push({ id: p.id, fen: p.fen, moves: uci, level: p.level });
}

/* Lichess candidates */
const cand = JSON.parse(fs.readFileSync('/tmp/contra_sah_candidates.json', 'utf8'));

/* Iau primele 10 cu ply=2 (mat în 1) + primele 8 cu ply=4 */
const ply2 = cand.filter(p => p.moves.length === 2).slice(0, 10);
const ply4 = cand.filter(p => p.moves.length === 4).slice(0, 8);

[...ply2, ...ply4].forEach(p => {
  const lvl = p.rating < 1200 ? 1 : (p.rating < 1500 ? 2 : 3);
  out.push({
    id: 'li-' + p.id,
    fen: p.fen,
    moves: p.moves,
    level: lvl,
    gameUrl: 'https://lichess.org/training/' + p.id
  });
});

/* Verify all via chess.js */
let allOk = true;
out.forEach(p => {
  const c = new Chess(p.fen);
  if (!c.in_check()) { console.warn('WARN', p.id, 'NOT in check at start'); }
  for (let i = 0; i < p.moves.length; i++) {
    const u = p.moves[i];
    const r = c.move({ from: u.slice(0,2), to: u.slice(2,4), promotion: u.length>4 ? u[4] : 'q' });
    if (!r) { console.error('FAIL', p.id, 'at move', i, u); allOk = false; break; }
  }
});

console.log('Total puzzles:', out.length, allOk ? '— ALL OK' : '— ERRORS');
fs.writeFileSync('data/contra_sah_top20.json', JSON.stringify(out, null, 2));
console.log('Written: data/contra_sah_top20.json');
