"""
Filtreaza puzzle-urile Lichess pentru Matul Coada de Randunica (Dovetail Mate).

Tiparul corect:
- Regina da mat
- Regina se afla la o singura patrata pe diagonala fata de regele advers
- Cel putin 2 piese proprii ale regelui atacat (care nu sunt cai) blocheaza fuga
"""

import chess, csv, json

def is_dovetail_mate(board):
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
    dr = abs(chess.square_rank(checker_sq) - chess.square_rank(king_sq))
    df = abs(chess.square_file(checker_sq) - chess.square_file(king_sq))
    if dr != 1 or df != 1:
        return False

    # Cel putin 2 piese proprii (non-cal) adiacente regelui
    king_adj = chess.SquareSet(chess.BB_KING_ATTACKS[king_sq])
    own_blockers = sum(
        1 for sq in king_adj
        if (p := board.piece_at(sq)) and p.color == mated_color and p.piece_type != chess.KNIGHT
    )
    return own_blockers >= 2


def rating_to_level(r):
    if r < 1500: return 1
    if r < 1900: return 2
    return 3


results = []
checked = 0
found   = 0

print("Scanez puzzle-urile Lichess pentru Matul Coada de Randunica...")

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

            if is_dovetail_mate(board):
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

with open('data/dovetail_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Salvat in data/dovetail_candidates.json")
