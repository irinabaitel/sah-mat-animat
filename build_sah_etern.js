const { Chess } = require('chess.js');
const fs = require('fs');

// Puzzles for ARENA (exclude the 3 that go to the lesson page)
// Format: { id, fen, san (string with moves space-separated), level, url }
const PUZZLES = [
  // ── Chess.com puzzles ──
  { id: 'cc-530266',  level: 1, fen: '8/3q2kp/6p1/PPQ5/8/8/5PbP/5BK1 w - - 0 1',
    san: 'Kxg2 Qg4+ Kh1 Qf3+ Kg1 Qg4+ Bg2 Qd1+ Bf1 Qg4+',
    url: 'https://www.chess.com/puzzles/problem/530266' },
  // cc-2605450 eliminat — material egal, prima mutare g5 nu justifică defensiva; nedidactic
  { id: 'cc-530064',  level: 2, fen: '7k/4q1p1/p1np3P/4p3/K5QP/3PP3/BPP2r2/8 b - - 0 1',
    san: 'Na7 hxg7+ Qxg7 Qh5+ Qh7 Qe8+',
    url: 'https://www.chess.com/puzzles/problem/530064' },
  { id: 'cc-528562',  level: 1, fen: '6k1/5p1p/4p1p1/3p4/1b1P1Q1P/4P1P1/q4PK1/8 b - - 0 1',
    san: 'Be1 Qb8+ Kg7 Qe5+ f6 Qc7+',
    url: 'https://www.chess.com/puzzles/problem/528562' },
  { id: 'cc-498376',  level: 1, fen: '4rrk1/5pp1/p2p3p/1p1B4/4P3/P1BP2qb/6P1/R2Q1R1K w - - 0 1',
    san: 'gxh3 Qxh3+ Kg1 Qg3+ Kh1 Qh3+',
    url: 'https://www.chess.com/puzzles/problem/498376' },
  { id: 'cc-1103270', level: 2, fen: 'r3r1k1/5ppp/1p6/3B4/3P1B2/PP4P1/4R2q/3QK3 w - - 0 27',
    san: 'Bxa8 Qg1+ Kd2 Qxd4+ Ke1 Qg1+',
    url: 'https://www.chess.com/puzzles/problem/1103270' },
  { id: 'cc-484104',  level: 2, fen: '5k2/1bp1rp1p/p3p1p1/2Qp4/8/2P1R2P/Pq3PP1/4R1K1 w - - 0 1',
    san: 'Rxe6 fxe6 Rxe6 Qc1+ Kh2 Qf4+',
    url: 'https://www.chess.com/puzzles/problem/484104' },
  { id: 'cc-495020',  level: 1, fen: '3rr3/p1k5/5RNp/1p2n2P/2pq2P1/2R5/PP4Q1/1K6 b - - 0 1',
    san: 'Nxg6 Qc6+ Kb8 Qxb5+ Ka8 Qc6+',
    url: 'https://www.chess.com/puzzles/problem/495020' },
  { id: 'cc-539546',  level: 1, fen: '8/6pk/1pQ1p2p/2b2p2/P1P5/1B5P/3n2PK/8 w - - 0 1',
    san: 'Bc2 Nf1+ Kh1 Ng3+ Kh2 Nf1+',
    url: 'https://www.chess.com/puzzles/problem/539546' },
  { id: 'cc-493182',  level: 2, fen: '3R4/6pk/p1p5/2p1Qr2/2P1p1qP/1P2PrP1/P4PK1/5R2 w - - 0 1',
    san: 'Qe8 Rxg3+ fxg3 Qe2+ Kh3 Qxf1+',
    url: 'https://www.chess.com/puzzles/problem/493182' },
  { id: 'cc-523850',  level: 1, fen: 'r4rk1/p1pR1p2/2p3pK/6B1/2P4P/8/PP6/6bq b - - 0 1',
    san: 'f6 Rg7+ Kh8 Rh7+ Kg8 Rg7+',
    url: 'https://www.chess.com/puzzles/problem/523850' },
  { id: 'cc-543758',  level: 1, fen: '5Q2/1p5p/5p2/1p6/4R1b1/1k6/5rPP/2KR4 w - - 0 1',
    san: 'Rxg4 Rc2+ Kb1 Rb2+ Ka1 Ra2+ Kb1 Rb2+',
    url: 'https://www.chess.com/puzzles/problem/543758' },
  { id: 'cc-495604',  level: 3, fen: '8/8/pp3r1k/3pp1Rp/P2r1n2/4NP2/1P6/4K1R1 b - - 0 1',
    san: 'Nh3 Nf5+ Rxf5 Rg6+ Kh7 Rg7+ Kh8 Rg8+',
    url: 'https://www.chess.com/puzzles/problem/495604' },
  { id: 'cc-501520',  level: 2, fen: '2n3k1/6p1/7p/3pN3/8/PP2p3/5qPP/2Q4K b - - 0 1',
    san: 'e2 Qxc8+ Kh7 Qc2+ Kg8 Qc8+',
    url: 'https://www.chess.com/puzzles/problem/501520' },
  { id: 'cc-506796',  level: 2, fen: '6k1/5p1p/7q/6p1/4P1P1/3r1PQ1/6KP/8 b - - 0 1',
    san: 'Qh4 Qb8+ Kg7 Qe5+ f6 Qe7+ Kg6 Qe8+',
    url: 'https://www.chess.com/puzzles/problem/506796' },
  { id: 'cc-498640',  level: 1, fen: '4k3/1p1R2r1/7Q/pP2p3/P1q5/6PP/7K/8 w - - 0 1',
    san: 'Rxg7 Qe2+ Kg1 Qe1+ Kg2 Qe2+',
    url: 'https://www.chess.com/puzzles/problem/498640' },
  { id: 'cc-510560',  level: 2, fen: '7r/4Q2p/5p1k/2p3p1/8/2q4P/5PP1/2BR2K1 w - - 0 1',
    san: 'Rd7 Qxc1+ Kh2 Qf4+ Kg1 Qc1+',
    url: 'https://www.chess.com/puzzles/problem/510560' },
  { id: 'cc-509552',  level: 3, fen: '1Q3rk1/p5p1/8/7Q/4p2P/7q/P7/1R5K w - - 0 1',
    san: 'Qh2 Rf1+ Rxf1 Qxf1+ Qg1 Qh3+ Qh2 Qf1+',
    url: 'https://www.chess.com/puzzles/problem/509552' },
  { id: 'cc-508242',  level: 3, fen: 'kr5r/p1Q5/6p1/3p4/3b2P1/5P2/q6P/4RR1K b - - 0 1',
    san: 'Bb6 Qc6+ Rb7 Re8+ Rxe8 Qxe8+ Rb8 Qc6+',
    url: 'https://www.chess.com/puzzles/problem/508242' },
  { id: 'cc-56726',   level: 2, fen: 'r4rk1/pp2qpp1/7p/bP6/2PB4/P2P3P/3nBPR1/3Q2K1 b - - 0 1',
    san: 'Qxa3 Rxg7+ Kh8 Rxf7+ Kg8 Rg7+',
    url: 'https://www.chess.com/puzzles/problem/56726' },
  { id: 'cc-510206',  level: 2, fen: '7k/p4Q1p/1p2pp2/2n1q3/8/7K/6PP/8 b - - 0 1',
    san: 'Qg5 Qf8+ Qg8 Qxf6+ Qg7 Qd8+',
    url: 'https://www.chess.com/puzzles/problem/510206' },
  { id: 'cc-493188',  level: 2, fen: '8/5p1k/5Qp1/2P4p/2q5/6PP/5P1K/4r3 b - - 0 1',
    san: 'Qe4 Qxf7+ Kh8 Qf8+ Kh7 Qf7+',
    url: 'https://www.chess.com/puzzles/problem/493188' },
  { id: 'cc-1030848', level: 2, fen: '1n1k2r1/1b1p4/p2R4/P4N2/4P3/8/1PP2PPP/5RK1 w - - 4 29',
    san: 'e5 Rxg2+ Kh1 Rxf2+ Kg1 Rg2+',
    url: 'https://www.chess.com/puzzles/problem/1030848' },
  { id: 'cc-739168',  level: 2, fen: 'r1b4k/ppp2rpp/7q/7n/3p4/1Q1P2N1/PP2B1PP/R4R1K w - - 0 22',
    san: 'Qxf7 Nxg3+ Kg1 Nxe2+ Kh1 Ng3+',
    url: 'https://www.chess.com/puzzles/problem/739168' },

  // ── Exemple vechi cu mutări (din sah_etern.html ex 2 + sah_etern_exemple.html ex 2,3,6,7,8,10) ──
  { id: 'old-sacrif-turn', level: 2,
    fen: '7k/p5p1/1p2p3/3q4/2P2P2/P6P/3pr1PK/3Q1R2 w - - 0 1',
    san: 'Rf2 Rxf2 Qh5+ Kg8 Qe8+ Kh7 Qh5+ Kg8 Qe8+' },
  { id: 'old-dama-neobosita', level: 1,
    fen: '8/2pk2pp/8/4q3/PQ3p2/2PP1P1P/2P3P1/6K1 b - - 0 1',
    san: 'Qe1+ Kh2 Qg3+ Kh1 Qe1+ Kh2 Qg3+ Kg1 Qe1+ Kh2 Qg3+ Kg1' },
  { id: 'old-sacrif-urmarire', level: 2,
    fen: '4r1k1/1R3pp1/7p/p1p5/1b2p3/4r2P/4N1P1/5RK1 w - - 0 1',
    san: 'Rfxf7 Rxe2 Rxg7+ Kh8 Rh7+ Kg8' },
  { id: 'old-doua-turnuri', level: 2,
    fen: 'r4rk1/pp3pp1/7p/bP6/2PB4/q2P3P/3nBPR1/3Q2K1 w - - 0 1',
    san: 'Rxg7+ Kh8 Rxf7+ Kg8 Rg7+ Kh8 Rf7+' },
  { id: 'old-un-turn', level: 1,
    fen: '7r/pp3kqP/4p1n1/3p2PQ/8/r7/2R2P2/6K1 w - - 0 1',
    san: 'Rc7+ Kf8 Rc8+ Ke7 Rc7+' },
  { id: 'old-sacrif-complex', level: 3,
    fen: '2R2b1r/k1p2ppp/pp3n2/8/P3P3/B2n1P1P/5QPK/1q6 w - - 0 1',
    san: 'Qg3 Bd6 Rxc7+ Bxc7 Qxc7+ Ka8 Qc6+ Ka7 Qc7+ Ka8 Qc6+ Ka7' },
  { id: 'old-dama-2', level: 2,
    fen: '2r2rk1/6q1/1p5R/pP3P1Q/2p1P3/P2p4/1P6/3RKB2 b - - 0 1',
    san: 'Qg3+ Kd2 Qf4+ Kc3 Qe5+ Kd2 Qf4+ Ke1 Qg3+' }
];

