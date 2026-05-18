/* ============================================================
   coach.js — „Modul Antrenor" pentru arenele de șah
   (practica2.html = vs robot, arena_2jucatori.html = 2 copii)

   Inspirat de ChessUp 2: când ridici o piesă, pătratele unde poate
   ajunge se colorează după cât de bună e mutarea, LIVE, în timpul
   partidei. Are propriul Stockfish de ANALIZĂ (separat de robotul de
   joc), ca să nu se încurce între ele.

   Culori cu înțeles FIX (nivelul schimbă doar cât de sever e):
     🟡 .coach-best  — cea mai bună mutare
     🟢 .coach-good  — mutare bună
     🔴 .coach-bad   — mutare slabă / gafă
     🔵 .coach-brill — briliantă (cea mai bună + sacrificiu corect)
     ⚪ .coach-any   — la nivelul 1: doar arată mutările posibile

   Folosește variabila globală `chess` (chess.js) deja existentă în
   ambele pagini, și clasele .square-XX ale chessboard.js.
   ============================================================ */
(function () {
  'use strict';

  var VAL = { p:1, n:3, b:3, r:5, q:9, k:0 };

  /* Niveluri 1–5: praguri în centipioni + adâncime motor + MultiPV.
     Culorile au mereu același înțeles; nivelul schimbă severitatea. */
  var LV = {
    1: { label:'Explorare',  engine:false },
    2: { label:'Începător',  engine:true, movetime:150,  multipv:6,  best:20, good:150, brill:false },
    3: { label:'Mediu',      engine:true, movetime:300,  multipv:8,  best:15, good:90,  brill:false },
    4: { label:'Avansat',    engine:true, movetime:600,  multipv:10, best:12, good:55,  brill:true  },
    5: { label:'Maestru',    engine:true, movetime:1000, multipv:12, best:10, good:35,  brill:true  }
  };

  var Coach = {
    enabled: false,
    level: 3,
    _sf: null,
    _ready: false,
    _cache: {},          // fen -> { best:cp, moves:{uci:cp} }
    _cur: null,          // analiza care rulează acum: { fen, lines, cbs }
    _queued: null,       // următoarea poziție de analizat (păstrăm doar ultima)
    _token: 0            // ca să ignorăm rezultate vechi (poziția s-a schimbat)
  };

  /* ─── CSS injectat o singură dată (overlay, nu acoperă chessboard.js) ─── */
  /* Marcaje DOAR pe colțuri — glow rotunjit cu gradient (radial), fără
     muchii dure. La fel pe pătrate goale sau cu piesă. Folosim
     background-image ca să NU acoperim culoarea pusă de chessboard.js. */
  /* Colțuri RACORDATE: un chenar rotunjit (border-radius) din care
     ascundem mijlocul fiecărei laturi cu o mască → rămân doar cele 4
     colțuri, cu cotul rotund care leagă cele două laturi. Subțire,
     margini blânde (drop-shadow). ::after = nu acoperă piesa/culoarea. */
  function corners(sel, rgb, bw, rad, arm) {
    var col = 'rgba(' + rgb + ',1)';
    var m = 'linear-gradient(#000 0 0) top/100% ' + arm + ' no-repeat,' +
            'linear-gradient(#000 0 0) bottom/100% ' + arm + ' no-repeat,' +
            'linear-gradient(#000 0 0) left/' + arm + ' 100% no-repeat,' +
            'linear-gradient(#000 0 0) right/' + arm + ' 100% no-repeat';
    return sel + '{position:relative!important;}' +
      sel + '::after{content:"";position:absolute;top:7%;left:7%;right:7%;bottom:7%;' +
      'border:' + bw + ' solid ' + col + ';border-radius:24%;box-sizing:border-box;' +
      'pointer-events:none;-webkit-mask:' + m + ';mask:' + m + ';' +
      'filter:drop-shadow(0 0 1px ' + col + ');}';
  }

  function injectCSS() {
    if (document.getElementById('coach-css')) return;
    var s = document.createElement('style');
    s.id = 'coach-css';
    s.textContent = [
      corners('.coach-any',   '120,120,140', '3px', '24%', '30%'),
      corners('.coach-good',  '46,170,80',   '4px', '24%', '32%'),
      corners('.coach-best',  '240,190,20',  '5px', '28%', '40%'),
      corners('.coach-bad',   '225,55,45',   '4px', '24%', '32%'),
      corners('.coach-brill', '40,140,255',  '5px', '28%', '40%'),
      /* bara de control */
      '.coach-bar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:6px;}',
      '.coach-toggle{display:inline-flex;align-items:center;gap:6px;padding:7px 12px;border-radius:50px;border:2px solid rgba(26,58,107,.3);background:rgba(255,255,255,.5);color:var(--c-navy,#1a3a6b);font-family:var(--font-display,inherit);font-weight:700;font-size:.85em;cursor:pointer;transition:all .15s;white-space:nowrap;}',
      '.coach-toggle.on{background:#2eaa50;color:#fff;border-color:#2eaa50;}',
      '.coach-levels{display:flex;gap:4px;align-items:center;}',
      '.coach-levels[hidden]{display:none;}',
      '.coach-lv{width:24px;height:24px;border-radius:6px;border:1px solid rgba(26,58,107,.3);background:rgba(255,255,255,.5);color:rgba(26,58,107,.7);font-family:var(--font-display,inherit);font-weight:700;font-size:11px;cursor:pointer;}',
      '.coach-lv.active{background:var(--c-navy,#1a3a6b);color:#fff;border-color:var(--c-navy,#1a3a6b);}',
      '.coach-lv-label{font-family:var(--font-display,inherit);font-weight:700;font-size:.78em;color:var(--c-navy,#1a3a6b);opacity:.8;}'
    ].join('\n');
    document.head.appendChild(s);
  }

  /* ─── Stockfish de analiză (propriu, separat de robotul de joc) ─── */
  function startEngine() {
    if (Coach._sf) return;
    try {
      var code = "importScripts('https://cdnjs.cloudflare.com/ajax/libs/stockfish.js/10.0.2/stockfish.js')";
      Coach._sf = new Worker(URL.createObjectURL(new Blob([code], { type:'application/javascript' })));
    } catch (e) {
      try { Coach._sf = new Worker('stockfish.js'); } catch (e2) { Coach._sf = null; }
    }
    if (!Coach._sf) return;
    Coach._sf.onmessage = function (ev) {
      var msg = ev.data;
      if (typeof msg !== 'string') return;
      if (msg === 'uciok') { Coach._sf.postMessage('isready'); return; }
      if (msg === 'readyok') { Coach._ready = true; return; }
      if (!Coach._cur) return;
      if (msg.indexOf('info ') === 0 && msg.indexOf(' multipv ') !== -1 && msg.indexOf(' pv ') !== -1) {
        var mpv = parseInt((msg.match(/ multipv (\d+)/) || [])[1], 10);
        var sc, mm;
        if ((mm = msg.match(/ score mate (-?\d+)/))) {
          var n = parseInt(mm[1], 10);
          sc = n > 0 ? (100000 - n * 100) : (-100000 - n * 100);
        } else if ((mm = msg.match(/ score cp (-?\d+)/))) {
          sc = parseInt(mm[1], 10);
        } else return;
        var pv = (msg.match(/ pv ([a-h][1-8][a-h][1-8][qrbn]?)/) || [])[1];
        if (!pv || isNaN(mpv)) return;
        Coach._cur.lines[mpv] = { uci: pv, cp: sc };
      } else if (msg.indexOf('bestmove') === 0) {
        var p = Coach._cur; Coach._cur = null;
        var moves = {}, best = -1e9;
        for (var k in p.lines) {
          var ln = p.lines[k];
          moves[ln.uci] = ln.cp;
          if (ln.cp > best) best = ln.cp;
        }
        var res = { best: best, moves: moves };
        Coach._cache[p.fen] = res;
        p.cbs.forEach(function (cb) { try { cb(res); } catch (e) {} });
        if (Coach._queued) {                       // pornește următoarea în coadă
          var q = Coach._queued; Coach._queued = null;
          if (Coach._cache[q.fen]) {
            var r2 = Coach._cache[q.fen];
            q.cbs.forEach(function (cb) { try { cb(r2); } catch (e) {} });
          } else {
            Coach._cur = { fen: q.fen, lines: {}, cbs: q.cbs };
            sendGo(q.fen);
          }
        }
      }
    };
    Coach._sf.postMessage('uci');
  }

  function sendGo(fen) {
    var cfg = LV[Coach.level], tries = 0;
    (function ask() {
      if (!Coach._sf || !Coach._cur || Coach._cur.fen !== fen) return;
      if (!Coach._ready) { if (tries++ < 30) setTimeout(ask, 200); return; }
      Coach._sf.postMessage('setoption name MultiPV value ' + cfg.multipv);
      Coach._sf.postMessage('position fen ' + fen);
      Coach._sf.postMessage('go movetime ' + cfg.movetime);
    })();
  }

  /* Serializăm analizele: o singură căutare odată, ca info/bestmove să
     corespundă mereu poziției corecte. Păstrăm doar ultima poziție în coadă. */
  function analyze(fen, cb) {
    if (Coach._cache[fen]) { cb(Coach._cache[fen]); return; }
    startEngine();
    if (!Coach._sf) return;
    if (Coach._cur && Coach._cur.fen === fen) { Coach._cur.cbs.push(cb); return; }
    if (Coach._queued && Coach._queued.fen === fen) { Coach._queued.cbs.push(cb); return; }
    if (Coach._cur) { Coach._queued = { fen: fen, cbs: [cb] }; return; }
    Coach._cur = { fen: fen, lines: {}, cbs: [cb] };
    sendGo(fen);
  }

  /* ─── Heuristică „briliantă" (aproximativă, cum am promis) ───
     mutare de top + lasă material (≥ o piesă minoră) ce poate fi
     luat fără recuperare egală = sacrificiu corect. */
  function isSacrifice(fenBefore, m) {
    try {
      var t = new Chess(fenBefore);
      var mv = t.move({ from: m.from, to: m.to, promotion: m.promotion || 'q' });
      if (!mv) return false;
      var movedVal = VAL[mv.piece] || 0;
      var caps = t.moves({ verbose: true }).filter(function (x) {
        return x.flags.indexOf('c') !== -1 || x.flags.indexOf('e') !== -1;
      });
      for (var i = 0; i < caps.length; i++) {
        var c = caps[i];
        var gain = VAL[c.captured] || 0;
        if (c.to !== m.to) { if (gain >= 3) { /* lasă altă piesă grea în priză */ } else continue; }
        // poate recaptura adversarul fiind apoi luat la rândul lui?
        var t2 = new Chess(t.fen());
        t2.move({ from: c.from, to: c.to, promotion: 'q' });
        var recap = t2.moves({ verbose: true }).some(function (x) {
          return x.to === c.to && (x.flags.indexOf('c') !== -1);
        });
        var recapVal = recap ? (VAL[c.piece] || 0) : 0;
        if (gain - recapVal >= 3) return true;
      }
    } catch (e) {}
    return false;
  }

  /* ─── Colorează pătratele unde poate ajunge piesa ridicată ─── */
  function clearSquares() {
    Coach._token++;   // invalidează orice analiză în curs (drag anulat etc.)
    document.querySelectorAll(
      '.coach-any,.coach-good,.coach-best,.coach-bad,.coach-brill'
    ).forEach(function (el) {
      el.classList.remove('coach-any','coach-good','coach-best','coach-bad','coach-brill');
    });
  }
  Coach.clear = clearSquares;

  function mark(sq, cls) {
    var el = document.querySelector('.square-' + sq);
    if (el) el.classList.add(cls);
  }

  Coach.show = function (square) {
    if (!Coach.enabled) return;
    if (typeof Chess === 'undefined' || !window.chess) return;
    clearSquares();
    var moves;
    try { moves = window.chess.moves({ square: square, verbose: true }); } catch (e) { return; }
    if (!moves || !moves.length) return;
    var cfg = LV[Coach.level];

    /* Nivel 1: doar arată mutările posibile, fără judecată */
    if (!cfg.engine) {
      moves.forEach(function (m) { mark(m.to, 'coach-any'); });
      return;
    }

    var fen = window.chess.fen();
    var myToken = ++Coach._token;
    analyze(fen, function (res) {
      if (myToken !== Coach._token) return;          // poziția s-a schimbat
      if (window.chess.fen() !== fen) return;        // siguranță în plus
      var worst = res.best;
      for (var u in res.moves) if (res.moves[u] < worst) worst = res.moves[u];
      moves.forEach(function (m) {
        var uci = m.from + m.to + (m.promotion || '');
        var cp = (uci in res.moves) ? res.moves[uci]
                                    : (worst - 60);  // în afara top-MultiPV = slabă
        var loss = res.best - cp;
        var cls;
        if (loss <= cfg.best) {
          cls = (cfg.brill && isSacrifice(fen, m)) ? 'coach-brill' : 'coach-best';
        } else if (loss <= cfg.good) {
          cls = 'coach-good';
        } else {
          cls = 'coach-bad';
        }
        mark(m.to, cls);
      });
    });
  };

  /* ─── Pre-analiză: cheamă la fiecare schimbare de rând, ca la
     ridicarea piesei culorile să fie deja gata (instant din cache) ─── */
  Coach.prime = function () {
    if (!Coach.enabled) return;
    if (typeof Chess === 'undefined' || !window.chess) return;
    if (!LV[Coach.level].engine) return;
    try { analyze(window.chess.fen(), function () {}); } catch (e) {}
  };

  /* ─── Bara de control: buton on/off + niveluri 1–5 ─── */
  Coach.mount = function (containerSel) {
    injectCSS();
    var host = (typeof containerSel === 'string')
      ? document.querySelector(containerSel) : containerSel;
    if (!host) return;
    var bar = document.createElement('div');
    bar.className = 'coach-bar';

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'coach-toggle';
    btn.innerHTML = '🎓 Antrenor: <span>oprit</span>';

    var levels = document.createElement('div');
    levels.className = 'coach-levels';
    levels.hidden = true;
    var lab = document.createElement('span');
    lab.className = 'coach-lv-label';
    for (var i = 1; i <= 5; i++) (function (n) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'coach-lv' + (n === Coach.level ? ' active' : '');
      b.textContent = n;
      b.title = LV[n].label;
      b.onclick = function () {
        Coach.level = n;
        Coach._cache = {};                 // praguri noi → reanalizăm
        levels.querySelectorAll('.coach-lv').forEach(function (x, idx) {
          x.classList.toggle('active', idx + 1 === n);
        });
        lab.textContent = n + ' · ' + LV[n].label;
      };
      levels.appendChild(b);
    })(i);
    levels.appendChild(lab);
    lab.textContent = Coach.level + ' · ' + LV[Coach.level].label;

    btn.onclick = function () {
      Coach.enabled = !Coach.enabled;
      btn.classList.toggle('on', Coach.enabled);
      btn.querySelector('span').textContent = Coach.enabled ? 'pornit' : 'oprit';
      levels.hidden = !Coach.enabled;
      if (Coach.enabled) { startEngine(); Coach.prime(); } else clearSquares();
    };

    bar.appendChild(btn);
    bar.appendChild(levels);
    host.appendChild(bar);
  };

  window.Coach = Coach;
})();
