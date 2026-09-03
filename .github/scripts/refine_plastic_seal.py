from pathlib import Path
p=Path('index.html')
s=p.read_text()
start=s.index('  function drawSealedWrap(c,S){')
end=s.index('\n  function drawGlitter(c,S){',start)
new=r'''  function drawSealedWrap(c,S){
    if(!state.sealed || state.sealedStrength<=0)return;
    const k=Math.max(0,Math.min(1,state.sealedStrength/100));
    c.save();

    // Clear cellophane film: almost invisible except where it catches light.
    c.globalCompositeOperation='screen';
    const film=c.createLinearGradient(S*.02,S*.02,S*.98,S*.98);
    film.addColorStop(0,`rgba(255,255,255,${.006+.010*k})`);
    film.addColorStop(.30,'rgba(255,255,255,0)');
    film.addColorStop(.55,`rgba(228,240,247,${.006+.012*k})`);
    film.addColorStop(.78,'rgba(255,255,255,0)');
    film.addColorStop(1,`rgba(255,255,255,${.008+.013*k})`);
    c.fillStyle=film;c.fillRect(0,0,S,S);

    // Long soft reflection rolls from stretched film, not painted white bands.
    const rolls=[
      [.09,.04,.30,.96,.18], [.35,.02,.53,.98,.12], [.66,.03,.82,.97,.10]
    ];
    for(const [x0,y0,x1,y1,a] of rolls){
      const g=c.createLinearGradient(S*x0,S*y0,S*x1,S*y1);
      g.addColorStop(0,'rgba(255,255,255,0)');
      g.addColorStop(.43,`rgba(255,255,255,${a*k*.34})`);
      g.addColorStop(.50,`rgba(255,255,255,${a*k*.14})`);
      g.addColorStop(.57,'rgba(255,255,255,0)');
      c.fillStyle=g;c.fillRect(S*.035,S*.035,S*.93,S*.93);
    }

    // Factory heat-seal seams: slightly doubled, irregular, and faintly shadowed.
    const seams=[
      [[.050,.071],[.948,.071]], [[.949,.073],[.949,.932]],
      [[.052,.928],[.944,.928]], [[.051,.077],[.051,.922]]
    ];
    c.lineCap='round';
    for(let i=0;i<seams.length;i++){
      const [[x0,y0],[x1,y1]]=seams[i];
      c.globalCompositeOperation='multiply';
      c.strokeStyle=`rgba(50,60,66,${.022+.040*k})`;
      c.lineWidth=Math.max(.45,S*.00055);
      c.beginPath();c.moveTo(S*(x0+.0014),S*(y0+.0014));c.lineTo(S*(x1+.0014),S*(y1+.0014));c.stroke();
      c.globalCompositeOperation='screen';
      c.strokeStyle=`rgba(244,249,252,${.070+.11*k})`;
      c.lineWidth=Math.max(.55,S*.00062);
      c.beginPath();c.moveTo(S*x0,S*y0);c.lineTo(S*x1,S*y1);c.stroke();
      c.strokeStyle=`rgba(255,255,255,${.026+.050*k})`;
      c.lineWidth=Math.max(.30,S*.00025);
      c.beginPath();c.moveTo(S*(x0+.0022),S*(y0+.0022));c.lineTo(S*(x1+.0022),S*(y1+.0022));c.stroke();
    }

    // Tension wrinkles: short, curved, paired highlight/shadow strokes near edges/corners.
    const zones=[
      [.055,.070,.22,.20], [.78,.065,.945,.20], [.055,.77,.22,.93], [.78,.78,.945,.93],
      [.31,.065,.66,.14], [.87,.29,.95,.68], [.06,.30,.13,.67]
    ];
    const count=Math.round(12+28*k);
    for(let i=0;i<count;i++){
      const z=zones[i%zones.length];
      const x=(z[0]+seeded(6000+i)*(z[2]-z[0]))*S;
      const y=(z[1]+seeded(6100+i)*(z[3]-z[1]))*S;
      const len=(.012+seeded(6200+i)*(.018+.034*k))*S;
      const ang=(-1.35+seeded(6300+i)*2.7)+(i%3===0?.55:0);
      const bend=(-.55+seeded(6400+i)*1.1);
      const ox=S*.0011,oy=S*.0010;
      c.globalCompositeOperation='multiply';
      c.strokeStyle=`rgba(58,68,74,${.018+.030*k})`;
      c.lineWidth=Math.max(.28,S*.00022);
      c.beginPath();c.moveTo(x+ox,y+oy);c.quadraticCurveTo(x+Math.cos(ang+bend)*len*.48+ox,y+Math.sin(ang+bend)*len*.48+oy,x+Math.cos(ang)*len+ox,y+Math.sin(ang)*len+oy);c.stroke();
      c.globalCompositeOperation='screen';
      c.strokeStyle=`rgba(255,255,255,${.030+.060*k})`;
      c.lineWidth=Math.max(.30,S*.00030);
      c.beginPath();c.moveTo(x,y);c.quadraticCurveTo(x+Math.cos(ang+bend)*len*.48,y+Math.sin(ang+bend)*len*.48,x+Math.cos(ang)*len,y+Math.sin(ang)*len);c.stroke();
    }

    // Gathered corner folds and tiny trapped-air creases.
    const corners=[[.052,.073,1,1],[.948,.073,-1,1],[.052,.928,1,-1],[.948,.928,-1,-1]];
    for(let ci=0;ci<corners.length;ci++){
      const [x,y,dx,dy]=corners[ci];
      for(let j=0;j<4;j++){
        const len=S*(.020+j*.010)*(.65+.35*k);
        c.globalCompositeOperation='screen';
        c.strokeStyle=`rgba(255,255,255,${.030+.050*k})`;
        c.lineWidth=Math.max(.30,S*.00028);
        c.beginPath();c.moveTo(S*x,S*y);c.lineTo(S*x+dx*len,S*y+dy*len*(.18+j*.13));c.stroke();
      }
    }

    // Sparse micro crinkles create a slightly uneven cellophane surface.
    c.globalCompositeOperation='screen';
    for(let i=0;i<16;i++){
      const x=(.08+seeded(700+i)*.84)*S,y=(.08+seeded(900+i)*.84)*S;
      const r=S*(.003+seeded(1100+i)*.006);
      c.strokeStyle=`rgba(255,255,255,${.012+.018*k})`;
      c.lineWidth=Math.max(.25,S*.00020);
      c.beginPath();c.arc(x,y,r,seeded(1300+i)*2.2,seeded(1400+i)*2.2+1.0);c.stroke();
    }
    c.restore();
  }
'''
s=s[:start]+new+s[end:]
p.write_text(s)
