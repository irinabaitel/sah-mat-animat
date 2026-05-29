"""
Lățește coloana pionilor 60px → 80px, ca să apară mai înalți.
Total coloană: 120 + 80 = 200px. Body padding: 24 + 200 = 224px.
"""
import os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

CHANGES = [
    ('width: 180px !important;\n    height: 100vh !important;',
     'width: 200px !important;\n    height: 100vh !important;'),

    ('body { padding-left: 204px !important; padding-right: 204px !important; }',
     'body { padding-left: 224px !important; padding-right: 224px !important; }'),

    ('    flex: 0 0 60px !important;\n    width: 60px !important;',
     '    flex: 0 0 80px !important;\n    width: 80px !important;'),
]

n_ok = 0
for fpath in sorted(glob.glob(os.path.join(BASE, 'pagina*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    if 'COLOANE FIXE' not in html:
        continue
    for old, new in CHANGES:
        html = html.replace(old, new, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {os.path.basename(fpath)}')
    n_ok += 1

print(f'\nGata! OK={n_ok}')
