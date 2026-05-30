# -*- coding: utf-8 -*-
from PIL import Image, ImageFilter
import numpy as np

src = r"C:\Users\irina\Downloads\Gemini_Generated_Image_huvnyihuvnyihuvn (1).png"
img = Image.open(src).convert("RGBA")
arr = np.array(img, dtype=np.float32)

r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

# fundal = gri/alb: R≈G≈B si luminozitate mare
saturation_range = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
luminosity = (r + g + b) / 3.0

# masca fundal: satura tie < 30 si luminozitate > 155
bg_mask = (saturation_range < 30) & (luminosity > 155)

# masca foreground: colorat SAU intunecat
fg_mask = ~bg_mask

# crop la bounding box al pionului
rows = np.where(fg_mask.max(axis=1))[0]
cols = np.where(fg_mask.max(axis=0))[0]
top, bottom = rows[0], rows[-1]
left, right = cols[0], cols[-1]
print(f"Pion bbox: {left},{top} -> {right},{bottom} ({right-left}x{bottom-top})")

# aplica transparenta
alpha_new = np.where(bg_mask, 0.0, 255.0)

# zona de tranzitie - smooth la margini (alpha partial bazat pe saturatie)
edge_zone = (saturation_range >= 10) & (saturation_range < 30) & (luminosity > 120) & (luminosity <= 155)
alpha_edge = np.clip((saturation_range - 10) / 20.0 * 255.0, 0, 255)
alpha_new = np.where(edge_zone, alpha_edge, alpha_new)

arr_out = arr.copy()
arr_out[:,:,3] = alpha_new.astype(np.uint8)

result = Image.fromarray(arr_out.astype(np.uint8), 'RGBA')

# crop la pion cu padding
pad = 20
top2    = max(0, top - pad)
bottom2 = min(img.height, bottom + pad)
left2   = max(0, left - pad)
right2  = min(img.width, right + pad)

cropped = result.crop((left2, top2, right2, bottom2))
print(f"Crop dupa padding: {cropped.width}x{cropped.height}")

# patrат centrat, transparent
size = max(cropped.width, cropped.height)
square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
ox = (size - cropped.width) // 2
oy = (size - cropped.height) // 2
square.paste(cropped, (ox, oy), cropped)

# resize la 64x64
favicon64 = square.resize((64, 64), Image.LANCZOS)
favicon64.save(r"C:\Users\irina\SahMatAnimat\img\favicon-64.png")
print("Salvat: img/favicon-64.png")

favicon64.save(r"C:\Users\irina\SahMatAnimat\img\favicon.ico",
               format="ICO", sizes=[(16,16),(32,32),(64,64)])
favicon64.save(r"C:\Users\irina\SahMatAnimat\favicon.ico",
               format="ICO", sizes=[(16,16),(32,32),(64,64)])
print("Salvat: favicon.ico")

# pion-logo.png la 300px pentru logo index/hub (mai mare = mai clar)
logo = square.resize((300, 300), Image.LANCZOS)
logo.save(r"C:\Users\irina\SahMatAnimat\img\pion-logo.png")
print("Salvat: img/pion-logo.png (300x300)")

print("GATA - deschide img/favicon-64.png sa verifici")
