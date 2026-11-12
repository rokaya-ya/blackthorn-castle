(()=>{'use strict';
const chapters=window.COMIC.chapters.slice().sort((a,b)=>a.n-b.n);
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const link=(c,p=1)=>`read.html#${c}/${p}`;
const title=c=>c.title||`Chapter ${String(c.n).padStart(2,'0')}`;
let saved=null;try{const raw=localStorage.getItem('bc-at')||('#'+(localStorage.getItem('bc-page')||''));const m=raw.match(/^#(?:(\d+)\/)?(\d+)$/);if(m){const ch=chapters.find(c=>c.n===Number(m[1]||1));const p=Number(m[2]);if(ch&&p>=1&&p<=ch.pages.length)saved={chapter:ch,page:p}}}catch{}
document.querySelector('#chapter-count').textContent=`${chapters.length} chapters · ${chapters.reduce((s,c)=>s+c.pages.length,0)} pages`;
const latest=chapters.at(-1);document.querySelector('#latest-link').href=link(latest.n);document.querySelector('#latest-label').textContent=`Latest · Chapter ${String(latest.n).padStart(2,'0')}`;
document.querySelector('#chapter-grid').innerHTML=chapters.map((c,i)=>`<a class="chapter-card" href="${link(c.n)}" aria-label="Read Chapter ${c.n}${c.title?': '+esc(c.title):''}"><div class="card-image"><img src="${esc(c.cover||`chapters/${c.n}/large/001.jpg`)}" width="1536" height="1024" alt="Artwork from Chapter ${c.n}" loading="lazy" decoding="async"><span class="card-number">${String(c.n).padStart(2,'0')}</span>${i===chapters.length-1?'<span class="card-badge">Latest chapter</span>':''}</div><div class="card-heading"><h3>${esc(title(c))}</h3><span aria-hidden="true">↗</span></div><div class="card-info"><span>${c.title?'Chapter '+String(c.n).padStart(2,'0')+' · ':''}${c.pages.length} story pages</span><span>${saved?.chapter.n===c.n?'Saved on page '+saved.page:'Read chapter'}</span></div></a>`).join('');
if(saved){const strip=document.querySelector('#continue');strip.hidden=false;document.querySelector('#continue-title').textContent=`Chapter ${saved.chapter.n} · Page ${saved.page}`;document.querySelector('#continue-link').href=link(saved.chapter.n,saved.page);const resume=document.querySelector('#hero-continue');resume.hidden=false;resume.href=link(saved.chapter.n,saved.page)}
})();
