# Instrucțiuni pentru Claude — SahMatAnimat

## REGULA #1 — Întreabă înainte de orice
**Înainte să te apuci de orice lucru, întreabă utilizatorul exact ce trebuie făcut.**
Nu citi fișiere, nu explora, nu schița planuri — pune întrebarea și așteaptă confirmarea.
Fă asta inclusiv dacă cererea pare clară. Cheltuirea de tokeni fără țintă este costisitoare.

## Piese aprobate
Set: `caliente` de pe lichess CDN — `https://lichess1.org/assets/piece/caliente/{piece}.svg`

## Highlight-uri pe tablă
Adaugă clasă CSS pe `.square-XX` existente (nu crea div-uri absolute poziționate manual).

## Tablă interactivă
Orice tablă — inclusiv cele cu exemple ilustrate (non-puzzle) — suportă **click ȘI drag-and-drop**; `touch-action:none` pe `.board-wrapper`. Inițializează întotdeauna cu `draggable: true`.

Include întotdeauna **`<script src="board-utils.js"></script>`** în orice pagină cu tablă interactivă (plasează după jQuery + chessboard.js, înainte de `</body>`). Conține:
- **Touch bridge** — convertește touch events în mouse events pentru chessboard.js (drag cu degetul pe touchscreen)
- **Adnotări 4 culori** — click-dreapta drag = săgeată, click-dreapta loc = pătrat evidențiat; taste modificatoare: nimic=verde, Shift=roșu, Ctrl=albastru, Alt=galben; expune `window._annClear()` și `window._annRender()`

## Clase CSS globale
`.hl-box` / `.hl-box.ok` / `.hl-box.warn` sunt în `master-template.css` — nu le redefini local.

## Butoane reset progres în arene
**Orice pagină de arenă trebuie să aibă buton de resetare a progresului.** Pattern standard:

```html
<!-- în lectureView, după continueBtn -->
<button class="btn-arena" id="resetAllBtn" onclick="resetAllProgress()"
        style="display:none; margin-top:8px; background:rgba(192,57,43,0.82);">
  ↺ Joacă din nou (resetează tot)
</button>
```

```js
function resetAllProgress() {
  try { localStorage.removeItem(SAVE_KEY); } catch(e) {}
  completed = {};
  updateArenaBtn();
  enterArena(0);
}
```

- `resetAllBtn` se afișează **imediat ce `done > 0`** (după primul puzzle rezolvat) — adaugă `if (rb) rb.style.display = 'flex';` în blocul `if (done > 0)` din `updateArenaBtn()`
- Există și `playAgainBtn` în puzzleView (pentru când toate puzzle-urile sunt rezolvate)
- Model de referință: `pagina52.html`

## Auto-scroll la lista de mutări (lecții cu exemple)
În paginile de lecție cu `.moves-log` + butoane ◄ ► (de derulare prin exemple), **nu folosi `active.scrollIntoView()`** — scrolează și panoul mare, iar butoanele „fug de sub mouse" când userul apasă pentru mutarea următoare (mai ales pe paginile cu poveste lungă).

Pattern corect — scrolează **doar** containerul `.moves-log`:
```js
const active = document.querySelector('.mlog-token.active');
if (active) {
  const log = document.getElementById('movesLog');
  const a = active.getBoundingClientRect();
  const l = log.getBoundingClientRect();
  if (a.top < l.top)            log.scrollTop += a.top - l.top;
  else if (a.bottom > l.bottom) log.scrollTop += a.bottom - l.bottom;
}
```
Aplicat în `pagina89.html`. Dacă apare aceeași problemă pe alte lecții (pagina88, 50, 52 etc.), copiază blocul.

## Starea proiectului (mai 2026)

**Proiect: Laboratorul de Șah** — platformă educațională de șah pentru copii.
Brandul vechi "Cufărul cu Șah" = abandonat. Storylinea Tusk + Kibo = **ABANDONATĂ de mult timp** — nu o mai folosi, nu o mai menționezi.

### Structura — 6 niveluri progresive + bonus

| Nivel | Titlu | Stare |
|-------|-------|-------|
| I | Bazele jocului | 11 lecții disponibile |
| II | Planuri și principii | în curând |
| III | Finaluri esențiale | 12 finaluri |
| IV | Tactici și combinații | 15 tehnici; Zugzwang: pagina88.html + arenă pagina88a.html; Calul Troian (Darul Grecesc): pagina89.html + arenă pagina89a.html; Subpromovarea: pagina90.html + arenă pagina90a.html (40 puzzle-uri fiecare) |
| V | Modele de mat | 28 modele; Damiano: pagina87.html |
| VI | Capcane și miniaturi | în curând |
| Bonus | 6 minijocuri interactive | |

Istoria Șahului = secțiune separată (Chaturanga, Shatranj, Xiangqi, Shogi, Răspândire, Europa, AI).

### Fișiere cheie
- `hub.html` — hub central cu cele 6 niveluri
- `index.html` — pagina principală
- `master-template.css` — CSS global (nu redefini clasele din el local)
- `board-utils.js` — obligatoriu în orice pagină cu tablă interactivă
- `pagina50.html` — **model de referință pentru arene** (Atac Dublu): turn badge, ctrl-row cu butoane mici, navigare ◄ ►, progress bar, feedback-bar
- `pagina52.html` — model de referință pentru butoanele de reset progres

### Pattern arene Lichess
Puzzle-urile de arenă vin **întotdeauna din Lichess API** — fișiere JSON pre-generate în `data/`.
Format UCI: `moves[0]` = mutarea de setup (jucată automat), userul joacă din `moves[1]` încolo.
`completed` = obiect indexat numeric (`completed[idx] = true`), salvat în `localStorage`.

---

## Efect mat pe pătrat rege
Folosește clasa **`.highlight-check`** (sec. 6 din `master-template.css`) — radial gradient roșu, stil Lichess.
**Nu inventa efecte noi.** Pattern JS standard (copiază din `pagina5.html`):
```js
function applyHL(sq, cls) {
  const el = document.querySelector('.square-' + sq);
  if (el) el.classList.add(cls);
}
// la mat:
applyHL(matedKingSquare(), 'highlight-check');
```
