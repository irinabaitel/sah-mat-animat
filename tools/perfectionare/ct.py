# Chess Tutor remote-control helpers (Windows, ctypes)
import ctypes, ctypes.wintypes as wt, time, json, os, sys
from PIL import Image
import numpy as np

u = ctypes.windll.user32; g = ctypes.windll.gdi32
u.SetProcessDPIAware()
HERE = os.path.dirname(os.path.abspath(__file__))
SCALE = 1.25  # app is DPI-unaware on a 125% monitor

def find_main():
    res = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    def cb(h, l):
        n = u.GetWindowTextLengthW(h)
        b = ctypes.create_unicode_buffer(n + 1); u.GetWindowTextW(h, b, n + 1)
        if b.value.startswith('Chess Tutor Step 1') and u.IsWindowVisible(h): res.append(h)
        return True
    u.EnumWindows(cb, 0)
    return res[0]

def rect(h):
    r = wt.RECT(); u.GetWindowRect(h, ctypes.byref(r)); return r.left, r.top, r.right, r.bottom

def cls(h):
    b = ctypes.create_unicode_buffer(256); u.GetClassNameW(h, b, 256); return b.value

def text(h):
    WM_GETTEXTLENGTH, WM_GETTEXT = 0x0E, 0x0D
    n = u.SendMessageW(h, WM_GETTEXTLENGTH, 0, 0)
    b = ctypes.create_unicode_buffer(n + 2); u.SendMessageW(h, WM_GETTEXT, n + 2, b); return b.value

def kids(W):
    out = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    def cb(h, l):
        if u.IsWindowVisible(h):
            L, T, R, B = rect(h); out.append(dict(h=h, cls=cls(h), L=L, T=T, W=R - L, H=B - T))
        return True
    u.EnumChildWindows(W, cb, 0)
    return out

def shot(W, path=None):
    L, T, R, B = rect(W); w, h = R - L, B - T
    hdc = u.GetWindowDC(W); mdc = g.CreateCompatibleDC(hdc); bmp = g.CreateCompatibleBitmap(hdc, w, h)
    g.SelectObject(mdc, bmp); u.PrintWindow(W, mdc, 2)
    class BIH(ctypes.Structure):
        _fields_ = [('biSize', wt.DWORD), ('biWidth', ctypes.c_long), ('biHeight', ctypes.c_long), ('biPlanes', wt.WORD), ('biBitCount', wt.WORD), ('biCompression', wt.DWORD), ('biSizeImage', wt.DWORD), ('biXPelsPerMeter', ctypes.c_long), ('biYPelsPerMeter', ctypes.c_long), ('biClrUsed', wt.DWORD), ('biClrImportant', wt.DWORD)]
    bi = BIH(); bi.biSize = ctypes.sizeof(BIH); bi.biWidth = w; bi.biHeight = -h; bi.biPlanes = 1; bi.biBitCount = 32
    buf = ctypes.create_string_buffer(w * h * 4)
    g.GetDIBits(mdc, bmp, 0, h, buf, ctypes.byref(bi), 0)
    g.DeleteObject(bmp); g.DeleteDC(mdc); u.ReleaseDC(W, hdc)
    img = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'BGRA', 0, 1).convert('RGB')
    # PrintWindow renders at logical size in top-left
    img = img.crop((0, 0, int(w / SCALE), int(h / SCALE)))
    if path: img.save(path)
    return img

def bm_click(h): u.SendMessageW(h, 0x00F5, 0, 0)

def post_click(h, x, y, double=False):
    lp = (int(y) << 16) | (int(x) & 0xFFFF)
    u.PostMessageW(h, 0x201, 1, lp); time.sleep(0.05); u.PostMessageW(h, 0x202, 0, lp)
    if double:
        time.sleep(0.05); u.PostMessageW(h, 0x203, 1, lp); u.PostMessageW(h, 0x202, 0, lp)

