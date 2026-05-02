import csv, chess, chess.pgn, io, random

CSV_FILE = 'lichess_db_puzzle.csv'

# Rating buckets: easy 900-1200, medium 1200-1500, hard 1500-1900
EASY_RANGE   = (900,  1200)
MEDIUM_RANGE = (1200, 1500)
HARD_RANGE   = (1500, 1900)

easy, medium, hard = [], [], []

with open(CSV_FILE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        themes = row.get('Themes', '') or row.get('themes', '')
        if 'Chekhover' not in themes:
            continue
        try:
            rating = int(row.get('Rating', row.get('rating', 0)))
        except:
            continue
        puzzle_id = row.get('PuzzleId', row.get('puzzleId', ''))
        fen       = row.get('FEN', row.get('fen', ''))
        moves     = row.get('Moves', row.get('moves', ''))
        if not fen or not moves:
            continue
        entry = (puzzle_id, fen, moves, rating, themes)
        if EASY_RANGE[0] <= rating < EASY_RANGE[1]:
            easy.append(entry)
        elif MEDIUM_RANGE[0] <= rating < MEDIUM_RANGE[1]:
            medium.append(entry)
        elif HARD_RANGE[0] <= rating < HARD_RANGE[1]:
            hard.append(entry)

print(f"Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")

random.seed(42)
random.shuffle(easy)
random.shuffle(medium)
random.shuffle(hard)

def apply_and_validate(fen, moves_str):
    uci_list = moves_str.strip().split()
    if len(uci_list) < 2:
        return None, None
    board = chess.Board(fen)
    # apply setup move
    try:
        board.push_uci(uci_list[0])
    except:
        return None, None
    puzzle_fen = board.fen()
    # determine turn from puzzle_fen
    turn = 'w' if board.turn == chess.WHITE else 'b'
    sol_uci = uci_list[1:]
    # validate all solution moves
    for uci in sol_uci:
        try:
            board.push_uci(uci)
        except:
            return None, None
    return puzzle_fen, sol_uci, turn

results = []
for bucket in [easy, medium, hard]:
    count = 0
    for entry in bucket:
        if count >= 14:
            break
        pid, fen, moves, rating, themes = entry
        r = apply_and_validate(fen, moves)
        if r is None or r[0] is None:
            continue
        puzzle_fen, sol_uci, turn = r
        results.append((puzzle_fen, sol_uci, turn, rating))
        count += 1

print(f"\nTotal valid: {len(results)}")
print()
for i, (fen, sol, turn, rating) in enumerate(results):
    sol_str = ', '.join(f"'{u}'" for u in sol)
    print(f"  {{ fen:'{fen}', sol:[{sol_str}], turn:'{turn}' }},  // #{i} rating={rating}")
