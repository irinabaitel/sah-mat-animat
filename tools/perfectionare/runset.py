import sys, time, json, os; sys.path.insert(0, '.')
import ct, nav
W = nav.W
def click_btn(x, y):
    b = [z for z in ct.buttons(W) if abs(z['x'] - x) < 6 and abs(z['y'] - y) < 6]
    if not b: return False
    ct.post_click(b[0]['h'], 15 * ct.SCALE, 10 * ct.SCALE); return True
def snap(tag):
    img = ct.shot(W, f'sets/{tag}.png')
    rows, unk = ct.read_board(img)
    tx = [t['t'] for t in ct.texts(W) if t['x'] < 700 or t['y'] > 200]
    return dict(fen=ct.fen_of(rows), unk=unk, texts=tx)
def run(setname, n=10):
    os.makedirs('sets', exist_ok=True)
    out = dict(set=setname, intro=ct.close_popups(W), tasks=[])
    for i in range(1, n + 1):
        click_btn(778 + 36 * (i - 1), 74); time.sleep(1.5)
        pops = ct.close_popups(W); time.sleep(0.3)
        before = snap(f'{setname}_{i}a')
        click_btn(1062, 874); time.sleep(3.5)
        pops2 = ct.close_popups(W)
        after = snap(f'{setname}_{i}b')
        out['tasks'].append(dict(i=i, pops=pops, before=before, after=after, pops2=pops2))
        print(i, before['fen'], before['unk'], '->', after['fen'], after['unk'], '|', ' / '.join(after['texts'])[:200], pops, pops2, flush=True)
    json.dump(out, open(f'sets/{setname}.json', 'w'), ensure_ascii=False, indent=1)
if __name__ == '__main__':
    run(sys.argv[1])
