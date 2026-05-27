const { Chess } = require('chess.js');
const fs = require('fs');

const pgn = fs.readFileSync('/tmp/lolli_study.pgn', 'utf8');

/* Strip variants (parentheses, recursive) and comments (braces, NAGs) */
function stripVariants(s) {
  let depth = 0, out = '';
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (ch === '(') { depth++; continue; }
    if (ch === ')') { depth--; continue; }
    if (depth === 0) out += ch;
  }
  return out;
}
function stripComments(s) {
  return s.replace(/\{[^}]*\}/g, ' ').replace(/\$\d+/g, ' ').replace(/[?!]+/g, '');
}

/* Split by Event headers */
const chapters = pgn.split(/(?=^\[Event )/m).filter(c => c.trim());

const puzzles = [];
chapters.forEach((chunk, idx) => {
  const chapterMatch = chunk.match(/^\[ChapterName "([^"]+)"/m);
  const chapterName = chapterMatch ? chapterMatch[1] : ('Chapter ' + idx);

  /* Linii de mutări = ce e după headerul ultim */
  const headerEnd = chunk.search(/^\s*$/m);
  if (headerEnd < 0) return;
  let body = chunk.substring(headerEnd);

  body = stripComments(body);
  body = stripVariants(body);
  body = body.replace(/\d+\.{1,3}/g, ' ').replace(/\s+/g, ' ').trim();
  body = body.replace(/\s*\*\s*$/, '').replace(/\s*1-0\s*$/, '').replace(/\s*0-1\s*$/, '').replace(/\s*1\/2-1\/2\s*$/, '');

  const sans = body.split(/\s+/).filter(s => s);

  /* Joc TOATE mutările */
  const c = new Chess();
  const fens = [c.fen()];
  for (const s of sans) {
    const r = c.move(s);
    if (!r) { console.warn('Stop at', s, 'in chapter', idx); break; }
    fens.push(c.fen());
  }

  if (sans.length < 3) {
    console.log(idx, chapterName, '— too short ('+sans.length+' plies), skip');
    return;
  }

  /* Vreau ULTIMELE 3 plies — pe ultimele 3 mutări (1 plies = una mutare albă/neagră).
     Așadar: FEN cu 3 plies înainte de final, plus ultimele 3 plies în 'moves'. */
  const finalPly = sans.length;
  const startPly = Math.max(0, finalPly - 3);
  const startFen = fens[startPly];
  const lastSans = sans.slice(startPly);

  /* Convertesc SAN-urile în UCI pornind de la startFen */
  const c2 = new Chess(startFen);
  const uci = [];
  for (const s of lastSans) {
    const r = c2.move(s);
    if (!r) { console.warn('Re-play failed at', s); break; }
    let u = r.from + r.to;
    if (r.promotion) u += r.promotion;
    uci.push(u);
  }

  if (uci.length < 3) return;

  /* Filtrez doar chapter-urile unde ULTIMA mutare e dama dând mat (sau ceva similar cu pattern Lolli) */
  const c3 = new Chess(startFen);
  let last = null;
  for (const u of uci) {
    last = c3.move({ from: u.slice(0,2), to: u.slice(2,4), promotion: u.length>4 ? u[4] : 'q' });
  }
  const isLolli = last && last.piece === 'q' && (last.to === 'g7' || last.to === 'g2') && last.san.includes('#');
  console.log(idx, chapterName, '— last:', last ? last.san : 'NONE', '— Lolli:', isLolli);

  puzzles.push({
    id: 'study-' + idx,
    fen: startFen,
    moves: uci,
    level: 2,
    chapterName,
    isLolli
  });
});

console.log('\nTotal puzzles:', puzzles.length);
console.log('Pure Lolli (Qg7/Qg2 mat):', puzzles.filter(p => p.isLolli).length);

/* Salvez TOATE (utilizatorul a zis „nu toate partidele" — adică toate chapters, dar doar ultimele 3 mutări) */
const out = puzzles.map(p => ({ id: p.id, fen: p.fen, moves: p.moves, level: p.level }));
fs.writeFileSync('/tmp/lolli_study_extracted.json', JSON.stringify(out, null, 2));
console.log('Saved to /tmp/lolli_study_extracted.json');
