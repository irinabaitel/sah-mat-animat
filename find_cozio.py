"""
Filtru Matul lui Cozio din baza Lichess.

Tiparul:
- Regina da mat diagonal adiacent regelui (|df|=1, |dr|=1)
- Cele doua campuri "aripi" ale tiparului sunt ocupate de piese proprii ale regelui matat
  arm1 = king + (-df, 0), arm2 = king + (0, -dr)  [filtru geometric strict, ca la Dovetail]
- PLUS: regele atacant este adiacent reginei (o apara)
  => asta distinge Cozio de Dovetail
"""

import chess, csv, json

def is_cozio_mate(board):
    if not board.is_checkmate():
        return False

    mated_color  = board.turn
    mating_color = not mated_color

    checkers = list(board.checkers())
    if len(checkers) != 1:
        return False

    checker_sq    = checkers[0]
    checker_piece = board.piece_at(checker_sq)
    if checker_piece is None or checker_piece.piece_type != chess.QUEEN:
        return False

    king_sq = board.king(mated_color)
    kf = chess.square_file(king_sq)
    kr = chess.square_rank(king_sq)
    qf = chess.square_file(checker_sq)
    qr = chess.square_rank(checker_sq)

    df = qf - kf
    dr = qr - kr
    if abs(df) != 1 or abs(dr) != 1:
        return False

    # Cele doua campuri "aripi"
    arm1_f, arm1_r = kf - df, kr
    arm2_f, arm2_r = kf,      kr - dr

    if not (0 <= arm1_f <= 7 and 0 <= arm1_r <= 7):
        return False
    if not (0 <= arm2_f <= 7 and 0 <= arm2_r <= 7):
        return False

    arm1 = chess.square(arm1_f, arm1_r)
    arm2 = chess.square(arm2_f, arm2_r)

    def own_non_knight(sq):
        p = board.piece_at(sq)
        return p is not None and p.color == mated_color and p.piece_type != chess.KNIGHT

    if not (own_non_knight(arm1) and own_non_knight(arm2)):
        return False

    # Regele atacant trebuie sa fie adiacent reginei (o apara)
    mating_king_sq = board.king(mating_color)
    if mating_king_sq is None:
        return False

    king_adj = chess.SquareSet(chess.BB_KING_ATTACKS[mating_king_sq])
    return checker_sq in king_adj


def rating_to_level(r):
    if r < 1500: return 1
    if r < 1900: return 2
    return 3


results = []
checked = 0
found   = 0

print("Scanez puzzle-urile Lichess pentru Matul lui Cozio...")

with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'mate' not in row['Themes'].lower():
            continue

        checked += 1
        if checked % 50000 == 0:
            print(f"  Verificat {checked:,} cu mat | Gasite: {found}")

        try:
            moves = row['Moves'].split()
            board = chess.Board(row['FEN'])
            for mv in moves:
                board.push_uci(mv)

            if is_cozio_mate(board):
                found += 1
                results.append({
                    "id":      f"li-{row['PuzzleId']}",
                    "fen":     row['FEN'],
                    "moves":   moves,
                    "level":   rating_to_level(int(row['Rating'])),
                    "gameUrl": f"https://lichess.org/training/{row['PuzzleId']}"
                })
        except Exception:
            continue

print(f"\nTotal gasite: {found}")

levels = {1:0, 2:0, 3:0}
for p in results:
    levels[p['level']] += 1
print(f"  Nivel 1 (<1500): {levels[1]}")
print(f"  Nivel 2 (1500-1900): {levels[2]}")
print(f"  Nivel 3 (>1900): {levels[3]}")

with open('data/cozio_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Salvat in data/cozio_candidates.json")
