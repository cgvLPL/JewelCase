from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

sealed = r'''  function drawSealedWrap(c,S){
    if(!state.sealed || state.sealedStrength<=0)return;
    const k=Math.max(0,Math.min(1,state.sealedStrength/100));
    c.save();

    // Very subtle clear film tint. Real shrink-wrap mostly reveals itself through
    // tension highlights, seams and small edge wrinkles rather than a milky wash.
    c.globalCompositeOperation='screen';
    const film=c.createLinearGradient(S*.04,S*.02,S*.96,S*.98);
    film.addColorStop(0,`rgba(255,255,255,${.012+.018*k})`);
    film.addColorStop(.34,'rgba(255,255,255,0)');
    film.addColorStop(.58,`rgba(232,242,248,${.010+.018*k})`);
    film.addColorStop(.82,'rgba(255,255,255,0)');
    film.addColorStop(1,`rgba(255,255,255,${.014+.022*k})`);
    c.fillStyle=film;c.fillRect(0,0,S,S);

    // Broad reflected bands warped slightly by the loose film.
    const bands=[
      [.13,.02,.44,.98,.020,.045],
      [.52,.02,.78,.98,.010,.030],
      [.02,.32,.98,.55,.008,.020]
    ];
    for(let i=0;i<bands.length;i++){
      const [x0,y0,x1,y1,a0,a1]=bands[i];
      const g=c.createLinearGradient(S*x0,S*y0,S*x1,S*y1);
      g.addColorStop(0,'rgba(255,255,255,0)');
      g.addColorStop(.43,`rgba(255,255,255,${a0+a1*k})`);
      g.addColorStop(.50,`rgba(255,255,255,${(a0+a1*k)*.45})`);
      g.addColorStop(.57,'rgba(255,255,255,0)');
      c.fillStyle=g;c.fillRect(S*.035,S*.035,S*.93,S*.93);
    }

    // Heat-sealed perimeter: double line, slightly uneven and never perfectly white.
    c.lineCap='round';c.lineJoin='round';
    const seams=[
      [[.050,.071],[.948,.071]],
      [[.949,.073],[.949,.932]],
      [[.052,.928],[.944,.928]],
      [[.051,.077],[.051,.922]]
    ];
    for(let i=0;i<seams.length;i++){
      const [[x0,y0],[x1,y1]]=seams[i];
      c.strokeStyle=`rgba(232,241,246,${.075+.095*k})`;
      c.lineWidth=Math.max(.65,S*.00072);
      c.beginPath();c.moveTo(S*x0,S*y0);c.lineTo(S*x1,S*y1);c.stroke();
      c.strokeStyle=`rgba(255,255,255,${.035+.060*k})`;
      c.lineWidth=Math.max(.4,S*.00034);
      c.beginPath();c.moveTo(S*(x0+.002),S*(y0+.002));c.lineTo(S*(x1+.002),S*(y1+.002));c.stroke();
    }

    // Wrinkles live mostly at corners/edges where film bunches up.
    const zones=[
      [.07,.08,.18,.17], [.79,.06,.94,.18], [.06,.79,.20,.93], [.79,.80,.94,.94],
      [.43,.06,.59,.12], [.88,.42,.95,.60]
    ];
    const wrinkles=Math.round(9+18*k);
    for(let i=0;i<wrinkles;i++){
      const z=zones[i%zones.length];
      const x=(z[0]+seeded(6000+i)*(z[2]-z[0]))*S;
      const y=(z[1]+seeded(6100+i)*(z[3]-z[1]))*S;
      const len=(.018+seeded(6200+i)*(.028+.035*k))*S;
      const a=(-1.15+seeded(6300+i)*2.3)+(i%2?0:.55);
      const bend=(-.45+seeded(6400+i)*.9);
      c.strokeStyle=`rgba(255,255,255,${(.032+seeded(6500+i)*.045)*(.45+.55*k)})`;
      c.lineWidth=Math.max(.35,S*(.00028+seeded(6600+i)*.00024));
      c.beginPath();
      c.moveTo(x,y);
      c.quadraticCurveTo(x+Math.cos(a+bend)*len*.48,y+Math.sin(a+bend)*len*.48,x+Math.cos(a)*len,y+Math.sin(a)*len);
      c.stroke();
      // faint shadow on the opposite side gives the wrinkle a folded-plastic profile
      c.globalCompositeOperation='multiply';
      c.strokeStyle=`rgba(80,95,105,${.018+.024*k})`;
      c.lineWidth=Math.max(.3,S*.00022);
      c.beginPath();
      c.moveTo(x+S*.0012,y+S*.0012);
      c.quadraticCurveTo(x+Math.cos(a+bend)*len*.48+S*.0012,y+Math.sin(a+bend)*len*.48+S*.0012,x+Math.cos(a)*len+S*.0012,y+Math.sin(a)*len+S*.0012);
      c.stroke();
      c.globalCompositeOperation='screen';
    }

    // Slight gathered triangular folds in two corners, common on factory wrap.
    const corners=[[.052,.073,1,1],[.949,.929,-1,-1]];
    for(const [x,y,dx,dy] of corners){
      for(let j=0;j<3;j++){
        const len=S*(.028+j*.010)*(.65+.35*k);
        c.strokeStyle=`rgba(255,255,255,${.035+.045*k})`;
        c.lineWidth=Math.max(.35,S*.0003);
        c.beginPath();
        c.moveTo(S*x,S*y);
        c.lineTo(S*x+dx*len,S*y+dy*len*(.25+j*.12));
        c.stroke();
      }
    }
    c.restore();
  }
'''

