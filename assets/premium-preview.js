(() => {
  const shell=document.querySelector('.stage-shell');
  const canvas=document.getElementById('preview');
  if(!shell||!canvas)return;
  if(!shell.id)shell.id='stageShell';
  if(!shell.querySelector('.preview-badge')){
    const badge=document.createElement('div');
    badge.className='preview-badge';
    badge.textContent='Live preview';
    shell.appendChild(badge);
  }
  const motionOK=!window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const enabled=()=>document.getElementById('premiumPreview')?.checked!==false;
  function tilt(x,y){
    if(!motionOK||!enabled())return;
    const r=shell.getBoundingClientRect();
    const nx=Math.max(0,Math.min(1,(x-r.left)/r.width));
    const ny=Math.max(0,Math.min(1,(y-r.top)/r.height));
    shell.style.setProperty('--tilt-x',((.5-ny)*5.2).toFixed(2)+'deg');
    shell.style.setProperty('--tilt-y',((nx-.5)*6.4).toFixed(2)+'deg');
    shell.style.setProperty('--shine-x',(nx*100).toFixed(1)+'%');
    shell.style.setProperty('--shine-y',(ny*100).toFixed(1)+'%');
    shell.classList.add('preview-active');
  }
  function reset(){
    shell.style.setProperty('--tilt-x','0deg');
    shell.style.setProperty('--tilt-y','0deg');
    shell.style.setProperty('--shine-x','50%');
    shell.style.setProperty('--shine-y','35%');
    shell.classList.remove('preview-active','preview-dragging');
  }
  function syncToggle(){
    const on=enabled();
    shell.classList.toggle('premium-preview-off',!on);
    const badge=shell.querySelector('.preview-badge');if(badge)badge.style.display=on?'':'none';
    if(!on)reset();
  }
  shell.addEventListener('pointerenter',e=>tilt(e.clientX,e.clientY));
  shell.addEventListener('pointermove',e=>tilt(e.clientX,e.clientY));
  shell.addEventListener('pointerleave',reset);
  shell.addEventListener('pointerdown',()=>{if(enabled())shell.classList.add('preview-dragging')});
  shell.addEventListener('pointerup',()=>shell.classList.remove('preview-dragging'));
  shell.addEventListener('pointercancel',()=>shell.classList.remove('preview-dragging'));
  document.addEventListener('change',e=>{if(e.target?.id==='premiumPreview')syncToggle()});
  setTimeout(syncToggle,0);
})();
