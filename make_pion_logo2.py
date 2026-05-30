# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

src = r"C:\Users\irina\Downloads\Gemini_Generated_Image_a0ohaga0ohaga0oh (1).png"
img = Image.open(src).convert("RGBA")
arr = np.array(img, dtype=np.float32)

r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
lum = (r + g + b) / 3.0
sat = np.maximum(np.maximum(r,g),b) - np.minimum(np.minimum(r,g),b)

# Fundal = crem deschis: luminozitate mare + saturatie mica
bg_mask = (lum > 210) & (sat < 35)

alpha = np.where(bg_mask, 0.0, 255.0)

# Zona de tranzitie la margini
edge = (sat >= 8) & (sat < 35) & (lum > 170) & (lum <= 210)
alpha = np.where(edge, np.clip((sat - 8) / 27.0 * 255.0, 0, 255), alpha)

out = arr.copy()
out[:,:,3] = alpha.astype(np.uint8)
pion = Image.fromarray(out.astype(np.uint8), 'RGBA')

# Crop la bounding box
fg = alpha > 30
rows = np.where(fg.max(axis=1))[0]
cols = np.where(fg.max(axis=0))[0]
pad = 30
pion = pion.crop((max(0,cols[0]-pad), max(0,rows[0]-pad),
                  min(img.width,cols[-1]+pad), min(img.height,rows[-1]+pad)))

# Patrат centrat
sz = max(pion.width, pion.height)
sq = Image.new("RGBA", (sz,sz), (0,0,0,0))
sq.paste(pion, ((sz-pion.width)//2, (sz-pion.height)//2), pion)

# Salveaza versiunea portocalie (300px pentru logo pagina)
logo_orange = sq.resize((300,300), Image.LANCZOS)
logo_orange.save(r"C:\Users\irina\SahMatAnimat\img\pion-logo-orange.png")
print("Salvat: pion-logo-orange.png")

# Versiunea navy: recoloreaza pixelii portocalii in #1a3a6b
arr2 = np.array(sq, dtype=np.float32)
r2,g2,b2,a2 = arr2[:,:,0],arr2[:,:,1],arr2[:,:,2],arr2[:,:,3]

# Pixelii vizibili si non-albi = corpul portocaliu al pionului
pion_body = (a2 > 30) & ~((r2 > 230) & (g2 > 230) & (b2 > 230))

arr_navy = arr2.copy()
arr_navy[:,:,0] = np.where(pion_body, 26.0,  arr2[:,:,0])   # R = 26
arr_navy[:,:,1] = np.where(pion_body, 58.0,  arr2[:,:,1])   # G = 58
arr_navy[:,:,2] = np.where(pion_body, 107.0, arr2[:,:,2])   # B = 107

logo_navy = Image.fromarray(arr_navy.astype(np.uint8), 'RGBA')
logo_navy = logo_navy.resize((300,300), Image.LANCZOS)
logo_navy.save(r"C:\Users\irina\SahMatAnimat\img\pion-logo-navy.png")
print("Salvat: pion-logo-navy.png")

print("GATA")
