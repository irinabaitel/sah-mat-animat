import csv

themes = {}
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        col = row.get('Themes') or row.get('themes') or ''
        for t in col.split():
            themes[t] = themes.get(t, 0) + 1

keywords = ['attr', 'decoy', 'lure', 'bait', 'attract']
found = [(v, k) for k, v in themes.items()
         if any(kw in k.lower() for kw in keywords)]
found.sort(reverse=True)
print("Teme gasite:", found if found else "NICIUNA")
print()
print("Top 30 teme in baza de date:")
top = sorted(themes.items(), key=lambda x: -x[1])[:30]
for k, v in top:
    print(f"  {v:7d}  {k}")
