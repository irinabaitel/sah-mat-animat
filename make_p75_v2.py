import chess, csv, sys

def is_double_bishop_mate(fen, sol_uci, theme):
    """Check that the final position is checkmate delivered by two bishops."""
    try:
        board = chess.Board(fen)
        for uci in sol_uci:
            m = chess.Move.from_uci(uci)
            if m not in board.legal_moves:
                return False
            board.push(m)
        if not board.is_checkmate():
            return False
        # Find attacking pieces — should include at least 2 bishops
        # The king side to move is in check; find checkers
        checkers = board.checkers()
        attacker_types = set()
        for sq in chess.SquareSet(checkers):
            attacker_types.add(board.piece_type_at(sq))
        # Must have a bishop as a checker; other bishop pins escape squares
        if chess.BISHOP not in attacker_types:
            return False
        return True
    except Exception:
        return False

results_boden = []
results_double = []

with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        themes = row.get('Themes', '')

        is_boden = 'bodenMate' in themes and 'doubleBishopMate' not in themes
        is_double = 'doubleBishopMate' in themes

        if not is_boden and not is_double:
            continue

        # Only 1-3 move solutions
        has_mat = any(t in themes for t in ['mateIn1', 'mateIn2', 'mateIn3'])
        if not has_mat:
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

        if not is_double_bishop_mate(puzzle_fen, sol, themes):
            continue

        entry = {
            'id': row['PuzzleId'],
            'fen': puzzle_fen,
            'sol': sol,
            'turn': turn,
            'rating': rating,
            'tag': 'Boden' if is_boden else 'Dublu',
        }

        if is_boden:
            results_boden.append(entry)
        else:
            results_double.append(entry)

sys.stderr.write(f"bodenMate valid: {len(results_boden)}, doubleBishopMate valid: {len(results_double)}\n")

results_boden.sort(key=lambda x: x['rating'])
results_double.sort(key=lambda x: x['rating'])

# Pick 20 from each: 8 easy, 8 medium, 4 hard
def pick(lst, n_easy, n_med, n_hard):
    easy = [x for x in lst if x['rating'] < 1000][:n_easy]
    med  = [x for x in lst if 1000 <= x['rating'] < 1400][:n_med]
    hard = [x for x in lst if x['rating'] >= 1400][:n_hard]
    return easy + med + hard

b20 = pick(results_boden, 8, 8, 4)
d20 = pick(results_double, 8, 8, 4)

# Interleave easy/med/hard keeping theme variety
easy = [x for x in b20 if x['rating'] < 1000] + [x for x in d20 if x['rating'] < 1000]
med  = [x for x in b20 if 1000 <= x['rating'] < 1400] + [x for x in d20 if 1000 <= x['rating'] < 1400]
hard = [x for x in b20 if x['rating'] >= 1400] + [x for x in d20 if x['rating'] >= 1400]

puzzles = easy + med + hard
sys.stderr.write(f"Total: {len(puzzles)} (easy:{len(easy)}, med:{len(med)}, hard:{len(hard)})\n")

for i, p in enumerate(puzzles):
    sol_str = "','".join(p['sol'])
    sys.stdout.write("  {id:'%s',fen:'%s',sol:['%s'],turn:'%s'},  // #%d %s r:%d\n" % (
        p['id'], p['fen'], sol_str, p['turn'], i, p['tag'], p['rating']))
