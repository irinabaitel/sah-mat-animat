#!/usr/bin/env python3
"""Micsoreaza pozele sahistilor: redimensioneaza la max 1000px pe latura lunga
si recomprima, pastrand o copie a originalelor in scratchpad/img_backup/.

Uz: python tools/optimize_images.py            (aplica modificarile)
    python tools/optimize_images.py --dry-run  (doar raporteaza)

Nu schimba niciodata numele sau formatul fisierelor, ca sa nu strice paginile.
Daca recomprimarea nu aduce niciun castig, fisierul original ramane neatins.
"""
import glob, os, shutil, sys
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP = os.path.join(REPO, 'scratchpad', 'img_backup')
MAX_SIDE = 1000
KEEP_UNDER = 150 * 1024          # sub atat si deja mic -> lasam in pace
QUALITY = 85
FOLDERS = ['img/sahisti', 'img/romani']

def main():
    dry = '--dry-run' in sys.argv
    files = []
    for d in FOLDERS:
        files += sorted(glob.glob(os.path.join(REPO, d, '*')))

    before_total = after_total = 0
    changed = []

    for f in files:
        before = os.path.getsize(f)
        before_total += before
        try:
            im = Image.open(f)
        except Exception as e:
            print('  sarit (nu se poate deschide):', f, e)
            after_total += before
            continue

        w, h = im.size
        needs_resize = max(w, h) > MAX_SIDE
        if not needs_resize and before <= KEEP_UNDER:
            after_total += before
            continue

        if dry:
            print('%-36s %6dKB  %s' % (os.path.relpath(f, REPO), before // 1024,
                                       'x'.join(map(str, im.size))))
            after_total += before
            continue

        rel = os.path.relpath(f, REPO).replace('\\', '/')
        dst = os.path.join(BACKUP, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst):
            shutil.copy2(f, dst)

        if needs_resize:
            r = MAX_SIDE / max(w, h)
            im = im.resize((round(w * r), round(h * r)), Image.LANCZOS)

        ext = os.path.splitext(f)[1].lower()
        if ext in ('.jpg', '.jpeg'):
            im.convert('RGB').save(f, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        else:
            im.save(f, optimize=True)

        after = os.path.getsize(f)
        if after >= before:               # niciun castig -> punem originalul inapoi
            shutil.copy2(dst, f)
            after = before
        else:
            changed.append((rel, before, after, im.size))
        after_total += after

    for rel, b, a, sz in sorted(changed, key=lambda x: x[1] - x[2], reverse=True):
        print('%-36s %6dKB -> %5dKB   %s' % (rel, b // 1024, a // 1024,
                                            'x'.join(map(str, sz))))
    print()
    print('optimizate: %d fisiere' % len(changed))
    print('total: %.2f MB -> %.2f MB  (-%.0f%%)'
          % (before_total / 1e6, after_total / 1e6,
             100 * (1 - after_total / before_total) if before_total else 0))
    if not dry:
        print('originalele: scratchpad/img_backup/  (ignorat de git)')

if __name__ == '__main__':
    main()
