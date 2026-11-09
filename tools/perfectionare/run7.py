# Rulează seturi de exerciții din Chess Tutor cu butoanele găsite dinamic (merge la orice scalare/mărime a ferestrei).
# Folosire:  set CT_SCALE=1 & python run7.py open <lecție_y> <set_y> <nume>     (y = poziția în listă, pixeli logici)
#            python run7.py learn e8=k b7=Q ...   (învață piesele din captura curentă)
import sys, time, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ct
ct.BY = float(os.environ.get('CT_BY', '101'))
W = ct.find_main()

def num_buttons():
    bs = [b for b in ct.buttons(W) if b['y'] < 100 and b['w'] == 30]
    return sorted(bs, key=lambda b: b['x'])
def answer_btn():
    bs = [b for b in ct.buttons(W) if b['y'] > 840 and b['w'] == 72]
    return max(bs, key=lambda b: b['x'])
def start_btn():
    bs = [b for b in ct.buttons(W) if b['y'] > 840 and b['w'] == 101]
    return max(bs, key=lambda b: b['x'])
def overview_btn():
    bs = [b for b in ct.buttons(W) if b['w'] == 124 and b['y'] < 300]
    return bs[0] if bs else None

def snap(tag):
    img = ct.shot(W, f'sets/img/{tag}.png')
    rows, unk = ct.read_board(img)
    tx = [t['t'] for t in ct.texts(W)]
    return dict(fen=ct.fen_of(rows), unk=unk, texts=tx)

def run(setname):
    os.makedirs('sets/img', exist_ok=True)
    out = dict(set=setname, intro=ct.close_popups(W), tasks=[])
    nb = num_buttons()
    for i, b in enumerate(nb, 1):
        ct.post_click(b['h'], 15, 10); time.sleep(float(os.environ.get('CT_WAIT', '1.5')))
        pops = ct.close_popups(W); time.sleep(0.3)
        before = snap(f'{setname}_{i}a')
        ab = answer_btn(); ct.post_click(ab['h'], 15, 10); time.sleep(float(os.environ.get('CT_WAIT2', '3.5')))
        pops2 = ct.close_popups(W)
        after = snap(f'{setname}_{i}b')
        out['tasks'].append(dict(i=i, pops=pops, before=before, after=after, pops2=pops2))
        print(i, before['fen'], before['unk'], '->', after['fen'], after['unk'], '|', ' / '.join(after['texts'])[:220], pops, pops2, flush=True)
    json.dump(out, open(f'sets/{setname}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def open_set(les_y, set_y):
    ov = overview_btn()
    if ov: ct.bm_click(ov['h']); time.sleep(2); ct.close_popups(W)
    import nav
    nav.W = W
    nav.pick(0, les_y); time.sleep(1.5); nav.pick(1, set_y); time.sleep(1.2)
    ct.bm_click(start_btn()['h']); time.sleep(4);

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'learn':
        img = ct.shot(W)
        print(ct.learn(img, dict(a.split('=') for a in sys.argv[2:])))
        print(ct.read_board(img))
    elif cmd == 'learnimg':  # learnimg file.png e8=k ...
        from PIL import Image
        img = Image.open(sys.argv[2]).convert('RGB')
        print(ct.learn(img, dict(a.split('=') for a in sys.argv[3:]))); print(ct.read_board(img))
    elif cmd == 'reread':  # reread setname : recitește FEN-urile din imaginile salvate
        from PIL import Image
        d = json.load(open(f'sets/{sys.argv[2]}.json', encoding='utf-8'))
        for t in d['tasks']:
            for k in ('before', 'after'):
                img = Image.open(f"sets/img/{sys.argv[2]}_{t['i']}{'a' if k == 'before' else 'b'}.png").convert('RGB')
                rows, unk = ct.read_board(img); t[k]['fen'] = ct.fen_of(rows); t[k]['unk'] = unk
            print(t['i'], t['before']['fen'], t['before']['unk'], '->', t['after']['fen'], t['after']['unk'])
        json.dump(d, open(f'sets/{sys.argv[2]}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    elif cmd == 'read':
        img = ct.shot(W, sys.argv[2] if len(sys.argv) > 2 else None); print(ct.read_board(img), [t['t'] for t in ct.texts(W)])
    elif cmd == 'open':
        open_set(float(sys.argv[2]), float(sys.argv[3])); run(sys.argv[4])
    elif cmd == 'runhere':
        run(sys.argv[2])
