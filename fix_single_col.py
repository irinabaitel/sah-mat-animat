"""
Revenim la coloană simplă 120px, 5 figuri (fără pion separat),
fiecare 20vh înălțime — piese de 2× mai late față de grila de 60px.
"""
import re, os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

def img(src, alt, style=''):
    s = f' style="{style}"' if style else ''
    return f'    <img src="{src}" alt="{alt}"{s}>\n'

WF = [
    ('piese_sah/rege_medieval',             'Rege alb',     'filter:brightness(1.18);'),
    ('piese_sah/regina_medieval.jpg',       'Regina albă',  ''),
    ('piese_sah/nebun_medieval.jpg',        'Nebun alb',    ''),
    ('piese_sah/turn_medieval.jpg',         'Turn alb',     ''),
    ('piese_sah/cal_medieval.jpg',          'Cal alb',      ''),
]
BF = [
    ('piese_sah/rege_medieval_negru.jpg',   'Rege negru',   ''),
    ('piese_sah/regina_medieval_negru.jpg', 'Regina neagră',''),
    ('piese_sah/nebun_medieval_negru.jpg',  'Nebun negru',  ''),
    ('piese_sah/turn_medieval_negru.jpg',   'Turn negru',   ''),
    ('piese_sah/cal_medieval_negru.jpg',    'Cal negru',    ''),
]

LEFT_COL  = '<div class="side-col">\n' + ''.join(img(s,a,st) for s,a,st in WF) + '</div>'
RIGHT_COL = '<div class="side-col">\n' + ''.join(img(s,a,st) for s,a,st in BF) + '</div>'

OLD_GRID = """\
    display: grid !important;
    grid-template-columns: 60px 60px !important;
    grid-auto-rows: 20vh !important;"""

NEW_FLEX = """\
    display: flex !important;
    flex-direction: column !important;"""

OLD_IMG = """\
    width: 60px !important;
    height: 20vh !important;
    object-fit: contain !important;
    align-self: center !important;
    display: block !important;"""

NEW_IMG = """\
    width: 120px !important;
    height: 20vh !important;
    object-fit: contain !important;
    display: block !important;"""

SIDE_RE = re.compile(
    r'<div class="side-col">\n(?:[ \t]*<img[^\n]*\n)+[ \t]*</div>',
    re.MULTILINE
)

n_ok = n_err = 0
for fpath in sorted(glob.glob(os.path.join(BASE, 'pagina*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    if 'COLOANE FIXE' not in html:
        continue
    fname = os.path.basename(fpath)

    html = html.replace(OLD_GRID, NEW_FLEX, 1)
    html = html.replace(OLD_IMG,  NEW_IMG,  1)

    matches = list(SIDE_RE.finditer(html))
    if len(matches) < 2:
        print(f'  WARN: {fname}'); n_err += 1; continue

    m_r = matches[-1]
    html = html[:m_r.start()] + RIGHT_COL + html[m_r.end():]
    m_l = list(SIDE_RE.finditer(html))[0]
    html = html[:m_l.start()] + LEFT_COL  + html[m_l.end():]

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {fname}')
    n_ok += 1

print(f'\nGata! OK={n_ok}  warn={n_err}')