def logical_of(W, k):
    L, T, _, _ = rect(W); return ((k['L'] - L) / SCALE, (k['T'] - T) / SCALE, k['W'] / SCALE, k['H'] / SCALE)

def buttons(W):
    """visible buttons with their caption (from window text) and logical position"""
    out = []
    for k in kids(W):
        if 'BUTTON' in k['cls'] and k['H'] > 0:
            x, y, w, h = logical_of(W, k); out.append(dict(h=k['h'], txt=text(k['h']), x=round(x), y=round(y), w=round(w)))
    return out

def texts(W):
    out = []
    for k in kids(W):
        if 'RichEdit' in k['cls'] or 'STATIC' in k['cls'] or 'EDIT' in k['cls']:
            t = text(k['h'])
            if t.strip():
                x, y, w, h = logical_of(W, k); out.append(dict(x=round(x), y=round(y), t=t))
    return out

# ---------- board ----------
BX, BY, SQ = 48.5, 110.5, 70.4   # logical px of a8 top-left, square size

def square_img(img, f, r):  # f 0..7 (a..h), r 1..8
    x0 = BX + f * SQ; y0 = BY + (8 - r) * SQ
    return img.crop((int(x0 + 3), int(y0 + 3), int(x0 + SQ - 3), int(y0 + SQ - 3)))

def feat(sq):
    a = np.asarray(sq.resize((24, 24))).astype(int)
    dark = (a.max(2) < 60).astype(float)
    white = (a.min(2) > 235).astype(float)
    return dark, white

TPL = os.path.join(HERE, 'tpl.json')
def load_tpl():
    return json.load(open(TPL)) if os.path.exists(TPL) else {}

def classify(sq, tpl):
    d, w = feat(sq)
    if d.sum() + w.sum() < 10: return '.', 0.0
    best, bd = '?', 1e9
    for k, lst in tpl.items():
        for td, tw in lst:
            dist = np.abs(d - np.array(td)).sum() + np.abs(w - np.array(tw)).sum()
            if dist < bd: best, bd = k, dist
    return (best if bd < 60 else '?'), bd

def read_board(img, tpl=None):
    tpl = tpl if tpl is not None else load_tpl()
    rows, unk = [], []
    for r in range(8, 0, -1):
        row = ''
        for f in range(8):
            p, dist = classify(square_img(img, f, r), tpl)
            if p == '?': unk.append('abcdefgh'[f] + str(r))
            row += p
        rows.append(row)
    return rows, unk

def fen_of(rows):
    out = []
    for row in rows:
        s, e = '', 0
        for c in row:
            if c == '.': e += 1
            else:
                if e: s += str(e); e = 0
                s += c
        if e: s += str(e)
        out.append(s)
    return '/'.join(out)

def learn(img, mapping):
    """mapping: {'e1':'K', ...} add templates"""
    tpl = load_tpl()
    for sqn, p in mapping.items():
        d, w = feat(square_img(img, 'abcdefgh'.index(sqn[0]), int(sqn[1])))
        tpl.setdefault(p, []).append([d.tolist(), w.tolist()])
    json.dump(tpl, open(TPL, 'w'))
    return sorted(tpl)

def popups(W):
    pid = wt.DWORD(); u.GetWindowThreadProcessId(W, ctypes.byref(pid)); res = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    def cb(h, l):
        p = wt.DWORD(); u.GetWindowThreadProcessId(h, ctypes.byref(p))
        if p.value == pid.value and u.IsWindowVisible(h) and h != W: res.append(h)
        return True
    u.EnumWindows(cb, 0); return res

def close_popups(W):
    """read text of each popup and press its first button; returns texts"""
    out = []
    for h in popups(W):
        ks = kids(h)
        out.append(' | '.join(text(k['h']) for k in ks if 'RichEdit' in k['cls'] or 'STATIC' in k['cls']))
        bs = [k for k in ks if 'BUTTON' in k['cls']]
        if bs: bm_click(bs[0]['h']); time.sleep(0.8)
    return out
