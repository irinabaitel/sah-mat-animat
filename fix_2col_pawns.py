"""
Coloană laterală = 2 sub-coloane:
  exterior 120px → figuri mari   (flex: 1, înălțime egală)
  interior  60px → pioni mici    (aliniat cu fiecare figură)
Structură HTML: .piece-row { figură + pion } × 5
Body padding: 24 + 180 = 204px.
"""
import re, os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

# ── CSS override nou ──────────────────────────────────────────────────────────
OLD_COL_W  = 'width: 120px !important;\n    height: 100vh !important;'
NEW_COL_W  = 'width: 180px !important;\n    height: 100vh !important;'

OLD_BODY_P = 'body { padding-left: 144px !important; padding-right: 144px !important; }'
NEW_BODY_P = 'body { padding-left: 204px !important; padding-right: 204px !important; }'

OLD_MEDIA  = '    body { padding-left: 10px !important; padding-right: 10px !important; }'
NEW_MEDIA  = '    body { padding-left: 10px !important; padding-right: 10px !important; }\n    .piece-row { min-height: 0; }'

# Înlocuiește blocul CSS al imaginilor cu regulile noi pentru piece-row
OLD_IMG_BLOCK = """\
.side-col img {
    width: 120px !important;
    height: 0 !important;
    flex: 1 1 0 !important;
    min-height: 0 !important;
    object-fit: contain !important;
    display: block !important;
}"""

NEW_IMG_BLOCK = """\
.piece-row {
    flex: 1 1 0 !important;
    display: flex !important;
    min-height: 0 !important;
    align-items: stretch !important;
}
.side-col .fig-img {
    flex: 0 0 120px !important;
    width: 120px !important;
    height: 100% !important;
    object-fit: contain !important;
    display: block !important;
}
.side-col .pion-img {
    flex: 0 0 60px !important;
    width: 60px !important;
    height: 100% !important;
    object-fit: contain !important;
    display: block !important;
}"""

OLD_FLEX = """\
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
    padding: 8px 0 !important;"""

NEW_FLEX = """\
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
    padding: 6px 0 !important;"""

# ── HTML coloane ──────────────────────────────────────────────────────────────
def row(fig_src, fig_alt, fig_style, pion_src, pion_alt, left_fig=True):
    fs = f' style="{fig_style}"' if fig_style else ''
    fig  = f'        <img class="fig-img"  src="{fig_src}"  alt="{fig_alt}"{fs}>\n'
    pion = f'        <img class="pion-img" src="{pion_src}" alt="{pion_alt}">\n'
    inner = (fig + pion) if left_fig else (pion + fig)
    return '    <div class="piece-row">\n' + inner + '    </div>\n'

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

# stânga: figură (exterior-stânga) | pion (interior-dreapta)
left_rows  = ''.join(row(s,a,st, WP,'Pion alb',  left_fig=True)  for s,a,st in WF)
# dreapta: pion (interior-stânga) | figură (exterior-dreapta)
right_rows = ''.join(row(s,a,st, BP,'Pion negru', left_fig=False) for s,a,st in BF)

LEFT_COL  = '<div class="side-col">\n' + left_rows  + '</div>'
RIGHT_COL = '<div class="side-col">\n' + right_rows + '</div>'

# ── Găsire robustă side-col (depth-counting) ──────────────────────────────────
def find_side_cols(html):
    results, start = [], 0
    marker = '<div class="side-col">'
    while True:
        idx = html.find(marker, start)
        if idx == -1:
            break
        depth, pos = 0, idx
        while pos < len(html):
            if html[pos:pos+4] == '<div':
                depth += 1; pos += 4
            elif html[pos:pos+6] == '</div>':
                depth -= 1
                if depth == 0:
                    results.append((idx, pos + 6))
                    start = pos + 6
                    break
                pos += 6
            else:
                pos += 1
        else:
            break
    return results

# ── Aplică ────────────────────────────────────────────────────────────────────
n_ok = n_err = 0
for fpath in sorted(glob.glob(os.path.join(BASE, 'pagina*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    if 'COLOANE FIXE' not in html:
        continue
    fname = os.path.basename(fpath)

    html = html.replace(OLD_BODY_P,    NEW_BODY_P,    1)
    html = html.replace(OLD_COL_W,     NEW_COL_W,     1)
    html = html.replace(OLD_IMG_BLOCK, NEW_IMG_BLOCK, 1)
    html = html.replace(OLD_FLEX,      NEW_FLEX,      1)

    cols = find_side_cols(html)
    if len(cols) < 2:
        print(f'  WARN ({len(cols)} side-col): {fname}'); n_err += 1; continue

    l_s, l_e = cols[0]
    r_s, r_e = cols[-1]
    # înlocuiește de la dreapta spre stânga
    html = html[:r_s] + RIGHT_COL + html[r_e:]
    cols2 = find_side_cols(html)
    l_s, l_e = cols2[0]
    html = html[:l_s] + LEFT_COL  + html[l_e:]

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {fname}')
    n_ok += 1

print(f'\nGata! OK={n_ok}  warn={n_err}')
