"""
Descarcă datele individuale pentru fiecare puzzle din cursul Chessable 33908.
Necesită cookie de sesiune din browser (DevTools > Application > Cookies > chessable.com).

Rulare: python fetch_chessable.py
"""

import json
import time
import urllib.request
import urllib.error

UID = "497286"

STRUCTURE_FILE = "data/chessable_33908_structure.json"
OUTPUT_FILE = "data/chessable_33908_puzzles.json"
BASE_URL = "https://www.chessable.com/api/v0/move/"

COOKIE_STRING = "tms_VisitorID=rkhfwh6xuj; _jst_profileid_fb5e9043b672481791ed69e733d9ac1e=6n7r22W9M; intercom-id-qzot1t7g=ccb8d5ca-3575-4c2d-8b63-0ccd7992f0be; intercom-device-id-qzot1t7g=49ed650e-597d-47fe-b124-70707f34189b; _clck=k2zx97%7C2%7Cfw9%7C0%7C1973; osano_consentmanager_uuid=84f9abd3-c9db-486b-b777-1da370e15b8f; osano_consentmanager=JFNHWKT0kgzOds4iQW_YQUMZrwKXRJL-f3kGuONBrRIs7ySmRNaolFdMGUqQdGyf5UaVia0TgiVOw2v0E3y94BZwIY1YacJXibF1z1ENkMXlQVpqZsfegWZaMhdbJP2mHFwLY-wf98TE9a5fWzsU76K869Xkn5XOv8v3vyqt610IiZdMvNNUu9pwSA1ny_qodBgFCqXZ8Z8044UjFcioAD6rrG664tCjXUUGY5qOqfqZVHDnYukkBiW_f6yEfQ_PbrqpB8wd_2SCyRPKgeos5P9IXGvvOR18JaTtMVsY3y_6JUCc_aqRizQXpN2LB6tdAvCZA26aWL8=; tms_VisitorID=rkhfwh6xuj; __stripe_mid=ad593b78-583a-4031-93b6-01a47b0b4da8a1766f; _hjSessionUser_3516533=eyJpZCI6IjEyYmY3N2M1LWUxOTUtNTFiMS04NDhhLTM5M2ZkZGRmNDJlMiIsImNyZWF0ZWQiOjE3NzAwNTQ4Nzk5MzgsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.222383120.1772555935; _gid=GA1.2.1893270833.1779858777; tms_wsip=1; intercom-session-qzot1t7g=; cf_clearance=XjM1aaAf7.EklsBMDV.iJLVybERzj6JFBf8hk8lslak-1779858784-1.2.1.1-Wx0Go7bT6dKpijXZhItvehMPiDb5XZXafinLiqcIPkKkSwHk8EF3CdKY._BN9Kuxc4fInl.VvVP7iY61D2WCG.wHg3pGEhkGGJp7koh1T6ZS0.vC.ALUIy4393Kcg0oxweRBPmp.C_3SXGg6Udb986R0LQCME.gS_VCU237uN4L2VFHnSFBmF9ld658gFWZmba1.5nHrmt_hwa5.FApNigL87mznbq.BCAzaLyVH7Pmv6rOWWMPAFV4EcbV.oyDTGHYakpqIia61m207bjBy2WFghW8d1EdXQ7oWz7WFrTV2LS12c1QNe7kkWyccHnQupDP8k95fXu1lfdE4l9u06WGt1pTCzVc9ZThgvuDLt5TcMRWL1EDsl1_ITZEpWQcsFW453G.LJPa5cDmR2BLTIJpOeU8yGXdD7cApmiCHjbs; sec_session_id=8ad941b1061362d3ad23f9179768a293; uidsessid=497286; unamesessid=nowhereman7; loginstringsessid=6f77774bf045f6c6%3A672c26b6c96b738e4d68782811901fce; _ga_SM6G6M7B8T=GS2.1.s1779858777$o7$g1$t1779859661$j60$l0$h0; _ga=GA1.1.377910248.1741031482; _ga_Z6ZD3CB4HN=GS2.2.s1779858777$o254$g1$t1779859661$j60$l0$h0; amp_dfb317=S6PnaBDJ74NXtx9TRAaB2l.NDk3Mjg2..1jpjtj8do.1jpjuk506.2je.82.2rg"

HEADERS = {
    "Cookie": COOKIE_STRING,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.chessable.com/setting-up-checkmate-patterns/course/33908/",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}

def fetch_variation(oid):
    url = f"{BASE_URL}?uid={UID}&oid={oid}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} pentru oid={oid}")
        return None
    except Exception as e:
        print(f"  Eroare pentru oid={oid}: {e}")
        return None

def main():
    with open(STRUCTURE_FILE, encoding="utf-8") as f:
        structure = json.load(f)

    results = []
    total = sum(len(ch["puzzles"]) for ch in structure["chapters"])
    count = 0

    for chapter in structure["chapters"]:
        print(f"\n--- {chapter['title']} ({chapter['difficulty']}) ---")
        for puzzle in chapter["puzzles"]:
            count += 1
            oid = puzzle["oid"]
            print(f"  [{count}/{total}] oid={oid} — {puzzle['name'][:50]}")
            data = fetch_variation(oid)
            if data:
                results.append({
                    "oid": oid,
                    "name": puzzle["name"],
                    "difficulty": chapter["difficulty"],
                    "chapter": chapter["title"],
                    "raw": data
                })
            time.sleep(1.5)  # nu spama serverul

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nGata! {len(results)}/{total} puzzle-uri salvate în {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
