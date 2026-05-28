import json, csv

candidates = json.load(open('data/dovetail_candidates.json', encoding='utf-8'))
id_to_candidate = {p['id'].replace('li-', ''): p for p in candidates}

print(f"Candidati: {len(id_to_candidate)}")
print("Caut popularitate in CSV...")

enriched = []
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row['PuzzleId']
        if pid in id_to_candidate:
            p = id_to_candidate[pid].copy()
            p['nbPlays'] = int(row['NbPlays'])
            enriched.append(p)

print(f"Imbogatiti: {len(enriched)}")

by_level = {1: [], 2: [], 3: []}
for p in enriched:
    by_level[p['level']].append(p)

for lv in (1, 2, 3):
    by_level[lv].sort(key=lambda x: x['nbPlays'], reverse=True)
    print(f"  Nivel {lv}: {len(by_level[lv])} candidati, top nbPlays={by_level[lv][0]['nbPlays'] if by_level[lv] else 0}")

selected = by_level[1][:15] + by_level[2][:15] + by_level[3][:10]
for p in selected:
    p.pop('nbPlays', None)

print(f"\nTotal selectate: {len(selected)}")

with open('data/dovetail_top40.json', 'w', encoding='utf-8') as f:
    json.dump(selected, f, ensure_ascii=False, indent=2)
print("Salvat in data/dovetail_top40.json")
