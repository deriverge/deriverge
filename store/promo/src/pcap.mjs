import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const SP='/tmp/claude-0/-home-user-deriverge/1455238e-1fdf-569a-95ff-a73d887ca0a6/scratchpad';
const b=await chromium.launch();
const now=Date.now();
const mkState=(lang,mode)=>{
  const N=(cs,en)=>lang==='cs'?cs:en;
  const items=[
    {id:'a',name:'Espresso',price:lang==='cs'?50:2,color:'hneda'},
    {id:'b',name:'Cappuccino',price:lang==='cs'?70:3,color:'oranzova'},
    {id:'c',name:N('Caffe latte','Caffe latte'),price:lang==='cs'?80:3,color:'zluta'},
    {id:'d',name:'Flat white',price:lang==='cs'?85:3.5,color:'grafit'},
    {id:'e',name:N('Ledová káva','Iced coffee'),price:lang==='cs'?75:3,color:'nebeska'},
    {id:'f',name:N('Čaj','Tea'),price:lang==='cs'?40:1.5,color:'zelena'},
    {id:'g',name:N('Limonáda','Lemonade'),price:lang==='cs'?45:2,color:'limetka'},
    {id:'h',name:N('Koláč','Cake'),price:lang==='cs'?55:2.5,color:'ruzova'}
  ];
  const L=(n,p,q,r,c)=>({name:n,price:p,qty:q,ready:r,color:c});
  const sales=[
    {id:'s11',no:11,ts:now-420000,updatedAt:now-420000,method:'card',total:lang==='cs'?150:6.5,status:'open',
      lines:[L('Cappuccino',lang==='cs'?70:3,1,1,'oranzova'),L(items[4].name,lang==='cs'?75:3,1,0,'nebeska')]},
    {id:'s12',no:12,ts:now-60000,updatedAt:now-60000,method:'cash',total:lang==='cs'?170:7,status:'open',
      lines:[L('Espresso',lang==='cs'?50:2,2,1,'hneda'),L(items[2].name,lang==='cs'?80:3,1,0,'zluta')]}
  ];
  return {v:3,setup:true,event:N('Sobotní trh','Saturday market'),mode,nextNo:13,voice:true,pair:'KQ7RD',
    license:'pro',lang,currency:lang==='cs'?'CZK':'USD',payDay:'',payN:0,biz:'',
    items,order:mode==='kasa'?[{ref:'a',name:'Espresso',price:lang==='cs'?50:2,qty:2,color:'hneda'},{ref:'b',name:'Cappuccino',price:lang==='cs'?70:3,qty:1,color:'oranzova'}]:[],
    sales,archives:[]};
};
for(const lang of ['cs','en']){
  // iPad: Kasa, prodej s účtem
  const c1=await b.newContext({viewport:{width:1024,height:1366},deviceScaleFactor:2,isMobile:true,hasTouch:true,locale:lang});
  await c1.addInitScript(`try{localStorage.setItem('kasa.setupDone','1');localStorage.setItem('kavakasa.v1',${JSON.stringify(JSON.stringify(mkState(lang,'kasa')))})}catch(e){}`);
  const p1=await c1.newPage();
  await p1.goto('file:///home/user/deriverge/tapkasa/index.html');
  await p1.waitForTimeout(700);
  await p1.evaluate(()=>document.fonts&&document.fonts.ready);
  await p1.waitForTimeout(300);
  await p1.screenshot({path:`${SP}/promo/dev-ipad-${lang}.png`});
  await c1.close();
  // iPhone: Výdej, fronta
  const c2=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,locale:lang});
  await c2.addInitScript(`try{localStorage.setItem('kasa.setupDone','1');localStorage.setItem('kavakasa.v1',${JSON.stringify(JSON.stringify(mkState(lang,'vydej')))})}catch(e){}`);
  const p2=await c2.newPage();
  await p2.goto('file:///home/user/deriverge/tapkasa/index.html');
  await p2.waitForTimeout(700);
  await p2.evaluate(()=>document.fonts&&document.fonts.ready);
  await p2.waitForTimeout(300);
  await p2.screenshot({path:`${SP}/promo/dev-iphone-${lang}.png`});
  await c2.close();
}
await b.close();
console.log('zachyceno');
