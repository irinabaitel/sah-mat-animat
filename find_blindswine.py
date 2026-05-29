"""
Puzzle-uri mat porcul orb (blindSwineMate) - selectie dupa popularitate Lichess.
- Rating 600-2000, minim 100 runde jucate
- Per camp de mat: cel mai jucat puzzle (orice lungime) + cel mai jucat cu 3+ mutari
- 50 puzzle-uri totale, sortate dupa rating
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
        generated_fen = board.fen()
        chess.Board(generated_fen)
        mate_sq = chess.square_name(tmp.peek().to_square)
        turn = 'w' if board.turn == chess.WHITE else 'b'
        return {
            'fen': generated_fen, 'sol': sol, 'turn': turn,
            'mate_sq': mate_sq, 'sol_len': len(sol)
        }
    except Exception:
        return None

MIN_RATING, MAX_RATING = 600, 2000
MIN_PLAYS = 100

# Per camp de mat: cel mai jucat (orice lungime) + cel mai jucat cu sol>=3
by_square = defaultdict(lambda: {'best': None, 'multi': None})

print("Scanam CSV (blindSwineMate - selectie dupa popularitate)...")
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i % 300_000 == 0:
            total = sum(
                (1 if v['best'] else 0) + (1 if v['multi'] else 0)
                for v in by_square.values()
            )
            print(f"  {i:,} randuri... {total} candidati in {len(by_square)} campuri")

        themes = row.get('Themes', '').lower()
        if 'blindswinemate' not in themes:
            continue
        try:
            rating = int(row['Rating'])
            nb_plays = int(row['NbPlays'])
        except Exception:
            continue
        if rating < MIN_RATING or rating > MAX_RATING:
            continue
        if nb_plays < MIN_PLAYS:
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
            'nb_plays': nb_plays,
            'sol_len': sl,
            'mate_sq': sq
        }

        bucket = by_square[sq]
        if bucket['best'] is None or nb_plays > bucket['best']['nb_plays']:
            bucket['best'] = entry
        if sl >= 3:
            if bucket['multi'] is None or nb_plays > bucket['multi']['nb_plays']:
                bucket['multi'] = entry

print(f"\nCampuri de mat gasite: {len(by_square)}")
for sq, bk in sorted(by_square.items()):
    b = bk['best']
    m = bk['multi']
    print(f"  {sq}: best={'r='+str(b['rating'])+' n='+str(b['nb_plays'])+' len='+str(b['sol_len']) if b else 'N/A'}"
          f"  multi={'r='+str(m['rating'])+' n='+str(m['nb_plays'])+' len='+str(m['sol_len']) if m else 'N/A'}")

# Candidati unici
all_puzzles = []
seen_ids = set()
for sq, bk in by_square.items():
    for key in ('best', 'multi'):
        p = bk[key]
        if p and p['id'] not in seen_ids:
            all_puzzles.append(p)
            seen_ids.add(p['id'])

all_puzzles.sort(key=lambda x: x['rating'])
print(f"\nTotal disponibil (unic): {len(all_puzzles)}")
print(f"  1-mutare: {sum(1 for p in all_puzzles if p['sol_len']==1)}")
print(f"  3+ mutari: {sum(1 for p in all_puzzles if p['sol_len']>=3)}")

TARGET = 50
# Sortam dupa popularitate si luam top TARGET
top_by_plays = sorted(all_puzzles, key=lambda x: x['nb_plays'], reverse=True)[:TARGET]
selected = sorted(top_by_plays, key=lambda x: x['rating'])

if len(selected) < TARGET:
    print(f"\nATENTIE: doar {len(selected)} puzzle-uri disponibile (sub target {TARGET})")

print(f"\nSelectate: {len(selected)}")
for p in selected:
    print(f"  {p['id']} r={p['rating']} plays={p['nb_plays']} turn={p['turn']} len={p['sol_len']} sq={p['mate_sq']}")

print(f"\n  1-mutare: {sum(1 for p in selected if p['sol_len']==1)}")
print(f"  3+ mutari: {sum(1 for p in selected if p['sol_len']>=3)}")

for p in selected:
    p.pop('sol_len', None)
    p.pop('mate_sq', None)
    p.pop('nb_plays', None)

with open('blindswine_puzzles.json', 'w') as f:
    json.dump(selected, f, indent=2)
print("\nSalvat in blindswine_puzzles.json")
