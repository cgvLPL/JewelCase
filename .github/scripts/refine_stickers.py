from pathlib import Path

p=Path('index.html')
s=p.read_text()

repls={
"const pos=state.stickerPos.barcode,x=S*(.770+pos.x),y=S*(.842+pos.y),w=S*.165,h=S*.074;":"const pos=state.stickerPos.barcode,x=S*(.745+pos.x),y=S*(.866+pos.y),w=S*.178,h=S*.070;",
"const pos=state.stickerPos.advisory,x=S*(.774+pos.x),y=S*(.756+pos.y),w=S*.158,h=S*.090;":"const pos=state.stickerPos.advisory,x=S*(.748+pos.x),y=S*(.770+pos.y),w=S*.160,h=S*.090;",
"const pos=state.stickerPos.price,x=S*(.795+pos.x),y=S*(.648+pos.y),w=S*.122,h=S*.061;":"const pos=state.stickerPos.price,x=S*(.802+pos.x),y=S*(.677+pos.y),w=S*.118,h=S*.060;",
"const pos=state.stickerPos.title,x=S*(.100+pos.x),y=S*(.852+pos.y),w=S*.345,h=S*.066;":"const pos=state.stickerPos.title,x=S*(.090+pos.x),y=S*(.875+pos.y),w=S*.330,h=S*.064;",
"title:{x:.100,y:.852,w:.345,h:.066,enabled:'titleSticker'},":"title:{x:.090,y:.875,w:.330,h:.064,enabled:'titleSticker'},",
"price:{x:.795,y:.648,w:.122,h:.061,enabled:'priceSticker'},":"price:{x:.802,y:.677,w:.118,h:.060,enabled:'priceSticker'},",
"advisory:{x:.774,y:.756,w:.158,h:.090,enabled:'advisory'},":"advisory:{x:.748,y:.770,w:.160,h:.090,enabled:'advisory'},",
"barcode:{x:.770,y:.842,w:.165,h:.074,enabled:'barcode'}":"barcode:{x:.745,y:.866,w:.178,h:.070,enabled:'barcode'}"
}
for a,b in repls.items():
    if a not in s: raise SystemExit(f'missing: {a}')
    s=s.replace(a,b,1)

# Keep the advisory renderer synchronized with its new default position.
s=s.replace("const pos=state.stickerPos.advisory,x=S*(.774+pos.x),y=S*(.756+pos.y),w=S*.158,h=S*.090;",
            "const pos=state.stickerPos.advisory,x=S*(.748+pos.x),y=S*(.770+pos.y),w=S*.160,h=S*.090;",1)

# Constrain dragged stickers to the visible jewel-case footprint instead of allowing them off-canvas.
old="p.x=Math.max(-.94,Math.min(.94,p.x+dx));p.y=Math.max(-.94,Math.min(.94,p.y+dy));"
new="const b=stickerBoxes[draggingSticker],margin=.035;\n      p.x=Math.max(margin-b.x,Math.min(1-margin-b.x-b.w,p.x+dx));\n      p.y=Math.max(margin-b.y,Math.min(1-margin-b.y-b.h,p.y+dy));"
if old in s:
    s=s.replace(old,new,1)

p.write_text(s)
