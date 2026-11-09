# Arena de pat: pozitii din Chess Tutor Step 2, lectia P6 Stalemate (seturile b-f)
import json, chess, sys, os
sys.stdout.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__))
RO={'K':'R','Q':'D','R':'T','B':'N','N':'C'}
def ro(san): return ''.join(RO.get(c,c) for c in san)
A=json.load(open(os.path.join(HERE,'sets/S2P6_arena.json'),encoding='utf-8'))
SIDE={'w':'albul','b':'negrul'}
TXT={
 'b1':'Un șah foarte bun. La mutarea următoare albul tot poate captura dama.',
 'b2':'Un șah foarte bun. La mutarea următoare albul tot poate captura dama.',
 'b3':'Turnul e apărat, iar nebunul a fost pus la adăpost.',
 'b4':'Albul nu dă pat: calul negru încă poate muta.',
 'b5':'Nebunul e apărat pe f6.',
 'b6':'Albul poate captura nebunul, dar atunci calul capturează pionul c7. Pericolul de pat a trecut.',
 'b7':'Un șah foarte bun. Pericolul de pat a trecut.',
 'b8':'Negrul trebuie să captureze nebunul, iar pionul alb trece mai departe.',
 'b9':'O mutare bună: albul câștigă.',
 'b10':'Un șah foarte bun. La mutarea următoare negrul tot poate captura dama.',
 'e1':'Un șah foarte bun. La mutarea următoare negrul tot poate captura dama.',
 'e2':'Nu contează dacă albul pierde calul. Turnul însă nu trebuie pierdut.',
 'e3':'Un șah foarte bun. La mutarea următoare (Nb7, Cb5+) albul tot poate captura nebunul.',
 'e4':'Pionul e acum apărat și mai târziu poate promova în damă. Promovarea imediată în damă sau în turn ar da pat. Dacă albul promovează în nebun, negrul câștigă o piesă (Rg7), iar doi cai singuri nu pot da mat.',
 'e5':'Albul tot poate captura pionul la mutarea următoare.',
 'e6':'Negrul primește mat.',
 'e7':'Foarte bine. După orice mutare a damei, turnul dă mat pe h1.',
 'e8':'Negrul primește mat în scurt timp.',
 'e9':'Amenințarea de mat pe h1 hotărăște partida.',
 'e10':'Albul câștigă dama în schimbul unui turn.',
}
ORDER=[f'c{i}' for i in range(1,11)]+[f'b{i}' for i in range(1,11)]+[f'd{i}' for i in range(1,11)]+[f'e{i}' for i in range(1,11)]+['f2','f6','f9']
out=[]
for k in ORDER:
    v=A[k]; b=chess.Board(v['fen']); side=v['side']; me=SIDE[side]; opp=SIDE['b' if side=='w' else 'w']
    sans=[ro(s) for s in v['san']]
    if k[0] in 'cdf':
        assert v['final']=='stalemate', k
        kind='defend'
        # mutarea finala e a adversarului; dupa ea, eu sunt in pat
        last=sans[-1]
        expl=f'Corect. După {last}, {me} nu mai poate muta nicio piesă, dar regele nu e în șah: pat. {me.capitalize()} salvează partida.'
        if k=='f6': expl=f'Corect. După {last}, albul nu mai poate muta nicio piesă, dar regele nu e în șah: pat.'
    else:
        kind='avoid'
        # mutari tentante care dau pat imediat
        trap=[]
        for m in b.legal_moves:
            b.push(m); st=b.is_stalemate(); b.pop()
            if st: trap.append(ro(b.san(m)))
        expl=TXT[k]
        if len(trap)>2: expl+=' Atenție: aici multe mutări ar fi dat pat, de exemplu '+trap[0]+'.'
        elif trap: expl+=' Atenție: '+(' sau '.join(trap))+' ar fi dat pat.'
    lvl=1 if k[0]=='c' else (2 if k[0] in 'bd' else 3)
    out.append({'id':'CT2-P6-'+k,'fen':v['fen'],'moves':v['line'],'san':sans,'kind':kind,'level':lvl,'expl':expl,
                'src':'Chess Tutor Step 2, lecția P6'})
    print(k,kind,sans,'|',expl)
json.dump(out,open(os.path.join(HERE,'../../data/stalemate_arena.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
