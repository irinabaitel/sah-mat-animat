"""
Procesează chessable_33908_raw.json → chessable_33908_puzzles.json
Grupează cele 250 de puzzle-uri pe teme de mat.

Rulare: python process_chessable.py
Necesar: data/chessable_33908_raw.json (generat de scriptul din console_test.txt)
"""

import json
import re
from collections import defaultdict

INPUT  = "data/chessable_33908_raw.json"
OUTPUT = "data/chessable_33908_puzzles.json"

# Teme canonice + alias-urile lor — ordinea contează: mai specific primul
THEME_ALIASES = {
    "Damiano's Bishop Mate":  ["damiano's bishop", "damiano bishop"],
    "Damiano's Mate":         ["damiano's mate", "damiano mate"],
    "Double Bishops Mate":    ["double bishops", "two bishops"],
    "Double Knights Mate":    ["double knights", "two knights"],
    "Swallow's Tail Mate":    ["swallow's tail", "swallow tail", "guéridon", "guerridon"],
    "Dovetail Mate":          ["dovetail"],
    "David & Goliath Mate":   ["david and goliath", "david & goliath", "david&goliath", "pawn mate"],
    "Smothered Mate":         ["smothered"],
    "Fool's Mate":            ["fool's mate", "fools mate"],
    "Back Rank Mate":         ["back rank"],
    "Blackburne's Mate":      ["blackburne"],
    "Legal's Mate":           ["legal"],
    "Lolli's Mate":           ["lolli"],
    "Boden's Mate":           ["boden"],
    "Pillsbury's Mate":       ["pillsbury"],
    "Suffocation Mate":       ["suffocation"],
    "Morphy's Mate":          ["morphy"],
    "Opera Mate":             ["opera mate", "mayet"],
    "Greco's Mate":           ["greco"],
    "Anastasia's Mate":       ["anastasia"],
    "Arabian Mate":           ["arabian"],
    "Blind Swine Mate":       ["blind swine"],
    "Réti's Mate":            ["réti", "reti"],
    "Corner Mate":            ["corner mate"],
    "Hook Mate":              ["hook mate"],
    "Epaulette Mate":         ["epaulette"],
    "Anderssen's Mate":       ["anderssen"],
    "Lawnmower Mate":         ["lawnmower"],
    "Box Mate":               ["box mate"],
    "Balestra Mate":          ["balestra"],
    "Triangle Mate":          ["triangle mate"],
    "Max Lange's Mate":       ["max lange"],
    "Vuković's Mate":         ["vuković", "vukovic"],
}

def extract_theme(last_comment: str) -> str:
    if not last_comment:
        return "Unknown"
    text = last_comment.lower()
    for canonical, aliases in THEME_ALIASES.items():
        for alias in aliases:
            if alias.lower() in text:
                return canonical
    # fallback: primul propoziție din comment
    m = re.match(r'^([^.!?\n]{3,120}[.!?])', last_comment.strip())
    if m:
        return m.group(1).strip()
    return last_comment[:80].strip()

def main():
    with open(INPUT, encoding="utf-8-sig") as f:
        raw = json.load(f)

    by_theme: dict[str, list] = defaultdict(list)
    errors = []

    for p in raw:
        if "error" in p:
            errors.append(p)
            continue
        theme = extract_theme(p.get("last_comment", ""))
        by_theme[theme].append({
            "oid":         p["oid"],
            "chapter":     p["chapter"],
            "initial_fen": p.get("initial_fen", ""),
            "color":       p.get("color", "white"),
            "moves":       p.get("moves", []),
            "comment":     p.get("last_comment", ""),
        })

    result = {
        "total":   len(raw) - len(errors),
        "errors":  len(errors),
        "themes":  {
            theme: {"count": len(pzls), "puzzles": pzls}
            for theme, pzls in sorted(by_theme.items())
        },
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Gata! {result['total']} puzzle-uri în {len(by_theme)} teme:")
    for theme, pzls in sorted(by_theme.items(), key=lambda x: -len(x[1])):
        print(f"  {len(pzls):>3}  {theme}")
    if errors:
        print(f"\n{len(errors)} erori:")
        for e in errors:
            print(f"  oid={e['oid']}: {e.get('error', '?')}")

if __name__ == "__main__":
    main()
