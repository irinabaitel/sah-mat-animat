"""
fetch_morphy.py — Ia puzzle-uri morphysMate de pe Lichess API si actualizeaza pagina83.html

Utilizare:
    python fetch_morphy.py

Necesita:
    - pip install chess  (python-chess)
    - Token Lichess setat in variabila LICHESS_TOKEN de mai jos
      (sau ca variabila de mediu: set LICHESS_TOKEN=lip_xxx)
"""

import os, json, re, io, sys
import urllib.request
import chess, chess.pgn

# ── CONFIGURARE ────────────────────────────────────────────────────────────────
LICHESS_TOKEN = os.environ.get('LICHESS_TOKEN', '')
HTML_FILE     = os.path.join(os.path.dirname(__file__), 'pagina83.html')

TEMA          = 'morphysMate'
FETCH_PER_REQ = 50      # cate puzzle-uri cerem per request
NR_REQUESTS   = 8       # 8x50 = 400 brut, suficient pentru filtrare
MIN_PLAYS     = 100     # popularitate minima
MIN_SOL_LEN   = 3       # minim 3 mutari in solutie (nu puzzle-uri de 1 mutare)
MAX_SOL_LEN   = 11      # maxim 11 mutari
# ──────────────────────────────────────────────────────────────────────────────

# Tinte: 10 usor, 20 mediu, 10 greu
EASY_TARGET   = 10
MEDIUM_TARGET = 20
HARD_TARGET   = 10

EASY_MAX_R    = 1200
HARD_MIN_R    = 1700


def fetch_batch(nb: int) -> list[dict]:
    url = f'https://lichess.org/api/puzzle/batch/{TEMA}?nb={nb}'
    headers = {'Accept': 'application/json'}
    if LICHESS_TOKEN:
        headers['Authorization'] = f'Bearer {LICHESS_TOKEN}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())['puzzles']


def validate_puzzle(raw: dict) -> dict | None:
    """
    Extrage FEN de start si valideaza intreaga solutie prin python-chess.
    Returneaza dict sau None.
    """
    try:
        pgn_text = raw['game']['pgn']
        init_ply = raw['puzzle']['initialPly']
        solution = raw['puzzle']['solution']

        game  = chess.pgn.read_game(io.StringIO(f'[Event "?"]\n1. {pgn_text}'))
        board = game.board()

        for i, move in enumerate(game.mainline_moves()):
            if i >= init_ply + 1:
                break
            board.push(move)

        # Prima mutare din solutie trebuie sa fie legala
        if chess.Move.from_uci(solution[0]) not in board.legal_moves:
            return None

        # Verifica intreaga solutie
        test = board.copy()
        for uci in solution:
            mv = chess.Move.from_uci(uci)
            if mv not in test.legal_moves:
                return None
            test.push(mv)

        # Trebuie sa se termine cu mat
        if not test.is_checkmate():
            return None

        turn = 'w' if board.turn == chess.WHITE else 'b'
        return {
            'id':     raw['puzzle']['id'],
            'fen':    board.fen(),
            'sol':    solution,
            'turn':   turn,
            'rating': raw['puzzle']['rating'],
            'plays':  raw['puzzle']['plays'],
        }
    except Exception:
        return None


def collect_all() -> list[dict]:
    """Descarca NR_REQUESTS runde si returneaza puzzle-urile valide unice."""
    seen_ids = set()
    raw_list = []
    for i in range(NR_REQUESTS):
        print(f'  Round {i+1}/{NR_REQUESTS}...', end=' ', flush=True)
        try:
            batch = fetch_batch(FETCH_PER_REQ)
            new = 0
            for p in batch:
                pid = p['puzzle']['id']
                if pid not in seen_ids:
                    seen_ids.add(pid)
                    raw_list.append(p)
                    new += 1
            print(f'+{new} unice ({len(raw_list)} total)')
        except Exception as e:
            print(f'EROARE: {e}')

    print(f'\nBrut: {len(raw_list)} puzzle-uri unice. Validez...')

    valid = []
    for raw in raw_list:
        p   = raw['puzzle']
        sol = p['solution']

        if p['plays'] < MIN_PLAYS:
            continue
        if len(sol) < MIN_SOL_LEN or len(sol) > MAX_SOL_LEN:
            continue

        result = validate_puzzle(raw)
        if result is None:
            continue
        valid.append(result)

    print(f'Valide dupa filtrare: {len(valid)}')
    return valid


