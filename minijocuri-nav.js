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
        ['nivel1_joc_cai_lacomi.html', 'Care cal mănâncă mai repede?'],
        ['nivel1_joc_drumul_regelui.html', 'Drumul regelui spre castel'],
        ['nivel1_joc_cursa_obstacole.html', 'Cursa cu obstacole'],
        ['nivel1_joc_piesa_contra_pionilor.html', 'Piesa contra pionilor'],
        ['nivel1_joc_vanatoarea_regelui.html', 'Vânătoarea regelui'],
        ['nivel1_joc_regi_nasturi.html', 'Regii și nasturii'],
        ['nivel1_joc_cine_pastreaza.html', 'Cine păstrează ceva?'],
        ['joc_stockfish.html?v=2',   'Regi și Pioni 2']
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
