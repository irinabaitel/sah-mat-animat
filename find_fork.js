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
  /* tema "fork" PRIMARY, nu doar prezent. Eliminăm puzzle-uri dominate de alte teme (mate, kingsideAttack…) */
  const themeList = themes.split(' ');
  if (!themeList.includes('fork')) return;
  if (themeList.includes('mateIn1') || themeList.includes('mateIn2')) return;  /* lăsăm mate-urile pentru alt loc */
  if (!themeList.includes('short') && !themeList.includes('oneMove')) return;
  found.push({
    id, fen, moves: moves.split(' '), rating: +rating, popularity: +popularity, themes
  });
});

rl.on('close', () => {
  console.log('Found fork puzzles:', found.length);
  found.sort((a, b) => b.popularity - a.popularity || a.rating - b.rating);
  fs.writeFileSync('/tmp/fork_candidates.json', JSON.stringify(found.slice(0, 60), null, 2));
  console.log('Top 10 candidates (by popularity):');
  found.slice(0, 10).forEach((p, i) => {
    console.log((i+1)+'. '+p.id, 'r='+p.rating, 'pop='+p.popularity, 'plies='+p.moves.length, 'themes:', p.themes.substring(0, 60));
  });
});
