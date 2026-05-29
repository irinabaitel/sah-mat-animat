"""
5 piese (Turn→Rege) + 5 pioni, fiecare rând = 20vh (100vh / 5).
"""
import re, os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

def img(src, alt, style=''):
    s = f' style="{style}"' if style else ''
    return f'    <img src="{src}" alt="{alt}"{s}>\n'

WF = [
    ('piese_sah/turn_medieval.jpg',         'Turn alb',     ''),
    ('piese_sah/cal_medieval.jpg',          'Cal alb',      ''),
    ('piese_sah/nebun_medieval.jpg',        'Nebun alb',    ''),
    ('piese_sah/regina_medieval.jpg',       'Regina albă',  ''),
    ('piese_sah/rege_medieval',             'Rege alb',     'filter:brightness(1.18);'),
]
BF = [
    ('piese_sah/turn_medieval_negru.jpg',   'Turn negru',   ''),
    ('piese_sah/cal_medieval_negru.jpg',    'Cal negru',    ''),
    ('piese_sah/nebun_medieval_negru.jpg',  'Nebun negru',  ''),
    ('piese_sah/regina_medieval_negru.jpg', 'Regina neagră',''),
    ('piese_sah/rege_medieval_negru.jpg',   'Rege negru',   ''),
]
WP = 'piese_sah/pion_medieval.jpg'
BP = 'piese_sah/pion negru.png'

left_imgs = ''.join(img(s,a,st) + img(WP,'Pion alb') for s,a,st in WF)
LEFT_COL  = '<div class="side-col">\n' + left_imgs + '</div>'

right_imgs = ''.join(img(BP,'Pion negru') + img(s,a,st) for s,a,st in BF)
RIGHT_COL  = '<div class="side-col">\n' + right_imgs + '</div>'

OLD_ROWS = 'grid-auto-rows: 12.5vh !important;'
NEW_ROWS = 'grid-auto-rows: 20vh !important;'

OLD_IMG_H = 'height: 12.5vh !important;'
NEW_IMG_H = 'height: 20vh !important;'

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

    html = html.replace(OLD_ROWS, NEW_ROWS, 1)
    html = html.replace(OLD_IMG_H, NEW_IMG_H, 1)

    matches = list(SIDE_RE.finditer(html))
    if len(matches) < 2:
        print(f'  WARN: {fname}')
        n_err += 1
        continue

    m_r = matches[-1]
    html = html[:m_r.start()] + RIGHT_COL + html[m_r.end():]
    m_l = list(SIDE_RE.finditer(html))[0]
    html = html[:m_l.start()] + LEFT_COL  + html[m_l.end():]

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {fname}')
    n_ok += 1

print(f'\nGata! OK={n_ok}  warn={n_err}')