def pick_by_level(puzzles: list[dict]) -> list[dict]:
    """Alege 10 usoare + 20 medii + 10 grele, distribuite uniform in rating."""
    puzzles.sort(key=lambda x: x['rating'])

    easy   = [p for p in puzzles if p['rating'] <= EASY_MAX_R]
    hard   = [p for p in puzzles if p['rating'] >= HARD_MIN_R]
    medium = [p for p in puzzles if EASY_MAX_R < p['rating'] < HARD_MIN_R]

    def pick_n(lst, n):
        if len(lst) <= n:
            return lst
        step = len(lst) / n
        return [lst[int(i * step)] for i in range(n)]

    selected_easy   = pick_n(easy,   EASY_TARGET)
    selected_medium = pick_n(medium, MEDIUM_TARGET)
    selected_hard   = pick_n(hard,   HARD_TARGET)

    print(f'\nDisponibile: easy={len(easy)}, medium={len(medium)}, hard={len(hard)}')
    print(f'Selectate:  easy={len(selected_easy)}, medium={len(selected_medium)}, hard={len(selected_hard)}')

    if len(selected_easy) < EASY_TARGET:
        print(f'ATENTIE: doar {len(selected_easy)}/{EASY_TARGET} puzzle-uri usoare!')
    if len(selected_medium) < MEDIUM_TARGET:
        print(f'ATENTIE: doar {len(selected_medium)}/{MEDIUM_TARGET} puzzle-uri medii!')
    if len(selected_hard) < HARD_TARGET:
        print(f'ATENTIE: doar {len(selected_hard)}/{HARD_TARGET} puzzle-uri grele!')

    return selected_easy + selected_medium + selected_hard


def to_js_array(puzzles: list[dict]) -> str:
    """Genereaza blocul JS cu array-ul PUZZLES."""
    easy_count   = sum(1 for p in puzzles[:EASY_TARGET])
    medium_count = sum(1 for p in puzzles[EASY_TARGET:EASY_TARGET+MEDIUM_TARGET])
    hard_count   = sum(1 for p in puzzles[EASY_TARGET+MEDIUM_TARGET:])

    lines = ['const PUZZLES=[']
    boundaries = {
        0:                          f'  /* 0-{EASY_TARGET-1} USOR */',
        EASY_TARGET:                f'  /* {EASY_TARGET}-{EASY_TARGET+MEDIUM_TARGET-1} MEDIU */',
        EASY_TARGET+MEDIUM_TARGET:  f'  /* {EASY_TARGET+MEDIUM_TARGET}-{len(puzzles)-1} GREU */',
    }
    for i, p in enumerate(puzzles):
        if i in boundaries:
            lines.append(boundaries[i])
        sol_js = "['" + "','".join(p['sol']) + "']"
        lines.append(f"  {{id:'{p['id']}',fen:'{p['fen']}',sol:{sol_js},turn:'{p['turn']}'}},  // r{p['rating']} x{p['plays']} {len(p['sol'])}mut")

    lines.append('];')
    return '\n'.join(lines)


def update_html(puzzles: list[dict]):
    """Inlocuieste sectiunea PUZZLES din pagina83.html."""
    with open(HTML_FILE, encoding='utf-8') as f:
        content = f.read()

    start = content.find('const PUZZLES=[')
    end   = content.find('];', start) + 2
    if start == -1 or end == 1:
        print('EROARE: nu am gasit const PUZZLES=[ in HTML!')
        return

    new_js      = to_js_array(puzzles)
    new_content = content[:start] + new_js + content[end:]

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'\nActualizat {HTML_FILE} cu {len(puzzles)} puzzle-uri.')
    for i, p in enumerate(puzzles):
        lv = 'USOR' if i < EASY_TARGET else ('MEDIU' if i < EASY_TARGET+MEDIUM_TARGET else 'GREU')
        print(f'  [{lv}] {p["id"]} r={p["rating"]} {len(p["sol"])}mut  {p["sol"]}')


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    print(f'Fetchuiesc puzzle-uri {TEMA} de pe Lichess API...')
    if not LICHESS_TOKEN:
        print('(fara token — incerc oricum, unele endpoint-uri sunt publice)\n')

    valid = collect_all()

    if len(valid) < EASY_TARGET + MEDIUM_TARGET + HARD_TARGET:
        print(f'\nPrea putine puzzle-uri valide ({len(valid)})!')
        print('Incearca sa maresti NR_REQUESTS sau sa relaxezi MIN_SOL_LEN.')
        sys.exit(1)

    puzzles = pick_by_level(valid)
    update_html(puzzles)
    print('\nGata!')


if __name__ == '__main__':
    main()
