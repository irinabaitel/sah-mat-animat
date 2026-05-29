"""
Puzzle-uri mat sufocat variate:
- Cel mult 2 per camp de mat (nu repetam acelasi colt)
- Pentru fiecare camp: un puzzle 1-mutare SI unul cu 3+ mutari (daca exista)
- Minim 12 puzzle-uri cu sol_len >= 3 in setul final
"""
import csv, chess, json
from collections import defaultdict

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
        mate_sq = chess.square_name(last_move.to_square)
        turn = 'w' if board.turn == chess.WHITE else 'b'
        return {
            'fen': board.fen(), 'sol': sol, 'turn': turn,
            'mate_sq': mate_sq, 'sol_len': len(sol)
        }
    except Exception:
        return None

# Per camp de mat: pastram cel mai bun 1-mutare si cel mai bun multi-mutare
by_square = defaultdict(lambda: {'single': None, 'multi': None})

print("Scanam CSV (mat sufocat variat)...")
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i % 300_000 == 0:
            total = sum(
                (1 if v['single'] else 0) + (1 if v['multi'] else 0)
                for v in by_square.values()
            )
            print(f"  {i:,} randuri... {total} puzzle-uri in {len(by_square)} campuri")

        themes = row.get('Themes', '').lower()
        if 'smotheredmate' not in themes:
            continue
        try:
            rating = int(row['Rating'])
        except Exception:
            continue
        if rating > 2400:
            continue

        result = validate_puzzle(row['FEN'], row['Moves'])
        if not result:
            continue

        sq = result['mate_sq']
        sl = result['sol_len']
        entry = {
            'id': row['PuzzleId'],
            'fen': result['fen'],
            'sol': result['sol'],
            'turn': result['turn'],
            'rating': rating,
            'sol_len': sl,
            'mate_sq': sq
        }

        bucket = by_square[sq]
        if sl == 1:
            if bucket['single'] is None:
                bucket['single'] = entry
            # pastram cel cu rating mai mic (mai accesibil)
            elif rating < bucket['single']['rating']:
                bucket['single'] = entry
        else:  # 3, 5, 7...
            if bucket['multi'] is None:
                bucket['multi'] = entry
            elif rating < bucket['multi']['rating']:
                bucket['multi'] = entry

print(f"\nCampuri de mat gasite: {len(by_square)}")
for sq, bk in sorted(by_square.items()):
    s = bk['single']
    m = bk['multi']
    print(f"  {sq}: single={'rating='+str(s['rating'])+' sol='+str(s['sol_len']) if s else 'N/A'}"
          f"  multi={'rating='+str(m['rating'])+' sol='+str(m['sol_len']) if m else 'N/A'}")

# Construim lista finala
all_puzzles = []
for sq, bk in by_square.items():
    if bk['single']:
        all_puzzles.append(bk['single'])
    if bk['multi']:
        all_puzzles.append(bk['multi'])

all_puzzles.sort(key=lambda x: x['rating'])
print(f"\nTotal disponibil: {len(all_puzzles)}")
print(f"  1-mutare: {sum(1 for p in all_puzzles if p['sol_len']==1)}")
print(f"  3+ mutari: {sum(1 for p in all_puzzles if p['sol_len']>=3)}")

# Selectie 35: toate multi-mutare + completam cu single-mutare distribuite uniform
def pick(lst, n):
    if len(lst) <= n:
        return lst
    step = len(lst) / n
    return [lst[int(i * step)] for i in range(n)]

TARGET = 35
multi  = [p for p in all_puzzles if p['sol_len'] >= 3]
single = [p for p in all_puzzles if p['sol_len'] == 1]

need_single = max(0, TARGET - len(multi))
selected = multi + pick(single, need_single)
selected.sort(key=lambda x: x['rating'])
print(f"\nSelectate: {len(selected)}")
for p in selected:
    print(f"  {p['id']} rating={p['rating']} turn={p['turn']} sol_len={p['sol_len']} mate_sq={p['mate_sq']}")

print(f"\n  1-mutare: {sum(1 for p in selected if p['sol_len']==1)}")
print(f"  3+ mutari: {sum(1 for p in selected if p['sol_len']>=3)}")

for p in selected:
    p.pop('sol_len', None)
    p.pop('mate_sq', None)

with open('smothered_puzzles2.json', 'w') as f:
    json.dump(selected, f, indent=2)
print("\nSalvat in smothered_puzzles2.json")
