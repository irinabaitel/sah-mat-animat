# Laptopul pe tabla de la școală, fără fir (Win + K)

Tabla e un calculator cu Windows, numit **DESKTOP-4D54D6O**. Ca să primească imaginea de la laptop, tabla are nevoie de funcția **„Wireless Display”**.

## Ce s-a întâmplat (3 nov. 2026)

O zi a mers, a doua zi nu. În Setări, la *Projecting to this PC*, tabla scria din nou **„Add the Wireless Display optional feature”**, adică funcția instalată în ziua dinainte **dispăruse**.

Cea mai probabilă cauză: **tabla se „resetează” la fiecare repornire.** Multe școli pun un program de protecție care șterge tot ce s-a schimbat peste zi: programe instalate, setări, fișiere. Atunci Win + K de pe laptop nu mai găsește tabla, pentru că tabla nu mai „ascultă”.

**Cum verifici:** lasă pe desktopul tablei un fișier gol, de exemplu `test.txt`. Dacă a doua zi a dispărut, tabla se resetează.

## Soluția bună: o dată, de către informatician

Roagă-l pe informaticianul școlii (sau pe cel care are parola de administrator a tablei) să instaleze **„Wireless Display”** pe tabla DESKTOP-4D54D6O **astfel încât să rămână** după repornire. El știe ce protecție e pusă și cum o oprește pe timpul instalării.

## Până atunci: pașii, în fiecare zi (cam 5 minute)

**Pe tablă** (nu are tastatură: pentru căutări folosește tastatura de pe ecran):
1. Start → Settings → caută **Projecting** → *Projecting to this PC*.
2. Apasă **Optional features** → **View features** (sau *Add a feature*) → caută **Wireless Display** → bifează → **Next** / **Install**. Durează câteva minute și are nevoie de internet.
3. Întoarce-te la *Projecting to this PC*. Acum apar opțiunile:
   - primul meniu: **Available everywhere**;
   - *Ask to project to this PC*: **First time only**;
   - *Require PIN for pairing*: **Never**.
4. Pornește aplicația **Connect** de pe tablă (Start → scrie „Connect”).

**Pe laptop:**

5. Wi-Fi pornit.
6. Apasă **Win + K** → alege **DESKTOP-4D54D6O**. Dacă tabla întreabă, acceptă pe tablă.
7. Ca să poți lucra **cu degetul pe tablă** în laptop: după conectare, în fereastra Win + K de pe laptop, bifează **„Allow input from a keyboard or mouse connected to this display”** (permite atingerea și tastatura de pe tablă).
8. **Gata?** Win + K → **Disconnect**.

## Dacă nu apare tabla la Win + K

- Pe tablă e deschisă aplicația **Connect**? (pasul 4)
- Pe tablă scrie din nou „Add the Wireless Display optional feature”? Atunci s-a resetat: reia de la pasul 2.
- Wi-Fi-ul e pornit **pe ambele** (laptop și tablă)?
- Pune-le pe **aceeași rețea Wi-Fi, Elevi_Dante**, setată **Private** pe amândouă (Settings → Network & internet → Wi-Fi → rețeaua → *Network profile type: Private*). Asta e configurația care **a mers**.

**De ținut minte:** tabla devine „descoperibilă” din *Projecting to this PC* (primul meniu: **Available everywhere**), iar meniul ăsta apare **doar după** ce e instalat Wireless Display.

## Cu cablu (din 4 nov. 2026)

Fără fir n-a mers cu **laptopul Dell de la școală** (mai vechi), nici la tablă, nici la televizorul de acasă: găsea televizorul, dar nu se conecta. Laptopul de acasă (Lenovo) știe să proiecteze fără fir. Acum folosesc **cablu HDMI**.

1. Cablul HDMI: laptop → intrarea HDMI a tablei.
2. Pe tablă: alege sursa **HDMI** (din meniul tablei, de obicei de pe butonul de sursă / *Input* / *Source*).
3. Pe laptop: **Win + P** → **Duplicate** (aceeași imagine pe ambele) sau **Second screen only**.
4. **Ca să meargă cu degetul pe tablă:** pe lângă HDMI mai trebuie un **cablu USB** de la portul **Touch** al tablei (scrie „Touch” sau „USB Touch” lângă HDMI) la laptop. Fără el, vezi imaginea, dar atingerea nu ajunge la laptop.

**Dacă vrei să afli dacă Dell-ul poate proiecta fără fir:** în PowerShell scrie `netsh wlan show drivers` și caută rândul **Wireless Display Supported**. Dacă scrie **No**, Dell-ul nu poate, și cablul rămâne singura variantă.
