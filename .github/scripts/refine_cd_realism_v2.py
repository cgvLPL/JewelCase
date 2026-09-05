from pathlib import Path

p = Path('index.html')
s = p.read_text()

fn = r'''
  function drawCdMicroPhysics(c,S){
    // High-detail pressed-CD optics. Keep all effects inside the data annulus so
    // the photographed spindle assembly remains untouched.
    const cx=S*.5030,cy=S*.4980,r=S*.3890,hub=S*.1120;
    const glare=Math.max(0,Math.min(1,state.glare/100));

    c.save();
    c.beginPath();
    c.arc(cx,cy,r,0,Math.PI*2);
    c.arc(cx,cy,hub,0,Math.PI*2,true);
    c.clip('evenodd');
    c.lineCap='round';

    // Silver data substrate: real pressed discs have a gentle radial density
    // shift instead of a perfectly flat reflective fill.
    c.globalCompositeOperation='soft-light';
    const substrate=c.createRadialGradient(cx,cy,hub*1.04,cx,cy,r);
    substrate.addColorStop(0,'rgba(214,224,231,.045)');
    substrate.addColorStop(.18,'rgba(88,105,117,.018)');
    substrate.addColorStop(.48,'rgba(244,249,252,.028)');
    substrate.addColorStop(.78,'rgba(82,105,120,.020)');
    substrate.addColorStop(.96,'rgba(238,246,250,.050)');
    substrate.addColorStop(1,'rgba(170,192,205,.035)');
    c.fillStyle=substrate;c.fillRect(cx-r,cy-r,r*2,r*2);

    // Dense micro-groove field. Alternating opacity bands create the very fine
    // pressed-track shimmer visible in macro product photos without turning into
    // decorative rings.
    if(state.grooves){
      c.globalCompositeOperation='screen';
      let n=0;
      for(let rr=hub*1.16;rr<r*.972;rr+=S*.00305){
        const pulse=(n%11===0)?1.75:(n%5===0?1.25:1);
        c.strokeStyle=`rgba(238,247,251,${(.0038+.0016*(n%4))*pulse})`;
        c.lineWidth=Math.max(.28,S*.00017);
        c.beginPath();c.arc(cx,cy,rr,0,Math.PI*2);c.stroke();
        n++;
      }

      // A few slightly stronger manufacturing band boundaries.
      for(const f of [.315,.428,.552,.684,.812,.914]){
        c.strokeStyle='rgba(248,252,255,.026)';
        c.lineWidth=Math.max(.34,S*.00024);
        c.beginPath();c.arc(cx,cy,r*f,0,Math.PI*2);c.stroke();
      }
    }

    // Angle-dependent diffraction wedges. The spectrum is split into thin arcs
    // with tiny angular offsets so white-light reflections feel optical rather
    // than like a rainbow gradient painted onto the artwork.
    if(state.discStyle!=='black'){
      c.globalCompositeOperation='screen';
      const bands=[
        ['rgba(255,72,112,.070)',0],
        ['rgba(255,162,68,.058)',.011],
        ['rgba(240,232,92,.046)',.021],
        ['rgba(86,238,190,.054)',.032],
        ['rgba(82,184,255,.068)',.043],
        ['rgba(153,105,255,.060)',.054]
      ];
      const wedges=[[-2.72,-2.03,.84],[.34,1.08,.735],[1.82,2.26,.905]];
      for(const [a0,a1,rf] of wedges){
        for(let i=0;i<bands.length;i++){
          const [col,off]=bands[i];
          c.strokeStyle=col;
          c.lineWidth=Math.max(.38,S*.00029);
          c.beginPath();c.arc(cx,cy,r*(rf+i*.0062),a0+off,a1+off);c.stroke();
        }
      }
    }

    // Narrow tangent glints that follow the circular geometry of the disc.
    // These are intentionally arcs, never ellipses, to avoid the synthetic oval
    // artifact that earlier versions produced.
    c.globalCompositeOperation='screen';
    c.strokeStyle=`rgba(255,255,255,${.055+.080*glare})`;
    c.lineWidth=Math.max(.7,S*.00072);
    c.beginPath();c.arc(cx,cy,r*.956,-2.48,-1.52);c.stroke();
    c.strokeStyle=`rgba(210,235,248,${.035+.050*glare})`;
    c.lineWidth=Math.max(.55,S*.00048);
    c.beginPath();c.arc(cx,cy,r*.905,.12,.82);c.stroke();

    // Polycarbonate outer bevel: transmitted cool highlight on the incident
    // side and a darker return edge opposite it gives the disc real thickness.
    c.globalCompositeOperation='screen';
    c.strokeStyle='rgba(221,243,252,.22)';
    c.lineWidth=Math.max(1.2,S*.00128);
    c.beginPath();c.arc(cx,cy,r*.996,-2.78,-.20);c.stroke();
    c.strokeStyle='rgba(255,255,255,.11)';
    c.lineWidth=Math.max(.7,S*.00060);
    c.beginPath();c.arc(cx,cy,r*.982,-2.62,-.34);c.stroke();
    c.globalCompositeOperation='multiply';
    c.strokeStyle='rgba(0,8,13,.23)';
    c.lineWidth=Math.max(1.0,S*.00105);
    c.beginPath();c.arc(cx,cy,r*.997,.34,2.72);c.stroke();

    // Mirror / matrix zone close to the center, common on commercially pressed
    // discs. It is separate from the photographed locking hub.
    c.globalCompositeOperation='screen';
    c.strokeStyle='rgba(235,244,249,.14)';
    c.lineWidth=Math.max(.75,S*.00062);
    for(const f of [1.16,1.205,1.255,1.315]){
      c.beginPath();c.arc(cx,cy,hub*f,0,Math.PI*2);c.stroke();
    }
    c.globalCompositeOperation='multiply';
    c.strokeStyle='rgba(10,20,26,.10)';
    c.lineWidth=Math.max(.5,S*.00040);
    c.beginPath();c.arc(cx,cy,hub*1.285,0,Math.PI*2);c.stroke();

    // Sparse radial micro-scuffs on the disc itself. They are deterministic and
    // far subtler than the case scratches, matching handling marks on used CDs.
    if(state.scratches){
      c.globalCompositeOperation='screen';
      for(let i=0;i<11;i++){
        const a=-2.8+seeded(31000+i)*5.6;
        const start=hub*(1.42+seeded(31100+i)*1.20);
        const len=S*(.018+seeded(31200+i)*.055);
        const x0=cx+Math.cos(a)*start,y0=cy+Math.sin(a)*start;
        const tang=a+Math.PI/2;
        c.strokeStyle=`rgba(255,255,255,${.010+seeded(31300+i)*.022})`;
        c.lineWidth=Math.max(.24,S*.00016);
        c.beginPath();
        c.moveTo(x0,y0);
        c.quadraticCurveTo(
          x0+Math.cos(tang)*len*.48,
          y0+Math.sin(tang)*len*.48,
          x0+Math.cos(tang)*len,
          y0+Math.sin(tang)*len
        );
        c.stroke();
      }
    }

    // Very soft silver rolloff, driven by the existing glare control.
    c.globalCompositeOperation='screen';
    const roll=c.createRadialGradient(cx-r*.24,cy-r*.27,r*.03,cx,cy,r*.88);
    roll.addColorStop(0,`rgba(255,255,255,${.018+.040*glare})`);
    roll.addColorStop(.34,`rgba(235,247,252,${.008+.016*glare})`);
    roll.addColorStop(.70,'rgba(255,255,255,0)');
    roll.addColorStop(1,'rgba(255,255,255,0)');
    c.fillStyle=roll;c.fillRect(cx-r,cy-r,r*2,r*2);

    c.restore();
  }
'''

if 'function drawCdMicroPhysics(c,S)' not in s:
    anchor = '  function seeded(seed){'
    if anchor not in s:
        raise SystemExit('Could not find seeded() anchor')
    s = s.replace(anchor, fn + '\n' + anchor, 1)

call_anchor = '    drawDisc(c,S);\n'
if '    drawCdMicroPhysics(c,S);\n' not in s:
    if call_anchor not in s:
        raise SystemExit('Could not find render drawDisc() call')
    s = s.replace(call_anchor, call_anchor + '    drawCdMicroPhysics(c,S);\n', 1)

p.write_text(s)
print('CD realism v2 patch applied')
