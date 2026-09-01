/* ═══════════════════════════════════════════════════════════════
 * nivel2-traseu.js — traseul Nivelului II, intr-un singur loc.
 *
 * Unele teme din traseu sunt predate pe pagini care apartin altui
 * nivel (tacticile, de la Nivelul IV). Ca sa NU clonam paginile alea,
 * ele se deschid din harta nivelului cu ?n=2 pe link. Scriptul de aici
 * citeste parametrul si rescrie doar butoanele de jos, ca sa duca la
 * vecinii din traseul Nivelului II. Fara parametru, pagina ramane
 * exact cum era la nivelul ei.
 *
 * Ordinea de mai jos oglindeste TRASEU din nivel2_intro.html.
 * ═══════════════════════════════════════════════════════════════ */

window.TRASEU_N2 = [
  { t: 'Fazele jocului și obiectivele lor', h: 'nivel2_lectia1.html' },
  { t: 'Ce văd pe tablă?', h: 'nivel2_ce_vad_pe_tabla.html' },
  { t: 'Relațiile dintre piese', h: 'nivel2_relatiile_dintre_piese.html' },
  { t: 'Atacul grupat', h: 'nivel2_atacul_grupat.html' },
  { t: 'Merită schimbul?', h: 'nivel2_numaratoarea.html' },
  { t: 'Centrul și spațiul', h: 'nivel2_centrul.html' },
  { t: 'Avantajul în dezvoltare', h: 'nivel2_dezvoltare.html' },
  { t: 'Regina scoasă prea repede', h: 'nivel2_dama_devreme.html' },
  { t: 'Legătura dintre turnuri și centralizarea', h: 'nivel2_turnuri.html' },
  { t: 'Cooperarea în deschidere', h: 'nivel2_cooperarea.html' },
  { t: 'Pionul lui Ahile — f2 și f7', h: 'nivel2_ahile.html' },
  { t: 'Mobilitatea și activitatea pieselor', h: 'nivel2_activitatea.html' },
  { t: 'Atacul dublu', h: 'pagina49.html' },
  { t: 'Furculița', h: 'pagina94.html' },
  { t: 'Mă apăr de un atac dublu', h: 'nivel2_aparare_atac_dublu.html' },
  { t: 'Legătura', h: 'pagina51.html' },
  { t: 'Piesa legată — cum o atac și cum o apăr', h: 'nivel2_piesa_legata.html' },
  { t: 'Atacul laser (frigăruia)', h: 'pagina53.html' },
  { t: 'Atacul prin descoperire', h: 'pagina95.html' },
  { t: 'Amenințările', h: 'nivel2_amenintari.html' },
  { t: 'Mă apăr de mat — bazele', h: 'aparare_mat.html' },
  { t: 'Cooperarea în jocul de mijloc', h: null },
  { t: 'Bateria', h: null },
  { t: 'Coloana deschisă și linia a 7-a', h: null },
  { t: 'Slăbiciunea ultimei linii', h: 'pagina65.html' },
  { t: 'Tabelul de analiză', h: null },
  { t: 'Cele trei întrebări', h: null },
  { t: 'Atragerea și devierea', h: 'pagina59.html' },
  { t: 'Îndepărtarea apărătorului', h: 'pagina98.html' },
  { t: 'Eliminarea apărătorului, pe cele patru feluri', h: null },
  { t: 'Atacul triplu', h: null },
  { t: 'Dubla lovitură', h: null },
  { t: 'Pioni dublați', h: null },
  { t: 'Pionul izolat', h: null },
  { t: 'Pionul înapoiat', h: null },
  { t: 'Avanpostul', h: null },
  { t: 'Perechea de nebuni', h: null },
  { t: 'Nebun bun, nebun rău', h: null },
  { t: 'Calul, mai puternic decât nebunul', h: null },
  { t: 'Când schimbi piese și când nu', h: null },
  { t: 'Atacul la rege', h: null },
  { t: 'Mă apăr de mat — când atacul e adevărat', h: null },
  { t: 'Ce faci cu avantajul material', h: null },
  { t: 'Pionul liber și susținerea lui', h: null },
  { t: 'Cooperarea în final', h: null },
  { t: 'Câmpuri cheie', h: null },
  { t: 'Opoziția', h: null },
  { t: 'Pătratul pionului', h: null },
  { t: 'Pătratul magic și pătratul mișcător', h: null },
  { t: 'Centralizarea regelui în final', h: null }
];

(function () {
  var params = new URLSearchParams(window.location.search);
  if (params.get('n') !== '2') return;

  var TR = window.TRASEU_N2;
  var aici = (window.location.pathname.split('/').pop() || '').toLowerCase();
  var i = -1;
  for (var k = 0; k < TR.length; k++) {
    if (TR[k].h && TR[k].h.toLowerCase() === aici) { i = k; break; }
  }
  if (i < 0) return;

  /* vecinul cel mai apropiat care chiar are pagina */
  function vecin(pas) {
    for (var j = i + pas; j >= 0 && j < TR.length; j += pas) if (TR[j].h) return TR[j];
    return null;
  }
  function adr(x) { return x.h + (x.h.indexOf('?') < 0 ? '?n=2' : '&n=2'); }

  function scurt(text) { return text.length > 26 ? text.slice(0, 25) + '…' : text; }

  /* sus-stanga: intoarcerea la harta nivelului, ca pe lectiile de Nivel II */
  function harta() {
    var cap = document.querySelector('.page-header');
    if (!cap || cap.querySelector('.header-back')) return;
    var a = document.createElement('a');
    a.href = 'nivel2_intro.html';
    a.className = 'header-back';
    a.title = 'Harta Nivelului II';
    a.innerHTML = '<span class="hb-ico">&#8862;</span><span class="hb-txt">Harta nivelului</span>';
    cap.insertBefore(a, cap.firstChild);
  }

  function gata() {
    harta();
    var f = document.querySelector('.page-footer');
    if (!f) return;
    var inainte = vecin(-1), dupa = vecin(1);
    var h = '';
    h += inainte
      ? '<a href="' + adr(inainte) + '" class="nav-btn nav-btn--back">' +
        '<span class="icon">&#8592;</span><span class="label">' + scurt(inainte.t) + '</span></a>'
      : '<a href="nivel2_intro.html" class="nav-btn nav-btn--back">' +
        '<span class="icon">&#8592;</span><span class="label">Înapoi</span></a>';
    /* butonul din mijloc ramane Cuprins; harta nivelului e sus-stanga */
    h += '<a href="hub.html" class="nav-btn nav-btn--contents">' +
         '<span class="icon">&#8862;</span><span class="label">Cuprins</span></a>';
    if (dupa) {
      h += '<a href="' + adr(dupa) + '" class="nav-btn nav-btn--forward">' +
           '<span class="icon">&#8594;</span><span class="label">' + scurt(dupa.t) + '</span></a>';
    } else {
      h += '<a href="nivel2_intro.html" class="nav-btn nav-btn--forward">' +
           '<span class="icon">&#8594;</span><span class="label">Harta nivelului</span></a>';
    }
    f.innerHTML = h;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', gata);
  } else {
    gata();
  }
})();
