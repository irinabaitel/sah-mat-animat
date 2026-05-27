const { Chess } = require('chess.js');
const fs = require('fs');

/* Cele 5 puzzle-uri ale utilizatorului — p1, p2, p4 sunt pe lecție; p3, p5 nu sunt
   pattern curat de „îndepărtare a apărătorului", deci NU le punem în arenă.
   Arena = 20 puzzle-uri Lichess pe tema deflection cu sacrificiu. */
const out = [];

const cand = JSON.parse(fs.readFileSync('/tmp/indepartare_candidates.json', 'utf8'));
for (const p of cand.slice(0, 20)) {
  const c = new Chess(p.fen);
  let ok = true;
  for (const u of p.moves) {
    const r = c.move({from: u.slice(0,2), to: u.slice(2,4), promotion: u.length>4?u[4]:'q'});
    if (!r) { ok = false; break; }
  }
  if (!ok) continue;
  const lvl = p.rating < 1450 ? 1 : (p.rating < 1650 ? 2 : 3);
  out.push({ id: 'li-' + p.id, fen: p.fen, moves: p.moves, level: lvl, gameUrl: 'https://lichess.org/training/' + p.id });
}

fs.writeFileSync('data/indepartare_top20.json', JSON.stringify(out, null, 2));
console.log('Written:', out.length);
