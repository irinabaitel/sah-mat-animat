import csv, chess, random

CSV_FILE = 'lichess_db_puzzle.csv'

EASY_RANGE   = (900,  1200)
MEDIUM_RANGE = (1200, 1500)
HARD_RANGE   = (1500, 1900)

easy, medium, hard = [], [], []

with open(CSV_FILE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        themes = row.get('Themes', '') or row.get('themes', '')
        if 'deflection' not in themes:
            continue
        try:
            rating = int(row.get('Rating', row.get('rating', 0)))
        except:
            continue
        fen   = row.get('FEN',   row.get('fen',   ''))
        moves = row.get('Moves', row.get('moves', ''))
        if not fen or not moves:
            continue
        entry = (fen, moves, rating)
        if EASY_RANGE[0]   <= rating < EASY_RANGE[1]:   easy.append(entry)
        elif MEDIUM_RANGE[0] <= rating < MEDIUM_RANGE[1]: medium.append(entry)
        elif HARD_RANGE[0]   <= rating < HARD_RANGE[1]:   hard.append(entry)

print(f"Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")

random.seed(99)
random.shuffle(easy)
random.shuffle(medium)
random.shuffle(hard)

def validate(fen, moves_str):
    uci_list = moves_str.strip().split()
    if len(uci_list) < 2:
        return None, None, None
    board = chess.Board(fen)
    try:
        board.push_uci(uci_list[0])
    except:
        return None, None, None
    puzzle_fen = board.fen()
    turn = 'w' if board.turn == chess.WHITE else 'b'
    sol = uci_list[1:]
    for uci in sol:
        try:
            board.push_uci(uci)
        except:
            return None, None, None
    return puzzle_fen, sol, turn

results = []
for bucket, target in [(easy, 12), (medium, 13), (hard, 15)]:
    count = 0
    for fen, moves, rating in bucket:
        if count >= target:
            break
        pfen, sol, turn = validate(fen, moves)
        if pfen is None:
            continue
        results.append((pfen, sol, turn, rating))
        count += 1

print(f"Total valid: {len(results)}")
print()
for i, (fen, sol, turn, rating) in enumerate(results):
    sol_str = ', '.join(f"'{u}'" for u in sol)
    print(f"  {{ fen:'{fen}', sol:[{sol_str}], turn:'{turn}' }},  // #{i} r={rating}")
