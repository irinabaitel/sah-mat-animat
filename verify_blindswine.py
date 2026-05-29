"""
Verificare candidati blind swine cu chess.js + selectie 40 puzzle-uri.
Niveluri: 0-13 usor (rating<1300), 14-27 mediu (1300-1700), 28-39 avansat (>1700)
"""

import csv, subprocess, json, random

CHESS_JS_PATH = r'C:\tmp\chess.js'
chess_js_code = open(CHESS_JS_PATH).read()

def verify_batch(puzzles):
    js_puzzles = json.dumps(puzzles)
    script = chess_js_code + """
const puzzles = """ + js_puzzles + """;
const results = [];
for (const p of puzzles) {
    try {
        const c = new Chess(p.fen);
        const sol = p.sol.split(' ');
        let ok = true, firstCheck = false, lastMate = false;
        for (let i = 0; i < sol.length; i++) {
            const uci = sol[i];
            const mv = c.move({ from: uci.slice(0,2), to: uci.slice(2,4), promotion: uci[4] || 'q' });
            if (!mv) { ok = false; break; }
            if (i === 0 && (mv.san.includes('+') || mv.san.includes('#'))) firstCheck = true;
            if (i === sol.length - 1 && mv.san.includes('#')) lastMate = true;
        }
        results.push({ id: p.id, ok: ok && firstCheck && lastMate });
    } catch(e) {
        results.push({ id: p.id, ok: false });
    }
}
console.log(JSON.stringify(results));
"""
    try:
        r = subprocess.run(['node', '-e', script], capture_output=True, text=True, timeout=60)
        if r.stdout.strip():
            return json.loads(r.stdout.strip())
        return [{'id': p['id'], 'ok': False} for p in puzzles]
    except Exception as e:
        print(f"  Eroare batch: {e}")
        return [{'id': p['id'], 'ok': False} for p in puzzles]

# Citeste toti candidatii
all_puzzles = []
with open('blindswine_candidates.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_puzzles.append({
            'id':      row['id'],
            'fen':     row['fen'],
            'sol':     row['sol'],
            'turn':    row['turn'],
            'rating':  int(row['rating']),
            'n_moves': int(row['n_moves']),
        })

all_puzzles.sort(key=lambda x: x['rating'])
print(f"Total candidati: {len(all_puzzles)}")

# Grupare pe niveluri
usor    = [p for p in all_puzzles if p['rating'] < 1300 and p['n_moves'] == 3]
mediu   = [p for p in all_puzzles if 1300 <= p['rating'] < 1700 and p['n_moves'] == 3]
avansat = [p for p in all_puzzles if p['rating'] >= 1700 and p['n_moves'] == 3]
print(f"Usor 3mut: {len(usor)}, Mediu 3mut: {len(mediu)}, Avansat 3mut: {len(avansat)}")

# Esantion distribuit din fiecare grup (max 120 per grup)
def sample_distributed(lst, n):
    if len(lst) <= n: return lst[:]
    step = len(lst) / n
    return [lst[int(i * step)] for i in range(n)]

sample = (sample_distributed(usor, 120) +
          sample_distributed(mediu, 120) +
          sample_distributed(avansat, 120))
print(f"Esantion de verificat: {len(sample)}")

# Verifica in batch-uri de 50
valid = []
BATCH = 50
for start in range(0, len(sample), BATCH):
    batch = sample[start:start+BATCH]
    res = verify_batch(batch)
    id_map = {r['id']: r['ok'] for r in res}
    for p in batch:
        if id_map.get(p['id'], False):
            valid.append(p)
    print(f"  {start+len(batch)}/{len(sample)} verificate, {len(valid)} valide...", flush=True)

print(f"\nValide: {len(valid)}")
valid_usor    = [p for p in valid if p['rating'] < 1300]
valid_mediu   = [p for p in valid if 1300 <= p['rating'] < 1700]
valid_avansat = [p for p in valid if p['rating'] >= 1700]
print(f"Usor: {len(valid_usor)}, Mediu: {len(valid_mediu)}, Avansat: {len(valid_avansat)}")

# Selectie finala: 14 usor + 14 mediu + 12 avansat = 40
def pick_spread(lst, n):
    lst.sort(key=lambda x: x['rating'])
    if len(lst) <= n: return lst[:]
    step = len(lst) / n
    return [lst[int(i*step)] for i in range(n)]

final = (pick_spread(valid_usor, 14) +
         pick_spread(valid_mediu, 14) +
         pick_spread(valid_avansat, 12))
print(f"Selectate final: {len(final)}")

# Afisare JS array
print("\n/* PUZZLES */")
print("const PUZZLES=[")
for p in final:
    sol_arr = "['" + "','".join(p['sol'].split()) + "']"
    print(f"  {{id:'{p['id']}',fen:'{p['fen']}',sol:{sol_arr},turn:'{p['turn']}'}},  // rating {p['rating']}")
print("];")
print(f"\n// Total: {len(final)} puzzle-uri | Usor 0-13, Mediu 14-27, Avansat 28-39")
