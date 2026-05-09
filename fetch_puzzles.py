"""
fetch_puzzles.py — Ia puzzle-uri de pe Lichess API si actualizeaza pagina75.html

Utilizare:
    python fetch_puzzles.py

Necesita:
    - pip install chess  (python-chess)
    - Token Lichess setat in variabila LICHESS_TOKEN de mai jos
      (sau ca variabila de mediu: set LICHESS_TOKEN=lip_xxx)
"""

import os, json, re, io, sys
import urllib.request
import chess, chess.pgn

# ── CONFIGURARE ────────────────────────────────────────────────────────────────
LICHESS_TOKEN = os.environ.get('LICHESS_TOKEN', '')  # pune tokenul tau aici sau in variabila de mediu LICHESS_TOKEN
HTML_FILE     = os.path.join(os.path.dirname(__file__), 'pagina75.html')

TEME = ['doubleBishopMate', 'bodenMate']   # temele de filtrat
NR_PE_TEMA    = 20     # cate puzzle-uri vrem din fiecare tema
FETCH_PER_REQ = 50     # cate puzzle-uri cerem per request
NR_REQUESTS   = 4      # cate requesturi facem (strangem 4x50 = 200 per tema)
MIN_PLAYS     = 200    # popularitate minima (nr. rezolvari pe Lichess)
MIN_RATING    = 700    # rating minim
MAX_RATING    = 1900   # rating maxim
MAX_SOL_LEN   = 7      # max mutari in solutie
# ──────────────────────────────────────────────────────────────────────────────


def fetch_puzzles_for_theme(theme: str, nb: int) -> list[dict]:
    """Descarca `nb` puzzle-uri cu tema `theme` de pe Lichess API."""
    url = f'https://lichess.org/api/puzzle/batch/{theme}?nb={nb}'
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {LICHESS_TOKEN}',
        'Accept': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())['puzzles']


def fen_from_puzzle(raw: dict) -> tuple[str, str] | None:
    """
    Din datele brute Lichess, returneaza (fen, turn) — pozitia de start a puzzle-ului.
    Aplica initialPly+1 mutari din PGN.
    Returneaza None daca ceva e invalid.
    """
    try:
        pgn_text  = raw['game']['pgn']
        init_ply  = raw['puzzle']['initialPly']
        solution  = raw['puzzle']['solution']

        game  = chess.pgn.read_game(io.StringIO(f'[Event "?"]\n1. {pgn_text}'))
        board = game.board()

        for i, move in enumerate(game.mainline_moves()):
            if i >= init_ply + 1:
                break
            board.push(move)

        # Verifica ca prima mutare din solutie e legala
        if chess.Move.from_uci(solution[0]) not in board.legal_moves:
            return None

        # Verifica intreaga solutie
        test = board.copy()
        for uci in solution:
            mv = chess.Move.from_uci(uci)
            if mv not in test.legal_moves:
                return None
            test.push(mv)

        # Ultimul test: solutia trebuie sa se termine cu mat
        if not test.is_checkmate():
            return None

        turn = 'w' if board.turn == chess.WHITE else 'b'
        return board.fen(), turn

    except Exception:
        return None


def process_theme(theme: str) -> list[dict]:
    """Descarca (mai multe runde), filtreaza si returneaza puzzle-urile valide."""
    print(f'\nFetchuiesc puzzle-uri pentru tema: {theme} ...')
    seen_ids = set()
    raw_list = []
    for i in range(NR_REQUESTS):
        batch = fetch_puzzles_for_theme(theme, FETCH_PER_REQ)
        for p in batch:
            pid = p['puzzle']['id']
            if pid not in seen_ids:
                seen_ids.add(pid)
                raw_list.append(p)
    print(f'  Primite unice: {len(raw_list)}')

    valid = []
    for raw in raw_list:
        p   = raw['puzzle']
        sol = p['solution']

        # Filtre simple (fara sa parsam PGN — rapid)
        if p['plays'] < MIN_PLAYS:
            continue
        if not (MIN_RATING <= p['rating'] <= MAX_RATING):
            continue
        if len(sol) > MAX_SOL_LEN:
            continue

        # Parseaza PGN si obtine FEN
        result = fen_from_puzzle(raw)
        if result is None:
            continue
        fen, turn = result

        valid.append({
            'id':     p['id'],
            'fen':    fen,
            'sol':    sol,
            'turn':   turn,
            'rating': p['rating'],
            'plays':  p['plays'],
            'theme':  theme,
        })

    print(f'  Valide dupa filtrare: {len(valid)}')
    return valid


def pick_distributed(puzzles: list[dict], n: int) -> list[dict]:
    """Alege `n` puzzle-uri distribuite uniform dupa rating."""
    puzzles.sort(key=lambda x: x['rating'])
    if len(puzzles) <= n:
        return puzzles
    step = len(puzzles) / n
    return [puzzles[int(i * step)] for i in range(n)]


def to_js_array(puzzles: list[dict]) -> str:
    """Genereaza blocul JS cu array-ul PUZZLES."""
    lines = ['const PUZZLES=[']

    boundaries = {0: '  /* 0-19 USOR */', 20: '  /* 20-33 MEDIU */', 34: '  /* 34-39 AVANSAT */'}
    for i, p in enumerate(puzzles):
        if i in boundaries:
            lines.append(boundaries[i])
        sol_js = "['" + "','".join(p['sol']) + "']"
        tag = 'DB' if p['theme'] == 'doubleBishopMate' else 'BM'
        lines.append(f"  {{id:'{p['id']}',fen:'{p['fen']}',sol:{sol_js},turn:'{p['turn']}'}},  // {tag} r{p['rating']} x{p['plays']}")

    lines.append('];')
    return '\n'.join(lines)


def update_html(puzzles: list[dict]):
    """Inlocuieste sectiunea PUZZLES din pagina75.html."""
    with open(HTML_FILE, encoding='utf-8') as f:
        content = f.read()

    start = content.find('const PUZZLES=[')
    end   = content.find('];', start) + 2
    if start == -1 or end == 1:
        print('EROARE: nu am gasit const PUZZLES=[ in HTML!')
        return

    # Actualizeaza si levelOf cu pragurile corecte
    new_js    = to_js_array(puzzles)
    new_content = content[:start] + new_js + content[end:]

    # Asigura ca levelOf foloseste 20/34
    new_content = re.sub(
        r'function levelOf\(idx\)\{[^}]+\}',
        'function levelOf(idx){ if(idx<20)return 0; if(idx<34)return 1; return 2; }',
        new_content
    )

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'\nActualizat {HTML_FILE} cu {len(puzzles)} puzzle-uri.')


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    all_puzzles = []
    for theme in TEME:
        raw = process_theme(theme)
        selected = pick_distributed(raw, NR_PE_TEMA)
        all_puzzles.extend(selected)

    # Amesteca dupa rating
    all_puzzles.sort(key=lambda x: x['rating'])
    total = len(all_puzzles)
    print(f'\nTotal puzzle-uri selectate: {total}')
    print('Ratings:', [p['rating'] for p in all_puzzles])

    update_html(all_puzzles)
    print('Gata!')


if __name__ == '__main__':
    main()
