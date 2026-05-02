/* arena_touch.js — click-to-move + last-move highlight for all arena pages
 * Loaded after chessboard.js + the page's own game script.
 * Relies on globals: chess (Chess.js), board (Chessboard), onDrop, onDragStart
 */
(function () {
    'use strict';

    /* ── CSS ── */
    var style = document.createElement('style');
    style.textContent = [
        '#board { touch-action: none; -webkit-user-select: none; user-select: none; }',
        '#board * { touch-action: none; }',
        '.arena-last-from { background: rgba(90,190,90,0.38) !important; }',
        '.arena-last-to   { background: rgba(50,170,50,0.55)  !important; }',
        '.arena-sel       { background: rgba(50,160,50,0.50)  !important;' +
                           ' box-shadow: inset 0 0 0 3px #27ae60; }'
    ].join('\n');
    document.head.appendChild(style);

    /* ── helpers ── */
    function clearClass(cls) {
        document.querySelectorAll('#board .' + cls)
            .forEach(function (el) { el.classList.remove(cls); });
    }
    function addCls(sq, cls) {
        var el = document.querySelector('#board .square-' + sq);
        if (el) el.classList.add(cls);
    }
    function clearHighlights() {
        clearClass('arena-last-from');
        clearClass('arena-last-to');
    }
    function showLastMove() {
        clearHighlights();
        if (typeof chess === 'undefined') return;
        var hist = chess.history({ verbose: true });
        if (!hist.length) return;
        var last = hist[hist.length - 1];
        addCls(last.from, 'arena-last-from');
        addCls(last.to,   'arena-last-to');
    }

    /* ── click-to-move state ── */
    var selSq = null;
    function clearSel() { clearClass('arena-sel'); selSq = null; }

    window.addEventListener('load', function () {

        var boardEl = document.getElementById('board');
        if (!boardEl) return;

        /* ── CLICK-TO-MOVE ── */
        boardEl.addEventListener('click', function (e) {
            if (typeof chess   === 'undefined') return;
            if (typeof onDrop  === 'undefined') return;
            /* respect game state flags when present */
            if (typeof gameStarted !== 'undefined' && !gameStarted) return;
            if (typeof gameOver    !== 'undefined' && gameOver)      return;

            /* find the [data-square] ancestor */
            var el = e.target, sq = null;
            for (var i = 0; i < 6 && el && el !== boardEl; i++) {
                if (el.getAttribute) { sq = el.getAttribute('data-square'); }
                if (sq) break;
                el = el.parentElement;
            }
            if (!sq) return;

            if (!selSq) {
                /* select a piece */
                var p = chess.get(sq);
                if (!p) return;
                if (p.color !== chess.turn()) return;
                if (typeof onDragStart === 'function') {
                    if (onDragStart(sq, p.color + p.type.toUpperCase()) === false) return;
                }
                selSq = sq;
                addCls(sq, 'arena-sel');
            } else {
                /* attempt the move */
                if (sq === selSq) { clearSel(); return; }
                var from = selSq;
                clearSel();
                var prevCount = chess.history().length;
                var result = onDrop(from, sq);
                if (result === 'snapback') return;
                /* sync board display (drag mechanism is bypassed, so do it manually) */
                if (typeof board !== 'undefined') {
                    board.position(chess.fen());
                }
                if (chess.history().length > prevCount) showLastMove();
            }
        });

        /* ── LAST-MOVE HIGHLIGHT for drag / stockfish moves ──
         * Watches board DOM changes; when chess.history() grows → highlight last move.
         * Also clears highlights when the game resets (history shrinks).
         */
        var prevMoveCount = (typeof chess !== 'undefined') ? chess.history().length : 0;
        var debTimer = null;

        new MutationObserver(function () {
            clearTimeout(debTimer);
            debTimer = setTimeout(function () {
                if (typeof chess === 'undefined') return;
                var cnt = chess.history().length;
                if      (cnt > prevMoveCount) showLastMove();
                else if (cnt < prevMoveCount) clearHighlights();
                prevMoveCount = cnt;
            }, 80);
        }).observe(boardEl, { childList: true, subtree: true });

    });
}());
