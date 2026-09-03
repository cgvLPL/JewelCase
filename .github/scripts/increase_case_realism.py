from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='  function drawNoise(c,S){'
if 'function drawCaseRealism(c,S)' not in s:
    fn="""  function drawCaseRealism(c,S){
    c.save();
    c.lineCap='round';c.lineJoin='round';
    c.globalCompositeOperation='screen';
    c.strokeStyle='rgba(246,252,255,.24)';c.lineWidth=Math.max(.8,S*.00115);
    c.beginPath();c.moveTo(S*.061,S*.071);c.lineTo(S*.936,S*.071);c.stroke();
    c.beginPath();c.moveTo(S*.057,S*.075);c.lineTo(S*.057,S*.925);c.stroke();
    c.strokeStyle='rgba(180,211,228,.10)';c.lineWidth=Math.max(.6,S*.00072);
    c.beginPath();c.moveTo(S*.066,S*.083);c.lineTo(S*.929,S*.083);c.stroke();
    c.globalCompositeOperation='multiply';
    c.strokeStyle='rgba(0,7,13,.20)';c.lineWidth=Math.max(.8,S*.0010);
    c.beginPath();c.moveTo(S*.063,S*.929);c.lineTo(S*.939,S*.929);c.stroke();
    c.beginPath();c.moveTo(S*.941,S*.079);c.lineTo(S*.941,S*.927);c.stroke();
    const rails=[[.105,.090,.105,.908],[.126,.092,.126,.906],[.876,.095,.876,.905],[.898,.098,.898,.902]];
    for(let i=0;i<rails.length;i++){
      const [x0,y0,x1,y1]=rails[i];
      c.globalCompositeOperation='multiply';c.strokeStyle='rgba(3,9,14,.10)';c.lineWidth=Math.max(.55,S*.00078);
      c.beginPath();c.moveTo(S*(x0+.0016),S*(y0+.0012));c.lineTo(S*(x1+.0016),S*(y1+.0012));c.stroke();
      c.globalCompositeOperation='screen';c.strokeStyle='rgba(246,251,255,.13)';c.lineWidth=Math.max(.45,S*.00055);
      c.beginPath();c.moveTo(S*x0,S*y0);c.lineTo(S*x1,S*y1);c.stroke();
    }
    const glow=c.createLinearGradient(S*.08,S*.08,S*.92,S*.92);
    glow.addColorStop(0,'rgba(255,255,255,.08)');glow.addColorStop(.22,'rgba(255,255,255,.012)');glow.addColorStop(.55,'rgba(255,255,255,0)');glow.addColorStop(1,'rgba(235,248,255,.05)');
    c.globalCompositeOperation='screen';c.fillStyle=glow;c.fillRect(S*.055,S*.070,S*.89,S*.86);
    for(let i=0;i<16;i++){
      const x=(.075+seeded(12000+i)*.85)*S,y=(.080+seeded(12100+i)*.83)*S,len=(.012+seeded(12200+i)*.045)*S,ang=-.55+seeded(12300+i)*1.15;
      c.strokeStyle=`rgba(255,255,255,${.016+seeded(12400+i)*.024})`;c.lineWidth=Math.max(.28,S*.00020);
      c.beginPath();c.moveTo(x,y);c.lineTo(x+Math.cos(ang)*len,y+Math.sin(ang)*len);c.stroke();
    }
    if(templateImage.complete&&templateImage.naturalWidth){
      c.globalCompositeOperation='screen';c.globalAlpha=.05+(state.glare/100)*.07;c.drawImage(templateImage,0,0,S,S);
    }
    c.restore();
  }

"""
    if marker not in s: raise SystemExit('drawNoise marker missing')
    s=s.replace(marker,fn+marker,1)
old='    drawDisc(c,S);\n    drawCase(c,S);\n    drawNoise(c,S);'
new='    drawDisc(c,S);\n    drawCase(c,S);\n    drawCaseRealism(c,S);\n    drawNoise(c,S);'
if old in s:s=s.replace(old,new,1)
elif 'drawCaseRealism(c,S);' not in s:raise SystemExit('render insertion missing')
p.write_text(s)
