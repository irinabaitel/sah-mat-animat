# -*- coding: utf-8 -*-
"""Randeaza pagini din manualele Step (PDF-uri scanate) ca imagini lizibile.

Manualele Step sunt scanate cu JBIG2, pe care pypdf nu-l poate decoda.
PyMuPDF are decodor propriu, deci merge.

Utilizare:
    python tools/steprender.py "Metoda step - manualul profesorului/step 3 m.pdf" 57
    python tools/steprender.py "...step 3 m.pdf" 57 --zoom 0.55 0.29 0.90 0.55
                                                        (x1   y1   x2   y2, fractii din pagina)
Iese un PNG in scratchpad, pe care il pot citi ca imagine.

ATENTIE la diagramele Step: multe sunt IMPARTITE in doua — o rama de 8x8
contine doua pozitii separate, stanga (coloanele a-d) si dreapta (e-h).
Sunt fragmente: de multe ori lipseste un rege. Ca sa le folosesti,
completeaza pozitia si verific-o cu motorul.
"""
import sys, os
import pymupdf

def main():
    pdf = sys.argv[1]
    page = int(sys.argv[2]) - 1
    dpi = 200
    clip = None
    if '--zoom' in sys.argv:
        i = sys.argv.index('--zoom')
        x1, y1, x2, y2 = (float(v) for v in sys.argv[i+1:i+5])
        dpi = 400
    d = pymupdf.open(pdf)
    p = d[page]
    r = p.rect
    if '--zoom' in sys.argv:
        clip = pymupdf.Rect(r.width*x1, r.height*y1, r.width*x2, r.height*y2)
    pix = p.get_pixmap(dpi=dpi, clip=clip)
    out = os.environ.get('SCRATCH', '.') + f"/step_p{page+1}.png"
    pix.save(out)
    print(out, pix.width, 'x', pix.height)

if __name__ == '__main__':
    main()
