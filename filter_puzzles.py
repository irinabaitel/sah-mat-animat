"""
Filtrează 50 puzzle-uri mateIn3 și 50 mateIn4 din lichess_db_puzzle.csv.
În CSV, prima mutare este "declanșatorul" adversarului; o aplicăm pe FEN
și stocăm restul ca soluție — același format ca puzzle-urile din API.
Rezultat: mat3_puzzles.json și mat4_puzzles.json
"""
import csv, json
import chess

CSV = "lichess_db_puzzle.csv"
TARGETS = {
    "mateIn3": {"moves_len": 6, "out": "mat3_puzzles.json", "limit": 50},
    "mateIn4": {"moves_len": 8, "out": "mat4_puzzles.json", "limit": 50},
}

collected = {k: [] for k in TARGETS}
done = {k: False for k in TARGETS}

print(f"Citesc {CSV} ...")

with open(CSV, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # sare antetul
    for row in reader:
        if all(done.values()):
            break
        if len(row) < 8:
            continue

        raw_fen = row[1]
        moves   = row[2].split()
        themes  = row[7].split()

        for theme, cfg in TARGETS.items():
            if done[theme]:
                continue
            if theme in themes and len(moves) == cfg["moves_len"]:
                # aplică mutarea declanșatoare → obținem FEN-ul real al puzzle-ului
                try:
                    board = chess.Board(raw_fen)
                    trigger = chess.Move.from_uci(moves[0])
                    if trigger not in board.legal_moves:
                        continue
                    board.push(trigger)
                    fen = board.fen()
                    sol = moves[1:]   # restul: alternativ jucător / oponent
                    turn = "w" if board.turn == chess.WHITE else "b"
                    collected[theme].append({"fen": fen, "sol": sol, "turn": turn})
                    n = len(collected[theme])
                    if n % 10 == 0 or n == cfg["limit"]:
                        print(f"  {theme}: {n}/{cfg['limit']}")
                    if n >= cfg["limit"]:
                        done[theme] = True
                except Exception:
                    continue

for theme, cfg in TARGETS.items():
    with open(cfg["out"], "w", encoding="utf-8") as f:
        json.dump(collected[theme], f, indent=2)
    print(f"✅ {theme}: {len(collected[theme])} puzzle-uri → {cfg['out']}")
