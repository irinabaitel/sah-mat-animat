#!/usr/bin/env python3
"""
Fetch 50 mate-in-2 puzzles from Lichess API and write to mat2_puzzles.json
"""

import urllib.request
import json
import time
import random

OUTPUT_FILE = r"C:\Users\irina\SahMatAnimat\mat2_puzzles.json"
TARGET = 50

puzzles = []
attempts = 0
max_attempts = 800

headers = {
    "User-Agent": "SahMatAnimat/1.0 (educational chess app; contact: irinabaitel@gmail.com)",
    "Accept": "application/json",
}

def fetch_url(url, retries=5):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 + attempt * 5 + random.uniform(0, 3)
                print(f"  Rate limited, waiting {wait:.1f}s...")
                time.sleep(wait)
            elif e.code in (500, 502, 503, 504):
                wait = 5 + attempt * 3
                print(f"  Server error {e.code}, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  HTTP error {e.code} for {url}")
                return None
        except Exception as ex:
            wait = 3 + attempt * 2
            print(f"  Error: {ex}, waiting {wait}s...")
            time.sleep(wait)
    return None

print(f"Starting fetch of {TARGET} mate-in-2 puzzles from Lichess...")
print()

while len(puzzles) < TARGET and attempts < max_attempts:
    attempts += 1

    # Fetch next puzzle
    data = fetch_url("https://lichess.org/api/puzzle/next")

    if data is None:
        time.sleep(2)
        continue

    puz = data.get("puzzle", {})
    themes = puz.get("themes", [])
    solution = puz.get("solution", [])
    pid = puz.get("id", "")

    # Check mateIn2 criteria
    is_mate2 = "mateIn2" in themes and len(solution) == 3

    status = "MATE2!" if is_mate2 else f"skip ({','.join(themes[:2])})"
    print(f"[{attempts:3d}] puzzle/{pid} sol={len(solution)} -> {status} | collected: {len(puzzles)}/{TARGET}")

    if is_mate2:
        # Get FEN from the puzzle detail endpoint
        detail = fetch_url(f"https://lichess.org/api/puzzle/{pid}")
        if detail:
            fen = detail.get("puzzle", {}).get("fen", puz.get("fen", ""))
            sol = detail.get("puzzle", {}).get("solution", solution)
            turn = "w" if " w " in fen else "b"
            entry = {"fen": fen, "sol": sol, "turn": turn}
            puzzles.append(entry)
            print(f"       -> Added! FEN: {fen[:50]}... turn={turn}")
            time.sleep(1.5)
        else:
            print(f"       -> Could not get detail for {pid}, skipping")

    # Rate limiting: be polite to the API
    time.sleep(1.2 + random.uniform(0, 0.5))

print()
print(f"Done! Collected {len(puzzles)} puzzles in {attempts} attempts.")

if len(puzzles) >= TARGET:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(puzzles[:TARGET], f, indent=2)
    print(f"Written to: {OUTPUT_FILE}")
else:
    print(f"WARNING: Only collected {len(puzzles)}/{TARGET} puzzles!")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2)
    print(f"Partial results written to: {OUTPUT_FILE}")
