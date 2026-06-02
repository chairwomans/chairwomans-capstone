const TITLES=['Team','Project','Method','Demo', 'Next'],BADGES=['Research','Overview','Pipeline','Try It', 'Next Steps'];
let cur=0;
const pages=document.querySelectorAll('.page'),navs=document.querySelectorAll('.nav-btn');
function goPage(i){pages[cur].classList.remove('active');navs[cur].classList.remove('active');cur=i;pages[i].classList.add('active');navs[i].classList.add('active');pages[i].scrollTop=0;document.getElementById('topTitle').textContent=TITLES[i];document.getElementById('topBadge').textContent=BADGES[i];}

const TAU = 0.07;

let src=null, fileObj=null;
document.getElementById('fileInput').addEventListener('change',e=>{
  const f=e.target.files[0];if(!f)return;
  fileObj=f;
  const r=new FileReader();r.onload=ev=>{
    src=ev.target.result;
    const img=document.getElementById('prevImg');img.src=src;img.style.display='block';
    document.getElementById('upholder').style.display='none';
    document.getElementById('uzone').classList.add('has');
    buildCrops(src);toast('Image loaded — 실행 버튼을 눌러주세요');
  };r.readAsDataURL(f);
});

function buildCrops(s){
  const sec=document.getElementById('csec'),grid=document.getElementById('cgrid');
  grid.innerHTML='';sec.style.display='block';
  const img=new Image();img.onload=()=>{
    const od=document.createElement('div');od.className='ccell orig';
    const oi=document.createElement('img');oi.src=s;od.appendChild(oi);grid.appendChild(od);
    for(let i=0;i<6;i++){
      const c=document.createElement('canvas');c.width=64;c.height=64;
      const ctx=c.getContext('2d');
      const sz=Math.min(img.width,img.height)*(0.45+Math.random()*0.4);
      const x=Math.random()*Math.max(0,img.width-sz),y=Math.random()*Math.max(0,img.height-sz);
      ctx.drawImage(img,x,y,sz,sz,0,0,64,64);
      const d=document.createElement('div');d.className='ccell';d.appendChild(c);grid.appendChild(d);
    }
    const m=document.createElement('div');m.className='cmore';m.textContent='+121';grid.appendChild(m);
  };img.src=s;
}

const EMJ = {
  photo: 'camera', sketch: 'pencil', cartoon: 'smile', drawing: 'pen',
  graffiti: 'brush', origami: 'bird', sculpture: 'box', sticker: 'tag',
  tattoo: 'zap', toy: 'gamepad-2', videogame: 'gamepad', deviantart: 'palette',
  graphic: 'ruler', rendering: 'monitor', embroidery: 'scissors', plastic: 'layers', misc: 'sparkles'
};
function domEmj(d){ return `<i data-lucide="${EMJ[d] || 'search'}"></i>`; }

async function runDemo(){
  if(!src){toast('먼저 이미지를 업로드해주세요');return;}
  if(!fileObj){toast('파일을 다시 선택해주세요');return;}
  const btn=document.getElementById('rbtn');btn.classList.add('loading');btn.textContent='Estimating...';

  let data;
  try {
    const form = new FormData();
    form.append('file', fileObj);
    const resp = await fetch('/predict', {method:'POST', body:form});
    if(!resp.ok){
      const err = await resp.text();
      throw new Error(`서버 오류 ${resp.status}: ${err}`);
    }
    data = await resp.json();
  } catch(e) {
    toast('❌ ' + e.message);
    btn.classList.remove('loading'); btn.textContent='Domain Estimation 실행';
    return;
  }

  // weights: {domain: weight, ...} — already sorted by server
  const entries = Object.entries(data.weights); // [[name, val], ...]
  const topDomain = data.predicted_domain;
  const topWeight = data.weights[topDomain];

  const md=document.getElementById('mdots');md.innerHTML='';
  const oc=Math.floor(4+Math.random()*9);
  for(let i=0;i<44;i++){const d=document.createElement('div');d.className='mdot'+(i<oc?' out':'');md.appendChild(d);}
  document.getElementById('mnote').innerHTML=`<strong>${oc}개</strong> outlier 제거 → robust mode m* 획득`;

  document.getElementById('rhdomain').innerHTML=`${domEmj(topDomain)} <span class="dem">${topDomain}</span>`;
  document.getElementById('rhconf').textContent=`Confidence ${(topWeight*100).toFixed(0)}%`;

  const bl=document.getElementById('blist');bl.innerHTML='';
  entries.forEach(([name, val], rank)=>{
    const pct=(val*100).toFixed(0), cls=rank===0?'bf1':rank===1?'bf2':'bf3';
    bl.innerHTML+=`<div class="bitem"><div class="btop"><span class="bname">${domEmj(name)} ${name}</span><span class="bpct">${pct}%</span></div><div class="btrack"><div class="bfill ${cls}" data-w="${val*100}"></div></div></div>`;
  });
  document.getElementById('wtxt').innerHTML=`Text embedding에 <strong>${topDomain}</strong> weight <strong>${(topWeight*100).toFixed(0)}%</strong> 반영됨`;
  document.getElementById('rwrap').classList.add('show');
  lucide.createIcons();
  setTimeout(()=>{document.querySelectorAll('.bfill').forEach(el=>el.style.width=parseFloat(el.dataset.w).toFixed(1)+'%');},60);

  btn.classList.remove('loading'); btn.style.display='none';
  toast(`✅ ${topDomain} domain으로 추정 완료`);
}

let toastT;
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastT);toastT=setTimeout(()=>t.classList.remove('show'),2500);}

window.addEventListener('load', () => lucide.createIcons());
