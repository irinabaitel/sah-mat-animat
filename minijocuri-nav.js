/* =====================================================
   MINIJOCURI — navigare comună + ajutoare
   - Subsolul: Cuprins + Jocul următor (ordinea din hub).
   - „Înapoi" apare doar dacă ai venit dintr-o lecție.
   - minigameHideHints(): la nivelul Dragon nu arătăm unde poate muta piesa.
   ===================================================== */
(function () {
    var GAMES = [
        ['joc_pioni.html',           'Jocul Pionilor'],
        ['joc_stockfish.html',       'Regi și Pioni'],
        ['joc_mcdonald.html',        'Old McDonald'],
        ['nivel1_joc_cai.html',      'Jocul Cailor'],
        ['nivel1_joc_cursa.html',    'Cursa Perimeterului'],
        ['nivel1_joc_acasa.html',    'Întoarcerea Acasă'],
        ['nivel1_joc_dama_cal.html', 'Dama contra calului'],
        ['nivel1_joc_nasturi.html',  'Vânătoarea de nasturi'],
        ['nivel1_joc_dama_turn_nebun.html', 'Dama și turnul contra nebunului'],
        ['nivel1_joc_cai_lacomi.html', 'Cursa cailor'],
        ['nivel1_joc_drumul_regelui.html', 'Drumul regelui spre castel'],
        ['nivel1_joc_cursa_obstacole.html', 'Cursa cu obstacole'],
        ['nivel1_joc_piesa_contra_pionilor.html', 'Piesa contra pionilor'],
        ['nivel1_joc_dama_contra_pionilor.html', 'Dama contra pionilor'],
        ['nivel1_joc_vanatoarea_regelui.html', 'Vânătoarea regelui'],
        ['nivel1_joc_regi_nasturi.html', 'Regii și diamantele'],
        ['nivel1_joc_cine_pastreaza.html', 'Cine păstrează ceva?'],
        ['joc_sah_progresiv.html', 'Șahul progresiv'],
        ['joc_sah_pierzator.html', 'Șahul pierzătorului'],
        ['joc_trei_sahuri.html', 'Trei șahuri'],
        ['joc_stockfish.html?v=2',   'Regi și Pioni 2'],
        ['joc_klotz.html', 'Klotz']
    ];
    var file = function (p) { return (p || '').split('?')[0].split('#')[0].split('/').pop(); };
    var here = file(location.pathname);
    /* un joc poate fi aceeași pagină cu alt parametru (ex. joc_stockfish.html?v=2): alegem potrivirea cea mai precisă */
    var i = -1, best = -1;
    for (var k = 0; k < GAMES.length; k++) {
        var parts = GAMES[k][0].split('?');
        if (parts[0] !== here) continue;
        var q = parts[1] || '';
        if (q && location.search.indexOf(q) < 0) continue;
        if (!q && /[?&]v=2/.test(location.search)) continue;
        if (q.length > best) { best = q.length; i = k; }
    }

    /* lecția de unde ai venit: aceeași origine, nu hub/index, nu alt minijoc */
    var lessonUrl = null, lessonKey = 'minijoc-from-lesson';
    try {
        if (document.referrer) {
            var ref = new URL(document.referrer);
            var rf = file(ref.pathname);
            var isGame = GAMES.some(function (g) { return g[0].split('?')[0] === rf; });
            if (ref.origin === location.origin && rf && !isGame && !/^(hub|index)\.html$/.test(rf) && /\.html$/.test(rf)) {
                lessonUrl = ref.pathname + ref.search;
                sessionStorage.setItem(lessonKey, lessonUrl);
            } else if (/^(hub|index)\.html$/.test(rf) || !isGame) {
                sessionStorage.removeItem(lessonKey);
            } else {
                lessonUrl = sessionStorage.getItem(lessonKey);   // treci de la un joc la altul: păstrăm lecția
            }
        }
    } catch (e) {}

    window.minigameNextUrl = i >= 0 && i < GAMES.length - 1 ? GAMES[i + 1][0] : null;

    window.minigameHideHints = function () {
        var b = document.querySelector('.animal-btn.active');
        if (!b || !/Dragon/.test(b.textContent)) return false;
        /* caseta de niveluri ascunsă explicit (modul „În doi") = indiciile rămân;
           altfel contează doar nivelul ales, chiar dacă panoul de setări nu se vede în timpul partidei */
        var box = document.getElementById('levelBox');
        if (box && box.contains(b)) return box.style.display !== 'none';
        return b.offsetParent !== null;
    };

    /* Cât „se gândește” Robotul, în milisecunde. Cu cât e mai puternic, cu atât se hotărăște mai repede:
       Pui de găină 3–7 s, Mânz 2–5 s, Dragon 1–3 s; la primele mutări de două ori mai repede.
       level: 'pui' | 'manz' | 'dragon' (sau 1 | 2 | 3); msLeft: timpul rămas pe ceasul lui (null = fără ceas);
       plies: câte mutări s-au jucat. Cu ceas, împarte timpul rămas ca pentru încă 30 de mutări
       (sub 10 secunde, pentru 60), ca să nu piardă la timp. */
    window.minigameThinkMs = function (level, msLeft, plies) {
        var L = { 1: 'pui', 2: 'manz', 3: 'dragon' }[level] || level || window.minigameLevel();
        var rnd = function (a, b) { return a + Math.random() * (b - a); };
        var ms = L === 'pui' ? rnd(3000, 7000) : L === 'manz' ? rnd(2000, 5000) : rnd(1000, 3000);
        if (plies < 4) ms /= 2;
        if (msLeft != null) ms = Math.min(ms, msLeft / (msLeft < 10000 ? 60 : 30));
        return ms;
    };

    /* nivelul ales, după butonul de adversar activ: 'pui' | 'manz' | 'dragon' */
    window.minigameLevel = function () {
        var b = document.querySelector('.animal-btn.active'), t = b ? b.textContent : '';
        return /Pui/.test(t) ? 'pui' : /Mânz/.test(t) ? 'manz' : 'dragon';
    };

    /* Ceas exact pentru ceasurile care țin secunde întregi: se apelează des (la ~100 ms) cu jucătorul la mutare
       și întoarce câte secunde întregi trebuie scăzute acum din ceasul lui. Fracțiunile rămân ale fiecăruia,
       deci o mutare de o jumătate de secundă costă o jumătate de secundă. Se face unul nou la fiecare pornire a ceasului. */
    window.minigameTickAcc = function () {
        var last = Date.now(), acc = {};
        var f = function (c) {
            var now = Date.now();
            acc[c] = (acc[c] || 0) + now - last; last = now;
            var s = Math.floor(acc[c] / 1000); acc[c] -= s * 1000;
            return s;
        };
        f.msUsed = function (c) { return (acc[c] || 0) + Date.now() - last; };   // fracțiunea de secundă deja consumată
        return f;
    };

    /* confetti peste toată pagina, timp de dur milisecunde */
    window.spawnConfetti = function (dur) {
        if (!document.getElementById('mjConfettiCss')) {
            var st = document.createElement('style'); st.id = 'mjConfettiCss';
            st.textContent = '@keyframes mj-confetti-fall{0%{opacity:1;transform:translate(0,0) rotate(0deg)}80%{opacity:1}' +
                '100%{opacity:0;transform:translate(var(--dx),var(--dy)) rotate(var(--rot))}}' +
                '.mj-confetti{position:fixed;pointer-events:none;z-index:9999;border-radius:3px;animation:mj-confetti-fall var(--dur,2s) ease-in forwards}';
            document.head.appendChild(st);
        }
        var cols = ['#ff3333', '#ff8800', '#ffee00', '#33cc55', '#4499ff', '#cc44ff', '#fff'];
        var end = Date.now() + (dur || 3000);
        (function batch() {
            if (Date.now() >= end) return;
            for (var i = 0; i < 12; i++) {
                var p = document.createElement('div'); p.className = 'mj-confetti';
                var w = 7 + Math.random() * 7, h = w * (0.35 + Math.random() * 0.7);
                p.style.cssText = 'width:' + w + 'px;height:' + h + 'px;background:' + cols[Math.floor(Math.random() * cols.length)] +
                    ';left:' + (Math.random() * 100) + 'vw;top:-14px;';
                p.style.setProperty('--dx', ((Math.random() - 0.5) * 180) + 'px');
                p.style.setProperty('--dy', (window.innerHeight * (0.65 + Math.random() * 0.45)) + 'px');
                p.style.setProperty('--rot', (Math.random() * 900 - 450) + 'deg');
                var d = 1.8 + Math.random() * 2.4; p.style.setProperty('--dur', d + 's');
                document.body.appendChild(p);
                (function (el, t) { setTimeout(function () { el.remove(); }, t); })(p, d * 1000 + 200);
            }
            setTimeout(batch, 110);
        })();
    };

    /* body.no-hints pornit/oprit după nivel și mod (CSS-ul e în master-template.css) */
    function syncHints() {
        if (document.body) document.body.classList.toggle('no-hints', window.minigameHideHints());
    }
    document.addEventListener('click', function () { setTimeout(syncHints, 0); }, true);

    function build() {
        var foot = document.querySelector('.page-footer');
        if (!foot) { syncHints(); return; }
        var html = '';
        if (lessonUrl) {
            html += '<a href="' + lessonUrl + '" class="nav-btn nav-btn--back">' +
                    '<span class="icon">&#8592;</span><span class="label">Înapoi la lecție</span></a>';
        }
        html += '<a href="hub.html" class="nav-btn nav-btn--contents">' +
                '<span class="icon">&#8862;</span><span class="label">Cuprins</span></a>';
        if (window.minigameNextUrl) {
            html += '<a href="' + window.minigameNextUrl + '" class="nav-btn nav-btn--forward">' +
                    '<span class="icon">&#8594;</span><span class="label">' + GAMES[i + 1][1] + '</span></a>';
        }
        foot.innerHTML = html;
        syncHints();
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
    else build();
})();
