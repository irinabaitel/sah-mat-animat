"""
Scanează CSV-ul Lichess o singură dată și filtrează simultan toate cele 10 tipare de mat.
Salvează câte un fișier candidates JSON pentru fiecare.
"""

import chess, csv, json, os

os.makedirs('data', exist_ok=True)

def rating_to_level(r):
    if r < 1500: return 1
    if r < 1900: return 2
    return 3

# ── 1. Epaulette Mate (Matul cu epoleți) ──────────────────────────────────────
def is_epaulette(board):
    if not board.is_checkmate(): return False
    mated = board.turn
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    if board.piece_at(csq).piece_type != chess.QUEEN: return False
    ksq = board.king(mated)
    kf, kr = chess.square_file(ksq), chess.square_rank(ksq)
    qf, qr = chess.square_file(csq),  chess.square_rank(csq)
    if qf == kf:   # șah pe coloană → aripi stânga/dreapta
        arms = [(kf-1, kr), (kf+1, kr)]
    elif qr == kr: # șah pe rând → aripi sus/jos
        arms = [(kf, kr-1), (kf, kr+1)]
    else:
        return False
    def own(f, r):
        if not (0 <= f <= 7 and 0 <= r <= 7): return False
        p = board.piece_at(chess.square(f, r))
        return p is not None and p.color == mated
    return own(*arms[0]) and own(*arms[1])

# ── 2. Pawn Mate (Matul cu pionii) ────────────────────────────────────────────
def is_pawn_mate(board):
    if not board.is_checkmate(): return False
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    return board.piece_at(checkers[0]).piece_type == chess.PAWN

# ── 3. Greco's Mate (Matul lui Greco) ─────────────────────────────────────────
# Nebunul dă mat diagonal, cu formula "aripi" identică Dovetail dar checker=BISHOP
def is_greco(board):
    if not board.is_checkmate(): return False
    mated = board.turn
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    if board.piece_at(csq).piece_type != chess.BISHOP: return False
    ksq = board.king(mated)
    kf, kr = chess.square_file(ksq), chess.square_rank(ksq)
    qf, qr = chess.square_file(csq),  chess.square_rank(csq)
    df, dr = qf - kf, qr - kr
    if abs(df) != abs(dr): return False  # trebuie să fie diagonal
    if abs(df) == 0: return False
    norm_df = df // abs(df)
    norm_dr = dr // abs(dr)
    a1f, a1r = kf - norm_df, kr
    a2f, a2r = kf,           kr - norm_dr
    if not (0 <= a1f <= 7 and 0 <= a1r <= 7): return False
    if not (0 <= a2f <= 7 and 0 <= a2r <= 7): return False
    def own_non_k(f, r):
        p = board.piece_at(chess.square(f, r))
        return p is not None and p.color == mated and p.piece_type != chess.KNIGHT
    return own_non_k(a1f, a1r) and own_non_k(a2f, a2r)

# ── 4. Blackburne's Mate (Matul lui Blackburne) ───────────────────────────────
# Nebunul dă mat, iar cel puțin un cal al mătuitoarei controlează câmpuri cheie
def is_blackburne(board):
    if not board.is_checkmate(): return False
    mated  = board.turn
    mating = not mated
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    if board.piece_at(csq).piece_type != chess.BISHOP: return False
    ksq = board.king(mated)
    # Cel puțin un cal al mătuitoarei atacă câmpuri adiacente regelui matat
    king_adj = chess.SquareSet(chess.BB_KING_ATTACKS[ksq])
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p and p.color == mating and p.piece_type == chess.KNIGHT:
            if board.attacks(sq) & king_adj:
                return True
    return False

# ── 5. Réti's Mate (Matul lui Réti) ──────────────────────────────────────────
# Nebunul dă mat de la distanță (>1 câmp), turnul mătuitoarei pe aceeași coloană/rând cu regele
def is_reti(board):
    if not board.is_checkmate(): return False
    mated  = board.turn
    mating = not mated
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    if board.piece_at(csq).piece_type != chess.BISHOP: return False
    ksq = board.king(mated)
    kf, kr = chess.square_file(ksq), chess.square_rank(ksq)
    bf, br = chess.square_file(csq),  chess.square_rank(csq)
    dist = max(abs(bf - kf), abs(br - kr))
    if dist < 2: return False  # nebunul trebuie să fie la distanță
    # Turnul mătuitoarei pe aceeași coloană sau rând cu regele matat
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p and p.color == mating and p.piece_type == chess.ROOK:
            sf, sr = chess.square_file(sq), chess.square_rank(sq)
            if sf == kf or sr == kr:
                return True
    return False

# ── 6. Légal's Mate (Matul lui Légal) ────────────────────────────────────────
# Calul dă mat; nebunul mătuitoarei controlează cel puțin un câmp de fugă al regelui
def is_legal(board):
    if not board.is_checkmate(): return False
    mated  = board.turn
    mating = not mated
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    if board.piece_at(csq).piece_type != chess.KNIGHT: return False
    ksq = board.king(mated)
    king_adj = chess.SquareSet(chess.BB_KING_ATTACKS[ksq])
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p and p.color == mating and p.piece_type == chess.BISHOP:
            if board.attacks(sq) & king_adj:
                return True
    return False

