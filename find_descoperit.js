const { Chess } = require('chess.js');
const fs = require('fs');
const readline = require('readline');
const { spawn } = require('child_process');

const proc = spawn('zstdcat', ['data/lichess_db_puzzle.csv.zst']);
const rl = readline.createInterface({ input: proc.stdout });

let found = [];
let isHeader = true;

rl.on('line', (line) => {
  if (isHeader) { isHeader = false; return; }
  if (!line || found.length >= 600) return;

  const parts = line.split(',');
  if (parts.length < 8) return;
  const [id, fen, moves, rating, , popularity, , themes] = parts;
  if (+rating < 1100 || +rating > 1700) return;
  if (+popularity < 88) return;
  const themeList = themes.split(' ');
  if (!themeList.includes('discoveredAttack')) return;
  if (themeList.includes('mateIn1') || themeList.includes('mateIn2')) return;
  if (!themeList.includes('short') && !themeList.includes('oneMove')) return;
  found.push({ id, fen, moves: moves.split(' '), rating: +rating, popularity: +popularity, themes });
});

rl.on('close', () => {
  console.log('Found discoveredAttack puzzles:', found.length);
  found.sort((a, b) => b.popularity - a.popularity || a.rating - b.rating);
  fs.writeFileSync('/tmp/descoperit_candidates.json', JSON.stringify(found.slice(0, 60), null, 2));
  found.slice(0, 10).forEach((p, i) => {
    console.log((i+1)+'.', p.id, 'r='+p.rating, 'pop='+p.popularity, 'plies='+p.moves.length, 'themes:', p.themes.substring(0, 60));
  });
});
