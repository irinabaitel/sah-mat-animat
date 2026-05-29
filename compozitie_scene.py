"""
Pune piesele Chaturanga peste piesele de șah clasic din scene.
Salvează în piese_sah/india/scene_finale/ (originalele rămân intacte).
"""

from PIL import Image, ImageFilter, ImageEnhance
import os

BASE     = r"c:\Users\irina\SahMatAnimat\piese_sah\india"
SCENE_IN = os.path.join(BASE, "scene")
PIESE_D  = os.path.join(BASE, "piese_chaturanga", "set_deschis")
PIESE_I  = os.path.join(BASE, "piese_chaturanga", "set_inchis")
OUT      = os.path.join(BASE, "scene_finale")
os.makedirs(OUT, exist_ok=True)

def incarca_piesa(folder, fname, inaltime_px):
    """Încarcă o piesă PNG, crop la conținut real, redimensionează la înălțime fixă."""
    path = os.path.join(folder, fname)
    img = Image.open(path).convert("RGBA")

    # Crop la bounding box al pixelilor non-transparenți
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    w, h = img.size
    new_h = inaltime_px
    new_w = int(w * inaltime_px / h)
    return img.resize((new_w, new_h), Image.LANCZOS)

def lipeste(scena, piesa_img, cx, cy):
    """Lipește piesa cu centrul la (cx, bottom_y = cy)."""
    pw, ph = piesa_img.size
    x = cx - pw // 2
    y = cy - ph
    scena.paste(piesa_img, (x, y), piesa_img)

def blur_zona(scena, x1, y1, x2, y2, raza=8, bright=0.88):
    """Estompează ușor zona cu piesele originale cu margini fade (fără dreptunghi vizibil)."""
    from PIL import ImageDraw
    W, H = scena.size
    crop = scena.crop((x1, y1, x2, y2))
    blurat = crop.filter(ImageFilter.GaussianBlur(raza))
    blurat = ImageEnhance.Brightness(blurat).enhance(bright)
    blurat = blurat.convert("RGBA")

    # Mască gradient: alb (opac) în centru, negru (transparent) la margini
    mask = Image.new("L", blurat.size, 0)
    draw = ImageDraw.Draw(mask)
    cw, ch = blurat.size
    fade = 60  # px de fade la margini
    # Centrul e complet opac; marginile dispar gradual
    for i in range(fade):
        val = int(255 * i / fade)
        draw.rectangle([i, i, cw-i-1, ch-i-1], outline=val)
    # Umplem centrul
    draw.rectangle([fade, fade, cw-fade-1, ch-fade-1], fill=255)

    scena.paste(blurat, (x1, y1), mask)

# ================================================================
# SCENA 1 — descoperirea cufărului (tablă goală, fără piese)
# ================================================================
def procesa_scena1():
    img = Image.open(os.path.join(SCENE_IN, "scena_1.png")).convert("RGBA")
    # Nimic de adăugat — scena e curată
    img.save(os.path.join(OUT, "scena_1.png"))
    print("  scena_1 OK")

# ================================================================
# SCENA 2 — Tusk prezintă Gaja (tablă goală, fără piese adăugate)
# ================================================================
def procesa_scena2():
    img = Image.open(os.path.join(SCENE_IN, "scena_2.png")).convert("RGBA")
    # Scena are deja un elefant mic în mâna lui Kibo — nu adăugăm nimic
    img.save(os.path.join(OUT, "scena_2.png"))
    print("  scena_2 OK")

# ================================================================
# SCENA 3 — armata Chaturanga (piese clasice pe masă → le acoperim)
# ================================================================
def procesa_scena3():
    img = Image.open(os.path.join(SCENE_IN, "scena_3.png")).convert("RGBA")

    # Fără blur — punem piesele direct peste cele clasice
    # Înălțime uniformă pentru tot setul: 130px (pare din același set)
    H = 130

    # Piese deschise (stânga mesei) — 6 piese
    lipeste(img, incarca_piesa(PIESE_D, "rege_raja.png",          H), cx=280, cy=600)
    lipeste(img, incarca_piesa(PIESE_D, "sfetnic_mantri.png",     H), cx=390, cy=608)
    lipeste(img, incarca_piesa(PIESE_D, "elefantul_gaja.png",     H), cx=495, cy=612)
    lipeste(img, incarca_piesa(PIESE_D, "calul_ashva.png",        H), cx=310, cy=648)
    lipeste(img, incarca_piesa(PIESE_D, "pion_padati.png",        H), cx=430, cy=650)
    lipeste(img, incarca_piesa(PIESE_D, "pion_padati.png",        H), cx=540, cy=648)

    # Piese închise (dreapta mesei) — 6 piese
    lipeste(img, incarca_piesa(PIESE_I, "caruldelupta_ratha.png", H), cx=640, cy=610)
    lipeste(img, incarca_piesa(PIESE_I, "calul_ashva.png",        H), cx=748, cy=608)
    lipeste(img, incarca_piesa(PIESE_I, "rege_raja.png",          H), cx=852, cy=600)
    lipeste(img, incarca_piesa(PIESE_I, "pion_padati.png",        H), cx=660, cy=648)
    lipeste(img, incarca_piesa(PIESE_I, "pion_padati.png",        H), cx=768, cy=650)
    lipeste(img, incarca_piesa(PIESE_I, "pion_padati.png",        H), cx=870, cy=648)

    img.save(os.path.join(OUT, "scena_3.png"))
    print("  scena_3 OK")

