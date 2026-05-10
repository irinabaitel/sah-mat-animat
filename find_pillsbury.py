"""
Cauta puzzle-uri Pillsbury's Mate din baza de date Lichess.
Valideaza: ultima mutare e de turn, pozitia e mat, minim 3 mutari in solutie.
"""
import csv, chess, json, sys

MIN_SOL_LEN = 3
MAX_SOL_LEN = 11

def validate_puzzle(fen, moves_str):
    try:
        board = chess.Board(fen)
        moves = moves_str.strip().split()
        if not moves:
            return None
        board.push(chess.Move.from_uci(moves[0]))
        sol = moves[1:]
        if len(sol) < MIN_SOL_LEN or len(sol) > MAX_SOL_LEN:
            return None
        tmp = board.copy()
        for uci in sol:
            mv = chess.Move.from_uci(uci)
            if not tmp.is_legal(mv):
                return None
            tmp.push(mv)
        if not tmp.is_checkmate():
            return None
        # Ultima mutare trebuie sa fie de turn
        last_move = tmp.peek()
        piece = tmp.piece_at(last_move.to_square)
        if not piece or piece.piece_type != chess.ROOK:
            return None
        turn = 'w' if board.turn == chess.WHITE else 'b'
        return {'fen': board.fen(), 'sol': sol, 'turn': turn}
    except Exception:
        return None

easy, medium, hard = [], [], []
MAX_EASY   = 30
MAX_MEDIUM = 60
MAX_HARD   = 30

sys.stdout.reconfigure(encoding='utf-8')
print("Scanam CSV pentru pillsburysMate (minim 3 mutari)...")
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i % 200_000 == 0:
            print(f"  {i:,} randuri... easy={len(easy)} med={len(medium)} hard={len(hard)}")
        themes = row.get('Themes', '').lower()
        if 'pillsburysmate' not in themes:
            continue
        try:
            rating = int(row['Rating'])
        except Exception:
            continue
        result = validate_puzzle(row['FEN'], row['Moves'])
        if not result:
            continue
        entry = {
            'id':     row['PuzzleId'],
            'fen':    result['fen'],
            'sol':    result['sol'],
            'turn':   result['turn'],
            'rating': rating,
        }
        if rating <= 1300 and len(easy) < MAX_EASY:
            easy.append(entry)
        elif rating <= 1800 and len(medium) < MAX_MEDIUM:
            medium.append(entry)
        elif rating <= 2400 and len(hard) < MAX_HARD:
            hard.append(entry)
        if len(easy) >= MAX_EASY and len(medium) >= MAX_MEDIUM and len(hard) >= MAX_HARD:
            print("Suficiente gasite!")
            break

print(f"\nRezultat brut: easy={len(easy)}, medium={len(medium)}, hard={len(hard)}")

def pick(lst, n):
    lst.sort(key=lambda x: x['rating'])
    if len(lst) <= n:
        return lst
    step = len(lst) / n
    return [lst[int(i * step)] for i in range(n)]

selected = pick(easy, 10) + pick(medium, 20) + pick(hard, 10)
print(f"Selectate: {len(selected)} puzzle-uri")
for p in selected:
    print(f"  {p['id']} r={p['rating']} mutari={len(p['sol'])} turn={p['turn']} sol={p['sol']}")

with open('pillsbury_puzzles.json', 'w', encoding='utf-8') as f:
    json.dump(selected, f, indent=2, ensure_ascii=False)
print("\nSalvat in pillsbury_puzzles.json")
