# HANDOFF — Nivelul VI „Deschideri și capcane în deschidere"

> Document de continuitate. Orice Claude care deschide acest repo (inclusiv de pe altă
> mașină / tabletă) poate relua lucrul de aici. Actualizat: 20 iulie 2026.

## Ce este Nivelul VI
Platforma **Laboratorul de Șah** (laboruldesah.ro / GitHub Pages), pentru copii.
Nivelul VI = deschideri consacrate + capcanele lor.

**Taxonomie confirmată de user (3 ramuri):**
1. **Maturi rapide** (pentru începători, orice culoare): mat-uri în câteva mutări.
2. **Deschideri cu Albul** — ce alegi să joci când ai albele (Italiana, Spaniola, Gambitul Damei…).
3. **Deschideri cu Negrul** — ce alegi să joci când ai negrele (Siciliana, Caro-Kann, Elephant…).

**Reguli de perspectivă și structură (de la user):**
- Deschiderea se prezintă din perspectiva celui care **o joacă** (o alege).
- Capcana se prezintă din perspectiva celui care **câștigă**.
- O deschidere e pe raft după cine o alege, DAR poate avea capcane cu **ambele culori**
  (🪤 câștigi cu deschiderea ta / ⚠️ ferește-te, aici te pedepsește adversarul).
- Ordine simplu→greu: Maturi rapide → Italiana → Spaniola → … → Gambitul Damei la final.
- **Categoria se numește „Maturi rapide"** (NU „matcuri" — cuvânt greșit).

## Lecții GATA (pe site)

