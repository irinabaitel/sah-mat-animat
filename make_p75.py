import chess, sys

# Raw lichess CSV data: (id, fen_before_first_move, moves_str, rating, tag)
raw = [
    # bodenMate easy (<900)
    ('09GYu','rnb1k1nr/ppp2ppp/3b4/8/8/5Nq1/PPPPP2P/RNBQKB1R w KQkq - 0 6','h2g3 d6g3',454,'Boden'),
    ('098RM','rnbqkbnr/ppppp2p/6p1/5P2/8/8/PPPPBPPP/RNBQK1NR b KQkq - 1 3','g6f5 e2h5',639,'Boden'),
    ('007c6','2kr3r/pp1n2pp/2QB1bp1/5q2/2B5/8/PPP2PPP/3R1RK1 b - - 0 17','b7c6 c4a6',721,'Boden'),
    ('0Bczc','2kr3r/pp1n1ppp/2pB2n1/2P5/3P4/5P2/P3BP1P/2KR3R b - - 0 16','b7b6 e2a6',800,'Boden'),
    # doubleBishopMate easy (<900)
    ('036MU','2r4k/pB4p1/1b1B4/1b5p/5P2/6P1/P6P/7K w - - 0 27','b7c8 b5c6',781,'Dublu'),
    ('05mPT','r1b1k1nr/ppp2p2/2qp2p1/3NN1p1/4P3/1P6/1PPP1bPP/R1BK3R w kq - 0 13','e5c6 c8g4',877,'Dublu'),
    ('00FjB','rnbk3r/pppp1Bpp/8/5p2/4p3/2PP4/P1P2PPP/R1B1K2R b KQ - 0 13','h8f8 c1g5',879,'Dublu'),
    ('08eZr','r1b1r2k/ppp4p/6p1/5nB1/2B5/P1P5/2P2KPP/R6R b - - 2 19','f5d6 g5f6',792,'Dublu'),
    # bodenMate medium (900-1200)
    ('001gi','r6r/1pNk1ppp/2np4/b3p3/4P1b1/N1Q5/P4PPP/R3KB1R w KQ - 3 18','c7a8 a5c3',819,'Boden'),
    ('033ae','2kr1b1r/1p1n1pp1/p1N1p1b1/2p4p/3PPB1P/1PP2P2/6P1/R3KB1R b KQ - 1 16','b7c6 f1a6',930,'Boden'),
    ('0824f','r1bk4/1pp1b3/2B3p1/p7/P7/3R1p2/1BP2P2/2K5 b - - 1 25','e7d6 b2f6',935,'Boden'),
    ('0BHDL','4kb1r/pb3p2/3p1Bp1/2p4p/8/2P1PPK1/P1q4P/R4B1R b k - 0 22','h8g8 f1b5 b7c6 b5c6',913,'Boden'),
    # doubleBishopMate medium (900-1200)
    ('07VmT','4k3/ppR5/2p4p/4n3/4P1b1/2N3P1/PP3b1P/7K w - - 1 29','c7b7 g4f3',901,'Dublu'),
    ('07F8Y','rnb1kb1r/pp3ppp/2p5/8/2P2q2/4PN2/PP1B2PP/R2Q1BKR w kq - 0 13','e3f4 f8c5 f3d4 c5d4 d2e3 d4e3',848,'Dublu'),
    ('06Wrz','r3qr1k/pp4pp/3p1N2/5P2/2BQP1b1/1P6/PBP5/R5K1 b - - 0 21','g7f6 d4f6 f8f6 b2f6',951,'Dublu'),
    ('0DL2F','k7/p4p2/Bp5p/8/2P1b1n1/2q3Q1/P2b2P1/K2R4 w - - 4 37','g3c3 d2c3',860,'Dublu'),
    # bodenMate hard (>=1200)
    ('01z9G','2kr1b1r/pp1n1pp1/1qp1pnp1/8/2BP1BP1/2N2Q1P/PPP2P2/2K1R2R b - - 1 15','b6d4 f3c6 b7c6 c4a6',1050,'Boden'),
    ('0ALUW','r3k2r/pp1nqpp1/2p1p3/8/1b1PQB1P/8/PPP5/2KR1B1R b kq - 0 18','e8c8 e4c6 b7c6 f1a6',1215,'Boden'),
    # doubleBishopMate hard (>=1200)
    ('02mx1','2bk4/1p2b2p/2n3p1/1B2Np2/4p3/2B1P2P/1P3PP1/5K2 b - - 3 34','c6e5 c3a5 b7b6 a5b6',1260,'Dublu'),
    ('02dgL','r1bq1r1k/p2n3p/2p1B1pQ/3p2B1/4p3/2P5/P1P4P/R3K2R b KQ - 0 20','d8a5 h6f8 d7f8 g5f6',1498,'Dublu'),
]

print("/* 0-7 UȘOR */")
for i, (pid, fen, moves_str, rating, tag) in enumerate(raw):
    moves = moves_str.split()
    board = chess.Board(fen)
    first = chess.Move.from_uci(moves[0])
    board.push(first)
    pfen = board.fen()
    sol = moves[1:]
    turn = 'w' if board.turn == chess.WHITE else 'b'
    sol_str = "','".join(sol)
    if i == 8:
        print("  /* 8-15 MEDIU */")
    elif i == 16:
        print("  /* 16-19 AVANSAT */")
    sys.stdout.write("  {id:'%s',fen:'%s',sol:['%s'],turn:'%s'},  // %s r:%d\n" % (
        pid, pfen, sol_str, turn, tag, rating))
