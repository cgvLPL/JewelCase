from pathlib import Path

p = Path('index.html')
s = p.read_text()

if 'id="effectsSection"' not in s:
    anchor = '''    <section class="section" id="labelsSection">'''
    effects = '''    <section class="section" id="effectsSection">
      <div class="section-title">Effects</div>
      <div class="sticker-hint">Layer optional physical and decorative effects over the jewel case.</div>
      <div class="toggle-row"><span>Sealed wrap</span><label class="switch"><input id="sealed" type="checkbox"><span class="slider"></span></label></div>
      <div class="control">
        <div class="control-head"><label for="sealedStrength">Wrap strength</label><span class="value" id="sealedStrengthVal"></span></div>
        <input id="sealedStrength" type="range" min="0" max="100" value="62" step="1">
      </div>
      <div class="toggle-row"><span>Glitter</span><label class="switch"><input id="glitter" type="checkbox"><span class="slider"></span></label></div>
      <div class="control">
        <div class="control-head"><label for="glitterStrength">Glitter amount</label><span class="value" id="glitterStrengthVal"></span></div>
        <input id="glitterStrength" type="range" min="0" max="100" value="45" step="1">
      </div>
      <div class="toggle-row"><span>Cracked case</span><label class="switch"><input id="cracks" type="checkbox"><span class="slider"></span></label></div>
      <div class="control">
        <div class="control-head"><label for="crackStrength">Crack amount</label><span class="value" id="crackStrengthVal"></span></div>
        <input id="crackStrength" type="range" min="0" max="100" value="52" step="1">
      </div>
    </section>

'''
    if anchor not in s:
        raise SystemExit('labels section anchor not found')
    s = s.replace(anchor, effects + anchor, 1)

old_state = "    grooves:true, scratches:true, titleSticker:false, advisory:false, priceSticker:false, barcode:false,\n    albumTitle:'', artistName:'', x:0, y:0,"
new_state = "    grooves:true, scratches:true, titleSticker:false, advisory:false, priceSticker:false, barcode:false,\n    sealed:false, sealedStrength:62, glitter:false, glitterStrength:45, cracks:false, crackStrength:52,\n    albumTitle:'', artistName:'', x:0, y:0,"
if old_state in s:
    s = s.replace(old_state, new_state, 1)
elif 'sealedStrength:62' not in s:
    raise SystemExit('state anchor not found')

old_controls = "    'grooves','scratches','titleSticker','advisory','priceSticker','barcode','albumTitle','artistName'"
new_controls = "    'grooves','scratches','titleSticker','advisory','priceSticker','barcode','sealed','sealedStrength','glitter','glitterStrength','cracks','crackStrength','albumTitle','artistName'"
if old_controls in s:
    s = s.replace(old_controls, new_controls, 1)
elif "'sealedStrength'" not in s:
    raise SystemExit('controls anchor not found')

sync_anchor = "    $('grainVal').textContent=state.grain+'%';"
sync_extra = """    $('grainVal').textContent=state.grain+'%';
    $('sealedStrengthVal').textContent=state.sealedStrength+'%';
    $('glitterStrengthVal').textContent=state.glitterStrength+'%';
    $('crackStrengthVal').textContent=state.crackStrength+'%';"""
if sync_anchor in s and "sealedStrengthVal').textContent" not in s:
    s = s.replace(sync_anchor, sync_extra, 1)