# ── 7. Killbox ────────────────────────────────────────────────────────────────
# Regele pe margine/colț, cel puțin 2 câmpuri de fugă blocate de piese proprii,
# dam sau turn dă mat
def is_killbox(board):
    if not board.is_checkmate(): return False
    mated = board.turn
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    ct = board.piece_at(csq).piece_type
    if ct not in (chess.QUEEN, chess.ROOK): return False
    ksq = board.king(mated)
    kf, kr = chess.square_file(ksq), chess.square_rank(ksq)
    if not (kf == 0 or kf == 7 or kr == 0 or kr == 7): return False  # pe margine
    king_adj = chess.SquareSet(chess.BB_KING_ATTACKS[ksq])
    own_blockers = sum(
        1 for sq in king_adj
        if (p := board.piece_at(sq)) and p.color == mated
    )
    return own_blockers >= 2

# ── 8. Hook Mate / Matul triunghi ────────────────────────────────────────────
# Calul dă mat, turnul mătuitoarei adiacent calului, pion propriu blochează o cale
def is_hook(board):
    if not board.is_checkmate(): return False
    mated  = board.turn
    mating = not mated
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    if board.piece_at(csq).piece_type != chess.KNIGHT: return False
    ksq = board.king(mated)
    king_adj = chess.SquareSet(chess.BB_KING_ATTACKS[ksq])
    # Turnul mătuitoarei adiacent regelui
    has_rook_adj = any(
        (p := board.piece_at(sq)) and p.color == mating and p.piece_type == chess.ROOK
        for sq in king_adj
    )
    if not has_rook_adj: return False
    # Pion propriu (al regelui matat) blochează cel puțin un câmp de fugă
    has_own_pawn = any(
        (p := board.piece_at(sq)) and p.color == mated and p.piece_type == chess.PAWN
        for sq in king_adj
    )
    return has_own_pawn

# ── 9. Vuković's Mate (Matul lui Vuković) ────────────────────────────────────
# Dama dă mat diagonal (ca Dovetail), turnul mătuitoarei pe aceeași coloană/rând cu regele
def is_vukovic(board):
    if not board.is_checkmate(): return False
    mated  = board.turn
    mating = not mated
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    if board.piece_at(csq).piece_type != chess.QUEEN: return False
    ksq = board.king(mated)
    kf, kr = chess.square_file(ksq), chess.square_rank(ksq)
    qf, qr = chess.square_file(csq),  chess.square_rank(csq)
    df, dr = qf - kf, qr - kr
    if abs(df) != 1 or abs(dr) != 1: return False  # diagonal adiacent
    # Turnul mătuitoarei pe aceeași coloană sau rând cu regele matat
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p and p.color == mating and p.piece_type == chess.ROOK:
            sf, sr = chess.square_file(sq), chess.square_rank(sq)
            if sf == kf or sr == kr:
                return True
    return False

# ── 10. Max Lange's Mate (Matul lui Max Lange) ───────────────────────────────
# Nebunul dă mat adiacent (1 câmp diagonal), turn și cal ale mătuitoarei prezente
def is_maxlange(board):
    if not board.is_checkmate(): return False
    mated  = board.turn
    mating = not mated
    checkers = list(board.checkers())
    if len(checkers) != 1: return False
    csq = checkers[0]
    if board.piece_at(csq).piece_type != chess.BISHOP: return False
    ksq = board.king(mated)
    kf, kr = chess.square_file(ksq), chess.square_rank(ksq)
    bf, br = chess.square_file(csq),  chess.square_rank(csq)
    if max(abs(bf - kf), abs(br - kr)) != 1: return False  # adiacent
    has_rook   = any(board.piece_at(sq) and board.piece_at(sq).color == mating
                     and board.piece_at(sq).piece_type == chess.ROOK for sq in chess.SQUARES)
    has_knight = any(board.piece_at(sq) and board.piece_at(sq).color == mating
                     and board.piece_at(sq).piece_type == chess.KNIGHT for sq in chess.SQUARES)
    return has_rook and has_knight

# ── Scanare ──────────────────────────────────────────────────────────────────

filters = [
    ('epaulette',  is_epaulette),
    ('pawn_mate',  is_pawn_mate),
    ('greco',      is_greco),
    ('blackburne', is_blackburne),
    ('reti',       is_reti),
    ('legal',      is_legal),
    ('killbox',    is_killbox),
    ('hook',       is_hook),
    ('vukovic',    is_vukovic),
    ('maxlange',   is_maxlange),
]

results = {name: [] for name, _ in filters}
checked = 0
counts  = {name: 0 for name, _ in filters}

print("Scanez toate cele 10 tipare simultan...")

with open('lichess_db_puzzle.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'mate' not in row['Themes'].lower():
            continue
        checked += 1
        if checked % 100000 == 0:
            summary = ' | '.join(f"{n}:{counts[n]}" for n, _ in filters)
            print(f"  {checked:,} verificate — {summary}")
        try:
            moves = row['Moves'].split()
            board = chess.Board(row['FEN'])
            for mv in moves:
                board.push_uci(mv)
            entry = {
                "id":      f"li-{row['PuzzleId']}",
                "fen":     row['FEN'],
                "moves":   moves,
                "level":   rating_to_level(int(row['Rating'])),
                "gameUrl": f"https://lichess.org/training/{row['PuzzleId']}"
            }
            for name, fn in filters:
                if fn(board):
                    results[name].append(entry)
                    counts[name] += 1
        except Exception:
            continue

print("\n=== REZULTATE FINALE ===")
for name, _ in filters:
    print(f"  {name}: {counts[name]} candidati")
    with open(f'data/{name}_candidates.json', 'w', encoding='utf-8') as f:
        json.dump(results[name], f, ensure_ascii=False, indent=2)

print("\nSalvat toate in data/")
