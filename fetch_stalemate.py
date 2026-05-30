"""
fetch_stalemate.py — Ia 25 puzzle-uri 'stalemate' de pe Lichess API

Utilizare:
    set LICHESS_TOKEN=lip_xxxxx
    python fetch_stalemate.py

Necesita:
    - pip install chess
"""

import os, json, io, sys, time
import urllib.request
import chess, chess.pgn

LICHESS_TOKEN = os.environ.get('LICHESS_TOKEN', '')
OUTPUT_FILE   = 'data/stalemate_top25.json'
NB_FETCH      = 50   # per request
NR_REQUESTS   = 6    # 6 x 50 = 300 candidate
TARGET        = 25
MIN_RATING    = 600
MAX_RATING    = 2000
MAX_SOL_LEN   = 9


def fetch_batch(nb):
    url = f'https://lichess.org/api/puzzle/batch/stalemate?nb={nb}'
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {LICHESS_TOKEN}',
        'Accept': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())['puzzles']


def verify(raw):
    """Returneaza dict puzzle sau None daca invalid."""
    try:
        p   = raw['puzzle']
        sol = p['solution']
        if not (MIN_RATING <= p['rating'] <= MAX_RATING): return None
        if len(sol) > MAX_SOL_LEN: return None

        pgn_text = raw['game']['pgn']
        init_ply = raw['puzzle']['initialPly']

        game  = chess.pgn.read_game(io.StringIO(f'[Event "?"]\n1. {pgn_text}'))
        board = game.board()
        for i, move in enumerate(game.mainline_moves()):
            if i >= init_ply + 1: break
            board.push(move)

        if chess.Move.from_uci(sol[0]) not in board.legal_moves: return None

        test = board.copy()
        for uci in sol:
            mv = chess.Move.from_uci(uci)
            if mv not in test.legal_moves: return None
            test.push(mv)

        if not test.is_stalemate(): return None

        moves_uci = [m for m in sol]
        level = 1 if p['rating'] < 1200 else (2 if p['rating'] < 1600 else 3)

        return {
            'id':       p['id'],
            'fen':      board.fen(),
            'moves':    moves_uci,
            'rating':   p['rating'],
            'level':    level,
            'themes':   p.get('themes', []),
        }
    except Exception as e:
        return None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if not LICHESS_TOKEN:
        print('EROARE: seteaza LICHESS_TOKEN ca variabila de mediu.')
        print('  Windows: set LICHESS_TOKEN=lip_xxxxx')
        return

    seen = set()
    valid = []

    for i in range(NR_REQUESTS):
        print(f'Request {i+1}/{NR_REQUESTS}...')
        try:
            batch = fetch_batch(NB_FETCH)
            for raw in batch:
                pid = raw['puzzle']['id']
                if pid in seen: continue
                seen.add(pid)
                result = verify(raw)
                if result:
                    valid.append(result)
        except Exception as e:
            print(f'  Eroare: {e}')
        if i < NR_REQUESTS - 1:
            time.sleep(2)

    print(f'\nValide: {len(valid)} din {len(seen)} unice')

    # Distribuie uniform dupa rating
    valid.sort(key=lambda x: x['rating'])
    if len(valid) >= TARGET:
        step = len(valid) / TARGET
        selected = [valid[int(i * step)] for i in range(TARGET)]
    else:
        selected = valid
        print(f'ATENTIE: am gasit doar {len(valid)} puzzle-uri (doream {TARGET})')

    os.makedirs('data', exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(selected, f, ensure_ascii=False, indent=1)
    print(f'Salvat: {OUTPUT_FILE} ({len(selected)} puzzle-uri)')
    print('Ratings:', [p['rating'] for p in selected])


if __name__ == '__main__':
    main()