cracks = r'''  function drawCracks(c,S){
    if(!state.cracks || state.crackStrength<=0)return;
    const k=Math.max(0,Math.min(1,state.crackStrength/100));
    const impacts=[
      [.086,.126,.43], [.903,.166,2.72], [.873,.865,-2.36], [.145,.887,-.74]
    ];
    const impactCount=k<.34?1:(k<.72?2:3);

    function crackPath(seed,x,y,a,len,segs,spread){
      const pts=[[x,y]];
      let px=x,py=y,ang=a;
      for(let j=0;j<segs;j++){
        const taper=1-j/(segs+1);
        const step=len*(.20+.18*taper)*( .76+seeded(seed+j*11)*.46 );
        ang += (-.5+seeded(seed+j*17+3))*spread*(.55+.45*taper);
        px+=Math.cos(ang)*step;py+=Math.sin(ang)*step;
        pts.push([px,py]);
      }
      return pts;
    }

    function strokeCrack(pts,alpha,width){
      c.globalCompositeOperation='multiply';
      c.strokeStyle=`rgba(18,25,31,${alpha*.72})`;
      c.lineWidth=Math.max(.45,S*width*1.7);
      c.beginPath();c.moveTo(pts[0][0],pts[0][1]);
      for(let i=1;i<pts.length;i++)c.lineTo(pts[i][0],pts[i][1]);
      c.stroke();

      c.globalCompositeOperation='screen';
      c.strokeStyle=`rgba(247,252,255,${alpha})`;
      c.lineWidth=Math.max(.32,S*width);
      c.beginPath();c.moveTo(pts[0][0]-S*.0005,pts[0][1]-S*.0004);
      for(let i=1;i<pts.length;i++)c.lineTo(pts[i][0]-S*.0005,pts[i][1]-S*.0004);
      c.stroke();
    }

    c.save();
    c.lineCap='round';c.lineJoin='miter';
    for(let r=0;r<impactCount;r++){
      const [rx,ry,baseA]=impacts[r];
      const ox=rx*S,oy=ry*S;
      const mainCount=Math.round(3+4*k);

      // Small compressed impact chip instead of a cartoon starburst.
      c.globalCompositeOperation='screen';
      c.fillStyle=`rgba(242,248,251,${.06+.12*k})`;
      c.beginPath();c.arc(ox,oy,S*(.0025+.0028*k),0,Math.PI*2);c.fill();
      c.strokeStyle=`rgba(255,255,255,${.16+.20*k})`;
      c.lineWidth=Math.max(.35,S*.00035);
      c.beginPath();c.arc(ox,oy,S*(.004+.003*k),0,Math.PI*2);c.stroke();

      for(let b=0;b<mainCount;b++){
        const seed=8000+r*500+b*41;
        const a=baseA+(-.62+seeded(seed)*1.24);
        const totalLen=S*(.055+seeded(seed+4)*(.075+.090*k));
        const segs=Math.round(5+4*k+seeded(seed+8)*3);
        const pts=crackPath(seed,ox,oy,a,totalLen,segs,.62);
        const alpha=.24+.30*k+seeded(seed+12)*.10;
        strokeCrack(pts,alpha,.00034+.00018*k);

        // Secondary forks grow from midpoints and are thinner/shorter than the trunk.
        const forks=Math.round((1+2*k)*seeded(seed+16));
        for(let f=0;f<forks;f++){
          const idx=1+Math.floor(seeded(seed+20+f)*Math.max(1,pts.length-2));
          const [fx,fy]=pts[Math.min(idx,pts.length-2)];
          const prev=pts[Math.max(0,idx-1)];
          const dir=Math.atan2(fy-prev[1],fx-prev[0]);
          const side=seeded(seed+30+f)>.5?1:-1;
          const fa=dir+side*(.45+seeded(seed+40+f)*.70);
          const flen=totalLen*(.18+.20*seeded(seed+50+f))*(.55+.45*k);
          const fpts=crackPath(seed+70+f*13,fx,fy,fa,flen,3+Math.round(2*k),.78);
          strokeCrack(fpts,alpha*.62,.00022+.00010*k);
        }
      }
    }
    c.restore();
  }
'''

s2, n1 = re.subn(r"  function drawSealedWrap\(c,S\)\{.*?\n  \}\n\n  function drawGlitter", sealed + "\n  function drawGlitter", s, flags=re.S)
s3, n2 = re.subn(r"  function drawCracks\(c,S\)\{.*?\n  \}\n\n  function render", cracks + "\n  function render", s2, flags=re.S)
if n1 != 1 or n2 != 1:
    raise SystemExit(f'patch counts sealed={n1} cracks={n2}')
p.write_text(s3)
print('refined sealed wrap and crack effects')
