# -*- coding: utf-8 -*-
import re, subprocess

OLD = '<link rel="icon" href="/img/pion-logo.png" type="image/png">\n<link rel="apple-touch-icon" href="/img/pion-logo.png">'
NEW = '<link rel="icon" type="image/x-icon" href="/img/favicon.ico">\n<link rel="icon" type="image/png" sizes="64x64" href="/img/favicon-64.png">\n<link rel="apple-touch-icon" href="/img/favicon-64.png">'

files = subprocess.check_output(['git','ls-files','*.html'], text=True).splitlines()

updated = 0
for f in files:
    try:
        content = open(f, encoding='utf-8').read()
    except:
        continue
    if OLD not in content:
        continue
    new_content = content.replace(OLD, NEW)
    open(f, 'w', encoding='utf-8').write(new_content)
    updated += 1

print(f'Actualizate: {updated}')
