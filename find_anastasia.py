import csv
import chess

CSV_PATH = r"C:\Users\irina\SahMatAnimat\lichess_db_puzzle.csv"

EXCLUDED_FENS = {
    "5r1k/1b2Nppp/8/2R5/4Q3/8/5PPP/6K1",
    "5rk1/1b3ppp/8/2RN4/8/8/2Q2PPP/6K1",
    "1r5k/6pp/2pr4/P1Q3bq/1P2Bn2/2P5/5PPP/R3NRK1",
}

def apply_move(fen, uci_move):
    board = chess.Board(fen)
    board.push_uci(uci_move)
    return board.fen()

def fen_position(fen):
    """Return just the board+turn part (first 2 fields) for comparison."""
    parts = fen.split()
    return parts[0]

def get_turn(fen):
    parts = fen.split()
    return parts[1]

puzzles = []

print("Reading CSV...")
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        themes = row['Themes'].split()
        if 'anastasiaMate' not in themes:
            continue

        base_fen = row['FEN']
        moves = row['Moves'].split()
        if len(moves) < 2:
            continue

        # Apply opponent's error move to get puzzle start FEN
        try:
            start_fen = apply_move(base_fen, moves[0])
        except Exception as e:
            continue

        start_pos = fen_position(start_fen)

        # Exclude already-used examples
        if start_pos in EXCLUDED_FENS:
            continue

        rating = int(row['Rating'])
        nb_plays = int(row['NbPlays'])
        turn = get_turn(start_fen)
        solution = moves[1:]

        # Validate solution moves
        try:
            board = chess.Board(start_fen)
            for m in solution:
                board.push_uci(m)
        except Exception:
            continue

        puzzles.append({
            'id': row['PuzzleId'],
            'rating': rating,
            'nb_plays': nb_plays,
            'turn': turn,
            'start_fen': start_fen,
            'start_pos': start_pos,
            'solution': solution,
            'themes': themes,
            'url': row['GameUrl'],
        })

print(f"Total anastasiaMate puzzles (after exclusions): {len(puzzles)}")

# ── LESSON EXAMPLES (Task 1) ──────────────────────────────────────────────────
# Want: pedagogically clear, different patterns, mateIn2/mateIn3 preferred,
# NbPlays > 500, rating 1000–1700, diverse (black side, different structures)

lesson_candidates = [p for p in puzzles if 1000 <= p['rating'] <= 1700 and p['nb_plays'] > 500]
lesson_candidates.sort(key=lambda p: p['nb_plays'], reverse=True)

# Pick 2 diverse examples: try to get one white-to-move and one black-to-move,
# and short solutions (mateIn2 = 2 moves, mateIn3 = 3 moves)
def sol_len_ok(p):
    return len(p['solution']) in (2, 3, 4, 5)

short_candidates = [p for p in lesson_candidates if sol_len_ok(p)]

lessons = []
used_ids = set()

# First: prefer black-to-move (less common, more interesting variety)
for p in short_candidates:
    if p['turn'] == 'b' and p['id'] not in used_ids:
        lessons.append(p)
        used_ids.add(p['id'])
        break

# Then: white-to-move
for p in short_candidates:
    if p['turn'] == 'w' and p['id'] not in used_ids:
        lessons.append(p)
        used_ids.add(p['id'])
        break

# Fallback: if not enough, just take top by nb_plays
for p in lesson_candidates:
    if len(lessons) >= 2:
        break
    if p['id'] not in used_ids:
        lessons.append(p)
        used_ids.add(p['id'])

# ── ARENA PUZZLES (Task 2) ────────────────────────────────────────────────────
# Exclude lesson examples too
for p in lessons:
    used_ids.add(p['id'])

easy_pool   = sorted([p for p in puzzles if  800 <= p['rating'] < 1400 and p['id'] not in used_ids],
                     key=lambda p: p['nb_plays'], reverse=True)
medium_pool = sorted([p for p in puzzles if 1400 <= p['rating'] < 1700 and p['id'] not in used_ids],
                     key=lambda p: p['nb_plays'], reverse=True)
hard_pool   = sorted([p for p in puzzles if 1700 <= p['rating'] <= 2300 and p['id'] not in used_ids],
                     key=lambda p: p['nb_plays'], reverse=True)

def pick(pool, n, used):
    result = []
    for p in pool:
        if len(result) >= n:
            break
        if p['id'] not in used:
            result.append(p)
            used.add(p['id'])
    return result

arena_easy   = pick(easy_pool,   14, used_ids)
arena_medium = pick(medium_pool, 13, used_ids)
arena_hard   = pick(hard_pool,   13, used_ids)

# ── OUTPUT ────────────────────────────────────────────────────────────────────
print("\n" + "="*80)
print("LESSON EXAMPLES:")
print("="*80)
for p in lessons:
    print(f"id={p['id']} rating={p['rating']} turn={p['turn']} "
          f"fen='{p['start_pos']}' "
          f"sol={p['solution']} "
          f"url='{p['url']}'")

print("\n" + "="*80)
print(f"ARENA EASY (0-{len(arena_easy)-1}):")
print("="*80)
for i, p in enumerate(arena_easy):
    print(f"[{i:2d}] id={p['id']} rating={p['rating']} nb_plays={p['nb_plays']} turn={p['turn']} "
          f"fen='{p['start_pos']}' "
          f"sol={p['solution']}")

print("\n" + "="*80)
print(f"ARENA MEDIUM ({len(arena_easy)}-{len(arena_easy)+len(arena_medium)-1}):")
print("="*80)
for i, p in enumerate(arena_medium):
    print(f"[{i+len(arena_easy):2d}] id={p['id']} rating={p['rating']} nb_plays={p['nb_plays']} turn={p['turn']} "
          f"fen='{p['start_pos']}' "
          f"sol={p['solution']}")

print("\n" + "="*80)
print(f"ARENA HARD ({len(arena_easy)+len(arena_medium)}-{len(arena_easy)+len(arena_medium)+len(arena_hard)-1}):")
print("="*80)
for i, p in enumerate(arena_hard):
    print(f"[{i+len(arena_easy)+len(arena_medium):2d}] id={p['id']} rating={p['rating']} nb_plays={p['nb_plays']} turn={p['turn']} "
          f"fen='{p['start_pos']}' "
          f"sol={p['solution']}")

print(f"\nSummary: {len(lessons)} lessons, {len(arena_easy)} easy, {len(arena_medium)} medium, {len(arena_hard)} hard")
