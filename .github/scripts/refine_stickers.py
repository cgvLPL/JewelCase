from pathlib import Path

p=Path('index.html')
s=p.read_text()

repls={
"const pos=state.stickerPos.barcode,x=S*(.790+pos.x),y=S*(.845+pos.y),w=S*.160,h=S*.076;":"const pos=state.stickerPos.barcode,x=S*(.770+pos.x),y=S*(.842+pos.y),w=S*.165,h=S*.074;",
"const pos=state.stickerPos.advisory,x=S*(.786+pos.x),y=S*(.748+pos.y),w=S*.152,h=S*.086;":"const pos=state.stickerPos.advisory,x=S*(.774+pos.x),y=S*(.756+pos.y),w=S*.158,h=S*.090;",
"const pos=state.stickerPos.price,x=S*(.815+pos.x),y=S*(.632+pos.y),w=S*.120,h=S*.063;":"const pos=state.stickerPos.price,x=S*(.795+pos.x),y=S*(.648+pos.y),w=S*.122,h=S*.061;",
"const pos=state.stickerPos.title,x=S*(.105+pos.x),y=S*(.866+pos.y),w=S*.340,h=S*.064;":"const pos=state.stickerPos.title,x=S*(.100+pos.x),y=S*(.852+pos.y),w=S*.345,h=S*.066;",
"title:{x:.105,y:.866,w:.340,h:.064,enabled:'titleSticker'},":"title:{x:.100,y:.852,w:.345,h:.066,enabled:'titleSticker'},",
"price:{x:.815,y:.632,w:.120,h:.063,enabled:'priceSticker'},":"price:{x:.795,y:.648,w:.122,h:.061,enabled:'priceSticker'},",
"advisory:{x:.786,y:.748,w:.152,h:.086,enabled:'advisory'},":"advisory:{x:.774,y:.756,w:.158,h:.090,enabled:'advisory'},",
"barcode:{x:.790,y:.845,w:.160,h:.076,enabled:'barcode'}":"barcode:{x:.770,y:.842,w:.165,h:.074,enabled:'barcode'}"
}
for a,b in repls.items():
    if a not in s: raise SystemExit(f'missing: {a}')
    s=s.replace(a,b,1)

start=s.index('  function drawAdvisory(c,S){')
end=s.index('\n  function drawPrice(c,S){',start)
new='''  function drawAdvisory(c,S){
    const pos=state.stickerPos.advisory,x=S*(.774+pos.x),y=S*(.756+pos.y),w=S*.158,h=S*.090;
    c.save();
    c.translate(x+w/2,y+h/2);
    c.rotate(-.012);

    // Thin paper/vinyl label sitting above the acrylic instead of a flat graphic.
    stickerShadow(c,S,.0048,.34,.0026);
    const paper=c.createLinearGradient(-w/2,-h/2,w/2,h/2);
    paper.addColorStop(0,'rgba(250,250,246,.995)');
    paper.addColorStop(.52,'rgba(239,239,234,.99)');
    paper.addColorStop(1,'rgba(248,248,243,.985)');
    c.fillStyle=paper;c.fillRect(-w/2,-h/2,w,h);
    c.shadowColor='transparent';

    // Slightly imperfect printed black border.
    c.strokeStyle='rgba(9,9,9,.96)';
    c.lineWidth=Math.max(1.5,S*.0025);
    c.strokeRect(-w*.472,-h*.445,w*.944,h*.89);
    c.strokeStyle='rgba(15,15,15,.36)';
    c.lineWidth=Math.max(.55,S*.00055);
    c.strokeRect(-w*.455,-h*.425,w*.91,h*.85);

    c.textAlign='center';c.textBaseline='middle';
    c.fillStyle='rgba(8,8,8,.98)';
    c.font=`900 ${S*.0148}px Arial Black,Impact,Arial,sans-serif`;
    c.fillText('PARENTAL',0,-h*.245);

    // Canonical heavy middle band with white reversed type.
    c.fillStyle='rgba(7,7,7,.985)';
    c.fillRect(-w*.432,-h*.082,w*.864,h*.285);
    c.fillStyle='rgba(250,250,248,.99)';
    c.font=`900 ${S*.0132}px Arial Black,Impact,Arial,sans-serif`;
    c.fillText('ADVISORY',0,h*.061);

    c.fillStyle='rgba(8,8,8,.98)';
    c.font=`900 ${S*.0090}px Arial Black,Arial,sans-serif`;
    c.fillText('EXPLICIT CONTENT',0,h*.330);

    // Registration/ink texture and tiny handling wear keep it from reading vector-clean.
    c.globalCompositeOperation='multiply';
    for(let i=0;i<42;i++){
      const px=-w*.44+seeded(9100+i)*w*.88;
      const py=-h*.41+seeded(9200+i)*h*.82;
      const rw=S*(.00016+seeded(9300+i)*.00034);
      c.fillStyle=`rgba(0,0,0,${.018+seeded(9400+i)*.032})`;
      c.fillRect(px,py,rw,rw*.45);
    }
    c.globalCompositeOperation='screen';
    c.fillStyle='rgba(255,255,255,.20)';
    c.fillRect(-w*.43,-h*.40,w*.72,S*.00075);

    // Slightly lifted lower-right edge / adhesive highlight.
    const peel=c.createLinearGradient(w*.25,h*.22,w*.48,h*.45);
    peel.addColorStop(0,'rgba(255,255,255,0)');
    peel.addColorStop(1,'rgba(255,255,255,.34)');
    c.fillStyle=peel;
    c.beginPath();c.moveTo(w*.28,h*.44);c.lineTo(w*.48,h*.44);c.lineTo(w*.48,h*.23);c.closePath();c.fill();
    c.restore();

    stickerPaperTexture(c,S,x,y,w,h,4100);
  }
'''
s=s[:start]+new+s[end:]
p.write_text(s)
