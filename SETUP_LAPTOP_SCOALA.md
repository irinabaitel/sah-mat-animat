# Setup pe laptopul de la școală

Scris pe 24.09.2026. Scopul: să pot repara site-ul `laboratoruldesah.ro` direct de la școală,
de pe tabla cu touch, fără să car laptopul acasă și înapoi.

De citit de pe GitHub, direct pe laptopul de la școală, înainte de instalare:
`github.com/irinabaitel/sah-mat-animat` → fișierul `SETUP_LAPTOP_SCOALA.md`

---

## 1. Ce se instalează

Patru lucruri, în ordinea asta. Toate se instalează o singură dată.

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

Contul cu care te loghezi: **irinabaitel-jpg**

### Claude Code

```
npm install -g @anthropic-ai/claude-code
```

Apoi îl pornești cu comanda `claude` și te loghezi cu contul Claude.

---

## 2. Aducerea site-ului pe laptop

Atenție: repo-ul are aproape 1 GB de istorie. Nu-l clona normal, că stai mult
pe internetul școlii. Iei doar ultima versiune:

```
cd C:\Users\irina
git clone --depth 1 https://github.com/irinabaitel/sah-mat-animat.git SahMatAnimat
```

Asta aduce câteva zeci de MB în loc de 991. Poți edita și poți da push normal.
Singurul lucru care nu merge e căutatul prin commit-uri vechi, de care n-ai nevoie
ca să repari un buton.

Verifici că a mers:

```
cd SahMatAnimat
dir
```

Trebuie să vezi `index.html`, `hub.html`, `master-template.css`, `board-utils.js`
și paginile de lecție.

---

## 3. Cum se repară ceva

Site-ul e pe GitHub Pages. Nu există panou de administrare și nu există FTP.
**A repara site-ul înseamnă commit și push.** După push, în una-două minute
modificarea e live pe `laboratoruldesah.ro`.

Pornești Claude Code din folderul repo-ului:

```
cd C:\Users\irina\SahMatAnimat
claude
```

Și îi spui ce e de reparat. La final, commit și push.

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
Ștergi folderul pe jumătate descărcat și reiei comanda cu `--depth 1`.
Dacă tot pică, încearcă de pe hotspot.

---

## 7. De făcut cândva, nu acum

Repo-ul are 991 MB de istorie pentru un site de fișiere HTML. Înseamnă că au intrat
în istoric fișiere mari — probabil imagini sau video care nu mai sunt folosite.
Se poate curăța, dar e o operație care rescrie istoria și se face o singură dată,
cu atenție, de pe un singur laptop.
