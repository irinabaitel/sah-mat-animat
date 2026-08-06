# HANDOFF — Nivelul VI „Deschideri și capcane în deschidere"

> Document de continuitate. Orice Claude care deschide acest repo (inclusiv de pe altă
> mașină / tabletă) poate relua lucrul de aici. Actualizat: 4 august 2026.

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
| `nivel6_lectia5.html` | **Partida Italiană** | cea mai lucrată lecție — vezi secțiunea dedicată mai jos |
| `nivel6_lectia1.html` | **Gambitul Damei** | Refuzat/Acceptat + lăcomia …b5 (Alb) + Capcana Elefantului (Negru) |

**Navigație (footer):** lectia2 → lectia3 → lectia4 → lectia5 (Italiana) → lectia1 (Gambitul Damei).
**Hub:** cardul Nivel VI din `hub.html` are toate linkabile.

## Partida Italiană — stare la zi (`nivel6_lectia5.html`)
**Intro** (în vocea antrenorului userului — vezi resursa Chess Architect mai jos):
- def-box „Ce este Partida Italiană?": originea (studiată de maeștrii italieni acum >400 ani, Polerio/Greco → numele; „Giuoco Piano" = jocul lent), desfășurare molcomă.
- card: descriere **până la 3.Nc4** (nebun→c4, f7 = „călcâiul lui Ahile", regele „derocat", azi mai ales controlul câmpului d5) + **cele 4 continuări ale Negrului**: 3…Nc5 (Giuoco Piano), 3…Cf6 (Doi Cai), 3…d6 (solid), agresive (Cd4?!/f5). Credit fin „Idei din seria «Lupta șahistă» (Chess Architect)".
- **Titlul de acordeon „Ideea deschiderii" a fost SCOS** (cerut de user).

