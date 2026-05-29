#!/usr/bin/env python3
# Computes start FENs for blindSwine arena puzzles
# Each row: id, original_fen, all_moves (space separated)
# Applies moves[0] to get start FEN, sol = moves[1:]

PUZZLES_RAW = [
    ("3FkcZ", "8/6k1/5pp1/5rP1/r4PK1/5RRP/8/8 w - - 0 62", "f3e3 a4f4"),
    ("pm9ev", "8/8/p2k4/Pr1p1p1p/KP1R1P1P/R5P1/8/1r6 w - - 8 47", "d4d3 b1b4"),
    ("XTjUq", "6k1/pp4bp/2p3r1/6P1/5R2/7P/P1Pr4/5R1K b - - 0 35", "g7e5 f4f8 g8g7 f1f7"),
    ("RzxGE", "6k1/pp4p1/4R2p/2pp4/4n3/2P5/PP3rPP/R1B1rNK1 w - - 0 22", "e6e4 e1f1"),
    ("N3CaK", "7r/5R2/R7/1pkp3r/8/3B1pP1/PPP2P2/6K1 w - - 1 41", "f7f3 h5h1 g1g2 h8h2"),
    ("zx2zu", "1r5k/7p/1r6/5pp1/B2PpP2/b1P1P1PP/1P1R3R/2K5 w - - 0 38", "b2a3 b6b1 c1c2 b8b2"),
    ("lJT8o", "k6r/P6r/4p3/R1BpPp2/3P2p1/2P3P1/5P2/6K1 w - - 1 37", "a5b5 h7h1 g1g2 h8h2"),
    ("NZvWG", "r5k1/3Q1pp1/r7/3p4/1p1q1P2/1P4P1/2P4P/1K1R4 w - - 0 37", "d1d4 a6a1 b1b2 a8a2"),
    ("tKI9A", "2r1k3/3R1p2/4p1p1/2N1P2p/7P/1P4r1/8/1K1R4 b - - 2 31", "c8c5 d7d8 e8e7 d1d7"),
    ("NOYzX", "k2r4/2R5/1R5p/1p4p1/p4p2/P1P2P2/1PKr2PP/8 w - - 14 38", "c2c1 d2d1 c1c2 d8d2"),
    ("0zYMN", "2k5/pp1r1pp1/2Q1p2p/4P2P/r7/8/PR3P2/KR6 b - - 0 30", "b7c6 b2b8 c8c7 b1b7"),
    ("NfxlE", "6k1/1ppn2pp/p6r/1P1p3r/3P4/4PPq1/P1Q2R1P/1RB3K1 w - - 0 22", "h2g3 h5h1 g1g2 h6h2"),
    ("woObl", "8/4k3/4r3/pR3R2/P4p1p/5P1P/4r1P1/5K2 w - - 7 46", "f5f4 e2e1 f1f2 e6e2"),
    ("XJ8Ja", "1k5r/2p5/1p1p2pp/1q1Pp3/1P2P2P/RKN3r1/8/R7 b - - 3 34", "h8h7 a3a8 b8b7 a1a7"),
    ("thH1i", "r5k1/5pp1/7p/8/2B2PP1/rPpR4/2P4P/1K6 w - - 4 31", "d3c3 a3a1 b1b2 a8a2"),
    ("KfxEl", "rn4kQ/pp3b1p/4q1pR/6P1/4p3/8/PPP2P2/1K5R b - - 0 29", "g8h8 h6h7 h8g8 h7h8 g8g7 h1h7"),
    ("ZrPA7", "r7/p2R2p1/1pk4p/2p2q2/2P1Q3/8/P5PP/2BR2K1 b - - 0 35", "f5e4 d1d6"),
    ("dDAT9", "6k1/p1p2p2/1p1prPpR/8/7R/3n3P/6P1/7K b - - 0 38", "e6f6 h6h8 g8g7 h4h7"),
    ("k4VKy", "2r1k3/3R1p2/p3p1p1/Pp2P2p/1P3P2/8/r5PP/3R2K1 b - - 0 34", "c8c2 d7d8 e8e7 d1d7"),
    ("U8H7K", "2k5/1p1R1p2/2p5/K7/2P4r/5r2/PP5P/3R4 b - - 0 22", "h4c4 d7d8 c8c7 d1d7"),
    ("8Yall", "6k1/5p2/4p1p1/6P1/1prr4/p2pK2R/7R/8 b - - 1 57", "a3a2 h3h8 g8g7 h2h7"),
    ("CQqMm", "2k5/1p3Kp1/p1p2p2/P6p/6r1/5r2/1P1R4/3R4 b - - 0 34", "h5h4 d2d8 c8c7 d1d7"),
    ("Sqvt9", "7r/2Cb1k1r/p1p2P2/2PpP3/5Rp1/2P3q1/Q4R1P/6K1 w - - 0 38", "h2g3 h7h1 g1g2 h8h2"),
    ("2U3Wn", "5k2/1p2r1pn/p4p1B/2pp1P2/6RP/1P1P2R1/1Pr3P1/6K1 b - - 0 34", "g7h6 g4g8 f8f7 g3g7"),
    ("nEvGa", "8/pp4Rk/7p/1P5q/P4KR1/8/8/8 b - - 1 42", "h7h8 g7g8 h8h7 g4g7"),
    ("iSG0t", "4r1k1/2R3pp/3R4/2p5/8/1P3PP1/4r1P1/5K2 w - - 1 33", "c7c5 e2e1 f1f2 e8e2"),
    ("x19k3", "r5k1/3R1ppp/4p3/7P/rp2P1P1/4BP2/1PP1N3/1K6 w - - 1 26", "b2b3 a4a1 b1b2 a8a2"),
    ("WRybJ", "3r2k1/1p1r2b1/6Q1/4p1RP/p7/2P5/PP4P1/2K5 w - - 0 30", "a2a3 d7d1 c1c2 d8d2"),
    ("KDkUC", "7k/1R6/5P2/pPpP3p/6r1/7R/6rK/8 w - - 11 61", "h2h1 g2g1 h1h2 g4g2"),
    ("XJ1Sr", "6k1/5p2/4pPp1/pp6/5rr1/8/PP2K2R/1B5R b - - 0 38", "f4f6 h2h8 g8g7 h1h7"),
    ("Fm9JP", "6kQ/1pq2pb1/4p1p1/1p1pP3/5P2/7R/PPr3P1/1K5R b - - 3 27", "g7h8 h3h8 g8g7 h1h7"),
    ("UTnvP", "8/1p2kp2/p1p1r1p1/6P1/5K2/1P1R1P2/P2R4/6r1 b - - 1 51", "e7e8 d3d8 e8e7 d2d7"),
    ("aHP6J", "rn4k1/3n1r1p/1q2p1Q1/ppppP1P1/5B1R/PN2P3/1P2BP2/2K4R b - - 0 20", "h7g6 h4h8 g8g7 h1h7"),
    ("Ws7i7", "4k3/pp3p2/4pP1r/7p/3R4/3R3P/PPr3PK/8 b - - 4 29", "h6f6 d4d8 e8e7 d3d7"),
    ("5b7ro", "4r3/p3rkpp/2R5/2p5/2Pp4/1P1R1Pb1/P5PP/5K2 w - - 0 30", "h2g3 e7e1 f1f2 e8e2"),
    ("dmF6r", "7r/R3bkp1/1P2p3/2p1Pp1r/3p1P2/1P1P1bP1/1BP5/5RK1 w - - 0 30", "f1f3 h5h1 g1g2 h8h2"),
    ("A8LPg", "1k6/2p2p2/1p1p4/3P3p/R2Pr3/8/4B2r/R4K2 b - - 3 43", "e4e2 a4a8 b8b7 a1a7"),
    ("86Afy", "2r5/2R1bkpp/p1K2p2/8/2r5/5N2/P4PPP/4R3 w - - 5 31", "c6d7 c4c7"),
    ("a6xm0", "5k2/p1p1R1pp/1pr2p2/7P/8/8/3r1PP1/4R1K1 b - - 0 30", "h7h6 e7e8 f8f7 e1e7"),
    ("4CUvk", "6k1/pp3p1p/2p1n1P1/4P3/4K3/2Pr2P1/P2r1P1R/7R b - - 4 29", "h7g6 h2h8 g8g7 h1h7"),
]

