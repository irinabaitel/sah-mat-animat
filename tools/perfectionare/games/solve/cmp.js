const fs=require('fs'),zlib=require('zlib');
const html=fs.readFileSync('C:/Users/irina/SahMatAnimat/nivel1_joc_vanatoarea_nebunului.html','utf8');
const common=fs.readFileSync(__dirname+'/../common.js','utf8').replace(/var snd[^\n]*\n/,'').replace(/function play[^\n]*\n/,'');
const core=html.split('/*CORE-START*/')[1].split('/*CORE-END*/')[0];
const {V}=new Function('T', common+core+';TAB=T;return {V};')(new Uint8Array(zlib.gunzipSync(fs.readFileSync('C:/Users/irina/SahMatAnimat/data/vanatoare_nebun.bin.gz'))));
let bad=0;for(const [q,r,n,b,v] of JSON.parse(fs.readFileSync(__dirname+'/samp.json')))if(V({q,r,n,b})!==v)bad++;console.log('mismatch',bad);