**Capitole (accordion):**
- 📖 Giuoco Piano (3…Nc5) — prezentare. Doi Cai (3…Cf6) — prezentare (cu nota Doi/Trei/Patru Cai).
- 🪤 Capcanele: **1. Fried Liver** (câștigă Albul, mat, Exersează: 6.Cxf7 … Df7#); **2. Capcana șilingului/Blackburne** (câștigă Negrul, …Cf3#, Exersează).
- ⚔️ **Cum pedepsești Fried Liver** (DOAR pedepse, userul a scos apărările Ca5/Fritz): **4…Cxe4** (linia userului din studiul Lichess `fMdmefv9`, mat în 9 …Dxf1#, Exersează) + **Contraatacul Traxler 4…Nc5** (din filmul ei 079; linia FORȚATĂ verificată: 7.Re3 Dh4 = mat, arătat 8.Cxh8 Df4+ 9.Re2 Df2+ 10.Rd3 Cb4+ 11.Rxe4 Df4#).

Chapters 3 (Ca5) și 4 (Fritz) încă există în array dar NU sunt în accData (nefolosite). accData a căpătat și `kind:'defense'` cu eticheta „⚔️ Cum pedepsești Fried Liver".

## Motorul lecțiilor (cum se construiește o lecție nouă)
Model de referință: `nivel6_lectia5.html` (sau `lectia1`). chessboard.js 1.0.0 + chess.js 0.10.3
+ jQuery 3.5.1, piese `caliente` de pe lichess CDN, `master-template.css`, `board-utils.js`.

Structură JS: array `chapters[]` (fen, orient, san[] în SAN **engleză**, ann{} adnotări pe pași,
arrows{} săgeți G/R/B/Y, iar pentru capcane cu Exersează: `winner:'w'|'b'`, `practiceFrom`, `winEval`)
+ array `accData[]` (chIdx, kind:'opening'|'trap'|'defense', num, title, badge, `practice:true/false`, desc).
Secțiuni în acordeon după `kind`: openings (fără titlu de secțiune acum), 🪤 „Capcanele…" (trap), ⚔️ „Cum pedepsești…" (defense).
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

**Stadiu clasificare:** valurile 1+2+3+4 gata (filme 000–113). ~44 capcane utile. **Rămân ~142 filme** (114+; câteva linkuri `/share/r/` au picat la descărcare — de reluat). Capcane noi din val 4: Apărarea Franceză (Alb), Caro-Kann Mate Trap (Alb), Gambitul Danez (Alb), Traxler (film 079, folosit în lecție).
Multe filme sunt de fapt FINALURI (→ Nivel III) sau MODELE DE MAT (→ Nivel V) — se pun deoparte, nu se reprocesează.
Rafturile vizuale cu capcanele clasificate: artifact la `https://claude.ai/code/artifact/49238ac5-9ddd-4d60-820d-57fb33e0bf5b` (16 deschideri cu Albul, 8 cu Negrul; se actualizează cu fiecare val).

**Pe măsură ce se clasifică filmele, se ADAUGĂ capcane la fiecare deschidere existentă** (structura e extensibilă).

## Filozofia deschiderilor (box în fiecare lecție de deschidere)
Fiecare lecție de deschidere are un box `.quote-box` cu două idei, ATRIBUITE CORECT:
- **Aron Nimzovici** — doar: teoria deschiderilor = **jocul marilor maeștri** (o linie a devenit „teorie" pentru că cineva a jucat-o cel mai bine).
- **Christiansen Sava (Chess Architect)** — partea practică: nu memora orbește, înțelege DE CE; din deschidere de obicei **pierzi**, nu câștigi; o capcană merge **doar dacă adversarul greșește** — deci învățăm și cum s-o dăm, și cum să n-o pățim.
Model: `nivel6_lectia5.html` (sub note-box-ul „Ține minte"). **Pune-l în orice deschidere nouă.**
Citare DELICATĂ (cerut de user): NU scrie „Antrenorul Christiansen Sava"; doar numele (link către episodul-sursă) + „Chess Architect" (link `https://chessarchitect.ro/`).

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

## STIL — scrie ca userul (IMPORTANT, cerut 3 aug)
Userul a observat că adnotările deveniseră **exagerate, „ca Gemini"**. Cerință: **exprimă-te ca ea** — limbaj **echilibrat, măsurat**, teacherly, cu câte o glumă din când în când. Evită: abundența de semne de exclamare, grămezile de emoji, cuvintele-hype („SACRIFICIUL!", „LĂCOMIA!", „MAT!", „Frumusețea…", 🏆). Semnele „!" ca notație de șah (4…d5!) sunt OK. Iconițele de structură (🪤/⚔️/📖/💡) sunt OK (navigare, nu ton). Se aplică la adnotările din lecții ȘI la conversație.

**Comentariile userului = ÎNTOCMAI:** când folosești comentariile ei (din studii Lichess), pune-le **exact cum le-a scris**; corectezi DOAR greșeli de tastare, diacritice lipsă, majuscule. NU reformula în stilul tău. (A prins că modificasem comentariile ei — le-am pus înapoi întocmai.)

## Efecte vizuale (la toate lecțiile)
- **Șah ȘI mat:** pătratul regelui în șah primește `.highlight-check` (radial roșu din master-template) — la ORICE șah, nu doar la mat. Helper `checkedKingSquare` (folosește `game.in_check()`, acoperă și matul) → `showCheckHL`. Apelat în studiu (`goToStep`) și în Exersează (`pracRecap`, `pracAttemptMove`, `pracAfterUser`, `pracFinish`). *(Model implementat în `nivel6_lectia5.html`, 6 aug — de copiat pe celelalte lecții.)*
- **Sunete (`Sounds/Move.mp3`, `Capture.mp3`, `Mate.mp3`):** la fiecare mutare — mat→Mate, captură (SAN cu „x")→Capture, altfel→Move. Helper `playMoveSound(san, game)` + `playSnd`. În studiu se aude doar la avans înainte (`s === prevStep + 1`), nu la salt/înapoi; în Exersează la toate mutările. *(Idem: model în lecția 5, de propagat.)*
- **Săgeți:** mici, proporționale cu tabla (`SW = sqSz*0.09`, `markerWidth=4`) — nu mari/fixe (arătau uriașe pe telefon). Aplicat în lecții + `board-utils.js`.

## Resursă: seria „Lupta șahistă" (Chess Architect)
Antrenorul userului, **Christiansen Sava**, are pe YouTube (canal **Chess Architect**, site `chessarchitect.ro`) o serie **„Lupta șahistă — Faza N: <Deschiderea>"** cu descrieri proprii, calde, ale deschiderilor.
- Ep. Partida Italiană: `https://www.youtube.com/watch?v=KjTpoqt27WA` (folosit la intro-ul lecției 5).
- **Caută episodul pentru fiecare deschidere nouă** (Spaniolă etc.) și folosește descrierea LUI la intro. Transcriere: `yt-dlp --skip-download --write-auto-subs --sub-lang "ro"` (videourile-s în română, NU „en").

## CE URMEAZĂ
1. **Partida Spaniolă** (Ruy Lopez) — următoarea deschidere „cu Albul" (după Italiana, înainte de Gambitul Damei). Are nevoie de o capcană „câștigă Albul" (Spaniola avea în rafturi doar capcane pro-Negru — caută una în filmele 084+).
2. Deschideri „cu Negrul": Siciliana, Caro-Kann/Franceză, Gambitul Stafford, Englund, Elephant.
3. Continuă clasificarea filmelor 084+ pe valuri; adaugă capcanele găsite la deschiderea potrivită.
4. `REGULA #1` din CLAUDE.md: **întreabă userul înainte de a începe lucru mare.**
