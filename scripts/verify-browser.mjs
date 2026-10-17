import {chromium} from '../.deploy/tools/node_modules/playwright/index.mjs';
import {createServer} from 'node:http';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {resolve,extname} from 'node:path';
const root=resolve('dist');
const server=createServer(async(req,res)=>{try{const path=new URL(req.url,'http://localhost').pathname;const file=resolve(root,'.'+decodeURIComponent(path==='/'?'/index.html':path));if(!file.startsWith(root+'\\')&&!file.startsWith(root+'/'))throw Error('path');res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.png':'image/png'})[extname(file)]||'application/octet-stream');res.end(await readFile(file));}catch{res.statusCode=404;res.end('Not found');}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({headless:true});
const failures=[],widths=[320,360,390,768,1024,1440,1920];
const expected=JSON.parse(await readFile('assets/creeds.json','utf8'));
const assert=(ok,message)=>{if(!ok)failures.push(message)};
try{
 await mkdir('.deploy/screenshots',{recursive:true});
 for(const width of widths){
  const page=await browser.newPage({viewport:{width,height:900}});
  page.on('pageerror',error=>failures.push(`${width}: ${error.message}`));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'load'});
  assert(await page.locator('.book-card').count()===66,`${width}: book count`);
  assert(await page.locator('.top-nav,.nav-inner').count()===0,`${width}: old quick links remain`);
  assert(await page.locator('#tocTree ul ul ul').count()>0,`${width}: multilevel toc absent`);
  assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),`${width}: overflow on initial view`);
  const overlap=await page.evaluate(()=>{const a=document.querySelector('#tocButton').getBoundingClientRect(),b=document.querySelector('.reader-settings').getBoundingClientRect();return a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;});
  assert(!overlap,`${width}: fixed controls overlap`);
  for(const c of expected){const actual=await page.locator(`#creed-${c.id} .creed-paragraphs p`).allTextContents();assert(JSON.stringify(actual)===JSON.stringify(c.paragraphs),`${width}: ${c.id} exact text mismatch`);}
  await page.locator('#tocButton').click();
  assert(await page.locator('#toc').isVisible()===(width<=900),`${width}: toc first toggle`);
  if(width<=900){
   await page.keyboard.press('Escape');assert(!await page.locator('#toc').isVisible(),`${width}: Escape close failed`);
   await page.locator('#tocButton').click();await page.locator('#tocClose').click();
  }else{await page.locator('#tocButton').click();}
  await page.locator('[data-year="722"]').click();assert((await page.locator('#atlasNorth').innerText()).includes('王国已亡'),`${width}: north fall`);
  await page.locator('[data-year="516"]').click();assert((await page.locator('#atlasSouth').innerText()).includes('归回'),`${width}: return era`);
  await page.locator('#atlasReset').click();await page.locator('#atlasPlay').click();
  await page.waitForFunction(()=>Number(document.querySelector('#atlasYearRange').value)>1);
  await page.locator('#atlasPlay').click();assert(await page.locator('#atlasPlay').getAttribute('aria-pressed')==='false',`${width}: pause failed`);
  await page.emulateMedia({reducedMotion:'reduce'});await page.locator('[data-route="return"]').click();
  assert((await page.locator('#routeCaption').innerText()).includes('归回'),`${width}: route failed`);
  await page.locator('#maskCreeds').click();assert(await page.locator('.creed-paragraphs p.masked').count()===25,`${width}: mask count`);
  await page.locator('#revealParagraph').click();assert(await page.locator('.creed-paragraphs p.masked').count()===24,`${width}: reveal count`);
  await page.locator('#restoreCreeds').click();assert(await page.locator('.masked').count()===0,`${width}: restore failed`);
  await page.locator('[data-filter="新约"]').click();assert(await page.locator('.book-card:visible').count()===27,`${width}: NT count`);
  await page.locator('#searchInput').fill('不存在的测试内容');assert(await page.locator('#noBooks').isVisible(),`${width}: empty result state`);
  await page.locator('#clearSearch').click();assert(await page.locator('.book-card:visible').count()===66,`${width}: clearing filter`);
  if(width<=900)await page.locator('#tocButton').click();
  const revelation=page.locator('#tocTree a[href="#book-66"]');
  await revelation.evaluate(el=>{let p=el.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}});
  await revelation.click();await page.waitForFunction(()=>document.activeElement?.id==='book-66');
  assert(await page.locator('#book-66').isVisible(),`${width}: deep toc navigation`);
  if(width<=900)assert(!await page.locator('#toc').isVisible(),`${width}: toc not closed after navigation`);
  await page.locator('#fontUp').click();await page.locator('#fontUp').click();
  assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),`${width}: overflow after font increase`);
  await page.locator('#themeToggle').click();assert(await page.locator('html').getAttribute('data-theme')==='dark',`${width}: dark theme`);
  await page.locator('#themeToggle').click();
  await page.locator('#reveal').click();assert(await page.locator('#answer').isVisible(),`${width}: recall reveal`);
  await page.locator('[data-review="today"]').click();assert(await page.locator('[data-review="today"]').getAttribute('aria-pressed')==='true',`${width}: review state`);
  await page.locator('#backTop').click();await page.locator('.reader-hero').screenshot({path:`.deploy/screenshots/v13-${width}-hero.png`});
  await page.goto(`http://127.0.0.1:${server.address().port}/creeds.html`);
  await page.locator('#printCreed').selectOption('nicene');assert(await page.locator('.creed-text:visible').count()===1,`${width}: print range`);
  assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),`${width}: clean page overflow`);
  for(const c of expected){assert(JSON.stringify(await page.locator(`#creed-${c.id} .creed-paragraphs p`).allTextContents())===JSON.stringify(c.paragraphs),`${width}: clean ${c.id} mismatch`);}
  if(width===1440){await page.emulateMedia({media:'print'});await page.pdf({path:'.deploy/screenshots/nicene-clean-v13.pdf',format:'A4',printBackground:true});}
  await page.close();
 }
 const page=await browser.newPage({viewport:{width:390,height:900}});page.on('pageerror',e=>failures.push(e.message));
 await page.goto(`http://127.0.0.1:${server.address().port}/study.html`);assert(await page.locator('.book-card').count()===66,'study alias missing main content');await page.close();
 const result={version:'1.3.0',widths,books:66,creeds:3,exactTextChecks:42,failures};
 await writeFile('.deploy/browser-verification.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));if(failures.length)process.exitCode=1;
}finally{await browser.close();await new Promise(r=>server.close(r));}
