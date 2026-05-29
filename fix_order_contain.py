"""
Ordine nouă: Rege, Regină, Nebun, Turn, Cal  (+pioni)
object-fit: contain → nu mai distorsionează proporțiile
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
WP = 'piese_sah/pion_medieval.jpg'
BP = 'piese_sah/pion negru.png'

left_imgs  = ''.join(img(s,a,st) + img(WP,'Pion alb')   for s,a,st in WF)
right_imgs = ''.join(img(BP,'Pion negru') + img(s,a,st) for s,a,st in BF)
LEFT_COL  = '<div class="side-col">\n' + left_imgs  + '</div>'
RIGHT_COL = '<div class="side-col">\n' + right_imgs + '</div>'

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

    # object-fit: fill → contain  +  adaugă align-self: center imaginilor
    html = html.replace(
        'object-fit: fill !important;\n    display: block !important;',
        'object-fit: contain !important;\n    align-self: center !important;\n    display: block !important;',
        1
    )

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
