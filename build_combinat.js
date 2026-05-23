const { Chess } = require('chess.js');
const fs = require('fs');

const PUZZLES = [
  { fen: 'rnb1k1nr/p4ppp/4p3/1p1q4/1bpP1B2/2N1PQ2/1P3PPP/R3KBNR w KQkq - 0 1', san: 'Qg3'  },
  { fen: '1rbn1rk1/1p4pp/p2qp3/6N1/8/PQR3P1/1P4BP/4R2K w - - 0 1',              san: 'Qc2'  },
  { fen: 'rnb1k2r/pp3pbp/4p1pn/3q4/3P4/4BN2/PP2BPPP/RN1QK2R w KQkq - 0 1',     san: 'Qc1'  },
  { fen: 'r3rnk1/1p3ppp/p7/1q1P4/4b3/P4RN1/1B1Q2PP/R6K w - - 0 1',             san: 'Qd4'  },
  { fen: 'rnb1k2r/pp1q2bp/2p3pn/3p1pB1/3P3P/2NB1Q2/PPP1NPP1/R3K2R w KQkq - 0 1', san: 'Qe3+' },
  { fen: 'r4r1k/2p2qbp/1p4p1/1N6/1P2RnB1/P3Q3/6PP/1R4K1 b - - 0 1',            san: 'Qa2'  },
  { fen: '8/1kpR4/1p4P1/p7/2KPp3/1P6/P7/r7 b - - 0 1',                          san: 'Kc6'  },
  { fen: 'Q7/5ppk/1p5p/b2N1q2/4p3/P3P2P/2r2PP1/5RK1 w - - 0 1',                 san: 'Ne7'  },
  { fen: 'r1b2rk1/pp1nbppp/1qp1p3/6N1/2PPp3/1Q4P1/PP2PPBP/R1B1R1K1 b - - 0 1', san: 'Qa5'  },
  { fen: '5Q2/r1b2ppk/N5bp/pP2p3/4P1q1/3B2P1/5PKP/4R3 w - - 0 1',                san: 'Qc5'  },
  { fen: '2N5/p4rk1/4R1b1/1P4p1/P1R2p2/5P2/5KP1/r7 b - - 0 1',                  san: 'Bd3'  }
];

const out = [];
PUZZLES.forEach((p, i) => {
  const c = new Chess(p.fen);
  const r = c.move(p.san);
  if (!r) { console.error('FAIL', i, p.san); return; }
  let uci = r.from + r.to;
  if (r.promotion) uci += r.promotion;
  out.push({ id: 'user-' + (i+1), fen: p.fen, moves: [uci], level: 2 });
});
fs.writeFileSync('data/combinat_top11.json', JSON.stringify(out, null, 2));
console.log('Written:', out.length);
