# -*- coding: utf-8 -*-
"""Decodeaza diagramele din lectiile scrise ale lui Christiansen (folderul „NIvelul 1 pdf").

Sunt scrise cu fontul de diagrame tip ChessBase, care in text arata asa:

    XABCDEFGHY
    8-+-+-+-+(
    7+-+-+l+-'
    ...
    xabcdefghy

Reguli:
  -  si  +   = camp gol (alb, respectiv negru)
  litera singura      = piesa pe camp ALB
  prefix + litera     = piesa pe camp NEGRU (prefixele: m w t v s z)
  MAJUSCULA = alb, minuscula = negru
  K rege · Q dama · R turn · L nebun · N cal · P pion

Utilizare:
    python tools/cbdec.py "NIvelul 1 pdf/N1_04_Relatii_figuri(1).pdf"
"""
import re, sys

PIESE = {'K': 'K', 'Q': 'Q', 'R': 'R', 'L': 'B', 'N': 'N', 'P': 'P',
         'k': 'k', 'q': 'q', 'r': 'r', 'l': 'b', 'n': 'n', 'p': 'p'}
PREFIXE = set('mwtvsz')


def _rand(body):
    """un rand de 8 campuri -> lista de simboluri FEN sau None"""
    out, i = [], 0
    while i < len(body) and len(out) < 8:
        c = body[i]
        if c in '-+':
            out.append(None); i += 1
        elif c in PREFIXE and i + 1 < len(body) and body[i + 1] in PIESE:
            out.append(PIESE[body[i + 1]]); i += 2
        elif c in PIESE:
            out.append(PIESE[c]); i += 1
        else:
            i += 1
    return out if len(out) == 8 else None


def diagrame(text):
    """intoarce lista de pozitii (partea de piese din FEN)"""
    fenuri = []
    for bloc in re.findall(r'XABCDEFGHY([\s\S]*?)xabcdefghy', text):
        randuri = {}
        for linie in bloc.split('\n'):
            linie = linie.strip()
            m = re.match(r'^([1-8])(.*?)[(\'&%$#"!]\s*$', linie)
            if not m:
                continue
            r = _rand(m.group(2))
            if r:
                randuri[int(m.group(1))] = r
        if len(randuri) != 8:
            continue
        rows = []
        for nr in range(8, 0, -1):
            row, gol = '', 0
            for p in randuri[nr]:
                if p is None:
                    gol += 1
                else:
                    if gol:
                        row += str(gol); gol = 0
                    row += p
            if gol:
                row += str(gol)
            rows.append(row)
        fenuri.append('/'.join(rows))
    return fenuri


if __name__ == '__main__':
    import pypdf, chess
    r = pypdf.PdfReader(sys.argv[1])
    txt = '\n'.join((p.extract_text() or '') for p in r.pages)
    for i, poz in enumerate(diagrame(txt), 1):
        for latura in ('w', 'b'):
            f = poz + ' ' + latura + ' - - 0 1'
            if chess.Board(f).is_valid():
                print(f'{i}|{f}')
                break
        else:
            print(f'{i}|NEVALID: {poz}')
