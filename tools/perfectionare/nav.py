import sys, time, json; sys.path.insert(0, '.')
import ct
W = ct.find_main()
def lists():
    lv = [k for k in ct.kids(W) if 'SysListView32' in k['cls']]
    lv.sort(key=lambda k: k['L']); return lv  # left, right
def pick(listidx, logical_y):
    lv = lists()[listidx]
    _, top, _, _ = ct.logical_of(W, lv)
    ct.post_click(lv['h'], 100 * ct.SCALE, (logical_y - top) * ct.SCALE)
def press(caption):
    for b in ct.buttons(W):
        if b['txt'].strip().lower() == caption.lower(): ct.bm_click(b['h']); return True
    return False
def press_at(x, y):
    bs = [b for b in ct.buttons(W) if abs(b['x'] - x) < 25 and abs(b['y'] - y) < 15]
    ct.bm_click(bs[0]['h']); return bs[0]
def state(name=None):
    img = ct.shot(W, f'{name}.png' if name else None)
    rows, unk = ct.read_board(img)
    return dict(fen=ct.fen_of(rows), unk=unk, texts=ct.texts(W), btn=[(b['txt'], b['x'], b['y']) for b in ct.buttons(W)])
if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'pick': pick(int(sys.argv[2]), float(sys.argv[3])); time.sleep(1.5)
    elif cmd == 'press': print(press(sys.argv[2])); time.sleep(2)
    elif cmd == 'pressat': print(press_at(float(sys.argv[2]), float(sys.argv[3]))); time.sleep(2)
    if len(sys.argv) > 1 and sys.argv[-1].startswith('@'):
        print(json.dumps(state(sys.argv[-1][1:]), ensure_ascii=False, indent=0))
