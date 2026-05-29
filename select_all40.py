import json, csv

names = ['epaulette','pawn_mate','greco','blackburne','reti','legal','killbox','hook','vukovic','maxlange']

id_maps = {}
for name in names:
    try:
        candidates = json.load(open(f'data/{name}_candidates.json', encoding='utf-8'))
        id_maps[name] = {p['id'].replace('li-', ''): p for p in candidates}
    except FileNotFoundError:
        print(f"LIPSA: data/{name}_candidates.json")
        id_maps[name] = {}

enriched = {name: [] for name in names}

print("Imbogatesc cu NbPlays din CSV...")
with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row['PuzzleId']
        for name in names:
            if pid in id_maps[name]:
                p = id_maps[name][pid].copy()
                p['nbPlays'] = int(row['NbPlays'])
                enriched[name].append(p)

print("\n=== REZULTATE SELECTIE ===")
for name in names:
    by_level = {1: [], 2: [], 3: []}
    for p in enriched[name]:
        by_level[p['level']].append(p)
    for lv in (1, 2, 3):
        by_level[lv].sort(key=lambda x: x['nbPlays'], reverse=True)
    selected = by_level[1][:15] + by_level[2][:15] + by_level[3][:10]
    for p in selected:
        p.pop('nbPlays', None)
    lvl_counts = f"n1={len(by_level[1])} n2={len(by_level[2])} n3={len(by_level[3])}"
    print(f"  {name:12s}: {len(enriched[name]):7,} candidati ({lvl_counts}) -> {len(selected)} selectate")
    with open(f'data/{name}_top40.json', 'w', encoding='utf-8') as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)

print("\nSalvat toate in data/")
