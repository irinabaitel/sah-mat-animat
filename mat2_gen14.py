"""
Generează 14 puzzle-uri mateIn2 verificate cu python-chess,
completând cele 36 deja colectate din Lichess → 50 total.
Scrie mat2_puzzles.json gata de integrat.
"""
import json, chess

# ── 36 puzzle-uri din Lichess ──────────────────────────────────────────────
LICHESS = [
  {"fen":"r6r/pQ3R2/6pk/6P1/3P4/PP3p1P/3q1P2/4R1K1 b - - 0 1","sol":["d2g5","g1f1","g5g2"],"turn":"b"},
  {"fen":"3r3r/1bkp1ppp/pp6/4P3/1QP2q1P/1R6/P3P1P1/5B1K w - - 0 1","sol":["b4b6","c7c8","b6b7"],"turn":"w"},
  {"fen":"5k2/5p2/4pp2/prq5/1p5Q/1P3P2/PK5P/3R4 w - - 0 1","sol":["h4h8","f8e7","h8d8"],"turn":"w"},
  {"fen":"4R3/Bp3kpp/2p5/8/PPb5/5p1P/5P2/1q2Q1K1 b - - 1 1","sol":["b1g6","g1h2","g6g2"],"turn":"b"},
  {"fen":"6k1/p5P1/2bN2Qp/2p5/8/8/P1q1p1PP/4n1K1 w - - 0 1","sol":["g6f7","g8h7","g7g8q"],"turn":"w"},
  {"fen":"r5r1/p4Q1p/2pkp3/q1ppp3/4nP1b/1P2P3/P1PPK1PP/RN5R w - - 0 1","sol":["f4e5","d6e5","f7f4"],"turn":"w"},
  {"fen":"2r3k1/3n1p1p/p3p1p1/1p2P3/3QbP1q/P1P4P/1P4P1/2NR1R1K b - - 1 1","sol":["h4h3","h1g1","h3g2"],"turn":"b"},
  {"fen":"r1bq2kr/2p1bp2/p1n2n2/1p2pQB1/3pP3/P2P3P/BPPN1PP1/R3K2R w KQ - 4 10","sol":["f5g6","g8f8","g6f7"],"turn":"w"},
  {"fen":"1r4k1/r4ppp/2n5/pp6/4nQ2/6P1/5P1P/3R2K1 w - - 0 1","sol":["f4b8","c6b8","d1d8"],"turn":"w"},
  {"fen":"8/pp2r1p1/2p1p3/4k2q/6R1/3QPKP1/PPP5/8 w - - 0 1","sol":["d3d4","e5f5","d4f4"],"turn":"w"},
  {"fen":"r1bqk2r/pp1np1b1/2p4p/4Npp1/2PPp3/4P1BP/PP3PP1/R2QKB1R w KQkq - 0 9","sol":["d1h5","e8f8","h5f7"],"turn":"w"},
  {"fen":"1r4nr/k4ppp/Bq1bp1b1/8/Q7/3P4/PPP2PP1/R3R2K w - - 1 1","sol":["a6c8","b6a5","a4a5"],"turn":"w"},
  {"fen":"5rk1/R3Qp1p/6p1/P1p5/2Bb4/6P1/3q1P1P/4N1K1 b - - 0 1","sol":["d2f2","g1h1","f2g1"],"turn":"b"},
  {"fen":"4Q3/1pk3bp/3N2p1/p1pP1pq1/2P5/P7/1P4PP/6K1 w - - 1 1","sol":["d6b5","c7b6","e8e6"],"turn":"w"},
  {"fen":"N4rk1/1b1nbqpp/p2p4/1p2n3/8/2P3N1/PPB2PPP/R1BQR1K1 b - - 1 1","sol":["f7f2","g1h1","f2g2"],"turn":"b"},
  {"fen":"2kr3B/pp6/2n4n/2bp4/6q1/2N3Pp/PPP2P1N/R2Q1RK1 b - - 1 1","sol":["g4g3","g1h1","g3g2"],"turn":"b"},
  {"fen":"7r/5pkp/6r1/4p1QP/4qp2/1P6/5PP1/3R2K1 w - - 1 1","sol":["h5h6","g7g8","g5d8"],"turn":"w"},
  {"fen":"1kr5/pppQ2pp/1q6/6B1/8/6bP/P1P2P2/3R2K1 w - - 0 1","sol":["d7c8","b8c8","d1d8"],"turn":"w"},
  {"fen":"8/pQ5p/2pk4/3b2q1/3P1p2/1PP4P/P5PK/6R1 b - - 1 1","sol":["g5g3","h2h1","g3h3"],"turn":"b"},
  {"fen":"8/3kp2p/2n5/2P5/1p1p2P1/3P4/qPKB1Q1P/3RR3 b - - 1 1","sol":["b4b3","c2c1","a2a1"],"turn":"b"},
  {"fen":"r4r1k/p4p1p/3p2p1/3Np1n1/2q1P3/P3PQ2/6PP/5RK1 w - - 1 1","sol":["f3f6","h8g8","d5e7"],"turn":"w"},
  {"fen":"Q7/6pk/4Bn1p/8/1p1q1P2/2r1R2P/6PK/8 w - - 1 1","sol":["e6f5","g7g6","e3e7"],"turn":"w"},
  {"fen":"4r1rk/pp3p1p/2pqnPpQ/3p2P1/3P1R2/2N4P/PPP5/3R2K1 w - - 1 1","sol":["h6h7","h8h7","f4h4"],"turn":"w"},
  {"fen":"r1b1k2r/ppp2ppp/5q2/8/6n1/1N1Pp1N1/PPP1Q1PP/R4BKR b kq - 1 1","sol":["f6f2","e2f2","e3f2"],"turn":"b"},
  {"fen":"r2r4/1p3pPk/p6p/2p1q1PQ/P7/7P/1PP4b/5R1K w - - 0 1","sol":["h5h6","h7g8","h6h8"],"turn":"w"},
  {"fen":"3Q4/k1p2pp1/1pP1pn1p/8/1n6/4B3/PPq2PPP/6K1 w - - 0 1","sol":["d8c7","a7a6","c7b6"],"turn":"w"},
  {"fen":"5rk1/Q4ppp/6r1/3P2P1/5q2/4RN1b/P3BP2/3R2K1 b - - 1 1","sol":["f4g4","g1h1","g4g2"],"turn":"b"},
  {"fen":"3r2k1/pp3ppp/5n2/8/2P5/2N3Q1/Pq3PPP/1R4K1 b - - 1 1","sol":["b2b1","c3b1","d8d1"],"turn":"b"},
  {"fen":"5rk1/p5pp/4p3/8/P7/6B1/4p1PP/2RrR1K1 b - - 1 1","sol":["f8f1","e1f1","e2f1q"],"turn":"b"},
  {"fen":"r3r1k1/ppb3pp/2pq4/2PPnp2/1P2p3/PQN1B2P/5PP1/R4RK1 b - - 1 1","sol":["e5f3","g2f3","d6h2"],"turn":"b"},
  {"fen":"5r1k/p1p3pp/8/2pQ4/3p4/3P2P1/PP4P1/R1B1rBK1 b - - 0 1","sol":["f8f1","g1h2","f1h1"],"turn":"b"},
  {"fen":"3q3r/r4p1k/2p2p1p/p4N1Q/1p2P3/1P5P/1PP2PP1/6K1 w - - 0 1","sol":["h5h6","h7g8","h6g7"],"turn":"w"},
  {"fen":"6k1/pp3np1/4Q2p/6P1/7P/8/P3rr2/K2R4 w - - 1 1","sol":["d1d8","g8h7","g5g6"],"turn":"w"},
  {"fen":"1r4k1/4pr1p/p2pR1pQ/1p6/2P5/1P4P1/PB3qBP/5b1K w - - 0 1","sol":["e6g6","h7g6","h6h8"],"turn":"w"},
  {"fen":"6k1/5p2/p3p1pp/8/2Q3N1/6PP/P3R2K/q2r4 b - - 1 1","sol":["d1h1","h2g2","a1f1"],"turn":"b"},
  {"fen":"6k1/6p1/6Np/1P3P2/rr6/8/8/3R2K1 w - - 1 1","sol":["d1d8","g8f7","d8f8"],"turn":"w"},
]

