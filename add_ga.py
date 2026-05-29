# -*- coding: utf-8 -*-
import re, subprocess

GA = (
    '<!-- Google Analytics -->\n'
    '<script async src="https://www.googletagmanager.com/gtag/js?id=G-CMTZ9GGPMP"></script>\n'
    '<script>\n'
    '  window.dataLayer = window.dataLayer || [];\n'
    '  function gtag(){dataLayer.push(arguments);}\n'
    '  gtag(\'js\', new Date());\n'
    '  gtag(\'config\', \'G-CMTZ9GGPMP\');\n'
    '</script>'
)

files = subprocess.check_output(['git','ls-files','*.html'], text=True).splitlines()

updated = skipped = errors = 0
for f in files:
    try:
        content = open(f, encoding='utf-8').read()
    except UnicodeDecodeError:
        try:
            content = open(f, encoding='utf-8-sig').read()
        except Exception as e:
            errors += 1
            continue
    if 'G-CMTZ9GGPMP' in content:
        skipped += 1
        continue
    new_content = re.sub(
        r'(<meta\s+charset=["\']UTF-8["\'][^>]*>)',
        r'\1\n' + GA,
        content, count=1, flags=re.IGNORECASE
    )
    if new_content == content:
        new_content = content.replace('</head>', GA + '\n</head>', 1)
    if new_content != content:
        open(f, 'w', encoding='utf-8').write(new_content)
        updated += 1

print(f"Actualizate: {updated}  |  deja aveau: {skipped}  |  erori: {errors}")
