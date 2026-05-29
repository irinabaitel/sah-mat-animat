"""
Fixează hărțile mentale: simetrie verticală + mai compacte spre centru.
Regula: gap_deasupra_centrului = gap_dedesubt_centrului (linii SVG spre marginile interne ale celulelor)
"""
import re

BASE = r'c:\Users\irina\SahMatAnimat'

# ── Valorile noi per pagină ───────────────────────────────────────────────────
# Cheie: fișier → dict cu valorile de înlocuit

FIXES = {

    # pagina11, 14, 18, 21 — layout identic
    # Top branches: top=20, height≈190px → bottom=210
    # gap=30 → center_top=240, center_bottom=326, center_mid=283
    # bottom_branch_top = 356
    # SVG: 283-210=73 deasupra, 356-283=73 dedesubt ✓
    'pagina11.html': {
        'wrap_h_old': 'height: 640px',    'wrap_h_new': 'height: 550px',
        'center_old': 'top: 260px',       'center_new': 'top: 240px',
        'red_old':    'top: 446px; left: 0px',   'red_new':  'top: 356px; left: 0px',
        'purp_old':   'top: 446px; left: 700px',  'purp_new': 'top: 356px; left: 700px',
        'vbox_old':   '0 0 1100 640',     'vbox_new': '0 0 1100 550',
        'svg_old': [
            'x1="550" y1="303" x2="428" y2="114"',
            'x1="550" y1="303" x2="672" y2="114"',
            'x1="550" y1="303" x2="428" y2="458"',
            'x1="550" y1="303" x2="672" y2="458"',
        ],
        'svg_new': [
            'x1="550" y1="283" x2="428" y2="210"',
            'x1="550" y1="283" x2="672" y2="210"',
            'x1="550" y1="283" x2="428" y2="356"',
            'x1="550" y1="283" x2="672" y2="356"',
        ],
    },
}

# pagina14, 18, 21 — identice cu pagina11
for p in ['pagina14.html', 'pagina18.html', 'pagina21.html']:
    FIXES[p] = FIXES['pagina11.html']

# pagina32
# Top branches: top=70, height≈175px → bottom=245
# gap=30 → center_top=275, center_bottom=365, center_mid=320
# bottom_branch_top=395; SVG: 320-245=75, 395-320=75 ✓
FIXES['pagina32.html'] = {
    'wrap_h_old': 'height: 680px',    'wrap_h_new': 'height: 570px',
    'center_old': 'top: 280px',       'center_new': 'top: 275px',
    'red_old':    'top: 405px; left: 10px',   'red_new':  'top: 395px; left: 10px',
    'purp_old':   'top: 405px; left: 690px',  'purp_new': 'top: 395px; left: 690px',
    'vbox_old':   '0 0 1100 680',     'vbox_new': '0 0 1100 570',
    'svg_old': [
        'x1="550" y1="325" x2="412" y2="245"',
        'x1="550" y1="325" x2="688" y2="245"',
        'x1="550" y1="325" x2="412" y2="407"',
        'x1="550" y1="325" x2="688" y2="407"',
    ],
    'svg_new': [
        'x1="550" y1="320" x2="412" y2="245"',
        'x1="550" y1="320" x2="688" y2="245"',
        'x1="550" y1="320" x2="412" y2="395"',
        'x1="550" y1="320" x2="688" y2="395"',
    ],
}

# pagina23
# Top branches: top=20, height≈250px → bottom=270
# gap=30 → center_top=300, center_bottom=386, center_mid=343
# bottom_branch_top=416; SVG: 343-270=73, 416-343=73 ✓
FIXES['pagina23.html'] = {
    'wrap_h_old': 'height: 720px',    'wrap_h_new': 'height: 660px',
    'center_old': 'top: 307px',       'center_new': 'top: 300px',
    'red_old':    'top: 557px; left: 0px',   'red_new':  'top: 416px; left: 0px',
    'purp_old':   'top: 557px; left: 700px',  'purp_new': 'top: 416px; left: 700px',
    'vbox_old':   '0 0 1100 720',     'vbox_new': '0 0 1100 660',
    'svg_old': [
        'x1="550" y1="350" x2="425" y2="133"',
        'x1="550" y1="350" x2="675" y2="133"',
        'x1="550" y1="350" x2="425" y2="567"',
        'x1="550" y1="350" x2="675" y2="567"',
    ],
    'svg_new': [
        'x1="550" y1="343" x2="425" y2="270"',
        'x1="550" y1="343" x2="675" y2="270"',
        'x1="550" y1="343" x2="425" y2="416"',
        'x1="550" y1="343" x2="675" y2="416"',
    ],
}

# pagina26
# Top branches: top=18, height≈280px → bottom=298
# gap=30 → center_top=328, center_bottom=420, center_mid=374
# bottom_branch_top=450; SVG: 374-298=76, 450-374=76 ✓
FIXES['pagina26.html'] = {
    'wrap_h_old': 'height: 800px',    'wrap_h_new': 'height: 700px',
    'center_old': 'top: 360px',       'center_new': 'top: 328px',
    'red_old':    'top: 567px; left: 0px',   'red_new':  'top: 450px; left: 0px',
    'purp_old':   'top: 567px; left: 680px',  'purp_new': 'top: 450px; left: 680px',
    'vbox_old':   '0 0 1100 800',     'vbox_new': '0 0 1100 700',
    'svg_old': [
        'x1="550" y1="406" x2="442" y2="145"',
        'x1="550" y1="406" x2="658" y2="145"',
        'x1="550" y1="406" x2="442" y2="575"',
        'x1="550" y1="406" x2="658" y2="575"',
    ],
    'svg_new': [
        'x1="550" y1="374" x2="442" y2="298"',
        'x1="550" y1="374" x2="658" y2="298"',
        'x1="550" y1="374" x2="442" y2="450"',
        'x1="550" y1="374" x2="658" y2="450"',
    ],
}

# ── Aplică fix-urile ──────────────────────────────────────────────────────────
import os

for fname, fix in FIXES.items():
    fpath = os.path.join(BASE, fname)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    html = html.replace(fix['wrap_h_old'], fix['wrap_h_new'], 1)
    html = html.replace(fix['center_old'], fix['center_new'], 1)
    html = html.replace(fix['red_old'],    fix['red_new'],    1)
    html = html.replace(fix['purp_old'],   fix['purp_new'],   1)
    html = html.replace(fix['vbox_old'],   fix['vbox_new'],   1)
    for old, new in zip(fix['svg_old'], fix['svg_new']):
        html = html.replace(old, new, 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {fname}')

print('\nGata!')
