#!/usr/bin/env python3
"""
Aplică formatul nivel1 pe paginile nivel3 rămase.
Rulează din directorul SahMatAnimat.
"""
import re, os

# ── Fișiere de procesat + titlul din nav ──────────────────────────────────────
FILES = {
    "pagina28.html":              "Exercițiu — Metoda Cuștii",
    "pagina29.html":              "Arena — Damă vs. Rege",
    "pagina31.html":              "Echipa de Șoc — Turn + Rege",
    "pagina32.html":              "Hartă Mentală — Turn + Rege",
    "pagina35.html":              "Arena — Două Turnuri vs. Rege",
    "pagina36.html":              "Arena — Damă + Nebun vs. Rege",
}

# ── Fix navigare ──────────────────────────────────────────────────────────────
NAV_FIXES = {
    # pagina28 now runs after pagina27 (Provocarea Reginei); already has back=pagina27, forward=pagina29 — OK
    # pagina35 back=pagina14 OK; pagina36 back=pagina18 OK
    # (fișier, ce căutăm în href, înlocuim cu)
    "pagina26.html": [
        ('pagina37.html" class="nav-next"', 'pagina27.html" class="nav-next"'),
        ('pagina37.html" class="nav-btn"',  'pagina27.html" class="nav-btn"'),
    ],
    "pagina27.html": [
        ('pagina28.html" class="nav-next"', 'pagina37.html" class="nav-next"'),
        ('pagina28.html" class="nav-btn"',  'pagina37.html" class="nav-btn"'),
    ],
    "pagina37.html": [
        ('pagina26.html" class="nav-prev"', 'pagina27.html" class="nav-prev"'),
        ('pagina26.html" class="nav-btn back"', 'pagina27.html" class="nav-btn back"'),
        ('pagina27.html" class="nav-next"', 'pagina28.html" class="nav-next"'),
        ('pagina27.html" class="nav-btn"',  'pagina28.html" class="nav-btn"'),
    ],
    "pagina33.html": [
        ('pagina34.html" class="nav-next"', 'hub.html" class="nav-next"'),
        ('pagina34.html" class="nav-btn"',  'hub.html" class="nav-btn"'),
    ],
}

NEW_CSS = '''\
        body { background: #F5A96E; font-family: 'Nunito', sans-serif; color: #1a1a2e; padding: 0 0 60px; }

        #nav {
            position: sticky; top: 0;
            background: rgba(245,169,110,0.92);
            backdrop-filter: blur(8px);
            display: flex; align-items: center; justify-content: space-between;
            padding: 10px 20px; z-index: 100;
            border-bottom: 2px solid rgba(255,255,255,0.4);
        }
        .nav-btn { background: rgba(255,255,255,0.55); border: 2px solid rgba(255,255,255,0.8); border-radius: 50px; padding: 6px 16px; font-family: 'Baloo 2', cursive; font-size: 0.88em; font-weight: 700; color: #1a3a6b; text-decoration: none; transition: background 0.2s; }
        .nav-btn:hover { background: rgba(255,255,255,0.85); }
        .nav-title { font-family: 'Baloo 2', cursive; font-size: 0.9em; color: #1a3a6b; text-align: center; }
        .nav-badge { background: #1a3a6b; color: white; font-family: 'Baloo 2', cursive; font-size: 0.75em; font-weight: 700; padding: 3px 12px; border-radius: 20px; letter-spacing: 0.06em; }

        .content { max-width: 780px; margin: 0 auto; padding: 28px 16px 0; display: flex; flex-direction: column; gap: 20px; }

        .lesson-title { text-align: center; margin-bottom: 8px; }
        .lesson-title h1 { font-family: 'Baloo 2', cursive; font-size: clamp(1.7em,5vw,2.4em); color: #1a3a6b; text-shadow: 2px 2px 0 rgba(255,255,255,0.4); line-height: 1.2; }

        .card { background: rgba(255,255,255,0.58); border: 2px solid rgba(255,255,255,0.85); border-radius: 20px; padding: 22px 24px; box-shadow: 0 3px 16px rgba(0,0,0,0.07); }
        .card p { font-size: 0.96em; line-height: 1.75; color: #2a2a3e; margin-bottom: 10px; text-align: justify; }
        .card p:last-child { margin-bottom: 0; }

        .bottom-nav { display: flex; justify-content: space-between; align-items: center; gap: 16px; margin-top: 8px; }
        .nav-next { background: #1a3a6b; color: white; font-family: 'Baloo 2', cursive; font-size: 0.95em; font-weight: 700; padding: 9px 22px; border-radius: 50px; text-decoration: none; transition: all 0.2s; box-shadow: 0 3px 12px rgba(26,58,107,0.35); }
        .nav-next:hover { background: #2a5aab; transform: translateY(-2px); }
        .nav-prev { background: rgba(255,255,255,0.45); border: 2px solid rgba(255,255,255,0.7); border-radius: 50px; padding: 9px 20px; font-family: 'Baloo 2', cursive; font-size: 0.85em; font-weight: 700; color: #1a3a6b; text-decoration: none; transition: background 0.2s; white-space: nowrap; }
        .nav-prev:hover { background: rgba(255,255,255,0.75); }

        @media (max-width: 560px) { .main-content { flex-direction: column; } .board-section { margin: 0 auto; } }'''

