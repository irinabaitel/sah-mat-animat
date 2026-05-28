"""
Rafinare Dovetail cu criteriu geometric strict:

Daca regina e la (kf+df, kr+dr) fata de rege (|df|=|dr|=1),
cele doua piese proprii TREBUIE sa fie exact pe:
  - (kf-df, kr)  — aripа perpendiculara pe coloana
  - (kf, kr-dr)  — aripa perpendiculara pe rand

Acesta e tiparul clasic "coada de randunica".
"""

import chess, json

def is_strict_dovetail(board):
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

    # Cele doua campuri "aripi" ale tiparului Dovetail
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

    return own_non_knight(arm1) and own_non_knight(arm2)


candidates = json.load(open('data/dovetail_candidates.json', encoding='utf-8'))
print(f"Candidati intrare: {len(candidates)}")

refined = []
for p in candidates:
    try:
        board = chess.Board(p['fen'])
        for mv in p['moves']:
            board.push_uci(mv)
        if is_strict_dovetail(board):
            refined.append(p)
    except Exception:
        continue

print(f"Dupa rafinare geometrica: {len(refined)}")
levels = {1:0, 2:0, 3:0}
for p in refined:
    levels[p['level']] += 1
print(f"  Nivel 1: {levels[1]}  Nivel 2: {levels[2]}  Nivel 3: {levels[3]}")

with open('data/dovetail_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(refined, f, ensure_ascii=False, indent=2)
print("Salvat in data/dovetail_candidates.json")
