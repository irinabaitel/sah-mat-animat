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
Orice tablă interactivă suportă **click ȘI drag-and-drop**; `touch-action:none` pe `.board-wrapper`.

Include întotdeauna **`<script src="board-utils.js"></script>`** în orice pagină cu tablă interactivă (plasează după jQuery + chessboard.js, înainte de `</body>`). Conține:
- **Touch bridge** — convertește touch events în mouse events pentru chessboard.js (drag cu degetul pe touchscreen)
- **Adnotări 4 culori** — click-dreapta drag = săgeată, click-dreapta loc = pătrat evidențiat; taste modificatoare: nimic=verde, Shift=roșu, Ctrl=albastru, Alt=galben; expune `window._annClear()` și `window._annRender()`

## Clase CSS globale
`.hl-box` / `.hl-box.ok` / `.hl-box.warn` sunt în `master-template.css` — nu le redefini local.
