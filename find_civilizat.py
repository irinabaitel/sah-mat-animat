"""
Cauta puzzle-uri "mat civilizat":
- Ambele TURNURI atacante pe linia 7 (alb) sau linia 2 (negru)
- Regele adversarului pe ultima linie (8 sau 1)
- Solutia: TURNURILE (nu regina!) captureaza piese de pe linia 7/2 -> mat
- Minim 2 capturi cu TURNURI pe linia de atac
- Matul final livrat de un turn
"""
import csv, chess, json

def check_civilizat(fen, moves_str):
    try:
        board = chess.Board(fen)
        moves = moves_str.strip().split()
        if len(moves) < 3:
            return None

        # Moves[0] = ultima mutare din partida (setup)
        try:
            board.push(chess.Move.from_uci(moves[0]))
        except Exception:
            return None

        player = board.turn
        attack_rank = 6 if player == chess.WHITE else 1  # linia 7 sau 2 (0-indexed)
        king_rank   = 7 if player == chess.WHITE else 0  # ultima linie adversar

        # Exact 2 turnuri ale atacantului pe linia de atac
        rooks = [sq for sq in chess.SQUARES
                 if board.piece_at(sq)
                 and board.piece_at(sq).piece_type == chess.ROOK
                 and board.piece_at(sq).color == player
                 and chess.square_rank(sq) == attack_rank]
        if len(rooks) < 2:
            return None

        # Regele adversarului pe ultima linie
        king_sq = board.king(not player)
        if king_sq is None or chess.square_rank(king_sq) != king_rank:
            return None

        sol = moves[1:]
        # Numarul impar de mutari = atacantul da ultima mutare (mat)
        if len(sol) < 3 or len(sol) % 2 == 0:
            return None

        # Joaca solutia — numaram DOAR capturile facute cu TURNURI pe linia de atac
        rook_captures = 0
        tmp = board.copy()
        last_player_piece = None
        for idx, uci in enumerate(sol):
            try:
                mv = chess.Move.from_uci(uci)
            except Exception:
                return None
            if not tmp.is_legal(mv):
                return None

            if tmp.turn == player:
                piece = tmp.piece_at(mv.from_square)
                to_rank = chess.square_rank(mv.to_square)
                is_rook = piece and piece.piece_type == chess.ROOK
                if is_rook and tmp.is_capture(mv) and to_rank == attack_rank:
                    rook_captures += 1
                last_player_piece = piece

            tmp.push(mv)

        if not tmp.is_checkmate():
            return None

        # Matul final trebuie dat de un turn
        if not (last_player_piece and last_player_piece.piece_type == chess.ROOK):
            return None

        # Cel putin 2 capturi cu turnuri pe linia de atac
        if rook_captures < 2:
            return None

        turn = 'w' if player == chess.WHITE else 'b'
        return {
            'fen':            board.fen(),
            'sol':            sol,
            'turn':           turn,
            'rook_captures':  rook_captures
        }
    except Exception:
        return None


easy, medium, hard = [], [], []
MAX_EACH = 25

print("Scanam CSV (filtrare stricta — doar capturi cu TURNURI)...")
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i % 500_000 == 0:
            print(f"  {i:,} randuri... easy={len(easy)} med={len(medium)} hard={len(hard)}")
        if i >= 6_000_000:
            break

        try:
            rating = int(row['Rating'])
        except Exception:
            continue

        if 'mate' not in row.get('Themes', '').lower():
            continue

        result = check_civilizat(row['FEN'], row['Moves'])
        if not result:
            continue

        entry = {
            'id':            row['PuzzleId'],
            'fen':           result['fen'],
            'sol':           result['sol'],
            'turn':          result['turn'],
            'rating':        rating,
            'rook_captures': result['rook_captures']
        }

        if rating <= 1300 and len(easy)   < MAX_EACH: easy.append(entry)
        elif rating <= 1800 and len(medium) < MAX_EACH: medium.append(entry)
        elif rating <= 2300 and len(hard)   < MAX_EACH: hard.append(entry)

        if len(easy) >= MAX_EACH and len(medium) >= MAX_EACH and len(hard) >= MAX_EACH:
            print("Suficiente puzzle-uri gasite!")
            break

print(f"\nRezultat brut: easy={len(easy)}, medium={len(medium)}, hard={len(hard)}")

# Selectam 5 din fiecare nivel
def pick(lst, n):
    lst.sort(key=lambda x: x['rating'])
    if len(lst) <= n:
        return lst
    step = len(lst) / n
    return [lst[int(i * step)] for i in range(n)]

n_each = 5
selected = pick(easy, n_each) + pick(medium, n_each) + pick(hard, n_each)

print(f"Selectate: {len(selected)} puzzle-uri")
for p in selected:
    print(f"  {p['id']} rating={p['rating']} turn={p['turn']} rook_capt={p['rook_captures']} sol={p['sol']}")

with open('civilizat_puzzles.json', 'w') as f:
    json.dump(selected, f, indent=2)
print("\nSalvat in civilizat_puzzles.json")
