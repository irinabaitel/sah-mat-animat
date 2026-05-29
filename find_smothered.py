"""
Cauta puzzle-uri de mat sufocat (smotheredMate) din baza de date Lichess.
Valideaza: ultima mutare e de cal, pozitia e mat.
"""
import csv, chess, json

def validate_puzzle(fen, moves_str):
    try:
        board = chess.Board(fen)
        moves = moves_str.strip().split()
        if not moves:
            return None
        try:
            board.push(chess.Move.from_uci(moves[0]))
        except Exception:
            return None
        sol = moves[1:]
        if not sol:
            return None
        tmp = board.copy()
        for uci in sol:
            try:
                mv = chess.Move.from_uci(uci)
            except Exception:
                return None
            if not tmp.is_legal(mv):
                return None
            tmp.push(mv)
        if not tmp.is_checkmate():
            return None
        last_move = tmp.peek()
        piece = tmp.piece_at(last_move.to_square)
        if not piece or piece.piece_type != chess.KNIGHT:
            return None
        turn = 'w' if board.turn == chess.WHITE else 'b'
        return {'fen': board.fen(), 'sol': sol, 'turn': turn}
    except Exception:
        return None

easy, medium, hard = [], [], []
MAX_EACH = 20

print("Scanam CSV pentru smotheredMate...")
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i % 200_000 == 0:
            print(f"  {i:,} randuri... easy={len(easy)} med={len(medium)} hard={len(hard)}")
        themes = row.get('Themes', '').lower()
        if 'smotheredmate' not in themes:
            continue
        try:
            rating = int(row['Rating'])
        except Exception:
            continue
        result = validate_puzzle(row['FEN'], row['Moves'])
        if not result:
            continue
        entry = {
            'id': row['PuzzleId'],
            'fen': result['fen'],
            'sol': result['sol'],
            'turn': result['turn'],
            'rating': rating,
        }
        if rating <= 1400 and len(easy) < MAX_EACH:
            easy.append(entry)
        elif rating <= 1800 and len(medium) < MAX_EACH:
            medium.append(entry)
        elif rating <= 2400 and len(hard) < MAX_EACH:
            hard.append(entry)
        if len(easy) >= MAX_EACH and len(medium) >= MAX_EACH and len(hard) >= MAX_EACH:
            print("Suficiente gasite!")
            break

print(f"\nRezultat: easy={len(easy)}, medium={len(medium)}, hard={len(hard)}")

def pick(lst, n):
    lst.sort(key=lambda x: x['rating'])
    if len(lst) <= n:
        return lst
    step = len(lst) / n
    return [lst[int(i * step)] for i in range(n)]

selected = pick(easy, 10) + pick(medium, 12) + pick(hard, 13)
print(f"Selectate: {len(selected)} puzzle-uri")
for p in selected:
    print(f"  {p['id']} rating={p['rating']} turn={p['turn']} sol_len={len(p['sol'])}")

with open('smothered_puzzles.json', 'w') as f:
    json.dump(selected, f, indent=2)
print("Salvat in smothered_puzzles.json")
