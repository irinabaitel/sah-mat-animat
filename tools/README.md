# tools/ — utilitare pentru repo

Scripturi ajutătoare. **Nu fac parte din site** — se rulează manual, de la rădăcina repo-ului.
Toate își calculează singure calea către repo, deci pot fi rulate de oriunde.

| Script | Ce face |
|--------|---------|
| `try_line.py` | **Verifică o linie de șah** (SAN, engleză) mutare cu mutare: spune dacă toate sunt legale și dacă e mat. Obligatoriu înainte ca o linie să intre într-o lecție.<br>`python tools/try_line.py "e4 e5 Nf3 Nc6 Bb5"`<br>Al doilea argument opțional = un pătrat (ex. `b3`) → arată mutările legale ale piesei de acolo în poziția finală. |
| `download_sahisti.py` | Descarcă de pe Wikipedia pozele marilor șahiști ai lumii în `img/sahisti/`. |
| `download_romani.py` | La fel, pentru cei 15 șahiști români, în `img/romani/`. |
| `remove_hearts.py` | Script de curățenie, **deja rulat o dată**: scoate din lecții CSS-ul și JS-ul vechi cu inimioare (`heartSteps`, `.heart-marker`, animațiile `hb-slow`/`hb-fast`). Se păstrează doar ca referință. |

Necesar: `python-chess` pentru `try_line.py` (`pip install chess`).
