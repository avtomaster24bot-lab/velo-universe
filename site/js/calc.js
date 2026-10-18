(()=>{const $=id=>document.getElementById(id);const v=id=>parseFloat(String($(id).value).replace(',','.'));
const BSD={203:'12"',305:'16" (детские)',349:'16 × 1 3/8" (Brompton)',406:'20" (BMX, складные)',451:'20 × 1 1/8"–1 3/8"',507:'24" (МТБ)',540:'24 × 1 3/8" (японские городские)',559:'26" (МТБ)',571:'650C / 26 × 1"',584:'650B / 27,5"',590:'26 × 1 3/8" (650A, японские городские)',597:'26 × 1 1/4" (старые британские)',622:'700C / 29" / 28"',630:'27 × 1 1/4" (японские 27")',635:'28 × 1 1/2" (старые дорожные)'};
const FR={622:'700',584:'650',571:'650',590:'650'},FL={622:'C',584:'B',571:'C',590:'A'};
function fillBSD(id,def){const s=$(id);if(!s)return;s.innerHTML=Object.entries(BSD).map(([k,n])=>`<option value="${k}"${+k===def?' selected':''}>${k} мм — ${n}</option>`).join('')}
['t_bsd','g_bsd','p_bsd'].forEach(i=>fillBSD(i,622));
const f=(x,d=1)=>Number.isFinite(x)?x.toFixed(d).replace('.',','):'—';
function tyre(){const b=v('t_bsd'),w=v('t_w');const od=b+2*w,c=Math.PI*od;let fr=FR[b]?`${FR[b]}×${Math.round(w)}${FL[b]}`:'—';
 $('t_out').innerHTML=`ETRTO: <b>${Math.round(w)}-${b}</b> · дюймовое обозначение: <b>${BSD[b]}</b> · французское: <b>${fr}</b><br>Наружный диаметр ≈ <b>${f(od,0)} мм</b> (${f(od/25.4,1)}″), длина окружности ≈ <b>${f(c,0)} мм</b> <span class="disc">(расчёт приблизительный: реальная высота шины зависит от модели и давления)</span>`}
function nums(id){return String($(id).value).split(/[^0-9]+/).map(Number).filter(x=>x>0)}
function gear(){const rings=nums('g_rings'),cogs=nums('g_cogs'),b=v('g_bsd'),w=v('g_w'),cad=v('g_cad');const D=b+2*w,circ=Math.PI*D/1000;
 if(!rings.length||!cogs.length){$('g_out').innerHTML='Введите числа зубьев';return}
 let h='<table class="ctab"><thead><tr><th>Задняя звезда</th>'+rings.map(r=>`<th>${r} зуб.: отношение / gear inches / развитие / скорость</th>`).join('')+'</tr></thead><tbody>';
 for(const c of cogs){h+=`<tr><td><b>${c}</b></td>`+rings.map(r=>{const g=r/c;return `<td>${f(g,2)} / ${f(g*D/25.4,1)}″ / ${f(g*circ,2)} м / <b>${f(g*circ*cad*60/1000,1)} км/ч</b></td>`}).join('')+'</tr>'}
 $('g_out').innerHTML=h+'</tbody></table><p class="disc">Скорость — при каденсе '+cad+' об/мин; диаметр колеса взят приблизительно (обод + 2 высоты шины).</p>'}
function chain(){const C=v('c_cs')/25.4,F=v('c_f'),R=v('c_r');const L=2*C+F/4+R/4+1;let links=Math.ceil(L*2);if(links%2)links++;
 $('c_out').innerHTML=`Длина ≈ <b>${f(L,1)}″</b> → около <b>${links}</b> звеньев (шагов по 1/2″, округлено вверх до чётного) <p class="disc">Формула Park Tool: L = 2·C + F/4 + R/4 + 1 (в дюймах), C — длина нижних перьев (от центра каретки до оси). Подходит для жёстких рам с задним переключателем; для двухподвесов, систем SRAM Eagle и планетарных втулок используйте метод производителя. Перед укорачиванием проверьте длину по методу «большая звезда + большая звезда»: <a href="../guides/chain-wear/">инструкция</a>.</p>`}
function spoke(){const E=v('s_erd'),P=v('s_pcd'),N=v('s_n'),k=v('s_x'),h=v('s_h');const a=(4*Math.PI*k)/N;
 const L=w=>Math.sqrt((P/2)**2+(E/2)**2+w**2-2*(P/2)*(E/2)*Math.cos(a))-h/2;
 const l=L(v('s_wl')),r=L(v('s_wr'));$('s_out').innerHTML=`Левая сторона: <b>${f(l,1)} мм</b> · правая сторона: <b>${f(r,1)} мм</b><p class="disc">Стандартная формула: L = √(r² + R² + w² − 2·r·R·cos(720°·k/N)) − d/2, где R = ERD/2, r = диаметр фланца/2, w — расстояние от центра втулки до фланца, k — число крестов, N — число спиц в колесе, d — диаметр отверстия во фланце. Спицы обычно продаются с шагом 1–2 мм; сверьте результат с калькулятором производителя обода/втулки и измерьте ERD сами.</p>`}
function pressure(){const w=v('p_w'),kg=v('p_kg'),srf=$('p_s').value,tl=$('p_tl').checked;
 const T=[[25,5.5,7],[28,5,6.5],[32,4,5.5],[38,3.2,4.5],[45,2.6,3.6],[52,2,3],[58,1.6,2.3],[66,1.3,1.9],[80,0.8,1.4],[200,0.4,0.9]];
 let row=T.find(t=>w<=t[0])||T[T.length-1];let k=1+((kg-75)/10)*0.05;k=Math.min(1.35,Math.max(0.75,k));
 const sf={asphalt:1,gravel:0.85,trail:0.78,snow:0.6}[srf];const t=tl?0.9:1;const lo=row[1]*k*sf*t,hi=row[2]*k*sf*t;
 $('p_out').innerHTML=`Ориентир: <b>${f(lo,1)}–${f(hi,1)} bar</b> (${f(lo*14.5,0)}–${f(hi*14.5,0)} psi)<p class="disc"><b>Это очень приблизительная подсказка</b>, а не норма. Всегда оставайтесь в пределах давления, указанного на боковине покрышки и на ободе (у бескамерных ободов свой максимум). Начните с середины диапазона и подбирайте по ощущениям: слишком низкое давление — «змеиный укус» и удары обода, слишком высокое — тряска и плохое сцепление.</p>`}
const calcs={tyre:[['t_bsd','t_w'],tyre],gear:[['g_rings','g_cogs','g_bsd','g_w','g_cad'],gear],chain:[['c_cs','c_f','c_r'],chain],spoke:[['s_erd','s_pcd','s_wl','s_wr','s_n','s_x','s_h'],spoke],pressure:[['p_w','p_kg','p_s','p_tl','p_bsd'],pressure]};
for(const [ids,fn] of Object.values(calcs)){if(!$(ids[0]))continue;ids.forEach(i=>$(i)&&$(i).addEventListener('input',fn));fn()}
})();
