import csv, chess, sys

results = {"boden": [], "double": []}

with open("lichess_db_puzzle.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row["PuzzleId"]
        fen = row["FEN"]
        moves_str = row["Moves"]
        themes = row.get("Themes", "")

        try:
            rating = int(row["Rating"])
        except Exception:
            rating = 9999

        moves = moves_str.split()
        if len(moves) < 2:
            continue

        board = chess.Board(fen)
        first_move = chess.Move.from_uci(moves[0])
        board.push(first_move)
        puzzle_fen = board.fen()
        sol = moves[1:]
        turn = "w" if board.turn == chess.WHITE else "b"

        entry = {"id": pid, "fen": puzzle_fen, "sol": sol, "turn": turn, "rating": rating, "themes": themes}

        if "bodenMate" in themes and "doubleBishopMate" not in themes:
            results["boden"].append(entry)
        elif "doubleBishopMate" in themes:
            results["double"].append(entry)

boden = sorted(results["boden"], key=lambda x: x["rating"])
double = sorted(results["double"], key=lambda x: x["rating"])

sys.stdout.write(f"bodenMate: {len(boden)}, doubleBishopMate: {len(double)}\n")

def pick(lst, n_easy, n_med, n_hard):
    easy = [x for x in lst if x["rating"] < 900][:n_easy]
    med  = [x for x in lst if 900 <= x["rating"] < 1200][:n_med]
    hard = [x for x in lst if x["rating"] >= 1200][:n_hard]
    return easy + med + hard

b = pick(boden, 4, 4, 2)
d = pick(double, 4, 4, 2)

easy = [x for x in b if x["rating"] < 900] + [x for x in d if x["rating"] < 900]
med  = [x for x in b if 900 <= x["rating"] < 1200] + [x for x in d if 900 <= x["rating"] < 1200]
hard = [x for x in b if x["rating"] >= 1200] + [x for x in d if x["rating"] >= 1200]

puzzles = easy + med + hard
sys.stdout.write(f"Total: {len(puzzles)} (easy:{len(easy)}, med:{len(med)}, hard:{len(hard)})\n")

for p in puzzles:
    sol_str = "','".join(p["sol"])
    tag = "Boden" if "bodenMate" in p["themes"] and "doubleBishopMate" not in p["themes"] else "Dublu"
    sys.stdout.write("  {id:'%s',fen:'%s',sol:['%s'],turn:'%s'},  // %s r:%d\n" % (
        p["id"], p["fen"], sol_str, p["turn"], tag, p["rating"]))
