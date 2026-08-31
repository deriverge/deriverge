import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const SP='/tmp/claude-0/-home-user-deriverge/1455238e-1fdf-569a-95ff-a73d887ca0a6/scratchpad';
const b=await chromium.launch();
const JOBS=[
  ['feature',1024,500,1],['shot67',645,1398,2],['shotipad',1024,1366,2],['shotplay',540,960,2]
];
for(const lang of ['cs','en']){
  for(const [mode,w,h,dsf] of JOBS){
    const c=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:dsf});
    const p=await c.newPage();
    await p.goto(`file://${SP}/promo/promo.html?lang=${lang}&mode=${mode}&still=1`);
    await p.evaluate(()=>document.fonts&&document.fonts.ready);
    await p.waitForTimeout(600);
    await p.screenshot({path:`${SP}/promo/pair-${mode}-${lang}.png`});
    await c.close();
  }
}
await b.close();
console.log('hotovo');
