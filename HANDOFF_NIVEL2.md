# HANDOFF — Nivelul II „Planuri și principii"

> Document de continuitate pentru Nivelul II. Actualizat: 23 august 2026.

## Ce este Nivelul II
Strategia — jocul de mijloc. Stă între Nivelul I (bazele) și Nivelurile III–VI.
Răspunde la întrebarea **„ce fac acum?"**, după ce piesele sunt scoase.

## Sursa: „Lupta șahistă — Faza 2" (Chess Architect)
Seria antrenorului userului are un **Faza 2 complet**, exact despre jocul de mijloc.
Cele 6 episoade (plus intro-ul, care e ACELAȘI material cu „Elaborarea Scenariilor" — o reîncărcare):
- Elaborarea Scenariilor — `ZggLDjjIp7c` (transcriere mai curată) / duplicat `ZlYh21-jIrU`
- Avantajul de Dezvoltare — `9PPbjDR4EVg`
- Avantajul de Spațiu — `KnHv8h6eUew`
- Perechea de Nebuni — `jy-SM3B-ik8`
- Isolani (pionul izolat) — `A3YBPRirncA`
- Principiul celor două slăbiciuni — `dbZUyN5e3JM`

Există și playlistul „Șah - Strategie" cu serii mai lungi (Avantajul de Spațiu 1–7, Perechea de Nebuni 1–3)
și „Tactica jocului de șah — Atacul asupra punctului h2/h7 (1) și (2)" — utile pentru lecțiile din Blocul 3.

## Planul convenit cu userul (23 aug 2026): 12 lecții, TOATE
**Bloc 1 — ce se întâmplă după deschidere**
1. ✅ `nivel2_lectia1.html` — Fazele jocului și obiectivele lor *(exista deja)*
2. ✅ `nivel2_lectia2.html` — **Elaborarea scenariilor** *(gata 23 aug — LECȚIA-MODEL)*

**Bloc 2 — avantajele mici (toate au episod)**
3. Avantajul de dezvoltare · 4. Avantajul de spațiu · 5. Perechea de nebuni ·
6. Isolani — pionul izolat · 7. Principiul celor două slăbiciuni

**Bloc 3 — ce lipsea din tot curriculumul (fără episod)**
8. Structura de pioni (dublați, izolați, atârnați, lanțuri, pionul trecut)
9. Coloana deschisă, linia a 7-a, bateria de turnuri
10. Nebun bun / nebun rău; calul pe avanpost; nebun contra cal
11. Când schimbi piese și când nu
12. Siguranța regelui după rocadă (se leagă de „atacul asupra punctului h7")

**Decizii ale userului:** finalurile de pioni (opoziția, regula pătratului, pionul trecut) **NU** intră aici —
merg la **Nivelul III**, care rămâne la locul lui. Nu există încă nicăieri pe site.

## FORMATUL LECȚIEI DE STRATEGIE (confirmat de user) — model: `nivel2_lectia2.html`
Motorul e cel din Nivelul VI (`nivel6_lectia6.html`) — tablă + acordeon + derulare ◄ ► + Exersează.
**Trei diferențe față de lecțiile de deschidere:**
1. Capitolele sunt **fragmente din partide adevărate**, comentate mutare cu mutare.
2. **„Alege planul"** — tip nou de item în `accData`: `kind: 'quiz'` cu
   `quiz: { q, opts: [{ t, ok, fb, go }] }`. Se randează ca 3 butoane; la click marchează
   corect/greșit, arată explicația, iar `go: <chIdx>` adaugă un buton „▶ Vezi scenariile pe tablă"
   care deschide capitolul respectiv. Funcția e `wireQuiz()`. Itemii `quiz` **nu au tablă proprie**
   (`openAcc` iese devreme dacă `dataset.kind === 'quiz'`).
3. `practice` e din nou **controlat de flag** (`d.practice`), nu pus pe toate — capitolul cu partida
   întreagă e doar de derulat. Butonul se numește „🤖 Joacă tu mutările".
CSS nou: `.plan-q`, `.plan-btns`, `.plan-btn` (+ `.ok` / `.nope`), `.plan-fb`, `.plan-go`.

## Lecția 2 — ce conține
Partida **Karpov–Topalov, Dos Hermanas 1994** (partida pe care o analizează chiar el).
Momentul-cheie: după 17…hxg6, Karpov joacă **18.Cc5!** fiindcă nebunul negru din d7 e slab apărat.
Cele trei scenarii ale lui: 18…dxc5 19.Dxd7 · 18…Dc7 19.Cxd7 · 18…Ne8 19.Cxe6!
(pe al treilea, motorul confirmă +2.3 pentru Alb). Partida reală continuă 19…Tc8 20.Txe6! Ta7
21.Txg6+!! fxg6 22.De6+ Rg7 23.Nxc6 — tot nebunul din g2, pregătit la mutarea 6.
Ideea pedagogică pe care o subliniază: **mai bine mai multe scenarii scurte decât unul lung**.

## De ținut minte
- Toate liniile se verifică cu Stockfish — vezi rețeta din `HANDOFF_NIVEL6.md`.
- Cardul de intro se scrie în **vocea lui Christiansen**, din transcriere (`yt-dlp --sub-lang ro`).
- Fiecare lecție nouă se adaugă în `hub.html`, la cardul Nivelului II, și se leagă în footere.