# ── Solver: verifică dacă poziția are mat în 2 forțat ─────────────────────
def find_mate2(fen):
    try:
        board = chess.Board(fen)
    except Exception:
        return None
    if board.is_game_over():
        return None

    for m1 in board.legal_moves:
        board.push(m1)
        if board.is_checkmate() or board.is_stalemate():
            board.pop(); continue

        key_ok = True
        example = None

        for m2 in board.legal_moves:
            board.push(m2)
            mated = False
            for m3 in board.legal_moves:
                board.push(m3)
                if board.is_checkmate():
                    if example is None:
                        example = [m1.uci(), m2.uci(), m3.uci()]
                    mated = True
                board.pop()
                if mated: break
            board.pop()
            if not mated:
                key_ok = False; break

        board.pop()
        if key_ok and example:
            turn = 'w' if board.turn == chess.WHITE else 'b'
            return {"fen": fen, "sol": example, "turn": turn}
    return None

# ── Candidați pentru cele 14 puzzle-uri rămase ────────────────────────────
CANDIDATES = [
    # Epaulette mate
    "8/8/8/8/8/3k4/3q4/3K4 b - - 0 1",
    # Corridor mate
    "8/8/8/8/8/1k6/8/KR6 w - - 0 1",
    # Queen + King vs King (ladder)
    "k7/8/KQ6/8/8/8/8/8 w - - 0 1",
    "k7/8/2K5/Q7/8/8/8/8 w - - 0 1",
    "8/k7/8/K7/Q7/8/8/8 w - - 0 1",
    # Arabian mate setup
    "7k/5N1R/8/8/8/8/8/6K1 w - - 0 1",
    "6Rk/7R/8/8/8/8/8/6K1 w - - 0 1",
    # Back rank
    "6k1/5ppp/8/8/8/8/5PPP/3RR1K1 w - - 0 1",
    "r5k1/5ppp/8/8/8/8/5PPP/4RRK1 w - - 0 1",
    # Anastasia
    "5R1k/p4ppp/8/4N3/8/8/PPP3PP/6K1 w - - 0 1",
    # Smothered
    "r1bqkbnr/pppp1ppp/8/4p3/2BnP3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
    # Dovetail mate
    "8/8/8/3k4/8/8/8/2KQ4 w - - 0 1",
    "8/8/8/8/3k4/8/8/2KQ4 w - - 0 1",
    # Queen endgame
    "8/8/8/8/8/k7/1Q6/1K6 w - - 0 1",
    "8/8/8/8/k7/8/1Q6/1K6 w - - 0 1",
    # Rook + King
    "8/8/8/8/8/k7/8/KR6 w - - 0 1",
    "k7/8/1K6/8/8/8/R7/8 w - - 0 1",
    # Rook + pawn
    "8/8/8/8/8/k7/pK6/R7 b - - 0 1",
    # Classical mate patterns
    "8/8/8/5k2/8/5K2/5Q2/8 w - - 0 1",
    "8/8/8/8/5k2/8/5KQ1/8 w - - 0 1",
    # Two bishops
    "8/8/8/8/3k4/3B4/3K4/3B4 w - - 0 1",
    "8/8/8/8/8/1k6/8/KBB5 w - - 0 1",
    # Discovered check
    "k7/1pR5/1K6/8/8/8/8/8 w - - 0 1",
    "1k6/1pR5/1K6/8/8/8/8/8 w - - 0 1",
    "k7/8/1K6/1R6/8/8/8/8 w - - 0 1",
    # More queen mates
    "8/8/1k6/8/8/8/1Q6/1K6 w - - 0 1",
    "8/1k6/8/8/8/8/1Q6/1K6 w - - 0 1",
    "8/8/8/1k6/8/1K6/1Q6/8 w - - 0 1",
    # Knight + Queen
    "k7/8/1K6/8/8/N7/1Q6/8 w - - 0 1",
    "k7/8/KN6/8/8/8/1Q6/8 w - - 0 1",
    # Rook + Bishop
    "k7/8/KR6/B7/8/8/8/8 w - - 0 1",
    "1k6/8/KR6/1B6/8/8/8/8 w - - 0 1",
    # More complex positions
    "r1b2rk1/pp2n1pp/3p4/q2Pp3/2P1Pp2/2N2Q2/PPB3PP/R4RK1 w - - 0 1",
    "2r3k1/1bqn1pp1/pp2p2p/8/3PB3/P1N1QP2/1PB3PP/5RK1 w - - 0 1",
    "r4rk1/3b1pp1/p3p3/1p1nN2Q/3P3P/q7/PP3PP1/2R1R1K1 w - - 0 1",
    "3q1r1k/1b4pp/p3Pn2/1p6/8/1B3Q2/PP3PPP/3R2K1 w - - 0 1",
    "r5k1/5ppp/p7/8/1b6/2N5/PPP2PPP/1K1R4 w - - 0 1",
    "5r1k/pp4pp/4p3/3pN3/3P3Q/8/PP3PPP/2qR2K1 w - - 0 1",
    "r4rk1/5ppp/8/3p4/3P2b1/4BN1q/PP3PPP/R2Q1RK1 b - - 0 1",
    "r2qr1k1/pp1n1pp1/2pN2bp/8/3PP3/1B4Q1/PPP3PP/R4RK1 w - - 0 1",
    "5rk1/p4ppp/8/2p5/4n3/1P3q2/PBQ2PPP/3R1RK1 b - - 0 1",
    "r1b2r1k/pp4pp/2p2q2/3pNb2/3P4/P4N2/1PP2QPP/R4RK1 w - - 0 1",
]

# ── Rulează solver-ul ──────────────────────────────────────────────────────
print(f"Pornesc cu {len(LICHESS)} puzzle-uri din Lichess.")
print(f"Caut 14 puzzle-uri valide din {len(CANDIDATES)} candidați...\n")

extra = []
for i, fen in enumerate(CANDIDATES):
    if len(extra) >= 14:
        break
    result = find_mate2(fen)
    if result:
        extra.append(result)
        print(f"  ✓ #{len(LICHESS)+len(extra):02d}  {result['turn']}  sol:{result['sol']}")
    else:
        print(f"  ✗ nu e mateIn2: {fen[:50]}")

print(f"\nGăsite: {len(extra)}/14")

all_puzzles = LICHESS + extra
with open("mat2_puzzles.json", "w") as f:
    json.dump(all_puzzles, f, indent=2)

print(f"✅ Salvat mat2_puzzles.json cu {len(all_puzzles)} puzzle-uri total.")
