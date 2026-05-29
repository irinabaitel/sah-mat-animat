"""
Aplică template-ul de piese medievale la toate paginile em_msf_*.
"""
import re, os

BASE = r'c:\Users\irina\SahMatAnimat'

# ── Piese per subcapitol ─────────────────────────────────────────────────────
# (fișiere din piese_sah/, stânga → dreapta, FĂRĂ regele negru care e mereu la dreapta)
SUBCAP = {
    'turn': ['turn_medieval.jpg', 'rege_medieval'],
    'dama': ['regina_medieval.jpg', 'rege_medieval'],
    'dt':   ['regina_medieval.jpg', 'turn_medieval.jpg', 'rege_medieval'],
    '2t':   ['turn_medieval.jpg',   'turn_medieval.jpg', 'rege_medieval'],
    'dn':   ['regina_medieval.jpg', 'nebun_medieval.jpg','rege_medieval'],
    '2n':   ['nebun_medieval.jpg',  'nebun_medieval.jpg','rege_medieval'],
    'dc':   ['regina_medieval.jpg', 'cal_medieval.jpg',  'rege_medieval'],
}

# PAGE_ID → subcapitol
PAGE_SUBCAP = {
    'em_msf_turn_l1': 'turn',  # pagina30 – deja făcută, dar o includem pentru siguranță
    'em_msf_turn_l2': 'turn',
    'em_msf_turn_hm': 'turn',
    'em_msf_turn_ex': 'turn',
    'em_msf_dama_l1': 'dama',
    'em_msf_dama_l2': 'dama',
    'em_msf_dama_hm': 'dama',
    'em_msf_dama_prov':'dama',
    'em_msf_dama_ex1': 'dama',
    'em_msf_dama_ex2': 'dama',
    'em_msf_dama_ex':  'dama',
    'em_msf_dt_l1':    'dt',
    'em_msf_dt_hm':    'dt',
    'em_msf_dt_ex':    'dt',
    'em_msf_2t_l1':    '2t',
    'em_msf_2t_l2':    '2t',
    'em_msf_2t_hm':    '2t',
    'em_msf_2t_ex':    '2t',
    'em_msf_dn_l1':    'dn',
    'em_msf_dn_l2':    'dn',
    'em_msf_dn_hm':    'dn',
    'em_msf_dn_ex':    'dn',
    'em_msf_2n_l1':    '2n',
    'em_msf_2n_l2':    '2n',
    'em_msf_2n_hm':    '2n',
    'em_msf_dc_l1':    'dc',
    'em_msf_dc_hm':    'dc',
    'em_msf_dc_ex':    'dc',
}

# ── CSS de adăugat (același pentru toate paginile) ────────────────────────────
NEW_CSS = """
        /* ===== COLOANE LATERALE CU PIESE ===== */
        .page-wrapper {
            display: flex;
            align-items: flex-start;
            justify-content: center;
            gap: 12px;
        }

        .side-col {
            flex: 1 1 0;
            min-width: 80px;
            max-width: 180px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding-top: 50px;
        }

        .side-col img {
            width: 100%;
            aspect-ratio: 2 / 3;
            object-fit: fill;
            mix-blend-mode: multiply;
        }

        /* ===== TITLU CU PIESE FLANC ===== */
        .title-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
            margin-bottom: 20px;
            margin-top: 10px;
        }

        .title-piece {
            width: clamp(70px, 10vw, 130px);
            aspect-ratio: 2 / 3;
            object-fit: fill;
            mix-blend-mode: multiply;
            flex-shrink: 0;
        }

        .title-row h1 { margin-bottom: 0; margin-top: 0; }
        .title-row + .text-block { margin-top: 18px; }
"""

MOBILE_ADD = """            .side-col { display: none; }
            .title-row { gap: 8px; }
            .title-piece { width: 52px; height: 75px; }
"""

# ── HTML helpers ──────────────────────────────────────────────────────────────
def side_col_left():
    return (
        '\n<div class="side-col">\n'
        '    <img src="piese_sah/regina_medieval.jpg" alt="Regina albă">\n'
        '    <img src="piese_sah/rege_medieval" alt="Rege alb" style="filter:brightness(1.18);">\n'
        '    <img src="piese_sah/cal_medieval.jpg" alt="Cal alb">\n'
        '</div>\n\n'
    )

def side_col_right():
    return (
        '\n</div><!-- /.page -->\n\n'
        '<div class="side-col">\n'
        '    <img src="piese_sah/regina_medieval_negru.jpg" alt="Regina neagră">\n'
        '    <img src="piese_sah/rege_medieval_negru.jpg" alt="Rege negru">\n'
        '    <img src="piese_sah/cal_medieval_negru.jpg" alt="Cal negru">\n'
        '</div>\n\n'
        '</div><!-- /.page-wrapper -->'
    )

