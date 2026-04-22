"""
Descarcă primele 50 puzzle-uri mateIn2 din baza de date publică Lichess.
Rulează cu:  python mat2_fetch.py
Rezultat:    mat2_puzzles.json  (în același folder)
"""
import urllib.request, json, sys

try:
    import zstandard as zstd
except ImportError:
    print("Instalez zstandard...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "zstandard", "-q"])
    import zstandard as zstd

URL     = "https://database.lichess.org/lichess_db_puzzle.csv.zst"
TARGET  = 50
CHUNK   = 1 << 16   # 64 KB

print(f"Conectare la {URL} ...")
req = urllib.request.Request(URL, headers={"User-Agent": "SahMatAnimat/1.0"})

collected = []
buf = b""

with urllib.request.urlopen(req, timeout=30) as resp:
    dctx = zstd.ZstdDecompressor()
    with dctx.stream_reader(resp) as reader:
        header_skipped = False
        while len(collected) < TARGET:
            chunk = reader.read(CHUNK)
            if not chunk:
                break
            buf += chunk
            lines = buf.split(b"\n")
            buf = lines[-1]          # ultimul rând poate fi incomplet
            for line in lines[:-1]:
                row = line.decode("utf-8", errors="ignore").strip()
                if not row:
                    continue
                if not header_skipped:
                    header_skipped = True
                    continue        # sare antetul CSV
                parts = row.split(",")
                if len(parts) < 8:
                    continue
                # CSV: PuzzleId, FEN, Moves, Rating, RatingDev, Popularity, NbPlays, Themes, ...
                fen    = parts[1]
                moves  = parts[2].split()
                themes = parts[7].split()
                if "mateIn2" in themes and len(moves) == 3:
                    turn = "w" if " w " in fen else "b"
                    collected.append({"fen": fen, "sol": moves, "turn": turn})
                    print(f"  #{len(collected):02d}  {fen[:45]}")
                    if len(collected) >= TARGET:
                        break

out = "mat2_puzzles.json"
with open(out, "w") as f:
    json.dump(collected, f, indent=2)

print(f"\n✅ Gata! {len(collected)} puzzle-uri salvate în {out}")
