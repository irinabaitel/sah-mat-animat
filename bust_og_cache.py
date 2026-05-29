import subprocess
files = subprocess.check_output(['git','ls-files','*.html'], text=True).splitlines()
updated = 0
for f in files:
    content = open(f, encoding='utf-8').read()
    new = content.replace('og-image.jpg">', 'og-image.jpg?v=2">')
    if new != content:
        open(f, 'w', encoding='utf-8').write(new)
        updated += 1
print(f'Actualizate: {updated}')
