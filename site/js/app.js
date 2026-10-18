(()=>{const R=document.body.dataset.root||'';const $=s=>document.querySelector(s);
const tb=$('#theme');tb&&tb.addEventListener('click',()=>{const t=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=t;localStorage.setItem('vu-theme',t)});
const mb=$('#menu');mb&&mb.addEventListener('click',()=>$('#nav').classList.toggle('open'));
// search
const q=$('#q'),box=$('#sr');let data=null,sel=-1;
const norm=s=>(s||'').toLowerCase().replace(/ё/g,'е').replace(/[«»"“”().,:;!?/\\-]/g,' ');
async function load(){if(data)return data;const r=await fetch(R+'search.json');data=(await r.json()).map(d=>({...d,nt:norm(d.t),ne:norm(d.e),ns:norm(d.s)}));return data}
function stem(w){return w.length>5?w.slice(0,w.length-2):w.length>4?w.slice(0,w.length-1):w}
function search(v){const ws=norm(v).split(/\s+/).filter(Boolean).map(stem);if(!ws.length)return[];
 return data.map(d=>{let sc=0;for(const w of ws){let s=0;if(d.nt.includes(w))s=d.nt.startsWith(w)?12:8;else if(d.ne.includes(w))s=6;else if(d.ns.includes(w))s=2;if(!s)return null;sc+=s}
 if(d.k==='Раздел')sc+=1;return{d,sc}}).filter(Boolean).sort((a,b)=>b.sc-a.sc).slice(0,12).map(x=>x.d)}
function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function render(list,v){sel=-1;if(!v){box.hidden=true;return}
 box.innerHTML=list.length?list.map(d=>`<a href="${R}${d.u}"><span class="k">${esc(d.k)}</span> ${esc(d.t)}${d.e?` <small>${esc(d.e)}</small>`:''}<small>${esc(d.s.slice(0,110))}…</small></a>`).join(''):'<a>Ничего не найдено. Попробуйте другое слово.</a>';box.hidden=false}
if(q){q.addEventListener('focus',load);q.addEventListener('input',async()=>{await load();render(search(q.value),q.value.trim())});
 q.addEventListener('keydown',e=>{const a=[...box.querySelectorAll('a[href]')];if(!a.length)return;
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();sel=(sel+(e.key==='ArrowDown'?1:-1)+a.length)%a.length;a.forEach((x,i)=>x.classList.toggle('sel',i===sel))}
  if(e.key==='Enter'){(a[sel]||a[0]).click()}if(e.key==='Escape'){box.hidden=true}});
 document.addEventListener('click',e=>{if(!e.target.closest('.search'))box.hidden=true});
 const p=new URLSearchParams(location.search).get('q');if(p){q.value=p;load().then(()=>render(search(p),p))}}
// guide filters
const gf=$('#gf');if(gf)gf.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;gf.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));const l=b.dataset.l;
 document.querySelectorAll('.gcard').forEach(c=>c.style.display=(l==='0'||c.dataset.level===l)?'':'none');
 document.querySelectorAll('.gcat').forEach(h=>{const g=h.nextElementSibling;const any=[...g.children].some(c=>c.style.display!=='none');h.style.display=g.style.display=any?'':'none'})});
if('serviceWorker' in navigator&&location.protocol==='https:')navigator.serviceWorker.register(R+'sw.js').catch(()=>{});
})();
