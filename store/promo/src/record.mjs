import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
const SP='/tmp/claude-0/-home-user-deriverge/1455238e-1fdf-569a-95ff-a73d887ca0a6/scratchpad';
const FF=`${SP}/ff/node_modules/ffmpeg-static/ffmpeg`;
const b=await chromium.launch();
const JOBS=[
  ['cs',1080,1920,'tapkasa-spot-cs-1080x1920'],
  ['en',1080,1920,'tapkasa-spot-en-1080x1920'],
  ['cs',1920,1080,'tapkasa-spot-cs-1920x1080'],
  ['en',1920,1080,'tapkasa-spot-en-1920x1080'],
];
for(const [lang,w,h,name] of JOBS){
  const dir=`${SP}/promo/rec-${name}`;
  fs.rmSync(dir,{recursive:true,force:true});
  const t0=Date.now();
  const c=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:1,
    recordVideo:{dir,size:{width:w,height:h}}});
  const p=await c.newPage();
  await p.goto(`file://${SP}/promo/ad.html?lang=${lang}`);
  await p.evaluate(()=>document.fonts&&document.fonts.ready);
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
  await p.waitForTimeout(400);
  const tGo=Date.now();
  await p.evaluate(()=>window.__go());
  await p.waitForTimeout(25900);
  await c.close();
  const webm=fs.readdirSync(dir).find(f=>f.endsWith('.webm'));
  const off=((tGo-t0)/1000).toFixed(2);
  execFileSync(FF,['-y','-hide_banner','-loglevel','error',
    '-ss',off,'-i',`${dir}/${webm}`,'-i',`${SP}/promo/music.wav`,
    '-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','20',
    '-pix_fmt','yuv420p','-r','30','-t','25.8','-c:a','aac','-b:a','160k',
    '-movflags','+faststart',`${SP}/promo/${name}.mp4`]);
  console.log(name, 'offset', off, '->', Math.round(fs.statSync(`${SP}/promo/${name}.mp4`).size/1024), 'KB');
}
await b.close();
