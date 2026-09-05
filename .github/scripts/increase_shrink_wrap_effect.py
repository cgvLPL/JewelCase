from pathlib import Path

p = Path('index.html')
s = p.read_text()

FN = r'''
  function drawShrinkWrapTension(c,S){
    if(!state.sealed || state.sealedStrength<=0)return;
    const k=Math.max(0,Math.min(1,state.sealedStrength/100));
    c.save();
    c.lineCap='round';c.lineJoin='round';

    // Tight contracted film hugs the case perimeter. A bright/dark paired contour
    // makes the plastic look physically stretched over the acrylic edges.
    c.globalCompositeOperation='multiply';
    c.strokeStyle=`rgba(26,34,39,${.035+.050*k})`;
    c.lineWidth=Math.max(.65,S*.00072);
    roundedRectPath(c,S*.032,S*.040,S*.936,S*.918,S*.008);c.stroke();
    c.globalCompositeOperation='screen';
    c.strokeStyle=`rgba(250,253,255,${.085+.115*k})`;
    c.lineWidth=Math.max(.60,S*.00064);
    roundedRectPath(c,S*.0305,S*.0385,S*.939,S*.921,S*.008);c.stroke();

    // Film compression strips over the four case edges. The inner fade creates
    // the illusion of transparent plastic being pulled tightly around thickness.
    const edgeBand=(x0,y0,x1,y1,px,py)=>{
      const g=c.createLinearGradient(S*(x0-px*.020),S*(y0-py*.020),S*(x0+px*.040),S*(y0+py*.040));
      g.addColorStop(0,'rgba(255,255,255,0)');
      g.addColorStop(.36,`rgba(255,255,255,${.018+.030*k})`);
      g.addColorStop(.50,`rgba(255,255,255,${.075+.105*k})`);
      g.addColorStop(.62,`rgba(180,208,220,${.018+.032*k})`);
      g.addColorStop(1,'rgba(255,255,255,0)');
      c.globalCompositeOperation='screen';c.strokeStyle=g;
      c.lineWidth=Math.max(1.2,S*(.0030+.0022*k));
      c.beginPath();c.moveTo(S*x0,S*y0);c.lineTo(S*x1,S*y1);c.stroke();
    };
    edgeBand(.055,.056,.945,.056,0,1);
    edgeBand(.055,.944,.945,.944,0,-1);
    edgeBand(.045,.080,.045,.920,1,0);
    edgeBand(.955,.080,.955,.920,-1,0);

    // Y-fold shrink-wrap corners, typical of retail jewel cases. Each corner has
    // a main fold with smaller radiating tension lines and a subtle return shadow.
    const yfold=(x,y,sx,sy,seed)=>{
      const mainLen=.090+.025*k;
      for(let j=0;j<5;j++){
        const spread=(j-2)*.16;
        const len=mainLen*(.55+j*.095)*( .90+seeded(seed+j)*.18 );
        const ex=x+sx*len;
        const ey=y+sy*len*(.30+Math.abs(spread)*.30);
        const mx=x+sx*len*.44;
        const my=y+sy*len*(.08+spread*.11);
        c.globalCompositeOperation='multiply';
        c.strokeStyle=`rgba(32,40,45,${(.030+.013*j)*k})`;
        c.lineWidth=Math.max(.38,S*.00042);
        c.beginPath();c.moveTo(S*(x+.0015*sx),S*(y+.0015*sy));c.quadraticCurveTo(S*(mx+.0015*sx),S*(my+.0015*sy),S*(ex+.0015*sx),S*(ey+.0015*sy));c.stroke();
        c.globalCompositeOperation='screen';
        c.strokeStyle=`rgba(255,255,255,${(.065+.018*j)*k})`;
        c.lineWidth=Math.max(.36,S*.00036);
        c.beginPath();c.moveTo(S*x,S*y);c.quadraticCurveTo(S*mx,S*my,S*ex,S*ey);c.stroke();
      }
      c.globalCompositeOperation='screen';
      const bloom=c.createRadialGradient(S*x,S*y,0,S*x,S*y,S*(.055+.018*k));
      bloom.addColorStop(0,`rgba(255,255,255,${.055*k})`);bloom.addColorStop(1,'rgba(255,255,255,0)');
      c.fillStyle=bloom;c.fillRect(S*(x-.07),S*(y-.07),S*.14,S*.14);
    };
    yfold(.040,.050,1,1,31000);yfold(.960,.050,-1,1,31100);
    yfold(.040,.950,1,-1,31200);yfold(.960,.950,-1,-1,31300);

    // Long taut wrinkles pulled between opposite edges. Paired highlights/shadows
    // create a shallow ridge instead of a simple line drawn over the image.
    const taut=[
      [.095,.120,.44,.105,.006], [.57,.095,.91,.135,-.007],
      [.080,.365,.115,.690,.006], [.905,.315,.940,.690,-.006],
      [.135,.890,.46,.925,-.005], [.56,.915,.895,.875,.006]
    ];
    taut.forEach((q,i)=>{
      const [x0,y0,x1,y1,b]=q;
      const mx=(x0+x1)/2,my=(y0+y1)/2+b;
      c.globalCompositeOperation='multiply';
      c.strokeStyle=`rgba(44,54,60,${(.022+.028*k)})`;c.lineWidth=Math.max(.30,S*.00028);
      c.beginPath();c.moveTo(S*(x0+.0012),S*(y0+.0012));c.quadraticCurveTo(S*(mx+.0012),S*(my+.0012),S*(x1+.0012),S*(y1+.0012));c.stroke();
      c.globalCompositeOperation='screen';
      c.strokeStyle=`rgba(255,255,255,${(.040+.060*k)})`;c.lineWidth=Math.max(.34,S*.00034);
      c.beginPath();c.moveTo(S*x0,S*y0);c.quadraticCurveTo(S*mx,S*my,S*x1,S*y1);c.stroke();
    });

    // Fine heat-shrink puckering is concentrated beside the perimeter seal.
    const perimeterWrinkles=Math.round(28+46*k);
    for(let i=0;i<perimeterWrinkles;i++){
      const side=i%4,t=.08+seeded(32000+i)*.84;
      let x,y,ang;
      if(side===0){x=t;y=.060+seeded(32100+i)*.032;ang=1.35+seeded(32200+i)*.40;}
      else if(side===1){x=.908+seeded(32300+i)*.032;y=t;ang=2.85+seeded(32400+i)*.40;}
      else if(side===2){x=t;y=.908+seeded(32500+i)*.032;ang=-1.75+seeded(32600+i)*.40;}
      else{x=.060+seeded(32700+i)*.032;y=t;ang=-.30+seeded(32800+i)*.40;}
      const len=S*(.008+seeded(32900+i)*(.014+.020*k));
      const bend=(-.35+seeded(33000+i)*.70);
      c.globalCompositeOperation='screen';
      c.strokeStyle=`rgba(255,255,255,${.025+.055*k})`;c.lineWidth=Math.max(.26,S*.00024);
      c.beginPath();c.moveTo(S*x,S*y);c.quadraticCurveTo(S*x+Math.cos(ang+bend)*len*.48,S*y+Math.sin(ang+bend)*len*.48,S*x+Math.cos(ang)*len,S*y+Math.sin(ang)*len);c.stroke();
    }

    // Uneven stretched-film specular ribbons. These are thin and broken so they
    // read as cellophane rather than a uniform glass overlay.
    c.globalCompositeOperation='screen';
    const ribbons=[
      [.16,.055,.30,.945,.040], [.41,.040,.49,.955,.026], [.70,.045,.83,.950,.032]
    ];
    ribbons.forEach(([x0,y0,x1,y1,a],i)=>{
      const g=c.createLinearGradient(S*x0,S*y0,S*x1,S*y1);
      g.addColorStop(0,'rgba(255,255,255,0)');
      g.addColorStop(.30,`rgba(255,255,255,${a*k*.55})`);
      g.addColorStop(.47,`rgba(255,255,255,${a*k})`);
      g.addColorStop(.53,`rgba(205,231,242,${a*k*.42})`);
      g.addColorStop(.70,'rgba(255,255,255,0)');
      c.fillStyle=g;c.fillRect(S*.035,S*.035,S*.93,S*.93);
    });

    // Slight cloudy compression at the heat-sealed corners and a few tiny air
    // pockets make the wrap feel mechanically shrunk rather than simply draped.
    for(let i=0;i<10;i++){
      const side=i%2;
      const x=(.12+seeded(34000+i)*.76)*S;
      const y=(side?(.065+seeded(34100+i)*.030):(.905+seeded(34200+i)*.030))*S;
      const rx=S*(.0025+seeded(34300+i)*.0055),ry=rx*(.24+seeded(34400+i)*.26);
      c.strokeStyle=`rgba(255,255,255,${(.045+.045*k)})`;
      c.lineWidth=Math.max(.30,S*.00025);c.beginPath();c.ellipse(x,y,rx,ry,seeded(34500+i)*.9,0,Math.PI*2);c.stroke();
    }

    c.restore();
  }
'''

if 'function drawShrinkWrapTension(c,S)' not in s:
    anchor = '  function drawNoise(c,S){'
    if anchor not in s:
        raise SystemExit('drawNoise anchor not found')
    s = s.replace(anchor, FN + '\n' + anchor, 1)

call = '    drawSealRetailFinish(c,S);\n'
if '    drawShrinkWrapTension(c,S);\n' not in s:
    if call not in s:
        raise SystemExit('render call anchor not found')
    s = s.replace(call, call + '    drawShrinkWrapTension(c,S);\n', 1)

p.write_text(s)
print('Shrink-wrap tension realism applied')
