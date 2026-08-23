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

| `nivel6_intro.html` | **De ce învățăm despre deschideri** | prima pagină a nivelului; doar text + tablă „avanpremieră" (buclă cu primele 3 mutări din Italiana, Spaniola, Gambitul Damei Refuzat/Acceptat, array `openings`) |

**Navigație (footer):** intro → lectia2 → lectia3 → lectia4 → lectia5 (Italiana) → lectia6 (Spaniola) → lectia7 (Vieneza) → lectia8 (Gambitul Regelui) → lectia1 (Gambitul Damei, ultima).

**Regulă (20 aug 2026):** note-box-ul „Ține minte" + quote-box-ul cu filozofia deschiderilor apar **o singură dată**, în `nivel6_intro.html` — au fost scoase din lecțiile 1, 5, 6 și NU se mai pun în lecții noi.
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

## Gambitul Damei — stare la zi (`nivel6_lectia1.html`) (23 aug 2026)
**Episoadele Chess Architect GĂSITE:** „Lupta Șahistă — Faza 1: Gambitul Damei Acceptat"
`https://www.youtube.com/watch?v=nXOg0b6ch8g` și „…Refuzat" `https://www.youtube.com/watch?v=v0M_xKz0Tpc`.
Adăugat cardul „Cum le descrie Christiansen Sava" cu descrierea LUI (jocuri închise / 1.d4; la Acceptat —
control permanent pe e4, atenție la lovitura …e5; la Refuzat — 2.c4 nu oferă un pion, ci amenință pionul
din d5, contează să rămână un grănicer acolo; Apărarea Tarrasch …c5, Siegbert Tarrasch, avută și de Kasparov;
„piatră de încercare" pentru cine joacă 1.d4).

**Corecturi 23 aug:** Albul/Negrul cu majusculă în toate adnotările · **Exersează la toate cele 4 capitole**
(și la deschideri, prin `isOpening`+`practiceFrom`+`finishMsg`, ca la Spaniolă) · **Capcana Elefantului mutată
la secțiunea ⚔️ „Cum pedepsești Albul lacom"**, cu `badge-black` (era 🪤 cu badge verde) și titlu corect
(pedepsești lăcomia de la d5, nu „Gambitul Damei Refuzat") · la capcana …b5, finalul spune concret ce pierde
Negrul (turnul din a8 **sau** pionul b5, în funcție de cum se apără).

## Partida Vieneză (`nivel6_lectia7.html`) și Gambitul Regelui (`nivel6_lectia8.html`) — GATA (23 aug 2026)
Episoade Chess Architect: Vieneza `https://www.youtube.com/watch?v=qiS3TvYlkg0`, Gambitul Regelui
`https://www.youtube.com/watch?v=Qi8XV8WUjiM`. Descrierile LUI sunt în cardurile de intro.

**Vieneza — 5 capitole:** 📖 3.Nc4 (joc liniștit) · 📖 3.g3 (fianchetto) · 📖 3.f4 Gambitul Vienez (răspunsul
corect 3…d5!) · 🪤 pro-Alb **capcana damei la h5** (3…Cxe4?! 4.Dh5! g6?? 5.Dxe5+! → +piesă) ·
⚔️ pro-Negru **capcana turnului din h1** (5.fxe5?? Cxc3 6.bxc3 Dh4+ 7.g3?? De4+! 8.De2 Dxh1).

**Gambitul Regelui — 4 capitole:** 📖 Acceptat (2…exf4, 3.Cf3! împotriva …Dh4+) · 📖 Refuzat (2…Nc5) ·
🪤 pro-Alb **nebunul rătăcit din Contragambitul Falkbeer** (7.De2! Nf2+?? 8.Rd1! — regele NU poate lua,
nebunul e apărat de calul e4; nebunul rămâne prins) · ⚔️ pro-Negru **3.fxe5?? Dh4+! 4.g3 Dxe4+! 5.De2 Dxh1**.

**⚙️ Instrument de verificare (important, de refolosit):** toate liniile au fost verificate cu **Stockfish**,
nu doar cu python-chess. Rețetă: `npm i stockfish` în scratchpad, apoi rulează motorul ca CLI cu
`node node_modules/stockfish/bin/stockfish-18-lite-single.js` (build-ul multithreaded NU merge în node).
Comenzile `position`+`go` trebuie **etalate cu `sleep`** între ele — `position` se execută imediat, deci fără
pauză toate căutările analizează ultima poziție. Scriptul `sfeval.sh` din scratchpad face asta.
Multe „capcane" din cărți nu rezistă la motor (Allgaier, Muzio, capcana coloanei h, Legall în Gambitul
Regelui) — **verifică înainte de a scrie o lecție**.

