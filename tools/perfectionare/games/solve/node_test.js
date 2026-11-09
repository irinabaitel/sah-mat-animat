const fs=require('fs'),zlib=require('zlib');
const html=fs.readFileSync('C:/Users/irina/SahMatAnimat/nivel1_joc_vanatoarea_nebunului.html','utf8');
const common=fs.readFileSync(__dirname+'/../common.js','utf8').replace(/var snd[^\n]*\n/,'').replace(/function play[^\n]*\n/,'');
const core=html.split('/*CORE-START*/')[1].split('/*CORE-END*/')[0];
const api=new Function('TABDATA', common+core+';TAB=TABDATA;return {V,robotPick,moved,bishopHits,whiteHits,START,LIMIT,name,whiteMoves,bishopMoves};')(new Uint8Array(zlib.gunzipSync(fs.readFileSync('C:/Users/irina/SahMatAnimat/data/vanatoare_nebun.bin.gz'))));
const {V,robotPick,moved,bishopHits,START,LIMIT,name}=api;
console.log('V(start)=',V(START));
// Dragon vs Dragon
function game(rw,rb,rnd){let s=Object.assign({},START),n=0,line=[];
 while(true){const m=robotPick(s,'w',rw,rnd);n++;line.push(m[0]+name(m[2]));if(m[2]===s.b)return ['w',n,line];s=moved(s,m);
  if(n>=LIMIT)return['b-limit',n,line];const b=robotPick(s,'b',rb,rnd);line.push('B'+name(b[2]));if(['q','r','n'].some(p=>s[p]===b[2]))return['b-cap',n,line];s=moved(s,b);}}
for(let i=0;i<5;i++)console.log(JSON.stringify(game(0,0,Math.random)));
// Dragon white vs random bishops: must always win within V(start)
let worst=0;for(let i=0;i<3000;i++){const g=game(0,Math.random()<.5?0.9:0.2,Math.random);if(g[0]!=='w')console.log('FAIL',g);worst=Math.max(worst,g[1]);}
console.log('worst white moves vs any bishop',worst);
// Dragon bishop vs random white: bishop never loses unless white strong; count
let bw={};for(let i=0;i<2000;i++){const g=game(0.9,0,Math.random);bw[g[0]]=(bw[g[0]]||0)+1;}console.log('Pui alb vs Dragon nebun',bw);
bw={};for(let i=0;i<2000;i++){const g=game(0.2,0,Math.random);bw[g[0]]=(bw[g[0]]||0)+1;}console.log('Mânz alb vs Dragon nebun',bw);
bw={};for(let i=0;i<2000;i++){const g=game(0,0.9,Math.random);bw[g[1]]=(bw[g[1]]||0)+1;}console.log('Dragon alb vs Pui nebun, mutari',bw);
