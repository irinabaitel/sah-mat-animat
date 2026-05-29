# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ---- 1. Extrage pionul din imaginea sursa (huvnyihuvnyihuvn (1).png) ----
src = r"C:\Users\irina\Downloads\Gemini_Generated_Image_huvnyihuvnyihuvn (1).png"
img = Image.open(src).convert("RGBA")
arr = np.array(img, dtype=np.float32)

r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
saturation_range = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
luminosity = (r + g + b) / 3.0

# Masca fundal alb/gri
bg_mask = (saturation_range < 30) & (luminosity > 155)

# Masca suplimentara: orice pixel cu saturatie mica sub baza piesei colorate
pion_colored_rows = np.where((saturation_range > 60).max(axis=1))[0]
pion_bottom_row = max(0, int(pion_colored_rows[-1]) - 10)  # 10px mai sus, pentru siguranta
extra_shadow = np.zeros(arr.shape[:2], dtype=bool)
extra_shadow[pion_bottom_row:, :] = saturation_range[pion_bottom_row:, :] < 90
bg_mask = bg_mask | extra_shadow

fg_mask = ~bg_mask

# Aplica transparenta
alpha_new = np.where(bg_mask, 0.0, 255.0)
edge_zone = (saturation_range >= 10) & (saturation_range < 30) & (luminosity > 120) & (luminosity <= 155)
alpha_edge = np.clip((saturation_range - 10) / 20.0 * 255.0, 0, 255)
alpha_new = np.where(edge_zone, alpha_edge, alpha_new)
# Forteaza 0 pentru zona de umbra - suprascrie orice ar fi lasat edge_zone
alpha_new = np.where(extra_shadow, 0.0, alpha_new)

arr_out = arr.copy()
arr_out[:,:,3] = alpha_new.astype(np.uint8)
pion_rgba = Image.fromarray(arr_out.astype(np.uint8), 'RGBA')

# Crop la bounding box al pionului
# Foloseste saturatie > 40 pentru bottom (exclude umbra tablei de sah)
colored_mask = saturation_range > 30
rows_color = np.where(colored_mask.max(axis=1))[0]
rows_all   = np.where(fg_mask.max(axis=1))[0]
cols       = np.where(fg_mask.max(axis=0))[0]

top    = rows_all[0]
bottom = rows_color[-1]   # ultima linie cu piese colorate (fara umbra)
left, right = cols[0], cols[-1]

pad_top  = 40
pad_bot  = 0   # nu adauga nimic jos - taie fix la baza piesei
pad_side = 40
top2    = max(0, top - pad_top)
bottom2 = min(img.height, bottom + pad_bot)
left2   = max(0, left - pad_side)
right2  = min(img.width, right + pad_side)
pion_cropped = pion_rgba.crop((left2, top2, right2, bottom2))

# Patrат centrat
size = max(pion_cropped.width, pion_cropped.height)
square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
ox = (size - pion_cropped.width) // 2
oy = (size - pion_cropped.height) // 2
square.paste(pion_cropped, (ox, oy), pion_cropped)

# Resize la ~520px pentru og-image (inalt ~520, lat proportional)
target_h = 610
ratio = target_h / square.height
target_w = int(square.width * ratio)
pion_final = square.resize((target_w, target_h), Image.LANCZOS)
print(f"Pion final: {target_w}x{target_h}")

# Estompeaza ultimii 20px de jos -> elimina orice reflexie reziduala
pion_arr = np.array(pion_final, dtype=np.float32)
fade_px = 10
for dy in range(fade_px):
    row_idx = target_h - fade_px + dy
    factor = dy / fade_px   # 0.0 la fund, 1.0 la linia de start fade
    pion_arr[row_idx, :, 3] *= factor
pion_final = Image.fromarray(pion_arr.astype(np.uint8), 'RGBA')

# ---- 2. Construieste og-image 1200x630 ----
W, H = 1200, 630
og = Image.new("RGBA", (W, H), (0,0,0,255))

# Fundal portocaliu gradient
draw = ImageDraw.Draw(og)
orange_top = (255, 140, 30)
orange_bot = (230, 100, 10)
for y in range(H):
    t = y / H
    rc = int(orange_top[0] * (1-t) + orange_bot[0] * t)
    gc = int(orange_top[1] * (1-t) + orange_bot[1] * t)
    bc_ = int(orange_top[2] * (1-t) + orange_bot[2] * t)
    draw.line([(0, y), (W, y)], fill=(rc, gc, bc_))

# ---- 3. Pion centrat, mare ----
pion_x = (W - target_w) // 2
pion_y = (H - target_h) // 2
og.paste(pion_final, (pion_x, pion_y), pion_final)

# ---- 4. Salveaza (fara text - titlul vine din meta tags) ----
og_rgb = og.convert("RGB")
og_rgb.save(r"C:\Users\irina\SahMatAnimat\img\og-image.jpg", "JPEG", quality=92)
print("Salvat: img/og-image.jpg (1200x630)")
