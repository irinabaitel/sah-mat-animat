# /puzzles-lichess

Actualizează puzzle-urile din `pagina75.html` cu puzzle-uri proaspete de pe Lichess API.

## Ce face

Rulează `fetch_puzzles.py` care:
1. Contactează Lichess API cu tokenul OAuth din fișier
2. Descarcă puzzle-uri cu temele `doubleBishopMate` și `bodenMate`
3. Filtrează după popularitate, rating și lungimea soluției
4. Amestecă și sortează după dificultate
5. Înlocuiește array-ul `PUZZLES` din `pagina75.html`

## Pași de executat

1. Rulează scriptul:
   ```
   python fetch_puzzles.py
   ```

2. Citește output-ul și raportează utilizatorului:
   - Câte puzzle-uri unice s-au primit per temă
   - Câte au trecut filtrarea
   - Rating-urile finale ale puzzle-urilor selectate

3. Dacă scriptul raportează mai puțin de 35 puzzle-uri totale, întreabă
   utilizatorul dacă vrea să relaxeze filtrele (MIN_PLAYS sau MIN_RATING).

4. Dacă scriptul eșuează cu eroare HTTP 401, tokenul Lichess a expirat —
   spune utilizatorului să genereze unul nou la:
   https://lichess.org/account/oauth/token/create
   și să îl pună în `fetch_puzzles.py` la linia `LICHESS_TOKEN = ...`

## Argumente opționale

Dacă utilizatorul scrie `/puzzles-lichess greu`, modifică temporar în script:
- `MIN_RATING = 1400`
- `MAX_RATING = 2200`

Dacă scrie `/puzzles-lichess usor`, modifică:
- `MIN_RATING = 500`
- `MAX_RATING = 1200`

Restaurează valorile originale după rulare.
