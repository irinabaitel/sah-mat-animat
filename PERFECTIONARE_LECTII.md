# Perfecționarea lecțiilor — jurnal de lucru

Documentul de continuitate pentru runda de perfecționare a lecțiilor din Nivelul I (început pe 9 noiembrie 2026). De aici se poate relua lucrul de pe orice calculator care are repo-ul.

## 1. Ce am stabilit

- Lecțiile se refac **pe rând**. Eu propun, iar Irina aprobă înainte să încep.
- Exemplele vin **numai din materiale**, nu sunt inventate:
  - Manualul Steps (Brunia & van Wijgerden) și caietul pasului 1: `D:\DIN ONEDRIVE\sah - tot ce am\Cărți de șah\`;
  - programul **Chess Tutor Step 1** (`C:\Program Files (x86)\Chess Tutor`);
  - lecțiile **ChessKid** (`Lectii chesskid/`, decodor `tools/ckdec.py`).
- **Modelul aprobat** este `nivel1_lectia5.html` („e minunate! așa le vom face pe toate!”). Structura modelului:
  - sertare cu exemplele din Manual. Butoanele joacă mutarea, iar greșelile sunt marcate cu „?”;
  - acordeonul „🏋️ Exerciții” are 3 taburi:
    - **De bază**: ChessKid și caietul Steps;
    - **Mediu**: „Exercises” din Chess Tutor;
    - **Avansat**: „Extra exercises” din Chess Tutor.
  - se folosesc **toate** pozițiile din fiecare set, nu o selecție;
  - feedback cu motivul greșelii, indiciu în trepte (pătrat verde, apoi săgeată, apoi mutarea scrisă), „Arată răspunsul”, progres salvat, „Ia setul de la capăt”;
  - acordeonul „🎮 Exersează!” cu minijocurile lecției. Jocurile din secțiunea „Play” a lecției din Chess Tutor se fac fie ca minijocuri noi, fie ca variante ale celor existente.
- Reguli de scris: „capturează” (nu „mănâncă”), fără virgulă înainte de „și”, stil măsurat, notație românească (R, D, T, N, C), fără detalii tehnice de lucru în lecții, cu sursa creditată.

## 2. Ce e gata

| Lecția | Pagina | Commit | Conținut |
|---|---|---|---|
| Atacul, captura, apărarea | `nivel1_lectia5.html` | 661cfa9 | Manual Step 1, lecțiile 3 și 5; 188 de exerciții (Chess Tutor L3+L5, ChessKid L5) |
| 4 minijocuri noi pentru lecția 5 | `nivel1_joc_cal_neaparate`, `_scapa_de_dame`, `_schimba_nebunii`, `_cal_trei_piese` | 92675e5 | Chess Tutor 5b, 5c, 3d, 5d |
| Atacul asupra regelui (șahul) | `nivel1_lectia6.html` | b2fbd1a | Manual Step 1, lecția 6; 130 de exerciții (ChessKid L3 + caietul Steps + Chess Tutor L6) |
| Jocuri pentru lecția 6 | `nivel1_joc_rege_pioni.html` (nou), `nivel1_joc_scapa_de_dame.html?p=2`, `nivel1_joc_cine_pastreaza.html?v=turn` | b2fbd1a | Chess Tutor 6e, 6c, 6d |
| Matul | `nivel1_lectia7.html` (nouă; înlocuiește pagina „în construcție”) | vezi git log | Manual Step 1, lecțiile 7 și 8 (32 de exemple în 8 sertare); 264 de exerciții: ChessKid L3 „Is this checkmate?”, 12 foi de mat din caiet, Chess Tutor L7+L8 (exercises + extra) |
| Apărarea împotriva matului | `nivel1_lectia16.html` (nouă) | vezi git log | Manual **Step 2**, lecția 12 + caietul Step 2 p. 49 (24 de exemple în 9 sertare, cu șahul dublu din ChessKid L11); 81 de exerciții: caietul Step 2 foile A și B, Chess Tutor **Step 2** L12 (12a–d + extra 12a–b) |
| Patul | `nivel1_lectia17.html` (nouă; `pagina7.html` trimite aici) | vezi git log | Manual Step 1, lecția 12 „Draw” + ChessKid L3–L4 (16 exemple în 7 sertare, cu partida Troițki – Vogt 1896); 79 de exerciții: caietul Step 1 „Mate, stalemate or play: A”, ChessKid L4 „Checkmate or Stalemate?”, Chess Tutor Step 1 L12 (12a–b) și lecția avansată P6 (P6a–d) |
| Mutări speciale (rocada, promovarea, en passant) | `nivel1_lectia3.html` (refăcută) | vezi git log | Manual Step 1, lecțiile 9 „Castling” și 14 „Promotion / en passant” + ChessKid (16 exemple în 8 sertare, cu subpromovarea c8=T); textele vechi ale Irinei în primul sertar; 68 de exerciții: caietul Step 1 „Castling A”, ChessKid (rocada, en passant, promovare/subpromovare), Chess Tutor Step 1 L9 (9a–c) și L14 (14a) |
| Piese atârnate | `nivel1_lectia13.html` (refăcută) | vezi git log | Textele Irinei păstrate (metodele de apărare ca butoane cu exemple pe tablă, 3 exemple din partide); 35 de exerciții: cele 5 poziții vechi „Capturează piesa atârnată!” (Manual Step 1), Chess Tutor Step 1 P2c, P1c și P2e; arena `nivel1_arena_atarnate.html` (40 de puzzle-uri Lichess hangingPiece) |

Lecția 6 are și jocurile care existau deja: Regii și diamantele (Chess Tutor 6a) și Regi și Pioni (6b, `joc_stockfish.html`).

### Rămase de confirmat de Irina

1. **Scapă de dame:** limita de 10 mutări după care calul câștigă e pusă de mine; programul nu o spune.
2. **Calul și piesele neapărate** și **Schimbă nebunii** au modurile „Singur” și „În doi”. La nebuni, modul „În doi” e cooperativ: un jucător mută albul, celălalt negrul.
3. **Calul contra trei piese:** dacă negrul joacă perfect, calul rezistă doar 7 mutări. Robotul Dragon câștigă aproape mereu cu negrul.
4. **Caietul, „Dă șah A”:** răspunsul nr. 2 din Manual (h5xg4+) nu se potrivește cu nicio diagramă, iar diagrama 6 nu are răspuns. Am pus singurul șah sigur, Td2+.
5. **Turn contra cal:** în Chess Tutor pierde cine nu mai poate muta. Am păstrat regulile paginii noastre (se trece rândul, apoi se numără materialul).
6. **Regele contra pionilor:** regula „dacă regele nu are mutare, mută iar albul” e pusă de mine. Pionul ajuns pe linia 8 iese de pe tablă și aduce un punct.

Despre **Matul**: în hub, „Matul” duce acum la `nivel1_lectia7.html`. `pagina5.html` a rămas „Arena de mat” (mat în 1–4, Lichess) și e legată din Exersează. Tipuri noi de sarcini în pagină: `move` cu `check: 'mate'` (orice mat e primit; la greșeală spune scăparea: fuge, capturează, se pune în cale), promovare la alegere în `move`, `addmate` (pune una sau mai multe piese, cu `cross` = pătrate marcate) și `mateq` (Este mat? Da/Nu).

7. **Matul:** din Chess Tutor am lăsat deoparte seturile extra „Name squares” și „Defending: mix” (7c, 7d, 8c, 8d), pentru că nu țin de mat.
9. **Apărarea împotriva matului:** în Step 1 nu există lecția, așa că am luat-o din Step 2, lecția 12. `aparare_mat.html` (pagina veche) a rămas „Arena de apărare” (25 de poziții), legată din Exersează. Am lăsat deoparte: extra 12c–12d (atac dublu, atac descoperit), 12b#6 (răspunsul e rocada, pe care pagina nu o știe), 12c#3 (captura nu s-a putut reconstitui), foaia A nr. 12 (e un desen). La 12c#2 și #8 Chess Tutor cere o serie (șah, răspuns, captură); exercițiul cere prima mutare, iar explicația arată restul. Caietul p. 49 dreapta-sus spune „Black” la o captură făcută de alb (greșeală de tipar): am scris „Albul”.
10. **Apărarea împotriva matului:** jocurile din Chess Tutor Step 2 L12 sunt făcute: 12a `nivel1_joc_doi_nebuni.html` (limita 5 mutări, nu 6: cu joc perfect nebunii rezistă doar 5), 12b `nivel1_joc_vanatoarea_nebunului.html` (tabelă retrogradă `data/vanatoare_nebun.bin.gz`, joc perfect = 3 mutări, limita 10; solverul în `games/solve/`), 12c `nivel1_joc_pozitia_initiala.html` (minimul real e 29, nu 31; `games/solve/pozinit_ida.py`), 12d `joc_stockfish.html?v=3` (regulile Regi și Pioni, poziția din Chess Tutor; albul câștigă).
11. **Patul:** pagina veche `pagina7.html` avea exemple și 25 de „puzzle-uri defensive” fără sursă (inventate), deci a devenit o redirecționare spre `nivel1_lectia17.html`. Textele Irinei din „Ce este patul?” și „Când îl evităm, când îl căutăm?” sunt în primul sertar. Tipuri noi în pagină: `msp` (Mat / Pat / Se joacă, cu mutarea după „Se joacă” la caiet), `kplace` (pune regele ca să fie pat; toate pătratele bune calculate) și `check: 'nostale'` (mutarea care dă pat e respinsă cu „Pat!”). La P6b#7 și P6c#10 Chess Tutor nu arată clar mutarea: `NS_FIX` în `build17.py` (g6, respectiv Tg6). Jocurile din Chess Tutor L12 (12a Mat cu regina și pionul contra nebunului, 12b Regina contra 2 cai, 12c Mat cu regina și nebunul, 12d Monede cu caii, 12e Folosirea avantajului) nu sunt făcute; în Exersează sunt Vânătoarea regelui și **Arena patului** (`nivel1_arena_pat.html`, 43 de poziții din Chess Tutor Step 2, lecția P6 Stalemate: seturile „Defend by stalemate” c–d, „Avoiding stalemate” b–e și 3 din „Draw” f). Lichess nu are puzzle-uri cu temă de pat (0 din 1160 căutate), de aceea arena vine din Chess Tutor. Liniile: `arena_pat_lines.py` → `arena_pat_sf.py` (Stockfish; fiecare poziție are o singură soluție) → `arena_pat.py` scrie `data/stalemate_arena.json`; pagina se refăce cu `make_arena_pat.py` din `pagina90a.html`. Chess Tutor Step 2 P6 e la y=525 în lista lecțiilor; seturile la y=202…297. Chess Tutor P6 „Draw” se află la y=563 în lista lecțiilor din Step 1; lecția 12 la y=354.
12. **Mutări speciale:** tipuri noi în pagină: `castles` (bifezi rocadele permise pentru alb și negru, apoi „Verifică”), `choice` (de ce nu e permisă rocada; 5 motive calculate de `why_not` în `build3.py`), `notmate` (mutarea care pare mat, dar en passant o anulează) și `badpromo` (promovarea în damă care dă pat e respinsă). Generatoare: `build3.py` (exerciții), `demo3.py` (sertare), `make3.py` (pagina, din `nivel1_lectia17.html`). Seturile Chess Tutor L4 (`sets/L4e_a/b.json`) sunt păstrate pentru lecția despre pion, unde promovarea e reluată ca scop al jocului pionilor. Chess Tutor Step 1: L9 la y=297, L14 la y=392.
13. **Piese atârnate:** generatoare `build13.py` (exerciții → `data/nivel1_lectia13_ex.js`) și `make13.py` (pagina, din `nivel1_lectia3.html`; textele vechi se citesc din git `bc25c64:nivel1_lectia13.html`). Metoda 5 („Poți neglija atacul…”) rămâne doar text, ca înainte. Arena: `tools/fetch_hanging.py` (Lichess batch hangingPiece; filtru: prima mutare capturează o piesă, nu pion, care nu poate fi recapturată) → `tools/build_hanging_arena.py` → `data/hanging_arena.json`; pagina e făcută din `nivel1_arena_pat.html`, cu mutarea adversarului marcată (`last`) și mat acceptat pe orice mutare la final.
    **Refăcută (11.11.2026), la cererea userului:** varianta cu 8 sertare era greu de urmărit. Pagina a revenit la scheletul vechi (Rocada, Promovarea, En passant, fiecare cu demonstrația pas cu pas, apoi Exerciții și Exersează cu ambele jocuri); textele vechi au rămas, s-au schimbat doar primele două reguli de turneu de la promovare (formularea userului). Exercițiile (78) sunt pe 3 niveluri, cu o singură notă despre surse. Cele 5 exerciții vechi de promovare și cele 5 de en passant se rezolvă acum cu mutarea pe tablă (câmpuri noi: `pre`, `post`, `ep`, `last`, `bad`, `failmsg`, `show`); variantele din comentarii au fost verificate cu Stockfish. Datele: `tools/perfectionare/build3b.py` (rescrie `data/nivel1_lectia3_ex.js`). Pagina se editează direct: NU rula `make3.py`, ar suprascrie structura. `data/nivel1_lectia3_demo.js` a fost scos.
8. **Matul:** 8a și 8b sunt făcute (11.11.2026): `nivel1_joc_paznicul_vanatorul.html` (varianta „Două turnuri” = `?v=2`), din template-ul `games/paznic.tpl`. Fără rege alb, ca în Chess Tutor; regulile, aprobate de Irina: dacă regele capturează o piesă albă sau dacă albul face pat, albul pierde; limita e de 50 de mutări. Tabelele `data/mat_dama_turn.bin.gz` și `data/mat_doua_turnuri.bin.gz` sunt făcute de `games/solve/mat_fara_rege.js`: joc perfect = 4, respectiv 5 mutări. Pagina trimite la Finaluri esențiale (pagina10, pagina12) pentru matul cu ambii regi. Împărțirea celorlalte jocuri, cerută de Irina: 7d Turn contra nebun, 7c Planificatorul de drum și 8d 3 piese ușoare contra turnului merg la „Cum se mișcă piesele” (8d și la Atacul, Captura și Apărarea); 8c (8 pioni contra 2 cai) există deja: e Cursa cu obstacole; 7a merge la lecția despre pion.

### Urmează

- Jocurile pentru Matul (punctul 8 de mai sus), dacă Irina le vrea.
- **Șahul dublu** (`pagina4.html`) s-a mutat în Nivelul IV, după Atacul dublu prin descoperire (95a → 4 → 96). În Nivelul I rămâne doar regula, ca sertar în lecția de apărare (`nivel1_lectia16.html`, sertarul „Șahul dublu”, făcut): la șah dublu doar regele se poate muta. Formularea: regele **pleacă**, nu „fuge” (fără panică).
- Apoi, în ordine: rocada, schimbul avantajos, atacul dublu, remiza/patul, matul cu dama, en passant, notația.

## 3. Cum se lucrează (pașii pentru o lecție)

Toate uneltele sunt în **`tools/perfectionare/`**. Ele erau în folderul temporar al sesiunii și au fost copiate în repo. Căile din scripturi sunt relative la acest folder, așa că rulează-le din el. Stockfish nu e în repo; înainte de `sfmulti.py` rulează o dată `npm install stockfish` în `tools/perfectionare/`. Pentru capturile din Chess Tutor mai trebuie `pip install pywin32 pillow python-chess pymupdf`.

### 3.1 Exemplele din Manual

1. Randez paginile lecției din PDF-ul Manualului (pymupdf, 200 dpi, coloana din dreapta cu diagramele) și citesc diagramele pătrat cu pătrat.
2. Scriu exemplele în `demo6.py` (model), cu `S(fen, side, text, arrows, acts)` și `A(label, move, text, arrows, hl)`.
3. Scriptul verifică faptul că fiecare mutare este posibilă și scrie `data/nivel1_lectiaX_demo.js` (`window.LXDEMO`).
4. Diagramele împărțite în două (stânga/dreapta sau sus/jos) le arăt ca două exemple separate.

### 3.2 Exercițiile din Chess Tutor

Programul trebuie să fie deschis, ca „Guest”. Nu folosi profilul Irina, pentru că „Answer” îi strică scorul.

- `ct.py`: capturează fereastra (PrintWindow), citește textele și butoanele, recunoaște tabla și dă FEN-ul.
- `nav.py`, `runset.py` și `batch.py` deschid un set și, pentru fiecare din cele 10 poziții, salvează poziția înainte și după „Answer”, plus textul de explicație.
  - Rulare: `set PYTHONUTF8=1` și apoi `python batch.py L6x_a,6,212 L6x_b,6,231 ...`
  - Formatul fiecărui argument e `nume,lecție,y`. Al doilea număr e lecția din Chess Tutor, iar `y` e poziția setului în lista din dreapta (în pixeli logici).
  - În `batch.py`, `LES` dă poziția lecției în lista din stânga: 3→193, 5→231, 6→250, iar fiecare lecție următoare e cu 19 mai jos.
  - Seturile salvate sunt în `sets/*.json`. Imaginile nu au fost păstrate.
- **Scalarea ecranului:** `ct.py` citește scalarea din `CT_SCALE` (implicit 1.25). Pe monitoarele la 100% rulează cu `CT_SCALE=1`. `run7.py` găsește butoanele singur (numerele, Answer, Start, Overview), deci merge la orice mărime a ferestrei: `python run7.py open <y_lecție> <y_set> <nume>`. Lecția 7 e la y=259, lecția 8 la y=278. Seturile: Exercises 202/221/240/259, Extra 430/449/468/487. Dacă răspunsul nu apare, mărește așteptarea cu `CT_WAIT=3 CT_WAIT2=6`.
- **Chess Tutor Step 2** (`C:\Program Files (x86)\Chess Tutor\Chess Tutor Step 2 CD\ChessTutor2.exe`): nu pornește cât e deschis Step 1, deci închide Step 1 întâi. Rulează cu `CT_TITLE="Chess Tutor Step 2" CT_SCALE=1 CT_BM=1` (butoanele lui răspund doar la BM_CLICK). Lecția 12 e la y=354. Stockfish pentru „mutări la fel de bune”: `npm install stockfish` în `tools/perfectionare/` (`node_modules` e ignorat).
- **Șabloanele pieselor** (`tpl.json`) sunt acum în repo. O piesă necunoscută apare ca „?”. O înveți cu `python run7.py learnimg sets/img/<set>_<i>a.png e4=q`, apoi `python run7.py reread <set>`.
- Pe tablă nu se pot face mutări prin program (clicurile simulate nu sunt primite). De aceea răspunsul se ia din poziția „după Answer” și din textul explicației.
- `derive6.py` află mutarea-răspuns comparând pozițiile. Apoi Stockfish (`sfmulti.py`, cu `node_modules/stockfish` în folderul uneltelor) găsește mutările la fel de bune: diferență de cel mult 30 de centipioni, acceptate și ele.

### 3.3 Caietul Steps și ChessKid

- **Caietul:** foile sunt scanate. Un agent le-a transcris în FEN, apoi fiecare poziție a fost verificată cu python-chess față de răspunsurile din Manual (mutarea legală, dă șah etc.). Rezultatul e în `wb/workbook_check.json`.
- **ChessKid:** `python tools/ckdec.py "Lectii chesskid/<lecția>.pdf"` dă FEN-urile, iar răspunsurile sunt în „Answer Key” de la sfârșitul PDF-ului.

### 3.4 Construirea paginii

1. `build6.py` (model) produce `data/nivel1_lectiaX_ex.js` (`window.LXEX`). Fiecare sarcină e verificată la generare: mutare legală, dă șah, iese din șah, pătratele „checksq” egale cu cele calculate, rută sigură.
2. `make6.py` face pagina nouă din `nivel1_lectia5.html`, prin înlocuiri exacte: titlu, sertare, taburi, `SAVE_KEY`, legături, Exersează, subsol.
3. **Tipuri de sarcini în pagină:**
   - `move`, cu `check` = `give` / `out` / `best`;
   - `route`, cu `mode` = `exact` / `min` / `check`, plus promovare cu alegerea piesei;
   - `squares`, `checksq`, `marks`, `place`, `nocircle`, `clicksq`, `namesq`, `yesno`.
4. Din lecția 6, motorul ține cont de regi:
   - `kingSq`, `inCheck`, `legalMove`, `capturers`, `markChecks`;
   - `.highlight-check` pe regele în șah.

### 3.5 Minijocurile

1. `games/gen.py` + `games/common.js` + `head.txt` / `css.txt` fac pagina jocului dintr-un șablon `games/<nume>.tpl`. Secțiunile șablonului sunt `===FILE===`, `===TITLE===`, `===HEADER===`, `===CSS===`, `===PANEL===` și `===SCRIPT===`, cu `/*COMMON*/` în locul unde intră codul comun.
2. Rulare: `python games/gen.py regepioni`.
3. Standardul jocurilor:
   - modurile 🤖 Contra Robotului / 👫 În doi;
   - nivelurile Pui de găină (0.9), Mânz (0.2), Dragon (0, perfect);
   - 3 încercări nepermise înseamnă pierderea meciului;
   - două reprize cu rolurile schimbate;
   - caseta „Cum se joacă” conține doar regulile.
4. Robotul Dragon joacă din calcul complet acolo unde se poate: tabelă retrogradă pentru dame, căutare cu memorare pentru pioni și pentru cele trei piese.
5. **Atenție:** la Dragon, scurtătura „capturează dacă poate” trebuie oprită (`randomness > 0`). Altfel nu mai joacă perfect.
6. După un joc nou:
   - adaugă-l în `minijocuri-nav.js` (`GAMES`) și în `hub.html` (lista „Joacă și exersează”);
   - schimbă `?v=` la `minijocuri-nav.js` în toate paginile.

### 3.6 Testare și urcare

1. `runtest.py` pornește un server local (port 8766) și deschide în Chrome headless o pagină-test cu un iframe. Pagina-test rulează un script care rezolvă singur toate exercițiile și raportează eșecurile.
   - Paginile-test (`_test_g.html`, `_t_*.js`) se șterg după folosire.
   - `shots.py` face capturi de ecran.
2. Înainte de push: `python tools/verifica_pagini.py`, plus o căutare după „, și ” și „mănânc”.
3. Push după fiecare rundă. Irina verifică pe site.
