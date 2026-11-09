const solve = require('./cursa_solver.js');
let t0 = Date.now(); const S = solve(); console.log('ms', Date.now() - t0);
const st = [S.sq('f1'), S.sq('c1'), S.sq('c8'), S.sq('f8')];
console.log('start white to move', S.V[S.enc(0, st)], ' black to move', S.V[S.enc(1, st)]);
let mx = 0, h = {}; for (const v of S.V) if (v !== 127) { mx = Math.max(mx, Math.abs(v)); h[v > 0 ? 'w' : v < 0 ? 'l' : 'd'] = (h[v > 0 ? 'w' : v < 0 ? 'l' : 'd'] || 0) + 1; }
console.log('max', mx, h);
