"""fetch_hanging.py — puzzle-uri „piesă atârnată” de pe Lichess (tema hangingPiece) pentru arena lecției Piese atârnate.
Rulare: LICHESS_TOKEN=lip_... python tools/fetch_hanging.py [runde]  -> tools/hanging_raw.json + data/hanging_top40.json
Filtru: prima mutare a elevului capturează o piesă (nu pion) pe care adversarul nu o poate recaptura."""
import os, json, io, sys, time, urllib.request, chess, chess.pgn
sys.stdout.reconfigure(encoding='utf-8')
TOKEN = os.environ.get('LICHESS_TOKEN', '')
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'hanging_raw.json'); OUT = os.path.join(HERE, '..', 'data', 'hanging_top40.json')
raw = json.load(open(RAW, encoding='utf-8')) if os.path.exists(RAW) else {}

def fetch(diff, nb=50):
    url = f'https://lichess.org/api/puzzle/batch/hangingPiece?nb={nb}&difficulty={diff}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json', 'Authorization': f'Bearer {TOKEN}'})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())['puzzles']

def analyse(p):
    game = chess.pgn.read_game(io.StringIO(p['game']['pgn'])); b = game.board()
    mv = list(game.mainline_moves()); ip = p['puzzle']['initialPly']
    for m in mv[:ip]: b.push(m)
    fen = b.fen(); setup = mv[ip].uci(); b.push(mv[ip])
    sol = p['puzzle']['solution']; t = b.copy()
    first = chess.Move.from_uci(sol[0])
    if first not in t.legal_moves or not t.is_capture(first): return None
    cap = t.piece_at(first.to_square)
    if not cap or cap.piece_type == chess.PAWN: return None
    t.push(first)
    if t.is_attacked_by(t.turn, first.to_square) and not t.is_checkmate(): return None   # se poate recaptura
    t = b.copy()
    for u in sol:
        m = chess.Move.from_uci(u)
        if m not in t.legal_moves: return None
        t.push(m)
    pz = p['puzzle']
    return dict(id=pz['id'], fen=fen, moves=[setup] + sol, rating=pz['rating'], plays=pz['plays'], themes=pz['themes'])

if __name__ == '__main__':
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for rnd in range(rounds):
        for diff in ('easier', 'normal', 'harder'):
            try:
                ps = fetch(diff); new = 0
                for p in ps:
                    if p['puzzle']['id'] not in raw: raw[p['puzzle']['id']] = p; new += 1
                print(rnd, diff, len(ps), 'noi', new, 'total', len(raw), flush=True)
            except Exception as e: print('err', diff, e, flush=True); time.sleep(30)
            json.dump(raw, open(RAW, 'w', encoding='utf-8'))
            time.sleep(10)
    found = [x for x in (analyse(p) for p in raw.values()) if x]
    print('trec filtrul', len(found))
