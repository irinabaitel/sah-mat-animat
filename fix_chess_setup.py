"""
Aranjament ca pe tabla de start:
  Col stângă:  [figură exterior | pion interior]  × 8 rânduri
  Col dreaptă: [pion interior | figură exterior]  × 8 rânduri
Înălțime per rând = 12.5vh → 8 rânduri umplu exact 100vh.
"""
import re, os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

# ── HTML pentru coloane ────────────────────────────────────────────────────────

def img(src, alt, style=''):
    s = f' style="{style}"' if style else ''
    return f'    <img src="{src}" alt="{alt}"{s}>\n'

# Ordinea figurilor: T C N R Re N C T
WF = [  # figuri albe
    ('piese_sah/turn_medieval.jpg',          'Turn alb',     ''),
    ('piese_sah/cal_medieval.jpg',           'Cal alb',      ''),
    ('piese_sah/nebun_medieval.jpg',         'Nebun alb',    ''),
    ('piese_sah/regina_medieval.jpg',        'Regina albă',  ''),
    ('piese_sah/rege_medieval',              'Rege alb',     'filter:brightness(1.18);'),
    ('piese_sah/nebun_medieval.jpg',         'Nebun alb',    ''),
    ('piese_sah/cal_medieval.jpg',           'Cal alb',      ''),
    ('piese_sah/turn_medieval.jpg',          'Turn alb',     ''),
]
WP = 'piese_sah/pion_medieval.jpg'          # pion alb

BF = [  # figuri negre
    ('piese_sah/turn_medieval_negru.jpg',    'Turn negru',   ''),
    ('piese_sah/cal_medieval_negru.jpg',     'Cal negru',    ''),
    ('piese_sah/nebun_medieval_negru.jpg',   'Nebun negru',  ''),
    ('piese_sah/regina_medieval_negru.jpg',  'Regina neagră',''),
    ('piese_sah/rege_medieval_negru.jpg',    'Rege negru',   ''),
    ('piese_sah/nebun_medieval_negru.jpg',   'Nebun negru',  ''),
    ('piese_sah/cal_medieval_negru.jpg',     'Cal negru',    ''),
    ('piese_sah/turn_medieval_negru.jpg',    'Turn negru',   ''),
]
BP = 'piese_sah/pion negru.png'             # pion negru (PNG transparent)

# Col stângă: figura (col ext) | pion (col int)
left_imgs = ''
for src, alt, style in WF:
    left_imgs += img(src, alt, style)
    left_imgs += img(WP, 'Pion alb')
LEFT_COL = '<div class="side-col">\n' + left_imgs + '</div>'

# Col dreaptă: pion (col int) | figura (col ext)
right_imgs = ''
for src, alt, style in BF:
    right_imgs += img(BP, 'Pion negru')
    right_imgs += img(src, alt, style)
RIGHT_COL = '<div class="side-col">\n' + right_imgs + '</div>'

# ── CSS override actualizat ────────────────────────────────────────────────────

OLD_CSS_BLOCK = """\
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
.page-wrapper > .side-col:first-child { left: 24px !important; right: auto !important; }
.page-wrapper > .side-col:last-child  { right: 24px !important; left: auto !important; }
.side-col { mix-blend-mode: multiply !important; }
.side-col img {
    width: 120px !important;
    height: 180px !important;
    object-fit: fill !important;
    flex-shrink: 0 !important;
    mix-blend-mode: normal !important;
    display: block !important;
}"""

NEW_CSS_BLOCK = """\
.side-col {
    position: fixed !important;
    top: 0 !important;
    width: 120px !important;
    height: 100vh !important;
    display: grid !important;
    grid-template-columns: 60px 60px !important;
    grid-auto-rows: 12.5vh !important;
    overflow: hidden !important;
    mix-blend-mode: multiply !important;
    z-index: 10 !important;
}
.page-wrapper > .side-col:first-child { left: 24px !important; right: auto !important; }
.page-wrapper > .side-col:last-child  { right: 24px !important; left: auto !important; }
.side-col img {
    width: 60px !important;
    height: 12.5vh !important;
    object-fit: fill !important;
    display: block !important;
}"""

# ── Regex pentru side-col div-uri ─────────────────────────────────────────────

SIDE_RE = re.compile(
    r'<div class="side-col">\n(?:[ \t]*<img[^\n]*\n)+[ \t]*</div>',
    re.MULTILINE
)

n_ok = n_skip = n_err = 0

for fpath in sorted(glob.glob(os.path.join(BASE, 'pagina*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    if 'COLOANE FIXE' not in html:
        continue

    fname = os.path.basename(fpath)

    # ① Actualizează blocul CSS
    if OLD_CSS_BLOCK in html:
        html = html.replace(OLD_CSS_BLOCK, NEW_CSS_BLOCK, 1)
    else:
        print(f'  WARN (CSS block negasit): {fname}')
        n_err += 1
        continue

    # ② Înlocuiește coloanele laterale (prima = stângă, ultima = dreaptă)
    matches = list(SIDE_RE.finditer(html))
    if len(matches) < 2:
        print(f'  WARN ({len(matches)} side-col): {fname}')
        n_err += 1
        continue

    # înlocuiește de la dreapta spre stânga
    m_right = matches[-1]
    m_left  = matches[0]
    html = html[:m_right.start()] + RIGHT_COL + html[m_right.end():]
    m_left = list(SIDE_RE.finditer(html))[0]
    html = html[:m_left.start()] + LEFT_COL  + html[m_left.end():]

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {fname}')
    n_ok += 1

print(f'\nGata! OK={n_ok}  skip={n_skip}  warn={n_err}')
