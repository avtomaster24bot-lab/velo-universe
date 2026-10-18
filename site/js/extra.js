(()=>{const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const norm=s=>(s||'').toLowerCase().replace(/ё/g,'е');
// troubleshooting filter
const tf=$('#tf'),tq=$('#tq');
function apply(){const c=(tf&&tf.querySelector('.on')||{}).dataset?.c||'all';const ws=norm(tq?tq.value:'').split(/\s+/).filter(Boolean).map(w=>w.length>5?w.slice(0,-2):w);
 let n=0;$$('.tcard').forEach(e=>{const t=e.dataset.t||(e.dataset.t=norm(e.textContent));const ok=(c==='all'||e.dataset.c===c)&&ws.every(w=>t.includes(w));e.hidden=!ok;if(ok)n++});
 const o=$('#tn');if(o)o.textContent=n?`Найдено: ${n}`:'Ничего не найдено — попробуйте другое слово или общий поиск вверху.'}
if(tf){tf.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;tf.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));apply()});
 tq&&tq.addEventListener('input',apply);if(location.hash){const el=document.getElementById(location.hash.slice(1));if(el&&el.tagName==='DETAILS')el.open=true}apply()}
// maintenance checklist
const K='vu-maint';if($('.mcheck')){let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
 $$('.mcheck input[type=checkbox]').forEach(b=>{b.checked=!!st[b.id];b.addEventListener('change',()=>{st[b.id]=b.checked;localStorage.setItem(K,JSON.stringify(st))})});
 const pr=$('#mprint');pr&&pr.addEventListener('click',()=>window.print());
 const rs=$('#mreset');rs&&rs.addEventListener('click',()=>{st={};localStorage.removeItem(K);$$('.mcheck input[type=checkbox]').forEach(b=>b.checked=false)})}
})();
