# -*- coding: utf-8 -*-
import subprocess

OLD = '<link rel="icon" type="image/x-icon" href="/img/favicon.ico?v=2">\n<link rel="icon" type="image/png" sizes="64x64" href="/img/favicon-64.png?v=2">\n<link rel="apple-touch-icon" href="/img/favicon-64.png?v=2">'
NEW = '<link rel="icon" type="image/png" sizes="64x64" href="/img/favicon-64.png?v=3">\n<link rel="apple-touch-icon" href="/img/favicon-64.png?v=3">'

files = subprocess.check_output(['git','ls-files','*.html'], text=True).splitlines()
updated = 0
for f in files:
    try:
        content = open(f, encoding='utf-8').read()
    except:
        continue
    new_content = content.replace(OLD, NEW)
    if new_content != content:
        open(f, 'w', encoding='utf-8').write(new_content)
        updated += 1
print(f'Actualizate: {updated}')
