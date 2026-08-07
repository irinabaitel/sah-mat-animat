import os, time, json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scriptul sta in tools/
DEST = os.path.join(REPO, 'img', 'romani')
os.makedirs(DEST, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

PLAYERS = [
    (1,  "r1_Albin",         "Adolf_Albin"),
    (2,  "r2_Gudju",         "Ion_Gudju"),
    (3,  "r3_Ciocaltea",     "Victor_Cioc%C3%A2ltea"),
    (4,  "r4_Polihroniade",  "Elisabeta_Polihroniade"),
    (5,  "r5_Gheorghiu",     "Florin_Gheorghiu"),
    (6,  "r6_Suba",          "Mihai_%C8%98uba"),
    (7,  "r7_Teodorescu",    "Margareta_Teodorescu"),
    (8,  "r8_Marin",         "Mihail_Marin"),
    (9,  "r9_Nisipeanu",     "Liviu-Dieter_Nisipeanu"),
    (10, "r10_LAmi",         "Alina_l%27Ami"),
    (11, "r11_Foisor",       "Sabina-Francesca_Foisor"),
    (12, "r12_Bulmaga",      "Irina_Bulmaga"),
    (13, "r13_Lupulescu",    "Constantin_Lupulescu"),
    (14, "r14_Deac",         "Bogdan-Daniel_Deac"),
    (15, "r15_Gavrilescu",   "Marian_Gavrilescu"),
]

def get_image_url(wiki_title):
    api = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + wiki_title
    req = urllib.request.Request(api, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            thumb = data.get('thumbnail', {}).get('source')
            if thumb:
                return thumb
            return data.get('originalimage', {}).get('source')
    except Exception as e:
        return None

def download(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
    if len(data) > 2000:
        with open(dest, 'wb') as f:
            f.write(data)
        return len(data)
    return 0

ok, fail, nourl = 0, 0, 0
for pid, fname, title in PLAYERS:
    # detect extension from existing file
    found = None
    for ext in ['.jpg', '.png', '.jpeg', '.webp']:
        p = os.path.join(DEST, fname + ext)
        if os.path.exists(p):
            found = p
            break
    if found:
        print(f'  [skip] {fname}')
        ok += 1
        continue

    img_url = get_image_url(title)
    time.sleep(1.5)

    if not img_url:
        print(f'  [NOURL] {fname} ({title})')
        nourl += 1
        continue

    ext = '.png' if '.png' in img_url.lower() else '.jpg'
    dest_file = os.path.join(DEST, fname + ext)

    try:
        size = download(img_url, dest_file)
        time.sleep(1.5)
        if size:
            print(f'  [ok]   {fname} ({size//1024}KB)')
            ok += 1
        else:
            print(f'  [SMALL] {fname}')
            fail += 1
    except Exception as e:
        print(f'  [ERR]  {fname} — {e}')
        fail += 1

print(f'\nGata: {ok} ok, {fail} erori, {nourl} fara URL.')
files = sorted(os.listdir(DEST))
print(f'Fisiere ({len(files)}):')
for f in files:
    print(' ', f)
