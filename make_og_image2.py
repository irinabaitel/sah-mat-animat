# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

W, H = 1200, 630

# Fundal portocaliu gradient
og = Image.new("RGBA", (W, H))
draw_arr = np.zeros((H, W, 4), dtype=np.uint8)
for y in range(H):
    t = y / H
    rc = int(255 * (1-t) + 230 * t)
    gc = int(140 * (1-t) + 100 * t)
    bc = int(30  * (1-t) + 10  * t)
    draw_arr[y, :] = [rc, gc, bc, 255]
og = Image.fromarray(draw_arr, 'RGBA')

# Pion navy pe transparent (deja generat)
pion = Image.open(r"C:\Users\irina\SahMatAnimat\img\pion-logo-navy.png").convert("RGBA")

# Resize pion la 520px inaltime
target_h = 520
ratio = target_h / pion.height
target_w = int(pion.width * ratio)
pion = pion.resize((target_w, target_h), Image.LANCZOS)

# Centrat
x = (W - target_w) // 2
y = (H - target_h) // 2
og.paste(pion, (x, y), pion)

og.convert("RGB").save(r"C:\Users\irina\SahMatAnimat\img\og-image.jpg", "JPEG", quality=92)
print(f"Salvat: og-image.jpg — pion navy {target_w}x{target_h} centrat pe portocaliu")
