# scrie data/vanatoare_nebun.bin.gz: V[dama în triunghiul a1-d1-d4][b][n][r], câte 4 biți; pozițiile „nu contează” (V=1 sau invalide) sunt umplute cu valoarea dinainte
import numpy as np, gzip
V=np.load(r'C:/Users/irina/AppData/Local/Temp/claude/5f5cca6ec2cb1060/57a79c16-0421-4278-82d3-fb32d3123bed/scratchpad/V.npy')
TRI=[f*8+r for f in range(4) for r in range(f+1)]
I=np.arange(64)
q4=I[:,None,None,None]; r4=I[None,:,None,None]; n4=I[None,None,:,None]; b4=I[None,None,None,:]
valid=(q4!=r4)&(q4!=n4)&(q4!=b4)&(r4!=n4)&(r4!=b4)&(n4!=b4)
dc=(V==1)|~valid
o=(0,3,2,1)
T=V[TRI].transpose(o).reshape(-1).copy(); D=dc[TRI].transpose(o).reshape(-1)
idx=np.where(~D,np.arange(len(T)),0); np.maximum.accumulate(idx,out=idx); F=T[idx]
nib=(F[0::2]|(F[1::2]<<4)).astype(np.uint8).tobytes()
open(r'C:/Users/irina/SahMatAnimat/data/vanatoare_nebun.bin.gz','wb').write(gzip.compress(nib,9,mtime=0))
print(len(nib))