def parse_fen(fen):
    parts = fen.split()
    return {
        'board': parts[0],
        'turn': parts[1],
        'castling': parts[2],
        'ep': parts[3],
        'halfmove': int(parts[4]),
        'fullmove': int(parts[5])
    }

def fen_to_board(board_str):
    rows = board_str.split('/')
    b = {}
    for rank_idx, row in enumerate(rows):
        file_idx = 0
        for ch in row:
            if ch.isdigit():
                file_idx += int(ch)
            else:
                sq = chr(ord('a') + file_idx) + str(8 - rank_idx)
                b[sq] = ch
                file_idx += 1
    return b

def board_to_fen(b):
    rows = []
    for rank in range(8, 0, -1):
        row = ''
        empty = 0
        for file_ch in 'abcdefgh':
            sq = file_ch + str(rank)
            piece = b.get(sq)
            if piece:
                if empty: row += str(empty); empty = 0
                row += piece
            else:
                empty += 1
        if empty: row += str(empty)
        rows.append(row)
    return '/'.join(rows)

def apply_uci(fen_str, uci):
    f = parse_fen(fen_str)
    b = fen_to_board(f['board'])
    fr = uci[:2]
    to = uci[2:4]
    promo = uci[4] if len(uci) > 4 else None

    piece = b.get(fr)
    if not piece:
        print(f"  ERROR: no piece at {fr} in {fen_str}")
        return fen_str

    captured = b.get(to)

    # Handle castling
    is_castling = piece.lower() == 'k' and abs(ord(fr[0]) - ord(to[0])) == 2

    del b[fr]

    # En passant
    ep_capture = None
    if piece.lower() == 'p' and to == f['ep'] and f['ep'] != '-':
        ep_rank = '5' if piece == 'P' else '4'
        ep_sq = to[0] + ep_rank
        del b[ep_sq]
        ep_capture = True

    if promo:
        b[to] = promo.upper() if piece.isupper() else promo.lower()
    else:
        b[to] = piece

    # Castling rook
    if is_castling:
        if to[0] == 'g':  # kingside
            rook_fr = 'h' + fr[1]
            rook_to = 'f' + fr[1]
        else:  # queenside
            rook_fr = 'a' + fr[1]
            rook_to = 'd' + fr[1]
        if rook_fr in b:
            b[rook_to] = b[rook_fr]
            del b[rook_fr]

    # New EP target
    new_ep = '-'
    if piece.lower() == 'p' and abs(int(fr[1]) - int(to[1])) == 2:
        ep_rank = str((int(fr[1]) + int(to[1])) // 2)
        new_ep = to[0] + ep_rank

    new_turn = 'b' if f['turn'] == 'w' else 'w'

    # Halfmove clock
    new_half = 0 if (piece.lower() == 'p' or captured or ep_capture) else f['halfmove'] + 1

    new_full = f['fullmove'] + (1 if f['turn'] == 'b' else 0)

    # Castling rights (simplified - just clear if king/rook moved)
    new_castling = f['castling']
    if new_castling != '-':
        if piece == 'K': new_castling = new_castling.replace('K','').replace('Q','')
        if piece == 'k': new_castling = new_castling.replace('k','').replace('q','')
        if fr == 'h1': new_castling = new_castling.replace('K','')
        if fr == 'a1': new_castling = new_castling.replace('Q','')
        if fr == 'h8': new_castling = new_castling.replace('k','')
        if fr == 'a8': new_castling = new_castling.replace('q','')
        if to == 'h1': new_castling = new_castling.replace('K','')
        if to == 'a1': new_castling = new_castling.replace('Q','')
        if to == 'h8': new_castling = new_castling.replace('k','')
        if to == 'a8': new_castling = new_castling.replace('q','')
        if not new_castling: new_castling = '-'

    new_board = board_to_fen(b)
    return f"{new_board} {new_turn} {new_castling} {new_ep} {new_half} {new_full}"

results = []
for pid, fen, moves_str in PUZZLES_RAW:
    moves = moves_str.strip().split()
    start_fen = apply_uci(fen, moves[0])
    sol = moves[1:]
    # Determine solver's turn (after moves[0])
    solver_turn = start_fen.split()[1]
    results.append((pid, start_fen, sol, solver_turn))

print("const PUZZLES = [")
for i, (pid, start_fen, sol, turn) in enumerate(results):
    sol_str = ','.join(f"'{m}'" for m in sol)
    comma = ',' if i < len(results)-1 else ''
    print(f"  {{id:'{pid}',fen:'{start_fen}',sol:[{sol_str}],turn:'{turn}'}}{comma}")
print("];")
