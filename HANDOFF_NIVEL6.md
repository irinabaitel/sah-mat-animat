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
| `nivel6_lectia6.html` | **Partida Spaniolă** | 2 intro (Morphy, Berlin) + 4 capcane, toate verificate python-chess ȘI chess.js 0.10.3 — vezi secțiunea dedicată mai jos |
| `nivel6_lectia1.html` | **Gambitul Damei** | Refuzat/Acceptat + lăcomia …b5 (Alb) + Capcana Elefantului (Negru) |

**Navigație (footer):** lectia2 → lectia3 → lectia4 → lectia5 (Italiana) → lectia6 (Spaniola) → lectia1 (Gambitul Damei).
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

## Partida Spaniolă — stare la zi (`nivel6_lectia6.html`) — GATA (6 aug 2026)
**Intro:** def-box „Ce este Partida Spaniolă?" (bazat pe textul cerut de user + ton echilibrat, „leagă" nu „pironit"), card cu cele 4 răspunsuri (Morphy 3…a6, Berlin 3…Cf6, Steinitz 3…d6, Schliemann 3…f5), quote-box Nimzovici+Chess Architect.
**Episodul Chess Architect pentru Spaniolă GĂSIT (7 aug):** „Lupta Șahistă — Faza 1: Partida Spaniolă"
`https://www.youtube.com/watch?v=3TXHuFSCK9s`. Am adăugat un card „Cum o descrie Christiansen Sava"
cu descrierea LUI (transcriere `yt-dlp --write-subs --sub-lang ro`): regina jocurilor deschise, cel mai
principial sistem deschis; amenințarea de la 3.Nb5 care „planează" dar nu poate fi dusă la capăt acum;
de ce nu schimbă pe c6 (perechea de nebuni); frontiera c+d și expansiunea lentă; „tortura spaniolă"
de pe vremea lui Karpov; sfatul „dacă ești temperamental, nu juca Spaniola". Toate linkurile de credit
din lecție duc acum la episodul exact.

