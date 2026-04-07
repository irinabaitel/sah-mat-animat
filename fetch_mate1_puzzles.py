"""
Descarcă puzzle-uri mateIn1 din baza de date Lichess și le exportă ca JS array.
Necesită: pip install zstandard requests
"""

import sys
import subprocess

# Auto-instalare pachete lipsă
for pkg in ['zstandard', 'requests']:
    try:
        __import__(pkg)
    except ImportError:
        print(f"Instalez {pkg}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

import csv
import io
import json
import random
import requests
import zstandard as zstd

URL = "https://database.lichess.org/lichess_db_puzzle.csv.zst"

RATING_MIN  = 500   # puzzle-uri ușoare pentru începători
RATING_MAX  = 1100
MIN_POP     = 60    # popularitate minimă (0-100)
TARGET      = 100   # câte puzzle-uri vrem
MAX_SCAN    = 500_000  # oprim după atâtea rânduri scanate (evită download complet)

def apply_uci_move(fen, uci):
    """
    Aplică o mutare UCI pe un FEN fără python-chess.
    Returnează noul FEN (simplificat — suficient pentru puzzle display).
    Folosim python-chess dacă e disponibil, altfel fallback simplu.
    """
    try:
        import chess
        board = chess.Board(fen)
        board.push_uci(uci)
        return board.fen()
    except ImportError:
        pass

    # Fallback minimal fără python-chess:
    # Parsăm FEN-ul și mutăm piesa pe tabla 8x8
    parts = fen.split()
    board_str, turn, castling, ep, half, full = parts

    rows = board_str.split('/')
    grid = []
    for row in rows:
        line = []
        for ch in row:
            if ch.isdigit():
                line.extend(['.'] * int(ch))
            else:
                line.append(ch)
        grid.append(line)

    files = 'abcdefgh'
    fc, rc = files.index(uci[0]), 8 - int(uci[1])
    ft, rt = files.index(uci[2]), 8 - int(uci[3])

    piece = grid[rc][fc]
    grid[rc][fc] = '.'
    grid[rt][ft] = piece

    # Reconstruim FEN (fără castle/ep update exact — suficient pentru afișare)
    new_rows = []
    for line in grid:
        s, cnt = '', 0
        for cell in line:
            if cell == '.':
                cnt += 1
            else:
                if cnt: s += str(cnt); cnt = 0
                s += cell
        if cnt: s += str(cnt)
        new_rows.append(s)

    new_turn = 'b' if turn == 'w' else 'w'
    return ' '.join(['/'.join(new_rows), new_turn, castling, ep, half, full])


def fetch_puzzles():
    print(f"Conectare la {URL} ...")
    resp = requests.get(URL, stream=True, timeout=30)
    resp.raise_for_status()

    dctx = zstd.ZstdDecompressor()
    collected = []
    scanned   = 0

    with dctx.stream_reader(resp.raw) as reader:
        text = io.TextIOWrapper(reader, encoding='utf-8')
        csv_reader = csv.reader(text)

        # Header: PuzzleId,FEN,Moves,Rating,RatingDeviation,Popularity,NbPlays,Themes,GameUrl,OpeningTags
        header = next(csv_reader)
        print(f"Header: {header[:8]}")

        for row in csv_reader:
            scanned += 1
            if scanned % 50_000 == 0:
                print(f"  Scanat {scanned:,} rânduri, găsite {len(collected)} puzzle-uri...")

            if scanned > MAX_SCAN:
                print(f"Limită de scanare ({MAX_SCAN:,}) atinsă.")
                break

            if len(row) < 8:
                continue

            puzzle_id = row[0]
            fen       = row[1]
            moves     = row[2]
            try:
                rating  = int(row[3])
                pop     = int(row[5])
            except ValueError:
                continue

            themes = row[7].split()

            # Filtre
            if 'mateIn1' not in themes:
                continue
            if not (RATING_MIN <= rating <= RATING_MAX):
                continue
            if pop < MIN_POP:
                continue

            moves_list = moves.strip().split()
            if len(moves_list) < 2:
                continue

            # Aplică prima mutare (mutarea adversarului) → poziția puzzle-ului
            try:
                puzzle_fen = apply_uci_move(fen, moves_list[0])
            except Exception as e:
                continue

            solution_uci = moves_list[1]   # mutarea care dă mat

            collected.append({
                'id':     puzzle_id,
                'fen':    puzzle_fen,
                'sol':    solution_uci,
                'rating': rating,
            })

            if len(collected) >= TARGET * 3:
                print(f"Am strâns destule ({len(collected)}), opresc download-ul.")
                break

    print(f"\nTotal scanate: {scanned:,} | Eligibile: {len(collected)}")

    if not collected:
        print("Nu s-au găsit puzzle-uri! Încearcă să lărgești filtrele RATING_MIN/MAX.")
        return []

    # Amestecăm și luăm TARGET-ul
    random.shuffle(collected)
    selected = collected[:TARGET]
    selected.sort(key=lambda x: x['rating'])   # ordine crescătoare dificultate

    return selected


def export_js(puzzles, out_file='mate1_puzzles.js'):
    lines = ['const MATE1_PUZZLES = [']
    for p in puzzles:
        lines.append(f"  {{ fen: '{p['fen']}', sol: '{p['sol']}' }},  // #{p['id']} ~{p['rating']}")
    lines.append('];')
    js = '\n'.join(lines)

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(js)

    print(f"\nExportat {len(puzzles)} puzzle-uri în '{out_file}'")
    print("Lipește conținutul fișierului în mat1.html (înlocuiește array-ul PUZZLES existent).")
    print("\nPrimele 3 puzzle-uri:")
    for p in puzzles[:3]:
        print(f"  FEN: {p['fen']}")
        print(f"  Sol: {p['sol']}  (rating: {p['rating']})\n")


if __name__ == '__main__':
    puzzles = fetch_puzzles()
    if puzzles:
        export_js(puzzles)
