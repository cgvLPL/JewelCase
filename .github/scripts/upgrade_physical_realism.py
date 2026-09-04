from pathlib import Path

p = Path('index.html')
s = p.read_text()

marker = 'function drawVintageRetailPhysical(c,S)'
if marker not in s:
    insert_before = '  function drawNoise(c,S){'
    realism = r'''  function drawVintageRetailPhysical(c,S){
    // Vintage retail + macro product-photography realism pass.
    // This layer is deterministic so preview and exported artwork always match.
    const cx=S*.5030,cy=S*.4980,r=S*.3890,hub=S*.1120;

    c.save();
    c.lineCap='round';c.lineJoin='round';

    // Thick acrylic edge refraction: bright incident edge and darker return edge.
    c.globalCompositeOperation='screen';
    c.lineWidth=Math.max(1,S*.00125);
    c.strokeStyle='rgba(250,253,255,.25)';
    roundedRectPath(c,S*.024,S*.032,S*.952,S*.936,S*.010);c.stroke();
    c.lineWidth=Math.max(.7,S*.00072);
    c.strokeStyle='rgba(185,217,232,.12)';
    roundedRectPath(c,S*.031,S*.040,S*.938,S*.918,S*.008);c.stroke();
    c.globalCompositeOperation='multiply';
    c.lineWidth=Math.max(1,S*.0010);
    c.strokeStyle='rgba(8,13,17,.16)';
    c.beginPath();c.moveTo(S*.030,S*.966);c.lineTo(S*.970,S*.966);c.stroke();
    c.beginPath();c.moveTo(S*.970,S*.040);c.lineTo(S*.970,S*.965);c.stroke();

    // Injection-moulding seams and tiny stress lines around corners/hinges.
    const seams=[
      [.041,.155,.071,.155],[.041,.843,.071,.843],[.930,.158,.960,.158],[.930,.842,.960,.842],
      [.090,.055,.210,.055],[.790,.055,.910,.055],[.090,.945,.210,.945],[.790,.945,.910,.945]
    ];
    for(let i=0;i<seams.length;i++){
      const q=seams[i];
      c.globalCompositeOperation='screen';
      c.strokeStyle='rgba(255,255,255,.14)';c.lineWidth=Math.max(.45,S*.00045);
      c.beginPath();c.moveTo(S*q[0],S*q[1]);c.lineTo(S*q[2],S*q[3]);c.stroke();
      c.globalCompositeOperation='multiply';
      c.strokeStyle='rgba(20,25,29,.12)';c.lineWidth=Math.max(.35,S*.00032);
      c.beginPath();c.moveTo(S*q[0],S*(q[1]+.002));c.lineTo(S*q[2],S*(q[3]+.002));c.stroke();
    }

    // Slight amber aging in the thickest perimeter plastic, typical of handled 90s/00s cases.
    c.globalCompositeOperation='soft-light';
    const age=c.createRadialGradient(S*.50,S*.49,S*.34,S*.50,S*.49,S*.72);
    age.addColorStop(0,'rgba(156,119,68,0)');
    age.addColorStop(.73,'rgba(156,119,68,.012)');
    age.addColorStop(1,state.caseStyle==='worn'?'rgba(151,103,48,.090)':'rgba(151,103,48,.032)');
    c.fillStyle=age;c.fillRect(0,0,S,S);

    // Oily handling smudges/fingerprint partials on the clear lid, kept very faint.
    c.globalCompositeOperation='screen';
    const prints=[
      [.235,.205,.083,.040,-.32],[.745,.265,.073,.035,.26],[.285,.724,.092,.044,.18],[.700,.760,.080,.037,-.24]
    ];
    for(let n=0;n<prints.length;n++){
      const [px,py,rx,ry,rot]=prints[n];
      c.save();c.translate(S*px,S*py);c.rotate(rot);
      for(let j=0;j<5;j++){
        c.strokeStyle=`rgba(255,255,255,${.010+j*.0025})`;
        c.lineWidth=Math.max(.35,S*.00026);
        c.beginPath();c.ellipse(0,0,S*(rx-j*.007),S*(ry-j*.0037),0,-2.55,1.0);c.stroke();
      }
      c.restore();
    }

    // Sparse handling scratches: fine enough to read as physical acrylic, not a texture overlay.
    if(state.scratches){
      c.globalCompositeOperation='screen';
      const count=state.caseStyle==='worn'?42:22;
      for(let i=0;i<count;i++){
        const x=(.065+seeded(20000+i)*.87)*S;
        const y=(.070+seeded(20100+i)*.85)*S;
        const len=(.010+seeded(20200+i)*.060)*S;
        const ang=(-.92+seeded(20300+i)*1.84);
        c.strokeStyle=`rgba(255,255,255,${.012+seeded(20400+i)*(state.caseStyle==='worn'?.055:.026)})`;
        c.lineWidth=Math.max(.25,S*(.00017+seeded(20500+i)*.00022));
        c.beginPath();c.moveTo(x,y);c.lineTo(x+Math.cos(ang)*len,y+Math.sin(ang)*len);c.stroke();
      }
    }

    // Dust settles near rails, corners and the spindle area rather than uniformly over the case.
    c.globalCompositeOperation='source-over';
    for(let i=0;i<36;i++){
      const side=i%4,t=seeded(21000+i);
      let x,y;
      if(side===0){x=.035+seeded(21100+i)*.055;y=.07+t*.86;}
      else if(side===1){x=.91+seeded(21200+i)*.055;y=.07+t*.86;}
      else if(side===2){x=.08+t*.84;y=.035+seeded(21300+i)*.045;}
      else{x=.08+t*.84;y=.92+seeded(21400+i)*.045;}
      const rr=S*(.00035+seeded(21500+i)*.00065);
      c.fillStyle=`rgba(226,224,214,${.040+seeded(21600+i)*.055})`;
      circlePath(c,S*x,S*y,rr);c.fill();
    }

    // Pressed-CD manufacturing rings and restrained spectral diffraction.
    c.save();
    c.beginPath();c.arc(cx,cy,r,0,Math.PI*2);c.arc(cx,cy,hub,0,Math.PI*2,true);c.clip('evenodd');
    c.globalCompositeOperation='screen';
    for(let i=0;i<8;i++){
      const rr=r*(.58+i*.046);
      c.lineWidth=Math.max(.35,S*.00024);
      c.strokeStyle=`rgba(235,245,250,${.012+i*.0015})`;
      circlePath(c,cx,cy,rr);c.stroke();
    }
    const spectrum=[
      ['rgba(255,82,116,.070)',-.12],['rgba(255,183,71,.055)',-.06],['rgba(88,232,198,.058)',0],['rgba(97,151,255,.070)',.06],['rgba(184,104,255,.055)',.12]
    ];
    for(let i=0;i<spectrum.length;i++){
      const [col,off]=spectrum[i];
      c.strokeStyle=col;c.lineWidth=Math.max(.45,S*.00038);
      c.beginPath();c.arc(cx,cy,r*(.78+off*.18),-2.54+off,-1.79+off);c.stroke();
      c.beginPath();c.arc(cx,cy,r*(.71+off*.15),.46+off,1.04+off);c.stroke();
    }
    // Translucent polycarbonate edge thickness.
    c.lineWidth=Math.max(1,S*.0012);c.strokeStyle='rgba(210,235,247,.18)';
    c.beginPath();c.arc(cx,cy,r*.994,-2.65,-.22);c.stroke();
    c.globalCompositeOperation='multiply';
    c.lineWidth=Math.max(.9,S*.0010);c.strokeStyle='rgba(0,7,12,.19)';
    c.beginPath();c.arc(cx,cy,r*.995,.42,2.65);c.stroke();
    c.restore();

    // Hub seat depth and contact shadow where the disc meets the spindle assembly.
    c.globalCompositeOperation='multiply';
    c.lineWidth=Math.max(1.1,S*.00125);c.strokeStyle='rgba(0,0,0,.24)';
    circlePath(c,cx,cy,hub*1.03);c.stroke();
    c.globalCompositeOperation='screen';
    c.lineWidth=Math.max(.7,S*.00065);c.strokeStyle='rgba(255,255,255,.12)';
    c.beginPath();c.arc(cx,cy,hub*1.055,-2.65,-.35);c.stroke();

    // Broad photographic softbox reflection. Low opacity keeps it from reading as CGI.
    c.globalCompositeOperation='screen';
    const softbox=c.createLinearGradient(S*.06,S*.06,S*.88,S*.90);
    softbox.addColorStop(0,'rgba(255,255,255,.070)');
    softbox.addColorStop(.14,'rgba(255,255,255,.018)');
    softbox.addColorStop(.46,'rgba(255,255,255,0)');
    softbox.addColorStop(.78,'rgba(236,248,255,.012)');
    softbox.addColorStop(1,'rgba(255,255,255,.042)');
    c.fillStyle=softbox;c.fillRect(S*.035,S*.045,S*.93,S*.91);

    // Small highlight bloom on the photographed acrylic corners.
    for(const q of [[.070,.080],[.930,.085],[.080,.925],[.925,.920]]){
      const g=c.createRadialGradient(S*q[0],S*q[1],0,S*q[0],S*q[1],S*.055);
      g.addColorStop(0,'rgba(255,255,255,.055)');g.addColorStop(1,'rgba(255,255,255,0)');
      c.fillStyle=g;c.fillRect(S*(q[0]-.06),S*(q[1]-.06),S*.12,S*.12);
    }
    c.restore();
  }

  function drawSealRetailFinish(c,S){
    if(!state.sealed || state.sealedStrength<=0)return;
    const k=Math.max(0,Math.min(1,state.sealedStrength/100));
    c.save();c.lineCap='round';c.lineJoin='round';

    // Extra factory-wrap tension creases at the four corners.
    const corner=(x,y,sx,sy)=>{
      for(let i=0;i<4;i++){
        const a=.018+i*.010;
        c.globalCompositeOperation='multiply';
        c.strokeStyle=`rgba(16,25,30,${(.035+i*.008)*k})`;c.lineWidth=Math.max(.45,S*.00045);
        c.beginPath();c.moveTo(S*x,S*y);c.quadraticCurveTo(S*(x+sx*a*.50),S*(y+sy*a*.72),S*(x+sx*a),S*(y+sy*(.042+i*.012)));c.stroke();
        c.globalCompositeOperation='screen';
        c.strokeStyle=`rgba(255,255,255,${(.075+i*.010)*k})`;c.lineWidth=Math.max(.4,S*.00036);
        c.beginPath();c.moveTo(S*(x-sx*.001),S*(y-sy*.001));c.quadraticCurveTo(S*(x+sx*a*.50-sx*.001),S*(y+sy*a*.72-sy*.001),S*(x+sx*a-sx*.001),S*(y+sy*(.042+i*.012)-sy*.001));c.stroke();
      }
    };
    corner(.028,.035,1,1);corner(.972,.035,-1,1);corner(.028,.965,1,-1);corner(.972,.965,-1,-1);

    // Slightly cloudy stretched-film bloom along the heat seals.
    c.globalCompositeOperation='screen';
    const top=c.createLinearGradient(0,S*.020,0,S*.075);
    top.addColorStop(0,`rgba(255,255,255,${.040*k})`);top.addColorStop(.40,`rgba(220,238,247,${.018*k})`);top.addColorStop(1,'rgba(255,255,255,0)');
    c.fillStyle=top;c.fillRect(S*.025,S*.020,S*.95,S*.070);
    const bottom=c.createLinearGradient(0,S*.980,0,S*.915);
    bottom.addColorStop(0,`rgba(255,255,255,${.035*k})`);bottom.addColorStop(.45,`rgba(220,238,247,${.015*k})`);bottom.addColorStop(1,'rgba(255,255,255,0)');
    c.fillStyle=bottom;c.fillRect(S*.025,S*.910,S*.95,S*.070);

    // A few tiny trapped-air pockets near the seal, not across the whole surface.
    for(let i=0;i<12;i++){
      const x=(.08+seeded(23000+i)*.84)*S;
      const y=(i%2?(.045+seeded(23100+i)*.028):(.925+seeded(23200+i)*.028))*S;
      const rx=S*(.003+seeded(23300+i)*.006),ry=rx*(.30+seeded(23400+i)*.35);
      c.strokeStyle=`rgba(255,255,255,${(.045+seeded(23500+i)*.035)*k})`;
      c.lineWidth=Math.max(.35,S*.00028);c.beginPath();c.ellipse(x,y,rx,ry,seeded(23600+i)*.8,0,Math.PI*2);c.stroke();
    }
    c.restore();
  }

'''
    if insert_before not in s:
        raise SystemExit('drawNoise anchor not found')
    s = s.replace(insert_before, realism + insert_before, 1)

if '    drawVintageRetailPhysical(c,S);' not in s:
    anchor = '    drawCaseRealism(c,S);\n    drawNoise(c,S);'
    if anchor not in s:
        raise SystemExit('render case anchor not found')
    s = s.replace(anchor, '    drawCaseRealism(c,S);\n    drawVintageRetailPhysical(c,S);\n    drawNoise(c,S);', 1)

if '    drawSealRetailFinish(c,S);' not in s:
    anchor = '    drawSealedWrap(c,S);\n\n    // Physical rails'
    if anchor not in s:
        raise SystemExit('render seal anchor not found')
    s = s.replace(anchor, '    drawSealedWrap(c,S);\n    drawSealRetailFinish(c,S);\n\n    // Physical rails', 1)

p.write_text(s)
print('Applied vintage retail + ultra-real photography physical realism pass')
