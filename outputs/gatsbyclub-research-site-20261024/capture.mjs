import {chromium} from '/Users/olivialee/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import fs from 'node:fs/promises';
const base=decodeURIComponent(new URL('.',import.meta.url).pathname);const browser=await chromium.launch({headless:true,channel:'chrome'});const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});let results=[];
for(const [id,url] of [['founder','https://founderfeast.com/how-it-works'],['owr','https://www.otherwayround.travel/mexico-city-4-days/'],['offline','https://www.theoffline-club.com/']]){
 try{await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});await page.waitForTimeout(2500);await page.screenshot({path:base+'dist/assets/'+id+'-website.jpg',type:'jpeg',quality:85});results.push({id,url,final_url:page.url(),title:await page.title(),captured_at:new Date().toISOString(),screenshot:'assets/'+id+'-website.jpg'});}catch(e){results.push({id,url,error:e.message})}await page.waitForTimeout(1800);
}
await fs.writeFile(base+'assets-sources.json',JSON.stringify(results,null,2));await browser.close();console.log(JSON.stringify(results));
