"""
Filtrează puzzle-urile Lichess pentru Matul lui Anderssen.

Tiparul corect:
- Turnul dă mat pe ultima linie (rând 8 sau 1)
- Un pion al aceluiași jucător stă pe rândul 7 (sau 2), coloană adiacentă (±1)
- Pionul participă activ: ocupă o diagonală de scăpare a regelui SAU atacă
  un câmp adiacent regelui
"""

import chess
import csv
import json

def is_anderssen_mate(board):
    if not board.is_checkmate():
        return False

    mated_color  = board.turn       # cel în mat
    mating_color = not mated_color

    checkers = list(board.checkers())
    if len(checkers) != 1:
        return False

    checker_sq    = checkers[0]
    checker_piece = board.piece_at(checker_sq)
    if checker_piece is None or checker_piece.piece_type != chess.ROOK:
        return False

    rook_rank = chess.square_rank(checker_sq)
    rook_file = chess.square_file(checker_sq)

    # Turnul trebuie să fie pe ultima linie
    last_rank  = 7 if mating_color == chess.WHITE else 0
    pawn_rank  = 6 if mating_color == chess.WHITE else 1
    if rook_rank != last_rank:
        return False

    king_sq  = board.king(mated_color)
    king_adj = chess.SquareSet(chess.BB_KING_ATTACKS[king_sq])

    for delta in (-1, 1):
        pf = rook_file + delta
        if not (0 <= pf <= 7):
            continue
        pawn_sq = chess.square(pf, pawn_rank)
        piece = board.piece_at(pawn_sq)
        if piece and piece.piece_type == chess.PAWN and piece.color == mating_color:
            # Pionul trebuie să fie adiacent regelui SAU să atace un câmp adiacent regelui
            pawn_adj_to_king    = pawn_sq in king_adj
            pawn_attacks_nearby = bool(board.attacks(pawn_sq) & king_adj)
            if pawn_adj_to_king or pawn_attacks_nearby:
                return True

    return False


def rating_to_level(r):
    if r < 1500: return 1
    if r < 1900: return 2
    return 3


results = []
checked = 0
found   = 0

print("Scanez puzzle-urile Lichess pentru Matul lui Anderssen...")
import sys; sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

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

            if is_anderssen_mate(board):
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

print(f"\nTotal găsite: {found}")

with open('data/anderssen_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Salvat în data/anderssen_candidates.json")
