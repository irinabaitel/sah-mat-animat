"""
Cauta puzzle-uri "porci curati" cu rege central:
- Exact 2 turnuri ale atacantului pe ACEEASI linie (7 sau 2)
- Toate mutarile atacantului sunt cu turnuri, toate raman pe linia de atac
- Ambele turnuri SUPRAVIETUIESC pana la mat
- Regele adversarului pe ultima linie, NU in colt (nu pe coloana a sau h)
- Miscarea regelui impiedicata din STANGA si din DREAPTA
- Cel putin un camp lateral blocat de un NEBUN sau CAL
"""
import csv, chess, json

MINOR = {chess.BISHOP, chess.KNIGHT}

def has_minor_blocker(board, player, king_sq, king_rank):
    """Regele nu in colt, cel putin un camp lateral controlat de nebun/cal."""
    king_file = chess.square_file(king_sq)
    if king_file < 1 or king_file > 6:
        return False
    for df in [-1, 1]:
        adj_file = king_file + df
        if not (0 <= adj_file <= 7):
            continue
        adj_sq = chess.square(adj_file, king_rank)
        for atk_sq in board.attackers(player, adj_sq):
            p = board.piece_at(atk_sq)
            if p and p.piece_type in MINOR:
                return True
    return False

def check_clean_rooks(fen, moves_str):
    try:
        board = chess.Board(fen)
        moves = moves_str.strip().split()
        if len(moves) < 2:
            return None

        try:
            board.push(chess.Move.from_uci(moves[0]))
        except Exception:
            return None

        player = board.turn
        attack_rank = 6 if player == chess.WHITE else 1
        king_rank   = 7 if player == chess.WHITE else 0

        # Exact 2 turnuri pe aceeasi linie de atac
        rooks = [sq for sq in chess.SQUARES
                 if board.piece_at(sq)
                 and board.piece_at(sq).piece_type == chess.ROOK
                 and board.piece_at(sq).color == player
                 and chess.square_rank(sq) == attack_rank]
        if len(rooks) != 2:
            return None

        # Regele adversarului pe ultima linie, nu in colt
        king_sq = board.king(not player)
        if king_sq is None or chess.square_rank(king_sq) != king_rank:
            return None

        sol = moves[1:]
        # Minim 3 mutari, numar impar (atacantul da ultima mutare)
        if len(sol) < 3 or len(sol) % 2 == 0:
            return None

        # Joaca solutia
        tmp = board.copy()
        last_player_piece = None
        for uci in sol:
            try:
                mv = chess.Move.from_uci(uci)
            except Exception:
                return None
            if not tmp.is_legal(mv):
                return None
            if tmp.turn == player:
                piece = tmp.piece_at(mv.from_square)
                # Toate mutarile atacantului trebuie sa fie cu turnuri
                if not piece or piece.piece_type != chess.ROOK:
                    return None
                # Turnurile raman pe linia de atac
                if chess.square_rank(mv.to_square) != attack_rank:
                    return None
                last_player_piece = piece
            tmp.push(mv)

        if not tmp.is_checkmate():
            return None

        # Ambele turnuri supravietuiesc
        surviving = sum(
            1 for sq in chess.SQUARES
            if tmp.piece_at(sq)
            and tmp.piece_at(sq).piece_type == chess.ROOK
            and tmp.piece_at(sq).color == player
        )
        if surviving < 2:
            return None

        # Matul dat de un turn
        if not (last_player_piece and last_player_piece.piece_type == chess.ROOK):
            return None

        # Pozitia de mat: regele nu in colt (file 1-6) si cel putin un camp
        # lateral acoperit de nebun/cal SAU regele pe file 1-5 (nu pe g/h)
        final_king_sq = tmp.king(not player)
        final_king_file = chess.square_file(final_king_sq)
        if final_king_file in [0, 7]:
            return None  # mat in colt a sau h — excludem
        has_minor = has_minor_blocker(tmp, player, final_king_sq, king_rank)
        # Acceptam: (a) minor piece blocker indiferent de coloana, sau
        #           (b) rege pe coloana b-f (file 1-5) chiar fara minor piece
        if not has_minor and final_king_file == 6:
            return None  # pe g-file fara minor e tot un mat de colt "mascat"

        turn = 'w' if player == chess.WHITE else 'b'
        return {'fen': board.fen(), 'sol': sol, 'turn': turn}
    except Exception:
        return None


easy, medium, hard = [], [], []
MAX_EACH = 25

print("Scanam CSV (rege central, blocat de nebun/cal)...")
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i % 500_000 == 0:
            print(f"  {i:,} randuri... easy={len(easy)} med={len(medium)} hard={len(hard)}")
        if i >= 10_000_000:
            break

        try:
            rating = int(row['Rating'])
        except Exception:
            continue

        if 'mate' not in row.get('Themes', '').lower():
            continue

        result = check_clean_rooks(row['FEN'], row['Moves'])
        if not result:
            continue

        entry = {
            'id':     row['PuzzleId'],
            'fen':    result['fen'],
            'sol':    result['sol'],
            'turn':   result['turn'],
            'rating': rating,
        }

        if rating <= 1300 and len(easy)   < MAX_EACH: easy.append(entry)
        elif rating <= 1800 and len(medium) < MAX_EACH: medium.append(entry)
        elif rating <= 2300 and len(hard)   < MAX_EACH: hard.append(entry)

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

# 4 easy + 3 medium + 3 hard = 10 total
selected = pick(easy, 4) + pick(medium, 3) + pick(hard, 3)

print(f"Selectate: {len(selected)} puzzle-uri")
for p in selected:
    print(f"  {p['id']} rating={p['rating']} turn={p['turn']} sol={p['sol']}")

with open('clean_rooks_puzzles.json', 'w') as f:
    json.dump(selected, f, indent=2)
print("\nSalvat in clean_rooks_puzzles.json")