# ================================================================
# SCENA 4 — prima mutare pe tablă (piese pe tabla de șah)
# ================================================================
def procesa_scena4():
    img = Image.open(os.path.join(SCENE_IN, "scena_4.png")).convert("RGBA")

    # Tabla in perspectiva — 4 randuri
    # cy fix per rand: 0=fata-deschis, 1=pioni-deschis, 2=pioni-inchis, 3=spate-inchis
    # Randurile 0 si 1 au functionat. Randurile 2 si 3 corectate mai jos (nu mai zboara).
    CY = [670, 592, 542, 498]

    def coord4(col, rand):
        t = rand / 3.0
        cy = CY[rand]
        xl = int(272 + t * 68)
        xr = int(940 - t * 58)
        cx = int(xl + col * (xr - xl) / 7)
        return cx, cy

    # Inaltimi descrescatoare cu perspectiva: fata = mare, spate = mic
    sizes4 = [130, 105, 76, 60]

    piese_back = [
        "caruldelupta_ratha.png", "calul_ashva.png", "elefantul_gaja.png",
        "sfetnic_mantri.png", "rege_raja.png", "elefantul_gaja.png",
        "calul_ashva.png", "caruldelupta_ratha.png",
    ]

    # Rand 0 — deschis fata (piese albe)
    for i, fname in enumerate(piese_back):
        cx, cy = coord4(i, 0)
        lipeste(img, incarca_piesa(PIESE_D, fname, sizes4[0]), cx=cx, cy=cy)
    # Rand 1 — pioni deschis
    for i in range(8):
        cx, cy = coord4(i, 1)
        lipeste(img, incarca_piesa(PIESE_D, "pion_padati.png", sizes4[1]), cx=cx, cy=cy)
    # Rand 2 — pioni inchisi (corectati sa nu zboare)
    for i in range(8):
        cx, cy = coord4(i, 2)
        lipeste(img, incarca_piesa(PIESE_I, "pion_padati.png", sizes4[2]), cx=cx, cy=cy)
    # Rand 3 — piese inchise spate (corectati sa nu zboare)
    for i, fname in enumerate(piese_back):
        cx, cy = coord4(i, 3)
        lipeste(img, incarca_piesa(PIESE_I, fname, sizes4[3]), cx=cx, cy=cy)

    img.save(os.path.join(OUT, "scena_4.png"))
    print("  scena_4 OK")

# ================================================================
# SCENA 5 — celebrare (2816×1536 → coordonate ×2 față de celelalte)
# ================================================================
def procesa_scena5():
    img = Image.open(os.path.join(SCENE_IN, "scena_5.png")).convert("RGBA")
    # 2816x1536 = dublu față de 1408x768, fără blur
    H = 260  # înălțime uniformă pentru toate piesele (×2 față de scena 3)

    # Piese deschise stânga
    lipeste(img, incarca_piesa(PIESE_D, "rege_raja.png",          H), cx=570,  cy=1200)
    lipeste(img, incarca_piesa(PIESE_D, "sfetnic_mantri.png",     H), cx=780,  cy=1216)
    lipeste(img, incarca_piesa(PIESE_D, "elefantul_gaja.png",     H), cx=990,  cy=1224)
    lipeste(img, incarca_piesa(PIESE_D, "pion_padati.png",        H), cx=620,  cy=1296)
    lipeste(img, incarca_piesa(PIESE_D, "pion_padati.png",        H), cx=840,  cy=1300)
    lipeste(img, incarca_piesa(PIESE_D, "pion_padati.png",        H), cx=1060, cy=1300)

    # Piese închise dreapta
    lipeste(img, incarca_piesa(PIESE_I, "caruldelupta_ratha.png", H), cx=1280, cy=1216)
    lipeste(img, incarca_piesa(PIESE_I, "calul_ashva.png",        H), cx=1490, cy=1208)
    lipeste(img, incarca_piesa(PIESE_I, "rege_raja.png",          H), cx=1700, cy=1200)
    lipeste(img, incarca_piesa(PIESE_I, "pion_padati.png",        H), cx=1300, cy=1296)
    lipeste(img, incarca_piesa(PIESE_I, "pion_padati.png",        H), cx=1510, cy=1300)
    lipeste(img, incarca_piesa(PIESE_I, "pion_padati.png",        H), cx=1720, cy=1296)

    img.save(os.path.join(OUT, "scena_5.png"))
    print("  scena_5 OK")

# ================================================================
if __name__ == "__main__":
    print("Procesez scenele...")
    procesa_scena1()
    procesa_scena2()
    procesa_scena3()
    procesa_scena4()
    procesa_scena5()
    print(f"\nGata! Scene salvate în: {OUT}")
