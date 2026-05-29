"""
Transformă coloanele laterale în position:fixed — ancorate la marginile ecranului,
cu toate piesele medievale disponibile (repetate pentru pagini lungi).
"""
import re, os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

OVERRIDE_CSS = """\
<style>
/* ===== COLOANE FIXE ===== */
body { padding-left: 144px !important; padding-right: 144px !important; }
.page-wrapper { display: block !important; }
.side-col {
    position: fixed !important;
    top: 0 !important;
    width: 120px !important;
    height: 100vh !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 0 !important;
    padding-top: 0 !important;
    z-index: 10 !important;
}
.page-wrapper > .side-col:first-child { left: 12px !important; right: auto !important; }
.page-wrapper > .side-col:last-child  { right: 12px !important; left: auto !important; }
.side-col img {
    width: 120px !important;
    height: 180px !important;
    object-fit: fill !important;
    flex-shrink: 0 !important;
    mix-blend-mode: multiply !important;
    display: block !important;
}
@media (max-width: 900px) {
    body { padding-left: 10px !important; padding-right: 10px !important; }
    .side-col { display: none !important; }
}
</style>
"""

# 6 piese albe
WHITE = [
    ('piese_sah/regina_medieval.jpg',       'Regina albă',  ''),
    ('piese_sah/rege_medieval',              'Rege alb',     'filter:brightness(1.18);'),
    ('piese_sah/cal_medieval.jpg',           'Cal alb',      ''),
    ('piese_sah/turn_medieval.jpg',          'Turn alb',     ''),
    ('piese_sah/nebun_medieval.jpg',         'Nebun alb',    ''),
    ('piese_sah/pion_medieval.jpg',          'Pion alb',     ''),
]
# 5 piese negre (nu există pion medieval negru)
BLACK = [
    ('piese_sah/regina_medieval_negru.jpg',  'Regina neagră',''),
    ('piese_sah/rege_medieval_negru.jpg',    'Rege negru',   ''),
    ('piese_sah/cal_medieval_negru.jpg',     'Cal negru',    ''),
    ('piese_sah/turn_medieval_negru.jpg',    'Turn negru',   ''),
    ('piese_sah/nebun_medieval_negru.jpg',   'Nebun negru',  ''),
]

def build_col(pieces, n_sets=3):
    lines = ['<div class="side-col">']
    for _ in range(n_sets):
        for src, alt, style in pieces:
            s = f' style="{style}"' if style else ''
            lines.append(f'    <img src="{src}" alt="{alt}"{s}>')
    lines.append('</div>')
    return '\n'.join(lines)

LEFT_COL  = build_col(WHITE)
RIGHT_COL = build_col(BLACK)

# Regex: orice <div class="side-col"> ... </div>  (conținut de img-uri)
SIDE_RE = re.compile(
    r'<div class="side-col">\s*\n(?:[ \t]*<img[^\n]*\n)+[ \t]*</div>',
    re.MULTILINE
)

n_ok = n_skip = n_err = 0

for fpath in sorted(glob.glob(os.path.join(BASE, 'pagina*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    if 'side-col' not in html:
        continue

    fname = os.path.basename(fpath)

    # Deja aplicat?
    if 'COLOANE FIXE' in html:
        print(f'  SKIP: {fname}')
        n_skip += 1
        continue

    matches = list(SIDE_RE.finditer(html))
    if len(matches) < 2:
        print(f'  WARN ({len(matches)} side-col găsite): {fname}')
        n_err += 1
        continue

    # Înlocuiește de la dreapta spre stânga (ca să nu deplasăm indecșii)
    left_m  = matches[0]
    right_m = matches[-1]

    html = (html[:right_m.start()] + RIGHT_COL + html[right_m.end():])
    # recalculăm după prima înlocuire
    left_m = list(SIDE_RE.finditer(html))[0]
    html = (html[:left_m.start()] + LEFT_COL + html[left_m.end():])

    # Injectează CSS override înainte de </head>
    html = html.replace('</head>', OVERRIDE_CSS + '</head>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {fname}')
    n_ok += 1

print(f'\nGata! OK={n_ok}  skip={n_skip}  warn={n_err}')
