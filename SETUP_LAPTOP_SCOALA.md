# Setup pe laptopul de la școală

Scris pe 24.09.2026. Scopul: să pot repara site-ul `laboratoruldesah.ro` direct de la școală,
de pe tabla cu touch, fără să car laptopul acasă și înapoi.

De citit de pe GitHub, direct pe laptopul de la școală, înainte de instalare:
`github.com/irinabaitel/sah-mat-animat` → fișierul `SETUP_LAPTOP_SCOALA.md`

---

## 1. Ce se instalează

Cinci lucruri, în ordinea asta. Toate se instalează o singură dată.

### VS Code
De pe `code.visualstudio.com`, butonul mare de Download for Windows.
La instalare, pe ecranul cu opțiuni suplimentare, bifează **„Add to PATH"** —
altfel comanda `code` nu merge din terminal. Restul, implicit.

Acasă e versiunea 1.139.0, instalată pe contul tău (nu pentru tot calculatorul).

### Node.js
De pe `nodejs.org`, versiunea **LTS** (cea din stânga, nu cea „Current").
Instalare cu opțiunile implicite, next-next-finish.

### Git for Windows
De pe `git-scm.com`. Tot cu opțiunile implicite — sunt multe ecrane, nu trebuie schimbat nimic.

### GitHub CLI
După ce ai Git, deschizi **PowerShell** și scrii:

```
winget install GitHub.cli
```

Închizi PowerShell și îl deschizi din nou (ca să vadă programul nou instalat), apoi:

```
gh auth login
```

Alegi pe rând: `GitHub.com` → `HTTPS` → `Yes` (să folosească datele pentru Git) →
`Login with a web browser`. Îți arată un cod de opt caractere, îl copiezi, se deschide
browserul, îl lipești acolo și confirmi.

Contul cu care te loghezi: **irinabaitel** (proprietarul repo-ului)

### Claude Code

```
npm install -g @anthropic-ai/claude-code
```

Apoi îl pornești cu comanda `claude` și te loghezi cu contul Claude.

---

## 2. Aducerea site-ului pe laptop

Pe 24.09.2026 repo-ul a fost curățat: de la 991 MB la 166 MB. Materialele de lucru
(manualele Stappen, planificările, seturile de piese nefolosite, fișierele de filtrare
a puzzle-urilor) au fost mutate pe discul de acasă, în folderul `Sah - materiale`.
Deci clonarea normală durează acum două-trei minute.

```
cd C:\Users\irina
git clone https://github.com/irinabaitel/sah-mat-animat.git SahMatAnimat
```

Verifici că a mers:

```
cd SahMatAnimat
dir
```

Trebuie să vezi `index.html`, `hub.html`, `master-template.css`, `board-utils.js`
și paginile de lecție.

---

## 3. Cum lucrezi, zi de zi

Site-ul e pe GitHub Pages. Nu există panou de administrare și nu există FTP.
**A repara site-ul înseamnă commit și push.** După push, în una-două minute
modificarea e live pe `laboratoruldesah.ro`.

### Pornirea

1. Deschizi **VS Code**.
2. **File → Open Folder**, alegi `C:\Users\irina\SahMatAnimat`.
   (A doua oară îl găsești direct în File → Open Recent.)
3. Deschizi terminalul: meniul **Terminal → New Terminal**.
   Scurtătura e `Ctrl` + tasta de deasupra lui `Tab`, dar pe tastatura românească
   e mai simplu prin meniu.
4. În terminal scrii:

```
claude
```

De aici încolo totul se întâmplă în discuția cu Claude: îi spui ce e de reparat,
el caută prin fișiere, modifică și dă push. Fișierele se văd în stânga, deci poți
urmări ce se schimbă.

### Prima dată, o singură dată

La prima pornire a lui `claude` ți se cere să te loghezi cu contul Claude —
se deschide browserul, confirmi, gata.

Extensia Claude Code pentru VS Code se instalează singură când pornești `claude`
din terminalul VS Code. Nu trebuie căutată în magazinul de extensii.

### Automatizarea: pull la pornire și amintirea de push

Pe fiecare dispozitiv, Claude poate face singur `git pull` când pornește și îți poate
aminti de push când ai modificări netrimise. Setările astea **nu vin de pe GitHub**,
fiindcă folderul `.claude` e exclus din repo, deci trebuie refăcute pe fiecare dispozitiv nou.

După prima pornire a lui `claude` în folderul proiectului, îi spui:

> Refă automatizarea: git pull automat la pornire și amintirea de push
> când am modificări netrimise.

Intră în funcțiune de la următoarea pornire a lui `claude`.

### La final

Îi spui lui Claude să dea push, sau scrii tu în terminal:

```
git add -A
git commit -m "ce am schimbat"
git push
```

---

## 4. REGULA CELOR DOUĂ LAPTOPURI

Asta e partea care poate strica lucruri, deci merită citită de două ori.

Ai acum două calculatoare care scriu în același proiect. Dacă modifici în amândouă
locurile fără să sincronizezi, Git nu mai știe care versiune e bună și apare un
conflict — mai neplăcut de reparat decât un fișier duplicat în OneDrive.

**Când te apuci de lucru, oriunde ai fi:**

```
git pull
```

**Când termini, înainte să pleci de la laptop:**

```
git add -A
git commit -m "ce am schimbat"
git push
```

Dacă respecți asta, nu ai niciodată probleme. Dacă uiți o dată, se rezolvă, dar cere ajutor
înainte să încerci să repari singură.

### Cum verifici că e totul sincronizat

```
git status
```

Dacă scrie `nothing to commit, working tree clean` și `Your branch is up to date`,
poți pleca liniștită.

---

## 5. De verificat pe tabla cu touch

Lucrurile care se strică de obicei doar pe touchscreen, nu și pe laptop cu mouse:

- tragerea pieselor cu degetul (drag-and-drop) pe tablele interactive
- derularea paginii când degetul pornește de pe o tablă
- butoanele mici din arene (◄ ► și cele de control)
- adnotările cu apăsare lungă

Fișierul `board-utils.js` se ocupă de traducerea atingerilor în clicuri
și trebuie inclus în **orice** pagină cu tablă interactivă. Dacă o tablă nu răspunde
la deget, primul lucru de verificat e dacă pagina are linia aceea de `script`.

---

## 6. Dacă ceva nu merge

Erori frecvente la instalare:

**`npm` sau `git` nu e recunoscut ca o comandă**
Programul s-a instalat, dar terminalul a fost deschis înainte. Închide PowerShell
și deschide-l din nou.

**`gh auth login` dă eroare de rețea**
Rețeaua școlii poate bloca unele adrese. Încearcă de pe hotspotul telefonului.

**Clona se oprește la jumătate**
Ștergi folderul pe jumătate descărcat și reiei comanda de clonare.
Dacă tot pică, încearcă de pe hotspot.

---

## 7. Unde sunt materialele de lucru

Nu mai sunt în repo. Pe 24.09.2026 au fost mutate pe laptopul de acasă, în
`C:\Users\irina\Sah - materiale`, păstrând aceeași structură de foldere:

- manualele Stappen (`Metoda step - manualul profesorului`)
- planificările școlare (`planificari educatie prin sah`)
- modulele de curs (`chess coach ready`)
- seturile de piese generate, nefolosite pe site (`piese_sah`)
- fișierele intermediare de la filtrarea puzzle-urilor (`data/*_candidates.json`)

Dacă ai nevoie de vreunul la școală, se copiază pe stick sau prin OneDrive —
nu se pun înapoi în repo, fiindcă `.gitignore` le ține deoparte intenționat.

Copia repo-ului de dinainte de curățare, cu toată istoria veche, e la
`C:\Users\irina\Sah - BACKUP repo 2026-09-24`.