def title_img(fname):
    extra = ' style="filter:brightness(1.18);"' if fname == 'rege_medieval' else ''
    return f'        <img class="title-piece" src="piese_sah/{fname}" alt=""{extra}>\n'

def title_row_html(left_pieces):
    imgs_left  = ''.join(title_img(p) for p in left_pieces)
    img_right  = title_img('rege_medieval_negru.jpg')
    return imgs_left, img_right

# ── Procesare fișier ──────────────────────────────────────────────────────────
def process(path, subcap):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # ── 0. Skip dacă deja procesat ──
    if 'page-wrapper' in html:
        print(f'  SKIP (deja procesat): {os.path.basename(path)}')
        return

    # ── 1. Elimină CSS corner-piece ──
    html = re.sub(
        r'\s*\.corner-piece\s*\{[^}]*\}\s*\.corner-tl\s*\{[^}]*\}\s*\.corner-tr\s*\{[^}]*\}',
        '', html, flags=re.DOTALL
    )

    # ── 2. Modifică h1 CSS: margin 0 ──
    html = re.sub(
        r'(h1\s*\{[^}]*?)margin-bottom\s*:\s*[\d.]+[a-z]*;',
        r'\1margin-bottom: 0;', html, flags=re.DOTALL
    )
    html = re.sub(
        r'(h1\s*\{[^}]*?)margin-top\s*:\s*[\d.]+[a-z]*;',
        r'\1margin-top: 0;', html, flags=re.DOTALL
    )

    # ── 3. Adaugă CSS nou înainte de </style> ──
    html = html.replace('    </style>', NEW_CSS + '    </style>', 1)

    # ── 4. Adaugă .side-col { display:none } în media query ──
    html = re.sub(
        r'(@media\s*\(max-width:\s*680px\)\s*\{)',
        r'\1\n' + MOBILE_ADD,
        html
    )

    # ── 5. Elimină imaginile vechi de colț (div stânga + img dreapta) ──
    # Pattern: <div style="position:absolute;top:0;left:0;...">...</div>
    html = re.sub(
        r'<div\s+style="position:absolute;top:0;left:0;[^"]*"[^>]*>.*?</div>\s*\n?',
        '', html, flags=re.DOTALL
    )
    # img dreapta: <img src="piese_sah/rege 2.png" style="position:absolute;top:0;right:0;...">
    html = re.sub(
        r'<img\s+src="piese_sah/rege 2\.png"[^>]*>\s*\n?',
        '', html
    )
    # img colț generic cu position:absolute top:0
    html = re.sub(
        r'<img\s[^>]*style="position:absolute;top:0[^"]*"[^>]*>\s*\n?',
        '', html
    )

    # ── 6. Învelește <div class="page"> în page-wrapper ──
    html = html.replace(
        '<div class="page">',
        '<div class="page-wrapper">' + side_col_left() + '<div class="page">',
        1
    )

    # ── 7. Găsește h1 și înfășoară în title-row ──
    left_pieces = SUBCAP[subcap]
    imgs_left, img_right = title_row_html(left_pieces)

    # Înlocuiește <h1>...</h1> (poate fi pe mai multe rânduri)
    def wrap_h1(m):
        return (
            '    <div class="title-row">\n'
            + imgs_left
            + '        ' + m.group(0).strip() + '\n'
            + img_right
            + '    </div>'
        )
    html = re.sub(r'<h1>.*?</h1>', wrap_h1, html, count=1, flags=re.DOTALL)

    # ── 8. Închide page-wrapper după </div><!-- /.page sau ultimul </div> al .page ──
    # Găsim ultimul </div>\n</body> și inserăm înaintea </body>
    # Strategia: ultimul </div> înainte de </body> = închiderea lui .page
    # Înlocuim </div>\n\n<script> nu e bun; găsim </div> urmat de \n</body>
    # Mai sigur: înlocuim </div>\n\n</body> cu side_col_right()\n</body>

    # Căutăm pattern-ul: </div> pe o linie separată, urmat de newlines și </body>
    html = re.sub(
        r'(</div>)\s*\n(\s*<script\s+src[^<]*>\s*</script>\s*\n)*\s*\n?(</body>)',
        lambda m: side_col_right() + '\n\n' + (m.group(2) or '') + m.group(3),
        html
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {os.path.basename(path)} [{subcap}]')


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import glob
    files = sorted(glob.glob(os.path.join(BASE, 'pagina*.html')))
    processed = 0
    for fpath in files:
        with open(fpath, encoding='utf-8') as f:
            content = f.read()
        m = re.search(r"PAGE_ID\s*=\s*'([^']+)'", content)
        if not m:
            continue
        pid = m.group(1)
        if pid in PAGE_SUBCAP:
            subcap = PAGE_SUBCAP[pid]
            process(fpath, subcap)
            processed += 1

    print(f'\nGata! {processed} pagini procesate.')
