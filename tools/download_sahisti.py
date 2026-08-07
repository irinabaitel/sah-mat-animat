import os, time, json, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scriptul sta in tools/
DEST = os.path.join(REPO, 'img', 'sahisti')
os.makedirs(DEST, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# (id, filename, wikipedia_page_title)
PLAYERS = [
    (2,  "p2_RuyLopez",     "Ruy_López_de_Segura"),
    (3,  "p3_Greco",        "Gioachino_Greco"),
    (5,  "p5_LaBourdonnais","Louis-Charles_Mahé_de_La_Bourdonnais"),
    (24, "p24_Fine",        "Reuben_Fine"),
    (25, "p25_Reshevsky",   "Samuel_Reshevsky"),
    (29, "p29_Bronstein",   "David_Bronstein"),
    (31, "p31_Geller",      "Efim_Geller"),
    (33, "p33_Polugaevsky", "Lev_Polugaevsky"),
    (35, "p35_Larsen",      "Bent_Larsen"),
    (37, "p37_Korchnoi",    "Viktor_Korchnoi"),
    (39, "p39_Portisch",    "Lajos_Portisch"),
    (41, "p41_Timman",      "Jan_Timman"),
    (47, "p47_Gelfand",     "Boris_Gelfand"),
    (48, "p48_Leko",        "Péter_Lékó"),
    (49, "p49_Kamsky",      "Gata_Kamsky"),
    (52, "p52_Caruana",     "Fabiano_Caruana"),
    (4,  "p4_Philidor",     "François-André_Danican_Philidor"),
    (6,  "p6_Staunton",     "Howard_Staunton"),
    (7,  "p7_Anderssen",    "Adolf_Anderssen"),
    (8,  "p8_Morphy",       "Paul_Morphy"),
    (9,  "p9_Winawer",      "Szymon_Winawer"),
    (10, "p10_Zukertort",   "Johannes_Zukertort"),
    (11, "p11_Steinitz",    "Wilhelm_Steinitz"),
    (12, "p12_Chigorin",    "Mikhail_Chigorin"),
    (13, "p13_Lasker",      "Emanuel_Lasker"),
    (14, "p14_Maroczy",     "Géza_Maróczy"),
    (15, "p15_Tarrasch",    "Siegbert_Tarrasch"),
    (16, "p16_Pillsbury",   "Harry_Nelson_Pillsbury"),
    (17, "p17_Schlechter",  "Carl_Schlechter"),
    (18, "p18_Rubinstein",  "Akiba_Rubinstein"),
    (19, "p19_Nimzowitsch", "Aron_Nimzowitsch"),
    (20, "p20_Capablanca",  "Jose_Raul_Capablanca"),
    (21, "p21_Alekhine",    "Alexander_Alekhine"),
    (22, "p22_Bogoljubov",  "Efim_Bogoljubov"),
    (23, "p23_Euwe",        "Max_Euwe"),
    (26, "p26_Najdorf",     "Miguel_Najdorf"),
    (27, "p27_Botvinnik",   "Mikhail_Botvinnik"),
    (28, "p28_Keres",       "Paul_Keres"),
    (30, "p30_Smyslov",     "Vasily_Smyslov"),
    (32, "p32_Tal",         "Mikhail_Tal"),
    (34, "p34_Petrosian",   "Tigran_Petrosian"),
    (36, "p36_Spassky",     "Boris_Spassky"),
    (38, "p38_Fischer",     "Bobby_Fischer"),
    (40, "p40_Karpov",      "Anatoly_Karpov"),
    (42, "p42_Kasparov",    "Garry_Kasparov"),
    (43, "p43_Ivanchuk",    "Vasyl_Ivanchuk"),
    (44, "p44_Anand",       "Viswanathan_Anand"),
    (45, "p45_Kramnik",     "Vladimir_Kramnik"),
    (46, "p46_Topalov",     "Veselin_Topalov"),
    (50, "p50_Aronian",     "Levon_Aronian"),
    (51, "p51_Karjakin",    "Sergey_Karjakin"),
    (53, "p53_Carlsen",     "Magnus_Carlsen"),
    (54, "p54_DingLiren",   "Ding_Liren"),
    (55, "p55_Gukesh",      "Gukesh_D"),
]

def get_image_url(wiki_title):
    api = f'https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}'
    req = urllib.request.Request(api, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            # prefer thumbnail (Wikipedia allows it), fallback to original
            thumb = data.get('thumbnail', {}).get('source')
            if thumb:
                return thumb
            return data.get('originalimage', {}).get('source')
    except:
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

ok, fail = 0, 0
for pid, fname, title in PLAYERS:
    ext = '.jpg'
    dest = os.path.join(DEST, fname + ext)
    if os.path.exists(dest):
        print(f'  [skip] {fname}')
        ok += 1
        continue

    img_url = get_image_url(title)
    if not img_url:
        print(f'  [NOURL] {fname}')
        fail += 1
        time.sleep(2.0)
        continue

    # detect extension
    if '.png' in img_url.lower():
        ext = '.png'
        dest = os.path.join(DEST, fname + ext)

    try:
        size = download(img_url, dest)
        if size:
            print(f'  [ok]   {fname} ({size//1024}KB)')
            ok += 1
        else:
            print(f'  [SMALL] {fname}')
            fail += 1
    except Exception as e:
        print(f'  [ERR]  {fname} — {e}')
        fail += 1

    time.sleep(2.0)

print(f'\nGata: {ok} descarcate, {fail} erori.')
print(f'Fisiere in {DEST}:')
files = os.listdir(DEST)
for f in sorted(files):
    print(' ', f)
