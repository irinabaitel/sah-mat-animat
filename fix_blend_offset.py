"""
Fix #1 — mix-blend-mode mutat de pe img pe .side-col (fixed context)
Fix #2 — coloanele trase spre centru cu 12px (left:12→24, right:12→24)
"""
import os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

OLD = """\
.page-wrapper > .side-col:first-child { left: 12px !important; right: auto !important; }
.page-wrapper > .side-col:last-child  { right: 12px !important; left: auto !important; }
.side-col img {
    width: 120px !important;
    height: 180px !important;
    object-fit: fill !important;
    flex-shrink: 0 !important;
    mix-blend-mode: multiply !important;
    display: block !important;
}"""

NEW = """\
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

n_ok = n_skip = 0
for fpath in sorted(glob.glob(os.path.join(BASE, 'pagina*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()
    if 'COLOANE FIXE' not in html:
        continue
    if OLD not in html:
        print(f'  SKIP (deja aplicat sau lipsă): {os.path.basename(fpath)}')
        n_skip += 1
        continue
    html = html.replace(OLD, NEW, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {os.path.basename(fpath)}')
    n_ok += 1

print(f'\nGata! OK={n_ok}  skip={n_skip}')
