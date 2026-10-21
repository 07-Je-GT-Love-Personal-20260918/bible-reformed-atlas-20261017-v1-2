/* Reading shell, memorization and local-only preferences. */
const $=selector=>document.querySelector(selector);
const $$=selector=>[...document.querySelectorAll(selector)];
const storage={get(key,fallback=null){try{return localStorage.getItem(key)??fallback}catch{return fallback}},set(key,value){try{localStorage.setItem(key,value)}catch{}}};
const mobile=matchMedia('(max-width: 900px)');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const toc=$('#toc'),tocButton=$('#tocButton'),scrim=$('#tocScrim');
let desktopOpen=storage.get('atlas-toc','open')!=='closed';
function setToc(open,{save=false,focus=false}={}){
 toc.hidden=!open;tocButton.setAttribute('aria-expanded',String(open));$('#tocLabel').textContent=open?'隐藏目录':'显示目录';
 document.body.classList.toggle('toc-closed',!open);document.body.classList.toggle('toc-open',open&&mobile.matches);scrim.hidden=!(open&&mobile.matches);
 if(mobile.matches){toc.setAttribute('role','dialog');toc.setAttribute('aria-modal',String(open));}else{toc.removeAttribute('role');toc.removeAttribute('aria-modal');}
 $('#main').inert=open&&mobile.matches;$('.reader-settings').inert=open&&mobile.matches;
 if(save&&!mobile.matches){desktopOpen=open;storage.set('atlas-toc',open?'open':'closed');}
 if(focus&&open&&mobile.matches)toc.querySelector('summary,a')?.focus();
}
setToc(mobile.matches?false:desktopOpen);
tocButton.addEventListener('click',()=>setToc(toc.hidden,{save:true,focus:true}));
scrim.addEventListener('click',()=>{setToc(false);tocButton.focus();});
$('#tocClose').addEventListener('click',()=>{setToc(false);tocButton.focus();});
mobile.addEventListener('change',()=>setToc(mobile.matches?false:desktopOpen));
document.addEventListener('keydown',event=>{
 if(!mobile.matches||toc.hidden)return;
 if(event.key==='Escape'){setToc(false);tocButton.focus();}
 if(event.key==='Tab'){
  const focusables=[...toc.querySelectorAll('a,summary,button')].filter(el=>el.getClientRects().length);
  const first=focusables[0],last=focusables.at(-1);
  if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
  else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
 }
});
function clearFilter(){if(!$('#searchInput').value&&activeFilter==='all')return;$('#searchInput').value='';activeFilter='all';updateBooks();}
toc.addEventListener('click',event=>{
 const link=event.target.closest('a[href^="#"]');if(!link)return;
 const target=$(link.getAttribute('href'));if(!target)return;event.preventDefault();
 clearFilter();if(mobile.matches)setToc(false);
 requestAnimationFrame(()=>{target.scrollIntoView({behavior:reduced.matches?'instant':'smooth',block:'start'});target.setAttribute('tabindex','-1');target.focus({preventScroll:true});});
});
let activeFilter='all';
const cards=$$('.book-card');
const cardTexts=new Map(cards.map(card=>[card,card.textContent.toLowerCase()]));
function updateBooks(){
 const query=$('#searchInput').value.trim().toLowerCase();let count=0;
 cards.forEach(card=>{const show=(!query||cardTexts.get(card).includes(query))&&(activeFilter==='all'||card.dataset.testament===activeFilter||card.dataset.tags.includes(activeFilter));card.hidden=!show;if(show)count++;});
 $$('.book-group').forEach(group=>group.hidden=![...group.querySelectorAll('.book-card')].some(card=>!card.hidden));
 $('#bookCount').textContent=`当前显示 ${count} / 66 卷`;$('#noBooks').hidden=count!==0;
 $$('.filter-btn').forEach(button=>{const selected=button.dataset.filter===activeFilter;button.classList.toggle('active',selected);button.setAttribute('aria-pressed',String(selected));});
}
let filterTimer;$('#searchInput').addEventListener('input',()=>{clearTimeout(filterTimer);filterTimer=setTimeout(updateBooks,100)});
$$('.filter-btn').forEach(button=>button.addEventListener('click',()=>{activeFilter=button.dataset.filter;updateBooks();}));
$('#clearSearch').addEventListener('click',clearFilter);
const tocLinks=$$('#tocTree a[href^="#"]');
const tocById=new Map(tocLinks.map(link=>[link.hash.slice(1),link]));
let currentLink;
const spy=new IntersectionObserver(entries=>{const visible=entries.filter(e=>e.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top);if(!visible.length)return;const link=tocById.get(visible[0].target.id);if(!link||link===currentLink)return;currentLink?.removeAttribute('aria-current');link.setAttribute('aria-current','location');currentLink=link;},{rootMargin:'-5% 0px -65% 0px',threshold:0});
for(const id of tocById.keys()){const el=document.getElementById(id);if(el)spy.observe(el);}
let progressScheduled=false,progressMax=0;
const cssProgress=CSS.supports('animation-timeline:scroll()')&&!reduced.matches;
function measureProgress(){progressMax=Math.max(1,document.documentElement.scrollHeight-innerHeight);updateProgress();}
function updateProgress(){if(!cssProgress)$('#readProgress').style.transform=`scaleX(${Math.min(1,Math.max(0,scrollY/progressMax))})`;progressScheduled=false;}
if(!cssProgress)addEventListener('scroll',()=>{if(!progressScheduled){progressScheduled=true;requestAnimationFrame(updateProgress)}},{passive:true});
new ResizeObserver(measureProgress).observe($('#main'));addEventListener('resize',measureProgress,{passive:true});
$('#backTop').addEventListener('click',()=>scrollTo({top:0,behavior:reduced.matches?'instant':'smooth'}));
let size=Math.min(22,Math.max(15,Number(storage.get('atlas-font','17'))||17));
function setSize(value){size=Math.min(22,Math.max(15,value));document.documentElement.style.setProperty('--body-size',`${size}px`);storage.set('atlas-font',String(size));$('#fontDown').disabled=size<=15;$('#fontUp').disabled=size>=22;}
$('#fontDown').addEventListener('click',()=>setSize(size-1));$('#fontUp').addEventListener('click',()=>setSize(size+1));setSize(size);
// Wording is never changed when masking or revealing creed paragraphs.
const paragraphs=$$('.creed-paragraphs p');
function maskState(){const masked=paragraphs.filter(p=>p.classList.contains('masked')).length;$('#maskCreeds').setAttribute('aria-pressed',String(masked>0));$('#creedStatus').textContent=masked?`已遮住 ${masked} 段。按“逐段揭示”，或点按单段进行核对。`:'全文已显示。背诵时先回忆结构，再核对原文。';}
$('#maskCreeds').addEventListener('click',()=>{const hide=!paragraphs.some(p=>p.classList.contains('masked'));paragraphs.forEach(p=>p.classList.toggle('masked',hide));maskState();});
$('#restoreCreeds').addEventListener('click',()=>{paragraphs.forEach(p=>p.classList.remove('masked'));maskState();});
$('#revealParagraph').addEventListener('click',()=>{const next=paragraphs.find(p=>p.classList.contains('masked'));if(next){next.classList.remove('masked');next.scrollIntoView({behavior:reduced.matches?'instant':'smooth',block:'center'});}maskState();});
paragraphs.forEach(p=>{p.addEventListener('click',()=>{p.classList.toggle('masked');maskState();});p.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();p.click();}});});
const speechAvailable='speechSynthesis' in window&&'SpeechSynthesisUtterance' in window;
function stopSpeech(){if(speechAvailable)speechSynthesis.cancel();$('#speakCreed').setAttribute('aria-pressed','false');}
$('#speakCreed').disabled=!speechAvailable;$('#stopSpeech').disabled=!speechAvailable;
if(!speechAvailable)$('#creedStatus').textContent='当前设备未提供系统语音，仍可阅读、遮文背诵。';
$('#speakCreed').addEventListener('click',()=>{stopSpeech();const section=$(`#creed-${$('#speechCreed').value}`);const utterance=new SpeechSynthesisUtterance([...section.querySelectorAll('.creed-paragraphs p')].map(p=>p.textContent).join('\n'));utterance.lang='zh-CN';utterance.rate=.85;const voice=speechSynthesis.getVoices().find(v=>v.lang.startsWith('zh'));if(voice)utterance.voice=voice;utterance.onend=stopSpeech;utterance.onerror=()=>{stopSpeech();$('#creedStatus').textContent='当前系统语音未能完成朗读，可继续使用文字背诵。';};speechSynthesis.speak(utterance);$('#speakCreed').setAttribute('aria-pressed','true');$('#creedStatus').textContent=`正在使用设备系统语音朗读《${section.querySelector('h3').textContent}》。`;});
$('#stopSpeech').addEventListener('click',stopSpeech);$('#speechCreed').addEventListener('change',stopSpeech);addEventListener('pagehide',stopSpeech);
let review;try{review=JSON.parse(storage.get('atlas-review','{}'))||{}}catch{review={}}
function showReview(){for(const button of $$('[data-review]')){const done=Boolean(review[button.dataset.review]);button.setAttribute('aria-pressed',String(done));button.textContent=button.textContent.replace(/^[○✓]/,done?'✓':'○');}}
$$('[data-review]').forEach(button=>button.addEventListener('click',()=>{review[button.dataset.review]=!review[button.dataset.review];storage.set('atlas-review',JSON.stringify(review));showReview();}));
$('#resetReview').addEventListener('click',()=>{review={};storage.set('atlas-review','{}');showReview();});showReview();
// Preserve readable map labels on phones within a deliberate horizontal viewport.
$$('#geography>svg,.motion-map').forEach(svg=>{const wrap=document.createElement('div');wrap.className='map-viewport';wrap.tabIndex=0;wrap.setAttribute('role','region');wrap.setAttribute('aria-label','地图，可横向滚动查看完整标签');svg.before(wrap);wrap.append(svg);});
// Make hashes into closed TOC branches reachable on direct page entry.
if(location.hash){const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target)requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}
updateBooks();measureProgress();
