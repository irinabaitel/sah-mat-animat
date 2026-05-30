# -*- coding: utf-8 -*-
import re, subprocess

FAVICON = '<link rel="icon" href="/img/pion-logo.png" type="image/png">\n<link rel="apple-touch-icon" href="/img/pion-logo.png">'

files = subprocess.check_output(['git','ls-files','*.html'], text=True).splitlines()

updated = skipped = 0
for f in files:
    try:
        content = open(f, encoding='utf-8').read()
    except:
        try:
            content = open(f, encoding='utf-8-sig').read()
        except:
            continue
    if 'pion-logo.png' in content:
        skipped += 1
        continue
    new_content = content.replace('</head>', FAVICON + '\n</head>', 1)
    if new_content != content:
        open(f, 'w', encoding='utf-8').write(new_content)
        updated += 1

print(f"Favicon adaugat: {updated}  |  deja aveau: {skipped}")