| Fișier | Lecție | Conținut |
|--------|--------|----------|
| `nivel6_lectia2.html` | **Matul prostului** | 2 variante (dat de Negru / dat de Alb), cu Exersează |
| `nivel6_lectia3.html` | **Altă mutare nefericită** | 1.e4 e5 2.Dh5 Re7?? 3.Dxe5# (regula piesei atinse) |
| `nivel6_lectia4.html` | **Matul școlarului** | Cum îl dai / cum te aperi (5 apărări cu butoane) / cum pedepsești (…Df2#) / **Altă pedeapsă — metoda Smirnov** (…Nd1#, cu Exersează) |
| `nivel6_lectia5.html` | **Partida Italiană** | Idee (Giuoco Piano + Doi Cai) + Fried Liver (câștigă Albul) + capcana șilingului/Blackburne (câștigă Negrul, mat, cu Exersează) |
| `nivel6_lectia1.html` | **Gambitul Damei** | Refuzat/Acceptat + lăcomia …b5 (Alb) + Capcana Elefantului (Negru) |

**Navigație (footer):** lectia2 → lectia3 → lectia4 → lectia5 (Italiana) → lectia1 (Gambitul Damei).
**Hub:** cardul Nivel VI din `hub.html` are toate linkabile.

## Motorul lecțiilor (cum se construiește o lecție nouă)
Model de referință: `nivel6_lectia5.html` (sau `lectia1`). chessboard.js 1.0.0 + chess.js 0.10.3
+ jQuery 3.5.1, piese `caliente` de pe lichess CDN, `master-template.css`, `board-utils.js`.

Structură JS: array `chapters[]` (fen, orient, san[] în SAN **engleză**, ann{} adnotări pe pași,
arrows{} săgeți G/R/B/Y, iar pentru capcane cu Exersează: `winner:'w'|'b'`, `practiceFrom`, `winEval`)
+ array `accData[]` (chIdx, kind:'opening'|'trap', num, title, badge, `practice:true/false`, desc).
Notație afișată în română via `toRo()` (K→R,Q→D,R→T,B→N,N→C). Mișcare liberă legală în studiu (`sGame`).
Mod Exersează: robotul joacă adversarul, userul joacă **partea câștigătoare** (jos pe tablă), bară eval + precizie %.

**REGULĂ TARE: userul exersează ÎNTOTDEAUNA partea CÂȘTIGĂTOARE.** Fried Liver e doar prezentare
(sacrificiu → bara de material ar deruta), deci `practice:false`.

**Indiciu în trepte (la toate lecțiile cu Exersează):** butonul „💡 Indiciu" ajută vizual —
1ª apăsare = pătratul piesei verde (`.hint-square`); 2ª = săgeată verde spre destinație; 3ª = mutarea scrisă.
Vezi `pracHint`/`drawPracHintArrow`/`clearPracHint` + `pracHintStage` în `nivel6_lectia5.html`.

## Verificarea liniilor (OBLIGATORIU)
**Nicio linie nu intră în lecție neverificată.** Folosește python-chess (instalat):
`scratchpad/try_line.py "e4 e5 Bc4 ..."` → spune dacă toate mutările sunt legale + dacă e MAT.
Userul urăște erorile de șah (ex. „furculiță pe pion apărat"). Reconstrucția din cadre video e
NESIGURĂ pentru linii demonstrative → **când e greu, cere userului să pună linia în studiul ei Lichess**
(xMvnWhmH) și importă PGN cu `?comments=true` (workflow care merge mereu).

## Workflow filme Facebook/YouTube (pentru capcane noi)
Userul a strâns ~253 filmulețe FB (linkuri în `scratchpad/fb_links.txt`). Pipeline:
1. `scratchpad/grab_wave.py START COUNT` → descarcă (yt-dlp, fără login) + taie cadre (ffmpeg din imageio-ffmpeg). Sare filmele >360s.
2. Agenți paraleli citesc cadrele din `scratchpad/frames_fb/{tag}/` și clasifică (deschidere/culoare/mat sau material).
3. Catalog în `capcane_din_filmulete.md`. Comentariile AUTORULUI: ia transcrierea audio cu
   `yt-dlp --skip-download --write-auto-subs --sub-lang "en.*"` → tradu în română (vezi mai jos).

**Stadiu clasificare:** valurile 1+2+3 gata (filme 000–083). ~37 capcane utile. **Rămân ~169 filme** (084+).
Multe filme sunt de fapt FINALURI (→ Nivel III) sau MODELE DE MAT (→ Nivel V) — se pun deoparte, nu se reprocesează.
Rafturile vizuale cu capcanele clasificate: artifact publicat (link în istoricul conversației).

**Pe măsură ce se clasifică filmele, se ADAUGĂ capcane la fiecare deschidere existentă** (structura e extensibilă).

## Filozofia deschiderilor (box în fiecare lecție de deschidere)
Fiecare lecție de deschidere are un box `.quote-box` cu ideea lui **Aron Nimzovici**:
teoria = jocul marilor maeștri; nu memora orbește, înțelege DE CE; din deschidere de obicei **pierzi**,
nu câștigi; o capcană merge **doar dacă adversarul greșește** — de aceea învățăm și cum s-o dăm, și cum să n-o pățim.
Model: `nivel6_lectia5.html` (sub note-box-ul „Ține minte"). **Pune-l în orice deschidere nouă.**

## Reguli de limbaj/stil (cerute de user — aplică-le mereu)
- „legat/a lega/leagă" pentru pin (NU „pironit/țintuit"); „capturează" (NU „înșfacă/ia"); „pentru că" (NU „fiindcă").
- Numește pionii pe pătrat: „pionul f7/f2" (NU „pionul din fața regelui").
- Prima capcană a unei deschideri = una în care JOCI deschiderea și CÂȘTIGI (partea care o alege).
- Titlul capcanei unde câștigă partea care NU deține deschiderea = „Cum pedepsești…".
- Badge: verde = „✅ Câștigi material/Mat în N (cu Albul/Negrul)"; roșu = „⚠️ Câștigă Negrul — material/mat". Distinge mereu mat vs material.
- Deschiderea se prezintă pe 4–6 mutări, scopul fiecărei mutări. **Max 10 mutări per capcană.**
- Ton educativ, hazliu cu măsură. NU intra în contul chess.com al userului.
- Sursă de încredere pentru explicații: **GM Igor Smirnov** (`youtube.com/@GMIgorSmirnov/shorts`).
  Când folosești un filmuleț, adnotările = comentariile LUI traduse în română, nu inventate.

## CE URMEAZĂ
1. **Partida Spaniolă** (Ruy Lopez) — următoarea deschidere „cu Albul" (după Italiana, înainte de Gambitul Damei). Are nevoie de o capcană „câștigă Albul" (Spaniola avea în rafturi doar capcane pro-Negru — caută una în filmele 084+).
2. Deschideri „cu Negrul": Siciliana, Caro-Kann/Franceză, Gambitul Stafford, Englund, Elephant.
3. Continuă clasificarea filmelor 084+ pe valuri; adaugă capcanele găsite la deschiderea potrivită.
4. `REGULA #1` din CLAUDE.md: **întreabă userul înainte de a începe lucru mare.**
