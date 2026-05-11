"""
fetch_damiano.py — Ia puzzle-uri damianosMate de pe Lichess API si actualizeaza pagina87.html

Utilizare:
    python fetch_damiano.py

Necesita:
    - pip install chess  (python-chess)
    - Token Lichess setat in variabila LICHESS_TOKEN de mai jos
      (sau ca variabila de mediu: set LICHESS_TOKEN=lip_xxx)
"""

import os, json, io, sys, time
import urllib.request
import chess, chess.pgn

# ── CONFIGURARE ────────────────────────────────────────────────────────────────
LICHESS_TOKEN = os.environ.get('LICHESS_TOKEN', '')
HTML_FILE     = os.path.join(os.path.dirname(__file__), 'pagina87.html')

TEMA          = 'damianosMate'
FETCH_PER_REQ = 2
NR_REQUESTS   = 10
MIN_PLAYS     = 0
MIN_SOL_LEN   = 3
MAX_SOL_LEN   = 11
# ──────────────────────────────────────────────────────────────────────────────

EASY_TARGET   = 10
MEDIUM_TARGET = 20
HARD_TARGET   = 10

DIFFICULTY_EASY   = 'easier'
DIFFICULTY_MEDIUM = 'normal'
DIFFICULTY_HARD   = 'harder'


def fetch_batch(nb: int, difficulty: str = 'normal') -> list[dict]:
    url = f'https://lichess.org/api/puzzle/batch/{TEMA}?nb={nb}&difficulty={difficulty}'
    headers = {'Accept': 'application/json'}
    if LICHESS_TOKEN:
        headers['Authorization'] = f'Bearer {LICHESS_TOKEN}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())['puzzles']


def validate_puzzle(raw: dict) -> dict | None:
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

        if chess.Move.from_uci(solution[0]) not in board.legal_moves:
            return None

        test = board.copy()
        for uci in solution:
            mv = chess.Move.from_uci(uci)
            if mv not in test.legal_moves:
                return None
            test.push(mv)

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


def collect_level(difficulty: str, target: int) -> list[dict]:
    seen_ids = set()
    raw_list = []
    needed   = max(target * 8, 40)
    rounds   = (needed // FETCH_PER_REQ) + 2

    print(f'  [{difficulty}] {rounds} requesturi...')
    for i in range(rounds):
        print(f'    Round {i+1}/{rounds}...', end=' ', flush=True)
        try:
            batch = fetch_batch(FETCH_PER_REQ, difficulty)
            new = sum(1 for p in batch if p['puzzle']['id'] not in seen_ids and not seen_ids.add(p['puzzle']['id']))
            raw_list.extend(p for p in batch if p['puzzle']['id'] in seen_ids)
            print(f'+{new} unice ({len(seen_ids)} total)')
        except Exception as e:
            print(f'EROARE: {e}')
        time.sleep(15)

    # validare
    valid = []
    for raw in raw_list:
        p   = raw['puzzle']
        sol = p['solution']
        if p['plays'] < MIN_PLAYS:
            continue
        if len(sol) < MIN_SOL_LEN or len(sol) > MAX_SOL_LEN:
            continue
        result = validate_puzzle(raw)
        if result:
            valid.append(result)

    # elimina duplicate intre runde
    seen = set(); dedup = []
    for p in valid:
        if p['id'] not in seen:
            seen.add(p['id']); dedup.append(p)

    dedup.sort(key=lambda x: x['rating'])
    print(f'  [{difficulty}] valide: {len(dedup)}')
    return dedup


def collect_all() -> tuple[list, list, list]:
    print('Fetching EASY...')
    easy_raw = collect_level(DIFFICULTY_EASY, EASY_TARGET)
    print('Fetching MEDIUM...')
    med_raw  = collect_level(DIFFICULTY_MEDIUM, MEDIUM_TARGET)
    print('Fetching HARD...')
    hard_raw = collect_level(DIFFICULTY_HARD, HARD_TARGET)
    return easy_raw, med_raw, hard_raw


def pick_n(lst, n):
    if len(lst) <= n:
        return lst
    step = len(lst) / n
    return [lst[int(i * step)] for i in range(n)]


def pick_by_level(easy_raw, med_raw, hard_raw) -> list[dict]:
    sel_easy = pick_n(easy_raw, EASY_TARGET)
    sel_med  = pick_n(med_raw,  MEDIUM_TARGET)
    sel_hard = pick_n(hard_raw, HARD_TARGET)

    print(f'\nSelectate: easy={len(sel_easy)}, medium={len(sel_med)}, hard={len(sel_hard)}')
    for lbl, lst, tgt in [('USOR', sel_easy, EASY_TARGET), ('MEDIU', sel_med, MEDIUM_TARGET), ('GREU', sel_hard, HARD_TARGET)]:
        if len(lst) < tgt:
            print(f'ATENTIE: doar {len(lst)}/{tgt} puzzle-uri {lbl}!')

    return sel_easy + sel_med + sel_hard


def to_js_array(puzzles: list[dict]) -> str:
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
        print('(fara token — incerc oricum)\n')

    easy_raw, med_raw, hard_raw = collect_all()

    puzzles = pick_by_level(easy_raw, med_raw, hard_raw)
    if len(puzzles) < EASY_TARGET + MEDIUM_TARGET + HARD_TARGET:
        print(f'\nPrea putine puzzle-uri ({len(puzzles)})!')
        sys.exit(1)
    update_html(puzzles)
    print('\nGata!')


if __name__ == '__main__':
    main()
