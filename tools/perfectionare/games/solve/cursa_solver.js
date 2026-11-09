/* CURSA NEBUNILOR — analiză retrogradă completă (se rulează și în pagină).
   Stare: latura la mutare + nebunii [alb-alb, alb-negru, negru-alb, negru-negru]
   (alb = pe pătrate albe, negru = pe pătrate negre), fiecare 0..31 în lista pătratelor de culoarea lui.
   V[stare] > 0: cel la mutare câștigă cu ultima mutare la semimutarea V (1 = acum);
   V < 0: pierde, adversarul câștigă la semimutarea -V; 0: remiză; 127 = poziție imposibilă. */
function solveCursa() {
    const LS = [], DS = [];
    for (let s = 0; s < 64; s++) (((s >> 3) + (s & 7)) % 2 ? LS : DS).push(s);
    const SQ = [LS, DS, LS, DS];                    // piesa 0 = alb pe alb, 1 = alb pe negru, 2 = negru pe alb, 3 = negru pe negru
    const POS = [new Int8Array(64).fill(-1), new Int8Array(64).fill(-1)];
    LS.forEach((s, i) => POS[0][s] = i); DS.forEach((s, i) => POS[1][s] = i);
    const sqI = (p, s) => POS[p & 1][s];
    const T = [sq('c8'), sq('f8'), sq('f1'), sq('c1')];   // ținta fiecărei piese
    function sq(n) { return 'abcdefgh'.indexOf(n[0]) * 8 + (+n[1] - 1); }
    const DIRS = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
    const N = 2 * 32 * 32 * 32 * 32;
    const V = new Int8Array(N), C = new Uint8Array(N);
    const enc = (side, p) => (((((side * 32 + sqI(0, p[0])) * 32 + sqI(1, p[1])) * 32 + sqI(2, p[2])) * 32) + sqI(3, p[3]));
    function dec(i) { const p = new Array(4); for (let k = 3; k >= 0; k--) { p[k] = SQ[k][i & 31]; i >>= 5; } return [i, p]; }
    function rays(p, k) {                            // pătratele atinse de piesa k (se oprește la prima piesă, inclusiv)
        const out = [], s0 = p[k];
        for (const [a, b] of DIRS) {
            let c = (s0 >> 3) + a, r = (s0 & 7) + b;
            while (c >= 0 && c < 8 && r >= 0 && r < 8) { const t = c * 8 + r; out.push(t); if (p.includes(t)) break; c += a; r += b; }
        }
        return out;
    }
    const mine = side => side === 0 ? [0, 1] : [2, 3];
    const enemyOf = k => k ^ 2;                       // același fel de pătrate, cealaltă culoare
    const home = (side, p) => mine(side).every(k => p[k] === T[k]);
    /* mutările laturii la mutare: [k, t, câștig?] */
    function moves(side, p) {
        const out = [];
        for (const k of mine(side)) for (const t of rays(p, k)) {
            const j = p.indexOf(t);
            if (j >= 0) { if (j === enemyOf(k)) out.push([k, t, true]); continue; }
            const q = p.slice(); q[k] = t;
            out.push([k, t, home(side, q)]);
        }
        return out;
    }
    const valid = (side, p) => p[0] !== p[2] && p[1] !== p[3] && !home(0, p) && !home(1, p);
    const queue = new Int32Array(N); let qh = 0, qt = 0;
    for (let i = 0; i < N; i++) {
        const [side, p] = dec(i);
        if (!valid(side, p)) { V[i] = 127; continue; }
        const ms = moves(side, p);
        if (ms.some(m => m[2])) { V[i] = 1; queue[qt++] = i; } else C[i] = ms.length;
    }
    while (qh < qt) {
        const i = queue[qh++], v = V[i];
        const [side, p] = dec(i), prev = 1 - side;
        for (const k of mine(prev)) for (const y of rays(p, k)) {   // de unde putea veni piesa k (mutările nebunului sunt reversibile)
            if (p.includes(y)) continue;
            const q = p.slice(); q[k] = y;
            const j = enc(prev, q);
            if (V[j] !== 0) continue;
            if (v > 0) { if (--C[j] === 0) { V[j] = -(v + 1); queue[qt++] = j; } }
            else { V[j] = -v + 1; queue[qt++] = j; }
        }
    }
    return { V, enc, dec, moves, T, sq };
}
if (typeof module !== 'undefined') module.exports = solveCursa;
