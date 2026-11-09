import sys, time; sys.path.insert(0, '.')
import ct, nav, runset
W = nav.W
LES = {3: 193, 5: 231, 6: 250}
def open_set(les, y):
    runset.click_btn(1009, 186); time.sleep(2); ct.close_popups(W)
    nav.pick(0, LES[les]); time.sleep(1.5); nav.pick(1, y); time.sleep(1.2)
    runset.click_btn(1042, 850); time.sleep(4)
for spec in sys.argv[1:]:
    name, les, y = spec.split(',')
    open_set(int(les), float(y))
    print('=====', name, flush=True)
    runset.run(name)
