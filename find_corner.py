"""Fetch cornerMate puzzles from Lichess API and save to corner_puzzles.json."""
import os, json, io, sys, time
import urllib.request
import chess, chess.pgn

LICHESS_TOKEN = os.environ.get('LICHESS_TOKEN', '')
THEME = 'cornerMate'
FETCH_NB = 50
NR_REQUESTS = 8
MIN_PLAYS = 200
MIN_RATING = 700
MAX_RATING = 1900
MAX_SOL_LEN = 7

def fetch(nb):
    url = f'https://lichess.org/api/puzzle/batch/{THEME}?nb={nb}'
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {LICHESS_TOKEN}',
        'Accept': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())['puzzles']

def validate(raw):
    try:
        p = raw['puzzle']
        sol = p['solution']
        game = chess.pgn.read_game(io.StringIO(f'[Event "?"]\n1. {raw["game"]["pgn"]}'))
        board = game.board()
        for i, mv in enumerate(game.mainline_moves()):
            if i >= p['initialPly'] + 1: break
            board.push(mv)
        test = board.copy()
        for uci in sol:
            mv = chess.Move.from_uci(uci)
            if mv not in test.legal_moves: return None
            test.push(mv)
        if not test.is_checkmate(): return None
        return board.fen(), 'w' if board.turn == chess.WHITE else 'b'
    except: return None

sys.stdout.reconfigure(encoding='utf-8')
seen, valid = set(), []
for i in range(NR_REQUESTS):
    print(f'Request {i+1}/{NR_REQUESTS}...')
    try:
        batch = fetch(FETCH_NB)
    except Exception as e:
        print(f'  EROARE: {e}')
        time.sleep(12)
        continue
    time.sleep(4)
    for raw in batch:
        p = raw['puzzle']
        pid = p['id']
        if pid in seen: continue
        seen.add(pid)
        if p['plays'] < MIN_PLAYS: continue
        if not (MIN_RATING <= p['rating'] <= MAX_RATING): continue
        if len(p['solution']) > MAX_SOL_LEN: continue
        r = validate(raw)
        if not r: continue
        fen, turn = r
        valid.append({'id': pid, 'fen': fen, 'sol': p['solution'],
                      'turn': turn, 'rating': p['rating'], 'plays': p['plays']})

valid.sort(key=lambda x: x['rating'])
seen2, dedup = set(), []
for v in valid:
    if v['id'] not in seen2:
        seen2.add(v['id']); dedup.append(v)

print(f'\nTotal valide: {len(dedup)}')
print('Ratings:', [p['rating'] for p in dedup])
with open('corner_puzzles.json', 'w', encoding='utf-8') as f:
    json.dump(dedup, f, indent=2, ensure_ascii=False)
print('Salvat corner_puzzles.json')
