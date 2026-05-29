# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

# Porneste de la versiunea navy si inlocuieste navy cu alb
img = Image.open(r"C:\Users\irina\SahMatAnimat\img\pion-logo-navy.png").convert("RGBA")
arr = np.array(img, dtype=np.float32)
r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]

# Pixelii vizibili (corpul pionului, non-albi)
body = (a > 30) & ~((r > 230) & (g > 230) & (b > 230))

arr_white = arr.copy()
arr_white[:,:,0] = np.where(body, 255.0, arr[:,:,0])
arr_white[:,:,1] = np.where(body, 255.0, arr[:,:,1])
arr_white[:,:,2] = np.where(body, 255.0, arr[:,:,2])

result = Image.fromarray(arr_white.astype(np.uint8), 'RGBA')
result.save(r"C:\Users\irina\SahMatAnimat\img\pion-logo-white.png")
print("Salvat: pion-logo-white.png")
