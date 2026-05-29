"""
Piese la înălțime naturală (height:auto) + gap mic între ele.
"""
import os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

OLD_FLEX = """\
    display: flex !important;
    flex-direction: column !important;"""

NEW_FLEX = """\
    display: flex !important;
    flex-direction: column !important;
    gap: 6px !important;
    padding-top: 8px !important;
    justify-content: flex-start !important;"""

OLD_IMG = """\
    width: 120px !important;
    height: 20vh !important;
    object-fit: contain !important;
    display: block !important;"""

NEW_IMG = """\
    width: 120px !important;
    height: auto !important;
    object-fit: contain !important;
    display: block !important;"""

n_ok = 0
for fpath in sorted(glob.glob(os.path.join(BASE, 'pagina*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    if 'COLOANE FIXE' not in html:
        continue
    html = html.replace(OLD_FLEX, NEW_FLEX, 1)
    html = html.replace(OLD_IMG,  NEW_IMG,  1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {os.path.basename(fpath)}')
    n_ok += 1

print(f'\nGata! OK={n_ok}')
