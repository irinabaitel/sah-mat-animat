// Tabelă completă pentru „Mat fără rege” (Chess Tutor Step 1, jocurile 8a/8b):
// albul: piesa A (dama sau turn) + turn, fără rege; negrul: regele singur.
// DW[(a*64+r)*64+k] = în câte mutări albe dă albul mat, albul la mutare (255 = nu poate forța).
// Regulile jocului: dacă regele capturează o piesă, albul pierde; patul = albul pierde.
// Folosire: node mat_fara_rege.js q|r out.bin
const fs = require('fs'), zlib = require('zlib');
const A = process.argv[2], OUT = process.argv[3];
const ORT = [[1,0],[-1,0],[0,1],[0,-1]], DIA = [[1,1],[1,-1],[-1,1],[-1,-1]];
const ADIR = A === 'q' ? ORT.concat(DIA) : ORT;
function slide(s, dirs, occ) { const out = [];
  for (const [a, b] of dirs) { let c = (s >> 3) + a, r = (s & 7) + b;
    while (c >= 0 && c < 8 && r >= 0 && r < 8) { const t = c * 8 + r; out.push(t); if (occ(t)) break; c += a; r += b; } }
  return out; }
const KM = []; for (let s = 0; s < 64; s++) { const o = [];
  for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) { if (!a && !b) continue;
    const c = (s >> 3) + a, r = (s & 7) + b; if (c >= 0 && c < 8 && r >= 0 && r < 8) o.push(c * 8 + r); } KM.push(o); }
function attacks(p, s, t, occ) { return slide(s, p === 'q' ? ORT.concat(DIA) : ORT, occ).includes(t); }
// atacat de alb pătratul t (regele negru nu blochează: îl scoatem; piesa capturată nu atacă)
function attacked(a, r, t) {
  const occ = x => x === a || x === r;
  return (a >= 0 && a !== t && attacks(A, a, t, occ)) || (r >= 0 && r !== t && attacks('r', r, t, occ));
}
// negrul la mutare: 'mate' | 'stale' | 'cap' | lista de pătrate
function blackStatus(a, r, k) {
  const chk = attacked(a, r, k), mv = [];
  let cap = false;
  for (const t of KM[k]) {
    if (t === a) { if (!attacked(-1, r, t)) cap = true; continue; }
    if (t === r) { if (!attacked(a, -1, t)) cap = true; continue; }
    if (!attacked(a, r, t)) mv.push(t);
  }
  if (cap) return 'cap';
  if (!mv.length) return chk ? 'mate' : 'stale';
  return mv;
}
function whiteMoves(a, r, k) { const occ = x => x === a || x === r || x === k, out = [];
  slide(a, ADIR, occ).forEach(t => { if (t !== r && t !== k) out.push([t, r]); });
  slide(r, ORT, occ).forEach(t => { if (t !== a && t !== k) out.push([a, t]); });
  return out; }
const N = 64 * 64 * 64, I = (a, r, k) => (a * 64 + r) * 64 + k;
const DW = new Uint8Array(N).fill(255), BS = new Array(N);
for (let a = 0; a < 64; a++) for (let r = 0; r < 64; r++) for (let k = 0; k < 64; k++)
  if (a !== r && a !== k && r !== k) BS[I(a, r, k)] = blackStatus(a, r, k);
const WM = new Array(N);
for (let a = 0; a < 64; a++) for (let r = 0; r < 64; r++) for (let k = 0; k < 64; k++)
  if (a !== r && a !== k && r !== k) WM[I(a, r, k)] = whiteMoves(a, r, k);
// DB(după mutarea albă) = câte mutări albe mai trebuie (0 = mat); 255 = nu
function DB(a, r, k) { const s = BS[I(a, r, k)];
  if (s === 'mate') return 0; if (s === 'stale' || s === 'cap') return 255;
  let w = 0; for (const t of s) { const v = DW[I(a, r, t)]; if (v > w) w = v; if (w === 255) break; } return w; }
for (let it = 1; it < 60; it++) { let ch = 0;
  for (let a = 0; a < 64; a++) for (let r = 0; r < 64; r++) for (let k = 0; k < 64; k++) {
    const i = I(a, r, k); if (a === r || a === k || r === k || DW[i] !== 255) continue;
    for (const [na, nr] of WM[i]) { if (DB(na, nr, k) === it - 1) { DW[i] = it; ch++; break; } }
  }
  if (!ch && it > 2) { console.log('stabil la', it); break; }
  console.log('it', it, ch);
}
const sq = s => 'abcdefgh'[s >> 3] + ((s & 7) + 1), idx = s => 'abcdefgh'.indexOf(s[0]) * 8 + (+s[1] - 1);
const start = A === 'q' ? I(idx('d1'), idx('a1'), idx('e6')) : I(idx('h1'), idx('a1'), idx('e6'));
console.log('start DW =', DW[start]);
let mx = 0; for (let i = 0; i < N; i++) if (DW[i] !== 255 && DW[i] > mx) mx = DW[i]; console.log('max', mx);
fs.writeFileSync(OUT, zlib.gzipSync(Buffer.from(DW), { level: 9 }));
console.log('scris', OUT, fs.statSync(OUT).size);
// linia principală de la start (pentru verificare)
let a = start >> 12, r = (start >> 6) & 63, k = start & 63, line = [];
while (true) { let best = null;
  for (const [na, nr] of WM[I(a, r, k)]) { const v = DB(na, nr, k); if (v !== 255 && (!best || v < best[0])) best = [v, na, nr]; }
  if (!best) break; const [v, na, nr] = best;
  line.push((na !== a ? A.toUpperCase() + sq(a) + sq(na) : 'R' + sq(r) + sq(nr)) + (v === 0 ? '#' : '')); a = na; r = nr;
  if (v === 0) break; const s = BS[I(a, r, k)]; let bk = s[0], bw = -1;
  for (const t of s) { const w = DW[I(a, r, t)]; if (w > bw) { bw = w; bk = t; } }
  line.push('K' + sq(k) + sq(bk)); k = bk; }
console.log(line.join(' '));
