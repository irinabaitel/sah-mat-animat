"""
Adaugă coloana dreaptă (piese negre) și închide page-wrapper
pe paginile em_msf_* care au deja left col dar nu au right col.
"""
import re, os, glob

BASE = r'c:\Users\irina\SahMatAnimat'

RIGHT_COL = (
    '\n</div><!-- /.page -->\n\n'
    '<div class="side-col">\n'
    '    <img src="piese_sah/regina_medieval_negru.jpg" alt="Regina neagră">\n'
    '    <img src="piese_sah/rege_medieval_negru.jpg" alt="Rege negru">\n'
    '    <img src="piese_sah/cal_medieval_negru.jpg" alt="Cal negru">\n'
    '</div>\n\n'
    '</div><!-- /.page-wrapper -->'
)

PAGE_IDS = {
    'em_msf_turn_l2','em_msf_turn_hm','em_msf_turn_ex',
    'em_msf_dama_l1','em_msf_dama_l2','em_msf_dama_hm',
    'em_msf_dama_prov','em_msf_dama_ex1','em_msf_dama_ex2','em_msf_dama_ex',
    'em_msf_dt_l1','em_msf_dt_hm','em_msf_dt_ex',
    'em_msf_2t_l1','em_msf_2t_l2','em_msf_2t_hm','em_msf_2t_ex',
    'em_msf_dn_l1','em_msf_dn_l2','em_msf_dn_hm','em_msf_dn_ex',
    'em_msf_2n_l1','em_msf_2n_l2','em_msf_2n_hm',
    'em_msf_dc_l1','em_msf_dc_hm','em_msf_dc_ex',
}

for fpath in sorted(glob.glob(os.path.join(BASE, 'pagina*.html'))):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    m = re.search(r"PAGE_ID\s*=\s*'([^']+)'", html)
    if not m or m.group(1) not in PAGE_IDS:
        continue

    # Deja are coloana dreaptă?
    if 'regina_medieval_negru' in html:
        print(f'  SKIP: {os.path.basename(fpath)}')
        continue

    # Găsim ultimul </div> al div.page — vine chiar înaintea hub-btn / script extern
    # Strategia: căutăm </div> urmat de newline + orice combinație de <script|<style|<a
    # care conține "hub-btn" sau PAGE_ID
    # Mai simplu: inserăm RIGHT_COL înaintea primului <script sau <style
    # care apare DUPĂ nav-buttons (deci după ultimul </div> al paginii)

    # Găsim poziția nav-buttons closing (ultimul nav-btn din pagină)
    nav_end = html.rfind('</div>', 0, html.find('hub-btn') if 'hub-btn' in html else len(html))

    if nav_end == -1:
        print(f'  ERROR (nu găsesc nav end): {os.path.basename(fpath)}')
        continue

    # Inserăm RIGHT_COL după poziția nav_end + len('</div>')
    insert_pos = nav_end + len('</div>')
    html = html[:insert_pos] + RIGHT_COL + html[insert_pos:]

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {os.path.basename(fpath)}')

print('\nGata!')