const out = [];
let errors = 0;

for (const p of PUZZLES) {
  const c = new Chess(p.fen);
  const sans = p.san.trim().split(/\s+/);
  const uci = [];
  let ok = true;
  for (const s of sans) {
    const r = c.move(s);
    if (!r) {
      console.error('ERR', p.id, 'invalid SAN:', s, 'remaining:', sans.slice(sans.indexOf(s)).join(' '));
      ok = false;
      errors++;
      break;
    }
    let u = r.from + r.to;
    if (r.promotion) u += r.promotion;
    uci.push(u);
  }
  if (!ok) continue;

  // For chess.com puzzles: invert perspective so the user plays the attacker.
  // Apply the first ply (opponent's defensive/setup move) and start FEN there.
  // The "old-" puzzles already have the right perspective.
  let entryFen = p.fen;
  let entryMoves = uci;
  if (p.id.startsWith('cc-')) {
    const sim = new Chess(p.fen);
    sim.move(sans[0]);          // apply first ply
    entryFen = sim.fen();
    entryMoves = uci.slice(1);  // user starts from move 2
  }

  const entry = { id: p.id, fen: entryFen, moves: entryMoves, level: p.level };
  if (p.url) entry.gameUrl = p.url;
  out.push(entry);
}

console.log('Total puzzles:', out.length, '/ Errors:', errors);
fs.writeFileSync('data/sah_etern_top30.json', JSON.stringify(out, null, 2));
console.log('Written: data/sah_etern_top30.json');
