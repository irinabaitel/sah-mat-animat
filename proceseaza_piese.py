"""
Procesează piesele Chaturanga:
- Scoate fundalul alb (cu anti-aliasing smooth)
- Set deschis  (lemn de arțar, mai luminos)
- Set închis   (nuc/abanos, întunecat)
"""

from PIL import Image, ImageEnhance
import numpy as np
import os

BASE = r"c:\Users\irina\SahMatAnimat\piese_sah\india\piese_chaturanga"
DIR_DESCHIS = os.path.join(BASE, "set_deschis")
DIR_INCHIS  = os.path.join(BASE, "set_inchis")
os.makedirs(DIR_DESCHIS, exist_ok=True)
os.makedirs(DIR_INCHIS,  exist_ok=True)

PIESE = [
    "elefantul_gaja.png",
    "rege_raja.png",
    "sfetnic_mantri.png",
    "calul_ashva.png",
    "caruldelupta_ratha.png",
    "pion_padati.png",
]

def scoate_alb(img, prag=245, penumbra=25):
    """Elimină fundalul alb cu margini moi (smooth alpha la anti-aliasing)."""
    img = img.convert("RGBA")
    data = np.array(img, dtype=np.float32)
    r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]

    # "Cât de alb" e fiecare pixel: 255 = pur alb
    albiciune = np.minimum(np.minimum(r, g), b)

    # Alpha: 0 unde albiciune > prag, 255 unde e sub (prag - penumbra)
    alpha = np.clip((prag - albiciune) / penumbra * 255, 0, 255).astype(np.uint8)

    result = data.astype(np.uint8)
    result[:, :, 3] = alpha
    return Image.fromarray(result)


def aplica_ton(img_rgba, brightness, saturation, contrast=1.0):
    img = img_rgba.copy()
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Color(img).enhance(saturation)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return img


for fname in PIESE:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f"  !! Lipsă: {fname}")
        continue

    orig = Image.open(path)
    transparent = scoate_alb(orig)

    # --- SET DESCHIS: lemn de arțar, luminos, cald ---
    deschis = aplica_ton(transparent, brightness=1.80, saturation=0.55, contrast=0.95)
    deschis.save(os.path.join(DIR_DESCHIS, fname), optimize=False)

    # --- SET ÎNCHIS: nuc întunecat (mai puțin negru ca să se vadă detaliile) ---
    inchis = aplica_ton(transparent, brightness=0.48, saturation=0.65, contrast=1.05)
    inchis.save(os.path.join(DIR_INCHIS, fname), optimize=False)

    print(f"  OK  {fname}")

print("\nGata! Seturi salvate în:")
print(f"  {DIR_DESCHIS}")
print(f"  {DIR_INCHIS}")
