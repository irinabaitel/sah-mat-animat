import pymupdf, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
# usage: crop.py pdf pageno(1-based) outprefix
pdf, pg, pref = sys.argv[1], int(sys.argv[2]), sys.argv[3]
d = pymupdf.open(pdf)
pix = d[pg-1].get_pixmap(dpi=220)
img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
g = np.array(img.convert('L')) < 110  # dark pixels
H, W = g.shape
# find board frames: long dark horizontal / vertical lines
rows = np.where(g.sum(1) > W*0.15)[0]
cols = np.where(g.sum(0) > H*0.10)[0]
def groups(a):
    out=[]; 
    for v in a:
        if out and v-out[-1][-1] <= 3: out[-1].append(v)
        else: out.append([v])
    return [int(np.mean(x)) for x in out]
print('rows', groups(rows)); print('cols', groups(cols))
