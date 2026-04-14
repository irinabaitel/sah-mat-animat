# Turneu Swiss de Șah — Instrucțiuni pentru Profesor

## Ce trebuie instalat (o singură dată)
- **Node.js**: descarcă și instalează de pe https://nodejs.org (versiunea LTS)

---

## Pornirea serverului (în ziua turneului)

1. Deschide folderul `turneu/`
2. **Dublu-click pe `start.bat`**
3. Aștepți să apară mesajul cu IP-ul (ex: `http://192.168.1.15:3000`)
4. Lasă această fereastră deschisă tot turneul

---

## Accesul elevilor

Elevii deschid browserul și merg la:
```
http://[IP-ul din consolă]:3000
```
*(sau exact ce scrie în consolă — ex: `http://192.168.1.15:3000`)*

Fiecare elev:
- Intră pe acea adresă
- Scrie **numele** lui
- Click "Intru în turneu"
- Așteptă în **sala de așteptare**

---

## Panoul de control (profesor)

```
http://[IP]:3000/admin.html
Parola: prof
```

### Pași turneu:

1. **Aștepți** până toți elevii se conectează (vezi lista din stânga)
2. Click **"Pornește Runda 1"** → perechi generate automat
3. Elevii joacă (mutări în timp real, table separate)
4. Când toate jocurile s-au terminat → apare **"Pornește Runda 2"**
5. Repezi pașii 2-4 pentru 4-5 runde
6. La final: click **"Finalizează Turneul"** → toți văd clasamentul

### Butoane utile în admin:
- **Forțează rezultat** (1-0 / 0-1 / ½) — dacă un joc e blocat
- **× Scoate jucător** — dacă cineva trebuie eliminat (doar în lobby)
- **Reset Complet** — șterge totul și reia de la zero

---

## Număr de runde recomandat

| Participanți | Runde |
|---|---|
| 8-16 | 4 runde |
| 17-32 | 5 runde |
| 33-64 | 6 runde |

**Pentru 28 de copii → 5 runde** (~50-60 min total cu jocuri de 10 min)

---

## Punctaj Swiss (standard)
- **Victorie** = 1 punct
- **Remiză** = ½ punct  
- **Pierdere** = 0 puncte
- **BYE** (număr impar) = 1 punct automat

---

## Problemă frecventă: elevul nu se poate conecta

- Verifică că PC-ul profesorului și tabletele/laptopurile elevilor sunt pe **aceeași rețea WiFi**
- Dezactivează temporar **firewall-ul Windows** pe PC-ul profesor (sau adaugă o regulă pentru portul 3000)

### Dezactivare rapidă firewall (doar în rețeaua școlii!):
```
Control Panel → Windows Defender Firewall → Turn off
```
(reactivează după turneu)