**7 capitole (toate verificate python-chess ȘI chess.js 0.10.3):**
- 📖 Ch0 Morphy (3…a6, linia clasică) · Ch1 Berlin (3…Cf6 → finalul Berlin, povestea Kramnik-Kasparov 2000).
- 🪤 pro-Alb (secțiune „Capcanele din această deschidere"): **Ch2 Tarrasch–Marco 1892** (Steinitz; greșeala 7…O-O??; câștig piesă la 18.c4; `practice:false` — 18 mutări, tehnică) · **Ch3 mat sufocat Mortimer** Cd6# (greșeala 6…cxb5??; refutare 6…d6!; `practice:false` fiindcă Albul dă nebunul înainte de mat = bara eval ar deruta) · **Ch4 Anastasia în Berlin** (…Dxh7+!! Th5#; **NU e forțat** — 11…Dxe7! salvează; marcat onest; `practice:false`).
- ⚔️ pro-Negru (secțiune „Cum pedepsești Albul lacom"): **Ch5 Arca lui Noe** (greșeala 8.Dxd4??; …c4! prinde nebunul b3; `practice:true`, winner 'b', practiceFrom:11) · **Ch6 Mortimer …Da5+** (greșeala 5.Cxe5??; furculiță câștigă calul; `practice:true`, winner 'b', practiceFrom:7).

**Observația frumoasă (Mortimer are ambele fețe din ACEEAȘI poziție):** după 4…Ce7 5.Cxe5 c6 — 6.Na4? → Negrul câștigă cu 6…Da5+ (Ch6); 6.Cc4! → Albul dă mat sufocat dacă Negrul se lăcomește 6…cxb5?? 7.Cd6# (Ch3). Adnotările se referă reciproc.

**Sursele:** 2 reel-uri FB ale userului — reel `1012679151230348` = Berlin/Anastasia (Ch4); reel `1649887902766531` = Mortimer …Da5+ (Ch6). Matul sufocat (Ch3) găsit de un agent. Arca lui Noe (Ch5) și Tarrasch (Ch2) = clasice, aduse de mine. Toate verificate cu `scratchpad/try_line.py`.

**Regulă nouă (user, 6 aug):** limita capcanelor ridicată 10→**20 mutări**. Și: în comentarii **marchează explicit mutarea-greșeală** care duce la înfrângere/pierdere de material (vezi memoria `feedback_marcheaza_mutarea_pierzatoare`).

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
`python tools/try_line.py "e4 e5 Bc4 ..."` (mutat din `scratchpad/` în `tools/`, ca să fie în repo
și pe tabletă; `scratchpad/` e acum în `.gitignore` — acolo stau doar filme/cadre temporare) → spune dacă toate mutările sunt legale + dacă e MAT.
Userul urăște erorile de șah (ex. „furculiță pe pion apărat"). Reconstrucția din cadre video e
NESIGURĂ pentru linii demonstrative → **când e greu, cere userului să pună linia în studiul ei Lichess**
(xMvnWhmH) și importă PGN cu `?comments=true` (workflow care merge mereu).

## Workflow filme Facebook/YouTube (pentru capcane noi)
Userul a strâns ~253 filmulețe FB. **ATENȚIE (7 aug):** `scratchpad/fb_links.txt` și
`scratchpad/grab_wave.py` **NU mai există** — au fost șterse odată cu curățarea spațiului de lucru.
Când se reia clasificarea filmelor 114+, trebuie cerută userului din nou lista de linkuri și rescris
scriptul de descărcare (rețeta e mai jos). Pipeline:
1. `grab_wave.py START COUNT` → descarcă (yt-dlp, fără login) + taie cadre (ffmpeg din imageio-ffmpeg). Sare filmele >360s.
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
- Deschiderea se prezintă pe 4–6 mutări, scopul fiecărei mutări. **Max 20 mutări per capcană.** (ridicat de la 10 → 20, cerut de user 6 aug 2026 — deblochează linii mai lungi ca Tarrasch în Spaniolă.)
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
- **Cum găsești episodul unei deschideri:**
  `yt-dlp --flat-playlist --print "%(title)s ||| %(url)s" "https://www.youtube.com/@ChessArchitect/search?query=Lupta%20%C8%99ahist%C4%83"`
  Seria are episoade (Faza 1) pentru: Italiana, Spaniola, Vieneza, Doi Cai, Gambitul Regelui, Gambitul Evans,
  Gambitul Nordic, Gambitul Danez/Central, Ponziani, Philidor, Apărarea Rusă, Deschiderea Owen, Deschiderea
  Nebunului, Apărarea Modernă, Mexicana, Chigorin, Baltică, Slavă, Marshall, Albin, Ben-Oni, Volga, Budapesta,
  Indiana Veche, Olandeza (3 variante), Gambitul Damei Acceptat/Refuzat, Jocuri Deschise/Închise/de Flanc.
  Fazele 2 și 3 = strategie/finaluri (utile pentru Nivel II și III).
- **Caută episodul pentru fiecare deschidere nouă** și folosește descrierea LUI la intro. Transcriere: `yt-dlp --skip-download --write-auto-subs --sub-lang "ro"` (videourile-s în română, NU „en").

## CE URMEAZĂ
1. ~~Partida Spaniolă~~ — **GATA** (`nivel6_lectia6.html`, 6 aug 2026). De rafinat: episodul Chess Architect exact pentru Spaniolă (creditul e acum doar către canal). Opțional: de decis cu userul dacă matul sufocat Mortimer (Ch3) merită `practice:true` în ciuda barei de eval.
2. Deschideri „cu Negrul": Siciliana, Caro-Kann/Franceză, Gambitul Stafford, Englund, Elephant.
3. Continuă clasificarea filmelor 084+ pe valuri; adaugă capcanele găsite la deschiderea potrivită.
4. `REGULA #1` din CLAUDE.md: **întreabă userul înainte de a începe lucru mare.**
