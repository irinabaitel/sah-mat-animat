import chess, csv, sys

# Puzzles already known to be bad (by lichess ID)
BLACKLIST = {'CKIgZ', '19ZIY', 'gNYEW'}

def is_true_double_bishop_mate(fen, sol_uci):
    """Both bishops must be NECESSARY for the checkmate (removing either breaks it)."""
    try:
        board = chess.Board(fen)
        for uci in sol_uci:
            m = chess.Move.from_uci(uci)
            if m not in board.legal_moves:
                return False
            board.push(m)

        if not board.is_checkmate():
            return False

        attacker_color = not board.turn
        bishops = list(board.pieces(chess.BISHOP, attacker_color))

        if len(bishops) < 2:
            return False

        # Both bishops must be necessary: removing either one breaks the checkmate
        for bsq in bishops:
            test = board.copy()
            test.remove_piece_at(bsq)
            if test.is_checkmate():
                # Still checkmate without this bishop → it's not needed
                return False

        return True
    except Exception:
        return False

results_boden = []
results_double = []

with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row['PuzzleId']
        if pid in BLACKLIST:
            continue

        themes = row.get('Themes', '')
        is_boden  = 'bodenMate'        in themes and 'doubleBishopMate' not in themes
        is_double = 'doubleBishopMate' in themes

        if not is_boden and not is_double:
            continue

        if not any(t in themes for t in ['mateIn1', 'mateIn2', 'mateIn3']):
            continue

        try:
            rating = int(row['Rating'])
        except Exception:
            continue

        if rating < 600:
            continue

        moves = row['Moves'].split()
        if len(moves) < 2:
            continue

        board = chess.Board(row['FEN'])
        first = chess.Move.from_uci(moves[0])
        if first not in board.legal_moves:
            continue
        board.push(first)
        puzzle_fen = board.fen()
        sol = moves[1:]
        turn = 'w' if board.turn == chess.WHITE else 'b'

        if not is_true_double_bishop_mate(puzzle_fen, sol):
            continue

        entry = {
            'id': pid, 'fen': puzzle_fen, 'sol': sol,
            'turn': turn, 'rating': rating,
            'tag': 'Boden' if is_boden else 'Dublu',
        }

        if is_boden:
            results_boden.append(entry)
        else:
            results_double.append(entry)

results_boden.sort(key=lambda x: x['rating'])
results_double.sort(key=lambda x: x['rating'])

sys.stderr.write(f"bodenMate OK: {len(results_boden)}, doubleBishopMate OK: {len(results_double)}\n")

def pick(lst, n_easy, n_med, n_hard):
    easy = [x for x in lst if x['rating'] < 1000][:n_easy]
    med  = [x for x in lst if 1000 <= x['rating'] < 1400][:n_med]
    hard = [x for x in lst if x['rating'] >= 1400][:n_hard]
    return easy + med + hard

b20 = pick(results_boden,  8, 8, 4)
d20 = pick(results_double, 8, 8, 4)

easy = [x for x in b20 if x['rating'] < 1000]  + [x for x in d20 if x['rating'] < 1000]
med  = [x for x in b20 if 1000 <= x['rating'] < 1400] + [x for x in d20 if 1000 <= x['rating'] < 1400]
hard = [x for x in b20 if x['rating'] >= 1400] + [x for x in d20 if x['rating'] >= 1400]

puzzles = easy + med + hard
sys.stderr.write(f"Total: {len(puzzles)} (easy:{len(easy)}, med:{len(med)}, hard:{len(hard)})\n")

for i, p in enumerate(puzzles):
    sol_str = "','".join(p['sol'])
    sys.stdout.write("  {id:'%s',fen:'%s',sol:['%s'],turn:'%s'},  // #%d %s r:%d\n" % (
        p['id'], p['fen'], sol_str, p['turn'], i+1, p['tag'], p['rating']))
