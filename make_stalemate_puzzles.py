# -*- coding: utf-8 -*-
import sys; sys.stdout.reconfigure(encoding='utf-8')
"""
Generează data/stalemate_top25.json cu 25 puzzle-uri stalemate hand-crafted,
verificate cu python-chess.
"""
import json, os, io
import chess, chess.pgn

def verify(fen, moves):
    """Verifică că după secvența de mutări poziția finală este pat."""
    board = chess.Board(fen)
    for uci in moves:
        mv = chess.Move.from_uci(uci)
        if mv not in board.legal_moves:
            return False, f"Mutare ilegală: {uci} în {board.fen()}"
        board.push(mv)
    if board.is_stalemate():
        return True, "OK"
    return False, f"Nu e pat! {board.fen()}"

# moves[0] = setup (jucat automat), moves[1+] = solver, oponent, solver...
# Ultimul din moves trebuie să ducă la pat.
candidates = [

    # ═══ NIVEL 1 — pion pe coloana a sau h (pat clasic K+p) ═══

    # 1. Pionul negru pe a2; albul găsește Rc2 → pat
    {"id":"stale001","fen":"8/8/8/8/8/2K5/p7/1k6 b - - 0 1",
     "moves":["b1a1","c3c2"],"rating":600,"level":1},

    # 2. Pionul negru pe h2; albul găsește Rf1 → pat
    {"id":"stale002","fen":"8/8/8/8/8/8/5K1p/6k1 b - - 0 1",
     "moves":["g1h1","f2f1"],"rating":600,"level":1},

    # 3. Pionul negru pe a2; albul vine din b3 → Rb2
    {"id":"stale003","fen":"8/8/8/8/8/1K6/p7/1k6 b - - 0 1",
     "moves":["b1a1","b3b2"],"rating":650,"level":1},

    # 4. Pionul negru pe h2; albul vine din g3 → Rg2
    {"id":"stale004","fen":"8/8/8/8/8/6K1/7p/6k1 b - - 0 1",
     "moves":["g1h1","g3g2"],"rating":650,"level":1},

    # 5. a-pawn, rege negru vine la a1 din b2
    {"id":"stale005","fen":"8/8/8/8/8/3K4/p7/1k6 b - - 0 1",
     "moves":["b1a1","d3c2"],"rating":700,"level":1},

    # ═══ NIVEL 1 — pat cu dame (Q vs K+p) ═══

    # 6. Albul are D+R, joacă Da8 → pat la Ra1
    {"id":"stale006","fen":"8/8/8/8/8/2k5/8/qK6 b - - 0 1",
     "moves":["c3b3","b1a1"],"rating":750,"level":1},

    # 7. Clasic: Ra1 încolțit, oponentul joacă Db3 → stalemate direct
    # Albul e Ra1; negrul joacă Dc2? → setup; albul stă pe loc (deja pat?)
    # Pattern alternativ: rege negru forțează patul cu pierdere de damă
    {"id":"stale007","fen":"8/8/8/8/8/k7/8/K1q5 b - - 0 1",
     "moves":["c1c2","a1b1"],"rating":800,"level":1},

    # 8. Regele alb în colț a8; pionul negru promovează și dă pat
    {"id":"stale008","fen":"K7/2k5/8/8/8/8/p7/8 b - - 0 1",
     "moves":["c7b7","a8a7"],"rating":850,"level":1},

    # ═══ NIVEL 2 — sacrificiu de turn pentru pat ═══

    # 9. Turnul alb se sacrifică pe a3+, regele negru ia, albul e pat
    {"id":"stale009","fen":"8/R7/8/8/8/kq6/8/K7 b - - 0 1",
     "moves":["b3b2","a7a3","a3a3"],"rating":900,"level":2},

    # 10. Turn alb pe h1, pat după Th3+ Rxh3
    {"id":"stale010","fen":"8/8/8/8/8/7k/6q1/K6R b - - 0 1",
     "moves":["g2g1","h1h3","h3h3"],"rating":950,"level":2},

    # 11. Turn pe b8 se sacrifică: Tb1+ Rxb1 → pat la Ra1
    {"id":"stale011","fen":"1R6/8/8/8/8/kq6/8/K7 b - - 0 1",
     "moves":["b3c3","b8b1","c3b1"],"rating":1000,"level":2},

    # 12. Albul sacrifică turnul: Ta5+ Ra6 xa5 → pat
    {"id":"stale012","fen":"8/8/k7/8/8/8/1q6/KR6 b - - 0 1",
     "moves":["b2b3","b1b5","a6b5"],"rating":1000,"level":2},

    # ═══ NIVEL 2 — pat cu cal sau nebun ═══

    # 13. Calul negru dă pat regelui alb prins în colț
    {"id":"stale013","fen":"8/8/8/8/8/1k6/2n5/K7 b - - 0 1",
     "moves":["b3a3","a1a2"],"rating":1050,"level":2},

    # 14. Regele + nebun forțează patul
    {"id":"stale014","fen":"8/8/8/8/8/k7/1b6/K7 b - - 0 1",
     "moves":["a3a2","a1a1"],"rating":1100,"level":2},

    # ═══ NIVEL 2 — pion pe coloana b, d etc (mai dificil) ═══

    # 15. Pion negru pe b2; pat după manevrare rege
    {"id":"stale015","fen":"8/8/8/8/8/2K5/1p6/1k6 b - - 0 1",
     "moves":["b1a1","c3b2"],"rating":1100,"level":2},

    # 16. Pion negru pe g2; pat similar
    {"id":"stale016","fen":"8/8/8/8/8/5K2/6p1/6k1 b - - 0 1",
     "moves":["g1h1","f3g2"],"rating":1100,"level":2},

    # ═══ NIVEL 3 — secvențe mai lungi ═══

    # 17. 3 mutări: turn sacrificat, oponent ia, pat
    {"id":"stale017","fen":"8/8/8/8/8/kqr5/8/KR6 b - - 0 1",
     "moves":["c3c2","b1b3","c2b3"],"rating":1200,"level":3},

    # 18. Sacrificiu de damă pentru pat
    {"id":"stale018","fen":"8/8/8/8/1q6/k7/8/KQ6 b - - 0 1",
     "moves":["b4b2","b1b2","a3b2"],"rating":1200,"level":3},

    # 19
    {"id":"stale019","fen":"8/8/8/8/8/k7/q7/K1R5 b - - 0 1",
     "moves":["a2b2","c1c3","a3c3"],"rating":1250,"level":3},

    # 20
    {"id":"stale020","fen":"8/8/8/8/8/1k6/q7/KR6 b - - 0 1",
     "moves":["a2a3","b1b3","a3b3"],"rating":1300,"level":3},

    # 21
    {"id":"stale021","fen":"8/8/8/8/8/k1r5/8/KR6 b - - 0 1",
     "moves":["c3c2","b1b3","a3b3"],"rating":1300,"level":3},

    # 22
    {"id":"stale022","fen":"8/8/8/8/8/k7/2r5/KR6 b - - 0 1",
     "moves":["c2c3","b1b3","a3b3"],"rating":1350,"level":3},

    # 23
    {"id":"stale023","fen":"8/8/8/8/8/2k5/q7/K1R5 b - - 0 1",
     "moves":["a2b2","c1c3","c3c3"],"rating":1350,"level":3},

    # 24
    {"id":"stale024","fen":"8/8/8/8/8/k7/rq6/KR6 b - - 0 1",
     "moves":["b2b3","b1b3","a3b3"],"rating":1400,"level":3},

    # 25
    {"id":"stale025","fen":"8/8/8/8/8/1k6/rq6/KR6 b - - 0 1",
     "moves":["b2c2","b1b3","b3b3"],"rating":1400,"level":3},
]

valid = []
for c in candidates:
    ok, msg = verify(c["fen"], c["moves"])
    if ok:
        valid.append({
            "id":     c["id"],
            "fen":    c["fen"],
            "moves":  c["moves"],
            "rating": c["rating"],
            "level":  c["level"],
            "themes": ["stalemate"],
        })
        print(f"✓ {c['id']}")
    else:
        print(f"✗ {c['id']}: {msg}")

print(f"\nValide: {len(valid)}/25")
os.makedirs("data", exist_ok=True)
with open("data/stalemate_top25.json", "w", encoding="utf-8") as f:
    json.dump(valid, f, ensure_ascii=False, indent=1)
print("Salvat: data/stalemate_top25.json")
