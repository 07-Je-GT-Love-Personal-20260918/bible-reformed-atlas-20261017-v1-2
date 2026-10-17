const select=document.querySelector('#printCreed');
select.addEventListener('change',()=>{document.querySelectorAll('[data-creed]').forEach(article=>{article.hidden=select.value!=='all'&&article.dataset.creed!==select.value;});});
document.querySelector('#printButton').addEventListener('click',()=>window.print());
