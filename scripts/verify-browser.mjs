import {chromium} from '../.deploy/tools/node_modules/playwright/index.mjs';
import {createServer} from 'node:http';
import {readFile,mkdir} from 'node:fs/promises';
import {resolve,extname} from 'node:path';
const root=resolve('dist');
const server=createServer(async(req,res)=>{try{const file=resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname==='/'?'/index.html':new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+'\\')&&!file.startsWith(root+'/'))throw Error('path');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.png':'image/png'})[extname(file)]||'application/octet-stream');res.end(await readFile(file));}catch{res.statusCode=404;res.end('Not found');}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({headless:true});
let failures=[];
try{
 await mkdir('.deploy/screenshots',{recursive:true});
 for(const width of [360,390,768,1440]){
  const page=await browser.newPage({viewport:{width,height:900}});
  page.on('pageerror',e=>failures.push(`${width}: ${e.message}`));
  // External fonts are not required for offline layout validation.
  await page.route('https://fonts.googleapis.com/**',route=>route.abort());
  await page.route('https://fonts.gstatic.com/**',route=>route.abort());
  for(const route of ['/index.html','/study.html']){
   await page.goto(`http://127.0.0.1:${server.address().port}${route}`,{waitUntil:'load'});
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
   if(overflow)failures.push(`${width}${route}: horizontal overflow`);
   await page.locator('[data-year="722"]').click();
   if(!(await page.locator('#atlasNorth').innerText()).includes('王国已亡'))failures.push('722 fall mismatch');
   await page.locator('[data-year="516"]').click();
   if(!(await page.locator('#atlasSouth').innerText()).includes('归回'))failures.push('516 return mismatch');
   await page.locator('#atlasReset').click();
   await page.locator('#atlasPlay').click();
   await page.waitForFunction(()=>Number(document.querySelector('#atlasYearRange').value)>1);
   await page.locator('#atlasPlay').click();
   if(await page.locator('#atlasPlay').getAttribute('aria-pressed')!=='false')failures.push('pause failed');
   await page.locator('[data-route="return"]').click();
   if(!(await page.locator('#routeCaption').innerText()).includes('归回'))failures.push('map route failed');
   if(route==='/study.html'){
    await page.locator('#tocButton').click();
    if(await page.locator('#toc').isVisible())failures.push('toc hide failed');
    await page.locator('#tocButton').click();
    await page.locator('#reveal').click();
    if(!(await page.locator('#answer').isVisible()))failures.push('answer reveal failed');
   }
   await page.locator('#animated-atlas').screenshot({path:`.deploy/screenshots/${width}-${route.slice(1,-5)}.png`});
  }
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.locator('#routeReplay').click();
  if(await page.locator('#atlasPlay').getAttribute('aria-pressed')!=='false')failures.push('motion preference pause failed');
  await page.close();
 }
 console.log(JSON.stringify({widths:[360,390,768,1440],pages:2,failures},null,2));
 if(failures.length)process.exitCode=1;
}finally{await browser.close();await new Promise(r=>server.close(r));}
