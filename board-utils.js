/* board-utils.js
 * Mod desen (fără mouse): ✋ = muți piesele; bulina colorată = desenezi.
 * În modul desen, o atingere scurtă colorează pătratul, iar tragerea face săgeată.
 * În modul ✋, prima atingere pe tablă șterge tot desenul.
 * Touch bridge + adnotări interactive pentru orice pagină cu chessboard.js.
 * Include după jQuery + chessboard.js: <script src="board-utils.js"></script>
 *
 * Adnotări mouse (click-dreapta):
 *   drag    → săgeată   |  nimic=verde · Shift=roșu · Ctrl=albastru · Alt=galben
 *   loc     → pătrat evidențiat (același toggle)
 *   stânga  → șterge tot
 *
 * Adnotări touch:
 *   ținut (450ms) + drag  → săgeată în culoarea aleasă
 *   ținut (450ms) pe loc  → pătrat în culoarea aleasă; din nou cu aceeași culoare → șters
 *   bara de bulinuțe deasupra tablei alege culoarea pentru deget; 🧽 șterge tot
 *
 * Touch bridge:
 *   mișcare rapidă (< 450ms)  → drag piesă normal
 */
(function () {
  'use strict';

  /* ── Culori ── */
  var COLORS = [
    { arrow: 'rgba(60,190,80,0.85)',   sq: 'rgba(60,190,80,0.42)'   },  /* verde    */
    { arrow: 'rgba(220,55,55,0.85)',   sq: 'rgba(220,55,55,0.38)'   },  /* roșu     */
    { arrow: 'rgba(50,130,210,0.85)',  sq: 'rgba(50,130,210,0.42)'  },  /* albastru */
    { arrow: 'rgba(215,165,20,0.85)',  sq: 'rgba(215,165,20,0.45)'  },  /* galben   */
  ];

  /* ── Stare partajată bridge + adnotări ── */
  var bridgeDragging = false;   /* bridge drag piese activ */
  var annMode        = false;   /* true = long-press annotation în desfășurare */

  /* ── Stare adnotări ── */
  var annArrows  = [];   /* [{from, to, ci}]  */
  var annSquares = {};   /* {sq: ci (0-3)}    */
  var rmbFrom = null, rmbCi = 0, rmbMoved = false;
  var activeCi = 0;   /* culoarea aleasă din bara de bulinuțe (verde implicit) */
  var drawMode = false;   /* true = atingerile desenează, nu mută piese */
  var drawFrom = null;
  var touchFrom = null, touchTimer = null;
  var annBoardEl = null;  /* tabla găsită la inițializare */

  /* orientarea tablei; `board` global poate lipsi sau poate fi altceva (pagini vechi) */
  function boardOrientation() {
    try {
      if (typeof board !== 'undefined' && board && typeof board.orientation === 'function') {
        return board.orientation();
      }
    } catch (e) {}
    return 'white';
  }

  /* ── SVG helpers ── */
  function fileRank(sq) {
    return { c: 'abcdefgh'.indexOf(sq[0]), r: parseInt(sq[1]) - 1 };
  }
  function sqCenter(sq, sz) {
    var fr = fileRank(sq), c = fr.c, r = fr.r;
    var ori = boardOrientation();
    if (ori === 'black') { c = 7 - c; r = 7 - r; }
    var s = sz / 8;
    return { x: c * s + s / 2, y: (7 - r) * s + s / 2 };
  }
  function getSq(el) {
    for (var i = 0; i < 8 && el; i++) {
      var s = el.getAttribute && el.getAttribute('data-square');
      if (s) return s;
      el = el.parentElement;
    }
    return null;
  }
  function getSqFromPoint(x, y) {
    var el = document.elementFromPoint(x, y);
    var sq = getSq(el);
    if (sq) return sq;
    /* piesa blochează — o ascundem temporar și re-testăm */
    if (el && el.style) {
      el.style.pointerEvents = 'none';
      sq = getSq(document.elementFromPoint(x, y));
      el.style.pointerEvents = '';
    }
    return sq;
  }

  /* ── Render SVG ── */
  function render() {
    /* containerul desenului: îl căutăm în jurul tablei, în mai multe feluri,
       pentru că paginile vechi nu au toate .board-wrapper */
    var bw = annBoardEl && annBoardEl.closest
           ? (annBoardEl.closest('.board-wrapper') || annBoardEl.closest('#boardWrapper') ||
              annBoardEl.closest('#board-wrap')   || annBoardEl.closest('.board-section'))
           : null;
    if (!bw) bw = document.getElementById('boardWrapper');
    if (!bw && annBoardEl) bw = annBoardEl.parentElement;   /* ultima soluție: părintele tablei */
    if (!bw) return;
    if (getComputedStyle(bw).position === 'static') bw.style.position = 'relative';
    var svg = bw.querySelector('.ann-svg');
    if (!svg) {
      svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'ann-svg');
      svg.style.cssText = 'position:absolute;pointer-events:none;z-index:25;';
      bw.appendChild(svg);
    }
    while (svg.firstChild) svg.removeChild(svg.firstChild);

    /* Aliniază SVG citind direct din DOM poziția pătrățelului din colțul stânga-sus */
    var ori = boardOrientation();
    var tlName = ori === 'white' ? 'a8' : 'h1';
    var tlSq   = bw.querySelector('[data-square="' + tlName + '"]');
    var sqSz, svgX = 0, svgY = 0;
    if (tlSq) {
      sqSz = tlSq.offsetWidth;
      var bwRect = bw.getBoundingClientRect();
      var tlRect = tlSq.getBoundingClientRect();
      svgX = Math.round(tlRect.left - bwRect.left);
      svgY = Math.round(tlRect.top  - bwRect.top);
    } else {
      sqSz = bw.offsetWidth / 8;
    }
    var sz = sqSz * 8;
    svg.style.left   = svgX + 'px';
    svg.style.top    = svgY + 'px';
    svg.style.width  = sz   + 'px';
    svg.style.height = sz   + 'px';

    var NS = 'http://www.w3.org/2000/svg';
    var defs = document.createElementNS(NS, 'defs');
    svg.appendChild(defs);

    /* pătrate evidențiate */
    Object.keys(annSquares).forEach(function (sq) {
      var ci = annSquares[sq];
      var fr = fileRank(sq), c = fr.c, r = fr.r;
      var ori = boardOrientation();
      if (ori === 'black') { c = 7 - c; r = 7 - r; }
      var rect = document.createElementNS(NS, 'rect');
      rect.setAttribute('x', c * sqSz);
      rect.setAttribute('y', (7 - r) * sqSz);
      rect.setAttribute('width',  sqSz);
      rect.setAttribute('height', sqSz);
      rect.setAttribute('fill', COLORS[ci].sq);
      svg.appendChild(rect);
    });

    /* săgeți — pornesc din centrul pătratului sursă,
       vârful ajunge exact în centrul pătratului destinație */
    var SW = Math.max(3, sqSz * 0.09);   /* proporțional cu tabla; vârful e la SW px după endpoint */
    annArrows.forEach(function (arr, i) {
      var col = COLORS[arr.ci || 0].arrow;
      var mid = 'ann' + i;
      var mk = document.createElementNS(NS, 'marker');
      mk.setAttribute('id', mid);
      mk.setAttribute('markerWidth', '4'); mk.setAttribute('markerHeight', '4');
      mk.setAttribute('refX', '3.5');      mk.setAttribute('refY', '2');
      mk.setAttribute('orient', 'auto');
      var mp = document.createElementNS(NS, 'path');
      mp.setAttribute('d', 'M0,0 L4,2 L0,4 L1,2 Z');
      mp.setAttribute('fill', col);
      mk.appendChild(mp); defs.appendChild(mk);

      var f = sqCenter(arr.from, sz), t = sqCenter(arr.to, sz);
      var dx = t.x - f.x, dy = t.y - f.y;
      var len = Math.sqrt(dx * dx + dy * dy);
      if (len < 1) return;
      var ux = dx / len, uy = dy / len;
      /* x1,y1 = centrul pătratului sursă;
         x2,y2 = centrul destinație retras cu SW px → vârful săgeții aterizează exact pe centru */
      var x1 = f.x,          y1 = f.y;
      var x2 = t.x - ux * SW, y2 = t.y - uy * SW;
      var ln = document.createElementNS(NS, 'line');
      ln.setAttribute('x1', x1); ln.setAttribute('y1', y1);
      ln.setAttribute('x2', x2); ln.setAttribute('y2', y2);
      ln.setAttribute('stroke', col);
      ln.setAttribute('stroke-width', String(SW));
      ln.setAttribute('stroke-linecap', 'round');
      ln.setAttribute('marker-end', 'url(#' + mid + ')');
      svg.appendChild(ln);
    });
  }

  function clearAll() { annArrows = []; annSquares = {}; render(); }
  window._annClear  = clearAll;
  window._annRender = render;
  window._annSet    = function(arrows) { annArrows = arrows || []; annSquares = {}; render(); };

  /* ── Helpers bridge ── */
  function colorIdx(e) {
    return e.altKey ? 3 : e.ctrlKey ? 2 : e.shiftKey ? 1 : activeCi;
  }
  var fromTouch = false;   /* true cât timp trimitem un eveniment de mouse creat dintr-o atingere */
  function toMouse(type, coords, target) {
    fromTouch = true;
    try {
    target.dispatchEvent(new MouseEvent(type, {
      bubbles: true, cancelable: true, view: window,
      button: 0, buttons: (type === 'mouseup' ? 0 : 1),
      clientX: coords.clientX, clientY: coords.clientY,
      screenX: coords.screenX, screenY: coords.screenY
    }));
    } finally { fromTouch = false; }
  }
  function cancelBridgeDrag() {
    if (bridgeDragging) {
      bridgeDragging = false;
      document.body.dispatchEvent(new MouseEvent('mouseup', {
        bubbles: true, cancelable: true, button: 0, buttons: 0
      }));
    }
  }

  /* ── Bara de culori: bulinuțe + gumă (pentru desenat cu degetul) ── */
  var NAMES = ['verde', 'roșu', 'albastru', 'galben'];
  function annBarCss() {
    if (document.getElementById('ann-bar-css')) return;
    var st = document.createElement('style');
    st.id = 'ann-bar-css';
    st.textContent =
      /* bara stă în antet, ca să NU ia din înălțimea tablei */
      '.ann-bar{display:flex;gap:6px;align-items:center;grid-column:1;justify-self:start;}' +
      '.ann-bar.ann-fixed{position:fixed;left:8px;bottom:8px;z-index:60;padding:6px 8px;' +
      'border-radius:24px;background:rgba(255,255,255,.75);box-shadow:0 2px 8px rgba(0,0,0,.25);}' +
      '.ann-dot{width:30px;height:30px;border-radius:50%;border:2px solid rgba(255,255,255,.9);cursor:pointer;' +
      'padding:0;box-shadow:0 1px 4px rgba(0,0,0,.25);transition:transform .15s,box-shadow .15s;}' +
      '.ann-dot:hover{transform:translateY(-1px);}' +
      '.ann-dot.on{border-color:#1a3a6b;box-shadow:0 0 0 3px rgba(26,58,107,.40);transform:translateY(-1px);}' +
      '.ann-erase{width:32px;height:30px;border-radius:15px;padding:0;cursor:pointer;line-height:1;' +
      'border:2px solid rgba(255,255,255,.9);background:rgba(255,255,255,.7);font-size:.95rem;' +
      'box-shadow:0 1px 4px rgba(0,0,0,.2);}' +
      '.ann-erase:hover{background:rgba(255,255,255,.95);}' +
      '.ann-hand{width:34px;height:30px;border-radius:15px;padding:0;cursor:pointer;line-height:1;' +
      'border:2px solid rgba(255,255,255,.9);background:rgba(255,255,255,.7);font-size:.95rem;' +
      'box-shadow:0 1px 4px rgba(0,0,0,.2);margin-right:2px;}' +
      '.ann-hand.on{background:#1a3a6b;border-color:#1a3a6b;}' +
      '@media (max-width:560px){.ann-dot{width:26px;height:26px;}.ann-erase{width:28px;height:26px;}}';
    document.head.appendChild(st);
  }
  function buildAnnBar(boardEl) {
    if (document.querySelector('.ann-bar')) return;
    annBarCss();
    var bar = document.createElement('div');
    bar.className = 'ann-bar';
    bar.setAttribute('role', 'toolbar');
    bar.setAttribute('aria-label', 'Culori pentru evidențiere');
    var hand = document.createElement('button');
    hand.type = 'button';
    hand.className = 'ann-hand on';
    hand.textContent = '✋';
    hand.title = 'Mută piesele';
    hand.setAttribute('aria-label', 'Mută piesele');
    bar.appendChild(hand);

    function refresh() {
      hand.classList.toggle('on', !drawMode);
      bar.querySelectorAll('.ann-dot').forEach(function (d, j) {
        d.classList.toggle('on', drawMode && j === activeCi);
      });
    }
    hand.addEventListener('click', function () { drawMode = false; drawFrom = null; refresh(); });

    COLORS.forEach(function (c, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'ann-dot';
      b.style.background = c.arrow;
      b.title = 'Desenează cu ' + NAMES[i];
      b.setAttribute('aria-label', 'Desenează cu ' + NAMES[i]);
      b.addEventListener('click', function () {
        /* aceeași culoare apăsată din nou = ieși din modul desen */
        if (drawMode && activeCi === i) drawMode = false;
        else { drawMode = true; activeCi = i; }
        drawFrom = null;
        refresh();
      });
      bar.appendChild(b);
    });
    var er = document.createElement('button');
    er.type = 'button';
    er.className = 'ann-erase';
    er.textContent = '🧽';
    er.setAttribute('aria-label', 'Șterge toate pătratele și săgețile');
    er.title = 'Șterge toate pătratele și săgețile';
    er.addEventListener('click', function () { clearAll(); });
    bar.appendChild(er);
    var header = document.querySelector('.page-header') || document.querySelector('#nav') || document.querySelector('header');
    if (header) header.insertBefore(bar, header.firstChild);
    else { bar.classList.add('ann-fixed'); document.body.appendChild(bar); }
  }

  /* ── Init (DOMContentLoaded) ── */
  document.addEventListener('DOMContentLoaded', function () {
    /* tabla are de obicei id=board; unele jocuri (myBoard, mcBoard) o pun direct în #boardWrapper */
    var boardEl = document.getElementById('board') || document.querySelector('#boardWrapper > div');
    if (!boardEl) return;
    annBoardEl = boardEl;
    buildAnnBar(boardEl);

    /* ════ TOUCH BRIDGE ════ */
    boardEl.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1 || annMode || drawMode) { if (drawMode) e.preventDefault(); return; }
      bridgeDragging = true;
      var t = e.touches[0];
      var el = document.elementFromPoint(t.clientX, t.clientY) || e.target;
      toMouse('mousedown', t, el);
      e.preventDefault();
    }, { passive: false });

    document.addEventListener('touchmove', function (e) {
      if (drawMode) return;
      if (!bridgeDragging || annMode || e.touches.length !== 1) return;
      var t = e.touches[0];
      toMouse('mousemove', t, document.body);
      e.preventDefault();
    }, { passive: false });

    document.addEventListener('touchend', function (e) {
      if (!bridgeDragging || annMode) return;
      bridgeDragging = false;
      var t = e.changedTouches[0];
      toMouse('mousemove', t, document.body);
      toMouse('mouseup',   t, document.body);
    });

    document.addEventListener('touchcancel', function () {
      if (!bridgeDragging) return;
      bridgeDragging = false;
      document.body.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
    });

    /* ════ MOD DESEN (deget, creion sau mouse) ════
       O atingere scurtă colorează pătratul; tragerea desenează săgeată.
       Merge la fel pe Android, pe tabla interactivă și cu mouse-ul. */
    boardEl.addEventListener('pointerdown', function (e) {
      if (!drawMode) {
        /* modul ✋: o atingere pe tablă șterge desenul, ca un click stânga cu mouse-ul */
        if (annArrows.length || Object.keys(annSquares).length) clearAll();
        return;
      }
      e.preventDefault(); e.stopPropagation();
      drawFrom = getSqFromPoint(e.clientX, e.clientY) || getSq(e.target);
    }, true);
    boardEl.addEventListener('pointermove', function (e) {
      if (drawMode) e.preventDefault();
    }, { capture: true, passive: false });
    boardEl.addEventListener('pointerup', function (e) {
      if (!drawMode) return;
      e.preventDefault(); e.stopPropagation();
      var to = getSqFromPoint(e.clientX, e.clientY) || getSq(e.target) || drawFrom;
      if (drawFrom && to) {
        if (drawFrom === to) {
          if (annSquares[to] === activeCi) delete annSquares[to];
          else annSquares[to] = activeCi;
        } else {
          var k = annArrows.findIndex(function (a) { return a.from === drawFrom && a.to === to; });
          if (k >= 0) annArrows.splice(k, 1);
          else annArrows.push({ from: drawFrom, to: to, ci: activeCi });
        }
        render();
      }
      drawFrom = null;
    }, true);
    boardEl.addEventListener('pointercancel', function () { drawFrom = null; }, true);

    /* ════ ADNOTĂRI MOUSE (click-dreapta) ════
       Capture phase la nivel document: rulăm ÎNAINTE de orice listener chessboard.js */
    document.addEventListener('mousedown', function (e) {
      if (e.button !== 2) return;
      if (!boardEl.contains(e.target)) return;
      e.preventDefault();
      e.stopImmediatePropagation();   /* oprim chessboard.js să apuce piesa */
      rmbFrom  = getSqFromPoint(e.clientX, e.clientY);
      rmbCi    = colorIdx(e);
      rmbMoved = false;
    }, true);
    boardEl.addEventListener('mousemove', function () {
      if (rmbFrom) rmbMoved = true;
    });
    boardEl.addEventListener('mouseup', function (e) {
      if (e.button !== 2) return;
      e.preventDefault();
      var to = getSqFromPoint(e.clientX, e.clientY);
      if (!rmbFrom || !to) { rmbFrom = null; return; }
      if (!rmbMoved || rmbFrom === to) {
        if (annSquares[to] === rmbCi) delete annSquares[to];
        else annSquares[to] = rmbCi;
      } else {
        var idx = annArrows.findIndex(function (a) { return a.from === rmbFrom && a.to === to; });
        if (idx >= 0) annArrows.splice(idx, 1);
        else annArrows.push({ from: rmbFrom, to: to, ci: rmbCi });
      }
      rmbFrom = null;
      render();
    });
    boardEl.addEventListener('contextmenu', function (e) { e.preventDefault(); });
    /* click stânga cu mouse-ul șterge adnotările; atingerile cu degetul NU le șterg
       (pe ecran tactil se șterg apăsând lung pe pătrat până trece de galben, sau refăcând aceeași săgeată) */
    boardEl.addEventListener('mousedown',   function (e) { if (e.button === 0 && !drawMode) clearAll(); });

    /* ════ ADNOTĂRI TOUCH (long-press 450ms + drag) ════ */
    boardEl.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1 || drawMode) return;
      var t = e.touches[0];
      touchFrom = getSq(e.target) || getSqFromPoint(t.clientX, t.clientY);
      touchTimer = setTimeout(function () {
        if (!touchFrom) return;
        annMode = true;
        cancelBridgeDrag();   /* piesa snap-back, intrăm în mod adnotare */
      }, 450);
    }, { passive: true });

    boardEl.addEventListener('touchmove', function (e) {
      /* mișcare înainte de 450ms = drag piesă → anulăm adnotarea */
      if (!annMode) {
        clearTimeout(touchTimer);
        touchFrom = null;
      }
    }, { passive: true });

    boardEl.addEventListener('touchend', function (e) {
      clearTimeout(touchTimer);
      if (!annMode) { touchFrom = null; return; }
      annMode = false;
      var t  = e.changedTouches[0];
      /* pe unele ecrane elementFromPoint nu dă pătratul (piesă, overlay, tabla redimensionată):
         cădem pe elementul atins, iar la urmă pe pătratul de pornire */
      var to = getSqFromPoint(t.clientX, t.clientY) || getSq(e.target) || getSq(t.target) || touchFrom;
      if (touchFrom && to) {
        if (touchFrom === to) {
          /* pătrat: apasă lung o dată = colorează, încă o dată cu aceeași culoare = șterge */
          if (annSquares[to] === activeCi) delete annSquares[to];
          else annSquares[to] = activeCi;
        } else {
          /* toggle săgeată verde */
          var idx = annArrows.findIndex(function (a) { return a.from === touchFrom && a.to === to; });
          if (idx >= 0) annArrows.splice(idx, 1);
          else annArrows.push({ from: touchFrom, to: to, ci: activeCi });
        }
        render();
      }
      touchFrom = null;
    }, { passive: true });

    boardEl.addEventListener('touchcancel', function () {
      clearTimeout(touchTimer);
      annMode   = false;
      touchFrom = null;
    }, { passive: true });
  });

  /* ── Move feedback badge: cerculeț ✓/✗ pe pătratul destinație ── */
  window._moveFeedback = function (square, type) {
    var el = document.querySelector('.square-' + square);
    if (!el) return;
    var prev = el.querySelector('.move-feedback');
    if (prev) prev.remove();
    var badge = document.createElement('div');
    badge.className = 'move-feedback ' + type;
    badge.textContent = type === 'ok' ? '✓' : '✗';
    el.appendChild(badge);
  };
}());
