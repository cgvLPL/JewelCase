(() => {
  const $=id=>document.getElementById(id);
  const effects=$('effectsSection');
  if(effects){
    effects.querySelector('.section-title').textContent='Physical effects';
    const hint=effects.querySelector('.sticker-hint');
    if(hint)hint.textContent='Three independent effects. Enable any combination; all are included in export.';
    const rows=[
      ['sealed','Sealed wrap','Shrink-wrap sheen, seams and subtle wrinkles','Wrap strength','sealedStrength','sealedStrengthVal','▱'],
      ['glitter','Glitter','Multicolour sparkle flecks and light-catching glints','Glitter amount','glitterStrength','glitterStrengthVal','✦'],
      ['cracks','Cracked case','Branching fractures across the clear plastic shell','Crack amount','crackStrength','crackStrengthVal','⌁']
    ];
    const grid=document.createElement('div');grid.className='feature-grid';
    rows.forEach(([id,title,desc,label,rangeId,valId,icon])=>{
      const input=$(id),range=$(rangeId),value=$(valId);if(!input||!range||!value)return;
      const card=document.createElement('div');card.className='feature-card';card.dataset.featureCard=id;
      card.innerHTML=`<div class="feature-card-head"><div class="feature-meta"><div class="feature-icon">${icon}</div><div class="feature-copy"><strong>${title}</strong><span>${desc}</span></div></div></div><div class="control"><div class="control-head"><label>${label}</label></div></div>`;
      const head=card.querySelector('.feature-card-head');
      const oldSwitch=input.closest('.switch');if(oldSwitch)head.appendChild(oldSwitch);
      const control=card.querySelector('.control');
      const ch=control.querySelector('.control-head');ch.appendChild(value);
      control.appendChild(range);
      grid.appendChild(card);
    });
    [...effects.querySelectorAll('.toggle-row,.control')].forEach(el=>{if(el.parentElement===effects)el.remove()});
    effects.appendChild(grid);
  }

  const labels=$('labelsSection');
  if(labels){
    const hint=labels.querySelector('.sticker-hint');
    if(hint)hint.textContent='Enable a sticker, then drag it directly on the preview to reposition it.';
  }

  if(!$('previewSection')&&effects){
    const section=document.createElement('section');section.className='section';section.id='previewSection';
    section.innerHTML='<div class="section-title">Live preview</div><div class="feature-card" data-feature-card="premiumPreview"><div class="feature-card-head"><div class="feature-meta"><div class="feature-icon">◇</div><div class="feature-copy"><strong>Premium motion</strong><span>3D tilt, moving shine, stage glow and depth</span></div></div><label class="switch"><input id="premiumPreview" type="checkbox" checked><span class="slider"></span></label></div><div class="preview-note">Presentation-only. This changes the interactive preview, not the exported artwork.</div></div>';
    effects.insertAdjacentElement('afterend',section);
  }

  const nav=document.querySelector('.mobile-tool-nav');
  if(nav&&!nav.querySelector('[data-target="effectsSection"]')){
    const labelsBtn=nav.querySelector('[data-target="labelsSection"]');
    const b=document.createElement('button');b.type='button';b.dataset.target='effectsSection';b.innerHTML='<span>✦</span>Effects';
    if(labelsBtn)nav.insertBefore(b,labelsBtn);else nav.appendChild(b);
    b.addEventListener('click',()=>{[...nav.querySelectorAll('button')].forEach(x=>x.classList.toggle('active',x===b));effects?.scrollIntoView({behavior:'smooth',block:'start'});});
  }

  function syncCards(){document.querySelectorAll('[data-feature-card]').forEach(card=>{const el=$(card.dataset.featureCard);card.classList.toggle('is-on',!!el?.checked);});}
  ['sealed','glitter','cracks','premiumPreview'].forEach(id=>$(id)?.addEventListener('change',syncCards));
  syncCards();
})();
