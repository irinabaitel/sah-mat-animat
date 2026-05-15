#!/usr/bin/env python3
# Prelucrare piese Shatranj: decupare fundal opac + recolor greige (ca chaturanga).
# Sursele = PNG-uri nanobanana din /sdcard/Download. Iesirea -> img/shatranj/.
import os, numpy as np
from PIL import Image

DL = "/sdcard/Download"
OUT = "/root/proiectele_mele/sah-mat-animat/img/shatranj"
os.makedirs(OUT, exist_ok=True)

# culori preluate exact din piesele chaturanga finalizate
BODY_W = np.array([203, 189, 167], np.float32)   # corp piesa alba
BODY_B = np.array([141, 139, 139], np.float32)   # corp piesa neagra
MARGIN = 8

# nume sursa -> (nume semantic, litera sah)
PIECES = {
    "FIL":    ("_test_fil.png",                                   "fil",    "B"),
    "SHAH":   ("Gemini_Generated_Image_jmxfrhjmxfrhjmxf.png",     "shah",   "K"),
    "FIRZAN": ("Gemini_Generated_Image_styd1qstyd1qstyd.png",     "firzan", "Q"),
    "RUKH":   ("Gemini_Generated_Image_js63ckjs63ckjs63.png",     "rukh",   "R"),
    "ASB":    ("Gemini_Generated_Image_p01ajfp01ajfp01a.png",     "asb",    "N"),
    "BAIDAQ": ("Gemini_Generated_Image_qfoto9qfoto9qfot.png",     "baidaq", "P"),
}

def lum(rgb):
    return 0.299*rgb[...,0] + 0.587*rgb[...,1] + 0.114*rgb[...,2]

def cut_bg(arr, T=105):
    """Sterge fundalul deschis legat de margini; se opreste la conturul negru."""
    h, w, _ = arr.shape
    L = lum(arr[..., :3].astype(np.float32))
    al = arr[..., 3]
    M = (L > T) & (al > 40)               # zone deschise (fundal SAU corpul piesei)
    reach = np.zeros((h, w), bool)
    reach[0, :] |= M[0, :]; reach[-1, :] |= M[-1, :]
    reach[:, 0] |= M[:, 0]; reach[:, -1] |= M[:, -1]
    for _ in range(5000):
        prev = reach.copy()
        reach[1:, :]  |= reach[:-1, :] & M[1:, :]
        reach[:-1, :] |= reach[1:, :]  & M[:-1, :]
        reach[:, 1:]  |= reach[:, :-1] & M[:, 1:]
        reach[:, :-1] |= reach[:, 1:]  & M[:, :-1]
        if np.array_equal(reach, prev):
            break
    out = arr.copy()
    out[reach, 3] = 0
    return out

def recolor(arr, body):
    """Contur -> negru, corp -> culoarea data; muchii anti-alias amestecate."""
    rgb = arr[..., :3].astype(np.float32)
    L = lum(rgb)
    t = np.clip((L - 55.0) / (150.0 - 55.0), 0, 1)[..., None]   # 0=contur 1=corp
    new = (t * body).astype(np.uint8)        # lerp(negru, corp)
    out = arr.copy()
    out[..., :3] = new
    return out

def crop_pad(im, m=MARGIN):
    bb = im.getbbox()
    im = im.crop(bb)
    c = Image.new("RGBA", (im.width + 2*m, im.height + 2*m), (0, 0, 0, 0))
    c.paste(im, (m, m), im)
    return c

report = []
for key, (src, name, letter) in PIECES.items():
    arr = np.array(Image.open(os.path.join(DL, src)).convert("RGBA"))
    arr = cut_bg(arr)
    cut = crop_pad(Image.fromarray(arr))
    cut.save(os.path.join(OUT, f"{name}_w_pre_recolor.png"))      # backup (git-ignored)

    w_img = crop_pad(Image.fromarray(recolor(np.array(cut), BODY_W)))
    b_img = crop_pad(Image.fromarray(recolor(np.array(cut), BODY_B)))
    w_img.save(os.path.join(OUT, f"{name}_w.png"))
    b_img.save(os.path.join(OUT, f"{name}_b.png"))
    # copii cu litera de sah (ca la chaturanga, pentru tabla interactiva)
    w_img.save(os.path.join(OUT, f"w{letter}.png"))
    b_img.save(os.path.join(OUT, f"b{letter}.png"))
    report.append(f"{key:7s} {name:7s} ({letter}) -> {w_img.size}")

print("\n".join(report))
print("GATA ->", OUT)
