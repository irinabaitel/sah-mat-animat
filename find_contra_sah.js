const { Chess } = require('chess.js');
const fs = require('fs');
const readline = require('readline');
const { spawn } = require('child_process');

const proc = spawn('zstdcat', ['data/lichess_db_puzzle.csv.zst']);
const rl = readline.createInterface({ input: proc.stdout });

let scanned = 0, found = [];
let isHeader = true;

rl.on('line', (line) => {
  if (isHeader) { isHeader = false; return; }
  if (!line || found.length >= 100) return;

  const parts = line.split(',');
  if (parts.length < 8) return;
  const [id, fen, moves, rating, , popularity, , themes] = parts;
  if (+rating < 1100 || +rating > 1900) return;
  if (+popularity < 80) return;
  if (!themes.includes('short') && !themes.includes('mate')) return;
  scanned++;
  try {
    const c = new Chess(fen);
    if (!c.in_check()) return;
    const ms = moves.split(' ');
    if (ms.length < 2) return;
    const first = ms[0];
    const mv = c.move({ from: first.slice(0,2), to: first.slice(2,4), promotion: first.length>4?first[4]:'q' });
    if (!mv) return;
    if (!c.in_check()) return;   // după mutare, regele advers trebuie să fie în șah
    found.push({ id, fen, moves: ms, rating: +rating, popularity: +popularity, themes, sanFirst: mv.san });
  } catch(e) {}
});

rl.on('close', () => {
  console.log('Scanned:', scanned, '/ Found:', found.length);
  // Sort: prefer didactic (shorter moves) and easier ratings first
  found.sort((a, b) => a.moves.length - b.moves.length || a.rating - b.rating);
  fs.writeFileSync('/tmp/contra_sah_candidates.json', JSON.stringify(found.slice(0, 50), null, 2));
  console.log('Top 20 candidates (shortest first):');
  found.slice(0, 20).forEach((p, i) => {
    console.log((i+1)+'. '+p.id, 'r='+p.rating, 'pop='+p.popularity, 'plies='+p.moves.length, 'first='+p.sanFirst, ' themes:', p.themes.substring(0,60));
  });
});
