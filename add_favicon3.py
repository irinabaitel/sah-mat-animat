# -*- coding: utf-8 -*-
import subprocess

OLD = 'href="/img/favicon.ico"'
NEW = 'href="/img/favicon.ico?v=2"'
OLD2 = 'href="/img/favicon-64.png"'
NEW2 = 'href="/img/favicon-64.png?v=2"'

files = subprocess.check_output(['git','ls-files','*.html'], text=True).splitlines()
updated = 0
for f in files:
    try:
        content = open(f, encoding='utf-8').read()
    except:
        continue
    new_content = content.replace(OLD, NEW).replace(OLD2, NEW2)
    if new_content != content:
        open(f, 'w', encoding='utf-8').write(new_content)
        updated += 1
print(f'Actualizate: {updated}')
