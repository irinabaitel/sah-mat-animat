/* board-utils.js
 * Touch bridge + adnotări interactive pentru orice pagină cu chessboard.js.
 * Include după jQuery + chessboard.js: <script src="board-utils.js"></script>
 *
 * Adnotări mouse (click-dreapta):
 *   drag    → săgeată   |  nimic=verde · Shift=roșu · Ctrl=albastru · Alt=galben
 *   loc     → pătrat evidențiat (același toggle)
 *   stânga  → șterge tot
 *
 * Adnotări touch:
 *   ținut (450ms) + drag  → săgeată verde
 *   ținut (450ms) pe loc  → toggle pătrat verde
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
  var touchFrom = null, touchTimer = null;

  /* ── SVG helpers ── */
  function fileRank(sq) {
    return { c: 'abcdefgh'.indexOf(sq[0]), r: parseInt(sq[1]) - 1 };
  }
  function sqCenter(sq, sz) {
    var fr = fileRank(sq), c = fr.c, r = fr.r;
    var ori = (typeof board !== 'undefined' && board) ? board.orientation() : 'white';
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
    return getSq(document.elementFromPoint(x, y));
  }

  /* ── Render SVG ── */
  function render() {
    var bw = document.getElementById('boardWrapper');
    if (!bw) return;
    var svg = bw.querySelector('.ann-svg');
    if (!svg) {
      svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'ann-svg');
      svg.style.cssText = 'position:absolute;pointer-events:none;z-index:25;';
      bw.appendChild(svg);
    }
    while (svg.firstChild) svg.removeChild(svg.firstChild);

    /* Aliniază SVG citind direct din DOM poziția pătrățelului din colțul stânga-sus */
    var ori = (typeof board !== 'undefined' && board) ? board.orientation() : 'white';
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
      var ori = (typeof board !== 'undefined' && board) ? board.orientation() : 'white';
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
    var SW = 5;   /* stroke-width; cu markerUnits=strokeWidth, vârful e la SW px după endpoint */
    annArrows.forEach(function (arr, i) {
      var col = COLORS[arr.ci || 0].arrow;
      var mid = 'ann' + i;
      var mk = document.createElementNS(NS, 'marker');
      mk.setAttribute('id', mid);
      mk.setAttribute('markerWidth', '10'); mk.setAttribute('markerHeight', '7');
      mk.setAttribute('refX', '8');         mk.setAttribute('refY', '3.5');
      mk.setAttribute('orient', 'auto');
      var mp = document.createElementNS(NS, 'path');
      mp.setAttribute('d', 'M0,0 L9,3.5 L0,7 L2.5,3.5 Z');
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

  /* ── Helpers bridge ── */
  function colorIdx(e) {
    return e.altKey ? 3 : e.ctrlKey ? 2 : e.shiftKey ? 1 : 0;
  }
  function toMouse(type, coords, target) {
    target.dispatchEvent(new MouseEvent(type, {
      bubbles: true, cancelable: true, view: window,
      button: 0, buttons: (type === 'mouseup' ? 0 : 1),
      clientX: coords.clientX, clientY: coords.clientY,
      screenX: coords.screenX, screenY: coords.screenY
    }));
  }
  function cancelBridgeDrag() {
    if (bridgeDragging) {
      bridgeDragging = false;
      document.body.dispatchEvent(new MouseEvent('mouseup', {
        bubbles: true, cancelable: true, button: 0, buttons: 0
      }));
    }
  }

  /* ── Init (DOMContentLoaded) ── */
  document.addEventListener('DOMContentLoaded', function () {
    var boardEl = document.getElementById('board');
    if (!boardEl) return;

    /* ════ TOUCH BRIDGE ════ */
    boardEl.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1 || annMode) return;
      bridgeDragging = true;
      var t = e.touches[0];
      var el = document.elementFromPoint(t.clientX, t.clientY) || e.target;
      toMouse('mousedown', t, el);
      e.preventDefault();
    }, { passive: false });

    document.addEventListener('touchmove', function (e) {
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

    /* ════ ADNOTĂRI MOUSE (click-dreapta) ════ */
    boardEl.addEventListener('mousedown', function (e) {
      if (e.button !== 2) return;
      e.preventDefault();
      rmbFrom  = getSq(e.target);
      rmbCi    = colorIdx(e);
      rmbMoved = false;
    });
    boardEl.addEventListener('mousemove', function () {
      if (rmbFrom) rmbMoved = true;
    });
    boardEl.addEventListener('mouseup', function (e) {
      if (e.button !== 2) return;
      e.preventDefault();
      var to = getSq(e.target);
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
    boardEl.addEventListener('mousedown',   function (e) { if (e.button === 0) clearAll(); });

    /* ════ ADNOTĂRI TOUCH (long-press 450ms + drag) ════ */
    boardEl.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1) return;
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
      var to = getSqFromPoint(t.clientX, t.clientY);
      if (touchFrom && to) {
        if (touchFrom === to) {
          /* toggle pătrat verde */
          if (annSquares[to] !== undefined) delete annSquares[to];
          else annSquares[to] = 0;
        } else {
          /* toggle săgeată verde */
          var idx = annArrows.findIndex(function (a) { return a.from === touchFrom && a.to === to; });
          if (idx >= 0) annArrows.splice(idx, 1);
          else annArrows.push({ from: touchFrom, to: to, ci: 0 });
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
