# -*- coding: utf-8 -*-
"""Decodeaza diagramele din PDF-urile ChessKid (font de diagrame) in FEN."""
import re, sys, chess

# fiecare piesa are doua caractere: pe camp alb / pe camp negru
MAP = {
 'P':'P', ')':'P',   'R':'R', '$':'R',   'N':'N', 'H':'N',
 'B':'B', 'G':'B',   'Q':'Q', '!':'Q',   'K':'K', 'I':'K',
 'p':'p', '0':'p',   'r':'r', '4':'r',   'n':'n', 'h':'n',
 'b':'b', 'g':'b',   'q':'q', '1':'q',   'k':'k', 'i':'k',
 'w':'.', 'd':'.',   '*':'.', '+':'.',   ' ':'.',
}
RANKS = {'(':8, '7':7, '6':6, '5':5, '&':4, '3':3, '2':2, '%':1}

def diagrame(text):
    """intoarce lista de FEN-uri (fara latura la mutare) gasite in text"""
    out, cur = [], {}
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('cuuuuuuuu'):
            cur = {}
            continue
        if not line or line[0] not in RANKS:
            if cur and len(cur) == 8:
                out.append(cur); cur = {}
            continue
        rank = RANKS[line[0]]
        body = line[1:].split('}')[0]
        if len(body) != 8:
            continue
        cur[rank] = body
        if len(cur) == 8:
            out.append(cur); cur = {}
    fens = []
    for d in out:
        rows = []
        ok = True
        for r in range(8, 0, -1):
            row, empty = '', 0
            for ch in d[r]:
                p = MAP.get(ch)
                if p is None: ok = False; break
                if p == '.': empty += 1
                else:
                    if empty: row += str(empty); empty = 0
                    row += p
            if not ok: break
            if empty: row += str(empty)
            rows.append(row)
        if ok and len(rows) == 8:
            fens.append('/'.join(rows))
    return fens

if __name__ == '__main__':
    import pypdf
    r = pypdf.PdfReader(sys.argv[1])
    txt = '\n'.join((p.extract_text() or '') for p in r.pages)
    for i, board in enumerate(diagrame(txt), 1):
        for side in ('w', 'b'):
            f = f"{board} {side} - - 0 1"
            b = chess.Board(f)
            if b.is_valid():
                print(f"{i}|{f}")
                break
        else:
            print(f"{i}|NEVALID: {board}")