**Regulă (user, 23 aug):** fiecare deschidere trebuie să aibă **cel puțin 2 capcane**. Plan: încă ~4-5
deschideri **cu Negrul** (Siciliana, Franceza/Caro-Kann, Scandinava, Gambitul Stafford).

## Apărări cu Negrul — 4 lecții noi (23 aug 2026)
`nivel6_lectia9` **Apărarea Rusă + Gambitul Stafford** · `nivel6_lectia10` **Apărarea Philidor** ·
`nivel6_lectia11` **Contragambitul Albin** · `nivel6_lectia12` **Gambitul Budapesta**.

**⚠️ DESCOPERIRE IMPORTANTĂ:** seria „Lupta șahistă — Faza 1" **NU a ajuns încă la jocurile semi-deschise** —
nu există episod pentru Siciliană, Franceză, Caro-Kann sau Scandinavă (playlisturile existente sunt Jocuri
Deschise / Închise / Semi-Închise). De aceea am ales apărări **care AU episod**. De verificat periodic dacă
au apărut episoade noi; abia atunci se pot face lecțiile de Siciliană/Franceză/Caro-Kann/Scandinavă în vocea lui.

**Capcanele (toate verificate cu Stockfish):**
- Rusă: 🪤 **matul din Gambitul Stafford** (6.Ng5?? Cxe4!! 7.Nxd8 Nxf2+! 8.Re2 Ng4#) · ⚔️ **capcana grabei**
  (3…Cxe4?? 4.De2! Cf6?? 5.Cc6+ șah descoperit → câștigă dama).
- Philidor: 🪤 **matul lui Legall** (5.Cxe5!! Nxd1?? 6.Nxf7+ Re7 7.Cd5#) · 🪤 **atacul dublu 7.Db3!** (f7+b7) ·
  ⚔️ **7.Ng5?? Cxe4!** (legarea care nu e legare — nu e regele în spate).
- Albin: 🪤 **capcana Lasker** cu **subpromovare în cal** (7…fxg1=C+!! 8.Txg1 Ng4+ → câștigă dama) ·
  ⚔️ **6.fxe3!** (nu lua nebunul).
- Budapesta: 🪤 **capcana Kieninger** (7.a3?? Cgxe5! 8.axb4?? Cd3# — mat sufocat) · ⚔️ **8.Cxe5!**.

**⚙️ Patch nou în motor (`nivel6_lectia11.html`):** modul Exersează avea `promotion: 'q'` hardcodat, deci
subpromovarea nu putea fi jucată. Acum `pracAttemptMove` citește piesa din SAN-ul așteptat
(`/=([QRBNDTNC])/`) și promovează corect. **De copiat în orice lecție viitoare cu subpromovare.**

**Navigație finală Nivel VI:** intro → 2 → 3 → 4 → 5 (Italiana) → 6 (Spaniola) → 7 (Vieneza) →
8 (Gambitul Regelui) → 9 (Rusa) → 10 (Philidor) → 1 (Gambitul Damei) → 11 (Albin) → 12 (Budapesta, ultima).

## Jocurile semi-deschise — 4 lecții noi, sursa Igor Smirnov (23 aug 2026)
`nivel6_lectia13` **Siciliana** · `nivel6_lectia14` **Franceza** · `nivel6_lectia15` **Caro-Kann** ·
`nivel6_lectia16` **Scandinava**.

**Decizia userului:** fiindcă „Lupta șahistă" nu are (încă) episoade pentru semi-deschise, intro-urile se
scriu după **GM Igor Smirnov** (Remote Chess Academy), traduse din engleză. Fiecare lecție are un
**note-box care spune explicit sursa**. Userul a propus și cartea lui Levy Rozman — nu o folosim: nu o avem
și oricum n-am putea reproduce text dintr-o carte pe un site public.
Transcrieri: `yt-dlp --skip-download --write-auto-subs --sub-lang "en"` pe `@GMIgorSmirnov`.
Videourile folosite: Siciliana `2miolLK8DiI`, Franceza `f0FIJePXmgk`, Caro-Kann `HvER2idtW6M`,
Scandinava `sKoBj-kL0hg`.

**Capcanele (toate arătate de Smirnov, toate verificate cu Stockfish):**
- Siciliana: 🪤 **Dxf2#** în varianta clasică (6.Ne3 Cg4! 7.N-mută Db6! 8.Cb3?? Dxf2#) ·
  ⚔️ **Smith-Morra** (5…Cf6?? 6.e5! dxe5?? 7.Nxf7+! Rxf7 8.Dxd8).
- Franceza: 🪤 **Cxe5** după 5.Nb5?! Nd7 (câștigi un pion) · ⚔️ **9.Nb5+!!** șah descoperit care câștigă
  dama, dacă Negrul capturează pe d4 înainte de …Nd7. Regula lecției: **întâi Nd7, apoi capturi**.
- Caro-Kann: 🪤 **pionul d4** în varianta Înaintată (…Ng4 iese ÎNAINTE de …e6 — diferența față de Franceză) ·
  ⚔️ **Cd6#** mat sufocat (5.De2! Cgf6?? 6.Cd6#) — merge doar în Caro-Kann, în Franceză c7 ar captura ·
  ⚔️ **nebunul prins** cu 4.h4! e6?? 5.g4 și 6.f3.
- Scandinava: 🪤 **Dxf2#** în varianta 2…Cf6 (7.Nd2?? Dxd4! 8.Cf3?? Dxf2#) · ⚔️ **Nxf7#** dacă Negrul
  retrage dama pe d8 (4.Nc4! întâi nebunul, apoi 6.Ce5!! Nxd1?? 7.Nxf7#) — același tipar ca matul lui Legall.

**Nivelul VI e complet acum: 17 pagini** — intro, 3 maturi rapide, 5 deschideri cu Albul
(Italiana, Spaniola, Vieneza, Gambitul Regelui, Gambitul Damei) și 8 apărări cu Negrul
(Rusa/Stafford, Philidor, Siciliana, Franceza, Caro-Kann, Scandinava, Albin, Budapesta).
Fiecare are minimum 2 capcane și Exersează la toate capitolele.

**Navigație finală:** intro → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 13 → 14 → 15 → 16 → 1 → 11 → 12.

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

## Pagina de intro (`nivel6_intro.html`)
Prima pagină a nivelului: „De ce învățăm despre deschideri" (Nimzovici + Christiansen), iar în stânga o **tablă care derulează în buclă primele mutări** din deschiderile nivelului.
**⚠️ La FIECARE lecție nouă de deschidere: adaugă deschiderea în lista `openings` din `nivel6_intro.html`**, în ordinea lecțiilor. Momentan conține: Italiana, Spaniola, Gambitul Damei (Refuzat + Acceptat).

## CE URMEAZĂ
1. ~~Partida Spaniolă~~ — **GATA** (`nivel6_lectia6.html`, 6 aug 2026; corecturi de conținut + Exersează la toate capitolele, 23 aug 2026). De rafinat: episodul Chess Architect exact pentru Spaniolă (creditul e acum doar către canal).
   - Corecturi 23 aug: numele deschiderii (Ruy López a studiat-o, nu a inventat-o) + regula generală de denumire; „pune presiune"/„face rocada" peste tot; explicat de ce nu 5…Cxe4 la Morphy; Berlineza — Kramnik a jucat-o **cu negrele**; Tarrasch — regele nu mai e pe coloana e după rocadă, nebunul e7 rămâne neapărat la 14.f3, turnul din d8 e **atacat**, nu legat, coloana d se deschide pentru Ta1; Mortimer — calul de pe c4 apără a5; 7.Cc3 apără nebunul a4. Capitolul **Anastasia a fost scos** (linia nu era autentică — 11…d6 nu e o mutare firească).
   - **Exersează activ la toate cele 7 capitole** (inclusiv deschiderile) prin `practiceFrom` + `winner` + `isOpening` + `finishMsg`. La `isOpening` bara de evaluare e ascunsă și mesajul e „Joacă mutarea din deschidere". **Model de copiat pe lecțiile viitoare.**
   - La Tarrasch, mutarea 13: explicat de ce Albul face **scut cu propriul cal** (13.Cd3!) în loc să ia calul negru — după 13.Txe4?? vine 13…Td1+! 14.Te1 Txe1#, mat pe ultima linie (turnul din a1 e blocat de propriul nebun din c1).
2. Deschideri „cu Negrul": Siciliana, Caro-Kann/Franceză, Gambitul Stafford, Englund, Elephant.
3. Continuă clasificarea filmelor 084+ pe valuri; adaugă capcanele găsite la deschiderea potrivită.
4. `REGULA #1` din CLAUDE.md: **întreabă userul înainte de a începe lucru mare.**