def remove_css_block(html, pattern):
    """Șterge un bloc CSS definit de pattern (regex) + acoladele sale."""
    return re.sub(pattern, '', html, flags=re.DOTALL)

def apply_format(fname, nav_title):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # ── 1. Șterge al doilea bloc <style> (col fixe cu !important) ─────────────
    # Unele pagini au un al doilea <style>...</style> cu reguli pentru side-col
    html = re.sub(r'\n<style>\n(?:[^<]|<(?!/style>))*?\.side-col[^<]*?</style>', '', html, flags=re.DOTALL)
    # Și cel cu .hub-btn la final
    html = re.sub(r'\n<style>\s*\.hub-btn\b.*?</style>\s*\n<a [^>]*hub-btn[^>]*>.*?</a>', '', html, flags=re.DOTALL)
    # Și cel cu .piece-row la final (dacă a rămas)
    html = re.sub(r'\n<style>\s*\.piece-row\b.*?</style>', '', html, flags=re.DOTALL)

    # ── 2. Înlocuiește body { ... } cu versiunea nouă ─────────────────────────
    html = re.sub(
        r'body\s*\{[^}]*background:\s*#F5A96E[^}]*\}',
        "body { background: #F5A96E; font-family: 'Nunito', sans-serif; color: #1a1a2e; padding: 0 0 60px; }",
        html, flags=re.DOTALL
    )

    # ── 3. Șterge blocuri CSS vechi ───────────────────────────────────────────
    patterns_to_remove = [
        r'\s*\.page\s*\{[^}]*\}',
        r'\s*/\*\s*=+\s*TITLU[^*]*\*/.*?\.title-row\s*\+\s*\.text-block\s*\{[^}]*\}',
        r'\s*\.title-row\s*h1\s*\{[^}]*\}',
        r'\s*\.title-row\s*\+\s*\.text-block\s*\{[^}]*\}',
        r'\s*\.title-row\s*\{[^}]*\}',
        r'\s*\.title-piece\s*\{[^}]*\}',
        r'\s*\.corner-piece\s*\{[^}]*\}',
        r'\s*\.corner-tl\s*\{[^}]*\}',
        r'\s*\.corner-tr\s*\{[^}]*\}',
        r'\s*\.text-block\s*\{[^}]*\}',
        r'\s*\.intro\s*\{[^}]*\}',
        # nav vechi (top-nav + tnav-*)
        r'\s*/\*\s*=+\s*TOP NAV[^*]*\*/.*?\.tnav-badge\s*\{[^}]*\}',
        r'\s*#top-nav\s*\{[^}]*\}',
        r'\s*\.tnav-btn\s*\{[^}]*\}',
        r'\s*\.tnav-btn:hover\s*\{[^}]*\}',
        r'\s*\.tnav-title\s*\{[^}]*\}',
        r'\s*\.tnav-badge\s*\{[^}]*\}',
        # nav buttons vechi (mari, cu box-shadow)
        r'\s*\.nav-buttons\s*\{[^}]*\}',
        r'\s*\.nav-btn\.back\s*\{[^}]*\}',
        r'\s*\.nav-btn\.disabled\s*\{[^}]*\}',
        # h1 standalone (dacă e înainte de conținut specific)
        r'\s*/\*\s*=+\s*TITLU CU PIESE FLANC[^*]*\*/[^/]*?\.title-row\s*\+\s*\.text-block\s*\{[^}]*\}',
        # text justify global
        r'\s*/\*\s*text justify global\s*\*/.*?(?=\n\s*\n|\n\s*/\*|\s*</style>)',
        # coloane laterale
        r'\s*/\*\s*=+\s*COLOANE[^*]*\*/.*?(?=\s*/\*|\s*</style>)',
        r'\s*\.page-wrapper\s*\{[^}]*\}',
        r'\s*\.side-col\s*\{[^}]*\}',
        r'\s*\.side-col\s*img\s*\{[^}]*\}',
        # media query vechi
        r'\s*@media\s*\(max-width:\s*(?:680|780|900)px\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}',
    ]
    for p in patterns_to_remove:
        html = re.sub(p, '', html, flags=re.DOTALL)

    # Șterge și blocul nav-btn vechi (cel mare cu font-size 1.3em)
    html = re.sub(
        r'\s*\.nav-btn\s*\{[^}]*font-size:\s*1\.3em[^}]*\}\s*\.nav-btn:hover\s*\{[^}]*\}',
        '', html, flags=re.DOTALL
    )
    # Dacă a mai rămas un nav-btn generic standalone
    html = re.sub(
        r'\s*\.nav-btn\s*\{\s*display:\s*inline-block[^}]*\}',
        '', html, flags=re.DOTALL
    )

    # ── 4. Inserează noul CSS după `* { box-sizing... }` ──────────────────────
    html = re.sub(
        r'(\* \{ box-sizing: border-box; margin: 0; padding: 0; \})',
        r'\1\n' + NEW_CSS,
        html
    )

    # ── 5. Curăță HTML ────────────────────────────────────────────────────────
    # Șterge side-col stânga (înainte de <div class="page">)
    html = re.sub(
        r'<div class="page-wrapper">\s*<div class="side-col">.*?</div>\s*(?=<div class="page">)',
        '', html, flags=re.DOTALL
    )
    # Șterge side-col dreapta + închidere page-wrapper (după </div><!-- /.page -->)
    html = re.sub(
        r'</div><!--\s*/\.page\s*-->\s*<div class="side-col">.*?</div>\s*</div><!--\s*/\.page-wrapper\s*-->',
        '</div>', html, flags=re.DOTALL
    )
    # Dacă page-wrapper simplu (fără comentariu)
    html = re.sub(r'<div class="page-wrapper">\s*', '', html)
    html = re.sub(r'</div>\s*<!--\s*/\.page-wrapper\s*-->', '', html)
    # Șterge side-col rămas
    html = re.sub(r'<div class="side-col">.*?</div>\s*', '', html, flags=re.DOTALL)
    # Șterge corner-piece img
    html = re.sub(r'\s*<img[^>]*corner-piece[^>]*>\s*', '\n', html)

    # Înlocuiește <nav id="top-nav"> cu noul nav (sau adaugă nav dacă lipsește)
    nav_html = (
        f'\n<nav id="nav">\n'
        f'    <a href="hub.html" class="nav-btn">&#9776; Cuprins</a>\n'
        f'    <div class="nav-title">{nav_title}</div>\n'
        f'    <span class="nav-badge">Nivelul III</span>\n'
        f'</nav>\n'
    )
    if 'id="top-nav"' in html:
        html = re.sub(r'<nav id="top-nav">.*?</nav>', nav_html.strip(), html, flags=re.DOTALL)
    elif '<nav id="nav">' not in html:
        # Inserează după <body>
        html = html.replace('<body>\n', '<body>\n' + nav_html)

    # <div class="page"> → <div class="content">
    html = html.replace('<div class="page">', '<div class="content">')
    html = re.sub(r'</div><!--\s*/\.page\s*-->', '</div>', html)

    # <div class="title-row"> → <div class="lesson-title">
    html = html.replace('<div class="title-row">', '<div class="lesson-title">')

    # .text-block → .card cu <p>
    def replace_text_block(m):
        inner = m.group(1).strip()
        return f'<div class="card"><p>{inner}</p></div>'
    html = re.sub(
        r'<div class="text-block">(.*?)</div>',
        replace_text_block, html, flags=re.DOTALL
    )

    # nav-buttons → bottom-nav
    html = html.replace('<div class="nav-buttons">', '<div class="bottom-nav">')
    # nav-btn back → nav-prev
    html = re.sub(r'class="nav-btn back"', 'class="nav-prev"', html)
    # nav-btn" (forward) → nav-next (doar linkurile, nu class-ul din CSS)
    html = re.sub(r'class="nav-btn">(&#206;nainte|Înainte)', r'class="nav-next">\1', html)
    # span nav-btn dezactivat
    html = re.sub(
        r'<span class="nav-btn"([^>]*)>(&#206;nainte|Înainte.*?)</span>',
        r'<span class="nav-next"\1>\2</span>', html
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ {fname}")

# ── Fix navigare ──────────────────────────────────────────────────────────────
def fix_nav(fname, replacements):
    path = os.path.join(os.path.dirname(__file__), fname)
    if not os.path.exists(path):
        print(f"  SKIP (negăsit): {fname}")
        return
    with open(path, encoding='utf-8') as f:
        html = f.read()
    for old, new in replacements:
        html = html.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ nav fix: {fname}")

if __name__ == '__main__':
    print("=== Fix format ===")
    for fname, title in FILES.items():
        apply_format(fname, title)

    print("\n=== Fix navigare ===")
    for fname, replacements in NAV_FIXES.items():
        fix_nav(fname, replacements)

    print("\nGata!")