insert_before = "  function render(target=canvas,size=900){"
if 'function drawSealedWrap' not in s:
    funcs = r'''  function drawSealedWrap(c,S){
    if(!state.sealed || state.sealedStrength<=0)return;
    const k=Math.max(0,Math.min(1,state.sealedStrength/100));
    c.save();
    c.globalCompositeOperation='screen';
    const sheen=c.createLinearGradient(S*.08,S*.03,S*.94,S*.94);
    sheen.addColorStop(0,`rgba(255,255,255,${.055+.075*k})`);
    sheen.addColorStop(.27,'rgba(255,255,255,0)');
    sheen.addColorStop(.56,`rgba(225,240,248,${.025+.045*k})`);
    sheen.addColorStop(.75,'rgba(255,255,255,0)');
    sheen.addColorStop(1,`rgba(255,255,255,${.035+.055*k})`);
    c.fillStyle=sheen;c.fillRect(0,0,S,S);

    c.lineCap='round';
    c.strokeStyle=`rgba(255,255,255,${.13+.18*k})`;
    c.lineWidth=Math.max(1,S*.0011);
    c.beginPath();c.moveTo(S*.055,S*.075);c.lineTo(S*.94,S*.075);c.stroke();
    c.beginPath();c.moveTo(S*.945,S*.08);c.lineTo(S*.945,S*.93);c.stroke();
    c.strokeStyle=`rgba(190,210,220,${.08+.10*k})`;
    c.lineWidth=Math.max(.7,S*.00065);
    c.beginPath();c.moveTo(S*.052,S*.925);c.lineTo(S*.94,S*.925);c.stroke();

    for(let i=0;i<11;i++){
      const x=(.09+seeded(6000+i)*.82)*S;
      const y=(.07+seeded(6100+i)*.84)*S;
      const len=(.025+seeded(6200+i)*.07)*S;
      const a=-.65+seeded(6300+i)*1.3;
      c.strokeStyle=`rgba(255,255,255,${(.025+seeded(6400+i)*.055)*k})`;
      c.lineWidth=Math.max(.45,S*.00042);
      c.beginPath();
      c.moveTo(x,y);
      c.quadraticCurveTo(x+Math.cos(a+.45)*len*.5,y+Math.sin(a+.45)*len*.5,x+Math.cos(a)*len,y+Math.sin(a)*len);
      c.stroke();
    }

    const fold=c.createLinearGradient(S*.66,0,S*.88,S*.22);
    fold.addColorStop(0,'rgba(255,255,255,0)');
    fold.addColorStop(.5,`rgba(255,255,255,${.07+.11*k})`);
    fold.addColorStop(1,'rgba(255,255,255,0)');
    c.fillStyle=fold;
    c.beginPath();
    c.moveTo(S*.70,S*.035);c.lineTo(S*.93,S*.035);c.lineTo(S*.93,S*.19);c.closePath();c.fill();
    c.restore();
  }

  function drawGlitter(c,S){
    if(!state.glitter || state.glitterStrength<=0)return;
    const k=Math.max(0,Math.min(1,state.glitterStrength/100));
    const count=Math.round(18+90*k);
    c.save();
    c.globalCompositeOperation='screen';
    for(let i=0;i<count;i++){
      const x=(.055+seeded(7000+i)*.89)*S;
      const y=(.055+seeded(7100+i)*.89)*S;
      const r=S*(.0008+seeded(7200+i)*(.0022+.0030*k));
      const hue=Math.floor(seeded(7300+i)*360);
      const alpha=.18+seeded(7400+i)*(.35+.30*k);
      c.fillStyle=`hsla(${hue},90%,78%,${alpha})`;
      c.beginPath();c.arc(x,y,r,0,Math.PI*2);c.fill();
      if(i%5===0){
        c.strokeStyle=`rgba(255,255,255,${.28+.42*k})`;
        c.lineWidth=Math.max(.5,S*.00045);
        c.beginPath();c.moveTo(x-r*3.1,y);c.lineTo(x+r*3.1,y);c.moveTo(x,y-r*3.1);c.lineTo(x,y+r*3.1);c.stroke();
      }
    }
    c.restore();
  }

  function drawCracks(c,S){
    if(!state.cracks || state.crackStrength<=0)return;
    const k=Math.max(0,Math.min(1,state.crackStrength/100));
    const roots=[
      [.075,.115,.50], [.90,.15,2.58], [.88,.86,-2.35], [.16,.89,-.72]
    ];
    const rootsToDraw=Math.max(1,Math.round(1+3*k));
    c.save();
    c.lineCap='round';c.lineJoin='round';
    for(let r=0;r<rootsToDraw;r++){
      const [rx,ry,baseA]=roots[r];
      const branches=Math.round(3+5*k);
      for(let b=0;b<branches;b++){
        let x=rx*S,y=ry*S;
        const a0=baseA+(-.50+seeded(8000+r*20+b)*1.0);
        const segs=Math.round(3+4*k);
        c.beginPath();c.moveTo(x,y);
        for(let j=0;j<segs;j++){
          const len=S*(.018+seeded(8100+r*100+b*10+j)*(.025+.028*k));
          const a=a0+(-.32+seeded(8200+r*100+b*10+j)*.64);
          x+=Math.cos(a)*len;y+=Math.sin(a)*len;
          c.lineTo(x,y);
        }
        c.strokeStyle=`rgba(6,10,14,${.16+.24*k})`;
        c.lineWidth=Math.max(1,S*.00115);c.stroke();
        c.strokeStyle=`rgba(245,250,255,${.22+.38*k})`;
        c.lineWidth=Math.max(.45,S*.00048);c.stroke();
      }
    }
    c.restore();
  }

'''
    if insert_before not in s:
        raise SystemExit('render anchor missing')
    s = s.replace(insert_before, funcs + insert_before, 1)

render_anchor = "    if(state.barcode)drawBarcode(c,S);"
render_new = """    if(state.barcode)drawBarcode(c,S);
    drawCracks(c,S);
    drawGlitter(c,S);
    drawSealedWrap(c,S);"""
if render_anchor in s and 'drawSealedWrap(c,S);' not in s.split(render_anchor,1)[1][:220]:
    s = s.replace(render_anchor, render_new, 1)

old_reset = "grooves:true,scratches:true,titleSticker:false,advisory:false,priceSticker:false,barcode:false,albumTitle:'',artistName:''"
new_reset = "grooves:true,scratches:true,titleSticker:false,advisory:false,priceSticker:false,barcode:false,sealed:false,sealedStrength:62,glitter:false,glitterStrength:45,cracks:false,crackStrength:52,albumTitle:'',artistName:''"
if old_reset in s:
    s = s.replace(old_reset, new_reset, 1)
elif 'sealed:false,sealedStrength:62' not in s:
    raise SystemExit('reset anchor missing')

p.write_text(s)
