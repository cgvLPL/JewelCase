from pathlib import Path

p = Path('index.html')
s = p.read_text()
old_draw = "const pos=state.stickerPos.barcode,x=S*(.745+pos.x),y=S*(.866+pos.y),w=S*.178,h=S*.070;"
new_draw = "const pos=state.stickerPos.barcode,x=S*(.760+pos.x),y=S*(.835+pos.y),w=S*.165,h=S*.065;"
old_box = "barcode:{x:.745,y:.866,w:.178,h:.070,enabled:'barcode'}"
new_box = "barcode:{x:.760,y:.835,w:.165,h:.065,enabled:'barcode'}"
if old_draw not in s or old_box not in s:
    raise SystemExit('Expected barcode geometry not found')
s = s.replace(old_draw, new_draw, 1)
s = s.replace(old_box, new_box, 1)
p.write_text(s)
