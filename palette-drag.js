/* palette-drag.js
 * Drag-and-drop dintr-o paletă de piese (.strip-piece) direct pe pătratul de pe tablă,
 * cu suport mouse + touch prin pointer events. Soluție pentru cazul în care
 * board-utils.js (touch bridge) blochează click event-ul nativ pe touchscreen.
 *
 * Include după chessboard.js și după declararea funcției/variabilelor locale.
 *
 * Exemplu de inițializare:
 *   PaletteDrag.init({
 *     dataAttr: 'code',                              // data-* atribut care conține codul piesei
 *     canDrag : () => mode === 'edit',               // condiție pentru a permite drag
 *     onStart : (p) => selectPiece(p),               // (opțional) sincronizare cu starea paginii
 *     onDrop  : (sq, p) => {                          // ce se întâmplă când piesa cade pe pătrat
 *       const pos = board.position();
 *       pos[sq] = p;
 *       board.position(pos, false);
 *     }
 *   });
 */
(function () {
  'use strict';

  var ghost = null;
  var dragPiece = null;
  var opts = null;

  function onPointerDown(e) {
    if (!opts || !opts.canDrag()) return;
    e.preventDefault();
    dragPiece = this.dataset[opts.dataAttr];
    if (opts.onStart) opts.onStart(dragPiece);
    ghost = document.createElement('img');
    ghost.className = 'palette-ghost';
    ghost.src = this.src;
    ghost.style.left = e.clientX + 'px';
    ghost.style.top  = e.clientY + 'px';
    document.body.appendChild(ghost);
  }

  function dropAt(x, y) {
    if (!dragPiece || !opts) return;
    var endEl = document.elementFromPoint(x, y);
    var sqEl  = endEl && endEl.closest ? endEl.closest('[data-square]') : null;
    if (sqEl) opts.onDrop(sqEl.getAttribute('data-square'), dragPiece);
    cleanup();
  }
  function cleanup() {
    if (ghost) { ghost.remove(); ghost = null; }
    dragPiece = null;
  }

  window.PaletteDrag = {
    init: function (o) {
      opts = o || {};
      var selector = opts.selector || '.strip-piece';
      document.querySelectorAll(selector).forEach(function (el) {
        el.setAttribute('draggable', 'false');
        el.addEventListener('pointerdown', onPointerDown);
      });
      document.addEventListener('pointermove', function (e) {
        if (!ghost) return;
        ghost.style.left = e.clientX + 'px';
        ghost.style.top  = e.clientY + 'px';
      });
      document.addEventListener('pointerup',     function (e) { if (dragPiece) dropAt(e.clientX, e.clientY); });
      document.addEventListener('pointercancel', cleanup);
    }
  };
}());
