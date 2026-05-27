const { Chess } = require('chess.js');
const fs = require('fs');

const cand = JSON.parse(fs.readFileSync('/tmp/fork_candidates.json', 'utf8'));

/* Iau 30 cele mai populare, le clasifez pe niveluri */
const out = [];
for (const p of cand.slice(0, 30)) {
  const c = new Chess(p.fen);
  /* Validez că UCI rulează */
  let ok = true;
  for (const u of p.moves) {
    const r = c.move({ from: u.slice(0,2), to: u.slice(2,4), promotion: u.length>4?u[4]:'q' });
    if (!r) { ok = false; break; }
  }
  if (!ok) continue;
  const lvl = p.rating < 1300 ? 1 : (p.rating < 1500 ? 2 : 3);
  out.push({
    id: p.id, fen: p.fen, moves: p.moves, level: lvl,
    gameUrl: 'https://lichess.org/training/' + p.id
  });
}
fs.writeFileSync('data/furculita_top30.json', JSON.stringify(out, null, 2));
console.log('Written:', out.length, 'puzzles');
