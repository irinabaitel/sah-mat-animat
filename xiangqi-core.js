/* ════════════════════════════════════════════════════════════════
   XIANGQI CORE — motor + tablă desenată în cod (SVG)
   Folosit de: xiangqi_pagina1 / _mutari / _arena / _tactici
   Tablă: 9 coloane (f=0..8) × 10 rânduri (r=0..9). Piesele stau pe
   INTERSECȚII. r=0 = rândul de bază ROȘU (jos), r=9 = NEGRU (sus).
   Pătrat (square) reprezentat ca string "f,r".
   ════════════════════════════════════════════════════════════════ */
window.XQ = (function () {

  const COLS = 9, ROWS = 10;
  const RED = 'r', BLACK = 'b';

  // Caractere autentice: roșul folosește varianta „de curte", negrul „de rând".
  const CHAR = {
    r: { K:'帥', A:'仕', E:'相', H:'傌', R:'俥', C:'炮', S:'兵' },
    b: { K:'將', A:'士', E:'象', H:'馬', R:'車', C:'砲', S:'卒' }
  };
  const NAME = { K:'Generalul', A:'Sfetnicul', E:'Elefantul', H:'Calul', R:'Carul', C:'Tunul', S:'Soldatul' };
  const PINYIN = { K:'shuài / jiàng', A:'shì', E:'xiàng', H:'mǎ', R:'jū', C:'pào', S:'bīng / zú' };

  const sq = (f, r) => f + ',' + r;
  const parse = s => { const a = s.split(','); return { f:+a[0], r:+a[1] }; };
  const onBoard = (f, r) => f >= 0 && f < COLS && r >= 0 && r < ROWS;

  /* Poziția de start. ROȘU jos (r=0..), NEGRU sus (r=9..). */
  function startPosition() {
    const p = {};
    const back = ['R','H','E','A','K','A','E','H','R'];
    for (let f = 0; f < 9; f++) {
      p[sq(f,0)] = { c:RED,   t:back[f] };
      p[sq(f,9)] = { c:BLACK, t:back[f] };
    }
    p[sq(1,2)] = { c:RED, t:'C' };  p[sq(7,2)] = { c:RED, t:'C' };
    p[sq(1,7)] = { c:BLACK,t:'C' };  p[sq(7,7)] = { c:BLACK,t:'C' };
    for (const f of [0,2,4,6,8]) {
      p[sq(f,3)] = { c:RED,   t:'S' };
      p[sq(f,6)] = { c:BLACK, t:'S' };
    }
    return p;
  }

  const inPalace = (c, f, r) =>
    f >= 3 && f <= 5 && (c === RED ? (r >= 0 && r <= 2) : (r >= 7 && r <= 9));
  // râul: roșul e pe r 0..4, negrul pe r 5..9
  const ownHalf = (c, r) => (c === RED ? r <= 4 : r >= 5);

  function findGeneral(pos, c) {
    for (const k in pos) if (pos[k].c === c && pos[k].t === 'K') return k;
    return null;
  }

  /* Generalii „zburători": pe aceeași coloană, fără nimic între ei. */
  function generalsFacing(pos) {
    const rk = findGeneral(pos, RED), bk = findGeneral(pos, BLACK);
    if (!rk || !bk) return false;
    const a = parse(rk), b = parse(bk);
    if (a.f !== b.f) return false;
    const lo = Math.min(a.r, b.r), hi = Math.max(a.r, b.r);
    for (let r = lo + 1; r < hi; r++) if (pos[sq(a.f, r)]) return false;
    return true;
  }

  /* Mutări PSEUDO-legale (fără verificarea propriului general). */
  function pseudoMoves(pos, s) {
    const pc = pos[s]; if (!pc) return [];
    const { f, r } = parse(s), c = pc.c, t = pc.t, out = [];
    const enemy = c === RED ? BLACK : RED;
    const add = (nf, nr) => {
      if (!onBoard(nf, nr)) return;
      const tg = pos[sq(nf, nr)];
      if (!tg || tg.c === enemy) out.push(sq(nf, nr));
    };

    if (t === 'K') {
      [[1,0],[-1,0],[0,1],[0,-1]].forEach(([df,dr]) => {
        const nf = f+df, nr = r+dr;
        if (inPalace(c, nf, nr)) add(nf, nr);
      });
    } else if (t === 'A') {
      [[1,1],[1,-1],[-1,1],[-1,-1]].forEach(([df,dr]) => {
        const nf = f+df, nr = r+dr;
        if (inPalace(c, nf, nr)) add(nf, nr);
      });
    } else if (t === 'E') {
      [[2,2],[2,-2],[-2,2],[-2,-2]].forEach(([df,dr]) => {
        const nf = f+df, nr = r+dr;
        if (!onBoard(nf, nr)) return;
        if (!ownHalf(c, nr)) return;                 // nu trece râul
        if (pos[sq(f+df/2, r+dr/2)]) return;          // ochiul elefantului
        add(nf, nr);
      });
    } else if (t === 'H') {
      const legs = [
        [ 1, 2, 0, 1],[ -1, 2, 0, 1],[ 1,-2, 0,-1],[ -1,-2, 0,-1],
        [ 2, 1, 1, 0],[ 2,-1, 1, 0],[ -2, 1,-1, 0],[ -2,-1,-1, 0]
      ];
      legs.forEach(([df,dr,lf,lr]) => {
        if (pos[sq(f+lf, r+lr)]) return;              // piciorul calului
        add(f+df, r+dr);
      });
    } else if (t === 'R') {
      [[1,0],[-1,0],[0,1],[0,-1]].forEach(([df,dr]) => {
        let nf = f+df, nr = r+dr;
        while (onBoard(nf, nr)) {
          const tg = pos[sq(nf, nr)];
          if (!tg) out.push(sq(nf, nr));
          else { if (tg.c === enemy) out.push(sq(nf, nr)); break; }
          nf += df; nr += dr;
        }
      });
    } else if (t === 'C') {
      [[1,0],[-1,0],[0,1],[0,-1]].forEach(([df,dr]) => {
        let nf = f+df, nr = r+dr, jumped = false;
        while (onBoard(nf, nr)) {
          const tg = pos[sq(nf, nr)];
          if (!jumped) {
            if (!tg) out.push(sq(nf, nr));
            else jumped = true;                       // ecranul tunului
          } else if (tg) {
            if (tg.c === enemy) out.push(sq(nf, nr)); // ținta de după ecran
            break;
          }
          nf += df; nr += dr;
        }
      });
    } else if (t === 'S') {
      const fwd = c === RED ? 1 : -1;
      add(f, r + fwd);
      if (!ownHalf(c, r)) { add(f+1, r); add(f-1, r); }   // după râu: lateral
    }
    return out;
  }

  function applyMove(pos, from, to) {
    const np = {};
    for (const k in pos) np[k] = pos[k];
    np[to] = np[from];
    delete np[from];
    return np;
  }

  function inCheck(pos, c) {
    const gk = findGeneral(pos, c); if (!gk) return true;
    const enemy = c === RED ? BLACK : RED;
    for (const k in pos) {
      if (pos[k].c !== enemy) continue;
      if (pseudoMoves(pos, k).includes(gk)) return true;
    }
    return false;
  }

  /* Mutări LEGALE: nu lasă propriul general în șah și nu pune
     generalii față în față pe coloană liberă. */
  function legalMoves(pos, s) {
    const pc = pos[s]; if (!pc) return [];
    return pseudoMoves(pos, s).filter(to => {
      const np = applyMove(pos, s, to);
      if (generalsFacing(np)) return false;
      return !inCheck(np, pc.c);
    });
  }

  function hasAnyMove(pos, c) {
    for (const k in pos) {
      if (pos[k].c === c && legalMoves(pos, k).length > 0) return true;
    }
    return false;
  }

  /* Stare joc. La xiangqi: șah-mat = victorie; FĂRĂ mutări (chiar
     fără șah) = PIERZI (pat = pierdere). */
  function status(pos, turn) {
    if (!findGeneral(pos, RED))   return { over:true, winner:BLACK, reason:'Generalul roșu a fost capturat' };
    if (!findGeneral(pos, BLACK)) return { over:true, winner:RED,   reason:'Generalul negru a fost capturat' };
    if (!hasAnyMove(pos, turn)) {
      const checked = inCheck(pos, turn);
      return {
        over: true,
        winner: turn === RED ? BLACK : RED,
        reason: checked ? 'Șah mat!' : 'Blocat fără mutări (la xiangqi, asta înseamnă pierdere!)'
      };
    }
    return { over:false };
  }

  /* ── RENDERER SVG ──────────────────────────────────────────────
     U = pasul grilei. Tabla: 9 puncte pe orizontală (8 celule),
     10 puncte pe verticală (9 celule). r=0 jos (roșu). */
  const U = 60, M = 46;
  const W = 8*U + 2*M, H = 9*U + 2*M;
  let FLIP = false;                       // true = negrul jos (tabla rotită 180°)
  const X = f => M + (FLIP ? (8 - f) : f) * U;
  const Y = r => M + (FLIP ? r : (9 - r)) * U;

  const SVGNS = 'http://www.w3.org/2000/svg';
  const el = (n, a) => { const e = document.createElementNS(SVGNS, n); for (const k in a) e.setAttribute(k, a[k]); return e; };

  function drawBoardBase(svg) {
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    // fundal lemn
    svg.appendChild(el('rect', { x:0, y:0, width:W, height:H, fill:'#e8d4a0' }));
    const g = el('g', { stroke:'#5a3a1c', 'stroke-width':2, fill:'none', 'stroke-linecap':'round' });
    // chenar exterior
    g.appendChild(el('rect', { x:X(0)-4, y:Y(9)-4, width:8*U+8, height:9*U+8, 'stroke-width':3.5 }));
    // orizontale (10)
    for (let r = 0; r < 10; r++) g.appendChild(el('line', { x1:X(0), y1:Y(r), x2:X(8), y2:Y(r) }));
    // verticale: continue pe margini; întrerupte de râu (r4–r5) pe coloanele 1..7
    for (let f = 0; f < 9; f++) {
      if (f === 0 || f === 8) {
        g.appendChild(el('line', { x1:X(f), y1:Y(0), x2:X(f), y2:Y(9) }));
      } else {
        g.appendChild(el('line', { x1:X(f), y1:Y(0), x2:X(f), y2:Y(4) }));
        g.appendChild(el('line', { x1:X(f), y1:Y(5), x2:X(f), y2:Y(9) }));
      }
    }
    // diagonalele palatelor
    [[3,0,5,2],[5,0,3,2],[3,7,5,9],[5,7,3,9]].forEach(([f1,r1,f2,r2]) =>
      g.appendChild(el('line', { x1:X(f1), y1:Y(r1), x2:X(f2), y2:Y(r2) })));
    svg.appendChild(g);
    // râul — text
    const t1 = el('text', { x:X(2), y:(Y(4)+Y(5))/2, fill:'#7a5320',
      'font-size':34, 'font-family':'serif', 'text-anchor':'middle', 'dominant-baseline':'middle',
      'letter-spacing':12 }); t1.textContent = '楚 河';
    const t2 = el('text', { x:X(6), y:(Y(4)+Y(5))/2, fill:'#7a5320',
      'font-size':34, 'font-family':'serif', 'text-anchor':'middle', 'dominant-baseline':'middle',
      'letter-spacing':12 }); t2.textContent = '漢 界';
    svg.appendChild(t1); svg.appendChild(t2);
  }

  // Discurile generate de user (desen + caracter), recolorate roșu/negru.
  const IMG_BUST = '?t=' + Date.now();
  function pieceGroup(f, r, pc) {
    const g = el('g', { class:'xq-pc', 'data-sq':sq(f,r) });
    const PS = U * 1.02;
    const src = 'img/xiangqi/' + pc.t + '_' + pc.c + '.png' + IMG_BUST;
    const img = el('image', { x:X(f)-PS/2, y:Y(r)-PS/2, width:PS, height:PS, href:src });
    img.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', src);
    g.appendChild(img);
    return g;
  }

  /* render(svg, pos, opts)
       opts.onPoint(f,r)  — click pe orice intersecție (piesă sau gol)
       opts.flip          — (nefolosit; roșu mereu jos)
     Marcaje: addHL(svg, "f,r", cls) cu cls din: hl-sel hl-move hl-cap hl-last hl-chk */
  function render(svg, pos, opts) {
    opts = opts || {};
    FLIP = !!opts.flip;
    svg.innerHTML = '';
    drawBoardBase(svg);
    const hlLayer = el('g', { class:'xq-hl' }); svg.appendChild(hlLayer);
    svg._hl = hlLayer;
    const pcLayer = el('g', { class:'xq-pieces' }); svg.appendChild(pcLayer);
    for (const k in pos) { const { f, r } = parse(k); pcLayer.appendChild(pieceGroup(f, r, pos[k])); }
    // strat transparent de click pe TOATE intersecțiile
    const hit = el('g', {}); svg.appendChild(hit);
    for (let f = 0; f < 9; f++) for (let r = 0; r < 10; r++) {
      const c = el('circle', { cx:X(f), cy:Y(r), r:U*0.46, fill:'transparent',
        style:'cursor:pointer', 'data-f':f, 'data-r':r });
      if (opts.onPoint) c.addEventListener('click', () => opts.onPoint(f, r));
      hit.appendChild(c);
    }
  }

  function clearHL(svg) { if (svg._hl) svg._hl.innerHTML = ''; }

  function addHL(svg, s, cls) {
    if (!svg._hl) return;
    const { f, r } = parse(s);
    if (cls === 'hl-move') {
      svg._hl.appendChild(el('circle', { cx:X(f), cy:Y(r), r:U*0.16,
        fill:'rgba(20,110,40,0.55)' }));
    } else if (cls === 'hl-cap') {
      svg._hl.appendChild(el('circle', { cx:X(f), cy:Y(r), r:U*0.46,
        fill:'none', stroke:'rgba(230,60,50,0.85)', 'stroke-width':5 }));
    } else if (cls === 'hl-sel') {
      svg._hl.appendChild(el('circle', { cx:X(f), cy:Y(r), r:U*0.47,
        fill:'rgba(26,120,255,0.20)', stroke:'rgba(26,120,255,0.8)', 'stroke-width':3 }));
    } else if (cls === 'hl-last') {
      svg._hl.appendChild(el('circle', { cx:X(f), cy:Y(r), r:U*0.47,
        fill:'rgba(20,110,40,0.30)' }));
    } else if (cls === 'hl-chk') {
      svg._hl.appendChild(el('circle', { cx:X(f), cy:Y(r), r:U*0.47,
        fill:'rgba(231,0,0,0.32)' }));
    } else if (cls === 'hl-from') {
      svg._hl.appendChild(el('circle', { cx:X(f), cy:Y(r), r:U*0.47,
        fill:'rgba(245,200,50,0.40)' }));
    } else if (cls === 'hl-to') {
      svg._hl.appendChild(el('circle', { cx:X(f), cy:Y(r), r:U*0.47,
        fill:'rgba(255,150,0,0.45)' }));
    } else if (cls === 'hl-atk') {
      svg._hl.appendChild(el('circle', { cx:X(f), cy:Y(r), r:U*0.46,
        fill:'none', stroke:'rgba(230,60,50,0.8)', 'stroke-width':5 }));
    }
  }

  return {
    COLS, ROWS, RED, BLACK, CHAR, NAME, PINYIN,
    sq, parse, startPosition, legalMoves, pseudoMoves, applyMove,
    inCheck, generalsFacing, hasAnyMove, status, findGeneral,
    inPalace, ownHalf,
    render, clearHL, addHL
  };
})();
