# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

src = r"C:\Users\irina\Downloads\Gemini_Generated_Image_92ohfn92ohfn92oh.png"
img = Image.open(src).convert("RGBA")
arr = np.array(img, dtype=np.float32)

# Acopera steaua Gemini din coltul dreapta-jos cu culoarea fundalului navy
h, w = arr.shape[:2]
bg_color = arr[10, 10, :3]  # culoarea fundalului navy din colt stanga-sus
patch = int(min(h, w) * 0.09)
arr[h-patch:h, w-patch:w, :3] = bg_color

r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

# Fundal = navy inchis: b > r, luminozitate mica
lum = (r + g + b) / 3.0
bg_mask = (lum < 130) & (b > r)

# Zona de tranzitie la margini
sat = np.maximum(np.maximum(r,g),b) - np.minimum(np.minimum(r,g),b)
edge = (lum >= 100) & (lum < 170) & (b > r)
alpha_edge = np.clip((lum - 100) / 70.0 * 255.0, 0, 255)

alpha = np.where(bg_mask, 0.0, 255.0)
alpha = np.where(edge, alpha_edge, alpha)

out = arr.copy()
out[:,:,3] = alpha.astype(np.uint8)
pion = Image.fromarray(out.astype(np.uint8), 'RGBA')

# Crop la bounding box al pionului
fg = alpha > 30
rows = np.where(fg.max(axis=1))[0]
cols = np.where(fg.max(axis=0))[0]
pad = 20
pion = pion.crop((max(0,cols[0]-pad), max(0,rows[0]-pad),
                  min(img.width,cols[-1]+pad), min(img.height,rows[-1]+pad)))

# Patrat centrat
sz = max(pion.width, pion.height)
sq = Image.new("RGBA", (sz,sz), (0,0,0,0))
sq.paste(pion, ((sz-pion.width)//2, (sz-pion.height)//2), pion)

# Versiune 300px pentru logo pagina (crem pe transparent)
logo = sq.resize((300,300), Image.LANCZOS)
logo.save(r"C:\Users\irina\SahMatAnimat\img\pion-logo.png")
print("Salvat: pion-logo.png (crem pe transparent)")

# Versiune navy (recoloreaza crem -> navy)
arr2 = np.array(sq, dtype=np.float32)
r2,g2,b2,a2 = arr2[:,:,0],arr2[:,:,1],arr2[:,:,2],arr2[:,:,3]
body = (a2 > 30)
arr_navy = arr2.copy()
arr_navy[:,:,0] = np.where(body, 26.0,  0)
arr_navy[:,:,1] = np.where(body, 58.0,  0)
arr_navy[:,:,2] = np.where(body, 107.0, 0)
logo_navy = Image.fromarray(arr_navy.astype(np.uint8),'RGBA').resize((300,300),Image.LANCZOS)
logo_navy.save(r"C:\Users\irina\SahMatAnimat\img\pion-logo-navy.png")
print("Salvat: pion-logo-navy.png (navy pe transparent)")

# Versiune alba
arr_white = arr2.copy()
arr_white[:,:,0] = np.where(body, 255.0, 0)
arr_white[:,:,1] = np.where(body, 255.0, 0)
arr_white[:,:,2] = np.where(body, 255.0, 0)
logo_white = Image.fromarray(arr_white.astype(np.uint8),'RGBA').resize((300,300),Image.LANCZOS)
logo_white.save(r"C:\Users\irina\SahMatAnimat\img\pion-logo-white.png")
print("Salvat: pion-logo-white.png (alb pe transparent)")

print("GATA")
